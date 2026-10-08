# Feature verdicts, exported from the picker on 2026-10-08. The picker database is the source; this file is a snapshot.

| id | category | feature | verdict | Peter's note | description |
|---|---|---|---|---|---|
| F-001 | Solver | LP auto-solve to target rates | mvp |  | You enter target items and rates; a linear-programming solver chooses which recipes to run and how many machines of each, minimising some cost. |
| F-002 | Solver | Recursive tree expansion (no optimiser) | skip |  | Each item is made by one chosen recipe and the tool expands ingredients recursively to the target rate; no optimisation, no global balancing. |
| F-003 | Solver | Manual node graph with rate propagation | shape |  | The user places recipe/splitter/merger nodes and wires them; the tool propagates rates through the user-built graph but never chooses recipes itself. |
| F-004 | Solver | Splitter/merger behaviour simulation | later |  | Simulates how in-game splitters and mergers actually divide and combine flow (including priority splitters), so a drawn layout's real throughput is computed, not the ideal ratio. |
| F-005 | Solver | Manual ledger with satisfy/trim sizing | later |  | The user sets quantities by hand; the tool reports each shortfall or surplus and offers buttons that size a row exactly to need or to supplier capacity, naming the number it will set. |
| F-006 | Solver | Maximize output under limits | mvp |  | Instead of a target rate, maximise production of one or more items (optionally in fixed ratios) subject to resource or recipe limits. |
| F-007 | Solver | Scale targets to a pinned input | mvp |  | Type how much of a raw resource you actually have and the targets scale to consume exactly that. |
| F-008 | Solver | Use on-hand / external supply | mvp |  | Mark items that arrive from elsewhere (another factory, a train) so the plan consumes them rather than building their chain. |
| F-009 | Solver | Per-resource caps | mvp |  | Set a per-minute maximum for each raw resource (default: the whole map's supply) that the plan may not exceed. |
| F-010 | Solver | Resource scarcity weighting | shape |  | Weights in the objective so the solver prefers abundant resources and spares scarce ones (or treats all equally). |
| F-011 | Solver | Selectable optimisation goal | shape |  | Choose what 'best' means — fewest buildings, least power, least raw resource, smallest footprint — and get a different plan. |
| F-012 | Solver | Solver cost tuning | skip |  | Expose the solver's penalty weights (surplus, unproduceable item, excluded item, machine count, footprint, recipe cost) to the user. |
| F-013 | Solver | Infeasibility diagnostics | shape |  | When no plan exists, say why — which limit is too tight, which recipe makes a maximise unbounded, which ticked alternate was kept out. |
| F-014 | Solver | Byproduct handling | mvp |  | Account for secondary outputs: feed them back in, route them to a sink, package them, or flag them as unhandled (which would back up and stop machines in game). |
| F-015 | Solver | Recipe loops and recursive recipes | mvp |  | Correctly solve chains where an item is (directly or indirectly) an ingredient of itself — recycled rubber/plastic, fuel loops, self-fertilising farms. |
| F-016 | Solver | Whole-machine counts and clock spreading | mvp |  | Turn fractional machine counts into buildable whole numbers with a clock speed (e.g. 3 machines at 83.3%), or spread a group so every machine runs identically. |
| F-017 | Solver | Pause or manual recalculation | shape |  | Stop automatic recomputation while editing a large plan and recompute on demand. |
| F-018 | UI | Undo / redo | shape |  | Step back and forward through edits to a plan. |
| F-019 | Recipes | Alternate recipe toggles | mvp |  | Enable or disable each alternate (and standard) recipe so the planner may or may not use it. |
| F-020 | Recipes | Converter recipe switch | mvp |  | Exclude or include the Converter's resource-transmutation recipes as a group (they make almost anything from SAM and distort optimal plans). |
| F-021 | Recipes | Progression gating (tier / research) | mvp |  | Pick your unlocked tier or research and hide recipes, buildings, belts and miners you cannot have yet. |
| F-022 | Recipes | Unlocked recipes read from a save | later |  | Read which alternates and milestones you actually own from your save file and restrict the planner to them. |
| F-023 | Recipes | Alternate recipe comparison | mvp |  | Compare the ways of making an item side by side (raw cost, power, buildings) to decide which alternate is better. |
| F-024 | Recipes | Hard drive research advisor | later |  | Given the alternates offered by a pending hard drive, recommend which to pick for your goals. |
| F-025 | Recipes | Recipe swap from the graph or row | mvp |  | Click a machine or row and switch it to another recipe for the same product without leaving the view. |
| F-026 | Recipes | Game-mode multipliers (1.2) | mvp |  | Apply 1.2 game-mode settings: recipe parts cost multiplier, power consumption multiplier, Space Elevator deliverable cost multiplier. |
| F-027 | Recipes | Seasonal content toggle | later |  | Include or hide event-only (FICSMAS) items and recipes. |
| F-028 | Recipes | Mod content support | shape |  | Plan with recipes and buildings added by mods, not only vanilla. |
| F-029 | Data | User-editable recipe database | later |  | Edit or add items and recipes in the tool itself (stored locally) to fix data errors or add content. |
| F-030 | Data | Game version switcher | shape |  | Choose which game version's data the plan uses (e.g. 1.0 vs 1.2, experimental vs stable). |
| F-031 | Production modifiers | Overclock / underclock per machine | mvp |  | Set a machine's clock speed (1–250%) and get the scaled rate and the game's non-linear power draw. |
| F-032 | Production modifiers | Power shard count and budget | mvp |  | Count the power shards a plan needs and optionally plan within a shard budget (prefer 100% clocks). |
| F-033 | Production modifiers | Somersloop production amplification | mvp |  | Model somersloops in a machine: up to double output, with power scaling by the square of the boost. |
| F-034 | Production modifiers | Auto-place a limited somersloop supply | later |  | Enter how many somersloops you own and let the planner place them where they save the most. |
| F-035 | Production modifiers | Research and upgrade levels | shape | was thinking upload to dim storage but that is an end state, miners speed depends on the miner, so that case its a different machine i guess | Account for researched bonuses that change rates (belt speed, machine efficiency, mining productivity, upload rate). |
| F-036 | Multi-game | Modules, beacons, proliferators, quality | shape |  | Game-specific machine modifiers (Factorio modules, beacons and quality; DSP proliferator), with presets and auto-allocation. |
| F-037 | Power | Plan power total | mvp |  | Total power a plan consumes, as average and as peak. |
| F-038 | Power | Variable-power machines | mvp | also for geothermal at the generation end of things | Handle machines whose draw cycles (Particle Accelerator, Converter, Quantum Encoder) as min/max/average instead of a constant. |
| F-039 | Power | Power plant planner | mvp |  | Size generators from a MW target or from available fuel, including the fuel chain, water and waste (nuclear). |
| F-040 | Power | Self-powered factory | mvp | i need to understand this one more | Fold the generators and fuel needed to power a plan into the plan itself, so power reduces to raw resources. |
| F-041 | Power | Power balance per factory or group | shape |  | Show generated vs consumed vs balance per factory, per group and per plan, with deficit warnings. |
| F-042 | Power | Power augmenter boost | mvp |  | Model the Alien Power Augmenter's grid-wide percentage boost. |
| F-043 | Extraction | Extractor sizing by mark, purity and clock | mvp | when we say hard coded we mean in the schema the model uses correct? not hard constants in the rust code | Compute how many miners/pumps/extractors a raw demand needs, given miner mark, node purity and clock speed. |
| F-044 | Extraction | Node inventory input | mvp |  | Enter the nodes you actually have (e.g. one pure, one impure) and get miners per node, or what would close a shortfall per purity. |
| F-045 | Extraction | Resource well planning | mvp |  | Plan Resource Well Pressurizers with satellite extractors of mixed purity for water, oil and nitrogen. |
| F-046 | Extraction | Raw resources must be sourced | shape | need to understand the ramifications of this one. seems all the games have to be mined, factorio has limited supply, what does this option provide of value | Treat raw resources like any other input that must be explicitly mined or imported, instead of assuming unlimited free supply. |
| F-047 | Extraction | Hand-gathered items | mvp |  | Recognise items no extractor can produce (leaves, wood, mycelia, alien remains, slugs) and treat them as gathered. |
| F-048 | Logistics | Belt and pipe sizing | mvp |  | For each flow, show how many belts or pipes of which tier it needs, and split a flow that exceeds one belt. |
| F-049 | Logistics | Splitter and balancer design | mvp | i was thinking this was a splitter calculator and sometimes i use use one especially if am shipping a part to multiple sites. ie build 240/min and send 75 to x and 100 to Y and store the rest. etc | Given a flow and a desired split, produce the splitter/merger arrangement (manifold, balancer or compressor). |
| F-050 | Logistics | Manifold fill time | skip |  | Estimate how long a manifold takes to saturate all machines after start-up. |
| F-051 | Logistics | Transport capacity planning | shape |  | For an inter-factory route, pick trains, trucks, drones or fluid trucks, enter distance or times, and get vehicles, wagons and stations needed. |
| F-052 | Logistics | Factory-to-factory import/export ledger | mvp |  | Track what each factory sends to and receives from every other factory, and whether the supplier can actually cover it. |
| F-053 | Factory network | Multiple factories per plan | mvp |  | Hold many factories (tabs or cards) in one plan or workspace instead of a single production target. |
| F-054 | Factory network | Nested sub-plans | mvp |  | A recipe or block can contain its own sub-plan (subfloor, nested table, outpost, blueprint) that collapses to a summary. |
| F-055 | Factory network | Factory groups with rollups | shape |  | Group factories into coloured folders whose headers summarise what the group delivers, its power and its problems. |
| F-056 | Factory network | Spin off a sub-chain | mvp |  | From a shortage or an item row, create a new factory or window that plans just that item, linked back as an import. |
| F-057 | Factory network | Plan statistics and building summary | mvp |  | Plan-wide totals: raw resources, every item's production vs consumption, building counts by type, shards and sloops used. |
| F-058 | Factory network | Construction bill of materials | shape |  | Parts needed to build all the machines and generators in a plan. |
| F-059 | Factory network | Plan health warnings | shape |  | Severity-coded warnings: shortage, unmet export, overproduction/backlog, unhandled byproduct, out of sync with game, redundant import. |
| F-060 | Factory network | Space Elevator phase targets | shape |  | Use Space Elevator phase deliverables as plan targets or show what remains for a phase. |
| F-061 | Factory network | Non-producing buildings in plan | mvp |  | Add buildings that make nothing (portals, stations, radar, AWESOME Sink) so their power and consumption (e.g. portal Singularity Cells) count. |
| F-062 | Factory network | AWESOME Sink planning | mvp | the tickets/points are a kind of coin as well. | Route surpluses to sinks and count sink points per minute; sinks draw power. |
| F-063 | Factory network | Dimensional Depot uploads | mvp |  | Model uploads to the Dimensional Depot as a destination, with the MAM-researched upload rate. |
| F-064 | Factory network | Storage buffers in model | skip |  | Model storage containers or fluid buffers as nodes with a fill state that can supply or absorb flow. |
| F-065 | Workflow | Build checklist | later |  | Tick off steps, machines or imports as built in-game, and see when the plan changed after you ticked. |
| F-066 | Workflow | Kanban build status | later |  | Give each factory a status (Draft, Todo, In Progress, Done) and view the megabase on a drag-and-drop board. |
| F-067 | Workflow | Notes and tasks per factory | mvp |  | Free-text notes and a task list attached to a factory. |
| F-068 | Workflow | Plan vs save diff | later |  | Compare a plan with what is actually built in the save: what is missing, what is extra. |
| F-069 | Visualisation | Flow graph with auto layout | mvp |  | Show the plan as nodes (machines or recipes) and edges (item flows) laid out automatically. |
| F-070 | Visualisation | Sankey diagram | skip | i saw factoriolabs version, didn't like it myself. But maybe some people do. if i ship factor this can be a feature request from someone | Show flows as a Sankey diagram, with band width proportional to rate. |
| F-071 | Visualisation | Configurable step table | shape |  | A table of steps with selectable columns (machines, belts, power, inserters, wagons, links), sortable and with precision control. |
| F-072 | Visualisation | Tree view of the chain | later |  | Show the chain as a collapsible hierarchy from target to raw resources. |
| F-073 | Visualisation | Edit from the graph | mvp |  | Change recipe, clock, count or sloops by selecting a node in the graph. |
| F-074 | Visualisation | Persisted manual layout | mvp |  | Node positions you drag are kept across sessions, recalculations and view switches. |
| F-075 | Visualisation | Graph image export | later |  | Export the graph as an image (PNG/SVG) for sharing outside the tool. |
| F-076 | UI | Display units and number format | shape |  | Choose per-second, per-minute or per-hour, and decimal precision or exact rationals. |
| F-077 | UI | Command palette and search | later |  | Global search (Cmd+K) across game data and your own factories, jumping to the matching row. |
| F-078 | UI | Localisation | shape |  | UI strings and item, building and recipe names in many languages. |
| F-079 | UI | Themes and display settings | later |  | Dark/light/system theme, hue, card and text size, interface scale. |
| F-080 | UI | Keyboard shortcuts | mvp |  | Keyboard control for adding, linking, moving and deleting nodes. |
| F-081 | UI | Guided tutorial and demo plans | later | i will say i saw satisfactory logistics demo/walkthrough. if the interface is bad enough you need that i think maybe making a better interface if possible. or incrementally add advanced options | An interactive tutorial and/or prebuilt example plans that show the tool's features. |
| F-082 | UI | In-app feedback with plan attached | skip |  | Send a bug report or idea from inside the app, optionally attaching the plan on screen. |
| F-083 | UI | New-version notice | skip |  | Tell an open tab that a new version is live and offer a reload; refuse saves from a stale client. |
| F-084 | Platform | Installable offline app (PWA) | skip | right, i assumed this was the desktop | Install as an app and run without network once cached (solver, icons and data included). |
| F-085 | Platform | Phone-friendly layout | later |  | A layout designed for phones (one pane at a time, bottom bar), not just a shrunken desktop. |
| F-086 | Platform | Native desktop app | mvp |  | Downloadable desktop application with local files instead of a website. |
| F-087 | Platform | Kiosk / second-screen mode | skip | i run the game in one window and the tools in another today, not sure what this is | A view that rotates through dashboards or follows a player, meant for a side monitor. |
| F-088 | Data | Codex / database browser | mvp |  | Browse items, recipes, buildings, generators, schematics with their stats and descriptions. |
| F-089 | Data | Recipe usage lookup | mvp |  | For an item: every way to make it and everything it goes into. |
| F-090 | Data | Milestone / MAM / AWESOME Shop tracker | mvp | so tiers change what you can build and above we talk about knowing what items we can and cannot use. Seems contradictory | Browse and tick off milestones, MAM research and AWESOME Shop unlocks with their costs. |
| F-091 | Data | Dependency explorer | shape |  | Show what an object requires and what it unlocks, transitively. |
| F-092 | Data | Per-item cost analysis | shape |  | Give every item a cost (e.g. raw resources or logistic actions under optimal recipes) to rank recipes and items. |
| F-093 | Data | Official data ingest pipeline | mvp |  | Generate the tool's data directly from the game's own export (Docs JSON) so updates are mechanical, not hand-entered. |
| F-094 | Data | Game icon extraction | mvp |  | Show real item and building icons, extracted from game assets. |
| F-095 | Map & world | Resource node map | shape |  | An interactive world map of resource nodes, wells and geysers, filterable by resource and purity. |
| F-096 | Map & world | Collectibles map | shape | my primary use case for use case for sat calc is the map with the collectable, i even load my save to see what i missed and where things are. So to me this is core, but it can be after the planning part. | Map of power slugs, hard drives, somersloops, Mercer spheres and drop pods, optionally tracking collected ones. |
| F-097 | Map & world | Build-site ranking | skip |  | Rank candidate sites for a factory by nearby nodes, or pick a build site for a plan. |
| F-098 | Map & world | World seed viewer and finder (1.2) | skip |  | Show node layout for a 1.2 randomised world seed and search seeds for wanted resources at wanted nodes. |
| F-099 | Map & world | Map measuring and annotations | later |  | Measure distances, drop notes or markers, filter by altitude. |
| F-100 | Map & world | 3D factory view | skip |  | Render a factory from the save in 3D or by floor. |
| F-101 | Layout | 2D layout planner | later |  | Place building footprints on a grid (per floor) to design a factory's physical layout. |
| F-102 | Layout | Generated layout or blueprint from a plan | later |  | Turn a solved plan into a physical layout or an importable in-game blueprint. |
| F-103 | Save files | Save upload with map overlay | later |  | Load a save and draw its buildings, belts, pipes, rails and vehicles on the map. |
| F-104 | Save files | Save statistics | later |  | Production and consumption per item, storage contents and game stats computed from a save. |
| F-105 | Save files | Save editing | skip |  | Modify a save and download it: move/copy/delete/rotate selections, recolour, unlock research, edit inventories, spawn miners. |
| F-106 | Save files | Auto-detect factories in a save | skip |  | Cluster a save's machines into named factories (e.g. by belt connectivity). |
| F-107 | Save files | Idle and starved machine detection | skip |  | Find machines that are stopped, starved or blocked, with the reason, and show them as a heatmap. |
| F-108 | Save files | Upstream trace / bottleneck finder | skip |  | From a product in your real factory, trace its supply chain upstream and find the thinnest link. |
| F-109 | Save files | Power circuit analysis | skip |  | List power circuits, their load and capacity, priority-switch break order, fuse-trip risk and unpowered machines. |
| F-110 | Save files | Plan from save state | skip |  | Plan new production using the surplus and unlocks that already exist in your save. |
| F-111 | Save files | Inventory and storage search | skip |  | Find how much of an item you own and which container holds it. |
| F-112 | Server & live | Pull save from a dedicated server | skip |  | Fetch the latest save directly from a dedicated server (HTTPS API with admin password, or SFTP/FTP) instead of uploading by hand. |
| F-113 | Server & live | Server status and admin | skip |  | Show server state (players, tech tier, active milestone, game phase) and run admin actions (save, load, settings, restart). |
| F-114 | Server & live | Live factory telemetry | skip |  | Near-real-time production rates, power, trains, vehicles and player positions from a running game. |
| F-115 | Server & live | Production history | skip |  | Store production and power over time (hours to months) and chart it. |
| F-116 | Server & live | Alerts and notifications | skip |  | Push alerts (e.g. a Discord webhook) on fuse trips, low battery or shortages. |
| F-117 | Server & live | What changed since last visit | skip |  | An overview of what is stuck now and what happened since you last looked. |
| F-118 | Sharing | Programmatic API to plan data | shape |  | Expose plans or factory data to other programs (remote interface, HTTP API, MCP). |
| F-119 | Sharing | Natural-language / LLM interface | shape |  | Ask questions or request plans in plain language and have a model call the planner. |
| F-120 | Platform | In-game planner | skip |  | The planner runs inside the game as a mod UI, with access to live unlock state. |
| F-121 | Platform | In-game throughput instruments | skip |  | Mod buildings or HUDs that measure actual belt throughput and machine efficiency in game. |
| F-122 | Sharing | URL-encoded sharing | later |  | The entire plan is encoded into a link, with no server storage; opening the link reproduces it. |
| F-123 | Sharing | Server-hosted snapshot link | skip |  | Upload a frozen copy of the plan and get a short link; the copy does not change when you keep editing. |
| F-124 | Sharing | Live collaborative editing | skip |  | Several people edit the same plan at once with changes synced live, presence shown and conflicts resolved. |
| F-125 | Sharing | Shared-plan permissions | skip |  | Per-person rights on a shared plan (viewer vs editor; read/write/delete), with revocation. |
| F-126 | Sharing | Accounts and cross-device sync | skip |  | Sign in and have plans follow you across devices. |
| F-127 | Sharing | No account required | skip |  | Full functionality without signing up; data stays in the browser or on disk. |
| F-128 | Sharing | Offline editing with conflict resolution | skip |  | Keep editing a synced plan offline and, on reconnect, see a prompt listing every conflicting change to choose from. |
| F-129 | Sharing | File export and import | mvp | not json please. | Save a plan to a file (JSON or a custom format) and load it back or send it to someone. |
| F-130 | Sharing | Import from another tool | later |  | Read another planner's export format to migrate plans. |
| F-131 | Sharing | Named local saved plans | mvp |  | Keep several named plans or presets in the browser and switch between them. |
| F-132 | Sharing | Community gallery | skip |  | Browse and publish other players' plans or in-game blueprints. |
| F-133 | Sharing | Shared-text safety rules | skip |  | Validate user text in shared plans (no links or markup, length limits) on client and server, and repair old data. |
| F-134 | Platform | Anonymous usage telemetry | skip |  | Count usage (tabs, plan sizes, feature use) without accounts, to know how the tool is used. |
| F-135 | Multi-game | Multiple games in one tool | shape | start with satisfactory | One app with per-game data packs and a game switcher. |
| F-136 | Multi-game | Custom game data editor | later |  | Define an entirely new game's items, recipes and machines inside the tool, then share it. |
| F-137 | Multi-game | Sell value and profit | later |  | Compute what a chain costs to run and what its output sells for. |
| F-138 | Multi-game | Secondary resource budgets | shape |  | Track non-item quantities a chain produces or consumes: heat, nutrients, pollution, net heat value. |
| F-139 | Multi-game | Footprint estimate | shape |  | Estimate the floor area the plan's buildings occupy. |
| F-140 | Multi-game | World seed statistics (non-Satisfactory) | later |  | Query a procedural world seed for resource availability and feed it into the plan. |
| F-141 | Misc | Customisation helpers | later | i use this site every game an manually type them in https://tai-jee.github.io/satisfactory-colour-table/ i'd something like this so i don't have to type, yes it just a time saver. | Colour code converters and palette tools for in-game painting. |
| F-142 | Misc | World leaderboards | skip |  | Compare progress or production across uploaded saves. |
