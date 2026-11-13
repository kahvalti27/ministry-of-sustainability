// Ministry of Sustainability: the rules of the game, with no screen attached.
// game.js draws a term in the browser; tools/balance.mjs plays thousands of them in Node.
// All content lives in events.json; nothing in this file knows about a specific event.

export const TURNS = 16;
export const METERS = { budget: "Budget", approval: "Approval", environment: "Environment", political: "Political capital" };
export const SECTORS = { tourism: "Tourism", agriculture: "Agriculture", fashion: "Fashion" };
const START = { budget: 30, approval: 45, environment: 40, political: 50, tourism: 50, agriculture: 50, fashion: 50 };

// A sector below CRISIS_BELOW is in crisis: every season it stays there costs CRISIS_COST.
// Without this, ignoring the economy would be free, because the sector bars cannot end a term.
export const CRISIS_BELOW = 30;
export const CRISIS_COST = { approval: 5 };

// Budget day: at the start of years 2, 3 and 4 the Ministry is paid. A base grant, plus tax from
// each sector by its bar, plus what the cabinet adds by your political capital.
// Each list is [at least this value, pays this much], best first.
export const YEAR = 4;  // seasons
export const INCOME = {
  base: 6,
  sector: [[70, 4], [50, 2]],
  political: [[70, 6], [40, 3]],
};

const LOSSES = {
  approval: ["Fired", "The Prime Minister thanks you for your service in a statement that does not mention your name."],
  budget: ["Closed, temporarily", "The Ministry is out of money. A sign on the door says \"back soon\". It has no date."],
  environment: ["Disaster zone", "The coast has been declared a disaster zone. The cabinet agrees on one thing: it was you."],
};

// Shown when a follow-up is still on its way but nothing else is ready.
const QUIET = {
  id: "quiet", sector: "cross", title: "A Quiet Season",
  text: "Nothing lands on your desk. You suspect this is a trap.",
  options: [{ label: "Catch up on paperwork.", result: "You finish a form that has been open since the previous government.", effects: {} }],
};

// The title a finished term earns: the first one whose test passes. It names what was given up.
const TITLES = [
  ["The Greenwasher", "Everything looked wonderful. The environment has asked not to be quoted.",
    (v, term) => term.looksGreen.length >= 2 && v.environment < 50],
  ["The Accountant", "The books balance. Very little else does.",
    (v) => v.budget >= 55 && v.environment < 50],
  ["The Martyr", "You saved the coast and lost the country.",
    (v) => v.environment >= 60 && v.approval < 40],
  ["The Gardener", "Things are growing that were not growing when you arrived.",
    (v) => v.environment >= 65],
  ["The Survivor", "Nothing was solved and nothing collapsed. You are calling that a win.",
    () => true],
];

/** Starts a term. `random` can be replaced with a seeded generator for repeatable runs. */
export function newTerm(data, random = Math.random) {
  const term = {
    data,
    random,
    turn: 1,
    values: { ...START },
    flags: new Set(),
    seen: new Set(),
    scheduled: [],          // { id, turn, order }
    looksGreen: [],         // labels of the "looks green" options the player picked
    shown: { tourism: 0, agriculture: 0, fashion: 0, cross: 0 },
    event: null,
    chosen: null,           // { option, changes } once the player has picked
    crisis: [],             // sectors that were in crisis when the last season closed
    income: null,           // { lines: [{ label, amount }], total } in the first season of a new year
    ending: null,           // { title, text, lost }
  };
  nextEvent(term);
  return term;
}

// ---- which event appears (TASARIM.md, section 3) ---------------------------

function isAllowed(term, ev) {
  return !ev.follow_up_only
    && !term.seen.has(ev.id)
    && term.turn >= (ev.earliest_turn ?? 1)
    && (ev.requires ?? []).every((f) => term.flags.has(f));
}

function pickEvent(term) {
  // 1. A scheduled follow-up that is due. The one scheduled first wins; the rest wait a turn.
  const due = term.scheduled.filter((s) => s.turn <= term.turn).sort((a, b) => a.order - b.order)[0];
  if (due) {
    term.scheduled = term.scheduled.filter((s) => s !== due);
    return term.data.events.find((ev) => ev.id === due.id);
  }
  // 2. Otherwise a random allowed event, from the sector shown least so far.
  const pool = term.data.events.filter((ev) => isAllowed(term, ev));
  if (pool.length) {
    const fewest = Math.min(...pool.map((ev) => term.shown[ev.sector]));
    const fair = pool.filter((ev) => term.shown[ev.sector] === fewest);
    return fair[Math.floor(term.random() * fair.length)];
  }
  // 3. Nothing ready: wait for a follow-up, or end early if none is coming.
  return term.scheduled.length ? QUIET : null;
}

