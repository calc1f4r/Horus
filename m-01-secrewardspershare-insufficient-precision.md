---
# Core Classification
protocol: Canto
chain: everychain
category: arithmetic
vulnerability_type: precision_loss

# Attack Vector Details
attack_type: precision_loss
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30073
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-canto
source_link: https://code4rena.com/reports/2024-01-canto
github_link: https://github.com/code-423n4/2024-01-canto-findings/issues/12

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
  - precision_loss
  - rounding

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - bin2chen
  - xuwinnie
---

## Vulnerability Title

[M-01] secRewardsPerShare Insufficient precision

### Overview


The report discusses a bug in the calculation formula for `secRewardsPerShare` in the Neofinance Coordinator platform. This field is used to distribute rewards to lending platforms integrated with the Coordinator. However, due to a lack of precision in the formula, the value of `secRewardsPerShare` is often rounded down to 0, resulting in a loss of yield for users. The recommended mitigation is to use a precision of 1e27 instead of 1e18. The severity of this bug is considered medium and has been confirmed by the sponsor of the project.

### Original Finding Content


> We also introduced the field secRewardDebt. The idea of this field is to enable any lending platforms that are integrated with Neofinance Coordinator to send their own rewards based on this value (or rather the difference of this value since the last time secondary rewards were sent) and their own emission schedule for the tokens.

The current calculation formula for `secRewardsPerShare` is as follows:

```solidity
market.secRewardsPerShare += uint128((blockDelta * 1e18) / marketSupply);
```

`marketSupply` is `cNOTE`, with a precision of `1e18`
So as long as the supply is greater than `1` cNote, `secRewardsPerShare` is easily `rounded down` to `0`
Example:
marketSupply = 10e18
blockDelta = 1
secRewardsPerShare=1 &ast;  1e18 / 10e18 = 0

### Impact

Due to insufficient precision, `secRewardsPerShare` will basically be 0.

### Recommended Mitigation

It is recommended to use 1e27 for `secRewardsPerShare`:

```solidity
    market.secRewardsPerShare += uint128((blockDelta * 1e27) / marketSupply);
```
**[Alex the Entreprenerd (Judge) commented](https://github.com/code-423n4/2024-01-canto-findings/issues/12#issuecomment-1920977276):**
 > The Warden has shown how, due to incorrect precision, it is possible to create a loss due to rounding down.
> 
> Because the loss is limited to yield, Medium Severity seems most appropriate.

**[OpenCoreCH (sponsor) confirmed](https://github.com/code-423n4/2024-01-canto-findings/issues/12#issuecomment-1923534235)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | bin2chen, xuwinnie |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-canto
- **GitHub**: https://github.com/code-423n4/2024-01-canto-findings/issues/12
- **Contest**: https://code4rena.com/reports/2024-01-canto

### Keywords for Search

`Precision Loss, Rounding`

