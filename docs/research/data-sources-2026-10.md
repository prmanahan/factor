# factor: game-data sources beyond the official bundle, and the cross-game data model

Research date 2026-10-05. Builds on `calc-tools.md` and `calc-features.json` in this folder and does not repeat them.

**Labels.** Every claim carries one of three labels.
- **[O] observed:** I read it myself in a primary artefact: a repo file, an API response, a fetched page, or the local bundle in `factor/resources/CommunityResources`.
- **[R] reported:** a third party says it, such as a README, a community dataset, a wiki, or another tool's research notes. Data read from a FactorioLab JSON is [O] *as a property of that dataset* but [R] *as a fact about the game*.
- **[I] inferred:** I reasoned it from evidence and did not check it directly.

Lines marked "search summary" came from a search engine's summary, not a fetched page. Treat them as weaker than [R].

**What the checks covered.**
- GitHub: `gh api` repo metadata, READMEs and trees, plus `gh search code` (GitHub's indexed code only).
- Pages: WebFetch, or curl where WebFetch was blocked.
- Steam: the `appdetails` API for six app ids, and store-page HTML for EULA links.
- Datasets: FactorioLab `public/data/{2.0,spa,sfy,dsp,fdy,tta}/data.json` as of 2026-10-05.
- The local bundle's `Headers/` and `CustomVersions.json`.

Nothing was installed or run against a game install, so every statement about extraction is [R] or [I].

---

## 1. Conclusions first

1. **A Rust Satisfactory save parser already exists and handles 1.2, but its licence is AGPL with a non-transferable permission.** `valentinps/satisfactorymap` is Rust/WASM, a port of GreyHak's GPL-3.0 Python parser, distributed as AGPL-3.0 under written permission that is "non-transferable" and tied to "a client-side, browser-based tool" [O, `NOTICES.md`].
   - **Only one permissive parser claiming 1.2 support turned up:** etothepii4/satisfactory-file-parser (TypeScript, MIT) [O]. The searches behind that were two GitHub repository searches (`satisfactory save language:rust`, `satisfactory sav parser`), a crates.io search for `satisfactory`, and the parser list in `calc-tools.md`.
   - **Its provenance is only partly visible.** `LICENCE.md` reads "Copyright (c) 2021-2025 etothepii" [O]. The repo begins 2024-10-06 with "Initial commit" then "migrate all files", so the history from 2021 to 2024 is not visible [O]. Its README, CHANGELOG and GUIDE contain no credit to SCIM, GreyHak or any other source [O]. "No derivation credit found" is as far as this goes. It does not establish a clean lineage.
   - A Rust port is realistic, since one exists. The MIT parser is the only permissive starting point found [I].
2. **The format documentation is good but sits two save versions behind the bundle.** moritz-h's `docs/SATISFACTORY_SAVE.md` (1,769 lines) says "Document Version: Satisfactory 1.2" and covers chunks, TOC/Data blobs, per-level layout, the property system and blueprints. It was last updated 2026-04-04 for 1.2.0.0, which GreyHak says is save version 58 [O]. The bundle's `SaveCustomVersion.h` ends at **60** [O]. Per their header comments, 59 and 60 are data migrations (pattern-rotation clamp, missing FICSIT materials), so they are probably not wire-format changes [I]. The wiki.gg format page states that the body "has not been analyzed beyond Patch 1.0.0.3" [O].
3. **Node positions, default purity and icons have a proven source: extraction from the user's own install with CUE4Parse/FModel plus the bundle's `.usmap` and `CustomVersions.json`.** Projects that do this keep the output out of their repos [O]. Node purity and position come from the level exports [R satisfactorymap]. Icons come from textures whose paths Docs already lists (750 classes carry `mSmallIcon`) [O], decoded by CUE4Parse [O dax sidecar].
   - **Purity multipliers** are probably extractable from the `FGResourceSettings` asset [I], but I found no project that does it. The values ×0.5 / ×1 / ×2 are [R], via FactorioLab.
   - **Machine port counts *and* positions have no source found.** They are probably in the building blueprints [I].
   - **1.2 adds a twist.** Game modes can randomise node type and purity. Node actors in a save carry `mResourceClassOverride` / `mPurityOverride`, and parsers read them [O: GreyHak `sav_cli.py`, satisfactorymap `world.rs`]. satisfactorymap's Python reference says these are written on the node actors, that it checked this "against a real save with Node Randomization on", and that only Geysers lack them [R, `map/sav_map_data.py` at e5a3092]. I did not test a save myself. If that holds, a static table is right only for the default world, and a randomised world needs save parsing [I].
4. **No published Coffee Stain terms were found that permit or forbid redistributing extracted data or art.** The community modding docs say redistributing extracted assets "should not be done without permission" [O]. The bundle carries no licence [O, prior check]. The satisfactory.wiki.gg text is **CC BY-NC-SA 4.0**, which is non-commercial [O]. This is a decision for Peter, possibly by asking Coffee Stain.
5. **Correction to my earlier survey: Alchemy Factory data is extractable from the game.** `calc-tools.md` inferred that it "ships no official data dump, so recipes are transcribed by hand". In fact the game is UE5 with unencrypted IoStore paks, and its DataTables (`DT_Enemies` = items, `DT_EnemyCrafting` = recipes, `DT_Buildings` with **port cells**) are named the same way by two independent extractor repos [R, PheeZz and Monstrel], and a datamine repo also exists [R]. `calc-tools.md` has been amended in place, with the old claim kept visible as superseded.
6. **Prior art: FactorioLab already has a cross-game vocabulary.** It covers more than ten games with one schema (MIT code). It folds Satisfactory purity, somersloops, DSP proliferator and Foundry robot stations into one "module" facet [O]. Compare Peter's Unit/Formula/Fabricator/GlobalModifiers against it before designing (§6.3).
7. **Distribution and platform are coupled, and nobody has raised it yet.** The "extract from your own install" pattern avoids redistributing game data. But four of the five target games are Windows-only [I]; Factorio has a native macOS build [O]. factor is macOS-first. The extractor itself is probably portable, since CUE4Parse is .NET and AssetRipper is cross-platform [I]. The real constraint is getting the Windows game files onto the Mac. For Alchemy Factory it is worse: the mappings must be dumped from the game while it is running [R]. Oodle decompression is a further dependency (§4).

---

## 2. Q1: Satisfactory save parsing

### 2.1 Parsers

All are GitHub repos read 2026-10-05. "Pushed" is `pushed_at`.

| Parser | Lang | Licence | Pushed | 1.2 support | Notes |
|---|---|---|---|---|---|
| [GreyHak/sat_sav_parse](https://github.com/GreyHak/sat_sav_parse) | Python | GPL-3.0-only [O] | 2026-08-15 | README: "Supports Satisfactory releases v1.2.0.0, v1.2.1.0, v1.2.2.0 and v1.2.2.1" [O] | Read and **write** (resave), a CLI with about 60 operations, blueprints. The reference that the Rust port was checked against. Its `RESOURCE_PURITY` table is credited as "extracted from Anthor's Interactive Map" (SCIM) [O]. |
| [valentinps/satisfactorymap](https://github.com/valentinps/satisfactorymap) `rust_parser/core` | **Rust** (WASM + native) | AGPL-3.0 with GreyHak's scoped permission [O] | 2026-09-13 | Yes (follows GreyHak) [R] | "validated field-by-field against the Python reference with bit-exact differential gates" [O README]. Chunked zlib, optional rayon. A Tauri desktop app (Windows). The 13× speed claim is the **author's own benchmark** [R]. Created 2026-07-02, 7 stars. |
| [etothepii4/satisfactory-file-parser](https://github.com/etothepii4/satisfactory-file-parser) | TypeScript (npm) | **MIT** [O] | 2026-09-13 | README table: "U1.2 ✅ compatible" [O] | Read/write saves and blueprints, streaming JSON. v4.1.0 2026-04-25, with a FicsIt-Networks fix 2026-07-26 [O]. |
| [moritz-h/satisfactory-3d-map](https://github.com/moritz-h/satisfactory-3d-map) `libsave` | C++ | GPL-3.0 [O] | 2026-04-10 | 1.2.0.0 [O commits "update for 1.2.0.0", 2026-03-18/19] | Holds the best format document (below). |
| [Goz3rr/SatisfactorySaveEditor](https://github.com/Goz3rr/SatisfactorySaveEditor) | C# | none stated [O] | 2024-08-17 | No [I, stale] | 305 stars, historical. |
| Small Rust attempts: bananasov/satisfactory-formats (none, 2024-11), gentoid/… (MIT, 2025-01), icdevin/convey-rs (GPL-3.0, 2024-08), backwardspy/… (none, 2024-09), crate `satisfactory-save-file` 0.2.0 (2021) | Rust | as listed [O] | stale | No [I] | Each has 0–2 stars. Not a base. |
| Others: Maurits825 (Go), yvalmor (Kotlin), lordralinc (Python, GPL) | — | — | 2024–2026 | not checked | — |

⚠ **Version currency, unresolved.** GreyHak's README lists 1.2 patches up to 1.2.2.1. My earlier survey called 1.2.4.0 the latest patch, and wiki.gg's Update 1.2 page shows 1.2.2.2 released 2026-06-02 [O]. Whether either parser reads 1.2.4.0 saves was not tested. Only a real save would settle it.

### 2.2 How complete is the format documentation?

| Layer | Bundle headers | moritz-h doc | wiki.gg Save_files |
|---|---|---|---|
| Byte order | not stated | "All binary data is encoded little-endian" [O] | little-endian [O] |
| Header fields and order | struct and version enum only [O] | full binary layout [O] | v13/v14 headers (1.0.0.3, 1.1.1.1) [O] |
| Compressed chunks | no | chunk header layout [O] | magic `0x9E2A83C1`, `0x22222222`, max chunk 131,072, compressed and uncompressed sizes [O] |
| Levels / world partition | partial (`FWorldPartitionValidationData`, etc.) | TOCBlob/DataBlob, `FPerStreamingLevelSaveData`, `FWPGridValidationData` [O ToC] | five grids plus sublevels plus persistent level, **as of 1.0.0.3** [O] |
| Property serialisation | — | every property type, `FPropertyTag`, `FPropertyTypeName` (UE5-style), the binary structs [O ToC] | 19 property types, pre-1.1 [O] |
| Game-specific binary structs | declared | `FInventoryItem`, conveyor items and chain actors, wires, circuits, the lightweight buildable subsystem, vehicles [O ToC] | partial |
| Currency | `SaveVersion` = **60** in `CustomVersions.json` and `SaveCustomVersion.h` [O] | 1.2.0.0 (version 58) [O/R] | "has not been analyzed beyond Patch 1.0.0.3" [O] |

**Licences on the documents themselves.** The moritz doc lives in a GPL-3.0 repo. The wiki text is CC BY-NC-SA 4.0 [O]. Whether *format facts* written from these documents carry the documents' licence is a legal question for Peter, not one I can settle [I].

### 2.3 Is a Rust port realistic?

- **Yes, and it has already been done** [O]: the satisfactorymap port, with differential tests against Python. The open questions are licence and maintenance cost, not feasibility.
- Three routes, each with what it carries [I]:
  - **Depend on or fork `sav_core`.** Carries AGPL-3.0 for factor as a whole. GreyHak's permission is non-transferable, so a fork's standing is unclear.
  - **Port etothepii4 (MIT).** Licence-compatible with a permissive or commercial factor, keeping the MIT notice. This assumes the MIT label reflects clean provenance, and the history before 2024 is not visible (§1). You pay for the port and for tracking each game update, because the TS parser is what moves upstream.
  - **Clean-room from moritz plus the headers.** Possible, but the doc's GPL and NC context needs the legal call above. There is no bit-exact reference you can legally diff against unless GPL tools are used only as test oracles; that too is a legal question.
- **Maintenance is real** [O]: save versions 46 (1.0.0.3), 58 (1.2.0.0) and 60 (bundle) span two years. Each parser ships per-patch fixes.

---

## 3. Q2: the missing Satisfactory data

### 3.1 Gap × source

| Gap | Local install via CUE4Parse/FModel + bundle `.usmap` | Saves | Community datasets |
|---|---|---|---|
| **Purity multipliers** (impure / normal / pure) | Values live in the `FGResourceSettings` asset [O, header in bundle], extractable [I] | Not stored [I] | FactorioLab models purity as a mining "module" with speed −0.5 / 0 / +1, i.e. ×0.5 / ×1 / ×2 [O dataset, R for the game]. Three numbers, widely published. |
| **Node positions and default purity** | Yes. Level exports under `FactoryGame/Map/GameLevel01/` carry `BP_ResourceNode_C` / `BP_FrackingSatellite_C` / `BP_ResourceNodeGeyser_C` with `mResourceClass`, `mPurity` and the world transform. 607 entries, matched 1:1 against the older table [R, satisfactorymap `extract_collectables.py`]. Needs a multi-GB FModel export in three modes [R]. | Positions: node actors appear in saves [O, GreyHak `--find-node`]. Default purity: "not derivable from SAVES" [R satisfactorymap]. | SCIM: **reuse forbidden** [O, from earlier survey]. GreyHak's table is SCIM-derived [O], so it is **tainted for our purposes** [I]. satisfactorymap's tables now regenerate from level exports, but are gitignored and offered only as a release-attached zip "on the same terms as any other extraction" [O]. |
| **1.2 randomised node type and purity** | No. The assets hold only the default [I] | **Very likely.** The properties exist and parsers read and write them: node `mResourceClassOverride` and `mPurityOverride`; game state `mNodeRandomization`, `mNodePuritySettings` and `mNodeRandomizationSeed` [O, GreyHak `sav_cli.py` lines 660–685 and 1048–1056; satisfactorymap `rust_parser/core/src/mapdata/collectors/world.rs` lines 123–143]. That the game writes an override on every non-Geyser node is [R], from satisfactorymap's Python reference: "confirmed against a real save with Node Randomization on: ~75% of nodes' actual mResourceClassOverride disagreed" with the static table. It was not tested by me. The alternative is re-deriving each node from the seed, which nobody has documented. The 1.2 notes list "Default, Random, Basic Resource Rich…" and six purity settings [O wiki.gg Update 1.2]. | Seed viewers exist (satisfactoryworldseed.com, closed) [O earlier survey]. |
| **Collectibles** (slugs, somersloops, mercer spheres, hard drives) | Yes, from the same level exports [R satisfactorymap] | Yes, and state shows what has been collected [O GreyHak CLI] | as above |
| **Resource deposits** | Not useful: "~75% … have no cooked resource type", rolled lazily per save [R satisfactorymap] | per save | — |
| **Machine port counts** | In each building blueprint, as `FGFactoryConnectionComponent` / pipe connection subobjects [I, from the headers' class names]. Docs fields are empty on all 11 manufacturers [O, CLAUDE.md, re-checked: `mFactoryInputConnections: ''`]. | Components are saved, but component headers carry no transform [I, from moritz's `FObjectSaveHeader` vs `FActorSaveHeader` split]. Counts might be read from a built machine's components [I]. | **No dataset found** (§7). The wiki infoboxes list counts [R, not fetched]. |
| **Port positions** | Same blueprints, `RelativeLocation` on the connection components [I]. Not demonstrated by any project I found. | No [I] | none found |
| **Icons** | Yes. Docs gives each texture path, e.g. `Texture2D /Game/FactoryGame/Resource/RawResources/CrudeOil/UI/LiquidOil_Pipe_512…`, on 750 classes [O]. CUE4Parse decodes to PNG: `dax-dot-gay/satisfactory-data/aextract/AExSidecar/Program.cs` does exactly this with `FactoryGame.usmap` plus `CustomVersions.json` [O]. | No | Every tool redistributes icons, but none has a licence for them [I] |

### 3.2 Extraction tooling and terms

| Tool | Lang | Licence | Fit |
|---|---|---|---|
| [CUE4Parse](https://github.com/FabianFG/CUE4Parse) | C# | Apache-2.0 [O] | The proven library. Pushed 2026-10-05. |
| [FModel](https://github.com/4sval/FModel) | C# GUI | GPL-3.0 [O] | Interactive. Windows. |
| [repak](https://github.com/trumank/repak) / [retoc](https://github.com/trumank/retoc) | Rust | Apache-2.0 / MIT [O] | Pak and IoStore containers. retoc converts Zen to legacy [O README]. |
| [unreal_asset](https://github.com/AstroTechies/unrealmodding) | Rust | MIT [O] | uasset parsing. Whether it handles UE 5.6 unversioned properties with `.usmap` is **unproven** [I]. |
| [dax-dot-gay/satisfactory-data](https://github.com/dax-dot-gay/satisfactory-data) | Rust + C# sidecar | MIT [O] | A Rust crate over Docs, with a CUE4Parse sidecar for icons. **1.1-era**: ships `satisfactory-1.1-en-US.zip` and sets `EGame.GAME_UE5_3` [O]. Pushed 2026-05-02. |

- Satisfactory 1.2 setup: "UE Version: `GAME_UE5_6`", custom versions from `CustomVersions.json`, mappings from `FactoryGame.usmap`, container `FactoryGame-Windows.utoc` [R docs.ficsit.app, fetched]. The sidecar also loads an Oodle library (`OodleHelper.Initialize`) [O]. Oodle is Epic/RAD proprietary [I]. Its redistribution terms were not checked.
- **A pure-Rust extraction pipeline for 1.2 is unproven.** CUE4Parse is the proven path, and Rust would mean a C# sidecar or new work [I].

### 3.3 Coffee Stain terms: what exists

| Source | What it says | Label |
|---|---|---|
| docs.ficsit.app, *Extracting Game Files* ([link](https://docs.ficsit.app/satisfactory-modding/latest/Development/ExtractGameFiles.html)) | "As a reminder, redistributing these assets should not be done without permission, as they are copyrighted content of Coffee Stain Studios." | [O]. This is community docs, not Coffee Stain. |
| docs.ficsit.app, *Reusing Game Files* | Reference base-game assets at runtime "since this process does not actually include the game's files in your own." | [O] |
| satisfactory.wiki.gg [Copyrights](https://satisfactory.wiki.gg/wiki/Satisfactory_Wiki:Copyrights) | Wiki content is "CC BY-NC-SA 4.0"; game content is "the intellectual property of their respective owners". | [O] |
| wiki.gg [first-party template](https://satisfactory.wiki.gg/wiki/Template:License/first-party) | Coffee Stain "hold the copyright of Satisfactory". Use of images "is believed to qualify as fair use". | [O]. This is the wiki's own opinion. |
| Steam `legal_notice` (app 526870) | "©2024 Coffee Stain Studios… All rights reserved." | [O] |
| satisfactorygame.com | The links are /press (press kit for "press or a content creator") and /support. No legal, terms or EULA page; `/eula` returns 404. | [O] |
| coffeestain.com (the group site) | Investor/press links only. `/legal` redirects to the home page. | [O] |
| CommunityResources | No licence or readme in any of its 61 entries [O, earlier check]. No patch note or wiki page found that states its terms (Patch 0.3.4.9 checked: no mention) [O]. | — |

**Range:** the two Coffee Stain sites, the Steam API and store HTML, two docs.ficsit pages, three wiki.gg pages and four web searches. **No entry found** for a Coffee Stain fan-content, modding or tool policy. That is an absence in what I could reach, not proof that none exists. The in-game EULA was not readable from here (§7).

A third-party repo, `ficsit/source-data` (stale since 2023), applies Apache-2.0 to the data "that we may lawfully license" [O]. A third party cannot license Coffee Stain's data. Do not treat this as a grant [I].

---

## 4. What each generator needs, and where it can run

| Game | Engine | Generator input | Mappings/schema | Runs where | Redistribution-free option |
|---|---|---|---|---|---|
| Satisfactory | UE 5.6 [R] | Docs JSON (shipped) plus paks for nodes, ports and icons | `FactoryGame.usmap` is **shipped in the bundle** [O] | Docs: anywhere. Paks: the game is Windows-only [I]; Oodle needed [O] | Docs only, without nodes, ports or icons, or the user extracts |
| Factorio | own engine | `factorio --dump-data`, `--dump-icon-sprites`, `--dump-prototype-locale` [O wiki] | `data-raw-dump.json` | **Native macOS build exists** [O, FactorioLab `factorio-dump-mac.sh`] | Lua prototypes are public at [wube/factorio-data](https://github.com/wube/factorio-data), but turning them into `data.raw` needs a Lua run [I] |
| Techtonica | Unity, **stripped TypeTrees** [R rhys-ender] | AssetRipper export → YAML ScriptableObjects (`craftingMethod`, `craftTierRequired`, `duration`, `ingTypes`/`ingQuantities`, …) [R] | none needed via AssetRipper [R] | AssetRipper is cross-platform [I]; the game is Windows [I] | user extracts |
| FOUNDRY | Unity [R search summary] | No dump found. The game's own types, as a mod references them, are `ItemTemplate`, `ElementTemplate`, `CraftingRecipe`, `BuildableObjectTemplate`, `BlastFurnaceModeTemplate` and `HotAirTemplate`, with fixed-point fields such as `energyConsumptionKW_fpm` and `speedBonus_fpm` [O, erkle64 `PlanIt/Scripts/ItemElementRecipe.cs`]. A dumper mod running in the game could export them [I]. | — | Windows, inside the running game [I] | user extracts |
| Alchemy Factory | UE5. "5.7" per one README [R Monstrel], but "only UE5 confirmed" per another [R PheeZz]: **unresolved** | IoStore paks, unencrypted, Oodle [R] | **No shipped mappings.** Must dump `.usmap` via UE4SS, or `.jmap` via jmap_dumper, **from the running game** [R]. A public pre-1.0 usmap "silently" yields empty rows [R PheeZz]. | Windows with the game running [R] | user extracts, or unlicensed datamines |
| DSP | Unity, BepInEx mods [R] | Community JSON mirroring the game's `RecipeProto` fields (`Items`, `ItemCounts`, `Results`, `ResultCounts`, `TimeSpend` in ticks) [O dsp-calc `Vanilla.json`] | — | — | user extracts |

---

## 5. Q3: the other games' data and terms

### Factorio
- **Exposure [O].** Wube publishes the Lua prototypes at [wube/factorio-data](https://github.com/wube/factorio-data), updated per release (2.1.20 on 2026-09-22). The README lists "Online references, cheat sheets, and calculators" as a use case. There is no licence file (`license: none`). `--dump-data` writes `data.raw` as JSON [O wiki]. Prototype API docs: lua-api.factorio.com, version 2.1.20 [O].
- **2.1 change [O].** Products now have `probability`, `independent_probability` and `shared_probability` (a min/max range on one shared roll). Uranium processing is `shared_probability = { min = 0, max = 0.007 }` in `base/prototypes/recipe.lua`. Recipes use `categories = {...}` (plural).
- **Terms, [Factorio ToS](https://factorio.com/terms-of-service), fetched, no date on the page [O]:**
  - "Distribution of the original art assets such as models, fonts or textures is not permitted, unless it is necessary to create your own mods in accordance with the previous paragraphs."
  - "Any commercial use of the Factorio source code, art assets or other affiliated assets is subject to express consent of Wube Software Ltd. For this purpose you can contact us on factorio@factorio.com."
  - The licence is for "personal, non-commercial use".
  - A forum line, "cannot allow any 3rd party project use any of our game art assets", is **search summary only** and was not fetched.

### Techtonica (Fire Hose Games; 1.0 released 2024-11-07 [O Steam])
- **Exposure:** no official dump. Two routes:
  - AssetRipper export of ScriptableObjects [R rhys-ender, GPL-3.0, gitignores all game data].
  - BepInEx mods via Thunderstore ([TechtonicaModdingResources](https://github.com/CubeSuite/TechtonicaModdingResources)) [R search summary].
- **FactorioLab's `tta` dataset is version "0.2"** [O], which predates 1.0. A 2026-01 issue reports a v1 update that was never merged [O, #1783].
- **Terms:** Steam `legal_notice` "©2024 Fire Hose Games, Inc. All Rights Reserved" [O]. No EULA link on the store page [O]. Mod pages carry "Techtonica Devs do not provide support for Mods" [R search summary]. **No data or asset policy found.**

### FOUNDRY (Channel 3 Entertainment, published by Paradox; Early Access since 2024-05-02 [O Steam])
- **Exposure:** Unity with community mods (erkle64's **UnFoundry** loader and the **PlanIt** in-game planner, MIT) [O repo tree].
  - PlanIt reads the game's runtime objects directly [O]:
    - `ItemTemplate` and `ElementTemplate`, so items and fluids/gases are separate types;
    - `CraftingRecipe`;
    - `BuildableObjectTemplate`;
    - `BlastFurnaceModeTemplate`;
    - `HotAirTemplate`;
    - fixed-point fields: `energyConsumptionKW_fpm`, `speedBonus_fpm`, `resourceConverter_speedBonusModules`, `transferRatePerSecond_liter`.
  - So the practical route is a dumper mod that runs in the game [I]. None was found.
  - How the FactorioLab `fdy` dataset was produced is undocumented (§7).
- **Terms [O, Paradox User Agreement](https://legal.paradoxplaza.com/eula?locale=en), linked from the Steam EULA:**
  - "We hereby grant you the right to create, enjoy and make publicly available UGC, for non-commercial purposes."
  - "'UGC' includes for example … scripts and programs, mods …"
  - UGC "shall be provided for free … but you may accept donations … or through sponsorships."
  - "We are not always the owner of the intellectual property for a Game and therefore, we cannot unconditionally allow UGC to all Games."
  - FOUNDRY's IP is Channel 3's per the Steam `legal_notice` [O], so Paradox's grant may not cover it [I].

### Alchemy Factory (D5 Copperhead / Gamirror Games; 1.0 on 2026-09-08 [R]; Steam release field says 7 Sep 2026 [O])
- **Exposure:** extractable DataTables, as in conclusion 5 [R ×2].
- **Datasets, all unlicensed** [R PheeZz `02-data-sources.md`]:
  - faultyd3v/AlchemyFactoryData (datamine, no licence);
  - starfi5h calculator DB ("Fork freely" is not a licence);
  - alchemy-factory-codex.com: "large-scale reuse requires permission", and its data is pre-1.0.
  - PheeZz is AI-assisted (its `docs/superpowers` plans) and says "Game names and icons belong to their owners."
- **Terms:** Steam `legal_notice`: none [O]. No EULA link on the store page [O]. **No policy found.**

### Dyson Sphere Program (Youthcat Studio / Gamirror Games)
- **Exposure:** BepInEx. Community JSON mirroring the `RecipeProto` fields (DSPCalculator/dsp-calc, MulanPSL-2.0 code) [O].
- The dsp-wiki rules for publishing modding info: "DO NOT upload any original game assets that are not released in the game itself", and "DO NOT share any original game source code obtained by decompiling" [O, wikitext via API]. These are **the wiki's rules**, not a Youthcat statement.
- **Terms:** Steam `legal_notice`: none [O]. **No policy found.**

**Instrument control.** One store-HTML grep found an EULA link for FOUNDRY (the control hit) and for Dinkum, and none for the other five [O]. `appdetails.legal_notice` returned text for 4 of 6 [O].

---

## 6. Q4: the cross-game data model

### 6.1 Matrix

Key: **C** = common shape across games. **S** = same shape, different numbers or units. **U** = unique to one game (or two).

| Concept | Satisfactory | Factorio (2.x) | Techtonica | FOUNDRY | Alchemy Factory | DSP | Class [I] |
|---|---|---|---|---|---|---|---|
| Items vs fluids | `mForm` solid/liquid/gas; fluid in m³/1000 [O] | separate fluid prototypes; fluid **temperature** variants, e.g. `steam-500` [O dataset] | no fluids in the 0.2 dataset [O]; 1.0 not checked | items + fluids [O dataset] | `liquid` flag [R] | fluids ride belts; no fluid carrier in the dataset [O] | **S**; temperature is **U** (Factorio) |
| Multi-output recipes | 37/296 [O dataset] | 12/403 base, 237/902 Space Age (recycling) [O] | 10/225 [O] | 10/371 [O] | `sideProduct`, nursery dual output [R] | 6/493 [O] | **C** |
| Probabilistic outputs | none [I] | `probability` / independent / shared (2.1) [O] | none [O dataset] | fractional outputs on 11 seed recipes [O dataset] | `failRate1/2` + `failProduct` [R] | fractional (fractionation, gas giants) [O dataset] | **S**: reduces to expected value for steady state [I] |
| Catalysts (input ∩ output) | 3 recipes [O dataset] | `catalyst` / `ignored_by_productivity` [O] | 0 [O] | 11 [O dataset] | catalyst **charges** (`catalystCharges`, `CatalystCost`) [R] | 2 [O dataset] | **C**; consumable charges are **U** (AF) |
| Recipe set enumerable | yes | yes | yes | yes | **no**: cauldron recipes are value-based, 447,580 triples [R alchemyfactorytools] | yes | **U** (AF) |
| Batch / time encoding | seconds [O] | seconds (`energy_required`) [O] | seconds [R] | seconds [O dataset] | `qty × fractionNum`, `craftTime × fractionNum` [R] | **ticks** (`TimeSpend` 60 = 1 s) [O] | **S**: normalise at import |
| Machine speed | speed 1 per machine; extractors vary (Miner Mk.3 ×4) [O dataset] | `crafting_speed` per machine [O] | per tier (drills 0.4167 / 0.625 / 2) [O dataset] | per machine [O dataset] | not in the dump; e.g. Enhanced Grinder ×2 [R] | tiers 0.75 / 1 / 1.5 / 3 [O dataset] | **S** |
| Recipe→machine binding | `mProducedIn` [O] | crafting **categories** [O] | `craftingMethod` + `craftTierRequired` [R] | producers [O dataset] | `craftType` enum (25 values) [R] | `Factories` list [O] | **S** (direct list vs category) |
| Per-machine modifiers | shards → clock 0–250% [I]; **somersloop** slots (Manufacturer 4, Smelter 1) doubling output [O dataset] | modules, **beacons**, **quality** [O] | none in dataset [O] | **Robot Station**: one per building, robots act as speed/consumption modules, with Xeno Power Core variants [R PR #1887] | none found | **proliferator**: a consumed spray item, products **or** speed mode, recipe-restricted [O dataset] | **S** (modules); quality is **U** (Factorio); proliferator is an **input**, not a slot |
| Global modifiers | 1.2 game-mode multipliers: recipe parts 0.25–2×, power 0.25–5×, elevator [R wiki]; **32 recipes exempt** (`noCostMultiplier`) [O dataset] | research: mining productivity, recipe productivity, belt stack [O dataset] | research: Smelting 133/167%, Assembling 125/150%, MDR 160/240%, electricity output 110–130% [R fandom wikitext, which itself says values need updating for 1.0] | none observed | `DT_Attributes`: ConveyerSpeed 60, FactorySpeed 100, FuelEfficiency, FertilizerEfficiency… [R] | research: mining speed (vein utilisation) [O flag] | **C**, with per-recipe exemptions |
| Power draw curve | `base × clock^1.321929`; boost exponent 2.0 [O Docs] | linear in module consumption % + drain [O] | fixed kW [R] | linear module consumption % [O dataset] | **no electricity**; heat speed per device × FactorySpeed [R] | linear + idle **drain** [O] | **S**; nonlinear is **U** (SF) |
| Power generation and fuels | fuel generators with `mFuel` and supplemental water, nuclear (waste), geothermal [O] | boiler → steam (temperature) → engine/turbine; burner fuel categories [O] | burner (bio, explosive fuel types) + electric [O dataset] | reactor and steam chains modelled as recipes [O dataset] | **heat**: furnaces with slots and adjacency, fuels have heat value [R] | thermal/fuel, wind, solar (location-dependent [I]), geothermal [O dataset] | **S**: "power" generalises to a per-game utility resource; AF's heat is the outlier |
| Extraction | node × purity (0.5/1/2) × miner tier × clock; wells; 1.2 randomisation [O/R] | resource patch, `mining_time`, depletion, infinite yield, mining-productivity research [O flags] | drill tiers on veins [O dataset] | drone miners; **fracking** with liquid input [O dataset] | mostly **bought** via Purchasing Portal with money; nursery growth with nutrients [R] | veins, oil seeps, orbital collectors [O dataset] | **S**: "extraction is a recipe with no inputs" holds for 5 of 6 [O FactorioLab] |
| Continuous carriers | belts Mk.1–6 = 1, 2, 4.5, 8, 13, 20 /s; pipes 5 / 10 m³/s [O dataset] | belts 15 / 30 / 45 /s; belt stacking (SA) [O] | belts 4 / 8 / 12 [O dataset] | conveyors 2.67–21.33 /s; pipe 600, pipeline 6000 [O dataset] | belt rate is **global** (`ConveyerSpeed`) [R] | belts 6 / 12 / 30 /s + stacking [O] | **S**; a fixed cap per tier breaks for AF and for stacking |
| Route carriers | train, truck, drone (slots) [O CLAUDE.md] | wagons **40 stacks** / 50,000 fluid; bots; platforms [O dataset] | monorail [R] | train **16 stacks** / 23,000; shuttle **4 stacks** / 10,000 [O dataset] | rails and wagons, new in 1.0 (`DT_Railroads`, `DT_Trolleys`) [R] | stations, drones, vessels (not modelled as carriers in FactorioLab) [O] | **C**: capacity in stacks supports the slot × stack proposal |
| Research / unlock | one-off item costs (milestones, MAM, AWESOME, hard drives) [O] | technologies as **rate-able** lab recipes [O dataset] | research cores accumulated, plus terminal tiers paid in items [R] | not checked | skill tree with research points and licences [R] | matrix hashes in labs, as recipes [O dataset] | **S**: an unlock graph is common; rate-able vs one-off is the split |
| Port / footprint data | footprint only (`mClearanceData`), ports empty [O] | `size` [O dataset] | `dimensions` [R] | `size` [O dataset] | **`GridConfigList` cells + `InOutList` ports (side, in/out, pipe)** [R, one source] | not checked | footprint **C**; ports usually missing |
| Economy | sink points [O] | — | — | — | money, buy/sell prices, contracts, profit [R] | — | **U** (AF) |

### 6.2 Where Peter's vocabulary holds and where it breaks

| Term | Holds | Breaks or strains |
|---|---|---|
| **Unit** (item or fluid) | All six: one identity, with a form flag [O/R]. Peter's "fluids are ordinary items" fits every game in the steady-state maths [I]. | Factorio fluid **temperature** makes `steam` at different temperatures into distinct units [O]. AF **heat** and **nutrient** are pooled quantities, not items [R]: they could be modelled as Units with no carrier [I]. |
| **Formula** | Inputs → outputs over a cycle time, with multiple outputs, fits all six [O]. Probability reduces to expected value [I]. | **AF cauldron**: value-based and combinatorial, so it cannot be enumerated statically [R]. **FractionNum** batches and **catalyst charges** need a normalisation step [R]. DSP ticks need unit conversion [O]. **Recipe-level flags** are needed: exempt from cost multiplier [O sfy], allowed effects / proliferator modes [O dsp, Factorio]. |
| **Fabricator** (speed, power) | Every game has machines with a speed scalar and a power or energy draw [O]. | **Slots** are part of the machine: somersloop slots, module slots, one Robot Station, furnace heat slots [O/R]. The power **curve** is per game [O]. **Tier-gated binding** (`craftTierRequired`) and category binding vary [R/O]. |
| **GlobalModifiers** | SF 1.2 game modes, Techtonica research, AF `DT_Attributes`, Factorio research productivity [O/R]. | (1) Needs **per-recipe exemptions** [O]. (2) Most modifiers are **per machine instance**, not global: shards, somersloops, modules, beacons, robot stations [O]. (3) The DSP proliferator is a **consumed input** with modes, so it is a Formula transform, not a scalar [O]. (4) Some affect **carriers** (AF belt speed, belt stacking) or **fuel value** (AF FuelEfficiency) [R/O], not only machines. |
| *(missing)* Carrier | — | Already split out by Peter's transport ruling. The evidence supports slot × stack capacity [O] and a global rate multiplier on continuous carriers [R]. |
| *(missing)* Extractor / Source | Five of six model extraction as a no-input Formula on a site with a multiplier (purity, yield) [O FactorioLab]. | AF raw input is **purchase with money** [R]. The SF 1.2 per-save site assignment lives in the save: the properties are [O], and that every node is written is [R]. |
| *(missing)* Unlock | — | Every game has an unlock graph [O/R]. Whether research is a **rate** (Factorio, DSP) or a **one-off cost** (SF, Techtonica) differs. |

### 6.3 Prior art: the FactorioLab schema [O, MIT code]

- **Items carry optional facets:** `belt{speed,itemTypes}`, `wagon{capacity,capacityType:'stacks'|…}`, `machine{speed,type,usage,drain,modules,size,fuelTypes,disallowedEffects}`, `module{speed,productivity,consumption,quality,limitation,sprays}`, `beacon`, `fuel{value,types}` and `technology{prerequisites,recipeUnlock}`.
- **Recipes:** `{time, in, out, producers, catalyst, cost, usage, flags}`.
- **Game behaviour is switched by per-game `flags`.** Satisfactory has `overclock`, `somersloop`, `resourcePurity`, `recipeCostMultiplier` and `consumptionAsDrain`. DSP has `proliferator`, `beltStack` and `miningSpeed`.
- **What it shows [I]:** one schema can cover all these games if machine modifiers are a slot-and-facet concept and game-specific maths sits behind flags.
- **What it lacks:**
  - Probability is flattened to expected values (uranium 0.007 / 0.993) [O].
  - No ports.
  - No AF cauldron.
  - Non-Factorio data is hand-curated and goes stale (Techtonica "0.2") [O].

### 6.4 The cross-game core the evidence supports [I]

**Rule for admission:** a concept is in the core only if the §6.1 matrix shows it in at least five of the six games, and each of those cells is [O], or [R] from two independent sources. Everything else is a per-game extension behind a flag or plug-in. This states the evidence. It is not a design; decision #8 stays with Peter.

**In the core:**

1. **A Unit with a form tag** (solid / fluid, and gas for SF). Present in six of six [O/R]. Steady-state maths treats every form the same.
2. **A Formula** = inputs → outputs over a cycle time, with multiple outputs and catalyst-style input∩output allowed. Six of six [O dataset ×5, R AF]. Times are normalised to seconds at import; DSP uses ticks and AF uses `fractionNum` [O/R].
3. **Probabilistic outputs reduced to expected rates.** Explicit in FA, AF and DSP, and fractional in FO [O/R]. For a planner, expected value is enough [I]. Keep the raw form only for display.
4. **A Fabricator with a speed scalar and a list of Formulas it may run.** Six of six [O/R]. Binding is either a direct producer list or a category; normalise to the list at import [I].
5. **Extraction as a no-input Formula, scaled by a site multiplier.** Five of six: SF, FA, TT, FO, DSP [O FactorioLab]. AF is the exception, because its raw input is bought.
6. **Two families of transport carrier.**
   - Continuous: a rate per tier. Six of six [O/R].
   - Route: capacity as slots × stack size. SF, FA and FO are [O]; TT and AF are [R].
   - This supports Peter's open proposal. A global multiplier on continuous carriers is needed for AF and for stacking [O/R].
7. **Global modifiers, with per-recipe exemptions.** Present in SF, FA, TT, AF and DSP [O/R]; FO has none observed. The exemption set is [O] in SF (`noCostMultiplier`, 32 recipes).
8. **An energy or utility draw per Fabricator, with generators modelled as Formulas.** Six of six, but the curve is per game:
   - SF: exponent [O];
   - FA, DSP, FO: linear percentage plus drain [O];
   - AF: heat rather than electricity [R].
   - The core is "a Fabricator consumes a utility Unit at a rate set by a per-game function" [I].
9. **An unlock graph** over Formulas and Fabricators. Six of six [O/R]. Whether research is a rate or a one-off cost is per game.

**Not in the core (per-game extensions):**
- Somersloop, shards and the SF nonlinear curve.
- Modules, beacons and quality (FA).
- Proliferator, a consumed spray (DSP).
- Robot Station (FO).
- Cauldron value-recipes, catalyst charges, heat adjacency, nutrients and money (AF).
- Fluid temperature (FA).
- 1.2 node randomisation (SF).

The shared shape among the first four is "a per-machine-instance slot that holds a modifier". That gives four of six games [O/R], one short of the bar. It is a strong candidate for a *core extension point* rather than core data [I].

---

## 7. Could not verify, and what I tried

| Item | What I tried | Result |
|---|---|---|
| Coffee Stain fan, modding or data terms; CommunityResources terms | coffeestain.com and satisfactorygame.com links, `/eula`, Steam API and store HTML, wiki.gg Copyrights and template, docs.ficsit (2 pages), 4 web searches, Patch 0.3.4.9 notes | **No entry found.** The in-game EULA is shown at launch and was not readable here. **Route to Peter.** |
| Satisfactory port counts or positions in any dataset | `gh search code 'FGFactoryConnectionComponent RelativeLocation'` (0 hits); `'FGFactoryConnectionComponent'` (headers only); control `'mManufactoringDuration'` returned hits, so the instrument works; read the architect FModel processor | **No entry found** in indexed GitHub code. Blueprint-CDO positions are [I]. |
| FOUNDRY extraction route and data provenance | wiki.foundry-game.com page (404) and its API (non-JSON); 4 GitHub searches; FactorioLab PR #1887 body; erkle64 PlanIt source | The in-game type names are now [O] (§4). No dumper and no dataset provenance found. The PR describes mechanics, not the source. |
| Whether the game writes a node override for *every* randomised node, or re-derives some from the seed | read GreyHak `sav_cli.py`, satisfactorymap `world.rs` and its deleted Python reference | Reported "confirmed against a real save" by satisfactorymap's author. **Not tested by me**: needs a randomised save. |
| etothepii4 parser lineage before 2024-10-06 | LICENCE, README, CHANGELOG, GUIDE, first commits | The history was migrated in and is not visible. No credit to another source was found. |
| Rust UE 5.6 asset pipeline | read repak/retoc/unreal_asset READMEs | Unproven. Not run. |
| Parser support for patch 1.2.4.0 | READMEs only | Untested. Needs a real save. |
| Techtonica 1.0 numbers | fandom wikitext via API (wiki.gg blocked curl) | The wiki says values need updating for 1.0. The search summary said "125%" where the wikitext says "133%". |
| Alchemy Factory UE minor version | two READMEs disagree (5.7 vs "UE5 only confirmed") | Unresolved, shown as conflict. |
| Oodle licence for an extraction pipeline | not attempted | Open. |

---

## 8. Decisions this leaves for Peter (not made here)

1. **Licence of factor, given the parser lineage.** AGPL (lets you build on `sav_core` and GreyHak), or permissive/commercial (port the MIT etothepii4 parser, or write a clean-room parser from the docs). Commercialisation possibly being on the table pushes toward the second; it is his call.
2. **Game data distribution model, per game.**
   - (a) Ship generated data files.
   - (b) Ship only generators that users run against their own install.
   - (c) Ship nothing and ask the publishers.

   **(b) is the pattern every careful open project here uses** [O: satisfactorymap, rhys-ender, PheeZz, dax]. But (b) means a macOS user without a Windows install cannot generate data (§4).
3. **Whether to ask Coffee Stain** (and Wube, whose ToS says commercial use of assets needs "express consent") before any commercial release. If so, what to ask: data, icons, or both.
4. **Icons:** ship, user-extract, or use none (text and colour) for an open-source or commercial build.
5. **Satisfactory 1.2 randomised worlds:** support them, or support only the default world from a static table. Supporting them means reading per-node overrides from the save. That depends on the [R] claim that the game writes them for every node; if it does not, the alternative is reimplementing the seeded roll, which is undocumented. Verify on a randomised save before committing.
6. **Which community datasets are acceptable inputs.** Several are unlicensed or reuse-restricted: SCIM; GreyHak's SCIM-derived purity table; every Alchemy Factory dataset; alchemy-factory-codex.
7. **Wiki-sourced numbers:** satisfactory.wiki.gg is **NC**, which matters if any number or text is copied.
8. **Model scope**, an architecture decision rather than a licensing one:
   - adopt FactorioLab-style per-machine slots/facets plus per-game flags;
   - decide whether the AF cauldron is in scope;
   - decide whether "power" becomes a per-game utility resource (electricity, heat).

---

## Sources

- Parsers and docs: [GreyHak/sat_sav_parse](https://github.com/GreyHak/sat_sav_parse) · [valentinps/satisfactorymap](https://github.com/valentinps/satisfactorymap) (`NOTICES.md`, `game_data/README.md`, `game_data/extractors/extract_collectables.py`, `rust_parser/README.md`) · [etothepii4/satisfactory-file-parser](https://github.com/etothepii4/satisfactory-file-parser) · [moritz-h/satisfactory-3d-map `docs/SATISFACTORY_SAVE.md`](https://github.com/moritz-h/satisfactory-3d-map/blob/master/docs/SATISFACTORY_SAVE.md) · [wiki.gg Save files](https://satisfactory.wiki.gg/wiki/Save_files) · [wiki.gg Update 1.2](https://satisfactory.wiki.gg/wiki/Update_1.2)
- Extraction: [docs.ficsit.app Extract Game Files](https://docs.ficsit.app/satisfactory-modding/latest/Development/ExtractGameFiles.html) · [Reuse Game Files](https://docs.ficsit.app/satisfactory-modding/latest/Development/ReuseGameFiles.html) · [CUE4Parse](https://github.com/FabianFG/CUE4Parse) · [FModel](https://github.com/4sval/FModel) · [repak](https://github.com/trumank/repak) · [retoc](https://github.com/trumank/retoc) · [unrealmodding](https://github.com/AstroTechies/unrealmodding) · [dax-dot-gay/satisfactory-data](https://github.com/dax-dot-gay/satisfactory-data)
- Terms: [wiki.gg Copyrights](https://satisfactory.wiki.gg/wiki/Satisfactory_Wiki:Copyrights) · [wiki.gg first-party template](https://satisfactory.wiki.gg/wiki/Template:License/first-party) · [satisfactorygame.com/press](https://www.satisfactorygame.com/press) · [Factorio ToS](https://factorio.com/terms-of-service) · [Paradox User Agreement](https://legal.paradoxplaza.com/eula?locale=en) · [dsp-wiki Modding](https://dsp-wiki.com/Modding:Modding) · Steam `appdetails` for 526870, 427520, 1457320, 983870, 3669570, 1366540
- Other games: [wube/factorio-data](https://github.com/wube/factorio-data) · [Factorio prototype docs 2.1.20](https://lua-api.factorio.com/latest/types/ItemProductPrototype.html) · [Factorio command-line parameters](https://wiki.factorio.com/Command_line_parameters) · [rhys-ender/techtonica-calculator](https://github.com/rhys-ender/techtonica-calculator) · [techtonica.fandom Synthesis](https://techtonica.fandom.com/wiki/Synthesis) / [Terraforming](https://techtonica.fandom.com/wiki/Terraforming) / [Technology Research](https://techtonica.fandom.com/wiki/Technology_Research) · [CubeSuite/TechtonicaModdingResources](https://github.com/CubeSuite/TechtonicaModdingResources) · [erkle64/FoundryMods](https://github.com/erkle64/FoundryMods) · [PheeZz/alchemy-factory-calculator](https://github.com/PheeZz/alchemy-factory-calculator) (`research/01`, `02`, `04`) · [Monstrel/yaafc](https://github.com/Monstrel/yaafc) · [alchemyfactorytools](https://github.com/alchemyfactorytools/alchemyfactorytools.github.io) · [DSPCalculator/dsp-calc](https://github.com/DSPCalculator/dsp-calc)
- Cross-game: [factoriolab/factoriolab `public/data`](https://github.com/factoriolab/factoriolab/tree/main/public/data) · [PR #1887](https://github.com/factoriolab/factoriolab/pull/1887) · [issue #1783](https://github.com/factoriolab/factoriolab/issues/1783)
- Local: `factor/resources/CommunityResources/CustomVersions.json`, `Headers/Source/FactoryGame/Public/SaveCustomVersion.h`, `FGSaveManagerInterface.h`
