---
# Core Classification
protocol: Dynamo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55650
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
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

[M-02] Assert statement in Dynamo4626#\_claimable_fees_available can cause vault softlock in the event of partial fund loss

### Overview


The bug report states that there is an issue with the assert statement in the code located at line 438 of the Dynamo4626.vy file. This assert statement may trigger incorrectly in cases where there is a partial loss of funds. This can cause the function to revert, which can lead to a denial of service attack until the difference is recovered. The recommended solution is to return 0 instead of reverting. This issue has been fixed in a recent commit.

### Original Finding Content

**Details**

[Dynamo4626.vy#L438](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/Dynamo4626.vy#L438)

    assert self.total_strategy_fees_claimed + self.total_yield_fees_claimed <= total_fees_ever, "Total fee calc error!"

In the event of partial fund loss there may be legit cases where this assert statement is triggered. If the vault suffers a partial loss but still maintains a positive return (i.e. it has made 100e18 but suffers a loss of 50e18) then this statement will improperly revert. Given this function is called with every deposit and withdraw the vault would be completely DOS'd until yield (or donation) recovered the difference.

**Lines of Code**

[Dynamo4626.vy#L418-L459](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/Dynamo4626.vy#L418-L459)

**Recommendation**

Instead of reverting, simply return 0.

**Remediation**

Fixed [here](https://github.com/DynamoFinance/vault/commit/6e762711f55f9cf4bece42706ddef7c92d5b4ac4) by returning 0 instead of reverting

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Dynamo |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

