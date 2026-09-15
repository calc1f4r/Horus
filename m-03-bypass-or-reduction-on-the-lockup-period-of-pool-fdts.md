---
# Core Classification
protocol: Maple Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25470
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-04-maple
source_link: https://code4rena.com/reports/2021-04-maple
github_link: https://github.com/code-423n4/2021-04-maple-findings/issues/117

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
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Bypass or reduction on the lockup period of Pool FDTs.

### Overview


A bug was discovered in the Pool.sol file of the Maple Core protocol, which allows liquidity providers to bypass or reduce the lockup restriction of withdrawal. The bug is caused by a weighted timestamp that is used to calculate the deposit date, which can be manipulated by two liquidity providers cooperating with each other. The first liquidity provider, Alice, deposits liquidity assets into the pool and mints some FDTs. She then waits for the lockup period and calls intendToWithdraw to pass her withdrawal window. The second liquidity provider, Bob, deposits liquidity assets into the pool and mints some FDTs. Bob and Alice then agree to cooperate with each other to reduce Bob's waiting time for withdrawal. Bob transfers his FDT to Alice via the _transfer function. Alice calls intendToWithdraw and waits for the withdrawCooldown period. Notice that Alice's depositDate is updated after the transfer; however, since it is calculated using a weighted timestamp, the increased amount of lockup time should be less than lockupPeriod. Alice then withdraws the amount of FDT that Bob transferred to her and transfers the funds (liquidity assets) to Bob. Bob successfully reduces (or bypasses) the lockup period of withdrawal.

To address this issue, Maple Labs proposed to either force users to wait for the lockup period when transferring FDT to others or let the depositDate variable record the timestamp of the last operation instead of a weighted timestamp. This was confirmed by Maple Labs and a pull request was submitted to fix the issue.

### Original Finding Content


In `Pool.sol`, the lockup restriction of withdrawal (`Pool.sol#396`) can be bypassed or reduced if new liquidity providers cooperate with existing ones.

1. A liquidity provider, Alice, deposits liquidity assets into the pool and minted some FDTs. She then waits for `lockupPeriod` days and calls `intendToWithdraw` to pass her withdrawal window. Now she is available to receive FDTs from others.
2. A new liquidity provider, Bob, deposits liquidity assets into the pool and minted some FDTs. Currently, he is not allowed to withdraw his funds by protocol design.
3. Bob and Alice agree to cooperate with each other to reduce Bob's waiting time for withdrawal. Bob transfers his FDT to Alice via the `_transfer` function.
4. Alice calls `intendToWithdraw` and waits for the `withdrawCooldown` period. Notice that Alice's `depositDate` is updated after the transfer; however, since it is calculated using a weighted timestamp, the increased amount of lockup time should be less than `lockupPeriod`. In situations where the deposit from Alice is much larger than that from Bob, Alice could only even need to wait for the `withdrawCooldown` period before she could withdraw any funds.
5. Alice then withdraws the amount of FDT that Bob transferred to her and transfers the funds (liquidity assets) to Bob. Bob successfully reduces (or bypasses) the lockup period of withdrawal.

Recommend forcing users to wait for the lockup period when transferring FDT to others or let the `depositDate` variable record the timestamp of the last operation instead of a weighted timestamp.

**[lucas-manuel (Maple) confirmed](https://github.com/code-423n4/2021-04-maple-findings/issues/117#issuecomment-827880947):**

> Addressed in [this PR](https://github.com/maple-labs/maple-core/pull/378)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maple Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-maple
- **GitHub**: https://github.com/code-423n4/2021-04-maple-findings/issues/117
- **Contest**: https://code4rena.com/reports/2021-04-maple

### Keywords for Search

`vulnerability`

