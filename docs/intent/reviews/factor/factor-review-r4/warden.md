# Warden review: factor product brief, Intake round 4

**Mode:** review mode first (ambiguity, scope gaps, contradictions, fix-induced drift), then security mode (discovery-stage read with the `security-implications-checklist` skill).
**Artifact:** `docs/intent/factor.md` @ `e8912b4` (worktree `3931-product-brief`). Context: `docs/decisions.md` @ `e8912b4`.
**Tier:** Intake. Mechanism is `[ARCH-DEFERRED]`. How a criterion is tested is `[SPEC-DEFERRED]`; no findings are raised on that.
**Verdict:** Approve with conditions. **No blocker or high.** 3 mediums and 3 lows. **All six are fix-induced or variants of round-3 findings.** No new design-shaped problem surfaced.

## What this review checked

- **Brief:** read in full @ `e8912b4`, 387 lines.
- **Decisions diff:** `git diff 93d6c53..HEAD -- docs/decisions.md`. This covers D-031 (accessibility now names Gate B), D-018 (F-009 re-described), D-016 (shards; pinned-count shortfall; node-ceiling shortfall) and D-022 (Context line).
- **Blocks read directly** for the gate-keying checks:
  - D-004, lines 46–53;
  - D-033, lines 192–202;
  - D-019, D-025 and D-026, lines 322–366.
- **Grep `HC-11|first share|first-share|Gate A|Gate B|public|first push|remote` over `docs/decisions.md`.** Hits at lines 52, 53, 129, 324 and 362. Line 129 says Gate B. Line 362 still says "first-share gate".
- **Grep `newer|downgrade|older` over the brief and decisions.**
  - Brief: one hit, SC-7 line 75 ("older version of factor").
  - Decisions: two hits, neither about plan files.
  - The instrument found a known hit, so the absence of a newer-version case is a real absence.
- **Remote:** `git remote -v` returned nothing, rc 0. No positive control, so this is consistent with "no remote today" but does not prove it.
- **Credential-pattern grep** over the brief and decisions returned 0. **No positive control was run** for that regex. There is no code at this stage, so the scan is reported as not applicable (Security Scan below).
- **Not checked:** Peter's round-6 answers are inherited as quoted, because their only source is the review conversation.

## Round-3 dispositions

| ID | Disposition | One line |
|---|---|---|
| W3-01 | **Resolved** | SC-7 now has three branches. A corrupt or self-contradicting file is rejected, which covers a dangling internal reference. A game-update plan opens with named problems. An older-version plan is migrated forward. Fix-induced: the version branch can still lose data (W4-03). |
| W3-02 | **Resolved in the brief** | HC-11 is two gates. The D-004 extract, D-025 and D-026 sit under Gate A, and RP-3 is per slice. Fix-induced: `decisions.md` still keys D-026 and D-019 on "first share" (W4-05). Gate B's event can't be observed (W4-01). Distribution items miss the build hand-over event (W4-02). |
| W3-03 | **Resolved for release integrity; partly for export** | Signed and notarised releases are under Gate B. Export contents are listed, but keyed to an event later than the one at which a plan file can leave Peter's machine (W4-04). |
| W3-04 | **Resolved** | The owner-id fixture is gone from SC-7 ("this criterion doesn't decide it"). FQ-4 now asks what the id is tied to and what makes it "known", and says the id "authenticates nothing". Whether the id should be opaque now sits in FQ-4, a legitimate Frame question. |
| W3-05 | **Partly resolved (Low)** | The rejection time and memory limits moved to FQ-10. They are outcome thresholds, not test mechanics: the brief keeps SC-2's 1 GB and SC-3's 100 ms in its criteria. The deferral is still valid, because FQ-10 is a named carrier that Spec reads. Residue is W4-06. The fuzz or generative check is `[SPEC-DEFERRED]`. |
| W3-06 (a) | **Resolved** | SC-3 now states the 1 s redraw and stale marks on every displayed value, on screen and to assistive technology. Timing is `[SPEC-DEFERRED]` (FQ-10). |
| W3-06 (b) | **Resolved** | SC-6 states "the fewest new machines". The 9/min and 10/min fixtures are in FQ-10, `[SPEC-DEFERRED]`. |
| W3-06 (c) | **Claim resolved; range mis-filed** | SC-8 now says "everything synced before that survives". The upper bound on the sync interval went into FQ-10 as a test mechanic, but it is the setting's allowed range, which is product behaviour. W3Q-2 is still unanswered and is re-asked as W4Q-4 (W4-06). |
| W3-07 | **Resolved** | The source list covers rounds 1 to 6, and SC-4 and SC-7 now carry Peter's rulings. A wording residue is suppressed below (confidence 70). |

