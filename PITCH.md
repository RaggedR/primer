# The Primer — StartSpace Challenge Pitch

> How might we reimagine library experiences for young people (12–18) so they feel as captivating, interactive, and immersive as the digital worlds they inhabit — while strengthening meaningful, curriculum-aligned learning?

## One sentence

An AI-powered game that turns the library into a dungeon crawl where the books are the weapons.

## The Problem

Young people don't lack access to information — they're drowning in it. What they lack is the skill to evaluate, argue, and think from primary sources. Libraries have the sources. Schools have the curriculum. Neither has the hook.

## The Hook

**The Gates.** A game played inside the library, on the student's phone. AI characters guard doors. Each guard has beliefs, values, and a position. The student must write persuasively to get through. No multiple choice. No rubric. A real conversation with an AI that pushes back, asks questions, and only opens the door when the argument actually lands.

The catch: the guard's position is grounded in a real historical primary source. To build a winning argument, the student needs to find and read the source. The game sends them to the library catalogue. The catalogue sends them to a shelf. The shelf has a book. They read it because they need it to win.

**The student thinks they're playing a game. They're actually learning to research, read critically, and write persuasively.**

## How It Works

### The Student Experience

1. **Enter the library.** Open the app. Two worlds load simultaneously: the physical library around you, and a 2D game map that mirrors its layout — the reading rooms, the stacks, the catalogue hall. Your avatar appears where you're standing.
2. **Explore.** Wander the library with phone in hand. AR characters are scattered through the space like Pokémon — a Roman senator near the history shelves, a mill girl by the periodicals, a scientist in the reference section. They shimmer on your camera feed, waiting. On the game map, your avatar moves through the mirrored space, and the gates glow.
3. **Approach a gate.** Walk up to an AR character physically, or tap a gate on the game map. The guard appears — on your camera if you're using AR, on screen if you prefer the game world. They introduce themselves. "I'm a merchant in 1840s Massachusetts. My mill employs 200 girls. Business is good. Why should I change anything?"
4. **Research.** The student doesn't know enough yet. The game nudges: "The library has letters from the people who worked in mills like mine. Maybe you should read what they said." A catalogue search is suggested. A call number appears. The game map highlights the shelf location.
5. **Hunt.** Walk to the shelf. Find the book. This is the Pokémon Go moment — the physical search IS the gameplay. The library stacks are the tall grass. The primary sources are the rare catches.
6. **Read.** The student reads the mill girls' letters. Sees the 14-hour days, the lung disease, the $3.50 a week. Sees that the girls organised. 3–10 pages, sitting right there in the library.
7. **Return to the gate.** Now the student writes. Not a generic essay — a targeted argument to this specific character, informed by what they just read. The guard responds, challenges, probes. The student revises.
8. **The door opens.** The student has done primary source research, critical reading, and persuasive writing — and it felt like catching a legendary.

### The 10 Gates (Progressive Difficulty)

| Level | Guard | Skill Taught |
|-------|-------|-------------|
| 1. The Librarian | Sympathetic, needs a reason | Clarity — state what you want and why |
| 2. The Sceptic | Friendly but unimpressed | Evidence — claims need support |
| 3. The Believer | Different moral framework | Empathy — understand before you argue |
| 4. The Bureaucrat | Following rules, not malice | Institutional persuasion — work within constraints |
| 5. The Opponent | Strong opposing position | Steelmanning — engage the best version of the other side |
| 6. The Mirror | Argues YOUR position badly | Self-criticism — your side can argue badly too |
| 7. The Historian | A character from history | Historical empathy — argue in their terms, not yours |
| 8. The Coalition | Three guards, different values | Coalition building — one argument for multiple audiences |
| 9. The Locked Door | Cannot be persuaded | Recognition — not every problem yields to rhetoric |
| 10. The Final Gate | The student's own patterns | Self-awareness — write outside your comfort zone |

### The Curriculum Layer

Behind the game is a curated collection of 63 primary historical sources — letters, speeches, diaries, legal documents, scientific papers — spanning Hammurabi to the Mahsa Amini protests. Organised by theme, paired for contradiction, rated by difficulty.

Each gate maps to specific sources. A Miranda (mentor — teacher, librarian, parent) selects 5–6 sources for their student and configures which gates use which sources. The game adapts.

The sources are chosen because they're:
- **Real** — primary, not textbook summaries
- **Short** — 3–10 pages each, manageable in one sitting
- **Rich** — dense enough to reward close reading
- **Paired** — designed to contradict each other (Pericles' democratic idealism vs Athens' imperial brutality, five years apart)
- **Available** — in library collections, translatable to any language

### The Miranda (Mentor) Role

Inspired by Stephenson's *The Diamond Age*: the AI is the book, but it needs a human who cares.

- A librarian, teacher, or parent selects sources and configures gates for their student
- They can review gate transcripts — seeing how the student's arguments evolved across drafts
- They don't need to be subject experts — the AI provides context and scaffolding
- **The AI educates the Miranda too** — the mentor reads the sources alongside the student

### The Mirrored Map

The game world is a top-down 2D map of the actual library. Built with Tech World's map editor, it mirrors the real floor plan — the reading rooms, the stacks, the catalogue terminals, the staircases. The student's avatar moves through the digital twin while the student moves through the physical space.

- **Gate locations on the map correspond to physical locations in the library.** A gate in the history stacks on-screen means a guard waiting near the history shelves in real life.
- **Shelf highlights.** When the game sends a student to find a source, the map highlights the shelf location — and the student walks there.
- **Multiplayer.** Other students appear on the map. They can see who's stuck at which gate, collaborate, compare strategies. The library becomes a social space.
- **Any library gets its own map.** The map editor is already built. A librarian creates a digital twin of their library in an afternoon. Gates are placed where the relevant collections live.

