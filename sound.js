// Ministry of Sustainability: sound. Every effect is a few notes from the browser's own
// synthesizer, so there are no audio files to load.

const KEY = "ministry-muted";
let context;   // made on the first sound, because browsers only allow audio after a click
let muted = false;
try { muted = localStorage.getItem(KEY) === "1"; } catch { /* private window: start with sound on */ }

// Each effect is a list of notes: [frequency in Hz, start in seconds, length in seconds, wave shape].
const EFFECTS = {
  stamp: [[110, 0, 0.09, "square"], [70, 0.03, 0.14, "triangle"]],       // a decision is made
  page: [[520, 0, 0.04, "square"], [660, 0.05, 0.05, "square"]],         // next season
  win: [[392, 0, 0.12, "square"], [494, 0.12, 0.12, "square"], [587, 0.24, 0.12, "square"], [784, 0.36, 0.3, "square"]],
  lose: [[330, 0, 0.18, "square"], [262, 0.18, 0.18, "square"], [196, 0.36, 0.45, "sawtooth"]],
};

export function play(name) {
  if (muted) return;
  try {
    context ??= new AudioContext();
    if (context.state === "suspended") context.resume();
    const now = context.currentTime;
    for (const [frequency, start, length, type] of EFFECTS[name]) {
      const tone = context.createOscillator();
      const volume = context.createGain();
      tone.type = type;
      tone.frequency.value = frequency;
      volume.gain.setValueAtTime(0.08, now + start);
      volume.gain.exponentialRampToValueAtTime(0.001, now + start + length);
      tone.connect(volume).connect(context.destination);
      tone.start(now + start);
      tone.stop(now + start + length);
    }
  } catch { /* no audio on this device: the game is fine without it */ }
}

export const isMuted = () => muted;

export function toggleMute() {
  muted = !muted;
  try { localStorage.setItem(KEY, muted ? "1" : "0"); } catch { /* the choice just will not be remembered */ }
  if (!muted) play("page");
}