`[SPEC-DEFERRED]`, not filed: HC-7 Tenancy still says "Tests exercise at least two owner ids". That is a test mechanic the restructure left in a hard constraint.

---

## Findings

"Fix-induced" means a round-3 fix introduced or reshaped the finding, and cites that round-3 finding.

### Blocker

None.

### High

None.

### Medium

**W4-01 [security]: Gate B's event can't be observed, so FQ-8 can't fire it without someone remembering.** Fix-induced from W3-02. **The event wording came from Warden's own W3-02 proposal** ("another person uses factor"). Confidence 80.
- **Anchor:** HC-11 Gate B ("anyone other than Peter runs a build"); HC-11 lead ("so neither relies on someone remembering"); FQ-8.
- **The gap.**
  - "Someone else runs a build" happens on someone else's machine. Nothing in Peter's repo or toolchain sees it. This holds when Peter copies the `.app` to a friend, and when anyone builds from source once Gate A has fired.
  - FQ-8 is asked to build a mechanism for an event that leaves no trace where a mechanism could run. That is the named-but-unfireable trip-wire that `P-GuaranteeByMechanism` (DF1) calls invalid: it reads as handled and no-ops.
  - Gate B carries the accessibility floor, foreign plan files as a trust boundary, export contents, and signing. All four would then rest on recall.
- **Proposed clarification** (Peter's call, W4Q-1). Key Gate B to an observable proxy:
  - the first build made for distribution (packaging, signing or notarisation is itself a step a mechanism can gate);
  - or the Gate A event, whichever comes first, if Peter treats a public source repo as "someone else can run a build".
- **Alternative:** relabel Gate B as *parked*, with a stated review cadence. DF1 allows that, but only under that name.

**W4-02 (legal, RP-4): the distribution items fire only at Gate A, but giving anyone a build also distributes.** Fix-induced from W3-02. That split keyed the legal items to the public remote alone. Confidence 80.
- **Anchor:** HC-11 Gate A and Gate B lists; RP-4; NG-5; D-026 option (a) and its "Licences not checked: … Oodle" line; D-025.
- **The gap.** A build handed to another person, with no public remote, can carry:
  - generated game data, if D-026 picks option (a);
  - any icons bundled rather than extracted on the user's machine (NG-5 allows icons for Peter's own use only);
  - third-party code whose licence terms attach to binary distribution: HiGHS and SQLite, and Oodle, whose licence D-026 records as unchecked.

  It also hands someone factor under an unchosen licence (D-025). Gate B lists none of this, so the gate can fire, pass, and leave these obligations untouched. This is the silent false-green W3-03 named.
- **Proposed clarification:** the Gate A legal items fire at whichever of Gate A or Gate B comes first. Or list them under both gates. W4Q-2.

