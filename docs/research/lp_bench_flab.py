# /// script
# dependencies = ["highspy", "numpy"]
# ///
"""Whole-database LP over a FactorioLab dataset (crafts/s per recipe, item balance rows).

Columns: one per recipe (crafts/s), one surplus per item (penalised), one supply per item
that no recipe produces OR that a no-input (mining) recipe produces (cost 1).
Positive control: with only iron-plate and iron-gear-wheel recipes, 1 gear/s needs 2 ore/s.
Every solve is checked by conservation residual |A x + u - s - d|_inf.
"""
import json, sys, time, statistics
import numpy as np
import highspy

d = json.load(open(sys.argv[1]))
mined = {i for r in d["recipes"] if not r.get("in") for i in r.get("out", {})}
recipes = [r for r in d["recipes"] if r.get("in")]  # no-input (mining/pumping) recipes become supply columns
items = sorted({i for r in recipes for k in ("in", "out") for i in r.get(k, {})})
row = {i: n for n, i in enumerate(items)}
produced = {i for r in recipes if r.get("in") for i in r.get("out", {})}
items = sorted(set(items) | mined)
row = {i: n for n, i in enumerate(items)}
supply_items = [i for i in items if i not in produced or i in mined]

def build(targets, allow=None):
    use = [r for r in recipes if allow is None or r["id"] in allow]
    cost, starts, idx, val = [], [0], [], []
    for r in use:
        net = {}
        for i, a in r.get("in", {}).items(): net[i] = net.get(i, 0) - a
        for i, a in r.get("out", {}).items(): net[i] = net.get(i, 0) + a
        for i, a in net.items():
            if a: idx.append(row[i]); val.append(a)
        cost.append(0.0); starts.append(len(idx))
    for i in items:
        idx.append(row[i]); val.append(-1.0); cost.append(1e-3); starts.append(len(idx))
    for i in supply_items:
        idx.append(row[i]); val.append(1.0); cost.append(1.0); starts.append(len(idx))
    lp = highspy.HighsLp()
    lp.num_col_ = len(cost); lp.num_row_ = len(items)
    lp.col_cost_ = np.array(cost); lp.col_lower_ = np.zeros(len(cost)); lp.col_upper_ = np.full(len(cost), highspy.kHighsInf)
    dem = np.array([targets.get(i, 0.0) for i in items])
    lp.row_lower_ = dem; lp.row_upper_ = dem
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array(starts, dtype=np.int32)
    lp.a_matrix_.index_ = np.array(idx, dtype=np.int32)
    lp.a_matrix_.value_ = np.array(val)
    h = highspy.Highs(); h.setOptionValue("output_flag", False); h.passModel(lp)
    return h, lp, dem, len(use)

def residual(h, lp, dem):
    x = np.array(h.getSolution().col_value)
    A = np.zeros(lp.num_row_)
    st, ix, vl = lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_
    for j in range(lp.num_col_):
        for k in range(st[j], st[j + 1]): A[ix[k]] += vl[k] * x[j]
    return float(np.max(np.abs(A - dem)))

if "iron-gear-wheel" in row:
    h, lp, dem, _ = build({"iron-gear-wheel": 1.0}, allow={"iron-plate", "iron-gear-wheel"})
    h.run(); x = h.getSolution().col_value
    ore = x[lp.num_col_ - len(supply_items) + supply_items.index("iron-ore")]
    print(f"CONTROL 1 gear/s -> iron-ore {ore:.6f}/s", "PASS" if abs(ore - 2.0) < 1e-6 else "FAIL")

targets = {i: 1.0 for i in items if i.endswith("science-pack") and i in produced}
print(f"{sys.argv[1]}: recipes={len(recipes)} items={len(items)} supply={len(supply_items)} targets={len(targets)}")
sts = []
for _ in range(5):
    h, lp, dem, n = build(targets)
    t = time.perf_counter(); h.run(); sts.append(time.perf_counter() - t)
print(f"cols={lp.num_col_} rows={lp.num_row_} nnz={len(lp.a_matrix_.value_)} solve median {statistics.median(sts)*1e3:.1f} ms "
      f"[{min(sts)*1e3:.1f}-{max(sts)*1e3:.1f}] status={h.modelStatusToString(h.getModelStatus())} "
      f"residual={residual(h, lp, dem):.2e} active_recipes={sum(1 for v in h.getSolution().col_value[:n] if v > 1e-9)}")
