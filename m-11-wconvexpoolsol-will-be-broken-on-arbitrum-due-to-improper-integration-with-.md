---
# Core Classification
protocol: Blueberry Update #3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24331
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/104
source_link: none
github_link: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/119

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
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Kow
---

## Vulnerability Title

M-11: WConvexPool.sol will be broken on Arbitrum due to improper integration with Convex Arbitrum contracts

### Overview


This bug report is about the issue M-11 which was found by Kow. It states that the WConvexPool contract, which is expected to be deployed to both mainnet and Arbitrum, will be completely broken on Arbitrum due to not accounting for implementation differences in Convex Arbitrum contracts. 

The primary issue is the change in arguments returned from ``cvxPools.poolInfo()`` when calling [``getPoolInfoFromPoolId``]. The return signature expects 6 values (through destructuring) while the Arbitrum Booster contract's getter only returns 5. This is called in ``pendingRewards``, ``mint``, and ``burn``, 3 of the main functions in WConvexPool, and will consequently disable any interaction with it (this includes ConvexSpell which also uses this function and also attempts to call mint/burn for position management).

Other issues include the use of ``cvxPools.deposit(...)`` and ``cvxPools.withdraw(...)`` which do not match any function signatures in the Arbitrum Booster contract.

The impact of this is that the Convex integration will be completely broken on Arbitrum due to unaccounted for implementation differences. The code snippets and manual review were used to identify the issue. The recommendation is to consider creating a separate contract for WConvexPools for Arbitrum that correctly accounts for the Convex Booster implementation changes.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/119 

## Found by 
Kow
WConvexPool (and consequently ConvexSpell) will be completely broken on Arbitrum due to not accounting for implementation differences in Convex Arbitrum contracts.

## Vulnerability Detail
WConvexPool.sol is the contract expected to be deployed to both mainnet and Arbitrum (sponsor confirmed). While it does integrate with mainnet Convex contracts, it does not account for implementation differences in Arbitrum Convex contracts (briefly mentioned in their [docs](https://docs.convexfinance.com/convexfinanceintegration/side-chain-implemention) with the Arbitrum version of the Booster contract that Blueberry integrates with found [here](https://arbiscan.io/address/0xF403C135812408BFbE8713b5A23a04b3D48AAE31#readContract)). The primary issue is the change in arguments returned from ``cvxPools.poolInfo()`` when calling [``getPoolInfoFromPoolId``](https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L103-L126). Since the return signature expects 6 values (through destructuring) while the Arbitrum Booster contract's getter only returns 5 (due to a slight change in the [PoolInfo struct](https://github.com/convex-eth/sidechain-platform/blob/b9525005549c8f2d364d092bfd902b8eb05d7079/contracts/contracts/Booster.sol#L36-L43) - mainnet struct [here](https://github.com/convex-eth/platform/blob/a5da3f127a321467a97a684c57970d2586520172/contracts/contracts/Booster.sol#L48-L55)), all attempts to call it will revert. This is called in [``pendingRewards``](https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L179-L191), [``mint``](https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L235-L241), and [``burn``](https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L276-L292), 3 of the main functions in WConvexPool, and will consequently disable any interaction with it (this includes ConvexSpell which also uses this function and also attempts to call mint/burn for position management).

Other issues include the use of ``cvxPools.deposit(...)`` and ``cvxPools.withdraw(...)`` which do not match any function signatures in the Arbitrum Booster contract (``withdraw`` has been changed to ``withdrawTo`` with different arguments and ``deposit`` no longer includes the 3rd argument).

## Impact
Convex integration will be completely broken on Arbitrum due to unaccounted for implementation differences.

## Code Snippet
https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L103-L126
https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L179-L191
https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L235-L241
https://github.com/sherlock-audit/2023-07-blueberry/blob/7c7e1c4a8f3012d1afd2e598b656010bb9127836/blueberry-core/contracts/wrapper/WConvexPools.sol#L276-L292

## Tool used

Manual Review

## Recommendation
Consider creating a separate contract for WConvexPools for Arbitrum that correctly accounts for the Convex Booster implementation changes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #3 |
| Report Date | N/A |
| Finders | Kow |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/119
- **Contest**: https://app.sherlock.xyz/audits/contests/104

### Keywords for Search

`vulnerability`

