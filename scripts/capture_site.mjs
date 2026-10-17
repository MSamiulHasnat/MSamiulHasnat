// Full-page capture of a URL via headless Edge + raw CDP (no Playwright).
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";

const [, , url, out, width = "1280", height = "800"] = process.argv;
const EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
const port = 9333;
const proc = spawn(EDGE, ["--headless=new", "--disable-gpu", "--hide-scrollbars",
  `--remote-debugging-port=${port}`, `--window-size=${width},${height}`,
  "--user-data-dir=" + process.env.TEMP + "/edge-cap", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let targets;
for (let i = 0; i < 40; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (targets.length) break; } catch {}
  await sleep(250);
}
const page = targets.find((t) => t.type === "page");
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => (await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width: +width, height: +height, deviceScaleFactor: 1, mobile: false });
await send("Page.navigate", { url });
await sleep(6000);
// Scroll through the page so lazy images and scroll-reveal animations fire.
const total = await evaluate("document.documentElement.scrollHeight");
for (let y = 0; y < total; y += 400) { await evaluate(`window.scrollTo(0, ${y})`); await sleep(250); }
await sleep(1500);
await evaluate("window.scrollTo(0, 0)");
await sleep(800);
const h = await evaluate("document.documentElement.scrollHeight");
const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
  clip: { x: 0, y: 0, width: +width, height: h, scale: 1 } });
writeFileSync(out, Buffer.from(shot.result.data, "base64"));
console.log("captured", width, "x", h);
ws.close(); proc.kill();
process.exit(0);
