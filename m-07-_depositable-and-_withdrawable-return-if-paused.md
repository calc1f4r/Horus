---
# Core Classification
protocol: Ionprotocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36441
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] `_depositable` and `_withdrawable` return if paused

### Overview


This bug report discusses a medium severity issue with the Vault, which uses deposit and withdrawal queues to process user assets. The functions `_depositable` and `_withdrawable` are used for this task, but they do not check if the pool is paused. This can lead to failures in deposit, mint, withdraw, and redeem operations, as well as incorrect results in maxDeposit, Mint, Withdraw, and Redeem functions. The recommendation is to verify if the pool is paused and return 0 in those functions. 

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

The Vault operates by using deposit and withdrawal queues. It starts from the first pool in the queue and checks the amount of assets available to process. If the amount is not enough, it moves to the next pool until all user's assets are used. The functions `_depositable` and `_withdrawable` are used for this task:

```solidity

    function _withdrawable(IIonPool pool) internal view returns (uint256) {
        uint256 currentSupplied = pool.getUnderlyingClaimOf(address(this));
        uint256 availableLiquidity = uint256(pool.extsload(ION_POOL_LIQUIDITY_SLOT));

        return Math.min(currentSupplied, availableLiquidity);
    }

    function _depositable(IIonPool pool) internal view returns (uint256) {
        uint256 allocationCapDiff = _zeroFloorSub(caps[pool], pool.getUnderlyingClaimOf(address(this)));
        uint256 supplyCapDiff =
            _zeroFloorSub(uint256(pool.extsload(ION_POOL_SUPPLY_CAP_SLOT)), pool.getTotalUnderlyingClaims());

        return Math.min(allocationCapDiff, supplyCapDiff);
    }
```

Unfortunately, it is not verified if the pool is paused. In case the pool is paused, neither the supply of assets nor withdrawal is possible. This results in:

- vault deposit/mint/withdraw/redeem operation failures since the paused pool is not skipped;
- incorrect results in maxDeposit/Mint/Withdraw/Redeem functions

**Recommendations**

Consider verifying if the pool is paused and return 0 inside `_depositable`, `_withdrawable`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

