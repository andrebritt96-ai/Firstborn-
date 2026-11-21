#!/usr/bin/env python3
"""Profit Prophet scorecard: read-only summary of a publication CSV.

    python3 score.py scorecard.csv [--min-basis 100]

Rules this enforces (from the Nov 21 handoff):
  * Blank cell = not measured (unknown). "0" = measured zero. Blanks are never treated as 0.
  * Posts are compared only within the same platform, checkpoint age (24h / 72h) and
    organic-vs-paid bucket. Rows measured outside the checkpoint window are excluded.
  * Tiny reach is reported as a distribution problem, not as a creative verdict.
  * No series call is made from fewer than 3 comparable posts.
  * Website visits and paid orders are reported separately from engagement.

Reads the CSV only. Writes nothing, calls no network, needs no packages (Python 3.9+).
"""
import argparse
import csv
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
IDENTITY = ["platform", "series", "format", "permalink", "published_et", "published_utc",
            "hook", "length_s", "source_hash", "paid"]
WINDOW_TOLERANCE = 0.25  # 24h checkpoint accepts 18-30h; 72h accepts 54-90h
MIN_COMPARABLE = 3


def num(v):
    v = (v or "").strip().replace(",", "")
    return None if v == "" else float(v)


def parse_et(s):
    s = (s or "").strip()
    return datetime.fromisoformat(s).replace(tzinfo=ET) if s else None


def parse_utc(s):
    s = (s or "").strip()
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "")).replace(tzinfo=timezone.utc)


def per_1k(x, basis):
    return None if x is None or not basis else x / basis * 1000


def sum_present(*vals):
    present = [v for v in vals if v is not None]
    return sum(present) if present else None


