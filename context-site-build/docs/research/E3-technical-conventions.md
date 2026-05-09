# E3 — Awwwards-Tier Site Engineering: Technical Conventions (2024–2025)

> Research conducted 2026-05-08 by a `general-purpose` subagent
> spawned during the v0.2 architecture-planning pass on
> context-site-build. ~68 web fetches across agency case studies,
> web.dev/Vercel material, conference posts, GitHub source, and
> design-system documentation.

Evidence-based input for a `context-site-build` skill library, drawn from agency case studies, web.dev/Vercel material, conference posts, GitHub source, and design-system documentation. Where consensus exists I name it; where the standard is honestly weak (a11y), I name the gap.

---

## 1. Performance Budgets — Realistic for Motion/WebGL-Heavy Sites

### 1.1 Core Web Vitals reality check

| Metric | Google "good" (p75) | Awwwards-tier reality |
|---|---|---|
| LCP | ≤ 2.5 s | Top sites hit ~1.3 s desktop / ~1.7 s 4G when disciplined ([Active Theory portfolio reported figures](https://medium.com/active-theory/the-story-of-technology-built-at-active-theory-5d17ae0e3fb4)); WebGL-heavy "art" sites often miss it on mobile |
| INP | ≤ 200 ms | The Achilles heel of WebGL + scroll-jacked sites; main-thread shader compile + Lenis RAF easily push past 300–500 ms on mid-range Android ([web.dev INP guidance](https://web.dev/articles/inp)) |
| CLS | ≤ 0.1 | Achievable; the discipline is reserving aspect-ratio boxes for video/canvas |

The 2025 Web Almanac reports **only 48% of mobile pages and 56% of desktop pages pass all three CWV** ([cited in CWV 2025 guides](https://www.gobyweb2.com/core-web-vitals-guide/)). LCP is the hardest of the three to pass. Hero-WebGL sites that "look winning" frequently **fail field LCP** on 4G but pass lab Lighthouse — a known gap.

### 1.2 How hero-WebGL sites legitimately keep LCP < 2.5 s

The pattern across Active Theory, Lusion, Igloo, and 14islands:

1. **LCP element is HTML, not the canvas.** A static hero image (or a `<h1>`/poster) renders first; the `<canvas>` initialises behind it. The canvas gets `pointer-events: none` until ready, then a fade swaps the layers. ([web.dev: don't lazy-load LCP](https://gtmetrix.com/dont-lazy-load-lcp-image.html), [Cloud Four: stop lazy-loading hero images](https://cloudfour.com/thinks/stop-lazy-loading-product-and-hero-images/)).
2. **`fetchpriority="high"` on the poster image, `loading="eager"`, preload its variant.** Never lazy-load the LCP element.
3. **WebGL is initialised after `requestIdleCallback` or after first interaction.** Active Theory's portfolio is documented doing this — meshes via Draco, video via `requestIdleCallback`.
4. **Background shader compilation + staged texture loading** — Igloo Inc's documented approach ([Igloo case study](https://www.awwwards.com/igloo-inc-case-study.html)): real-time shader iteration, custom geometry exporters minimise loading time, textures stream in stages so the scene appears progressively rather than blocking on a giant payload.
5. **Skeleton 3D**: a low-poly LOD or a pre-rendered video poster shows while the high-quality scene streams. Three.js docs and community recommend this LOD pattern explicitly ([three.js forum: lazy-loading 3D scenes](https://discourse.threejs.org/t/lazy-loading-parts-of-a-large-scene/31831)).

### 1.3 Network/CPU budgets agency tech leads commit to

Synthesizing Alex Russell's "Can You Afford It?" ([infrequently.org](https://infrequently.org/2017/10/can-you-afford-it-real-world-web-performance-budgets/)), Addy Osmani's [performance budget post](https://addyosmani.com/blog/performance-budgets/), the Three.js best-practices reference at [utsubo.com](https://www.utsubo.com/blog/threejs-best-practices-100-tips), and stated agency budgets:

| Resource | Marketing-site target | WebGL-hero target |
|---|---|---|
| Critical-path JS (gz, on-wire) | ≤ 130–170 KB | ≤ 200 KB excluding three.js core |
| Total JS (gz) | ≤ 300 KB | ≤ 600 KB; three.js + drei + R3F alone ≈ 200–250 KB |
| CSS | ≤ 20–40 KB | Same |
| Image weight (above fold) | ≤ 500 KB | ≤ 1 MB (poster + LQIP) |
| Total page weight | ≤ 1.5–2 MB | 3–6 MB acceptable; 10 MB+ is the danger zone |
| Time-to-Interactive (Slow 3G / Moto G4) | ≤ 5 s first load | ≤ 7 s first load, ≤ 2 s subsequent |
| Draw calls / frame | n/a | ≤ 100 (smooth 60 fps), > 500 even strong GPUs struggle |
| Active lights with shadows | n/a | ≤ 3 |
| GPU texture VRAM (with KTX2) | n/a | < 100 MB; one 4K texture can hit 64 MB+ |

Tinder's documented public budget is **170 KB main JS, 20 KB CSS, enforced via `bundlesize` on every PR** ([Osmani](https://addyosmani.com/blog/performance-budgets/)). For motion-heavy sites the equivalent enforcement tools are [`size-limit`](https://github.com/ai/size-limit), webpack `performance.hints`, and Calibre/SpeedCurve in CI.

---

## 2. Motion Library Stack

### 2.1 Current consensus (2024–2025)

| Library | What it's used for | Typical caller |
|---|---|---|
| **GSAP (with ScrollTrigger / SplitText / Flip)** | Marketing hero, scroll-driven scenes, complex sequenced timelines, anything cinematic | Bruno Simon, Igloo, Federico Pian, Working Stiff Films, virtually every Awwwards SOTD |
| **Motion (formerly Framer Motion → motion.dev)** | App-shell UI, layout transitions, gestures, exit animations in React. Now has a vanilla JS variant (Motion One) | Linear, Vercel, most product UIs |
| **Motion One** (vanilla, WAAPI-based) | Tiny pages (3.8 KB animate fn), CMS sites where every KB matters, design-system primitives | Sites where the motion is "reactive UI" not "scene direction" |
| **Native CSS scroll-driven animations** (`animation-timeline: scroll() / view()`) | Simple parallax and reveal where Chromium-only is acceptable | Increasingly used as a progressive-enhancement layer in 2024–2025 ([Chrome DevRel](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)) |
| **Lottie / Rive** | Designer-authored micro-animations, illustrations | MindMarket case study uses Rive triggered via IntersectionObserver |

The **operating consensus** in agency code: **GSAP for marketing/scene direction, Motion (Framer Motion) for app UI, native CSS for the cheap stuff, Rive/Lottie for illustration**. GSAP went **fully free including all plugins under MIT** in mid-2024 (Webflow acquisition), removing the historical licensing friction.

### 2.2 Lenis (smooth scroll) — when used, when avoided

Lenis is built by **darkroom.engineering** (formerly Studio Freight). MIT, ~3 KB, ~13.8K stars ([github.com/darkroomengineering/lenis](https://github.com/darkroomengineering/lenis), [lenis.dev](https://www.lenis.dev/)).

**When teams reach for it:**
- WebGL-DOM sync sites where the canvas must track DOM scroll positions (it's the engine inside [`@14islands/r3f-scroll-rig`](https://github.com/14islands/r3f-scroll-rig) and [Locomotive Scroll v5](https://scroll.locomotive.ca/)).
- "Cinematic" feel with damped inertia; the visual signature of a Resn / Active Theory / Lusion-tier build.

**When teams avoid it:**
- Long-form content (docs, blogs). The momentum becomes a barrier to scanning.
- Sites where keyboard/PageDown/`Space`/screen-reader scrolling matters — Lenis hijacks wheel/touch and breaks user expectations.
- Inside iframes (it doesn't forward wheel events).
- Safari < M1 (position:fixed lag, 60 fps cap, 30 fps in low-power mode).
- `prefers-reduced-motion: reduce` users — must be hard-disabled or it's an accessibility violation. The library does **not auto-respect** the media query; teams must wire it up explicitly.

### 2.3 ScrollTrigger / ScrollSmoother — how teams structure scenes

The dominant agency pattern (visible in Codrops case studies, GSAP forums, and 14islands' open source):

1. **One global ScrollTrigger + Lenis (or ScrollSmoother) bootstrap** at the app root. ScrollTrigger `.scrollerProxy()` is used so Lenis's virtualised scroll position is the source of truth.
2. **Scenes scoped per "chapter"** — each scroll section is a `gsap.context(() => { ... }, ref)` (or `useGSAP` hook) so unmounting cleans up triggers.
3. **`scrub: true` for tight scroll-coupled motion**, otherwise `toggleActions` with named labels.
4. **`pin: true` for long-form pinned scenes** — the workhorse of "scrolly-telling" hero sequences; ScrollSmoother adds variable-speed parallax via `data-speed`.
5. **For R3F**: ScrollTrigger drives a shared `progress` value via `onUpdate`; `useFrame` reads it. Or, more idiomatic, drei's `ScrollControls` + `useScroll().offset` is used, paired with `useGSAP` for HTML overlays. Theatre.js is the pro-grade alternative when motion designers want a timeline editor.

### 2.4 Confirmed usage in winning sites

| Site | Confirmed stack |
|---|---|
| **Igloo Inc** (Site of the Year 2024) | Three.js + three-mesh-bvh + **Svelte** + **GSAP** + Vite |
| **Federico Pian Portfolio 2024** | Nuxt 3 + Tailwind + **GSAP (SplitText, Flip)** + TresJS (Vue Three.js wrapper) |
| **Rogier de Boevé 2024** | **Astro** + Three.js + Alien.js + **GSAP** + **Lenis** + Howler |
| **14islands** | React/Next.js + Sanity + **Framer Motion** + **Lenis** + **Lottie** + r3f-scroll-rig |
| **Working Stiff Films** | **GSAP**-only DOM timelines, no WebGL |
| **Active Theory** | In-house **Hydra** engine (Three.js until mid-2018) |

---

## 3. WebGL / Three.js Conventions

### 3.1 R3F vs vanilla Three.js — when each

| Factor | Reach for R3F | Reach for vanilla Three.js |
|---|---|---|
| App is React | ✅ default | If the canvas is purely the page chrome and the rest is HTML, vanilla is fine |
| Many independent objects with their own camera/lights | ✅ portals, viewports | Manual scene graph bookkeeping |
| Need drei helpers (loaders, controls, environment, instancing, shaders) | ✅ — typical agency time-saver | — |
| Need raw WebGL/WebGPU pipeline control (memory pooling, custom render targets, atypical RAF) | — | ✅ |
| Game / simulation-grade | Possible since R3F physics matured 2024–2025 | Still preferred for tight control |
| Non-React framework (Svelte / Vue / Astro / vanilla) | Not applicable | ✅ vanilla, or Svelte-Cubed / TresJS |

The **agency justification** repeated across [creativedevjobs](https://www.creativedevjobs.com/blog/react-three-fiber-vs-threejs), [elkayal.me](https://elkayal.me/article/react-three-fiber-vs-vanilla-three-js-what%E2%80%99s-right-for-your-project/), and [discourse.threejs.org](https://discourse.threejs.org/t/threejs-or-r3f-technology-pick/57973): drei collapses 20–30 lines of vanilla Three.js setup into 1–2 lines (loading a glTF, setting environment lighting, OrbitControls). For agency time pressure that's decisive. Vanilla is preferred by studios with proprietary engines (Active Theory's Hydra, Lusion's custom pipelines) or for non-React stacks (Igloo Inc uses Svelte + vanilla Three.js).

### 3.2 Common patterns

- **Custom GLSL shaders for hero effects** — reveal masks, distortions, ASCII/dot-matrix passes. The Codrops corpus is essentially the canon: shader-based reveal effects, 3D bulge/distortion text, liquid raymarching scenes.
- **Post-processing**: `postprocessing` library (Vanruesc) over Three's stock `EffectComposer` for performance — bloom, chromatic aberration, vignette, custom passes.
- **GPGPU for particles** — using a render target as a position buffer, ping-ponged each frame. Agency-grade alternative to CPU `BufferAttribute` updates.
- **Scene composition for chapters** — ScrollControls' page-based slicing, or independent viewports per section (r3f-scroll-rig pattern). Chapters get their own camera + lights to bound complexity.
- **WebGL UI for text effects** (glitch, scramble) — Igloo Inc explicitly chose WebGL UI over HTML/CSS for these, because shader-based per-glyph effects are cheaper than DOM mutation.
- **Instanced rendering everywhere** — the [utsubo 100 tips post](https://www.utsubo.com/blog/threejs-best-practices-100-tips) reports a real-world reduction from 9,000 → 300 draw calls by switching to instancing; LOD gives 30–40% FPS uplift.

### 3.3 Asset pipeline — glTF + Draco + KTX2

Canonical pipeline ([gltf-transform.dev](https://gltf-transform.dev/), [CesiumGS/gltf-pipeline](https://github.com/CesiumGS/gltf-pipeline), [utsubo tips](https://www.utsubo.com/blog/threejs-best-practices-100-tips)):

1. Author in Blender / Houdini / Cinema 4D.
2. Export glTF 2.0 (`.glb`).
3. Run `gltf-transform optimize --compress draco --texture-compress ktx2` (or use `gltfpack`).
4. **Draco**: ~90–95% geometry size reduction; decode in a Web Worker via Three.js `DRACOLoader`.
5. **KTX2 (Basis Universal)**: UASTC for high quality, ETC1S for tighter compression. Stays compressed on the GPU → ~10× VRAM saving. Ship via Three.js `KTX2Loader`. A 200 KB PNG occupies 20 MB+ of VRAM uncompressed; the same texture as KTX2 stays at ~2 MB on the GPU.
6. **Combined Draco + KTX2 ⇒ 70–90% file-size reduction** with negligible perceived quality loss.

For meshes that can't be Draco'd (animated cloth, vertex anim) — Lusion's published technique ([their pipeline post](https://medium.com/lusion-ltd/from-concept-prototyping-to-production-in-a-creative-studio-f2083e96c4b9)) — bake into a 128³ voxel PNG with SDF gradient in RGB and signed distance in alpha; sample in shader. Cloth animation came in at **983 KB desktop / 246 KB mobile** that way.

### 3.4 Performance instrumentation

The triad agencies actually use:

| Tool | What it tells you |
|---|---|
| `THREE.WebGLRenderer.info` | Live `calls`, `triangles`, `points`, `lines`, `geometries`, `textures`, `programs` — watch these stay stable to catch leaks |
| **stats-gl** (or stats.js) | FPS / frame time / GPU time overlay for live profiling |
| **[Spector.js](https://chromewebstore.google.com/detail/spectorjs/denbgaamihkadbghdceggmchnflmhpmk)** (Chrome extension) | Frame capture: every WebGL call, draw, shader, texture state. The standard "what is my GPU actually doing" tool. Compatible with R3F |
| **lil-gui** | Live param tweaking; standard alternative to dat.gui |
| Chrome DevTools **Performance** panel | Long tasks, INP root-causes, hydration pauses |
| Chrome DevTools **GPU** panel + **Memory** tab | Texture/VRAM tracking |

Production discipline: ship `stats-gl` behind a `?debug` query flag; bake `WebGLRenderer.info` polling into your error monitoring (Sentry custom metric) so you spot scene-graph regressions in the field.

---

## 4. Accessibility on Motion-Heavy Sites

### 4.1 The honest reality

Awwwards-tier sites have **systematically poor a11y posture**. Most fail at multiple levels:

- Custom cursors that don't change for keyboard focus
- Scroll-jacking that breaks `Space`, `PageDown`, screen-reader skip links
- Text-as-WebGL with no DOM equivalent (Igloo Inc does some of this — beautiful, but blind to screen readers)
- Decorative `<canvas>` with no `aria-hidden="true"` and no equivalent text alternative
- Hover-only navigation without focus-visible parity
- Animations that ignore `prefers-reduced-motion`
- "Loading" experiences that block keyboard for 5+ seconds with no skip

The **agency consensus** in 2024–2025 is "we ship a Reduce-Motion CSS branch and call it done." The **WCAG 2.2 reality** is much stricter.

### 4.2 `prefers-reduced-motion` patterns — three flavours

| Pattern | Description | When |
|---|---|---|
| **Hard-disable** | Wrap motion in `@media (prefers-reduced-motion: no-preference) { … }`. Smooth scroll, parallax, autoplay carousels, hover transitions all simply don't happen. Static content shown instead. | The default and only safe approach for decorative motion |
| **Soft-degrade** | Replace large vestibular triggers (full-page swipes, parallax, zoom-in/out) with `opacity` cross-fades. Functional motion (e.g. tooltip slide-in) keeps a 100ms version. | Component design systems; what Material/Carbon do |
| **Alternative experience** | Whole alternative content path — e.g. a static "lite" version or a `<noscript>`-style HTML-only hero. | When the motion *is* the message (cinematic site, scrolly-telling) |

The opt-in pattern: write base CSS *without* motion, then layer it inside `@media (prefers-reduced-motion: no-preference)`. This makes "no motion" the safe default.

### 4.3 Keyboard navigation on scroll-jacked / cursor-driven sites

Actual patterns observed:

- **Skip links to chapters** — `aria-label`'d "Skip to next section" buttons.
- **Focus trap inside the active "page"** in a scroll-snap site, with `Tab` cycling intra-section.
- **Arrow keys consume scroll** — bind `ArrowDown`/`PageDown`/`Space` to ScrollTrigger's `gotoSection(i+1)`.
- **`prefers-reduced-motion` + hijacked-scroll users get native scroll back**. Lenis is destroyed; sections become normal long-scroll columns. The only pattern that works for WCAG 2.1.1.

### 4.4 The honest gap

| WCAG 2.2 says | Awwwards-tier reality |
|---|---|
| 2.1.1 Keyboard (A) — all functionality keyboard-accessible | Custom cursors and drag-only interactions routinely break this |
| 2.2.2 Pause, Stop, Hide (A) — auto-updating motion must have a control | Hero loops rarely have a pause control |
| 2.3.3 Animation from Interactions (AAA) — non-essential animation can be disabled | Honoured only via `prefers-reduced-motion` — and only for sites that bothered |
| 2.4.7 Focus Visible (AA) — focus indicator must be visible | Custom cursors often suppress focus rings without replacement |
| 2.5.7 Dragging Movements (AA, new in 2.2) — drag must have a single-pointer alternative | "Drag to explore" interactions almost universally fail |
| 2.5.8 Target Size (Minimum) (AA, new in 2.2) — 24×24 CSS px | Tight cursor-driven UIs frequently fail |

**Build-skill recommendation**: ship a "motion-conformance" template that codifies `prefers-reduced-motion` opt-in CSS, a global motion toggle in the UI, focus-visible parity for any custom cursor, keyboard scroll bindings, and a non-WebGL "lite mode" alternative experience. Bake `axe-core` + Lighthouse CI into the pipeline. Be honest in the skill that automated tools catch only **30–40%** of real barriers — the rest needs manual keyboard testing.

---

## 5. Recurring Stack Combos

Across confirmed source-inspections of Awwwards SOTD/SOTY sites and agency tech-stack posts, four canonical combos repeat:

### Combo A — "React-cinematic" (the most common)
- **Frontend**: Next.js (App Router) + TypeScript
- **Animation**: GSAP + ScrollTrigger + (Motion/Framer Motion for app UI)
- **Smooth scroll**: Lenis (often via @14islands/r3f-scroll-rig)
- **3D**: React Three Fiber + drei + @react-three/postprocessing
- **CMS**: Sanity (GROQ + Studio)
- **Hosting**: Vercel
- **Assets**: Cloudinary or self-hosted on Vercel Blob; Mux for any HLS/streaming video
- **Email**: Resend (transactional) + Loops (marketing) — increasingly the default 2024–2025
- **Analytics**: Plausible or Fathom; PostHog if product analytics + experiments are needed
- **Emblematic sites**: 14islands.com, basement.studio, Federico Pian–style portfolios, Vercel's own marketing properties

### Combo B — "Vue/Nuxt-cinematic"
- **Frontend**: Nuxt 3 + Tailwind + Pinia
- **Animation**: GSAP + plugins
- **3D**: TresJS (Vue wrapper around Three.js)
- **CMS**: Sanity or Storyblok (Storyblok especially strong here because of its Vue-first visual editor)
- **Hosting**: Vercel or Netlify
- **Emblematic sites**: Federico Pian Portfolio 2024, Akaru (Nuxt 3 + Sanity), many French/Belgian agency portfolios

### Combo C — "Astro-static-with-WebGL-islands"
- **Frontend**: Astro + Vite + Tailwind + PostCSS
- **Animation**: GSAP + Lenis + (Howler for audio)
- **3D**: vanilla Three.js + Alien.js, or React island with R3F where React is justified
- **CMS**: none (JSON files in repo) or Sanity for content-driven projects
- **Hosting**: Vercel, Netlify, or Cloudflare Pages
- **Emblematic sites**: Rogier de Boevé Portfolio 2024, many engineering-focused personal portfolios. Astro's strength is the **only major framework where >50% of sites pass CWV** (cited from Web Almanac 2023).

### Combo D — "Svelte/SvelteKit, when the lead is performance-pure"
- **Frontend**: SvelteKit + Vite
- **Animation**: GSAP + Svelte's native `crossfade`/`flip` for UI
- **3D**: vanilla Three.js (Svelte-Cubed exists but is less mature than R3F or TresJS)
- **CMS**: Sanity, sometimes Hygraph
- **Hosting**: Vercel, Netlify, Cloudflare Pages
- **Emblematic sites**: **Igloo Inc** (Site of the Year 2024 — Svelte + vanilla Three.js + GSAP); a non-trivial slice of the Awwwards Developer category

### Wider stack notes

- **Hosting**: Vercel dominates Next.js sites; Cloudflare Pages is rising fast in 2025 (especially for Astro). Netlify retains a Nuxt/Astro footprint.
- **CMS distribution** (Wappalyzer signals as of 2024): Sanity ~42K live sites, Storyblok ~15K, Contentful much larger but skews enterprise rather than creative. Prismic and DatoCMS occupy a long tail. **Strapi** is largely absent from Awwwards-tier — self-hosting is friction.
- **Forms / leads**: Resend + React Email for transactional; Loops for marketing sequences; HubSpot only when the client requires it.
- **Analytics privacy posture**: Top agencies have largely **moved off GA4** for marketing sites — Plausible (open-source, EU-hosted), Fathom (Canadian, EU isolation), or PostHog (self-hostable, full product analytics).
- **Asset pipeline / DAM**: For images, **Cloudinary** when there's marketing-team self-service, else **Vercel/Next.js `<Image>`** with the platform's built-in optimisation. **Imgix** for URL-driven CDN image transforms when DAM features aren't needed. **Mux** is the runaway choice for any non-trivial video.

---

## 6. Tooling Conventions

### 6.1 Design tokens

The 2024–2025 reality:

- **W3C DTCG specification reached its first stable version Oct 2025** ([W3C announcement](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)). Editors include Adobe, Google, Figma, Salesforce, Shopify, Tokens Studio.
- **Style Dictionary v4** has first-class DTCG support and is the de-facto agency choice for transforming JSON tokens → CSS / SCSS / TS / Tailwind config / iOS / Android outputs.
- **Tokens Studio (Figma plugin)** is the most common upstream source-of-truth on the design side. The bridge to Style Dictionary is `@tokens-studio/sd-transforms`.
- **Tailwind config tokens**: The 2024–2025 pattern is *not* hard-coded `tailwind.config.js`. Style Dictionary emits `tokens.css` with CSS custom properties, and Tailwind v4 `@theme` reads them.
- **Vanilla CSS variables** with `:root { --color-… : … }` is still the production-shipped layer; tokens flow into them. Avoid CSS-in-JS for token wiring — runtime cost.

**Recommendation**: codify a "tokens" convention that is *DTCG JSON → Style Dictionary → CSS variables + Tailwind v4 @theme + TypeScript export*, with a watch script in the dev loop and a CI gate that fails the build if `tokens.json` is edited without regenerating outputs.

### 6.2 Component states matrix

The "9-state" matrix (default / hover / focus / focus-visible / active / disabled / loading / error / empty / skeleton) is **rigorously documented in mature design systems** (Carbon, Material, GitLab Pajamas, the Australian Government Agriculture DS, the Intelligence Community DS). It is **inconsistently documented at agencies** — most ship default + hover + active + a sloppy skeleton, and reach for empty/error states only when the page demands them.

**Recommendation**: the component scaffolder must generate a stories file with all 9 states stubbed and refuse to mark a component "ready" until each state is filled in.

### 6.3 Motion specs

| Approach | Where used |
|---|---|
| **Motion principles doc in Notion/Markdown** (durations, easings, choreography) | Most teams that have any motion language |
| **Motion tokens in the design system** (`motion-duration-fast: 150ms`, `motion-ease-out: cubic-bezier(0.16, 1, 0.3, 1)`) | Mature DSes (IBM Carbon, Material, FluentUI). Agency work is catching up |
| **Lottie/Rive files** + Storybook-embedded previews | When motion designers own the spec |
| **Theatre.js studio captures** | When a motion designer needs timeline-grade authoring with a visual scrubber |
| **Figma Smart Animate / Motion plugin screencaps** | Most common "spec" hand-off in practice — fragile but quick |
| **GSAP Timelines as the spec** | Engineer-led teams; the timeline *is* the documentation |

The IBM model (motion as expressive vs productive) and the Material model (informative / focused / expressive × hierarchy / feedback / status / character) are the two named taxonomies in active use. Motion tokens follow the naming `{prefix}-motion-{property}-{modifier}`, e.g. `motion-duration-medium-2`.

### 6.4 Storybook vs Ladle

- **Storybook 8/9/10** is the enterprise default. It carries the full ecosystem (Chromatic, addons, MDX docs, Vitest integration, multi-framework).
- **Ladle** is Vite-native, esbuild-fast (1.2 s cold / <500 ms hot vs Storybook's 8 s / 2 s), React-only, and is a drop-in replacement for stories. **Used at Uber across 335 projects with ~16K stories.**
- **Histoire** is the Vue-native equivalent.

**Recommendation**: Storybook for production design systems, Ladle for solo-dev portfolios where startup time matters and the team is React-only.

### 6.5 Visual regression

- **Chromatic** dominates the Storybook-shop space — built by the Storybook team, free for open source, TurboSnap optimises diff cost, GitHub PR integration is best-in-class.
- **Percy** is the cross-framework / non-Storybook alternative; CI-first; BrowserStack-owned.
- **Loki** is a free Storybook-only visual regression runner.
- **Lost Pixel** and **Playwright `toHaveScreenshot()`** are the rising open-source options.

### 6.6 Design-to-dev handoff

The 2024–2025 default chain:

1. **Figma** (with variables + Tokens Studio + Auto Layout + Component Properties) → source of truth for tokens *and* component specs.
2. **Tokens Studio** exports DTCG JSON → repo.
3. **Style Dictionary** transforms JSON → CSS variables + Tailwind v4 `@theme` + TS types.
4. **Storybook** (with Chromatic) renders components against the live tokens, shows all 9 states, and is the contract between design and engineering.
5. **Motion tokens** flow the same way; motion principles doc lives in Notion or `docs/motion.md`.

**Anti-patterns**:
- Hand-coded `tailwind.config.ts` with hex values (no token sync).
- "Storybook is just for the engineer" — it must be the design-review surface.
- Motion specs as Loom links — they decay; use Theatre.js or a Lottie/Rive file in Storybook instead.
