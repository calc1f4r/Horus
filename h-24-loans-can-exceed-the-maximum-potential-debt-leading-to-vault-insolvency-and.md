---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3662
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/169

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

H-24: Loans can exceed the maximum potential debt leading to vault insolvency and possible loss of LP funds

### Overview


Bug report H-24 is about a vulnerability found in the `LienToken.createLien` function of the Sherlock Audit project. The function tries to prevent loans and the total potential debt from surpassing the defined `params.terms.maxPotentialDebt` limit. However, the `getTotalDebtForCollateralToken` function does not consider the new lien being added and for which this check is being performed. This can allow loans on a collateral to exceed maximum potential debt leading to vault insolvency and potential loss of LP funds. 

The bug was found by 0xRajeev and a PoC has been provided by berndartmueller. The impact of this bug is that the strategist's defined max potential debt limit can be exceeded, changing/increasing the risk for LPs, as it imposes a higher debt to the public vault. This could lead to vault insolvency and loss of LP funds.

The code snippet provided is from the `LienToken.sol` file at line 253-262. The bug was discovered during a manual review. The recommendation is to check the total debt limit after adding the new lien to the `liens[collateralId]` array. The bug was discussed by androolloyd, secureum, sherlock-admin, and Evert0x, and has been accepted for 2 USDC. The contestants' payouts and scores will be updated according to the changes made on this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/169 

## Found by 
0xRajeev

## Summary

Missing to account for the new lien can allow loans on a collateral to exceed maximum potential debt leading to vault insolvency and potential loss of LP funds.

## Vulnerability Detail

The `LienToken.createLien` function tries to prevent loans and the total potential debt from surpassing the defined `params.terms.maxPotentialDebt` limit. When the `getTotalDebtForCollateralToken` function is called, the new lien (which will be created within this transaction) is not yet added to the `liens[collateralId]` array. However, the `getTotalDebtForCollateralToken` function iterates over this very same array and will return the total debt without considering the new lien being added and for which this check is being performed.

## Impact

The strategist's defined max potential debt limit can be exceeded, which changes/increases the risk for LPs, as it imposes a higher debt to the public vault. This could lead to vault insolvency and loss of LP funds.

PoC: https://gist.github.com/berndartmueller/8b0f870962acc4c999822d742e89151b

Example exploit: Given a public vault and a lien with a max potential debt amount of 50 ETH (that's the default `standardLien` in TestHelpers.t.sol)

    1. 100 ETH have been deposited in the public vault by LPs
    2. Bob borrows 50 ETH with his 1st NFT -> success
    3. Bob borrows another 50 ETH with his 2nd NFT -> successful as well even though theirs a limit of 50 ETH 
    4. Bob now has 100 ETH -> The max potential debt limit is exceeded by 50 ETH

## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L253-L262

## Tool used

Manual Review

## Recommendation

Check the total debt limit after adding the new lien to the `liens[collateralId]` array.

## Discussion

**androolloyd**

this is working as intended, the value is intended to represent the max potential debt the collateral can potentnially be under at the moment the new terms are originated.

**secureum**

Escalate for 2 USDC.

We still think this is a valid issue with a high-severity impact as described above and demonstrated in the PoC.

cc @berndartmueller @lucyoa 

**sherlock-admin**

 > Escalate for 2 USDC.
> 
> We still think this is a valid issue with a high-severity impact as described above and demonstrated in the PoC.
> 
> cc @berndartmueller @lucyoa 

You've created a valid escalation for 2 USDC!

To remove the escalation from consideration: Delete your comment.
To change the amount you've staked on this escalation: Edit your comment **(do not create a new comment)**.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**Evert0x**

Escalation accepted

Having the possibility of exceeding the maximum potential debt should be mitigated

**sherlock-admin**

> Escalation accepted
> 
> Having the possibility of exceeding the maximum potential debt should be mitigated

This issue's escalations have been accepted!

Contestants' payouts and scores will be updated according to the changes made on this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/169
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

