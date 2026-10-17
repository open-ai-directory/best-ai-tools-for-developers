# Contributing

Thanks for helping keep this list useful. Adding a tool takes about two minutes.

## Adding a tool

Open a PR that adds one `<tr>` row to the relevant category's table in `README.md`, in this exact format:

```markdown
<tr>
<td width="48"><img src="assets/icons/tool-slug.png" width="32" height="32" alt="Tool Name icon"></td>
<td><strong><a href="https://example.com">Tool Name</a></strong><br><sub>One factual sentence on what it does and who it's for. <code>PricingTag</code></sub></td>
</tr>
```

Add the icon at `assets/icons/tool-slug.png` (32×32 or larger, square, transparent/white background preferred) — a site favicon is fine. Grab one quickly with:

```sh
curl -sL "https://www.google.com/s2/favicons?domain=example.com&sz=128" -o assets/icons/tool-slug.png
```

Rules:

- **Alphabetical order within the category**, by tool name. CI checks this automatically — if your PR fails the check, just re-sort and push again. It's not a judgment on the tool.
- **Exactly one pricing tag**, one of: `` `Free` ``, `` `Freemium` ``, or `` `Paid` ``. If the vendor only offers custom/enterprise pricing with no public number, use `` `Paid` `` and add `(enterprise/custom pricing)` after it.
- **Extra badges are welcome alongside the pricing tag** — e.g. `` `Open Source` ``, `` `Self-Hosted` ``, `` `Free for OSS` `` — as additional `<code>` tags after it. Keep it to one or two; don't turn the row into a badge wall.
- **Description ≤ 160 characters**, factual, no superlatives ("best," "revolutionary," "leading"). Say what it does and who uses it.
- **One tool per PR is preferred** (easier to review), but not required.
- Don't add yourself/your own product without disclosing it in the PR description — that's fine, we just want to know.

## What gets a tool rejected

- Not a live product (waitlist, "coming soon," defunct, or the link 404s).
- No pricing information anywhere, public or sales-gated (we need *some* signal, even "contact sales").
- Not actually used by developers — a generic tool with one tangential dev use case doesn't qualify.
- Already listed (check the category first).

## Suggesting a new category

Categories are meant to track real developer workflows, not generic tech buckets. [Open a "Suggest a category" issue](../../issues/new/choose) explaining what workflow it covers and why it doesn't fit an existing category.

## Reporting a dead link

[Open a "Report broken link" issue](../../issues/new/choose), or just fix it yourself in a PR — removals are welcome.

## Review

PRs are reviewed by the repo's [CODEOWNERS](.github/CODEOWNERS). CI runs a formatting/lint check and a link check automatically; a green check doesn't guarantee a merge, but a red one means it needs another look before anyone reviews it.
