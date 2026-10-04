---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26083
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/634

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

protocol_categories:
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Voyvoda
---

## Vulnerability Title

[M-14] `BoostAggregator` owner can set fees to 100% and steal all of the user's rewards

### Overview


A bug has been reported in the BoostAggregator code in the Maia project, which can lead to users losing all their rewards. The bug exists in two lines of code (<https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/boost-aggregator/BoostAggregator.sol#L119> and <https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/boost-aggregator/BoostAggregator.sol#L153>).

The bug is that the owner of the BoostAggregator can set the protocolFee to 10_000 (100%) and steal the user's rewards. This is an unnecessary vulnerability as anyone can create their own BoostAggregator and it is supposed to be publicly used.

The severity of the bug was decreased to Medium by Trust (judge), as it requires a malicious aggregator owner while other bugs can happen during normal interaction.

To address the bug, Maia suggested creating a mapping which tracks the protocolFee at which the user has deposited their NFT. Upon withdrawing, the protocolFee can be retrieved from the said mapping. This was addressed in the Maia project's eco-c4-contest.

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/boost-aggregator/BoostAggregator.sol#L119> <br><https://github.com/code-423n4/2023-05-maia/blob/main/src/talos/boost-aggregator/BoostAggregator.sol#L153>

### Impact

Users who use `BoostAggregator` will suffer a 100% loss of their rewards.

### Proof of Concept

After users have staked their tokens, the owner of the `BoostAggregator` can set `protocolFee` to `10_000` (100%) and steal the user's rewards. Anyone can create their own `BoostAggregator` and it is supposed to be publicly used; therefore, the owner of it cannot be considered trusted. Allowing the owner to steal the user's rewards is an unnecessary vulnerability.

```solidity
    function setProtocolFee(uint256 _protocolFee) external onlyOwner { 
        if (_protocolFee > DIVISIONER) revert FeeTooHigh();
        protocolFee = _protocolFee; // @audit - owner can set it to 100% and steal all rewards
    }
```

### Recommended Mitigation Steps

Create a mapping which tracks the `protocolFee` at which the user has deposited their NFT. Upon withdrawing, get the `protocolFee` from the said mapping.

**[Trust (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-05-maia-findings/issues/634#issuecomment-1649475291):**
 > A fair level of trust is assumed on receiving `boostAggregator`, but the loss of yield is serious. Therefore, medium is appropriate.

**[Trust (judge) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/634#issuecomment-1653252394):**
 > A different severity from [#731](https://github.com/code-423n4/2023-05-maia-findings/issues/731), as this requires a malicious aggregator owner, while #731 can happen during normal interaction.

**[0xLightt (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/634#issuecomment-1708826139):**
 > Addressed [here](https://github.com/Maia-DAO/eco-c4-contest/tree/634).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | Voyvoda |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/634
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