def med(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def fmt(v, pct=False):
    if v is None:
        return "–"
    if pct:
        return f"{v * 100:.0f}%"
    return f"{v:.1f}" if v != int(v) else str(int(v))


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--min-basis", type=float, default=100,
                    help="reach/views below this is 'underpowered' (default 100)")
    a = ap.parse_args()

    with open(a.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    problems, posts, measured = [], {}, []
    for line, r in enumerate(rows, start=2):
        pid = (r.get("post_id") or "").strip()
        if not pid:
            problems.append(f"line {line}: missing post_id")
            continue
        ident = {k: (r.get(k) or "").strip() for k in IDENTITY}
        if pid in posts and posts[pid] != ident:
            problems.append(f"line {line}: `{pid}` identity columns differ from its first row")
        posts.setdefault(pid, ident)

        try:
            pub_et, pub_utc = parse_et(r.get("published_et")), parse_utc(r.get("published_utc"))
            meas = parse_utc(r.get("measured_utc"))
        except ValueError as e:
            problems.append(f"line {line}: `{pid}` bad timestamp ({e})")
            continue
        if pub_et and pub_utc and abs((pub_et - pub_utc).total_seconds()) > 60:
            problems.append(f"line {line}: `{pid}` published_et and published_utc disagree")
        pub = pub_utc or pub_et

        cp = num(r.get("checkpoint_h"))
        if cp is None:
            continue  # identity-only row: prepared/scheduled/published, not yet measured

        reach, views = num(r.get("reach")), num(r.get("views"))
        basis_name, basis = ("reach", reach) if reach is not None else ("views", views)
        if basis is None:
            basis_name = "–"
        length, watch = num(r.get("length_s")), num(r.get("avg_watch_s"))
        m = {
            "pid": pid, "platform": ident["platform"], "series": ident["series"] or "?",
            "paid": ident["paid"] or "?", "cp": int(cp), "basis_name": basis_name, "basis": basis,
            "watch_ratio": watch / length if watch is not None and length else None,
            "hold_2s": (num(r.get("hold_2s_pct")) / 100) if num(r.get("hold_2s_pct")) is not None else None,
            "replies_1k": per_1k(num(r.get("genuine_replies")), basis),
            "shares_saves_1k": per_1k(sum_present(num(r.get("shares")), num(r.get("saves"))), basis),
            "follows_1k": per_1k(num(r.get("follows")), basis),
            "follows": num(r.get("follows")),
            "site_visits": num(r.get("site_visits")), "paid_orders": num(r.get("paid_orders")),
        }
        if not pub or not meas:
            m["status"] = "missing publish/measure time"
        else:
            age = (meas - pub).total_seconds() / 3600
            if abs(age - cp) > WINDOW_TOLERANCE * cp:
                m["status"] = f"off-window (measured at {age:.0f}h)"
            elif basis is None:
                m["status"] = "distribution unknown"
            elif basis < a.min_basis:
                m["status"] = "underpowered"
            else:
                m["status"] = "ok"
        measured.append(m)

    print("# Profit Prophet scorecard\n")
    print(f"Source: `{a.csv}` · {len(posts)} publications · {len(measured)} measurements · "
          f"min basis {a.min_basis:.0f}\n")

    print("## Data checks\n")
    dupes = defaultdict(set)
    for pid, i in posts.items():
        if i["source_hash"]:
            dupes[(i["platform"], i["source_hash"])].add(pid)
    for (plat, h), ids in sorted(dupes.items()):
        if len(ids) > 1:
            problems.append(f"possible duplicate publication on {plat}: same source_hash `{h[:12]}` "
                            f"in {', '.join(sorted(ids))}")
    print("\n".join(f"- {p}" for p in problems) if problems else "- none")

    print("\n## Per measurement\n")
    print(table(
        ["post", "platform", "series", "paid", "age", "basis", "watch", "hold 2s",
         "replies/1k", "shares+saves/1k", "follows/1k", "status"],
        [[m["pid"], m["platform"], m["series"], m["paid"], f'{m["cp"]}h',
          (f'{fmt(m["basis"])} {m["basis_name"]}' if m["basis"] is not None else "–"), fmt(m["watch_ratio"], True), fmt(m["hold_2s"], True),
          fmt(m["replies_1k"]), fmt(m["shares_saves_1k"]), fmt(m["follows_1k"]), m["status"]]
         for m in sorted(measured, key=lambda m: (m["platform"], m["cp"], m["series"], m["pid"]))]
    ) if measured else "No measurement rows yet.")

    print("\n## Distribution (diagnose before judging creative)\n")
    dist = defaultdict(list)
    for m in measured:
        if m["basis"] is not None and not m["status"].startswith(("off-window", "missing")):
            dist[(m["platform"], m["cp"], m["paid"])].append(m["basis"])
    lines = []
    for (plat, cp, paid), b in sorted(dist.items()):
        mb = statistics.median(b)
        verdict = ("fix distribution first" if mb < a.min_basis else "enough to compare creative")
        lines.append([plat, f"{cp}h", paid, len(b), fmt(mb), verdict])
    print(table(["platform", "age", "paid", "posts", "median basis", "read"], lines) if lines
          else "No reach/views recorded yet. Unknown is not zero.")

    print("\n## Series comparison (status ok only)\n")
    groups = defaultdict(list)
    for m in measured:
        if m["status"] == "ok":
            groups[(m["platform"], m["cp"], m["paid"], m["series"])].append(m)
    lines = []
    for (plat, cp, paid, series), ms in sorted(groups.items()):
        lines.append([plat, f"{cp}h", paid, series, len(ms),
                      fmt(med([x["watch_ratio"] for x in ms]), True),
                      fmt(med([x["hold_2s"] for x in ms]), True),
                      fmt(med([x["replies_1k"] for x in ms])),
                      fmt(med([x["shares_saves_1k"] for x in ms])),
                      fmt(med([x["follows_1k"] for x in ms])),
                      "compare" if len(ms) >= MIN_COMPARABLE else f"n<{MIN_COMPARABLE}: no call"])
    print(table(["platform", "age", "paid", "series", "n", "med watch", "med hold 2s", "med replies/1k",
                 "med shares+saves/1k", "med follows/1k", "read"], lines) if lines
          else "No comparable measurements yet.")

    print("\n## Website and orders (kept separate from engagement)\n")
    latest = {}  # cumulative counts: use each post's latest checkpoint only, never sum 24h + 72h
    for m in measured:
        if m["pid"] not in latest or m["cp"] > latest[m["pid"]]["cp"]:
            latest[m["pid"]] = m
    biz = defaultdict(lambda: [None, None])
    for m in latest.values():
        k = (m["series"], m["paid"])
        biz[k][0] = sum_present(biz[k][0], m["site_visits"])
        biz[k][1] = sum_present(biz[k][1], m["paid_orders"])
    lines = [[s, p, fmt(v), fmt(o)] for (s, p), (v, o) in sorted(biz.items()) if v is not None or o is not None]
    print(table(["series", "paid", "site visits", "paid orders"], lines) if lines
          else "None recorded. Site visits are not orders; only a traced paid order counts as revenue.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
