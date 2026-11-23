// Lab chrome styles. Plain CSS in a <style> tag: the Lab is DOM-only and must not leak into the app.
export const LAB_CSS = `
:root { color-scheme: dark; }
html, body, #root { height: 100%; margin: 0; }
.lab-root {
  --bg: #12141b; --panel: #181b24; --panel-2: #1f2330; --line: #2b3040; --text: #e7e9f1;
  --muted: #9aa1b5; --accent: #9d8cf7; --accent-2: #6f5fe0; --danger: #f08a8a; --handle: #ffffff;
  position: fixed; inset: 0; display: grid; background: var(--bg); color: var(--text);
  grid-template-columns: 272px minmax(0, 1fr) 312px; grid-template-rows: 44px minmax(0, 1fr) auto 34px;
  grid-template-areas: "top top top" "left center right" "timeline timeline timeline" "status status status";
  font: 12px/1.4 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
.lab-root button, .lab-root input, .lab-root select { font: inherit; color: inherit; }
.lab-toolbar { grid-area: top; display: flex; align-items: center; gap: 6px; padding: 0 10px; background: var(--panel); border-bottom: 1px solid var(--line); overflow-x: auto; white-space: nowrap; }
.lab-brand { font-size: 13px; letter-spacing: .2px; }
.lab-sep { width: 1px; height: 20px; background: var(--line); margin: 0 4px; }
.lab-grow { flex: 1; }
.lab-btn { display: inline-flex; align-items: center; gap: 4px; height: 28px; padding: 0 10px; border-radius: 6px; border: 1px solid var(--line); background: var(--panel-2); cursor: pointer; }
.lab-btn:hover:not(:disabled) { border-color: var(--accent); }
.lab-btn:disabled { opacity: .4; cursor: default; }
.lab-btn:focus-visible, .lab-icon-btn:focus-visible, .lab-object-name:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
.lab-danger { color: var(--danger); }
.lab-inline { display: inline-flex; align-items: center; gap: 6px; color: var(--muted); }
.lab-inline select { height: 28px; border-radius: 6px; border: 1px solid var(--line); background: var(--panel-2); padding: 0 6px; }
.lab-zoom { min-width: 40px; text-align: center; font-variant-numeric: tabular-nums; }
.lab-left, .lab-right { background: var(--panel); overflow-y: auto; min-height: 0; }
.lab-left { grid-area: left; border-right: 1px solid var(--line); }
.lab-right { grid-area: right; border-left: 1px solid var(--line); }
.lab-panel-title { margin: 0; padding: 10px 12px 6px; font-size: 11px; text-transform: uppercase; letter-spacing: .8px; color: var(--muted); font-weight: 600; }
.lab-layer { border-bottom: 1px solid var(--line); }
.lab-layer.is-hidden .lab-layer-name { opacity: .45; }
.lab-layer-row { display: flex; align-items: center; gap: 2px; padding: 4px 6px; }
.lab-layer-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 600; }
.lab-layer-index { color: var(--muted); font-variant-numeric: tabular-nums; font-weight: 400; margin-right: 2px; }
.lab-icon-btn { display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 5px; border: 0; background: transparent; color: var(--muted); cursor: pointer; padding: 0; }
.lab-icon-btn:hover { background: var(--panel-2); color: var(--text); }
.lab-icon-btn.is-active { color: var(--accent); }
.lab-object-row { display: flex; align-items: center; gap: 2px; padding: 1px 6px 1px 34px; }
.lab-object-row.is-selected { background: rgba(157, 140, 247, .16); }
.lab-object-row.is-selected .lab-object-name { color: #fff; }
.lab-object-name { flex: 1; text-align: left; border: 0; background: transparent; color: #c9cede; padding: 4px 2px; cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lab-object-name:disabled { opacity: .45; cursor: not-allowed; }
.lab-object-row .lab-icon-btn { width: 22px; height: 22px; opacity: 0; }
.lab-object-row:hover .lab-icon-btn, .lab-object-row.is-selected .lab-icon-btn, .lab-object-row .lab-icon-btn:focus-visible { opacity: 1; }
.lab-center { grid-area: center; position: relative; min-width: 0; min-height: 0; }
.lab-stage { position: absolute; inset: 0; overflow: hidden; background: radial-gradient(circle at 50% 40%, #232838, #12141b 70%); touch-action: none; user-select: none; }
.lab-stage.is-panning { cursor: grab; }
.lab-frame { position: absolute; left: 50%; top: 50%; border-radius: 46px; box-shadow: 0 0 0 10px #0b0c10, 0 0 0 11px #3a3f50, 0 30px 80px rgba(0,0,0,.55); transform-origin: center center; }
.lab-screen { position: absolute; inset: 0; border-radius: 46px; overflow: hidden; background: #F9F8FF; }
.lab-overlay { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; overflow: hidden; }
.lab-grid line { stroke: rgba(41, 61, 112, .35); }
.lab-safe { position: absolute; left: 0; right: 0; background: repeating-linear-gradient(45deg, rgba(240,138,138,.22) 0 6px, rgba(240,138,138,.08) 6px 12px); pointer-events: none; }
.lab-bbox { fill: none; stroke: var(--accent-2); }
.lab-anchor { stroke: var(--accent-2); }
.lab-handle { fill: var(--handle); stroke: var(--accent-2); pointer-events: all; cursor: grab; }
.lab-handle:hover { fill: #e4dcff; }
.lab-inspector { padding-bottom: 24px; }
.lab-empty, .lab-note, .lab-meta { margin: 6px 12px; color: var(--muted); }
.lab-meta code, .lab-palette-row code { color: #c9cede; }
.lab-section { border-bottom: 1px solid var(--line); }
.lab-section summary { padding: 8px 12px; cursor: pointer; font-weight: 600; list-style: none; }
.lab-section summary::-webkit-details-marker { display: none; }
.lab-section summary::before { content: "▾"; color: var(--muted); margin-right: 6px; }
.lab-section:not([open]) summary::before { content: "▸"; }
.lab-section-body { padding: 0 12px 10px; display: grid; gap: 6px; }
.lab-field { display: grid; align-items: center; gap: 6px; color: #c9cede; }
.lab-number { grid-template-columns: 1fr; }
.lab-number { grid-template-columns: minmax(0, 1fr) 64px; grid-template-areas: "label label" "range num"; row-gap: 2px; }
.lab-number label { grid-area: label; }
.lab-number input[type=range] { grid-area: range; width: 100%; accent-color: var(--accent); }
.lab-number input[type=number] { grid-area: num; width: 100%; box-sizing: border-box; height: 24px; border-radius: 5px; border: 1px solid var(--line); background: var(--panel-2); padding: 0 4px; font-variant-numeric: tabular-nums; }
.lab-color { grid-template-columns: minmax(0, 1fr) 36px 96px; }
.lab-color input[type=color], .lab-palette-row input[type=color] { width: 36px; height: 24px; border: 1px solid var(--line); border-radius: 5px; background: var(--panel-2); padding: 1px; cursor: pointer; }
.lab-color select { height: 24px; border-radius: 5px; border: 1px solid var(--line); background: var(--panel-2); }
.lab-palette-row { grid-template-columns: minmax(0, 1fr) 36px 64px; }
.lab-field input[type=text] { height: 26px; border-radius: 5px; border: 1px solid var(--line); background: var(--panel-2); padding: 0 6px; }
.lab-toggle { grid-template-columns: auto 1fr; }
.lab-toggle input { accent-color: var(--accent); }
.lab-status { grid-area: status; display: flex; align-items: center; gap: 14px; padding: 0 12px; background: var(--panel); border-top: 1px solid var(--line); white-space: nowrap; overflow: hidden; }
.lab-step { margin-left: 4px; width: 22px; height: 22px; border-radius: 5px; border: 1px solid var(--line); background: var(--panel-2); cursor: pointer; }
.lab-step.is-active { border-color: var(--accent); color: var(--accent); }
.lab-coords { font-variant-numeric: tabular-nums; min-width: 130px; }
.lab-muted { color: var(--muted); }
.lab-error { color: var(--danger); }
.lab-message { border: 1px solid var(--accent); background: rgba(157,140,247,.12); border-radius: 5px; padding: 2px 8px; cursor: pointer; max-width: 40vw; overflow: hidden; text-overflow: ellipsis; }
.lab-number { grid-template-columns: minmax(0, 1fr) 64px; grid-template-areas: "label key" "range num"; }
.lab-number .lab-key { grid-area: key; justify-self: end; }
.lab-color { grid-template-columns: minmax(0, 1fr) 36px 96px 20px; }
.lab-palette-row { grid-template-columns: minmax(0, 1fr) 36px 64px 20px; }
.lab-select-row { grid-template-columns: minmax(0, 1fr) 150px; }
.lab-select-row select, .lab-track select, .lab-timeline select { height: 24px; border-radius: 5px; border: 1px solid var(--line); background: var(--panel-2); }
.lab-key { width: 20px; height: 20px; padding: 0; border: 0; background: transparent; cursor: pointer; color: var(--muted); font-size: 13px; line-height: 1; }
.lab-key.is-tracked { color: #e9c46a; }
.lab-key.is-on { color: #ffd166; }
.lab-key:hover { color: #fff; }
.lab-timeline { grid-area: timeline; background: var(--panel); border-top: 1px solid var(--line); min-width: 0; }
.lab-timeline-bar { display: flex; align-items: center; gap: 12px; padding: 6px 12px; flex-wrap: wrap; }
.lab-play { min-width: 112px; justify-content: center; }
.lab-scrub { flex: 1 1 220px; min-width: 160px; accent-color: #ffd166; }
.lab-progress { min-width: 170px; font-variant-numeric: tabular-nums; }
.lab-small-num { width: 64px; height: 24px; border-radius: 5px; border: 1px solid var(--line); background: var(--panel-2); padding: 0 4px; }
.lab-tracks { max-height: 132px; overflow-y: auto; border-top: 1px solid var(--line); }
.lab-track { display: grid; grid-template-columns: 240px 84px minmax(0, 1fr) 24px 24px; align-items: center; gap: 8px; padding: 2px 12px; }
.lab-track.is-selected { background: rgba(157, 140, 247, .16); }
.lab-track-name { text-align: left; border: 0; background: transparent; color: #c9cede; cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding: 2px 0; }
.lab-lane { position: relative; height: 18px; margin: 0 8px; border-radius: 4px; background: var(--panel-2); }
.lab-lane-tick { position: absolute; top: 0; bottom: 0; width: 1px; background: var(--line); }
.lab-diamond { position: absolute; top: 50%; width: 10px; height: 10px; margin: -5px 0 0 -5px; transform: rotate(45deg); border: 1px solid #ffd166; background: #3b3420; padding: 0; cursor: pointer; }
.lab-diamond.is-current { background: #ffd166; }
.lab-playhead { position: absolute; top: -2px; bottom: -2px; width: 2px; margin-left: -1px; background: #ffd166; pointer-events: none; }
`;
