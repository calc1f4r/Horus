---
# Core Classification
protocol: Liquity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18023
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Alexander Remie
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Reentrancy could lead to incorrect order of emitted events

### Overview

See description below for full details.

### Original Finding Content

## Type: Data Validation
## Target: Throughout

### Difficulty: High

### Description
The order of operations in the `_moveTokensAndETHfromAdjustment` function in the BorrowOperations contract may allow an attacker to cause events to be emitted out of order.

When executing operations on a trove, the internal `_adjustTrove` function calls `_moveTokensAndETHfromAdjustment`.

```solidity
_moveTokensAndETHfromAdjustment(msg.sender, L.collChange, L.isCollIncrease, _debtChange, _isDebtIncrease, L.rawDebtChange);
emit TroveUpdated(_borrower, L.newDebt, L.newColl, L.stake, BorrowerOperation.adjustTrove);
emit LUSDBorrowingFeePaid(msg.sender, L.LUSDFee);
```

_Figure 6.1_: A snippet of the `BorrowerOperations._adjustTrove` function.

If LUSD is to be burned, resulting in collateralized ETH being returned, then this function invokes `sendETH` in the ActivePool contract.

```solidity
function sendETH(address _account, uint _amount) external override {
    _requireCallerIsBOorTroveMorSP();
    ETH = ETH.sub(_amount);
    emit EtherSent(_account, _amount);
    (bool success, ) = _account.call{value: _amount}("");
    require(success, "ActivePool: sending ETH failed");
}
```

_Figure 6.2_: The `ActivePool.sendETH` function body.

This call will actually perform the transfer of ETH to the borrower. As this function uses `call.value` without a specified gas amount, all of the remaining gas is forwarded to this call.

In the event that the borrower is a contract, this could trigger a callback into `BorrowerOperations`, executing the `_adjustTrove` flow above again. As the `_moveTokensAndETHfromAdjustment` call is the final operation in the function, the state of the system on-chain cannot be manipulated. However, there are events that are emitted after this call. In the event of a reentrant call, these events would be emitted in the incorrect order.

### Exploit Scenario
Alice operates a trove through a smart contract. She invokes a change in her trove that causes the Liquity system to return ETH to her smart contract. This triggers the contract’s fallback function, which calls back into the Liquity system and triggers another similar operation. The event for the second operation is emitted first, followed by the event for the first operation. Any off-chain monitoring tools may now have an inconsistent view of on-chain state.

### Recommendation
Short term, apply the checks-effects-interactions pattern and move the event emissions above the call to `_moveTokensAndETHfromAdjustment` to avoid the potential reentrancy.

Long term, use Slither to detect potential reentrant function calls.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Liquity |
| Report Date | N/A |
| Finders | Gustavo Grieco, Alexander Remie, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf

### Keywords for Search

`vulnerability`

