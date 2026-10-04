---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25224
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/39

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
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-13] It's not possible to execute governance proposals through the `GovernorBravoDelegate` contract

### Overview


A bug has been identified in the GovernorBravoDelegate contract of the Plex-Engineer lending-market repository, which makes it impossible to execute a proposal. The `executed` property of the contract is set to `true` when it is queued up, causing the `state()` function to return `Executed` even though the proposal has not been executed yet. This can result in locked-up funds if those were transferred to the contract before the issue comes up. This bug has been rated HIGH in terms of severity.

The bug was discovered by Ruhum, 0xmint, cccz, csanuragjain, dipp, hake, and zzzitron. The proof of concept was provided in the form of links to the code in the Plex-Engineer repository, as well as the code in the original compound repo.

The recommended mitigation step is to delete the line where `executed` is set to `true`, as the zero-value is `false` anyway, and this will also save gas. This was confirmed by tkkwon1998 (Canto) and Alex the Entreprenerd (judge) commented that due to the coding decision, no transaction can be executed from the Governor Contract, and agreed that the severity of the bug is HIGH.

### Original Finding Content

_Submitted by Ruhum, also found by 0xmint, cccz, csanuragjain, dipp, hake, and zzzitron_

It's not possible to execute a proposal through the GovernorBravoDelegate contract because the `executed` property of it is set to `true` when it's queued up.

Since this means that the governance contract is unusable, it might result in locked-up funds if those were transferred to the contract before the issue comes up. Because of that I'd rate it as HIGH.

#### Proof of Concept

`executed` is set to `true`: <https://github.com/Plex-Engineer/lending-market/blob/main/contracts/Governance/GovernorBravoDelegate.sol#L63>

Here, the `execute()` function checks whether the proposal's state is `Queued`: <https://github.com/Plex-Engineer/lending-market/blob/main/contracts/Governance/GovernorBravoDelegate.sol#L87>

But, since the `execute` property is `true`, the `state()` function will return `Executed`: <https://github.com/Plex-Engineer/lending-market/blob/main/contracts/Governance/GovernorBravoDelegate.sol#L117>

In the original compound repo, `executed` is `false` when the proposal is queued up: <https://github.com/compound-finance/compound-protocol/blob/master/contracts/Governance/GovernorBravoDelegate.sol#L111>

### Recommended Mitigation Steps

Just delete the line where `executed` is set to `true`. Since the zero-value is `false` anyway, you'll save gas as well.

**[tkkwon1998 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-findings/issues/39)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/39#issuecomment-1211409709):**
 > The warden has shown how, due to a coding decision, no transaction can be executed from the Governor Contract.
> 
> Because the functionality is broken, I agree with High Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/39
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

