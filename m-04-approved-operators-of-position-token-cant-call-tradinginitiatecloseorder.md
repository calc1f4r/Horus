---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6334
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/124

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - __141345__  UniversalCrypto
  - rvierdiiev
---

## Vulnerability Title

[M-04] Approved operators of Position token can’t call Trading.initiateCloseOrder

### Overview


This bug report is about a vulnerability that affects the Trading contract, which is part of the code-423n4/2022-12-tigris repository. The bug allows approved operators of the owner of the Position token to not be able to call several functions in the Trading contract. The bug is caused by a check in the _checkOwner function that doesn't allow the approved operators to pass the check, and thus the functions are not possible to call for them on behalf of the owner. The recommended mitigation step is to allow operators of the token's owner to call functions on behalf of the owner. The bug was discovered using the VsCode tool.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L235
https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L847-L849


## Vulnerability details

## Impact
Approved operators of owner of Position token can't call several function in Trading.

## Proof of Concept
Functions that accept Position token in Trading are checking that the caller is owner of token using _checkOwner function.
https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L847-L849
```soldiity
    function _checkOwner(uint _id, address _trader) internal view {
        if (position.ownerOf(_id) != _trader) revert("2"); //NotPositionOwner   
    }
```
As you can see this function doesn't allow to approved operators of token's owner to pass the check. As result functions are not possible to call for them on behalf of owner.
For example [here](https://github.com/code-423n4/2022-12-tigris/blob/main/contracts/Trading.sol#L235) there is a check that doesn't allow to call initiateCloseOrder function.
## Tools Used
VsCode
## Recommended Mitigation Steps
Allow operators of token's owner to call functions on behalf of owner.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | __141345__  UniversalCrypto, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/124
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

