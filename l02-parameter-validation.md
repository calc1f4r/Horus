---
# Core Classification
protocol: Set Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11303
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/set-protocol-audit/
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

protocol_categories:
  - dexes
  - yield
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L02] Parameter Validation

### Overview

See description below for full details.

### Original Finding Content

The following is a list of code snippets that could benefit from additional validation:


* The `initialize` function of the `Controller` contract [does not check for duplicates in the passed `_factories`, `_modules` or `_resources` arrays](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/Controller.sol#L141-L143). This could lead to inconsistencies in the internal state, particularly if any of the items are removed. Consider checking for duplicates before assigning these arrays.
* Similarly, the `PriceOracle` constructor [does not check for duplicates in the passed `_adapters` array](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/PriceOracle.sol#L91)
* The [`addFee`](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/Controller.sol#L375), [`editFee`](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/Controller.sol#L392) and [`editFeeRecipient`](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/Controller.sol#L407) functions of the `Controller` contract do not prevent a zero fee recipient with a non-zero fee. If this occurs, the [`mintTraderAndProtocolFee` function of the `StreamingFeeModule` contract](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/modules/StreamingFeeModule.sol#L248) will revert for any non-zero fee. This will effectively disable the module.
* The `hasDuplicate` function of `AddressArrayUtils` [implicitly assumes the array is not empty when computing the loop bound](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/lib/AddressArrayUtils.sol#L62). Although this is [checked before the call](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/SetTokenCreator.sol#L77-L79), library functions should not depend on external validation. Consider explicitly checking that the array has at least one element, or using `SafeMath` for the subtraction.
* Similarly, the `pop` function of `AddressArrayUtils` [implicitly assumes the array is not empty](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/lib/AddressArrayUtils.sol#L100) and that the [`index` is within the array](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/lib/AddressArrayUtils.sol#L101-L103). Consider explicitly checking these conditions.
* The `SetToken` contract does not perform consistency checks when positions are changed.
* [the `addComponent` function](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/SetToken.sol#L214) does not validate that the input is non-zero, or that it doesn’t already exist in the `components` array.
* [the `addExternalPositionModule` function](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/SetToken.sol#L242) does not validate that the component is in the `_components` mapping or if the module already exists in the `externalPositionModules` array. It also does not add any new position to the `externalPositions` mapping but the existence of the module is used to count the positions.
* [the `editExternalPositionUnit` function](https://github.com/SetProtocol/set-protocol-v2/blob/b8286f431547823ff3935a1343cd4cf4d77585a1/contracts/protocol/SetToken.sol#L269) does not validate that the component or position exist.


***Update:** Partially fixed in [PR#118](https://github.com/SetProtocol/set-protocol-v2/pull/118). The `editFeeRecipient` now ensures new fee recipients are non-zero. For completeness, the constructor should also ensure the fee recipient is not initialized to zero. The `hasDuplicate` and `pop` functions of `AddressArrayUtils` now perform the recommended validations.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Set Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/set-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

