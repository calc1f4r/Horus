---
# Core Classification
protocol: Dopex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29479
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-dopex
source_link: https://code4rena.com/reports/2023-08-dopex
github_link: https://github.com/code-423n4/2023-08-dopex-findings/issues/6

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
finders_count: 6
finders:
  - ItsNio
  - HHK
  - Tendency
  - LowK
  - ak1
---

## Vulnerability Title

[M-17] The RdpxV2Core contract allows anyone to call redeem tokens even if the contract is paused

### Overview


A bug was discovered in the RdpxV3core smart contract that allows anyone to use the `redeem` function even when the contract is paused. This is an issue as the contract should be locked when paused. The bug is due to the lack of a `whenNotPaused()` check in the `redeem()` function. 

To reproduce the vulnerability, a test called `testRedeem()` was modified in `/test/rdpxV2-core/Unit.t.sol`. After running the test, the results showed that the vulnerability was present.

The recommended mitigation step for this bug is to add the line `_whenNotPaused();` into the `redeem()` function. This was confirmed by psytama (Dopex).

### Original Finding Content


When the admin pauses the contract RdpxV3core locks anyone to use this contract such as a bond, bondWithDelegate, and withdraw. But a function redeem is still available to use.
Any situations that occur like a hack accident or system are under maintenance then anyway, your smart contract is running to continue to get unexpected.

### Proof of Concept

The code below does not call a function `whenNotPause()` to check whether this contract is paused or not.

    function redeem(
        uint256 id,
        address to
      ) external returns (uint256 receiptTokenAmount) {
        // Validate bond ID
        _validate(bonds[id].timestamp > 0, 6);
        // Validate if bond has matured
        _validate(block.timestamp > bonds[id].maturity, 7);

        _validate(
          msg.sender == RdpxV2Bond(addresses.receiptTokenBonds).ownerOf(id),
          9
        );

        // Burn the bond token
        // Note requires an approval of the bond token to this contract
        RdpxV2Bond(addresses.receiptTokenBonds).burn(id);

        // transfer receipt tokens to user
        receiptTokenAmount = bonds[id].amount;
        IERC20WithBurn(addresses.rdpxV2ReceiptToken).safeTransfer(
          to,
          receiptTokenAmount
        );

        emit LogRedeem(to, receiptTokenAmount);
      }

To reproduce this vulnerability, let's modify a test called `testRedeem()` in a `/test/rdpxV2-core/Unit.t.sol`. After running the test, you will get everything passed. So it is proof of vulnerable

    function testRedeem() public {
        rdpxV2Core.bond(1 * 1e18, 0, address(this));
        // ...
        rdpxV2Core.pause(); // <- add this line to test

        // test redeem after expiry
        rdpxV2Bond.approve(address(rdpxV2Core), 0);
        rdpxV2Core.redeem(0, address(1));
        assertEq(rdpxV2Bond.balanceOf(address(this)), 0);
        assertEq(rdpxV2ReceiptToken.balanceOf(address(1)), 25 * 1e16);
        // ...
    }

### Recommended Mitigation Steps

Adding the line `_whenNotPaused();` into the function `redeem()`.

**[psytama (Dopex) confirmed](https://github.com/code-423n4/2023-08-dopex-findings/issues/6#issuecomment-1734116507)**

*** 



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Dopex |
| Report Date | N/A |
| Finders | ItsNio, HHK, Tendency, LowK, ak1, Inspecktor |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-dopex
- **GitHub**: https://github.com/code-423n4/2023-08-dopex-findings/issues/6
- **Contest**: https://code4rena.com/reports/2023-08-dopex

### Keywords for Search

`vulnerability`

