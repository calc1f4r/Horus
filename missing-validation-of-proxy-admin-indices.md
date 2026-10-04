---
# Core Classification
protocol: NFTX Protocol v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18157
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jaime Iglesias
  - Evan Sultanik
---

## Vulnerability Title

Missing validation of proxy admin indices

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

**Difficulty:** High

**Type:** Data Exposure

## Description

Multiple functions of the `ProxyController` contract take an index as an input. The index determines which proxy (managed by the controller) is being targeted. However, the index is never validated, which means that the function will be executed even if the index is out of bounds with respect to the number of proxies managed by the contract (in this case, five).

```solidity
function changeProxyAdmin(uint256 index, address newAdmin) public onlyOwner {
    if (index == 0) {
        vaultFactoryProxy.changeAdmin(newAdmin);
    } else if (index == 1) {
        eligManagerProxy.changeAdmin(newAdmin);
    } else if (index == 2) {
        stakingProviderProxy.changeAdmin(newAdmin);
    } else if (index == 3) {
        stakingProxy.changeAdmin(newAdmin);
    } else if (index == 4) {
        feeDistribProxy.changeAdmin(newAdmin);
    }
    emit ProxyAdminChanged(index, newAdmin);
}
```

*Figure 2.1: The `changeProxyAdmin` function in `ProxyController.sol`:79-95*

In the `changeProxyAdmin` function, a `ProxyAdminChanged` event is emitted even if the supplied index is out of bounds (figure 2.1). Other `ProxyController` functions return the zero address if the index is out of bounds. For example, `getAdmin()` should return the address of the targeted proxy’s admin. If `getAdmin()` returns the zero address, the caller cannot know whether they supplied the wrong index or whether the targeted proxy simply has no admin.

```solidity
function getAdmin(uint256 index) public view returns (address admin) {
    if (index == 0) {
        return vaultFactoryProxy.admin();
    } else if (index == 1) {
        return eligManagerProxy.admin();
    } else if (index == 2) {
        return stakingProviderProxy.admin();
    } else if (index == 3) {
        return stakingProxy.admin();
    } else if (index == 4) {
        return feeDistribProxy.admin();
    }
}
```

*Figure 2.2: The `getAdmin` function in `ProxyController.sol`:38-50*

## Exploit Scenario

A contract relying on the `ProxyController` contract calls one of the view functions, like `getAdmin()`, with the wrong index. The function is executed normally and implicitly returns zero, leading to unexpected behavior.

## Recommendations

**Short term:** Document this behavior so that clients are aware of it and are able to include safeguards to prevent unanticipated behavior.

**Long term:** Consider adding an index check to the affected functions so that they revert if they receive an out-of-bounds index.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | NFTX Protocol v2 |
| Report Date | N/A |
| Finders | Jaime Iglesias, Evan Sultanik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/NFTX.pdf

### Keywords for Search

`vulnerability`

