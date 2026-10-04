---
# Core Classification
protocol: RipIt_2025-05-10
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62614
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-05-10.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-17] Missing refund in `SpinLottery.sol` when prize distribution fails

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

In the `SpinLottery.sol` contract, the `fulfillRandomness()` function contains an issue related to prize distribution failures. When a user pays for a spin, their payment is processed immediately, but the actual prize is distributed asynchronously after Chainlink VRF provides randomness.
The relevant code in `fulfillRandomness()` is:
```solidity
// Step 3: Prize Selection
try this._distributePrize(req.player, requestId, rarity, prizeRandom) {
    // Prize distributed successfully
} catch {
    // If prize distribution fails, emit a no-win event
    emit NoWin(req.player, requestId);
}
```

When the prize distribution fails. The contract simply emits a NoWin event without refunding the user's payment. This scenario is particularly problematic in cases such as:
When a lottery manager calls `configureRarity()` to add a new rarity but hasn't yet added any NFT prizes using `addPrize()`.

Recommendations:
When prize distribution fails in the catch block, the contract should refund the user's payment, so you need to keep track of the exact amount paid by each user for each spin to ensure accurate refunds.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RipIt_2025-05-10 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-05-10.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

