---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51215
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/plural-energy/protocol-smart-contract-security-assessment-7
source_link: https://www.halborn.com/audits/plural-energy/protocol-smart-contract-security-assessment-7
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

USING TRANSFER INSTEAD OF SAFETRANSFER

### Overview


The `claim()` function in the `RewardsManagerRetroactive` and `RewardsManagerConstant` contracts use the `IERC20` interface to transfer currencies from the contract to a designated wallet. However, some tokens do not return a value when the transfer function is used, making them incompatible with the current version of the contracts. This can cause the `claim()` function to fail and revert. To solve this, the team has implemented a solution using the OpenZeppelin's `SafeERC20` wrapper in their code.

### Original Finding Content

##### Description

It was identified that the `claim()` function in the `RewardsManagerRetroactive` and `RewardsManagerConstant` contracts use the `IERC20` interface to interact with the `rewardTokenAddress` to transfer currencies from the contract to the parameter wallet. The `IERC20` interface expects the `transfer` function to have a return value on success. The rewards manager contracts are designed to be used with different currencies. It is important to note that the transfer functions of some tokens (e.g., USDT, BNB) do not return any values, so these tokens are incompatible with the current version of the rewards' manager contracts.

Code Location
-------------

The `claim()` function uses the `IERC20` interface to interact with `rewardTokenAddress`:

#### src/RewardsManagerRetroactive.sol

```
    accountClaimedRewards[account] = claimed + unscaledClaimable;
    claimedRewards += unscaledClaimable;

    bool success = IERC20(rewardTokenAddress).transfer(account, claimable);
    if (!success) {
        revert ClaimError();
    }

    emit RewardClaimed(assetTokenAddress, account, unscaledClaimable);

```

The `claim()` function reverts if used with tokens not having a return value (e.g., USDT):

![halxx_safetransfer.png](https://halbornmainframe.com/proxy/audits/images/659f8ff8a1aa3698c0f56087)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:N/R:N/S:U)

##### Recommendation

**SOLVED:** The \client team solved the issue in commit [3735f2f](https://github.com/plural-energy/plural-protocol/commit/3735f2f100042467b4d0370473e5dc648f0ade49) by using the OpenZeppelin's `SafeERC20` wrapper.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/plural-energy/protocol-smart-contract-security-assessment-7
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/plural-energy/protocol-smart-contract-security-assessment-7

### Keywords for Search

`vulnerability`

