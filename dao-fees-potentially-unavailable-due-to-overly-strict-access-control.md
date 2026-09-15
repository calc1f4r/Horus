---
# Core Classification
protocol: CLOBER
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7264
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - access_control

protocol_categories:
  - dexes
  - bridge
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Desmond Ho
  - Grmpyninja
  - Christoph Michel
  - Throttle
  - Taek Lee
---

## Vulnerability Title

DAO fees potentially unavailable due to overly strict access control

### Overview


This bug report is about the collectFees function in the OrderBook.sol code. This function was guarded by an inline access control require statement condition which only allowed the host of the market to invoke it, effectively delivering all collected fees, including the part of the fees belonging to the DAO. This access control was too strict and could lead to funds being locked permanently in the worst case scenario. As the host is a single point of failure, it was recommended to remove the access control from the collectFees function so that anyone could trigger the function and deliver collected fees at any time. This bug was fixed in PR 315, and authorization was modified so that everyone can trigger the function.

### Original Finding Content

## Audit Report

## Severity: Medium Risk

### Context
OrderBook.sol#L790

### Description
The `collectFees` function is guarded by an inline access control require statement condition which prevents anyone, except a host, from invoking the function. Only the host of the market is authorized to invoke, effectively delivering all collected fees, including the part of the fees belonging to the DAO.

```solidity
function collectFees() external nonReentrant {
    require(msg.sender == _host(), Errors.ACCESS); // @audit only host authorized
    if (_baseFeeBalance > 1) {
        _collectFees(_baseToken, _baseFeeBalance - 1);
        _baseFeeBalance = 1;
    }
    if (_quoteFeeBalance > 1) {
        _collectFees(_quoteToken, _quoteFeeBalance - 1);
        _quoteFeeBalance = 1;
    }
}
```

This access control is too strict and can lead to funds being locked permanently in the worst-case scenario. As the host is a single point of failure, if access to the wallet is lost or is incorrectly transferred, the fees for both the host and the DAO will be locked.

### Recommendation
It is recommended to remove the access control from the `collectFees` function, as collected fees are transferred to fixed addresses being the host and the treasury. In such a setup, anyone should be able to invoke the function and trigger collected fees delivery at any time, and it should not be limited only to the host of the market.

### Clober
Fixed in PR 315.

### Spearbit
Verified. Authorization modified. Everyone can trigger the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Spearbit |
| Protocol | CLOBER |
| Report Date | N/A |
| Finders | Desmond Ho, Grmpyninja, Christoph Michel, Throttle, Taek Lee |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf

### Keywords for Search

`Access Control`

