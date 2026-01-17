---
# Core Classification
protocol: ES3D
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51484
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/mesh-connect/mesh-es3d
source_link: https://www.halborn.com/audits/mesh-connect/mesh-es3d
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Lack of input validation in native assets transfers function might lead to loss of funds

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `prepareNativeTransfer()` function from the `CeFiSmartTransfer` contract allows for operators to set the `NativeTransfer` struct, which contains all the crucial information to the native asset transfer that will be executed when the contract receives assets via the `receive()` method. Nevertheless, this function lacks input validation for the input parameters.

Similarly, the `executeNativeTransfer()` function from the `DeFiSmartTransfer` contract allows any address to transfer native tokens to a `receiver` and a `feeReceiver` but lacks input validation for these parameters.

Such oversight on both functions can result in a potential loss of funds if either the `receiver` or `feeReceiver` are inadvertently set to `address(0)`.

##### Proof of Concept

```
function testReceiveNativeTransferWhenFeeReceiverIsZeroAddress(
    address ethSender,
    string memory _id,
    uint256 _amount,
    uint256 _fee,
    address payable _receiver
  ) public {
    /* ------------------------------- preparation ------------------------------ */
    _notFoundryReservedAddress(_receiver);
    vm.assume(_receiver != address(0));
    vm.assume(_receiver != address(ceFiSmartTransfer));
    vm.assume(_amount != 0);
    _fee = bound(_fee, 0, _amount);

    /* -------------------------------- execution ------------------------------- */
    testPrepareNativeTransfer(_id, _amount, _fee, payable(address(0)), _receiver);
    hoax(ethSender, _amount);
    (bool ok, ) = (address(ceFiSmartTransfer)).call{value: _amount}("");
    assert(ok);
    assertEq((address(0)).balance, _fee);
}

function testReceiveNativeTransferWhenReceiverIsZeroAddress(
    address ethSender,
    string memory _id,
    uint256 _amount,
    uint256 _fee,
    address payable _feeReceiver
  ) public {
    /* ------------------------------- preparation ------------------------------ */
    _notFoundryReservedAddress(_feeReceiver);
    vm.assume(_feeReceiver != address(0));
    vm.assume(_feeReceiver != address(ceFiSmartTransfer));
    vm.assume(_amount != 0);
    _fee = bound(_fee, 0, _amount);

    /* -------------------------------- execution ------------------------------- */
    testPrepareNativeTransfer(_id, _amount, _fee, _feeReceiver, payable(address(0)));
    hoax(ethSender, _amount);
    (bool ok, ) = (address(ceFiSmartTransfer)).call{value: _amount}("");
    assert(ok);
    assertEq((address(0)).balance, _amount - _fee);
}

  function testExecuteNativeTransferToReceiverZeroAddress(
    address ethSender,
    string memory _id,
    uint256 _amount,
    uint256 _fee,
    address payable _feeReceiver
  ) public {
    /* ------------------------------- preparation ------------------------------ */
    vm.assume(_feeReceiver != address(deFiSmartTransfer));
    vm.assume(_feeReceiver != address(ethSender));
    vm.assume(_feeReceiver != address(0));
    vm.assume(ethSender != address(0));
    vm.assume(_amount != 0);
    _fee = bound(_fee, 0, _amount);
    _notFoundryReservedAddress(_feeReceiver);
    uint256 balanceReceiverBefore = address(0).balance;
    uint256 balanceFeeReceiverBefore = address(_feeReceiver).balance;
    uint256 amountForReceiver = _amount - _fee;

    deFi.Transfer memory _transfer = deFi.Transfer({
      id: _id,
      amount: _amount,
      fee: _fee,
      feeReceiver: _feeReceiver,
      receiver: payable(address(0)),
      payer: ethSender,
      token: address(0)
    });

    /* -------------------------------- execution ------------------------------- */
    hoax(ethSender, _amount);
    assertEq(ethSender.balance, _amount);
    deFiSmartTransfer.executeNativeTransfer{value: _amount}(_transfer);
    assertEq(ethSender.balance, 0);

    /* ------------------------------ verification ------------------------------ */
    uint256 balanceReceiverAfter = address(0).balance;
    uint256 balanceFeeReceiverAfter = address(_feeReceiver).balance;

    assertEq(balanceReceiverAfter, balanceReceiverBefore + amountForReceiver);
    assertEq(balanceFeeReceiverAfter, balanceFeeReceiverBefore + _fee);
  }

  function testExecuteNativeTransferToFeeReceiverZeroAddress(
    address ethSender,
    string memory _id,
    uint256 _amount,
    uint256 _fee,
    address payable _receiver
  ) public {
    /* ------------------------------- preparation ------------------------------ */
    vm.assume(_receiver != address(deFiSmartTransfer));
    vm.assume(_receiver != address(ethSender));
    vm.assume(_receiver != address(0));
    vm.assume(ethSender != address(0));
    vm.assume(_amount != 0);
    _fee = bound(_fee, 0, _amount);
    _notFoundryReservedAddress(_receiver);
    uint256 balanceReceiverBefore = address(_receiver).balance;
    uint256 balanceFeeReceiverBefore = address(0).balance;
    uint256 amountForReceiver = _amount - _fee;

    deFi.Transfer memory _transfer = deFi.Transfer({
      id: _id,
      amount: _amount,
      fee: _fee,
      feeReceiver: payable(address(0)),
      receiver: _receiver,
      payer: ethSender,
      token: address(0)
    });

    /* -------------------------------- execution ------------------------------- */
    hoax(ethSender, _amount);
    assertEq(ethSender.balance, _amount);
    deFiSmartTransfer.executeNativeTransfer{value: _amount}(_transfer);
    assertEq(ethSender.balance, 0);

    /* ------------------------------ verification ------------------------------ */
    uint256 balanceReceiverAfter = address(_receiver).balance;
    uint256 balanceFeeReceiverAfter = address(0).balance;

    assertEq(balanceReceiverAfter, balanceReceiverBefore + amountForReceiver);
    assertEq(balanceFeeReceiverAfter, balanceFeeReceiverBefore + _fee);
  }
```

##### BVSS

[AO:S/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:C/Y:N (2.0)](/bvss?q=AO:S/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:C/Y:N)

##### Recommendation

Add a check to ensure that the `receiver` and the `feeReceiver` are not `address(0)`.

Remediation Plan
----------------

**SOLVED:** The **Mesh Connect team** solved this finding in commits `76c823f` and `cea7f6f` by following the mentioned recommendation and adding a check to verify that the `receiver` and the `feeReceiver` are not `address(0)`.

##### Remediation Hash

<https://github.com/FrontFin/smart-contracts/commit/76c823fa3d6948294d3d923336b336af1e2454a8>

##### References

CeFiSmartTransfer.sol#L57-L70

DeFiSmartTransfer.sol#L26-L43

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | ES3D |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/mesh-connect/mesh-es3d
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/mesh-connect/mesh-es3d

### Keywords for Search

`vulnerability`

