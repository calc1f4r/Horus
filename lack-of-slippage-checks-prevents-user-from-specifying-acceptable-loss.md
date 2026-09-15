---
# Core Classification
protocol: AladdinDAO f(x) Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31040
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
github_link: none

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
finders_count: 2
finders:
  - Troy Sargent
  - Robert Schneider
---

## Vulnerability Title

Lack of slippage checks prevents user from specifying acceptable loss

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Medium

## Type: Data Validation

## Target: contracts/gateways/facets/FxUSDFacet.sol

## Description

The router contract to interact with the FxUSD contract and Market contract does not allow specifying slippage limits for redeeming xToken and minting FxUSD, respectively. Note, there is a slippage check for the target asset in the Facet contract but not for the intermediary assets exchanged during the multi-leg “swap”.

```sol
uint256 _baseOut = IFxMarketV2(_market).redeemXToken(_amountIn, address(this), 0);
```
**Figure 14.1:** Lack of slippage check on redeeming xToken  
(aladdin-v3-contracts/contracts/gateways/facets/FxUSDFacet.sol#205)

```sol
uint256 _fxUSDMinted = IFxUSD(fxUSD).mint(_baseTokenIn, _amountIn, address(this), 0);
```
**Figure 14.2:** Lack of slippage check on minting FxUSD  
(aladdin-v3-contracts/contracts/gateways/facets/FxUSDFacet.sol#355)

This also affects the Balancer wrapper contract, which was not in the scope of our review.

```sol
function unwrap(uint256 _amount) external override returns (uint256) {
    address[] memory _assets = new address[](2);
    uint256[] memory _amounts = new uint256[](2);
    _assets[srcIndex] = src;
    _assets[1 - srcIndex] = WETH;
    uint256 _balance = IERC20(src).balanceOf(msg.sender);
    IBalancerVault(BALANCER_VAULT).exitPool(
        poolId,
        address(this),
        msg.sender,
        IBalancerVault.ExitPoolRequest({
            assets: _assets,
            minAmountsOut: _amounts,
```
**Figure 14.3:** Lack of slippage check on Balancer swap  
(aladdin-v3-contracts/contracts/f(x)/wrapper/FxTokenBalancerV2Wrapper.sol#89–102)

## Recommendations

- **Short term:** Allow users to specify a slippage tolerance for all paths.
- **Long term:** Do not hard-code arguments that users should be able to input, especially ones that protect against losses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AladdinDAO f(x) Protocol |
| Report Date | N/A |
| Finders | Troy Sargent, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

