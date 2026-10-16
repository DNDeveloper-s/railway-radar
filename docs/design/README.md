# RailRadar UI build guide

This folder holds the finished design of the app and the rules for building it. Read this page once before you start any UI ticket.

## What is here

| File                    | What it is                                                                                                                                                                                                                                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RailRadar-design.html` | The design. Open it in Chrome. It shows three boards: **Desktop live map**, **Mobile train sheet** and **Mobile train details**. Use F12 (Elements) to inspect sizes, colours and spacing of any part. Comments in the source (`NAV RAIL`, `TOP BAR`, `MAP AREA`, `DETAIL DRAWER`) mark the sections. |
| `sample-data.json`      | All the sample data the design uses: 8 trains with timetables and crossings, 13 stations, Hindi station names, coach layouts, coach classes, fares, dates and quotas. **It is fake.**                                                                                                                 |
| `README.md`             | This guide.                                                                                                                                                                                                                                                                                           |

## Decisions already made

1. **One style.** The desktop board is the truth for colours and fonts. The mobile boards in the design use a slightly different palette and IBM Plex fonts; we do not. Build mobile with the desktop tokens.
2. **Status colours:** blue = on time, orange = delayed, coral red = cancelled. Green is only for the pulsing "live" dot and for available seats.
3. **Six tabs** in the train details, on desktop and mobile: Journey, Timetable, Coaches, Seats, Xings, Info.
4. **Breakpoint:** 900 px. In Tailwind it is the prefix `desk:` (for example `hidden desk:flex`).
5. **Map pieces are plain components.** `TrainMarker`, `StationMarker`, `MapControls` and so on do not import any map library and do not place themselves. Suraj puts them on the real map later.
6. **Everything uses fake data first.** Components take props. They never call `fetch`.

## Colour tokens (Tailwind classes)

| Token              | Hex                             | Used for                           |
| ------------------ | ------------------------------- | ---------------------------------- |
| `app`              | `#0A0F14`                       | page background                    |
| `panel`            | `#0D131A`                       | rail, top bar, fleet strip         |
| `drawer`           | `#0F161D`                       | details drawer, mobile sheet       |
| `surface`          | `#121A22`                       | inputs, cards                      |
| `card`             | `#151E27`                       | stat tiles, list cards             |
| `chip`             | `#18212A`                       | filled icon buttons, selected card |
| `glass`            | `rgb(15 22 29 / 0.92)`          | floating map controls              |
| `line`             | `#1A242E`                       | dividers                           |
| `line-bar`         | `#1F2B36`                       | borders of floating bars           |
| `line-strong`      | `#22303C`                       | input borders, tracks              |
| `line-hi`          | `#26333F`                       | selected segment, chip border      |
| `line-btn`         | `#2A3845`                       | small button borders               |
| `track`            | `#34434F`                       | upcoming station ring              |
| `ink`              | `#EAF0F5`                       | main text                          |
| `ink-soft`         | `#B7C4D0`                       | secondary text                     |
| `muted`            | `#8C9DAD`                       | labels                             |
| `faint`            | `#5E6F7F`                       | hints                              |
| `accent`           | `#FFCE1F`                       | brand yellow                       |
| `accent-soft`      | `#FFE27A`                       | link hover                         |
| `on-accent`        | `#111111`                       | text on yellow                     |
| `ontime`           | `#47B5FF`                       | on time                            |
| `delayed`          | `#FF9838`                       | delayed                            |
| `cancelled`        | `#FF8A65`                       | cancelled                          |
| `live`             | `#4BE39A`                       | live dot                           |
| `avl`, `rac`, `wl` | `#4BE39A`, `#FFD27A`, `#FF8A65` | seat status                        |

Use them as normal Tailwind classes: `bg-panel`, `text-muted`, `border-line-strong`, `text-ontime`, `bg-accent/15`.

## Fonts

| Class          | Font                 | Used for                                                         |
| -------------- | -------------------- | ---------------------------------------------------------------- |
| `font-display` | Big Shoulders        | train numbers, headings, big numbers (use `font-extrabold`, 800) |
| `font-sans`    | Instrument Sans      | body text                                                        |
| `font-mono`    | JetBrains Mono       | codes, times, counts                                             |
| `font-deva`    | Noto Sans Devanagari | Hindi station names (use `font-bold`, 700)                       |

