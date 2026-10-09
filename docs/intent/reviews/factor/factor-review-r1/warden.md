# Warden review: factor product brief, Intake round 1

**Mode:** review mode for correctness, then security mode as a discovery-stage security read. The second pass uses the `security-implications-checklist` skill.
**Artifact:** `docs/intent/factor.md` (worktree `3931-product-brief`, HEAD `e020783`).
**Verdict:** Request changes. There is 1 blocker and 3 high findings.

## What this review checked

- **Feature register.** The brief's 142 `F-NNN` entries were reconciled mechanically against `docs/design/feature-verdicts.md` @ `c60f8db`, on ID, verdict and name.
  - The result was identical: 49 mvp, 29 shape, 27 later and 37 skip.
  - Positive control: one verdict was mutated deliberately, and the diff caught it (rc=1).
  - Every Committed line maps its verdict to its release note consistently: mvp to "first build" (49), shape to "first build: backend structure only" (29), later to "eventually, not immediately" (27).
  - The NG-6 count of 37 matches.
  - Every Committed entry passes the Committed-tier validator, because each carries a commit pointer.
- **Decision log.** Every `D-NNN` the brief cites was read against `docs/decisions.md`, including its status (ruled or open).
- **Verdicts quoted in the decision log.** Every `F-NNN ... *verdict*` that `decisions.md` quotes was cross-checked against the snapshot. The regex returned 23 hits covering 21 distinct features. F-124 and F-125, which share a sentence in D-030, were checked by hand, for 23 distinct features in all. One mismatched (WR-12).
- **Clock fixture.** The SC-4 fixture's expected values were recomputed from `docs/design/ui-brief.md` §"Real content" and checked against D-016.
- **Not checked.**
  - Brief lines that cite the 2026-10-08 intake answers, such as "Peter chose all four of SC-1, SC-2, SC-4 and SC-5 by option label". Their only source is the intake conversation, which this context cannot see.
  - Mechanism choices, which are tagged `[ARCH-DEFERRED]` where they come up.

---

## Findings

Severity follows the dispatch scale. The confidence figure (0–100) measures how sure the review is that the finding is real.

### Blocker

**WR-01: SC-2 and SC-3 can pass without proving scale.** Confidence 85.
- **Anchor:** Success criteria, SC-2 and SC-3.
- **The SC-2 hole.** SC-2 sets its threshold as "at least 5,000 machines in one plan", checked against "a generated reference plan". Under the ruled engine, machine count does not measure what scales.
  - D-016 says whole machines are chosen *after* the rate solve, so the size of the linear program depends on distinct recipe instances, items and factories, not on machines.
  - The view scales with diagram nodes. D-012's proposal lets one node stand for many machines.
  - So a generated plan with one recipe node at 5,000 machines meets the letter of SC-2 and proves nothing about solve size or diagram size.
- **The SC-3 hole.** SC-3 inherits the reference plan and adds a second gap. Under D-017, "a change recomputes only the connected part of the graph it touches". An edit to a small isolated component therefore meets the 100 ms budget on a plan of any size.
- **Why this is a blocker.** Both criteria can pass whatever the scale behaviour is. Downstream tests built on them would inherit the hole.
  - Peter's own complaint is node-keyed: "can't calculate all the nodes on a change".
- **Proposed clarification.** Restate the SC-2 threshold in the attributes that the solver and the view each scale with: distinct recipe nodes, items, factories (F-053), loops (F-015) and alternates enabled. Keep "5,000+ machines" as the label Peter chose.
  - Either derive those numbers from the whole-game recipe set and EV-3's measured cases, or put them to Peter as a reading to confirm.
  - Require that SC-3's edit lands on the largest connected component. A target change on the root output is the obvious worst case.
  - How the reference plan is generated is `[ARCH-DEFERRED]`.

### High