function nextEvent(term) {
  term.chosen = null;
  term.event = pickEvent(term);
  if (!term.event) {
    term.turn -= 1;  // the season we just stepped into never happened
    term.ending = { title: "Term cut short", text: `No more events are written yet. The term ended in season ${term.turn} of ${TURNS}.` };
    return;
  }
  term.seen.add(term.event.id);
  term.shown[term.event.sector] += 1;
}

// ---- choosing ---------------------------------------------------------------

/** Political capital is spent, not lost: an option that costs more than you have is locked. */
export function canAfford(term, option) {
  return term.values.political + (option.effects?.political ?? 0) >= 0;
}

export function choose(term, option) {
  const changes = [];
  for (const [key, amount] of Object.entries(option.effects ?? {})) {
    const before = term.values[key];
    term.values[key] = Math.max(0, Math.min(100, before + amount));
    changes.push({ key, amount: term.values[key] - before });
  }
  (option.sets_flags ?? []).forEach((f) => term.flags.add(f));
  if (option.looks_green) term.looksGreen.push(option.label);
  if (option.schedules && term.data.events.some((ev) => ev.id === option.schedules.event)) {
    term.scheduled.push({ id: option.schedules.event, turn: term.turn + option.schedules.in_turns, order: term.turn });
  }
  term.chosen = { option, changes };
}

/** Closes the season: the term is lost, complete, or moves to the next event. */
export function endTurn(term) {
  term.crisis = Object.keys(SECTORS).filter((key) => term.values[key] < CRISIS_BELOW);
  for (const [key, cost] of Object.entries(CRISIS_COST)) {
    term.values[key] = Math.max(0, term.values[key] - cost * term.crisis.length);
  }
  const lostBy = Object.keys(LOSSES).find((key) => term.values[key] <= 0);
  if (lostBy) {
    term.ending = { title: LOSSES[lostBy][0], text: LOSSES[lostBy][1], lost: lostBy };
  } else if (term.turn === TURNS) {
    term.ending = { title: "Term complete", text: "Four years. Sixteen seasons. You are still here, which is more than anyone predicted." };
  } else {
    term.income = term.turn % YEAR === 0 ? payBudget(term) : null;
    term.turn += 1;
    nextEvent(term);
  }
}

function payBudget(term) {
  const pays = (steps, key) => steps.find(([least]) => term.values[key] >= least)?.[1] ?? 0;
  const lines = [
    { label: "Base grant", amount: INCOME.base },
    ...Object.keys(SECTORS).map((key) => ({ label: `${SECTORS[key]} taxes`, amount: pays(INCOME.sector, key) })),
    { label: "Cabinet goodwill", amount: pays(INCOME.political, "political") },
  ];
  const before = term.values.budget;
  term.values.budget = Math.min(100, before + lines.reduce((sum, line) => sum + line.amount, 0));
  return { lines, total: term.values.budget - before };
}

// ---- what the card and the report show --------------------------------------

/** An event can open with an extra sentence when an earlier choice set a flag ("intro_if"). */
export function eventText(term) {
  const ev = term.event;
  const intro = ev.intro_if && term.flags.has(ev.intro_if.flag) ? ev.intro_if.text + " " : "";
  return intro + ev.text;
}

/** A character's portrait can follow a meter (events.json, "portrait_moods"). */
export function portraitFor(term, speaker) {
  const mood = term.data.portrait_moods?.[speaker];
  return mood && term.values[mood.meter] < mood.below ? mood.portrait : speaker;
}

export function grade(value) {
  return value >= 80 ? "A" : value >= 65 ? "B" : value >= 50 ? "C" : value >= 35 ? "D" : "F";
}

export function overallGrade(term) {
  const v = term.values;
  return grade(Math.round((v.tourism + v.agriculture + v.fashion + v.environment) / 4));
}

export function reportLines(term, sector) {
  return (term.data.report_lines ?? []).filter((l) => l.sector === sector && term.flags.has(l.flag)).map((l) => l.text);
}

/** What each recurring character says at the end: each one judges a single number ("opinions"). */
export function opinions(term) {
  return (term.data.opinions ?? []).map(({ who, meter, lines }) =>
    ({ who, text: lines.find(([least]) => term.values[meter] >= least)[1] }));
}

/** Only a term that was not lost earns a title. */
export function termTitle(term) {
  if (!term.ending || term.ending.lost) return null;
  const [name, text] = TITLES.find(([, , test]) => test(term.values, term));
  return { name, text };
}
