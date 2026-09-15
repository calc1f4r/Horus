---
# Core Classification
protocol: Revert Lend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32288
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-revert-lend
source_link: https://code4rena.com/reports/2024-03-revert-lend
github_link: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/140

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
finders_count: 3
finders:
  - lanrebayode77
  - 0xAlix2
  - Aymen0909
---

## Vulnerability Title

[M-22] `dailyDebtIncreaseLimitLeft` is not updated in `liquidate()`

### Overview


The bug report describes an issue where on days with a lot of liquidated positions, there is an excess of assets in the vault that cannot be borrowed. This causes a decrease in the utilization rate and contradicts what was stated in the `repay()` function. The proof of concept shows that the `dailyDebtIncreaseLimitLeft` was not incremented in the `liquidate()` function, which should be fixed by including the increment in the function. The bug has been confirmed and mitigated by the Revert team.

### Original Finding Content


On days with a significant number of liquidated positions, particularly when the asset quantity is substantial, there will be an excess of assets available in the vault that cannot be borrowed; thereby, causing a drastic decrease in the utilization rate.

This also contradicts what was stated in the `repay()` function, which asserts that repaid amounts should be borrowed again. Liquidation is also a form of repayment:

```solidity
 // when amounts are repayed - they may be borrowed again
        dailyDebtIncreaseLimitLeft += assets; 
```

### Proof of Concept

`dailyDebyIncreaseLimitLeft` was not increamented in `liquidate()`, see [here](https://github.com/code-423n4/2024-03-revert-lend/blob/435b054f9ad2404173f36f0f74a5096c894b12b7/src/V3Vault.sol#L685-L757).

### Recommended Mitigation Steps

Include `dailyDebyIncreaseLimitLeft` increment in `liquidate()`.

```solidity
dailyDebtIncreaseLimitLeft += state.liquidatorCost;
```

### Assessed type

Context

**[kalinbas (Revert) confirmed](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/140#issuecomment-2020691059)**

**[Revert mitigated](https://github.com/code-423n4/2024-04-revert-mitigation?tab=readme-ov-file#scope):**
> Fixed [here](https://github.com/revert-finance/lend/pull/11).

**Status:** Mitigation Confirmed. Full details in reports from [thank_you](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/97), [b0g0](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/56) and [ktg](https://github.com/code-423n4/2024-04-revert-mitigation-findings/issues/24).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Revert Lend |
| Report Date | N/A |
| Finders | lanrebayode77, 0xAlix2, Aymen0909 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-revert-lend
- **GitHub**: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/140
- **Contest**: https://code4rena.com/reports/2024-03-revert-lend

### Keywords for Search

`vulnerability`

