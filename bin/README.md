# Morning brief refresh

`morning-brief.sh` regenerates `brief.json` (the site's Morning Brief tab)
and pushes it, so the page is current before the open.

It runs **locally, not as a cloud routine**: the cloud routine environment
blocks network egress to the quote and news sources this needs
(`EGRESS_BLOCKED` on every fetch), so a scheduled cloud agent cannot do it.

## One-time setup

The script calls `claude -p`, which needs its own credentials — the
desktop app's session is not enough, and a headless run currently fails
with `401 OAuth access token has been revoked`. Mint a token first:

    claude setup-token

Then confirm a headless call works:

    claude -p "Reply with exactly: OK" --model claude-sonnet-5

## Install the schedule

    cp bin/com.kevinyang.morning-brief.plist ~/Library/LaunchAgents/
    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.kevinyang.morning-brief.plist

Runs weekdays at 6:00 local time. launchd reads the machine clock, so it
stays at 6am across daylight saving changes — unlike a UTC cron.

## Check on it

    launchctl print gui/$(id -u)/com.kevinyang.morning-brief   # status
    ./bin/morning-brief.sh                                     # run now
    tail -f bin/morning-brief.log                              # watch output

## Remove it

    launchctl bootout gui/$(id -u)/com.kevinyang.morning-brief
    rm ~/Library/LaunchAgents/com.kevinyang.morning-brief.plist

## Related

- `quotes.py --pe` — refresh forward P/E in `heatmap.html`
- `quotes.py --events` — refresh `events.json` earnings and ex-dividend dates
- Catalyst routine (cloud) — currently fails on the same egress block;
  see https://claude.ai/code/routines
