---
# Core Classification
protocol: CompliFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17803
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/CompliFi.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/CompliFi.pdf
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
finders_count: 3
finders:
  - Devashish Tomar
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Lack of access modiﬁers on Vault.initialize leaves it susceptible to front-running

### Overview


This bug report is about data validation in the CompliFi protocol internal contract DerivativeSpecification.sol. The severity of the issue was initially set to high but was later lowered after CompliFi provided additional context. The Vault implementation contract has an initialization function that can be front-run, allowing an attacker to incorrectly initialize the contract. An attacker could front-run this function and initialize instances of the Vault contract with a malicious _underlyingStarts value which would lead to the creation of a valid but unusual derivative. This could lead to certain users failing to carefully read the derivative and make incorrect assumptions about its properties, resulting in a loss of funds.

Short term, it is recommended to implement an access control modifier for the initialize function and develop clear documentation warning users that the values of derivatives may be unusual and reminding them to carefully check information on derivatives. Long term, it is recommended to analyze all contracts to identify any functions that could be front-run by attackers seeking to assign their own variables.

### Original Finding Content

## Data Validation

**Target:** complifi-protocol-internal/contracts/DerivativeSpecification.sol  

**Difficulty:** High  

## Description

July 9, 2021 Update: The severity of this issue was initially set to high. However, we agreed to lower the severity rating after CompliFi provided the following additional context:

1. “Anyone is free to call Vault.initialize, and in practice it is the person who wants to create a particular derivative for whatever purpose.“
2. “Minting of derivative is a risk-free event at all parametrisation levels - the user receives equal amounts of long and short positions.”
3. “If the attacker manages to alter the intended parametrisation of a derivative, the AMM would not allow them to dispose of it at anything other than fair market value.”

The Vault implementation contract has an initialization function that can be front-run, allowing an attacker to incorrectly initialize the contract. The Vault contract is initialized through a two-step process, first through its constructor and then through the `initialize` function.

```solidity
/// @notice Initialize vault by creating derivative token and switching to Live state
/// @dev Extracted from constructor to reduce contract gas creation amount
function initialize(int256[] calldata _underlyingStarts) external {
    require(state == State.Created, "Incorrect state.");
    underlyingStarts = _underlyingStarts;
    changeState(State.Live);
    (primaryToken, complementToken) = tokenBuilder.buildTokens(
        derivativeSpecification,
        settleTime,
        address(collateralToken)
    );
    emit LiveStateSet(address(primaryToken), address(complementToken));
}
```
_Figure 4.1: complifi-protocol-internal/contracts/Vault.sol#L172-L188_

An attacker could front-run this function and initialize instances of the Vault contract with a malicious `_underlyingStarts` value.

## Exploit Scenario

Bob deploys the Vault contract through the VaultFactory and must execute a separate transaction to invoke `initialize` and finish setting up the Vault. Eve front-runs the contract’s initialization and sets an arbitrary value as `_underlyingStarts`. This leads to the creation of a valid but unusual derivative. Certain users fail to carefully read the derivative and make incorrect assumptions about its properties, which could lead to a loss of funds.

## Recommendations

**Short term:** 

- Implement an access control modifier for the `initialize` function. 
- Develop clear documentation warning users that the values of derivatives may be unusual and reminding them to carefully check information on derivatives.

**Long term:** 

- Analyze all contracts to identify any functions that could be front-run by attackers seeking to assign their own variables.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | CompliFi |
| Report Date | N/A |
| Finders | Devashish Tomar, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/CompliFi.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/CompliFi.pdf

### Keywords for Search

`vulnerability`

