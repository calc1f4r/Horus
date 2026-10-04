---
# Core Classification
protocol: Mimo DeFi
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3147
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-mimo-august-2022-contest
source_link: https://code4rena.com/reports/2022-08-mimo
github_link: https://github.com/code-423n4/2022-08-mimo-findings/issues/34

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - wrong_math
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-05] MIMOManagedRebalance.sol#rebalance calculates managerFee incorrectly

### Overview


The reported bug affects the MIMOManagedRebalance.sol contract, which is part of the 2022-08-mimo GitHub repository. The bug has the potential to cause inconsistent manager fees, which could lead to lack of incentivization to rebalance and unexpected liquidation. This is because the variable portion of the fee is calculated using the amount of the flashloan, but pays out in PAR. The value of the flashloan asset is constantly fluctuating in value against PAR, making the fee unpredictable for both the user and the manager.

The recommended mitigation step is to calculate the varFee against the PAR of the rebalance, like it is done in MIMOAutoRebalance.sol. This will ensure that the fee is consistent and that the manager is properly incentivized to call the vault. This will also prevent unexpected liquidation, which can result in loss of user funds.

### Original Finding Content

_Submitted by 0x52_

Inconsistent manager fees could lead to lack of incentivization to rebalance and unexpected liquidation.

### Proof of Concept

    uint256 managerFee = managedVault.fixedFee + flData.amount.wadMul(managedVault.varFee);

    IERC20(a.stablex()).safeTransfer(managedVault.manager, managerFee);

The variable portion of the fee is calculated using the amount of the flashloan but pays out in PAR. This is problematic because the value of the flashloan asset is constantly fluctuating in value against PAR. This results in an unpredictable fee for both the user and the manager. If the asset drops in price then the user will pay more than they intended. If the asset increases in price then the fee may not be enough to incentivize the manager to call them. The purpose of the managed rebalance is to limit user interaction. If the manager isn't incentivized to call the vault then the user may be unexpectedly liquidated, resulting in loss of user funds.

### Recommended Mitigation Steps

varFee should be calculated against the PAR of the rebalance like it is in MIMOAutoRebalance.sol:

    IPriceFeed priceFeed = a.priceFeed();
    address fromCollateral = vaultsData.vaultCollateralType(rbData.vaultId);

    uint256 rebalanceValue = priceFeed.convertFrom(fromCollateral, flData.amount);
    uint256 managerFee = managedVault.fixedFee + rebalanceValue.wadMul(managedVault.varFee);

**[RayXpub (Mimo) confirmed and commented](https://github.com/code-423n4/2022-08-mimo-findings/issues/34#issuecomment-1210609570):**
 > We acknowledge this issue and intend to fix it.

**horsefacts (warden) reviewed mitigation:**
> **Status:** ✅ Resolved

> **Finding:** A warden identified that the variable portion of manager fees in `MIMOManagedRebalance` was calculated incorrectly, based on the amount of the rebalance flash loan denominated in the collateral asset rather than the amount of the rebalance denominated in PAR.

> **What changed:** The Mimo team updated the [fee calculation](https://github.com/mimo-capital/2022-08-mimo/blob/5186ef4be23f9dda81c8474096edb1f0594d70c3/contracts/actions/managed/MIMOManagedRebalance.sol#L61) to calculate the rebalance amount in PAR using a price feed.

> **Why it works:** Since the rebalance amount is now denominated in PAR, it no longer fluctuates in terms of the collateral asset.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Mimo DeFi |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-mimo
- **GitHub**: https://github.com/code-423n4/2022-08-mimo-findings/issues/34
- **Contest**: https://code4rena.com/contests/2022-08-mimo-august-2022-contest

### Keywords for Search

`Wrong Math, Business Logic`

