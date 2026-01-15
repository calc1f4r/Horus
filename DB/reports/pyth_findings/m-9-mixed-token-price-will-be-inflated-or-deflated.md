---
# Core Classification
protocol: Debita Finance V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44237
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/627
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-debita-judging/issues/362

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
finders_count: 2
finders:
  - jsmi
  - dimulski
---

## Vulnerability Title

M-9: Mixed Token Price Will Be Inflated or Deflated

### Overview


The issue reported is regarding a logical error in the `MixOracle::getThePrice()` function, which can cause the price of a token to be incorrectly inflated or deflated. This happens when token pairs with different decimal scales are used, leading to inaccurate pricing data. The root cause of this issue is a discrepancy in using the wrong variable for scaling. This can result in incorrect exchange rates and loss of funds for users or systems relying on this data. The suggested mitigation is to replace the incorrect variable with the correct one. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-debita-judging/issues/362 

## Found by 
dimulski, jsmi
### Summary

The `MixOracle::getThePrice()` function contains a logical error, causing the calculated price of a token to be incorrectly inflated or deflated. This issue arises when token pairs with differing decimal scales are used, leading to inaccurate pricing data.


### Root Cause

1. The problem lies in the following function:
https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/main/Debita-V3-Contracts/contracts/oracles/MixOracle/MixOracle.sol#L40-L70
```solidity
    function getThePrice(address tokenAddress) public returns (int) {
        // get tarotOracle address
        address _priceFeed = AttachedTarotOracle[tokenAddress];
        require(_priceFeed != address(0), "Price feed not set");
        require(!isPaused, "Contract is paused");
        ITarotOracle priceFeed = ITarotOracle(_priceFeed);

        address uniswapPair = AttachedUniswapPair[tokenAddress];
        require(isFeedAvailable[uniswapPair], "Price feed not available");
        // get twap price from token1 in token0
        (uint224 twapPrice112x112, ) = priceFeed.getResult(uniswapPair);
        address attached = AttachedPricedToken[tokenAddress];

        // Get the price from the pyth contract, no older than 20 minutes
        // get usd price of token0
        int attachedTokenPrice = IPyth(debitaPythOracle).getThePrice(attached);
        uint decimalsToken1 = ERC20(attached).decimals();
57:     uint decimalsToken0 = ERC20(tokenAddress).decimals();

        // calculate the amount of attached token that is needed to get 1 token1
        int amountOfAttached = int(
61:         (((2 ** 112)) * (10 ** decimalsToken1)) / twapPrice112x112
        );

        // calculate the price of 1 token1 in usd based on the attached token
        uint price = (uint(amountOfAttached) * uint(attachedTokenPrice)) /
66:         (10 ** decimalsToken1);

        require(price > 0, "Invalid price");
        return int(uint(price));
    }
```
Here, `decimalsToken1` is mistakenly used for scaling instead of `decimalsToken0` in line `66`. This discrepancy is critical when the token pair has different decimals. Furthermore, the variable `decimalsToken0` is defined but not utilized anywhere else in the function, highlighting a clear logical oversight.


### Internal pre-conditions

The admin sets token pairs in the `MixOracle` where the tokens have differing decimals (e.g., `USDC` with `6` decimals and `DAI` with `18` decimals).


### External pre-conditions

_No response_

### Attack Path

1. Assume `MixOracle::getThePrice()` is called with `tokenAddress = DAI`.
2. In the contract:
    - `decimalsToken0 = 1e18` (`DAI` has `18` decimals).
    - `decimalsToken1 = 1e6` (`USDC` has `6` decimals).
3. Due to the logical error in line `66`, the token price will be inflated by `1e12` (or deflated in other cases), depending on the tokens in the pair.
4. This incorrect price propagation may result in:
    - Incorrect exchange rates.
    - Loss of funds for users or systems relying on this data.


### Impact

Mix oracle get the inflated/deflated price, leading to the loss of funds.


### PoC

_No response_

### Mitigation

In line `61`, replace `decimalsToken1` with `decimalsToken0`.
```diff
        uint price = (uint(amountOfAttached) * uint(attachedTokenPrice)) /
-           (10 ** decimalsToken1);
+           (10 ** decimalsToken0);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Debita Finance V3 |
| Report Date | N/A |
| Finders | jsmi, dimulski |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-debita-judging/issues/362
- **Contest**: https://app.sherlock.xyz/audits/contests/627

### Keywords for Search

`vulnerability`