The design file calls the display font "Big Shoulders Display". Google Fonts has merged that into one font called **Big Shoulders**, which is what we load. The browser picks the right optical size from the text size automatically.

All four fonts are loaded with `next/font/google`, so they are self-hosted and the browser never contacts Google.

## Animations

`animate-live` (pulsing green ring, for the live dot) and `animate-ring` (growing, fading ring, for the selected train). Always add `motion-reduce:animate-none`.

## Rules for every UI ticket

1. **No hard-coded colours.** No `#hex` and no `zinc-` classes in components. Use the tokens above.
2. **Props only.** A component gets everything through props. No `fetch`, no map library, no global state. State lives in the parent (assembly tickets).
3. **Real HTML.** Buttons are `<button>`, links are `<a>` or `<Link>`, lists are `<ul>`, tables are `<table>`. Icon-only buttons must have an `aria-label`.
4. **Keyboard.** Everything you can click can be reached with Tab and used with Enter or Space, and shows a visible focus ring (`focus-visible:ring-2 focus-visible:ring-accent`).
5. **Colour is never the only signal.** A status always has words.
6. **One component per file**, PascalCase file name, a typed `Props` interface, no `any`.
7. **Where files go:** atoms in `apps/web/src/components/ui/`, layout in `.../Layout/`, map pieces in `.../Map/`, fleet in `.../Fleet/`, train details in `.../Train/`, screens in `.../Screens/`. Pure helpers in `apps/web/src/lib/uiTrain.ts`. Types in `apps/web/src/types/ui.ts`. Fake data in `apps/web/src/data/uiMock.ts`.
8. **Check it side by side.** Make a temporary page `apps/web/src/app/dev/ui/page.tsx`, open it next to the design file, take screenshots, and **delete the page before you open the pull request**.
9. **Tests.** Once Vitest is set up (SCRUM-36), pure helpers get tests.
10. **Pull request:** use the branch name and commit message from the Jira Development panel, attach the two screenshots, tick the checklist.

## Build order (waves)

| Wave | What                                                                                 | Tickets                                                                                            |
| ---- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| 0    | Tokens, fonts, design files                                                          | foundation ticket (Saurabh)                                                                        |
| 1    | Atoms: badge, spinner, dot, progress bar, chips, segmented control, icons, fake data | StatusBadge/Spinner, LiveDot/ProgressBar, FilterChip/SegmentedControl, Icons/IconButton, fake data |
| 2    | Page shell: rail, top bar, stats and clock, search box, search dropdown              | NavRail, TopBar, StatsBar/LiveClock, search restyle, dropdown states                               |
| 3    | Map pieces: markers, controls, filters, fleet                                        | TrainMarker, StationMarker, MapControls, MapFilterBar, FleetCard, FleetStrip                       |
| 4    | Details drawer: shell, ribbon, board, stats, tabs and six tab contents, action bar   | drawer shell and its parts                                                                         |
| 5    | Mobile pieces and the two assembly tickets                                           | MobileTrainSheet, MobileTopControls, train page, desktop and mobile assembly                       |

Tickets in a wave can be done in any order. A ticket may not start before the tickets it says it **needs** are merged.

## What is fake in the design

| In the design                         | Real source?                                  | Plan                                                 |
| ------------------------------------- | --------------------------------------------- | ---------------------------------------------------- |
| Speed (km/h)                          | RailKit gives only an average speed per train | fake for now; may come from the schedule-speed spike |
| Seat availability, fares, Book button | none; booking is out of scope                 | fake, the button does nothing                        |
| Crossings and overtakes (Xings)       | Phase 3 prediction                            | fake                                                 |
| Coach layout                          | RailKit `coachPosition` text                  | fake layout now, parse real text later               |
| Follow, Arrival alert, Alerts bell    | needs accounts and notifications              | buttons only                                         |
| PNR, Saved, Settings pages            | not planned                                   | rail buttons only                                    |
| Exact train position and heading      | RailKit gives the station and distance only   | markers use fake coordinates and headings            |
| Map                                   | real map comes from the map spike             | the design draws a fake SVG map; ignore it           |
