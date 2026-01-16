---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57163
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 33
finders:
  - kkk
  - oluwaseyisekoni
  - nikolavelev241390
  - vs_
  - holydevoti0n
---

## Vulnerability Title

`GaugeController` does not send funds to FeeCollector disrupting fees distribution and causing loss of funds

### Overview


The GaugeController is not sending funds to the FeeCollector, which is causing a disruption in the distribution of fees and resulting in a loss of funds. This is a high-risk issue that breaks the protocol's fee management system. The issue is that the GaugeController is bypassing the FeeCollector and directly sending funds to Gauges, which means that performance fees are not being tracked and cannot be withdrawn. This goes against the design of the FeeCollector, which is meant to manage all fee collections and distributions. The impact of this bug is that 20% of all revenue is lost, the fee distribution system is broken, and the protocol's accounting becomes unreliable. The recommendation is to ensure that all fees go through the FeeCollector and track performance fees properly. 

### Original Finding Content

## Summary

The `GaugeController` bypasses the `FeeCollector` contract when distributing revenue, directly sending funds to Gauges and completely losing the performance fees. This breaks the protocol's fee management system, which is designed to have the `FeeCollector` as the central point for managing and distributing all protocol fees to various stakeholders.

## Vulnerability Details

The `FeeCollector` is designed as the central contract for managing protocol fee collection and distribution to stakeholders including veRAAC holders, treasury, and repair fund. However, the `GaugeController's` `distributeRevenue` function:

```Solidity
    function distributeRevenue(
        GaugeType gaugeType,
        uint256 amount
    ) external onlyRole(EMERGENCY_ADMIN) whenNotPaused {
        if (amount == 0) revert InvalidAmount();
        
        uint256 veRAACShare = amount * 80 / 100; // 80% to veRAAC holders
        // @audit-issue 1. performance fees calculated but never used.
        // @audit-issue 2. performance fees are not tracked
@>        uint256 performanceShare = amount * 20 / 100; // 20% performance fee
        
        revenueShares[gaugeType] += veRAACShare;
        // @audit-issue 3. bypass FeeCollector by directly distributing 80% to Gauges
        _distributeToGauges(gaugeType, veRAACShare);
        
        emit RevenueDistributed(gaugeType, amount, veRAACShare, performanceShare);
    }
```

As we can see in the code above: 

1. Bypasses `FeeCollector` by directly distributing 80% to Gauges.
2. Performance fees calculated but never used(should be sent to the `FeeCollector`)
3. Performance fees are not tracked(`performanceFees`is not used)

    

Notice that for the performance fees, there is no way to withdraw those funds, which will lead to permanently loss of funds.

This contradicts the FeeCollector's design which should:



* Collect all protocol fees
* Manage fee distributions through its configured fee types
* Ensure proper splitting between stakeholders
* Track all fee collections and distributions



The implementation meets the documentation, putting `FeeCollector`in charge of distributing all the collected fees.&#x20;



```Solidity
    function _processDistributions(uint256 totalFees, uint256[4] memory shares) internal {
        uint256 contractBalance = raacToken.balanceOf(address(this));
        if (contractBalance < totalFees) revert InsufficientBalance();


        if (shares[0] > 0) {
            uint256 totalVeRAACSupply = veRAACToken.getTotalVotingPower();
            if (totalVeRAACSupply > 0) {
                TimeWeightedAverage.createPeriod(
                    distributionPeriod,
                    block.timestamp + 1,
                    7 days,
                    shares[0],
                    totalVeRAACSupply
                );
                totalDistributed += shares[0];
            } else {
                shares[3] += shares[0]; // Add to treasury if no veRAAC holders
            }
        }


        if (shares[1] > 0) raacToken.burn(shares[1]);
        if (shares[2] > 0) raacToken.safeTransfer(repairFund, shares[2]);
        if (shares[3] > 0) raacToken.safeTransfer(treasury, shares[3]);
    }
```

## Impact

* 20% of all revenue (performance fees) are permanently lost.
* Broken fee distribution system:
  * FeeCollector loses visibility of revenue flows
  * Fee distributions bypass intended controls and splits
  * No proper tracking of collected fees
  * Stakeholders don't receive their intended share of fees
* Compromised protocol accounting:
  * Performance fees are not tracked in `performanceFees` mapping
  * FeeCollector's accounting system becomes unreliable&#x20;

## Tools Used

Manual Review

## Recommendations

1. Ensure all fees go through `FeeCollector`.

```diff
function distributeRevenue(
    GaugeType gaugeType,
    uint256 amount
) external onlyRole(EMERGENCY_ADMIN) whenNotPaused {
    if (amount == 0) revert InvalidAmount();
    
    uint256 veRAACShare = amount * 80 / 100; // 80% to veRAAC holders
    uint256 performanceShare = amount * 20 / 100; // 20% performance fee
    
    // ps: constructor should receive feeCollector and give max approval to it.
+    feeCollector.collectFee(performanceShare, 0); // 0 == Protocol Fees
+    feeCollector.collectFee(performanceShare, 2); // 2 == Performance Fees
+    performanceFees[msg.sender] += performanceShare; // Track the fees
    
    revenueShares[gaugeType] += veRAACShare;
-    _distributeToGauges(gaugeType, veRAACShare);
    
    emit RevenueDistributed(gaugeType, amount, veRAACShare, performanceShare);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | kkk, oluwaseyisekoni, nikolavelev241390, vs_, holydevoti0n, modey, udo, amarfares, 0xwhyzee, kwakudr, takarez, 0x23r0, dharkartz, kodyvim, notbozho, ke1cam, kalii, heheboii, iamthesvn, 0xaman, pyro, waydou, cipherhawk, vladislavvankov0, kirobrejka, 0xgremlincat, almur100, orangesantra, tamer, stanchev, josh4324, falendar, 0xslowbug |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

