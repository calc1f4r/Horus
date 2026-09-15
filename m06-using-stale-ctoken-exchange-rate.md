---
# Core Classification
protocol: BarnBridge Smart Yield Bonds Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10974
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/barnbridge-smart-yield-bonds-audit/
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M06] Using stale cToken exchange rate

### Overview


A bug was identified in the CompoundProvider contract of the BarnBridge-SmartYieldBonds repository. The bug was related to the exchange rate between cTokens and uTokens in a given Compound pool, where the pool's exchangeRateStored function was being used rather than the exchangeRateCurrent function. This resulted in incorrect calculations of fees, underlying balance, and expected COMP reward.

The bug was fixed in the commit 6a2b956d6b9df4639358368c93e518ea458f5d68, which replaced the exchangeRateStored function with the exchangeRateCurrent function. The commit also included other changes to the codebase which have not been reviewed by OpenZeppelin.

### Original Finding Content

Throughout the [`CompoundProvider` contract](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/providers/CompoundProvider.sol#L305), when considering the exchange rate between cTokens and uTokens in a given Compound pool, the pool’s [`exchangeRateStored`](https://github.com/compound-finance/compound-protocol/blob/c5fcc34222693ad5f547b14ed01ce719b5f4b000/contracts/CToken.sol#L328) function is used rather than its [`exchangeRateCurrent`](https://github.com/compound-finance/compound-protocol/blob/c5fcc34222693ad5f547b14ed01ce719b5f4b000/contracts/CToken.sol#L318) function. The result is that the exchange rate used is out of date, and relies on parties interacting with the Compound pool incredibly regularly. This leads to incorrect [calculations of fees](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/providers/CompoundProvider.sol#L225), incorrect [calculation of the underlying balance](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/providers/CompoundProvider.sol#L273), and incorrect [calculation of the expected COMP reward](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/blob/943df3a8fcd8dd128af3beb0c85a0480c0e95ead/contracts/providers/CompoundProvider.sol#L309).


Consider using the [`exchangeRateCurrent`](https://github.com/compound-finance/compound-protocol/blob/c5fcc34222693ad5f547b14ed01ce719b5f4b000/contracts/CToken.sol#L318) function to increase the overall accuracy of the protocol.


**Update**: *Fixed in commit [`6a2b956d6b9df4639358368c93e518ea458f5d68`](https://github.com/BarnBridge/BarnBridge-SmartYieldBonds/commit/6a2b956d6b9df4639358368c93e518ea458f5d68). There are no longer any instances of `exchangeRateStored` being used in the revised code. The referenced commit includes other changes to the codebase which have not been reviewed by OpenZeppelin.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | BarnBridge Smart Yield Bonds Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/barnbridge-smart-yield-bonds-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

