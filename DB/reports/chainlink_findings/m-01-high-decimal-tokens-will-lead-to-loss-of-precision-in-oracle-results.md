---
# Core Classification
protocol: Splits Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31835
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
github_link: none

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
finders_count: 1
finders:
  - Zach Obront
---

## Vulnerability Title

[M-01] High decimal tokens will lead to loss of precision in oracle results

### Overview


The Chainlink Oracle is a tool that calculates the relative price between two assets. However, when converting the calculated price into a final result, there is a loss of precision that can lead to incorrect results. This is due to the order of operations in the conversion function, which should be changed to avoid this issue. A proof of concept has been provided to demonstrate the problem and a recommendation has been made to fix it. The issue has been fixed in the codebase.

### Original Finding Content

When the Chainlink Oracle has calculated a relative price between two assets, it results in a `price`, which is always represented in 18 decimals. This price is used to convert the passed `baseAmount` into a final result:
```solidity
function _convertPriceToQuoteAmount(uint256 price_, QuoteParams calldata quoteParams_)
    internal
    view
    returns (uint256 finalAmount)
{
    uint8 baseDecimals = quoteParams_.quotePair.base._decimals();
    uint8 quoteDecimals = quoteParams_.quotePair.quote._decimals();

    finalAmount = price_ * quoteParams_.baseAmount / 10 ** baseDecimals;
    if (18 > quoteDecimals) {
        finalAmount = finalAmount / (10 ** (18 - quoteDecimals));
    } else if (18 < quoteDecimals) {
        finalAmount = finalAmount * (10 ** (quoteDecimals - 18));
    }
}
```
In the case of high decimal tokens, this function performs a large division before multiplying the amount back up by `(10 ** (quoteDecimals - 18))`. In that division and subsequent multiplication, there is a loss of precision that can lead to incorrect oracle results.

**Proof of Concept**

The following proof of concept pulls out the `_convertPriceToQuoteAmount()` function to display its behavior more clearly. We create two tokens with 24 decimals ([highest value I know of that exists in the wild](https://etherscan.io/address/0xaba8cac6866b83ae4eec97dd07ed254282f6ad8a)) and presume they have equal value (`price = 1e18`). We input `amount = 1e6 - 1` for `tokenA`, which should return an equal number of `tokenB`, but instead returns `0`.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import { Test, console2 } from "forge-std/Test.sol";
import { ERC20 } from "solmate/tokens/ERC20.sol";
import {QuotePair, QuoteParams} from "splits-utils/LibQuotes.sol";
import {TokenUtils} from "splits-utils/TokenUtils.sol";

contract MockERC20 is ERC20 {
    constructor(uint8 decimals_) ERC20("Token", "TKN", decimals_) {}
}

contract HighDecimalsTest is Test {
    using TokenUtils for address;

    function _convertPriceToQuoteAmount(uint256 price_, QuoteParams memory quoteParams_)
        internal
        view
        returns (uint256 finalAmount)
    {
        uint8 baseDecimals = quoteParams_.quotePair.base._decimals();
        uint8 quoteDecimals = quoteParams_.quotePair.quote._decimals();

        finalAmount = price_ * quoteParams_.baseAmount / 10 ** baseDecimals;
        if (18 > quoteDecimals) {
            finalAmount = finalAmount / (10 ** (18 - quoteDecimals));
        } else if (18 < quoteDecimals) {
            finalAmount = finalAmount * (10 ** (quoteDecimals - 18));
        }
    }


    function testZach_getQuoteAmtsHighDecimals() public {
        // deploy two high decimal ERC20s
        MockERC20 tokenA = new MockERC20(24);
        MockERC20 tokenB = new MockERC20(24);

        // let's assume these two tokens have equal value
        // oracle always returns 1e18 prices, so:
        uint price = 1e18;

        // if we try to convert tokenA to tokenB,
        // division by baseDecimals will round us down
        // for small amounts, this will round down to 0
        uint128 amount = 1e6 - 1;
        QuotePair memory quotePair = QuotePair({base: address(tokenA), quote: address(tokenB)});
        QuoteParams memory quoteParams = QuoteParams({quotePair: quotePair, baseAmount: amount, data: ""});

        assertEq(_convertPriceToQuoteAmount(price, quoteParams), 0);
    }
}
```

**Recommendation**

Change the order of operations in the relevant function so that multiplication comes before division:
```diff
function _convertPriceToQuoteAmount(uint256 price_, QuoteParams memory quoteParams_)
    internal
    view
    returns (uint256 finalAmount)
{
    uint8 baseDecimals = quoteParams_.quotePair.base._decimals();
    uint8 quoteDecimals = quoteParams_.quotePair.quote._decimals();

-   finalAmount = price_ * quoteParams_.baseAmount / 10 ** baseDecimals;
+   finalAmount = price_ * quoteParams_.baseAmount;
    if (18 > quoteDecimals) {
        finalAmount = finalAmount / (10 ** (18 - quoteDecimals));
    } else if (18 < quoteDecimals) {
        finalAmount = finalAmount * (10 ** (quoteDecimals - 18));
    }
+   finalAmount = finalAmount  / 10 ** baseDecimals;
}
```

**Review**

[Fixed as recommended.](https://github.com/0xSplits/splits-oracle/commit/082662d17a75cec02fe6b0e43c6f4a69360fc99d)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Splits Oracle |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

