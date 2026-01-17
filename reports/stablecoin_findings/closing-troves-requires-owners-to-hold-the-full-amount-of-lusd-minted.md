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
solodit_id: 18026
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

Closing troves requires owners to hold the full amount of LUSD minted

### Overview

See description below for full details.

### Original Finding Content

## Auditing and Logging

**Type:** Auditing and Logging  
**Target:** LockupContractFactory.sol, OneYearLockupContract.sol, CustomDurationLockupContract.sol  

**Difficulty:** Low  

## Description  

Users should hold the complete amount of LUSD minted before closing their trove; otherwise, the trove closing operation will fail. The Liquity protocol allows any user to deposit collateral and open troves in order to mint LUSD tokens:

```solidity
function openTrove(uint _LUSDAmount, address _hint) external payable override {
    uint price = priceFeed.getPrice();
    _requireTroveisNotActive(msg.sender);
    …
}
```
*Figure 9.1: Header of the `openTrove` function in `BorrowOperations.sol`.*

If any user wants to close their trove, they can use the `closeTrove` function:

```solidity
function closeTrove() external override {
    _requireTroveisActive(msg.sender);
    _requireNotInRecoveryMode();
    troveManager.applyPendingRewards(msg.sender);
    uint coll = troveManager.getTroveColl(msg.sender);
    uint debt = troveManager.getTroveDebt(msg.sender);
    troveManager.removeStake(msg.sender);
    troveManager.closeTrove(msg.sender);
    // Burn the debt from the user's balance, and send the collateral back to the user
    _repayLUSD(msg.sender, debt.sub(LUSD_GAS_COMPENSATION));
    activePool.sendETH(msg.sender, coll);
    // Refund gas compensation
    _repayLUSD(GAS_POOL_ADDRESS, LUSD_GAS_COMPENSATION);
    emit TroveUpdated(msg.sender, 0, 0, 0, BorrowerOperation.closeTrove);
}
```
*Figure 9.2: `closeTrove` in `BorrowOperations.sol`.*

This operation requires that the user account holds the corresponding amount of LUSD token minted. According to the code, these LUSD will be burned to remove the trove debt. However, the fact that the user should hold enough LUSD is not clearly documented or tested anywhere in the codebase. Also, it was unclear if the LUSD provided to the stability pool can be used directly to repay the debt.

```
assertion in closeTrove_should_not_revert: failed!💥
```

### Call sequence:
- `openTrove_should_not_revert(1)` Value: `0x10b66c7775da5e4`
- `provideToSP_should_not_revert()`
- `closeTrove_should_not_revert()`

*Figure 9.3: Echidna report of this issue.*

## Exploit Scenario  

Alice creates a new trove. Then she calls `provideToSP` with any positive amount of tokens. Later, she wants to close her trove, but the call fails. So she is unable to close her trove.

## Recommendation  

- **Short term:** Properly document and test this corner case and add a suitable revert message.  
- **Long term:** Make sure every system property is carefully specified and use Echidna or Manticore to test it.

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

