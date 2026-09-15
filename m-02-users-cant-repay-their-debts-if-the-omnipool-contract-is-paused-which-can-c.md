---
# Core Classification
protocol: Beta Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28976
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-11-betafinance
source_link: https://code4rena.com/reports/2023-11-betafinance
github_link: https://github.com/code-423n4/2023-11-betafinance-findings/issues/32

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
finders_count: 3
finders:
  - 0xStalin
  - 1
  - 2
---

## Vulnerability Title

[M-02] Users can't repay their debts if the OmniPool contract is paused which can cause users to fall into liquidation and lose their collateral

### Overview


A bug has been found in the OmniPool contract that prevents users from repaying their debts if the contract is paused. This can lead to users falling into liquidation and losing their collateral. The bug is caused by the `whenNotPaused` modifier, which prevents the `repay()` function from being used if the contract is paused. To fix this issue, the `whenNotPaused` modifier should be removed from the `repay()` function, allowing users to repay their debts even if the contract is paused. The root cause of this issue is that users cannot repay their debts when the contract is paused, which can lead to their accounts becoming unhealthy due to the interest accrued. The bug has been confirmed and the recommended mitigation steps have been accepted.

### Original Finding Content


Users can't repay their debts if the OmniPool contract is paused which can cause users to fall into liquidation and lose their collateral

### Proof of Concept

The [`OmniPool::repay()` function](https://github.com/code-423n4/2023-11-betafinance/blob/main/Omni_Protocol/src/OmniPool.sol#L303-L310) has implemented the [`whenNotPaused` modifier](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/49c0e4370d0cc50ea6090709e3835a3091e33ee2/contracts/security/Pausable.sol#L44-L47), which will prevent the function from being used if the contract is paused. The problem is that the usage of this function should not be prevented because if users are unable to repay their debts, their accounts can fall into liquidation status while the OmniPool contract is paused, and once the contract is unpaused, and liquidations are enabled too, if the account felt into liquidation status, now the users and liquidators will be in a mev run to either repay the debt or liquidate the collateral.

This presents an unnecessary risk to users by preventing them from repaying their debts.

> OmniPool contract

```solidity
//@audit-issue -> If contract is paused, this function can't be called if the contract is paused because of the whenNotPaused modifier!
function repay(uint96 _subId, address _market, uint256 _amount) external whenNotPaused {
    ...
}
```
### Recommended Mitigation Steps

The mitigation is very straight forward, don't disable the borrower's repayments, and don't interrupt the repayments. Remove the whenNotPaused modifier:

> OmniPool contract

```solidity
- function repay(uint96 _subId, address _market, uint256 _amount) external whenNotPaused {
//@audit-ok => Allow repayments even if the contract is paused!
+ function repay(uint96 _subId, address _market, uint256 _amount) external {
    ...
}
```
**[allenjlee (BetaFinance) confirmed and commented](https://github.com/code-423n4/2023-11-betafinance-findings/issues/32#issuecomment-1807208128):**
 > We will remove the `whenNotPaused` modifier for `repay`

**[cccz (Judge) commented](https://github.com/code-423n4/2023-11-betafinance-findings/issues/32#issuecomment-1808342436):**
 > I think the root cause of this issue is that users are not able to repay when paused and the interest accrued may lead to the user's account being unhealthy.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Beta Finance |
| Report Date | N/A |
| Finders | 0xStalin, 1, 2 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-11-betafinance
- **GitHub**: https://github.com/code-423n4/2023-11-betafinance-findings/issues/32
- **Contest**: https://code4rena.com/reports/2023-11-betafinance

### Keywords for Search

`vulnerability`

