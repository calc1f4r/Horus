---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49031
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
github_link: https://github.com/code-423n4/2024-07-loopfi-findings/issues/116

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
finders_count: 4
finders:
  - pkqs90
  - hash
  - nnez
  - 0xAlix2
---

## Vulnerability Title

[H-09] `decreaseLever` uses incorrect position address when withdrawing

### Overview


The `decreaseLever` function in the `Position4626` contract is not working properly. When trying to decrease the lever, the call will always fail and revert. This is because the function is attempting to withdraw collateral from its own address instead of the passed in position. To fix this, the function should be updated to withdraw from the correct position. This bug has been confirmed and given a high severity rating.

### Original Finding Content


`decreaseLever` will always revert for `Position4626` associated vaults.

### Proof of Concept

When decreasing lever, the control is passed over to the actual implementation contract for the `flashLoan` execution:

```solidity
    function decreaseLever(
        LeverParams calldata leverParams,
        uint256 subCollateral,
        address residualRecipient
    ) external onlyDelegatecall {
       
       ....

        // @audit execution passed to the implementation contract by setting it as the callback 
        // take out credit flash loan
        IPermission(leverParams.vault).modifyPermission(leverParams.position, self, true);
        uint loanAmount = leverParams.primarySwap.amount;
        flashlender.creditFlashLoan(
            ICreditFlashBorrower(self),
            loanAmount,
            abi.encode(leverParams, subCollateral, residualRecipient)
        );
        IPermission(leverParams.vault).modifyPermission(leverParams.position, self, false);       
```

Inside the `onCreditFlashLoan` call, it attempts to withdraw the collateral of the passed in position by the passed in `subCollateral` amount:

```solidity
    function onCreditFlashLoan(
        address /*initiator*/,
        uint256 /*amount*/,
        uint256 /*fee*/,
        bytes calldata data
    ) external returns (bytes32) {
        

        // sub collateral and debt
        ICDPVault(leverParams.vault).modifyCollateralAndDebt(
            leverParams.position,
            address(this),
            address(this),
            0,
            -toInt256(subDebt)
        );

        // withdraw collateral and handle any CDP specific actions
        // @audit should withdraw `subCollateral` amount from `leverParams.position`
=>      uint256 withdrawnCollateral = _onDecreaseLever(leverParams, subCollateral);
```

But the `_onDecreaseLever` function of the `Position4626` contract is flawed as it attempts to withdraw the collateral from its own address instead of the passed in `position`:

```solidity
    function _onDecreaseLever(
        LeverParams memory leverParams,
        uint256 subCollateral
    ) internal override returns (uint256 tokenOut) {
        // @audit attempts to withdraw from address(this) rather than leverParams.position
=>      uint256 withdrawnCollateral = ICDPVault(leverParams.vault).withdraw(address(this), subCollateral);
```

Since the collateral is actually present in the passed in position, this attempt to withdraw will  cause the call to revert.

### Recommended Mitigation Steps

Inside `_onDecreaseLever`, withdraw from `leverParams.position` instead.

**[Koolex (judge) increased severity to High](https://github.com/code-423n4/2024-07-loopfi-findings/issues/116#issuecomment-2386505529)**

**[amarcu (LoopFi) confirmed](https://github.com/code-423n4/2024-07-loopfi-findings/issues/116#event-15616256917)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | pkqs90, hash, nnez, 0xAlix2 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: https://github.com/code-423n4/2024-07-loopfi-findings/issues/116
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

