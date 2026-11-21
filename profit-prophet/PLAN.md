# Profit Prophet: operating plan, Nov 22–28

Written Sat Nov 21, 4:25 p.m. ET. **Nothing live was verified in this session.** The Mac mini isn't connected, and this cloud container is blocked from the platforms. Every claim about live state comes from the 8:39 a.m. handoff, now about 8 hours old. Recheck it on the Mac before any write.

## 1. Check first on the Mac (time-sensitive)

1. **Today's 11 a.m. Instagram carousel** was queued locally and not confirmed at 8:39 a.m. Find its receipt or the live post. If its state is unknown, reconcile it. Don't rerun it, and don't move it into an hourly slot.
2. **The hourly rotation's stop.** Hourly posting is authorized only while the Meta ad runs, and the ad ends **Wed Nov 25, 7:30 a.m. ET**. Find what actually stops the job: an ad-status check or a hard end date. If it has neither, that's the first fix, with Mike's OK. Confirm it really stopped around 8:30 a.m. Nov 25.
3. **"Make the Offer Clear" on TikTok at 6 p.m. tonight** is scheduled in Studio. Confirm it went live, then fill in its row in the scorecard.

Read-only inventory commands. They print job schedules, never credentials:

```bash
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/profit-prophet-yt && git status -sb && git log --oneline -5
launchctl list | grep -iE 'profit|prophet|queue|post'
ls ~/Library/LaunchAgents; crontab -l | grep -vE '^\s*[A-Za-z_]+='   # drop env/key lines
# per plist: read only these keys, never EnvironmentVariables
plutil -extract ProgramArguments json -o - <plist>; plutil -extract StartCalendarInterval json -o - <plist>
```

Output to produce: one row per **platform × slot** with the writer (job or tool), its time zone, where its queue lives, where its receipt lands, and whether it runs locked or needs a browser session.

## 2. Seven-day lineup

Existing queues keep their slots until a cutover is agreed. New pieces go only into open slots. **Empty slots are on purpose: no filler.**

| Day (ET) | Locked: existing owners, don't touch | New: proposed, needs Mike's OK + one writer | Measure |
|---|---|---|---|
| Sun 22 | Hourly IG/FB/Threads · 9:30 FB/Threads · 11:00 IG · 6 p.m. TikTok | None. Finish the 3 pieces below | Design Room #01 at 24h (~8 a.m.) |
| Mon 23 | Same (last day of the 11:00 IG queue) | None | |
| Tue 24 | Hourly · 9:30 FB/Threads (last day) · 6 p.m. TikTok (last day) | None (hourly would bury anything new) | Design Room #01 at 72h (~8 a.m.) |
| **Wed 25** | Ad ends 7:30; hourly must stop | 9:30 FB/Threads + 11:00 IG: **Design Room #02**. 6 p.m. TikTok + YouTube Short: **Kairo, "The River Is Rising"** | Confirm hourly stopped |
| Thu 26 (Thanksgiving) | — | Threads only: a native text post that follows up Design Room #02 | Both Nov 25 pieces at 24h |
| Fri 27 | — | 9:30 FB/Threads + 11:00 IG: **before/after demo** (the control) | |
| Sat 28 | — | 6 p.m. TikTok + YouTube: Design Room #02 process cut, **only if rendered and QA'd** | Both Nov 25 pieces at 72h |
| Sun 29 | — | Existing audience review. Coordinate with its owner; don't add a second check | Demo at 72h falls on Nov 30 |

- Holiday traffic on Nov 26–28 is abnormal. Note "holiday" on those scorecard rows, and only compare within the same platform and age.
- Black Friday and Small Business Saturday: the handoff has no promotion, so don't invent a discount. If Mike wants a sales post, it gets its own slot and uses only real shop products with their exact variants.

## 3. The three pieces to finish first (existing assets, no-cost edits)

