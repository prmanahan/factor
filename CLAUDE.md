# factor

A production calculator for factory games. It has two core jobs: diagramming factories, and
calculating plans that stay correct and responsive on large factories. Satisfactory Modeler is the
benchmark it has to beat. Hobby project.

## Decisions

**`docs/decisions.md` holds every design decision and open question.** Each block has a stable
`D-NNN` id, Peter's words verbatim, the options considered, and a status. Read it before designing
anything. Add new questions there, never inline here. This section lists only the **ruled** outcomes:

- **Platform (D-001):** Rust desktop app first. macOS now, Windows later, so nothing may rule Windows out.
- **Desktop first (D-030):** no server side and no accounts in the first build. They are deferred, not ruled out.
- **Shape what is hard to retrofit (D-031):** a concern that is expensive to add later gets a minimal internal
  accommodation now. Globalisation and tenancy are the named examples.
- **Graphics are a view (D-032):** the drawing is separate from the backend and replaceable, possibly with a
  web view later.
- **Multi-game (D-002):** the core is game-neutral, and Satisfactory is the first game, not the
  template. Games in scope: Satisfactory, Factorio, Techtonica, Foundry, Alchemy Factory.
- **Data pipeline (D-003):** each game gets a generator that emits data files. The app loads them at
  runtime into a typed Rust model, with validation at load.
- **Raw bundle out of git (D-004):** see `resources/` below.
- **Planning, not simulation (D-005):** steady-state rates at full capacity. Fluids are ordinary
  items, and only throughput matters.
- **Transport is a generic carrier concept (D-006):** each game supplies its own types, each with a cap.
- **Power and modifiers follow per-game curves (D-007), and clocks are continuous and exact (D-008):**
  load is spread evenly across whole machines, and clock values are ones the game accepts, to 4
  decimal places.
- **Calculation is separate from layout and drawing (D-009).** D-032 extends this: the drawing is a replaceable view.
- **Tracking (D-010):** decisions go in `docs/decisions.md`, and work goes in brain project `factor` (id 40).

## Layout and vocabulary (D-011, applied)

These come from Peter's earlier attempt at `~/work/repos/factory_calc`; the code itself wasn't
carried over.

- **Layout:** a Cargo workspace with binaries in `cmd/`, libraries in `libs/`, and no `src/`
  directories. Rust 2024 edition.
- **Vocabulary:**
  - `Unit`: an item or fluid.
  - `Formula`: a recipe.
  - `Fabricator`: a machine type.
  - `GlobalModifiers`: game-wide multipliers.
  - ⚠ The cross-game research found `Formula` and `GlobalModifiers` don't hold as they stand. See
    D-029 before using either.
- **All code work happens in a worktree.**
  - Research briefs and benchmarks live in `docs/research/`.
  - Agent memory under `.claude/agent-memory/` is local only: Peter's global gitignore excludes it, and `git worktree remove` silently deletes ignored files. Copy any agent memory written in a worktree to the main checkout before tearing that worktree down.

## resources/ — Satisfactory CommunityResources

Coffee Stain's community resource bundle, which ships with the game for modders and tool-builders.
Peter describes it as game information "we are permitted to use". The archive contains no licence or
readme (checked: all 61 archive entries), so the terms of **redistribution** are unverified.

**⛔ The raw bundle is not tracked in git**, by Peter's ruling of 2026-10-05: redistribution terms are
unverified and the bundle is 585 MB. `.gitignore` excludes the zip and the expanded tree.
- **Fresh clone:** copy `CommunityResources.zip` from the game install's `CommunityResources` folder
  into `resources/` and expand it as shown below.
- **What to commit instead:** a small extract derived from the bundle, once the calculator produces one.

```
resources/
  CommunityResources.zip          original archive, kept as delivered
  CommunityResources/             expanded from it
    Docs/<locale>.json            game data, one file per locale (55 files, ~10 MB each)
    CustomVersions.json           Unreal custom-version GUIDs with their current numbers (89 entries)
    FactoryGame.usmap             unversioned-property mappings (binary)
    DedicatedServerAPIDocs.md     Dedicated Server query API + HTTPS API reference
    Headers.zip                   nested archive, as delivered
    Headers/                      expanded from Headers.zip by us (NOT part of the archive's layout)
```

