---
# Core Classification
protocol: Velar Artha PerpDEX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41286
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/526
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-velar-artha-judging/issues/82

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
finders_count: 8
finders:
  - Bauer
  - y4y
  - bughuntoor
  - KupiaSec
  - Greed
---

## Vulnerability Title

M-6: Usage of `tx.origin` to determine the user is prone to attacks

### Overview


The bug report discusses a vulnerability found by multiple individuals in a code that uses `tx.origin` to determine the user. This method is dangerous as it can put the user at risk when interacting with unverified contracts or contracts that can change implementation. It also breaks compatibility with Account Abstract wallets. The impact of this vulnerability is that users risk losing their funds when calling any contract on the BOB chain. The recommendation is to pass `msg.sender` as a parameter instead of using `tx.origin`. There was a discussion among the team members about whether to escalate the issue, but it was ultimately resolved with the status of "Medium" and having duplicates.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-velar-artha-judging/issues/82 

## Found by 
Bauer, Greed, Japy69, KupiaSec, Waydou, bughuntoor, ctf\_sec, y4y
## Summary
Usage of `tx.origin` to determine the user is prone to attacks

## Vulnerability Detail
Within `core.vy` to user on whose behalf it is called is fetched by using `tx.origin`.
```vyper
  self._INTERNAL()

  user        : address   = tx.origin
```

This is dangerous, as any time a user calls/ interacts with an unverified contract, or a contract which can change implementation, they're put under risk, as the contract can make a call to `api.vy` and act on user's behalf.

Usage of `tx.origin` would also break compatibility with Account Abstract wallets.

## Impact
Any time a user calls any contract on the BOB chain, they risk getting their funds lost.
Incompatible with AA wallets.

## Code Snippet
https://github.com/sherlock-audit/2024-08-velar-artha/blob/main/gl-sherlock/contracts/core.vy#L166

## Tool used

Manual Review

## Recommendation
Instead of using `tx.origin` in `core.vy`, simply pass `msg.sender` as a parameter from `api.vy`



## Discussion

**T1MOH593**

Escalate

Noticed there were 19 escalations on preliminary valid issues. This is final escalation to make it 20/20 🙂

**sherlock-admin3**

> Escalate
> 
> Noticed there were 19 escalations on preliminary valid issues. This is final escalation to make it 20/20 🙂

You've created a valid escalation!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**WangSecurity**

bruh

**WangSecurity**

Planning to reject the escalation and leave the issue as it is.

**WangSecurity**

Result:
Medium
Has duplicates

**sherlock-admin4**

Escalations have been resolved successfully!

Escalation status:
- [T1MOH593](https://github.com/sherlock-audit/2024-08-velar-artha-judging/issues/82/#issuecomment-2347091773): rejected

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Velar Artha PerpDEX |
| Report Date | N/A |
| Finders | Bauer, y4y, bughuntoor, KupiaSec, Greed, Waydou, Japy69, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-velar-artha-judging/issues/82
- **Contest**: https://app.sherlock.xyz/audits/contests/526

### Keywords for Search

`vulnerability`

