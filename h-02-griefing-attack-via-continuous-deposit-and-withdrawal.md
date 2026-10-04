---
# Core Classification
protocol: Radiant June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36370
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] Griefing attack via continuous deposit and withdrawal

### Overview


This bug report discusses a potential issue with the `deposit` function in a contract that manages liquidity pools. An attacker can exploit this function to repeatedly withdraw liquidity from the pool, causing a loss of potential fees. This attack can be made more severe when combined with another issue that allows the attacker to use flash loans. The report recommends considering fulfilling withdrawals from the contract's balance before removing liquidity from the pool if there are not enough funds available.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** High

**Description**

The `deposit` function allows users to deposit funds to be added to liquidity pools (LPs) managed by the Rebalancer. When withdrawing tokens, the contract removes the necessary liquidity from the pool to fulfill the withdrawal request. This mechanism can be exploited by an attacker to perform a griefing attack. The attacker can continuously deposit large amounts in each block and withdraw in the next block, thereby forcing the contract to repeatedly remove liquidity from the pool.

This repeated withdrawal of liquidity leaves the funds uninvested in the contract, resulting in the loss of potential fees that could have been generated until the next rebalance. The severity of this attack increases when combined with the `checkLastBlockAction` modifier bypass issue, as it allows the attacker to utilize flash loans and backrun each rebalance transaction, effectively removing all liquidity from the pool continuously.

**Recommendations**

Consider fulfilling the withdrawals from the contract's balance first before opting for a liquidity removal from the pool if the contract's funds are not enough.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Radiant June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

