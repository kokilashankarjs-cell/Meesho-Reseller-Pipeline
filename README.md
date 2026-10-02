\# Meesho Reseller Growth \& Alert Intelligence Pipeline



\## Project Overview



This project builds one integrated monthly monitoring pipeline:



SQL → Python Guardrails → Narrative → Agent → Human Approval



The pipeline validates data, calculates Month-over-Month growth, identifies significant category movements, creates stakeholder-ready drafts, and holds them for human approval.



No message is automatically sent.



\## Dataset



The dataset is generated using the exact supplied script and fixed seed.



Expected dataset:



\- 24 resellers

\- 900 orders

\- April, May, June 2026

\- 5 categories

\- 4 regions



\### Regenerate the Dataset



From the project root:



```powershell

cd data

python generate\_dataset.py