**W4-03: SC-7's version branch can lose Peter's data.** Fix-induced from W3-01(b). Confidence 80.
- **Anchor:** SC-7, the "A plan saved by an older version of factor" sub-bullet; SC-3 ("the save of the edit (SC-8) [is] inside that window"); SC-8.
- **(a) Lossy migration, then autosave.**
  - The criterion says anything that can't be carried over "is named as a problem". It does not say the data is kept.
  - The game-update branch says "nothing is silently dropped". The migration branch has no matching clause.
  - Every edit is saved inside SC-3's window. So the first edit after a lossy migration overwrites the only copy of whatever wasn't carried over, unless the pre-migration file survives.
  - A named problem whose underlying data is already gone gives Peter nothing to fix it with.
- **(b) A plan saved by a *newer* factor falls through all three branches.**
  - It is not corrupt, not a game update, and not older. The grep for `newer` and `downgrade` returned no hits.
  - The realistic case is in the brief's own scope: a Windows build that lags the Mac build (HC-1), or a dev build. D-019 records Peter moving files between machines.
  - If an older factor opens the file and autosaves, it can silently discard what it doesn't understand.
- **Proposed clarification** (W4Q-3):
  - Migration keeps the pre-migration file, or keeps the uncarried data, until Peter acts on the named problem.
  - A newer-version file gets a named outcome: refuse with a named error, or open read-only.

### Low

**W4-04 [security, data minimisation]: export contents are keyed to Gate B, but a plan file can leave Peter's machine earlier.** A variant of W3-03. The fix placed the item, but under a later event. Confidence 80.
- **Anchor:** HC-11 Gate B ("what an exported plan file carries (F-129 export is in the first build)"); D-033 ("the `sqlite3` tool or a factor reader as the way to get text out"); NG-4 and D-034 (a shipped demo plan).
- **The gap.** Reading a plan file doesn't need a factor build, because `sqlite3` reads it (D-033). A plan file leaves the machine:
  - when Peter posts one;
  - when a demo plan or a test fixture is committed to the repo and published at Gate A.

  What it carries (owner id, local paths, F-067 notes, free-page residue, per W3-03) goes with it in every case.
- **Proposed clarification:** key export contents to the earliest of Gate A, Gate B, or the first plan file committed to the repo. Sensitivity is low while the only user is Peter, so Low.

**W4-05: `decisions.md` still keys D-026 and D-019 on "first share".** Fix-induced from W3-02. The brief was re-keyed; the decision records were not. Confidence 90.
- **Anchor:**
  - `docs/decisions.md:362` (D-026): "The first-share gate (product brief HC-11, FQ-8) is what fires this."
  - D-019's Outcome (icons, first build): "the redistribution question waits until factor is shared."
- **The gap.**
  - HC-11 has no gate called "first share" now.
  - "Share" reads most naturally as Gate B, the later event, which is exactly the W3-02(a) mis-keying.
  - `CLAUDE.md` tells agents to read `decisions.md` before designing, so a Frame agent can pick up the stale key.
  - D-031's line 129 was updated to name Gate B, so this is an incomplete sweep, not a deliberate difference.
- **Proposed fix:** name Gate A in D-026 and in D-019's Outcome (and Gate B too, if W4-02 is accepted).

**W4-06: FQ-10 holds two outcome parameters labelled as test mechanics.** A partial resolution of W3-05 and W3-06(c). This is the dispatch's "is it really a testing question" check. Confidence 80.
- **Anchor:** FQ-10's bullets "time and memory limits for rejecting bad input (SC-7)" and "an upper bound on the sync-interval setting (SC-8)"; the success-criteria preamble.
- **The test used here.** The brief keeps SC-2's 1 GB and SC-3's 100 ms and 1 s inside its criteria. So an item that changes what Peter observes or can configure is an outcome. An item that changes only how a test observes it is a mechanic.
- **(a) SC-7's rejection limits** are outcome thresholds of the same kind as SC-2's and SC-3's. Leaving them for Spec to size is a valid deferral. Filing them as "how each criterion is tested" is the problem: it lets a Spec agent treat them as harness timeouts rather than product limits. That is the unrecorded divergence the Consistency value calls the defect.
- **(b) The sync-interval range** decides whether SC-8's power-loss guarantee can be configured away. If the setting allows "never", "everything synced before that survives" holds only by default. Peter said "allow it to be tuned", which does not answer whether it may be turned off. W3Q-2 asked this and got no answer. FQ-10 deferred it as a mechanic instead.
- **Proposed fix:**
  - Label both bullets as outcome thresholds that Spec sets.
  - Put (b) to Peter (W4Q-4).

