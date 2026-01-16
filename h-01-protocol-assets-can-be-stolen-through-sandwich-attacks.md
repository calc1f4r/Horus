---
# Core Classification
protocol: Nftcapsule
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31399
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-NFTCapsule.md
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
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[H-01] Protocol assets can be stolen through sandwich attacks

### Overview


This bug report highlights a vulnerability in the `Capsule` contract that could result in the loss of protocol assets. This vulnerability is caused by a flaw in the slippage checks, which are used in various methods such as swapping and providing/removing liquidity. The issue arises when an attacker manipulates the pool with a large transaction, causing a significant decrease in the expected amount of assets received. This is followed by another transaction that restores the pool's price, resulting in a loss for the user. To prevent this, it is recommended to add an off-chain calculation for slippage tolerance in all methods that use it.

### Original Finding Content

**Severity**

**Impact:**
High, as protocol assets will be lost

**Likelihood:**
High, as sandwich attacks are very common and easy to execute

**Description**

The `Capsule` contract is currently vulnerable to sandwich attack in many places. Every place which does a swap or provides/removes liquidity is done in a manner that is vulnerable. While the code has slippage checks, they are flawed. Take for example the `tradeCRVtoWETH` method, here is how a swap is done:

```solidity
uint256 expectedAmount = curvePoolWETHCRV.get_dy(2, 1, crvBal); // Estimate WETH received for CRV:WETH exchange
// Exchange CRV for WETH within the slippage limit
curvePoolWETHCRV.exchange(2, 1, crvBal, expectedAmount * LPslippageNum / LPslippageDen);
```

The problem is that if an attacker sees you calling `tradeCRVtoWETH` he can imbalance the pool with a very big front-run transaction, which will give you a much smaller `expectedAmount`, and then after you do the swap he will execute a back-run transaction putting the price back to normal, essentially sandwiching your bad trade and profiting your loss. This is a problem in all methods that have an underlying call to `add_liquidity`, `remove_liquidity_one_coin`, `calc_withdraw_one_coin` and `calc_token_amount`.

**Recommendations**

Instead of doing on-chain same transaction calculations to calculate slippage tolerance, add an argument to all methods that use slippage calculations called "minAmountReceived" - it has to be calculated off-chain so it is not prone to on-chain manipulation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nftcapsule |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-NFTCapsule.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

