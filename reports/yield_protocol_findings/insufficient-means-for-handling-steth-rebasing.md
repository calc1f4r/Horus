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
solodit_id: 60119
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Insufficient Means for Handling stETH Rebasing

### Overview


A bug has been reported in the EToken project. The issue is that the code is not properly accounting for stETH rewards when users deposit stETH into a trove. This results in excess stETH accumulating in the ActivePool and DefaultPool. The client has acknowledged the bug and recommends implementing extensive testing to ensure proper handling of stETH's rebasing mechanism. The affected files are EToken.sol, TroveManager.sol, ActivePool.sol, and DefaultPool.sol.

### Original Finding Content

**Update**
At the moment, shares and balance are equivalent. That is to say, shares are not currently being recorded.

Marked as "Acknowledged" by the client. The client provided the following explanation:

> EToken will maintain the same rebasing mechanism as the corresponding collateral. For rebase tokens, the protocol records the share value.

**File(s) affected:**`EToken.sol`, `TroveManager.sol`, `ActivePool.sol`, `DefaultPool.sol`

**Description:** When a user deposits stETH into a trove they recieve eTokens equivalent to the deposit amount. However, stETH rebases such that an address holding stETH will gradually receive more stETH over time. As of now, the codebase does not display any mechanism for allowing borrowers who collateralize stETH to claim these rewards. This will result in excess stETH accumulating in `ActivePool` and `DefaultPool`.

**Recommendation:** Fully handle stETH's rebasing mechanism in the contracts so that each user's stETH collateral rewards are correctly accounted for. We recommend implementing extensive testing on this front to ensure that everything is working as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

