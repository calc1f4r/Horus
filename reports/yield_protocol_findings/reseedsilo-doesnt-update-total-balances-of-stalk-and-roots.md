---
# Core Classification
protocol: Beanstalk: The Finale
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36252
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n
source_link: none
github_link: https://github.com/Cyfrin/2024-05-beanstalk-the-finale

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

protocol_categories:
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - deadrosesxyz
  - T1MOH
---

## Vulnerability Title

ReseedSilo doesn't update total balances of Stalk and Roots

### Overview


The ReseedSilo function is used to migrate deposits owned by EOA. However, it does not update the total balances of Stalk and Roots. This has a high risk severity as it can lead to imbalances in voting and distribution of Beans. The vulnerability details show that the function does not increase global values of `s.sys.silo.stalk` and `s.sys.silo.roots`. This can affect the calculation of `s.sys.seedGauge.averageGrownStalkPerBdvPerSeason` and `s.sys.seedGauge.averageGrownStalkPerBdvPerSeason` is used to calculate the amount of Grown Stalk for the next season. This can result in lower Stalk rewards and an imbalance in voting. The bug can be fixed by increasing global Stalk and Roots values in the function. This report was done through manual review. The recommendation is to update the function to set Stalk and increase global Roots. 

### Original Finding Content

## Summary

ReseedSilo is used to migrate Silo deposits owned by EOA. It writes Stalk associated with migrated deposits and misses to write Roots (but that's another issue submitted in another report). However it doesn't update total supply

## Vulnerability Details

As you can see this function doesn't increase global values of `s.sys.silo.stalk` and `s.sys.silo.roots`:
<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/df2dd129a878d16d4adc75049179ac0029d9a96b/protocol/contracts/beanstalk/init/reseed/L2/ReseedSilo.sol#L109-L180>

## Impact

As you can see after migration `s.sys.silo.stalk` will be much much lower. This value is used in Gauge Point system.

It is used to calculate `s.sys.seedGauge.averageGrownStalkPerBdvPerSeason`:
<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/df2dd129a878d16d4adc75049179ac0029d9a96b/protocol/contracts/libraries/LibGauge.sol#L343-L352>

```solidity
    function updateAverageStalkPerBdvPerSeason() internal {
        ...
@>      s.sys.seedGauge.averageGrownStalkPerBdvPerSeason = uint128(
@>          getAverageGrownStalkPerBdv().mul(BDV_PRECISION).div(
                s.sys.seedGaugeSettings.targetSeasonsToCatchUp
            )
        );
        ...
    }

    function getAverageGrownStalkPerBdv() internal view returns (uint256) {
        AppStorage storage s = LibAppStorage.diamondStorage();
        uint256 totalBdv = getTotalBdv();
        if (totalBdv == 0) return 0;
@>      return s.sys.silo.stalk.div(totalBdv).sub(STALK_BDV_PRECISION);
    }
```

Then `s.sys.seedGauge.averageGrownStalkPerBdvPerSeason` is used to calculate amount of Grown Stalk for the next season:
<https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/df2dd129a878d16d4adc75049179ac0029d9a96b/protocol/contracts/libraries/LibGauge.sol#L267-L269>

```solidity
    function updateGrownStalkEarnedPerSeason(
        uint256 maxLpGpPerBdv,
        LpGaugePointData[] memory lpGpData,
        uint256 totalGaugePoints,
        uint256 totalLpBdv
    ) internal {
        ...

        // update the average grown stalk per BDV per Season.
        // beanstalk must exist for a minimum of the catchup season in order to update the average.
        if (s.sys.season.current > s.sys.seedGaugeSettings.targetSeasonsToCatchUp) {
@>          updateAverageStalkPerBdvPerSeason();
        }

        // Calculate grown stalk issued this season and GrownStalk Per GaugePoint.
@>      uint256 newGrownStalk = uint256(s.sys.seedGauge.averageGrownStalkPerBdvPerSeason)
            .mul(totalGaugeBdv)
            .div(BDV_PRECISION);

        ...
    }
```

As you remember total Stalk is much lower than it should be, it means Stalk rewards in future seasons will be much lower too. It will lead to imbalance in voting because Stalk is governance token.

Additionally Stalk is associated with Roots. There will also be imbalance in distribution of Beans minted to Silo at the start of the season.

## Tools Used

Manual Review

## Recommendations

Here is solution to set Stalk. You should also increase global Roots.

```diff
    function reseedSiloDeposit(SiloDeposits calldata siloDeposit) internal {
        uint256 totalCalcDeposited;
        uint256 totalCalcDepositedBdv;
        uint256 stalkIssuedPerBdv = s.sys.silo.assetSettings[siloDeposit.token].stalkIssuedPerBdv;
+       uint256 totalStalk;
        for (uint256 i; i < siloDeposit.siloDepositsAccount.length; i++) {
            ...
            }
            ...

            // set stalk for account.
            s.accts[deposits.accounts].stalk = accountStalk;
            
+           totalStalk += accountStalk;
        }

        ...
        // set global state
        s.sys.silo.balances[siloDeposit.token].deposited = siloDeposit.totalDeposited;
        s.sys.silo.balances[siloDeposit.token].depositedBdv = siloDeposit.totalDepositedBdv;
+       s.sys.silo.stalk += totalStalk;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk: The Finale |
| Report Date | N/A |
| Finders | deadrosesxyz, T1MOH |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-beanstalk-the-finale
- **Contest**: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n

### Keywords for Search

`vulnerability`

