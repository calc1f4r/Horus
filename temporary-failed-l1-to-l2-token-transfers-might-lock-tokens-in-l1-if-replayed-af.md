---
# Core Classification
protocol: Wonderland
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40343
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5295cf96-7a54-4150-9d94-396944b3604e
source_link: https://cdn.cantina.xyz/reports/cantina_wonderland_jul2024.pdf
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
finders_count: 4
finders:
  - shung
  - Optimum
  - 0xicingdeath
  - r0bert
---

## Vulnerability Title

Temporary failed L1 to L2 token transfers might lock tokens in L1 if replayed after migrating to native USDC 

### Overview


The L2OpUSDCBridgeAdapter contract is experiencing a bug that could potentially lock user funds in L1. This is due to a potential failure in the bridging mechanism, causing calls to USDC.mint to revert. To mitigate this issue, the report recommends implementing changes such as changing the isMessagingDisabled variable to an enum and moving the logic of the .sendMessage call to an internal function. The bug has been fixed by other projects by sending a message back to L1 to withdraw the funds or implementing the auditor's recommendation with slight changes. 

### Original Finding Content

## L2OpUSDCBridgeAdapter Overview

## Context
L2OpUSDCBridgeAdapter.sol#L205

## Description
The current system uses a well-known token bridging mechanism, locking tokens on one chain and minting them on the other. The `L2OpUSDCBridgeAdapter` contract is assigned the minter role within the bridged USDC contract. This role is intended to be revoked as part of the migration process as described in `bridged_USDC_standard.md`.

Additionally, the partner is expected to remove all configured minters prior to (or concurrently with) transferring the roles to Circle. Although unlikely, messages to Optimism L2 chains might fail due to business logic issues (e.g., pausing of the bridged USDC contract) or an out-of-gas exception on L2 (as described in `replaying-messages`). In the current system, this could cause calls to `USDC.mint` to revert. If messages are not replayed before migrating the bridged USDC contract to native USDC, any call to `USDC.mint` will revert since the bridged USDC minting permission was revoked for the `L2OpUSDCBridgeAdapter` contract. This will result in user funds being locked inside the `L1OpUSDCBridgeAdapter` contract in L1.

## Impact
High since users' funds will be locked in L1.

## Likelihood
Low since it is less likely that messages will have to be replayed and will be replayed only after the migration.

## Recommendation
To mitigate this issue, consider implementing the following changes in `L2OpUSDCBridgeAdapter`:

1. Change the `isMessagingDisabled` variable from a boolean to an enum with three values: `Active(0)`, `Paused(1)`, `Upgraded(2)`. Additionally, consider changing its name to `messengerStatus`.
2. Change `receiveMigrateToNative` to set the state of `messengerStatus` to `Upgraded` instead of setting `isMessagingDisabled` to true.
3. Change `receiveStopMessaging` and `receiveResumeMessaging` to change the `messengerStatus` from `Paused` to `Active` respectively.
4. Move the logic of the `.sendMessage` call and event emission of `MessageSent` from the two different implementations of `sendMessage` to an internal function named `_sendMessage`.
5. Change the `receiveMessage` function so that in case the `messengerStatus` is `Upgraded`, the call to `mint` will be wrapped in a try and catch clause where the catch block filters the cause for the failure. If it is equal to "FiatToken: caller is not a minter", then call `_sendMessage`, which will in turn call `receiveMessage` on L1 with `_user` and `_amount`.

> **Note**: This proposed solution is not perfect. In the rare case of multiple bridged USDC minters, users' tokens that remain locked on L1 might be permanently burned if Circle calls `burnLockedUSDC`.

## Wonderland
Fixed in commit `eb625f95` by sending a message back to L1 to withdraw to the original spender.

## Cantina Managed
Fixed by implementing the auditor's recommendation with slight changes that achieve the same result.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Wonderland |
| Report Date | N/A |
| Finders | shung, Optimum, 0xicingdeath, r0bert |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_wonderland_jul2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5295cf96-7a54-4150-9d94-396944b3604e

### Keywords for Search

`vulnerability`

