---
# Core Classification
protocol: Vetenet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34030
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2023-12-01-veTenet.md
github_link: none

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
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[C-01] Cloning a `subGauge` can result in an uninitialized proxy

### Overview


The bug report states that there is a high severity and likelihood of a bug in the `subGauge` initialization process in the `GaugeFactory::createSubGauge` function. This can result in a front-running attack, where an attacker can control the `subGauge` by initializing it with their own arguments. The report recommends that the `subGauge` should be initialized in the same way as it is done in the `GaugeFactory::createGaugeProxyAndSubGauges` function.

### Original Finding Content

**Severity**

**Impact:**
High, as `subGauge` initialization can be front-ran

**Likelihood:**
High, as every new `subGauge` will be vulnerable

**Description**

In `GaugeFactory::createSubGauge`, the `Clones::cloneDeterministic` method is used to deploy a new `subGauge`. The problem is, in contrast to `GaugeFactory::createGaugeProxyAndSubGauges`, in `createSubGauge` the `subGauge` is not initialized after cloning, which leaves it vulnerable to a front-running attack. Example scenario:

1. Alice calls `GaugeFactory::createSubGauge` to deploy a new `subGauge`
2. The `subGauge` is added to a `GaugeProxy` by calling `GaugeProxy::addSubGauge`
3. Now Alice sends a transaction to call `initialize` on the `subGauge`
4. Bob sees Alice's transaction and front-runs it, initializing it with his own supplied arguments (`stakingToken`, `governance` etc), so he controls it

**Recommendations**

Initialize a newly cloned `subGauge` in `GaugeFactory::createSubGauge` in the same way that it is done in `GaugeFactory::createGaugeProxyAndSubGauges`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Vetenet |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2023-12-01-veTenet.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

