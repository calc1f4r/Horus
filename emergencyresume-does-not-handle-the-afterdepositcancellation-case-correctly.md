---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27640
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
  - 0xCiphky
---

## Vulnerability Title

emergencyResume does not handle the afterDepositCancellation case correctly

### Overview


This bug report concerns the **`emergencyResume`** function, which is intended to recover the vault's liquidity following an **`emergencyPause`**. It operates under the assumption of a successful deposit call, but if the deposit call is cancelled by GMX, the **`emergencyResume`** function does not account for this scenario, potentially locking funds. 

The **`emergencyResume`** function sets the vault's status to "Resume" and deposits all LP tokens back into the pool. When the deposit fails, the callback contract's **`afterDepositCancellation`** is expected to revert, which does not impact the continuation of the GMX execution. After the cancellation occurs, the vault status is "Resume" and the liquidity is not re-added to the pool. This means that another attempt to execute **`emergencyResume`** will fail because the vault status is not "Paused". An attempt to revert to "Paused" status via **`emergencyPause`** could fail in GMXManager.removeLiquidity, as there are no tokens to send back to the GMX pool, leading to a potential fund lock within the contract.

The impact of this bug is that funds may be irretrievably locked within the contract. The bug was identified using manual analysis, and the recommendation is to handle the afterDepositCancellation case correctly by allowing emergencyResume to be called again.

### Original Finding Content

## Summary

The **`emergencyResume`** function is intended to recover the vault's liquidity following an **`emergencyPause`**. It operates under the assumption of a successful deposit call. However, if the deposit call is cancelled by GMX, the **`emergencyResume`** function does not account for this scenario, potentially locking funds.

## Vulnerability Details

When **`emergencyResume`** is invoked, it sets the vault's status to "Resume" and deposits all LP tokens back into the pool. The function is designed to execute when the vault status is "Paused" and can be triggered by an approved keeper.

```solidity
function emergencyResume(
    GMXTypes.Store storage self
  ) external {
    GMXChecks.beforeEmergencyResumeChecks(self);

    self.status = GMXTypes.Status.Resume;

    self.refundee = payable(msg.sender);

    GMXTypes.AddLiquidityParams memory _alp;

    _alp.tokenAAmt = self.tokenA.balanceOf(address(this));
    _alp.tokenBAmt = self.tokenB.balanceOf(address(this));
    _alp.executionFee = msg.value;

    GMXManager.addLiquidity(
      self,
      _alp
    );
  }
```

Should the deposit fail, the callback contract's **`afterDepositCancellation`** is expected to revert, which does not impact the continuation of the GMX execution. After the cancellation occurs, the vault status is "Resume", and the liquidity is not re-added to the pool.

```solidity
function afterDepositCancellation(
    bytes32 depositKey,
    IDeposit.Props memory /* depositProps */,
    IEvent.Props memory /* eventData */
  ) external onlyController {
    GMXTypes.Store memory _store = vault.store();

    if (_store.status == GMXTypes.Status.Deposit) {
      if (_store.depositCache.depositKey == depositKey)
        vault.processDepositCancellation();
    } else if (_store.status == GMXTypes.Status.Rebalance_Add) {
      if (_store.rebalanceCache.depositKey == depositKey)
        vault.processRebalanceAddCancellation();
    } else if (_store.status == GMXTypes.Status.Compound) {
      if (_store.compoundCache.depositKey == depositKey)
        vault.processCompoundCancellation();
    } else {
      revert Errors.DepositCancellationCallback();
    }
  }
```

Given this, another attempt to execute **`emergencyResume`** will fail because the vault status is not "Paused".

```solidity
function beforeEmergencyResumeChecks (
    GMXTypes.Store storage self
  ) external view {
    if (self.status != GMXTypes.Status.Paused)
      revert Errors.NotAllowedInCurrentVaultStatus();
  }
```

In this state, an attempt to revert to "Paused" status via **`emergencyPause`** could fail in GMXManager.removeLiquidity, as there are no tokens to send back to the GMX pool, leading to a potential fund lock within the contract.

## Impact

The current implementation may result in funds being irretrievably locked within the contract. 

## Tools Used

Manual Analysis

## Recommendations

To address this issue, handle the afterDepositCancellation case correctly by allowing emergencyResume to be called again.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | 0xCiphky |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

