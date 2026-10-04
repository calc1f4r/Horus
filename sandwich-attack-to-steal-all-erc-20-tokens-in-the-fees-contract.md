---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: economic
vulnerability_type: sandwich_attack

# Attack Vector Details
attack_type: sandwich_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34500
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
  - sandwich_attack

# Audit Details
report_date: unknown
finders_count: 19
finders:
  - 0xAsen
  - 0xyPhilic
  - Arabadzhiev
  - Lalanda
  - 0xAadhi
---

## Vulnerability Title

Sandwich attack to steal all ERC-20 tokens in the Fees contract

### Overview


The Fees contract has a high-risk bug that allows attackers to steal all ERC-20 tokens locked in the contract. The `sellProfits()` function can be called by anyone and lacks protection against price manipulation. This means an attacker can use a flash loan to drain all tokens (such as USDC, DAI, CRV) from the contract. To fix this, the function should only be accessible to the contract owner and the parameters should be adjusted to prevent price manipulation. This is a serious issue and should be fixed as soon as possible.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Fees.sol#L38-L39">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Fees.sol#L38-L39</a>


## Summary

The `Fees::sellProfits()` lacks slippage protection, resulting in being attacked by a sandwich attack to drain all locked ERC-20 tokens.

## Vulnerability Details

The `sellProfits()` is a permissionless function that can be called by anyone. The function lacks [slippage protection](https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Fees.sol#L38-L39) (the parameters `amountOutMinimum` and `sqrtPriceLimitX96` are set to 0) when swapping tokens through Uniswap's pools. 

In this way, an attacker can launch a sandwich attack with a flash loan to drain all ERC-20 tokens (e.g., USDC, DAI, CRV, etc.) locked in the `Fees` contract. 

For instance, to drain all USDC, consider the following proof-of-concept.
1. Attacker borrows a flash loan for USDC and buys WETH from Uniswap's WETH/USDC pool.
2. Attacker executes the `sellProfits(USDC)`.
3. The `sellProfits()` will spend all locked USDC for buying WETH at a very high price.
4. Attacker sells the previously obtained WETH for USDC at the same pool and repays the flash loan.
5. Attacker takes all locked USDC as profit.

Moreover, an attacker can perform steps 1-5 above to steal other ERC-20 tokens locked in the `Fees` contract.

```solidity
    function sellProfits(address _profits) public {
        require(_profits != WETH, "not allowed");
        uint256 amount = IERC20(_profits).balanceOf(address(this));

        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
            .ExactInputSingleParams({
                tokenIn: _profits,
                tokenOut: WETH,
                fee: 3000,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: amount,
@>              amountOutMinimum: 0,
@>              sqrtPriceLimitX96: 0
            });

        amount = swapRouter.exactInputSingle(params);
        IERC20(WETH).transfer(staking, IERC20(WETH).balanceOf(address(this)));
    }
```

https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Fees.sol#L38-L39

## Impact

An attacker can drain all ERC-20 tokens (e.g., USDC, DAI, CRV, etc.) locked in the `Fees` contract. Therefore, I consider this vulnerability a high-risk issue.

## Tools Used

Manual Review

## Recommendations

I recommend adding the `onlyOwner` modifier and setting the `amountOutMinimum` parameter to protect price slippage from MEV bots. If necessary, specify the `sqrtPriceLimitX96` parameter to set a stop price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | 0xAsen, 0xyPhilic, Arabadzhiev, Lalanda, 0xAadhi, JohnnyTime, InAllHonesty, Auditism, 0xdeth, serialcoder, 0xcm, Rotcivegaf, B353N, 0x4non, Bauer, ABA, djanerch, 0xWeb3boy |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`Sandwich Attack`

