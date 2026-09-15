---
# Core Classification
protocol: Popcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22000
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-popcorn
source_link: https://code4rena.com/reports/2023-01-popcorn
github_link: https://github.com/code-423n4/2023-01-popcorn-findings/issues/780

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
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - ustas
  - rbserver
  - immeas
  - bin2chen
  - yellowBirdy
---

## Vulnerability Title

[M-03] `Vault::takeFees` can be front run to minimize `accruedPerformanceFee`

### Overview


A bug has been identified in the `performanceFee` of the vault, which is a fee on the profits of the vault. This fee can be collected by the `feeRecipient` or any user at any point. The bug is that the `highWaterMark` which records a historical share value is written on interactions with the vault such as `deposit`, `mint`, `withdraw`. This means that a malicious user can front run the fee collection with any of these calls, setting the `highWaterMark` to the current share value and removing the performance fee. A proof of concept test has been written in `Vault.t.sol` and RedVeil (Popcorn) has acknowledged the bug. The recommended mitigation step is to take fees before adding or removing the new users shares and assets at every deposit, mint, redeem and withdraw.

### Original Finding Content


`performanceFee` is a fee on the profits of the vault. The `feeRecipient` (or any user) can collect these at any point.

They rely on the difference between the current share value and the `highWaterMark` that records a historical share value.

The issue is that this `highWaterMark` is written on interactions with the vault: `deposit`, `mint`, `withdraw`. Hence a user can front run the fee collection with any of these calls. That will set the `highWaterMark` to the current share value and remove the performance fee.

### Impact

A malicious user can maximize the yield and deny any performance fee by front running the fee collection with a call to either `deposit`, `mint` or `withdraw` with only dust amounts.

### Proof of Concept

PoC test in `Vault.t.sol`

```javascript
  function test__front_run_performance_fee() public {
   _setFees(0, 0, 0, 1e17); // 10% performance fee

    asset.mint(alice, 1e18);

    vm.startPrank(alice);
    asset.approve(address(vault), 1e18);
    vault.deposit(1e18);
    vm.stopPrank();

    asset.mint(address(adapter),1e18); // fake yield

    // performanceFee is 1e17 (10% of 1e18)
    console.log("performanceFee before",vault.accruedPerformanceFee());

    vm.prank(alice);
    vault.withdraw(1); // malicious user withdraws dust which triggers update of highWaterMark

    // performanceFee is 0
    console.log("performanceFee after",vault.accruedPerformanceFee());
  }
```

### Tools Used

VS Code, Forge

### Recommended Mitigation Steps

At every deposit, mint, redeem and withdraw, take fees before adding or removing the new users shares and assets.

 **[RedVeil (Popcorn) acknowledged](https://github.com/code-423n4/2023-01-popcorn-findings/issues/780)** 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Popcorn |
| Report Date | N/A |
| Finders | ustas, rbserver, immeas, bin2chen, yellowBirdy, KIntern\_NA, rvierdiiev, minhtrng |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-popcorn
- **GitHub**: https://github.com/code-423n4/2023-01-popcorn-findings/issues/780
- **Contest**: https://code4rena.com/reports/2023-01-popcorn

### Keywords for Search

`vulnerability`

