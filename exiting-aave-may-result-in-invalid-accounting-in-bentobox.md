---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19609
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Exiting Aave May Result In Invalid Accounting in BentoBox

### Overview


This bug report is about a situation in the Aave protocol where the balance of strategyToken in Aave is less than that owed to the BentoBox strategy. If there is insufficient balance, the BentoBox strategy will only withdraw the available balance, causing a deficit between the deposited amount and withdrawn amount. This loss will cause the value of BentoBox shares to decrease. Furthermore, during the process of withdrawing the remaining amount, admins will have full control over the funds, creating a centralization risk. Additionally, if the external call fails, the entire balance will remain in the Aave pool and the deficit will be the entire amount deposited, again resulting in a loss distributed amongst BentoBox share holders.

A possible solution to this issue is to introduce code which will revert if the withdraw() external call fails. This code will withdraw the entire user balance in Aave if successful.

In conclusion, this bug report describes a situation in the Aave protocol which results in a loss for BentoBox share holders. The bug report suggests introducing code which will revert if the withdraw() external call fails, thus withdrawing the entire user balance in Aave.

### Original Finding Content

## Description

The Aave protocol lends out deposited funds, and it is possible to have a situation where the balance of `strategyToken` in Aave is less than that owed to the BentoBox strategy. If there is insufficient balance, the BentoBox strategy will only withdraw the available balance.

The deficit between the deposited amount and the withdrawn amount will be considered a loss in BentoBox when calling `setStrategy()`. The loss will cause the value of BentoBox shares to decrease.

The amount remaining in the Aave protocol may be withdrawn by the admins at a later time when there are sufficient tokens in the protocol to accept a withdrawal. However, the shares would need to be redistributed to users manually by taking a snapshot of the user share balances at the time the exit was made. This is highly impractical as there is a large number of users requiring a large distribution of tokens. Furthermore, during this process, admins will have full control over the funds, creating a centralization risk.

A similar issue occurs during `_exit()` since the `withdraw()` external call is wrapped in a try-catch statement. If the external call fails, the entire balance will remain in the Aave pool. The deficit in this case will be the entire amount deposited, and the loss will be distributed among BentoBox shareholders.

The function `_exit()` can be seen in the following code snippet demonstrating the try-catch statements and only withdrawing the available balance.

```solidity
function _exit() internal override {
    uint256 tokenBalance = aToken.balanceOf(address(this));
    uint256 available = strategyToken.balanceOf(address(aToken));
    if (tokenBalance <= available) {
        // If there are more tokens available than our full position, take all based on aToken balance (continue if unsuccessful).
        try aaveLendingPool.withdraw(address(strategyToken), tokenBalance, address(this)) {} catch {}
    } else {
        // Otherwise redeem all available and take a loss on the missing amount (continue if unsuccessful).
        try aaveLendingPool.withdraw(address(strategyToken), available, address(this)) {} catch {}
    }
}
```

## Recommendations

This issue may be mitigated by reverting if the entire balance cannot be withdrawn during an exit. Consider introducing the following code, which will revert if the `withdraw()` external call fails.

```solidity
function _exit() internal override {
    // (uint256).max withdraws the entire user balance in Aave
    aaveLendingPool.withdraw(address(strategyToken), (uint256).max, address(this));
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/bentobox-strategies-staking-contract/review.pdf

### Keywords for Search

`vulnerability`

