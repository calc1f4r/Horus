---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42271
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-08-yield
source_link: https://code4rena.com/reports/2021-08-yield
github_link: https://github.com/code-423n4/2021-08-yield-findings/issues/27

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] `TimeLock` cannot schedule the same calls multiple times

### Overview


The bug report highlights an issue with the `TimeLock.schedule` function, where it reverts if the same `targets` and `data` fields are used. This is because the `txHash` will be the same, making it impossible to schedule the same transaction multiple times. This can cause problems for situations where a contractor needs to be paid every 2 weeks, but the delay is set to 30 days. The report suggests including `eta` in the hash, which would allow for the same transaction data to be used by specifying a different `eta`. The report also mentions that the issue has been confirmed by another user and has been patched by the Yield team by refactoring the `TimeLock` function.

### Original Finding Content

_Submitted by cmichel_

The `TimeLock.schedule` function reverts if the same `targets` and `data` fields are used as the `txHash` will be the same.
This means one cannot schedule the same transactions multiple times.

Imagine the delay is set to 30 days, but a contractor needs to be paid every 2 weeks. One needs to wait 30 days before scheduling the second payment to them.

Recommend also including `eta` in the hash. (Compound's `Timelock` does it as well.) This way the same transaction data can be used by specifying a different `eta`.

**[alcueca (Yield) confirmed](https://github.com/code-423n4/2021-08-yield-findings/issues/27#issuecomment-898830142):**
 > Funny, [BoringCrypto was quite negative about including the eta in the txHash](https://twitter.com/Boring_Crypto/status/1425401221091762189). At the time I couldn't think of a reason to repeat the same call with the same data, but you are right that sometimes it might make sense, and storing off-chain the expected eta of each timelocked transaction is something you should do anyway.
>
> I'll confirm this issue, and will bring it for public discussion once the contest is over.

**[alcueca (Yield) patched](https://github.com/code-423n4/2021-08-yield-findings/issues/27#issuecomment-921487023):**
> I ended up [refactoring the Timelock](https://github.com/yieldprotocol/yield-utils-v2/blob/main/contracts/utils/Timelock.sol) so that the eta is not included in the parameters, but repeated proposals are allowed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-yield
- **GitHub**: https://github.com/code-423n4/2021-08-yield-findings/issues/27
- **Contest**: https://code4rena.com/reports/2021-08-yield

### Keywords for Search

`vulnerability`

