---
# Core Classification
protocol: GainsNetwork-February
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37790
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Lost roles after the proxy upgrade

### Overview


This report discusses a bug in the `GNSMultiCollatDiamond` contract where the `accessControl` mapping is located in a different storage slot in the new version compared to the current version. This change would result in the loss of all current roles information and make role-gated functionality inaccessible. However, no funds are at risk. The report recommends updating the storage in a way that would not change the location of current variables.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

In the current implementation of the `GNSMultiCollatDiamond` contract, the `accessControl` mapping takes slot `2` in the proxy storage:
[Link](https://arbiscan.io/address/0x1b7aeaeab4ffd6b3070ae601a038146b80c6ea8a#code#F20#L20)

The first two slots are taken by variables from the `Initializable` contract and by struct `Addresses` which currently holds only one address - `gns`.

But in the new version of the `GNSMultiCollatDiamond` contract, struct `Addresses` would take 2 more storage slots:

```solidity
File: IAddressStore.sol
15:     struct Addresses {
16:         address gns; // GNS token address
17:         address gnsStaking; // GNS staking address
18:         address linkErc677; // ERC677 LINK token address
19:     }
20:
21:     struct AddressStore {
22:         Addresses globalAddresses;
23:         mapping(address => mapping(Role => bool)) accessControl;
24:         uint256[47] __gap;
25:     }
```

This would put the `accessControl` mapping at slot `4`.
In Solidity mapping values are addressed based on the key and storage slot number that mapping takes, meaning addressing used in the current version of `GNSMultiCollatDiamond` would be changed in the new one. This would result in losing all current roles info since `hasRole` now would address `accessControl` mapping using storage slot `4` instead of `2`.

No funds would be at risk but all role-gated functionality would be inaccessible and a new upgrade of proxy that fixes the storage layout would be required.

Next foundry test could demonstrate the described issue:

```solidity
pragma solidity 0.8.23;

import "lib/forge-std/src/Test.sol";
import "contracts/core/GNSMultiCollatDiamond.sol";
import "node_modules/@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

contract Unit is Test {
    function setUp() public {}

    function test_UpgradeBrokeRoles() public {
        uint256 mainnetFork = vm.createFork("https://arb1.arbitrum.io/rpc");
        vm.selectFork(mainnetFork);

        // Fetch current proxy address
        ITransparentUpgradeableProxy proxyDiamond;
        proxyDiamond = ITransparentUpgradeableProxy(
            payable(0xFF162c694eAA571f685030649814282eA457f169)
            );

        // Check that address has manager role before upgrade
        bool _hasRole = GNSAddressStore(payable(address(proxyDiamond)))
            .hasRole(0x1632C38cB208df8409753729dBfbA5c58626F637, IAddressStore.Role.ROLES_MANAGER);

        GNSMultiCollatDiamond newDiamondImplementation;
        newDiamondImplementation = new GNSMultiCollatDiamond();
        // Upgrading diamond with new implementation
        vm.prank(0xe18be0113c38c91b3B429d04fDeb84359fBCb2eB);
        proxyDiamond.upgradeTo(address(newDiamondImplementation));

        // Check that address has manager role after upgrade
        bool hasRole_ = GNSAddressStore(payable(address(proxyDiamond)))
            .hasRole(0x1632C38cB208df8409753729dBfbA5c58626F637, IAddressStore.Role.ROLES_MANAGER);

        assertTrue(_hasRole == hasRole_, "Address should not lose role after upgrade");
    }
}
```

## Recommendations

Consider updating storage in a way that would not change the current variables' location, for example, `gnsStaking` and `linkErc677` could be added after the `accessControl` mapping.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-February |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

