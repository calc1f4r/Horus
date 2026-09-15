---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1637
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/8

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
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - danb
  - hickuphh3
  - Dravee
  - Ruhum
  - throttle
---

## Vulnerability Title

[M-09] Improper Upper Bound Definition on the Fee

### Overview


A bug report has been filed regarding a vulnerability in the TokenManager.sol contract. This vulnerability can cause reversions in several critical functions or the LP user to lose all funds when paying the fee. The bug is due to the lack of upper or lower bounds on the equilibriumFee and maxFee. To exploit this vulnerability, the owner must navigate to the TokenManager.sol contract and identify the fee amount. Upon inspection, it can be seen that there is no upper bound defined. To mitigate this vulnerability, it is recommended to define upper and lower bounds on the equilibriumFee and maxFee. Code review was used as a tool in this bug report.

### Original Finding Content

_Submitted by defsec, also found by catchup, danb, Dravee, gzeon, hickuphh3, hubble, peritoflores, Ruhum, and throttle_

The **equilibriumFee** and **maxFee** does not have any upper or lower bounds. Values that are too large will lead to reversions in several critical functions or the LP user will lost all funds when paying the fee.

### Proof of Concept

1.  Navigate to the following contract.

[TokenManager.sol#L52](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/token/TokenManager.sol#L52)<br>

2.  Owner can identify fee amount. That directly affect to LP management. [LiquidityPool.sol#L352](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityPool.sol#L352)

3.  Here you can see there is no upper bound has been defined.

```
    function changeFee(
        address tokenAddress,
        uint256 _equilibriumFee,
        uint256 _maxFee
    ) external override onlyOwner whenNotPaused {
        require(_equilibriumFee != 0, "Equilibrium Fee cannot be 0");
        require(_maxFee != 0, "Max Fee cannot be 0");
        tokensInfo[tokenAddress].equilibriumFee = _equilibriumFee;
        tokensInfo[tokenAddress].maxFee = _maxFee;
        emit FeeChanged(tokenAddress, tokensInfo[tokenAddress].equilibriumFee, tokensInfo[tokenAddress].maxFee);
    }

```

### Recommended Mitigation Steps

Consider defining upper and lower bounds on the **equilibriumFee** and **maxFee**.

**[ankurdubey521 (Biconomy) confirmed and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/8):**
 > [HP-25: C4 Audit Fixes, Dynamic Fee Changes bcnmy/hyphen-contract#42](https://github.com/bcnmy/hyphen-contract/pull/42)

**[pauliax (judge) commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/8#issuecomment-1114023886):**
 > Valid concern. I am grouping all the issues related to the validation of fee variables together and making this the primary one as it contains the most comprehensive description.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | danb, hickuphh3, Dravee, Ruhum, throttle, gzeon, peritoflores, catchup, hubble, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/8
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`vulnerability`

