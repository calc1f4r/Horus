---
# Core Classification
protocol: Backd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2093
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backd-contest
source_link: https://code4rena.com/reports/2022-04-backd
github_link: https://github.com/code-423n4/2022-04-backd-findings/issues/161

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
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Ruhum
---

## Vulnerability Title

[M-04] `CvxCrvRewardsLocker` implements a swap without a slippage check that can result in a loss of funds through MEV

### Overview


This bug report is about a vulnerability in the CvxCrvRewardsLocker contract which swaps tokens through the CRV cvxCRV pool. It does not have any slippage checks which makes it vulnerable to frontrunning or sandwiching, resulting in a loss of funds. The vulnerability is present in the swap code, which can be found at the given link. No tools were used to identify this vulnerability. The recommended mitigation step is to use a proper value for 'minOut' instead of 0.

### Original Finding Content

_Submitted by Ruhum_

The CvxCrvRewardsLocker contract swaps tokens through the CRV cvxCRV pool. But, it doesn't use any slippage checks. The swap is at risk of being frontrun / sandwiched which will result in a loss of funds.

Since MEV is very prominent I think the chance of that happening is pretty high.

### Proof of Concept

Here's the swap: [CvxCrvRewardsLocker.sol#L247-L252](https://github.com/code-423n4/2022-04-backd/blob/c856714a50437cb33240a5964b63687c9876275b/backd/contracts/CvxCrvRewardsLocker.sol#L247-L252).

### Recommended Mitigation Steps

Use a proper value for `minOut` instead of `0`.

**[chase-manning (Backd) confirmed](https://github.com/code-423n4/2022-04-backd-findings/issues/161)**

**[gzeon (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-04-backd-findings/issues/161#issuecomment-1120269300):**
 > According to [C4 Judging criteria](https://docs.code4rena.com/roles/judges/how-to-judge-a-contest#notes-on-judging):
> > Unless there is something uniquely novel created by combining vectors, most submissions regarding vulnerabilities that are inherent to a particular system or the Ethereum network as a whole should be considered QA. Examples of such vulnerabilities include front running, sandwich attacks, and MEV. 
> 
> However since there is a configurable `minOut` that is deliberately set to 0, this seems to be a valid issue. I am judging this as Medium Risk.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backd |
| Report Date | N/A |
| Finders | Ruhum |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backd
- **GitHub**: https://github.com/code-423n4/2022-04-backd-findings/issues/161
- **Contest**: https://code4rena.com/contests/2022-04-backd-contest

### Keywords for Search

`vulnerability`

