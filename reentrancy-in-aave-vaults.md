---
# Core Classification
protocol: SOFA.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36054
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Reentrancy In AAVE Vaults

### Overview

See description below for full details.

### Original Finding Content

## Description

There is a reentrancy vector within the AAVE vaults when `supply()` is called. The issue exists within the vault’s `mint()` function, as the call to `POOL.supply()` will perform a transfer of the underlying token. If the underlying token is reenterable then it will be possible to reenter into `mint()`.

## AAVEDNTVault.sol

```solidity
206 uint256 aTokenShare;
POOL.supply(address(COLLATERAL), totalCollateral, address(this), REFERRAL_CODE); // @audit potentially reenterable
208 uint256 aTokenBalance = ATOKEN.balanceOf(address(this));
if (totalSupply > 0) {
210 aTokenShare = totalCollateral * totalSupply / (aTokenBalance - totalCollateral);
} else {
212 aTokenShare = totalCollateral * SHARE_MULTIPLIER;
}
214 totalSupply += aTokenShare;
```

The issue is raised as informational as AAVE currently does not support tokens which relinquish control of execution. Furthermore, the external transfer would occur before the aToken balance is modified, removing the benefit to an attacker of performing this attack.

## Recommendations

It is recommended to add a `nonReentrant` modifier to the `_mint()` function to prevent potential reentrancy.

## Resolution

This issue has been fixed in commit `ef1e9b9`. The function `_mint()` of `AAVESmartTrendVault` and `AAVEDNTVault` now has the `nonReentrant` modifier.

## SFA-19 Miscellaneous General Comments

## Asset
All contracts

## Status
Closed: See Resolution

## Rating
Informational

### Description

This section details miscellaneous findings discovered by the testing team that do not have direct security implications:

1. **Use Readable Format**
   - **Related Asset(s):** `tokenomics/RCH.sol`
   - Use `37_000_000` instead of `37000000` for the constant variable `MAX_SUPPLY`. Consider the suggested modification.

2. **Gas: Copy Variable Before Check**
   - **Related Asset(s):** `vaults/*`
   - Consider the following code:
     ```solidity
     function harvest() external {
         require(totalFee > 0, "Vault: zero fee");
         uint256 fee = totalFee;
         totalFee = 0;
     }
     ```
     It would save on one SLOAD to check fee, like so:
     ```solidity
     function harvest() external {
         uint256 fee = totalFee;
         require(fee > 0, "Vault: zero fee");
         totalFee = 0;
     }
     ```
     Consider the suggested modification.

3. **Unnecessary if Test**
   - **Related Asset(s):** `oracles/HlOracle.sol`
   - Consider the following test from lines [91-93]:
     ```solidity
     if (settlePrices[expiry][1] > 0 && settlePrices[expiry][1] > hlPrices[1]) {
         hlPrices[1] = settlePrices[expiry][1];
     }
     ```
     As `hlPrices[1]` starts at zero and can only get bigger, the first condition in this test is unnecessary. Consider removing the first condition in the test.

4. **Modifiable State Variables Styled As Constants**
   - **Related Asset(s):** `vaults/*`
   - The following variables are storage variables:
     - `IWETH public WETH;`
     - `IPermit2 public PERMIT2;`
     - `IDNTStrategy public STRATEGY;`
     - `IERC20Metadata public COLLATERAL;`
     - `IHlOracle public ORACLE;`
   
   However, they are written in block capitals, which is usually used to signify a constant. It is acknowledged that these variables are treated as constants but they are modifiable in storage, which could have future security implications. Consider turning these variables into constants, or immutable variables that are set in the constructor. Alternatively, consider changing them to the standard "camel case".

5. **Different Functions With Identical Names**
   - **Related Asset(s):** `vaults/*`
   - The following functions are defined in the vault contracts, but also have related functions in OpenZeppelin's `ERC1155Upgradeable.sol` which are also called, often within functions of the same name:
     - `_mint()`
     - `_mintBatch()`
     - `_burn()`
     - `_burnBatch()`
   
   It is acknowledged that the function signatures are different, as the parameters are not the same. However, the code would be clearer if these functions did not share identical names. Consider changing the function names in the vault, even minimally. For example `_vaultMint()`, `_productMint()`, `_sofaMint()` or even `_vMint()`.

6. **DNT Vault Anchor Prices Can Be Impossible To Avoid**
   - **Related Asset(s):** `vaults/AAVEDNTVault.sol & vaults/DNTVault.sol & vaults/LeverageDNTVault.sol`
   - The check for DNT vault anchor prices is:
     ```solidity
     require(params.anchorPrices[0] < params.anchorPrices[1], "Vault: invalid strike prices");
     ```
     Note that, even if `params.anchorPrices[0] + 1 == params.anchorPrices[1]`, it is still inevitable that the prices will be touched on minting. Regardless of the gap between the anchor prices, it is also possible to mint when the current price is touching one of them. This may be an acceptable liability, and one for which the user is considered responsible. Nevertheless, creating products that instantly expire has questionable legitimate utility but is a potentially useful tool when crafting attacks. Consider specifying a minimum gap between anchor prices for DNT vaults. Consider checking that the anchor prices are not already touched when minting products for DNT vaults.

7. **Missing Sanity Check**
   - **Related Asset(s):** `oracles/HlOracle.sol`
   - There is no on-chain check in the `settle()` function that `currentPrices[0] < currentPrices[1]`. Consider adding this check to ensure that the prices are in ascending order.

8. **Missing Events on Configuration Variable Changes**
   - **Related Asset(s):** `vaults/LeverageSmartTrendVault.sol & vaults/LeverageDNTVault.sol`
   - Consider emitting events when the `updateBorrowAPR` and `updateSpreadAPR` functions successfully update their variables.

## Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

## Resolution

The development team’s responses to the raised issues above are as follows.

1. **Use Readable Format**
   - **Related Asset(s):** `tokenomics/RCH.sol`
   - This change was implemented as can be seen in described in commit `ef1e9b9`.

2. **Gas: Copy Variable Before Check**
   - This change was implemented as can be seen in described in commit `ef1e9b9`.

3. **Unnecessary if Test**
   - This change was implemented as can be seen in described in commit `ef1e9b9`.

4. **Modifiable State Variables Styled As Constants**
   - This change was implemented as can be seen in described in commit `ef1e9b9`.

5. **Different Functions With Identical Names**
   - The development team has acknowledged the issue and resolved to monitor for potential developments.

6. **DNT Vault Anchor Prices Can Be Impossible To Avoid**
   - The development team has acknowledged the issue and resolved to monitor for potential developments.

7. **Missing Sanity Check**
   - This change was implemented as can be seen in described in commit `ef1e9b9`.

8. **Missing Events on Configuration Variable Changes**
   - The development team has acknowledged the issue and resolved to monitor for potential developments.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | SOFA.org |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf

### Keywords for Search

`vulnerability`

