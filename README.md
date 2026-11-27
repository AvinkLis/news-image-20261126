# The Daily Picture — Thursday, 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/AvinkLis/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/AvinkLis/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A newspaper front page that sums up 26 November 2026's world news in
a single image — drawn entirely in code with Pillow, no photographs,
no external assets. Entry for the
[make.fun news-image-20261126 competition](https://make.fun/bounty/news-image-20261126).

## The stories on the page

- **Lead — United States:** A powerful storm batters Thanksgiving:
  roofs torn off, streets flooded, hundreds of thousands without
  power, thousands of flights delayed.
- **Ukraine:** Russia launches missiles and 113 drones at Ukrainian
  cities, killing at least three; Zelensky tells the BBC the US is
  too focused on the Middle East.
- **Gaza:** Israeli strikes kill eight Palestinians, among them a
  Hamas political official and his wife, testing the ceasefire.
- **Kuwait:** A drone attack kills two Italian technicians; the
  strike is blamed on Iranian drones and Tehran denies it.
- **Egypt:** The Giza fire death toll rises to 31.
- **Myanmar:** Myanmar rejects parts of the ICJ ruling that convicted
  it of genocide against the Rohingya minority.
- **In brief:** a cheaper HIV prevention jab reaches Africa; nine
  injured in a Bangkok refinery explosion; Duran Duran guitarist
  Andy Taylor dies at 65; Mumbai marks 18 years since 26/11.

Sources: BBC, Reuters and AP wires, WebIndia123 — every story
checked in at least two independent reports before it was drawn.

The delivered image is 1024×1024 pixels and 157,622 bytes — inside
the competition's 1024×1024 and 1 MiB limits.

## Run it

`main.py` is standard library only. It takes the finished artwork
(`entry.png`, or the base64 copy `entry.png.b64` that the grading
sandbox's text-only checkout carries), verifies the whole PNG chunk
by chunk with CRCs, and copies it to the output folder:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The artwork itself is drawn by `make_image.py` (kept outside this
repository as build tooling; it needs Pillow and is only used locally).
