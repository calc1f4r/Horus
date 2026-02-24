---
# Core Classification
protocol: ERC-4337 Account Abstraction Incremental Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32534
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/erc-4337-account-abstraction-incremental-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Operations Can Throttle Paymasters [core]

### Overview


The `simulateValidation` function in `EntryPointSimulations` has a bug where it does not handle the `aggregator` parameter correctly. This can lead to two possible mistakes: overwriting an account's "signature success" flag with a paymaster's non-zero aggregator parameter, or ignoring a paymaster's "signature failed" flag in the presence of an account's non-zero aggregator. This can cause unauthorized operations to be included in a bundle and unfairly blame the paymaster for the failure. The bug has been fixed in a recent pull request by removing the `simulateValidation` code and returning the "raw" validationData from the account and paymaster separately. 

### Original Finding Content

*Note: this error was present in the previous audit commit but was not identified by the auditors at the time.*


The `simulateValidation` function of `EntryPointSimulations` [combines the validity conditions](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/core/EntryPointSimulations.sol#L71) of the account and the paymaster to determine when the operation is considered valid by both parties. However, the `aggregator` parameter is [semantically overloaded](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/interfaces/IAccount.sol#L26-L27), to represent either a signature success flag or an aggregator address, and this is not completely handled in the combination.


Specifically, the combined `aggregator` is either [the value chosen by the account](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/core/Helpers.sol#L55-L58), or if that is zero, the value chosen by the paymaster. This leads to two possible mistakes:


* an account's "signature success" flag (`0`) would be overwritten by a paymaster's non-zero aggregator parameter.
* a paymaster's "signature failed" flag (`1`) would be ignored in the presence of an account's non-zero aggregator.


The first condition would be identified by the rest of the security architecture and likely has minimal consequences. However, the second condition would cause bundlers to include unauthorized operations in a bundle and then [blame the paymaster](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/core/EntryPoint.sol#L556) for the failure. This would cause paymasters to be unfairly throttled.


Consider updating the simulation to require paymasters to only return `0` or `1` as the `aggregator` parameter, and to ensure that the "signature failed" flag (`1`) always takes precedence.


***Update:** Resolved in [pull request #406](https://github.com/eth-infinitism/account-abstraction/pull/406). The Ethereum Foundation team stated:*



> *Remove the simulateValidation code to intersect the paymaster and account time-ranges (and signature validation). This calculation should be done off-chain by the bundler. The simulation functions now return the "raw" validationData, as returned by the account and paymaster (separately).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | ERC-4337 Account Abstraction Incremental Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/erc-4337-account-abstraction-incremental-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

