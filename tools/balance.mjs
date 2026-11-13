// Plays thousands of terms with simple strategies and reports how they end.
// Run:  node tools/balance.mjs [terms per strategy, default 20000]
//
// Targets (TASARIM.md, section 4): a player who picks at random should lose roughly 30-50% of the
// time; a careful player should usually finish the term.

import { readFileSync } from "node:fs";
import { TURNS, newTerm, choose, endTurn, canAfford, termTitle } from "../engine.js";

const data = JSON.parse(readFileSync(new URL("../events.json", import.meta.url), "utf8"));
const TERMS = Number(process.argv[2] ?? 20000);
const LETHAL = ["budget", "approval", "environment"];

// A small seeded generator, so two runs give the same numbers.
function seeded(seed) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const after = (term, option, key) => Math.max(0, Math.min(100, term.values[key] + (option.effects?.[key] ?? 0)));
const best = (options, score) => options.reduce((a, b) => (score(b) > score(a) ? b : a));

const STRATEGIES = {
  // Picks any option it can afford.
  random: (term, options) => options[Math.floor(term.random() * options.length)],
  // Protects whichever of the three lethal meters would end up lowest.
  careful: (term, options) => best(options, (o) => Math.min(...LETHAL.map((k) => after(term, o, k)))
    + 0.01 * LETHAL.reduce((sum, k) => sum + after(term, o, k), 0)),
  // Always does what is best for the environment.
  green: (term, options) => best(options, (o) => o.effects?.environment ?? 0),
  // Always does what voters like.
  populist: (term, options) => best(options, (o) => o.effects?.approval ?? 0),
};

function play(strategy, random) {
  const term = newTerm(data, random);
  while (!term.ending) {
    const options = term.event.options.filter((o) => canAfford(term, o));
    choose(term, strategy(term, options.length ? options : term.event.options));
    endTurn(term);
  }
  return term;
}

const pct = (n) => `${((100 * n) / TERMS).toFixed(1)}%`.padStart(6);
const avg = (terms, f) => Math.round(terms.reduce((sum, t) => sum + f(t), 0) / terms.length);

console.log(`${data.events.length} events, ${TERMS} terms per strategy\n`);
console.log("strategy   lost  | budget approval environ | cut short | seasons | final: bud app env pol | tou agr fas | looks-green");
for (const [name, strategy] of Object.entries(STRATEGIES)) {
  const random = seeded(12345);
  const terms = Array.from({ length: TERMS }, () => play(strategy, random));
  const lostBy = (key) => terms.filter((t) => t.ending.lost === key).length;
  const lost = terms.filter((t) => t.ending.lost).length;
  const short = terms.filter((t) => t.ending.title === "Term cut short").length;
  const v = (key) => String(avg(terms, (t) => t.values[key])).padStart(3);
  console.log(
    `${name.padEnd(9)} ${pct(lost)} | ${pct(lostBy("budget"))} ${pct(lostBy("approval"))}  ${pct(lostBy("environment"))} |    ${pct(short)} | ${String(avg(terms, (t) => t.turn)).padStart(4)}/${TURNS} |`
    + `        ${v("budget")} ${v("approval")} ${v("environment")} ${v("political")} | ${v("tourism")} ${v("agriculture")} ${v("fashion")} | ${(terms.reduce((s, t) => s + t.looksGreen.length, 0) / TERMS).toFixed(1)}`,
  );
  const titles = {};
  for (const t of terms) {
    const title = termTitle(t);
    if (title) titles[title.name] = (titles[title.name] ?? 0) + 1;
  }
  console.log(`          titles: ${Object.entries(titles).sort((a, b) => b[1] - a[1]).map(([n, c]) => `${n} ${pct(c).trim()}`).join(", ") || "none"}`);
}

// How often each event is seen and how its options do under random play.
const random = seeded(999);
const seen = {};
for (let i = 0; i < TERMS; i++) for (const id of play(STRATEGIES.random, random).seen) seen[id] = (seen[id] ?? 0) + 1;
console.log("\nevent seen in % of random terms:");
console.log(Object.entries(seen).sort((a, b) => a[1] - b[1]).map(([id, n]) => `  ${id.padEnd(20)} ${pct(n)}`).join("\n"));
