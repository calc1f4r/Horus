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
solodit_id: 31045
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

Unclear economic sustainability of allowing user to avoid liquidations

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

## Target: contracts/f(x)/v2/FxUSD.sol

## Description
The FxUSD contracts allow moving fToken from the rebalance pool into them and minting FxUSD. (This method is used to attempt to increase the collateral ratio by burning fToken.) Moving tokens in this way is allowed even when liquidations are possible (i.e., the collateral ratio is sufficiently low). The rebalance pool is intended to socialize the losses among fToken depositors, but nothing prevents withdrawing prior to liquidation transactions. This does not ensure that all depositors are on the hook for liquidation. 

Users who front-run liquidations and withdraw from the rebalance pool will not have the liquidated collateral credited to their share of rewards from the rebalance pool, but they will retain their balance of fToken. Since redeeming fToken may be the only action for re-collateralizing the protocol if xToken minting is failing (TOB-ADFX-18), allowing withdrawals during stability mode may threaten the ability of the protocol to recover from delinquency.

```solidity
function wrapFrom (
    address _pool,
    uint256 _amount,
    address _receiver
) external override onlySupportedPool(_pool) {
    if (isUnderCollateral()) revert ErrorUnderCollateral();
    address _baseToken = IFxShareableRebalancePool(_pool).baseToken();
    _checkBaseToken(_baseToken);
    _checkMarketMintable(_baseToken, false);
    IFxShareableRebalancePool(_pool).withdrawFrom(_msgSender(), _amount, address(this));
    _mintShares(_baseToken, _receiver, _amount);
    emit Wrap(_baseToken, _msgSender(), _receiver, _amount);
}
```
*Figure 20.1: Users can withdraw from the rebalance pool and mint FxUSD in stability mode (aladdin-v3-contracts/contracts/f(x)/v2/FxUSD.sol#160–175)*

```solidity
function liquidate(uint256 _maxAmount, uint256 _minBaseOut)
    external
    override
    onlyRole(LIQUIDATOR_ROLE)
    returns (uint256 _liquidated, uint256 _baseOut)
{
    [...]
    // distribute liquidated base token
    _accumulateReward(_token, _baseOut);
    // notify loss
    _notifyLoss(_liquidated);
}
```
*Figure 20.1: Users who evade liquidation miss rewards and avoid losses (aladdin-v3-contracts/contracts/f(x)/rebalance-pool/ShareableRebalancePoolV2.sol#35–82)*

## Recommendations
**Short term**: Consider preventing withdrawals from the rebalance pool when the fToken’s treasury’s collateral ratio is below the stability ratio and thus able to be liquidated. 

**Long term**: Perform additional economic analysis regarding liquidations and whether the incentives of fToken holders and FxUSD holders align with the protocol’s interests.

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

