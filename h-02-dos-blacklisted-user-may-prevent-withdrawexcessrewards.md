---
# Core Classification
protocol: FactoryDAO
chain: everychain
category: uncategorized
vulnerability_type: blacklisted

# Attack Vector Details
attack_type: blacklisted
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2242
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-factorydao-contest
source_link: https://code4rena.com/reports/2022-05-factorydao
github_link: https://github.com/code-423n4/2022-05-factorydao-findings/issues/57

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.73
financial_impact: high

# Scoring
quality_score: 3.6666666666666665
rarity_score: 2

# Context Tags
tags:
  - blacklisted
  - erc20

protocol_categories:
  - dexes
  - cdp
  - yield
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - AuditsAreUS
---

## Vulnerability Title

[H-02] DoS: Blacklisted user may prevent withdrawExcessRewards()

### Overview


This bug report is about a vulnerability in the code of the Permissionless Basic Pool Factory. If one user becomes blacklisted or otherwise cannot be transferred funds in any of the rewards tokens or the deposit token then they will not be able to call `withdraw()` for that token. This will prevent the owner of the contract from being able to call `withdrawExcessRewards()` and therefore lock not only the users rewards and deposit but also and excess rewards attributed to the owner. This attack is very cheap as the attacker may do it with a negligible balance in their `deposit()`. To mitigate this issue, it is recommended to consider allowing `withdrawExcessRewards()` to be called after a set period of time after the pool end if most users have withdrawn or some similar criteria.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-05-factorydao/blob/db415804c06143d8af6880bc4cda7222e5463c0e/contracts/PermissionlessBasicPoolFactory.sol#L242-L256
https://github.com/code-423n4/2022-05-factorydao/blob/db415804c06143d8af6880bc4cda7222e5463c0e/contracts/PermissionlessBasicPoolFactory.sol#L224-L234


## Vulnerability details

## Impact

If one user becomes blacklisted or otherwise cannot be transferred funds in any of the rewards tokens or the deposit token then they will not be able to call `withdraw()` for that token.

The impact of one user not being able to call `withdraw()` is that the owner will now never be able to call `withdrawExcessRewards()` and therefore lock not only the users rewards and deposit but also and excess rewards attributed to the owner.

Thus, one malicious user may deliberately get them selves blacklisted to prevent the owner from claiming the final rewards. Since the attacker may do this with negligible balance in their `deposit()` this attack is very cheap.

## Proof of Concept

It is possible for `IERC20(pool.rewardTokens[i]).transfer(receipt.owner, transferAmount);` to fail for numerous reasons. Such as if a user has been blacklisted (in certain ERC20 tokens) or if a token is paused or there is an attack and the token is stuck.

This will prevent `withdraw()` from being called.

```solidity
        for (uint i = 0; i < rewards.length; i++) {
            pool.rewardsWeiClaimed[i] += rewards[i];
            pool.rewardFunding[i] -= rewards[i];
            uint tax = (pool.taxPerCapita * rewards[i]) / 1000;
            uint transferAmount = rewards[i] - tax;
            taxes[poolId][i] += tax;
            success = success && IERC20(pool.rewardTokens[i]).transfer(receipt.owner, transferAmount);
        }

        success = success && IERC20(pool.depositToken).transfer(receipt.owner, receipt.amountDepositedWei);
        require(success, 'Token transfer failed');
```

Since line 245 of `withdrawExcessRewards()` requires that `require(pool.totalDepositsWei == 0, 'Cannot withdraw until all deposits are withdrawn');`, if one single user is unable to withdraw then it is impossible for the owner to claim the excess rewards and they are forever stuck in the contract.

## Recommended Mitigation Steps

Consider allowing `withdrawExcessRewards()` to be called after a set period of time after the pool end if most users have withdrawn or some similar criteria.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3.6666666666666665/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | FactoryDAO |
| Report Date | N/A |
| Finders | AuditsAreUS |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-factorydao
- **GitHub**: https://github.com/code-423n4/2022-05-factorydao-findings/issues/57
- **Contest**: https://code4rena.com/contests/2022-05-factorydao-contest

### Keywords for Search

`Blacklisted, ERC20`

