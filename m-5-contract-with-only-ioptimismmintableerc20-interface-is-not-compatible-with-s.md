---
# Core Classification
protocol: Optimism
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6501
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/38
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-optimism-judging/issues/220

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - lemonmon
  - Barichek
---

## Vulnerability Title

M-5: contract with only `IOptimismMintableERC20` interface is not compatible with `StandardBridge`

### Overview


This bug report is about an issue with the `StandardBridge` using the `OptimismMintableERC20` contract. If a custom contract implements only the `IOptimismMintableERC20` interface, but not the `ILegacyMintableERC20`, the contract is not compatible with the `StandardBridge`. This is because the bridge uses the `l1Token` function from the legacy interface, which will fail if the token does not implement it. The bug was found by Barichek and lemonmon, and it was confirmed by manual review. The impact of this issue is that any custom contract without the `l1Token` function will not be compatible with `StandardBridge`. It is unclear if this is intended behavior. A possible recommendation is that the `_isOptimismMintableERC20` function should return true only when both of the interfaces are implemented, so that tokens with only the `IOptimismMintableERC20` will be treated as if they are not the optimism mintable function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-optimism-judging/issues/220 

## Found by 
Barichek, lemonmon



## Summary

If a custom contract implements only the `IOptimismMintableERC20`, but no the `ILegacyMintableERC20`, the contract is not compatible with the `StandardBridge`, as the bridge uses the `l1Token` function from the legacy interface

## Vulnerability Detail

The comment in the `IOptimismMintableERC20` suggests that one can make a custom implementation of `OptimismMintableERC20` using the interface `IOptimismMintableERC20`.

https://github.com/sherlock-audit/2023-01-optimism/blob/main/optimism/packages/contracts-bedrock/contracts/universal/IOptimismMintableERC20.sol#L8-L10

Also, the `StandardBridge`, which uses the `OptimismMintableERC20` has `_isOptimismMintableERC20` function, which checks whether the given token address is implementing `OptimismMintableERC20`. The function will be true if either of `ILegacyMintableERC20` or `IOptimismMintableERC20` is implemented. it means that if a token implements only one of the interfaces, it will return true.

https://github.com/sherlock-audit/2023-01-optimism/blob/main/optimism/packages/contracts-bedrock/contracts/universal/StandardBridge.sol#L446-L450

However, if the given token passes the `_isOptimismMintableERC20`, the legacy function `l1Token` will be called on the token. If the token does not implement the legacy interface, the call will fail.

https://github.com/sherlock-audit/2023-01-optimism/blob/main/optimism/packages/contracts-bedrock/contracts/L2/L2StandardBridge.sol#L170

Therefore, the token which only implements `IOptimismMintableERC20`, but not the `ILegacyMintableERC20`, is not compatible with `StandardBridge`.


## Impact

Any custom contract without `l1Token` function will not be compatible with `StandardBridge`


## Code Snippet


https://github.com/sherlock-audit/2023-01-optimism/blob/main/optimism/packages/contracts-bedrock/contracts/universal/IOptimismMintableERC20.sol#L8-L10


https://github.com/sherlock-audit/2023-01-optimism/blob/main/optimism/packages/contracts-bedrock/contracts/universal/StandardBridge.sol#L446-L450


https://github.com/sherlock-audit/2023-01-optimism/blob/main/optimism/packages/contracts-bedrock/contracts/L2/L2StandardBridge.sol#L170


## Tool used

Manual Review

## Recommendation

It is unclear it is intended behavior.
If the `_isOptimismMintableERC20` function returns true only when the both of interfaces are implemented, the token with only the `IOptimismMintableERC20` will be treated as if they are not the optimism mintable function, without failing.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Optimism |
| Report Date | N/A |
| Finders | lemonmon, Barichek |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-optimism-judging/issues/220
- **Contest**: https://app.sherlock.xyz/audits/contests/38

### Keywords for Search

`vulnerability`

