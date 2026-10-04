---
# Core Classification
protocol: Arkis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59952
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
source_link: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Julio Aguilar
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Lenders Provide an Interest-Free Loan if the Protocol Has Insufficient Liquidity

### Overview


The client has acknowledged an issue where users may not receive their withdrawal from a pool if there is not enough liquidity. This results in users not receiving rewards and essentially providing an interest-free loan to the protocol. The recommendation is to continue accumulating rewards for users until they receive their liquidity back and to consider calling `debt.tryRepay()` on `deposit()` calls to speed up the repayment process. The affected file is `Pool.sol`.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We understand this issues and this is the part of the business logic. If a pool does not have liquidity but user decided still to withdraw he will be first in the withdrawal queue by refusing to receive interest.

**File(s) affected:**`Pool.sol`

**Description:** When `withdraw()` is called, the pool may lack the liquidity for a Liquidity Provider to withdraw their position. In this case, their position is deleted after tallying their debt in a queue. Positions are repaid as rewards are distributed via `returnAndDistribute()`.

While a perfect liquidation mechanism could guarantee that all positions are eventually repaid, liquidity providers are not guaranteed to receive their withdrawals within any clear time horizon. In the meantime, they no longer accumulate rewards, resulting in providing an interest-free loan to the protocol.

**Recommendation:** Keep accumulating rewards for liquidity providers until they receive back their liquidity. To help speed the repayment process, consider calling `debt.tryRepay()` on calls to `deposit()` as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Arkis |
| Report Date | N/A |
| Finders | Julio Aguilar, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/arkis/07924f14-1727-4e72-8e7a-2bc71aa735dd/index.html

### Keywords for Search

`vulnerability`

