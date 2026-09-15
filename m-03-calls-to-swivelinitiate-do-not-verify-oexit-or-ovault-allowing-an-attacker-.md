---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25287
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/93

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
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Calls To `Swivel.initiate()` Do Not Verify `o.exit` or `o.vault` Allowing An Attacker To Manipulate Accounting In Their Favour

### Overview


Kirk-baird reported a bug in Swivel’s ‘lend()’ function, which does not validate the ‘o.exit’ and ‘o.vault’ for each order before making the external call to Swivel. These values determine which internal function is called in Swivel. If an incorrect function is called, the accounting in ‘lend()’ may transfer more tokens from the lender to Swivel than paid for by the caller of ‘lend()’. This could result in underlying tokens being stolen from the lender. 

To demonstrate this, an example was given where the ‘initiateZcTokenFillingZcTokenExit()’ function is called. This would transfer ‘a - premiumFilled + fee’ from the lender to Swivel instead of the expected ‘a + fee’. 

The recommended mitigation step is to restrict the values of ‘o.exit’ and ‘o.vault’ in the ‘lend()’ function so that only one case can be triggered in ‘Swivel.initiate()’. Sourabhmarathe (Illuminate) commented that while users could get better execution by submitting certain orders, invalid orders would be rejected by Swivel and users should be free to execute the best possible orders. JTraversa (Illuminate) confirmed the issue, but disagreed with the severity. Gzeoneth (judge) decreased the severity to Medium, as no funds are lost after maturity.

### Original Finding Content

_Submitted by kirk-baird_

Swivel `lend()` does not validate the `o.exit` and `o.vault` for each order before making the external call to Swivel. These values determine which internal functions is [called in Swivel](https://github.com/Swivel-Finance/swivel/blob/2471ea5cda53568df5e5515153c6962f151bf358/contracts/v2/swivel/Swivel.sol#L64-L77).

The intended code path is `initiateZcTokenFillingVaultInitiate()` which takes the underlying tokens and mints zcTokens to the `Lender`. If one of the other functions is called the accounting in `lend()`. Swivel may transfer more tokens from `Lender` to `Swivel` than paid for by the caller of `lend()`.

The impact is that underlying tokens may be stolen from `Lender`.

### Proof of Concept

Consider the example where [initiateZcTokenFillingZcTokenExit()](https://github.com/Swivel-Finance/swivel/blob/2471ea5cda53568df5e5515153c6962f151bf358/contracts/v2/swivel/Swivel.sol#L162) is called. This will transfer `a - premiumFilled + fee` from `Lender` to `Swivel` rather than the expected `a + fee`.

### Recommended Mitigation Steps

In `lend()` restrict the values of `o.exit` and `o.vault` so only one case can be triggered in `Swivel.initiate()`.

**[sourabhmarathe (Illuminate) commented](https://github.com/code-423n4/2022-06-illuminate-findings/issues/93#issuecomment-1170106132):**
 > While it is true that a user could get better execution by submitting certain orders, we don't think this is a problem. Invalid orders would be rejected by Swivel, and users should be free to execute the best possible orders.

**[JTraversa (Illuminate) confirmed, but disagreed wtih severity and commented](https://github.com/code-423n4/2022-06-illuminate-findings/issues/93#issuecomment-1172933061):**
 > So reviewing this, there is an issue though it may not be high-risk.
> 
> The user *can* manipulate the method by sending it an order that is not the correct type to go down the intended order path.
> 
> That said, the result on line [297](https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L297) is still that the calculated lent value is sent to the contract.
> 
> So the result is that the user inputting this manipulation actually still pays for their iPTs, and their underlying just sits in lender.sol until maturity with no personal benefit. The attack would none-the-less leak value and with that in mind I'd probably just drop it down to medium?

**[gzeoneth (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-06-illuminate-findings/issues/93#issuecomment-1186218223):**
 > Judging as Med Risk as no fund is lost (after maturity).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/93
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

