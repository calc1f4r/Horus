---
# Core Classification
protocol: Dharma Labs Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16792
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
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
  - eric.rafaloﬀ@trailofbits.com Dominik Czarnota
  - Eric Rafaloﬀ
---

## Vulnerability Title

Compound’s redeem call failure emits ExternalError with incorrect function name

### Overview

See description below for full details.

### Original Finding Content

## Type: Access Controls
**Target:** DharmaUpgradeBeaconController.sol and Ownable contracts

**Difficulty:** High

## Description
The `DharmaSmartWalletImplementationV2` contract checks the results of its interactions with Compound by using the `_checkCompoundInteractionAndLogAnyErrors` function. This function (Figure 3.1) emits an `ExternalError` event specifying which Compound function call failed. The Compound function name is retrieved by forwarding the `functionSelector` argument to the `_getCTokenDetails` function.

The `_checkCompoundInteractionAndLogAnyErrors` function is called three times across the codebase with the following function selectors:

- In `_depositOnCompound` with `_CDAI.mint.selector`
- In `_withdrawFromCompound` with `_CDAI.redeemUnderlying.selector`
- In `_withdrawMaxFromCompound` with `_CDAI.redeem.selector`

However, the `_getCTokenDetails` function (Figure 3.2) only supports the `mint` and `redeemUnderlying` functions. As a result, when the redeem Compound call fails in the `_withdrawMaxFromCompound` function, `_checkCompoundInteractionAndLogAnyErrors` inaccurately reports that it was the `redeemUnderlying` function that failed.

```solidity
function _checkCompoundInteractionAndLogAnyErrors(
    AssetType asset,
    bytes4 functionSelector,
    bool ok,
    bytes memory data
) internal returns (bool success) {
    // Log an external error if something went wrong with the attempt.
    if (ok) {
        uint256 compoundError = abi.decode(data, (uint256));
        if (compoundError != _COMPOUND_SUCCESS) {
            // Get called contract address, name of contract, and function name.
            (address account, string memory name, string memory functionName) = _getCTokenDetails(asset, functionSelector);
            emit ExternalError(
                account,
                string(
                    abi.encodePacked(
                        "Compound ", name, " contract returned error code ",
                        uint8((compoundError / 10) + 48), uint8((compoundError % 10) + 48),
                        " while attempting to call ", functionName, "."
                    )
                )
            );
        }
    }
    // (...) - similar calls occur in the "else" branch
}
```
**Figure 3.1:** The `_checkCompoundInteractionAndLogAnyErrors` function, reformatted to take less space. Text highlighted in red marks the usage of `functionSelector` and `functionName`, which is calculated from `functionSelector` in the `_getCTokenDetails` function.

```solidity
function _getCTokenDetails(
    AssetType asset,
    bytes4 functionSelector
) internal pure returns (
    address account,
    string memory name,
    string memory functionName
) {
    // (...) - sets `account` and `name`
    // Note: since both cTokens have the same interface, just use cDAI's.
    if (functionSelector == _CDAI.mint.selector) {
        functionName = "mint";
    } else {
        functionName = "redeemUnderlying";
    }
}
```
**Figure 3.2:** The `_getCTokenDetails` function that returns `functionName` based on the value of `functionSelector`.

## Exploit Scenario
While not currently an exploitable issue, incorrect error reporting could lead to bugs in the future if other routines were to depend on its accuracy.

## Recommendation
- **Short term:** Fix the `_getCTokenDetails` function by setting `functionName` to “redeem” when a `_CDAI.redeem.selector` function selector is passed.
- **Long term:** Add more unit testing to ensure that error reporting works as intended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Dharma Labs Smart Wallet |
| Report Date | N/A |
| Finders | eric.rafaloﬀ@trailofbits.com Dominik Czarnota, Eric Rafaloﬀ |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf

### Keywords for Search

`vulnerability`

