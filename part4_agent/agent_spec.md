\# Meesho Reseller Growth \& Alert Intelligence — Agent Specification



\## 1. GOAL



Keep category managers informed about categories whose Month-over-Month (MoM) change is beyond the 8% threshold.



A human must approve any drafted message before it can be sent.



The agent must never automatically send a message.



\---



\## 2. TOOLS



The agent uses:



1\. `validate\_feed()` from `part2\_engine/growth\_engine.py`

2\. `mom\_growth()` from `part2\_engine/growth\_engine.py`

3\. `is\_flagged()` from `part2\_engine/growth\_engine.py`

4\. The Part 3 narrative template-fill logic



The Part 2 functions must be reused without modification.



\---



\## 3. MEMORY / STATE



The agent maintains the previous month's verified revenue for every category.



For each category, the state contains:



\- category

\- previous month

\- previous revenue

\- current month

\- current revenue

\- MoM percentage

\- flag status



\---



\## 4. PLANNER



The agent follows this exact sequence:



1\. Load the monthly revenue feed.

2\. Run `validate\_feed()`.

3\. If validation fails, perform a hard stop. Record the validation errors and do not calculate MoM or create drafts.

4\. If validation succeeds, calculate `mom\_growth()` for every category against the previous month.

5\. Run `is\_flagged()` for every category.

6\. Sort flagged categories by absolute MoM percentage in descending order.

6b. Draft messages for at most the top 3 flagged categories by magnitude.

7\. Log remaining flagged categories beyond the top-3 cap as `suppressed, review manually`.

7b. Separately log exact-boundary categories in `escalated\_categories`. Do not merge them with flagged or suppressed categories.

8\. Emit one structured JSON object for the run.



\---



\## 5. FEEDBACK LOOP / HUMAN APPROVAL



Every drafted message is held for human approval.



The system may simulate an approval decision for testing, but it must not send email, SMS, or any other external message.



No SMTP or real messaging service is required.



\---



\## 6. GUARDRAILS



\### Input Guardrail



`validate\_feed()` must pass before any MoM calculation or narrative drafting.



\### Action Guardrail



No message is automatically sent.



Messages are only drafted and held for human approval.



\### Output Guardrail



Every number in a draft must trace back to the verified Part 1 data and Part 2 calculations.



The agent must not invent figures or unsupported business facts.



\---



\## 7. INVALID FEED BEHAVIOUR



When the feed is invalid:



\- `validation\_status` must be `"invalid"`.

\- `action\_taken` must be `"hard\_stop"`.

\- All validation errors must be included.

\- No MoM calculations are performed.

\- No drafts are created.

\- `flagged\_categories` must be empty.

\- `suppressed\_categories` must be empty.

\- `escalated\_categories` must be empty.



\---



\## 8. TOP-3 CAP



The agent drafts at most 3 flagged categories.



Flagged categories are sorted by:



`abs(mom\_pct)` descending.



The first 3 are drafted.



Any remaining flagged categories are logged as:



`suppressed, review manually`



The top-3 cap is intentional and prevents too many notifications from being drafted in one run.



\---



\## 9. EXACT-BOUNDARY HANDLING



A category with exactly 8.0% absolute MoM change receives:



`escalate\_exact\_boundary`



It must be stored separately in `escalated\_categories`.



It must not be merged into either `flagged\_categories` or `suppressed\_categories`.



\---



\## 10. ACCEPTANCE SCENARIOS



\### May



Expected flagged categories by absolute MoM magnitude:



1\. Ethnic Wear: +77.10%

2\. Western Wear: -23.60%

3\. Kids Wear: -23.48%

4\. Home \& Kitchen: -9.25%

5\. Beauty \& Personal Care: -12.75%



Top 3 are drafted:



\- Ethnic Wear

\- Western Wear

\- Kids Wear



The remaining two are suppressed.



\### June



Expected flagged categories:



1\. Ethnic Wear: -58.74%

2\. Home \& Kitchen: +42.59%

3\. Kids Wear: +23.90%

4\. Western Wear: +11.97%



Beauty \& Personal Care is +5.67% and is not flagged.



Top 3 are drafted:



\- Ethnic Wear

\- Home \& Kitchen

\- Kids Wear



Western Wear is suppressed.



\---



\## 11. STRUCTURED JSON OUTPUT



Each run must emit one JSON object with exactly these top-level keys:



```text

run\_month

validation\_status

validation\_errors

flagged\_categories

suppressed\_categories

escalated\_categories

action\_taken