### Nit

None reported.

---

## Suppressed findings (confidence < 80)

| Severity | Found | Suppressed |
|---|---|---|
| Blocker | 0 | 0 |
| High | 0 | 0 |
| Medium | 5 | 2 |
| Low | 5 | 2 |
| Nit | 1 | 1 |

- **Medium (65).** SC-3's list of edits ("a target change, a change to an extractor's settings, or setting or releasing a pin") leaves out structural edits. If the list is exhaustive, adding or deleting a node, connecting an edge and F-056 spin-off fall outside the 100 ms outcome. It may instead be a sample list, which would make it `[SPEC-DEFERRED]`.
- **Medium (60).** SC-6 has two rules that a reader could set against each other:
  - kept machines are re-clocked "at or below 100%";
  - "a shortfall's fix may use shards already placed".

  They read consistently if "fix" means a proposal and placing shards counts as a clock-kind pin (SC-9). A sharded node with no pinned count is the case to confirm.
- **Low (70).** HC-11 says each gate "fires" its obligations, but not that they must clear *before* the push or hand-over. A detector that fires after the push has already published the extract.
- **Low (50).** A game update that changes a recipe's numbers, rather than removing or renaming it, silently changes a plan's results on open. SC-7 names only removals and renames.
- **Nit (70).** The source list's "SC-2's test plan" refers to content now in FQ-7. "SC-3's numbers" can be read as excluding the round-5 redraw answer.

---

## Security Implications (Warden, discovery stage)

**Trigger surfaces detected:**
- **Multi-tenancy:** shaped, not built.
- **Network and auth:** none in the first build. F-118 and F-119 are *shape*.
- **PII and data minimisation:** an exit path in the first build through F-129 and committed plan files.
- **Untrusted file parsing:** outside the checklist's four triggers, but carried because RP-1 names it.

### Surface assessments

#### Multi-tenancy
- **What's in scope:** an owner/workspace id on every stored plan (HC-7, D-031). There is one tenant value, and no cross-tenant or admin operation.
- **Silent gaps:** none new. FQ-4 now holds the id's binding, what makes it "known", and the scoping-key-not-credential point.
- **Severity:** low.

#### Network and auth
- **What's in scope:** nothing in the first build (D-030). RP-3's re-trigger is now per slice and lists F-083, F-112, F-118, F-119, F-134 and every sharing feature. FQ-8 carries the mechanism.
- **Silent gaps:** none new. The F-118 and F-119 AI/LLM surfaces stay uncovered by any shipped lens, and RP-3 names that gap correctly.
- **Severity:** low at this scope.

#### PII and data minimisation
- **What's in scope:** plan-file contents once a file leaves Peter's machine.
- **Silent gaps:** the gate event for export contents (W4-04).
- **Severity:** low.

#### Untrusted file parsing
- **What's in scope:** RP-1's classes, with the first-build trust assumption stated. Plan files are validated on open (SC-7).
- **Silent gaps:**
  - the version-branch data loss (W4-03);
  - rejection limits labelled as test mechanics (W4-06a).
- **Severity:** medium (W4-03).

#### Release and distribution (not a checklist trigger; carried from W3-03)
- **What's in scope:** signed and notarised releases at Gate B.
- **Silent gaps:**
  - Gate B's event can't be observed (W4-01).
  - The legal items miss the build hand-over event (W4-02).
- **Severity:** medium.

### Scope-level recommendations

