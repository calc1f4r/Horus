---
# Core Classification
protocol: Basis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16750
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Gustavo Grieco
  - Robert Tonic
  - Josselin Feist
  - Benjamin Perez
  - Dominik Czarnota
---

## Vulnerability Title

A multiplication over�low allows an attacker to block the tally

### Overview


This bug report is about the ElectionCommission.sol (v0) which is a smart contract written in Solidity. This contract has a function called postOracleSupplyChange which allows delegates to vote for a new Basis total supply. However, if a malicious delegate votes for an arbitrarily large supply increase, they can block the tally by triggering a multiplication overflow. This is due to the convertSupplyChangeToPercentileChange function which uses SafeMath to multiply the total supply by 10,000. If the number is too large, it will trigger an overflow which will cause the tallyOracleSupplyChange function to throw an error.

The exploit scenario is that the Basis token price decreases and a proposal is made to decrease the total supply. The majority of the delegates vote in favor, but Bob, a malicious delegate, wants to prevent the burn of tokens and votes for a new total supply of 2**255‑1, which triggers an overflow and blocks the tally.

The recommendation is to prevent unrealistic values in postOracleSupplyChange in the short term and be aware that SafeMath will throw an error in case of an overflow. In the long term, consider testing all arithmetic operations through a fuzzer or symbolic execution engine.

### Original Finding Content

## Timing Issue in ElectionCommission.sol (v0)

## Difficulty
High

## Description
Every day, delegates can vote for a new Basis total supply. If a malicious delegate votes for an arbitrarily large supply increase, they can block the tally by triggering a multiplication overflow. 

A delegate can vote for a new Basis total supply through the `postOracleSupplyChange` function:

```solidity
function postOracleSupplyChange(int256 supplyChange) public notDuringVoteTally {
    shares.noteDelegateVoted(msg.sender);
    oracleSupplyChange[msg.sender] = supplyChange;
}
```
**Figure 1:** `postOracleSupplyChange` function

The `tallyOracleSupplyChange` function will call `convertSupplyChangeToPercentileChange` to convert the total supply to a percentage:

```solidity
function tallyOracleSupplyChange() public onlyDuringVoteTally returns (bool complete) {
    …
    int16 idx = convertSupplyChangeToPercentileChange(oracleSupplyChange[address(currDelegate)]);
}
```
**Figure 2:** `tallyOracleSupplyChange` function

The `convertSupplyChangeToPercentileChange` function uses SafeMath to multiply the total supply by 10,000:

```solidity
function convertSupplyChangeToPercentileChange(int256 delta) internal view returns (int16) {
    delta = delta.mul(int256(10000)) / basis.totalSupply().signed();
}
```
**Figure 3:** `convertSupplyChangeToPercentileChange` function

However, SafeMath.mul throws an error in case of overflow:

```solidity
function mul(int256 a, int256 b) internal pure returns (int256 c) {
    if (a == 0) return 0;
    c = a * b;
    require(b == c / a);
}
```
**Figure 4:** `mul(int256 a, int256 b)` function

An attacker can prevent a successful call to `tallyOracleSupplyChange` by voting for a very large supply number that will trigger an overflow in SafeMath.mul. This will always cause `tallyOracleSupplyChange` to throw. As a result, a malicious delegate can block the tally.

## Exploit Scenario
The Basis token price decreases. A proposal is made to decrease the total supply. The majority of the delegates vote in favor. Bob is a delegate who wants to prevent the burn of tokens, and therefore votes for a new total supply of `2**255‑1`. As a result, the tally is blocked and the Basis total supply does not decrease.

## Recommendation
In the short term, prevent unrealistic values in `postOracleSupplyChange`. Additionally, be aware that SafeMath will throw if an overflow is triggered.

`ElectionCommission` lacks unit tests despite its complexity. In the long term, consider testing all arithmetic operations through a fuzzer, such as Echidna, or a symbolic execution engine, such as Manticore.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Basis |
| Report Date | N/A |
| Finders | Gustavo Grieco, Robert Tonic, Josselin Feist, Benjamin Perez, Dominik Czarnota, https://docs.google.com/document/d/1kKWrVfLjwWBtEMDSsidDeerC6Q4bnR-qC5p0z0_SYnE/edit# 1/68 |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf

### Keywords for Search

`vulnerability`

