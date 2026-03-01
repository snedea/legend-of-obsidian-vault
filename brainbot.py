"""
BrainBot AI Integration for Legend of the Obsidian Vault
Multi-provider AI integration: TinyLlama (local), Claude CLI, Claude API
"""
import re
import random
import threading
import time
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# Try to import the AI libraries
try:
    from llama_cpp import Llama
    from huggingface_hub import hf_hub_download
    TINYLLAMA_AVAILABLE = True
except ImportError:
    TINYLLAMA_AVAILABLE = False
    Llama = None
    hf_hub_download = None

# Try to import Anthropic SDK
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

# TinyLlama model configuration (same as BrainBot)
MODEL_REPO = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
MODEL_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
MODEL_DIR = Path.home() / ".cache" / "brainbot"

@dataclass
class QuizQuestion:
    """AI-generated quiz question"""
    question: str
    answer: str
    difficulty: int  # 1-5 scale
    question_type: str  # definition, concept, relationship, etc.
    context: str  # Additional context from the note

    # Multiple choice fields
    options: List[str] = field(default_factory=list)  # List of 3 options
    correct_index: int = 0  # Index of correct answer (0, 1, or 2)

@dataclass
class EnemyDescription:
    """AI-generated enemy description with rich narrative"""
    name: str
    description: str
    weapon: str
    armor: str
    backstory: str
    combat_phrases: List[str]
    defeat_message: str
    victory_message: str
    recommended_hp: int = 15
    recommended_attack: int = 5

    # Rich narrative fields
    encounter_narrative: str = ""
    environment_description: str = ""
    manifestation_story: str = ""


# =============================================================================
# AI Provider Abstract Base Class
# =============================================================================

class AIProvider(ABC):
    """Abstract base class for AI providers"""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the provider. Returns True if successful."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is ready to use."""
        pass

    @abstractmethod
    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Optional[QuizQuestion]:
        """Generate a quiz question from note content."""
        pass

    @abstractmethod
    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate an enemy description from note content."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the human-readable provider name."""
        pass


# =============================================================================
# TinyLlama Provider (Local AI)
# =============================================================================

class LocalAIClient:
    """Local TinyLlama client for AI services"""

    def __init__(self):
        self.model = None
        self.model_path = None
        self.available = False
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        self.loading = False

    def initialize(self) -> bool:
        """Initialize the local AI model"""
        if not TINYLLAMA_AVAILABLE:
            print("🤖 TinyLlama libraries not available - using fallback mode")
            return False

        if self.loading:
            return False

        try:
            self.loading = True
            print("🧠 Initializing TinyLlama model...")

            # Ensure model directory exists
            MODEL_DIR.mkdir(parents=True, exist_ok=True)
            self.model_path = MODEL_DIR / MODEL_FILE

            # Download model if not exists
            if not self.model_path.exists():
                print(f"📥 Downloading TinyLlama model ({MODEL_FILE})...")
                print("   This may take a few minutes on first run...")

                try:
                    downloaded_path = hf_hub_download(
                        repo_id=MODEL_REPO,
                        filename=MODEL_FILE,
                        cache_dir=MODEL_DIR.parent,
                        local_dir=MODEL_DIR,
                        local_dir_use_symlinks=False
                    )
                    print("✅ Model downloaded successfully!")
                except Exception as e:
                    print(f"❌ Model download failed: {e}")
                    return False

            # Load the model
            print("🔄 Loading TinyLlama model into memory...")
            self.model = Llama(
                model_path=str(self.model_path),
                n_ctx=2048,        # Context window
                n_threads=4,       # CPU threads
                n_gpu_layers=0,    # CPU only for compatibility
                temperature=0.7,   # Creativity vs consistency
                verbose=False      # Quiet mode
            )

            self.available = True
            print("🎉 TinyLlama AI ready for intelligent quiz generation!")
            return True

        except Exception as e:
            print(f"❌ AI initialization failed: {e}")
            print("🔄 Falling back to regex-based quiz generation")
            self.available = False
            return False
        finally:
            self.loading = False

    def generate_text(self, prompt: str, max_tokens: int = 150, generation_type: str = "quiz") -> Optional[str]:
        """Generate text using local TinyLlama model with context-aware prompts"""
        if not self.available or not self.model:
            return None

        try:
            # Dynamic system prompt based on generation type
            if generation_type == "enemy":
                system_prompt = """You are a creative fantasy writer who transforms any content into magical encounters.
Transform mundane notes into atmospheric fantasy adventures with vivid descriptions.
Use structured output format for easy parsing."""
            else:  # quiz or default
                system_prompt = """You are a helpful AI that creates quiz questions from notes.
Generate clear, educational questions that test understanding of key concepts.
Be concise and focused."""

            # Format the prompt
            full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>\n"

            # Generate response with appropriate settings for the task
            response = self.model(
                full_prompt,
                max_tokens=max_tokens,
                temperature=0.8 if generation_type == "enemy" else 0.7,  # More creative for enemies
                top_p=0.9,
                stop=["<|user|>", "<|system|>"],  # Remove \n\n to allow full responses
                echo=False
            )

            if response and "choices" in response and response["choices"]:
                generated_text = response["choices"][0]["text"].strip()

                # Minimal debug logging for enemy generation
                if generation_type == "enemy":
                    print(f"🧠 AI generated {len(generated_text)} chars")
                    # Debug: Show first 200 chars of response
                    print(f"🔍 AI Response preview: {generated_text[:200]}...")

                return generated_text

        except Exception as e:
            print(f"🔥 AI generation error ({generation_type}): {e}")

        return None

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Optional[QuizQuestion]:
        """Generate an intelligent quiz question from note content"""
        cache_key = f"quiz_{hash(note_content)}_{difficulty}"

        # Check cache
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_result

        # Create context-aware prompt for multiple choice
        prompt = f"""Based on this note about "{note_title}":

{note_content[:500]}

Generate a multiple choice quiz question that tests understanding of the key concept.

Create 3 answer options:
1. One correct answer
2. One plausible but incorrect answer (similar to correct but wrong in key detail)
3. One humorous/obviously wrong answer

Format your response exactly as:
QUESTION: [your question here]
CORRECT: [the correct answer]
DECOY: [plausible but incorrect answer]
FUNNY: [humorous wrong answer]
TYPE: [definition/concept/relationship/fact]

Make the decoy answer similar enough to confuse someone who doesn't know the material well."""

        response = self.generate_text(prompt, max_tokens=200)

        if response:
            # Parse the AI response for multiple choice
            question_match = re.search(r'QUESTION:\s*(.+?)(?=CORRECT:|$)', response, re.DOTALL)
            correct_match = re.search(r'CORRECT:\s*(.+?)(?=DECOY:|$)', response, re.DOTALL)
            decoy_match = re.search(r'DECOY:\s*(.+?)(?=FUNNY:|$)', response, re.DOTALL)
            funny_match = re.search(r'FUNNY:\s*(.+?)(?=TYPE:|$)', response, re.DOTALL)
            type_match = re.search(r'TYPE:\s*(.+?)$', response, re.DOTALL)

            if question_match and correct_match and decoy_match and funny_match:
                correct_answer = correct_match.group(1).strip()
                decoy_answer = decoy_match.group(1).strip()
                funny_answer = funny_match.group(1).strip()

                # Create options list and randomize order
                options = [correct_answer, decoy_answer, funny_answer]
                correct_index = 0  # Start with correct at index 0

                # Shuffle options and track where correct answer ends up
                import random
                shuffled_options = options.copy()
                random.shuffle(shuffled_options)
                correct_index = shuffled_options.index(correct_answer)

                quiz = QuizQuestion(
                    question=question_match.group(1).strip(),
                    answer=correct_answer,
                    difficulty=difficulty,
                    question_type=type_match.group(1).strip() if type_match else "concept",
                    context=note_content[:200],
                    options=shuffled_options,
                    correct_index=correct_index
                )

                # Cache the result
                self.cache[cache_key] = (time.time(), quiz)
                return quiz

        return None

    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate enemy backstory and combat dialog"""
        cache_key = f"enemy_{hash(note_content)}_{base_enemy}"

        # Check cache
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_result

        # Extract structured content for richer context
        structured_content = self._extract_structured_content(note_content)

        # Build enhanced content for AI context
        enhanced_content = note_content[:600]
        if structured_content['headers']:
            enhanced_content += f"\n\nHeaders: {', '.join(structured_content['headers'][:3])}"
        if structured_content['lists']:
            enhanced_content += f"\nList items: {', '.join(structured_content['lists'][:5])}"
        if structured_content['numbers']:
            enhanced_content += f"\nNumbers: {', '.join(map(str, structured_content['numbers'][:5]))}"

        prompt = f"""You are a dungeon master describing a magical encounter. Create a rich, atmospheric description of discovering a mystical realm where the knowledge from this note has come alive:

