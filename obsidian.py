"""
Obsidian Vault Integration for Legend of the Obsidian Vault
Reads notes and converts them to forest enemies
"""
import os
import re
import random
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple
from game_data import ObsidianNote, Enemy, FOREST_ENEMIES

class ObsidianVault:
    """Interface to Obsidian vault"""

    def __init__(self, vault_path: str = None):
        self.vault_path = Path(vault_path) if vault_path else self.find_vault()
        self.notes_cache = {}
        self.last_scan = None

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
            enemy_name = self._generate_enemy_name(note, base_enemy[0])

            # Scale stats based on note difficulty vs player level
            difficulty_multiplier = min(1.5, max(0.8, note.difficulty_level / level))

            return Enemy(
                name=enemy_name,
                hitpoints=int(base_enemy[1] * difficulty_multiplier),
                attack=int(base_enemy[2] * difficulty_multiplier),
                gold_reward=base_enemy[3],
                exp_reward=base_enemy[3] // 2,
                level=level,
                note_content=note.content[:500],  # Truncate for performance
                note_title=note.title
            )
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
        """Generate enemy name incorporating note title"""
        templates = [
            f"{base_enemy} of {note.title}",
            f"{base_enemy} guarding {note.title}",
            f"{note.title} {base_enemy}",
            f"Forgotten {base_enemy} from {note.title}",
            f"{base_enemy} wielding {note.title}",
        ]

        # Keep it under 40 characters for display
        name = random.choice(templates)
        if len(name) > 40:
            # Truncate note title
            max_title_len = 40 - len(base_enemy) - 10
            short_title = note.title[:max_title_len] + "..." if len(note.title) > max_title_len else note.title
            name = f"{base_enemy} of {short_title}"

        return name

    def generate_quiz_question(self, note: ObsidianNote) -> Tuple[str, str]:
        """Generate a quiz question from note content (AI-enhanced)"""
        try:
            # Try AI-enhanced quiz generation first
            from brainbot import sync_generate_quiz_question, is_ai_available

            if is_ai_available():
                return sync_generate_quiz_question(note.title, note.content, note.difficulty_level)
        except ImportError:
            pass
        except Exception as e:
            print(f"AI quiz generation failed: {e}")

        # Fallback to regex-based generation
        content = note.content.lower()

        # Try to find definition patterns
        definition_match = re.search(r'(.+?)\s+is\s+(.+?)[\.\n]', content)
        if definition_match:
            concept = definition_match.group(1).strip()
            definition = definition_match.group(2).strip()
            return f"What is {concept}?", definition[:50]

        # Try to find list items
        list_match = re.search(r'[-\*]\s+(.+)', content)
        if list_match:
            item = list_match.group(1).strip()
            return f"Name something related to {note.title}", item[:50]

        # Extract first sentence
        first_sentence = re.search(r'^([^\.!?]+[\.!?])', content.strip())
        if first_sentence:
            sentence = first_sentence.group(1).strip()
            # Create question from sentence
            if len(sentence) < 100:
                return f"Complete: {sentence[:50]}...", sentence[50:100]

        # Fallback questions
        fallback_questions = [
            (f"What category does {note.title} belong to?", "knowledge"),
            (f"When did you last think about {note.title}?", "recently"),
            (f"Why is {note.title} important?", "learning"),
        ]

        return random.choice(fallback_questions)

    def get_vault_path(self) -> str:
        """Get current vault path"""
        return str(self.vault_path) if self.vault_path else "No vault found"

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