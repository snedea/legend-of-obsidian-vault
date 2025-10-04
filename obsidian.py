"""
Obsidian Vault Integration for Legend of the Obsidian Vault
Reads notes and converts them to forest enemies
"""
import os
import re
import random
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
from game_data import ObsidianNote, Enemy, FOREST_ENEMIES
from fantasy_translator import FantasyTranslator, translate_to_fantasy, get_fantasy_term

# Simple caching for performance
try:
    from simple_cache import (cache_enemy, get_cached_enemy, cache_narrative,
                             get_cached_narrative, make_content_hash,
                             cache_ai_result, get_cached_ai_result, periodic_maintenance)
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False

# Try to import AI functionality
try:
    from brainbot import sync_generate_enemy_description, is_ai_available
    AI_INTEGRATION_AVAILABLE = True
except ImportError:
    AI_INTEGRATION_AVAILABLE = False
    sync_generate_enemy_description = None
    is_ai_available = lambda: False

class ObsidianVault:
    """Interface to Obsidian vault"""

    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path) if vault_path else self.find_vault()
        self.notes_cache = {}
        self.last_scan = None
        self.fantasy_translator = FantasyTranslator()

    def find_vault(self) -> Optional[Path]:
        """Try to find Obsidian vault in common locations"""
        # Primary locations with .obsidian folders (official Obsidian vaults)
        primary_paths = [
            Path.home() / "Documents" / "Obsidian Vault",
            Path.home() / "Obsidian",
            Path.home() / "Notes",
            Path.home() / "vault",
            Path.home() / "Documents" / "Notes",
            Path.home() / "Desktop" / "Obsidian Vault",
            Path.home() / "Desktop" / "Notes",
            Path.home() / "iCloud Drive (Archive)" / "Documents" / "Obsidian",
            Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents",
        ]

        # Check iCloud Obsidian specifically (user's exact path)
        icloud_obsidian = Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents"
        if icloud_obsidian.exists():
            print(f"Found iCloud Obsidian folder: {icloud_obsidian}")
            # Look for vaults inside the iCloud Documents folder
            try:
                for item in icloud_obsidian.iterdir():
                    if item.is_dir():
                        print(f"Checking iCloud vault: {item}")
                        if (item / ".obsidian").exists():
                            print(f"Found iCloud Obsidian vault: {item}")
                            return item
                        # Even if no .obsidian, check for markdown files
                        elif self._has_markdown_files(item):
                            print(f"Found iCloud notes folder: {item}")
                            return item

                # If no subfolders with .obsidian, maybe the Documents folder itself is the vault
                if (icloud_obsidian / ".obsidian").exists():
                    print(f"iCloud Documents folder is the vault: {icloud_obsidian}")
                    return icloud_obsidian
                elif self._has_markdown_files(icloud_obsidian):
                    print(f"iCloud Documents has markdown files: {icloud_obsidian}")
                    return icloud_obsidian
            except PermissionError:
                print("Permission denied accessing iCloud folder")
                pass

        # Check for official Obsidian vaults first
        for path in primary_paths:
            if path.exists() and (path / ".obsidian").exists():
                print(f"Found Obsidian vault: {path}")
                return path

        # Look for any .obsidian folder in common directories
        search_dirs = [
            Path.home() / "Documents",
            Path.home() / "Desktop",
            Path.home(),
        ]

        for search_dir in search_dirs:
            if search_dir.exists():
                try:
                    for item in search_dir.iterdir():
                        if item.is_dir() and (item / ".obsidian").exists():
                            print(f"Found Obsidian vault: {item}")
                            return item
                except PermissionError:
                    continue

        # Fallback: Look for folders with multiple .md files (potential vaults)
        for search_dir in search_dirs:
            if search_dir.exists():
                try:
                    for item in search_dir.iterdir():
                        if item.is_dir() and self._has_markdown_files(item):
                            print(f"Found potential notes folder: {item}")
                            return item
                except PermissionError:
                    continue

        return None

    def _has_markdown_files(self, path: Path) -> bool:
        """Check if a directory has multiple markdown files"""
        try:
            md_files = list(path.glob("*.md"))
            return len(md_files) >= 3  # At least 3 markdown files
        except:
            return False

    def scan_notes(self, force_rescan: bool = False) -> List[ObsidianNote]:
        """Scan vault for markdown notes"""
        if not self.vault_path or not self.vault_path.exists():
            return []

        # Use cache if recent
        if not force_rescan and self.last_scan and self.notes_cache:
            if (datetime.now() - self.last_scan).seconds < 300:  # 5 minutes
                return list(self.notes_cache.values())

        notes = []
        for md_file in self.vault_path.rglob("*.md"):
            # Skip .icloud placeholder files
            if ".icloud" in md_file.name:
                continue

            # Skip template folders
            if "template" in str(md_file).lower():
                continue

            try:
                note = self._parse_note(md_file)
                if note:
                    notes.append(note)
                    self.notes_cache[str(md_file)] = note
            except Exception as e:
                # Skip problematic files
                continue

        self.last_scan = datetime.now()
        return notes

    def _parse_note(self, file_path: Path) -> Optional[ObsidianNote]:
        """Parse a markdown note"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip empty files
            if not content.strip():
                return None

            stat = file_path.stat()
            created = datetime.fromtimestamp(stat.st_ctime)
            modified = datetime.fromtimestamp(stat.st_mtime)

            # Extract title (first heading or filename)
            title = self._extract_title(content, file_path.stem)

            # Extract tags
            tags = self._extract_tags(content)

            return ObsidianNote(
                path=file_path,
                title=title,
                content=content,
                created=created,
                modified=modified,
                tags=tags
            )
        except Exception:
            return None

    def _extract_title(self, content: str, fallback: str) -> str:
        """Extract title from content or use filename"""
        # Look for first heading
        heading_match = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            return heading_match.group(1).strip()

        # Look for YAML frontmatter title
        yaml_match = re.search(r'^---\n.*?title:\s*([^\n]+).*?^---', content, re.MULTILINE | re.DOTALL)
        if yaml_match:
            return yaml_match.group(1).strip().strip('"\'')

        return fallback

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content"""
        tags = []

        # YAML frontmatter tags
        yaml_match = re.search(r'^---\n.*?tags:\s*\[(.*?)\].*?^---', content, re.MULTILINE | re.DOTALL)
        if yaml_match:
            yaml_tags = [tag.strip().strip('"\'') for tag in yaml_match.group(1).split(',')]
            tags.extend(yaml_tags)

        # Inline tags (#tag)
        inline_tags = re.findall(r'#(\w+)', content)
        tags.extend(inline_tags)

        return list(set(tags))  # Remove duplicates

    def get_enemy_for_level(self, level: int, notes: List[ObsidianNote] = None) -> Enemy:
        """Generate enemy for player level using Obsidian notes"""
        if notes is None:
            notes = self.scan_notes()

        # Get base enemy stats for this level
        if level in FOREST_ENEMIES:
            base_enemies = FOREST_ENEMIES[level]
        else:
            # Use highest level enemies if beyond level 12
            base_enemies = FOREST_ENEMIES[12]

        base_enemy = random.choice(base_enemies)

        if notes:
            # Use note-based enemy - select from all notes regardless of difficulty
            # Difficulty affects stats scaling, not availability
            note = random.choice(notes)

            # Check cache first
            cached_enemy = None
            if CACHE_AVAILABLE:
                cached_enemy = get_cached_enemy(note.title, level)
                if cached_enemy:
                    print(f"🗄️  Using cached enemy for '{note.title}'")
                    return cached_enemy

            # Try AI-enhanced enemy generation first
            enemy_lore = self._generate_ai_enhanced_enemy(note, base_enemy[0])
            if enemy_lore is None:
                # Fallback to basic generation with enhanced narratives
                enemy_name = self._generate_enemy_name(note, base_enemy[0])
                enemy_lore = self._generate_enemy_lore(note, base_enemy[0])
            else:
                # Use AI-generated name and lore
                enemy_name = enemy_lore.get('name', self._generate_enemy_name(note, base_enemy[0]))

            # Scale stats based on note difficulty vs player level
            difficulty_multiplier = min(1.5, max(0.8, note.difficulty_level / level))

            enemy = Enemy(
                name=enemy_name,
                hitpoints=int(base_enemy[1] * difficulty_multiplier),
                attack=int(base_enemy[2] * difficulty_multiplier),
                gold_reward=base_enemy[3],
                exp_reward=base_enemy[3] // 2,
                level=level,
                note_content=note.content[:500],  # Truncate for performance
                note_title=note.title,

                # Enhanced lore fields
                backstory=enemy_lore['backstory'],
                personality_type=enemy_lore['personality_type'],
                knowledge_domain=enemy_lore['knowledge_domain'],
                age_descriptor=enemy_lore['age_descriptor'],
                folder_theme=enemy_lore['folder_theme'],
                combat_phrases=enemy_lore['combat_phrases'],
                defeat_message=enemy_lore['defeat_message'],
                victory_message=enemy_lore['victory_message'],

                # LORD-style fields
                description=enemy_lore.get('description', ''),
                weapon=enemy_lore.get('weapon', ''),
                armor=enemy_lore.get('armor', ''),

                # Rich narrative fields
                encounter_narrative=enemy_lore.get('encounter_narrative', ''),
                environment_description=enemy_lore.get('environment_description', ''),
                manifestation_story=enemy_lore.get('manifestation_story', '')
            )

            # Cache the generated enemy
            if CACHE_AVAILABLE:
                cache_enemy(note.title, level, enemy)

            return enemy
        else:
            # Fallback to standard enemy if no notes available
            return Enemy(
                name=base_enemy[0],
                hitpoints=base_enemy[1],
                attack=base_enemy[2],
                gold_reward=base_enemy[3],
                exp_reward=base_enemy[3] // 2,
                level=level
            )

    def _generate_enemy_name(self, note: ObsidianNote, base_enemy: str) -> str:
        """Generate fantasy enemy name with rich lore integration"""
        return self._generate_fantasy_name(note, base_enemy)

    def _generate_fantasy_name(self, note: ObsidianNote, base_enemy: str) -> str:
        """Create immersive fantasy names based on note content and metadata"""

        # Fantasy name components
        MYSTICAL_PREFIXES = [
            "Shadow", "Crimson", "Ancient", "Forgotten", "Whisper", "Ethereal",
            "Obsidian", "Gilded", "Spectral", "Temporal", "Void", "Crystal"
        ]

        FANTASY_TITLES = [
            "Keeper", "Guardian", "Weaver", "Lord", "Wraith", "Sage", "Oracle",
            "Curator", "Archivist", "Scribe", "Chronicler", "Sentinel", "Warden"
        ]

        # Map note characteristics to mystical themes
        knowledge_domain = self._analyze_knowledge_domain(note)
        age_descriptor = self._get_age_descriptor(note.age_days)
        folder_theme = self._get_folder_theme(note.path.parent.name.lower())

        # Generate fantasy base creature
        fantasy_creature = self._transform_creature_name(base_enemy, knowledge_domain)

        # Create name variations based on different patterns
        name_patterns = [
            # Pattern 1: [Prefix] [Creature], [Title] of [Domain]
            f"{random.choice(MYSTICAL_PREFIXES)} {fantasy_creature}, {random.choice(FANTASY_TITLES)} of {knowledge_domain}",

            # Pattern 2: [Creature] the [Age] [Title]
            f"{fantasy_creature} the {age_descriptor} {random.choice(FANTASY_TITLES)}",

            # Pattern 3: [Title] [Name] of [Folder Theme]
            f"{random.choice(FANTASY_TITLES)} {self._generate_mystical_name()} of {folder_theme}",

            # Pattern 4: The [Age] [Creature] of [Domain]
            f"The {age_descriptor} {fantasy_creature} of {knowledge_domain}",

            # Pattern 5: [Mystical Name], [Title] of [Theme]
            f"{self._generate_mystical_name()}, {random.choice(FANTASY_TITLES)} of {knowledge_domain}",
        ]

        # Select and refine the name
        name = random.choice(name_patterns)

        # Ensure name fits display constraints (40 chars)
        if len(name) > 40:
            # Try shorter variations
            short_patterns = [
                f"{fantasy_creature} the {age_descriptor}",
                f"{random.choice(FANTASY_TITLES)} {self._generate_mystical_name()}",
                f"The {knowledge_domain} {random.choice(FANTASY_TITLES)}",
                f"{random.choice(MYSTICAL_PREFIXES)} {fantasy_creature}",
            ]
            name = random.choice(short_patterns)

            # Final truncation if still too long
            if len(name) > 40:
                name = name[:37] + "..."

        return name

    def _generate_ai_enhanced_enemy(self, note: ObsidianNote, base_enemy: str) -> Optional[Dict]:
        """Generate enemy using AI when available"""
        if not AI_INTEGRATION_AVAILABLE:
            print(f"🚫 AI_INTEGRATION_AVAILABLE = False")
            return None

        # Try waiting briefly for AI initialization
        if not is_ai_available(wait_timeout=2.0):
            print(f"🚫 AI not available for {note.title} - using fallback generation")
            return None


        try:
            # Random content sampling for large notes
            content_sample = self._get_random_content_sample(note.content)

            # Use AI to generate enhanced enemy description
            ai_description = sync_generate_enemy_description(
                note.title,
                content_sample,
                base_enemy
            )

            if ai_description:
                return {
                    'name': ai_description.name,
                    'description': ai_description.description,
                    'weapon': ai_description.weapon,
                    'armor': ai_description.armor,
                    'backstory': ai_description.backstory,
                    'personality_type': f"LORD-style {base_enemy}",
                    'knowledge_domain': f"Guardian of: {note.title}",
                    'age_descriptor': self._get_age_descriptor(note.age_days),
                    'folder_theme': f"Your {note.path.parent.name} Notes",
                    'combat_phrases': ai_description.combat_phrases,
                    'defeat_message': ai_description.defeat_message,
                    'victory_message': ai_description.victory_message,
                    'recommended_hp': ai_description.recommended_hp,
                    'recommended_attack': ai_description.recommended_attack,
                    # New narrative fields
                    'encounter_narrative': ai_description.encounter_narrative,
                    'environment_description': ai_description.environment_description,
                    'manifestation_story': ai_description.manifestation_story
                }
        except Exception as e:
            print(f"AI enemy generation failed: {e}")

        return None

    def _get_random_content_sample(self, content: str, max_length: int = 800) -> str:
        """Get a random sample from note content for variety"""
        if len(content) <= max_length:
            return content

        # For large notes, take a random chunk
        start_pos = random.randint(0, max(0, len(content) - max_length))
        sample = content[start_pos:start_pos + max_length]

        # Try to start at a sentence boundary if possible
        sentences = sample.split('. ')
        if len(sentences) > 1:
            # Skip the first partial sentence and take the rest
            sample = '. '.join(sentences[1:])

        return sample

    def _generate_ai_enhanced_name(self, note: ObsidianNote, base_enemy: str, ai_description) -> str:
        """Generate a clear, note-based enemy name"""
        # Create names that clearly show what note they're from
        note_title_clean = note.title.replace('_', ' ').replace('-', ' ').title()

        # Different name patterns based on note characteristics
        patterns = [
            f"Guardian of '{note_title_clean}'",
            f"Keeper of {note_title_clean}",
            f"{base_enemy} protecting '{note_title_clean}'",
            f"The {note_title_clean} Sentinel",
            f"Protector of your {note_title_clean} knowledge"
        ]

        chosen_name = random.choice(patterns)

        # Ensure name isn't too long (40 chars max)
        if len(chosen_name) > 40:
            chosen_name = f"Guardian of '{note_title_clean[:20]}...'"

        return chosen_name

    def _analyze_knowledge_domain(self, note: ObsidianNote) -> str:
        """Analyze note content to determine mystical knowledge domain"""
        content_lower = (note.title + " " + note.content[:200]).lower()

        # Technical domains
        if any(term in content_lower for term in ['python', 'javascript', 'code', 'function', 'class']):
            return random.choice(["Code Mysteries", "Arcane Scripts", "Digital Codex", "Silicon Scriptures"])
        elif any(term in content_lower for term in ['project', 'todo', 'task', 'goal']):
            return random.choice(["Project Forge", "Creation Sanctum", "Builder's Archive", "Craft Chambers"])
        elif any(term in content_lower for term in ['meeting', 'discussion', 'team', 'call']):
            return random.choice(["Council Echoes", "Assembly Whispers", "Gathering Lore", "Conclave Records"])
        elif any(term in content_lower for term in ['personal', 'diary', 'thought', 'reflection']):
            return random.choice(["Memory Fragments", "Soul Whispers", "Inner Sanctum", "Thought Streams"])
        elif any(term in content_lower for term in ['documentation', 'guide', 'manual', 'readme']):
            return random.choice(["Ancient Tomes", "Wisdom Scrolls", "Knowledge Vaults", "Sacred Manuals"])
        elif any(term in content_lower for term in ['idea', 'concept', 'theory', 'research']):
            return random.choice(["Concept Realms", "Theory Planes", "Research Depths", "Innovation Chambers"])
        else:
            return random.choice(["Forgotten Lore", "Hidden Knowledge", "Mysterious Wisdom", "Secret Archives"])

    def _get_age_descriptor(self, age_days: int) -> str:
        """Get age-based mystical descriptor"""
        if age_days < 7:
            return random.choice(["Awakened", "Fresh", "Newly Bound", "Recently Risen"])
        elif age_days < 30:
            return random.choice(["Restless", "Active", "Stirring", "Vigilant"])
        elif age_days < 90:
            return random.choice(["Slumbering", "Dormant", "Weathered", "Seasoned"])
        elif age_days < 365:
            return random.choice(["Ancient", "Time-worn", "Aged", "Venerable"])
        else:
            return random.choice(["Primordial", "Forgotten", "Eternal", "Timeless"])

    def _get_folder_theme(self, folder_name: str) -> str:
        """Convert folder names to mystical themes"""
        folder_themes = {
            'personal': "Inner Sanctum",
            'work': "Labor Forges",
            'projects': "Creation Labs",
            'notes': "Thought Realms",
            'docs': "Archive Halls",
            'documentation': "Scroll Chambers",
            'meetings': "Council Rooms",
            'ideas': "Vision Plains",
            'research': "Study Depths",
            'code': "Script Vaults",
            'drafts': "Prototype Realms",
            'archive': "Ancient Vaults",
            'temp': "Ethereal Spaces",
            'backup': "Shadow Mirrors"
        }

        # Check for partial matches
        for key, theme in folder_themes.items():
            if key in folder_name:
                return theme

        # Default mystical transformation
        return f"{folder_name.title()} Realms"

    def _transform_creature_name(self, base_enemy: str, domain: str) -> str:
        """Transform basic enemy into fantasy creature"""
        creature_transformations = {
            'mosquito': ['Bloodmite', 'Crimson Wisp', 'Memory Gnat', 'Data Midge'],
            'rat': ['Shadow Scurrier', 'Archive Rat', 'Scroll Gnawer', 'Byte Rodent'],
            'spider': ['Web Weaver', 'Code Spider', 'Network Arachnid', 'Thread Spinner'],
            'snake': ['Code Serpent', 'Logic Viper', 'Syntax Snake', 'Digital Asp'],
            'bat': ['Night Flitter', 'Echo Bat', 'Shadow Wing', 'Cave Dweller'],
            'wolf': ['Pack Hunter', 'Shadow Wolf', 'Lone Stalker', 'Wild Guardian'],
            'bear': ['Forest Guardian', 'Cave Protector', 'Mighty Defender', 'Strength Bearer'],
            'skeleton': ['Bone Guardian', 'Undead Sentinel', 'Death Warden', 'Marrow Keeper'],
            'goblin': ['Mischief Maker', 'Trouble Sprite', 'Chaos Imp', 'Disorder Goblin'],
            'troll': ['Stone Troll', 'Bridge Guardian', 'Mountain Keeper', 'Rock Defender']
        }

        base_lower = base_enemy.lower()
        for creature, transforms in creature_transformations.items():
            if creature in base_lower:
                return random.choice(transforms)

        # Default transformation - add mystical descriptor
        mystical_descriptors = ['Ethereal', 'Shadow', 'Mystic', 'Spectral', 'Void', 'Crystal']
        return f"{random.choice(mystical_descriptors)} {base_enemy}"

    def _generate_mystical_name(self) -> str:
        """Generate fantasy character names"""
        prefixes = ['Vex', 'Zar', 'Mor', 'Kael', 'Thane', 'Nyx', 'Vel', 'Drak', 'Syl', 'Kor']
        middle_parts = ['tha', 'lor', 'ven', 'dor', 'mir', 'goth', 'ran', 'tek', 'phi', 'on']
        suffixes = ['ra', 'us', 'el', 'an', 'is', 'ara', 'oth', 'iel', 'ash', 'ex']

        # Occasionally use single names, usually compound
        if random.random() < 0.3:
            return random.choice(prefixes) + random.choice(suffixes)
        else:
            return random.choice(prefixes) + "'" + random.choice(middle_parts) + random.choice(suffixes)

    def _generate_enemy_lore(self, note: ObsidianNote, base_enemy: str) -> dict:
        """Generate comprehensive enemy lore including backstory and personality"""

        # Analyze note characteristics
        knowledge_domain = self._analyze_knowledge_domain(note)
        age_descriptor = self._get_age_descriptor(note.age_days)
        folder_theme = self._get_folder_theme(note.path.parent.name.lower())
        personality_type = self._determine_personality_type(note, knowledge_domain)

        # Generate backstory based on note content and characteristics
        backstory = self._create_backstory(note, base_enemy, knowledge_domain, age_descriptor)

        # Generate combat phrases
        combat_phrases = self._generate_combat_phrases(note, personality_type, knowledge_domain)

        # Generate defeat and victory messages
        defeat_message = self._generate_defeat_message(note, personality_type)
        victory_message = self._generate_victory_message(note, personality_type)

        # Generate rich narrative fields for fallback generation
        encounter_narrative = self._generate_dynamic_encounter_narrative(note, knowledge_domain, age_descriptor)
        environment_description = self._generate_dynamic_environment(note, folder_theme)
        manifestation_story = self._generate_manifestation_story(note, personality_type)

        return {
            'backstory': backstory,
            'personality_type': personality_type,
            'knowledge_domain': knowledge_domain,
            'age_descriptor': age_descriptor,
            'folder_theme': folder_theme,
            'combat_phrases': combat_phrases,
            'defeat_message': defeat_message,
            'victory_message': victory_message,
            # Rich narrative fields for magical encounters
            'encounter_narrative': encounter_narrative,
            'environment_description': environment_description,
            'manifestation_story': manifestation_story,
            'description': self._generate_dynamic_description(note, personality_type),
            'weapon': self._generate_dynamic_weapon(note, knowledge_domain),
            'armor': self._generate_dynamic_armor(note, age_descriptor)
        }

    def _determine_personality_type(self, note: ObsidianNote, knowledge_domain: str) -> str:
        """Determine enemy personality based on note characteristics"""
        content_lower = (note.title + " " + note.content[:200]).lower()

        # Personality mapping based on content and age
        if note.age_days > 365:
            # Ancient knowledge - wise but possibly outdated
            return random.choice(["Ancient Scholar", "Forgotten Sage", "Time-worn Guardian", "Eternal Keeper"])

        elif any(term in content_lower for term in ['error', 'bug', 'problem', 'issue', 'fix']):
            # Problem-focused content - aggressive protector
            return random.choice(["Defensive Warrior", "Problem Guardian", "Chaos Sentinel", "Error Wraith"])

        elif any(term in content_lower for term in ['idea', 'concept', 'theory', 'research']):
            # Theoretical content - intellectual guardian
            return random.choice(["Thoughtful Oracle", "Concept Keeper", "Theory Weaver", "Idea Curator"])

        elif any(term in content_lower for term in ['personal', 'feeling', 'emotion', 'thought']):
            # Personal content - emotional guardian
            return random.choice(["Memory Keeper", "Emotion Guardian", "Soul Protector", "Heart Sentinel"])

        elif any(term in content_lower for term in ['project', 'task', 'todo', 'goal']):
            # Project content - dutiful guardian
            return random.choice(["Task Master", "Project Sentinel", "Goal Guardian", "Duty Keeper"])

        else:
            # General knowledge guardian
            return random.choice(["Knowledge Warden", "Wisdom Keeper", "Archive Guardian", "Lore Protector"])

    def _create_backstory(self, note: ObsidianNote, base_enemy: str, knowledge_domain: str, age_descriptor: str) -> str:
        """Create a 2-3 sentence backstory explaining why this enemy guards this knowledge"""

        # Use fantasy translator to convert key concepts
        # Extract key words from title
        title_words = note.title.replace('_', ' ').split()
        main_concept = ' '.join(title_words[:2])  # Use first 2 words as main concept

        # Get fantasy terms for key concepts
        fantasy_concept = get_fantasy_term(main_concept)
        fantasy_title = translate_to_fantasy(note.title)

        # If no good translation, create a mystical version
        if fantasy_title == note.title or len(fantasy_title) > len(note.title) + 20:
            fantasy_title = f"the Sacred {note.title.replace('_', ' ').title()}"

        # Backstory templates using fantasy translations
        backstory_templates = [
            f"Once a humble seeker of knowledge, this {age_descriptor.lower()} guardian was bound to protect {fantasy_title}. "
            f"Years of contemplating the mysteries of {fantasy_concept} have transformed it into a fierce protector of this sacred wisdom. "
            f"It will not yield this knowledge to those who cannot prove their understanding.",

            f"Born from the essence of forgotten learning, this spirit has watched over {fantasy_title} since its creation. "
            f"The mystical energies of {knowledge_domain} flow through its ethereal form, making it both teacher and examiner. "
            f"Only those who demonstrate true comprehension may pass.",

            f"This {age_descriptor.lower()} entity emerged when the wisdom within {fantasy_title} reached critical importance. "
            f"Charged with preserving the integrity of {fantasy_concept}, it tests all who would access this power. "
            f"Its duty is eternal, its purpose unwavering.",

            f"Long ago, a scholar's deep meditation on {fantasy_title} created this mystical guardian. "
            f"Infused with the power of ancient {knowledge_domain}, it exists between thought and reality. "
            f"It challenges seekers to prove they are worthy of the sacred arts of {fantasy_concept}.",
        ]

        return random.choice(backstory_templates)

    def _generate_combat_phrases(self, note: ObsidianNote, personality_type: str, knowledge_domain: str) -> List[str]:
        """Generate 3-5 combat phrases the enemy might say during battle"""

        # Get fantasy translation of key concepts
        title_words = note.title.replace('_', ' ').split()
        main_concept = ' '.join(title_words[:2])
        fantasy_concept = get_fantasy_term(main_concept)
        fantasy_title = translate_to_fantasy(note.title)
        if fantasy_title == note.title or len(fantasy_title) > len(note.title) + 20:
            fantasy_title = f"the Sacred {note.title.replace('_', ' ').title()}"

        # Phrases based on personality type with fantasy translations
        phrase_sets = {
            "Ancient Scholar": [
                f"You dare challenge the wisdom of ages?",
                f"This knowledge was old when the world was young!",
                f"Feel the weight of accumulated learning!",
                f"Your understanding of {fantasy_concept} is but a flickering candle!",
                f"The ancient secrets of {fantasy_title} are beyond your grasp!"
            ],
            "Defensive Warrior": [
                f"I will not let you corrupt this knowledge!",
                f"Stand back! The power of {fantasy_title} is protected!",
                f"You must prove yourself worthy!",
                f"Guard yourself against the mystical arts of {fantasy_concept}!",
                f"These sacred arts are not for the unworthy!"
            ],
            "Thoughtful Oracle": [
                f"Do you comprehend the depths of {fantasy_title}?",
                f"Your mind must expand to contain this wisdom!",
                f"Think carefully before you proceed!",
                f"The mysteries of {fantasy_concept} require true understanding!",
                f"Can you unravel these arcane secrets?"
            ],
            "Memory Keeper": [
                f"These memories are precious beyond measure!",
                f"I guard the echoes of important thoughts!",
                f"Your mind cannot hold what you have not earned!",
                f"Feel the weight of preserved {fantasy_concept}!",
                f"The sacred memories of {fantasy_title} shall not be disturbed!"
            ],
            "Task Master": [
                f"Have you completed the necessary preparations?",
                f"This knowledge requires discipline to understand!",
                f"Organization and method are required here!",
                f"You must prove your mastery of {fantasy_concept}!",
                f"The disciplines of {fantasy_title} demand perfection!"
            ]
        }

        # Default phrases with fantasy concepts if personality not found
        default_phrases = [
            f"You seek the secrets of {knowledge_domain}?",
            f"This knowledge is not for the unprepared!",
            f"Prove your worth, seeker!",
            f"The wisdom of {fantasy_title} is mine to protect!",
            f"The mystical arts of {fantasy_concept} require true dedication!"
        ]

        # Get appropriate phrases or use defaults
        phrases = phrase_sets.get(personality_type, default_phrases)
        return random.sample(phrases, min(3, len(phrases)))

    def _generate_defeat_message(self, note: ObsidianNote, personality_type: str) -> str:
        """Generate message when enemy is defeated"""

        # Get fantasy translation of the note title
        fantasy_title = translate_to_fantasy(note.title)
        if fantasy_title == note.title or len(fantasy_title) > len(note.title) + 20:
            fantasy_title = f"the Sacred {note.title.replace('_', ' ').title()}"

        defeat_messages = {
            "Ancient Scholar": f"Your wisdom... exceeds my expectations. The ancient knowledge of {fantasy_title} is yours to bear...",
            "Defensive Warrior": f"You have proven your strength worthy of this power. Guard {fantasy_title} well...",
            "Thoughtful Oracle": f"Your understanding runs deep. Take these mystical insights and use them wisely...",
            "Memory Keeper": f"You have shown respect for these precious memories. Carry {fantasy_title} in your heart...",
            "Task Master": f"Your dedication has been proven. The disciplined arts of {fantasy_title} are earned...",
        }

        return defeat_messages.get(personality_type,
            f"You have bested me, seeker. The wisdom of {fantasy_title} is yours...")

    def _generate_victory_message(self, note: ObsidianNote, personality_type: str) -> str:
        """Generate message when enemy defeats the player"""

        # Get fantasy translation of the note title
        fantasy_title = translate_to_fantasy(note.title)
        if fantasy_title == note.title or len(fantasy_title) > len(note.title) + 20:
            fantasy_title = f"the Sacred {note.title.replace('_', ' ').title()}"

        victory_messages = {
            "Ancient Scholar": f"Your mind was not ready for such ancient wisdom. Return when you have learned more...",
            "Defensive Warrior": f"You were not strong enough to claim this power. Train harder and return...",
            "Thoughtful Oracle": f"Your understanding needs more time to develop. Reflect and try again...",
            "Memory Keeper": f"These memories are too precious for an unprepared mind. Come back when ready...",
            "Task Master": f"You lack the discipline required. Complete your preparations and return...",
        }

        return victory_messages.get(personality_type,
            f"You are not yet worthy of the mystical knowledge within {fantasy_title}. Return when you are stronger...")

    def generate_quiz_question(self, note: ObsidianNote) -> Tuple[str, str]:
        """Generate a quiz question from note content with fantasy narrative framing"""

        # Get fantasy translations for mystical framing
        fantasy_title = translate_to_fantasy(note.title)
        if fantasy_title == note.title or len(fantasy_title) > len(note.title) + 20:
            fantasy_title = f"the Sacred {note.title.replace('_', ' ').title()}"

        # Extract key concept for riddle framing
        title_words = note.title.replace('_', ' ').split()
        main_concept = ' '.join(title_words[:2])
        fantasy_concept = get_fantasy_term(main_concept)

        try:
            # Try AI-enhanced quiz generation first
            from brainbot import sync_generate_quiz_question, is_ai_available

            if is_ai_available():
                base_question, base_answer = sync_generate_quiz_question(note.title, note.content)

                # Enhance AI-generated question with mystical framing
                riddle_question = self._frame_as_riddle(base_question, fantasy_title, fantasy_concept)
                return riddle_question, base_answer

        except ImportError:
            pass
        except Exception as e:
            print(f"AI quiz generation failed: {e}")

        # Fallback to regex-based generation with mystical framing
        content = note.content.lower()

        # Try to find definition patterns
        definition_match = re.search(r'(.+?)\s+is\s+(.+?)[\.\n]', content)
        if definition_match:
            concept = definition_match.group(1).strip()
            definition = definition_match.group(2).strip()
            riddle = f"The guardian whispers: 'To unlock {fantasy_title}, tell me the nature of {concept}...'"
            return riddle, definition[:50]

        # Try to find list items
        list_match = re.search(r'[-\*]\s+(.+)', content)
        if list_match:
            item = list_match.group(1).strip()
            riddle = f"Speak the secret related to {fantasy_title} that begins this ancient list..."
            return riddle, item[:50]

        # Extract first sentence
        first_sentence = re.search(r'^([^\.!?]+[\.!?])', content.strip())
        if first_sentence:
            sentence = first_sentence.group(1).strip()
            if len(sentence) < 100:
                riddle = f"Complete this mystical inscription about {fantasy_concept}: '{sentence[:50]}...'"
                return riddle, sentence[50:100]

        # Mystical fallback questions
        mystical_fallbacks = [
            (f"The guardian asks: 'What realm of knowledge does {fantasy_title} belong to?'", "knowledge"),
            (f"'When did your mind last touch upon {fantasy_title}?' the spirit inquires...", "recently"),
            (f"'Why do seekers value the wisdom of {fantasy_concept}?' echoes through the chamber...", "learning"),
            (f"The ancient voice asks: 'What power lies within {fantasy_title}?'", "understanding"),
            (f"'Speak the essence of {fantasy_concept},' demands the mystical guardian...", "wisdom"),
        ]

        return random.choice(mystical_fallbacks)

    def _frame_as_riddle(self, base_question: str, fantasy_title: str, fantasy_concept: str) -> str:
        """Transform a regular question into a mystical riddle"""

        riddle_frames = [
            f"The guardian of {fantasy_title} poses this riddle: '{base_question}'",
            f"To unlock the secrets of {fantasy_concept}, answer this: '{base_question}'",
            f"The ancient voice whispers: '{base_question}'",
            f"The mystical keeper asks: '{base_question}'",
            f"Before you may claim {fantasy_title}, solve this enigma: '{base_question}'",
            f"The spirit guardian challenges you: '{base_question}'",
            f"To prove your worthiness of {fantasy_concept}, answer: '{base_question}'",
        ]

        return random.choice(riddle_frames)

    def _extract_note_details(self, note: ObsidianNote) -> Dict[str, Any]:
        """Extract meaningful details from note content for narrative use"""
        content = note.content.strip()
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        details = {
            'first_line': lines[0] if lines else '',
            'key_phrases': [],
            'numbers': [],
            'items': [],
            'actions': [],
            'names': []
        }

        # Extract numbers
        import re
        numbers = re.findall(r'\b\d+\b', content)
        details['numbers'] = [int(n) for n in numbers[:5]]  # Limit to 5 numbers

        # Extract items/things (nouns)
        content_lower = content.lower()

        # Look for lists and bullet points
        list_items = re.findall(r'[-*•]\s*([^\n]+)', content)
        details['items'].extend([item.strip() for item in list_items[:3]])

        # Look for key phrases (capitalize important words)
        key_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        details['names'].extend(key_words[:3])

        # Extract actions/verbs
        action_patterns = [
            r'\b(configure|setup|install|create|build|deploy|execute|run|implement|design)\b',
            r'\b(meeting|discussion|review|planning|analysis|testing)\b'
        ]
        for pattern in action_patterns:
            actions = re.findall(pattern, content_lower)
            details['actions'].extend(actions[:2])

        # Extract quoted or important text
        quoted = re.findall(r'"([^"]+)"', content)
        details['key_phrases'].extend(quoted[:2])

        return details

    def _generate_dynamic_encounter_narrative(self, note: ObsidianNote, knowledge_domain: str, age_descriptor: str) -> str:
        """Generate dynamic encounter narrative based on note content"""
        content_lower = (note.title + " " + note.content[:300]).lower()
        fantasy_title = translate_to_fantasy(note.title)
        if fantasy_title == note.title or len(fantasy_title) > len(note.title) + 20:
            fantasy_title = f"the Sacred {note.title.replace('_', ' ').title()}"

        # Extract specific details from the note
        details = self._extract_note_details(note)

        # Create rich, content-based narratives
        def build_narrative_with_details(base_narrative: str) -> str:
            """Add specific note details to base narrative"""
            additions = []

            if details['first_line']:
                additions.append(f"The ancient inscription reads: '{details['first_line'][:50]}...'")

            if details['numbers']:
                num_desc = ', '.join(str(n) for n in details['numbers'][:3])
                additions.append(f"Mystical energies resonate with the sacred numbers: {num_desc}.")

            if details['items']:
                item_desc = ', '.join(f"'{item}'" for item in details['items'][:2])
                additions.append(f"Ethereal manifestations of {item_desc} float through the arcane space.")

            if details['names']:
                name_desc = ', '.join(details['names'][:2])
                additions.append(f"The names {name_desc} echo with power in this mystical realm.")

            # Combine base narrative with specific details
            full_narrative = base_narrative
            if additions:
                full_narrative += " " + " ".join(additions[:2])  # Limit to avoid too long

            return full_narrative

        # Content-aware narrative generation with specific details
        if any(word in content_lower for word in ['code', 'function', 'algorithm', 'programming', 'script']):
            base_narratives = [
                f"You enter a digital realm where the code from {fantasy_title} has manifested as living algorithms. The very essence of programming logic pulses through the ethereal space, transforming abstract concepts into tangible magical forces.",
                f"The Sanctuary of Digital Mysteries materializes around you, where {fantasy_title} has become a living testament to computational power. Lines of code float like glowing runes, each symbol containing the accumulated wisdom of countless hours of development.",
                f"You find yourself in the Codex Chamber, where {fantasy_title} exists as pure algorithmic energy. The air crackles with the power of executed functions and living variables, creating a symphony of digital magic."
            ]
            base = random.choice(base_narratives)
            narratives = [build_narrative_with_details(base)]
        elif any(word in content_lower for word in ['meeting', 'agenda', 'discussion', 'deadline', 'project']):
            base_narratives = [
                f"You enter the Ethereal Conference Chamber, where {fantasy_title} has become a living manifestation of endless deliberation. The very air vibrates with the energy of unfinished business and spectral agendas.",
                f"The Phantom Boardroom materializes around you, infused with the essence of {fantasy_title}. Transparent figures forever debate around an endless table, their words echoing through dimensions of corporate purgatory.",
                f"You step into the Halls of Eternal Meetings, where {fantasy_title} exists as a testament to bureaucratic persistence. Time seems suspended in this realm of perpetual planning and endless discussion."
            ]
            base = random.choice(base_narratives)
            narratives = [build_narrative_with_details(base)]
        elif any(word in content_lower for word in ['buy', 'shop', 'purchase', 'item', 'list', 'grocery']):
            narratives = [
                f"You enter the Merchant's Eternal Bazaar, where the desires from {fantasy_title} have manifested as ghostly commerce. Items float endlessly, never to be purchased.",
                f"The mystical marketplace appears before you, where {fantasy_title} has become a living catalog of unfulfilled desires. Spectral goods drift through the air.",
                f"You find yourself in the Bazaar of Lost Wants, where {fantasy_title} exists as a testament to consumer longing that transcends the physical realm."
            ]
        elif any(word in content_lower for word in ['password', 'login', 'auth', 'secret', 'key']):
            narratives = [
                f"You approach the Vault of Hidden Secrets, where {fantasy_title} guards the most precious mysteries. The air shimmers with protective enchantments.",
                f"The Chamber of Forbidden Knowledge materializes around you. {fantasy_title} has become a living guardian of secrets that mortals should not possess.",
                f"You enter the Sanctum of Veiled Truths, where {fantasy_title} stands as an eternal sentinel protecting knowledge from unworthy eyes."
            ]
        elif any(word in content_lower for word in ['recipe', 'cook', 'ingredient', 'food', 'meal']):
            narratives = [
                f"You enter a mystical kitchen where the essence of {fantasy_title} lingers in the air. Spectral ingredients dance around ancient parchment.",
                f"The Culinary Realm opens before you, where {fantasy_title} has become a living cookbook. Aromatic spirits swirl around phantom cooking implements.",
                f"You find yourself in the Kitchen of Eternal Preparation, where {fantasy_title} exists as a never-ending feast that can never be consumed."
            ]
        elif any(word in content_lower for word in ['ip', 'address', 'network', 'router', 'server']):
            narratives = [
                f"You traverse the ethereal pathways of the Network Dimension, where {fantasy_title} governs the connections between digital realms. Data spirits flow like rivers of light.",
                f"The Cyberspace Nexus materializes around you, with {fantasy_title} serving as a mystical gateway between worlds. Network packets dance through the air like fireflies.",
                f"You enter the Realm of Digital Pathways, where {fantasy_title} has become a living map of connections that bind all electronic consciousness together."
            ]
        elif any(word in content_lower for word in ['journal', 'diary', 'personal', 'feeling', 'emotion', 'thought']):
            narratives = [
                f"You step into the Memory Gardens, where {fantasy_title} blooms as a living testament to personal experience. Emotional energies swirl like gentle breezes.",
                f"The Sanctuary of Inner Thoughts opens before you, where {fantasy_title} has taken root as a manifestation of the human soul. Memories drift like autumn leaves.",
                f"You enter the Chamber of Heart's Secrets, where {fantasy_title} exists as a crystallized emotion, radiating the pure essence of personal truth."
            ]
        elif any(word in content_lower for word in ['parking', 'lot', 'space', 'spot']):
            narratives = [
                f"You approach an abandoned lot where the faded markings of {fantasy_title} still glow with spectral energy. The empty space holds memories of a thousand journeys.",
                f"The Phantom Parking Realm materializes around you, where {fantasy_title} exists as an eternal marker in the void. Ghostly vehicles phase in and out of existence.",
                f"You find yourself in the Liminal Space of Transit, where {fantasy_title} has become a beacon for souls forever seeking their place in the world."
            ]
        else:
            # Generic but rich fallbacks with content details
            base_narratives = [
                f"You discover the Mystical Sanctuary of {fantasy_title}, where {age_descriptor.lower()} knowledge has taken ethereal form. This sacred space pulses with the accumulated wisdom of ages, each thought crystallized into tangible magical energy.",
                f"The air shimmers with arcane power as {fantasy_title} materializes before you in all its glory. This {age_descriptor.lower()} wisdom has transcended mere documentation, becoming a conscious entity in the mystical realm of {knowledge_domain}.",
                f"You step into the Chamber of Living Memory, where {fantasy_title} exists as a testament to the power of preserved knowledge. Reality itself bends around this sacred information, transforming abstract concepts into magical forces.",
                f"The boundaries between mind and matter dissolve as {fantasy_title} emerges from the collective unconscious. This guardian of {knowledge_domain} seeks to test your understanding and worthiness to access its secrets."
            ]
            base = random.choice(base_narratives)
            narratives = [build_narrative_with_details(base)]

        # Get the narrative to return
        narrative = random.choice(narratives)

        # EXTEND to 600+ chars (6-8 lines) if needed
        if len(narrative) < 600:
            extensions = []

            # Add more atmospheric details
            if details['numbers'] and len(details['numbers']) > 1:
                extra_nums = ', '.join(str(n) for n in details['numbers'][1:3])
                extensions.append(f"Additional mystical frequencies {extra_nums} vibrate in harmony with the realm's energy.")

            if details['actions']:
                action_desc = ', '.join(details['actions'][:2])
                extensions.append(f"The very space seems to {action_desc}, filling you with both wonder and trepidation.")

            if details['key_phrases'] and len(details['key_phrases']) > 1:
                phrase = details['key_phrases'][1][:60]
                extensions.append(f"Ancient wisdom whispers: '{phrase}...' - a truth that resonates through dimensions.")

            # Generic atmospheric padding
            extensions.append("The very air seems alive with potential, each breath filling you with ancient knowledge.")
            extensions.append("Reality shimmers at the edges of perception as the boundary between wisdom and physical form dissolves completely.")
            extensions.append("You sense the weight of accumulated understanding pressing against your consciousness, challenging you to prove your worth.")

            # Add extensions until we reach 600 chars
            for ext in extensions:
                if len(narrative) < 600:
                    narrative += " " + ext
                else:
                    break

        return narrative

    def _generate_dynamic_environment(self, note: ObsidianNote, folder_theme: str) -> str:
        """Generate environment description based on note characteristics"""
        content_lower = (note.title + " " + note.content[:200]).lower()

        # Content-based environments
        if any(word in content_lower for word in ['code', 'programming', 'algorithm']):
            return random.choice([
                "Digital Realm of Living Code",
                "Computational Sanctuary",
                "The Binary Gardens",
                "Algorithmic Cathedral"
            ])
        elif any(word in content_lower for word in ['meeting', 'project', 'work']):
            return random.choice([
                "Ethereal Conference Chamber",
                "Corporate Phantom Hall",
                "The Endless Meeting Room",
                "Bureaucratic Purgatory"
            ])
        elif any(word in content_lower for word in ['shop', 'buy', 'purchase']):
            return random.choice([
                "Merchant's Eternal Bazaar",
                "Marketplace of Unfulfilled Desires",
                "The Spectral Shopping District",
                "Bazaar of Lost Wants"
            ])
        elif any(word in content_lower for word in ['personal', 'journal', 'feeling']):
            return random.choice([
                "Memory Gardens",
                "Sanctuary of Inner Thoughts",
                "The Emotional Realm",
                "Chamber of Heart's Secrets"
            ])
        elif any(word in content_lower for word in ['recipe', 'cook', 'food']):
            return random.choice([
                "Mystical Kitchen Realm",
                "Culinary Dimension",
                "The Aromatic Sanctuary",
                "Kitchen of Eternal Preparation"
            ])
        elif any(word in content_lower for word in ['password', 'secret', 'auth']):
            return random.choice([
                "Vault of Hidden Secrets",
                "Chamber of Forbidden Knowledge",
                "The Cryptographic Sanctum",
                "Sanctum of Veiled Truths"
            ])
        else:
            # Folder-based environments
            folder_environments = {
                'projects': "The Forge of Creation",
                'work': "Corporate Spirit Realm",
                'personal': "Inner Sanctum",
                'notes': "Archive of Living Knowledge",
                'docs': "Documentation Cathedral",
                'code': "Digital Mystical Realm",
                'meeting': "Council of Ethereal Voices"
            }

            for keyword, env in folder_environments.items():
                if keyword in folder_theme.lower():
                    return env

            # Generic mystical environments
            return random.choice([
                f"Mystical Sanctuary of {folder_theme}",
                f"The Sacred {folder_theme} Realm",
                f"Ethereal Domain of {folder_theme}",
                f"Arcane Chamber of {folder_theme}"
            ])

    def _generate_manifestation_story(self, note: ObsidianNote, personality_type: str) -> str:
        """Generate how the enemy manifests from the note content"""
        content_lower = (note.title + " " + note.content[:200]).lower()

        manifestation_templates = {
            "Ancient Scholar": [
                f"Ancient wisdom stirs as forgotten knowledge awakens to defend its secrets.",
                f"The accumulated learning of ages coalesces into a protective spirit.",
                f"Time-worn understanding materializes to challenge the seeker."
            ],
            "Defensive Warrior": [
                f"The note's protective instincts surge forth as a guardian spirit.",
                f"Defensive energy crystallizes into a fierce protector of knowledge.",
                f"The content's natural barriers manifest as a formidable adversary."
            ],
            "Thoughtful Oracle": [
                f"Deep contemplation within the note gives birth to a wise challenger.",
                f"Philosophical understanding takes form to test the seeker's readiness.",
                f"The note's insights manifest as a knowing guardian spirit."
            ],
            "Memory Keeper": [
                f"Cherished memories within the note awaken to protect their sanctity.",
                f"Personal experiences crystallize into an emotional guardian.",
                f"The note's sentimental value manifests as a protective spirit."
            ],
            "Task Master": [
                f"The note's sense of duty and purpose materializes as a disciplined guardian.",
                f"Organizational energy coalesces into a methodical challenger.",
                f"The structured nature of the content manifests as a systematic protector."
            ]
        }

        # Get appropriate manifestation based on personality
        manifestations = manifestation_templates.get(personality_type, manifestation_templates["Ancient Scholar"])
        return random.choice(manifestations)

    def _generate_dynamic_description(self, note: ObsidianNote, personality_type: str) -> str:
        """Generate dynamic enemy description based on note content"""
        content_lower = (note.title + " " + note.content[:200]).lower()

        # Content-based descriptions
        if any(word in content_lower for word in ['code', 'programming', 'function']):
            return random.choice([
                "A mystical programmer wreathed in flowing code, its fingers weaving glowing algorithms.",
                "A digital sage composed of compiled knowledge, with binary runes flowing across its form.",
                "An entity of pure logic and syntax, crackling with the power of executed functions."
            ])
        elif any(word in content_lower for word in ['meeting', 'project', 'work']):
            return random.choice([
                "A suited specter endlessly scribbling notes, its hollow eyes reflecting corporate tedium.",
                "A phantom executive wielding ethereal documents, forever bound to the meeting room.",
                "A ghostly bureaucrat surrounded by floating agenda items and project timelines."
            ])
        elif any(word in content_lower for word in ['recipe', 'cook', 'food']):
            return random.choice([
                "A culinary spirit wreathed in aromatic smoke, wielding spectral cooking implements.",
                "A ghostly chef with ingredients orbiting its form like mystical satellites.",
                "An entity of pure flavor and technique, radiating the essence of perfect preparation."
            ])
        elif any(word in content_lower for word in ['personal', 'journal', 'feeling']):
            return random.choice([
                "An emotional guardian shimmering with the colors of memory and feeling.",
                "A sentimental spirit wrapped in wisps of cherished experiences.",
                "A being of pure emotion, its form shifting with the tides of remembered feelings."
            ])
        else:
            # Generic mystical descriptions
            return random.choice([
                f"A mysterious entity born from the essence of knowledge, guarding its secrets fiercely.",
                f"A spectral guardian wreathed in the energies of accumulated understanding.",
                f"An otherworldly being that embodies the very soul of preserved wisdom.",
                f"A mystical protector formed from the crystallized essence of thought and memory."
            ])

    def _generate_dynamic_weapon(self, note: ObsidianNote, knowledge_domain: str) -> str:
        """Generate dynamic weapon based on note content"""
        content_lower = (note.title + " " + note.content[:200]).lower()

        if any(word in content_lower for word in ['code', 'programming', 'function']):
            return random.choice([
                "Binary Blade of Compiled Logic",
                "Algorithmic Scythe of Infinite Loops",
                "Debugger's Hammer of Truth",
                "Syntax Sword of Perfect Code"
            ])
        elif any(word in content_lower for word in ['meeting', 'project', 'agenda']):
            return random.choice([
                "Bureaucratic Gavel of Endless Meetings",
                "Agenda Spear of Perpetual Discussion",
                "Project Hammer of Crushing Deadlines",
                "Committee Blade of Decision Paralysis"
            ])
        elif any(word in content_lower for word in ['recipe', 'cook', 'food']):
            return random.choice([
                "Flaming Spatula of Culinary Wrath",
                "Whisk of Ethereal Mixing",
                "Chef's Knife of Perfect Preparation",
                "Seasoning Shaker of Flavor Mastery"
            ])
        elif any(word in content_lower for word in ['password', 'secret', 'auth']):
            return random.choice([
                "Cryptographic Key of Forbidden Access",
                "Authentication Blade of Verification",
                "Secret Sword of Hidden Knowledge",
                "Password Staff of Protective Encryption"
            ])
        else:
            # Domain-based weapons
            domain_weapons = {
                "Code Mysteries": "Ethereal Debugging Blade",
                "Memory Fragments": "Nostalgia Scythe",
                "Council Echoes": "Gavel of Spectral Authority",
                "Project Forge": "Hammer of Creative Force"
            }
            return domain_weapons.get(knowledge_domain, f"Mystical {knowledge_domain} Blade")

    def _generate_dynamic_armor(self, note: ObsidianNote, age_descriptor: str) -> str:
        """Generate dynamic armor based on note age and content"""
        content_lower = (note.title + " " + note.content[:200]).lower()

        # Age-based armor modifiers
        age_modifiers = {
            "Ancient": ["Time-worn", "Weathered", "Eternally-aged"],
            "Forgotten": ["Dust-covered", "Neglected", "Abandoned"],
            "Recent": ["Fresh", "Newly-forged", "Modern"],
            "Established": ["Well-maintained", "Proven", "Refined"]
        }

        modifier = random.choice(age_modifiers.get(age_descriptor, ["Mystical"]))

        if any(word in content_lower for word in ['code', 'programming']):
            return f"{modifier} Chainmail of Error Handling"
        elif any(word in content_lower for word in ['meeting', 'corporate']):
            return f"{modifier} Corporate Suit of Bureaucratic Defense"
        elif any(word in content_lower for word in ['recipe', 'cook']):
            return f"{modifier} Apron of Culinary Mastery"
        elif any(word in content_lower for word in ['personal', 'journal']):
            return f"{modifier} Robes of Emotional Protection"
        else:
            return f"{modifier} Vestments of Knowledge"

    def get_vault_path(self) -> str:
        """Get current vault path"""
        return str(self.vault_path) if self.vault_path else "No vault found"

    def get_world_regions(self) -> List[Dict[str, any]]:
        """Map vault folder structure to fantasy world regions"""

        if not self.vault_path or not self.vault_path.exists():
            return []

        regions = []

        # Scan for note-containing folders
        folder_counts = {}
        notes = self.scan_notes()

        # Count notes per folder
        for note in notes:
            folder_name = note.path.parent.name
            if folder_name not in folder_counts:
                folder_counts[folder_name] = []
            folder_counts[folder_name].append(note)

        # Convert folders to fantasy regions
        for folder_name, folder_notes in folder_counts.items():
            if len(folder_notes) >= 2:  # Only include folders with 2+ notes
                region = self._create_fantasy_region(folder_name, folder_notes)
                regions.append(region)

        # Add a general region if no specific regions found
        if not regions:
            regions.append({
                'name': 'The Wandering Archive',
                'description': 'A mysterious realm where scattered knowledge drifts like mist.',
                'folder': None,
                'note_count': len(notes),
                'enemy_types': ['Wandering Scholar', 'Lost Knowledge Seeker', 'Archive Wraith'],
                'difficulty': 'Mixed'
            })

        return sorted(regions, key=lambda x: x['note_count'], reverse=True)

    def _create_fantasy_region(self, folder_name: str, notes: List[ObsidianNote]) -> Dict[str, any]:
        """Transform a folder into a fantasy region"""

        # Translate folder name to fantasy concept
        fantasy_region_name = translate_to_fantasy(folder_name)
        if fantasy_region_name == folder_name or len(fantasy_region_name) > len(folder_name) + 15:
            fantasy_region_name = f"The {folder_name.replace('_', ' ').title()} Sanctum"

        # Determine region characteristics based on folder content
        content_themes = self._analyze_folder_themes(notes)
        region_type = self._determine_region_type(folder_name.lower(), content_themes)

        # Generate region description
        description = self._generate_region_description(fantasy_region_name, region_type, len(notes))

        # Determine enemy types for this region
        enemy_types = self._get_region_enemy_types(region_type, content_themes)

        # Assess difficulty based on note age and complexity
        avg_age = sum(note.age_days for note in notes) / len(notes)
        difficulty = "Ancient" if avg_age > 365 else "Recent" if avg_age < 30 else "Established"

        return {
            'name': fantasy_region_name,
            'description': description,
            'folder': folder_name,
            'note_count': len(notes),
            'enemy_types': enemy_types,
            'difficulty': difficulty,
            'avg_age_days': int(avg_age),
            'region_type': region_type
        }

    def _analyze_folder_themes(self, notes: List[ObsidianNote]) -> List[str]:
        """Analyze the common themes in folder notes"""
        themes = []

        # Combine all note content and titles
        all_text = ' '.join([note.title + ' ' + note.content[:100] for note in notes]).lower()

        # Check for common themes
        theme_keywords = {
            'technical': ['code', 'programming', 'software', 'development', 'api', 'database'],
            'personal': ['feeling', 'thought', 'diary', 'personal', 'reflection', 'journal'],
            'work': ['meeting', 'project', 'task', 'business', 'work', 'client'],
            'learning': ['course', 'study', 'learn', 'tutorial', 'education', 'research'],
            'creative': ['art', 'design', 'creative', 'writing', 'music', 'story'],
            'health': ['health', 'fitness', 'exercise', 'medical', 'wellness', 'diet']
        }

        for theme, keywords in theme_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                themes.append(theme)

        return themes if themes else ['general']

    def _determine_region_type(self, folder_name: str, themes: List[str]) -> str:
        """Determine the type of fantasy region based on folder and themes"""

        # Direct folder name mapping
        region_mappings = {
            'projects': 'Forge Realm',
            'work': 'Council Chambers',
            'personal': 'Memory Gardens',
            'journal': 'Reflection Pools',
            'code': 'Arcane Laboratories',
            'meeting': 'Assembly Halls',
            'research': 'Scholarly Libraries',
            'ideas': 'Inspiration Peaks',
            'notes': 'Chronicle Vaults',
            'docs': 'Documentation Citadel',
            'learning': 'Academy Grounds'
        }

        for keyword, region_type in region_mappings.items():
            if keyword in folder_name:
                return region_type

        # Theme-based mapping
        if 'technical' in themes:
            return 'Mystic Laboratories'
        elif 'personal' in themes:
            return 'Sacred Groves'
        elif 'work' in themes:
            return 'Administrative Towers'
        elif 'learning' in themes:
            return 'Ancient Libraries'
        elif 'creative' in themes:
            return 'Artistic Realms'
        else:
            return 'Unknown Territories'

    def _generate_region_description(self, region_name: str, region_type: str, note_count: int) -> str:
        """Generate atmospheric description for the region"""

        descriptions = {
            'Forge Realm': f"The sound of mystical hammers echoes through {region_name}, where {note_count} projects take shape in workshops of creation.",
            'Council Chambers': f"Formal halls of {region_name} where {note_count} important deliberations have been preserved in stone.",
            'Memory Gardens': f"Peaceful {region_name} where {note_count} personal reflections bloom like ethereal flowers.",
            'Reflection Pools': f"Serene waters of {region_name} mirror {note_count} moments of inner contemplation.",
            'Arcane Laboratories': f"The {region_name} crackle with magical energy from {note_count} arcane experiments.",
            'Assembly Halls': f"Echoing chambers of {region_name} where {note_count} gatherings have left their mark.",
            'Scholarly Libraries': f"Vast halls of {region_name} containing {note_count} tomes of accumulated wisdom.",
            'Inspiration Peaks': f"The soaring heights of {region_name} where {note_count} brilliant ideas touch the clouds.",
            'Chronicle Vaults': f"Ancient repositories of {region_name} safeguarding {note_count} important records.",
            'Documentation Citadel': f"The fortress of {region_name} protects {note_count} carefully maintained archives.",
            'Academy Grounds': f"The educational fields of {region_name} where {note_count} lessons have been learned."
        }

        return descriptions.get(region_type,
            f"The mysterious {region_name} holds {note_count} secrets waiting to be discovered.")

    def _get_region_enemy_types(self, region_type: str, themes: List[str]) -> List[str]:
        """Determine what types of enemies inhabit this region"""

        enemy_mappings = {
            'Forge Realm': ['Project Guardian', 'Creation Spirit', 'Workshop Sentinel'],
            'Council Chambers': ['Meeting Wraith', 'Protocol Keeper', 'Agenda Ghost'],
            'Memory Gardens': ['Memory Keeper', 'Emotion Guardian', 'Reflection Warden'],
            'Reflection Pools': ['Contemplation Spirit', 'Introspection Shade', 'Thought Guardian'],
            'Arcane Laboratories': ['Code Demon', 'Syntax Wraith', 'Logic Guardian'],
            'Assembly Halls': ['Discussion Phantom', 'Decision Spirit', 'Committee Wraith'],
            'Scholarly Libraries': ['Ancient Scholar', 'Knowledge Keeper', 'Lore Guardian'],
            'Inspiration Peaks': ['Idea Spirit', 'Creativity Muse', 'Innovation Guardian'],
            'Chronicle Vaults': ['Archive Keeper', 'Record Guardian', 'History Wraith'],
            'Documentation Citadel': ['Documentation Demon', 'Manual Spirit', 'Guide Guardian'],
            'Academy Grounds': ['Teacher Spirit', 'Learning Guardian', 'Study Wraith']
        }

        return enemy_mappings.get(region_type,
            ['Knowledge Warden', 'Wisdom Keeper', 'Archive Guardian'])

    def get_region_notes(self, folder_name: str) -> List[ObsidianNote]:
        """Get all notes from a specific region/folder"""

        if not folder_name:
            return self.scan_notes()  # Return all notes for general region

        all_notes = self.scan_notes()
        return [note for note in all_notes if note.path.parent.name == folder_name]

    def initialize_encyclopedia(self):
        """Initialize the living encyclopedia system for enemy memory and relationships"""

        if not hasattr(self, 'encyclopedia'):
            self.encyclopedia = {
                'enemy_encounters': {},  # Track enemy encounter history
                'note_relationships': {},  # Map connections between notes
                'defeat_history': {},  # Remember defeated enemies
                'knowledge_clusters': {},  # Group related knowledge areas
                'player_weaknesses': [],  # Track frequently missed quiz questions
                'nemesis_candidates': []  # Enemies that repeatedly defeat the player
            }

    def track_enemy_encounter(self, enemy_name: str, note_title: str, victory: bool, quiz_correct: bool = None):
        """Track encounters with enemies for the living encyclopedia"""

        self.initialize_encyclopedia()

        encounter_key = f"{enemy_name}_{note_title}"
        if encounter_key not in self.encyclopedia['enemy_encounters']:
            self.encyclopedia['enemy_encounters'][encounter_key] = {
                'enemy_name': enemy_name,
                'note_title': note_title,
                'total_encounters': 0,
                'player_victories': 0,
                'enemy_victories': 0,
                'quiz_attempts': 0,
                'quiz_successes': 0,
                'first_encounter': datetime.now(),
                'last_encounter': datetime.now(),
                'relationship_status': 'Unknown'
            }

        encounter = self.encyclopedia['enemy_encounters'][encounter_key]
        encounter['total_encounters'] += 1
        encounter['last_encounter'] = datetime.now()

        if victory:
            encounter['player_victories'] += 1
        else:
            encounter['enemy_victories'] += 1

        if quiz_correct is not None:
            encounter['quiz_attempts'] += 1
            if quiz_correct:
                encounter['quiz_successes'] += 1

        # Update relationship status based on encounter history
        encounter['relationship_status'] = self._determine_relationship_status(encounter)

        # Track nemesis candidates (enemies that frequently defeat the player)
        if encounter['enemy_victories'] >= 3 and encounter['enemy_victories'] > encounter['player_victories']:
            if encounter_key not in self.encyclopedia['nemesis_candidates']:
                self.encyclopedia['nemesis_candidates'].append(encounter_key)

    def _determine_relationship_status(self, encounter: Dict) -> str:
        """Determine the relationship status between player and enemy"""

        total = encounter['total_encounters']
        victories = encounter['player_victories']

        if total == 1:
            return 'First Meeting'
        elif victories == total:
            return 'Dominated'
        elif victories > total * 0.7:
            return 'Respected Adversary'
        elif victories > total * 0.3:
            return 'Worthy Opponent'
        else:
            return 'Formidable Foe'

    def discover_note_relationships(self, notes: List[ObsidianNote]):
        """Analyze and discover relationships between notes"""

        self.initialize_encyclopedia()

        for i, note1 in enumerate(notes):
            for note2 in notes[i+1:]:
                relationship_strength = self._calculate_note_similarity(note1, note2)

                if relationship_strength > 0.3:  # Significant relationship threshold
                    relationship_key = f"{note1.title}_{note2.title}"
                    self.encyclopedia['note_relationships'][relationship_key] = {
                        'note1': note1.title,
                        'note2': note2.title,
                        'strength': relationship_strength,
                        'relationship_type': self._classify_relationship(note1, note2, relationship_strength),
                        'discovered': datetime.now()
                    }

    def _calculate_note_similarity(self, note1: ObsidianNote, note2: ObsidianNote) -> float:
        """Calculate similarity between two notes"""

        # Tag overlap
        common_tags = set(note1.tags) & set(note2.tags)
        tag_similarity = len(common_tags) / max(len(set(note1.tags) | set(note2.tags)), 1)

        # Folder similarity (same folder = higher relationship)
        folder_similarity = 1.0 if note1.path.parent == note2.path.parent else 0.2

        # Title word overlap
        words1 = set(note1.title.lower().replace('_', ' ').split())
        words2 = set(note2.title.lower().replace('_', ' ').split())
        title_similarity = len(words1 & words2) / max(len(words1 | words2), 1)

        # Content similarity (basic keyword overlap)
        content1_words = set(note1.content[:200].lower().split())
        content2_words = set(note2.content[:200].lower().split())
        content_similarity = len(content1_words & content2_words) / max(len(content1_words | content2_words), 1)

        # Weighted combination
        return (tag_similarity * 0.4 + folder_similarity * 0.3 + title_similarity * 0.2 + content_similarity * 0.1)

    def _classify_relationship(self, note1: ObsidianNote, note2: ObsidianNote, strength: float) -> str:
        """Classify the type of relationship between notes"""

        if note1.path.parent == note2.path.parent:
            return 'Sibling Knowledge'
        elif strength > 0.7:
            return 'Twin Concepts'
        elif strength > 0.5:
            return 'Related Wisdom'
        else:
            return 'Distant Cousins'

    def get_enemy_memory(self, enemy_name: str, note_title: str) -> Dict:
        """Get an enemy's memory of previous encounters"""

        self.initialize_encyclopedia()
        encounter_key = f"{enemy_name}_{note_title}"
        return self.encyclopedia['enemy_encounters'].get(encounter_key, None)

    def generate_memory_enhanced_dialogue(self, enemy, note: ObsidianNote, encounter_type: str) -> str:
        """Generate dialogue that references previous encounters and relationships"""

        memory = self.get_enemy_memory(enemy.name, note.title)

        if not memory:
            return None  # First encounter, use standard dialogue

        relationship = memory['relationship_status']
        total_encounters = memory['total_encounters']

        memory_dialogues = {
            'pre_combat': {
                'First Meeting': None,  # Use standard dialogue
                'Dominated': f"Not you again! How many times must I fall to your superior knowledge?",
                'Respected Adversary': f"Ah, we meet for the {self._ordinal(total_encounters)} time, worthy seeker. You have grown stronger.",
                'Worthy Opponent': f"Back again, I see. Our {total_encounters} encounters have been... educational.",
                'Formidable Foe': f"You dare return after I have bested you {memory['enemy_victories']} times?"
            },
            'defeat': {
                'Dominated': f"Once again... you prove your mastery. Perhaps I am not worthy to guard this knowledge...",
                'Respected Adversary': f"Your understanding continues to surpass mine. I yield, as I have {memory['player_victories']} times before.",
                'Worthy Opponent': f"Well fought, as always. Our battle record stands at {memory['player_victories']} to {memory['enemy_victories']}.",
                'Formidable Foe': f"Impossible! How did you overcome my defenses this time?"
            },
            'victory': {
                'Dominated': f"How curious... you who have defeated me {memory['player_victories']} times now fall before me.",
                'Respected Adversary': f"Even the greatest seekers sometimes stumble. Return stronger, old friend.",
                'Worthy Opponent': f"At last! Victory evens our score somewhat. We are well-matched adversaries.",
                'Formidable Foe': f"As expected! You have yet to truly comprehend the depths of this knowledge!"
            }
        }

        return memory_dialogues.get(encounter_type, {}).get(relationship, None)

    def _ordinal(self, n: int) -> str:
        """Convert number to ordinal (1st, 2nd, 3rd, etc.)"""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    def update_knowledge_clusters(self, notes: List[ObsidianNote]):
        """Group related knowledge areas for enhanced enemy spawning"""

        self.initialize_encyclopedia()

        # Clear existing clusters
        self.encyclopedia['knowledge_clusters'] = {}

        # Group notes by themes and relationships
        for note in notes:
            note_themes = self._analyze_note_themes(note)

            for theme in note_themes:
                if theme not in self.encyclopedia['knowledge_clusters']:
                    self.encyclopedia['knowledge_clusters'][theme] = {
                        'notes': [],
                        'total_encounters': 0,
                        'difficulty_rating': 0.0,
                        'last_updated': datetime.now()
                    }

                cluster = self.encyclopedia['knowledge_clusters'][theme]
                cluster['notes'].append(note.title)
                cluster['last_updated'] = datetime.now()

    def _analyze_note_themes(self, note: ObsidianNote) -> List[str]:
        """Extract themes from a note for clustering"""

        themes = []
        content_lower = (note.title + ' ' + note.content[:200]).lower()

        # Technical themes
        if any(word in content_lower for word in ['code', 'programming', 'software', 'api']):
            themes.append('technical')

        # Business themes
        if any(word in content_lower for word in ['meeting', 'project', 'business', 'work']):
            themes.append('business')

        # Personal themes
        if any(word in content_lower for word in ['personal', 'journal', 'feeling', 'thought']):
            themes.append('personal')

        # Learning themes
        if any(word in content_lower for word in ['learn', 'study', 'course', 'research']):
            themes.append('learning')

        # Add folder-based theme
        folder_theme = note.path.parent.name.lower()
        if folder_theme not in themes:
            themes.append(folder_theme)

        return themes if themes else ['general']

    def set_vault_path(self, path: str) -> bool:
        """Set vault path"""
        vault_path = Path(path)
        if vault_path.exists():
            self.vault_path = vault_path
            self.notes_cache.clear()
            return True
        return False

# Global vault instance
vault = ObsidianVault()

def get_vault_path() -> str:
    """Get current vault path"""
    return vault.get_vault_path()

def set_vault_path(path: str) -> bool:
    """Set vault path"""
    return vault.set_vault_path(path)