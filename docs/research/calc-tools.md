# Factory-game calculator survey: tools

Survey date 2026-10-05. Current Satisfactory release: **1.2** (released 2026-06-02, latest patch 1.2.4.0, per [wiki.gg Update 1.2](https://satisfactory.wiki.gg/wiki/Update_1.2)). The CommunityResources Docs JSON in `factor/resources/` is 1.2 data (it contains `Build_FluidTruckStation_C` and `Recipe_PipelineJunction_T_C`, both new in 1.2).

**Evidence labels.** *Observed* means I read it on the tool's own repo, store page, changelog or site. *Reported* means a third party said it: wiki.gg listing, Steam review aggregator, news site. *Inferred* means I reasoned it from indirect evidence, such as source file names or open feature requests.

**How maintenance was measured.** Unless a line says otherwise, "pushed" is GitHub `pushed_at` from `gh api repos/<owner>/<repo>`, read 2026-10-05.

**Index used for discovery:** [satisfactory.wiki.gg/wiki/Tools](https://satisfactory.wiki.gg/wiki/Tools) lists about 60 entries. The tools below are the ones relevant to calculating or planning. Entries under "Listed only" were seen only in that index and not checked further.

---

## Satisfactory: checked against a primary source

### SatisfactoryTools
- **URL:** https://www.satisfactorytools.com · repo [greeny/SatisfactoryTools](https://github.com/greeny/SatisfactoryTools). Licence: NOASSERTION (custom LICENSE file). 537 stars, 74 open issues.
- **Maintained?** Barely. Last push 2026-03-29, which was CI and package bumps plus a `.sft` export fix. The last data change was "Added 1.0" on 2024-09-10, with a default switch to 1.0 on 2025-03-24. *Observed* (commit log).
- **Game version:** 1.0, with older versions selectable. No 1.1 or 1.2 data commit found (*inferred* from the commit log).
- **Standout:** LP solver (`src/Solver/Solver.ts` calls a server-side API) with per-resource max, per-resource weights, blocked recipes, allowed alternates, sinkable resources, and two production modes, per-minute or MAXIMIZE by ratio (`IProductionToolRequest.ts`, `Constants.ts`, *observed*). Multiple production tabs, cytoscape/ELK visualisation, codex for items, buildings, schematics and generators, version dropdown, `.sft` file export.
- **Gaps and complaints:** these are open feature requests on its own tracker (*observed*, [issues](https://github.com/greeny/SatisfactoryTools/issues)). No somersloop support (2025-07 "Accounting for Somersloops", 2026-02 "Manual Somersloop assignment", 2024-10 "Somersloop assignation"). A grep for `somersloop` over 157 source files found nothing; the same grep found `overclock`, which serves as the control. Overclocking appears only in codex detail views. The planner cannot set clocks, its power total says `// TODO handle overclocking` (`ProductionToolResult.ts:67`), and the request has been open since 2022-09. No "done" state on graph nodes (2024-10 and 2026-03). Alternates cannot be extracted from a save (open since 2021-03). Cannot pick a recipe from the visualisation (2026-05). Graph layout is not saved between tabs (2020-11). Users want converter recipes off by default. A solver bug "creates diamonds for no reason" (2026-05).

### SCIM (satisfactory-calculator.com)
- **URL:** https://satisfactory-calculator.com · map source [AnthorNet/SC-InteractiveMap](https://github.com/AnthorNet/SC-InteractiveMap), 216 stars. Planner repo [AnthorNet/SC-ProductionPlanner](https://github.com/AnthorNet/SC-ProductionPlanner) holds issues only; last push 2024-10.
- **Licence:** "Reuse of the source code and data assets is not permitted in any case… solely intended to be used on the satisfactory-calculator.com domain" (map README, *observed*). Its node and collectible data **cannot be a source for us**.
- **Maintained?** Yes. Map repo commits on 2026-08-28 add Dimensional Depot support. The homepage says "Stable build 1.2, updated until build 492,064" (*observed* via WebFetch of the homepage).
- **Standout (homepage, *observed*):** production planner, interactive map (459 nodes, 118 wells, 31 geysers, 1,242 slugs, 118 hard drives), save editor, power planner, blueprint library (4,938 blueprints, 467 "megaprints"), database, milestone/MAM/AWESOME trackers, world leaderboards, colour converter, hard-drive optimiser, balancer designs, mod data (93 mods).
- **Save editor (*inferred* from source file names in `src/`, not exercised):** `Selection/Copy|Delete|MoveTo|Offset|Rotate`, `Modal/Statistics/Game|Production|Storage`, `Modal/Power/Circuits|CircuitsBreakPriority`, `Modal/Train/Timetable`, `Modal/Map/Todo|Players|Hotbars|GameRules|Collectables`, `Modal/Node/SpawnAround`, `SubSystem/Blueprint|Foliage|Fauna|Unlock`. Remote save loading via `?url=` needs the server to have SSL and CORS (README, *observed*).
- **Gaps and complaints (*observed*, map issues):** an advert pop-up (2024-10 "Add log in option to the advert pop up"). Cloudflare blocks (2026-03; my own fetch of the planner page also got a Cloudflare 403). No 1.2 seed viewer (2026-03). Requested: mass-change clocks per recipe (2026-04), manage Depot items (2026-08), somersloop column (2024-10).
- **Not verified:** the planner's own option set. The page is behind a Cloudflare JS challenge (HTTP 403 to both WebFetch and curl).

### Satisfactory Modeler
- **URL:** [Steam app 3187030](https://store.steampowered.com/app/3187030/Satisfactory_Modeler/) · [itch.io](https://satisfactorymodeler.itch.io/satisfactorymodeler). Free desktop app (Windows, macOS, Linux) by David Price. Closed source.
- **Maintained?** Yes. Steam news posts on 2026-05-11 "Game Modes" (1.2 cost multipliers), 2026-04-24 translations, 2026-01-23 experimental manual calculator, 2025-08-26 blueprints and automatic clock speed (*observed*, Steam `GetNewsForApp` API).
- **Game version:** 1.2, based on the game-mode multiplier post.
- **Standout (*observed*):** a freeform canvas where you place machines and limits, and the tool simulates **how splitters and mergers actually divide flow, including priority splitting**. The store page says "advanced calculations that no other Satisfactory planning tool can do". Also outposts (nested sub-canvases), blueprints (reusable sub-modules with limits), miner type and node purity, parts/min or machine-count entry, a summary panel, storage containers, auto-save with backups, Steam Cloud sync, Space Elevator phases, game-mode multipliers, three calculation modes (none, manual, simulated), and 30 languages.
- **Reviews:** 97% positive of 1,737 on the store page (*observed*).
- **Complaints (*reported*, [vaporlens](https://vaporlens.app/app/3187030/satisfactory_modeler.md) aggregate of Steam reviews):** steep learning curve; slow or freezing on large builds; clunky UI; cannot set custom split ratios. Missing: no trains, trucks or drones, no snap-to-grid. Steam forum threads ask for a map background, notes and checklists, a mobile version, and help with save/load (*observed*, [discussions](https://steamcommunity.com/app/3187030/discussions/)).

### Kirk McDonald Satisfactory Calculator
- **URL:** https://kirkmcdonald.github.io/satisfactory-calculator/calc.html · repo [KirkMcDonald/satisfactory-calculator](https://github.com/KirkMcDonald/satisfactory-calculator). Apache-2.0, 81 stars.
- **Maintained?** No. Last push 2024-10-11 (*observed*).
- **Game version:** 1.0, the data snapshot from Oct 2024 (*inferred* from the date).
- **Standout (*observed* on the page and in the repo):** an in-browser simplex solver (`simplex.js`), resource priority set by drag-and-drop, recipe toggles, **per-recipe overclock and somersloops** (`factory.js`, `building.js` `maxSomersloop`, `solve.js`), node purity per miner recipe, belt and pipe tier, Sankey diagram (d3-sankey), state held in the URL fragment, average and peak power, values shown as decimals or rationals.
- **Gaps:** these are *observed* open issues. No 1.2 cost multipliers (2026-04). No saving or sharing beyond the URL (2025-03). No FICSMAS recipes. The data has no fuel generators, so there is no power-plant planning (*inferred* from `data/data.json` buildings). Requests from 2019 for overclock and somersloop-era features are **stale**: the code implements overclocking, so open issues are not evidence of absence here.

### FactorioLab
- **URL:** https://factoriolab.github.io/satisfactory · repo [factoriolab/factoriolab](https://github.com/factoriolab/factoriolab). MIT, 870 stars, 86 open issues.
- **Maintained?** Very. Pushed 2026-10-01. Satisfactory data updated 2026-08-11, recipe-cost-multiplier fixes 2026-08-16 and 2026-09-17 (*observed* commits).
- **Game version:** Satisfactory 1.2 (`public/data/sfy/data.json` shows `{"Satisfactory":"1.2"}`, *observed*).
- **Multi-game:** Factorio (incl. Space Age), Dyson Sphere Program, Satisfactory, Captain of Industry, Techtonica, Final Factory, Factor Y, Foundry, Outworld Station. The UI strings also list Belts of Iron, Mindustry, MoteMancer, SkyFormer, StarRupture and a "Custom" game (*observed*, README and `en.json`).
- **Standout (*observed* in `public/i18n/en.json` and the source tree):** GLPK simplex. Objective types Output, Input, Limit and Maximize, with units items, belts, machines or wagons. A cost-settings dialog weighting surplus, unproduceable, excluded, machine count, footprint and recipe cost, with infeasible or unbounded diagnostics naming the recipe responsible. Preferred machine, belt, fuel and wagon rankings. Presets. Technologies-researched import. A recipe cost multiplier. Flow diagram as Sankey or box-line (ELK layered, force or stress). Configurable list columns, a tree column, step checkmarks. Full URL state plus named saved states. A game-data editor for custom datasets. i18n. Light, dark or system theme with hue and lightness.
- **Gaps:** single-factory model, with no factory network and no collaboration. There is no map and no save import.

### Satisfactory Factories
- **URL:** https://satisfactory-factories.app · repo [satisfactory-factories/application](https://github.com/satisfactory-factories/application). 53 stars. Licence file present but type not checked.
- **Maintained?** Very. Pushed 2026-10-05, with a long CHANGELOG through "Beta v0.7.2" plus unreleased work (*observed*).
- **Game version:** 1.2 per the wiki.gg listing (*reported*). The changelog covers 1.1-era content such as the Dimensional Depot and Mercer Spheres (*observed*).
- **Standout (*observed* CHANGELOG):** a **manual factory-network ledger**, not an auto-solver. You set product quantities per factory, and the tool resolves imports and exports between factories, flags shortages and surpluses, and offers named "Satisfy (240)" / "Trim (480)" sizing buttons, including sizing against supplier capacity. Nine factory status chips across red, amber and blue tiers. Factory groups with rollups. A checklist mode with desync detection. Tasks and notes. Building groups (miner mark and purity per group, "Spread" even clocks). Mining factories and resource wells. A **breaking choice that raw resources must be explicitly mined or imported**, with a migration wizard. AWESOME Sink and Dimensional Depot modelling. Custom non-producing buildings (portals, stations). Material-cost bill. Plan search. Up to 300 factories per plan.
- **Collaboration and sync:** local, synced or shared tabs. Snapshot links. Live rooms (`/room/three-word-slug`) with optional password. Per-field edit locks. Offline mode with a conflict prompt. Accounts optional. Server-side text-content rules. An anonymous usage heartbeat.
- **Gaps:** no solver, so recipe choice is manual, and no map.

### Satisfactory Logistics
- **URL:** https://satisfactory-logistics.xyz · repo [rockfactory/satisfactory-logistics](https://github.com/rockfactory/satisfactory-logistics). 61 stars. Changelog on [featurebase](https://satisfactorylogistics.featurebase.app/changelog).
- **Maintained?** Yes. v0.15.1 on 2026-06-09 added 1.2 power and recipe multipliers (*observed* commits).
- **Game version:** 1.2 multipliers (v0.15). 1.1 data since v0.10 (2026-04-13).
- **Standout (*observed* changelog and source tree):** combines factories (inputs and outputs tracked between them) with an LP calculator. Optimisation method can be "compact" or "power-efficient". Somersloop and overclock per machine node. Building restrictions at game and factory level. Converter-recipe kill switch. Kanban board with Draft/Todo/In Progress/Done states. Disabled factories. Real-time sync across tabs, devices and teammates (Supabase, Discord or Google login). Codex. Cmd+K spotlight. Per-factory notepad. Splitter calculator. Interactive tutorial. PWA offline mode. **Import from SatisfactoryTools `.txt`**. Sankey and graph charts.
- **Gaps:** no map and no save import (*inferred* from the source tree).

### FICSIT Planner
- **URL:** https://ficsit-planner.pages.dev · repo [Albis0/ficsit_planner](https://github.com/Albis0/ficsit_planner). GPL-3.0.
- **Maintained?** Created 2026-09-23 and pushed 2026-10-05, so it is two weeks old. The README says "Coded with AI". Its feature list is **author claims, not exercised** (*observed* README only).
- **Game version:** 1.2, based on game settings for cost, power and Space Elevator multipliers in the README.
- **Standout (claimed):** HiGHS-WASM LP. Multi-target factory tabs. On-hand inputs. Tier gating. Per-resource caps, with "spare scarce first" or "all equal" weighting. Pinned inputs that scale the targets. Automatic clock speeds with minimum shards. Somersloops placed automatically ("Auto place" / "Use all"). Extraction by miner mark, purity, clock and the actual nodes you own. Graph that splits a flow over several belts. A transport view where you pick belt, train, truck, drone or fluid truck and enter a distance. A power-plant planner. Codex. World map with all nodes and collectibles. Linked factories. URL share links with nothing uploaded. In-app feedback with the factory attached. PWA offline with a phone layout.
- **Gaps:** age. Nothing about it has been tested by users yet.

### Ficsit Companion
- **URL:** https://adepierre.github.io/ficsit-companion · repo [adepierre/ficsit-companion](https://github.com/adepierre/ficsit-companion). MIT, 48 stars. C++/ImGui, runs on the web and as a desktop app.
- **Maintained?** Yes. v1.2.2 on 2026-06-14 added production and power multipliers (*observed* releases).
- **Standout (*observed*):** a manual node editor. The user wires recipe, merger and splitter nodes, and rates propagate through the graph. Pins can be locked. Somersloop counter. The author says on purpose: "I'm not a fan of fully automatic tools… they take away part of the fun of the planning phase."
- **Gaps (author's roadmap, *observed*):** no auto-planning, no auto-layout, no image export. In-game integration and other games are only ideas.

### SatisfactoryBase
- **URL:** https://satisfactorybase.com. Closed source.
- **Maintained?** The site says "Satisfactory 1.2 (Beta)" (*observed* via WebFetch).
- **Standout (*observed* site text):** all-in-one. Exact solver with alternates and resource limits. Overclock and shards per machine. "Magic Wand" that builds upstream chains. World map. **Train route planning where moving a waypoint updates route capacity**. Belt and pipe throughput planning. Balancer tool. **1.2 world-seed entry for randomised layouts**. Accounts with publish/privacy controls. Invite viewers or editors. Savegame upload rendered on the map. Blueprint gallery. Wiki. World statistics.
- **Gaps:** not checked beyond the landing text. The train-route, world-seed and collaboration lines were confirmed in raw HTML. The site is built with **Svelte**: `svelte-*` class hashes appear in the HTML (*observed*).

### Ferrumium
- **URL:** https://ferrumium.com. Open beta, closed source.
- **Standout (*observed* site text):** React Flow node editor that "auto-assembles production lines". Belt splitters. Save analysers. Real-time co-op planning. Community sharing. Works without an account. Keyboard shortcuts.
- **Maintained?** Unknown. No date found on the landing page. **Game version:** not stated. **Gaps:** not checked. The co-op and auto-assemble claims were confirmed in raw HTML ("Auto-assemble production lines, plan together in real time with co-op").

### Factory Manager
- **URL:** repo [raffaelemaiorino/factory-manager](https://github.com/raffaelemaiorino/factory-manager). Local desktop app. Pushed 2026-09-09.
- **Standout (*observed* README):** auto-plan from targets, combining shared intermediates. Power plans sized by MW or by fuel/min. A power-shard budget. Caps on the highest belt and pipe Mk. A "sink byproducts" option. Simple or complex tree view, where complex mode splits steps into manifold banks. PNG export. **Transport plans** (route, vehicle, cargo, outbound and return times, giving vehicle and freight-car counts and train composition). Dashboard KPIs. JSON export and import. Fully offline. SCIM-derived catalogue languages.
- **Game version:** not stated in README. **Gaps:** no map, no save import, no sharing beyond JSON files (*inferred* from the README feature list). Using SCIM catalogue data may conflict with SCIM's no-reuse licence (*inferred*; not checked).

### Satisfactory Architect
- **URL:** https://satisfactory-architect.com · repo [ArthurHeitmann/satisfactory-architect](https://github.com/ArthurHeitmann/satisfactory-architect). 17 stars. **Svelte** frontend with an optional Deno backend. Pushed 2026-03-03.
- **Standout (*inferred* from the `ui/src/lib` tree):** a graph editor with pages, undo history (`StateHistory.svelte.ts`), throughput calculation, and a sync server (`sync/ServerConnection`, `objectDiff`, zstd). Game data is extracted with FModel (README, *observed*).
- **Game version:** 1.0 per wiki.gg (*reported*). **Gaps:** not checked; README is build instructions only.
- **Note:** this and SatisfactoryBase are the closest stack matches to Peter's SvelteKit.

### Satisfactory Solver
- **URL:** repo [Scott1903/satisfactory-solver](https://github.com/Scott1903/satisfactory-solver). Django + Pyomo + HiGHS. Pushed 2026-02-19. It replaces the PySimpleGUI desktop app, which was abandoned when that library went paid (*observed* README).
- **Standout:** resource limits, optimisation weights, alternate toggles, accounts with saved presets. The older version read `CommunityResources/Docs/Docs.json` directly (`read_docs.py`), and its README says that script was "out of date for 1.0, some manual input was needed".
- **Game version:** not stated. **Gaps:** no graph view or extraction modelling is mentioned. A Django server is required.

### Satisfactory-Optimizer
- **URL:** repo [Zistack/Satisfactory-Optimizer](https://github.com/Zistack/Satisfactory-Optimizer). A Python script using `scipy.optimize.linprog` with "a highly configurable set of constraints". Pushed 2026-03-19, 16 stars (*observed* repo description). **Game version:** not stated. **Gaps:** a script, not an app; no UI.

### Satisfactory Logistics Map
- **URL:** repo [Fade97/satisfactory-logistics-map](https://github.com/Fade97/satisfactory-logistics-map). Self-hosted Docker. Pushed 2026-10-02.
- **Standout (*observed* README):** a web map for **your own dedicated server**. It pulls the save through the **Dedicated Server API (`api://server:7777` with the admin password)**, or SFTP, FTP or a folder. Overview of what is stuck. Map with trains, trucks, players (follow mode), a heatmap of stopped machines and item flow. Factories detected automatically from the belt network. Stopped machines with the reason. 3D view per factory. Power grids and fuel range. Train schedule check. History from hours to months (SQLite). A planner restricted to unlocked recipes that can use factory surplus. Experimental blueprint export. Kiosk mode. PWA. Optional FRM for 5-second live updates.
- **Security posture (*observed*):** reading is open, writing needs a password, and an IP is blocked for 10 minutes after 10 failed attempts. The README says "Do not expose the FRM port publicly."
- **Game version:** not stated; it reads current saves. **Gaps:** dedicated servers only, Docker self-host, autosave cadence (about 5 minutes) without FRM. The UI is EN/DE only.

### SatisfactoryMCP
- **URL:** repo [lukszi/SatisfactoryMCP](https://github.com/lukszi/SatisfactoryMCP). Pushed 2026-10-05.
- **Standout (*observed* README):** an MCP server with 49 tools, plus a local web map, that reads your saves (read-only) and the game's own data dump from a local install. It plans with an optimiser over your **unlocked** recipes. Tools include `diff_vs_save`, `commission_plan`, `trace_upstream`, `factory_health`, `rank_build_sites`, `advise_hard_drive_pick`, `bom` and `explain_byproducts`. It "reports infeasible instead of overstated" when byproducts would be stranded. Each answer names the save file and its age.
- **Game version:** whatever local install it reads, so it tracks the game automatically. **Gaps:** Windows-first. Needs a local game install and an MCP client. No sharing.

### FicsIt Remote Monitoring
- **URL:** [ficsit.app/mod/FicsitRemoteMonitoring](https://ficsit.app/mod/FicsitRemoteMonitoring) · repo [porisius/FicsitRemoteMonitoring](https://github.com/porisius/FicsitRemoteMonitoring). Last mod version 2026-08-12, 55,944 downloads (*observed*, ficsit.app API).
- **Standout:** an in-game mod that serves a JSON HTTP API (`getFactory`, `getPower`, `getProdStats`, `getTrains`…), a web UI, websockets and **serial output to Arduino**, with an integrated alert system.
- **Game version:** latest release 1.5.3 requires game build >=491125, i.e. 1.2 (*observed*, ficsit.app API). **Gaps (README):** the icon system does not work on dedicated servers without copying files by hand. 43 open issues.

### FRM Companion Bundle
- **URL:** repo [featheredtoast/satisfactory-monitoring](https://github.com/featheredtoast/satisfactory-monitoring). 126 stars, pushed 2026-04-05.
- **Standout (*observed* README):** Docker stack of Grafana, Prometheus, Alertmanager and Postgres over FRM. Production over time, power and battery, drone, train and truck paths with round-trip times, a machine-efficiency heatmap, storage search, drop-pod map, and **Discord alerts on tripped fuses and low battery**. Can monitor several servers.
- **Game version:** follows FRM. **Gaps:** needs about 2 GB RAM and the FRM mod. Default Grafana credentials are admin/admin (README).

### Satisfactory World Seed Tool
- **URL:** https://satisfactoryworldseed.com (*observed* via WebFetch).
- **Standout:** a 1.2 world-seed viewer. Randomisation presets, six purity settings, and a **seed finder that ranks seeds against the resources you want at chosen nodes**. Covers 608 markers.
- **Maintained?** No date found. **Gaps:** not checked. Closed source, author unknown.

### Satisfactory in-game mods
- Versions and downloads from the ficsit.app GraphQL API, *observed*:
  - **Efficiency Checker** (2026-09-27, 470k): shows production underflow, with a hand tool.
  - **Factory Analytics** (2026-08-14): per-item production, storage, power and efficiency with an always-on HUD.
  - **Factory Statistics** (2024-10-23, stale): lists producers with filters, plus inventories.
  - **Throughput Counter and Limiter** (2026-08-17): belt items/min.
  - **Power Checker** (2026-08-16): "check if your fuses can blow".
  - **Cartograph** (2026-06-11): buildings on the in-game map.
  - **FicsIt-Networks** (2025-09-09): scriptable computers.
- **Game version (latest release `game_version`, *observed*):** FRM, Cartograph >=491125; Efficiency Checker, Factory Analytics, Throughput Counter >=502094; Power Checker >=495413 — all 1.2-era builds. FicsIt-Networks >=415558 and Factory Statistics >=365306 are older builds.
- **URL:** https://ficsit.app (the mod pages are `ficsit.app/mod/<reference>`). **Gaps:** these are instruments, not planners.
- **No in-game production *planner* mod was found for Satisfactory.** The ficsit.app search by reference returned none for `ProductionPlanner` and `SatisfactoryProductionPlanner`, and keyword search is popularity-ranked, so it is noisy. That is "no entry found", not proof that none exists.

### Save parser libraries
- [etothepii4/satisfactory-file-parser](https://github.com/etothepii4/satisfactory-file-parser): MIT, saves and blueprints, pushed 2026-09-13.
- [GreyHak/sat_sav_parse](https://github.com/GreyHak/sat_sav_parse): pushed 2026-08-15.
- [Goz3rr/SatisfactorySaveEditor](https://github.com/Goz3rr/SatisfactorySaveEditor): 305 stars, stale since 2024-08.
- [ficsit-felix](https://github.com/ficsit-felix/ficsit-felix): save visualiser, stale since 2022.
- *Observed* via repo metadata. These are libraries, not end-user tools, and they are the realistic route to save features. **Game version:** not checked per library. Save format changes with game updates, so currency matters. **Gaps:** not checked.

### Splitter Calculator
- **URL:** https://icemoonmagic.github.io/Satisfactory-Splitter-Calculator/ · repo [IceMoonMagic/Satisfactory-Splitter-Calculator](https://github.com/IceMoonMagic/Satisfactory-Splitter-Calculator). 47 stars, pushed 2025-11-01. Computes splitter arrangements for an exact items/min split (*observed* description). **Game version:** not version-dependent (pure arithmetic). **Gaps:** not checked.

---

## Satisfactory: listed only (wiki.gg index, not checked further, so all *reported*)

### Satisfactory Balancer Calculator
satisfactory-balancer-calculator.app. Three modes: belt balancer, load balancer, belt compressor.

### Satisfactory Hub
satisfactory-hub.vercel.app. Calculator plus an offline interactive map, installable as a PWA on mobile.

### Satisfactory Toolbox (Android)
`dev.tievo.satisfactory_toolbox`. The wiki says "server management, map, calculator, collectible tracking; offline support". The Play Store page did not render through fetch, and web search found nothing beyond the wiki listing.

### satisfactoryplanner.net
"Ultimate factory planning tool" in 4 languages. The page did not render (empty JS shell).

### Manifolder
manifolder.app. Production calculator plus a layout mode with modular planning. The page returned only its title.

### 2D layout planners
satisfactory-layouts.com (1.0+, blueprint and hotkey features), planit-mocha.vercel.app (grid), ficsitproductionplanner.atrumcore.com (1.2, multi-floor, "seed generation"), SaLT (outdated, 2021), satisfactory-schematics.7tonshark.com (pre-rendered 2D building drawings).

### Statisfactory
statisfactory.net. "More insights and stats about your factories", with maps and tables, from saves. The page errored when fetched.

### Blueprint repositories
satisfactoryblueprints.com, sbs.kmods.space (accessible in game through the SBS mod), ficsitdb.com/blueprints. SCIM's own library is covered under SCIM.

### Satisfied Planner 2
madeinnewyork87.github.io/SatisfiedVisual2. Visual node planner with an "AI Architect", 1.0 with somersloops.

### Sankey Factory
sankeyfactory.github.io. Production chains in a Sankey view, mobile-compatible.

### Machine Fill
satisfactory.greeny.dev/machine-fill. Manifold fill-time calculator. Update 2 only, so stale.

### Spreadsheets
satisfactory-sheet.com (rate calculator with saves, 1.0), a Steam-guide Google Sheet, refactory.ignorare.app (spreadsheet-like, 1.0).

### World Generator (konsl)
konsl.github.io/satisfactory-world-generator. Evaluates world-seed options.

### SatisGraphtory
satisgraphtory.com / [rhocode/SatisGraphtory](https://github.com/rhocode/SatisGraphtory). Graph planner, last pushed 2023, Update 5/6, so stale. A new `SatisGraphtory/SatisGraphtory` repo pushed 2026-09 has only "It's a Graph!" as its README.

---

## Other games (lighter pass, aimed at features the Satisfactory tools lack)

### Kirk McDonald Factorio Calculator
https://kirkmcdonald.github.io · repo [KirkMcDonald/kirkmcdonald.github.io](https://github.com/KirkMcDonald/kirkmcdonald.github.io). 750 stars, pushed 2025-07-02, 127 open issues. The original "ratio calculator" that FactorioLab explicitly builds on. URL-fragment state, simplex solver, modules and beacons, Sankey. Game version and gaps were not checked (light pass).

### Helmod
[mods.factorio.com/mod/helmod](https://mods.factorio.com/mod/helmod) · [Helfima/helmod](https://github.com/Helfima/helmod). MIT. v2.3.3, about 3 months old, for Factorio 0.14–2.1, about 546k downloads (*observed* mod page). An **in-game** planner with production blocks, energy, modules and beacons, a selectable time base, and **multiplayer sheet sharing with read/write/delete permissions** managed by an admin. Exposes a remote Lua API (`helmod_interface`). **Gaps:** not checked (light pass).

### Factory Planner (Factorio)
[mods.factorio.com/mod/factoryplanner](https://mods.factorio.com/mod/factoryplanner) · [ClaudeMetz/FactoryPlanner](https://github.com/ClaudeMetz/FactoryPlanner). MIT. v2.1.18, released 3 days before the survey, pushed 2026-10-05. **In-game.** Infinitely nesting subfloors, an optional matrix solver for complex loops, timescale choice, mining productivity, modules, works with any content mod, and a remote data interface. **Game version:** Factorio 0.17–2.1, including Space Age (mod page). **Gaps:** not checked (light pass).

### YAFC-CE
repo [shpaass/yafc-ce](https://github.com/shpaass/yafc-ce). GPL-3.0, desktop (.NET plus OR-Tools), pushed 2026-08-18, 124 open issues. Built for heavily modded, recursive Factorio. Links balance only the goods you link. Nested tables. Auto-modules from milestones. **Analyses:** accessibility, milestone gating, "cannot be automated", **per-item cost**, whole-base flow. "Never Enough Items" recipe explorer. Dependency explorer. Undo. CLI project load. **Game version:** Factorio 2.0+ (0.9.1 was the last for 1.1). **Gaps:** inserters are not included in energy totals (README). Accessibility analysis may fail on some modpacks.

### Foreman2
repo [DanielKote/Foreman2](https://github.com/DanielKote/Foreman2). 344 stars, pushed 2026-08-03, Windows .NET plus OR-Tools. A visual flowchart editor with source, sink, passthrough and recipe nodes. Fixed or auto building counts. Colour-coded node health: red for unachievable, gold for overproduction, orange for errors, with **click-to-auto-resolve**. Copy and paste of node groups. Grid snap. Image export. Preset compare across modpacks, so you can see what a mod update changed. **Game version:** Factorio 2.0 vanilla preset by default. **Gaps:** the README calls it a DEV version that is "prone to crashes" with no auto-save. Windows only (a Mac/Linux fork exists).

### dsp-calc-opt
Dyson Sphere Program. https://yuki-216.github.io/dsp-calc-opt/ · repo [yuki-216/dsp-calc-opt](https://github.com/yuki-216/dsp-calc-opt), a fork of DSPCalculator/dsp-calc. Pushed 2026-10-01. HiGHS-WASM whole-network LP. Multiple mod data sources. Proliferator optimisation against min power, rarity weight, min net heat or min footprint. **Integer-count suggestions** that mix machine tiers to reach even counts. Footprint estimate. Fuel chain reduced to raw minerals. "Compute this item in a new window". Negative demand meaning external supply. Seed viewer with statistics. LP-failure fallback to the last good recipe set. JSON config import and export. (README in Chinese, *observed*.) **Game version:** not stated. **Gaps:** on phones it renders the desktop layout at a fixed 850px viewport (README).

### Alchemy Factory Calculator
The game is **Alchemy Factory** by D5 Copperhead, published by Gamirror Games. Early Access 2025-12-11, 1.0 on 2026-09-07, Steam app 3669570. It has co-op, a dedicated server and Steam Workshop blueprints (*observed* store page). Not to be confused with *Liz and Rose's Alchemy Factory* (2026-04-22), which is an adventure RPG (*observed* store page).
Tool: https://joejoesgit.github.io/AlchemyFactoryCalculator/ · repo [JoeJoesGit/AlchemyFactoryCalculator](https://github.com/JoeJoesGit/AlchemyFactoryCalculator), pushed 2026-10-03, AI-assisted. Recursive chain calculator. Share "chain-codes" or links. Self-feeding fuel and fertiliser loops. Per-item byproduct recycling. Construction list with cost. **Heat and nutrient totals**. **Profit/loss against sell price**. External-input toggles. Recipe swaps. Research upgrade levels. **In-browser recipe database editor**. ~~Needed because the game ships no official data dump, so recipes are transcribed by hand (*inferred* from the editor's existence and the README's "if the recipe I have is wrong").~~ **Superseded 2026-10-05 by `data-sources-research.md` §5:** the game ships no official dump, but its data is extractable. It is UE5 with unencrypted IoStore paks, and its DataTables `DT_Enemies` (items), `DT_EnemyCrafting` (recipes) and `DT_Buildings` are read with CUE4Parse plus a usmap/jmap dumped from the running game (*reported* by two independent repos, PheeZz/alchemy-factory-calculator and Monstrel/yaafc). This calculator's own DB is still hand-maintained.
- **Game version:** not stated. **Gaps (README to-do):** World Tree, cauldron and paradox items are unhandled. Recursive loops sometimes fail. No efficient-recipe finder. No tier locking. No visual module planner yet.

### Alchemy Factory Tools
https://alchemyfactorytools.com · repo [moldy530/alchemy-factory-planner](https://github.com/moldy530/alchemy-factory-planner) (Next.js, pushed 2026-09-25). Self-description only: "plan crafting chains, calculate resource requirements, and optimize your factory layouts" (*observed* landing text). Features not verified, so **it is deliberately absent from every `seen_in` list**. **Game version:** not stated. **Gaps:** not checked. Attributing a feature from a one-line tagline would be guessing.

### Alchemy Factory Codex
https://alchemy-factory-codex.com. Mentioned in the JoeJoesGit README as the community codex, "actively working on it still" per that README (*reported*). Not fetched, so maintenance, game version and gaps were not checked.

---

## Deliberately excluded
- `Basaltzedolmen/satisfactory-hack-2026-ficsit-megafactory-toolkit` and `leon-tech-eng90i3/Alchemy-Factory-Assistant`. Their descriptions ("Hack 2026"; "Unlimited Resources… Instant Crafting… Mega XP") match the shape of cheat or malware-lure repos. Not opened.