**WR-02: SC-3's check times the solve, but the criterion times edit-to-view.** Confidence 85.
- **Anchor:** Success criteria, SC-3.
- **The mismatch.** The criterion is "re-solves and the diagram updates in under 100 ms, measured from the edit to the updated view". The check is "solve time recorded on every solve, plus a budget test".
  - Solve time covers only one segment of that span.
  - Auto-layout (F-069 mvp) and rendering in a toolkit not yet chosen (D-036) both sit inside the span, and either can dominate it.
  - As written, the check can stay green while the experience Peter was promised ("instant") is broken.
- **Proposed clarification.** The check measures the same span as the criterion, edit to updated view. Solve time can also be recorded as its own segment, so a regression can be located.
  - The instrumentation mechanism is `[ARCH-DEFERRED]`. The requirement is that check and claim are keyed on the same span.

**WR-03: SC-4's named fixture contradicts D-016's default machine sizing, and its expected answer is Puck-authored.** Confidence 85.
- **Anchor:** Success criteria, SC-4, and HC-4 (D-016).
- **The source.** SC-4's check names "the 80/min-capped iron chain whose clocks are 8/9". The only source in the repo is `docs/design/ui-brief.md`, which says "Smelters become x3 at 88.8888% (8/9) and every downstream clock scales by 8/9".
- **The recomputation.** Base rates come from the ui-brief's own table: plate 20/min, rod 15/min, screw 40/min and RIP 5/min per machine. Under the 80/min cap, D-016's default ("by fewest buildings") gives:
  - Smelters: x3 at 8/9. This matches the fixture.
  - Iron Plate, 40/min: **x2 at 100%**, where the fixture gives x3 at 66.67%.
  - Screws, 80/min: **x2 at 100%**, where the fixture gives x3 at 66.67%.
  - Rods and RIP: x2 at 2/3. These match.
- **What follows.** "Every downstream clock scales by 8/9" holds only if machine counts carry over from the previous solve. Nothing rules that.
  - D-016's other branch is "a count Peter sets", and the fixture does not set one.
- **Two problems.**
  - (a) The fixture's expected answer contradicts a ruled decision under its default.
  - (b) The oracle is a mockup example Puck wrote. It is not a plan Peter worked out by hand, which is what the criterion promises ("the exact clocks Peter would pick by hand"). Nothing in the brief labels it as Puck-authored.
- **The requirement gap underneath.** When an edit or a cap changes a plan, does factor keep the machine counts already built and re-clock them, or re-minimise the buildings? It is a real product question, because Peter builds from the plan in game (EV-5).
- **Proposed clarification.** Put the stability question to Peter as a requirement. Then source the SC-4 fixtures from his own hand-planned examples (2 × 75%, and his "multiple instances" of 88.8888). Any Puck-derived fixture should be labelled as such.

