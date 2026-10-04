---
# Core Classification
protocol: MorpheusAI
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41618
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clrzgrole0007xtsq0gfdw8if
source_link: none
github_link: https://github.com/Cyfrin/2024-01-Morpheus

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - PratRed
  - wttt
  - SovaSlava
  - matej
  - Denzi
---

## Vulnerability Title

Due to no access control on `DistributionV2::_authorizeUpgrade()` anyone can change the implementation contract and can destroy the main Proxy contract.

### Overview


This bug report highlights a high-risk vulnerability in the `DistributionV2` contract, which is used for distributing tokens. The issue arises due to the lack of access control on the `_authorizeUpgrade()` function, which allows anyone to change the implementation contract and potentially destroy the main Proxy contract. This can be exploited by setting a malicious contract as the implementation, which can then use the `selfdestruct()` function to erase all storage from the main proxy contract. The report recommends adding proper access control to the `_authorizeUpgrade()` function, using the `OwnableUpgradeable` contract from OpenZeppelin and adding an initializer function to initialize the owner. This will ensure that only the owner can authorize upgrades to the implementation contract, mitigating the vulnerability.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-01-Morpheus/blob/main/contracts/mock/DistributionV2.sol#L36">https://github.com/Cyfrin/2024-01-Morpheus/blob/main/contracts/mock/DistributionV2.sol#L36</a>

<a data-meta="codehawks-github-link" href="https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/utils/UUPSUpgradeable.sol#L86-L90">https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/utils/UUPSUpgradeable.sol#L86-L90</a>



## Vulnerability Details :

`DistributionV2` contract inheriting `UUPSUpgradeable` so overriding `_authorizeUpgrade()` function. But adding no access control to this function can lead to setting implementation contract by anyone since this function is called for authorization in `UUPSUpgradeable`. By setting any malicious contract as implementation attacker can **selfdestruct()** the proxy contract. Since implementation is called using delegatecall from proxy.

### Code Snippet :

[contracts/mock/DistributionV2.sol](https://github.com/Cyfrin/2024-01-Morpheus/blob/main/contracts/mock/DistributionV2.sol#L36)

```solidity
36:  function _authorizeUpgrade(address) internal view override {}
```

Since `DistributionV2` contract is inheriting `UUPSUpgradeable` from openzeppelin we can see in upgrading implementation address `_authorizeUpgrade()` is called.

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/utils/UUPSUpgradeable.sol#L86C5-L90C1

```solidity
function upgradeToAndCall(address newImplementation, bytes memory data) public payable virtual onlyProxy {
        _authorizeUpgrade(newImplementation);
        _upgradeToAndCallUUPS(newImplementation, data);
    }
```

### Malicious `DistributionV2` implementation contract

```javascript
contract DistributionV2 is UUPSUpgradeable {
    IDistribution.Pool[] public pools;

    function version() external pure returns (uint256) {
        return 2;
    }

    function createPool(IDistribution.Pool calldata pool_) public {
        selfdestruct(address(0));//@audit this code will be implanted here
    }

    function getPeriodReward(uint256 poolId_, uint128 startTime_, uint128 endTime_) public view returns (uint256) {
        IDistribution.Pool storage pool = pools[poolId_];

        return LinearDistributionIntervalDecrease.getPeriodReward(
            pool.initialReward, pool.rewardDecrease, pool.payoutStart,  pool.decreaseInterval, startTime_, endTime_
        );
    }

    function _authorizeUpgrade(address) internal view override {}
}

```

First attacker will call `upgradeToAndCall` to main proxy contract which will change the implementation contract address to his malicious `DistributionV2` contract.
Now Attacker will call `createPool` to main proxy contract of `DistributionV2` and by `delegatecall` proxy will call implementation contract .It will destroy the main proxy contract using `selfdestruct()`. And erase all the storage from main proxy contract of DistributionV2.

## Impact :

The main proxy contract will be destroyed and erase all the storage from main proxy contract of DistributionV2.

## Tools Used

Manual Review

## Recommended Mitigation Steps :

Add proper access control to `_authorizeUpgrade()` function since it is used for authorization at the time of changing implementation contract address. This can be mitigated by using 'OwnableUpgradeable' of openzeppelin and add `onlyOwner` modifier to the `_authorizeUpgrade()` function so. Only owner can be authorized to upgrade the implementation address. Add one initalizer function also to initialize the owner.

```diff

File : contracts/mock/DistributionV2.sol
  ...

+  import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

-  contract DistributionV2 is UUPSUpgradeable {
+  contract DistributionV2 is OwnableUpgradeable, UUPSUpgradeable {

 ...


+  function Distribution_init() external initializer
+    {
+        __Ownable_init();
+        __UUPSUpgradeable_init();
+    }

       ...

- function _authorizeUpgrade(address) internal view override {}
+ function _authorizeUpgrade(address) internal view override onlyOwner {}
}

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Codehawks |
| Protocol | MorpheusAI |
| Report Date | N/A |
| Finders | PratRed, wttt, SovaSlava, matej, Denzi, 0x11singh99 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-01-Morpheus
- **Contest**: https://codehawks.cyfrin.io/c/clrzgrole0007xtsq0gfdw8if

### Keywords for Search

`vulnerability`

