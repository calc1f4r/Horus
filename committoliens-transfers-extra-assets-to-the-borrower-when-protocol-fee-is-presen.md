---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7304
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - wrong_math
  - business_logic

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

commitToLiens transfers extra assets to the borrower when protocol fee is present

### Overview


This bug report is about a problem with the AstariaRouter.sol and VaultImplementation.sol contracts. The totalBorrowed amount is the sum of all commitments[i].lienRequest.amount. However, when the ifs.feeTo is set, some of the funds/assets from the vaults get transferred to s.feeTo when_handleProtocolFee is called, and only the remaining is sent to the ROUTER(). This can lead to a situation where the total amount of assets sent to ROUTER() is more than the totalBorrowed, due to rounding errors. To fix this issue, the recommendation is to make sure only (1 �np
dp)T is transferred to the borrower. Both Astaria and Spearbit have acknowledged the bug report.

### Original Finding Content

## Severity: High Risk

## Context
- AstariaRouter.sol#L417-L422
- VaultImplementation.sol#L392

## Description
`totalBorrowed` is the sum of all `commitments[i].lienRequest.amount`. But if `s.feeTo` is set, some of the funds/assets from the vaults get transferred to `s.feeTo` when `handleProtocolFee` is called, and only the remaining is sent to the `ROUTER()`. 

In this scenario, the total amount of assets sent to `ROUTER()` (so that it can be transferred to `msg.sender`) is subject to rounding errors:

\[
(1 - \frac{np}{dp})T
\]

Where:
- \( T \) is the `totalBorrowed`
- \( np \) is `protocolFeeNumerator`
- \( dp \) is `protocolFeeDenominator`

But we are transferring \( T \) to `msg.sender`, which is more than we are supposed to send.

## Recommendation
Make sure only \( (1 - \frac{np}{dp})T \) is transferred to the borrower.

## Acknowledgements
- **Astaria**: Acknowledged.
- **Spearbit**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Wrong Math, Business Logic`

