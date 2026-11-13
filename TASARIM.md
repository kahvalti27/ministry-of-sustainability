# Ministry of Sustainability: Design Document

> Working document. Game text is in English; notes for us can be in Turkish.
> The player names the country on the first screen. In all game text it is written as **{Country}**.

## 1. Pitch

You are the new Minister of Sustainability of {Country}, a small Mediterranean nation that lives on
**tourism, agriculture and fashion**. Every season a new crisis lands on your desk. Every choice
helps one sector and quietly creates a problem in another. Survive a four-year term without being
fired by the Prime Minister, running out of budget, or wrecking the coastline.

Why this game: sustainability is about connected systems. Three sectors that depend on each other
(water, land, labour, image) let the player *feel* trade-offs instead of being lectured about them.

## 2. Decisions so far

| Topic | Decision |
|---|---|
| Setting | Fictional Mediterranean country, mixing Turkish and Italian details |
| Player | Minister of Sustainability |
| Sectors | Tourism, Agriculture, Fashion |
| Tone | Humorous, satirical |
| Language | English only for the first release |
| Platform | Web game that also works on phones |
| Technology | Plain HTML, CSS and JavaScript. No framework, no build step |
| Visual style | Text first: each event looks like a ministry memo or a newspaper front page. Pixel art. 64×64 portraits for the six recurring characters, a ministry seal and a cover image (brief in `CIZIM_TARIFI.md`). The current portraits are drawn by code (`art/deneme/portreler.py`). Pixel font and open-source pixel icons for the meters. No illustration per event |
| Events per turn | Always one |
| Country name | Chosen by the player on the first screen (20 characters at most). The box starts with "Meltemia" |

## 3. Core loop

1. A season starts. One event card appears.
2. The player picks one of 2–3 options.
3. Meters change right away. The game shows a funny result line and, where there is one, a
   small **true story** note (section 7).
4. The choice can set **flags** and **schedule** a follow-up event for a later turn.
5. After 16 turns (4 years × 4 seasons) the term ends with the **National Sustainability Report**.

### Which event appears

1. If a scheduled follow-up is due this turn, it appears. If two are due, the one scheduled first
   appears and the other moves to the next turn.
2. Otherwise the game picks at random from the events that are allowed: not shown yet, turn is at
   or past `earliest_turn`, all `requires` flags are set, no `blocks` flag is set.
3. Among allowed events, the sector shown least often so far goes first, so no sector disappears.

No event appears twice in one term.

### Lose conditions

- **Approval hits 0:** the Prime Minister fires you.
- **Budget hits 0:** the Ministry is shut down "temporarily".
- **Environment hits 0:** the coast is declared a disaster zone and the cabinet needs someone to blame.

**Political capital** is not a lose condition. It is a resource: options that overrule another
minister cost it, and an option the player cannot afford is greyed out. At 0 the player can only
pick the options the cabinet already likes.

### End: National Sustainability Report

- A grade per sector (Tourism, Agriculture, Fashion) and overall.
- A short funny paragraph per sector based on the flags collected.
- What each recurring character thinks of you.

### What success means

Nobody finishes a term with everything saved. Success is surviving sixteen seasons *and* being able
to live with what you gave up. The report should make that trade visible.

*Proposal, not approved yet:* the report gives the player a title worked out from the final numbers,
for example **The Accountant** (budget full, environment wrecked), **The Martyr** (environment fine,
approval at the floor), **The Survivor** (everything average, nothing solved) and
**The Greenwasher** (voters happy, environment poor, many "looks green" choices).

## 4. Meters

Four meters, always visible:

| Meter | Meaning | At 0 |
|---|---|---|
| **Budget** | The Ministry's money | Game over |
| **Approval** | What voters think | Game over |
| **Environment** | Water, soil, emissions, biodiversity | Game over |
| **Political capital** | Your influence in the cabinet | Costly options are locked |

Three **sector bars** (Tourism, Agriculture, Fashion), shown smaller. They cannot end the game.
They decide the grades in the final report, and they replace a separate "economy" meter: the
economy is how the three sectors are doing.

All values run from 0 to 100. Start: every meter and bar at 50, Budget at 60.

### Balance targets

- A single effect is usually between ±5 and ±15, never more than ±20.
- A player who picks at random should lose roughly 30–50% of the time. A careful player should
  usually finish the term.
- These numbers are checked with a small script that plays thousands of random terms (section 10),
  not by feel.

## 5. Design rules

