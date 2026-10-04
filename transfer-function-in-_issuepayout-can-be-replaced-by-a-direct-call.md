---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21839
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-Mon and Natalie
  - Jonah1005
  - Blockdev
---

## Vulnerability Title

transfer(...) function in _issuePayout(...) can be replaced by a direct call

### Overview


This bug report is about a medium risk issue in the _issuePayout(...) internal function of the VaultImplementation. If the asset is WETH, the amount is withdrawn from WETH to native tokens and then transferred to the borrower. The problem is that this transfer limits the amount of gas shared to the call to the borrower, which could prevent executing a complex callback and, due to changes in gas prices in EVM, might even break some features for a potential borrower contract. The recommendation is to call the borrower directly without restricting the gas shared, but only if the recommendation from the issue 'Storage parameters are updated after a few callback sites to external addresses in the commitToLien(...) flow' is applied.

### Original Finding Content

## Severity: Medium Risk

## Context
- VaultImplementation.sol#L245

## Description
In the `_issuePayout(...)` internal function of the `VaultImplementation`, if the asset is WETH, the amount is withdrawn from WETH to native tokens and then transferred to the borrower:

```solidity
if (asset() == WETH()) {
    IWETH9 wethContract = IWETH9(asset());
    wethContract.withdraw(newAmount);
    payable(borrower).transfer(newAmount);
}
```

The `transfer` limits the amount of gas shared to the call to the borrower, which would prevent executing a complex callback. Due to changes in gas prices in the EVM, it might even break some feature for a potential borrower contract. For the analysis of the flow for both types of vaults, please refer to the following issue:
- 'Storage parameters are updated after a few callback sites to external addresses in the commitToLien(...) flow'

## Recommendation
Call the borrower directly without restricting the gas shared and only apply this recommendation if the recommendation from the issue 'Storage parameters are updated after a few callback sites to external addresses in the commitToLien(...) flow' is applied.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Jonah1005, Blockdev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf

### Keywords for Search

`vulnerability`

