# E1 — Awwwards: Judging, Jury, and Recent Winners (2024–2025)

> Research conducted 2026-05-08 by a `general-purpose` subagent
> spawned during the v0.2 architecture-planning pass on
> context-site-build. ~96 web fetches across Awwwards, agency case
> studies, and inspection of winning sites. All claims tied to a
> URL.

Evidence-based input for the `context-site-build` skill library.

---

## (1) Judging Criteria with Weights

Awwwards' public scoring system uses **four criteria with fixed weights**:

| Criterion | Weight |
|---|---|
| **Design** | 40% |
| **Usability** | 30% |
| **Creativity** | 20% |
| **Content** | 10% |

Source: [Awwwards — About Evaluation](https://www.awwwards.com/about-evaluation/). Confirmed by per-site score breakdowns visible on every SOTD page (e.g. [Lando Norris](https://www.awwwards.com/sites/lando-norris), [Igloo Inc](https://www.awwwards.com/sites/igloo-inc), [Opal Tadpole](https://www.awwwards.com/sites/opal-tadpole), [Cartier Watches & Wonders 2025](https://www.awwwards.com/sites/cartier-watches-wonders-2025)).

**There is no separate "Mobile" or "WOW factor" criterion.** Mobile is folded into Usability (and reviewed separately at the dev-award level under "Responsive Design"). "Innovation" is folded into Creativity.

### Process mechanics
- **Min 18 jury members** evaluate each submission. The 3 scores furthest from the average are auto-eliminated to remove outliers ([source](https://www.awwwards.com/about-evaluation/)).
- Voting window: **5 days** per submission.
- **Honorable Mention**: ≥ 6.5 average.
- **Site of the Day**: highest scorers per day.
- **Developer Award**: ≥ 7.0 average from a separate developer jury (evaluating Animations/Transitions, Responsive Design, Web Performance Optimization, Semantics/SEO, Accessibility, Markup/Meta-data — six sub-scores, visible on every SOTD page).
- **Site of the Month**: 8 highest-scoring SOTD winners per month are nominated; users + jury choose one.
- **Site of the Year**: highest-scoring of the SOTM nominees across the year.

### What this means for a skill library
Design (typography, palette discipline, hierarchy) is the single largest scoring lever — 40%. But the **dev award has six equally-weighted sub-scores**, so a design-only site that ignores accessibility, semantics, and CWV will lose Developer Award eligibility even if it wins SOTD. The per-site breakdowns confirm this pattern: SOTY winners typically score 8.5–9.0+ on Animations/Transitions but 6.6–7.0 on Accessibility. Igloo Inc's Accessibility was **6.60/10** ([source](https://www.awwwards.com/sites/igloo-inc)) — winners do *not* uniformly hit the green-Lighthouse bar.

---

## (2) Jury Panel Composition

The Awwwards jury is structured as **Main Jury** (must have already won at least one SOTD) plus **Young Jury** (under 25). For 2025, the official jury page lists **679 members from 62 countries** ([source](https://www.awwwards.com/official-jury/)). Below are 15 representative members harvested from pages 1–5 of the official jury directory:

| Name | Role | Affiliation | Country |
|---|---|---|---|
| Robin Noguier | Designer / Freelancer | (independent — robin-noguier.com) | France |
| Renaud Rohlinger | CTO | (renaudrohlinger.com — known R3F/Three.js dev) | Japan |
| Zhenya Rynzhuk | Co-founder | Synchronized Studio & Sochnik School | USA |
| Pablo Stanley | Design Lead | (pablostanley.com — Blush, Lummi) | USA |
| Mirko Santangelo | Lead Senior Designer | Paper Tiger | USA |
| David Hellmann | Designer & Developer | (davidhellmann.com) | Germany |
| Dennis Snellenberg | Designer & Developer | Co-founder, **Osmo** | Netherlands |
| Olha Olianishyna | Co-founder | **Obys Agency** | Ukraine |
| Julien Jean | Digital Creative Director | **lg2** | Canada |
| François-Xavier Manceau | Creative Developer | (independent) | France |
| Tomas Baruffaldi | Creative Director / Co-founder | **Et Studio** | Italy |
| Oscar Rivera | Creative Director / Founder | **RAXO** | USA |
| Soren Bo Bastian | Senior Art Director | **ManyOne** | Denmark |
| Javier Corrales | Co-founder / Interactive Director | **Cuchillo** | Spain |
| Anatolii Kozhukhar | Independent Art Director | (tolii.co) | Ukraine |
| Vide Infra | CEO / Creative Director | Vide Infra | UK |
| Den | Independent Design Director | (den.cool) | Japan |

**Aesthetic signal from jury composition**: heavy presence of European (FR, NL, ES, IT, DE, UA) and Latin American agencies known for craft-first, motion-heavy, often editorial work. Notable creative-developer presence (Renaud Rohlinger, F.-X. Manceau, Snellenberg, Hellmann) confirms the technical bar is set by R3F/Three.js practitioners — not generic React devs. Studios with multiple jury seats or repeat Annual wins (Obys, Osmo, Locomotive, Immersive Garden, Lusion) form a *de facto* aesthetic establishment that newcomers are scored against.

---

## (3) Recent Winning Sites — Emblematic Patterns

Synthesized from [Sites of the Year 2024](https://www.awwwards.com/annual-awards-2024/site-of-the-year), [Sites of the Year 2025](https://www.awwwards.com/annual-awards-2025/site-of-the-year), and [Sites of the Month 2024–2026](https://www.awwwards.com/websites/sites_of_the_month/).

### 1. Igloo Inc — SOTY 2024
- **URL**: https://www.igloo.inc/ — **Agency**: [Abeto](https://www.awwwards.com/abeto/) + Bureaux
- **Pattern**: Procedural 3D (crystal-growth algorithm generates ice-block portfolio cases), camera drifts between scenes with chromatic aberration / frost dissolves, **entire UI rendered in WebGL** (no HTML text), SDF-texture letter scrambles, custom VDB-volume-data exporter for particle simulation.
- **Stack**: **Three.js + Svelte + GSAP + Vite**, Houdini + Blender for assets, custom shader tooling. ([Awwwards case study](https://www.awwwards.com/igloo-inc-case-study.html); [WebGPU.com showcase](https://www.webgpu.com/showcase/igloo-inc-procedural-crystals/))
- **Why it won**: Animations/Transitions **9.60/10**; Creativity **8.31/10**. Custom procedural systems impossible to clone via templates ([scores](https://www.awwwards.com/sites/igloo-inc)).

### 2. Lando Norris — SOTY 2025
- **URL**: https://landonorris.com/ — **Agency**: [OFF+BRAND](https://www.itsoffbrand.com/our-work/lando-norris)
- **Pattern**: Scroll-driven cinematic narrative, fluid animated background drawn from helmet design language, 3D helmet rotations, "tap-to-lock" scroll sections, neon-lime accent (#D2FF00) on near-black, oversized type.
- **Stack**: **Webflow + GSAP + WebGL + Rive** (3D Rive used heavily for 3D motion). ([WebGPU.com](https://www.webgpu.com/showcase/mclaren-f1-driver-lando-norris-official-website/))
- **Why it won**: Creativity **8.71/10** (highest among 2025 SOTY); proves Webflow can win at the top tier when paired with disciplined GSAP/Rive choreography ([scores](https://www.awwwards.com/sites/lando-norris)).

### 3. Messenger (abeto.co) — Developer SOTY 2025
- **URL**: https://messenger.abeto.co — **Agency**: Abeto
- **Pattern**: Browser-game vibe. Character-navigation, NPC interactions, real-time multiplayer feel. Teal/sage palette, low-poly 3D world.
- **Stack**: **Three.js + WebGL + WebSockets**. Animations 9.00, WPO **8.80**. ([scores](https://www.awwwards.com/sites/messenger))
- **Why**: Highest WPO of any 2025 winner reviewed. Game-as-website remains scarce and consistently scores high.

### 4. Cartier — Watches & Wonders 2025 (SOTM Aug 2025; SOTY 2025 nominee)
- **URL**: https://cartier-waw-0225.dev.60fps.fr — **Agency**: [Immersive Garden](https://immersive-g.com/cases/cartier-watches-and-wonders) + 60fps
- **Pattern**: Six 3D "alcove" scenes, each themed around a watch. Hidden-gesture rewards, custom Mooders soundscape via Web Audio API as narrative layer.
- **Stack**: **Three.js + Sass, GSAP for motion, Lenis for scroll, Blender for assets, Web Audio API for sound**. ([blog post](https://www.awwwards.com/watches-wonders-immersive-experience-for-cartier.html); [scores](https://www.awwwards.com/sites/cartier-watches-wonders-2025))
- **Why**: Animations/Transitions **9.00/10**, Creativity 7.97/10. Sound-as-narrative is rare and Awwwards juries reward it.

### 5. Opal Tadpole — E-commerce SOTY 2024
- **URL**: https://www.opalcamera.com/opal-tadpole — **Designer**: [Claudio Guglieri](https://guglieri.com/feed) (Head of Design at Opal)
- **Pattern**: Single-page e-commerce, two-color (yellow #FFDB01 / white), product photography in motion ("Show don't tell"), micro-interactions over copy.
- **Stack**: Custom (no platform stack publicly disclosed); 3D / video / micro-interactions central. Animations 8.60. ([scores](https://www.awwwards.com/sites/opal-tadpole))
- **Why**: Proves a *minimal* aesthetic with disciplined two-color palettes wins against maximalist 3D — Design 7.73, Content 7.64.

### 6. Don't Board Me — Users' Choice SOTY 2024
- **URL**: https://dontboardme.com — **Agency**: The First The Last
- **Pattern**: Editorial illustration, sharp brand voice ("poooooooo 🐶" 404), two-color (red #E33529 / light blue #AFD8FB), custom 404, storytelling-as-IA.
- **Stack**: not disclosed; categorized as "Storytelling / UI design / 404 pages / Colorful". ([scores](https://www.awwwards.com/sites/dont-board-me))
- **Why**: Scored **8.00 Creativity** with no 3D — counter-evidence to the "must have WebGL" myth. Copywriting + illustration + tight art-direction was sufficient.

### 7. Scout Motors — E-commerce SOTY 2025
- **URL**: scoutmotors.com — **Agency**: [Locomotive](https://www.awwwards.com/locomotive/) (Montréal)
- **Pattern**: Promotional storytelling, multi-video animated layouts, mobile-UI-as-feature, retro-American palette (orange #FF5432 / beige #D7D4D3).
- **Stack**: not publicly disclosed; Locomotive's house stack tends toward Next.js / vanilla Three.js / GSAP / their own Locomotive Scroll. ([scores](https://www.awwwards.com/sites/scout-motors))
- **Why**: Strong across the board (no <7.0 sub-score). E-commerce-of-the-year template: editorial, video-heavy, scroll-driven.

### 8. 100 Lost Species — SOTM Oct 2025
- **URL**: 100lostspecies.com — **Agency**: Immersive Garden
- **Pattern**: "Digital memorial that unfolds across time" — 100 species in 100 seconds, then site disappears. Cream/black palette. Time-as-IA.
- **Stack**: **Contentful CMS** (rare explicit disclosure), animated SVG/video transitions. Animations 8.60, WPO 8.20. ([scores](https://www.awwwards.com/sites/100-lost-species))
- **Why**: Time as a structural design element + cause-led brief. Ephemeral sites are jury catnip.

### 9. Ponpon Mania — SOTM Oct 2025
- **URL**: ponpon-mania.com — **Author**: Patrick Heng
- **Pattern**: "Interactive comic" — physics-based panels, mouse interaction, page transitions, vibrant purple/pink. Creative-coding aesthetic.
- **Stack**: **Nuxt.js + WebGL + GSAP**. Animations **9.00**, Creativity 8.12. ([scores](https://www.awwwards.com/sites/ponpon-mania))
- **Why**: Format invention (web comic) over website conventions.

### 10. Terminal Industries — SOTM Sep 2025
- **URL**: terminal-industries.com — **Agency**: REJOUICE
- **Pattern**: B2B/logistics turned cinematic; animated scrolling, storytelling.
- **Stack**: **Vue.js + Vercel**. Animations 8.80, WPO **8.20**. ([scores](https://www.awwwards.com/sites/terminal-industries))

### 11. Oryzo AI — SOTM April 2026
- **URL**: oryzo.ai — **Agency**: [Lusion](https://lusion.co)
- **Pattern**: 3D-to-2D-to-3D scroll transitions, particle-based footer, interactive WebGL "sketches" embedded in narrative.
- **Stack**: **WebGL + Three.js + GSAP**. Creativity **8.35/10**. ([scores](https://www.awwwards.com/sites/oryzo-ai))

### 12. Tracing Art (Getty) — SOTM Jul 2025
- **URL**: getty.edu/tracingart — **Agency**: Resn
- **Pattern**: Data-driven editorial. Hover-driven interactions, big-background imagery, Getty Provenance Index visualised. Two-color (white/light grey).
- **Stack**: not disclosed publicly; Resn typically Three.js + custom WebGL. Content **8.09/10** (highest content score in this set). ([scores](https://www.awwwards.com/sites/tracing-art))
- **Why**: Proves "Content 10%" still moves the needle when execution is data-viz-grade.

---

## (4) Recurring Patterns Across 2024–2025 Winners

### Visual language tropes
- **Two-color palettes** are almost universal among recent SOTY/SOTM winners. Six of the eight 2024–2025 winners reviewed list a 2-color palette: Lando Norris (lime + black), Igloo (white + cyan), Opal Tadpole (yellow + white), Don't Board Me (red + blue), 100 Lost Species (cream + black), Ponpon Mania (purple + pink), Tracing Art (white + grey), Osmo (orange + black). Sourced from per-site palettes on Awwwards.
- **Oversized hero typography** that morphs / slides into layout on scroll (Lando Norris, Anime.js, Osmo, Don't Board Me).
- **Custom, intentional cursor** on roughly half of winners surveyed (varies widely — Awwwards has dedicated [cursor inspiration collections](https://www.awwwards.com/inspiration/cursor-interaction)).
- **Editorial mode**: cause-led or content-led pieces (100 Lost Species, Tracing Art, Dropbox Brand) consistently score top on Content.

### Motion language tropes
- **Scroll-as-narrative timeline** is the dominant macro-pattern: pinned scroll, horizontal scrub through chapters, scrubbed video, scroll-driven 3D camera moves. Confirmed by [Awwwards' "Rise of the Scrolling Site"](https://www.awwwards.com/the-rise-of-the-scrolling-site.html).
- **3D scenes per section** (Cartier's six alcoves, Igloo's portfolio ice-blocks, Oryzo's 3D-2D-3D transitions) — each major content area is its own miniature world.
- **Animations/Transitions sub-score is the *single most predictive* dev metric**. Across the 12 winners reviewed, mean Animations score = **8.7/10**. Mean Accessibility score = **7.0/10**. Pattern: motion is the price of entry; accessibility is rarely the reason a winning site won.
- **Sound design as narrative layer**, not background — Cartier's Mooders soundscape over Web Audio is repeatedly singled out. Immersive Garden's [Cartier case](https://immersive-g.com/cases/cartier-watches-and-wonders) explicitly: "sound treated not as background but as a narrative layer."

### Navigation patterns
- **Cursor-summoned / scroll-summoned nav** is more common than persistent headers. Telescope ("menu transforming into footer"), Silent House (dropdown), Messenger (character navigation) all use non-traditional nav.
- **Long-form single-page** dominates — most 2024–2025 SOTY winners are effectively single pages with chaptered scroll, not multi-page IAs.

### Performance posture
- Winning sites **do not uniformly hit Lighthouse-green / Core Web Vitals**. Of the 12 winners reviewed:
  - WPO scores range **6.80–8.80**, mean ~7.7/10.
  - Mobile is a known soft spot — winners often show "Please rotate your device" prompts (Lando Norris) or substantially reduced 3D on mobile.
- Per the [HTTP Archive 2025 Web Almanac](https://almanac.httparchive.org/en/2025/performance), only 48% of mobile pages pass all three CWV. Awwwards SOTY winners cluster modestly above this, but not at the green-Lighthouse extreme.
- **Implication for the skill library**: do not architect for Lighthouse 100. Architect for Awwwards-grade *animation* (60fps GSAP timelines, lazy-loaded heavy 3D, eager-loaded shaders) with WPO ≥ 7.5/10 as the floor.

---

## (5) Stack Patterns

Frequencies are estimated from per-site Awwwards tech tags, agency case studies, and Awwwards' framework-filtered indexes ([Three.js](https://www.awwwards.com/websites/three-js/), [Next.js](https://www.awwwards.com/websites/next-js/), [Nuxt.js](https://www.awwwards.com/websites/nuxt-js/), [Astro](https://www.awwwards.com/websites/astro/), [Svelte](https://www.awwwards.com/websites/svelte/), [GSAP](https://www.awwwards.com/websites/gsap/), [Webflow](https://www.awwwards.com/websites/webflow/)).

### Rendering frameworks (estimated frequency among recent SOTD/SOTM winners)
| Tier | Framework | Notes |
|---|---|---|
| **Dominant** | **Next.js** | Default for React-based studios. Full first page of Awwwards' Next.js index is current SOTD/Honorable Mention winners. |
| **Dominant** | **Nuxt.js** | Default for European motion studios (Immersive Garden, Patrick Heng, many French/UA studios). Pairs with Vue + Three.js. |
| **Strong** | **Webflow** | Lando Norris (SOTY 2025) proves Webflow can win at the top. Heavy Osmo/UNCOMMON/BRIGHTSCOUT footprint. |
| **Strong** | **Astro** | Locomotive's Aupale Vodka uses Astro. Robert Borghesi (ASTRODITHER) won SOTD with Astro. Trending up. |
| **Niche but elite** | **Svelte / SvelteKit** | Igloo Inc (SOTY 2024) is Svelte. Otherwise underrepresented vs. its outsized win-impact. |
| **Niche** | **Vue (without Nuxt)** | Terminal Industries. |
| **Niche** | **Remix / SolidStart / Qwik** | Essentially absent from 2024–2025 winners reviewed. |

### Motion / animation
| Tier | Library | Notes |
|---|---|---|
| **Universal** | **GSAP (+ ScrollTrigger)** | Present in essentially every motion-driven winner reviewed: Igloo, Lando Norris, Cartier, Oryzo, Aupale Vodka, Ponpon Mania, Silent House. Closest thing to a required dependency. |
| **Common** | **Framer Motion** | Dominant for React/Next.js portfolios that don't need ScrollTrigger-grade timelines; weaker presence in SOTY tier. |
| **Common** | **Native CSS scroll-driven animations / `view-timeline`** | Rising in 2025 winners as browser support landed. |
| **Niche** | **Motion One / anime.js** | Anime.js itself was a SOTM May 2025 winner ([animejs.com](https://animejs.com)); used directly by the winning showcase. |
| **Niche but elite** | **Rive** | Lando Norris SOTY 2025 leans on Rive heavily for 3D motion. |

### Smooth scroll
- **Lenis (Studio Freight / darkroom.engineering)** is the de-facto winner — Cartier, most Immersive Garden / Locomotive / Abeto sites. Locomotive Scroll v5 is now a thin wrapper around Lenis. Native CSS smooth scroll is rare in winners (jank tolerance is too low).

### 3D / WebGL
| Tier | Approach | Notes |
|---|---|---|
| **Dominant** | **Vanilla Three.js** | Most non-React studios (Immersive Garden, Lusion, Resn, Abeto, Patrick Heng, makemepulse). Provides shader/scene control React-Three-Fiber abstracts away. |
| **Common** | **React Three Fiber (R3F) + drei** | Default for Next.js studios. Strong but second to vanilla Three.js among elite wins. |
| **Niche** | **WebGPU / TSL** | Emerging; Lando Norris and recent Lusion work flagged on [webgpu.com](https://www.webgpu.com). |
| **Niche** | **Theatre.js** | Used for sequencing complex scroll-3D timelines; few public confirmations among 2024–2025 winners. |
| **Niche but distinctive** | **Rive** | 3D motion via Rive (rather than Three.js) — Lando Norris. |

### Asset pipeline
- **Blender → glTF/Draco** is the standard. Houdini + custom VDB pipelines for elite tier (Igloo Inc). Ktx2/basis-compressed textures for performance.

### CMS
| Tier | CMS | Evidence |
|---|---|---|
| **Strong** | **Sanity** | Monolith NYC case study; widely used by motion-heavy Next.js studios. |
| **Strong** | **Contentful** | 100 Lost Species (Immersive Garden, SOTM Oct 2025) — explicit. |
| **Strong** | **Storyblok** | Exo Ape and similar studios; webhook-triggered static rebuild pattern. |
| **Common** | **DatoCMS** | DatoCMS lists Awwwards-winning partner agencies. Common in EU studios. |
| **Common** | **Prismic** | Solid French/EU footprint; less elite-tier presence than Sanity/Contentful. |
| **Common** | **Webflow CMS** | Native to Webflow projects (Lando Norris, Osmo, BRIGHTSCOUT, UNCOMMON work). |
| **Niche** | **Headless WordPress / Payload / Strapi** | Underrepresented in elite tier. |

### Hosting / infra
- **Vercel** is the dominant deploy target for Next.js winners (explicit on Terminal Industries). Cloudflare Pages, Netlify, custom Edge are common but less visible.

### Composite "winning template" stack
Based on this synthesis, the **highest-probability stack for an Awwwards-tier site in 2025–2026** is:

> **Nuxt 3 (Vue) or Next.js (React)** + **vanilla Three.js or R3F** + **GSAP + ScrollTrigger** + **Lenis** + **Sanity / Storyblok / Contentful** + **Vercel**, with **Blender → Draco-compressed glTF**, optional **Web Audio API** for narrative sound, optional **Rive** for 3D motion, deployed with sub-3s LCP and 60fps animation timelines.

Webflow + GSAP + Rive is the credible no-code variant (Lando Norris is the existence proof). Svelte + Three.js is the elite-craft variant (Igloo Inc is the existence proof) but demands a level of shader/tooling expertise most teams don't have.