- **No free option.** Every option costs something.
- **The sustainable option is not always the winning one.** Good intentions can backfire.
  The player should feel real trade-offs, never a moral lecture.
- **Delayed consequences.** The best consequences show up 2–6 turns later.
- **Cross-sector chains.** A choice in one sector should regularly open an event in another.
- **Systems are realistic, outcomes can be absurd.** The joke can be silly; the cause and effect
  behind it should be believable.
- **Effects only use what exists.** An option changes the four meters and the three sector bars,
  nothing else. No "approval among farmers": if farmers are happy, Agriculture goes up.
- **Never bend the country's name.** The player types it, so write "the farmers of {Country}" or
  "{Country}'s farmers", never an adjective made from it ("Meltemian").
- **One new follow-up per event, at most.** Any other consequence must lead to an event already on
  the list or to a line in the final report. This keeps the amount of writing under control.

### Humour rules
- Punch up: politicians, bureaucracy, corporations, greenwashing, absurd situations.
- Never punch down at farmers, workers, migrants or activists as people.
- Serious topics (worker exploitation, migrant labour) keep the satire on the people in power;
  the affected people are written with dignity.

### Looks green, isn't

Some options are things people believe are sustainable and that do little or nothing. They are an
option type, not a separate list of events:

- The **looks-green option** is cheap and popular: Approval goes up now, Environment does not move
  or goes down.
- The **option that works** is dull, costly and wins no applause.
- The player is not told which is which. The true story note reveals it after the choice.
- It must not become a quiz with one right answer. The looks-green option is sometimes the right
  call: a minister with no Approval is a former minister.

A looks-green option is marked `"looks_green": true` in `events.json`. The report counts them under
"Things that looked good". Such an option can carry its own `real_story`, which replaces the
event's note when that option is picked.

Topics the owner picked, each placed inside an event already on the list. Facts checked against
sources in November 2026 (listed in `README.md`).

| Topic | Home event | True story note |
|---|---|---|
| Paper straws | X1 Poll Panic: the quick win is a paper-straw law for every beach bar | 2023: most paper straws tested had forever chemicals in them. |
| Hotel towel cards | T6 All Inclusive, Nothing Local: the resorts answer criticism with towel cards | 1986: the word "greenwashing" was invented to describe hotel towel cards. |
| Cotton tote bags | F1 The Green Gala: a free organic tote for every citizen | 2018: a study found a cotton tote must be used thousands of times to match a plastic bag. |
| "Biodegradable" plastic | T3 The Secret Beach: the beach bars switch to "biodegradable" cups | 2019: "biodegradable" bags could still carry shopping after three years in soil and sea. |
| Carbon offsets | X3 The Neighbours' Green Fund: the fund pays in offset credits | 2023: an investigation found most of one big certifier's rainforest credits saved no carbon. |

## 6. Recurring cast

All names are plain English, with no wordplay. Approved by the owner.

| Name | Character | Role | Running joke |
|---|---|---|---|
| Edward Collins | The Prime Minister | Your boss | Only cares about polls: "How many points does this cost us?" Two portraits: pleased with a rising poll, worried with a falling one |
| Margaret Hale | Minister of Tourism | Rival in cabinet | Every problem's solution is "more cruise ships" |
| Julian Frost | Fashion mogul | Industry | Markets everything as "sustainable", changes nothing |
| Lily Carter | Young activist | Civil society | Protests get more creative every time |
| Grandma Rose | The grandmother | The public | Comments on your choices from the village café; the game's conscience |
| Walter Briggs | Farmers' Union leader | Agriculture | Delivers opinions, and sometimes manure |

Mr. Harris, the sheep farmer, appears only in The Sheep Situation and has no portrait.

## 7. Event format (data)

Events live in a data file (`events.json`), not in code, so new events can be written without
touching the game engine.

