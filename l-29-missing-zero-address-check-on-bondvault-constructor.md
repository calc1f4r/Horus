---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4140
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/144

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
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-29] Missing zero address check on BondVault constructor

### Overview

See description below for full details.

### Original Finding Content

## Handle

maplesyrup


## Vulnerability details

## Impact

This is a low risk vulnerability due to the fact that it is possible to lose funds if the Base address is set to a zero address and someone sends funds to this address. As a rule, there should always be checks to make sure that initialized addresses are never a zero address.

## Proof of Concept

According to Slither analysis documentation (https://github.com/crytic/slither/wiki/Detector-Documentation#exploit-scenario-49), there needs to be a zero address checkpoint when initializing a base address in a contract. In the case for BondVault, the constructor initializes a base address. There should be a check to make sure this address is never zero to make sure there is no way to lose funds.

Slither detector:

missing-zero-check:

BondVault.constructor(address)._base (contracts/BondVault.sol#37) lacks a zero-check on :

BASE = _base (contracts/BondVault.sol#38)

------------------------------------------------

Slither output from console (JSON format):

"missing-zero-check": [
    "BondVault.constructor(address)._base (contracts/BondVault.sol#37) lacks a zero-check on :\n\t\t- BASE = _base (contracts/BondVault.sol#38)\n",
    "Dao.constructor(address)._base (contracts/Dao.sol#96) lacks a zero-check on :\n\t\t- BASE = _base (contracts/Dao.sol#97)\n",
    "DaoVault.constructor(address)._base (contracts/DaoVault.sol#16) lacks a zero-check on :\n\t\t- BASE = _base (contracts/DaoVault.sol#17)\n",
    "Pool.constructor(address,address)._base (contracts/Pool.sol#43) lacks a zero-check on :\n\t\t- BASE = _base (contracts/Pool.sol#44)\n",
    "Pool.constructor(address,address)._token (contracts/Pool.sol#43) lacks a zero-check on :\n\t\t- TOKEN = _token (contracts/Pool.sol#45)\n",
    "Router.constructor(address,address)._base (contracts/Router.sol#29) lacks a zero-check on :\n\t\t- BASE = _base (contracts/Router.sol#30)\n",
    "Router.constructor(address,address)._wbnb (contracts/Router.sol#29) lacks a zero-check on :\n\t\t- WBNB = _wbnb (contracts/Router.sol#31)\n",
    "Synth.constructor(address,address)._base (contracts/Synth.sol#36) lacks a zero-check on :\n\t\t- BASE = _base (contracts/Synth.sol#37)\n",
    "Synth.constructor(address,address)._token (contracts/Synth.sol#36) lacks a zero-check on :\n\t\t- LayerONE = _token (contracts/Synth.sol#38)\n",
    "Utils.constructor(address)._base (contracts/Utils.sol#13) lacks a zero-check on :\n\t\t- BASE = _base (contracts/Utils.sol#14)\n",
    "PoolFactory.constructor(address,address)._base (contracts/poolFactory.sol#28) lacks a zero-check on :\n\t\t- BASE = _base (contracts/poolFactory.sol#29)\n",
    "PoolFactory.constructor(address,address)._wbnb (contracts/poolFactory.sol#28) lacks a zero-check on :\n\t\t- WBNB = _wbnb (contracts/poolFactory.sol#30)\n",
    "SynthFactory.constructor(address,address)._base (contracts/synthFactory.sol#15) lacks a zero-check on :\n\t\t- BASE = _base (contracts/synthFactory.sol#16)\n",
    "SynthFactory.constructor(address,address)._wbnb (contracts/synthFactory.sol#15) lacks a zero-check on :\n\t\t- WBNB = _wbnb (contracts/synthFactory.sol#17)\n",
    "SynthVault.constructor(address)._base (contracts/synthVault.sol#35) lacks a zero-check on :\n\t\t- BASE = _base (contracts/synthVault.sol#36)\n"
  ],

## Tools Used

Spartan Contracts
Solidity (v 0.8.3)
Slither Analyzer (v 0.8.0)

## Recommended Mitigation Steps

1. Clone repository for Spartan Smart Contracts
2. Create a python virtual environment with a stable python version
3. Install Slither Analyzer on the python VEM
4. Run Slither against all contracts

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/144
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`vulnerability`

