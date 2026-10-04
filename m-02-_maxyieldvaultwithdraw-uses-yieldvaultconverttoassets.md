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
solodit_id: 30668
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-pooltogether
source_link: https://code4rena.com/reports/2024-03-pooltogether
github_link: https://github.com/code-423n4/2024-03-pooltogether-findings/issues/336

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
finders_count: 2
finders:
  - d3e4
---

## Vulnerability Title

[M-02] `_maxYieldVaultWithdraw()` uses `yieldVault.convertToAssets()`

### Overview


The bug report discusses a potential issue with the code in the `maxWithdraw()` and `maxRedeem()` functions of the PoolTogether smart contract. These functions use the `yieldVault.convertToAssets()` function, which is not always accurate according to the EIP-4626 standard. This means that these functions may return too much, violating the standard. The report recommends using the `yieldVault.previewRedeem()` function as a mitigation step. The bug has been confirmed and a fix has been proposed by the PoolTogether team. 

### Original Finding Content


### Proof of Concept

```solidity
function _maxYieldVaultWithdraw() internal view returns (uint256) {
    return yieldVault.convertToAssets(yieldVault.maxRedeem(address(this)));
}
```

The above code uses `yieldVault.convertToAssets()` which, per EIP-4626, is only approximate. Especially, it might return too much, and thus `_maxYieldVaultWithdraw()` might return too much.
`_maxYieldVaultWithdraw()` is used [in `maxWithdraw()`](https://github.com/code-423n4/2024-03-pooltogether/blob/480d58b9e8611c13587f28811864aea138a0021a/pt-v5-vault/src/PrizeVault.sol#L405), [in `maxRedeem()`](https://github.com/code-423n4/2024-03-pooltogether/blob/480d58b9e8611c13587f28811864aea138a0021a/pt-v5-vault/src/PrizeVault.sol#L416), and [in `liquidatableBalanceOf()`](https://github.com/code-423n4/2024-03-pooltogether/blob/480d58b9e8611c13587f28811864aea138a0021a/pt-v5-vault/src/PrizeVault.sol#L639) which functions may thus return too much. In the case of `maxWithdraw()` and `maxRedeem()` this violates EIP-4626.

### Recommended Mitigation Steps

Use `yieldVault.previewRedeem(yieldVault.maxRedeem(address(this)))`.

### Assessed type

ERC4626

**[trmid (PoolTogether) confirmed and commented](https://github.com/code-423n4/2024-03-pooltogether-findings/issues/336#issuecomment-2018842026):**
 > Mitigation [here](https://github.com/GenerationSoftware/pt-v5-vault/pull/97). Also see [here](https://github.com/GenerationSoftware/pt-v5-vault/pull/96) for more details.

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
| Finders | d3e4 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-pooltogether
- **GitHub**: https://github.com/code-423n4/2024-03-pooltogether-findings/issues/336
- **Contest**: https://code4rena.com/reports/2024-03-pooltogether

### Keywords for Search

`vulnerability`

