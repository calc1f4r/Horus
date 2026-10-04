---
# Core Classification
protocol: Malt Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1096
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-malt-finance-contest
source_link: https://code4rena.com/reports/2021-11-malt
github_link: https://github.com/code-423n4/2021-11-malt-findings/issues/125

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
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Meta0xNull
---

## Vulnerability Title

[M-01] TIMELOCK_ROLE Has Absolute Power to Withdraw All FUND May Raise Red Flags for Investors

### Overview


This bug report is about a vulnerability that could allow the TIMELOCK_ROLE to withdraw all funds from a contract using emergencyWithdrawGAS(), emergencyWithdraw(), partialWithdrawGAS(), and partialWithdraw() functions. This could be seen as a rug pull, which is when a developer takes all the funds from a contract without warning, leaving investors with nothing. This vulnerability could be exploited by malicious actors to steal funds.

The proof of concept is provided in the report, which is a link to a GitHub page. The tools used to find the vulnerability were manual review.

The recommended mitigation steps are to pause the contract and disable all functions when bad things happen, and if withdrawing funds can't be avoided, a multi-sig ETH address should be hardcoded into the contract to ensure the funds move to a safe wallet.

### Original Finding Content

_Submitted by Meta0xNull_


`TIMELOCK_ROLE` Can Withdraw All FUND from the Contracts via `emergencyWithdrawGAS(), emergencyWithdraw(), partialWithdrawGAS(), partialWithdraw()`.

While I believe developer have good intention to use these functions. It often associate with Rug Pull by developer in the eyes of investors because Rug Pull is not uncommon in Defi. Investors lose all their hard earn money.

Read More: \$10.8M Stolen, Developers Implicated in Alleged Smart Contract 'Rug Pull'
<https://www.coindesk.com/tech/2020/12/02/108m-stolen-developers-implicated-in-alleged-smart-contract-rug-pull/>

Read More: The Rise of Cryptocurrency Exit Scams and DeFi Rug Pulls
<https://www.cylynx.io/blog/the-rise-of-cryptocurrency-exit-scams-and-defi-rug-pulls/>

#### Proof of Concept

<https://github.com/code-423n4/2021-11-malt/blob/main/src/contracts/Permissions.sol#L80-L109>

#### Recommended Mitigation Steps

1.  Pause the Contract and Disable All Functions when Bad Thing Happen rather than Withdraw All Fund to a random address.
2.  If Withdraw Fund can't avoid, a Multi Sig ETH Address should be hardcoded into the contract to ensure the fund move to a safe wallet.


**[0xScotch (sponsor) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/125#issuecomment-988785042):**
 > Duplicate of #263

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-11-malt-findings/issues/125#issuecomment-1008068213):**
 > This is not a duplicate of #263, where 263 talks about sidestepping the delay of the timelock, this finding talks about the high degree of power that the TIMELOCK_ROLE has.
> 
> This is a typical "admin privilege" finding, it's very important to disclose admin privileges to users so that they can make informed decisions
> 
> In this case the TIMELOCK_ROLE can effectively rug the protocol, however this is contingent on the account that has the role to pull the rug.
> 
> Because of its reliance on external factors, am downgrading the finding to medium severity





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Malt Finance |
| Report Date | N/A |
| Finders | Meta0xNull |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-malt
- **GitHub**: https://github.com/code-423n4/2021-11-malt-findings/issues/125
- **Contest**: https://code4rena.com/contests/2021-11-malt-finance-contest

### Keywords for Search

`vulnerability`

