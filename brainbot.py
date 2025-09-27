"""
BrainBot AI Integration for Legend of the Obsidian Vault
Direct integration with TinyLlama model for intelligent quiz generation
"""
import re
import random
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

# Try to import the AI libraries
try:
    from llama_cpp import Llama
    from huggingface_hub import hf_hub_download
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    Llama = None
    hf_hub_download = None

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

@dataclass
class EnemyDescription:
    """AI-generated enemy description"""
    backstory: str
    combat_phrases: List[str]
    defeat_message: str
    victory_message: str

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
        if not AI_AVAILABLE:
            print("🤖 AI libraries not available - using fallback mode")
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

    def generate_text(self, prompt: str, max_tokens: int = 150) -> Optional[str]:
        """Generate text using local TinyLlama model"""
        if not self.available or not self.model:
            return None

        try:
            # Create a system prompt for quiz generation
            system_prompt = """You are a helpful AI that creates quiz questions from notes.
Generate clear, educational questions that test understanding of key concepts.
Be concise and focused."""

            # Format the prompt
            full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>\n"

            # Generate response
            response = self.model(
                full_prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stop=["<|user|>", "<|system|>", "\n\n"],
                echo=False
            )

            if response and "choices" in response and response["choices"]:
                return response["choices"][0]["text"].strip()

        except Exception as e:
            print(f"🔥 AI generation error: {e}")

        return None

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Optional[QuizQuestion]:
        """Generate an intelligent quiz question from note content"""
        cache_key = f"quiz_{hash(note_content)}_{difficulty}"

        # Check cache
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_result

        # Create context-aware prompt
        prompt = f"""Based on this note about "{note_title}":

{note_content[:500]}

Generate a quiz question that tests understanding of the key concept.

Format your response exactly as:
QUESTION: [your question here]
ANSWER: [short answer]
TYPE: [definition/concept/relationship/fact]

Make it challenging but fair."""

        response = self.generate_text(prompt, max_tokens=100)

        if response:
            # Parse the AI response
            question_match = re.search(r'QUESTION:\s*(.+?)(?=ANSWER:|$)', response, re.DOTALL)
            answer_match = re.search(r'ANSWER:\s*(.+?)(?=TYPE:|$)', response, re.DOTALL)
            type_match = re.search(r'TYPE:\s*(.+?)$', response, re.DOTALL)

            if question_match and answer_match:
                quiz = QuizQuestion(
                    question=question_match.group(1).strip(),
                    answer=answer_match.group(1).strip(),
                    difficulty=difficulty,
                    question_type=type_match.group(1).strip() if type_match else "concept",
                    context=note_content[:200]
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

        prompt = f"""Create a fantasy enemy based on the note "{note_title}" and base creature "{base_enemy}":

{note_content[:300]}

Generate:
1. A brief backstory (2-3 sentences) explaining why this {base_enemy} guards this knowledge
2. 3 combat phrases it might say during battle
3. A defeat message when you beat it
4. A victory message if it beats you

Keep it fantasy-themed and related to the note content. Be creative but respectful."""

        response = self.generate_text(prompt, max_tokens=200)

        if response:
            # Simple parsing - in a real implementation you'd want more robust parsing
            lines = [line.strip() for line in response.split('\n') if line.strip()]

            if len(lines) >= 4:
                description = EnemyDescription(
                    backstory=" ".join(lines[:2]),
                    combat_phrases=lines[2:5] if len(lines) >= 5 else lines[2:4],
                    defeat_message=lines[-2] if len(lines) > 1 else "The enemy falls!",
                    victory_message=lines[-1] if lines else "You have been defeated!"
                )

                # Cache the result
                self.cache[cache_key] = (time.time(), description)
                return description

        return None

class AIEnhancedQuizSystem:
    """Enhanced quiz system using local TinyLlama with fallbacks"""

    def __init__(self):
        self.local_ai = LocalAIClient()
        self.ai_available = False
        self.initialization_attempted = False

    def initialize(self):
        """Initialize the AI system (runs in background thread)"""
        if self.initialization_attempted:
            return

        self.initialization_attempted = True

        def init_thread():
            self.ai_available = self.local_ai.initialize()

        # Run initialization in background to avoid blocking the game
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()

    def generate_quiz_question(self, note_title: str, note_content: str, difficulty: int = 1) -> Tuple[str, str]:
        """Generate quiz question with AI fallback"""
        if self.ai_available:
            try:
                ai_quiz = self.local_ai.generate_quiz_question(note_title, note_content, difficulty)
                if ai_quiz:
                    return ai_quiz.question, ai_quiz.answer
            except Exception as e:
                print(f"AI quiz generation failed: {e}")

        # Fallback to regex-based generation
        return self._fallback_quiz_generation(note_title, note_content)

    def _fallback_quiz_generation(self, note_title: str, note_content: str) -> Tuple[str, str]:
        """Fallback quiz generation using regex patterns"""
        content = note_content.lower()

        # Try to find definition patterns
        definition_match = re.search(r'(.+?)\s+is\s+(.+?)[.\n]', content)
        if definition_match:
            concept = definition_match.group(1).strip()
            definition = definition_match.group(2).strip()
            return f"What is {concept}?", definition[:50]

        # Try to find list items
        list_match = re.search(r'[-*]\s+(.+)', content)
        if list_match:
            item = list_match.group(1).strip()
            return f"Name something related to {note_title}", item[:50]

        # Extract first sentence
        first_sentence = re.search(r'^([^.!?]+[.!?])', content.strip())
        if first_sentence:
            sentence = first_sentence.group(1).strip()
            if len(sentence) < 100:
                return f"Complete: {sentence[:50]}...", sentence[50:100]

        # Fallback questions
        fallback_questions = [
            (f"What category does {note_title} belong to?", "knowledge"),
            (f"When did you last think about {note_title}?", "recently"),
            (f"Why is {note_title} important?", "learning"),
        ]

        return random.choice(fallback_questions)

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

# Global AI system instance
ai_quiz_system = AIEnhancedQuizSystem()

def initialize_ai():
    """Initialize the AI system - call this on game startup"""
    ai_quiz_system.initialize()

def is_ai_available() -> bool:
    """Check if AI is available"""
    return ai_quiz_system.ai_available

# Sync wrapper functions for use in the main game
def sync_generate_quiz_question(note_title: str, note_content: str, difficulty: int = 1) -> Tuple[str, str]:
    """Synchronous wrapper for quiz generation"""
    return ai_quiz_system.generate_quiz_question(note_title, note_content, difficulty)

def sync_generate_enemy_description(note_title: str, note_content: str, base_enemy: str) -> Optional[EnemyDescription]:
    """Synchronous wrapper for enemy description generation"""
    return ai_quiz_system.generate_enemy_description(note_title, note_content, base_enemy)