### The AR Discovery Layer — Pokémon in the Library

The guards don't just sit behind gates on a screen. **They're hiding in the library.**

- **Explore with your camera.** Walk through the stacks. Point your phone. AR characters shimmer into view — a Roman senator leaning against the classics shelf, a factory girl sitting on the floor by the periodicals, a scientist examining a reference book. They're waiting to be found.
- **Discovery is gameplay.** Finding the guards is part of the fun. Not every guard is visible from every angle. Some only appear when you're near their section. The library rewards exploration.
- **Tap to engage.** Walk up to an AR character, tap them, and the gate conversation begins — voice or text. The guard speaks (text-to-speech) and the student responds.
- **Dual mode.** Students who prefer the game map can play entirely on-screen. Students who want the AR hunt can explore with their camera. Both modes are the same game, the same gates, the same curriculum. The AR layer is an enhancement, not a requirement.
- **Minimal AR, maximum impact.** Character overlay on camera feed — not complex environment mapping or surface detection. A sprite that appears at GPS/beacon coordinates inside the library. Technically lightweight, experientially magical.
- Built in Flutter — cross-platform iOS/Android from one codebase.

### The Library as Game Board

This is not an app that happens to be used near a library. **The library IS the game board.**

- Gate challenges reference materials in the library's collection
- The game integrates with the library catalogue — search prompts, call numbers, shelf locations
- Students physically walk to shelves, find books, read sources
- The catalogue is the inventory system. The shelves are the dungeon. The books are the loot.
- Foot traffic to underused collections increases measurably

## What Already Exists

This is not a concept pitch. Core infrastructure is built:

| Component | Status |
|-----------|--------|
| **Game engine** | Built — Flutter/Flame multiplayer 2D world, 6 maps, pathfinding, cross-platform |
| **AI tutor** | Built — Claude API via LiveKit, real-time chat with voice I/O |
| **Terminal interaction** | Built — walk to station, tap, engage with AI, submit |
| **Map editor** | Built — paint custom maps, auto-terrain, tile layers |
| **Auth & backend** | Built — Firebase Auth, Firestore, Cloud Functions |
| **Code editor with LSP** | Built — in-game coding with language server support |
| **Source curriculum** | Drafted — 63 sources across 8 themes with Talmudic pairs |
| **Gate design** | Drafted — 10 levels with progressive difficulty |
| **Multi-turn dialogue** | Needed — extend single-shot submission to conversation |
| **Gate state tracking** | Needed — Firestore collection for progress and transcripts |
| **Library mirror map** | Needed — digital twin of SLV floor plan using existing map editor |
| **Library catalogue integration** | Needed — API integration with SLV catalogue |
| **AR discovery layer** | Needed — camera feed with character overlay at GPS/beacon locations |
| **Miranda dashboard** | Needed — mentor view of student progress and transcripts |

## The MVP (May–July)

For the StartSpace Challenge, we build and test:

1. **3 gates** (Levels 1, 2, and 5) — sympathetic, sceptic, opponent
2. **6 primary sources** mapped to those gates, drawn from SLV collections
3. **Catalogue integration** — the game sends students to real shelves in State Library Victoria
4. **Miranda view** — a librarian can configure gates and review transcripts
5. **Test with 5–10 students** aged 14–18 in the library

What we measure:
- Do students find and read the primary sources?
- Does argument quality improve across drafts within a single gate?
- Does argument quality improve across gates?
- Do students return voluntarily?
- Do librarians find the Miranda role sustainable?

## The Team

**Robin Langer** — Developer and architect. Built the Tech World game platform. Background in AI-assisted education tools and infrastructure engineering.

**Nick Meinhold** — Co-developer. Background in Flutter development and educational technology.

### The Miranda Role — Librarians as Mentors

The Miranda is our name for the human mentor — the person who makes the AI meaningful. In the library context, **the Miranda is the librarian.**

The role is lightweight by design:
- **Configure:** Select which sources and gates a student or group will encounter. The AI provides recommendations; the librarian makes the call.
- **Observe:** Review gate transcripts to see how students' arguments evolved. Not grading — noticing. "She struggled with empathy-based argument but nailed the evidence gate."
- **Intervene:** When a student is stuck, the Miranda can nudge — not with answers, but with questions. "Have you looked at the letters section on Level 3?" The librarian's knowledge of the collection becomes a superpower.
- **Curate:** Over time, librarians build gate configurations tuned to their collection. A librarian at State Library Victoria creates different gates than one in a regional branch — same mechanics, different sources, same learning.

The AI prepares the Miranda. A librarian who hasn't read the Geniza documents gets a briefing — context, key passages, what students might find. **The system educates the educator.**

## Why This Works

- **The game is real.** Students write real arguments to AI characters who actually push back. There is no "correct answer" — only persuasion that works or doesn't.
- **The library is essential.** You can't win without the books. The game doesn't replace the library — it makes the library the most important room in the school.
- **The AI levels the playing field.** A student in any language, any country, any background gets the same quality of interlocutor. The sources can be translated. The guards can speak any language.
- **The mentor doesn't need to be an expert.** The AI prepares the Miranda. A parent who left school at 16 can guide their child through the Geniza documents if the AI provides the scaffolding.
- **It scales.** One library, one cohort, one set of sources → any library, any curriculum, any language. The gate mechanics are content-agnostic. Swap the sources and guards for science, philosophy, law, literature.

## The Vision

Every library becomes a game world. Every book becomes a weapon. Every student learns that the most powerful thing you can do with information is make an argument that changes someone's mind.

The Primer doesn't teach students what to think. It teaches them that they're entitled to think at all — from the sources, on their own terms, with rigour. And it tricks them into reading along the way.
