---
# Core Classification
protocol: Yearn v2 Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16950
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
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
finders_count: 2
finders:
  - Gustavo Grieco
  - Mike Martel
---

## Vulnerability Title

setWithdrawalQueue allows for duplicated strategies

### Overview

See description below for full details.

### Original Finding Content

## Access Controls

**Target:** Vault.vy

**Difficulty:** High

## Description

The function to set the order of the withdrawal queue does not check for duplicated strategies, which can force a vault into an invalid state. Once strategies have been added to a vault, they will automatically be included in the withdrawal queue.

```python
@external
def addStrategy(
    strategy: address,
    debtRatio: uint256,
    minDebtPerHarvest: uint256,
    maxDebtPerHarvest: uint256,
    performanceFee: uint256,
):
    ...
    log StrategyAdded(strategy, debtRatio, minDebtPerHarvest, maxDebtPerHarvest, performanceFee)
    # Update Vault parameters
    self.debtRatio += debtRatio
    # Add strategy to the end of the withdrawal queue
    self.withdrawalQueue[MAXIMUM_STRATEGIES - 1] = strategy
    self._organizeWithdrawalQueue()
```
*Figure 8.1: Part of the `addStrategy` function*

The vault’s management or governance can reorder a queue using the `setWithdrawalQueue` function:

```python
@external
def setWithdrawalQueue(queue: address[MAXIMUM_STRATEGIES]):
    assert msg.sender in [self.management, self.governance]
    # HACK: Temporary until Vyper adds support for Dynamic arrays
    for i in range(MAXIMUM_STRATEGIES):
        if queue[i] == ZERO_ADDRESS and self.withdrawalQueue[i] == ZERO_ADDRESS:
            break
        assert self.strategies[queue[i]].activation > 0
        self.withdrawalQueue[i] = queue[i]
    log UpdateWithdrawalQueue(queue)
```
*Figure 8.2: The `setWithdrawalQueue` function*

However, this function does not check whether the elements in the queue are duplicated, which would break an important invariant of the vault.

## Exploit Scenario

Alice is the manager of a vault. During a call to `setWithdrawalQueue`, she includes the same strategy twice by mistake. As a result, users trying to withdraw their shares could experience unexpected reverts, since the duplicated strategy will cause the strategy’s debt to decrease by more than the expected amount.

## Recommendations

**Short term:** Clearly document the fact that `setWithdrawalQueue` does not check for duplicated strategies so that management and governance will be aware of this issue before performing reordering operations.

**Long term:** Review the security and correctness properties and use Echidna or Manticore to test them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yearn v2 Vaults |
| Report Date | N/A |
| Finders | Gustavo Grieco, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf

### Keywords for Search

`vulnerability`

