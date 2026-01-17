---
# Core Classification
protocol: INIT Capital
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29595
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-initcapital
source_link: https://code4rena.com/reports/2023-12-initcapital
github_link: https://github.com/code-423n4/2023-12-initcapital-findings/issues/26

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

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - said
---

## Vulnerability Title

[M-04] `setPosMode` should not allow changing the mode when the new mode's `canRepay` status is disabled

### Overview


This bug report discusses an issue where positions using a certain mode cannot be repaid and liquidated. However, users are allowed to change their position's mode to one where this is not possible, which could be exploited to prevent liquidation. The report includes a proof of concept and recommended mitigation steps, which involve adding a check for the `canRepay` status when changing a position's mode. 

### Original Finding Content


In the scenario where the mode's `canRepay` status is set to false, positions using that mode cannot be repaid and liquidated. However, users are allowed to change their position's mode to one where the `canRepay` status is currently set to false. This could be exploited when a position owner observes that their position's health is approaching the liquidation threshold, allowing them to prevent liquidation.

### Proof of Concept

It can be observed that when `setPosMode` is called, it checks that `newModeStatus.canBorrow` and `currentModeStatus.canRepay` is set to true. However, it doesn't check the status of `newModeStatus.canRepay` flag.

<https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L203-L204>

<details>

```solidity
    function setPosMode(uint _posId, uint16 _mode)
        public
        virtual
        onlyAuthorized(_posId)
        ensurePositionHealth(_posId)
        nonReentrant
    {
        IConfig _config = IConfig(config);
        // get current collaterals in the position
        (address[] memory pools,, address[] memory wLps, uint[][] memory ids,) =
            IPosManager(POS_MANAGER).getPosCollInfo(_posId);
        uint16 currentMode = _getPosMode(_posId);
        ModeStatus memory currentModeStatus = _config.getModeStatus(currentMode);
        ModeStatus memory newModeStatus = _config.getModeStatus(_mode);
        if (pools.length != 0 || wLps.length != 0) {
            _require(newModeStatus.canCollateralize, Errors.COLLATERALIZE_PAUSED);
            _require(currentModeStatus.canDecollateralize, Errors.DECOLLATERALIZE_PAUSED);
        }
        // check that each position collateral belongs to the _mode
        for (uint i; i < pools.length; i = i.uinc()) {
            _require(_config.isAllowedForCollateral(_mode, pools[i]), Errors.INVALID_MODE);
        }
        for (uint i; i < wLps.length; i = i.uinc()) {
            for (uint j; j < ids[i].length; j = j.uinc()) {
                _require(_config.isAllowedForCollateral(_mode, IBaseWrapLp(wLps[i]).lp(ids[i][j])), Errors.INVALID_MODE);
            }
        }
        // get current debts in the position
        uint[] memory shares;
        (pools, shares) = IPosManager(POS_MANAGER).getPosBorrInfo(_posId);
        IRiskManager _riskManager = IRiskManager(riskManager);
        // check that each position debt belongs to the _mode
        for (uint i; i < pools.length; i = i.uinc()) {
            _require(_config.isAllowedForBorrow(_mode, pools[i]), Errors.INVALID_MODE);
            _require(newModeStatus.canBorrow, Errors.BORROW_PAUSED);
            _require(currentModeStatus.canRepay, Errors.REPAY_PAUSED);
            // update debt on current mode
            _riskManager.updateModeDebtShares(currentMode, pools[i], -shares[i].toInt256());
            // update debt on new mode
            _riskManager.updateModeDebtShares(_mode, pools[i], shares[i].toInt256());
        }
        // update position mode
        IPosManager(POS_MANAGER).updatePosMode(_posId, _mode);
        emit SetPositionMode(_posId, _mode);
    }
```
</details>

As mentioned before, if users see his position's health status is about to reach liquidation threshold and change the mode, this will allow users to prevent their positions from getting liquidated, as both `liquidate` and `liquidateWLp` will check the `canRepay` flag and revert if it's not allowed.

<https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L282-L314><br>
<https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L317-L353><br>
<https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L587-L599>

```solidity
    /// @dev liquidation internal logic
    function _liquidateInternal(uint _posId, address _poolToRepay, uint _repayShares)
        internal
        returns (LiquidateLocalVars memory vars)
    {
        vars.config = IConfig(config);
        vars.mode = _getPosMode(_posId);

        // check position must be unhealthy
        vars.health_e18 = getPosHealthCurrent_e18(_posId);
        _require(vars.health_e18 < ONE_E18, Errors.POSITION_HEALTHY);

>>>     (vars.repayToken, vars.repayAmt) = _repay(vars.config, vars.mode, _posId, _poolToRepay, _repayShares);
    }
```

<https://github.com/code-423n4/2023-12-initcapital/blob/main/contracts/core/InitCore.sol#L530-L551>

