"""
Quiz screen for knowledge-based combat in Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.containers import Container
from textual import events

# Import will be updated after refactor
from obsidian import vault


class QuizScreen(Screen):
    """Quiz question for bonus combat damage"""

    def __init__(self, enemy, combat_screen):
        super().__init__()
        self.enemy = enemy
        self.combat_screen = combat_screen

        # Get quiz question from AI system
        try:
            from brainbot import sync_generate_quiz_question
            self.quiz = sync_generate_quiz_question(enemy.note_title, enemy.note_content)
        except Exception as e:
            # Fallback to old system
            question, answer = vault.generate_quiz_question(
                type('Note', (), {
                    'title': enemy.note_title,
                    'content': enemy.note_content
                })()
            )
            # Create a basic QuizQuestion object for compatibility
            from brainbot import QuizQuestion
            self.quiz = QuizQuestion(
                question=question,
                answer=answer,
                difficulty=1,
                question_type="fallback",
                context=enemy.note_content[:200],
                options=[answer, "Unknown", "Something else"],
                correct_index=0
            )

    def compose(self) -> ComposeResult:
        with Container(classes="main-border") as container:
            container.border_title = "🧠  KNOWLEDGE STRIKE  🧠"
            container.border_subtitle = "📚 Test Your Wisdom 📚"
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
            yield Static(f"Question: {self.quiz.question}")
            yield Static("")

            # Display multiple choice options
            if self.quiz.options and len(self.quiz.options) == 3:
                for i, option in enumerate(self.quiz.options, 1):
                    yield Button(f"({i}) {option}", id=f"option_{i}")
                yield Static("")
                yield Static("Press (1), (2), or (3) to select answer, (Escape) to cancel")
            else:
                # Fallback to text input for old style questions
                yield Input(placeholder="Your answer...", id="answer")
                yield Static("")
                yield Static("(Enter) to answer, (Escape) to cancel")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Check quiz answer with AI-enhanced validation (for text input fallback)"""
        user_answer = event.value.strip()

        # Try AI-enhanced answer validation
        correct = False
        try:
            from brainbot import ai_quiz_system, is_ai_available
            if is_ai_available():
                correct = ai_quiz_system.validate_answer(user_answer, self.quiz.answer, ai_question=True)
            else:
                # Fallback to simple matching
                user_lower = user_answer.lower()
                correct_lower = self.quiz.answer.lower()
                correct = any(word in user_lower for word in correct_lower.split() if len(word) > 2)
        except Exception as e:
            # Fallback to simple matching
            user_lower = user_answer.lower()
            correct_lower = self.quiz.answer.lower()
            correct = any(word in user_lower for word in correct_lower.split() if len(word) > 2)

        self.app.pop_screen()
        self.combat_screen.quiz_attack(correct)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks for multiple choice"""
        if event.button.id and event.button.id.startswith("option_"):
            option_num = int(event.button.id.split("_")[1])
            selected_index = option_num - 1  # Convert to 0-based index
            correct = (selected_index == self.quiz.correct_index)

            self.app.pop_screen()
            self.combat_screen.quiz_attack(correct)

    def on_key(self, event: events.Key) -> None:
        key = event.key

        if key == "escape":
            self.app.pop_screen()
        elif key in ["1", "2", "3"] and self.quiz.options and len(self.quiz.options) == 3:
            # Multiple choice selection
            selected_index = int(key) - 1  # Convert to 0-based index
            correct = (selected_index == self.quiz.correct_index)

            self.app.pop_screen()
            self.combat_screen.quiz_attack(correct)