**Refreshing from a new game build takes two unzips:** the outer archive, then `Headers.zip` into `Headers/`.
The file dates are the only version marker: data files 2026-08-12, server API doc 2025-10-27. The
archive names no game version anywhere. `CustomVersions.json` has `Release` = 44. The data is
probably **game version 1.2** (released 2026-06-02). That comes from the 2026-10-05 tool survey, not
from the archive: Docs contains the Fluid Truck Station and the Pipeline T-Junction, which the survey
says are new in 1.2. The Fluid Truck Station's presence was confirmed; its newness was not.

### Docs/*.json — the game data (what the calculator runs on)

- **Shape:** a top-level array of 114 groups `{ "NativeClass": "...FactoryGame.FGRecipe'", "Classes": [ ... ] }`.
  Each class is a flat object keyed by `ClassName` (e.g. `Recipe_IngotIron_C`), with 2,868 classes in total.
- **Use `en-US.json` for numbers.** Measured against `de.json`: same 2,868 class names, and the only
  fields that differ are display text (`mDisplayName`, `mDescription`, `mAbbreviatedDisplayName`, unlock
  and UI strings). The other locales are localisation tables over the same data. `en-US`, `af`, `hi`, `vun`,
  `en-AE` and `en-AU` are byte-identical, so they are untranslated fallbacks. That covers only the six
  files hashed, not a census of all 55.
- **⚠ Encoding varies per file, so detect it per file (measured):**
  - Most Docs files are UTF-16LE with a BOM and CRLF line endings.
  - `io.json` is UTF-8 with a BOM.
  - `CustomVersions.json` is UTF-16LE **without** a BOM.
- **⚠ Values are mostly Unreal text-serialised strings, not JSON.**
  Example: `mIngredients = "((ItemClass=\"/Script/Engine.BlueprintGeneratedClass'/Game/.../Desc_OreIron.Desc_OreIron_C'\",Amount=1))"`.
  Parsing it needs a parenthesis- and quote-aware parser. Numbers are strings (`"2.000000"`), and
  booleans are `True`/`False`. A few fields are real JSON arrays with Unreal strings nested inside,
  among them `mFuel` on generators and `mUnlocks` on schematics.
- **⚠ The recipe duration field is misspelled in the data:** `mManufactoringDuration`. A search for
  the correct spelling finds nothing.

**What it covers (counts measured on en-US):**

| Area | Native class(es) | Notes |
|---|---|---|
| Recipes | `FGRecipe` (872) | **291 are made in a machine.** The other 576 are build-gun, workbench or equipment-workshop recipes, and 5 list no producer. `mIngredients`, `mProduct`, `mManufactoringDuration` (seconds), `mProducedIn`, plus variable-power fields |
| Alternate recipes | within `FGRecipe` | Counted two ways: 110 by display-name prefix `Alternate:` and 110 by class name containing `Alternate`. The two sets differ by one each: `Recipe_PureAluminumIngot_C` is named as an alternate but its class isn't, and `Recipe_Alternate_Turbofuel_C` is the reverse. `FGSchematic` has 109 `EST_Alternate` schematics |
| Items | `FGItemDescriptor`, `FGResourceDescriptor`, biomass, nuclear fuel, consumable, equipment, power-shard, … | `mForm` (`RF_SOLID`/`RF_LIQUID`/`RF_GAS`), `mStackSize` (enum such as `SS_BIG`, `SS_FLUID`), `mEnergyValue` (fuel MJ), `mResourceSinkPoints`, `mRadioactiveDecay` |
| Machines | `FGBuildableManufacturer` (8), `…VariablePower` (3) | `mPowerConsumption` (MW), `mPowerConsumptionExponent` (overclock curve, 1.321929), `mProductionBoostPowerConsumptionExponent` (2.0), `mMinPotential`/`mMaxPotential`, shard-slot fields. Variable-power machines carry estimated min/max MW instead |
| Extractors | `FGBuildableResourceExtractor`, `FGBuildableWaterPump`, `FGBuildableFrackingExtractor` | rate = `mItemsPerCycle / mExtractCycleTime`. Measured: Miner Mk.1 works out to 1 item/s = 60/min, which matches the game's normal-node rate |
| Generators | `FGBuildableGeneratorFuel`, `…Nuclear`, `…GeoThermal` | `mPowerProduction` (MW); `mFuel` lists fuel / supplemental (water) / byproduct; `mSupplementalToPowerRatio` |
| Logistics | `FGBuildableConveyorBelt` (6), `FGBuildableConveyorLift`, `FGBuildablePipeline` (4), pumps | belts `mSpeed`, pipes `mFlowLimit` |
| Vehicles and drones | `FGVehicleDescriptor` (8), `FGBuildableDroneStation`, `FGBuildableTrainPlatformCargo`, `FGBuildableDockingStation` | `mInventorySize` (slots: Freight Car 32, Truck 48, Tractor 25, Drone 9), `mAutopilotFuelConsumption`, drone `mTripPowerCost`/`mTripPowerPerMeterCost`, locomotive power min/max. Feeds D-014 |
| Progression | `FGSchematic` (574) | `mType`: ResourceSink 173, MAM 120, Alternate 109, Custom 93, Milestone 42, Customization 30, Tutorial 6, HardDrive 1. `mTechTier`, `mCost`, `mUnlocks`, `mSchematicDependencies` |
| Everything else | building pieces, vehicles, equipment, customisation (`FGCustomizationRecipe` 106) | Mostly irrelevant to a calculator |

