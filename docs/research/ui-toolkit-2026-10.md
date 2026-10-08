# factor: UI toolkit research (D-036)

Researched 2026-10-08 by Sage for D-036 in `../decisions.md` (brain task #3930). The constraints come from
D-001, D-024, D-031, D-032 and D-034, from `../design/ui-brief.md`, and from Peter's words quoted in D-036
and in §1. **This brief does not decide.** It screens the field, ranks a shortlist for factor's context,
and defines the spike that would let Peter rule.

**Labels.** Every claim carries one of three.
- **[observed]**: I read it in a primary source (repo file, crate manifest, crates.io API, licence text,
  issue thread) or produced it with a command I ran.
- **[reported]**: someone else says it: a vendor README, a press release, third-party guidance. Where the
  speaker has an interest, it is named.
- **[inferred]**: my own reasoning, untested.

**What this research ranged over.** These are the limits of the conclusions below.
- crates.io API metadata and the last 10 release dates for 30 crates, read 2026-10-08.
- `gh api` repo metadata for 21 repositories, plus targeted manifest, source and issue reads, all cited inline.
- Resolve-only `cargo` (`add`, `metadata`, `tree`) in five scratch projects, on `aarch64-apple-darwin`
  and `x86_64-pc-windows-msvc`. Nothing was compiled.
- The Blitz CSS status page, the Dioxus docsite source, and two web searches (Unreal licence terms, Zed funding).
- **Nothing was rendered, and no performance was measured.** Every performance statement below is
  [reported] or [inferred]. The spike in §9 is the instrument.
- No Context7 tool was exposed this session, so library docs were read from their repositories directly.

---

## 0. Headline

1. **No toolkit ships a diagram component known to hold 500+ rich nodes.** In every native option, factor's
   diagram is a canvas factor builds itself: custom painting, culling, hit-testing, edge-following keyboard
   focus, and accessibility nodes. Its labelled edges attach to a node as a whole (`ui-brief.md` §6), while
   the node-graph crates are built for pin-and-wire editors. So the toolkit question splits three ways:
   - what the canvas can draw, and how far it can drop to the GPU when the built-in painter runs out;
   - how much of the *rest* of the UI comes ready-made: tables, text input, menus, drawers;
   - text and accessibility.
   [inferred, from §3]
2. **Five candidates pass all four hard screens:** Windows, a Rust core, upstream screen-reader support,
   and active maintenance with a named funder. Two are cut on second-order grounds, which leaves three:
   **egui**, **GPUI (with gpui-kit)** and **Slint**.
   - **Dioxus Native** is cut on maturity and on specific gaps (§6).
   - **Bevy UI** is cut for having no table widget and a different programming model (§5).
   - **Iced** is the near miss on the screens themselves: it has no screen-reader support upstream (§2).
   [observed, §2]
3. **Ranked shortlist, each failing in a different way:**
   - **egui**'s risk is in its text engine: no bidirectional text, and right-to-left editing regressed in 0.35.
   - **GPUI + gpui-kit**'s risk is process and provenance: no versioned API, delivered through a weekly
     third-party snapshot.
   - **Slint**'s risk is a licence choice that is coupled to D-025.
   §7 gives the fit reasoning.
4. **The Dioxus note in D-036 is stale on the label and right on the substance.**
   - Blitz now calls itself **beta**, while Dioxus's own 0.7 docs still say "experimental".
   - The stable `dioxus-native` 0.7.10 still ships the older Blitz 0.2 line, and Dioxus 0.8 is alpha.
   - The note also missed three things: an MPL-2.0 CSS engine bundled in, no `unicode-bidi`, and SVG
     `fill`/`stroke` that can't be styled. [observed, §6]
5. **"Overkill" holds for UE5, holds as a build-cost argument for raw wgpu or OpenGL, and is the wrong
   reason for Bevy.**
   - Bevy is not too heavy. Its widget layer is the youngest of the set: no table widget, and three
     breaking releases so far in 2026. Bevy 0.20 was released today.
   - A custom wgpu pass *inside* a toolkit is the realistic middle path, and egui and Slint expose one (§5).
6. **What carries over from the HTML/CSS mockups:**
   - Design tokens (colour, spacing, type) become a theme struct in any toolkit, cheaply.
   - Layout and structure carry over directly only to a webview or Blitz.
   - Among native toolkits, GPUI comes closest: Tailwind-style builder methods over Taffy's flexbox and grid.
   [observed for GPUI's API, inferred for the cost]

---

## 1. What this ranks against

**Peter, verbatim (D-036 and the dispatch):**
- "i was considering dioxus, i'd prefer close to native vs web format but that will cause some concerns :-)"
- "i'd prefer for the local version to be naitive drawn, libraries will be the key or we need to roll some up. we could also maybe use something like opengl or bevy or UE5 but they seem overkill."

So the preference is a native-drawn local build, and the deciding axis is **library coverage**. Building
missing pieces is acceptable, at a cost.

**Bound by rulings:**
- **D-001:** macOS now, Windows later. Nothing may rule Windows out. **Windows is a hard screen.**
- **D-032:** the drawing is a replaceable view, and a web view is possible later. Puck's derivation in D-032
  is that the boundary is a serialisable data interface. On that reading, a web target in the *desktop*
  toolkit is a bonus, not a requirement: a later web view can be a separate front end over the same
  interface. [inferred]
- **D-024:** one view; edits on the diagram re-solve.
- **D-031:** globalisation shaped in: text shaping, longer strings, numbers formatted in the view.
- **D-034:** a dense tool UI with no walkthroughs.

**Implied by `ui-brief.md`, and used as assessment axes:**
- §3 window shell: the menu bar and file dialogs are **native, not drawn**.
- §4.11 and §4.12: legible at hundreds of nodes, with compact chips when zoomed out; arrow keys move between
  nodes along edges.
- §4.13: an accessibility floor. Contrast; status never by colour alone; visible focus; nothing in hover only.
- §4.14: tabular, equal-width figures, right-aligned.
- §4.10: light and dark following the system, from one set of tokens.

**Added here [inferred]:**
- **Idle cost.** factor runs beside Satisfactory (`ui-brief.md` §1). A toolkit that redraws continuously
  takes GPU time from the game, so the redraw model is recorded below and idle CPU is a spike measure.

---

## 2. Screening: every candidate on four hard facts

The four screens:
- **Windows**, per D-001.
- **A Rust core.** A Rust-first API, not bindings to C++.
- **Screen-reader support upstream.** Values: accessibility is a committed floor on any surface another
  human uses. D-030 makes the first build Peter's alone, but the tool is intended for others.
- **Maintained, with a named funder.**

Release dates are from crates.io, stars and last push from `gh api`, all read 2026-10-08 [observed unless
marked].

| Candidate | What draws the pixels | Windows | Rust core | Screen reader upstream | Latest release · activity | Funder | Crate licence | Screen |
|---|---|---|---|---|---|---|---|---|
| **egui** + eframe | wgpu (default in 0.36.2), or glow/OpenGL; text rasterised with skrifa + vello_cpu | yes | yes | **yes**, AccessKit on by default in eframe 0.36.2 | 0.36.2, 2026-09-08. Minors 0.34→0.35→0.36 at 2026-03-26, 06-25, 08-05. 31,041★ | **Rerun** ("egui development is sponsored by Rerun", egui README) | MIT OR Apache-2.0 | **pass** |
| **GPUI** (Zed) + **gpui-kit** (Longbridge) | Metal on macOS (gpui README); on Windows, Win32 windowing and DirectWrite text (README). The Windows GPU backend was not checked | yes | yes | **yes, since 2026-05-27** (zed #56065, AccessKit). Only through git or snapshots, see below | gpui 0.2.2 on crates.io is from 2025-10-22. 172 commits on `crates/gpui` since 2026-07-08. gpui-kit 0.7.1, 2026-10-05 | **Zed Industries** (Series B $32M led by Sequoia, Aug 2025 [reported, press]); **Longbridge** for gpui-kit | gpui Apache-2.0 (`crates/gpui/Cargo.toml`, `LICENSE-APACHE`); gpui-kit Apache-2.0 | **pass**, with a provenance caveat (§7.2) |
| **Slint** | FemtoVG on OpenGL (default) or software. Skia optional; wgpu behind `unstable-wgpu-29/30` | yes | yes. Rust core, but the UI is written in the `.slint` DSL | **yes**, `accessibility` is a default feature of the `slint` crate | 1.18.1, 2026-09-21. A minor every 2–4 months. 24,115★ | **SixtyFPS GmbH**, which sells commercial licences | **GPL-3.0-only OR Slint Royalty-free 2.0 OR Slint Software 3.0** | **pass**, with a licence decision (§7.3) |
| Iced | wgpu, tiny-skia fallback; text via cosmic-text | yes | yes | **no.** Draft PR #3111 is open; PR #3281 was closed unmerged on 2026-03-14 with the maintainer's "I'll work on this myself" | 0.14.0, 2025-12-07; previous 0.13.0, 2024-09-18. 100+ commits since 2026-07-08 | Kraken / Cryptowatch (iced README "Sponsors") | MIT | **fail: screen reader** (near miss) |
| Dioxus desktop | **system webview** (Wry) | yes | Rust logic, HTML/CSS view | yes, the browser accessibility tree [inferred] | 0.7.10, 2026-07-30 | FutureWei, Satellite.im, GitHub Accelerator (dioxus README) | MIT OR Apache-2.0 | **not native-drawn.** Baseline only |
| Dioxus Native (Blitz) | Vello on wgpu, through anyrender. CSS via Stylo, layout via Taffy, text via Parley | yes (Blitz README downloads list) | yes | yes, AccessKit in `blitz-shell` | stable `dioxus-native` 0.7.10 pulls `blitz-dom` **0.2.4** (cargo tree). Blitz 0.3.0-beta.2 is from 2026-08-24; Dioxus 0.8.0-alpha.1 from 2026-07-31 | as Dioxus | MIT OR Apache-2.0, **bundling MPL-2.0 Stylo** | passes the screens, fails on maturity (§6) |
| Xilem / Masonry | Vello on wgpu; Parley text | yes [inferred: winit] | yes | yes, AccessKit (README) | 0.3.0, 2025-05-10; 0.4.0, 2025-10-29; none since | Linebender (funding not checked) | Apache-2.0 | **fail: maturity.** README: "An experimental Rust architecture for reactive UI" |
| Makepad | its own shader DSL on GPU | yes [reported, README] | yes | **no.** Issue #196 "On Accessibility" open since 2023-08-08; no `accesskit` in any manifest (code search; control: egui returned 8) | makepad-widgets 1.0.0, 2025-05-13. Repo pushed 2026-10-08 on `dev` | not checked | MIT OR Apache-2.0 | **fail: screen reader** |
| Floem (Lapce) | wgpu via vger or Vello, Skia via anyrender, tiny-skia fallback (README) | yes | yes | **no.** Issue #8 open since 2023-04-14; no `accesskit` in any manifest | 0.2.0, 2024-11-14. Repo pushed 2026-09-24 | not checked | MIT | **fail: screen reader** |
| Freya | Skia (`skia-safe`) | yes (README notes `windows-gnu` issues) | yes | yes, AccessKit in its manifests | 0.5.0-rc.9, 2026-10-04 | one maintainer plus GitHub Sponsors | MIT | **fail: funder.** A single sponsored maintainer |
| vizia | Skia | yes | yes | yes, AccessKit (README) | 0.4.0, 2026-04-23; 0.3.0, 2025-04-16 | not named | MIT | **fail: funder.** It earns a mention in §4 for its CSS-like stylesheets |
| Bevy UI (0.20) | wgpu | yes | yes | yes. `bevy_a11y`, `accesskit_winit` 0.34 in `bevy_winit` | **0.20.0, released 2026-10-08 (today)**; 0.19.0, 2026-06-19; 0.18.0, 2026-01-13 | Bevy Foundation (not checked) | MIT OR Apache-2.0 | passes the screens; examined in §5 |
| raw wgpu / OpenGL + hand-rolled UI | whatever you build | yes | yes | only what you build, through an AccessKit adapter | wgpu 30.0.1, 2026-08-22 | gfx-rs (not checked) | MIT OR Apache-2.0 | examined in §5 |
| Unreal Engine 5 | Unreal renderer, Slate UI | yes | **no.** C++ engine | Slate has accessibility support [inferred, not checked] | — | Epic | **royalty or seat licence** [reported, §5] | **fail: not Rust** |
| Tauri + Svelte | system webview (WKWebView, WebView2) | yes | Rust backend, TypeScript view | yes, the browser accessibility tree [inferred] | 2.12.1, 2026-09-30; 3.0.0-alpha.4 | CrabNebula / Tauri org (not checked) | Apache-2.0 OR MIT | **not native-drawn.** Baseline only |

**Not examined:** Qt through cxx-qt, GTK through gtk4-rs, and other smaller crates. See §11.

---

## 3. The diagram: what each toolkit gives a 500-node canvas

**Framing [inferred].** At 500 nodes and about 750 labelled edges, with LOD chips and pan and zoom, no
toolkit's retained widget tree is the obvious answer. The diagram is either:
- (a) one custom-painted canvas element doing its own culling and hit-testing, or
- (b) hundreds of lightweight positioned elements, if the toolkit's per-element cost is low enough.

The questions that discriminate:

| | egui | GPUI | Slint | Dioxus Native | Iced (near miss) |
|---|---|---|---|---|---|
| **Canvas primitive** | `Painter` shapes and paths [inferred: the long-standing egui API, not re-read this session]; `egui::Scene` for pan and zoom (added in #5505) [observed, CHANGELOG] | `paint_quad`, `paint_path`, `paint_svg`, `paint_glyph`, `insert_hitbox` on `Window` [observed, `crates/gpui/src/window.rs`]. A `canvas()` element exposes them [inferred from the API shape] | `Path` elements plus `for` repeaters of components placed at absolute x/y [inferred from the language model; not read in source] | absolutely positioned elements plus inline SVG; 2D transforms supported [observed, Blitz status page] | `canvas` widget with `Cache` [observed, CHANGELOG] |
| **Shaped text inside the canvas** | yes, the same galley layout as widgets [inferred] | yes, `paint_glyph` with the platform shaper [inferred] | yes, components carry `Text` [inferred] | yes, it is HTML text [inferred] | yes, cosmic-text [inferred] |
| **Custom GPU escape hatch** | **yes**: `egui_wgpu::Callback` / `CallbackTrait` [observed, `crates/egui-wgpu/src/renderer.rs`] | **no public custom-shader API found.** `paint_surface` takes a macOS `CVPixelBuffer` only [observed, `window.rs`]. So beyond its primitives you cannot inject a pipeline [inferred] | **yes, behind unstable features**: `unstable-wgpu-29/30` modules in `api/rs/slint/lib.rs` [observed] | `wgpu_texture` example in the Blitz repo [observed, README] | **yes**: the `shader` widget and `shader::Pipeline` trait [observed, CHANGELOG] |
| **Accessibility for custom-drawn nodes** | yes in principle: `ui.interact` plus `Response::widget_info`, and the role is now `accesskit::Role` (0.37 unreleased, #8555) [observed API; untested for this use] | element-based: a `div` with `.id()` plus `.role()` becomes a node [observed, `_accessibility.rs`]. So nodes must be elements, not raw paint calls, to be announced [inferred] | per component, automatically [inferred] | per element, through Blitz's AccessKit tree [inferred] | none (§2) |
| **Node-graph crates** | egui-snarl 0.12.0 (2026-08-26, pin-and-wire), egui_graphs 0.32.0 (2026-08-31, petgraph-backed). egui_node_graph is unmaintained (0.0.0, 2022) | none found | `slint-node-editor` 1.0.1: 46 recent downloads, so effectively unproven | none found | none on crates.io (a search for "iced node" returned none) |
| **Redraw model** | repaints on input or animation only; "if your app is idle, no CPU is wasted" [reported, egui README] | hybrid immediate and retained (README); idle behaviour not checked | event-driven [inferred] | event-driven [inferred] | "Reactive rendering" (#2662) [observed, 0.14 CHANGELOG] |
| **Published scale evidence** | "1-2 ms per frame" for typical UIs [reported, author's README]. **No graph-scale number found** (searched the egui-snarl and egui_graphs issues) | "120 FPS", tables over "hundreds of thousands of rows" [reported, vendor: Longbridge's gpui-kit README]. Zed itself is the production proof, but for editor text, not graphs [inferred] | no entry found | no entry found | no entry found |

**Toolkit-neutral pieces that have to be built or chosen anyway:**
- **Auto-layout.** Sugiyama-style layered layout: `rust-sugiyama` 0.4.0 and `dagre` 0.1.1 exist on
  crates.io, unexamined.
- **Edge routing and label placement**, LOD switching, and edge-following keyboard navigation.

This is the same work in every option, so it does not discriminate between them. Its cost is real, and it
sits outside the spike (§9 precomputes positions). [inferred]

**Webview baseline for comparison.** For React Flow, one third-party guide suggests visible-only rendering
at 100–500 nodes, simplified nodes at 500–1,000, and WebGL alternatives beyond that [reported,
third-party skill guides found by web search; **not from xyflow's maintainers**]. No official xyflow or
Svelte Flow benchmark was found.

---

## 4. Full assessment of the survivors

The shortlist plus the two named alternates. Cells are [observed] unless marked.

| Axis | egui | GPUI + gpui-kit | Slint | Dioxus Native | Iced |
|---|---|---|---|---|---|
| **1. Pixels** | wgpu → Metal or DX12 [inferred mapping]; CPU glyph rasterising (skrifa + vello_cpu, 0.34 CHANGELOG) | Metal (macOS); DirectWrite text on Windows | FemtoVG on OpenGL by default. ⚠ OpenGL is deprecated on macOS [inferred; general knowledge, not checked]. FemtoVG-on-wgpu needs `unstable-wgpu-30` | Vello on wgpu | wgpu, or tiny-skia |
| **2. Library coverage: tables** | `egui_table` 0.10.0, virtualised (Rerun); `egui_extras` TableBuilder | gpui-kit "Data Tables: Virtual scrolling, fixed and resizable columns, sorting" [reported, vendor] | `StandardTableView` (std-widgets) [inferred; not read] | HTML `<table>` is emulated through CSS grid ("Partial", status page). No virtualisation found | `table` widget, new in 0.14 (#3018). Virtualisation not checked |
| **2. Text input and IME** | `TextEdit`; IME reworked in 0.35 (#8083, #7983) | gpui-kit has a code editor and inputs [reported, vendor]; Zed's own IME is in production [inferred] | std-widgets `LineEdit`; IME not checked | form controls (README goal); IME not checked | "Input method support" (#2777) |
| **2. Menus and drawers** | panels and popups built in. **No native menu bar**: eframe has no `muda` dependency, so it means adding muda [observed absence in eframe's `Cargo.toml`; remedy inferred] | `set_menus` in `crates/gpui/src/app.rs` (native app menus); gpui-kit has dock, overlays and menus [reported, vendor] | native menus through muda (`internal/backends/winit/muda.rs`, which uses `i_slint_core::menus`). The `.slint` element name was not checked | `muda` in blitz-shell (README) | not checked |
| **2. Theming, tokens, light/dark** | `Style` / `Visuals` structs; class-based `StyleProvider` behind an `experimental` flag (0.37, unreleased) | gpui-kit "semantic themes", `.theme-schema.json` at the repo root [observed file; semantics reported] | `global` singletons carry tokens [inferred, from the language] | CSS custom properties: **not listed** on the status page. `color-scheme` is "Not supported" | `Theme` / palette [inferred] |
| **2. What factor would build** | the diagram canvas (§3); a native menu bar through muda; a token-to-`Visuals` mapping | the diagram (nodes as `div`s with id and role, or painted plus hitboxes); token mapping onto gpui-kit themes | the diagram as repeated components plus `Path` edges, or a wgpu texture through the unstable API; token globals | the diagram as positioned elements plus SVG edges, working around SVG styling; virtualised tables | the diagram on `canvas`; **the screen-reader layer** |
| **3. Diagram evidence** | none at scale (§3) | vendor claims only | none | none | none |
| **4. Screen reader** | AccessKit, default-on; still being extended (0.37: menus, popups, invisible widgets hidden) | AccessKit since 2026-05-27 (zed #56065); `Application::inaccessible()` opt-out (#57954) | AccessKit, default feature | AccessKit (blitz-shell) | none |
| **4. Text: shaping** | **yes since 0.35.0, via harfrust** (CHANGELOG #8031 "Use `harfrust` for better kerning and ligatures"; `harfrust` in `crates/epaint/Cargo.toml`) | platform shapers (CoreText through `font-kit`, DirectWrite) [inferred from README backends] | **Parley** by default (`shared-parley` in `internal/core/Cargo.toml`) | Parley | cosmic-text (`text::Shaping`) |
| **4. Text: bidi / RTL** | **no.** #1016 "Bidirectional text support", open since 2021-12-29. **RTL caret editing regressed in 0.35** (#8576, 2026-09-17, measured by its reporter) | **open.** zed #31102 "RTL Right-to-Left Text Input/Rendering Support" (2025-05-21); bidi shaping crash fixed in `gpui_wgpu` (PR #61651, 2026-07-26) | via Parley [inferred: Parley does bidi] | `unicode-bidi` "Not supported"; `direction` partial (status page) | via cosmic-text [inferred] |
| **4. Text: font fallback** | manual font lists today. System fonts through `fontique` arrive in **0.37, unreleased** | platform [inferred] | `fontique` [observed dependency] | `@font-face` supported | cosmic-text system fonts [inferred] |
| **5. macOS / Windows** | both | both. **Full Xcode required for Metal** (gpui README); gpui-kit enables `runtime_shaders` [observed], which may avoid that requirement [inferred] | both | both | both |
| **5. Web target** | yes (eframe web) | wasm32 section in `crates/gpui/Cargo.toml` [observed]; gpui-kit "WebAssembly" [reported, vendor] | yes, WebAssembly demos in its README | the web is Dioxus's main renderer anyway | yes (WebGPU and WebGL fixes in 0.14) |
| **6. Maturity and churn** | 0.x. Each minor carries breaking changes (0.37's list is in its CHANGELOG). A minor every 1.5–3 months | **pre-1.0**: "There will often be breaking changes between versions" (gpui README). No crates.io release since 2025-10-22, so consumers pin a Zed git rev or `gpui-pre` | **1.x**, with explicit `compat-1-N` feature gates for stability | Dioxus 0.6 → 0.7 → 0.8 alpha; Blitz beta | about one release a year |
| **6. Production apps** | Rerun Viewer (egui README) | Zed (GPUI); Longbridge Pro (gpui-kit) [reported, vendor] | not checked | not checked | COSMIC desktop uses a fork, libcosmic [inferred, not checked] |
| **7. Licence (whole graph)** | clean. No non-permissive package in the resolve on either target (`cargo metadata`) | crates Apache-2.0. MPL-2.0 in the graph: `option-ext` (runtime, through `dirs`) and `cbindgen` (build-only, through `gpui-pre-apple`). `libbz2-rs-sys` is under the permissive bzip2 licence | **the toolkit itself**: GPL-3.0 / royalty-free with attribution / commercial (§7.3) | **15 MPL-2.0 packages** (`stylo*`, `selectors`, `cssparser`, `app_units`, …), confirmed in `cargo tree` | clean |
| **7. Dependency weight** (unique packages in `cargo tree`, normal plus build edges, root included; macOS / Windows) | 178 / 182, *with* `egui_table` and `egui-snarl` | 457 / 434, gpui-kit **default features** | 249 / 248, defaults | 397 / 401, defaults | 153 / 160, bare `iced` |
| **8. Carry-over from HTML/CSS mockups** | tokens by hand into `Visuals`; layout rewritten imperatively | **closest native**: `.flex()`, `.flex_col()`, `.grid()`, `.gap_*`, `.px_*` over Taffy (`crates/gpui/src/styled.rs`, `taffy` in its manifest). Tailwind classes translate almost one for one [inferred] | tokens become `global`s; layout rewritten in `.slint` | **highest**: it *is* HTML/CSS, within the status-page gaps | tokens by hand; layout rewritten |
| **9. Rust fit** | pure Rust, immediate mode | pure Rust, its own entity/context model | Rust core; UI in a compiled DSL | Rust plus RSX (React-like) | pure Rust, Elm architecture |

**vizia note.** Its README advertises "stylesheets with hot-reloading" in a CSS-like form, which is the
best structural carry-over among the native toolkits. It failed the funder screen (§2), and its community
is the smallest of the set (2,325★).

**Licence census, its range and a caveat.**
- **Tool:** `cargo metadata --filter-platform <target>` in scratch projects, scanned for any package whose
  licence expression offers no permissive alternative.
- **Positive controls:** it flagged Slint's core and Dioxus Native's Stylo stack, and passed egui and Iced
  clean, so it fires in both directions.
- **Over-inclusion:** `cargo metadata` includes optional packages. It listed `skia-bindings` under Slint,
  where `cargo tree -i skia-bindings` found nothing. Every flag above was re-confirmed with `cargo tree`.
- **Build-time downloaders:** checked against a fixed name list only (`skia-bindings`, `skia-safe` and a
  few others), not derived from the graph.
- **No `deny.toml`:** the repo has none (it has no Cargo workspace yet), so `cargo deny` was not run
  against a repo policy.

---

## 5. Is the "overkill" claim right? Engines and raw GPU APIs

| Option | Verdict on "overkill" | Why |
|---|---|---|
| **Unreal Engine 5** | **Overkill, confirmed, and it fails the Rust-core screen besides** | A C++ engine whose UI layer (Slate) is C++. factor's Rust backend would sit behind FFI. Terms [reported; Epic's licence page returned 403 to my fetch, so this comes from a search summary of Epic's pages]: **5% royalty on lifetime gross revenue above $1M** for a product that relies on engine code at runtime and is distributed to end users; a seat subscription (**$1,850 per user per year** was quoted) for companies over $1M annual revenue. A royalty on factor's possible commercial use is a standing cost no other option carries. |
| **Bevy (0.20, today)** | **The wrong reason.** It is not too heavy; its widget layer is the youngest | For: wgpu, AccessKit (`bevy_a11y`), Parley text (`bevy_text`), a widget set (`bevy_ui_widgets`: button, menu, tabs, text_input, tree, list, scrollarea, …), and `bevy_feathers`, which is *designed for editor and inspector tooling* (its crate doc) [all observed]. Against: no table or virtualised grid in either crate's file list [observed]; three breaking releases so far in 2026 (0.18.0 on 01-13, 0.19.0 on 06-19, 0.20.0 on 10-08) [observed]; an ECS-driven UI is a different programming model for every panel [inferred]. Idle: a game loop by default; a reactive desktop mode exists [inferred, not checked this session]. For drawing very large diagrams it is plausibly the strongest option (instanced meshes) [inferred, untested]. |
| **Raw wgpu, plus parley, AccessKit and winit** | **Overkill as build cost; right as a rendering layer** | You would build a toolkit: layout, focus, IME plumbing, an AccessKit tree, every widget, menus and tables [inferred]. But the *diagram* can be a raw wgpu pass hosted inside a toolkit: egui through `egui_wgpu::Callback`, Iced through `shader::Pipeline`, Slint through `unstable-wgpu-30` (§3). That keeps the fast path open if the painter runs out. **GPUI has no such hatch** (§3). |
| **OpenGL** | **Overkill, and it points the wrong way** | Deprecated on macOS [general knowledge, not checked this session]. wgpu covers Metal and DirectX with one API. Nothing found argues for OpenGL over wgpu here [inferred]. |

---

## 6. Dioxus: what the D-036 note got right and wrong

| Note's claim (D-036, read via Context7 2026-10-08) | Status 2026-10-08 | Evidence |
|---|---|---|
| Desktop renderer is a system webview (Wry) | **Still true** | docsite `docs-src/0.7/src/beyond/project_structure.md`: "the UI is rendered using a system webview" [observed] |
| Blitz is "experimental" | **Stale on the label.** Dioxus's own 0.7 docs still say "(experimental)" [observed, same file]. The Blitz README now says: "Blitz is currently in a **beta** state … usable for making apps if you are an early adopter and willing to live on the bleeding edge. But there are also still many bugs and missing features" [observed] | Blitz README; `blitz-dom` 0.3.0-beta.2, 2026-08-24 |
| "close to native" means betting on Blitz maturing | **True, and stronger than stated** | Stable `dioxus-native` 0.7.10 depends on **`blitz-dom` 0.2.4**, the old line [observed, `cargo tree`]. The beta 0.3 line arrives with Dioxus **0.8.0-alpha.1** (2026-07-31) or a Blitz git rev (Blitz README). The alpha release notes promise "a huge quality upgrade to dioxus-native" [observed]. |
| API changed between 0.6 and 0.7 | **True, and a third cycle is under way** | 0.8.0-alpha.0 (2026-05-19), alpha.1 (2026-07-31) [observed] |
| **Not in the note:** licence | MPL-2.0 Stylo stack bundled | 15 MPL-2.0 packages in `cargo tree` [observed]. MPL is file-level copyleft, so modified MPL files must be published; plain use is permissive [general licence knowledge] |
| **Not in the note:** CSS gaps that bear on factor | SVG `fill`/`stroke` "Not supported" ("styling SVGs is not yet supported"); `unicode-bidi` "Not supported"; `direction` partial; `text-overflow` "In Progress"; `color-scheme` "Not supported"; tables emulated through grid | blitz.is/status/css [observed; the page carries no date] |

**Why it is not shortlisted [inferred].** It is the only native path where Claude Design's HTML/CSS carries
over structurally, which is what made it Peter's first thought. But the diagram would lean on exactly the
gaps listed: SVG edges that can't be styled, no bidi, no ellipsis. And Peter's deciding axis, library
coverage, is thin for native: its component ecosystem targets the webview. Re-entry condition, for
whoever rules: a non-beta Blitz shipped in a stable Dioxus release. **Nothing watches for that, so it is
parked, not deferred;** re-checking it is a human step at the next D-036 review.

---

## 7. Ranked shortlist

Ranked for factor: a native-drawn local build, library coverage as the deciding axis, Windows required,
D-031 text, the accessibility floor, and possible open-source or commercial release.

**Why egui ranks above the broader library [inferred].** On Peter's axis, library coverage, GPUI with
gpui-kit claims the most. But that coverage is a vendor claim, delivered through an unofficial snapshot.
egui's coverage is observed in released crates. If the spike confirms gpui-kit's claims and the snapshot
risk is accepted, ranks 1 and 2 can swap.

### 7.1 egui (eframe 0.36.2, egui_table) — rank 1

- **Fit.**
  - Pure Rust with the cleanest licence graph and the smallest build of the three.
  - AccessKit is on by default and being actively extended.
  - A virtualised table maintained by its sponsor (Rerun).
  - Repaints only on interaction, which matters beside a running game.
  - A wgpu escape hatch for the diagram if the painter runs out.
  - A production tool of the same genre (Rerun Viewer: dense panels, big canvases).
  - Immediate mode suits a view that redraws from solver results. [inferred]
- **What factor builds:** the diagram canvas, a native menu bar through muda, and token-to-`Visuals`
  mapping.
- **Biggest risk: the upstream text engine, which factor cannot cheaply build around.**
  - There is no bidirectional text (#1016, open since 2021).
  - Right-to-left caret editing regressed in 0.35 (#8576).
  - System font fallback is unreleased (0.37).
  - So D-031 is met for left-to-right scripts (shaping via harfrust) and **not** for Arabic or Hebrew
    until upstream lands bidi. The draft Parley PR #5784 was last updated 2026-03-03.
  - Whether RTL locales are in D-031's scope is a decision (§8).
- **Second risk:** each 0.x minor breaks the API. That is a known, recurring migration cost every 1.5–3
  months. [observed cadence]

### 7.2 GPUI (via gpui-kit 0.7.1) — rank 2

- **Fit.**
  - The broadest ready-made library of the set, if gpui-kit's claims hold: virtualised tables, dock
    layout, menus, overlays, inputs and themes [reported, vendor: Longbridge].
  - Native app menus [observed, `set_menus`].
  - The closest native match to the HTML/CSS mockups (Tailwind-style builder over Taffy) [observed].
  - Proven at Zed's scale and frame rates in production [inferred from Zed].
  - Peter uses Zed daily.
- **What factor builds:** the diagram, as positioned elements with id and role (so nodes are announced)
  or as painted primitives plus hitboxes.
- **Biggest risk: process and provenance.**
  - GPUI has no versioned release for outside consumers (crates.io 0.2.2 dates from 2025-10-22, and the
    README warns of frequent breaks).
  - gpui-kit pins `gpui-pre =0.3.8`, a **weekly snapshot of Zed's crates republished by gpui-kit's own
    author** (crates.io owner `huacnlee`; description "gpui-pre snapshot of zed@279fe07") [observed].
  - The alternative is a git dependency on the Zed monorepo.
  - AccessKit support is five months old and has never been in a Zed-published crate.
  - **Security lens:** a third party sits in the supply chain between Zed's source and factor's build.
    Pinning `=` versions with a lockfile limits drift, but every update trusts that republication.
    [inferred]
- **Second risk:**
  - No public custom-GPU path on macOS, so the diagram has to stay within GPUI's primitives.
  - RTL is open upstream (zed #31102).
  - It carries the heaviest dependency graph (457 packages).
  - It needs full Xcode on macOS unless `runtime_shaders` avoids it.

### 7.3 Slint 1.18.1 — rank 3

- **Fit.**
  - The only 1.x API with explicit compatibility gates.
  - The best text stack of the three (Parley).
  - AccessKit by default.
  - Native menus through muda.
  - A company behind it.
  - A wgpu interop path.
- **What factor builds:** the diagram, as repeated components plus `Path` edges, with no evidence on how
  that scales to 500 nodes; or as a wgpu texture through the unstable feature.
- **Biggest risk: a licence decision coupled to D-025.** It is not a defect; it has to be *chosen*. The
  terms are quoted from `LICENSES/LicenseRef-Slint-Royalty-free-2.0.md` [observed]:
  - **GPL-3.0** costs nothing extra only if factor itself is GPL-3-compatible, which D-025 has not ruled.
  - **Royalty-free 2.0** requires either an `AboutSlint` widget "in an 'About' screen or dialog that is
    accessible from the top level menu", or "the Slint attribution badge on a public webpage". It
    forbids use "within Embedded Systems". And it forbids "distribution of Application that exposes the
    APIs, in part or in total, of the Software". That last clause matters if factor ever grows a plugin or
    scripting surface [inferred].
  - **Commercial** licence: paid. Pricing not checked.
- **Second risk:**
  - The UI lives in a separate DSL, which no current agent writes (D-036 "Agent coverage").
  - The default renderer is OpenGL on macOS.

**Not shortlisted, with the reason each lost:**
- **Iced:** no screen reader upstream, and about one release a year.
- **Dioxus Native:** beta, gaps on factor's exact needs, MPL (§6).
- **Freya, vizia:** a single maintainer or no named funder.
- **Makepad, Floem:** no screen reader.
- **Xilem:** self-described experimental.
- **Bevy:** no table, and a different programming model (§5).
- **UE5:** not Rust, and royalty terms.
- **Tauri:** not native-drawn. Kept as the spike's optional control.

---

## 8. Decisions this hands back

None is decided here. Each carries a recommendation.

1. **D-036 itself.** *Recommendation:* rule after the spike. Do not rule on this brief alone, because the
   discriminating quantity (frame time at 500 nodes) is unmeasured for every option.
2. **Are RTL scripts (Arabic, Hebrew) inside D-031's scope?**
   - If yes, egui's bidi gap becomes a blocker until upstream fixes it, and Slint's Parley stack gains weight.
   - If D-031 means only "no structural barrier to later localisation", egui's gap is a tracked risk.
   - *Recommendation:* Peter states it. The spike measures it either way (§9, P7).
3. **Slint's licence route, if Slint survives the spike.** This is coupled to D-025.
   - *Recommendation:* do not let the toolkit choice pre-empt D-025. If Slint leads, rule D-025 first,
     or choose royalty-free with the About-dialog attribution and record the API-exposure clause as a
     constraint on any future plugin system.
4. **Spike thresholds (§9).** They are proposals, and the lead or Peter sets them.
5. **Who builds the spike.**
   - D-036 records that no current implementer covers native Rust UI: Forge is backend Rust, Rune is Svelte.
   - *Recommendation:* route this before scheduling. The spike is three small UIs in three unfamiliar
     toolkits.
6. **Whether to run the webview control arm (Tauri + Svelte Flow).** *Recommendation:* yes if Rune is
   free. It turns "native is faster" from an assumption into a number, and it is the fallback if no
   native arm passes.

---

## 9. Spike proposal: S-UI-1, a 500-node plan diagram in each shortlisted toolkit

**Purpose.** Measure frame time, idle cost, memory, accessibility, text and build friction on one
identical workload, so that D-036 is ruled on numbers. It is not a prototype of factor.

### 9.1 Arms, with versions and renderers pinned

| Arm | Toolkit | Pinned | Renderer |
|---|---|---|---|
| A | egui | `eframe =0.36.2`, `egui_table =0.10.0` (`egui-snarl` optional; record whether used) | wgpu (eframe default) |
| B | GPUI | `gpui-kit =0.7.1`, which pins `gpui-pre =0.3.8` (= zed@279fe07) | Metal |
| C | Slint | `slint =1.18.1`, default features | FemtoVG on OpenGL (default). If time allows, one extra run with `renderer-skia`, recording that Skia's build fetches prebuilt binaries |
| D (optional control) | Tauri + Svelte + Svelte Flow | `tauri =2.12.1`; front-end versions recorded | WKWebView |

Layout follows D-011: a **separate** Cargo workspace (proposal: `spikes/ui-toolkit/`) with
`libs/spike-fixture` and `cmd/spike-egui`, `cmd/spike-gpui`, `cmd/spike-slint`. Rust 2024. Whether spike
code lands on `main` at all is the lead's call.

### 9.2 The shared fixture (`libs/spike-fixture`)

A deterministic generator, so no fixture file and no format question.
`fn plan(seed: u64, nodes: usize) -> Plan`, called with seed **3930** in every arm.
- **Shape:** a layered DAG with 25 layers.
  - Each node in layer k > 0 takes 1–3 inputs, mostly from layer k−1. 10% of edges skip one or more layers.
  - Target edge count is 1.5 × nodes: **500 nodes and about 750 edges** (gating), and **2,000 nodes and
    about 3,000 edges** (stretch).
- **Node content,** per `ui-brief.md` §2:
  - a 32px icon slot (a flat placeholder square);
  - an item name drawn from real names, including "Reinforced Iron Plate" and "Heavy Oil Residue";
  - a machine name, and a recipe name (10% prefixed "Alternate: ");
  - a count, `x1`–`x20`;
  - a clock from an exact fraction shown to 4 dp (e.g. `88.8888%`);
  - power `NN.NN MW`.
- **Edge content:** an exact rate label (e.g. `37.5/min`), drawn at the edge midpoint.
- **Positions are precomputed by the fixture** (layer x = k × 260 px, row y = i × 120 px), so layout cost
  is excluded. Auto-layout is measured separately and is toolkit-neutral.
- **A table dataset of 2,000 rows** (item, machine, count, clock, power), used in both the 500 and the
  2,000 runs.
- **A text set:**
  - `強化鉄板`
  - `صفيحة حديد مقواة`
  - `प्रबलित लोहे की प्लेट`
  - `Iron Ore — خام الحديد 80/min`
  These are test strings, not vetted translations.

### 9.3 The screen, identical in every arm

- **Window:** 1440×900 logical, on the M4's Retina display (2×).
- **Left panel, 280 px:** 10 target rows, each with an item label, an editable numeric rate field and a
  mode dropdown. Below them, a free-text **"Add target"** field (`ui-brief.md` §2). That field is the
  target of the IME and Arabic-caret tests.
- **Centre:** the diagram.
  - Nodes are rounded rectangles holding the fields in 9.2.
  - Edges are cubic Béziers with arrowheads and rate labels.
  - **Below 40% zoom, nodes render as compact chips (icon plus count)**, per `ui-brief.md` §4.11.
  - Off-screen culling is allowed. Record whether the toolkit or the arm does it.
- **Right inspector, 320 px:** the selected node's fields.
- **Bottom:** the 2,000-row table, virtualised, sortable by clock, with numbers right-aligned in tabular
  figures (`tnum`) where the toolkit allows it. Record whether it does.
- **Theme:** light and dark from one token set, following the system setting.

### 9.4 The scripted run

Each arm takes `--drive --nodes <N>`. The synthetic input goes through the toolkit's **event path**, not
by mutating state directly; record the path used.

**Two runs per arm:**
- `--nodes 500`: all steps 1–7. This is the run P1, P3, P4 and P5 are judged on.
- `--nodes 2000`: steps 1, 3, 4 and 7. This is the run P2 is judged on.

**Display:** set the display to **60 Hz** (System Settings → Displays → Refresh Rate) for every run, and
record the refresh rate in the results. The 16.7 ms thresholds and the positive control's expected rate
both assume 60 Hz. If 60 Hz cannot be set, halve the frame budgets (8.3 ms at 120 Hz), expect two
control hitches per animated second, and say so in the results.
1. Launch and load. Record **time to first frame** from process start.
2. **Idle 30 s,** with no input.
3. **Pan sweep, 10 s:** constant speed across the full diagram extent.
4. **Zoom sweep, 10 s:** 100% → 20% → 100%, crossing the LOD threshold twice.
5. **Select** a node with a synthetic click. Then **20 arrow-key moves along edges**; selection follows edges.
6. **Type** `45` into a target's numeric rate field.
7. **Table scroll:** top to bottom of 2,000 rows in 5 s.

### 9.5 Measurements and instruments

- **Frame time:** p50, p95 and p99, plus the count of frames over 33.3 ms. Reported separately for steps
  3, 4 and 7.
  - **Instrument:** external, `xcrun xctrace record --template 'Animation Hitches' --launch -- <bin> --drive`.
  - In-app present timestamps are secondary, and labelled as such if used. If the template does not see a
    given renderer (for example OpenGL), record that and fall back to the in-app timestamps.
- **Positive control, required before any number counts:** `--stall-every 60 --stall-ms 30` injects a
  30 ms UI-thread sleep every 60th frame. The instrument must report about one hitch per animated second.
  A run whose control does not show is **void**, not a pass.
- **Idle cost** during step 2:
  - CPU via `top -l 31 -s 1 -pid <pid> -stats cpu` (average of samples 2–31);
  - frames presented while idle, from the trace (expected about 0);
  - GPU activity via `sudo powermetrics --samplers gpu_power -i 1000 -n 30`. This is optional, and if
    skipped, record it as not run.
- **Memory:** `footprint <pid>` and RSS (`ps -o rss=`), after step 1 and after step 7.
- **Build friction:**
  - clean `cargo build --release` wall time (after `cargo clean`);
  - incremental rebuild after touching one UI file;
  - stripped release binary size;
  - unique packages, `cargo tree --prefix none -e normal,build | sort -u | wc -l`;
  - every non-Rust toolchain needed (Xcode, CMake, Skia download);
  - **hours to a working arm, and each blocker hit.**
- **Windows:** `cargo build --release --target x86_64-pc-windows-msvc` on a GitHub Actions
  `windows-latest` runner. The build is required; running on Windows is optional.
- **Accessibility,** with VoiceOver on; confirm the tree in Accessibility Inspector. Binary checks:
  - (a) a numeric rate field and the "Add target" field are each announced with their labels;
  - (b) a table row is announced;
  - **(c) the selected diagram node is announced** with machine, recipe, count and clock;
  - **(d) an arrow-key move announces the new node.**
- **Text:**
  - Render the text set. Pass when Arabic letters join and the RTL run order is correct, Devanagari
    conjuncts form, and CJK shows no tofu, judged side by side against macOS TextEdit rendering the same
    strings. Keep both screenshots.
  - **IME:** in the "Add target" field, type `てつ` and convert to `鉄`. Composition shows inline and
    commits.
  - In the same field, run egui's #8576 sequence on the string `عدد 123 مرحبا`: click, End, ArrowLeft ×3,
    type `x`. The correct result inserts at logical index 10 (`عدد 123 مرxحبا`, per #8576). Record the
    actual insertion point in every arm.

### 9.6 What "pass" means

These are proposed thresholds; the lead or Peter sets them.

| ID | Criterion | Gating? |
|---|---|---|
| P1 | 500 nodes, pan and zoom (steps 3–4): **p95 ≤ 16.7 ms and p99 ≤ 33.3 ms** | **gating** |
| P2 | 2,000 nodes, pan and zoom: p95 ≤ 33.3 ms | reported, not gating |
| P3 | Idle: **CPU ≤ 1%** averaged over 30 s, and about 0 frames presented | **gating** (it runs beside the game) |
| P4 | Table scroll (step 7): p95 ≤ 16.7 ms | **gating** |
| P5 | Accessibility (a)–(d) | (a) and (b) **gating**. (c) and (d) recorded with the build cost to close them; recommend gating before any release to others |
| P6 | Windows CI build green | **gating** (D-001) |
| P7 | Text set and IME correct | recorded. Whether it gates depends on §8 decision 2 |
| P8 | Memory | reported only; no basis for a threshold yet |
| P9 | The arm reaches the full screen within **2 working days** | **gating.** An arm that does not is a build-friction fail, recorded with where it stuck |

An arm **passes** when every gating row passes with a valid positive control. The spike **reports** all
rows for all arms. It ranks the arms but does not choose between them; that is D-036.

---

## 10. Sources

- Rulings and context: `../decisions.md` (D-001, D-024, D-030–D-034, D-036), `../design/ui-brief.md`.
- egui: https://github.com/emilk/egui (README, `CHANGELOG.md`, `crates/epaint/Cargo.toml`,
  `crates/eframe/Cargo.toml` at tag 0.36.2, `crates/egui-wgpu/src/renderer.rs`); issues
  https://github.com/emilk/egui/issues/1016, https://github.com/emilk/egui/issues/8576,
  https://github.com/emilk/egui/pull/5784; https://github.com/rerun-io/egui_table;
  https://github.com/zakarumych/egui-snarl; https://github.com/blitzarx1/egui_graphs
- GPUI: https://github.com/zed-industries/zed (`crates/gpui/README.md`, `Cargo.toml`, `src/_accessibility.rs`,
  `src/window.rs`, `src/styled.rs`); PR #56065 (AccessKit); issue
  https://github.com/zed-industries/zed/issues/31102; https://github.com/longbridge/gpui-kit (README,
  `Cargo.toml`, `LICENSE-APACHE`); crates.io `gpui-pre` (owner huacnlee).
- Zed funding [reported]: https://pulse2.com/zed-32-million-series-b-raised-for-scaling-collaborative-ai-coding
- Slint: https://github.com/slint-ui/slint (README, `LICENSES/LicenseRef-Slint-Royalty-free-2.0.md`,
  `api/rs/slint/Cargo.toml`, `api/rs/slint/lib.rs`, `internal/core/Cargo.toml`,
  `internal/backends/winit/Cargo.toml`, `internal/backends/winit/muda.rs`)
- Iced: https://github.com/iced-rs/iced (README, `CHANGELOG.md`); https://github.com/iced-rs/iced/pull/3281,
  https://github.com/iced-rs/iced/pull/3111
- Dioxus and Blitz: https://github.com/DioxusLabs/blitz (README); https://blitz.is/status/css;
  https://github.com/DioxusLabs/docsite (`docs-src/0.7/src/beyond/project_structure.md`,
  `docs-src/blog/src/release-070.md`); release notes
  https://github.com/DioxusLabs/dioxus/releases/tag/v0.8.0-alpha.0
- Others: https://github.com/linebender/xilem, https://github.com/makepad/makepad (issue #196),
  https://github.com/lapce/floem (issue #8), https://github.com/marc2332/freya, https://github.com/vizia/vizia,
  https://github.com/bevyengine/bevy (`crates/bevy_text/Cargo.toml`, `crates/bevy_winit/Cargo.toml`,
  `crates/bevy_feathers/src/lib.rs`, `crates/bevy_ui_widgets/src/`), https://github.com/AccessKit/accesskit
  (README licence section, `LICENSE.chromium`)
- UE5 [reported]: https://www.unrealengine.com/en-US/license (403 to fetch; summarised via search)
- Webview diagram scale [reported, third-party]: https://playbooks.com/skills/existential-birds/beagle/react-flow-architecture
- Crate metadata: https://crates.io/api/v1/crates/{name} and `/versions`, read 2026-10-08.

---

## 11. Not verified

| Claim | What I tried | Status |
|---|---|---|
| Diagram frame time at 500 or more nodes, any toolkit | Searched READMEs and the egui-snarl and egui_graphs issues; the only numbers are vendor or author claims | **Unmeasured.** This is the spike's job. |
| gpui-kit's "120 FPS", "hundreds of thousands of rows", "75+ components", AccessKit coverage | Read its README; did not run it | Vendor claim (Longbridge) |
| GPUI's Windows GPU backend, and whether `runtime_shaders` removes the full-Xcode requirement | gpui README covers macOS Metal and Windows text only | Unverified |
| GPUI `canvas()` element shape | Read the `Window` paint API in `window.rs`, not the element | Inferred |
| Slint scaling of 500 repeated components plus `Path` edges | No source or benchmark found | Unknown |
| Slint's `StandardTableView` virtualisation, IME, and the commercial-licence price | Not read | Not checked |
| Iced `table` virtualisation; Iced idle behaviour beyond "reactive rendering" | CHANGELOG only | Partly checked |
| Tabular figures (`tnum`) support in egui, GPUI and Slint | Not checked | Unknown; the spike records it (§9.3) |
| Bevy's reactive desktop mode in 0.20 | Not checked this session | Inferred |
| UE5 royalty and seat terms | Epic's licence page returned 403 to WebFetch; the terms come from a search summary of Epic's pages | Reported |
| Zed's funding | Press coverage via web search, with conflicting dates on aggregator sites | Reported |
| Funders of Linebender, Bevy, Floem, Makepad and Tauri | Not checked | Unknown |
| OpenGL deprecation on macOS as it affects Slint's default renderer | General knowledge | Not checked this session |
| Webview diagram scale (xyflow) | Web search found only third-party guidance | Reported, weak |
| Qt via cxx-qt, GTK via gtk4-rs, and smaller toolkits | Not examined | Out of range |
| Library docs via Context7 | The tool was not exposed this session | Docs read from repositories instead |
| GitHub code-search absences (Makepad and Floem `accesskit`) | Ran with a positive control (egui: 8 hits) and cross-checked against open issues #196 and #8 | Observed, with control. ⚠ GitHub code search **missed** `paint_path` in GPUI's 378 KB `window.rs`, which a direct read found, so a code-search zero alone proves nothing on large files |
| Build-time binary downloads | Checked a fixed list of crate names, not derived from the graph | Partial |
