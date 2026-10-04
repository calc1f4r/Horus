---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 15991
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/321

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
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-08] Adversary can force user to pay large gas fees by transfering them collateral

### Overview


This bug report is about an issue in the code of a platform where users can transfer collateral to each other. The issue is that when the sending user has the collateral enabled and the receiving user does not have a balance already, the code automatically enables the collateral for the receiver. This increases the gas costs for the receiver every time they do anything that requires a health check, which includes turning off the collateral. If enough different kinds of collateral are added to the platform, it could even be enough gas to cause a denial of service (DOS) attack on the users. The recommended mitigation step for this issue is to not automatically enable the collateral for the receiver. This can be done by making changes to the code so that it does not enable the collateral for the receiver when the conditions in the bug report are met.

### Original Finding Content


<https://github.com/code-423n4/2022-11-paraspace/blob/c6820a279c64a299a783955749fdc977de8f0449/paraspace-core/contracts/protocol/libraries/logic/SupplyLogic.sol#L462-L512>

Adversary can DOS user and make them pay more gas by sending them collateral.

### Proof of Concept

    if (fromConfig.isUsingAsCollateral(reserveId)) {
        if (fromConfig.isBorrowingAny()) {
            ValidationLogic.validateHFAndLtvERC20(
                reservesData,
                reservesList,
                usersConfig[params.from],
                params.asset,
                params.from,
                params.reservesCount,
                params.oracle
            );
        }

        if (params.balanceFromBefore == params.amount) {
            fromConfig.setUsingAsCollateral(reserveId, false);
            emit ReserveUsedAsCollateralDisabled(
                params.asset,
                params.from
            );
        }

        //@audit collateral is automatically turned on for receiver
        if (params.balanceToBefore == 0) {
            DataTypes.UserConfigurationMap
                storage toConfig = usersConfig[params.to];

            toConfig.setUsingAsCollateral(reserveId, true);
            emit ReserveUsedAsCollateralEnabled(
                params.asset,
                params.to
            );
        }
    }

The above lines are executed when a user transfer collateral to another user. If the sending user currently has the collateral enabled and the receiving user doesn't have a balance already, the collateral will automatically be enabled for the receiver. Since the collateral is enabled, it will now be factored into the health check calculation. This increases gas for the receiver every time the user does anything that requires a health check (which ironically includes turning off a collateral). If enough different kinds of collateral are added to the platform it may even be enough gas to DOS the users.

### Recommended Mitigation Steps

Don't automatically enable the collateral for the receiver.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/321
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

