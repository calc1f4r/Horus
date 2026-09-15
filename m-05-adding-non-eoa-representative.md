---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5913
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/93

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - validation

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - yixxas
  - Jeiwan
  - joestakey
  - HE1M
  - SmartSek
---

## Vulnerability Title

[M-05] Adding non EOA representative

### Overview


A bug was reported in the Liquid Staking Manager smart contract of the 2022-11-stakehouse repository on GitHub. This bug allowed users to bypass a check that only EOA (Externally Owned Account) representatives are permitted when registering a node runner to the LSD. This could be done by rotating representatives in the two functions `rotateEOARepresentative` and `rotateEOARepresentativeOfNodeRunner`. Without the check, a contract could be used as a representative, which should not be allowed.

The recommended mitigation step to address this bug is to add the following line to the two functions:

```
require(!Address.isContract(_newRepresentative), "Only EOA representative permitted");
```

This will ensure that only EOA representatives are allowed when registering a node runner to the LSD.

### Original Finding Content


<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/LiquidStakingManager.sol#L308><br>
<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/LiquidStakingManager.sol#L289>

It is not allowed to add non-EOA representative to the smart wallet.<br>
But, this limitation can be bypassed by rotating representatives.

### Proof of Concept

During registering a node runner to LSD by creating a new smart wallet, it is checked that the `_eoaRepresentative` is an EOA or not.

    require(!Address.isContract(_eoaRepresentative), "Only EOA representative permitted");

<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/LiquidStakingManager.sol#L426>

But this check is missing during rotating EOA representative in two functions `rotateEOARepresentative` and `rotateEOARepresentativeOfNodeRunner`.

<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/LiquidStakingManager.sol#L289><br>
<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/LiquidStakingManager.sol#L308>

In other words `_newRepresentative` can be a contract in these two functions without being prevented. So, this can bypass the check during registering a node runner to LSD.

### Recommended Mitigation Steps

The following line should be added to functions `rotateEOARepresentative` and `rotateEOARepresentativeOfNodeRunner`:

    require(!Address.isContract(_newRepresentative), "Only EOA representative permitted");

**[vince0656 (Stakehouse) confirmed duplicate issue #187](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/187#issuecomment-1329469080)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | yixxas, Jeiwan, joestakey, HE1M, SmartSek |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/93
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Validation`

