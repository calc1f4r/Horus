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
solodit_id: 31046
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

Validation of system invariants is error prone

### Overview

See description below for full details.

### Original Finding Content

## Target Contracts

- `contracts/f(x)/v2/TreasuryV2.sol`
- `contracts/f(x)/v2/MarketV2.sol`
- `contracts/f(x)/v2/FxUSD.sol`

## Description

The architecture of the f(x) protocol is interleaved, and its interactions are complex. The interdependencies of the components are not managed well, and validations are distributed in disparate components rather than maintaining logical separation. We recommend simplifying the architecture and refactoring assertions about how the state is updated to be closely tied to where the state is updated. This is especially important in light of the concerns related to stability and incentives and lack of specification, as logical errors and economic issues may be coupled together. Making these investments will strengthen the security posture of the system and facilitate invariant testing.

The Treasury does not validate the postcondition that the collateral ratio increases when minting xToken and redeeming fToken. In stability mode, liquidations perform fToken redemptions to attempt re-collateralizing the protocol to a collateral ratio above the stability ratio.

```solidity
function redeemFToken(
    uint256 _fTokenIn,
    address _recipient,
    uint256 _minBaseOut
) external override nonReentrant returns (uint256 _baseOut, uint256 _bonus) {
    if (redeemPaused()) revert ErrorRedeemPaused();
    if (_fTokenIn == type(uint256).max) {
        _fTokenIn = IERC20Upgradeable(fToken).balanceOf(_msgSender());
    }
    if (_fTokenIn == 0) revert ErrorRedeemZeroAmount();
    uint256 _stabilityRatio = stabilityRatio();
    (uint256 _maxBaseOut, uint256 _maxFTokenInBeforeSystemStabilityMode) =
        IFxTreasuryV2(treasury).maxRedeemableFToken(_stabilityRatio);
    uint256 _feeRatio = _computeFTokenRedeemFeeRatio(_fTokenIn, _maxFTokenInBeforeSystemStabilityMode);
    _baseOut = IFxTreasuryV2(treasury).redeem(_fTokenIn, 0, _msgSender());
}
```

