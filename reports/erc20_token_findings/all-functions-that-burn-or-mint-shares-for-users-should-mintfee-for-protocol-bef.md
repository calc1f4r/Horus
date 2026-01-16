---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27630
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

All functions that burn or mint shares for user's should mintFee for protocol before

### Overview


This bug report is about incorrect fee payments in the Steadefi protocol. The Steadefi protocol takes a management fee from stakers, which accrues each second and is a percentage of the totalSupply. The GMXVault should call the mintFee function before minting or burning shares for users in order to get the correct portion of the fee. Currently, the mintFee is only called in two places in the code. However, minting and burning is not done in any of them. As a result, some time has passed and fees should be accrued, but in the current implementation, new shares are added to the totalSupply and fees are taken out of them for the time when these shares were not even minted. This means that users or the protocol could suffer from incorrect fee payment, depending on the situation. The recommendation is to consider calling the mintFee for all the cases described in the report.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L172">https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L172</a>


## Summary
In case if GMXVault mints/burns shares for users, then it should call `mintFee` before in order to get correct portion of fee.
## Vulnerability Details
Steadefi protocol takes management fee from stakers. This fee accrues each second and is some percentage of totalSupply. In order to mint fees, [GMXVault.mintFee should be called](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXVault.sol#L334-L337). Once, it's done, then `_store.lastFeeCollected` is updated up to date.

Currently `mintFee` is called only in 2 places in the code. Once in the deposit and once in the withdraw function. However, minting and burning is not done in any of them. For example, minting of shares is done [in the `processDeposit` function](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXDeposit.sol#L172) and this function is called after some time, when `deposit` is called. As result some time already has passed and fees should be accrued. But in  current implementation, new shares will be added to the totalSupply and fees will be taken out of them for the time when this shares were not even minted.

Same for the withdraw. When withdraw is called, then shares are not burnt. They are burnt [inside `processWithdraw` function](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXWithdraw.sol#L197). So in case if burn is done before `feeMint` is called, then this removed shares doesn't pay management fee.

And last place is `GMXEmergency.emergencyWithdraw`. This function [also burns shares](https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/strategy/gmx/GMXEmergency.sol#L182), which means that `mintFee` should be called before it.
## Impact
Incorrect fee payment is done, depending on the situation users or protocol will suffer.
## Tools Used
VsCode
## Recommendations
Consider call `mintFee` for all these cases that i have described.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

