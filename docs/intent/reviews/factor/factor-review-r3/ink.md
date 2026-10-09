# Ink review, round 3: product brief Stage 1 (Intake), clarity lens

**Reviewed:** `docs/intent/factor.md` at `93d6c53` (383 lines). Checked against `docs/decisions.md` (D-003, D-008, D-016, D-018, D-022, D-023, D-024, D-026, D-031), `CLAUDE.md`, `docs/design/ui-brief.md` §7, `docs/design/feature-verdicts.md` (F-009, F-043, F-044), my round-2 review, and `git diff 8de9127 HEAD` over the brief, `CLAUDE.md` and `decisions.md`, which shows what each finding's fix changed. I didn't read the other round-3 reviews.

**Lens:** same as rounds 1 and 2. I looked for ambiguous phrasing, undefined terms, cross-references that don't resolve, inconsistent names and unlabelled inference. The audience is internal and agent-primary, so em-dashes and stylistic tells aren't findings. Nothing inside a Peter quote is flagged.

**Checked and clean:**
- **No stale `Q-F` ids.** `grep -rn 'Q-F[0-9]' docs CLAUDE.md` returns nothing. The control, `grep -c 'FQ-8' docs/decisions.md`, returns 1, so the instrument works.
- **`I-1` is unique.** `grep -rn 'I-1\b' docs` hits only the brief's two uses (lines 70 and 230).
- **SC-4 arithmetic** holds against the §7 recipes. §7 states those recipes were checked against `en-US.json` on 2026-10-08; I took that claim from §7 and did not re-run it. The miner at 2/3 gives 80/min, so the smelters run at 80/90 = 8/9. Downstream clocks go from 3/4 to 3/4 × 8/9 = 2/3. Reinforced Iron Plate comes out at 7.5 × 8/9 = 20/3, which is 5/6 short of the target. The round-up bound of 0.00005 percentage points is half of the fourth-decimal step.
- **CLAUDE.md's D-018 summary** was updated with the amendment, so the injected project instructions no longer carry the old "free up to a cap" default.
- **Decision names.** Every cited id resolves to a heading. D-012, D-025, D-028, D-031, D-032, D-035 and D-036 are named only by a paraphrase that sits next to the id (for example HC-7's title for D-031), not by the exact heading. F11 is dismissed, so I'm not raising this.

## Round-2 dispositions

- **N1** (SC-4 overdraw self-contradiction, D-022 drift, unlabelled acceptance): **resolved in the brief.** SC-4's lead sentence now says "The exact plan never overdraws". The round-up case cites Peter's round-4 "Say nothing", and D-022's Outcome is amended with the superseded wording kept. One residual sits outside the brief: D-022's **Context** line still reads "D-008 requires exact clock values to 4 decimal places that never overdraw a limited input", which restates the old rule in the decision SC-4 cites (R3-9).
- **N2** (stale provenance header, SC-7 unlabelled): **partly resolved.** SC-7's extension to plan files is now labelled. The new header has gone stale in a different way; see R3-8.
- **N3** (target increase past kept counts): **resolved** by "Add machines" in round 4. The fix opens a case that isn't covered (R3-3).
- **N4** (fixture wording and pre-ruling display strings): **resolved.**
- **N5** (machine definition too wide): **resolved** in the glossary. One small residual is in R3-9.
- **N6** (HC-10 capability vs behaviour): **partly resolved.** The "Now" bullet is concrete: screen-reader support is a toolkit capability, while keyboard reach and contrast are first-build behaviour. The bullet carries no source label, and D-031's accessibility line still has the old ambiguous wording (R3-9).
- **N7** (SC-5 criterion vs check): **resolved** on the text: a core change outside the declared extension points fails SC-5. Whose ruling that is isn't stated (R3-8).
- **N8** (two definitions of first build; *shape* entries): **partly resolved.** The glossary now gives one content-keyed definition. SC-1 still says "The first build's content is the parity list against Modeler", and that content now explicitly includes backend-only structure for 29 *shape* entries, which Peter can't compare against Modeler (R3-9).
- **N9** (ids): **resolved.** I-1 and FQ-1 to FQ-9 are in place, and nothing stale remains (control above).
- **N10** (HC-7 merged bullet, ordering): **resolved.**
- **N11** (FQ-3 is product intent): **resolved.** Both the section intro and HC-7 say its answer comes back to Peter.
- **N12** (small trips): **resolved** on all four points: the Mac is recorded per measurement, memory covers all processes, and the RP-1 one-to-one wording is gone. The SC-3 edit-list fix removed "cap", and SC-9 now has its own pin list, which brings back an overlap in a new form (R3-1).
- **N13** (SC-9 release target for a count): **resolved** by "Re-minimise that node" in round 4.

## Findings

### R3-1 · medium · fix-induced (rounds 4 and 5) · Caps dropped out of the pin list, the register still commits them, and target rate went into the list
**Anchor:** SC-9 line 96; SC-3 line 61; F-009 line 278; D-024 Outcome; D-018 amendment.
- **Caps.** D-018's amendment makes an extractor's ceiling "derived from them, never typed". After that, SC-3's edit list dropped "a cap change", and SC-9's Puck's-reading list of pin kinds leaves out cap, even though Peter answered SC-9 with "a cap" among the question's examples. **F-009 Per-resource caps** is still Committed *mvp*, and its verdict-sheet description is "Set a per-minute maximum for each raw resource (default: the whole map's supply)", which is a typed value. D-024's Outcome still lists "cap an input" as a diagram edit. A cold agent can't tell whether typed caps exist in the first build. The drop rests on the words "never typed", which appear in D-018 only after the "Miner sets the cap" option label. The record doesn't show whether they were the option's wording or Puck's summary of it, and Peter's own words in the same entry say he changes the ceiling "manually to a percentage". Two readings fit: F-009 is a separate map-wide limit that sits alongside the per-extractor ceiling, or it has been folded into D-018's amendment. The brief should say which (Domain Question 2).
- **Target rate.** SC-9's list now includes target rate. Its release rule ("Other kinds return to factor's choice") and its check ("observe the value return to factor's choice") can't apply to a target, because factor never chooses one. The glossary's "any value Peter sets that the solver must keep" also takes in targets. That makes SC-3's "a target change, a change to a miner's or extractor's settings, or setting or releasing a pin" list three overlapping things, which is N12's first point coming back.
- *Suggested:* take target rate out of SC-9's list, or give it its own release rule. Then state F-009's standing after D-018.

### R3-2 · medium · fix-induced (round 5, HC-11 new) · HC-11 puts RP-3's security review at first share, and RP-3 fires it earlier
**Anchor:** HC-11 lines 133–140; RP-3 line 169; FQ-8 line 209.
HC-11 says the listed obligations "wait for the first time factor is used by anyone other than Peter", and the list includes "network-feature security review (RP-3)". RP-3 says that review re-triggers "when **any** feature with network, credential or external-model reach enters a slice's scope, not only 'sharing'". RP-3's own words, "not only 'sharing'", mean the review can fall due before first share. To illustrate: if F-083 New-version notice (Idea tier today) were promoted into a slice that only Peter runs, its review would wait under HC-11 and wouldn't under RP-3. FQ-8 treats the two as separate triggers ("the first-share gate (HC-11) and RP-3's re-trigger"), so HC-11 is the line that's off. A reader using HC-11 as the gate list will defer exactly the review RP-3 was written to keep from waiting on sharing.
*Suggested:* drop RP-3 from HC-11's list, or reword it as "network features used by others (RP-3 fires earlier, per slice)". This one sits in Warden's lens too.

### R3-3 · medium · fix-induced (round-3 rewording, round-4 ruling) · SC-6 leaves two cases open
**Anchor:** SC-6 lines 80–85; SC-9 line 97; D-016.
- **A pinned count when the target rises.** The new ruling says factor "adds the fewest new machines needed", and "A clock above 100% appears only where Peter has pinned it". When Peter has pinned a node's *count* but not its clock, adding machines would break the pin, overclocking isn't licensed, and nothing says the remaining choice, a named shortfall (D-023), applies. A pinned count is the normal case (§7's edit example pins Iron Plate to 4), and three implementers would pick three behaviours (Domain Question 1).
- **"After an edit" now covers a recipe swap.** The round-2 text said "After a target or cap change", and the new text says "After an edit". A recipe swap on an existing node (F-025, *mvp*) can change the machine type, for example from a Constructor recipe to an alternate made in an Assembler. "Existing machine counts stay as they are" means nothing across machine types. The Puck's reading on "a node an edit creates" may or may not cover it, depending on whether a swap counts as creating a node (Domain Question 3).

### R3-4 · medium · fix-induced (round 5, SC-7 check list new) · SC-7's fixture list contradicts its own ruling and pre-decides FQ-4
**Anchor:** SC-7 lines 86–89; FQ-4 line 205; RP-2 line 168.
- **"A missing reference" is rejected whole.** Directly above it (line 88), Peter's round-5 choice says a plan that refers to recipes or items a game update removed **opens**, with each affected node named as a problem. A recipe that no longer exists is a missing reference, so on that reading the check rejects what the criterion says must open. That's N7's shape again: the criterion and the check disagree. If "missing reference" means a broken internal link, such as an edge to a node id that isn't in the file, say so, and add a fixture for the removed-recipe case that asserts the plan opens.
- **"An unknown or foreign owner id" is rejected.** FQ-4 asks what owner id an imported plan file gets, and it's open. Rejection is one answer to it. Re-stamping the plan with the local owner is another. The fixture settles FQ-4 by the back door. *Suggested:* "an owner id the FQ-4 answer rejects", or leave it out of the list until FQ-4 is answered.

### R3-5 · low · fix-induced (round 5) · SC-8 has two Peter choices that disagree, and one unlabelled default
**Anchor:** SC-8 lines 90–95.
- **Two choices.** SC-8 still cites "Yes, lose at most the last edit" (round 2). The power-loss bullet, from round 5, can lose up to the sync interval, which by Peter's suggested default is 10 seconds or 10 edits. The reconciliation (round 2 governs a process crash, round 5 governs power loss) is the obvious reading, but the text doesn't say it, and a reader sees two rulings by Peter that don't agree.
- **"Whichever comes first"** isn't in Peter's words ("maybe every 10secs or 10edits"). It's a reasonable reading of them, but it's unlabelled.
- **Write versus sync.** A completed edit is one "whose new numbers were displayed", and every completed edit must survive a process crash. So the write has to land before the display, inside SC-3's window, and only the sync to disk can sit outside it. The Puck's-reading line places only "the sync" outside, which is right, but a reader who takes "sync" to mean "save" will move the write out as well. "The write happens before the numbers show, and the sync to disk runs outside SC-3's window" would close it.

### R3-6 · low · fix-induced (round 5) · SC-3 doesn't say where "visible" is measured, and the stale marking is unlabelled
**Anchor:** SC-3 lines 61–65.
The numbers must be visible within 100 ms, and the redraw follows within 1 s. The UI brief puts them on the nodes ("What a node shows", `ui-brief.md` line 53: machine count, clock, and the rates on the edges). If they stay there, then "numbers visible" already needs part of the diagram redrawn, and "redraw" must mean re-layout. If they live in a separate panel, the diagram's labels can lag by up to a second, and they aren't covered by the stale-marking rule, which covers only "numbers from the previous solve" before the new numbers land. A test author needs to know which surface the instrument watches. The stale-marking requirement also isn't part of the option Peter chose ("Under 1 second"), and it carries no **Puck's reading** label.

### R3-7 · low · fix-induced (round 4) · SC-6's second check has no start state and doesn't exercise "evenly"
**Anchor:** SC-6 line 85.
"Raising the target from 7.5 to 10/min adds machines, with none above 100%." The following is my arithmetic from §7's recipes. From the first-solve state, 10/min needs 120 ingots/min, so one smelter is added. Every other node lands at exactly 100% on its kept count, and the miner runs at its 120/min ceiling.
- **Start state.** If the check runs after the SC-4 miner pin (80/min), the result is a shortfall, not added machines. The check should say "from the first solve".
- **Coverage.** Every node ends at exactly 100%, so an implementation that adds one machine at full clock and leaves the others alone gives the same numbers as one that "re-clocks all of them evenly". A target such as 9/min (smelters 4 at 90%) would tell the two apart.

### R3-8 · low · fix-induced (rounds 4 and 5) · Provenance labels lag the answers
**Anchor:** lines 37–42; SC-5 line 77.
- **The header** says "His review answers (rounds 1 to 4…)", but SC-3's redraw bound, SC-7's removed-recipe rule and SC-8's sync setting cite round 5. SC-4 cites rounds 3 and 4, and it isn't in the header's list at all. SC-7 appears only under "Review findings", though it now carries a Peter choice. Each criterion cites inline, so the cost is that the header can't be trusted as an index. Replacing it with "each SC names its source inline" removes something that has to be kept up to date.
- **SC-5's "fails SC-5 for that game"** settles N7 by choosing one of the two options I offered. SC-5 is listed as resting on Peter's chosen label, and the failure rule carries no label. I looked for a record that Peter was asked: the commit bodies of `93e3fc5` and `93d6c53`, and the brief itself. I found none. Either label it **Puck's reading** or cite the round.

### R3-9 · low · residuals and small fix-induced trips
- **SC-1 parity list (N8 residual).** "The first build's content is the parity list against Modeler." Under the new glossary, that content includes backend-only structure for the *shape* entries. *Suggested:* "the *mvp* entries are the parity list."
- **HC-10 "Now" (N6 residual).** The keyboard requirement is backed by F-080 *mvp* and ui-brief item 12, so it's not new scope, but the bullet cites neither, and a cold reader can't tell it apart from Puck's addition. D-031's accessibility line still reads "the toolkit and design support screen readers … from the start", the wording N6 flagged. Updating it is for whoever owns `decisions.md`.
- **"Machine recipe" against the widened "machine" (N5 residual).** The glossary now makes extractors and generators machines. SC-2's "every machine recipe in the game: 291" counts manufacturer recipes only (CLAUDE.md: "291 are made in a machine"). That 291 includes no extraction recipes is my inference, not checked against the Docs data (the bundle isn't in this worktree): CLAUDE.md lists extractors under their own native classes, and D-018's extraction recipes are factor's own. "Every manufacturer recipe" would keep the count and the term aligned.
- **HC-4, extraction bullet.** "never typed" reads, in a Rust brief that also says "typed model" (HC-3), as a statement about the type system. It means "never entered by hand", and even that is loose, because Peter changes the miner's clock by hand (D-018 quote). "never entered directly; it follows from the extractor's settings" would avoid both readings. In the same bullet, "more than one node's ceiling needs more nodes" means "a rate above one node's ceiling needs more nodes".
- **D-022's Context line** (outside the brief) still says the displayed 4-decimal clocks never overdraw; see N1's disposition.
- **D-016's refinements** (outside the brief). The older "Refined" entry still ends "So fewest buildings applies at a first solve and on an explicit re-minimise". The "Refined further" entry above it adds a third case (a released count pin) without correcting that sentence. SC-6 has the right three-case list.
- **Not fix-induced; I missed these in round 2.** SC-3's "largest connected part" of a reference plan that SC-2 defines as "one connected plan" is the whole plan, so the qualifier either does nothing or means something narrower, such as the largest loop. The glossary's "Release note: the 'first build' or 'eventually' label" names two labels where line 222 has three.

## Domain Questions

1. **SC-6, a count you pinned and a rising target (R3-3).** You've pinned Iron Plate to 4 Constructors, and then you raise the target past what 4 at 100% make. What do you expect factor to do, and does it matter whether you also set their clock?
2. **F-009 caps after the miner ruling (R3-1).** Now that a raw resource's ceiling comes from its miner, node and clock, when would you still want to set a per-resource maximum yourself, and what would it be a maximum of?
3. **SC-6, swapping a recipe on a built node (R3-3).** When you swap a node to an alternate recipe made in a different building, what should happen to the machines that were there?
4. **SC-8, crashes and power loss (R3-5).** How do your round-2 answer ("lose at most the last edit") and your round-5 sync setting fit together? Which kinds of failure does each one cover?
5. **HC-11 and RP-3, timing of a network feature's security review (R3-2).** If a feature that reaches the network, such as the new-version notice, goes into a build only you use, when should its security review happen?
