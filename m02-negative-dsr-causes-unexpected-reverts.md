---
# Core Classification
protocol: Compound Finance – MCD & DSR Integration
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11578
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-finance-mcd-dsr-integration/
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
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M02] Negative DSR causes unexpected reverts

### Overview


This bug report is related to the Compound Protocol's DAIInterestRateModel.sol. On line 66 of the file, `1e27` is subtracted from `dsr`. If `dsr` is less than `1e27`, any calls to the `dsrPerBlock` function, `poke` function, and `getSupplyRate` function will revert. This could prevent updating the `baseRatePerBlock` and `multiplierPerBlock` state variables. The Maker developers have said they do not plan to ever allow `dsr` to be less than `1e27`, but this could still happen via the Maker governance system. To prevent this, consider modifying `dsrPerBlock` such that it returns `0` when `dsr` is less than `1e27`, and also consider implementing a mechanism to remove DAI from the DSR contract and to stop deposits into the DSR contract.

### Original Finding Content

[On line 66 of `DAIInterestRateModel.sol`](https://github.com/compound-finance/compound-protocol/blob/9ea64ddd166a78b264ba8006f688880085eeed13/contracts/DAIInterestRateModel.sol#L66), `1e27` is subtracted from `dsr`. If for any reason, `dsr` is less than `1e27` (which corresponds to a “negative” interest rate), any calls to [the `dsrPerBlock` function](https://github.com/compound-finance/compound-protocol/blob/9ea64ddd166a78b264ba8006f688880085eeed13/contracts/DAIInterestRateModel.sol#L64) will revert. This includes all calls to [the `poke` function](https://github.com/compound-finance/compound-protocol/blob/9ea64ddd166a78b264ba8006f688880085eeed13/contracts/DAIInterestRateModel.sol#L74) and [the `getSupplyRate` function](https://github.com/compound-finance/compound-protocol/blob/9ea64ddd166a78b264ba8006f688880085eeed13/contracts/DAIInterestRateModel.sol#L48).


While the Maker developers have said they do not have plans to ever allow `dsr` to be less than `1e27`, this could still happen via the Maker governance system.


Reverting on `poke` could prevent updating the `baseRatePerBlock` and `multiplierPerBlock` state variables.


Consider modifying `dsrPerBlock` such that it returns `0` when `dsr &lt; 1e27` (corresponding to a DSR of 0%). Also consider implementing a mechanism to remove DAI from the DSR contract, and to stop deposits into the DSR contract, just in case `dsr` is ever made less than `1e27`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Finance – MCD & DSR Integration |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-finance-mcd-dsr-integration/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

