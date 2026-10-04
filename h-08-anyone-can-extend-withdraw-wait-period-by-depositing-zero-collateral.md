---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 929
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/69

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

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - harleythedog
---

## Vulnerability Title

[H-08] Anyone can extend withdraw wait period by depositing zero collateral

### Overview


A bug has been identified in the MochiVault.sol contract where anyone can call the deposit function with an amount of 0, which would reset the amount of time the owner has to wait before they can withdraw their collateral from their position. This could be used maliciously to lock out all other users from withdrawing from their positions, compromising the functionality of the contract. This has been identified through manual inspection of the code, and the recommended mitigation step is to add a require statement to the start of the function to prevent anyone from depositing zero collateral. It may also be worthwhile to consider only allowing the owner of a position to deposit collateral.

### Original Finding Content

## Handle

harleythedog


## Vulnerability details

## Impact
In MochiVault.sol, the deposit function allows anyone to deposit collateral into any position. A malicious user can call this function with amount = 0, which would reset the amount of time the owner has to wait before they can withdraw their collateral from their position. This is especially troublesome with longer delays, as a malicious user would only have to spend a little gas to lock out all other users from being able to withdraw from their positions, compromising the functionality of the contract altogether.

## Proof of Concept
deposit function here: https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/vault/MochiVault.sol#:~:text=function-,deposit,-(uint256%20_id%2C%20uint256

Notice that calling this function with amount = 0 is not disallowed. This overwrites lastDeposit[_id], extending the wait period before a withdraw is allowed.

## Tools Used
Manual inspection.

## Recommended Mitigation Steps
I would recommend adding:

require(amount > 0, "zero")

at the start of the function, as depositing zero collateral does not seem to be a necessary use case to support.

It may also be worthwhile to consider only allowing the owner of a position to deposit collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | WatchPug, harleythedog |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/69
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

