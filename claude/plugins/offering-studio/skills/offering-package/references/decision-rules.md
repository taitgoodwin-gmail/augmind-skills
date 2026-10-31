# Decision rules: which outputs an offering needs

Answer each rule from the input the deck was built from. Cite the sentence the answer rests on. Unknown counts as no. Record the answers in `decisions.json`:

```json
{
  "brand": "levarum",
  "frame": "product",
  "rules": {
    "A1": {"answer": true, "basis": "Weekly runs ... on n8n at launch (architecture review, Oct 21)"},
    "P1": {"answer": true, "basis": "Next.js with Cognito (architecture review, Appendix A)"}
  },
  "outputs": {"architecture": "full", "home_page": true, "prototype": "full"}
}
```

Vocabulary, exactly: `frame` is `service`, `product` or `hybrid`; `architecture` is `full`, `card` or `none`; `prototype` is `full`, `screens` or `none`; `home_page` is always `true`. `brand` is the pack id (a folder name under `brands/`) or an absolute path to a pack.

Answer all seven rules (A1 to A4, P1 to P3). When no sentence in the input answers a rule, the answer is `false` and the basis is exactly `Not stated in the input; unknown counts as no.`, followed by one short line on what would make it true if the decision makers know otherwise. That way every answer has a basis a reader can check, and an unknown is never mistaken for a quoted fact.

Keep to the keys above. The one extra key allowed is `open_items`: a list of short strings naming what the input leaves open that could change an answer (for example "How Example Co gets into the client's content system; if Example Co holds the credentials, A4 is true and architecture becomes full"). Reasons for the outputs belong in the rule bases, not in new keys, because `offering-package` and the checker read this file by its keys.

## Architecture

| Rule | True when |
|---|---|
| A1 | A deliverable exists only while software the brand runs is running. |
| A2 | The offering reads from or writes to a client or third-party system by API, export, webhook or login. |
| A3 | The brand holds client data outside the client's own systems. |
| A4 | The brand manages hosting, accounts or credentials for the offering. |

- Two or more true: **full** architecture (systems, flows, data held, who hosts, decisions already made).
- Exactly one true: **card** (card only). One architecture card goes on the deck's deliverables slide; no separate output.
- None true: **none**.

## Prototype

| Rule | True when |
|---|---|
| P1 | A buyer or user works in a screen the brand controls. |
| P2 | The user gets value without a person from the brand doing the work for that user. |
| P3 | The thing changes by release, not by engagement. |

- P1 and P2: frame **product**, prototype **full** (the core journey).
- P1 and not P2: frame **hybrid** (a service with a portal), prototype **screens** (only the screens the home page shows).
- Not P1: frame **service**, prototype **none**.
- P3 breaks ties only.

## Home page

Always built. The only question is whether a live site exists; if it does, the page is a proposed replacement for its home page and says so in the build note.
