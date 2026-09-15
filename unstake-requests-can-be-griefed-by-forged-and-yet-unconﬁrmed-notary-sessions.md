---
# Core Classification
protocol: Lombard Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46306
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/3a1c4f65-6ef7-4d26-97f4-480f8093801d
source_link: https://cdn.cantina.xyz/reports/cantina_lombard_december2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Haxatron
  - dontonka
  - Bernd
---

## Vulnerability Title

Unstake requests can be griefed by forged and yet unconﬁrmed notary sessions 

### Overview


This bug report discusses an issue with the Lombard ledger system where notary sessions can be submitted without permission. This can lead to forged unstake receipts being used to prevent users from receiving their unstaked BTC. The recommendation is to only mark an unstake request as paid if the associated receipt has been confirmed by the required number of notaries. The issue has been fixed in a recent update. 

### Original Finding Content

## Context
`unstake.go#L184-L187`

## Description
Notary sessions can be permissionlessly submitted to the Lombard ledger through the `MsgSubmitPayload` Cosmos SDK message (`msg_server_submit_payload.go#L13-L41`). Although a quorum of authorized notaries is needed for confirmation, any notary session, unconfirmed or confirmed, is retrieved by the approver and processed thereafter.

When processing an unstake receipt, the associated unstake request will be marked as paid (`unstake.go#L185`) in `processReceipt()`, so long as the receipt is not expired yet. This measure is intended as a safety guard to prevent multiple payouts for the same unstake request.

However, by prematurely marking an unstake request as paid, the approver will reject it, as it cannot match the UTXO output with an unpaid unstake request. As a result, it errors (`lombard_unstake.go#L139`) with "no valid unpaid unstake notarization found on Ledger" in `validateUnstakingOutput()`. Consequently, forged unstake receipts can be used to grief users by preventing them from receiving their unstaked BTC.

## Recommendation
When processing unstake receipts in `processReceipt()`, consider only marking the associated unstake request as paid if the receipt has the status `notarytypes.Completed`, i.e., it has been confirmed by the required quorum of notaries.

## Lombard
Fixed in PR 72.

## Cantina Managed
Fix looks good.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Lombard Finance |
| Report Date | N/A |
| Finders | Haxatron, dontonka, Bernd |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_lombard_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/3a1c4f65-6ef7-4d26-97f4-480f8093801d

### Keywords for Search

`vulnerability`

