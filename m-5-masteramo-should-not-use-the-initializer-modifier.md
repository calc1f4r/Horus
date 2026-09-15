---
# Core Classification
protocol: AXION
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43538
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/552
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-axion-judging/issues/244

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
finders_count: 5
finders:
  - calc1f4r
  - KupiaSec
  - UsmanAtique
  - hunter\_w3b
  - FonDevs
---

## Vulnerability Title

M-5: MasterAMO should not use the `initializer` modifier

### Overview


This bug report discusses an issue with the `MasterAMO` contract, which is meant to be inherited by other contracts. The problem is that the `initialize` function in `MasterAMO` uses the `initializer` modifier, which limits initialization to only one call. This conflicts with the initialization process of inheriting contracts, leading to a failure in the deployment of critical protocol components. To fix this, the `initializer` modifier should be replaced with the `onlyInitializing` modifier, which allows the `initialize` function to be used by both the `MasterAMO` and any inheriting contracts.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-axion-judging/issues/244 

## Found by 
FonDevs, KupiaSec, UsmanAtique, calc1f4r, hunter\_w3b
### Summary

`MasterAMO` is a utils contract that intended to be inherited by SolidlyV2AMO, SolidlyV3AMO contracts, therefore. it's initializer function should not use the [initializer](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/MasterAMO.sol#L104) modifier, instead, it should use onlyInitializing modifier.



### Root Cause

In the [MasterAMO.sol:104](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/MasterAMO.sol#L104) contract, the initialize function uses the initializer modifier. This is incorrect for a contract like MasterAMO, which is meant to be inherited by other contracts, such as [SolidlyV2AMO](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/SolidlyV2AMO.sol#L10) and [SolidlyV3AMO](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/SolidlyV3AMO.sol#L8).


In this inheritance model, the [SolidlyV2AMO](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/SolidlyV2AMO.sol#L62-L82) contract also has its own initialize function, which includes the initializer modifier and calls the initialize function of MasterAMO. The problem here is that both the parent contract [MasterAMO](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/MasterAMO.sol#L104) and the child contracts [SolidlyV2AMO](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/SolidlyV2AMO.sol#L79), [SolidlyV3AMO](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/SolidlyV3AMO.sol#L67) are using the [initializer](https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-initializer--) modifier, which limits initialization to only one call. 

According to the [OpenZeppelin documentation](https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-initializer--), the [onlyInitializing](https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-onlyInitializing--) modifier should be used to allow initialization in both the parent and child contracts. The  [onlyInitializing](https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-onlyInitializing--) modifier ensures that when the initialize function is called, any contracts in its inheritance chain can still complete their own initialization.

https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-initializer--

>> A modifier that defines a protected initializer function that can be invoked at most once. In its scope, onlyInitializing functions can be used to initialize parent contracts.



### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

In this scenario, no direct attack or monetary loss is likely. However, the vulnerability causes a significant operational issue, preventing inheriting contracts from completing initialization. This could lead to a failure in the deployment of critical protocol components, affecting the overall system functionality.

### PoC

A simple POC in Remix.

![Screenshot from 2024-10-15 15-49-31](https://github.com/user-attachments/assets/c1fc0f96-c7cc-493b-aba3-71191edafa61)


### Mitigation


Replace the initializer modifier in the [MasterAMO](https://github.com/sherlock-audit/2024-10-axion/blob/main/liquidity-amo/contracts/MasterAMO.sol#L96C1-L104C27) contract with the onlyInitializing modifier. This allows the initialize function to be used by both the MasterAMO and any inheriting contracts during their initialization phase, without conflicting with their individual setup processes.

```diff
    function initialize(
        address admin, // // Address assigned the admin role (given exclusively to a multi-sig wallet)
        address boost_, // The Boost stablecoin address
        address usd_, // generic name for $1 collateral ( typically USDC or USDT )
        address pool_, // The pool where AMO logic applies for Boost-USD pair
        // On each chain where Boost is deployed, there will be a stable Boost-USD pool ensuring BOOST's peg.
        // Multiple Boost-USD pools can exist across different DEXes on the same chain, each with its own AMO, maintaining independent peg guarantees.
        address boostMinter_ // the minter contract
-   ) public initializer {
+   ) public onlyInitializing {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | AXION |
| Report Date | N/A |
| Finders | calc1f4r, KupiaSec, UsmanAtique, hunter\_w3b, FonDevs |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-axion-judging/issues/244
- **Contest**: https://app.sherlock.xyz/audits/contests/552

### Keywords for Search

`vulnerability`

