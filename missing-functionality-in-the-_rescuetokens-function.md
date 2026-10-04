---
# Core Classification
protocol: Ondo Finance: Ondo Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17494
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
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
finders_count: 3
finders:
  - Damilola Edwards
  - Anish Naik
  - Justin Jacob
---

## Vulnerability Title

Missing functionality in the _rescueTokens function

### Overview

See description below for full details.

### Original Finding Content

## Difficulty: High

## Type: Undefined Behavior

### Description
The `RegistryClient` contract is a helper contract designed to aid in the protocol’s role-based access control (RBAC) mechanism. It has various helper functions that serve as safety mechanisms to rescue funds trapped inside a contract. The inline documentation for the `_rescueTokens` function states that if the `_amounts` array contains a zero-value entry, then the entire token’s balance should be transferred to the caller. However, this functionality is not present in the code; instead, the function sends zero tokens to the caller on a zero-value entry.

```solidity
/**
 * @dev If the _amount[i] is 0, then transfer all the tokens
 *
 * @param _tokens List of tokens
 * @param _amounts Amount of each token to send
 */
function _rescueTokens(address[] calldata _tokens, uint256[] memory _amounts)
internal
virtual
{
    for (uint256 i = 0; i < _tokens.length; i++) {
        uint256 amount = _amounts[i];
        IERC20(_tokens[i]).safeTransfer(msg.sender, amount);
    }
}
```

Figure 3.1: The `_rescueTokens` function in `RegistryClient.sol:#L192–L205`

### Exploit Scenario
A user accidentally sends ERC20 tokens to the PSM contract. To rescue the tokens, Bob, the guardian of the Ondo protocol contracts, calls `_rescueTokens` and specifies zero as the amount for the ERC20 tokens in question. However, the contract incorrectly transfers zero tokens to him and, therefore, the funds are not rescued.

### Recommendations
- **Short term:** Adjust the `_rescueTokens` function so that it transfers the entire token balance when it reaches a zero-value entry in the `_amounts` array.
- **Long term:** Improve the unit test coverage to cover additional edge cases and to ensure that the system behaves as expected.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Ondo Finance: Ondo Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Anish Naik, Justin Jacob |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-10-shimacapital-ondo-securityreview.pdf

### Keywords for Search

`vulnerability`