**Figure 21.1:** Treasury lacks postcondition that collateral ratio increases for fToken redemptions  
*(aladdin-v3-contracts/contracts/f(x)/v2/MarketV2.sol#301–319)*

The Treasury does not validate the postcondition that the collateral ratio is not below the stability ratio, allowing immediate liquidations when minting fToken. The credit health is softly enforced by the `maxMintableFToken` math library function used in the Market and by the FxUSD contract (when enabled), but it would be more robust to strictly require the collateral ratio has not fallen too far when performing mint actions to prevent insolvency. This applies to redeeming xToken as well since it is also expected to reduce the collateral ratio like minting fToken.

```solidity
function mintFToken(uint256 _baseIn, address _recipient)
    external
    override
    onlyRole(FX_MARKET_ROLE)
    returns (uint256 _fTokenOut)
{
}
```

```solidity
FxStableMath.SwapState memory _state = _loadSwapState(Action.MintFToken);
if (_state.xNav == 0) revert ErrorUnderCollateral();
if (_state.baseSupply + _baseIn > baseTokenCap) revert ErrorExceedTotalCap();
_updateEMALeverageRatio(_state);
_fTokenOut = _state.mintFToken(_baseIn);
totalBaseToken = _state.baseSupply + _baseIn;
IFxFractionalTokenV2(fToken).mint(_recipient, _fTokenOut);
```

**Figure 21.2:** Treasury lacks postcondition that collateral ratio is greater than stability ratio  
*(aladdin-v3-contracts/contracts/f(x)/v2/TreasuryV2.sol#286–303)*

While the Market charges extra fees when too much is minted, the fees aren’t deposited as collateral in the Treasury, and this added complexity increases the likelihood of bugs. In pursuit of simplicity, we recommend disallowing minting excess beyond `_maxBaseInBeforeSystemStabilityMode` and only allowing minting up to the maximum amount. Currently, the minted amount is only bound if the `fTokenMintPausedInStabilityMode` is explicitly enabled but not by default. This has the added benefit of making validation and testing/verification easier to perform.

```solidity
(uint256 _maxBaseInBeforeSystemStabilityMode,) =
    IFxTreasuryV2(treasury).maxMintableFToken(_stabilityRatio);
if (_maxBaseInBeforeSystemStabilityMode > 0) {
    _maxBaseInBeforeSystemStabilityMode = IFxTreasuryV2(treasury).getWrappedValue(_maxBaseInBeforeSystemStabilityMode);
}
if (fTokenMintPausedInStabilityMode()) {
    uint256 _collateralRatio = IFxTreasuryV2(treasury).collateralRatio();
    if (_collateralRatio <= _stabilityRatio) revert ErrorFTokenMintPausedInStabilityMode();
    // bound maximum amount of base token to mint fToken.
    if (_baseIn > _maxBaseInBeforeSystemStabilityMode) {
        _baseIn = _maxBaseInBeforeSystemStabilityMode;
    }
}
uint256 _amountWithoutFee = _deductFTokenMintFee(_baseIn, _maxBaseInBeforeSystemStabilityMode);
IERC20Upgradeable(baseToken).safeTransferFrom(_msgSender(), treasury, _amountWithoutFee);
_fTokenMinted = IFxTreasuryV2(treasury).mintFToken(
    IFxTreasuryV2(treasury).getUnderlyingValue(_amountWithoutFee),
    _recipient
);
```

**Figure 21.3:** Excess minting is permitted for additional fee  
*(aladdin-v3-contracts/contracts/f(x)/v2/MarketV2.sol#226–249)*

Rather than having the Treasury validate that it is solvent, the validation is performed in FxUSD (which requires calling the Market and Treasury). This makes the composability of the system fragile as modifying a contract locally can have far-reaching consequences that are not apparent in the scope of the diff. Important validations related to core invariants should be clearly documented and be performed as close as possible to the component they are relevant to.

```solidity
function _checkMarketMintable(address _baseToken, bool _checkCollateralRatio) private view {
    address _treasury = markets[_baseToken].treasury;
    if (_checkCollateralRatio) {
        uint256 _collateralRatio = IFxTreasuryV2(_treasury).collateralRatio();
        uint256 _stabilityRatio = IFxMarketV2(markets[_baseToken].market).stabilityRatio();
        // not allow to mint when collateral ratio <= stability ratio 
        if (_collateralRatio <= _stabilityRatio) revert ErrorMarketInStabilityMode();
    }
    // not allow to mint when price is invalid
    if (!IFxTreasuryV2(_treasury).isBaseTokenPriceValid()) revert ErrorMarketWithInvalidPrice();
}
```

**Figure 21.4:** FxUSD performs validation that should be in the core Treasury  
*(aladdin-v3-contracts/contracts/f(x)/v2/FxUSD.sol#391–401)*

Rather than validating that the mint cap of fToken is reached in the FractionalToken implementation, it is done in FxUSD. This does not consider when FxUSD has not been added to the Market, and the validation should be done in the token implementation instead. In general, performing validations against other contracts’ state variables instead of having the contract maintain the invariant is error-prone.

```solidity
if (IERC20Upgradeable(_fToken).totalSupply() > _mintCap) revert ErrorExceedMintCap();
```

**Figure 21.5:** FxUSD enforces fToken mint cap instead of the token doing it  
*(aladdin-v3-contracts/contracts/f(x)/v2/FxUSD.sol#422)*

## Recommendations

**Short term:** Validate that the collateral ratio has increased for minting xToken and redeeming fToken and that minting fToken and redeeming xToken do not put the collateral ratio below the stability ratio, allowing for immediate liquidations. While certain configurations of fees may be sufficient to prevent unexpected behavior, it is more robust to simply prohibit actions which have undesired effects.

**Long term:** Perform validations specific to a component locally rather than sporadically performing validations in separate components. Simplify the architecture by refactoring disjointed components and make each component strictly validate itself. Create specifications for each component and their interactions, and perform invariant testing to ensure the specification matches the implementation.

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

