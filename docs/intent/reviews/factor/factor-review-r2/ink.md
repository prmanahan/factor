# Ink review, round 2: product brief Stage 1 (Intake), clarity lens

**Reviewed:** `docs/intent/factor.md` at `8de9127` (298 lines). Checked against `docs/decisions.md`, `docs/design/ui-brief.md` §7, `docs/design/feature-verdicts.md`, the round-1 reviews in `scratch/factor-review-r1/`, and `git show` of `b843aeb`, `1cd4a90` and `56a98ea` for what each revision changed.

**Lens:** same as round 1. Ambiguous phrasing, undefined terms, cross-references that don't resolve, inconsistent names, and unlabelled inference. Audience is internal and agent-primary, so em-dashes and stylistic tells are not findings, and nothing inside a Peter quote is flagged.

**Checked and clean, so these are not findings:**
- Register counts: 37 `F-` entries in Idea plus 105 in Committed make 142 (awk over the `- **F-` lines by section). Idea also holds one entry with no `F-` id; see N9.
- Every decision name cited in the brief matches its heading in `decisions.md` (D-001 to D-005, D-008, D-019, D-020, D-022, D-026, D-029, D-030, D-034 checked).
- Every reviewer id cited resolves: Warden WQ-2, WQ-3, WR-06, WR-07, WR-10, WTB-1 to WTB-8; Pixel F2, F6, F7; Glitch F9. `scratch/factor-review-r1/` is tracked in git, so the paths survive a clone.
- `V-Accessibility` resolves in the plugin canon (`canon/architecture-values.md:171`).
- The SC-4 arithmetic: 75% × 8/9 = 2/3, and the ui-brief's three plate constructors at 75% re-clock to 2/3 with counts kept, which is what SC-6's check asserts.

## Round-1 dispositions

