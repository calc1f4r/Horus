---
# Core Classification
protocol: Dharma Labs Smart Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16801
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
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
  - eric.rafaloﬀ@trailofbits.com Dominik Czarnota
  - Eric Rafaloﬀ
---

## Vulnerability Title

Missing validation in DharmaSmartWalletImplementationV2

### Overview

See description below for full details.

### Original Finding Content

## Data Validation

**Target:** DharmaSmartWalletImplementationV2.sol

**Difficulty:** Low

## Description

Within the DharmaSmartWalletImplementationV2 contract, the `withdrawDai` and `withdrawUSDC` functions do not perform adequate validation of their amount and recipient parameters (Figures 12.1 and 12.2).

### Function: withdrawDai

```solidity
function withdrawDai(
    uint256 amount,
    address recipient,
    uint256 minimumActionGas,
    bytes calldata userSignature,
    bytes calldata dharmaSignature
) external returns (bool ok) {
    // Ensure caller and/or supplied signatures are valid and increment nonce.
    _validateActionAndIncrementNonce(
        ActionType.DAIWithdrawal,
        abi.encode(amount, recipient),
        minimumActionGas,
        userSignature,
        dharmaSignature
    );
    // Set the self-call context so we can call _withdrawDaiAtomic.
    _selfCallContext = this.withdrawDai.selector;
    // Make the atomic self-call - if redeemUnderlying fails on cDAI, it will
    // succeed but nothing will happen except firing an ExternalError event. If
    // the second part of the self-call (the Dai transfer) fails, it will revert
    // and roll back the first part of the call, and we'll fire an ExternalError
    // event after returning from the failed call.
    bytes memory returnData;
    (ok, returnData) = address(this).call(abi.encodeWithSelector(
        this._withdrawDaiAtomic.selector, amount, recipient
    ));
    // If the atomic call failed, emit an event signifying a transfer failure.
    if (!ok) {
        emit ExternalError(address(_DAI), "DAI contract reverted on transfer.");
    } else {
        // Set ok to false if the call succeeded but the withdrawal failed.
        ok = abi.decode(returnData, (bool));
    }
}
```

Figure 12.1: The withdrawDai function.

### Function: withdrawUSDC

```solidity
function withdrawUSDC(
    uint256 amount,
    address recipient,
    uint256 minimumActionGas,
    bytes calldata userSignature,
    bytes calldata dharmaSignature
) external returns (bool ok) {
    // Ensure caller and/or supplied signatures are valid and increment nonce.
    _validateActionAndIncrementNonce(
        ActionType.USDCWithdrawal,
        abi.encode(amount, recipient),
        minimumActionGas,
        userSignature,
        dharmaSignature
    );
    // Set the self-call context so we can call _withdrawUSDCAtomic.
    _selfCallContext = this.withdrawUSDC.selector;
    // Make the atomic self-call - if redeemUnderlying fails on cUSDC, it will
    // succeed but nothing will happen except firing an ExternalError event. If
    // the second part of the self-call (USDC transfer) fails, it will revert
    // and roll back the first part of the call, and we'll fire an ExternalError
    // event after returning from the failed call.
    bytes memory returnData;
    (ok, returnData) = address(this).call(abi.encodeWithSelector(
        this._withdrawUSDCAtomic.selector, amount, recipient
    ));
    if (!ok) {
        // Find out why USDC transfer reverted (doesn't give revert reasons).
        _diagnoseAndEmitUSDCSpecificError(_USDC.transfer.selector);
    } else {
        // Ensure that ok == false in the event the withdrawal failed.
        ok = abi.decode(returnData, (bool));
    }
}
```

Figure 12.2: The withdrawUSDC function.

## Exploit Scenario

Due to human error or a bug in a script, either function is incorrectly called with their amount and/or recipient parameters set to zero.

## Recommendation

**Short term:** Perform validation of the amount and recipient parameters by checking if either value is equal to zero.

**Long term:** Add more unit testing to check that invalid inputs are rejected from both functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Dharma Labs Smart Wallet |
| Report Date | N/A |
| Finders | eric.rafaloﬀ@trailofbits.com Dominik Czarnota, Eric Rafaloﬀ |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/dharma-smartwallet.pdf

### Keywords for Search

`vulnerability`

