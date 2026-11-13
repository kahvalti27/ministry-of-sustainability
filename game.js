// Ministry of Sustainability: the screen. The rules live in engine.js, the content in events.json.

import { TURNS, YEAR, METERS, SECTORS, CRISIS_BELOW, CRISIS_COST, newTerm, choose, endTurn, canAfford,
  eventText, portraitFor, grade, overallGrade, reportLines, opinions, termTitle } from "./engine.js";
import { play, isMuted, toggleMute } from "./sound.js";

const SEASONS = ["Spring", "Summer", "Autumn", "Winter"];  // one year: YEAR seasons
const LABELS = { ...METERS, ...SECTORS };
const LETHAL = ["budget", "approval", "environment"];  // a term ends when one of these hits 0
const DANGER_BELOW = 20;
const CAST = ["edward_collins", "margaret_hale", "julian_frost", "lily_carter", "grandma_rose", "walter_briggs"];

const app = document.getElementById("app");
let data;    // events.json
let country; // typed by the player on the first screen; events.json holds the default
let state;   // the current term (see newTerm in engine.js)
let help = true;      // the "how to play" card is open
let started = false;  // the player has left the first screen

// ---- small helpers ----------------------------------------------------------

const esc = (text) => String(text).replace(/[&<>"]/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]));
const fill = (text) => esc(text.replaceAll("{Country}", country));
const signed = (n) => (n > 0 ? `+${n}` : `${n}`);
const icon = (key, size = 24) => `<img class="icon" src="assets/ui/${key}.png" width="${size}" height="${size}" alt="">`;
const personName = (id) => id.split("_").map((word) => word[0].toUpperCase() + word.slice(1)).join(" ");

// ---- header: where we are, and the seven numbers ------------------------------

function meter(key) {
  const value = state.values[key];
  const change = !state.ending && state.chosen?.changes.find((c) => c.key === key && c.amount !== 0);
  const danger = LETHAL.includes(key) ? value < DANGER_BELOW : key in SECTORS && value < CRISIS_BELOW;
  return `
    <div class="meter meter--${key} ${key in SECTORS ? "meter--sector" : ""} ${change ? "has-change" : ""} ${danger ? "is-danger" : ""}">
      ${icon(key, key in SECTORS ? 16 : 24)}
      <span class="meter__name">${LABELS[key]}</span>
      <span class="meter__value">${value}${change ? `<b class="${change.amount > 0 ? "up" : "down"}">${signed(change.amount)}</b>` : ""}</span>
      <span class="meter__track" role="meter" aria-label="${LABELS[key]}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${value}">
        <span class="meter__fill" style="width:${value}%"></span>
      </span>
    </div>`;
}

function header() {
  const year = Math.ceil(state.turn / YEAR);
  const seasons = Array.from({ length: TURNS }, (_, i) =>
    `<i class="${i + 1 < state.turn ? "is-past" : i + 1 === state.turn ? "is-now" : ""}"></i>`).join("");
  return `
    <header class="top">
      <img class="top__seal" src="assets/ui/seal.png" width="40" height="40" alt="">
      <div class="top__text">
        <h1>Ministry of Sustainability</h1>
        <p class="when">${esc(country)} · Year ${year}, ${SEASONS[(state.turn - 1) % YEAR]}</p>
      </div>
      <span class="top__buttons">
        <button class="help ${isMuted() ? "is-off" : ""}" data-mute aria-label="Sound" aria-pressed="${!isMuted()}">♪</button>
        <button class="help" data-help aria-label="How to play">?</button>
      </span>
      <div class="seasons" role="img" aria-label="Season ${state.turn} of ${TURNS}">${seasons}</div>
    </header>
    <section class="meters" aria-label="Meters">${Object.keys(METERS).map(meter).join("")}</section>
    <section class="meters meters--sectors" aria-label="Sectors">${Object.keys(SECTORS).map(meter).join("")}</section>`;
}

// Shown above the card in the first season of a new year: what the Ministry was paid, and why.
function budgetNote() {
  if (!state.income) return "";
  const lines = state.income.lines.map((l) => `<li class="${l.amount ? "" : "is-zero"}"><span>${l.label}</span><b>${signed(l.amount)}</b></li>`).join("");
  return `
    <section class="payday" aria-label="Budget day">
      <h3>${icon("budget", 16)}Budget day · Year ${Math.ceil(state.turn / YEAR)}</h3>
      <ul>${lines}</ul>
      <p><span>Paid into your Budget</span><b>${signed(state.income.total)}</b></p>
    </section>`;
}

// Shown above the card while a sector is in crisis, so the drain is no surprise.
function crisisNote() {
  if (!state.crisis.length) return "";
  const costs = Object.entries(CRISIS_COST).map(([key, cost]) => `${cost * state.crisis.length} ${LABELS[key]}`);
  return `<p class="crisis"><b>In crisis:</b> ${state.crisis.map((k) => SECTORS[k]).join(", ")}. That cost you ${costs.join(" and ")} this season.</p>`;
}

// ---- the event card -----------------------------------------------------------

function eventCard() {
  const ev = state.event;
  const speaker = ev.speaker ? `
        <figure class="speaker">
          <img src="assets/portraits/${portraitFor(state, ev.speaker)}.png" width="64" height="64" alt="">
          <figcaption>${personName(ev.speaker)}</figcaption>
        </figure>` : "";
  const body = state.chosen ? resultPanel() : `
      <div class="options">
        ${ev.options.map((o, i) => canAfford(state, o)
          ? `<button class="option" data-option="${i}"><kbd>${"ABC"[i]}</kbd><span>${fill(o.label)}</span></button>`
          : `<button class="option" disabled><kbd>${"ABC"[i]}</kbd><span>${fill(o.label)}<small>Needs ${-o.effects.political} political capital</small></span></button>`).join("")}
      </div>`;
  return `
    <article class="card card--${ev.sector} ${state.chosen ? "is-decided" : ""}" aria-live="polite">
      <p class="memo"><span>Memo No. ${String(state.turn).padStart(2, "0")}</span><span>${esc(SECTORS[ev.sector] ?? "Cabinet")}</span></p>
      <div class="card__head">
        ${speaker}
        <h2>${fill(ev.title)}</h2>
      </div>
      <p class="text">${fill(eventText(state))}</p>
      ${body}
      <img class="stamp" src="assets/ui/seal.png" width="64" height="64" alt="">
    </article>`;
}

function resultPanel() {
  const { option, changes } = state.chosen;
  const chips = changes.filter((c) => c.amount !== 0)
    .map((c) => `<li class="${c.amount > 0 ? "up" : "down"}">${icon(c.key, 16)}${LABELS[c.key]} ${signed(c.amount)}</li>`).join("");
  const note = option.real_story ?? state.event.real_story;  // an option can carry its own note
  return `
      <p class="chosen">${fill(option.label)}</p>
      <p class="result">${fill(option.result)}</p>
      ${chips ? `<ul class="changes">${chips}</ul>` : ""}
      ${note ? `<p class="story"><b>True story</b> ${fill(note)}</p>` : ""}
      <button class="button" data-next>${state.turn === TURNS ? "Read the report" : "Next season"}</button>`;
}

// ---- the end-of-term report -----------------------------------------------------

function reportCard() {
  const title = termTitle(state);
  const sectors = Object.keys(SECTORS).map((key) => `
      <section class="sector">
        <h3>${icon(key, 16)}${SECTORS[key]}<span class="grade">${grade(state.values[key])}</span></h3>
        ${reportLines(state, key).map((line) => `<p>${fill(line)}</p>`).join("") || "<p>Nothing to report. Suspicious.</p>"}
      </section>`).join("");
  const looksGood = state.looksGreen.length ? `
      <section class="sector">
        <h3>Things that looked good<span class="grade">${state.looksGreen.length}</span></h3>
        ${state.looksGreen.map((label) => `<p>${fill(label)}</p>`).join("")}
      </section>` : "";
  return `
    <article class="card card--report ${state.ending.lost ? "is-lost" : ""}">
      <p class="memo"><span>${state.ending.lost ? "Game over" : "National Sustainability Report"}</span><span>${esc(country)}</span></p>
      ${state.ending.lost ? `<img class="scene" src="assets/scenes/${state.ending.lost}.png" width="160" height="80" alt="">` : ""}
      <h2>${esc(state.ending.title)}</h2>
      ${state.ending.cause ? `<p class="cause">${esc(state.ending.cause)}</p>` : ""}
      <p class="text">${esc(state.ending.text)}</p>
      ${title ? `<p class="title"><span>Your title</span><b>${esc(title.name)}</b>${esc(title.text)}</p>` : ""}
      <p class="overall">Overall grade <span class="grade grade--big">${overallGrade(state)}</span></p>
      ${sectors}
      ${looksGood}
      <section class="sector">
        <h3>What they say</h3>
        ${opinions(state).map(({ who, text }) => `
        <figure class="quote">
          <img src="assets/portraits/${portraitFor(state, who)}.png" width="64" height="64" alt="">
          <figcaption><b>${personName(who)}</b>${esc(text)}</figcaption>
        </figure>`).join("")}
      </section>
      <button class="button" data-restart>Run for another term</button>
      <img class="stamp" src="assets/ui/seal.png" width="64" height="64" alt="">
    </article>`;
}

// ---- the first screen and the rules ---------------------------------------------

function helpCard() {
  const rules = [
    `You are the new Minister of Sustainability of ${started ? esc(country) : "a country"}. Your term lasts ${TURNS} seasons.`,
    "Each season one problem lands on your desk. Pick one answer. Every answer costs something.",
    `Keep ${icon("budget", 16)}<b>Budget</b>, ${icon("approval", 16)}<b>Approval</b> and ${icon("environment", 16)}<b>Environment</b> above zero. If one of them hits zero, <strong class="fired">you are fired!</strong>`,
    `${icon("political", 16)}<b>Political capital</b> is what you spend to overrule the cabinet. Run out, and those answers are locked.`,
    `<b>Tourism</b>, <b>Agriculture</b> and <b>Fashion</b> decide your grades in the final report. A sector below ${CRISIS_BELOW} is in crisis and drains your Approval every season.`,
    "Every new year is budget day. Healthy sectors pay more tax, and a cabinet that likes you adds more on top.",
    "Some choices come back to your desk a few seasons later.",
  ];
  const list = `<ol class="rules">${rules.map((r) => `<li>${r}</li>`).join("")}</ol>`;
  if (started) {
    return `
    <article class="card">
      <p class="memo"><span>How to play</span></p>
      ${list}
      <button class="button" data-close-help>Back to your desk</button>
    </article>`;
  }
  return `
    <article class="card card--intro">
      <img class="intro__seal" src="assets/ui/seal.png" width="128" height="128" alt="">
      <h1>Ministry of Sustainability</h1>
      <p class="intro__tag">Sixteen seasons. Three industries. One desk.</p>
      <div class="cast" aria-hidden="true">${CAST.map((id) => `<img src="assets/portraits/${id}.png" width="64" height="64" alt="">`).join("")}</div>
      <p class="memo"><span>How to play</span></p>
      ${list}
      <form class="naming">
        <label for="country">Name your country</label>
        <input id="country" name="country" maxlength="20" value="${esc(country)}" autocomplete="off" spellcheck="false">
        <button class="button" type="submit">Start your term</button>
      </form>
    </article>`;
}

// ---- drawing and input ------------------------------------------------------------

function render() {
  if (help) {
    app.innerHTML = (started ? header() : "") + helpCard();
    return window.scrollTo(0, 0);
  }
  app.innerHTML = header() + budgetNote() + crisisNote() + (state.ending ? reportCard() : eventCard());
  const next = app.querySelector("[data-next]");
  if (next) next.focus({ preventScroll: true });
  else window.scrollTo(0, 0);  // a new card or the report starts at the top
}

app.addEventListener("click", (e) => {
  const button = e.target.closest("button");
  if (!button || button.disabled) return;
  if (button.dataset.option) {
    choose(state, state.event.options[Number(button.dataset.option)]);
    play("stamp");
  } else if ("next" in button.dataset) {
    endTurn(state);
    play(!state.ending ? "page" : state.ending.lost ? "lose" : "win");
  } else if ("restart" in button.dataset) state = newTerm(data);
  else if ("mute" in button.dataset) toggleMute();
  else if ("help" in button.dataset) help = true;
  else if ("closeHelp" in button.dataset) help = false;
  else return;
  render();
});

// Keyboard: A, B, C (or 1, 2, 3) pick an option.
document.addEventListener("keydown", (e) => {
  if (e.target.matches?.("input") || e.metaKey || e.ctrlKey || e.altKey) return;
  const key = e.key.toLowerCase();
  const index = Math.max("abc".indexOf(key), "123".indexOf(key));
  if (key.length === 1 && index >= 0) app.querySelector(`[data-option="${index}"]`)?.click();
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
  .then((json) => { data = json; country = json.country; state = newTerm(data); render(); })
  .catch(() => { app.innerHTML = '<p class="loading">Could not load events.json. Open the game through a web server, not as a file.</p>'; });
