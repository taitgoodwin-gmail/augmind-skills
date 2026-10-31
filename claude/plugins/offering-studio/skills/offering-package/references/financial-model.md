# Financial model

The model answers one question for the decision makers: what does it cost to deliver this offering to one customer, at what capacity, and at which price assumptions does it make money. It is an internal decision tool. Its figures never appear in the deck, the home page or the prototype; those keep the no-price rule.

## Source of truth: `financials.json`

Write `financials.json` in the build folder first. The spreadsheet is drawn from it, and a later revision changes the file, then redraws the sheet. Every figure is one line:

```json
{
  "brand": "levarum",
  "offering": "<offering name, as in the spec>",
  "currency": "USD",
  "as_of": "2026-10-30",
  "lines": [
    {"id": "C1", "group": "cost", "name": "Model API calls per customer per week", "low": 0, "base": 0, "high": 0, "unit": "USD per customer per week",
     "tag": "platform", "source": "<Publisher: short topic>", "url": "<page opened>", "opened": "2026-10-30", "basis": "<what the page says, in your words>", "card": "2.1.3"},
    {"id": "K1", "group": "capacity", "name": "Customers one analyst can support", "low": 0, "base": 0, "high": 0, "unit": "customers",
     "tag": "open", "basis": "Proposed by Claude. <Decision makers> to confirm."},
    {"id": "P1", "group": "price", "name": "Monthly price, single brand", "low": 0, "base": 0, "high": 0, "unit": "USD per customer per month",
     "tag": "open", "basis": "Proposed by Claude. <Decision makers> to confirm."}
  ]
}
```

- `group` is `cost`, `capacity`, `price` or `volume`.
- `tag` uses the deck's four tags with the same meaning. `platform` and `official` need `source`, `url` and `opened`, and the figure must be on the opened page (a vendor's own pricing page, a government wage table). `own` is a figure the brand has decided, with the record it was decided in. Everything else is `open`.
- Every price line is `open` unless the input records a brand decision. Claude never sets a price; it proposes a range.
- `card` names the deck card the cost line belongs to, where there is one, so a change to the offering shows which costs move.
- No figure from memory. If a vendor page will not open, the line is `open` with the reason.

## The sheet

Build it from the Sheets artifact type when the session lists one; otherwise build an .xlsx with the `xlsx` skill. Publish privately; never share it.

1. **Assumptions**: every line of `financials.json`, one row each, with low, base and high columns, the tag in words, and the source link.
2. **Unit economics**: per customer per month, in three scenarios: revenue, delivery cost, gross margin and gross margin percent, and people-hours per customer. Formulas only; no typed results.
   - **Downside**: every cost line at its high value, every price line at its low value, every volume line at its low value, every capacity line at its low value.
   - **Base**: every line at its base value.
   - **Upside**: the reverse of the downside: costs low; price, volume and capacity high.

   Do not take a column straight across the lines (all lows, all highs): that pairs the high price with the high costs and gives a scenario nobody would plan for. The lines' low and high are each line's own range; the scenarios decide which end of each range is bad news. Name the scenarios Downside, Base and Upside on the sheet.
3. **Capacity**: customers per person and per platform limit, and the first limit reached at each scale (10, 50, 200 customers), in the base and downside scenarios.
4. **Open items**: every `open` line, in the order it moves gross margin most, with the person who must confirm it.

A figure in sheets 2 to 4 is a formula over sheet 1. Label the sheet "Draft: open figures are proposals, not decisions."

## Check

Run `python3 <this skill>/scripts/check_financials.py <build folder>/financials.json`. It fails a line with no tag, a `platform` or `official` line with no source, URL or date opened, a line where low, base and high are out of order, and a price line tagged anything but `open` or `own`. Fix every line it prints, then build the sheet.
