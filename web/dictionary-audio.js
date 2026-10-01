// Recorded dictionary audio is used only for a clicked vocabulary headword.
// Sentence/reading audio remains browser TTS; book IPA and meanings stay intact.
const dictionaryCache = new Map();
let dictionaryPlayer = null;
let dictionaryRequest = null;
let dictionaryRun = 0;
const originalStopSpeech = stopSpeech;
const normalizeDictionaryWord = value => String(value || '').replace(/\*/g, '').replace(/:\d+$/, '').trim().toLowerCase();
function mwExactAudio(entries, word) {
  const target = normalizeDictionaryWord(word), result = [];
  function visit(value) {
    if (!value || typeof value !== 'object') return;
    if (Array.isArray(value)) { value.forEach(visit); return; }
    const names = [value.meta?.id, value.hwi?.hw, value.ure, value.va, value.if, value.drp];
    if (names.some(name => name && normalizeDictionaryWord(name) === target)) {
      for (const p of [...(value.hwi?.prs || []), ...(value.prs || [])]) {
        const url = mwAudioUrl(p.sound?.audio); if (url) result.push(url);
      }
    }
    Object.values(value).forEach(visit);
  }
  visit(entries);
  return [...new Set(result)];
}
function mwAudioUrl(name) {
  if (typeof name !== 'string' || !/^[a-z0-9_-]+$/i.test(name)) return null;
  const directory = name.startsWith('bix') ? 'bix' : name.startsWith('gg') ? 'gg' : /^[^a-z]/i.test(name) ? 'number' : name[0];
  return `https://media.merriam-webster.com/audio/prons/en/us/mp3/${directory}/${name}.mp3`;
}
stopSpeech = function () {
  dictionaryRun++;
  dictionaryRequest?.abort();
  dictionaryRequest = null;
  if (dictionaryPlayer) { dictionaryPlayer.pause(); dictionaryPlayer.src = ''; }
  dictionaryPlayer = null;
  originalStopSpeech();
};
async function playDictionaryWord(word) {
  stopSpeech();
  const run = dictionaryRun;
  const config = window.OXFORD_AUDIO;
  const button = document.querySelector(`.vocab-heading [data-action="speak"][data-text="${CSS.escape(word)}"]`);
  button?.setAttribute('aria-busy', 'true');
  let timer;
  try {
    let audioUrl = dictionaryCache.get(word);
    if (!audioUrl) {
      const controller = new AbortController(); dictionaryRequest = controller;
      timer = setTimeout(() => controller.abort(), config.timeoutMs);
      const mw = config.provider === 'merriam-webster';
      const mwConfig = window.MW_CONFIG || {};
      const key = String(mwConfig.MW_API_KEY || '').trim();
      if (mw && (!key || key === '8xxx')) throw new Error('Configure MW_API_KEY first');
      const url = mw ? `https://www.dictionaryapi.com/api/v3/references/${encodeURIComponent(mwConfig.REFERENCE || 'sd3')}/json/${encodeURIComponent(word)}?key=${encodeURIComponent(key)}` : config.endpoint.replace('{word}', encodeURIComponent(word));
      const headers = !mw && config.apiKey ? { [config.apiKeyHeader]: config.apiKey } : {};
      const response = await fetch(url, { signal: controller.signal, headers });
      if (!response.ok) throw new Error('Dictionary lookup failed');
      const entries = await response.json();
      const objects = (Array.isArray(entries) ? entries : []).filter(e => e && typeof e === 'object');
      const mwCandidates = mwExactAudio(objects, word);
      const candidates = mw ? mwCandidates : objects.flatMap(e => e.phonetics || [])
        .map(p => p.audio).filter(a => typeof a === 'string' && a.length)
        .map(a => a.startsWith('//') ? 'https:' + a : a).filter(a => a.startsWith('https://'));
      audioUrl = candidates.find(a => new RegExp('[-_]' + config.preferAccent + '[-_.]', 'i').test(a)) || candidates[0];
      if (!audioUrl && mw && config.freeFallback !== false) {
        const fallback = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`, { signal: controller.signal });
        if (fallback.ok) {
          const data = await fallback.json();
          const clips = (Array.isArray(data) ? data : []).filter(e => normalizeDictionaryWord(e.word) === normalizeDictionaryWord(word))
            .flatMap(e => e.phonetics || []).map(p => p.audio).filter(a => typeof a === 'string' && /^https:\/\//.test(a));
          audioUrl = clips.find(a => /[-_]us[-_.]/i.test(a)) || clips[0];
        }
      }
      if (!audioUrl) throw new Error('No recorded pronunciation');
      dictionaryCache.set(word, audioUrl);
    }
    clearTimeout(timer);
    if (run !== dictionaryRun) return;
    const player = new Audio(audioUrl); dictionaryPlayer = player;
    player.onended = () => { if (dictionaryPlayer === player) dictionaryPlayer = null; };
    player.onerror = () => {
      if (run !== dictionaryRun) return;
      dictionaryCache.delete(word);
      toast('Dictionary audio unavailable. Using the browser voice.'); speak(word);
    };
    await player.play();
  } catch (error) {
    if (run === dictionaryRun) {
      toast('Dictionary audio unavailable. Using the browser voice.');
      speak(word);
    }
  } finally {
    clearTimeout(timer);
    button?.removeAttribute('aria-busy');
  }
}
document.addEventListener('click', event => {
  const button = event.target.closest('.vocab-heading [data-action="speak"]');
  if (!button || !window.OXFORD_AUDIO?.enabled) return;
  event.stopImmediatePropagation();
  playDictionaryWord(button.dataset.text);
}, true);
