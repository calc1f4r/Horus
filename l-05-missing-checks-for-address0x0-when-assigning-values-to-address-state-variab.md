---
# Core Classification
protocol: Tessera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24517
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-12-tessera
source_link: https://code4rena.com/reports/2022-12-tessera
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
  - cdp
  - cross_chain
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05]  Missing checks for `address(0x0)` when assigning values to `address` state variables

### Overview

See description below for full details.

### Original Finding Content


*There are 12 instances of this issue:*

```solidity
File: src/punks/protoforms/PunksMarketBuyer.sol

32:           registry = _registry;

33:           wrapper = _wrapper;

34:           listing = _listing;

```
https://github.com/code-423n4/2022-12-tessera/blob/f37a11407da2af844bbfe868e1422e3665a5f8e4/src/punks/protoforms/PunksMarketBuyer.sol#L32

```solidity
File: src/seaport/modules/OptimisticListingSeaport.sol

71:           registry = _registry;

72:           seaport = _seaport;

73:           zone = _zone;

75:           supply = _supply;

76:           seaportLister = _seaportLister;

77:           feeReceiver = _feeReceiver;

78:           OPENSEA_RECIPIENT = _openseaRecipient;

338:          feeReceiver = _new;

```
https://github.com/code-423n4/2022-12-tessera/blob/f37a11407da2af844bbfe868e1422e3665a5f8e4/src/seaport/modules/OptimisticListingSeaport.sol#L71

```solidity
File: src/seaport/targets/SeaportLister.sol

20:           conduit = _conduit;

```
https://github.com/code-423n4/2022-12-tessera/blob/f37a11407da2af844bbfe868e1422e3665a5f8e4/src/seaport/targets/SeaportLister.sol#L20

## Non-Critical Issues Summary

| |Issue|Instances|
|-|:-|:-:|
| [N&#x2011;01] | Debugging functions should be moved to a child class rather than being deployed | 1 | 
| [N&#x2011;02] | Typos | 4 | 
| [N&#x2011;03] | `public` functions not called by the contract should be declared `external` instead | 10 | 
| [N&#x2011;04] | `constant`s should be defined rather than using magic numbers | 4 | 
| [N&#x2011;05] | Missing event and or timelock for critical parameter change | 1 | 
| [N&#x2011;06] | NatSpec is incomplete | 7 | 
| [N&#x2011;07] | Consider using `delete` rather than assigning zero to clear values | 4 | 
| [N&#x2011;08] | Contracts should have full test coverage | 1 | 
| [N&#x2011;09] | Large or complicated code bases should implement fuzzing tests | 1 | 

Total: 33 instances over 9 issues




### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tessera |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tessera
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-12-tessera

### Keywords for Search

`vulnerability`

