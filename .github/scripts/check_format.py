#!/usr/bin/env python3
"""Enforce README.md formatting rules: alphabetical tool order, valid pricing tags,
description length. See CONTRIBUTING.md for the rules this checks.

Entries live inside an HTML <table> under each category, one <tr> per tool:

    <tr>
    <td width="48"><img src="assets/icons/slug.png" width="32" height="32" alt="Name icon"></td>
    <td><strong><a href="https://example.com">Name</a></strong><br><sub>Description. <code>Tag</code></sub></td>
    </tr>

Exactly one of the three canonical pricing tags (`Free`, `Freemium`,
`Paid`/`Paid (enterprise/custom pricing)`) must appear among an entry's
`<code>` badges; extra descriptive badges (`Open Source`, `Self-Hosted`, ...)
are allowed alongside it.
"""
import re
import sys

NON_CATEGORY_HEADINGS = {
    "table of contents",
    "how tools get listed",
    "quick comparison",
    "faq",
    "sponsors",
    "contributing",
    "more directories",
}

ENTRY_RE = re.compile(
    r'<td><strong><a href="(?P<url>[^"]+)">(?P<name>[^<]+)</a></strong>'
    r"<br><sub>(?P<rest>.*?)</sub></td>",
    re.DOTALL,
)
PRICING_TAG_RE = re.compile(r"^Free$|^Freemium$|^Paid$|^Paid \(enterprise/custom pricing\)$")
CODE_RE = re.compile(r"<code>([^<]+)</code>")
MAX_DESC_LEN = 160
SUPERLATIVES = {"best", "revolutionary", "leading", "top", "unrivaled", "unmatched", "#1"}


def heading_text(line):
    return re.sub(r"^#+\s*", "", line).strip()


def strip_emoji_prefix(text):
    return re.sub(r"^[^\w]+", "", text).strip().lower()


def main():
    with open("README.md", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Map each H2 heading to the line range of its section body.
    sections = []  # (category_name, start_line_idx, end_line_idx)
    current_category = None
    current_start = None
    for idx, line in enumerate(lines):
        if line.startswith("## "):
            if current_category is not None:
                sections.append((current_category, current_start, idx))
            current_category = heading_text(line)
            current_start = idx + 1
    if current_category is not None:
        sections.append((current_category, current_start, len(lines)))

    errors = []

    for category, start, end in sections:
        if strip_emoji_prefix(category) in NON_CATEGORY_HEADINGS:
            continue

        section_text = "\n".join(lines[start:end])
        section_offset = sum(len(l) + 1 for l in lines[:start])

        current_names = []
        for match in ENTRY_RE.finditer(section_text):
            lineno = content[: section_offset + match.start()].count("\n") + 1
            name = match.group("name")
            rest = match.group("rest")

            codes = CODE_RE.findall(rest)
            pricing_tags = [c for c in codes if PRICING_TAG_RE.match(c)]
            if len(pricing_tags) != 1:
                errors.append(
                    f"README.md:{lineno}: entry '{name}' must have exactly one "
                    f"pricing tag (`Free`, `Freemium`, or `Paid`), found {pricing_tags or 'none'}"
                )

            desc = CODE_RE.sub("", rest)
            desc = re.sub(r"\s+", " ", desc).strip()

            sort_key = name.lower()
            if current_names and sort_key < current_names[-1]:
                errors.append(
                    f"README.md:{lineno}: '{name}' is out of alphabetical order in "
                    f"'{category}' (comes after '{current_names[-1]}')"
                )
            current_names.append(sort_key)

            if len(desc) > MAX_DESC_LEN:
                errors.append(
                    f"README.md:{lineno}: description for '{name}' is {len(desc)} chars, "
                    f"max is {MAX_DESC_LEN}"
                )

            lowered = desc.lower()
            for word in SUPERLATIVES:
                if re.search(rf"\b{re.escape(word)}\b", lowered):
                    errors.append(
                        f"README.md:{lineno}: description for '{name}' contains "
                        f"superlative '{word}' — keep it factual"
                    )

    if errors:
        print(f"Found {len(errors)} formatting issue(s):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("README.md format check passed.")


if __name__ == "__main__":
    main()