- **Defer to v2:** unchanged. F-118 and F-119 stay *shape*, and foreign plan files stay out of the first build (RP-1, ruled).
- **Add to v1:**
  - A Gate B event that a mechanism can see (W4-01).
  - Legal items at whichever gate fires first (W4-02).
  - Migration that keeps what it cannot carry, and a named outcome for a newer-version file (W4-03).
- **Out-of-scope dependencies to state:** unchanged from round 3. FModel, CUE4Parse and Oodle are third-party dependencies, and Oodle's licence is unchecked (D-026). This now matters at Gate B as well (W4-02).

### Items for Architecture Threat Modeling

WTB-1 to WTB-11 stand. FQ-9 now carries WTB-9, WTB-10 and WTB-11 inline. New:

- **WTB-12: SQLite opening a file factor did not just write.**
  - Source: Warden's platform knowledge, not measured.
  - A SQLite file's schema can carry triggers and views that run when it is queried. SQLite's own guidance for files from an untrusted source is `PRAGMA trusted_schema=OFF`, defensive mode and `cell_size_check`.
  - RP-1 keeps foreign plans out of the first build. But "validated on open" (SC-7) has to mean validated *before* any file-supplied schema object runs, not after. This becomes live at Gate B, and at F-130 import.
- **WTB-13: migration is a write path over Peter's only copy of a plan** (W4-03). It is an integrity boundary between format versions. Frame decides where the pre-migration copy lives and when it is released.
- **Quality attributes (unchanged ranking):**
  - **Integrity: high.** SC-4 exactness, SC-8 crash safety, and SC-7 migration without loss.
  - **Availability: high.** SC-2 and SC-3, and Peter's own plans opening across game, factor and machine changes (W4-03, FQ-4).
  - **Confidentiality: low.** It rises at the first plan file to leave the machine (W4-04).

### Security Scan
- **Dependency audit:** not applicable at Intake. There is no code and no manifest, and none was run.
- **Dangerous patterns:** not applicable at Intake. There is no code. The credential regex over the two documents returned 0, with no positive control.

---

## Domain Questions

| ID | Domain area | Question | What I can't see from the doc |
|---|---|---|---|
| W4Q-1 | Gate B | "Someone else runs a build" happens off your machine, so nothing can detect it. Should Gate B fire at the first build packaged or signed for distribution, or at the public remote, whichever comes first? **Recommendation:** whichever comes first. | Whether a public source repo counts as "someone else can run a build" for you (W4-01). |
| W4Q-2 | Licence and redistribution | Must factor's licence and the game-data and art questions be settled before you hand anyone a build, even with no public repo? **Recommendation:** yes. A binary can bundle game data, icons and Oodle. | Whether "Two events" meant the legal items fire *only* at the public remote (W4-02). |
| W4Q-3 | Plan compatibility | When migrating a plan loses something, should factor keep the original file until you act? And what should an older factor do with a plan from a newer one: refuse, or open read-only? **Recommendation:** keep the original, and open newer files read-only. | "Migrate forward" says what is named, not what is kept. The newer-version case is absent (W4-03). |
| W4Q-4 | Crash safety | May the disk-sync setting be turned off entirely, or does it have a longest allowed interval? **Recommendation:** a maximum, with no "never". | "Allow it to be tuned" does not say whether it can be off. If it can, SC-8's power-loss guarantee holds only by default (W4-06b; re-asks W3Q-2). |

---

## Summary

No blocker or high, so Warden's lens adds no stopping-rule trigger. All six findings are fix-induced from round-3 fixes, or variants of round-3 findings. The loop is converging, not grinding. Round 3's design-shaped gate problems have shrunk to:
- event keying (W4-01, W4-02, W4-04);
- one stale cross-reference sweep (W4-05);
- one filing label (W4-06);
- one data-retention gap in a newly ruled branch (W4-03).

The most consequential is W4-01: as written, Gate B is a trip-wire no mechanism can fire. Part of that traces to Warden's own round-3 wording.
