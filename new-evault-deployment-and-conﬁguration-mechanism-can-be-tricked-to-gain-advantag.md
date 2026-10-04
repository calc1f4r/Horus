---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54212
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Akshay Srivastav
---

## Vulnerability Title

New EVault deployment and conﬁguration mechanism can be tricked to gain advantages 

### Overview

See description below for full details.

### Original Finding Content

## Issue in EVault Deployment

## Context
`Initialize.sol#L20`

## Description
When a new EVault is deployed, all its configuration parameters do not get set in the deployment transaction. The governor needs to set them after the deployment using dedicated setter functions (like `setCaps`). In the meanwhile, nothing prevents a user from interacting with the vault. If a user interacts with the vault before the vault's configuration is complete, then the vault may behave differently than expected by the deployer.

### Some scenarios:
- User can become a depositor of a synthetic asset vault before `hookedOps` and `hookTarget` get set.
- In case the vault's security depends upon the hook call, then that can also be escaped.
- User can escape the supply cap by depositing before the supply cap is set.

## Impact & Likelihood
- The protocol intends for the ESynth to be the only depositor of a synthetic asset vault. However, by backrunning the vault's deployment, any user can become a depositor and break the original assumption of the protocol.
- We assume that vault creation and configuration will be done in an EVC batch, which eliminates this issue. However, nothing prevents deployers from interacting with `GenericFactory` directly, which exposes them to this problem. 

Considering the open nature of EulerV2 in the creation and management of EVaults, this issue can materialize in real life. Hence, medium severity is appropriate.

## Proof of Concept
A test case was added in `test/unit/esvault/ESVault.allocate.t.sol`. Also, add this statement at the top of the file:
```solidity
import {ESVaultTestBase, ESynth, IEVault} from "./ESVaultTestBase.t.sol";
```

### Test Case
```solidity
function test_poc_initialize() public {
    address user = makeAddr("user");
    assetTSTAsSynth.mint(user, 100); // Optionally, ESynth can be purchased from PSM as well
    // New Synthetic Asset Vault gets deployed
    IEVault esVault = IEVault(
        factory.createProxy(address(0), true, abi.encodePacked(address(assetTSTAsSynth), address(oracle), unitOfAccount))
    );
    
    assertEq(esVault.governorAdmin(), address(this));

    // Before admin sets other necessary parameters of Vault
    // (like `hookedOps` which prevent deposits of users into EsVault)
    // A user performs the deposit
    vm.startPrank(user);
    assetTSTAsSynth.approve(address(esVault), 100);
    esVault.deposit(100, user);
    assertEq(esVault.balanceOf(user), 100);
    // User becomes depositor of EsVault
    vm.stopPrank();
}
```

## Recommendation
Consider taking all configuration parameters of EVault as input from the `GenericFactory.createProxy` function. Alternatively, add a flag that can only be enabled by the governor, before which no user can interact with the vault.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

