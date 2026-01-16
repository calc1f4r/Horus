---
# Core Classification
protocol: Growth Labs GSquared
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17355
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
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
finders_count: 4
finders:
  - Damilola Edwards
  - Gustavo Grieco
  - Anish Naik
  - Michael Colburn
---

## Vulnerability Title

Incorrect rounding direction in GVault

### Overview


This bug report is about the GMigration and GVault smart contracts. The minting and withdrawal operations in the GVault use rounding in favor of the user instead of the protocol, giving away a small amount of shares or assets that can accumulate over time. This is due to the convertToShares and convertToAssets functions which both round down, providing slightly fewer shares or assets than expected for some amount of shares or assets. Additionally, the mint function uses previewMint which also uses convertToAssets. This means that the function favors the user, since they get some fixed amount of shares for a rounded-down amount of assets. In a similar way, the withdraw function uses convertToShares, also providing slightly fewer assets than expected for some amount of shares. 

The exploit scenario is that Alice deploys a new GVault and provides some liquidity, and Eve uses mints and withdrawals to slowly drain the liquidity, possibly affecting the internal bookkeeping of the GVault. 

The recommendations are to consider refactoring the GVault code to specify the rounding direction across the codebase in order keep the error in favor of the user or the protocol. Additionally, to expand the unit test suite to cover additional edge cases and to ensure that the system behaves as expected.

### Original Finding Content

## Timing Assessment for GVault

## Type
**Timing**

## Target
**GMigration.sol**

## Difficulty
**High**

## Target
**GVault.sol**

### Description
The minting and withdrawal operations in the GVault use rounding in favor of the user instead of the protocol, giving away a small amount of shares or assets that can accumulate over time.

`convertToShares` is used in the GVault code to know how many shares correspond to a certain amount of assets:

```solidity
{
    /// @notice Value of asset in shares
    /// @param _assets amount of asset to convert to shares
    function convertToShares(uint256 _assets)
        public
        view
        override
        returns (uint256 shares)
    uint256 freeFunds_ = _freeFunds();  // Saves an extra SLOAD if _freeFunds is non-zero.
}
return freeFunds_ == 0 ? _assets : (_assets * totalSupply) / freeFunds_;
```
_Figure 11.1: The convertToShares function in GVault.sol_

This function rounds down, providing slightly fewer shares than expected for some amount of assets.

Additionally, `convertToAssets` is used in the GVault code to know how many assets correspond to a certain amount of shares:

```solidity
/// @notice Value of shares in underlying asset
/// @param _shares amount of shares to convert to tokens
function convertToAssets(uint256 _shares)
{
    public
    view
    override
    returns (uint256 assets)
    uint256 _totalSupply = totalSupply;  // Saves an extra SLOAD if _totalSupply is non-zero.
}
return _totalSupply == 0 ? _shares : ((_shares * _freeFunds()) / _totalSupply);
```
_Figure 11.2: The convertToAssets function in GVault.sol_

This function also rounds down, providing slightly fewer assets than expected for some amount of shares.

However, the mint function uses `previewMint`, which utilizes `convertToAssets`:

```solidity
function mint(uint256 _shares, address _receiver)
    external
    override
    nonReentrant
    returns (uint256 assets)
{
    // Check for rounding error in previewMint.
    if ((assets = previewMint(_shares)) == 0) revert Errors.ZeroAssets();
    _mint(_receiver, _shares);
    asset.safeTransferFrom(msg.sender, address(this), assets);
    emit Deposit(msg.sender, _receiver, assets, _shares);
    return assets;
}
```
_Figure 12.3: The mint function in GVault.sol_

This means that the function favors the user since they get some fixed amount of shares for a rounded-down amount of assets.

In a similar way, the withdraw function uses `convertToShares`:

```solidity
function withdraw(
    uint256 _assets,
    address _receiver,
    address _owner
) external override nonReentrant returns (uint256 shares) {
    if (_assets == 0) revert Errors.ZeroAssets();
    shares = convertToShares(_assets);
    if (shares > balanceOf[_owner]) revert Errors.InsufficientShares();
    if (msg.sender != _owner) {
        uint256 allowed = allowance[_owner][msg.sender];  // Saves gas for limited approvals.
    }
    if (allowed != type(uint256).max)
        allowance[_owner][msg.sender] = allowed - shares;
}
_assets = beforeWithdraw(_assets, asset);
_burn(_owner, shares);
asset.safeTransfer(_receiver, _assets);
emit Withdraw(msg.sender, _receiver, _owner, _assets, shares);
return shares;
```
_Figure 11.4: The withdraw function in GVault.sol_

This means that the function favors the user, since they get some fixed amount of assets for a rounded-down amount of shares.

This issue should also be considered when minting fees since they should favor the protocol instead of the user or the strategy.

## Exploit Scenario
Alice deploys a new GVault and provides some liquidity. Eve uses mints and withdrawals to slowly drain the liquidity, possibly affecting the internal bookkeeping of the GVault.

## Recommendations
**Short term:** Consider refactoring the GVault code to specify the rounding direction across the codebase in order to keep the error in favor of the user or the protocol.

**Long term:** Expand the unit test suite to cover additional edge cases and to ensure that the system behaves as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Growth Labs GSquared |
| Report Date | N/A |
| Finders | Damilola Edwards, Gustavo Grieco, Anish Naik, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf

### Keywords for Search

`vulnerability`

