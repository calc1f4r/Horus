---
# Core Classification
protocol: HypurrFi_2025-02-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55468
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
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

[M-01] DeployHyFiConfigEngine: double deployment of `proxyAdmin`

### Overview


The report is about a medium severity bug that affects the `DeployHyFiConfigEngine.run` function. This function creates a `ProxyAdmin` using `transparentProxyFactory` and then calls `_createAndSetupRatesFactory` while passing the address of `proxyAdmin` as `ownerForFactory`. The problem is that the `create` function expects the address of the owner and deploys its own `adminProxy`, resulting in a pattern of proxyAdmin(1) > proxyAdmin(2) > transparentProxy > Impl. This prevents the admin from upgrading the contract. The recommendation is to not deploy a separate `proxyAdmin` and instead pass the address of `admin` to the `create` function.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

`DeployHyFiConfigEngine.run` creates a `ProxyAdmin` using `transparentProxyFactory` :

```solidity
    function run() external {
        --snip--
        transparentProxyFactory = new TransparentProxyFactory();
        proxyAdmin = ProxyAdmin(transparentProxyFactory.createProxyAdmin(admin));

        (ratesFactory,) = DeployRatesFactoryLib._createAndSetupRatesFactory(
             poolAddressesProvider, address(transparentProxyFactory), address(proxyAdmin), reservesToSkip);
       --snip--
     }
```

then calls `_createAndSetupRatesFactory` and passes the address of `proxyAdmin` as `ownerForFactory`:

```solidity
    function _createAndSetupRatesFactory(
        IPoolAddressesProvider addressesProvider,
        address transparentProxyFactory,
        address ownerForFactory,
        address[] memory reservesToSkip
    ) internal returns (V3RateStrategyFactory, address[] memory) {
        --snip--
        V3RateStrategyFactory ratesFactory = V3RateStrategyFactory(
            ITransparentProxyFactory(transparentProxyFactory).create(
                address(new V3RateStrategyFactory(addressesProvider)),
                ownerForFactory,
                abi.encodeWithSelector(V3RateStrategyFactory.initialize.selector, uniqueStrategies)
            )
        );
       --snip--
}
```

It calls `ITransparentProxyFactory(transparentProxyFactory).create` and passes the address of `ownerForFactory` (already deployed`proxyAdmin`) as `initialOwner`:
The problem is that `create` function expects the address of owner and deploys its own `adminProxy`:

https://github.com/bgd-labs/solidity-utils/blob/90266e46868fe61ed0b54496c10458c247acdb51/src/contracts/transparent-proxy/TransparentProxyFactoryBase.sol#L29

```solidity
function create(
    address logic,
    address initialOwner,
    bytes calldata data
  ) external returns (address) {
    address proxy = address(new TransparentUpgradeableProxy(logic, initialOwner, data));
    _storeProxyInRegistry(proxy);

    emit ProxyCreated(proxy, logic, initialOwner);

    return proxy;
  }
```

So the pattern will be like:
proxyAdmin(1) > proxyAdmin(2) > transparentProxy > Impl
As a result, the admin will not be able to upgrade the contract.

Note:
`import {ITransparentProxyFactory} from "solidity-utils/contracts/transparent-proxy/interfaces/ITransparentProxyFactory.sol"; `
The code for the above interface is here:
https://github.com/bgd-labs/solidity-utils/blob/main/src/contracts/transparent-proxy/interfaces/ITransparentProxyFactory.sol

## Recommendations

Dont deploy a separate `proxyAdmin` and just pass address of `admin` to `create` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | HypurrFi_2025-02-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/HypurrFi-security-review_2025-02-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

