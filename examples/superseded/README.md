# Superseded specs

Specs kept for the record that must **not** be rendered in a batch.

`bin/sankey.py` names its output from the spec's own `ticker` and `period`, not from the
filename, so two specs for the same company-quarter write the same `charts/<TICKER>-<PERIOD>.json`.
A loop over `examples/*.json` then renders whichever sorts last, silently.

- `tsm-q3-fy26-usd.json` — TSMC Q3 FY26 in USD, transcribed from the App Economy Insights
  reference image. Replaced by `examples/tsm-q3-fy26-filed.json`, which uses the filed NT$
  figures and matches the KPIs on the card.
