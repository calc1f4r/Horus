---
# Core Classification
protocol: Radiant V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32844
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Initial Liquidity Can Be Lost by Front-Running Pool Initialization

### Overview


This bug report discusses an issue with the `UniswapPoolHelper` and `BalancerPoolHelper` contracts, which are responsible for creating new liquidity pools for the RDNT token. These contracts have an `initializePool` function that is currently unrestricted, allowing anyone to execute it. This creates a front-running scenario where an attacker can monitor the mempool and take advantage of the protocol owners sending tokens to the contract to provide liquidity and receive LP tokens. To fix this, the report suggests adding an `onlyOwner` modifier to the `initializePool` function or implementing an atomic flow of contract deployment, transfer of funds, and pool initialization. The bug has been resolved in a recent pull request by adding the `onlyOwner` modifier to both `initializePool` functions.

### Original Finding Content

Both the [`UniswapPoolHelper`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/zap/helpers/UniswapPoolHelper.sol#L56-L80) and [`BalancerPoolHelper`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/zap/helpers/BalancerPoolHelper.sol#L71-L142) contracts implement an `initializePool` function that is responsible for creating a new liquidity pool for the RDNT token paired with a base token. In the currently deployed contracts, RDNT is paired with WETH on Arbitrum and WBNB on Binance Smart Chain. In the case of Uniswap, this initialization will revert if a pair has already been created.


The logic in both pool initialization functions expects the input RDNT/WETH or RDNT/WBNB tokens to be sent to the respective helper contract in advance, before calling either `initializePool` function. This is outlined in the deployment script for [UniswapPoolHelper](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/deploy/core/004_deploy_zappers.ts#L69-L91) and [BalancerPoolHelper](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/deploy/core/004_deploy_zappers.ts#L129-L135) as a manual set of transactions, instead of being executed atomically. After depositing liquidity into a pool, the respective `initializePool` function will send the received liquidity (LP) tokens to the caller (see [here](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/zap/helpers/UniswapPoolHelper.sol#L77) and [here](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/zap/helpers/BalancerPoolHelper.sol#L141)).


However, access to these `initializePool` functions is unrestricted, which allows any user to perform the pool initialization step. This leads to the front-running scenario where an attacker monitors the mempool and waits for the protocol owners to send RDNT and WETH tokens to the contract, and then front-runs the `initializePool` transaction, or alternatively (on Layer 2 chains that do not feature public mempools), the attacker can back-run the second token transfer to accomplish the same goal. The existing RDNT and WETH or WBNB contract balances will then be used to provide liquidity and send the minted LP tokens to the attacker.


Consider adding the `onlyOwner` modifier to the `initializePool` functions of `UniswapPoolHelper` and `BalancerPoolHelper` to ensure they can only be executed by the protocol owners, and/or implementing an atomic flow of contract deployment, transfer of funds, and pool initialization.


***Update:** Resolved in [pull request #177](https://github.com/radiant-capital/v2-core/pull/177) at commit [7ce4838](https://github.com/radiant-capital/v2-core/commit/7ce48386b9d7a76e17ee66924a11e5a49d1b9a1e). The `onlyOwner` modifier was added to both `initializePool` functions.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

