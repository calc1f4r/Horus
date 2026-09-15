---
# Core Classification
protocol: Growth Labs GSquared
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17345
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
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
finders_count: 4
finders:
  - Damilola Edwards
  - Gustavo Grieco
  - Anish Naik
  - Michael Colburn
---

## Vulnerability Title

Unbounded loop can cause denial of service

### Overview


This bug report is about a data validation issue in the contracts/GVault.sol file. The issue arises when a user attempts to withdraw funds from the protocol. Under certain conditions, the withdrawal code will loop, permanently blocking users from getting their funds. The beforeWithdraw function runs before any withdrawal to ensure that the vault has sufficient assets. If the vault reserves are insufficient to cover the withdrawal, it loops over each strategy, incrementing the _strategyId pointer value with each iteration, and withdrawing assets to cover the withdrawal amount. However, during an iteration, if the vault raises enough assets that the amount needed by the vault becomes zero or that the current strategy no longer has assets, the loop would keep using the same strategyId until the transaction runs out of gas and fails, blocking the withdrawal.

The exploit scenario is that Alice tries to withdraw funds from the protocol, and the contract may be in a state that sets the conditions for the internal loop to run indefinitely, resulting in the waste of all sent gas, the failure of the transaction, and blocking all withdrawal requests.

The recommendation is to add logic to increment the _strategyId variable to point to the next strategy in the StrategyQueue before the continue statement. In the long term, it is recommended to use unit tests and fuzzing tools like Echidna to test that the protocol works as expected, even for edge cases.

### Original Finding Content

## GSquared Security Assessment

## Difficulty
High

## Type
Data Validation

## Target
contracts/GVault.sol

## Description
Under certain conditions, the withdrawal code will loop, permanently blocking users from getting their funds.

The `beforeWithdraw` function runs before any withdrawal to ensure that the vault has sufficient assets. If the vault reserves are insufficient to cover the withdrawal, it loops over each strategy, incrementing the `_strategyId` pointer value with each iteration, and withdrawing assets to cover the withdrawal amount.

```solidity
function beforeWithdraw(uint256 _assets, ERC20 _token)
internal
returns (uint256)
// If reserves don't cover the withdrawal, start withdrawing from strategies
if (_assets > _token.balanceOf(address(this))) {
    uint48 _strategyId = strategyQueue.head;
    while (true) {
        address _strategy = nodes[_strategyId].strategy;
        uint256 vaultBalance = _token.balanceOf(address(this));
        // break if we have withdrawn all we need
        if (_assets <= vaultBalance) break;
        uint256 amountNeeded = _assets - vaultBalance;
        StrategyParams storage _strategyData = strategies[_strategy];
        amountNeeded = Math.min(amountNeeded, _strategyData.totalDebt);
        // If nothing is needed or strategy has no assets, continue
        if (amountNeeded == 0) {
            continue;
        }
    }
}
```
*Figure 1.1: The `beforeWithdraw` function in GVault.sol #L643-662*

However, during an iteration, if the vault raises enough assets that the amount needed by the vault becomes zero, or that the current strategy no longer has assets, the loop would keep using the same `strategyId` until the transaction runs out of gas and fails, blocking the withdrawal.

## Exploit Scenario
Alice tries to withdraw funds from the protocol. The contract may be in a state that sets the conditions for the internal loop to run indefinitely, resulting in the waste of all sent gas, the failure of the transaction, and blocking all withdrawal requests.

## Recommendations
- **Short term:** Add logic to increment the `_strategyId` variable to point to the next strategy in the `StrategyQueue` before the continue statement.
- **Long term:** Use unit tests and fuzzing tools like Echidna to test that the protocol works as expected, even for edge cases.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Growth Labs GSquared |
| Report Date | N/A |
| Finders | Damilola Edwards, Gustavo Grieco, Anish Naik, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf

### Keywords for Search

`vulnerability`

