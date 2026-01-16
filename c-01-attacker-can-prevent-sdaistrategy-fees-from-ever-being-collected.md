---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31526
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-02-01-TapiocaDAO.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[C-01] Attacker can prevent `sDaiStrategy` fees from ever being collected

### Overview


The bug report discusses an issue in the `sDaiStrategy` contract where an attacker can manipulate the `totalActiveDeposits` variable, resulting in no fees being collected from the generated yield. This is because the variable is incremented by the contract balance of the deposited asset, but the deposited assets are only placed into the underlying pool when a certain threshold is reached. The report suggests that the `totalActiveDeposits` variable should only be incremented if the deposited assets are actually greater than the threshold and deposited into the pool. This will prevent the attacker from manipulating the variable and ensure that fees are collected correctly.

### Original Finding Content

**Severity**

**Impact:** High, since zero fees will be captured by the strategy

**Likelihood:** High, since this attack can be easily performed and persisted by a single attacker

**Description**

In the `sDaiStrategy`, when a user deposits assets into the strategy, the deposited assets are only placed into the underlying pool when the `depositThreshold` (which is set by the owner) is reached:

```solidity
function _deposited(uint256 amount) internal override nonReentrant {
        if (paused) revert Paused();

        // Assume that YieldBox already transferred the tokens to this address
        uint256 queued = IERC20(contractAddress).balanceOf(address(this));
        totalActiveDeposits += queued; // Update total deposits

        if (queued >= depositThreshold) {
            ITDai(contractAddress).unwrap(address(this), queued);
            dai.approve(address(sDai), queued);
            sDai.deposit(queued, address(this));
            emit AmountDeposited(queued);
            return;
        }
        emit AmountQueued(amount);
    }
```

During this flow, the `totalActiveDeposits` variable is incremented by the contract balance of the deposited asset.

Now, during withdrawals, this variable is used to calculate how many fees are still pending:

```solidity
// Compute the fees
        {
            uint256 _totalActiveDeposits = totalActiveDeposits; // Cache total deposits
            (uint256 fees, uint256 accumulatedTokens) = _computePendingFees(_totalActiveDeposits, maxWithdraw); // Compute pending fees
            if (fees > 0) {
                feesPending += fees; // Update pending fees
            }

            // Act as an invariant, totalActiveDeposits should never be lower than the amount to withdraw from the pool
            totalActiveDeposits = _totalActiveDeposits + accumulatedTokens - amount; // Update total deposits
        }
```

This logic is important because it makes sure that we're not charging fees multiple times over the same capital deposited in the strategy. The `_computePendingFees` method only charges fees when `maxWithdraw` is greater than `_totalActiveDeposits` (i.e. the strategy has generated yield, of which the fee recipient is due a percentage):

```solidity
function _computePendingFees(uint256 _totalDeposited, uint256 _amountInPool)
        internal
        view
        returns (uint256 result, uint256 accumulated)
    {
        if (_amountInPool > _totalDeposited) {
            accumulated = _amountInPool - _totalDeposited; // Get the occurred gains amount
            (, result) = _processFees(accumulated); // Process fees
        }
    }
```

So, `totalActiveDeposits` should never be greater than `maxWithdraw` otherwise no fees will ever be charged.

An attacker can force this situation to occur by doing the following:

1. The attacker makes a deposit that brings the queued asset balance of the strategy to just below the `depositThreshold`
2. The attacker can now make multiple tiny deposits that keep the asset balance close to but still below the `depositThreshold`

This is a problem because of the following logic:

```
uint256 queued = IERC20(contractAddress).balanceOf(address(this));
totalActiveDeposits += queued; // Update total deposits
```

The `totalActiveDeposits` variable is increased by `~depositThreshold` every time the attacker makes a tiny deposit, yet there are no deposits being made into the underlying sDai pool. As a result the `totalActiveDeposits` variable is now significantly larger than the `maxWithdraw` from the pool and no fees will be collected from the generated yield. This attack could be performed again in the future once accumulated rewards catch up with the inflated active deposit accounting.

**Recommendations**

In the `_deposited` method the `totalActiveDeposits` variable should only be incremented if the queued deposits are actually greater than the `depositThreshold` and deposited into the sDai pool.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-02-01-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

