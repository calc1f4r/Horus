---
# Core Classification
protocol: Interest Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19420
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

get_vault_borrowing_power() could prevent vault’s functionality

### Overview


The bug report describes a potential issue with the get_vault_borrowing_power() function in the Interest Protocol Smart Contracts. This function contains a loop which makes external calls to vault.tokenBalance() and _oracleMaster.getLivePrice(). If any of these external calls were to revert, it could disable the ability to borrow against or liquidate a vault, and if this happened to many vaults across the protocol, the entire protocol could become insolvent. 

Recommendations to mitigate this issue include carefully managing and curating the list of registered tokens and oracles, as well as making all vaults single asset and wrapping external calls in try blocks. The risk was accepted by the project team and no mitigations have been implemented.

### Original Finding Content

## Description

External calls from `get_vault_borrowing_power()` could revert, disabling the ability to borrow against a vault or liquidate a vault. 

`get_vault_borrowing_power()` contains a loop, starting on line [580], which loops through all of the registered tokens and queries the vault for its balance through a call to `vault.tokenBalance()` on line [589]. This, in turn, makes the external call `IERC20(addr).balanceOf(address(this))`. It also contains external calls to external oracles for each registered token through `_oracleMaster.getLivePrice()` on line [594]. 

There is a chance, with all of these external calls, that one of them might revert. In that case, the entire transaction would revert. Some potential revert scenarios might be:

- If the anchor oracle and the main oracle are reporting prices too far apart.
- If an oracle is experiencing a problem with its data source and reverts to prevent providing potentially bad data.
- If a token has a complex balance calculation system, akin to uFragments, but containing an error which causes some balance queries to revert.

Consider a situation where an arbitrary token, let’s call it RVRT, is added to the protocol. After a few weeks of normal operation, it experiences the third issue listed above and reverts on all calls to `RVRT.balanceOf()`. Because this function is called inside `get_vault_borrowing_power()` for all vaults, even those not containing RVRT, all calls to borrow against a vault, or to liquidate a vault would also revert.

In the event that a vault cannot be liquidated and the asset it contains drops heavily, it would be possible for it to become heavily insolvent. If this happened to many vaults across the entire protocol, then the entire protocol would become insolvent: the value of the USDC reserve and the assets in vaults would be significantly lower than the total USDi in circulation.

## Recommendations

This issue can be partially mitigated by carefully managing and curating the list of registered tokens and oracles. However, this does not completely mitigate the issue. 

To fully address this issue, more significant changes may be required. One approach would be to make all vaults single asset. That way, there is no need for the loop within `get_vault_borrowing_power()`. Another approach might be to create a copy of `get_vault_borrowing_power()` for use in transactions, and have that wrap its external calls in try blocks.

## Resolution

This risk was accepted by the project team. No mitigations have been implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Interest Protocol |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf

### Keywords for Search

`vulnerability`

