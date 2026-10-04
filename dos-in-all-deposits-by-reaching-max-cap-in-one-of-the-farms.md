---
# Core Classification
protocol: infiniFi contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55057
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
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
finders_count: 4
finders:
  - R0bert
  - Slowfi
  - Jonatas Martins
  - Noah Marconi
---

## Vulnerability Title

DoS in all deposits by reaching max. cap in one of the farms

### Overview


The AfterMintHook contract has a bug that can cause a denial of service (DoS) condition, stopping all deposits across the protocol. This happens because the function that selects the best farm for deposits does not check if the farm is already full. If a farm is full, the deposit will fail and the whole transaction will fail, leading to a DoS condition. To fix this, the function should check if the farm has enough space before selecting it for a deposit. This issue has been partially fixed, but it is still possible for the bug to occur. The InfiniFi team can use a Guardian or manual rebalancer to fix the issue if it occurs. 

### Original Finding Content

## Severity: Medium Risk

## Context
`AfterMintHook.sol#L36-L44`

## Description
The AfterMintHook implementation could lead to a denial of service (DoS) condition, halting all deposit operations across the protocol. This issue occurs due to the behavior of the `_findOptimalDepositFarm` function, which is tasked with selecting the most appropriate farm for depositing assets based on parameters such as farm weights, total power, and available assets. 

The flaw is that this function does not check whether the selected farm has already reached its maximum deposit capacity, as enforced by the farm's own deposit function. 

In the farm contract, the deposit function includes a cap check:

```solidity
function deposit() external onlyCoreRole(CoreRoles.FARM_MANAGER) whenNotPaused {
    uint256 currentAssets = assets();
    if (currentAssets > cap) {
        revert CapExceeded(currentAssets, cap);
    }
    _deposit();
}
```

If the farm's current asset level exceeds its predefined cap, the function reverts with a `CapExceeded` error.

In the AfterMintHook contract, after `_findOptimalDepositFarm` selects a farm, the code proceeds to call `IFarm(farm).deposit()`:

```solidity
address farm = _findOptimalDepositFarm(farms, weights, totalPower, totalAssets, _assetsIn);
if (farm == address(0)) {
    // No optimal farm found, skip the deposit
    return;
}
IFarm(msg.sender).withdraw(_assetsIn, address(farm));
IFarm(farm).deposit();
```

If the selected farm has reached its cap, this deposit call will revert, causing the entire transaction in AfterMintHook to fail. Since `_findOptimalDepositFarm` does not account for farm capacities, it will repeatedly select a farm that is already full, leading to a persistent failure of all deposit attempts. This effectively creates a DoS condition, blocking new deposits across the protocol until the situation is manually addressed, such as by adjusting farm caps or weights.

## Recommendation
To address this, the `_findOptimalDepositFarm` function should be modified to verify each farm's available capacity before selecting it for a deposit. Specifically, it should ensure that adding the incoming deposit amount (`_assetsIn`) to the farm's current assets does not exceed its cap. If a farm would surpass its cap with the new deposit, it should be skipped, and the function should continue evaluating other farms. Only if no farm can accommodate the deposit without exceeding its cap should the function indicate that the system is fully utilized, reverting with an error that indicates that the protocol has no capacity to handle that deposit.

## infiniFi
Partially fixed in `d12c936` by adding pausability on the hooks which will allow faster reaction if there is an issue on farm movements. The Guardian can be used to unstuck the situation, as well as a manual rebalancer to deploy capital in the meantime, before the governor can change the hooks configuration.

## Spearbit
While the new implementation does not totally prevent the issue, it really allows the InfiniFi team to react and correct it in case it occurs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | infiniFi contracts |
| Report Date | N/A |
| Finders | R0bert, Slowfi, Jonatas Martins, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

