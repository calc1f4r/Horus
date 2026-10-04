---
# Core Classification
protocol: Redacted Cartel
chain: everychain
category: uncategorized
vulnerability_type: swap

# Attack Vector Details
attack_type: swap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6040
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-redacted-cartel-contest
source_link: https://code4rena.com/reports/2022-11-redactedcartel
github_link: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/91

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - swap

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - rbserver
  - cccz
  - immeas
  - Jeiwan
  - Englave
---

## Vulnerability Title

[M-03] Anyone can call AutoPxGmx.compound and perform sandwich attacks with control parameters

### Overview


This bug report is about a vulnerability in the AutoPxGmx.compound function of the code-423n4/2022-11-redactedcartel repository on GitHub. The vulnerability allows anyone to call the function and get an incentive, but it also allows malicious users to perform a sandwich attack for profit. This is possible by providing certain parameters to the SWAP_ROUTER.exactInputSingle function, such as the fee parameter to make the token swap occur in a small liquid pool, and the amountOutMinimum parameter set to 1 to make the token swap accept a large slippage. To mitigate this vulnerability, it is recommended to use poolFee as the fee and an onchain price oracle to calculate the amountOutMinimum.

### Original Finding Content


AutoPxGmx.compound allows anyone to call to compound the reward and get the incentive.

However, AutoPxGmx.compound calls `SWAP_ROUTER`.exactInputSingle with some of the parameters provided by the caller, which allows the user to perform a sandwich attack for profit.

For example, a malicious user could provide the fee parameter to make the token swap occur in a small liquid pool, and could make the amountOutMinimum parameter 1 to make the token swap accept a large slippage, thus making it easier to perform a sandwich attack.

### Proof of Concept

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/vaults/AutoPxGmx.sol#L242-L278>

### Recommended Mitigation Steps

Consider using poolFee as the fee and using an onchain price oracle to calculate the amountOutMinimum.

**[Picodes (judge) commented](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/91#issuecomment-1337106500):**
 > Flagging as best as the warden identifies that the main risk is not the possibility to increase fees but the fact that some of the pools will be highly illiquid.

**[drahrealm (Redacted Cartel) disagreed with severity and commented](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/91#issuecomment-1342052424):**
 > Please refer to:
> https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/185#issuecomment-1341252133

**[Picodes (judge) commented](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/91#issuecomment-1368089130):**
 > It's very likely that this attack is profitable as most of the time only 1 or 2 pools have decent liquidity, so Medium severity is appropriate.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Redacted Cartel |
| Report Date | N/A |
| Finders | rbserver, cccz, immeas, Jeiwan, Englave, xiaoming90, hansfriese, aphak5010 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-redactedcartel
- **GitHub**: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/91
- **Contest**: https://code4rena.com/contests/2022-11-redacted-cartel-contest

### Keywords for Search

`Swap`