- **F1** (SC-3's 100 ms unattributed): **resolved.** Peter chose "Numbers under 100 ms".
- **F2** (SC-3 check measures less than the criterion): **resolved.** The interval is now edit to updated numbers, timed outside the solver, with redraw explicitly excluded.
- **F3** (machine, megabase, node edit undefined): **resolved**, with a new ambiguity in the glossary's definition of machine (N5). One caveat, below finding level: the glossary's "Megabase: the SC-2 reference plan" turns Peter's loose term into Puck's constructed test plan with no **Puck's reading** label. The reference plan itself is Peter's choice ("Whole game, scaled up"), so the equation is reasonable. It's just unlabelled.
- **F4** (SC-4 fixture mis-stated and uncited): **resolved** on the clocks and the citation. The fix introduced N4.
- **F5** (the count rule behind "exact clocks"): **partly resolved.** SC-4 now states the clock formula for a given count, which is the computable part. Whether "fewest buildings" caps clocks at 100% is still unstated, and SC-6 now makes it matter on every edit (N3).
- **F6** (NG-4 vs F-081): **resolved.** F-081's line carries the D-034 limit.
- **F7** (NG-1 vs F-004): **resolved.** F-004 carries a labelled reading that ties it to #3924 and NG-1.
- **F8** (Check lines unlabelled): **resolved.** Line 37 and every Check line label them Puck's proposal.
- **F9** (F-002 tier vs D-017): **resolved** in `decisions.md`. D-017 now records *later* in round 1, changed to *skip* in round 2.
- **F10** (NG-5 leaning on open D-019): **resolved.**
- **F11** (bare decision ids): **dismissed** by the lead, and I accept that. One residual: line 13 still promises citation "by `D-NNN` id and name", and the dismissal's reason ("the glossary covers the terms") doesn't apply, because the glossary holds no decision names. Narrowing the line 13 promise to "by `D-NNN` id, with the name at first cite" would make it true at no cost.
- **F12** (terms a cold agent can't resolve): **resolved** by the glossary, except "clock". The gloss defines it as the game's setting "to 4 decimal places", which is Satisfactory's. Round 1 asked whether clock is game-neutral, and the gloss doesn't answer that. It stays low, and I'm not re-raising it as a finding.
- **F13** (EV-3 measured and observed run together): **resolved.**
- **F14** (SC-5 wording, `[ARCH-DEFERRED]` mechanism): **partly resolved.** The mechanism is carried as Q-F6, and "declared" now has a time anchor. The criterion and the check still disagree on one case (N7).

## Findings

### N1 · high · fix-induced (round 3) · SC-4 says displayed clocks never overdraw and then says they can, and D-022 still rules that they can't
**Why high:** the rating rests on the third bullet, an inference of Puck's attributed to Peter, which is round-1 F1's shape (rated high). The D-022 drift alone is F9's shape and would be medium.
**Anchor:** SC-4, line 47; D-022 Outcome in `decisions.md`; D-008.
- **Inside SC-4.** The third sentence says clocks "are shown to 4 decimal places as values the game accepts, and never overdraw a limited input". Four sentences later, "the 'never overdraw' clause applies to the exact plan", and a rounded-up shown clock "can draw up to 0.00005 percentage points more". The first sentence is still unqualified, so a reader who stops there gets the opposite rule.
- **Against the cited decision.** SC-4 cites D-022 Exactness. D-022 is **ruled**, and its Outcome still reads "Rounding for display never overdraws a limited input (D-008)". The round-3 supersession was written into D-008, and only into the "Puck's derivation, not ruled" part of it. D-022's ruled line wasn't touched. An agent following SC-4's cite to D-022 lands on the rule SC-4 has just relaxed. This is the same shape as round-1 F9.
- **Unlabelled inference.** "which Peter's ruling accepts" is attributed to Peter. His quote is about display consistency with the game ("in game the value is rounded to nearest, so i think consistent with the game is the correct answer"), and it says nothing about overdraw. Unless the round-3 question put the overdraw to him, the acceptance is Puck's reading and should carry the label.

*Suggested:* in the third sentence, "and the exact plan never overdraws a limited input". Then label the acceptance as **Puck's reading**, or quote the question Peter answered if it named the overdraw. Amend D-022's Outcome alongside D-008, which falls to whoever owns `decisions.md`.

### N2 · medium · fix-induced (rounds 1 to 3) · Line 37's provenance header is stale, and SC-7 has no source label
**Anchor:** line 37; SC-7, line 52.
- **The header.** Line 37 accounts for SC-1 to SC-6. It doesn't mention SC-7, SC-8 or SC-9, or the round-2 and round-3 answers that now sit inside SC-2 (memory) and SC-4 (display rounding).
- **SC-8 and SC-9** each cite Peter's choice inline, so they are covered in practice.
- **SC-7 cites no choice of Peter's.** It comes from Glitch round-1 F10, which proposed it "for Peter's decision". SC-7 calls itself D-003's ruling "made observable", but D-003 rules validation at load for **generated data files** only. SC-7 extends it to plan files, and it adds the named-error and never-partly requirements. Line 13 says every field is Peter's, ruled or labelled. SC-7 is none of the three, so a cold agent will read it as ratified.

*Suggested:* bring line 37 up to date, or replace it with "each SC names its source inline". Either label SC-7 **Puck's reading, extending D-003 to plan files**, or record Peter's choice if one was made.

### N3 · medium · fix-induced (round 1, SC-6) · SC-6 doesn't say what happens when the kept counts can't carry the new rate
**Anchor:** SC-6, line 49; SC-4, line 47; D-016.
"Existing machine counts stay as they are and only their clocks change" is fully specified for a decrease, which is the iron-chain fixture. On an increase, kept counts may need clocks above 100%. In Satisfactory that takes power shards (F-032) and stops at 250%. The brief doesn't say which of these happens:
- factor overclocks within the shard budget;
- factor adds machines despite SC-6;
- factor names a shortfall (D-023) and leaves re-minimising to Peter.

This is round-1 F5's open half: whether "fewest buildings" allows clocks above 100% at all. Peter's own example (two at 75% rather than one at 150%) implies a 100% ceiling, but nothing states it. Three implementers would build three behaviours. See Domain Question 1.

### N4 · medium · fix-induced (round 1 F4 fix, round 3 ruling) · The SC-4 fixture's wording and its cited source both disagree with the brief
**Anchor:** SC-4, line 47 ("Smelters go to 3 at 8/9"); `docs/design/ui-brief.md` §7 lines 233 and 240–241.
- **"Go to 3" reads as a count change.** In §7 the Smelters are already ×3 at 100%. With counts kept (SC-6) they stay at 3 and only re-clock. A fixture author could read "go to 3" as a re-minimise, which is the behaviour SC-6 rules out. *Suggested:* "Smelters stay at 3 and re-clock to 8/9".
- **The cited source predates the rounding ruling.** §7 (and §3, §8) shows the 8/9 clock as `88.8888%`. SC-4 now rules round-to-nearest, `88.8889%`. A fixture author who takes display strings from the source SC-4 points at will assert the truncated value. The ui-brief defect is outside the brief, as with Pixel F6. The brief can still stop the drift with one clause: "§7's exact fractions govern; its display strings predate the rounding ruling".

### N5 · medium · fix-induced (round 1, glossary) · "Machine" is defined wide enough to change the SC-2 target by a large factor
**Anchor:** Glossary line 100; SC-2, line 40.
"One building instance in the game (for example, one Constructor)". In Satisfactory, belts, lifts, pipes, splitters, mergers, power poles and foundations are all building instances. SC-2 scales the reference plan "to at least 5,000 machines". If logistics pieces count, the reference plan reaches 5,000 with far fewer production buildings than if they don't, so the two readings give very different solver and diagram loads. Extractors and generators are a smaller version of the same question: CLAUDE.md's count reads "**291 are made in a machine.**" My inference, unlabelled in either source: "machine" there means the manufacturer classes, so extraction, which D-018 models as a recipe of factor's own, isn't among the 291.
*Suggested:* "Machine: one production building instance (manufacturer, extractor or generator). Belts, pipes, splitters, power poles and other logistics or construction pieces don't count." Whether extractors and generators are in is Peter's call (Domain Question 3).

### N6 · medium · fix-induced (round 2, HC-10) · HC-10 can be read as requiring screen-reader support in the first build, or only a toolkit that allows it later
**Anchor:** HC-10, line 66; D-031's accessibility line.
The title says "shaped now and enforced on first share". The body says the toolkit and design "support screen readers, keyboard-only use and readable contrast from the start". One reader takes "support" as capability: pick a toolkit with an accessibility tree and design nothing that blocks it. The other takes it as behaviour: the first build works with VoiceOver. The second reading is close to the "Floor from the first build" option Peter rejected, and it would set first-build scope that he didn't choose. Q-F5 (non-visual diagram access) inherits whichever reading lands.
*Suggested:* "From the start, the UI toolkit and the design are chosen so that screen-reader, keyboard-only and contrast support can be added without a rewrite. The first build is not tested against the floor." Peter should confirm (Domain Question 5).

### N7 · medium · residual of F14 / WR-10 · SC-5's criterion allows a recorded core change, and its check fails one
**Anchor:** SC-5, line 48.
The criterion says "Any other core change is a recorded decision, so it can't land silently". That makes an undeclared core change permissible when it is recorded. The check passes only if "the diff to the core touches only declared extension points". So a recorded, deliberate core change passes the criterion and fails the check. *Suggested:* say which one governs. Either "a recorded core change fails SC-5 and is accepted as a known miss", or "the check passes when every core change outside declared extension points has a recorded decision".

### N8 · medium · fix-induced (rounds 1 and 3) · "First build" has two definitions, and neither says whether *shape* entries count
**Anchor:** Glossary line 105; SC-1, line 39; register tier mapping, line 137.
- **Two definitions.** The glossary defines first build by use: "the first release Peter uses for real play". SC-1 defines it by completion: "when every Committed entry marked 'first build' … has landed". Those come apart if Peter plays on an earlier release, and SC-1's question is asked at a different moment depending on which one holds.
- **Shape entries.** "Marked 'first build'" also matches the 29 *shape* register lines labelled "first build: backend structure only". SC-1 makes that set "the parity list against Modeler", and backend-only structure is no capability Peter can compare.
*Suggested:* use one definition, keyed on the register, e.g. "every *mvp* entry has landed and every *shape* entry's backend structure is in place", and say SC-1's parity list is the *mvp* entries.

(The 29 is `grep -c 'first build: backend structure only. Provenance' docs/intent/factor.md`. The same pattern without "Provenance" returns 30, because line 137 quotes the label once.)

### N9 · low · fix-induced (round 3, round-2 additions) · New identifiers without stable ids, and one scheme that collides by eye
**Anchor:** Idea tier line 145; "Questions carried to the Frame", lines 120–126.
- **The truncate-display entry has no id.** SC-4 can only refer to it by description ("a truncate-instead setting is an Idea-tier register entry"). Every other register entry has an `F-NNN`, and this entry isn't a catalogue feature, so it needs an id from a disjoint scheme. The same block also stretches line 138's mapping ("*skip* is Idea"), because this entry was never a *skip* verdict.
- **`Q-F` ids.** "Q-F1" reads as "question about F-001", and line 124 puts `Q-F5`, Pixel's `F2`/`F7` and feature `F-071` in one sentence. Something like `FQ-1` would make the scheme distinct at a glance.

### N10 · low · fix-induced (round 2) · Ordering and a merged bullet in HC-7
**Anchor:** lines 50–52, 62, 66–67.
- **HC-7, line 62.** The "**Tenancy:**" sub-item was merged onto HC-7's own line ("…not the full list. - **Tenancy:** …"), while Globalisation and Accessibility are indented sub-bullets beneath it. It renders as a literal dash mid-sentence, and Tenancy no longer reads as one of the three list members.
- **Order.** The success criteria run SC-6, SC-9, SC-8, SC-7, and the hard constraints run HC-8, HC-10, HC-9. A cold reader scanning for SC-7 or HC-9 finds them out of place. They should be renumbered or reordered, with ids kept stable if anything already cites them.

### N11 · low · fix-induced (round 2) · Q-F3 is product intent, not a Frame question, by the section's own test
**Anchor:** line 119 ("belonging to a later stage, not to product intent"); Q-F3, line 122.
Q-F3 asks whether input validation at the view-to-backend interface joins D-031's hard-to-retrofit list. That list is HC-7, a hard constraint, and its membership is Peter's to rule (D-031 is his). Warden WR-07 flagged it "for Peter and not decided here". Filed under Frame questions, it reads as an architecture choice the Frame can settle on its own. *Suggested:* keep it here but add "Peter rules whether it joins HC-7", or move it to an open item under HC-7.

### N12 · low · fix-induced (round 1) · Small resolutions a cold reader still trips on
- **SC-3's edit list overlaps the glossary** (line 45, line 103). "A target change, a cap change, or a pin": the glossary makes a cap one kind of pin, while D-024 lists pin a recipe, fix a count and cap an input as three edits. *Suggested:* "a target change, or setting or releasing a pin (recipe, machine count, cap)".
- **"On Peter's Mac"** (SC-3) isn't a reproducible reference for a budget test. D-017's measurements name an Apple M4. Name the machine once, or label it to be recorded at Frame.
- **SC-2's "the process stays under 1 GB"** (line 44). D-036's optional Tauri comparison arm renders in a system webview. A webview's content running in separate processes is my inference from how system webviews generally work; no source I read states it. "The process" can then be measured as the Rust process alone and pass while the app as a whole is far over. *Suggested:* "factor's total memory, across all its processes". This would rise to medium if a webview toolkit wins D-036.
- **RP-1, "Warden's appendix lists these as WTB-1 to WTB-8".** RP-1 has six bullets and the appendix has eight items. WTB-6 (Rust and native code) and WTB-7 (view and backend) aren't file inputs. "Maps these onto" or "covers these in" would avoid implying a one-to-one list.

### N13 · medium · fix-induced (round 3 SC-9 meeting round 1 SC-6) · SC-9's check depends on a "solver's choice" that SC-6 leaves undefined for machine counts
**Anchor:** SC-9, line 50; SC-6, line 49.
SC-9's check reads "release it, observe the value return to the solver's choice". For a recipe or a cap that is well defined. For a machine count, SC-6 holds that factor keeps existing counts and re-minimises only on Peter's explicit action. So when a pinned count is released, "the solver's choice" could be the count before the pin, the count SC-6 would have kept, or a fresh fewest-buildings count. A test author has to pick one, and SC-6's rejected option "Keep only what I pinned" shows that the pinned/kept distinction is load-bearing. *Suggested:* state the rule for released counts in SC-9, or carry it as an open item (Domain Question 2).

## Domain Questions

1. **SC-6, on a target increase.** When kept counts can't make the new rate at 100% clock, what should factor do? Is the answer different when power shards are available? This also settles whether D-016's "fewest buildings" ever overclocks (N3).
2. **SC-6 with SC-9, releasing a pinned count (N13).** When you release a machine count you pinned, where should it go: the count it had before you pinned it, a fresh fewest-buildings count, or something else? The SC-9 check needs this answer to know what "the solver's choice" is.
3. **SC-2, what counts toward 5,000.** In your big builds, which buildings would you count as machines? Production buildings only, or also miners, extractors and generators (N5)?
4. **SC-4, a rounded clock against a cap.** When you enter a rounded-up clock in the game and it draws a hair over a capped input, how do you treat that in practice, and should factor say anything about it (N1)?
5. **HC-10, the first build.** What should the first build itself do for screen-reader and keyboard-only use, as distinct from what the toolkit choice has to leave possible (N6)?