**WR-04 [security]: RP-1 lists only part of the untrusted-input surface that Frame will threat-model.** Confidence 80.
- **Anchor:** Risk profile, RP-1.
- **What RP-1 covers.** RP-1 names "game data bundles, and saves later". It is the line that carries the parsing trust boundary to Frame. Other committed inputs also parse bytes factor did not write:
  - **F-094 Game icon extraction (mvp).** This parses the game's asset archives. D-026 notes the Satisfactory pipeline depends on Oodle decompression, a native third-party library.
  - **F-028 Mod content support (shape).** Mod recipes and buildings come from third-party authors by definition. D-003 names modded recipes as the reason for loading at runtime.
  - **HC-3 / D-003 generated data files, loaded at runtime.** They are trusted while Peter's own generator writes them. Under D-026 option (a), shipped data files, they become untrusted. Validation at load is already ruled, but RP-1 does not frame it as a trust boundary.
  - **Later items:** F-022, F-103 and F-104 (saves), F-130 (another tool's export format), F-136 (custom game data, "then share it").
- **The open case.** Plan files (F-129 mvp, SQLite per D-033) are untrusted only if they are exchanged between people. The brief does not say whether they are in the first build, so that is WQ-1, not evidence here.
- **Threat class.** CWE-20 (improper input validation) and OWASP A08:2025 (software and data integrity). The parsers involved include memory-unsafe native code (see the appendix).
- **Why high.** RP-1 is the handoff Frame reads. A boundary missing from it is not drawn, and nothing reports the gap.
- **Proposed clarification.** RP-1 lists every committed input class, each with the feature that brings it in, and states which ones are trusted-by-assumption in the first build ("Peter's own install").

### Medium

**WR-05 [security]: RP-3's re-trigger is keyed on "sharing" and has nothing that fires it.** Confidence 80.
- **Anchor:** Risk profile, RP-3.
- **The text.** "Sharing later adds them and re-triggers this review."
- **Features outside "sharing" that bring in network or credentials:**
  - F-119, the LLM interface (shape). A hosted model means an outbound connection and an API key on disk.
  - F-118, the programmatic API (shape): "remote interface, HTTP API, MCP".
  - F-112, server pull (skip): a dedicated-server admin password.
  - F-083 and F-134 (skip): new-version notice and telemetry.
  - The catalogue files F-118 and F-119 under "Sharing", but a reader of RP-3 will not take a local MCP server or an LLM call as sharing.
- **Why this is not cosmetic.** Frame's `threat-modeling` pass loads only when the architecture touches auth, PII, network or tenancy. Whoever dispatches Frame decides that partly from this Risk profile. "Network, auth, PII: none" can therefore suppress the very review RP-3 promises will come back.
- **Proposed clarification.**
  - Key the re-trigger on the attribute: any feature that opens a socket, stores a credential, or stores data identifying a person.
  - Name what fires it. For example, the per-feature Frame stage reads RP-3 as a checklist rather than a verdict.
  - Otherwise label it *parked*, with a cadence.

**WR-06 [security]: The tenancy shape (RP-2, HC-7) has no observable check.** Confidence 80.
- **Anchor:** Risk profile, RP-2, and Hard constraints, HC-7.
- **Why it cannot fail.** D-031 says "storage is reached through that scope, even while there is only ever one value". With a single owner value, a missing scope filter returns the same rows as a correct one. Nothing can catch the shape rotting before the second tenant arrives, and that is exactly when the retrofit becomes expensive, which is what D-031 exists to avoid.
- **The second gap.** Nothing says what happens to the owner/workspace id inside a plan file from another installation (F-129 import). It might be trusted, re-assigned or rejected.
  - That is where tenancy and untrusted input meet: a user-controlled key selecting the scope (CWE-639, latent until a multi-plan library or sharing exists).
- **Proposed clarification.**
  - Add a check: storage access scoped to owner A never returns owner B's plan, exercised with at least two ids.
  - State the rule for the owner id on import.
  - The form of the test is `[ARCH-DEFERRED]`.

**WR-07: HC-7 drops D-031's "examples, not the full list" qualifier.** Confidence 85.
- **Anchor:** Hard constraints, HC-7.
- **The misstatement.** D-031 says globalisation and tenancy "are examples, not the full list". HC-7 lists the two with no qualifier, so a cold-reading agent treats the list as closed.
- **Candidate third concern, flagged for Peter and not decided here.** The view-to-backend data interface. D-032's derivation makes it a serialisable interface. The same interface is what a web view (D-032), F-118 and F-119 would later call. If it is built assuming its only caller is a trusted in-process view, then validating input at it is a retrofit.
- **Proposed clarification.** Restore the qualifier, and decide whether the backend interface's input validation joins the list.

**WR-08: NG-5 cites an open decision as its source, extends it to game data, and conflicts with D-004.** Confidence 80.
- **Anchor:** Non-goals, NG-5. This is a legal finding, not a security one.
- **The source is open.** NG-5 says "No redistribution of game data or game art in the first build" and cites D-019. D-019's status is **open**. Its first-build outcome covers **icons** only.
  - Redistribution of game *data* is D-026, which is also open.
- **The conflict with D-004.** D-004's ruled outcome, also in `CLAUDE.md`, is "commit a small extract the calculator produces". D-019 says repo visibility is "public by default". Pushing that extract publicly would be redistribution of game data.
  - Measured today: `git remote -v` is empty, so the conflict is latent.
- **Proposed clarification.** Cite NG-5 to D-019's icon outcome and to Peter's quote, and label the data half as Puck's reading. Then raise the D-004/NG-5 conflict as a question for Peter: either the extract is committed only while the repo has no public remote, or D-004 is amended.

**WR-09: No requirement says a plan survives a crash.** Confidence 80.
- **Anchor:** Hard constraints and Success criteria. The gap is absent from the whole brief.
- **Why it matters.** Peter's first complaint about Modeler is that it "dies". One of D-033's deciding reasons for SQLite was "transactions give crash-safe autosave".
  - That reason was Puck's, adopted with the ruling.
  - No SC or HC states the requirement, and no catalogue row covers autosave. A grep for autosave, crash, backup and recover across the brief, the verdicts and the ui-brief found nothing.
  - HC-8 records the mechanism with no requirement behind it. If a later decision replaces the mechanism, nothing would show that crash safety went with it.
- **Proposed clarification.** Ask Peter to state it as a requirement. One possible form: "no confirmed edit is lost when factor crashes or is killed". That would give it a check of its own.

**WR-10: SC-5's criterion and its check disagree, and the criterion rests on an open decision.** Confidence 80.
- **Anchor:** Success criteria, SC-5, and HC-9.
- **The disagreement.** The criterion allows changes to the core "beyond declared per-game extension points". The check allows "no diff to the core model's crate" at all.
  - "Declared" has no time anchor. If extension points can be declared in the same change as the second game, the criterion is vacuous.
  - The extension points are D-029's subject, and D-029 is **open**. HC-9's list of open items omits it.
  - The check also presumes a single core crate, which is a mechanism. The crate layout is `[ARCH-DEFERRED]`, but the check depends on it.
- **Proposed clarification.** Anchor "declared" to "before the second game's work begins". Make the check measure the same thing. Add D-029 to HC-9.

**WR-11: SC-1's review point is never named.** Confidence 85.
- **Anchor:** Success criteria, SC-1.
- **The gap.** The check is "Peter's own statement at a review point". The brief says honestly that this is a self-report. It does not say when the review point happens or what triggers it, so as written SC-1 is never evaluated.
- **Proposed clarification.** Name the trigger: a date, a milestone such as the first real build planned end to end, or a stated cadence. Otherwise label SC-1 parked, with that cadence.

**WR-12: F-002's verdict differs between `decisions.md` and the snapshot the brief cites.** Confidence 85.
- **Anchor:** Feature register, Idea tier, F-002.
- **The mismatch.** `docs/decisions.md` D-017, under "Picker verdicts, 2026-10-08", records "F-002 Recursive tree expansion: *later*". The snapshot @ `c60f8db`, and so the brief, has *skip*, which places it in the Idea tier.
  - The tier assignment turns on which one is right.
  - This review does not say which copy is stale. It may be a round-1 versus round-2 difference.
  - The other 22 distinct features whose verdicts `decisions.md` quotes all match the snapshot.
- **Proposed clarification.** Reconcile the two at the intake gate, and correct whichever record is wrong.

---

## Suppressed findings (confidence < 80)

Counts only. The findings stay in working notes; WR-S1 is folded into WQ-1 and the appendix.

| Severity | Found | Suppressed |
|---|---|---|
| Blocker | 1 | 0 |
| High | 3 | 0 |
| Medium | 9 | 1 |
| Low | 2 | 2 |

The medium suppression is WR-S1: RP-3's "PII: none" would fail once plan files carry an owner id, local paths or notes to another person. It turns on WQ-1. The two lows are both scope-wording items, below the bar.

---

## Security Implications (Warden, discovery stage)

**Trigger surfaces detected:**
- Multi-tenancy: shaped, not built.
- Network and auth: none in the first build, but there are first-build *shape* hooks (F-118, F-119).
- PII: latent, depending on WQ-1.
- An additional surface outside the checklist's four triggers, carried because RP-1 names it: untrusted file parsing.

### Surface assessments

#### Multi-tenancy
- **What's in scope.** An owner/workspace id on every stored plan, with storage reached through that scope (D-031). There is one tenant value, and no cross-tenant or admin operation.
- **Silent gaps in requirements.**
  - No isolation check (WR-06).
  - No rule for the owner id in an imported plan file (WR-06).
  - No requirement that the owner id be opaque rather than derived from the OS user or machine.
- **Severity:** medium.

#### Network and auth
- **What's in scope.** Nothing in the first build (D-030).
  - F-118 (programmatic API) and F-119 (LLM interface) are *shape*: the backend is structured for them in the first build.
  - F-112, F-083, F-134, F-124 to F-128 and F-132 are *skip*.
- **Silent gaps in requirements.**
  - The re-trigger is keyed on the wrong attribute and has nothing to fire it (WR-05).
  - Nothing says whether F-119 means a hosted model, which brings a credential on disk and an outbound connection, or a local one (WQ-3).
- **Severity:** medium.
- **Uncovered lens.** F-118 and F-119 (MCP, LLM) are AI/LLM surfaces. No AI/LLM lens ships in this plugin, so tool schemas, prompt construction and prompt injection through plan text are not covered by this review.

#### PII and sensitive data
- **What's in scope.** None by declaration (RP-3). Three latent carriers exist if plan files leave the machine:
  - the owner id;
  - local absolute paths to the save or install, which contain the macOS username, if a plan stores them (F-096, F-094);
  - free-text notes (F-067 mvp).
- **Silent gaps in requirements.** Nothing says what a plan file may carry when it leaves the machine. No retention or deletion question applies while the data stays local.
- **Severity:** low in the first build. It rises with WQ-1.

#### Untrusted file parsing (RP-1)
- **What's in scope.** Game data bundles (F-093 mvp), game asset archives (F-094 mvp), mod content (F-028 shape), generated data files (HC-3), and later saves, other tools' exports and custom game data.
- **Silent gaps in requirements.** The input classes are listed incompletely (WR-04). Nothing says how the app behaves on malformed or hostile input: whether it rejects with a named error, never crashes, and stays bounded in time and memory.
- **Severity:** high.

### Scope-level recommendations

These are recommendations, not findings. Peter decides scope.

- **Defer to v2.**
  - Keep F-118 and F-119 at *shape*, with nothing exposed in the first build. Then the backend interface has one caller in v1.
  - Keep plan-file exchange out of the first build, if WQ-1 allows. That defers the foreign-plan-file boundary and the PII question together.
- **Add to v1.**
  - A tenancy isolation check (WR-06).
  - A plan-durability requirement (WR-09).
  - A first-build requirement that loading any file is fail-closed: malformed input is rejected with a named error and never crashes or hangs the app.
  - The opaque owner id is cheap now and hard to change after plan files are in the wild, because it is in the persisted format.
- **Out-of-scope dependencies to state.**
  - The first build trusts Peter's own game install and his own generator output. State this as an assumption, so it is visibly withdrawn when D-026 (a) or F-028 arrives.
  - External extraction tools (FModel or CUE4Parse, D-019) and Oodle (D-026) are third-party dependencies.
  - Release distribution integrity, meaning code signing, notarisation and any update channel, has no catalogue row. RP-4 gates public release on legal items only, so nothing currently brings release integrity to review before a release.

### Items for Architecture Threat Modeling

These are for `/brief`'s Frame-stage `threat-modeling` pass. Mechanisms are `[ARCH-DEFERRED]`. The boundaries below are the ones the Frame diagrams will need to draw.

- **WTB-1: game data bundle → generator.**
  - Inputs: Unreal text-serialised values, which need a hand-written parser that tracks parentheses and quotes, and encoding that differs per file (CLAUDE.md, measured).
  - A hand-written parser over third-party bytes is the classic place to fuzz.
- **WTB-2: generated data files → app load (D-003 validation at load).** Trusted while they are local. Untrusted under D-026 (a), F-028 and F-136. Validation should check fields against an allow-list, not mere well-formedness.
- **WTB-3: plan file (SQLite, D-033) → app.**
  - Opening a SQLite database from a foreign source is a known attack surface: schema objects run on open, and the SQLite library is native.
  - Schema migrations run on foreign files.
  - Deleted content (notes) can remain in free pages of a file that is then shared.
  - The owner id arrives on import.
- **WTB-4: game asset archives → icon extraction (F-094 mvp).** Native Oodle decompression (D-026), and possibly an external extractor process. If factor launches one, it is a process-execution sink whose path and argument values come from configuration.
- **WTB-5: save files → save parser** (F-096 shape; F-022, F-103 and F-104 later). The parser's provenance and licence hang on D-025. Randomised-world node data comes from saves (D-027).
- **WTB-6: Rust ↔ native code.**
  - HiGHS, a C++ library, through the `highs` crate, with unsafe FFI planned for IIS, ranging and warm-start (D-021).
  - Bundled SQLite.
  - Model sizes derived from WTB-1 to WTB-3 cross into memory-unsafe code.
  - Availability: a crafted model can drive solve time up. EV-3 measured 8.9 s to prove infeasibility, against SC-3's 100 ms.
- **WTB-7: view ↔ backend data interface (D-032).** Two D-036 options, Dioxus via Wry and Tauri, render in a system webview. Strings from WTB-1 to WTB-3 would then render in an HTML context:
  - display names from 55 locale files;
  - mod names;
  - plan notes (F-067).
  - F-133, shared-text safety rules, is *skip*.
  - The webview's IPC bridge exposes backend commands to any script that gets in. This applies even with no network.
- **WTB-8 (future): external callers → backend** (F-118 API or MCP; F-119 model-driven tool calls). Prompt injection through plan or game text is in scope for whichever lens covers AI/LLM. None ships today.
- **Quality attributes, by priority.**
  - **Integrity: high.** Exact results that never overdraw (D-022, SC-4), and plan data that is not corrupted (WR-09).
  - **Availability: high.** Megabase scale (SC-2, SC-3); hostile or malformed input must not crash or hang the app (WTB-1 to WTB-6).
  - **Confidentiality: low in the first build.** It rises with plan-file exchange: owner id, local paths, notes and SQLite residue (WTB-3).

### Security Scan
- **Dependency audit:** not applicable at Intake. There is no code and no manifest to audit, and none was run.
- **Dangerous patterns:** not applicable at Intake. There is no code.

---

## Domain Questions

| ID | Domain area | Question | What I can't see from the doc |
|---|---|---|---|
| WQ-1 | Plan files | In the first build, will a plan file ever be opened that someone other than Peter wrote, or is F-129 only save and load on his own machine? | The catalogue row says "send it to someone". Peter's only note there is "not json please". The answer decides whether WTB-3 and the PII question are v1 or v2. |
| WQ-2 | Icon extraction | For F-094, does factor parse the game's asset archives itself, or read the output of an extractor Peter runs separately? | It decides whether native Oodle decompression and archive parsing sit inside factor's trust boundary or outside it (WTB-4). |
| WQ-3 | LLM interface | Is the model for F-119 local or a hosted provider? | A hosted provider brings an API credential at rest and an outbound connection. Both affect what the *shape* has to accommodate in the first build (WR-05). |