**Units:**
- Inferred from game knowledge, not checked against the data: fluid `Amount` is in thousandths of m³
  (`4000` = 4 m³), belt `mSpeed` is twice the items/min figure (Mk.1 `120` = 60/min), and pipe
  `mFlowLimit` is m³/s (Mk.1 `5` = 300 m³/min).
- Measured: the Water Extractor is `2000` per 1 s cycle, which is consistent with the fluid unit above.

**⚠ Not in the data:**
- **Resource-node purity multipliers.** `mPurityMultiplier` has zero hits in Docs. `FGResourceSettings.h`
  declares it, but the values live in game assets.
- **Resource-node locations.** None of the 114 native classes is a resource node.
- **Machine ports.** `mFactoryInputConnections` and `mPipeInputConnections` are empty on all 11 manufacturers. Footprints are present (`mClearanceData`). Feeds D-012.
- A calculator needs both from another source.

### Headers/ — C++ public headers

1,112 `.h`, 24 `.cs` (UBT target/build rules), 7 `.uplugin`. Declarations only, no `.cpp`.

- Useful for field semantics: `Resources/FGResourceNode.h` (purity enum `RP_Inpure`/`RP_Normal`/`RP_Pure`), `FGResourceSettings.h`, `FGRecipe`/building headers.
- Useful for the save format: see below.

### Save-game format — partly described

The headers **describe** the outer layers:
- **File layout** (`FGSaveSession.h`): `[FSaveHeader (uncompressed)][SaveWorld (ZLIB-compressed)]`.
- **`FSaveHeader`** (`FGSaveManagerInterface.h`): its fields, and a dated version history from `InitialVersion` to `AddedSaveName` (2024-09-12).
  - Fields: save/build version, save name, map name and options, session name, play duration, save time, mod metadata, partitioned-world flag, creative-mode flag, UE5 object version.
- **Per-object and per-actor save headers** (`FGActorSaveHeaderTypes.h`): class name, object reference, flags, outer path, and transform plus placement flags for actors.
- **Version enums:** `SaveCustomVersion.h` and `FactoryGameCustomVersion.h`. The current numbers are in `CustomVersions.json`.

They **do not describe**:
- the byte order of the header fields (`operator<<` is declared, but its body is in a `.cpp` that isn't shipped);
- how the compressed body is chunked;
- the level and world-partition layout inside `SaveWorld`.

Object properties are Unreal tagged/unversioned property serialisation, and `FactoryGame.usmap` supplies the schemas for it.

**Conclusion:** the bundle gives the vocabulary and versioning. A working parser still needs the
engine's serialisation format, either from Unreal knowledge or from an existing community parser.

### DedicatedServerAPIDocs.md

Covers the dedicated server's protocols:
- a UDP lightweight query API for server state;
- an HTTPS JSON API (auth, server options, save/load/upload/download saves, run commands).

It is relevant only if the tool ever talks to a running server.

### FactoryGame.usmap

A binary mapping file of class property names and types for unversioned-property assets. Asset and
save tools (FModel, CUE4Parse-style parsers) consume it. The calculator does not need it unless it
parses saves or game assets.
