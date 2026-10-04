---
# Core Classification
protocol: Bitcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46344
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2ce1f8e6-2000-4b3f-a131-58931e0c445e
source_link: https://cdn.cantina.xyz/reports/cantina_bitcorn_november2024.pdf
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
finders_count: 2
finders:
  - Denis Miličević
  - Sujith Somraaj
---

## Vulnerability Title

Inconsistent native fee validation leading to transaction failures 

### Overview


The report is about a bug found in the WrappedBitcornNativeOFTAdapter.sol contract. The contract has contradictory validation logic for native fees in its send and _payNative functions, causing unnecessary transaction failures. This bug can also result in users overpaying fees and having their transactions fail. The recommendation is to remove the redundant validation in the _lzSend function or modify the send function to have consistent validation. The bug has been fixed in the Bitcorn commit 69d1ec6c and verified in Cantina Managed.

### Original Finding Content

## WrappedBitcornNativeOFTAdapter.sol Contract Issue

## Context
(No context files were provided by the reviewer)

## Description
The `WrappedBitcornNativeOFTAdapter.sol` contract contains contradictory native fee validation logic between its `send` and `_payNative` functions, causing unnecessary transaction failures.

- In `_payNative`:
  ```solidity
  if (msg.value < _nativeFee) revert NotEnoughNative(msg.value);
  ```
  
- In `send`:
  ```solidity
  if (msg.value != feeWithExtraAmount.nativeFee) {
      revert NotEnoughNative(msg.value);
  }
  ```
  
Since the refund address is explicitly forwarded to the LayerZero endpoint, any excessive gas fees will be refunded automatically.

## Proof of Concept
The following proof of concept demonstrates transaction reverts, though the user overpays:
```solidity
function test_e2e() external {
    vm.startPrank(deployer);
    vm.selectFork(forkId[ARBI]);
    deal(deployer, 100 ether);
    wrapper.deposit{value: 1 ether}();
    SendParam memory sendParam = SendParam(30101, bytes32(uint256(uint160(deployer))), 1 ether, 0,
    OptionsBuilder.encodeLegacyOptionsType1(200_000), bytes(""), bytes(""));
    MessagingFee memory lzFee = MessagingFee(1 ether, 0);
    wrapper.send{value: 2 ether}(sendParam, lzFee, address(deployer));
}
```

## Impact
- Valid transactions revert unnecessarily in certain paths.
- Users overpaying fees have transactions fail in certain paths.

## Recommendation
The gas fee validation is done inside the `_lzSend` function; hence, remove this redundant validation to ensure consistency and avoid unexpected behavior. If you still think reverting earlier in the stack is relevant, then modify the `send` function to use consistent validation:

- In `send`:
  ```solidity
  if (msg.value < feeWithExtraAmount.nativeFee) {
      revert NotEnoughNative(msg.value);
  }
  ```

## Bitcorn
Fixed in commit `69d1ec6c`.

## Cantina Managed
Verified fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bitcorn |
| Report Date | N/A |
| Finders | Denis Miličević, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_bitcorn_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2ce1f8e6-2000-4b3f-a131-58931e0c445e

### Keywords for Search

`vulnerability`

