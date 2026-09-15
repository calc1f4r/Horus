---
# Core Classification
protocol: Mugen
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20422
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Mugen.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[H-01] Anyone can use or steal `ArbitrumSwaps` native asset balance

### Overview


This bug report describes an issue with the `ArbitrumSwaps` native asset balance in which an attacker is able to steal the balance by calling the `arbitrumSwaps` method with steps `WETH_DEPOSIT` and `WETH_WITHDRAW`. This exploit is possible because the `_refundAddress` argument of the `swap` method call to the `stargateRouter` is `address(this)`, which means that all of the native asset that is refunded will be held by the `ArbitrumSwaps` contract. The likelihood of this issue is high, and the impact is medium, as value can be stolen, but it should be limited to gas refunds.

The recommendation to fix this issue is to change the refund address to `msg.sender` rather than `address(this)`. This way, the protocol won't be expected to receive native assets, so they can only be stolen if someone mistakenly sends them to the `ArbitrumSwaps` contract. This is an expected risk, but should be minimized by the change in the refund address.

### Original Finding Content

**Likelihood:**
High, because this can easily be noticed and exploited

**Impact:**
Medium, because value can be stolen, but it should be limited to gas refunds

**Description**

An attacker can steal the `ArbitrumSwaps` native asset balance by doing a call to the `arbitrumSwaps` method with steps `WETH_DEPOSIT` and `WETH_WITHDRAW` - this will send over the whole contract balance to a caller-supplied address. This shouldn't be a problem, because the contract is a "swap router" and is not expected to hold any native asset balance at any time. Well this assumption does not hold, because in the `stargateSwap` method the `_refundAddress` argument of the `swap` method call to the `stargateRouter` is `address(this)`. This means that all of the native asset that is refunded will be held by the `ArbitrumSwaps` contract and an attacker can back-run this refund and steal the balance.

**Recommendations**

The refund address should be `msg.sender` and not `address(this)`. This way the protocol won't be expected to receive native assets, so they can be stolen only if someone mistakenly sends them to the `ArbitrumSwaps` contract which is an expected risk.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Mugen |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Mugen.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