```solidity
    function _repay(IConfig _config, uint16 _mode, uint _posId, address _pool, uint _shares)
        internal
        returns (address tokenToRepay, uint amt)
    {
        // check status
>>>     _require(_config.getPoolConfig(_pool).canRepay && _config.getModeStatus(_mode).canRepay, Errors.REPAY_PAUSED);
        // get position debt share
        uint positionDebtShares = IPosManager(POS_MANAGER).getPosDebtShares(_posId, _pool);
        uint sharesToRepay = _shares < positionDebtShares ? _shares : positionDebtShares;
        // get amtToRepay (accrue interest)
        uint amtToRepay = ILendingPool(_pool).debtShareToAmtCurrent(sharesToRepay);
        // take token from msg.sender to pool
        tokenToRepay = ILendingPool(_pool).underlyingToken();
        IERC20(tokenToRepay).safeTransferFrom(msg.sender, _pool, amtToRepay);
        // update debt on the position
        IPosManager(POS_MANAGER).updatePosDebtShares(_posId, _pool, -sharesToRepay.toInt256());
        // call repay on the pool
        amt = ILendingPool(_pool).repay(sharesToRepay);
        // update debt on mode
        IRiskManager(riskManager).updateModeDebtShares(_mode, _pool, -sharesToRepay.toInt256());
        emit Repay(_pool, _posId, msg.sender, _shares, amt);
    }
```
### Recommended Mitigation Steps

Add a `canRepay` check status inside `setPosMode`; if it is paused, revert the change. Besides that, the `canRepay` and `canBorrow` checks don't need to be inside the pools check loop.

<details>

```diff
    function setPosMode(uint _posId, uint16 _mode)
        public
        virtual
        onlyAuthorized(_posId)
        ensurePositionHealth(_posId)
        nonReentrant
    {
        IConfig _config = IConfig(config);
        // get current collaterals in the position
        (address[] memory pools,, address[] memory wLps, uint[][] memory ids,) =
            IPosManager(POS_MANAGER).getPosCollInfo(_posId);
        uint16 currentMode = _getPosMode(_posId);
        ModeStatus memory currentModeStatus = _config.getModeStatus(currentMode);
        ModeStatus memory newModeStatus = _config.getModeStatus(_mode);
        if (pools.length != 0 || wLps.length != 0) {
            _require(newModeStatus.canCollateralize, Errors.COLLATERALIZE_PAUSED);
            _require(currentModeStatus.canDecollateralize, Errors.DECOLLATERALIZE_PAUSED);
        }
        // check that each position collateral belongs to the _mode
        for (uint i; i < pools.length; i = i.uinc()) {
            _require(_config.isAllowedForCollateral(_mode, pools[i]), Errors.INVALID_MODE);
        }
        for (uint i; i < wLps.length; i = i.uinc()) {
            for (uint j; j < ids[i].length; j = j.uinc()) {
                _require(_config.isAllowedForCollateral(_mode, IBaseWrapLp(wLps[i]).lp(ids[i][j])), Errors.INVALID_MODE);
            }
        }
        // get current debts in the position
        uint[] memory shares;
        (pools, shares) = IPosManager(POS_MANAGER).getPosBorrInfo(_posId);
        IRiskManager _riskManager = IRiskManager(riskManager);
        // check that each position debt belongs to the _mode
+      _require(newModeStatus.canBorrow, Errors.BORROW_PAUSED);
+      _require(currentModeStatus.canRepay, Errors.REPAY_PAUSED);
+      _require(newModeStatus.canRepay, Errors.REPAY_PAUSED);
        for (uint i; i < pools.length; i = i.uinc()) {
            _require(_config.isAllowedForBorrow(_mode, pools[i]), Errors.INVALID_MODE);
-            _require(newModeStatus.canBorrow, Errors.BORROW_PAUSED);
-            _require(currentModeStatus.canRepay, Errors.REPAY_PAUSED);
            // update debt on current mode
            _riskManager.updateModeDebtShares(currentMode, pools[i], -shares[i].toInt256());
            // update debt on new mode
            _riskManager.updateModeDebtShares(_mode, pools[i], shares[i].toInt256());
        }
        // update position mode
        IPosManager(POS_MANAGER).updatePosMode(_posId, _mode);
        emit SetPositionMode(_posId, _mode);
    }
```

</details>

**[fez-init (INIT) confirmed](https://github.com/code-423n4/2023-12-initcapital-findings/issues/26#issuecomment-1870318447)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | INIT Capital |
| Report Date | N/A |
| Finders | said |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-initcapital
- **GitHub**: https://github.com/code-423n4/2023-12-initcapital-findings/issues/26
- **Contest**: https://code4rena.com/reports/2023-12-initcapital

### Keywords for Search

`vulnerability`

