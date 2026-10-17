# MSamiulHasnat profile repo

This repo is the GitHub profile README for MSamiulHasnat.

- All visuals in `assets/` are custom SVGs. Don't swap them for third-party widgets such as capsule-render, typing-svg, skillicons or stats cards; the profile deliberately avoids them.
- Each SVG switches between light and dark through an internal `@media (prefers-color-scheme)` block. Animations use CSS keyframes or SMIL. Never give content a starting `opacity:0` that depends on an animation to reveal it.
- The project cards, stack panel and footer are generated. Edit the text in the scripts, then regenerate with:
  ```bash
  python scripts/gen_cards.py assets
  python scripts/gen_stack_footer.py assets
  ```
  `assets/hero.svg` is edited by hand. `gen_cards.py` needs Pillow (`pip install pillow`).
- The EASTARCH card shows a full-page capture of the live site (`scripts/eastarch-site.jpg`) that auto-scrolls through SMIL. The image is embedded as base64 because GitHub-rendered SVGs can't load external images. To refresh it after the site changes (needs Node 18+ and Microsoft Edge on Windows), run the capture, convert it with Pillow to a 720px-wide JPEG at about quality 70 saved over `scripts/eastarch-site.jpg`, then rerun `gen_cards.py`:
  ```bash
  node scripts/capture_site.mjs https://www.eastarchconsulting.com full.png 1280 800
  ```
  GitHub READMEs can't embed live, interactive sites (iframes and JS are stripped), so the auto-scroll is the closest option.
- To verify animations, use real-time headless Edge over CDP. `--virtual-time-budget` screenshots and the app's preview pane both show SVG animations frozen.
- SVG text doesn't wrap, so keep card description lines under about 55 characters for half-width cards and under about 68 for wide cards.
- Only feature repos that are public, plus the live EASTARCH site (its repo is private).
