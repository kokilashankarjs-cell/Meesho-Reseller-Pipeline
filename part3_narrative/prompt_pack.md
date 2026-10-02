# Part 3 Narrative Prompt Pack

## 1. Trigger

Create a business alert narrative when a category's Month-over-Month (MoM) revenue movement requires review.

## 2. Input List

Category: {category}
Previous Revenue: {previous_revenue}
Current Revenue: {current_revenue}
MoM Growth: {mom_pct}
Current Month: {month}
Previous Month: {prev_month}

## 3. Prompt

Use the supplied inputs only.

### Context

State the category, previous-month revenue, current-month revenue, and the months being compared.

### Insight

State the calculated MoM percentage as a FACT.

### Implication

Explain a possible business reason only as a HYPOTHESIS.
Do not present an unverified cause as a FACT.

Use this structure:

Context → Insight → Implication

FACT = directly supported by the supplied data.

HYPOTHESIS = possible explanation that requires business verification.

## 4. Checklist

- Use only supplied numbers.
- Keep all revenue values traceable to the input.
- Keep MoM percentage traceable to the calculation.
- Clearly separate FACT and HYPOTHESIS.
- Do not invent business causes.
- Keep the narrative suitable for a category manager.
- Include a practical follow-up for human review.