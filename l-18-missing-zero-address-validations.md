---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4106
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-yield-contest
source_link: https://code4rena.com/reports/2021-05-yield
github_link: https://github.com/code-423n4/2021-05-yield-findings/issues/42

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-18] Missing zero-address validations

### Overview

See description below for full details.

### Original Finding Content

## Handle

0xRajeev


## Vulnerability details

## Impact

While the codebase does a great job of input validation for parameters of all kinds and especially addresses, there are a few places where zero-address validations are missing. None of them are catastrophic, will result in obvious reverts and can be reset given the permissioned/controlled interactions with the contracts. 

Nevertheless, it is helpful to add zero-address validations to be consistent and ensure high availability of the protocol with resistance to accidental misconfigurations.

## Proof of Concept

1. Spot oracle address:

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/Cauldron.sol#L124-L127

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/Wand.sol#L78

2. Grab receiver addresses for other liquidation engines besides the Witch (which is fine because it uses address(this) for receiver):

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/Cauldron.sol#L235-L240

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/Cauldron.sol#L349-L360

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/Witch.sol#L53


3. Spot oracle’s spotSource in makeIlk() [unlike the checks in makeBase()]:

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/Wand.sol#L76-L77


4. Oracle setSource() in Compound, Uniswap and Chainlink can zero-address validate the source, instead of at the callers in Wand:

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/oracles/compound/CompoundMultiOracle.sol#L22-L23

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/oracles/uniswap/UniswapV3Oracle.sol#L49-L60

https://github.com/code-423n4/2021-05-yield/blob/e4c8491cd7bfa5dc1b59eb1b257161cd5bf8c6b0/contracts/oracles/chainlink/ChainlinkMultiOracle.sol#L29-L44


## Tools Used

Manual Analysis

## Recommended Mitigation Steps

Add require() to zero-address validate the address parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-yield
- **GitHub**: https://github.com/code-423n4/2021-05-yield-findings/issues/42
- **Contest**: https://code4rena.com/contests/2021-05-yield-contest

### Keywords for Search

`vulnerability`

