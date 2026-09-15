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
solodit_id: 51483
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

Lack of input validation for amount and fee values

### Overview

See description below for full details.

### Original Finding Content

##### Description

Both `CeFiSmartTransfer` and `DeFiSmartTransfer` smart contracts allow users to transfer a specific `amount` of assets to a `receiver` and a `fee` amount to a `feeReceiver`.

Nevertheless, these contracts lack input validation for the `amount` and `fee` parameters. Such oversight can result in the submission of transactions with invalid amounts, such as an amount set to `0`, or a `fee` being greater than the `amount` to transfer, which would revert the transactions.

The affected functions are:

* CeFiSmartTransfer: `prepareNativeTransfer()`, `executeErc20Transfer()` and `receive()`.
* DeFiSmartTransfer: `executeErc20Transfer()` and `executeNativeTransfer()`.

Additionally, there is no threshold for minimum and/or maximum amounts, which can allow malicious actors to congest the network with `0` amounts of dust transactions, particularly via `DeFiSmartTransfer::executeErc20Transfer(),` given that any user could initiate any number of transactions with `msg.value = 0`.

##### Proof of Concept

```
function testReceiveNativeTransferFailsWithFeeIsHigherThanAmount(
    address ethSender,
    string memory _id,
    uint256 _amount,
    uint256 _fee,
    address payable _feeReceiver,
    address payable _receiver
  ) public {

    vm.assume(_feeReceiver != address(ceFiSmartTransfer));
    vm.assume(_receiver != address(ceFiSmartTransfer));
    vm.assume(_amount != 0);
    vm.assume(_amount != type(uint256).max);
    _fee = bound(_fee, _amount + 1, type(uint256).max);
    _notFoundryReservedAddress(_receiver);
    _notFoundryReservedAddress(_feeReceiver);

    assert(_fee > _amount);

    testPrepareNativeTransfer(_id, _amount, _fee, _feeReceiver, _receiver);

    hoax(ethSender, _fee);
    vm.expectRevert();
    (bool ok, ) = address(ceFiSmartTransfer).call{value: _amount}("");
    ok;
}

function testPrepareNativeTransfer(
    string memory _id,
    uint256 _amount,
    uint256 _fee,
    address payable _feeReceiver,
    address payable _receiver
  ) public {
    vm.startPrank(operator1);
    assertEq(uint8(ceFiSmartTransfer.nativeTransferLock()), uint8(CeFi.Lock.Unlocked));

    CeFi.NativeTransfer memory _nativeTransfer = CeFi.NativeTransfer({
      id: _id,
      amount: _amount,
      fee: _fee,
      feeReceiver: payable(_feeReceiver),
      receiver: payable(_receiver)
    });

    ceFiSmartTransfer.prepareNativeTransfer(_nativeTransfer);

    (string memory id_, uint amount_, uint fee_, address feeReceiver_, address receiver_) = ceFiSmartTransfer.nativeTransfer();

    assertEq(_id, id_);
    assertEq(_amount, amount_);
    assertEq(_fee, fee_);
    assertEq(_feeReceiver, feeReceiver_);
    assertEq(_receiver, receiver_);

    assertEq(uint8(ceFiSmartTransfer.nativeTransferLock()), uint8(CeFi.Lock.Locked));

    vm.stopPrank();
}
```

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:L/I:N/D:N/Y:N (2.5)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:L/I:N/D:N/Y:N)

##### Recommendation

Add checks to ensure that the `fee` is lower than the amount to `transfer`, and that the `amount` to transfer is greater than `0`.

Also, consider disallowing transactions below a certain threshold to maintain efficiency and prevent denial of service through dust spamming.

Remediation Plan
----------------

**SOLVED:** The **Mesh Connect team** solved this finding in commits `a790ac9` and `cea7f6f` by following the mentioned recommendations.

##### Remediation Hash

<https://github.com/FrontFin/smart-contracts/commit/cea7f6f80a3fec5aee972a9cfe37449287f75776>

##### References

CeFiSmartTransfer.sol#L57-L107

DeFiSmartTransfer.sol#L26-L66

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

