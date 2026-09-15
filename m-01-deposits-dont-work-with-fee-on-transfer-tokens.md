---
# Core Classification
protocol: PoolTogether
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25559
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-pooltogether
source_link: https://code4rena.com/reports/2021-10-pooltogether
github_link: https://github.com/code-423n4/2021-10-pooltogether-findings/issues/30

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Deposits don't work with fee-on transfer tokens

### Overview


This bug report is about ERC20 tokens that have certain customizations, such as deflationary tokens or rebasing tokens. The `PrizePool._depositTo()` function attempts to supply more `_amount` than was actually transferred, causing the transaction to revert and the tokens to be unusable. A possible mitigation is to measure the asset change before and after asset-transferring routines. The sponsor acknowledges the finding and suggests not using `feeOnTransfer` tokens in the protocol to avoid this issue.

### Original Finding Content

_Submitted by cmichel_.

There are ERC20 tokens that may make certain customizations to their ERC20 contracts.
One type of these tokens is deflationary tokens that charge a certain fee for every `transfer()` or `transferFrom()`.
Others are rebasing tokens that increase in value over time like Aave's aTokens (`balanceOf` changes over time).

#### Impact

The `PrizePool._depositTo()` function will try to supply more `_amount` than was actually transferred.
The tx will revert and these tokens cannot be used.

#### Recommended Mitigation Steps

One possible mitigation is to measure the asset change right before and after the asset-transferring routines

**[asselstine (PoolTogether) acknowledged](https://github.com/code-423n4/2021-10-pooltogether-findings/issues/30#issuecomment-942994789):**
 > We don't plan on incorporating fee-on-transfer tokens, so I think we can safely ignore this.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-10-pooltogether-findings/issues/30#issuecomment-943854691):**
 > The sponsor acknowledges the finding, simple mitigation is to not use `feeOnTransfer` tokens in the protocol





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | PoolTogether |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-pooltogether
- **GitHub**: https://github.com/code-423n4/2021-10-pooltogether-findings/issues/30
- **Contest**: https://code4rena.com/reports/2021-10-pooltogether

### Keywords for Search

`vulnerability`

