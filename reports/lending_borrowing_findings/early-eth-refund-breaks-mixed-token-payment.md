---
# Core Classification
protocol: Algebra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57981
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Limit%20Order%20Plugin/README.md#3-early-eth-refund-breaks-mixed-token-payment
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Early ETH Refund Breaks Mixed-Token Payment

### Overview


The report describes a bug in the Limit Order Manager that interrupts liquidity provision. When a user supplies ETH and a non-native token, the payment process fails because the contract refunds all ETH back to the user before the second payment is processed. This is considered a medium severity bug as it blocks legitimate actions. The recommendation is to refund the surplus ETH after both payments are processed. The bug has been fixed in the latest commit.

### Original Finding Content

##### Description
In `LimitOrderManager.algebraMintCallback()` the debts to the pool are paid in order: first `token0`, then `token1`.

When `token0` is not `wNativeToken` but `token1` is, and the user supplies ETH with the call:

1. `_pay(token0, …)` executes the ERC-20 branch, transferring `token0` from the user.
2. The final `if (address(this).balance > 0)` line refunds all ETH held by the contract back to the payer, even though it will be needed momentarily.
3. `_pay(token1, …)` now finds the contract’s ETH balance at zero, cannot wrap ETH into `WNativeToken`, and reverts.

The order fails despite the user providing sufficient ETH, interrupting liquidity provision and forcing a retry. 

This finding has been classified as **Medium** severity because legitimate actions are being blocked.
<br/>
##### Recommendation
We recommend refunding the surplus ETH after both payments are processed.

> **Client's Commentary:**
> Fixed. Commit: https://github.com/cryptoalgebra/plugins-monorepo/commit/417edc77ad50789fb16fbab50d697b29e967cca6

---

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | MixBytes |
| Protocol | Algebra Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Limit%20Order%20Plugin/README.md#3-early-eth-refund-breaks-mixed-token-payment
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

