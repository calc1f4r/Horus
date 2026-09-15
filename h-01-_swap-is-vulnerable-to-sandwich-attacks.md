---
# Core Classification
protocol: Gacha_2025-01-27
chain: everychain
category: economic
vulnerability_type: sandwich_attack

# Attack Vector Details
attack_type: sandwich_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53302
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Gacha-security-review_2025-01-27.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - sandwich_attack

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] `_swap()` is vulnerable to sandwich attacks

### Overview


This bug report describes a high severity issue where anyone can buy a ticket from a specified pool and use a payment token to swap for meme tokens. The swapping process includes a dynamic calculation of a minimum token amount, which can be manipulated by attackers through front-running. This allows them to profit from the price movement of the meme token. The recommendation is to calculate the minimum token amount on the frontend and pass it as an input parameter to the GachaTickets#purchase() function.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

Anyone can buy a ticket from a specified pool, a certain payment token will be used to swap for meme tokens. The swapping process is implemented as below:

```solidity
    function _swap(
        address token,
        uint256 cost
    ) private returns (uint256 actualTokens) {
        Storage storage $ = _getOwnStorage();
        IUniswapV2Router01 uni = IUniswapV2Router01($.uniswapRouter);
        IUniswapV2Factory factory = IUniswapV2Factory($.uniswapFactory);

        address pair = factory.getPair($.paymentToken, token);
        (uint256 wethReserve, uint256 tokenReserve, ) = IUniswapV2Pair(pair)
            .getReserves();
        if (wethReserve == 0 || tokenReserve == 0) revert InvalidPair();

@>      uint256 maxTokens = uni.getAmountOut(cost, wethReserve, tokenReserve); // includes 0.3%
@>      uint256 minTokens = Math.mulDiv(maxTokens, 95, 100); // 5% slippage

        address[] memory path = new address[](2);
        path[0] = $.paymentToken;
        path[1] = token;

        IERC20($.paymentToken).approve($.uniswapRouter, cost);
        uint256[] memory amounts = uni.swapExactTokensForTokens(
            cost,
@>          minTokens,
            path,
            address(this),
            block.timestamp + 1
        );
        actualTokens = amounts[amounts.length - 1];
    }
```

Before swapping for meme tokens using `uni.swapExactTokensForTokens()`, a `minTokens` amount is calculated. This value serves as a slippage protection measure. However it is calculated dynamically, attackers can manipulate the price by front-running the meme token purchase, buying the token before the ticket purchase, and then selling it immediately after, profiting from the price movement.

## Recommendations

`minTokens` should be calculated on the frontend and passed as an input parameter to `GachaTickets#purchase()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Gacha_2025-01-27 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Gacha-security-review_2025-01-27.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Sandwich Attack`

