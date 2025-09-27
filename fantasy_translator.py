"""
Fantasy Translation Layer - Convert any content into magical concepts

This module transforms technical jargon, mundane content, and everyday concepts
into rich fantasy language that makes every Obsidian note feel like mystical knowledge.
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class FantasyTranslation:
    """A translated concept with fantasy equivalents"""
    original: str
    fantasy_term: str
    description: str
    power_level: str  # "minor", "moderate", "major", "legendary"


class FantasyTranslator:
    """Converts any content into fantasy/magical concepts"""

    def __init__(self):
        self.technical_translations = self._build_technical_translations()
        self.concept_translations = self._build_concept_translations()
        self.mundane_translations = self._build_mundane_translations()
        self.power_words = self._build_power_words()

    def _build_technical_translations(self) -> Dict[str, List[str]]:
        """Technical terms → Magical equivalents"""
        return {
            # Programming Concepts
            "function": ["ritual spell", "arcane method", "mystical procedure", "enchanted formula"],
            "variable": ["essence container", "spirit vessel", "mystical binding", "ethereal holder"],
            "class": ["magical order", "arcane brotherhood", "mystic guild", "spell consortium"],
            "object": ["enchanted artifact", "mystical construct", "arcane creation", "spirit manifestation"],
            "method": ["ritual technique", "magical practice", "arcane discipline", "mystical art"],
            "property": ["inherent power", "mystical attribute", "arcane quality", "spiritual essence"],
            "parameter": ["ritual component", "spell ingredient", "mystical requirement", "arcane element"],
            "return": ["mystical yield", "arcane output", "spiritual manifestation", "magical result"],
            "loop": ["cyclical incantation", "repetitive ritual", "eternal binding", "spiral enchantment"],
            "condition": ["mystical requirement", "arcane prerequisite", "spiritual condition", "magical law"],
            "array": ["ordered crystal matrix", "mystical sequence", "arcane collection", "spirit array"],
            "database": ["ancient tome", "mystical archive", "knowledge codex", "wisdom repository"],
            "server": ["mystical nexus", "arcane conduit", "spirit realm", "magical gateway"],
            "client": ["knowledge seeker", "mystical petitioner", "arcane supplicant", "wisdom pilgrim"],
            "api": ["dimensional gateway", "mystical interface", "arcane portal", "spirit bridge"],
            "url": ["mystical address", "arcane location", "spiritual coordinates", "dimensional path"],
            "file": ["knowledge scroll", "mystical document", "arcane manuscript", "wisdom tablet"],
            "folder": ["knowledge chamber", "mystical vault", "arcane repository", "wisdom sanctuary"],
            "backup": ["spirit echo", "mystical reflection", "arcane duplicate", "ethereal mirror"],
            "cache": ["quick-access crystal", "memory stone", "instant recall gem", "swift knowledge orb"],
            "bug": ["cursed flaw", "malevolent spirit", "arcane corruption", "mystical blight"],
            "error": ["ritual failure", "mystical disruption", "arcane mishap", "spiritual discord"],
            "debug": ["curse breaking", "spirit cleansing", "mystical diagnosis", "arcane investigation"],
            "compile": ["spell weaving", "magical binding", "arcane assembly", "mystical construction"],
            "execute": ["ritual casting", "spell activation", "mystical invocation", "arcane manifestation"],
            "syntax": ["mystical grammar", "arcane structure", "spiritual syntax", "magical composition"],
            "algorithm": ["mystical formula", "arcane procedure", "spiritual method", "magical sequence"],
            "data": ["mystical essence", "arcane information", "spiritual knowledge", "magical substance"],
            "code": ["arcane script", "mystical runes", "spirit writing", "magical inscription"],
            "script": ["mystical scroll", "arcane incantation", "spirit text", "magical manuscript"],
            "commit": ["mystical binding", "arcane inscription", "spiritual commitment", "magical recording"],
            "branch": ["reality divergence", "mystical path", "arcane timeline", "spiritual fork"],
            "merge": ["reality convergence", "mystical union", "arcane combining", "spiritual fusion"],

            # Modern Technology
            "computer": ["thinking crystal", "mystical calculator", "arcane processor", "spirit machine"],
            "phone": ["distant voice crystal", "mystical communicator", "arcane speaking stone", "spirit caller"],
            "internet": ["ethereal web", "mystical network", "arcane connection realm", "spirit information plane"],
            "email": ["mystical message", "arcane correspondence", "spirit letter", "ethereal missive"],
            "website": ["mystical portal", "arcane destination", "spirit gathering place", "ethereal sanctuary"],
            "app": ["mystical tool", "arcane utility", "spirit assistant", "magical instrument"],
            "password": ["mystical key phrase", "arcane entry word", "spirit protection spell", "magical lock code"],
            "security": ["mystical protection", "arcane warding", "spirit shielding", "magical safeguarding"],
            "network": ["mystical web", "arcane connection", "spirit pathway", "magical linkage"],
            "wifi": ["ethereal connection", "mystical air bridge", "arcane wireless bond", "spirit network"],
            "bluetooth": ["mystical short-range bond", "arcane proximity link", "spirit close connection", "magical nearby bridge"],

            # Business/Work Terms
            "meeting": ["mystical gathering", "arcane council", "spirit assembly", "magical congregation"],
            "project": ["mystical endeavor", "arcane undertaking", "spirit quest", "magical mission"],
            "deadline": ["temporal binding", "mystical time limit", "arcane urgency", "spirit pressure"],
            "task": ["mystical duty", "arcane obligation", "spirit mission", "magical assignment"],
            "goal": ["mystical objective", "arcane destination", "spirit target", "magical purpose"],
            "budget": ["resource allocation spell", "mystical fund management", "arcane treasury", "spirit economics"],
            "report": ["mystical chronicle", "arcane documentation", "spirit account", "magical record"],
            "analysis": ["mystical examination", "arcane investigation", "spirit scrutiny", "magical assessment"],
            "strategy": ["mystical battle plan", "arcane approach", "spirit methodology", "magical tactics"],
            "team": ["mystical fellowship", "arcane brotherhood", "spirit alliance", "magical consortium"],
            "manager": ["mystical overseer", "arcane coordinator", "spirit leader", "magical guide"],
            "client": ["mystical patron", "arcane benefactor", "spirit customer", "magical contractor"],
            "feedback": ["mystical response", "arcane reflection", "spirit commentary", "magical insight"],
            "workflow": ["mystical process", "arcane procedure", "spirit methodology", "magical sequence"],

            # Academic/Learning Terms
            "research": ["mystical investigation", "arcane exploration", "spirit inquiry", "magical discovery"],
            "study": ["mystical contemplation", "arcane examination", "spirit learning", "magical absorption"],
            "theory": ["mystical hypothesis", "arcane principle", "spirit concept", "magical understanding"],
            "experiment": ["mystical trial", "arcane test", "spirit probe", "magical exploration"],
            "analysis": ["mystical breakdown", "arcane dissection", "spirit examination", "magical scrutiny"],
            "conclusion": ["mystical revelation", "arcane discovery", "spirit insight", "magical understanding"],
            "hypothesis": ["mystical theory", "arcane supposition", "spirit guess", "magical premise"],
            "data": ["mystical evidence", "arcane information", "spirit facts", "magical observations"],
            "result": ["mystical outcome", "arcane consequence", "spirit conclusion", "magical effect"],
            "reference": ["mystical source", "arcane authority", "spirit citation", "magical foundation"],
        }

    def _build_concept_translations(self) -> Dict[str, List[str]]:
        """Abstract concepts → Fantasy equivalents"""
        return {
            # Time Concepts
            "time": ["temporal flow", "chronological essence", "time stream", "moment magic"],
            "past": ["ancient echoes", "bygone shadows", "temporal memories", "yesterday's spirits"],
            "future": ["approaching destiny", "coming prophecies", "temporal promises", "tomorrow's mysteries"],
            "now": ["present moment magic", "current reality essence", "immediate power", "this-breath eternity"],
            "schedule": ["temporal blueprint", "chronological ritual", "time-binding spell", "moment orchestration"],
            "calendar": ["temporal codex", "chronological tome", "time keeper's scroll", "moment mapping crystal"],

            # Emotional Concepts
            "happiness": ["joy essence", "blissful energy", "light spirit manifestation", "golden emotional aura"],
            "sadness": ["melancholy mist", "sorrowful shadows", "blue emotional essence", "heavy heart magic"],
            "anger": ["rage fire", "fury tempest", "red emotional storm", "burning spirit energy"],
            "fear": ["shadow whispers", "dark anticipation", "cold spirit touch", "uncertainty mist"],
            "love": ["heart binding magic", "soul connection essence", "warm light energy", "unity spirit"],
            "stress": ["pressure shadows", "tension crystals", "overwhelming force", "chaos energy buildup"],

            # Learning Concepts
            "knowledge": ["accumulated wisdom", "learned essence", "understanding crystals", "mental treasures"],
            "wisdom": ["ancient understanding", "deep insight magic", "profound awareness", "elderly spirit knowledge"],
            "skill": ["practiced mastery", "honed ability essence", "developed talent magic", "refined capability"],
            "talent": ["natural gift magic", "inherent ability essence", "born power", "blessed skill energy"],
            "experience": ["lived wisdom", "accumulated moments", "practiced understanding", "time-earned knowledge"],

            # Physical Concepts
            "health": ["life force energy", "bodily harmony magic", "wellness essence", "vital spirit balance"],
            "strength": ["physical power essence", "bodily might magic", "muscular energy", "force manifestation"],
            "energy": ["life spark", "vital essence", "power current", "dynamic spirit force"],
            "rest": ["restoration magic", "renewal essence", "peace energy", "recovery spirit"],
        }

    def _build_mundane_translations(self) -> Dict[str, List[str]]:
        """Everyday items → Magical equivalents"""
        return {
            # Food & Cooking
            "food": ["nourishment essence", "sustenance magic", "life energy source", "bodily fuel crystals"],
            "recipe": ["culinary spell", "cooking incantation", "nourishment ritual", "sustenance formula"],
            "cooking": ["culinary alchemy", "food transmutation", "nourishment crafting", "sustenance magic"],
            "kitchen": ["culinary laboratory", "food alchemist's den", "nourishment workshop", "cooking sanctum"],
            "meal": ["nourishment ritual", "sustenance ceremony", "life energy gathering", "bodily fuel communion"],

            # Transportation
            "car": ["iron steed", "mechanical mount", "wheeled companion", "self-moving chariot"],
            "travel": ["journey magic", "distance conquest", "path walking ritual", "exploration essence"],
            "road": ["earthen pathway", "stone river", "travel channel", "journey conduit"],
            "map": ["territory scroll", "land knowledge crystal", "path-finding tome", "geographic wisdom"],

            # Home & Living
            "house": ["dwelling sanctuary", "life fortress", "personal realm", "existence stronghold"],
            "room": ["personal chamber", "life space", "existence cell", "being container"],
            "furniture": ["life support artifacts", "comfort manifestations", "rest enablers", "dwelling spirits"],
            "cleaning": ["purification ritual", "cleansing magic", "purity restoration", "order manifestation"],

            # Entertainment
            "music": ["harmonic magic", "sound essence", "auditory enchantment", "rhythmic spirit energy"],
            "movie": ["visual story magic", "light narrative", "moving picture spell", "cinematic enchantment"],
            "book": ["knowledge tome", "wisdom vessel", "story container", "learning artifact"],
            "game": ["challenge magic", "competition essence", "play energy", "entertainment spell"],

            # Shopping & Money
            "money": ["exchange essence", "value crystals", "trade energy", "commerce magic"],
            "shopping": ["acquisition ritual", "gathering magic", "procurement quest", "obtaining ceremony"],
            "store": ["goods sanctuary", "trade temple", "commerce hall", "acquisition center"],
            "price": ["exchange requirement", "value demand", "trade cost", "commerce fee"],
        }

    def _build_power_words(self) -> Dict[str, List[str]]:
        """Power level descriptors for different types of magic"""
        return {
            "minor": ["Lesser", "Small", "Basic", "Simple", "Novice", "Beginning"],
            "moderate": ["Intermediate", "Skilled", "Practiced", "Developed", "Refined", "Enhanced"],
            "major": ["Greater", "Powerful", "Advanced", "Masterful", "Superior", "Elevated"],
            "legendary": ["Ultimate", "Supreme", "Transcendent", "Divine", "Mythical", "Eternal"]
        }

    def translate_text(self, text: str, context: str = "general") -> str:
        """Translate entire text passages into fantasy language"""

        # Start with the original text
        fantasy_text = text
        translations_applied = []

        # Apply technical translations first (highest priority)
        for term, fantasy_options in self.technical_translations.items():
            if term.lower() in text.lower():
                fantasy_term = random.choice(fantasy_options)
                # Use case-insensitive replacement but preserve original case
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                fantasy_text = pattern.sub(fantasy_term, fantasy_text)
                translations_applied.append((term, fantasy_term))

        # Apply concept translations
        for concept, fantasy_options in self.concept_translations.items():
            if concept.lower() in fantasy_text.lower():
                fantasy_term = random.choice(fantasy_options)
                pattern = re.compile(re.escape(concept), re.IGNORECASE)
                fantasy_text = pattern.sub(fantasy_term, fantasy_text)
                translations_applied.append((concept, fantasy_term))

        # Apply mundane translations
        for item, fantasy_options in self.mundane_translations.items():
            if item.lower() in fantasy_text.lower():
                fantasy_term = random.choice(fantasy_options)
                pattern = re.compile(re.escape(item), re.IGNORECASE)
                fantasy_text = pattern.sub(fantasy_term, fantasy_text)
                translations_applied.append((item, fantasy_term))

        return fantasy_text

    def get_fantasy_concept(self, term: str) -> Optional[FantasyTranslation]:
        """Get a single fantasy translation for a specific term"""

        term_lower = term.lower()

        # Check technical translations first
        for original, options in self.technical_translations.items():
            if original.lower() == term_lower:
                fantasy_term = random.choice(options)
                power_level = self._determine_power_level(original, "technical")
                description = self._generate_description(original, fantasy_term, power_level)
                return FantasyTranslation(original, fantasy_term, description, power_level)

        # Check concept translations
        for original, options in self.concept_translations.items():
            if original.lower() == term_lower:
                fantasy_term = random.choice(options)
                power_level = self._determine_power_level(original, "concept")
                description = self._generate_description(original, fantasy_term, power_level)
                return FantasyTranslation(original, fantasy_term, description, power_level)

        # Check mundane translations
        for original, options in self.mundane_translations.items():
            if original.lower() == term_lower:
                fantasy_term = random.choice(options)
                power_level = self._determine_power_level(original, "mundane")
                description = self._generate_description(original, fantasy_term, power_level)
                return FantasyTranslation(original, fantasy_term, description, power_level)

        return None

    def _determine_power_level(self, original: str, category: str) -> str:
        """Determine the magical power level of a concept"""

        # High-power technical concepts
        high_power_technical = ["algorithm", "database", "server", "api", "network", "security"]

        # High-power concepts
        high_power_concepts = ["wisdom", "knowledge", "love", "time", "energy", "strength"]

        if category == "technical" and original.lower() in high_power_technical:
            return "major"
        elif category == "concept" and original.lower() in high_power_concepts:
            return "major"
        elif category == "technical":
            return "moderate"
        elif category == "concept":
            return "moderate"
        else:  # mundane
            return "minor"

    def _generate_description(self, original: str, fantasy_term: str, power_level: str) -> str:
        """Generate a description explaining the fantasy concept"""

        power_descriptor = random.choice(self.power_words[power_level])

        descriptions = {
            "minor": f"A {power_descriptor.lower()} magical manifestation that transforms mundane {original} into mystical energy.",
            "moderate": f"A {power_descriptor.lower()} enchantment that elevates {original} beyond its ordinary nature into something mystical.",
            "major": f"A {power_descriptor.lower()} arcane force that transmutes {original} into a powerful magical concept.",
            "legendary": f"A {power_descriptor.lower()} divine essence that transforms {original} into transcendent magical energy."
        }

        return descriptions[power_level]

    def create_spell_description(self, concept: str, note_content: str) -> str:
        """Create a magical spell description from note content"""

        # Extract key terms from the content
        key_terms = self._extract_key_terms(note_content)

        # Translate key terms
        translated_terms = []
        for term in key_terms[:3]:  # Limit to top 3 terms
            translation = self.get_fantasy_concept(term)
            if translation:
                translated_terms.append(translation.fantasy_term)
            else:
                translated_terms.append(f"mystical {term}")

        # Create spell description
        if translated_terms:
            spell_components = ", ".join(translated_terms)
            return f"A powerful spell woven from {spell_components}, channeling the ancient wisdom of {concept}."
        else:
            return f"An arcane enchantment that harnesses the mystical properties of {concept}."

    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract important terms from text for translation"""

        # Simple extraction - look for common technical and important words
        important_patterns = [
            r'\b(?:function|class|method|variable|data|code|file|system|process|network|security|algorithm|database)\b',
            r'\b(?:project|task|goal|meeting|team|work|business|strategy|plan|objective)\b',
            r'\b(?:research|study|analysis|theory|knowledge|learning|education|training)\b',
            r'\b(?:health|fitness|nutrition|wellness|exercise|medical|treatment)\b',
            r'\b(?:travel|journey|adventure|explore|discover|experience|visit)\b'
        ]

        key_terms = []
        text_lower = text.lower()

        for pattern in important_patterns:
            matches = re.findall(pattern, text_lower)
            key_terms.extend(matches)

        # Remove duplicates and return
        return list(set(key_terms))

    def enhance_enemy_description(self, enemy_name: str, note_title: str, note_content: str) -> str:
        """Create an enhanced fantasy description for an enemy"""

        # Translate the note title into fantasy concepts
        fantasy_title = self.translate_text(note_title)

        # Extract and translate key concepts from content
        key_terms = self._extract_key_terms(note_content)
        magical_elements = []

        for term in key_terms[:2]:  # Use top 2 terms
            translation = self.get_fantasy_concept(term)
            if translation:
                magical_elements.append(translation.fantasy_term)

        # Create enhanced description
        if magical_elements:
            elements_text = " and ".join(magical_elements)
            return f"{enemy_name} is bound to the mystical knowledge of '{fantasy_title}', drawing power from {elements_text} to protect these sacred secrets."
        else:
            return f"{enemy_name} is an ancient guardian bound to protect the mystical wisdom contained within '{fantasy_title}'."


# Global translator instance
fantasy_translator = FantasyTranslator()


def translate_to_fantasy(text: str, context: str = "general") -> str:
    """Convenience function to translate text to fantasy language"""
    return fantasy_translator.translate_text(text, context)


def get_fantasy_term(term: str) -> str:
    """Convenience function to get a single fantasy translation"""
    translation = fantasy_translator.get_fantasy_concept(term)
    return translation.fantasy_term if translation else f"mystical {term}"


def create_magical_spell_description(concept: str, content: str) -> str:
    """Convenience function to create spell descriptions"""
    return fantasy_translator.create_spell_description(concept, content)