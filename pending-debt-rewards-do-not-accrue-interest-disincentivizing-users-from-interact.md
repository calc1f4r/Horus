---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60131
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Pending Debt Rewards Do Not Accrue Interest, Disincentivizing Users From Interacting with Protocol

### Overview


The client has reported a bug in the `TroveManager.sol` file where interest on debt is not being accrued when a trove is liquidated and the debt is added to the `DefaultPool`. This means that borrowers can avoid paying interest on their debt by waiting to adjust or close their trove. The client recommends that debt should accrue on USDE in the `DefaultPool`.

### Original Finding Content

**Update**
We disagree with the reasoning provided in the client's explanation, as whether debt is allocated or pending allocation is a consequence of a gas-saving implementation detail.

Marked as "Acknowledged" by the client. The client provided the following explanation:

> We think that this part of the debt has not been actually allocated to trove, so the interest should not be accumulated.

**File(s) affected:**`TroveManager.sol`

**Description:** When liquidating a trove, one possibility is for the debt and collateral of that trove to be liquidated across all remaining active troves. This is done by adding the funds to the `DefaultPool` and applying the debt and collateral to an applicable trove (via `TroveManager.applyPendingRewards()`) when it is being adjusted, when it is being closed, and when it is being redeemed against. However, while debt is held in `DefaultPool`, interest is not accrued against it as it does not count towards the debt of an active trove.

As a result, it would be in a borrower's interest to, with all else being equal, wait for as long as possible to adjust a trove or close it, as doing so would allow them to avoid paying interest on pending debt rewards.

**Recommendation:** Consider having debt accrue on USDE that is in `DefaultPool`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

