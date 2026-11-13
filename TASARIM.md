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
| Visual style | Text first: each event looks like a ministry memo or a newspaper front page. Pixel art. 64×64 portraits for the six recurring characters, a ministry seal and a cover image (brief in `CIZIM_TARIFI.md`). The current portraits are drawn by code (`tools/portraits.py`), and so are the seven meter icons and the seal (`tools/ui_art.py`). Fonts: Jersey 15 for headings, VT323 for text. Each event is a memo on a desk: a sector-coloured strip, the speaker's framed portrait, options lettered A to C, and the seal pressed on once a decision is made. No illustration per event |
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
   or past `earliest_turn`, all `requires` flags are set.
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
- What each recurring character thinks of you. Each one judges a single number: the Prime
  Minister your Political capital, Grandma Rose your Approval, Lily Carter the Environment, and
  Margaret Hale, Julian Frost and Walter Briggs their own sector. Three possible lines each.

### What success means

Nobody finishes a term with everything saved. Success is surviving sixteen seasons *and* being able
to live with what you gave up. The report should make that trade visible.

A term that is not lost earns a title, worked out from the final numbers. The first one that fits
is used:

| Title | When |
|---|---|
| **The Greenwasher** | Two or more looks-green choices, and Environment under 50 |
| **The Accountant** | Budget 55 or more, Environment under 50 |
| **The Martyr** | Environment 60 or more, Approval under 40 |
| **The Gardener** | Environment 65 or more |
| **The Survivor** | Everything else |

## 4. Meters

Four meters, always visible:

| Meter | Meaning | At 0 |
|---|---|---|
| **Budget** | The Ministry's money | Game over |
| **Approval** | What voters think | Game over |
| **Environment** | Water, soil, emissions, biodiversity | Game over |
| **Political capital** | Your influence in the cabinet | Costly options are locked |

Three **sector bars** (Tourism, Agriculture, Fashion), shown smaller. They decide the grades in the
final report, and they replace a separate "economy" meter: the economy is how the three sectors
are doing.

**Sector crisis.** A sector bar cannot end the game by itself, but a sector below 30 is in crisis:
every season it stays there costs 5 Approval (the jobs are gone). Without this rule, ignoring the
economy was free: a player who always picked the greenest option never lost.

**Budget day.** Money has a source. At the start of years 2, 3 and 4 the Ministry is paid, and the
card shows the sum line by line:

| Source | Rule | Pays |
|---|---|---|
| Base grant | every year | +6 |
| Each sector's taxes | bar at 70 or more / 50–69 / under 50 | +4 / +2 / 0 |
| Cabinet goodwill | Political capital at 70 or more / 40–69 / under 40 | +6 / +3 / 0 |

So a year pays between 6 and 24. This ties the economy to the Ministry's money (wrecking the
sectors makes you poor) and gives Political capital a second use: spend it now to unlock an
option, or keep it for a bigger budget next year. Budget stops at 100.

All values run from 0 to 100. Start: Budget 30, Approval 45, Environment 40, Political capital 50,
every sector 50. The Minister inherits a country whose environment is already in trouble and a
Ministry with little money: the first year is tight, and the first budget day is a relief.

### Balance targets

- A single effect is usually between ±5 and ±15, never more than ±20.
- A player who picks at random should lose roughly 30–50% of the time. A careful player should
  usually finish the term.
- These numbers are checked with `tools/balance.mjs`, which plays thousands of terms, not by feel.

Measured in November 2026, 20,000 terms per strategy, all 26 events:

| Strategy | Loses | Lost to Budget / Approval / Environment |
|---|---|---|
| Random | 34% | 12% / 12% / 9% |
| Careful (protects the lowest of the three lethal meters, ignores sectors) | 13% | 0% / 13% / 0% |
| Always the greenest option | 96% | 0% / 96% / 0% |
| Always the most popular option | 8% | 7% / 0% / 1% |

Before the sector crisis rule and the new start values, random play lost 13% of the time and the
greenest-option strategy never lost. Before budget day (start Budget 60, no income, crisis also
cost 2 Budget) the always-popular strategy lost 35% of the time, nearly all to Budget; yearly
income now keeps it alive, and it usually ends as The Greenwasher or The Survivor.

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
| `requires` | Optional. Flags that must be set for the event to appear |
| `earliest_turn` | Optional. The event cannot appear before this turn |
| `follow_up_only` | If true, the event never comes up at random; it only appears when scheduled |
| `effects` | Keys: `budget`, `approval`, `environment`, `political`, `tourism`, `agriculture`, `fashion` |
| `sets_flags` | Flags remembered for the rest of the term |
| `looks_green` | Optional, on an option. Marks it as something that looks sustainable and is not; the report lists it |
| `real_story` (on an option) | Optional. A true story note for this option only; it replaces the event's note |
| `schedules` | One follow-up event that will appear after `in_turns` turns |
| `intro_if` | Optional, on an event. `flag` and `text`: a sentence put before the event text when that flag is set |

The two tools do different jobs:

- **`schedules`** is a promise: this follow-up *will* happen, on that turn.
- **Flags** are memory: they open events in the random pool, change an event's opening sentence
  and decide the text of the final report. An option only sets a flag that something reads.

The file also has four top-level fields: `opinions`, the lines each character can say in the
final report (`who`, `meter`, and `lines` as pairs of a minimum value and a sentence, highest first); `portrait_moods`, which swaps a character's portrait
while a meter is below a number (the Prime Minister looks worried while Approval is under 50);
`country`, the name the first screen suggests when the player has not typed one; and
`report_lines`, the flag-based sentences of the final report (`flag`, `sector`, `text`).

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
| C4 | A Slight Scrape | The world's largest cruise ship hits the old harbour (Tourism) | T1, option 1 |
| C5 | Blue Harvest | The fields downstream of the dye works grow indigo tomatoes (Agriculture) | F2, option 2 |
| C6 | One Bad Frost | One cold night kills a third of the hazelnut crop, and nothing else is planted (Agriculture) | A5, option 1 |

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
2. **All events written and playable.** *Written:* all 26 are in `events.json`. A1 and A2 are final;
   the other 24 are drafts (`"draft": true`) waiting for the owner to read and rewrite.
3. **Balance script.** *Done:* `tools/balance.mjs` plays thousands of terms and reports how often
   each lose condition happens and where the meters end. The numbers meet the targets in section 4.
   Run it again after any change to effects.
4. **Playtest with 5–10 people** (how to run it: `TEST_REHBERI.md`), short written report: where they got stuck, which events they
   remembered, how long a term took.
5. **Look and polish, then release.** *Started:* icons, seal, memo layout, first screen with the
   cast, season track, danger and crisis warnings, keyboard shortcuts (A/B/C). The cover (`art/cover.png`,
   630×500) and a picture for each of the three lose screens are drawn by `tools/scenes.py`. Sound:
   five short effects made by the browser's synthesizer (`sound.js`), with a mute button that is
   remembered.

### Not in the first release

Turkish and Italian versions, achievements, a separate landing page, an illustration per event, two events in
one turn, sound.

## 11. Open questions

- **Final portraits.** Keep the code-drawn set, or have the owner's friend redraw them? If the
  code-drawn set ships, the store page must say the art was made with AI.
