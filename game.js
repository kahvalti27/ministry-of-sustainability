// Ministry of Sustainability: the screen. The rules live in engine.js, the content in events.json.

import { TURNS, METERS, SECTORS, newTerm, choose, endTurn, canAfford, eventText, portraitFor,
  grade, overallGrade, reportLines, termTitle } from "./engine.js";

const SEASONS = ["Spring", "Summer", "Autumn", "Winter"];
const LABELS = { ...METERS, ...SECTORS };

const app = document.getElementById("app");
let data;    // events.json
let country; // typed by the player on the first screen; events.json holds the default
let state;   // the current term (see newTerm in engine.js)
let help = true;      // the "how to play" card is open
let started = false;  // the player has left the first screen

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

// Shown above the card while a sector is in crisis, so the drain on Budget and Approval is no surprise.
function crisisNote() {
  if (!state.crisis.length) return "";
  const costs = Object.entries(state.rules.crisis_cost).map(([key, cost]) => `${cost * state.crisis.length} ${LABELS[key]}`);
  return `<p class="crisis"><b>In crisis:</b> ${state.crisis.map((k) => SECTORS[k]).join(", ")}. That cost you ${costs.join(" and ")} this season.</p>`;
}

function eventCard() {
  const ev = state.event;
  const speaker = ev.speaker
    ? `<img class="portrait" src="assets/portraits/${portraitFor(state, ev.speaker)}.png" width="64" height="64" alt="${esc(ev.speaker.replaceAll("_", " "))}">`
    : "";
  const body = state.chosen ? resultPanel() : `
      <div class="options">
        ${ev.options.map((o, i) => canAfford(state, o)
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
      <p class="text">${fill(eventText(state))}</p>
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
  const title = termTitle(state);
  const sectors = Object.keys(SECTORS).map((key) => `
      <section class="sector">
        <h3><span class="grade">${grade(state.values[key])}</span> ${SECTORS[key]}</h3>
        ${reportLines(state, key).map((line) => `<p>${fill(line)}</p>`).join("") || "<p>Nothing to report. Suspicious.</p>"}
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
      ${title ? `<p class="title"><b>${esc(title.name)}</b> ${esc(title.text)}</p>` : ""}
      <p class="overall">Overall grade <span class="grade">${overallGrade(state)}</span></p>
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
    `<b>Tourism</b>, <b>Agriculture</b> and <b>Fashion</b> decide your grades in the final report. A sector below ${state.rules.crisis_below} is in crisis and drains your Budget and Approval every season.`,
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
  app.innerHTML = header() + crisisNote() + (state.ending ? reportCard() : eventCard());
  const next = app.querySelector("[data-next]");
  if (next) next.focus();
  else window.scrollTo(0, 0);  // a new card or the report starts at the top
}

app.addEventListener("click", (e) => {
  const button = e.target.closest("button");
  if (!button || button.disabled) return;
  if (button.dataset.option) choose(state, state.event.options[Number(button.dataset.option)]);
  else if ("next" in button.dataset) endTurn(state);
  else if ("restart" in button.dataset) state = newTerm(data);
  else if ("help" in button.dataset) help = true;
  else if ("closeHelp" in button.dataset) help = false;
  else return;
  render();
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
