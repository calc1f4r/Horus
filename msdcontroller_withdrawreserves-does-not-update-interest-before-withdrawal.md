---
# Core Classification
protocol: dForce Lending Protocol Review
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13521
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/dforce-lending-protocol-review/
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Heiko Fisch
  - Alexander Wade
---

## Vulnerability Title

MSDController._withdrawReserves does not update interest before withdrawal

### Overview


This bug report is about the MSDController._withdrawReserves function in the MSD token contract. This function allows the owner of the token to mint the difference between an MSD asset's accumulated debt and earnings. However, the debt and earnings values are not updated when this function is used, meaning that the withdrawal amount may be calculated using stale values.

The issue was addressed in commit 2b5946e by changing the calcEquity method to update the interest of each MSDMinter assigned to an MSD asset. This is done by iterating over each MSDMinter, which may cause out-of-gas issues if the number of MSDMinters grows. dForce has informed us that the MSDMinter role will only be held by two contracts per asset (iMSD and MSDS).

The recommendation is to ensure that the _withdrawReserves function invokes iMSD.updateInterest() and MSDS.updateInterest(). This will ensure that the withdrawal amount is calculated using the latest values.

### Original Finding Content

#### Resolution



This issue was addressed in commit [`2b5946e`](https://github.com/dforce-network/LendingContracts/commit/2b5946e4aa280240a4fccf76d027b5fe4c83fb0b) by changing `calcEquity` to update the interest of each MSDMinter assigned to an MSD asset.


Note that this method iterates over each MSDMinter, which may cause out-of-gas issues if the number of MSDMinters grows. dForce has informed us that the MSDMinter role will only be held by two contracts per asset (`iMSD` and `MSDS`).




#### Description


`MSDController._withdrawReserves` allows the Owner to mint the difference between an MSD asset’s accumulated debt and earnings:


**code/contracts/msd/MSDController.sol:L182-L195**



```
function \_withdrawReserves(address \_token, uint256 \_amount)
    external
    onlyOwner
    onlyMSD(\_token)
{
    (uint256 \_equity, ) = calcEquity(\_token);

    require(\_equity >= \_amount, "Token do not have enough reserve");

    // Increase the token debt
    msdTokenData[\_token].debt = msdTokenData[\_token].debt.add(\_amount);

    // Directly mint the token to owner
    MSD(\_token).mint(owner, \_amount);

```
Debt and earnings are updated each time the asset’s `iMSD` and `MSDS` contracts are used for the first time in a given block. Because `_withdrawReserves` does not force an update to these values, it is possible for the withdrawal amount to be calculated using stale values.


#### Recommendation


Ensure `_withdrawReserves` invokes `iMSD.updateInterest()` and `MSDS.updateInterest()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | dForce Lending Protocol Review |
| Report Date | N/A |
| Finders | Heiko Fisch, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/dforce-lending-protocol-review/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

