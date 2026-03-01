# Reddit Post: Legend of the Obsidian Vault

## For r/ObsidianMD, r/LocalLLaMA, r/MachineLearning, r/opensource

---

**🎮 I turned my Obsidian vault into a retro BBS RPG with local AI - and it's surprisingly addictive**

Remember Legend of the Red Dragon (LORD)? I've been working on something that combines that nostalgic BBS gaming experience with modern knowledge management, and the results have been way more engaging than I expected.

**What it is:** Legend of the Obsidian Vault transforms your notes into enemy encounters in a classic LORD-style RPG. Your forgotten markdown files become forest creatures you battle, with TinyLlama generating contextual quiz questions from your actual note content.

**The AI integration that actually works:**
- Local TinyLlama 1.1B model (no cloud dependencies)
- Generates intelligent questions from note content: "This note mentions 27 design patterns - which pattern ensures only one instance exists?"
- Answer correctly = 2x damage critical hit
- Falls back gracefully when AI is unavailable
- Processes 1700+ notes efficiently

**Why this scratches a weird itch:**
- Your procrastinated reading becomes actual game progression
- Ancient notes you forgot about become challenging boss fights
- Knowledge gaps are immediately obvious (and fun to fix)
- Authentic BBS terminal aesthetic with VGA colors
- Actually helps with knowledge retention through gamification

**Current features:**
- Full character creation (3 classes: Death Knight, Mystical, Thieving)
- Combat system with note-based enemies
- Working shops (armor, weapons, healing, banking)
- LORD Secrets implementation (hidden commands, IGM modules)
- Beautiful ASCII art and authentic BBS styling
- Auto-detects Obsidian vaults (including iCloud sync)

**Demo of AI-generated encounter:**
```
You enter the Algorithm Archive where 27 mystical patterns swirl around ancient
CodeReview scrolls. The DataStructure Guardian emerges from shadows of forgotten
documentation, its eyes glowing with the fire of unresolved merge conflicts...

Question: "According to your notes on design patterns, which pattern ensures
only one instance of a class exists?"
```

**The honest bit:** This started as a weekend hack to make myself actually read my scattered notes, but it's turned into something that genuinely makes knowledge review enjoyable. There's something deeply satisfying about your ML study notes becoming a "Neural Network Wraith" that you defeat by correctly explaining backpropagation.

**Technical stuff for the curious:**
- Python + Textual for the TUI
- SQLite for persistence
- Automatic Obsidian vault detection and parsing
- TinyLlama integration with smart caching
- Modular architecture (36% code reduction through refactoring)
- Cross-platform (Mac/Linux/Windows)

**Where I could use some help:**
The core game works great, but there are some interesting challenges I'm tackling:

1. **Platform expansion** - Would love to support Google Keep, Apple Notes, Notion, etc. The note parsing architecture is already modular.

2. **UI polish** - While the BBS aesthetic is intentional, there are some rough edges in screen transitions and responsive design.

3. **IGM modules** - There's a fascinating technical limitation where certain game modules can't modify player stats without crashes (something about threading + database access). Would love fresh eyes on this.

4. **AI improvements** - The TinyLlama integration works well, but there's room for better question generation and answer validation.

If you're curious about local LLM integration, note parsing at scale, or just want to see your knowledge vault become a dungeon crawler, I'd love to hear your thoughts. The code is on GitHub and definitely benefits from more perspectives.

**For the Obsidian folks:** It's read-only on your vault, auto-detects standard locations (including iCloud), and works with 1000+ note vaults without performance issues.

**For the LLM folks:** Interesting case study in local model deployment, prompt engineering for educational content, and graceful AI fallbacks in user applications.

Repository: https://github.com/snedea/legend-of-obsidian-vault

---

*P.S. - If anyone remembers the original LORD and wants to help implement the remaining features (Seth's songs, Olivia encounters, marriage system), that would be amazing. There's something beautifully recursive about collaborative development on a game about knowledge sharing.*

---

## Alternative shorter version for r/SideProject or r/LocalLLaMA:

**🎮 Turned my Obsidian notes into an RPG with local AI question generation**

Built a retro BBS-style game where your markdown notes become enemies, and TinyLlama generates quiz questions from the content. Answer correctly for 2x damage.

Surprisingly effective for actually reviewing old notes - your forgotten ML study materials become "Neural Network Wraiths" you defeat by explaining backpropagation correctly.

- Local TinyLlama 1.1B (no cloud)
- 1700+ note processing
- Authentic LORD/BBS aesthetic
- Read-only on your vault

Looking for contributors interested in expanding to other note platforms (Google Keep, Apple Notes) or tackling some interesting threading/database challenges.

GitHub: https://github.com/snedea/legend-of-obsidian-vault

*Sometimes the best way to organize knowledge is to make it fightable.*