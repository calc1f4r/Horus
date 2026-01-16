---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29705
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-particle
source_link: https://code4rena.com/reports/2023-12-particle
github_link: https://github.com/code-423n4/2023-12-particle-findings/issues/36

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bin2chen
---

## Vulnerability Title

[M-08] collectLiquidity() Lack of can specify recipient leads to inability to retrieve token1 after entering the blacklist of token0

### Overview


The report is about a problem with a code in the LP contract. The contract only has one way to retrieve tokens, which is by first decreasing liquidity and then using the collectLiquidity() method. However, this method only allows the tokens to be transferred to the contract owner, which can cause issues if the contract owner is blacklisted from a certain token. This means that both tokens cannot be retrieved. The report suggests adding a recipient parameter to the collectLiquidity() method to avoid this problem. However, some argue that this is not a good design and should not be changed to allow for arbitrary recipients, as it may facilitate tampering with blacklists. The team has acknowledged the issue but has not made any changes to the code.

### Original Finding Content


`LP` has only one way to retrieve `token`, first `decreaseLiquidity()`, then retrieve through the `collectLiquidity()` method.

`collectLiquidity()` only has one parameter, `tokenId`.

```solidity
    function collectLiquidity(
        uint256 tokenId
    ) external override nonReentrant returns (uint256 amount0Collected, uint256 amount1Collected) {
        (amount0Collected, amount1Collected) = lps.collectLiquidity(tokenId);
    }
```

So `LP` can only transfer the retrieved `token` to himself: `msg.sender`.

This leads to a problem. If `LP` enters the blacklist of a certain `token`, such as the `USDC` blacklist,

Because the recipient cannot be specified (`lps[]` cannot be transferred), this will cause another `token` not to be retrieved, such as `WETH`.

Refer to `NonfungiblePositionManager.collect()` and `UniswapV3Pool.collect()`, both can specify `recipient` to avoid this problem.

### Impact

`collectLiquidity()` cannot specify the recipient, causing `LP` to enter the blacklist of a certain token, and both tokens cannot be retrieved.

### Recommended Mitigation

```diff
    function collectLiquidity(
        uint256 tokenId,
+      address recipient
    ) external override nonReentrant returns (uint256 amount0Collected, uint256 amount1Collected) {
...
```

**[wukong-particle (Particle) commented](https://github.com/code-423n4/2023-12-particle-findings/issues/36#issuecomment-1868216251):**
 > Good suggestion, recipient should be added here too: https://github.com/code-423n4/2023-12-particle/blob/main/contracts/libraries/LiquidityPosition.sol#L329 


**[0xleastwood (Judge) commented](https://github.com/code-423n4/2023-12-particle-findings/issues/36#issuecomment-1868382997):**
 > I would argue this is good design and should not be changed to allow for arbitrary recipients. If a token is blacklisted, and a protocol allows the user to circumvent this blacklist, then they may potentially be liable for the behaviour of this individual. Better to take an agnostic approach and leave it as is unless liquidations are ultimately being limited because of this.

**[wukong-particle (Particle) acknowledged and commented](https://github.com/code-423n4/2023-12-particle-findings/issues/36#issuecomment-1868471782):**
 > I agree with the judge. We shouldn't facilitate to temper the blacklist. So only acknowledging the issue.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Particle Protocol |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-particle
- **GitHub**: https://github.com/code-423n4/2023-12-particle-findings/issues/36
- **Contest**: https://code4rena.com/reports/2023-12-particle

### Keywords for Search

`vulnerability`

