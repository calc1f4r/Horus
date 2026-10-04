---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27646
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - arnie
---

## Vulnerability Title

USDC is not valued correctly in case of a depeg, which causes a loss of funds

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXManager.sol#L170-L214">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXManager.sol#L170-L214</a>


## Summary
USDC is not valued correctly in case of a depeg, which causes a loss of funds.
## Vulnerability Details
The protocol uses a chainlink feed to get prices of a specific token. In this case the token of interest is USDC which is a stable coin. Let us get some context for this issue, from the GMX V2 documentation we can read the following:
> In case the price of a stablecoin depegs from 1 USD:
To ensure that profits for all short positions can always be fully paid out, the contracts will pay out profits in the stablecoin based on a price of 1 USD or the current Chainlink price for the stablecoin, whichever is higher.
For swaps using the depegged stablecoin, a spread from 1 USD to the Chainlink price of the stablecoin will apply. If Chainlink Data Stream prices are used then the spread would be from the data stream and may not be to 1 USD.

https://gmx-docs.io/docs/trading/v2

From the above snippet we now know that gmx will never value USDC below 1$ when closing a short or withdrawing from a position, and that gmx uses the spread from 1 usd to the chainlink price is used. The problem here is that Steadefi does not account for this and will continue to use the chainlink price of usdc in a withdraw and swap when calculating the appropriate slippage amount. Let me demonstrate.

```solidity
function consult(address token) public view whenNotPaused returns (int256, uint8) {
    address _feed = feeds[token];

    if (_feed == address(0)) revert Errors.NoTokenPriceFeedAvailable();

    ChainlinkResponse memory chainlinkResponse = _getChainlinkResponse(_feed);
    ChainlinkResponse memory prevChainlinkResponse = _getPrevChainlinkResponse(_feed, chainlinkResponse.roundId);

    if (_chainlinkIsFrozen(chainlinkResponse, token)) revert Errors.FrozenTokenPriceFeed();
    if (_chainlinkIsBroken(chainlinkResponse, prevChainlinkResponse, token)) revert Errors.BrokenTokenPriceFeed();

    return (chainlinkResponse.answer, chainlinkResponse.decimals);
  }
``` 
Here consult calls `_getChainlinkResponse(_feed)` which gets the current value of a token, for our purpose this token is USDC. The problem begins because consult is called by `consultIn18Decimals` and this is called by `convertToUsdValue`, this is then called by `calcMinTokensSlippageAmt`. This function decides how much slippage is appropriate given the value of the asset being withdrawn. The problems is, as i showed, it will use chainlink value of USDC and in case of a depeg, it will use the depegged value. But as i have shown from gmx docs, when withdrawing, the value of USDC will always be valued at 1 or higher. So now we are calculating slippage for a usdc value that is depegged when we are withdrawing on gmx with the pegged assets normal value.

For example
1. there is a depeg of usdc
2. usdc chainlink value is $ 0.4
3. gmx withdraw value is always $1

because we use the chainlink value to calc slippage tolerance, we will be using the slippage tolerance for a USDC price of 0.4 when in fact we are valuing USDC at $1 in gmx. The amount of slippage allowed will be very incorrect and in some cases extreme. In case of total depeg, slippage will be almost 99% and users may lose almost all of their funds when trying to withdraw.

## Impact
In case of total depeg, slippage will be almost 99% and users may lose almost all of their funds when trying to withdraw.
## Tools Used
manual review
## Recommendations
implement logic specific to stablecoins to handle depegs events. Such would be to always value stable coins at the maximum of the stablecoing proposed value and the chainlink response value. Currently we are only using the chainlink response answer to valuate stable coins like usdc, and as i have explained this is a problem.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | arnie |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

