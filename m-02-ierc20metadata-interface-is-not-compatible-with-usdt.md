---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63601
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] `IERC20Metadata` interface is not compatible with `USDT`

### Overview


The report describes a bug in MorphoMarketFactory which prevents the transfer of loan token. The bug occurs when using non-compliant ERC20 tokens like USDT which do not return a value on `approve()`. This causes the transaction to revert, making it impossible to use these tokens as loan tokens in the Morpho market. The recommended solution is to replace `loan.approve` with `loan.forceApprove` in the code.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

`MorphoMarketFactory.create()` approves the Morpho protocol to transfer the loan token. However, the `IERC20Metadata` interface is not compatible with `USDT` and other non-compliant ERC20 tokens that do not return a value on `approve()`, making the transaction revert.

```solidity
        // Feed the market with exactly 1 token so that there is available liquidity for the subsequent borrow.
        uint256 loanToSupply = 10 ** loan.decimals();
        loan.safeTransferFrom(msg.sender, address(this), loanToSupply);
    @>  loan.approve(address(MORPHO_BLUE), loanToSupply);
```

As a result, `USDT` and similar tokens cannot be used as a loan token in the Morpho market.

## Recommendations

```diff
-   loan.approve(address(MORPHO_BLUE), loanToSupply);
+   loan.forceApprove(address(MORPHO_BLUE), loanToSupply);
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

