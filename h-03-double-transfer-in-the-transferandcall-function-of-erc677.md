---
# Core Classification
protocol: Behodler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1361
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-behodler-contest
source_link: https://code4rena.com/reports/2022-01-behodler
github_link: https://github.com/code-423n4/2022-01-behodler-findings/issues/302

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:

protocol_categories:
  - cross_chain
  - services
  - cdp
  - dexes
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - shw
  - wuwe1
  - danb
---

## Vulnerability Title

[H-03] Double transfer in the transferAndCall function of ERC677

### Overview


This bug report is about an incorrect implementation of the `transferAndCall` function in `ERC677`, a smart contract. The incorrect implementation causes the `_value` amount of tokens to be transferred twice instead of once when the function is called. The `Flan` contract inherits `ERC667`, so anyone calling the `transferAndCall` function on `Flan` is affected by this double-transfer bug. The recommended mitigation step is to remove `_transfer(msg.sender, _to, _value);` in the `transferAndCall` function.

### Original Finding Content

## Handle

shw


## Vulnerability details

## Impact

The implementation of the `transferAndCall` function in `ERC677` is incorrect. It transfers the `_value` amount of tokens twice instead of once. Since the `Flan` contract inherits `ERC667`, anyone calling the `transferAndCall` function on `Flan` is affected by this double-transfer bug.

## Proof of Concept

Below is the implementation of `transferAndCall`:

```
function transferAndCall(
    address _to,
    uint256 _value,
    bytes memory _data
) public returns (bool success) {
    super.transfer(_to, _value);
    _transfer(msg.sender, _to, _value);
    if (isContract(_to)) {
        contractFallback(_to, _value, _data);
    }
    return true;
}
```

We can see that `super.transfer(_to, _value);` and `_transfer(msg.sender, _to, _value);` are doing the same thing - transfering `_value` of tokens from `msg.sender` to `_to`.

Referenced code:
[ERC677/ERC677.sol#L28-L29](https://github.com/code-423n4/2022-01-behodler/blob/main/contracts/ERC677/ERC677.sol#L28-L29)

## Recommended Mitigation Steps

Remove `_transfer(msg.sender, _to, _value);` in the `transferAndCall` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Behodler |
| Report Date | N/A |
| Finders | cccz, shw, wuwe1, danb |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-behodler
- **GitHub**: https://github.com/code-423n4/2022-01-behodler-findings/issues/302
- **Contest**: https://code4rena.com/contests/2022-01-behodler-contest

### Keywords for Search

`vulnerability`

