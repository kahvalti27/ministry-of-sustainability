// Ministry of Sustainability: game engine.
// All content lives in events.json; nothing in this file knows about a specific event.

const TURNS = 16;
const SEASONS = ["Spring", "Summer", "Autumn", "Winter"];
const METERS = { budget: "Budget", approval: "Approval", environment: "Environment", political: "Political capital" };
const SECTORS = { tourism: "Tourism", agriculture: "Agriculture", fashion: "Fashion" };
const LABELS = { ...METERS, ...SECTORS };
const START = { budget: 60, approval: 50, environment: 50, political: 50, tourism: 50, agriculture: 50, fashion: 50 };

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

const app = document.getElementById("app");
let data;   // events.json
let country; // typed by the player on the first screen; events.json holds the default
let state;  // everything that changes during a term
let help = true;      // the "how to play" card is open
let started = false;  // the player has left the first screen

function newTerm() {
  state = {
    turn: 1,
    values: { ...START },
    flags: new Set(),
    seen: new Set(),
    scheduled: [],          // { id, turn, order }
    looksGreen: [],         // labels of the "looks green" options the player picked
    shown: { tourism: 0, agriculture: 0, fashion: 0, cross: 0 },
    event: null,
    chosen: null,           // { option, changes } once the player has picked
    ending: null,           // { title, text, lost }
  };
  nextEvent();
}

// ---- which event appears (TASARIM.md, section 3) ---------------------------

function isAllowed(ev) {
  return !ev.follow_up_only
    && !state.seen.has(ev.id)
    && state.turn >= (ev.earliest_turn ?? 1)
    && (ev.requires ?? []).every((f) => state.flags.has(f))
    && !(ev.blocks ?? []).some((f) => state.flags.has(f));
}

function pickEvent() {
  // 1. A scheduled follow-up that is due. The one scheduled first wins; the rest wait a turn.
  const due = state.scheduled.filter((s) => s.turn <= state.turn).sort((a, b) => a.order - b.order)[0];
  if (due) {
    state.scheduled = state.scheduled.filter((s) => s !== due);
    return data.events.find((ev) => ev.id === due.id);
  }
  // 2. Otherwise a random allowed event, from the sector shown least so far.
  const pool = data.events.filter(isAllowed);
  if (pool.length) {
    const fewest = Math.min(...pool.map((ev) => state.shown[ev.sector]));
    const fair = pool.filter((ev) => state.shown[ev.sector] === fewest);
    return fair[Math.floor(Math.random() * fair.length)];
  }
  // 3. Nothing ready: wait for a follow-up, or end early if none is coming.
  return state.scheduled.length ? QUIET : null;
}

function nextEvent() {
  state.chosen = null;
  state.event = pickEvent();
  if (!state.event) {
    state.turn -= 1;  // the season we just stepped into never happened
    return finish({ title: "Term cut short", text: `No more events are written yet. The term ended in season ${state.turn} of ${TURNS}.` });
  }
  state.seen.add(state.event.id);
  state.shown[state.event.sector] += 1;
  render();
}

// ---- choosing ---------------------------------------------------------------

// Political capital is spent, not lost: an option that costs more than you have is locked.
function canAfford(option) {
  return state.values.political + (option.effects?.political ?? 0) >= 0;
}

function choose(option) {
  const changes = [];
  for (const [key, amount] of Object.entries(option.effects ?? {})) {
    const before = state.values[key];
    state.values[key] = Math.max(0, Math.min(100, before + amount));
    changes.push({ key, amount: state.values[key] - before });
  }
  (option.sets_flags ?? []).forEach((f) => state.flags.add(f));
  if (option.looks_green) state.looksGreen.push(option.label);
  if (option.schedules) {
    const { event, in_turns } = option.schedules;
    if (data.events.some((ev) => ev.id === event)) {
      state.scheduled.push({ id: event, turn: state.turn + in_turns, order: state.turn });
    } else {
      console.warn(`Scheduled event "${event}" is not in events.json`);
    }
  }
  state.chosen = { option, changes };
  render();
}

