---
# Core Classification
protocol: Stusdcxbloom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55682
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
github_link: none

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
finders_count: 1
finders:
  - @IAm0x52
---

## Vulnerability Title

[M-02] In the event of a partial match inside \_convertMatchOrders, borrower funds will be over-allocated

### Overview


This bug report is about a problem in the code of a smart contract called BloomPool. The issue is in the matching loop of the code, where orders are handled. In the case of a fully matched order, the code correctly pops the order. However, in the case of a partially filled order, the code only decreases one type of collateral, leaving the other type unchanged. This can result in borrower funds being double filled, causing a shortage of funds in the contract. The recommendation is to also decrease the other type of collateral in this scenario. This bug has been fixed in a recent update to the code.

### Original Finding Content

**Details**

[BloomPool.sol#L399-L403](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L399-L403)

    if (lenderFunds == matches[index].lCollateral) {
        matches.pop();
    } else {
        matches[index].lCollateral -= uint128(lenderFunds);
    }

Above is the final portion of the matching loop in which filled orders are handled. `lenderFunds == matches[index].lCollateral` indicates the order has been fully matched. In this scenario it is correctly popped. The other case is when the the match is partially filled. We see that lCollateral is decreased but bCollateral is not. The result is that borrower funds can be double filled. This creates a shortfall in funds that can only be remedied by donating the over-allocated funds to the contract.

**Lines of Code**

[BloomPool.sol#L377-L416](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L377-L416)

**Recommendation**

`matches[index].lCollateral` should also be decremented

**Remediation**

Fixed as recommended in bloom-v2 [PR#16](https://github.com/Blueberryfi/bloom-v2/pull/16)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Stusdcxbloom |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

