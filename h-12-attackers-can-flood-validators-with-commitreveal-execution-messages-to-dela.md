---
# Core Classification
protocol: SEDA Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55239
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/729
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/246

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - tallo
  - g
---

## Vulnerability Title

H-12: Attackers can flood validators with Commit/Reveal execution messages to delay blocks or DOS the node

### Overview


This bug report discusses an issue with the SEDA protocol, where attackers can exploit a loophole to flood validators with Commit/Reveal execution messages. These messages are not charged any gas fees, allowing malicious actors to delay blocks or even cause the entire chain to halt. The root cause of this issue is a check in the AnteHandler that sets the gas price to 0 for certain types of messages, making them eligible for free gas. This can be abused by sending multiple transactions filled with the same CommitDataResult or RevealDataResult message. The impact of this bug can cause chain delays or halts. The protocol team has fixed this issue by implementing a check to ensure that transactions do not contain duplicate messages before being eligible for free gas or by charging gas up front and providing a refund mechanism. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/246 

## Found by 
g, tallo

### Summary

Commit and Reveal execution messages sent to the SEDA Core Contract are [not charged](https://github.com/sherlock-audit/2024-12-seda-protocol/blob/main/seda-chain/app/ante.go#L55-L71) any gas fees. This provides a way for malicious actors
to DOS nodes or at the least delay blocks.

### Root Cause

Before a transaction is executed, the AnteHandler is run. It checks if all of the transactions' messages is [eligible for free gas](https://github.com/sherlock-audit/2024-12-seda-protocol/blob/main/seda-chain/app/ante.go#L62-L67) and sets
[gas price to 0](https://github.com/sherlock-audit/2024-12-seda-protocol/blob/main/seda-chain/app/ante.go#L70) when they are. 

A message is [eligible](https://github.com/sherlock-audit/2024-12-seda-protocol/blob/main/seda-chain/app/ante.go#L108-L122) for free gas when it is a `CommitDataResult` or a `RevealDataResult`, and the
executor can commit or reveal.

```golang
  switch contractMsg := contractMsg.(type) {
  case CommitDataResult:
    result, err := d.queryContract(ctx, coreContract, CanExecutorCommitQuery{CanExecutorCommit: contractMsg})
    if err != nil {
      return false
    }

    return result
  case RevealDataResult:
    result, err := d.queryContract(ctx, coreContract, CanExecutorRevealQuery{CanExecutorReveal: contractMsg})
    if err != nil {
      return false
    }

    return result
```

A malicious user can abuse this unmetered execution by filling a transaction with _the same_ CommitDataResult or RevealDataResult message.


### Internal Pre-conditions
None


### External Pre-conditions
None


### Attack Path

1. Attacker sends a Transaction filled with the same CommitDataResult message for a data request that is ready for commitment.
2. Since the attacker's transaction passes `checkFreeGas()` for all its messages, the transaction will be eligible for free gas.

Multiple attackers can repeat this attack to exploit unmetered execution and unnecessarily consume validator resources.

### Impact

This can cause chain delays or chain halts.


### PoC
None


### Mitigation
Consider checking that the transaction does not contain duplicate messages before making it eligible for free gas. Another option is to charge gas up front and provide a refund mechanism instead. 

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/sedaprotocol/seda-chain/pull/527

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | SEDA Protocol |
| Report Date | N/A |
| Finders | tallo, g |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-seda-protocol-judging/issues/246
- **Contest**: https://app.sherlock.xyz/audits/contests/729

### Keywords for Search

`vulnerability`

