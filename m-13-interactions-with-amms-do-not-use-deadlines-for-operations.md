---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 15996
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/429

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
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - IllIllI
---

## Vulnerability Title

[M-13] Interactions with AMMs do not use deadlines for operations

### Overview


This bug report is about a vulnerability in the code of a decentralized application (dApp) called ParaSpace. It is related to the "DecreaseLiquidity" function, which is used to reduce the liquidity of a token in an automated market maker (AMM) pool. The bug is that the function is passing the "block.timestamp" parameter to the pool, which means that whenever the miner decides to include the transaction in a block, it will be valid at that time. This could lead to a situation where a malicious miner holds the transaction, which may be done in order to free up capital to prevent a liquidation. It is also possible that a miner might wait until maximum slippage is incurred. The recommended mitigation step is to add deadline arguments to all functions that interact with AMMs, and pass it along to AMM calls.

### Original Finding Content


From a judge's comment in a previous [contest](https://code4rena.com/reports/2022-06-canto-v2/#m-01-stableswap---deadline-do-not-work):

```md
Because Front-running is a key aspect of AMM design, deadline is a useful tool to ensure that your tx cannot be “saved for later”.

Due to the removal of the check, it may be more profitable for a miner to deny the transaction from being mined until the transaction incurs the maximum amount of slippage.
```

Most of the functions that interact with AMM pools do not have a deadline parameter, but specifically the one shown below is passing `block.timestamp` to a pool, which means that whenever the miner decides to include the txn in a block, it will be valid at that time, since `block.timestamp` will *be* the current timestamp.

### Proof of Concept

```solidity
File: /paraspace-core/contracts/protocol/tokenization/NTokenUniswapV3.sol   #1

51       function _decreaseLiquidity(
52           address user,
53           uint256 tokenId,
54           uint128 liquidityDecrease,
55           uint256 amount0Min,
56           uint256 amount1Min,
57           bool receiveEthAsWeth
58       ) internal returns (uint256 amount0, uint256 amount1) {
59           if (liquidityDecrease > 0) {
60               // amount0Min and amount1Min are price slippage checks
61               // if the amount received after burning is not greater than these minimums, transaction will fail
62               INonfungiblePositionManager.DecreaseLiquidityParams
63                   memory params = INonfungiblePositionManager
64                       .DecreaseLiquidityParams({
65                           tokenId: tokenId,
66                           liquidity: liquidityDecrease,
67                           amount0Min: amount0Min,
68                           amount1Min: amount1Min,
69 @>                        deadline: block.timestamp
70                       });
71   
72               INonfungiblePositionManager(_underlyingAsset).decreaseLiquidity(
73                   params
74               );
75           }
76:  
```

<https://github.com/code-423n4/2022-11-paraspace/blob/c6820a279c64a299a783955749fdc977de8f0449/paraspace-core/contracts/protocol/tokenization/NTokenUniswapV3.sol#L51-L76>

A malicious miner can hold the transaction, which may be being done in order to free up capital to ensure that there are funds available to do operations to prevent a liquidation. It is highly likely that a liquidation is more profitable for a miner to mine, with its associated follow-on transactions, than to allow the decrease of liquidity. A miner can also just hold it until maximum slippage is incurred, as the judge stated.

### Recommended Mitigation Steps

Add deadline arguments to all functions that interact with AMMs, and pass it along to AMM calls.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | IllIllI |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/429
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

