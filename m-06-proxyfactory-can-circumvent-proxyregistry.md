---
# Core Classification
protocol: Mimo DeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3148
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-mimo-august-2022-contest
source_link: https://code4rena.com/reports/2022-08-mimo
github_link: https://github.com/code-423n4/2022-08-mimo-findings/issues/123

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
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xDjango
---

## Vulnerability Title

[M-06] ProxyFactory can circumvent ProxyRegistry

### Overview


This bug report is about a vulnerability in the `deployFor()` function in `MIMOProxyFactory.sol`. The vulnerability allows users to create many MIMOProxies that are not registered within the registry. This means that certain actions such as leveraging and emptying the vault cannot be called. The issue was found through manual review.

To mitigate this vulnerability, it is recommended to add an `onlyRegistry` modifier to the `ProxyFactory.deployFor()` function. This will ensure that the factory deployFor function is called from the proxy registry.

### Original Finding Content

_Submitted by 0xDjango_

The `deployFor()` function in `MIMOProxyFactory.sol` can be called directly instead of being called within `MIMOProxyRegistry.sol`. This results in the ability to create many MIMOProxies that are not registered within the registry. The proxies deployed directly through the factory will lack the ability to call certain actions such as leveraging and emptying the vault, but will be able to call all functions in `MIMOVaultAction.sol`.

This inconsistency doesn't feel natural and would be remedied by adding an `onlyRegistry` modifier to the `ProxyFactory.deployFor()` function.

### Proof of Concept

`MIMOProxyFactory.deployFor()` lacking any access control:

      function deployFor(address owner) public override returns (IMIMOProxy proxy) {
        proxy = IMIMOProxy(mimoProxyBase.clone());
        proxy.initialize();


        // Transfer the ownership from this factory contract to the specified owner.
        proxy.transferOwnership(owner);


        // Mark the proxy as deployed.
        _proxies[address(proxy)] = true;


        // Log the proxy via en event.
        emit DeployProxy(msg.sender, owner, address(proxy));
      }
    }

Example of reduced functionality: `MIMOEmptyVault.executeOperation()` checks proxy existence in the proxy registry therefore can't be called.

      function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
      ) external override returns (bool) {
        (address owner, uint256 vaultId, SwapData memory swapData) = abi.decode(params, (address, uint256, SwapData));
        IMIMOProxy mimoProxy = IMIMOProxy(proxyRegistry.getCurrentProxy(owner));

### Recommended Mitigation Steps

Adding access control to ensure that the factory deployFor function is called from the proxy registry would mitigate this issue.

**[RnkSngh (Mimo) confirmed and commented](https://github.com/code-423n4/2022-08-mimo-findings/issues/123#issuecomment-1210553480):**
 > We confirm this is an issue and intend to implement a fix.

**horsefacts (warden) reviewed mitigation:**
> **Status:** ✅ Resolved

> **Finding:** Wardens identified that proxies could be deployed directly from the `MIMOProxyFactory` without being registered with the `MIMOProxyRegistry`.

> **What changed:** The `ProxyRegistry` contract has been removed, and registration functionality is now included in `MIMOProxyFactory`.<br>
> The [only mechanism](https://github.com/mimo-capital/2022-08-mimo/blob/4e579420ecbe3fc3e770996610e6ab66b0c8d15b/contracts/proxy/MIMOProxyFactory.sol#L47) for deploying a proxy is now to call `MIMOProxyFactory#deploy`.

> **Why it works:** Since there is only one code path to deploy a `MIMOProxy` and `MIMOProxyFactory` is the single source of truth for proxy registration, it is no longer possible to deploy an unregistered proxy as described in the finding.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mimo DeFi |
| Report Date | N/A |
| Finders | 0xDjango |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-mimo
- **GitHub**: https://github.com/code-423n4/2022-08-mimo-findings/issues/123
- **Contest**: https://code4rena.com/contests/2022-08-mimo-august-2022-contest

### Keywords for Search

`vulnerability`

