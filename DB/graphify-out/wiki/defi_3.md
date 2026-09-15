# defi 3

> 120 nodes · cohesion 0.25

## Key Concepts

- **Move Event Emission, Configuration & Upgrade Safety Vulnerabilities [MEDIUM]** (81 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 1: Missing Events for Critical State Changes — move-evtcfg-001 [MEDIUM]** (79 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Move State Management & Data Integrity Vulnerabilities [HIGH]** (77 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 10: Two-Step Ownership Transfer Missing — move-evtcfg-010 [MEDIUM]** (75 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 9: Version Check Missing in Upgrade-Sensitive Functions — move-evtcfg-009 [MEDIUM]** (75 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 7: Missing Approval Revocation Function — move-evtcfg-007 [MEDIUM]** (73 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 8: Dispatchable Token Store Missing withdraw/deposit Implementation — move-evtcfg-008 [MEDIUM]** (73 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 1: Local Copy Mutation Without Write-Back — move-state-001 [HIGH]** (73 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 11: Reentrancy via External Module Callback — move-evtcfg-011 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 12: Hardcoded Batch Parameters in Event Emission — move-evtcfg-012 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 13: Assertion Inconsistency Between Getter and Setter — move-evtcfg-013 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 2: Misleading Event Type in Emissions — move-evtcfg-002 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 3: Event Emission on No-Op State Change — move-evtcfg-003 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 4: Fee Annotation Mismatch with Actual Calculation — move-evtcfg-004 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 5: Liquidation Bonus Configuration Exceeding Bounds — move-evtcfg-005 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 6: Cooldown Bypass via Timestamp Manipulation — move-evtcfg-006 [MEDIUM]** (71 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 10: Last Modifier Tracking Failure — move-state-010 [HIGH]** (69 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 14: Inability to Withdraw Collected Fees — move-evtcfg-014 [MEDIUM]** (67 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 15: Front-Running Public Validation for Initialization — move-evtcfg-015 [MEDIUM]** (65 connections) — `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- **Pattern 11: Pause State Allowing Partial Operations — move-state-011 [HIGH]** (65 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 2: Variable Shadowing Zeroing State Values — move-state-002 [HIGH]** (65 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 3: Investor Count Arithmetic Mismatch — move-state-003 [HIGH]** (65 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 4: Wallet Balance Tracking Desync — move-state-004 [HIGH]** (65 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 5: Resource Attribute Cleanup on Removal — move-state-005 [HIGH]** (65 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- **Pattern 6: Group ID Reuse After Deletion — move-state-006 [HIGH]** (65 connections) — `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- *... and 95 more nodes in this community*

## Relationships

- [access-control](access-control.md) (39 shared connections)
- [general 4](general_4.md) (26 shared connections)
- [defi 8](defi_8.md) (19 shared connections)
- [defi 9](defi_9.md) (18 shared connections)
- [defi 4](defi_4.md) (16 shared connections)
- [general](general.md) (13 shared connections)
- [cosmos 6](cosmos_6.md) (7 shared connections)
- [defi 6](defi_6.md) (6 shared connections)
- [bridge](bridge.md) (5 shared connections)
- [cosmos 7](cosmos_7.md) (4 shared connections)
- [oracle](oracle.md) (2 shared connections)
- [cosmos](cosmos.md) (1 shared connections)

## Source Files

- `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`
- `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`
- `DB/cosmos/app-chain/rewards/reward-distribution-failures.md`
- `DB/general/access-control/defihacklabs-access-control-2024-2025.md`
- `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`
- `DB/general/reentrancy/reentrancy.md`
- `DB/general/restaking/LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md`
- `DB/general/restaking/RESTAKING_OPERATOR_DELEGATION_VULNERABILITIES.md`
- `DB/general/restaking/RESTAKING_REWARD_DISTRIBUTION_VULNERABILITIES.md`
- `DB/general/restaking/RESTAKING_SLASHING_VULNERABILITIES.md`
- `DB/unique/l1-misc/stacks/sbtc-coordinator-unvalidated-transaction-drain.md`

## Audit Trail

- EXTRACTED: 677 (35%)
- INFERRED: 1273 (65%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*