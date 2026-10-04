---
# Core Classification
protocol: Liquity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18022
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Alexander Remie
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Unclear if the gas pool account is controlled by someone

### Overview

See description below for full details.

### Original Finding Content

## Undefined Behavior

**Type:** Undefined Behavior  
**Target:** BorrowerOperations.sol  

**Difficulty:** Medium  

## Description
The special gas pool account is used to mint LUSD tokens and pay for the gas operations performed by users, but it is unclear if someone owns its private key. The Liquity protocol mints LUSD to compensate for the gas spent by users when they call certain functions, such as `openTrove`:

```solidity
function openTrove(uint _LUSDAmount, address _hint) external payable override {
    ...
    // Move the LUSD gas compensation to the Gas Pool
    _withdrawLUSD(GAS_POOL_ADDRESS, LUSD_GAS_COMPENSATION, LUSD_GAS_COMPENSATION);
    emit TroveUpdated(msg.sender, rawDebt, msg.value, stake, BorrowerOperation.openTrove);
    emit LUSDBorrowingFeePaid(msg.sender, LUSDFee);
}
```

Figure 5.1: `_requireValidRecipient` in LUSDToken.sol. This address is defined as `0x00000000000000000000000000000000000009A5` and it’s just like any other address that can hold LUSD tokens. It is unclear whether someone owns its private key or not. If it exists, it can be easily used to steal the tokens minted to compensate for the cost of gas.

## Exploit Scenario
Eve somehow gets the private key of the gas pool account and is able to steal all the tokens from it. The Liquity protocol cannot be modified in any sense, and therefore it cannot change this address and it needs to be re-deployed.

## Recommendation
**Short term:** Consider refactoring the code to avoid using the gas pool account. Instead, use a state variable that keeps track of the amount of LUSD tokens available to compensate for gas costs.

**Long term:** Avoid hard-coding any account address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Liquity |
| Report Date | N/A |
| Finders | Gustavo Grieco, Alexander Remie, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf

### Keywords for Search

`vulnerability`

