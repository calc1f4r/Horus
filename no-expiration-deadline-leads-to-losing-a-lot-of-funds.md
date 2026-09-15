---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34515
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 38
finders:
  - offkey
  - ni8mare
  - Daniel526
  - dacian
  - fakemonkgin
---

## Vulnerability Title

No expiration deadline leads to losing a lot of funds

### Overview


This bug report is about a bug in the `Fees::sellProfits()` function of the `Fees` contract. The function does not have an expiration deadline, which means that it can accept token swaps at any block number. This can result in losing a lot of funds when swapping tokens. The bug has a medium risk and the vulnerability details can be found on GitHub. The impact of this bug is that a malicious miner/validator can hold a transaction until they favor it or make a profit, causing the `Fees` contract to lose funds. The recommendation is to set a proper timestamp for the `deadline` parameter to prevent this from happening. This bug was found through a manual review.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Fees.sol#L36">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Fees.sol#L36</a>


## Summary

The `Fees::sellProfits()` does not set an expiration deadline, resulting in losing a lot of funds when swapping tokens.

## Vulnerability Details

The `deadline` parameter in the `sellProfits()` is set to `block.timestamp`. That means the function will accept a token swap at any block number (i.e., no expiration deadline). 

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
@>              deadline: block.timestamp,
                amountIn: amount,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        amount = swapRouter.exactInputSingle(params);
        IERC20(WETH).transfer(staking, IERC20(WETH).balanceOf(address(this)));
    }
```

https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Fees.sol#L36

## Impact

Without an expiration deadline, a malicious miner/validator can hold a transaction until they favor it or they can make a profit. As a result, the `Fees` contract can lose a lot of funds from slippage.

## Tools Used

Manual Review

## Recommendations

I recommend setting the `deadline` parameter with a proper timestamp.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | offkey, ni8mare, Daniel526, dacian, fakemonkgin, 0xSmartContract, 0xAsen, Yanev, qbs, Breeje, JohnnyTime, sonny2k, jnrlouis, serialcoder, 0xJuda, Silvermist, pks27, Vagner, Norah, aviggiano, Harut, Martin, niluke, crippie, smbv1923, Madalad, 0x3b, gkrastenov, nabeel, Bauchibred, castleChain, hlx, PTolev, ABA, 0xCiphky, rvierdiiev, ZedBlockchain, jonatascm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

