---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31452
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
github_link: none

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
  - Pashov Audit Group
---

## Vulnerability Title

[M-14] Magnetar `_depositRepayAndRemoveCollateralFromMarket` can fail due to rounding errors

### Overview


This bug report describes a problem that can occur when a user tries to remove collateral and withdraw from a yieldbox. If the user sets the `collateralAmount` to be more than 0, the function may revert. This happens because the contract is using a rounding down method to calculate the `collateralShare` which can result in not enough shares being available for withdrawal. The report recommends using a rounding up method instead to ensure that enough shares are available for withdrawal.

### Original Finding Content

**Severity**

**Impact**: Medium, can cause function to revert

**Likelihood**: Medium, happens when user tries to remove collateral and withdraw from yieldbox

**Description**

If `collateralAmount` is set to be more than 0 while calling the `_depositRepayAndRemoveCollateralFromMarket` function, the following snippet is executed.

```solidity
if (collateralAmount > 0) {
            address collateralWithdrawReceiver = withdrawCollateralParams
                .withdraw
                ? address(this)
                : user;
            uint256 collateralShare = yieldBox.toShare(
                marketInterface.collateralId(),
                collateralAmount,
                false
            );
            marketInterface.removeCollateral(
                user,
                collateralWithdrawReceiver,
                collateralShare
            );

            //withdraw
            if (withdrawCollateralParams.withdraw) {
                _withdrawToChain(
                    yieldBox,
                    collateralWithdrawReceiver,
                    marketInterface.collateralId(),
                    withdrawCollateralParams.withdrawLzChainId,
                    LzLib.addressToBytes32(user),
                    collateralAmount,
                    withdrawCollateralParams.withdrawAdapterParams,
                    valueAmount > 0 ? payable(msg.sender) : payable(this),
                    valueAmount,
                    withdrawCollateralParams.unwrap
                );
            }
        }
```

In the first bit, `collateralShare` is calculated from the yieldBox rebase calculations. since the last parameter is false, the answer is rounded down. Lets assume `collateralAmount` is set to 100, and the `collateralShare` calculated is between 49 and 50, and is set as 49 due to the rounding down.

Later in the `_withdrawToChain` call, the contract tries to withdraw the full `collateralAmount` amount of tokens. Here the yieldBox is called again to take those tokens out of it.

```solidity
yieldBox.withdraw(
                assetId,
                from,
                LzLib.bytes32ToAddress(receiver),
                amount,
                0
            );
```

But in this call, due to it being a withdraw, the amount of shares to be deducted is rounded up. So now for withdrawing the same 100 units of `collateralAmount`, the amount of shares to be burnt is calculated as 50 due to the rounding up. Since the contract has withdrawn only 49 shares but the yieldBox is trying to burn 50, this function will revert.

This is similar to the M-02 report showing a similar rounding error forcing a revert but in a different scenario.

**Recommendations**

Calculate `collateralShare` by rounding it up. This will ensure enough shares are present to burn during withdrawal.

```solidity
uint256 collateralShare = yieldBox.toShare(
                marketInterface.collateralId(),
                collateralAmount,
                true
            );
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