Title: "{note_title}"
Content: {enhanced_content}

Write a 3-4 sentence narrative describing the encounter as a dungeon master would. Include specific details from the note content (numbers, names, concepts, actions). Make it magical and immersive, like the knowledge itself has awakened to challenge intruders. Keep it concise but atmospheric.

Examples of good style:
- "You enter the Algorithm Archive where 27 mystical patterns swirl in the air..."
- "The ancient text declares: 'Machine learning automates analytical model building' as glowing runes..."
- "Five frameworks materialize as spectral guardians: TensorFlow, PyTorch..."

Write ONLY the narrative description:"""

        response = self.generate_text(prompt, max_tokens=400, generation_type="enemy")

        if response:
            # Clean up the AI response and use it as the main narrative
            encounter_narrative = response.strip()

            # Remove any formatting artifacts or unwanted prefixes
            if encounter_narrative.startswith(('Narrative:', 'ENCOUNTER_NARRATIVE:', 'Description:')):
                encounter_narrative = encounter_narrative.split(':', 1)[1].strip()

            print(f"🎭 AI generated rich narrative: {len(encounter_narrative)} chars")

            # Generate other fields using fallback methods since AI focuses only on narrative
            environment_desc = self._generate_fallback_environment(note_title, note_content)
            enemy_name = self._generate_fallback_name(note_title, note_content)
            description = self._generate_fallback_description(note_title, note_content)
            weapon = self._generate_fallback_weapon(note_title, note_content)
            armor = self._generate_fallback_armor(note_title, note_content)
            backstory = f"Born from the essence of {note_title}, this creature embodies forgotten knowledge."
            combat_phrase = f"Your understanding of {note_title} means nothing to me!"
            defeat_msg = f"The secrets of {note_title}... are yours to claim..."

            # Calculate recommended stats based on note content
            recommended_hp, recommended_attack = self._calculate_stats_from_content(note_content, note_title)

            # Cache the result
            enemy_desc = EnemyDescription(
                name=enemy_name,
                description=description,
                weapon=weapon,
                armor=armor,
                backstory=backstory,
                combat_phrases=[combat_phrase],
                defeat_message=defeat_msg,
                victory_message=f"The {enemy_name} has fallen!",
                recommended_hp=recommended_hp,
                recommended_attack=recommended_attack,
                encounter_narrative=encounter_narrative,
                environment_description=environment_desc,
                manifestation_story=f"The essence of {note_title} has awakened to guard its secrets."
            )

            self.cache[cache_key] = (time.time(), enemy_desc)
            return enemy_desc

        print(f"❌ AI enemy generation failed - no response generated")
        return None

    def _extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract a specific field from AI response"""
        pattern = f"{field_name}:\\s*(.+?)(?=\\n[A-Z_]+:|$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None

    def _calculate_stats_from_content(self, content: str, title: str) -> Tuple[int, int]:
        """Calculate enemy stats based on note characteristics and content nature"""
        content_lower = content.lower()

        # Base stats
        base_hp = 15
        base_attack = 5

        # Content type multipliers (some content types are inherently more "powerful")
        content_type_bonus = self._get_content_type_bonus(content_lower)

        # Scale by content length (knowledge depth)
        content_length = len(content)
        if content_length > 2000:
            length_hp = 20
            length_attack = 8
        elif content_length > 1000:
            length_hp = 10
            length_attack = 4
        elif content_length > 500:
            length_hp = 5
            length_attack = 2
        else:
            length_hp = 0
            length_attack = 0

        # Content complexity (technical, emotional, or conceptual depth)
        complexity_bonus = self._calculate_complexity_bonus(content_lower)

        # Content age factor (older knowledge can be more "entrenched")
        age_bonus = self._calculate_age_bonus(title, content)

        # Calculate final stats
        final_hp = base_hp + length_hp + content_type_bonus['hp'] + complexity_bonus['hp'] + age_bonus['hp']
        final_attack = base_attack + length_attack + content_type_bonus['attack'] + complexity_bonus['attack'] + age_bonus['attack']

        # Cap the stats reasonably
        final_hp = min(120, max(8, final_hp))
        final_attack = min(60, max(2, final_attack))

        return final_hp, final_attack

    def _get_content_type_bonus(self, content_lower: str) -> Dict[str, int]:
        """Get stat bonuses based on content type"""
        # Different content types have different "power levels"

        # High-power content (complex, important, or dangerous knowledge)
        if any(word in content_lower for word in ['password', 'secret', 'confidential', 'private']):
            return {'hp': 15, 'attack': 10}  # Secrets are well-defended
        elif any(word in content_lower for word in ['algorithm', 'database', 'api', 'framework', 'architecture']):
            return {'hp': 12, 'attack': 8}   # Technical knowledge is complex
        elif any(word in content_lower for word in ['financial', 'money', 'budget', 'investment', 'salary']):
            return {'hp': 10, 'attack': 6}   # Money matters are serious

        # Medium-power content
        elif any(word in content_lower for word in ['meeting', 'project', 'deadline', 'plan', 'strategy']):
            return {'hp': 8, 'attack': 5}    # Work content has moderate power
        elif any(word in content_lower for word in ['health', 'medical', 'doctor', 'symptoms']):
            return {'hp': 8, 'attack': 4}    # Health is important but less aggressive
        elif any(word in content_lower for word in ['recipe', 'cook', 'ingredient', 'food']):
            return {'hp': 6, 'attack': 7}    # Culinary knowledge can be surprisingly fierce

        # Low-power content (personal, simple, or routine)
        elif any(word in content_lower for word in ['shopping', 'list', 'reminder', 'note', 'thought']):
            return {'hp': 3, 'attack': 2}    # Simple notes are less formidable
        elif any(word in content_lower for word in ['dream', 'journal', 'diary', 'feeling']):
            return {'hp': 5, 'attack': 3}    # Personal content is more defensive than aggressive

        # Default for unrecognized content
        return {'hp': 5, 'attack': 3}

    def _calculate_complexity_bonus(self, content_lower: str) -> Dict[str, int]:
        """Calculate complexity bonus based on various indicators"""
        complexity_score = 0

        # Technical complexity indicators
        technical_words = ['function', 'class', 'variable', 'algorithm', 'database', 'API', 'framework', 'implementation']
        complexity_score += sum(1 for word in technical_words if word in content_lower)

        # Emotional complexity indicators
        emotional_words = ['feeling', 'emotion', 'anxiety', 'stress', 'happiness', 'sadness', 'anger', 'fear']
        complexity_score += sum(0.5 for word in emotional_words if word in content_lower)

        # Conceptual complexity indicators
        conceptual_words = ['analysis', 'theory', 'concept', 'philosophy', 'principle', 'methodology', 'paradigm']
        complexity_score += sum(1.5 for word in conceptual_words if word in content_lower)

        # URL/link complexity (interconnected knowledge)
        url_count = content_lower.count('http') + content_lower.count('www.') + content_lower.count('.com')
        complexity_score += url_count * 0.5

        # List complexity (structured information)
        list_indicators = content_lower.count('- ') + content_lower.count('* ') + content_lower.count('1. ')
        complexity_score += list_indicators * 0.3

        # Convert complexity score to stat bonuses
        hp_bonus = min(25, int(complexity_score * 2))
        attack_bonus = min(15, int(complexity_score * 1.2))

        return {'hp': hp_bonus, 'attack': attack_bonus}

    def _calculate_age_bonus(self, title: str, content: str) -> Dict[str, int]:
        """Calculate bonus based on perceived age/importance of content"""
        age_score = 0
        content_lower = content.lower()

        # Date patterns suggest historical/archived content
        import re
        date_patterns = len(re.findall(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}', content))
        age_score += date_patterns * 2

        # Words that suggest established/important knowledge
        establishment_words = ['established', 'founded', 'historical', 'legacy', 'traditional', 'classic', 'original']
        age_score += sum(2 for word in establishment_words if word in content_lower)

        # Reference indicators (suggests accumulated knowledge)
        reference_indicators = content_lower.count('reference') + content_lower.count('source') + content_lower.count('citation')
        age_score += reference_indicators

        # Long-term words
        longterm_words = ['always', 'never', 'forever', 'permanent', 'eternal', 'ancient', 'old']
        age_score += sum(1 for word in longterm_words if word in content_lower)

        # Convert to modest stat bonus (age brings wisdom, not necessarily raw power)
        hp_bonus = min(15, int(age_score * 1.5))
        attack_bonus = min(8, int(age_score * 0.8))

        return {'hp': hp_bonus, 'attack': attack_bonus}

    def _extract_structured_content(self, content: str) -> Dict[str, List]:
        """Extract structured elements from note content for richer AI context"""
        result = {
            'headers': [],
            'lists': [],
            'numbers': [],
            'code_blocks': [],
            'bold_items': []
        }

        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Extract headers (markdown style)
            if line.startswith('#'):
                header_text = line.lstrip('#').strip()
                if header_text:
                    result['headers'].append(header_text)

            # Extract list items
            elif line.startswith(('-', '*', '+')):
                list_item = line[1:].strip()
                if list_item:
                    result['lists'].append(list_item)

            # Extract numbered lists
            elif re.match(r'^\d+\.', line):
                list_item = re.sub(r'^\d+\.\s*', '', line)
                if list_item:
                    result['lists'].append(list_item)

            # Extract bold/important items
            elif '**' in line:
                bold_items = re.findall(r'\*\*([^*]+)\*\*', line)
                result['bold_items'].extend(bold_items)

        # Extract numbers from entire content
        numbers = re.findall(r'\b\d+\b', content)
        result['numbers'] = [int(n) for n in numbers if 0 < int(n) < 10000]  # Reasonable range

        # Extract code blocks
        code_blocks = re.findall(r'```[\w]*\n([^`]+)\n```', content, re.MULTILINE)
        if code_blocks:
            result['code_blocks'] = [block.strip()[:100] for block in code_blocks[:2]]  # First 2 blocks, truncated

        return result

    def _generate_fallback_narrative(self, title: str, content: str) -> str:
        """Generate rich dungeon master style encounter narrative when AI fails"""
        content_lower = content.lower()

        # Extract specific details from content for richer narratives
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        numbers = re.findall(r'\b\d+\b', content)
        key_phrases = [line for line in lines[:3] if len(line) > 10]  # First few meaningful lines

        # Build rich narrative based on content type
        if any(word in content_lower for word in ['machine learning', 'algorithm', 'neural', 'data']):
            narrative = f"You enter the Sacred Algorithm Sanctum, where the ancient knowledge of '{title}' has crystallized into living code. "
            if numbers:
                narrative += f"The air crackles with {numbers[0]} different patterns of mystical energy, each representing a layer of understanding. "
            if key_phrases:
                narrative += f"Glowing runes spell out the eternal truth: '{key_phrases[0][:60]}...' "
            narrative += "Data streams flow like luminous rivers through the ethereal space, while spectral frameworks stand sentinel over the accumulated wisdom."
            return narrative

        elif any(word in content_lower for word in ['parking', 'spot', 'lot', 'space']):
            narrative = f"You approach the Phantom Parking Realm, where the faded markings of '{title}' still glow with spectral energy. "
            if numbers:
                narrative += f"Exactly {numbers[0]} ghostly vehicles materialize and vanish in endless cycles. "
            if key_phrases:
                narrative += f"Ancient inscriptions read: '{key_phrases[0][:50]}...' "
            narrative += "The asphalt beneath your feet pulses with forgotten memories of countless arrivals and departures."
            return narrative

        elif any(word in content_lower for word in ['recipe', 'cook', 'ingredient', 'bake', 'food']):
            narrative = f"You enter the Mystical Culinary Chamber, where the essence of '{title}' has manifested as living cuisine. "
            if numbers:
                narrative += f"The sacred recipe calls for {numbers[0]} mystical components, each floating in shimmering suspension. "
            if key_phrases:
                narrative += f"The air whispers ancient culinary secrets: '{key_phrases[0][:50]}...' "
            narrative += "Spectral ingredients dance through the air while phantom aromas awaken primordial hunger in your soul."
            return narrative

        elif any(word in content_lower for word in ['meeting', 'agenda', 'deadline', 'office']):
            narrative = f"You find yourself in the Ethereal Conference Dimension, where echoes of '{title}' still reverberate through spacetime. "
            if numbers:
                narrative += f"The phantom agenda lists {numbers[0]} items that will never be completed. "
            if key_phrases:
                narrative += f"Ghostly voices discuss: '{key_phrases[0][:50]}...' "
            narrative += "Corporate spirits gather around a table that exists in all timelines simultaneously, their eternal deliberations shaping reality itself."
            return narrative

        elif any(word in content_lower for word in ['code', 'function', 'programming', 'software']):
            narrative = f"You traverse the Digital Plane of '{title}', where lines of code have achieved consciousness. "
            if numbers:
                narrative += f"Exactly {numbers[0]} functions execute in parallel dimensions, their outputs weaving reality itself. "
            if key_phrases:
                narrative += f"The core algorithm declares: '{key_phrases[0][:50]}...' "
            narrative += "Variables drift through the air like glowing moths while conditional statements branch into infinite possibilities."
            return narrative

        elif any(word in content_lower for word in ['network', 'ip', 'server', 'connection']):
            narrative = f"You navigate the Ethereal Network Realm of '{title}', where data flows like rivers of light. "
            if numbers:
                narrative += f"The network topology reveals {numbers[0]} nodes pulsing with digital life. "
            if key_phrases:
                narrative += f"The server speaks in binary tongues: '{key_phrases[0][:50]}...' "
            narrative += "Packets of information swim through fiber-optic streams while routers stand as ancient guardians of the data pathways."
            return narrative

        else:
            # Generic but rich fallback
            narrative = f"You discover the Sanctum of Eternal Knowledge, where the essence of '{title}' has achieved mystical consciousness. "
            if numbers:
                narrative += f"The sacred text contains {numbers[0]} fundamental truths that shape this reality. "
            if key_phrases:
                narrative += f"Ancient wisdom speaks: '{key_phrases[0][:50]}...' "
            narrative += "Reality bends and flows around you as pure knowledge takes physical form, challenging any who dare approach its secrets."
            return narrative

    def _generate_fallback_environment(self, title: str, content: str) -> str:
        """Generate environment description when AI fails"""
        content_lower = content.lower()

        if any(word in content_lower for word in ['parking', 'lot']):
            return "Abandoned Phantom Parking Lot"
        elif any(word in content_lower for word in ['recipe', 'cook']):
            return "Spectral Kitchen of Lost Recipes"
        elif any(word in content_lower for word in ['meeting', 'office']):
            return "Ethereal Conference Chamber"
        elif any(word in content_lower for word in ['code', 'programming']):
            return "Digital Realm of Living Code"
        elif any(word in content_lower for word in ['network', 'ip']):
            return "Cyberspace Nexus"
        elif any(word in content_lower for word in ['shop', 'buy']):
            return "Merchant's Eternal Bazaar"
        else:
            return f"Mystical Sanctuary of {title}"

    def _generate_fallback_name(self, title: str, content: str) -> str:
        """Generate creative enemy name when AI fails"""
        content_lower = content.lower()

        # Detect content patterns and generate appropriate names (order matters!)
        if any(word in content_lower for word in ['recipe', 'cook', 'ingredient', 'bake', 'flour', 'sugar']):
            return f"Culinary Phantom of {title}"
        elif any(word in content_lower for word in ['password', 'login', 'auth', 'secret']):
            return f"Gatekeeper of Hidden Secrets"
        elif any(word in content_lower for word in ['code', 'function', 'class', 'variable', 'algorithm']):
            return f"Digital Scribe of {title}"
        elif any(word in content_lower for word in ['ip', 'address', 'network', 'server', 'router', 'ssid']):
            return f"Subnet Phantom of {title}"
        elif any(word in content_lower for word in ['buy', 'shop', 'purchase', 'item', 'milk', 'bread', 'eggs']):
            return f"Merchant Wraith of Endless Desires"
        elif any(word in content_lower for word in ['meeting', 'agenda', 'discussion', 'deadline']):
            return f"Echo of the {title} Assembly"
        elif any(word in content_lower for word in ['travel', 'trip', 'journey', 'flight', 'hotel']):
            return f"Wandering Spirit of {title}"
        elif any(word in content_lower for word in ['dream', 'sleep', 'night']):
            return f"Oneiric Guardian of {title}"
        elif any(word in content_lower for word in ['money', 'cost', 'price', 'budget']):
            return f"Coinkeeper of {title}"
        elif any(word in content_lower for word in ['health', 'doctor', 'medical']):
            return f"Vitality Warden of {title}"
        else:
            # Generic but more interesting than "Guardian of X"
            mystical_prefixes = ["Essence of", "Spirit of", "Echo of", "Phantom of", "Keeper of"]
            return f"{random.choice(mystical_prefixes)} {title}"

    def _generate_fallback_description(self, title: str, content: str) -> str:
        """Generate enemy description when AI fails"""
        content_lower = content.lower()

        if any(word in content_lower for word in ['recipe', 'cook', 'ingredient', 'bake']):
            return "A chef-like demon wreathed in aromatic smoke, wielding kitchen implements as weapons."
        elif any(word in content_lower for word in ['code', 'function', 'algorithm']):
            return "A mystical programmer, its fingers weaving glowing runes of compiled knowledge."
        elif any(word in content_lower for word in ['ip', 'address', 'network', 'router']):
            return "A translucent entity crackling with digital energy, its form shifting like data packets."
        elif any(word in content_lower for word in ['meeting', 'agenda', 'deadline']):
            return "A suited specter endlessly scribbling notes, its hollow eyes reflecting corporate tedium."
        elif any(word in content_lower for word in ['travel', 'trip', 'flight', 'hotel']):
            return "A restless wanderer with a map of ethereal destinations, forever planning journeys never taken."
        else:
            return f"A mysterious entity born from the essence of {title}, guarding its secrets fiercely."

    def _generate_fallback_weapon(self, title: str, content: str) -> str:
        """Generate weapon when AI fails"""
        content_lower = content.lower()

        if any(word in content_lower for word in ['recipe', 'cook', 'ingredient', 'bake']):
            return "Flaming Spatula of Culinary Wrath"
        elif any(word in content_lower for word in ['code', 'function', 'algorithm']):
            return "Binary Blade of Compiled Logic"
        elif any(word in content_lower for word in ['password', 'login', 'auth']):
            return "Cryptographic Key of Forbidden Access"
        elif any(word in content_lower for word in ['ip', 'network', 'router']):
            return "Ethernet Lash of Digital Pain"
        elif any(word in content_lower for word in ['meeting', 'agenda', 'deadline']):
            return "Bureaucratic Gavel of Endless Meetings"
        elif any(word in content_lower for word in ['travel', 'trip', 'flight', 'hotel']):
            return "Compass Blade of Wandering Paths"
        else:
            return f"Ethereal Blade of {title}"

    def _generate_fallback_armor(self, title: str, content: str) -> str:
        """Generate armor when AI fails"""
        content_lower = content.lower()

        if any(word in content_lower for word in ['recipe', 'cook', 'ingredient', 'bake']):
            return "Apron of Culinary Mastery"
        elif any(word in content_lower for word in ['code', 'function', 'algorithm']):
            return "Chainmail of Error Handling"
        elif any(word in content_lower for word in ['ip', 'network', 'router']):
            return "Firewall Robes of Packet Protection"
        elif any(word in content_lower for word in ['meeting', 'agenda', 'deadline']):
            return "Corporate Suit of Bureaucratic Defense"
        elif any(word in content_lower for word in ['travel', 'trip', 'flight', 'hotel']):
            return "Traveler's Cloak of Endless Journeys"
        else:
            return f"Mystical Vestments of {title}"


class TinyLlamaProvider(AIProvider):
    """TinyLlama provider - wraps LocalAIClient to implement AIProvider interface"""

    def __init__(self):
        self._client = LocalAIClient()
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize TinyLlama model"""
        self._initialized = self._client.initialize()
        return self._initialized

    def is_available(self) -> bool:
        """Check if TinyLlama is ready"""
        return self._client.available

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Optional[QuizQuestion]:
        """Generate quiz question using TinyLlama"""
        return self._client.generate_quiz_question(note_title, note_content, difficulty)

    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate enemy description using TinyLlama"""
        return self._client.generate_enemy_description(note_title, note_content, base_enemy)

    @property
    def provider_name(self) -> str:
        return "TinyLlama (Local)"


# =============================================================================
# Claude CLI Provider
# =============================================================================

class ClaudeCLIProvider(AIProvider):
    """Claude CLI provider - uses existing Claude Code subscription via CLI"""

    def __init__(self):
        self._available = False
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes

    def initialize(self) -> bool:
        """Check if Claude CLI is available and authenticated"""
        try:
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            self._available = result.returncode == 0
            if self._available:
                print("🤖 Claude CLI detected and ready")
            return self._available
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("🤖 Claude CLI not found - install Claude Code to use this provider")
            self._available = False
            return False

    def is_available(self) -> bool:
        """Check if Claude CLI is ready"""
        return self._available

    def _run_claude(self, prompt: str, timeout: int = 30) -> Optional[str]:
        """Run claude CLI with a prompt and return the response"""
        try:
            result = subprocess.run(
                ['claude', '--print', '--output-format', 'text'],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"🔥 Claude CLI error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("🔥 Claude CLI timed out")
        except Exception as e:
            print(f"🔥 Claude CLI error: {e}")
        return None

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Optional[QuizQuestion]:
        """Generate quiz question using Claude CLI"""
        cache_key = f"quiz_{hash(note_content)}_{difficulty}"

        # Check cache
        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_result

        prompt = f"""Based on this note about "{note_title}":

{note_content[:500]}

Generate a multiple choice quiz question that tests understanding of the key concept.

Create 3 answer options:
1. One correct answer
2. One plausible but incorrect answer (similar to correct but wrong in key detail)
3. One humorous/obviously wrong answer

Format your response exactly as:
QUESTION: [your question here]
CORRECT: [the correct answer]
DECOY: [plausible but incorrect answer]
FUNNY: [humorous wrong answer]
TYPE: [definition/concept/relationship/fact]

Make the decoy answer similar enough to confuse someone who doesn't know the material well."""

        response = self._run_claude(prompt)
        if response:
            quiz = self._parse_quiz_response(response, note_content, difficulty)
            if quiz:
                self._cache[cache_key] = (time.time(), quiz)
                return quiz
        return None

    def _parse_quiz_response(self, response: str, note_content: str, difficulty: int) -> Optional[QuizQuestion]:
        """Parse Claude's quiz response into QuizQuestion object"""
        question_match = re.search(r'QUESTION:\s*(.+?)(?=CORRECT:|$)', response, re.DOTALL)
        correct_match = re.search(r'CORRECT:\s*(.+?)(?=DECOY:|$)', response, re.DOTALL)
        decoy_match = re.search(r'DECOY:\s*(.+?)(?=FUNNY:|$)', response, re.DOTALL)
        funny_match = re.search(r'FUNNY:\s*(.+?)(?=TYPE:|$)', response, re.DOTALL)
        type_match = re.search(r'TYPE:\s*(.+?)$', response, re.DOTALL)

        if question_match and correct_match and decoy_match and funny_match:
            correct_answer = correct_match.group(1).strip()
            decoy_answer = decoy_match.group(1).strip()
            funny_answer = funny_match.group(1).strip()

            options = [correct_answer, decoy_answer, funny_answer]
            random.shuffle(options)
            correct_index = options.index(correct_answer)

            return QuizQuestion(
                question=question_match.group(1).strip(),
                answer=correct_answer,
                difficulty=difficulty,
                question_type=type_match.group(1).strip() if type_match else "concept",
                context=note_content[:200],
                options=options,
                correct_index=correct_index
            )
        return None

    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate enemy description using Claude CLI"""
        cache_key = f"enemy_{hash(note_content)}_{base_enemy}"

        # Check cache
        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_result

        prompt = f"""You are a dungeon master describing a magical encounter. Create a rich, atmospheric description of discovering a mystical realm where the knowledge from this note has come alive:

Title: "{note_title}"
Content: {note_content[:600]}

Write a 3-4 sentence narrative describing the encounter as a dungeon master would. Include specific details from the note content (numbers, names, concepts, actions). Make it magical and immersive, like the knowledge itself has awakened to challenge intruders. Keep it concise but atmospheric.

Write ONLY the narrative description, nothing else."""

        response = self._run_claude(prompt, timeout=45)
        if response:
            enemy_desc = EnemyDescription(
                name=f"Spirit of {note_title}",
                description=f"A mystical entity born from the essence of {note_title}",
                weapon=f"Ethereal Blade of {note_title}",
                armor=f"Mystical Vestments of {note_title}",
                backstory=f"Born from the essence of {note_title}, this creature embodies forgotten knowledge.",
                combat_phrases=[f"Your understanding of {note_title} means nothing to me!"],
                defeat_message=f"The secrets of {note_title}... are yours to claim...",
                victory_message=f"The Spirit of {note_title} has fallen!",
                encounter_narrative=response.strip()
            )
            self._cache[cache_key] = (time.time(), enemy_desc)
            print(f"🎭 Claude CLI generated narrative: {len(response)} chars")
            return enemy_desc
        return None

    @property
    def provider_name(self) -> str:
        return "Claude CLI (Subscription)"


# =============================================================================
# Claude API Provider
# =============================================================================

class ClaudeAPIProvider(AIProvider):
    """Claude API provider - uses Anthropic API with user-provided key"""

    def __init__(self, api_key: str = "", model: str = "claude-sonnet-4-20250514"):
        self._api_key = api_key
        self._model = model
        self._client = None
        self._available = False
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes

    def initialize(self) -> bool:
        """Initialize Anthropic client with API key"""
        if not ANTHROPIC_AVAILABLE:
            print("🤖 Anthropic SDK not installed - run: pip install anthropic")
            return False

        if not self._api_key:
            print("🤖 No API key provided for Claude API")
            return False

        try:
            self._client = anthropic.Anthropic(api_key=self._api_key)
            # Test the connection with a minimal request
            self._client.messages.create(
                model=self._model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            self._available = True
            print(f"🤖 Claude API ready (model: {self._model})")
            return True
        except Exception as e:
            print(f"🤖 Claude API initialization failed: {e}")
            self._available = False
            return False

    def is_available(self) -> bool:
        """Check if Claude API is ready"""
        return self._available

    def _generate_text(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """Generate text using Claude API"""
        if not self._available or not self._client:
            return None

        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"🔥 Claude API error: {e}")
            return None

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Optional[QuizQuestion]:
        """Generate quiz question using Claude API"""
        cache_key = f"quiz_{hash(note_content)}_{difficulty}"

        # Check cache
        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_result

        prompt = f"""Based on this note about "{note_title}":

{note_content[:500]}

Generate a multiple choice quiz question that tests understanding of the key concept.

Create 3 answer options:
1. One correct answer
2. One plausible but incorrect answer (similar to correct but wrong in key detail)
3. One humorous/obviously wrong answer

Format your response exactly as:
QUESTION: [your question here]
CORRECT: [the correct answer]
DECOY: [plausible but incorrect answer]
FUNNY: [humorous wrong answer]
TYPE: [definition/concept/relationship/fact]

Make the decoy answer similar enough to confuse someone who doesn't know the material well."""

        response = self._generate_text(prompt, max_tokens=200)
        if response:
            quiz = self._parse_quiz_response(response, note_content, difficulty)
            if quiz:
                self._cache[cache_key] = (time.time(), quiz)
                return quiz
        return None

    def _parse_quiz_response(self, response: str, note_content: str, difficulty: int) -> Optional[QuizQuestion]:
        """Parse Claude's quiz response into QuizQuestion object"""
        question_match = re.search(r'QUESTION:\s*(.+?)(?=CORRECT:|$)', response, re.DOTALL)
        correct_match = re.search(r'CORRECT:\s*(.+?)(?=DECOY:|$)', response, re.DOTALL)
        decoy_match = re.search(r'DECOY:\s*(.+?)(?=FUNNY:|$)', response, re.DOTALL)
        funny_match = re.search(r'FUNNY:\s*(.+?)(?=TYPE:|$)', response, re.DOTALL)
        type_match = re.search(r'TYPE:\s*(.+?)$', response, re.DOTALL)

        if question_match and correct_match and decoy_match and funny_match:
            correct_answer = correct_match.group(1).strip()
            decoy_answer = decoy_match.group(1).strip()
            funny_answer = funny_match.group(1).strip()

            options = [correct_answer, decoy_answer, funny_answer]
            random.shuffle(options)
            correct_index = options.index(correct_answer)

            return QuizQuestion(
                question=question_match.group(1).strip(),
                answer=correct_answer,
                difficulty=difficulty,
                question_type=type_match.group(1).strip() if type_match else "concept",
                context=note_content[:200],
                options=options,
                correct_index=correct_index
            )
        return None

    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate enemy description using Claude API"""
        cache_key = f"enemy_{hash(note_content)}_{base_enemy}"

        # Check cache
        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_result

        prompt = f"""You are a dungeon master describing a magical encounter. Create a rich, atmospheric description of discovering a mystical realm where the knowledge from this note has come alive:

Title: "{note_title}"
Content: {note_content[:600]}

Write a 3-4 sentence narrative describing the encounter as a dungeon master would. Include specific details from the note content (numbers, names, concepts, actions). Make it magical and immersive, like the knowledge itself has awakened to challenge intruders. Keep it concise but atmospheric.

Write ONLY the narrative description, nothing else."""

        response = self._generate_text(prompt, max_tokens=400)
        if response:
            enemy_desc = EnemyDescription(
                name=f"Spirit of {note_title}",
                description=f"A mystical entity born from the essence of {note_title}",
                weapon=f"Ethereal Blade of {note_title}",
                armor=f"Mystical Vestments of {note_title}",
                backstory=f"Born from the essence of {note_title}, this creature embodies forgotten knowledge.",
                combat_phrases=[f"Your understanding of {note_title} means nothing to me!"],
                defeat_message=f"The secrets of {note_title}... are yours to claim...",
                victory_message=f"The Spirit of {note_title} has fallen!",
                encounter_narrative=response.strip()
            )
            self._cache[cache_key] = (time.time(), enemy_desc)
            print(f"🎭 Claude API generated narrative: {len(response)} chars")
            return enemy_desc
        return None

    def set_model(self, model: str):
        """Change the Claude model being used"""
        self._model = model
        print(f"🤖 Claude API model changed to: {model}")

    @property
    def provider_name(self) -> str:
        return f"Claude API ({self._model.split('-')[1].title()})"


# =============================================================================
# Ollama Provider (Remote GPU)
# =============================================================================

class OllamaProvider(AIProvider):
    """Ollama provider - uses remote Ollama server for GPU-accelerated inference"""

    def __init__(self, host: str = "http://100.86.138.79:11434", model: str = "gemma3:4b"):
        self._host = host.rstrip("/")
        self._model = model
        self._available = False
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._cache_ttl = 300  # 5 minutes

    def initialize(self) -> bool:
        """Test connectivity to Ollama server"""
        import urllib.request
        import urllib.error
        try:
            req = urllib.request.Request(f"{self._host}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                import json as _json
                data = _json.loads(resp.read())
                models = [m.get("name", "") for m in data.get("models", [])]
                # Check if our model is available (match with or without tag)
                model_base = self._model.split(":")[0]
                found = any(model_base in m for m in models)
                if found:
                    self._available = True
                    print(f"🦙 Ollama ready: {self._model} on {self._host}")
                    return True
                else:
                    print(f"🦙 Ollama server reachable but model '{self._model}' not found. Available: {models}")
                    # Still mark available - the model might be pullable
                    self._available = True
                    return True
        except Exception as e:
            print(f"🦙 Ollama connection failed ({self._host}): {e}")
            self._available = False
            return False

    def is_available(self) -> bool:
        return self._available

    def _generate_text(self, prompt: str, max_tokens: int = 200) -> Optional[str]:
        """Generate text using Ollama HTTP API"""
        if not self._available:
            return None

        import urllib.request
        import urllib.error
        import json as _json

        payload = _json.dumps({
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7,
            }
        }).encode("utf-8")

        try:
            req = urllib.request.Request(
                f"{self._host}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = _json.loads(resp.read())
                return data.get("response", "")
        except Exception as e:
            print(f"🦙 Ollama generation error: {e}")
            return None

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Optional[QuizQuestion]:
        """Generate quiz question using Ollama"""
        cache_key = f"quiz_{hash(note_content)}_{difficulty}"

        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_result

        prompt = f"""Based on this note about "{note_title}":

{note_content[:500]}

Generate a multiple choice quiz question that tests understanding of the key concept.

Create 3 answer options:
1. One correct answer
2. One plausible but incorrect answer (similar to correct but wrong in key detail)
3. One humorous/obviously wrong answer

Format your response exactly as:
QUESTION: [your question here]
CORRECT: [the correct answer]
DECOY: [plausible but incorrect answer]
FUNNY: [humorous wrong answer]
TYPE: [definition/concept/relationship/fact]

Make the decoy answer similar enough to confuse someone who doesn't know the material well."""

        response = self._generate_text(prompt, max_tokens=200)
        if response:
            quiz = self._parse_quiz_response(response, note_content, difficulty)
            if quiz:
                self._cache[cache_key] = (time.time(), quiz)
                return quiz
        return None

    def _parse_quiz_response(self, response: str, note_content: str, difficulty: int) -> Optional[QuizQuestion]:
        """Parse Ollama's quiz response into QuizQuestion object"""
        question_match = re.search(r'QUESTION:\s*(.+?)(?=CORRECT:|$)', response, re.DOTALL)
        correct_match = re.search(r'CORRECT:\s*(.+?)(?=DECOY:|$)', response, re.DOTALL)
        decoy_match = re.search(r'DECOY:\s*(.+?)(?=FUNNY:|$)', response, re.DOTALL)
        funny_match = re.search(r'FUNNY:\s*(.+?)(?=TYPE:|$)', response, re.DOTALL)
        type_match = re.search(r'TYPE:\s*(.+?)$', response, re.DOTALL)

        if question_match and correct_match and decoy_match and funny_match:
            correct_answer = correct_match.group(1).strip()
            decoy_answer = decoy_match.group(1).strip()
            funny_answer = funny_match.group(1).strip()

            options = [correct_answer, decoy_answer, funny_answer]
            random.shuffle(options)
            correct_index = options.index(correct_answer)

            return QuizQuestion(
                question=question_match.group(1).strip(),
                answer=correct_answer,
                difficulty=difficulty,
                question_type=type_match.group(1).strip() if type_match else "concept",
                context=note_content[:200],
                options=options,
                correct_index=correct_index
            )
        return None

    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate enemy description using Ollama"""
        cache_key = f"enemy_{hash(note_content)}_{base_enemy}"

        if cache_key in self._cache:
            cached_time, cached_result = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_result

        prompt = f"""You are a dungeon master describing a magical encounter. Create a rich, atmospheric description of discovering a mystical realm where the knowledge from this note has come alive:

Title: "{note_title}"
Content: {note_content[:600]}

Write a 3-4 sentence narrative describing the encounter as a dungeon master would. Include specific details from the note content (numbers, names, concepts, actions). Make it magical and immersive, like the knowledge itself has awakened to challenge intruders. Keep it concise but atmospheric.

Write ONLY the narrative description, nothing else."""

        response = self._generate_text(prompt, max_tokens=400)
        if response:
            enemy_desc = EnemyDescription(
                name=f"Spirit of {note_title}",
                description=f"A mystical entity born from the essence of {note_title}",
                weapon=f"Ethereal Blade of {note_title}",
                armor=f"Mystical Vestments of {note_title}",
                backstory=f"Born from the essence of {note_title}, this creature embodies forgotten knowledge.",
                combat_phrases=[f"Your understanding of {note_title} means nothing to me!"],
                defeat_message=f"The secrets of {note_title}... are yours to claim...",
                victory_message=f"The Spirit of {note_title} has fallen!",
                encounter_narrative=response.strip()
            )
            self._cache[cache_key] = (time.time(), enemy_desc)
            print(f"🦙 Ollama generated narrative: {len(response)} chars")
            return enemy_desc
        return None

    @property
    def provider_name(self) -> str:
        return f"Ollama ({self._model})"


# =============================================================================
# AI Provider Manager
# =============================================================================

class AIProviderManager:
    """Manages AI providers and handles fallback logic"""

    def __init__(self):
        self._providers: Dict[str, AIProvider] = {}
        self._current_provider_type: str = "tinyllama"
        self._initialization_attempted = False
        self._initialization_complete = False
        self._initialization_thread = None
        self._fallback_generator = LocalAIClient()  # For fallback quiz generation

    def register_provider(self, provider_type: str, provider: AIProvider):
        """Register a provider"""
        self._providers[provider_type] = provider

    def set_provider(self, provider_type: str) -> bool:
        """Set the current provider type"""
        if provider_type in self._providers:
            self._current_provider_type = provider_type
            return True
        return False

    def get_current_provider(self) -> Optional[AIProvider]:
        """Get the current active provider based on game settings"""
        # Import settings to get current provider preference
        from game_data import game_settings, AIProviderType

        # Map AIProviderType enum to provider keys
        provider_map = {
            AIProviderType.TINYLLAMA: "tinyllama",
            AIProviderType.CLAUDE_CLI: "claude_cli",
            AIProviderType.CLAUDE_API: "claude_api",
            AIProviderType.OLLAMA: "ollama",
        }

        # Update internal state to match settings
        self._current_provider_type = provider_map.get(game_settings.ai_provider, "tinyllama")

        # Lazily create providers if not yet initialized
        if not self._providers:
            self._providers = {
                "tinyllama": TinyLlamaProvider(),
                "claude_cli": ClaudeCLIProvider(),
                "claude_api": ClaudeAPIProvider(
                    api_key=game_settings.claude_api_key,
                    model=game_settings.claude_model
                ),
                "ollama": OllamaProvider(
                    host=game_settings.ollama_host,
                    model=game_settings.ollama_model
                ),
            }

        return self._providers.get(self._current_provider_type)

    def initialize(self, provider_type: str = None, api_key: str = "", model: str = "claude-sonnet-4-20250514"):
        """Initialize the AI system with specified provider"""
        if self._initialization_attempted:
            return

        self._initialization_attempted = True

        # Import settings
        from game_data import game_settings, AIProviderType

        # Use settings if not explicitly provided
        if provider_type is None:
            provider_type = game_settings.ai_provider.value
        if not api_key:
            api_key = game_settings.claude_api_key
        if model == "claude-sonnet-4-20250514":
            model = game_settings.claude_model

        # Create providers
        self._providers = {
            "tinyllama": TinyLlamaProvider(),
            "claude_cli": ClaudeCLIProvider(),
            "claude_api": ClaudeAPIProvider(api_key=api_key, model=model),
            "ollama": OllamaProvider(
                host=game_settings.ollama_host,
                model=game_settings.ollama_model
            ),
        }

        self._current_provider_type = provider_type

        def init_thread():
            try:
                # Initialize the selected provider
                provider = self._providers.get(provider_type)
                if provider:
                    success = provider.initialize()
                    if not success and provider_type != "tinyllama":
                        # Fallback to TinyLlama if preferred provider fails
                        print(f"⚠️ {provider_type} failed, falling back to TinyLlama")
                        tinyllama = self._providers.get("tinyllama")
                        if tinyllama:
                            tinyllama.initialize()
                            self._current_provider_type = "tinyllama"
            finally:
                self._initialization_complete = True

        # Run initialization in background
        self._initialization_thread = threading.Thread(target=init_thread, daemon=True)
        self._initialization_thread.start()

    def wait_for_initialization(self, timeout: float = 3.0) -> bool:
        """Wait for initialization to complete"""
        if self._initialization_complete:
            provider = self.get_current_provider()
            return provider.is_available() if provider else False
        if not self._initialization_attempted:
            self.initialize()
        if self._initialization_thread:
            self._initialization_thread.join(timeout=timeout)
        provider = self.get_current_provider()
        return provider.is_available() if provider else False

    def is_available(self) -> bool:
        """Check if current provider is available"""
        provider = self.get_current_provider()
        return provider.is_available() if provider else False

    def reinitialize_provider(self) -> None:
        """Rebuild and re-initialize the current provider from latest settings.

        Called when the user changes ai_provider, ollama_host, or ollama_model
        at runtime so the live provider instance reflects the new config.
        """
        from game_data import game_settings, AIProviderType

        # Sync _current_provider_type from latest settings
        provider_map = {
            AIProviderType.TINYLLAMA: "tinyllama",
            AIProviderType.CLAUDE_CLI: "claude_cli",
            AIProviderType.CLAUDE_API: "claude_api",
            AIProviderType.OLLAMA: "ollama",
        }
        self._current_provider_type = provider_map.get(game_settings.ai_provider, "tinyllama")

        # Rebuild the specific provider that changed
        provider_key = self._current_provider_type
        if provider_key == "ollama":
            self._providers["ollama"] = OllamaProvider(
                host=game_settings.ollama_host,
                model=game_settings.ollama_model
            )
        elif provider_key == "claude_api":
            self._providers["claude_api"] = ClaudeAPIProvider(
                api_key=game_settings.claude_api_key,
                model=game_settings.claude_model
            )
        elif provider_key == "claude_cli":
            self._providers["claude_cli"] = ClaudeCLIProvider()
        elif provider_key == "tinyllama":
            self._providers["tinyllama"] = TinyLlamaProvider()

        # Re-initialize in background
        self._initialization_complete = False

        def reinit_thread():
            try:
                provider = self._providers.get(provider_key)
                if provider:
                    success = provider.initialize()
                    if not success and provider_key != "tinyllama":
                        print(f"⚠️ {provider_key} re-init failed, falling back to TinyLlama")
                        tinyllama = self._providers.get("tinyllama")
                        if tinyllama and not tinyllama.is_available():
                            tinyllama.initialize()
                        self._current_provider_type = "tinyllama"
            finally:
                self._initialization_complete = True

        self._initialization_thread = threading.Thread(target=reinit_thread, daemon=True)
        self._initialization_thread.start()

    @property
    def initialization_status(self) -> str:
        """Get current initialization status"""
        if not self._initialization_attempted:
            return "not_started"
        elif not self._initialization_complete:
            return "initializing"
        elif self.is_available():
            return "ready"
        else:
            return "failed"

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> QuizQuestion:
        """Generate quiz question with provider fallback"""
        provider = self.get_current_provider()
        if provider and provider.is_available():
            try:
                quiz = provider.generate_quiz_question(note_title, note_content, difficulty)
                if quiz:
                    return quiz
            except Exception as e:
                print(f"AI quiz generation failed: {e}")

        # Fallback to regex-based generation
        return self._fallback_quiz_generation(note_title, note_content)

    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate enemy description with provider"""
        provider = self.get_current_provider()
        if provider and provider.is_available():
            try:
                return provider.generate_enemy_description(note_title, note_content, base_enemy)
            except Exception as e:
                print(f"AI enemy generation failed: {e}")
        return None

    def _fallback_quiz_generation(self, note_title: str, note_content: str) -> QuizQuestion:
        """Fallback quiz generation using regex patterns"""
        content = note_content.lower()

        # Try to find definition patterns
        definition_match = re.search(r'(.+?)\s+is\s+(.+?)[.\n]', content)
        if definition_match:
            concept = definition_match.group(1).strip()
            definition = definition_match.group(2).strip()

            question = f"What is {concept}?"
            correct = definition[:50]
            decoy = f"A type of {concept.split()[-1] if concept.split() else 'concept'}"
            funny = "A magical unicorn that grants wishes"

            options = [correct, decoy, funny]
            random.shuffle(options)
            correct_index = options.index(correct)

            return QuizQuestion(
                question=question,
                answer=correct,
                difficulty=1,
                question_type="definition",
                context=note_content[:200],
                options=options,
                correct_index=correct_index
            )

        # Generic fallback
        fallback_data = [
            (f"What category does '{note_title}' belong to?", "knowledge", "random stuff", "interdimensional portals"),
            (f"When might you use '{note_title}'?", "when learning", "never", "during zombie apocalypse"),
            (f"Why might '{note_title}' be important?", "for understanding", "it's not important", "to summon dragons"),
        ]

        question_text, correct, decoy, funny = random.choice(fallback_data)
        options = [correct, decoy, funny]
        random.shuffle(options)
        correct_index = options.index(correct)

        return QuizQuestion(
            question=question_text,
            answer=correct,
            difficulty=1,
            question_type="general",
            context=note_content[:200],
            options=options,
            correct_index=correct_index
        )

    def validate_answer(self, user_answer: str, correct_answer: str, ai_question: bool = False) -> bool:
        """Validate answer with improved matching"""
        user_lower = user_answer.lower().strip()
        correct_lower = correct_answer.lower().strip()

        # Exact match
        if user_lower == correct_lower:
            return True

        # For AI-generated questions, use more sophisticated matching
        if ai_question and self.is_available():
            correct_words = set(word for word in correct_lower.split() if len(word) > 2)
            user_words = set(word for word in user_lower.split() if len(word) > 2)

            if correct_words and len(user_words.intersection(correct_words)) / len(correct_words) >= 0.5:
                return True

        # Fallback to simple word matching
        return any(word in user_lower for word in correct_lower.split() if len(word) > 2)


# =============================================================================
# Legacy AIEnhancedQuizSystem (kept for backwards compatibility)
# =============================================================================

class AIEnhancedQuizSystem:
    """Enhanced quiz system using local TinyLlama with fallbacks"""

    def __init__(self):
        self.local_ai = LocalAIClient()
        self.ai_available = False
        self.initialization_attempted = False
        self.initialization_complete = False
        self.initialization_thread = None

    def initialize(self):
        """Initialize the AI system (runs in background thread)"""
        if self.initialization_attempted:
            return

        self.initialization_attempted = True

        def init_thread():
            try:
                self.ai_available = self.local_ai.initialize()
            finally:
                self.initialization_complete = True

        # Run initialization in background to avoid blocking the game
        self.initialization_thread = threading.Thread(target=init_thread, daemon=True)
        self.initialization_thread.start()

    def wait_for_initialization(self, timeout: float = 3.0) -> bool:
        """Wait for AI initialization to complete, up to timeout seconds"""
        if self.initialization_complete:
            return self.ai_available
        if not self.initialization_attempted:
            self.initialize()
        if self.initialization_thread:
            self.initialization_thread.join(timeout=timeout)
        return self.ai_available

    @property
    def initialization_status(self) -> str:
        """Get current initialization status"""
        if not self.initialization_attempted:
            return "not_started"
        elif not self.initialization_complete:
            return "initializing"
        elif self.ai_available:
            return "ready"
        else:
            return "failed"

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> QuizQuestion:
        """Generate quiz question with AI fallback"""
        if self.ai_available:
            try:
                ai_quiz = self.local_ai.generate_quiz_question(note_title, note_content, difficulty)
                if ai_quiz:
                    return ai_quiz
            except Exception as e:
                print(f"AI quiz generation failed: {e}")

        # Fallback to regex-based generation
        return self._fallback_quiz_generation(note_title, note_content)

    def _fallback_quiz_generation(self, note_title: str, note_content: str) -> QuizQuestion:
        """Fallback quiz generation using regex patterns with multiple choice"""
        content = note_content.lower()
        import random

        # Try to find definition patterns
        definition_match = re.search(r'(.+?)\s+is\s+(.+?)[.\n]', content)
        if definition_match:
            concept = definition_match.group(1).strip()
            definition = definition_match.group(2).strip()

            question = f"What is {concept}?"
            correct = definition[:50]
            decoy = f"A type of {concept.split()[-1] if concept.split() else 'concept'}"
            funny = "A magical unicorn that grants wishes"

            options = [correct, decoy, funny]
            random.shuffle(options)
            correct_index = options.index(correct)

            return QuizQuestion(
                question=question,
                answer=correct,
                difficulty=1,
                question_type="definition",
                context=note_content[:200],
                options=options,
                correct_index=correct_index
            )

        # Try to find list items
        list_match = re.search(r'[-*]\s+(.+)', content)
        if list_match:
            item = list_match.group(1).strip()

            question = f"Name something related to {note_title}"
            correct = item[:50]
            decoy = f"Something about {note_title.split()[0] if note_title.split() else 'notes'}"
            funny = "Pizza delivery instructions"

            options = [correct, decoy, funny]
            random.shuffle(options)
            correct_index = options.index(correct)

            return QuizQuestion(
                question=question,
                answer=correct,
                difficulty=1,
                question_type="list",
                context=note_content[:200],
                options=options,
                correct_index=correct_index
            )

        # Extract first sentence
        first_sentence = re.search(r'^([^.!?]+[.!?])', content.strip())
        if first_sentence:
            sentence = first_sentence.group(1).strip()
            if len(sentence) < 100:
                question = f"Complete this from {note_title}: '{sentence[:30]}...'"
                correct = sentence[30:80] if len(sentence) > 30 else sentence
                decoy = f"...something about {note_title.split()[0] if note_title.split() else 'notes'}"
                funny = "...and then the aliens arrived"

                options = [correct, decoy, funny]
                random.shuffle(options)
                correct_index = options.index(correct)

                return QuizQuestion(
                    question=question,
                    answer=correct,
                    difficulty=1,
                    question_type="completion",
                    context=note_content[:200],
                    options=options,
                    correct_index=correct_index
                )

        # Fallback questions
        fallback_data = [
            (f"What category does '{note_title}' belong to?", "knowledge", "random stuff", "interdimensional portals"),
            (f"When might you use '{note_title}'?", "when learning", "never", "during zombie apocalypse"),
            (f"Why might '{note_title}' be important?", "for understanding", "it's not important", "to summon dragons"),
        ]

        question_text, correct, decoy, funny = random.choice(fallback_data)
        options = [correct, decoy, funny]
        random.shuffle(options)
        correct_index = options.index(correct)

        return QuizQuestion(
            question=question_text,
            answer=correct,
            difficulty=1,
            question_type="general",
            context=note_content[:200],
            options=options,
            correct_index=correct_index
        )

    def generate_enemy_description(self, note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
        """Generate enemy description with AI"""
        if self.ai_available:
            try:
                return self.local_ai.generate_enemy_description(note_title, note_content, base_enemy)
            except Exception as e:
                print(f"AI enemy generation failed: {e}")

        return None

    def validate_answer(self, user_answer: str, correct_answer: str, ai_question: bool = False) -> bool:
        """Validate answer with improved matching for AI questions"""
        user_lower = user_answer.lower().strip()
        correct_lower = correct_answer.lower().strip()

        # Exact match
        if user_lower == correct_lower:
            return True

        # For AI-generated questions, use more sophisticated matching
        if ai_question and self.ai_available:
            # Check if user answer contains key words from correct answer
            correct_words = set(word for word in correct_lower.split() if len(word) > 2)
            user_words = set(word for word in user_lower.split() if len(word) > 2)

            # If 50% of important words match, consider it correct
            if correct_words and len(user_words.intersection(correct_words)) / len(correct_words) >= 0.5:
                return True

        # Fallback to simple word matching
        return any(word in user_lower for word in correct_lower.split() if len(word) > 2)

# =============================================================================
# Global Instances and Functions
# =============================================================================

# New multi-provider manager (preferred)
ai_provider_manager = AIProviderManager()

# Legacy instance for backwards compatibility
ai_quiz_system = AIEnhancedQuizSystem()


def initialize_ai():
    """Initialize the AI system - call this on game startup"""
    # Use the new provider manager
    ai_provider_manager.initialize()
    # Also initialize legacy system for backwards compatibility
    ai_quiz_system.initialize()


def is_ai_available(wait_timeout: float = 1.0) -> bool:
    """Check if AI is available, with optional brief wait for initialization"""
    # Try new provider manager first
    if ai_provider_manager._initialization_attempted:
        if ai_provider_manager._initialization_complete:
            return ai_provider_manager.is_available()
        return ai_provider_manager.wait_for_initialization(timeout=wait_timeout)

    # Fall back to legacy system
    if ai_quiz_system.initialization_complete:
        return ai_quiz_system.ai_available

    if not ai_quiz_system.initialization_attempted:
        return False

    return ai_quiz_system.wait_for_initialization(timeout=wait_timeout)


def get_current_provider_name() -> str:
    """Get the name of the currently active AI provider"""
    provider = ai_provider_manager.get_current_provider()
    if provider:
        return provider.provider_name
    return "None"


# Sync wrapper functions for use in the main game
def sync_generate_quiz_question(note_title: str, note_content: str, difficulty: int = 1) -> QuizQuestion:
    """Synchronous wrapper for quiz generation"""
    # Use new provider manager if initialized
    if ai_provider_manager._initialization_attempted:
        return ai_provider_manager.generate_quiz_question(note_title, note_content, difficulty)
    # Fall back to legacy system
    return ai_quiz_system.generate_quiz_question(note_title, note_content, difficulty)


def sync_generate_enemy_description(note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
    """Synchronous wrapper for enemy description generation"""
    # Use new provider manager if initialized
    if ai_provider_manager._initialization_attempted:
        return ai_provider_manager.generate_enemy_description(note_title, note_content, base_enemy)
    # Fall back to legacy system
    return ai_quiz_system.generate_enemy_description(note_title, note_content, base_enemy)