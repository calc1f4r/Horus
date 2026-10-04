---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: approve_max

# Attack Vector Details
attack_type: approve_max
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 487
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/29

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - approve_max

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - shw
  - hickuphh3
  - jonah1005
  - 0xRajeev  cmichel
---

## Vulnerability Title

[H-02] Pool.sol & Synth.sol: Failing Max Value Allowance

### Overview


This bug report discusses a vulnerability in the `_approve` function of a contract. If the allowance passed in is `type(uint256).max`, nothing happens, meaning the allowance will remain at the previous value. This causes issues for contract integrations, such as DEXes that hardcode this value to set the maximum allowance initially, as the result is zero allowance being given instead. Furthermore, the comment `// No need to re-approve if already max` is misleading, as the max allowance attainable is `type(uint256).max - 1` and re-approval does happen in this case. This also affects the `approveAndCall` implementation since it uses `type(uint256).max` as the allowance amount, but the resulting allowance set is zero. The recommended mitigation step is to remove the condition from the `_approve` function.

### Original Finding Content

## Handle

hickuphh3


## Vulnerability details

### Impact

In the `_approve` function, if the allowance passed in is `type(uint256).max`, nothing happens (ie. allowance will still remain at previous value). Contract integrations (DEXes for example) tend to hardcode this value to set maximum allowance initially, but this will result in zero allowance given instead.

This also makes the comment `// No need to re-approve if already max` misleading, because the max allowance attainable is `type(uint256).max - 1`, and re-approval does happen in this case.

This affects the `approveAndCall` implementation since it uses `type(uint256).max` as the allowance amount, but the resulting allowance set is zero.

### Recommended Mitigation Steps

Keep it simple, remove the condition.

```jsx
function _approve(address owner, address spender, uint256 amount) internal virtual {
        require(owner != address(0), "!owner");
        require(spender != address(0), "!spender");
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | shw, hickuphh3, jonah1005, 0xRajeev  cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/29
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`Approve Max`

