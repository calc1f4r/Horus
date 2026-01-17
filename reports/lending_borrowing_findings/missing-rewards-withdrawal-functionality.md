---
# Core Classification
protocol: Composable Bridge + PR
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47046
audit_firm: OtterSec
contest_link: https://www.composablefoundation.com/
source_link: https://www.composablefoundation.com/
github_link: https://github.com/ComposableFi/bridge-contract

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Missing Rewards Withdrawal Functionality

### Overview


The collect_rewards instruction in MarginFi only allows for the collection and deposit of rewards into a specific account, but there is no way to withdraw or manage these rewards once they are deposited. This means that the rewards will continue to accumulate in the account without a way to access or use them. To fix this issue, a new function needs to be implemented to allow for the withdrawal or transfer of rewards from the account. This bug has been addressed in PR#8.

### Original Finding Content

## Collect Rewards Instruction

The `collect_rewards` instruction only handles the process of collecting rewards from a MarginFi lending account and depositing them into the `rewards_token_account`. There is no accompanying functionality to withdraw or manage these rewards once they are deposited. This implies that after the rewards are collected, they remain in the `rewards_token_account` without a defined way to be withdrawn or utilized. This will result in a buildup of rewards that are effectively locked in the account.

## Remediation

Implement functionality that allows the withdrawal or transfer of the rewards from the `rewards_token_account`.

## Patch

Fixed in PR#8.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Composable Bridge + PR |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.composablefoundation.com/
- **GitHub**: https://github.com/ComposableFi/bridge-contract
- **Contest**: https://www.composablefoundation.com/

### Keywords for Search

`vulnerability`