```json
{
  "id": "sheep_protest",
  "sector": "agriculture",
  "title": "The Sheep Situation",
  "text": "...",
  "real_story": "...",
  "requires": [],
  "blocks": [],
  "earliest_turn": 1,
  "follow_up_only": false,
  "options": [
    {
      "label": "...",
      "result": "...",
      "effects": { "approval": -5, "agriculture": 10 },
      "sets_flags": ["..."],
      "schedules": { "event": "...", "in_turns": 3 }
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `sector` | `tourism`, `agriculture`, `fashion` or `cross` |
| `speaker` | Optional. Whose portrait sits on the card: the file name in `assets/portraits/`, e.g. `walter_briggs` |
| `draft` | Optional. Marks an event whose text is a first draft the owner has not rewritten yet. The engine ignores it |
| `real_story` | Optional. The true story note shown after the choice: a year and what happened, no names |
| `requires` / `blocks` | Flags that must be set / must not be set for the event to appear |
| `earliest_turn` | The event cannot appear before this turn |
| `follow_up_only` | If true, the event never comes up at random; it only appears when scheduled |
| `effects` | Keys: `budget`, `approval`, `environment`, `political`, `tourism`, `agriculture`, `fashion` |
| `sets_flags` | Flags remembered for the rest of the term |
| `looks_green` | Optional, on an option. Marks it as something that looks sustainable and is not; the report lists it |
| `real_story` (on an option) | Optional. A true story note for this option only; it replaces the event's note |
| `schedules` | One follow-up event that will appear after `in_turns` turns |

The two tools do different jobs:

- **`schedules`** is a promise: this follow-up *will* happen, on that turn.
- **Flags** are memory: they open or close events in the random pool and decide the text of the
  final report.

The file also has three top-level fields: `portrait_moods`, which swaps a character's portrait
while a meter is below a number (the Prime Minister looks worried while Approval is under 50); `country`, the name the first screen suggests when the
player has not typed one, and `report_lines`, the flag-based sentences of
the final report (`flag`, `sector`, `text`).

### True story notes

A small stamp under the result line, after the player has chosen, so it never tells them what to
pick. It gives a year and what happened, and nothing else: no country, company, institution or
person. The game's world is invented and the note should not point a finger at anyone real.

- When the event itself happened: *True story · 2024: farmers dumped manure outside government
  buildings in several countries.*
- When the option's outcome is the real part: *True story · 2023: most paper straws tested had
  forever chemicals in them.*

The text in `real_story` starts with the year (or "today") and a colon. The sources behind every
note are listed in `README.md`, not in the game.

## 8. Written events

### The Sheep Situation (Agriculture)
Animal rights activists have chained themselves to the gates of {Country}'s largest sheep farm.
The sheep appear unbothered. The farmer, Mr. Harris, is less so.

1. **"Sheep have been protested before. They'll survive."**
   Approval −5. The activists start a TikTok account. It has more followers than the Ministry.
   → flag `sheep_ignored`; schedules **The Documentary** (C1) in 3 turns.
2. **Shut the farm down.**
   Environment +5, Agriculture −10. 400 sheep are now unemployed. The fashion industry calls,
   panicking about wool.
   → flag `farm_closed`; schedules **Wool-Free Wool** (C2) in 4 turns.
3. **Fund a Sheep Wellbeing Program.**
   Budget −15, Agriculture +15. The sheep now have a better pension plan than your staff.
   → flag `ethical_wool`: opens **Ethical Wool** (F5). The final report mentions the farm's new
   visitor centre.

### Special Delivery (Agriculture)
*True story · 2024: farmers dumped manure outside government buildings in several countries.*
You arrive at the Ministry to find the entrance buried under four tonnes of manure, delivered
personally by the {Country} Farmers' Union. A note on top reads: *"You've been treating us like
this for years. Now you know how it smells."* The press is already here. So are the flies.

1. **Hold the press conference in front of it. Authenticity sells.**
   Agriculture +10, Approval −5. A photo of you mid-sentence, holding your nose, becomes the
   country's most popular meme.
   → flag `manure_meme`: the final report prints the meme on its cover.
2. **Meet the union and open negotiations.**
   Political capital −10 (the PM wanted you to "stand firm"), Agriculture +15.
   → flag `farmers_at_table`: the farmers return with a real demand, water quotas; opens
   **The Water War** (X2).
3. **Turn it into compost and donate it to the city's parks.**
   Budget −5, Environment +10. The parks are glorious next spring.
   → flag `compost_minister`: opens **Mount Textile** (F3): "You're the waste person, right?"

## 9. Event list for the first release

20 base events and up to 6 follow-ups, so 26 at most. A term shows 16, so two playthroughs differ.
Each event needs its full text, options and a true story note. We change names and details of the
real cases.

### Agriculture
| # | Event | Premise | Links |
|---|---|---|---|
| A1 | The Sheep Situation | Written above | → C1, C2, F5 |
| A2 | Special Delivery | Written above | → X2, F3 |
| A3 | The Olive Plague | A bacterium is killing ancient olive trees (inspired by Xylella in Puglia). Cut them, quarantine, or plant resistant varieties? | → Tourism bar (olive landscapes) |
| A4 | Where Did the Bees Go? | Honey producers vs big growers over a pesticide | → Environment, Grandma Rose |
| A5 | The Hazelnut Empire | A Very Large Chocolate Company wants to buy every hazelnut harvest for 10 years (inspired by Black Sea hazelnuts) | → monoculture line in the report |
| A6 | Who Picks the Tomatoes? | Seasonal workers found in terrible housing (inspired by caporalato). Satire targets the middlemen, not the workers | → Agriculture bar, Approval |

### Tourism
| # | Event | Premise | Links |
|---|---|---|---|
| T1 | The Floating City | The Tourism Minister wants the world's largest cruise ship to dock in the old harbour (inspired by Venice) | → Environment, Political capital |
| T2 | Nobody Lives Here Anymore | Short-term rentals have emptied the old town (inspired by Florence) | → Approval, Grandma Rose |
| T3 | The Secret Beach | An influencer posts the country's last secret beach | → Environment |
| T4 | Umbrella Wars | Beach clubs have fenced off the public beach (Italy's beach concessions, Turkey's private beach clubs) | → Approval, Political capital |
| T5 | Pay to Enter | Charge day-trippers an entry fee? (inspired by Venice's access fee) | → Budget, Tourism bar |
| T6 | All Inclusive, Nothing Local | Giant all-inclusive resorts are killing local restaurants (inspired by Turkish resort towns) | → Agriculture bar (local suppliers) |

### Fashion
| # | Event | Premise | Links |
|---|---|---|---|
| F1 | The Green Gala | The Fashion mogul launches an "eco collection" that is 2% recycled | → greenwashing line in the report |
| F2 | The River Is Blue Today | A dye factory turns the river a fashionable shade of indigo | → Agriculture bar (irrigation water) |
| F3 | Mount Textile | A mountain of discarded clothes appears outside the capital | ← `compost_minister` changes the opening text |
| F4 | Behind the Workshop Door | Subcontracted workshops break every labour rule (inspired by Prato). Satire targets the brands | → Approval, Fashion bar |
| F5 | Ethical Wool | Certified local wool could become a luxury export | ← requires `ethical_wool` |

### Cross-sector and politics
| # | Event | Premise | Links |
|---|---|---|---|
| X1 | Poll Panic | The PM's approval drops; he wants a "quick win" from you this season | → Political capital |
| X2 | The Water War | Drought summer: hotels and farmers both need the same water | ← `farmers_at_table` changes who is at the table |
| X3 | The Neighbours' Green Fund | A rich neighbouring bloc offers a green fund, with strings attached | → Budget, sovereignty jokes |

### Follow-ups (only appear when scheduled)
| # | Event | Premise | Scheduled by |
|---|---|---|---|
| C1 | The Documentary | A streaming documentary about the sheep farm airs abroad; tourists start a boycott (Tourism) | A1, option 1 |
| C2 | Wool-Free Wool | With local wool gone, textile makers switch to imported synthetics; microplastics turn up in the fish (Fashion) | A1, option 2 |
| C3 | Ban the Meme | The manure meme is everywhere; the Prime Minister wants to ban the app it spreads on (inspired by Nepal's 2025 social media ban). Not scheduled: it joins the random pool once `manure_meme` is set (Cabinet) | A2, option 1 |
| C4–C6 | *(free slots)* | To be filled as the other events are written, one per event at most | |

## 10. First release

- One full term: 16 turns.
- The events in section 9.
- 4 meters and 3 sector bars.
- A true story note on every event that has a real case behind it.
- The end-of-term report screen.
- Works on a phone.
- Published on itch.io, code public on GitHub.

### Build order

1. **Engine with the two written events.** *Done.* Ugly is fine. Goal: one choice changes meters and a
   follow-up arrives on the right turn.
2. **All events written and playable.** *In progress:* 15 of 26 are in `events.json`. A1 and A2 are final;
   A3–A6, T1–T6, C1, C2 and C3 are drafts (`"draft": true`) waiting for the owner to read and rewrite.
3. **Balance script:** plays thousands of random terms and reports how often each lose condition
   happens and where the meters end. Adjust numbers until the targets in section 4 are met.
4. **Playtest with 5–10 people**, short written report: where they got stuck, which events they
   remembered, how long a term took.
5. **Look and polish, then release.**

### Not in the first release

Turkish and Italian versions, achievements, a separate landing page, an illustration per event, two events in
one turn, sound.

## 11. Open questions

- **Final portraits.** Keep the code-drawn set, or have the owner's friend redraw them? If the
  code-drawn set ships, the store page must say the art was made with AI.
