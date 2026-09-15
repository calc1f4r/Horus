---
# Core Classification
protocol: Redacted Cartel
chain: everychain
category: uncategorized
vulnerability_type: hardcoded_address

# Attack Vector Details
attack_type: hardcoded_address
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6042
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-redacted-cartel-contest
source_link: https://code4rena.com/reports/2022-11-redactedcartel
github_link: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/132

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 2

# Context Tags
tags:
  - hardcoded_address

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - ladboy233
  - gzeon
---

## Vulnerability Title

[M-05] `SWAP_ROUTER` in `AutoPxGmx.sol` is hardcoded and not compatible on Avalanche

### Overview


This bug report is about a vulnerability found in the code of a project hosted on GitHub. The code in question is located at three different lines: 18, 96, and 268 in the file AutoPxGmx.sol. The vulnerability is that the code is intended to support an Avalanche side-chain, but the SWAP_ROUTER is hardcoded as an address for Uniswap V3 router address in arbitrium, which is a EOA address in Avalanche. This means that the AutoPxGmx.sol is not working in Avalanche. The code below reverts because the EOA address on Avalanche does not have exactInputSingle method in compound method, as can be seen in the code snippet provided. The bug was discovered through manual review.

To mitigate this vulnerability, we recommend that the project not hardcode the SWAP_ROUTER in AutoPxGmx.sol, and instead pass this parameter in the constructor.

### Original Finding Content


<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L18>

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L96>

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L268>

### Impact

I want to quote from the doc:

```solidity
- Does it use a side-chain? Yes
- If yes, is the sidechain evm-compatible? Yes, Avalanche
```

This shows that the projects is intended to support Avalanche side-chain.

`SWAP_ROUTER` in the AutoPxGmx.sol is hardcoded as:

```solidity
IV3SwapRouter public constant SWAP_ROUTER =
	IV3SwapRouter(0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45);
```

But this address is the Uniswap V3 router address in arbitrium, but it is a EOA address in Avalanche,

<https://snowtrace.io/address/0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45>

Then the AutoPxGmx.sol is not working in Avalanche.

```solidity
gmxAmountOut = SWAP_ROUTER.exactInputSingle(
	IV3SwapRouter.ExactInputSingleParams({
		tokenIn: address(gmxBaseReward),
		tokenOut: address(gmx),
		fee: fee,
		recipient: address(this),
		amountIn: gmxBaseRewardAmountIn,
		amountOutMinimum: amountOutMinimum,
		sqrtPriceLimitX96: sqrtPriceLimitX96
	})
);
```

### Proof of Concept

The code below reverts because the EOA address on Avalanche does not have exactInputSingle method in compound method.

```solidity
gmxAmountOut = SWAP_ROUTER.exactInputSingle(
	IV3SwapRouter.ExactInputSingleParams({
		tokenIn: address(gmxBaseReward),
		tokenOut: address(gmx),
		fee: fee,
		recipient: address(this),
		amountIn: gmxBaseRewardAmountIn,
		amountOutMinimum: amountOutMinimum,
		sqrtPriceLimitX96: sqrtPriceLimitX96
	})
);
```

```solidity
/**
	@notice Compound pxGMX rewards
	@param  fee                    uint24   Uniswap pool tier fee
	@param  amountOutMinimum       uint256  Outbound token swap amount
	@param  sqrtPriceLimitX96      uint160  Swap price impact limit (optional)
	@param  optOutIncentive        bool     Whether to opt out of the incentive
	@return gmxBaseRewardAmountIn  uint256  GMX base reward inbound swap amount
	@return gmxAmountOut           uint256  GMX outbound swap amount
	@return pxGmxMintAmount        uint256  pxGMX minted when depositing GMX
	@return totalFee               uint256  Total platform fee
	@return incentive              uint256  Compound incentive
 */
function compound(
	uint24 fee,
	uint256 amountOutMinimum,
	uint160 sqrtPriceLimitX96,
	bool optOutIncentive
)
```

### Recommended Mitigation Steps

We recommend the project not hardcode the `SWAP_ROUTER `in AutoPxGmx.sol, can pass this parameter in the constructor.

**[kphed (Redacted Cartel) commented](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/132#issuecomment-1404064316):**
> The core set of contracts currently functions for both Arbitrum and Avalanche, but the AutoPxGmx contract does not (the auto-compounding contracts are part of the non-core "Easy Mode" offering). We're aware of this and are holding off on completing those changes launching on Avalanche until after our Arbitrum launch goes smoothly. Thank you for participating in our C4 contest!



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Redacted Cartel |
| Report Date | N/A |
| Finders | ladboy233, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-redactedcartel
- **GitHub**: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/132
- **Contest**: https://code4rena.com/contests/2022-11-redacted-cartel-contest

### Keywords for Search

`Hardcoded Address`