function endTurn() {
  const lostBy = Object.keys(LOSSES).find((key) => state.values[key] <= 0);
  if (lostBy) return finish({ title: LOSSES[lostBy][0], text: LOSSES[lostBy][1], lost: true });
  if (state.turn === TURNS) return finish({ title: "Term complete", text: "Four years. Sixteen seasons. You are still here, which is more than anyone predicted." });
  state.turn += 1;
  nextEvent();
}

function finish(ending) {
  state.ending = ending;
  render();
}

// ---- end-of-term report -----------------------------------------------------

function grade(value) {
  return value >= 80 ? "A" : value >= 65 ? "B" : value >= 50 ? "C" : value >= 35 ? "D" : "F";
}

function reportLines(sector) {
  return (data.report_lines ?? []).filter((l) => l.sector === sector && state.flags.has(l.flag)).map((l) => l.text);
}

// ---- drawing ----------------------------------------------------------------

const esc = (text) => String(text).replace(/[&<>"]/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]));
const fill = (text) => esc(text.replaceAll("{Country}", country));
const signed = (n) => (n > 0 ? `+${n}` : `${n}`);

function bar(key, small) {
  const value = state.values[key];
  const change = state.chosen?.changes.find((c) => c.key === key && c.amount !== 0);
  return `
    <div class="bar ${small ? "bar--small" : ""} bar--${key}">
      <span class="bar__name">${LABELS[key]}</span>
      <span class="bar__track" role="meter" aria-label="${LABELS[key]}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${value}">
        <span class="bar__fill" style="width:${value}%"></span>
      </span>
      <span class="bar__value">${value}${change ? `<b class="${change.amount > 0 ? "up" : "down"}">${signed(change.amount)}</b>` : ""}</span>
    </div>`;
}

function header() {
  const year = Math.ceil(state.turn / 4);
  return `
    <header class="top">
      <button class="help" data-help aria-label="How to play">?</button>
      <h1>Ministry of Sustainability</h1>
      <p class="when">Year ${year} · ${SEASONS[(state.turn - 1) % 4]} · Season ${state.turn} of ${TURNS}</p>
    </header>
    <section class="bars" aria-label="Meters">${Object.keys(METERS).map((k) => bar(k)).join("")}</section>
    <section class="bars bars--sectors" aria-label="Sectors">${Object.keys(SECTORS).map((k) => bar(k, true)).join("")}</section>`;
}

// A character's portrait can follow a meter (events.json, "portrait_moods").
function portraitFor(speaker) {
  const mood = data.portrait_moods?.[speaker];
  return mood && state.values[mood.meter] < mood.below ? mood.portrait : speaker;
}

// An event can open with an extra sentence when an earlier choice set a flag ("intro_if").
function eventText(ev) {
  const intro = ev.intro_if && state.flags.has(ev.intro_if.flag) ? ev.intro_if.text + " " : "";
  return intro + ev.text;
}

function eventCard() {
  const ev = state.event;
  const speaker = ev.speaker
    ? `<img class="portrait" src="assets/portraits/${portraitFor(ev.speaker)}.png" width="64" height="64" alt="${esc(ev.speaker.replaceAll("_", " "))}">`
    : "";
  const body = state.chosen ? resultPanel() : `
      <div class="options">
        ${ev.options.map((o, i) => canAfford(o)
          ? `<button class="option" data-option="${i}">${fill(o.label)}</button>`
          : `<button class="option" disabled>${fill(o.label)}<small>Needs ${-o.effects.political} political capital</small></button>`).join("")}
      </div>`;
  return `
    <article class="card" aria-live="polite">
      <div class="card__head">
        ${speaker}
        <div>
          <p class="tag">${esc(SECTORS[ev.sector] ?? "Cabinet")}</p>
          <h2>${fill(ev.title)}</h2>
        </div>
        <span class="stamp" aria-hidden="true">URGENT</span>
      </div>
      <p class="text">${fill(eventText(ev))}</p>
      ${body}
    </article>`;
}

function resultPanel() {
  const { option, changes } = state.chosen;
  const chips = changes.filter((c) => c.amount !== 0)
    .map((c) => `<li class="${c.amount > 0 ? "up" : "down"}">${LABELS[c.key]} ${signed(c.amount)}</li>`).join("");
  const note = option.real_story ?? state.event.real_story;  // an option can carry its own note
  const story = note ? `<p class="story"><b>True story</b> ${fill(note)}</p>` : "";
  return `
      <p class="chosen">${fill(option.label)}</p>
      <p class="result">${fill(option.result)}</p>
      ${chips ? `<ul class="changes">${chips}</ul>` : ""}
      ${story}
      <button class="option option--next" data-next>${state.turn === TURNS ? "Read the report" : "Next season"}</button>`;
}

function reportCard() {
  const overall = Math.round((state.values.tourism + state.values.agriculture + state.values.fashion + state.values.environment) / 4);
  const sectors = Object.keys(SECTORS).map((key) => `
      <section class="sector">
        <h3><span class="grade">${grade(state.values[key])}</span> ${SECTORS[key]}</h3>
        ${reportLines(key).map((line) => `<p>${fill(line)}</p>`).join("") || "<p>Nothing to report. Suspicious.</p>"}
      </section>`).join("");
  const looksGood = state.looksGreen.length ? `
      <section class="sector">
        <h3><span class="grade">${state.looksGreen.length}</span> Things that looked good</h3>
        ${state.looksGreen.map((label) => `<p>${fill(label)}</p>`).join("")}
      </section>` : "";
  return `
    <article class="card card--report">
      <p class="tag">${state.ending.lost ? "Game over" : "National Sustainability Report"}</p>
      <h2>${esc(state.ending.title)}</h2>
      <p class="text">${esc(state.ending.text)}</p>
      <p class="overall">Overall grade <span class="grade">${grade(overall)}</span></p>
      ${sectors}
      ${looksGood}
      <button class="option option--next" data-restart>Run for another term</button>
    </article>`;
}

function helpCard() {
  const rules = [
    `You are the new Minister of Sustainability of ${started ? esc(country) : "a small Mediterranean country"}. Your term lasts ${TURNS} seasons.`,
    "Each season one problem lands on your desk. Pick one answer. Every answer costs something.",
    "Keep <b>Budget</b>, <b>Approval</b> and <b>Environment</b> above zero. If one of them hits zero, your term is over.",
    "<b>Political capital</b> is what you spend to overrule the cabinet. Run out, and those answers are locked.",
    "<b>Tourism</b>, <b>Agriculture</b> and <b>Fashion</b> cannot end your term, but they decide your grades in the final report.",
    "Some choices come back to your desk a few seasons later.",
  ];
  return `
    <article class="card">
      ${started ? "" : "<h1>Ministry of Sustainability</h1>"}
      <p class="tag">How to play</p>
      <ol class="rules">${rules.map((r) => `<li>${r}</li>`).join("")}</ol>
      ${started ? '<button class="option option--next" data-close-help>Back to your desk</button>' : `
      <form class="naming">
        <label for="country">Name your country</label>
        <input id="country" name="country" maxlength="20" value="${esc(country)}" autocomplete="off" spellcheck="false">
        <button class="option option--next" type="submit">Start your term</button>
      </form>`}
    </article>`;
}

function render() {
  if (help) {
    app.innerHTML = (started ? header() : "") + helpCard();
    return window.scrollTo(0, 0);
  }
  app.innerHTML = header() + (state.ending ? reportCard() : eventCard());
  const next = app.querySelector("[data-next]");
  if (next) next.focus();
  else window.scrollTo(0, 0);  // a new card or the report starts at the top
}

app.addEventListener("click", (e) => {
  const button = e.target.closest("button");
  if (!button || button.disabled) return;
  if (button.dataset.option) choose(state.event.options[Number(button.dataset.option)]);
  else if ("next" in button.dataset) endTurn();
  else if ("restart" in button.dataset) newTerm();
  else if ("help" in button.dataset) { help = true; render(); }
  else if ("closeHelp" in button.dataset) { help = false; render(); }
});

// The first screen: the player names the country, then the term starts.
app.addEventListener("submit", (e) => {
  e.preventDefault();
  country = new FormData(e.target).get("country").trim() || data.country;
  help = false;
  started = true;
  render();
});

fetch("events.json")
  .then((response) => response.json())
  .then((json) => { data = json; country = json.country; newTerm(); })
  .catch(() => { app.innerHTML = '<p class="loading">Could not load events.json. Open the game through a web server, not as a file.</p>'; });
