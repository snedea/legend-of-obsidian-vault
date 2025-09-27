"""
Quiz screen for knowledge-based combat in Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input
from textual import events

# Import will be updated after refactor
from obsidian import vault


class QuizScreen(Screen):
    """Quiz question for bonus combat damage"""

    def __init__(self, enemy, combat_screen):
        super().__init__()
        self.enemy = enemy
        self.combat_screen = combat_screen
        self.question, self.answer = vault.generate_quiz_question(
            type('Note', (), {
                'title': enemy.note_title,
                'content': enemy.note_content
            })()
        )

    def compose(self) -> ComposeResult:
        yield Static("Knowledge Strike!", classes="header")
        yield Static("=-" * 40, classes="separator")
        yield Static(f"Facing: {self.enemy.name}")

        # Show AI status for quiz
        try:
            from brainbot import is_ai_available
            if is_ai_available():
                yield Static("🧠 AI-Enhanced Question", classes="stats")
            else:
                yield Static("📝 Pattern-Based Question", classes="stats")
        except ImportError:
            yield Static("📝 Pattern-Based Question", classes="stats")

        yield Static("")
        yield Static("Answer correctly for a CRITICAL HIT!")
        yield Static("")
        yield Static(f"Question: {self.question}")
        yield Static("")
        yield Input(placeholder="Your answer...", id="answer")
        yield Static("")
        yield Static("(Enter) to answer, (Escape) to cancel")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Check quiz answer with AI-enhanced validation"""
        user_answer = event.value.strip()

        # Try AI-enhanced answer validation
        correct = False
        try:
            from brainbot import ai_quiz_system, is_ai_available
            if is_ai_available():
                correct = ai_quiz_system.validate_answer(user_answer, self.answer, ai_question=True)
            else:
                # Fallback to simple matching
                user_lower = user_answer.lower()
                correct_lower = self.answer.lower()
                correct = any(word in user_lower for word in correct_lower.split() if len(word) > 2)
        except Exception as e:
            # Fallback to simple matching
            user_lower = user_answer.lower()
            correct_lower = self.answer.lower()
            correct = any(word in user_lower for word in correct_lower.split() if len(word) > 2)

        self.app.pop_screen()
        self.combat_screen.quiz_attack(correct)

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.pop_screen()