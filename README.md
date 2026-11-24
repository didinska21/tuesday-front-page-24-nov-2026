[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/didinska21/tuesday-front-page-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/didinska21/tuesday-front-page-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124)

# THE WORLD — Tuesday 24 November 2026

One day of world news, one picture: a complete newspaper front page for
Tuesday 24 November 2026, drawn entirely in code (Python + PIL) so that
every headline stays crisp and legible at any size.

**44 date-checked stories · 8 regions — each one happened, or was first
reported, on this Tuesday.**

- 6 illustrated lead stories: Asia's markets rocket in a chip rally,
  a dawn quake shakes Nepal, a Russian strike kills two in Zaporizhzhia,
  Seoul sounds an air alert over a Russian jet, a Himalayan flood leaves
  100 missing, and America takes off for Thanksgiving.
- 38 numbered briefs across all 8 regions, each carrying a colour-coded
  region tag.
- A masthead with the day's counts, a one-line UTC timeline of the day,
  a region key with per-region story counts, and a footer stating the
  date-check rule: if it did not happen on Tuesday, it is not on the page.

## How it runs

`main.ts` (Node 22, standard library only) copies the bundled `entry.png`
into the output directory as `entry.png` — byte-identical on every run.
`draw_frontpage.py` is the program that drew the page; run it with
Python 3 + Pillow to regenerate `entry.png` from the story data.
