---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27649
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
  - pontifex
---

## Vulnerability Title

The `svTokenValue` function can return overestimated value of each strategy vault share token

### Overview


A bug has been discovered in the `GMXReader.svTokenValue` function, which can return an overestimated value of each strategy vault share token. This is due to the outdated `totalSupply` value, which does not include pending management fees. The longer the period since the last `mintFee` was called, the larger the overestimation in the share value.

This bug can lead to unexpected behavior in the protocol, such as when keepers are providing rebalance and when other protocols receive information about the shares value.

The bug was discovered through manual review. The recommendation is to consider adding `pendingFee` to the `totalSupply` in the `svTokenValue` function.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXReader.sol#L27-L32">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXReader.sol#L27-L32</a>


## Summary
The `GMXReader.svTokenValue` function can return overestimated value of each strategy vault share token due to outdated `totalSupply`, i.e. without including pending management fees for a long period. This issue can cause the protocol unexpected behavior while keepers provide rebalance and when other protocols receive information about shares value.

## Vulnerability Details
The `svTokenValue` function calculates the value of each strategy vault share token with the current amount of `totalSupply`, which may not include pending management fees:
```solidity
  function svTokenValue(GMXTypes.Store storage self) public view returns (uint256) {
    uint256 equityValue_ = equityValue(self);
    uint256 totalSupply_ = IERC20(address(self.vault)).totalSupply();
    if (equityValue_ == 0 || totalSupply_ == 0) return SAFE_MULTIPLIER;
    return equityValue_ * SAFE_MULTIPLIER / totalSupply_;
  }
```  
So the returned share value will be overestimated. The longer the period since the last `mintFee` was called the more overestimated shares value is.

## Impact
The `GMXReader.svTokenValue` function returns an overestimated value of the share token. This issue can cause the protocol unexpected behavior while keepers provide rebalance and when other protocols receive information about the shares value.

## Tools used
Manual Review

## Recommendations
Consider adding `pendingFee` to the `totalSupply`:
```diff
  function svTokenValue(GMXTypes.Store storage self) public view returns (uint256) {
    uint256 equityValue_ = equityValue(self);
    uint256 totalSupply_ = IERC20(address(self.vault)).totalSupply();
    if (equityValue_ == 0 || totalSupply_ == 0) return SAFE_MULTIPLIER;
-    return equityValue_ * SAFE_MULTIPLIER / totalSupply_;
+    return equityValue_ * SAFE_MULTIPLIER / (totalSupply_ + pendingFee(self));
  } 
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | pontifex |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

