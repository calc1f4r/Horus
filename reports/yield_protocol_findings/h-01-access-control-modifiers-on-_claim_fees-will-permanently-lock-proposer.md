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
solodit_id: 55644
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
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
  - @IAm0x52
---

## Vulnerability Title

[H-01] Access control modifiers on \_claim_fees will permanently lock proposer

### Overview


The bug report is about a problem in the code for the Dynamo4626 contract. The issue is that when the contract tries to distribute fees to the proposer, it requires that the person calling the function is also the proposer. However, since the function can only be called by governance, this will always cause the function to fail. This means that the first proposer will have a monopoly on all proposals, as any other proposer's strategies will fail when trying to activate them. The recommendation is to revise the access control for this function, allowing anyone to claim tokens and sending them to the correct target instead of the person calling the function. The bug has been fixed by allowing governance to claim on behalf of the proposer.

### Original Finding Content

**Details**

[Dynamo4626.vy#L519-L521](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/Dynamo4626.vy#L519-L521)

    elif _yield == FeeType.PROPOSER:
        assert msg.sender == self.current_proposer, "Only curent proposer may claim strategy fees."
        self.total_strategy_fees_claimed += claim_amount

Dynamo4626#\_set_strategy attempts to distribute fees to proposer when proposer changes. The problem is that \_claim_fees requires that msg.sender == proposer. Since \_set_strategy can only be called by governance this subcall will always revert. The result is that the first proposer will have a monopoly on all proposals since any strategy that wasn't submitted by them would fail when attempting to activate it.

**Lines of Code**

https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/Dynamo4626.vy#L496-L533

**Recommendation**

Revise access control on \_set_strategy. I would suggest allowing anyone to claim tokens but sending to the correct target instead of msg.sender

**Remediation**

Fixed [here](https://github.com/DynamoFinance/vault/commit/1601b0acd23783ed87b9b3ae01c6a97a462a41a8) by allowing governance to claim on behalf of proposer

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

