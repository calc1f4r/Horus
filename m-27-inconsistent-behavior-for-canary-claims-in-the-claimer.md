---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26396
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-pooltogether
source_link: https://code4rena.com/reports/2023-07-pooltogether
github_link: https://github.com/code-423n4/2023-07-pooltogether-findings/issues/61

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - volodya
---

## Vulnerability Title

[M-27] Inconsistent behavior for canary claims in the `claimer`

### Overview


This bug report is about an error in the code for the PoolTogether project. The code, written in Solidity, was used to calculate fees per claim without taking into account canary claims. The bug was discovered and confirmed by asselstine (PoolTogether).

The recommended mitigation steps were to consider canary claims as a claim in the code. This was done by adding the line `prizePool.canaryClaimCount()` to the code.

PoolTogether mitigated the issue by unifying the standard and canary tiers and creating a pull request. The mitigation was confirmed by rvierdiiev, dirk_y and 0xStalin.

### Original Finding Content


### Proof of Concept

Whenever a `claimer` claims prizes they compute fees per `claim` without considering canary claims.

```solidity
  function claimPrizes(
    Vault vault,
    uint8 tier,
    address[] calldata winners,
    uint32[][] calldata prizeIndices,
    address _feeRecipient
  ) external returns (uint256 totalFees) {
    uint256 claimCount;
    for (uint i = 0; i < winners.length; i++) {
      claimCount += prizeIndices[i].length;
    }

    uint96 feePerClaim = uint96(
      _computeFeePerClaim(
        _computeMaxFee(tier, prizePool.numberOfTiers()),
        claimCount,
        prizePool.claimCount()
      )
    );

    vault.claimPrizes(tier, winners, prizeIndices, feePerClaim, _feeRecipient);

    return feePerClaim * claimCount;
  }
```

[src/Claimer.sol#L76](https://github.com/GenerationSoftware/pt-v5-claimer/blob/57a381aef690a27c9198f4340747155a71cae753/src/Claimer.sol#L76)

### Recommended Mitigation Steps

Consider canary as a `claim`.

```diff
    uint96 feePerClaim = uint96(
      _computeFeePerClaim(
        _computeMaxFee(tier, prizePool.numberOfTiers()),
        claimCount,
-        prizePool.claimCount()
+        prizePool.claimCount() + prizePool.canaryClaimCount()
      )
    );

```

### Assessed type

Error

**[asselstine (PoolTogether) confirmed](https://github.com/code-423n4/2023-07-pooltogether-findings/issues/61#issuecomment-1641093811)**

**[PoolTogether mitigated](https://github.com/code-423n4/2023-08-pooltogether-mitigation#individual-prs):**
> Unified standard and canary tier.<br>
> PR: https://github.com/GenerationSoftware/pt-v5-prize-pool/pull/17

**Status**: Mitigation confirmed. Full details in report from [rvierdiiev](https://github.com/code-423n4/2023-08-pooltogether-mitigation-findings/issues/66), [dirk\_y](https://github.com/code-423n4/2023-08-pooltogether-mitigation-findings/issues/103) and [0xStalin](https://github.com/code-423n4/2023-08-pooltogether-mitigation-findings/issues/94).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | volodya |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-pooltogether
- **GitHub**: https://github.com/code-423n4/2023-07-pooltogether-findings/issues/61
- **Contest**: https://code4rena.com/reports/2023-07-pooltogether

### Keywords for Search

`vulnerability`