**A. Kairo, "The River Is Rising"** (12 s; finished and privately QA'd per the handoff; not uploaded)
- Finish: frame 1 must be action, not a title card. If it opens on a card, trim to the first action frame. Keep the required AI and platform disclosures. Use a one-line caption, and never say or imply that the full episode is out.
- Hypothesis: an action-first beat that resolves inside the clip holds viewers better than tutorials. Baseline: the Nov 18 Kairo clip held **29%** of its length (3.78 of 13 s). The Nov 20 tutorial held **12%** (2.36 of 20 s). Most viewers left in the first 1–2 s.
- Pass: watch ratio of 29% or more, plus a better 2-second hold than Nov 18, at both 24h and 72h. One clip is not a verdict; the lane needs 3 comparable beats.
- If people watch but don't follow, fix the series identity (same character, same opening sting, end on a reason to return), not the animation.

**B. Design Room #02, Built Not Given long-sleeve**
- Facts: Mike asked for the long-sleeve version, and a development teaser already ran. Don't put the long-sleeve decision to a vote.
- To confirm on the Mac: the final design file, and whether it's a real shop product. If it isn't, label it a concept.
- Format: frame 1 is the finished design, full bleed, with the hook on the frame. Frames 2–3 show the one design decision that changed from tee to sleeve. The last frame asks one question about a detail people can actually see. Never "thoughts?". If people are shown, they're Black men or women in accurate fits. No logo-on-a-blank-tee hero shot.
- Hypothesis: a specific, visible design question earns genuine replies. In Nov 14–20, 47 hourly images earned 1 Instagram like and 4 Threads views.
- Pass: more genuine replies plus saves per 1k reach than Design Room #01 at the same age. If reach is under 100, it's a distribution problem, not a creative verdict.
- Thursday's Threads follow-up: one line, text only, about something people have a stake in (for example, how they wear a long sleeve). Don't copy the image caption.

**C. Before/after demo** (prepared and unpublished per the handoff; post it in the format it was prepared in)
- Its role: the control, not the brand's identity. Frame 1 puts the result next to the "before". No sales call in it.
- Hypothesis: useful contrast earns saves and shares, and gives the two lanes a benchmark.
- Read: shares plus saves per 1k reach against A and B, same platform and age.

## 4. The one change after the baseline

When the ad ends Nov 25, **let hourly companion posting end, and don't replace it with another rotation.** Run at most one original post per platform per day from the two lanes, and log each one in the scorecard. The evidence: in Nov 14–20, 47 hourly images produced 1 Instagram like and 4 combined Threads views. Volume isn't producing reach.

How to prove it won't duplicate. This needs the Mac inventory first, so it isn't proven yet:
- The writer table from section 1 shows exactly one writer per platform and slot.
- No new slot overlaps an existing queue.
- `score.py` flags any repeated `source_hash` on the same platform.

## 5. Decision for Mike

**Approve "The River Is Rising" for TikTok Wed Nov 25 at 6 p.m. plus a YouTube Short the same evening?** TikTok would go through the existing Studio scheduling owner. YouTube would go through the existing one-off authorized path, and the local queue worker stays disabled.

## 6. Cutover rules (only after Mike says go)

- Name one writer per platform and slot, in writing, before the first write.
- Before each write, check the platform for the same `source_hash` or caption in the last 7 days.
- A timeout or uncertain write gets reconciled, never blindly retried. Never backfill missed slots.
- Every publish leaves a receipt (platform ID, permalink, ET and UTC time, source hash) that becomes a scorecard row.
- Rollback: unschedule or delete only our own post, and hand the slot back to its previous owner.

## 7. Scorecard

`python3 profit-prophet/scorecard/score.py profit-prophet/scorecard/scorecard.csv`. Read-only, standard library only, Python 3.9 or later. It exits with code 1 if the data checks find problems.

- One row per post per checkpoint (`checkpoint_h` = 24 or 72). A row with no `checkpoint_h` holds identity only (prepared, scheduled, or published, but not yet measured).
- **Blank = not measured. 0 = measured zero.** Instagram reach, saves, and shares were unavailable in the handoff, not zero, so leave them blank.
- It compares only within the same platform, checkpoint, and organic/paid bucket. It drops rows measured outside ±25% of the checkpoint and makes no series call from fewer than 3 posts.
- Website visits and paid orders are reported apart from engagement, using each post's latest checkpoint only.
- `scorecard.csv` is seeded with the 6 posts whose permalinks are in the handoff, with no measures. Its notes say which fields to fill from receipts.
