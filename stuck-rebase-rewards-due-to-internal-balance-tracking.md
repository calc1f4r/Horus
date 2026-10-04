---
# Core Classification
protocol: Enjoyoors
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49876
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Enjoyoors/EVM%20Vaults/README.md#2-stuck-rebase-rewards-due-to-internal-balance-tracking
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
  - MixBytes
---

## Vulnerability Title

Stuck Rebase Rewards Due to Internal Balance Tracking

### Overview


The report discusses a bug in the `_deposit` function of the contract `EnjoyoorsVaultDeposits`. This function does not account for rebasing tokens, which can increase their balance over time through rewards or interest. This leads to a permanent loss of user rewards and affects all users of rebasing tokens. The bug is classified as critical because it has no mechanism for recovery and can result in significant loss over time. The report recommends two solutions: tracking user shares instead of absolute amounts or prohibiting the use of rebasing tokens if the contract cannot handle them properly.

### Original Finding Content

##### Description
The issue is identified within the function `_deposit` of contract `EnjoyoorsVaultDeposits`.

The contract implements internal balance tracking through `userSupply[token][msg.sender] += amount` which does not account for rebasing tokens. Rebasing tokens (like stETH, aTokens) can increase their balance over time through protocol rewards or interest accrual. Since the contract tracks user balances internally and limits withdrawals to the tracked deposit amount, any additional tokens received from rebasing will become permanently locked in the contract.

The issue is classified as **Critical** severity because:
1. It leads to permanent loss of user rewards from rebasing tokens
2. There is no mechanism to recover these stuck tokens
3. The issue affects all users of rebasing tokens systematically
4. The locked rewards could potentially accumulate to significant amounts over time

##### Recommendation
We recommend implementing one of the following solutions:
1. Track user shares instead of absolute amounts:
   - Convert deposit amounts to shares based on the current total supply
   - Calculate withdrawal amounts based on the share of total balance
   - This automatically distributes rebases proportionally to all users

2. As a minimal solution:
   - Explicitly prohibit rebasing tokens if the contract cannot properly handle them
   - Use wrapped alternative of a rebasing token if exists (wstETH for stETH as an example)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Enjoyoors |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Enjoyoors/EVM%20Vaults/README.md#2-stuck-rebase-rewards-due-to-internal-balance-tracking
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

