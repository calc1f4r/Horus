# Hunt Card Enrichment Checklist

This is the durable DB-local tracker for report-backed hunt-card enrichment.
Generated hunt-card JSON must not be edited by hand; mark work complete only after fixing canonical `DB/**/*.md` source and regenerating manifests.

- Manifest source: `DB/manifests/huntcards/all-huntcards.json`
- Reports dir used for latest mapping: `not provided`
- Cards tracked: 1362
- Cards still missing explicit/strong report mapping: 578

## Status Legend

- `[x]` Source has report-backed triage fields and the card has explicit/strong report mapping.
- `[ ]` Source still needs report-backed enrichment or report mapping.

## Source File Checklist

### `DB/Solana-chain-specific/solana-program-security.md`

- [x] `solana-solana-program-security-1-account-validation-vulnerabi-000` (16/21) 1. Account Validation Vulnerabilities - lines [245, 502]
- [ ] `solana-solana-program-security-10-event-emission-vulnerabilit-009` (8/21) 10. Event Emission Vulnerabilities - lines [1654, 1741]
- [x] `solana-solana-program-security-11-arithmetic-and-data-handlin-010` (11/21) 11. Arithmetic and Data Handling Vulnerabilities - lines [1742, 1828]
- [ ] `solana-solana-program-security-12-seed-collision-vulnerabilit-011` (9/21) 12. Seed Collision Vulnerabilities - lines [1836, 1927]
- [x] `solana-solana-program-security-13-account-type-confusion-vuln-012` (10/21) 13. Account Type Confusion Vulnerabilities - lines [1928, 1979]
- [x] `solana-solana-program-security-14-ed25519-instruction-introsp-013` (11/21) 14. Ed25519 Instruction Introspection Vulnerabilities - lines [1980, 2069]
- [x] `solana-solana-program-security-15-signature-replay-attack-vul-014` (11/21) 15. Signature Replay Attack Vulnerabilities - lines [2070, 2163]
- [x] `solana-solana-program-security-16-unrestricted-cpi-vulnerabil-015` (9/21) 16. Unrestricted CPI Vulnerabilities - lines [2164, 2235]
- [x] `solana-solana-program-security-17-initialization-front-runnin-016` (10/21) 17. Initialization Front-Running Vulnerabilities - lines [2236, 2329]
- [x] `solana-solana-program-security-18-create-account-pre-funding--017` (11/21) 18. Create Account Pre-Funding DOS - lines [2330, 2409]
- [x] `solana-solana-program-security-19-rent-exemption-validation-e-018` (11/21) 19. Rent Exemption Validation Errors - lines [2410, 2469]
- [ ] `solana-solana-program-security-2-account-data-reallocation-vu-001` (11/21) 2. Account Data Reallocation Vulnerabilities - lines [503, 617]
- [x] `solana-solana-program-security-20-liquidation-and-state-invar-019` (13/21) 20. Liquidation and State Invariant Vulnerabilities - lines [2470, 2602]
- [x] `solana-solana-program-security-21-cpi-policy-and-program-upgr-020` (13/21) 21. CPI Policy and Program Upgradeability Bypass - lines [2603, 2689]
- [ ] `solana-solana-program-security-3-lamports-transfer-from-pda-v-002` (10/21) 3. Lamports Transfer from PDA Vulnerabilities - lines [618, 745]
- [ ] `solana-solana-program-security-4-cpi-cross-program-invocation-003` (11/21) 4. CPI (Cross-Program Invocation) Vulnerabilities - lines [746, 943]
- [ ] `solana-solana-program-security-5-unvalidated-account-vulnerab-004` (9/21) 5. Unvalidated Account Vulnerabilities - lines [944, 1152]
- [ ] `solana-solana-program-security-6-account-reloading-vulnerabil-005` (11/21) 6. Account Reloading Vulnerabilities - lines [1153, 1245]
- [ ] `solana-solana-program-security-7-account-closure-vulnerabilit-006` (9/21) 7. Account Closure Vulnerabilities - lines [1246, 1393]
- [x] `solana-solana-program-security-8-dos-attack-vectors-007` (12/21) 8. DOS Attack Vectors - lines [1394, 1506]
- [x] `solana-solana-program-security-9-mint-token-extension-vulnera-008` (12/21) 9. Mint & Token Extension Vulnerabilities - lines [1507, 1653]

Progress: 13/21 cards source-enriched for this file.

### `DB/Solana-chain-specific/token-2022-extensions.md`

- [x] `solana-token-2022-extensions-1-mintcloseauthority-extension-000` (15/21) 1. MintCloseAuthority Extension Vulnerabilities - lines [183, 382]
- [ ] `solana-token-2022-extensions-11-non-transferable-token-exte-011` (10/21) 11. Non-Transferable Token Extension Vulnerabilities - lines [1204, 1277]
- [ ] `solana-token-2022-extensions-12-confidential-transfer-exten-012` (12/21) 12. Confidential Transfer Extension Vulnerabilities - lines [1278, 1333]
- [ ] `solana-token-2022-extensions-13-metadata-pointer-extension--013` (9/21) 13. Metadata Pointer Extension Vulnerabilities - lines [1334, 1372]
- [ ] `solana-token-2022-extensions-15-cpi-guard-extension-vulnera-015` (10/21) 15. CPI Guard Extension Vulnerabilities - lines [1408, 1483]
- [ ] `solana-token-2022-extensions-18-comprehensive-token-2022-ex-018` (8/21) 18. Comprehensive Token-2022 Extension Whitelist Pattern - lines [1564, 1666]
- [x] `solana-token-2022-extensions-2-freeze-authority-vulnerabili-001` (14/21) 2. Freeze Authority Vulnerabilities - lines [383, 529]
- [x] `solana-token-2022-extensions-3-transfer-fee-extension-vulne-002` (14/21) 3. Transfer Fee Extension Vulnerabilities - lines [530, 708]
- [ ] `solana-token-2022-extensions-4-permanent-delegate-extension-003` (13/21) 4. Permanent Delegate Extension Vulnerabilities - lines [709, 776]
- [x] `solana-token-2022-extensions-5-token-account-size-vulnerabi-004` (12/21) 5. Token Account Size Vulnerabilities - lines [777, 846]
- [ ] `solana-token-2022-extensions-6-default-account-state-extens-005` (7/21) 6. Default Account State Extension Vulnerabilities - lines [847, 890]
- [ ] `solana-token-2022-extensions-7-transfer-hook-extension-vuln-006` (10/21) 7. Transfer Hook Extension Vulnerabilities - lines [891, 949]
- [ ] `solana-token-2022-extensions-8-interest-bearing-extension-v-007` (12/21) 8. Interest Bearing Extension Vulnerabilities - lines [950, 1046]
- [ ] `solana-token-2022-extensions-token-2022-extension-quick-ref-010` (6/21) Token-2022 Extension Quick Reference - lines [1167, 1182]

Progress: 4/14 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md`

- [ ] `sui-move-move-access-control-authorization-vulner-move-access-control-and-author-000` (11/21) Move Access Control and Authorization Vulnerabilities - lines [80, 137]
- [ ] `sui-move-move-access-control-authorization-vulner-pattern-4-missing-capability-r-007` (8/21) Pattern 4: Missing Capability Revocation - move-acl-004 - lines [363, 416]
- [ ] `sui-move-move-access-control-authorization-vulner-pattern-6-unverified-object-po-010` (8/21) Pattern 6: Unverified Object/Pool Instance in Operations - move-acl-006 - lines [477, 523]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-002` (6/21) Vulnerable Pattern Example - lines [150, 192]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-004` (6/21) Vulnerable Pattern Example - lines [221, 263]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-006` (6/21) Vulnerable Pattern Example - lines [300, 341]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-009` (6/21) Vulnerable Pattern Example - lines [429, 455]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-012` (8/21) Vulnerable Pattern Example - lines [536, 547]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-014` (6/21) Vulnerable Pattern Example - lines [572, 586]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-016` (6/21) Vulnerable Pattern Example - lines [616, 627]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-018` (6/21) Vulnerable Pattern Example - lines [651, 669]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-020` (6/21) Vulnerable Pattern Example - lines [705, 719]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-022` (6/21) Vulnerable Pattern Example - lines [747, 762]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-024` (6/21) Vulnerable Pattern Example - lines [788, 800]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-026` (6/21) Vulnerable Pattern Example - lines [827, 851]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-028` (6/21) Vulnerable Pattern Example - lines [877, 893]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-030` (6/21) Vulnerable Pattern Example - lines [926, 936]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-032` (6/21) Vulnerable Pattern Example - lines [962, 972]
- [ ] `sui-move-move-access-control-authorization-vulner-vulnerable-pattern-example-034` (6/21) Vulnerable Pattern Example - lines [997, 1011]

Progress: 0/19 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md`

- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-move-arithmetic-and-precision--000` (11/21) Move Arithmetic and Precision Vulnerabilities - lines [84, 136]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-pattern-7-faulty-constant-defi-013` (7/21) Pattern 7: Faulty Constant Definitions - move-arith-007 - lines [530, 573]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-pattern-8-fee-accounting-denom-014` (9/21) Pattern 8: Fee Accounting Denomination Errors - move-arith-008 - lines [574, 629]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-002` (6/21) Vulnerable Pattern Example - lines [149, 197]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-004` (6/21) Vulnerable Pattern Example - lines [236, 264]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-006` (6/21) Vulnerable Pattern Example - lines [291, 324]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-008` (6/21) Vulnerable Pattern Example - lines [357, 384]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-010` (6/21) Vulnerable Pattern Example - lines [421, 441]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-012` (6/21) Vulnerable Pattern Example - lines [467, 505]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-016` (6/21) Vulnerable Pattern Example - lines [642, 672]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-018` (6/21) Vulnerable Pattern Example - lines [701, 720]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-020` (6/21) Vulnerable Pattern Example - lines [748, 769]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-022` (6/21) Vulnerable Pattern Example - lines [793, 806]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-024` (6/21) Vulnerable Pattern Example - lines [831, 849]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-026` (6/21) Vulnerable Pattern Example - lines [873, 888]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-028` (6/21) Vulnerable Pattern Example - lines [917, 943]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-030` (6/21) Vulnerable Pattern Example - lines [969, 988]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-032` (6/21) Vulnerable Pattern Example - lines [1012, 1032]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-034` (6/21) Vulnerable Pattern Example - lines [1056, 1065]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-036` (6/21) Vulnerable Pattern Example - lines [1089, 1104]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-038` (8/21) Vulnerable Pattern Example - lines [1133, 1147]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-040` (6/21) Vulnerable Pattern Example - lines [1172, 1190]
- [ ] `sui-move-move-arithmetic-precision-vulnerabilitie-vulnerable-pattern-example-042` (6/21) Vulnerable Pattern Example - lines [1217, 1229]

Progress: 0/23 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md`

- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-move-cross-chain-and-bridge-vu-000` (12/21) Move Cross-Chain and Bridge Vulnerabilities - lines [76, 138]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-10-inconsistent-deadli-013` (7/21) Pattern 10: Inconsistent Deadline Checks Across Chains - move-bridge-010 - lines [658, 690]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-11-zero-value-burn-wit-014` (9/21) Pattern 11: Zero-Value Burn Without Supply Validation - move-bridge-011 - lines [691, 733]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-12-deserialization-acc-015` (12/21) Pattern 12: Deserialization Access Control Bypass - move-bridge-012 - lines [734, 860]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-2-missing-validator-se-003` (7/21) Pattern 2: Missing Validator Set Integrity Checks - move-bridge-002 - lines [207, 276]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-4-unrestricted-cross-c-006` (9/21) Pattern 4: Unrestricted Cross-Chain Message Sending - move-bridge-004 - lines [365, 419]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-5-signature-replay-in--007` (7/21) Pattern 5: Signature Replay in Cross-Chain Claims - move-bridge-005 - lines [420, 483]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-7-missing-version-chec-010` (7/21) Pattern 7: Missing Version Check in Admin Functions - move-bridge-007 - lines [540, 571]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-8-cross-chain-replay-f-011` (7/21) Pattern 8: Cross-Chain Replay from Missing Chain ID - move-bridge-008 - lines [572, 617]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-pattern-9-transceiver-id-overf-012` (7/21) Pattern 9: Transceiver ID Overflow Past Bitmap Limit - move-bridge-009 - lines [618, 657]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-vulnerable-pattern-example-002` (6/21) Vulnerable Pattern Example - lines [153, 182]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-vulnerable-pattern-example-005` (6/21) Vulnerable Pattern Example - lines [290, 333]
- [ ] `sui-move-move-cross-chain-bridge-vulnerabilities-vulnerable-pattern-example-009` (6/21) Vulnerable Pattern Example - lines [497, 517]

Progress: 0/13 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md`

- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-move-defi-protocol-logic-vulne-000` (11/21) Move DeFi Protocol Logic Vulnerabilities - lines [88, 140]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-pattern-3-flashloan-repayment--005` (7/21) Pattern 3: Flashloan Repayment Bypass via Double Scaling - move-defi-003 - lines [272, 318]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-pattern-4-excessive-claims-via-006` (9/21) Pattern 4: Excessive Claims via Missing Cumulative Tracking - move-defi-004 - lines [319, 380]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-pattern-5-fee-accounting-misma-007` (7/21) Pattern 5: Fee Accounting Mismatch - move-defi-005 - lines [381, 451]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-pattern-6-forced-withdrawal-to-008` (10/21) Pattern 6: Forced Withdrawal Tolerance Bypass - move-defi-006 - lines [452, 514]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-pattern-7-state-desynchronizat-009` (8/21) Pattern 7: State Desynchronization Between Modules - move-defi-007 - lines [515, 558]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-pattern-8-permissionless-front-010` (7/21) Pattern 8: Permissionless Front-Running of Auctions/Orders - move-defi-008 - lines [559, 623]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-pattern-9-incorrect-withdrawal-011` (7/21) Pattern 9: Incorrect Withdrawal/Vesting Abort Conditions - move-defi-009 - lines [624, 686]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-002` (8/21) Vulnerable Pattern Example - lines [154, 182]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-004` (6/21) Vulnerable Pattern Example - lines [209, 247]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-013` (6/21) Vulnerable Pattern Example - lines [699, 717]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-015` (6/21) Vulnerable Pattern Example - lines [743, 756]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-017` (6/21) Vulnerable Pattern Example - lines [785, 801]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-019` (9/21) Vulnerable Pattern Example - lines [827, 838]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-021` (6/21) Vulnerable Pattern Example - lines [862, 877]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-023` (6/21) Vulnerable Pattern Example - lines [906, 918]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-025` (6/21) Vulnerable Pattern Example - lines [946, 967]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-027` (6/21) Vulnerable Pattern Example - lines [994, 1007]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-029` (6/21) Vulnerable Pattern Example - lines [1034, 1049]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-031` (6/21) Vulnerable Pattern Example - lines [1081, 1094]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-033` (6/21) Vulnerable Pattern Example - lines [1123, 1136]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-035` (6/21) Vulnerable Pattern Example - lines [1162, 1178]
- [ ] `sui-move-move-defi-protocol-logic-vulnerabilities-vulnerable-pattern-example-037` (6/21) Vulnerable Pattern Example - lines [1205, 1218]

Progress: 0/23 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_DENIAL_OF_SERVICE_VULNERABILITIES.md`

- [ ] `sui-move-move-denial-of-service-vulnerabilities-move-denial-of-service-vulnera-000` (11/21) Move Denial of Service Vulnerabilities - lines [85, 137]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-10-hash-collision-buck-012` (7/21) Pattern 10: Hash Collision Bucket Overload - move-dos-010 - lines [654, 692]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-11-division-by-zero-on-013` (7/21) Pattern 11: Division by Zero on Empty State - move-dos-011 - lines [693, 726]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-12-front-running-deplo-014` (7/21) Pattern 12: Front-Running Deployment Blocking Initialization - move-dos-012 - lines [727, 762]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-13-epoch-transition-im-015` (8/21) Pattern 13: Epoch Transition Imbalance Abort - move-dos-013 - lines [763, 799]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-14-unnecessary-asserti-016` (8/21) Pattern 14: Unnecessary Assertion Causing Protocol Lockup - move-dos-014 - lines [800, 834]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-15-object-size-limit-e-017` (8/21) Pattern 15: Object Size Limit Exceeded - move-dos-015 - lines [835, 877]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-16-zero-value-deposit--018` (8/21) Pattern 16: Zero-Value Deposit Disabling Withdrawals - move-dos-016 - lines [878, 917]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-17-mint-limit-exhausti-019` (10/21) Pattern 17: Mint Limit Exhaustion via Cycling - move-dos-017 - lines [918, 952]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-18-commission-rate-ove-020` (10/21) Pattern 18: Commission Rate Overflow Blocking Epoch - move-dos-018 - lines [953, 1081]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-3-event-object-limit-e-005` (8/21) Pattern 3: Event/Object Limit Exhaustion - move-dos-003 - lines [305, 368]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-4-division-by-zero-in--006` (9/21) Pattern 4: Division by Zero in Pool/Epoch Operations - move-dos-004 - lines [369, 429]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-5-hash-collision-dos-i-007` (8/21) Pattern 5: Hash Collision DoS in Address-Keyed Tables - move-dos-005 - lines [430, 464]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-6-overflow-abort-in-ar-008` (9/21) Pattern 6: Overflow Abort in Arithmetic Operations - move-dos-006 - lines [465, 522]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-7-mint-rate-limit-exha-009` (8/21) Pattern 7: Mint/Rate Limit Exhaustion - move-dos-007 - lines [523, 561]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-8-missing-parameter-va-010` (7/21) Pattern 8: Missing Parameter Validation Causing Protocol Halt - move-dos-008 - lines [562, 606]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-pattern-9-unbounded-map-growth-011` (8/21) Pattern 9: Unbounded Map Growth in Reward Tracking - move-dos-009 - lines [607, 653]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-vulnerable-pattern-example-002` (6/21) Vulnerable Pattern Example - lines [150, 195]
- [ ] `sui-move-move-denial-of-service-vulnerabilities-vulnerable-pattern-example-004` (6/21) Vulnerable Pattern Example - lines [233, 274]

Progress: 0/19 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_EVENT_CONFIGURATION_VULNERABILITIES.md`

- [ ] `sui-move-move-event-configuration-vulnerabilities-move-event-emission-configurat-000` (11/21) Move Event Emission, Configuration & Upgrade Safety Vulnerabilities - lines [86, 125]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-1-missing-events-for-c-001` (8/21) Pattern 1: Missing Events for Critical State Changes - move-evtcfg-001 - lines [126, 177]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-10-two-step-ownership--010` (7/21) Pattern 10: Two-Step Ownership Transfer Missing - move-evtcfg-010 - lines [493, 532]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-11-reentrancy-via-exte-011` (7/21) Pattern 11: Reentrancy via External Module Callback - move-evtcfg-011 - lines [533, 572]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-12-hardcoded-batch-par-012` (8/21) Pattern 12: Hardcoded Batch Parameters in Event Emission - move-evtcfg-012 - lines [573, 636]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-13-assertion-inconsist-013` (8/21) Pattern 13: Assertion Inconsistency Between Getter and Setter - move-evtcfg-013 - lines [637, 677]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-14-inability-to-withdr-014` (8/21) Pattern 14: Inability to Withdraw Collected Fees - move-evtcfg-014 - lines [678, 718]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-15-front-running-publi-015` (10/21) Pattern 15: Front-Running Public Validation for Initialization - move-evtcfg-015 - lines [719, 850]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-2-misleading-event-typ-002` (7/21) Pattern 2: Misleading Event Type in Emissions - move-evtcfg-002 - lines [178, 224]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-3-event-emission-on-no-003` (7/21) Pattern 3: Event Emission on No-Op State Change - move-evtcfg-003 - lines [225, 258]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-4-fee-annotation-misma-004` (7/21) Pattern 4: Fee Annotation Mismatch with Actual Calculation - move-evtcfg-004 - lines [259, 292]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-5-liquidation-bonus-co-005` (7/21) Pattern 5: Liquidation Bonus Configuration Exceeding Bounds - move-evtcfg-005 - lines [293, 336]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-6-cooldown-bypass-via--006` (7/21) Pattern 6: Cooldown Bypass via Timestamp Manipulation - move-evtcfg-006 - lines [337, 372]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-7-missing-approval-rev-007` (7/21) Pattern 7: Missing Approval Revocation Function - move-evtcfg-007 - lines [373, 412]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-8-dispatchable-token-s-008` (9/21) Pattern 8: Dispatchable Token Store Missing withdraw/deposit Implementation - move-evtcfg-008 - lines [413, 454]
- [ ] `sui-move-move-event-configuration-vulnerabilities-pattern-9-version-check-missin-009` (7/21) Pattern 9: Version Check Missing in Upgrade-Sensitive Functions - move-evtcfg-009 - lines [455, 492]

Progress: 0/16 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`

- [ ] `sui-move-move-merkle-verification-vulnerabilities-move-merkle-proof-verification-000` (11/21) Move Merkle Proof Verification Vulnerabilities - lines [68, 118]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-pattern-4-fee-bypass-at-maximu-007` (7/21) Pattern 4: Fee Bypass at Maximum Fee Setting - move-merkle-004 - lines [334, 369]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-pattern-5-missing-domain-separ-008` (7/21) Pattern 5: Missing Domain Separation Between Leaf and Internal Nodes - move-merkle-005 - lines [370, 427]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-pattern-6-resource-index-colli-009` (7/21) Pattern 6: Resource Index Collision Enabling Claim Spoofing - move-merkle-006 - lines [428, 470]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-pattern-7-odd-length-proof-pad-010` (9/21) Pattern 7: Odd-Length Proof Padding Bypass - move-merkle-007 - lines [471, 515]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-pattern-8-bitmap-claim-trackin-011` (13/21) Pattern 8: Bitmap Claim Tracking Overflow - move-merkle-008 - lines [516, 637]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-vulnerable-pattern-example-002` (6/21) Vulnerable Pattern Example - lines [132, 161]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-vulnerable-pattern-example-004` (6/21) Vulnerable Pattern Example - lines [204, 236]
- [ ] `sui-move-move-merkle-verification-vulnerabilities-vulnerable-pattern-example-006` (6/21) Vulnerable Pattern Example - lines [280, 308]

Progress: 0/9 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_ORACLE_PRICING_VULNERABILITIES.md`

- [ ] `sui-move-move-oracle-pricing-vulnerabilities-move-oracle-and-pricing-vulner-000` (11/21) Move Oracle and Pricing Vulnerabilities - lines [79, 132]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-10-undervalued-collate-014` (8/21) Pattern 10: Undervalued Collateral from Naive LPT Pricing - move-oracle-010 - lines [537, 575]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-11-duplicate-source-id-015` (7/21) Pattern 11: Duplicate Source ID Corrupting Price Aggregation - move-oracle-011 - lines [576, 620]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-12-custom-price-exceed-016` (8/21) Pattern 12: Custom Price Exceeding Oracle Price Cap - move-oracle-012 - lines [621, 654]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-13-confidence-before-t-017` (10/21) Pattern 13: Confidence-Before-Timestamp Ordering Error - move-oracle-013 - lines [655, 782]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-5-incorrect-price-boun-009` (7/21) Pattern 5: Incorrect Price Boundary Checks - move-oracle-005 - lines [358, 387]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-6-faulty-constant-defi-010` (7/21) Pattern 6: Faulty Constant Definition - move-oracle-006 - lines [388, 424]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-7-unauthorized-price-f-011` (7/21) Pattern 7: Unauthorized Price Feed Registration - move-oracle-007 - lines [425, 464]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-8-fixed-point-arithmet-012` (8/21) Pattern 8: Fixed-Point Arithmetic Sign Bit Confusion - move-oracle-008 - lines [465, 497]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-pattern-9-oracle-not-updated-w-013` (8/21) Pattern 9: Oracle Not Updated When Tick Unchanged but Price Changes - move-oracle-009 - lines [498, 536]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-vulnerable-pattern-example-002` (6/21) Vulnerable Pattern Example - lines [146, 164]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-vulnerable-pattern-example-004` (6/21) Vulnerable Pattern Example - lines [200, 222]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-vulnerable-pattern-example-006` (6/21) Vulnerable Pattern Example - lines [252, 275]
- [ ] `sui-move-move-oracle-pricing-vulnerabilities-vulnerable-pattern-example-008` (8/21) Vulnerable Pattern Example - lines [313, 334]

Progress: 0/14 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_STATE_MANAGEMENT_VULNERABILITIES.md`

- [ ] `sui-move-move-state-management-vulnerabilities-move-state-management-data-int-000` (11/21) Move State Management & Data Integrity Vulnerabilities - lines [82, 123]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-1-local-copy-mutation--001` (7/21) Pattern 1: Local Copy Mutation Without Write-Back - move-state-001 - lines [124, 154]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-10-last-modifier-track-010` (7/21) Pattern 10: Last Modifier Tracking Failure - move-state-010 - lines [483, 520]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-11-pause-state-allowin-011` (7/21) Pattern 11: Pause State Allowing Partial Operations - move-state-011 - lines [521, 565]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-12-token-metadata-swap-012` (10/21) Pattern 12: Token Metadata Swap Between Objects - move-state-012 - lines [566, 698]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-2-variable-shadowing-z-002` (8/21) Pattern 2: Variable Shadowing Zeroing State Values - move-state-002 - lines [155, 189]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-3-investor-count-arith-003` (9/21) Pattern 3: Investor Count Arithmetic Mismatch - move-state-003 - lines [190, 226]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-4-wallet-balance-track-004` (7/21) Pattern 4: Wallet Balance Tracking Desync - move-state-004 - lines [227, 269]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-5-resource-attribute-c-005` (8/21) Pattern 5: Resource Attribute Cleanup on Removal - move-state-005 - lines [270, 308]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-6-group-id-reuse-after-006` (7/21) Pattern 6: Group ID Reuse After Deletion - move-state-006 - lines [309, 358]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-7-storage-split-accoun-007` (7/21) Pattern 7: Storage Split Accounting Inconsistency - move-state-007 - lines [359, 399]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-8-stale-share-rate-in--008` (8/21) Pattern 8: Stale Share Rate in Multi-Step Operations - move-state-008 - lines [400, 438]
- [ ] `sui-move-move-state-management-vulnerabilities-pattern-9-missing-default-grou-009` (7/21) Pattern 9: Missing Default Group Assignment - move-state-009 - lines [439, 482]

Progress: 0/13 cards source-enriched for this file.

### `DB/Sui-Move-specific/MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md`

- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-move-token-supply-and-inflatio-000` (11/21) Move Token Supply and Inflation Vulnerabilities - lines [78, 129]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-10-peg-inconsistency-f-012` (11/21) Pattern 10: Peg Inconsistency from Unbounded Burn/Mint - move-inflate-010 - lines [611, 652]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-11-uncapped-derivative-013` (7/21) Pattern 11: Uncapped Derivative Token Minting - move-inflate-011 - lines [653, 687]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-12-kapt-double-minting-014` (12/21) Pattern 12: kAPT Double Minting from Fee Mismatch - move-inflate-012 - lines [688, 819]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-3-uncapped-share-token-005` (10/21) Pattern 3: Uncapped Share/Token Minting - move-inflate-003 - lines [282, 344]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-4-permanent-freeze-wit-006` (7/21) Pattern 4: Permanent Freeze Without Unfreeze - move-inflate-004 - lines [345, 391]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-5-improper-mint-limit--007` (8/21) Pattern 5: Improper Mint Limit Reset Logic - move-inflate-005 - lines [392, 436]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-6-missing-activation-e-008` (7/21) Pattern 6: Missing Activation Epoch Check in Staking - move-inflate-006 - lines [437, 469]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-7-unbacked-equity-shar-009` (9/21) Pattern 7: Unbacked Equity Share Minting on Zero Registry - move-inflate-007 - lines [470, 514]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-8-debt-share-dilution--010` (8/21) Pattern 8: Debt Share Dilution on Zero Liability - move-inflate-008 - lines [515, 561]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-pattern-9-inflation-attack-on--011` (7/21) Pattern 9: Inflation Attack on Zero Total Stake - move-inflate-009 - lines [562, 610]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-vulnerable-pattern-example-002` (6/21) Vulnerable Pattern Example - lines [144, 186]
- [ ] `sui-move-move-token-supply-inflation-vulnerabilit-vulnerable-pattern-example-004` (8/21) Vulnerable Pattern Example - lines [225, 262]

Progress: 0/13 cards source-enriched for this file.

### `DB/Sui-Move-specific/SUI_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md`

- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-1-evm-state-persistence-despit-000` (13/21) 1. EVM State Persistence Despite Sui Failure - lines [142, 252]
- [ ] `sui-move-sui-cross-chain-bridge-vulnerabilities-10-blocklist-iterator-state-bu-009` (8/21) 10. Blocklist Iterator State Bug - lines [591, 603]
- [ ] `sui-move-sui-cross-chain-bridge-vulnerabilities-11-cross-chain-flow-rate-direc-010` (8/21) 11. Cross-Chain Flow Rate Direction Mismatch - lines [604, 616]
- [ ] `sui-move-sui-cross-chain-bridge-vulnerabilities-12-wrong-integration-function--011` (8/21) 12. Wrong Integration Function Call - lines [617, 629]
- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-2-outbound-nonce-manipulation--001` (9/21) 2. Outbound Nonce Manipulation DoS - lines [253, 296]
- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-3-sui-node-dos-blocks-intx-obs-002` (8/21) 3. Sui Node DoS Blocks InTx Observation - lines [297, 351]
- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-4-missing-receiver-module-vali-003` (10/21) 4. Missing Receiver Module Validation - lines [352, 404]
- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-5-improper-coin-type-validatio-004` (10/21) 5. Improper Coin Type Validation - lines [405, 442]
- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-6-duplicate-cctx-re-signing-005` (9/21) 6. Duplicate CCTX Re-signing - lines [443, 488]
- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-7-tss-fund-drainage-via-gas-ma-006` (10/21) 7. TSS Fund Drainage via Gas Manipulation - lines [489, 535]
- [x] `sui-move-sui-cross-chain-bridge-vulnerabilities-8-wrong-gas-price-for-outbound-007` (9/21) 8. Wrong Gas Price for Outbound Transactions - lines [536, 577]
- [ ] `sui-move-sui-cross-chain-bridge-vulnerabilities-9-epoch-transition-failure-via-008` (8/21) 9. Epoch Transition Failure via Duplicate PubKey - lines [578, 590]

Progress: 8/12 cards source-enriched for this file.

### `DB/Sui-Move-specific/SUI_MOVE_ACCESS_CONTROL_VALIDATION_VULNERABILITIES.md`

- [x] `sui-move-sui-move-access-control-validation-vulne-1-public-vs-public-package-vis-000` (13/21) 1. Public vs Public(package) Visibility Misuse - lines [176, 264]
- [x] `sui-move-sui-move-access-control-validation-vulne-10-repeated-invocation-replay-009` (8/21) 10. Repeated Invocation / Replay - lines [659, 708]
- [x] `sui-move-sui-move-access-control-validation-vulne-11-inconsistent-assert-conditi-010` (8/21) 11. Inconsistent Assert Conditions - lines [709, 745]
- [ ] `sui-move-sui-move-access-control-validation-vulne-12-missing-range-bounds-valida-011` (9/21) 12. Missing Range / Bounds Validation - lines [746, 801]
- [x] `sui-move-sui-move-access-control-validation-vulne-13-mint-limit-exhaustion-dos-012` (10/21) 13. Mint Limit Exhaustion DoS - lines [802, 842]
- [x] `sui-move-sui-move-access-control-validation-vulne-14-excessive-gas-consumption-d-013` (8/21) 14. Excessive Gas Consumption DoS - lines [843, 886]
- [x] `sui-move-sui-move-access-control-validation-vulne-15-snapshot-integrity-bypass-014` (9/21) 15. Snapshot Integrity Bypass - lines [887, 933]
- [x] `sui-move-sui-move-access-control-validation-vulne-16-missing-invariant-enforceme-015` (8/21) 16. Missing Invariant Enforcement - lines [934, 978]
- [x] `sui-move-sui-move-access-control-validation-vulne-18-price-manipulation-via-miss-017` (9/21) 18. Price Manipulation via Missing Guards - lines [991, 1030]
- [x] `sui-move-sui-move-access-control-validation-vulne-2-missing-owner-authority-chec-001` (10/21) 2. Missing Owner/Authority Check - lines [265, 319]
- [x] `sui-move-sui-move-access-control-validation-vulne-3-missing-object-uid-id-valida-002` (10/21) 3. Missing Object UID/ID Validation - lines [320, 371]
- [x] `sui-move-sui-move-access-control-validation-vulne-4-trade-proof-capability-bypas-003` (10/21) 4. Trade Proof / Capability Bypass - lines [372, 414]
- [x] `sui-move-sui-move-access-control-validation-vulne-5-flash-loan-receipt-manipulat-004` (8/21) 5. Flash Loan Receipt Manipulation - lines [415, 471]
- [x] `sui-move-sui-move-access-control-validation-vulne-6-missing-zk-proof-verificatio-005` (9/21) 6. Missing ZK Proof Verification - lines [472, 518]
- [x] `sui-move-sui-move-access-control-validation-vulne-7-signature-length-format-vali-006` (10/21) 7. Signature Length / Format Validation - lines [519, 564]
- [x] `sui-move-sui-move-access-control-validation-vulne-8-security-level-constraint-by-007` (12/21) 8. Security Level Constraint Bypass - lines [565, 620]
- [x] `sui-move-sui-move-access-control-validation-vulne-9-unsafe-role-removal-008` (12/21) 9. Unsafe Role Removal - lines [621, 658]

Progress: 16/17 cards source-enriched for this file.

### `DB/Sui-Move-specific/SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md`

- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-1-clmm-sqrt-price-overflow-000` (16/21) 1. CLMM Sqrt-Price Overflow - lines [158, 314]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-10-share-price-inflation-first-009` (12/21) 10. Share Price Inflation / First-Depositor Attack - lines [630, 699]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-11-share-to-asset-rounding-dir-010` (11/21) 11. Share-to-Asset Rounding Direction - lines [700, 742]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-12-incorrect-price-scaling-con-011` (10/21) 12. Incorrect Price Scaling / Conversion - lines [743, 778]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-13-incorrect-quantity-calculat-012` (10/21) 13. Incorrect Quantity Calculation in Order Books - lines [779, 824]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-14-reward-period-miscalculatio-013` (8/21) 14. Reward Period Miscalculation - lines [825, 870]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-15-improper-integer-type-conve-014` (8/21) 15. Improper Integer Type Conversion - lines [871, 906]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-3-bigvector-container-size-ove-002` (9/21) 3. BigVector / Container Size Overflow - lines [323, 354]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-4-accumulator-volume-counter-o-003` (11/21) 4. Accumulator / Volume Counter Overflow - lines [355, 396]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-5-type-boundary-overflow-u64-u-004` (10/21) 5. Type Boundary Overflow (u64 -> u128) - lines [397, 438]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-6-rpc-node-crash-overflow-005` (9/21) 6. RPC / Node-Crash Overflow - lines [439, 480]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-7-faulty-constant-definitions-006` (8/21) 7. Faulty Constant Definitions - lines [481, 529]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-8-precision-loss-in-token-redi-007` (9/21) 8. Precision Loss in Token Redistribution - lines [530, 579]
- [x] `sui-move-sui-move-arithmetic-precision-vulnerabil-9-reward-calculation-rounding--008` (8/21) 9. Reward Calculation Rounding Errors - lines [580, 629]

Progress: 14/14 cards source-enriched for this file.

### `DB/Sui-Move-specific/SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md`

- [x] `sui-move-sui-move-defi-logic-vulnerabilities-1-improper-stake-accounting-up-000` (13/21) 1. Improper Stake Accounting Updates - lines [162, 235]
- [ ] `sui-move-sui-move-defi-logic-vulnerabilities-10-liquid-staking-share-roundi-009` (8/21) 10. Liquid Staking: Share Rounding Direction - lines [558, 570]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-11-order-book-base-quote-quant-010` (9/21) 11. Order Book: Base/Quote Quantity Mismatch - lines [571, 608]
- [ ] `sui-move-sui-move-defi-logic-vulnerabilities-12-order-book-partial-fill-tra-011` (8/21) 12. Order Book: Partial Fill Tracking - lines [609, 621]
- [ ] `sui-move-sui-move-defi-logic-vulnerabilities-13-share-price-manipulation-vi-012` (7/21) 13. Share Price Manipulation via Donation - lines [622, 649]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-14-share-price-inflation-via-r-013` (9/21) 14. Share Price Inflation via Rounding Drift - lines [650, 693]
- [ ] `sui-move-sui-move-defi-logic-vulnerabilities-15-exchange-rate-manipulation--014` (8/21) 15. Exchange Rate Manipulation at Low TVL - lines [694, 721]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-2-tank-stability-pool-value-up-001` (11/21) 2. Tank/Stability Pool Value Update Errors - lines [236, 275]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-3-surplus-claim-logic-failure-002` (9/21) 3. Surplus Claim Logic Failure - lines [276, 319]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-4-incorrect-flow-rate-tracking-003` (8/21) 4. Incorrect Flow Rate Tracking - lines [320, 359]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-5-wrong-function-call-in-integ-004` (9/21) 5. Wrong Function Call in Integration - lines [360, 400]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-6-reward-accumulation-during-i-005` (8/21) 6. Reward Accumulation During Inactive Periods - lines [401, 451]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-8-liquid-staking-pending-coin--007` (12/21) 8. Liquid Staking: Pending Coin Inclusion in Unstake - lines [465, 504]
- [x] `sui-move-sui-move-defi-logic-vulnerabilities-9-liquid-staking-restake-routi-008` (10/21) 9. Liquid Staking: Restake Routing Errors - lines [505, 557]

Progress: 10/14 cards source-enriched for this file.

### `DB/Sui-Move-specific/SUI_MOVE_OBJECT_MODEL_VULNERABILITIES.md`

- [x] `sui-move-sui-move-object-model-vulnerabilities-1-uid-leak-object-identity-byp-000` (16/21) 1. UID Leak / Object Identity Bypass - lines [156, 309]
- [x] `sui-move-sui-move-object-model-vulnerabilities-2-dynamic-field-hash-collision-001` (13/21) 2. Dynamic Field Hash Collision - lines [310, 372]
- [x] `sui-move-sui-move-object-model-vulnerabilities-3-package-digest-collision-002` (9/21) 3. Package Digest Collision - lines [373, 421]
- [x] `sui-move-sui-move-object-model-vulnerabilities-4-object-size-limit-dos-003` (10/21) 4. Object Size Limit DoS - lines [422, 490]
- [x] `sui-move-sui-move-object-model-vulnerabilities-5-kiosk-extension-fund-locking-004` (9/21) 5. Kiosk Extension Fund Locking - lines [491, 526]
- [x] `sui-move-sui-move-object-model-vulnerabilities-7-committee-epoch-management-b-006` (11/21) 7. Committee / Epoch Management Bugs - lines [548, 607]
- [ ] `sui-move-sui-move-object-model-vulnerabilities-8-visibility-ability-misuse-vi-007` (8/21) 8. Visibility / Ability Misuse via Upgrades - lines [608, 653]
- [ ] `sui-move-sui-move-object-model-vulnerabilities-9-name-service-validation-fail-008` (8/21) 9. Name Service Validation Failures - lines [654, 689]

Progress: 6/8 cards source-enriched for this file.

### `DB/Sui-Move-specific/SUI_WALLET_SNAP_VULNERABILITIES.md`

- [x] `sui-move-sui-wallet-snap-vulnerabilities-1-markdown-control-character-i-000` (13/21) 1. Markdown/Control Character Injection in Transaction Rendering - lines [142, 207]
- [x] `sui-move-sui-wallet-snap-vulnerabilities-2-markdown-injection-in-messag-001` (9/21) 2. Markdown Injection in Message Signing - lines [282, 334]
- [x] `sui-move-sui-wallet-snap-vulnerabilities-3-forced-transaction-signing-v-002` (12/21) 3. Forced Transaction Signing via RPC - lines [335, 422]
- [ ] `sui-move-sui-wallet-snap-vulnerabilities-4-public-key-extraction-withou-003` (8/21) 4. Public Key Extraction Without User Consent - lines [423, 435]
- [x] `sui-move-sui-wallet-snap-vulnerabilities-5-user-confirmation-suppressio-004` (9/21) 5. User Confirmation Suppression - lines [436, 484]
- [x] `sui-move-sui-wallet-snap-vulnerabilities-6-key-derivation-path-manipula-005` (12/21) 6. Key Derivation Path Manipulation - lines [485, 532]
- [x] `sui-move-sui-wallet-snap-vulnerabilities-7-development-origins-in-produ-006` (10/21) 7. Development Origins in Production Builds - lines [533, 575]

Progress: 6/7 cards source-enriched for this file.

### `DB/account-abstraction/aa-erc7579-module-system-enable-mode.md`

- [ ] `account-abstraction-aa-erc7579-module-system-enable-mode-erc-7579-module-system-registr-000` (9/21) ERC-7579 Module System - Registry Bypass, moduleType Confusion, Hook PostCheck Skip, Fallback Flaws - lines [148, 325]

Progress: 0/1 cards source-enriched for this file.

### `DB/account-abstraction/aa-paymaster-gas-accounting-vulnerabilities.md`

- [ ] `account-abstraction-aa-paymaster-gas-accounting-vulnerabilit-aa-paymaster-gas-accounting-pr-000` (9/21) AA Paymaster Gas Accounting - Prefund Errors, Duplicate Snapshots, Stake Bypass, and Fee Escape - lines [145, 300]

Progress: 0/1 cards source-enriched for this file.

### `DB/account-abstraction/aa-session-key-permission-abuse.md`

- [ ] `account-abstraction-aa-session-key-permission-abuse-session-key-abuse-spend-limit--000` (9/21) Session Key Abuse - Spend Limit Bypass, Cross-Wallet Consumption, Permission Overwrite, PermissionId Frontrun - lines [133, 333]

Progress: 0/1 cards source-enriched for this file.

### `DB/account-abstraction/aa-signature-replay-attacks.md`

- [ ] `account-abstraction-aa-signature-replay-attacks-aa-signature-replay-missing-bi-000` (9/21) AA Signature Replay - Missing Binding Fields in UserOperation and Enable Mode Hashes - lines [133, 310]

Progress: 0/1 cards source-enriched for this file.

### `DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md`

- [ ] `amm-dos-arithmetic-initialization-secure-pattern-2-consistent-un-002` (7/21) Secure Pattern 2: Consistent Underflow Handling - lines [545, 566]
- [ ] `amm-dos-arithmetic-initialization-secure-pattern-3-first-deposit-003` (7/21) Secure Pattern 3: First Depositor Protection - lines [567, 595]
- [ ] `amm-dos-arithmetic-initialization-secure-pattern-4-bounded-queue-004` (7/21) Secure Pattern 4: Bounded Queue with Rate Limiting - lines [596, 620]

Progress: 0/3 cards source-enriched for this file.

### `DB/amm/concentrated-liquidity/fee-collection-distribution.md`

- [ ] `amm-fee-collection-distribution-keywords-008` (8/21) Keywords - lines [557, 586]
- [ ] `amm-fee-collection-distribution-secure-pattern-3-proportional--003` (9/21) Secure Pattern 3: Proportional Fee Collection - lines [467, 487]

Progress: 0/2 cards source-enriched for this file.

### `DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md`

- [ ] `amm-liquidity-management-vulnerabilities-secure-pattern-2-per-position--002` (8/21) Secure Pattern 2: Per-Position Liquidity Accounting - lines [519, 547]

Progress: 0/1 cards source-enriched for this file.

### `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`

- [ ] `amm-price-oracle-manipulation-secure-pattern-1-twap-oracle-w-001` (10/21) Secure Pattern 1: TWAP Oracle with Proper Configuration - lines [417, 445]
- [ ] `amm-price-oracle-manipulation-secure-pattern-2-dual-price-va-002` (8/21) Secure Pattern 2: Dual Price Validation - lines [446, 475]
- [ ] `amm-price-oracle-manipulation-secure-pattern-3-sqrtprice-bas-003` (10/21) Secure Pattern 3: sqrtPrice-Based Tick Derivation - lines [476, 494]

Progress: 0/3 cards source-enriched for this file.

### `DB/amm/concentrated-liquidity/slippage-sandwich-frontrun.md`

- [ ] `amm-slippage-sandwich-frontrun-vulnerability-title-000` (14/21) Vulnerability Title - lines [91, 405]

Progress: 0/1 cards source-enriched for this file.

### `DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md`

- [ ] `amm-tick-range-position-vulnerabilities-keywords-008` (8/21) Keywords - lines [387, 416]
- [ ] `amm-tick-range-position-vulnerabilities-secure-pattern-1-proper-tick-v-001` (9/21) Secure Pattern 1: Proper Tick Validation - lines [290, 301]
- [ ] `amm-tick-range-position-vulnerabilities-secure-pattern-2-fee-growth-wi-002` (8/21) Secure Pattern 2: Fee Growth with unchecked{} - lines [302, 312]

Progress: 0/3 cards source-enriched for this file.

### `DB/amm/concentrated-liquidity/v4-hook-token-compatibility.md`

- [ ] `amm-v4-hook-token-compatibility-secure-pattern-2-robust-token--002` (7/21) Secure Pattern 2: Robust Token Transfer Handling - lines [611, 637]
- [ ] `amm-v4-hook-token-compatibility-secure-pattern-3-gas-optimized-003` (7/21) Secure Pattern 3: Gas-Optimized Hook Callbacks - lines [638, 668]

Progress: 0/2 cards source-enriched for this file.

### `DB/amm/constantproduct/CONSTANT_PRODUCT_AMM_VULNERABILITIES.md`

- [x] `amm-constant-product-amm-vulnerabilities-1-first-depositor-inflation-at-000` (18/21) 1. First Depositor / Inflation Attacks - lines [332, 540]
- [x] `amm-constant-product-amm-vulnerabilities-10-decimal-math-calculation-is-009` (9/21) 10. Decimal & Math Calculation Issues - lines [1198, 1284]
- [x] `amm-constant-product-amm-vulnerabilities-11-liquidity-migration-protoco-010` (10/21) 11. Liquidity Migration & Protocol Upgrade Attacks - lines [1285, 1370]
- [x] `amm-constant-product-amm-vulnerabilities-12-flash-loan-based-graduation-011` (9/21) 12. Flash Loan-Based Graduation/Threshold Manipulation - lines [1371, 1434]
- [ ] `amm-constant-product-amm-vulnerabilities-13-detection-patterns-audit-ch-012` (8/21) 13. Detection Patterns & Audit Checklist - lines [1435, 1474]
- [x] `amm-constant-product-amm-vulnerabilities-13-imbalanced-liquidity-additi-013` (10/21) 13. Imbalanced Liquidity Addition Exploitation - lines [1475, 1547]
- [x] `amm-constant-product-amm-vulnerabilities-14-rebasing-token-integration--014` (12/21) 14. Rebasing Token Integration Issues - lines [1548, 1610]
- [x] `amm-constant-product-amm-vulnerabilities-15-impermanent-loss-protection-015` (11/21) 15. Impermanent Loss Protection Abuse - lines [1611, 1666]
- [x] `amm-constant-product-amm-vulnerabilities-16-protocol-invariant-breaking-016` (9/21) 16. Protocol Invariant Breaking - lines [1667, 1708]
- [x] `amm-constant-product-amm-vulnerabilities-17-dex-swap-slippage-accountin-017` (9/21) 17. DEX Swap Slippage Accounting Discrepancies - lines [1709, 1755]
- [x] `amm-constant-product-amm-vulnerabilities-18-leftover-token-accumulation-018` (9/21) 18. Leftover Token Accumulation in Autocompounding - lines [1756, 1803]
- [x] `amm-constant-product-amm-vulnerabilities-19-weth-eth-pool-asset-mismatc-019` (8/21) 19. WETH/ETH Pool Asset Mismatch - lines [1804, 1845]
- [x] `amm-constant-product-amm-vulnerabilities-2-slippage-protection-vulnerab-001` (14/21) 2. Slippage Protection Vulnerabilities - lines [541, 656]
- [x] `amm-constant-product-amm-vulnerabilities-20-single-sided-vs-proportiona-020` (9/21) 20. Single-Sided vs Proportional Exit Confusion - lines [1846, 1891]
- [x] `amm-constant-product-amm-vulnerabilities-21-type-casting-integer-overfl-021` (12/21) 21. Type Casting & Integer Overflow Issues - lines [1892, 1993]
- [x] `amm-constant-product-amm-vulnerabilities-22-spot-price-abuse-in-protoco-022` (12/21) 22. Spot Price Abuse in Protocol Swaps - lines [1994, 2080]
- [x] `amm-constant-product-amm-vulnerabilities-23-lp-token-burn-hijack-attack-023` (12/21) 23. LP Token Burn/Hijack Attacks - lines [2081, 2166]
- [x] `amm-constant-product-amm-vulnerabilities-24-constant-sum-amm-arbitrage-024` (11/21) 24. Constant Sum AMM Arbitrage - lines [2167, 2236]
- [x] `amm-constant-product-amm-vulnerabilities-25-state-accounting-discrepanc-025` (12/21) 25. State Accounting Discrepancies - lines [2237, 2321]
- [x] `amm-constant-product-amm-vulnerabilities-26-incorrect-liquidity-ownersh-026` (11/21) 26. Incorrect Liquidity Ownership Assumptions - lines [2322, 2404]
- [x] `amm-constant-product-amm-vulnerabilities-27-dividend-reward-gaming-027` (12/21) 27. Dividend/Reward Gaming - lines [2405, 2489]
- [x] `amm-constant-product-amm-vulnerabilities-28-missing-account-validation--028` (13/21) 28. Missing Account Validation (Solana-Specific) - lines [2490, 2576]
- [ ] `amm-constant-product-amm-vulnerabilities-29-detection-patterns-audit-ch-029` (8/21) 29. Detection Patterns & Audit Checklist - lines [2577, 2651]
- [x] `amm-constant-product-amm-vulnerabilities-3-sandwich-mev-attacks-002` (10/21) 3. Sandwich & MEV Attacks - lines [657, 704]
- [x] `amm-constant-product-amm-vulnerabilities-4-spot-price-manipulation-slot-003` (12/21) 4. Spot Price Manipulation (slot0) - lines [705, 793]
- [x] `amm-constant-product-amm-vulnerabilities-5-deadline-vulnerabilities-004` (8/21) 5. Deadline Vulnerabilities - lines [794, 845]
- [x] `amm-constant-product-amm-vulnerabilities-6-reserve-manipulation-attacks-005` (9/21) 6. Reserve Manipulation Attacks - lines [846, 883]
- [x] `amm-constant-product-amm-vulnerabilities-7-lp-token-calculation-issues-006` (9/21) 7. LP Token Calculation Issues - lines [884, 926]
- [x] `amm-constant-product-amm-vulnerabilities-8-callback-reentrancy-attacks-007` (13/21) 8. Callback & Reentrancy Attacks - lines [927, 1043]
- [x] `amm-constant-product-amm-vulnerabilities-9-factory-pool-creation-attack-008` (15/21) 9. Factory & Pool Creation Attacks - lines [1044, 1197]

Progress: 28/30 cards source-enriched for this file.

### `DB/bridge/axelar/axelar-integration-vulnerabilities.md`

- [ ] `bridge-axelar-integration-vulnerabilities-1-gateway-validation-bypass-000` (12/21) 1. Gateway Validation Bypass - lines [133, 270]
- [ ] `bridge-axelar-integration-vulnerabilities-10-command-id-collision-009` (7/21) 10. Command ID Collision - lines [778, 833]
- [ ] `bridge-axelar-integration-vulnerabilities-2-source-chain-address-spoofin-001` (7/21) 2. Source Chain & Address Spoofing - lines [271, 351]
- [ ] `bridge-axelar-integration-vulnerabilities-3-token-burn-but-call-fails-002` (7/21) 3. Token Burn-but-Call-Fails - lines [352, 420]
- [ ] `bridge-axelar-integration-vulnerabilities-4-express-execution-front-runn-003` (7/21) 4. Express Execution Front-Running - lines [421, 473]
- [ ] `bridge-axelar-integration-vulnerabilities-5-its-token-manager-misconfigu-004` (8/21) 5. ITS Token Manager Misconfiguration - lines [474, 528]
- [ ] `bridge-axelar-integration-vulnerabilities-6-gas-service-payment-issues-005` (9/21) 6. Gas Service Payment Issues - lines [529, 611]
- [ ] `bridge-axelar-integration-vulnerabilities-7-string-based-chain-matching-006` (8/21) 7. String-Based Chain Matching - lines [612, 663]
- [ ] `bridge-axelar-integration-vulnerabilities-8-executable-contract-reentran-007` (7/21) 8. Executable Contract Reentrancy - lines [664, 718]
- [ ] `bridge-axelar-integration-vulnerabilities-9-governance-proposal-replay-008` (7/21) 9. Governance Proposal Replay - lines [719, 777]

Progress: 0/10 cards source-enriched for this file.

### `DB/bridge/ccip/ccip-integration-vulnerabilities.md`

- [ ] `bridge-ccip-integration-vulnerabilities-1-router-message-validation-000` (12/21) 1. Router Message Validation - lines [142, 268]
- [ ] `bridge-ccip-integration-vulnerabilities-10-token-amount-validation-009` (7/21) 10. Token Amount Validation - lines [862, 909]
- [ ] `bridge-ccip-integration-vulnerabilities-11-message-size-limit-violatio-010` (7/21) 11. Message Size Limit Violations - lines [910, 971]
- [ ] `bridge-ccip-integration-vulnerabilities-12-self-service-token-registra-011` (10/21) 12. Self-Service Token Registration Issues - lines [972, 1022]
- [ ] `bridge-ccip-integration-vulnerabilities-2-fee-estimation-errors-001` (7/21) 2. Fee Estimation Errors - lines [269, 373]
- [ ] `bridge-ccip-integration-vulnerabilities-3-token-pool-configuration-002` (8/21) 3. Token Pool Configuration - lines [374, 456]
- [ ] `bridge-ccip-integration-vulnerabilities-4-extra-args-gas-limit-misconf-003` (9/21) 4. Extra Args & Gas Limit Misconfiguration - lines [457, 526]
- [ ] `bridge-ccip-integration-vulnerabilities-5-lane-allowlist-bypass-004` (8/21) 5. Lane Allowlist Bypass - lines [527, 599]
- [ ] `bridge-ccip-integration-vulnerabilities-6-manual-execution-replay-005` (7/21) 6. Manual Execution Replay - lines [600, 660]
- [ ] `bridge-ccip-integration-vulnerabilities-7-sender-receiver-validation-006` (8/21) 7. Sender & Receiver Validation - lines [661, 731]
- [ ] `bridge-ccip-integration-vulnerabilities-8-rate-limiter-griefing-007` (7/21) 8. Rate Limiter Griefing - lines [732, 787]
- [ ] `bridge-ccip-integration-vulnerabilities-9-off-ramp-processing-failures-008` (8/21) 9. Off-Ramp Processing Failures - lines [788, 861]

Progress: 0/12 cards source-enriched for this file.

### `DB/bridge/custom/cross-chain-general-vulnerabilities.md`

- [x] `bridge-cross-chain-general-vulnerabilities-1-cross-chain-replay-attacks-000` (16/21) 1. Cross-Chain Replay Attacks - lines [137, 386]
- [ ] `bridge-cross-chain-general-vulnerabilities-2-signature-validation-issues-001` (7/21) 2. Signature Validation Issues - lines [387, 451]
- [x] `bridge-cross-chain-general-vulnerabilities-3-token-bridging-issues-002` (10/21) 3. Token Bridging Issues - lines [452, 563]
- [x] `bridge-cross-chain-general-vulnerabilities-4-sequencer-l2-specific-issues-003` (8/21) 4. Sequencer & L2 Specific Issues - lines [564, 646]
- [x] `bridge-cross-chain-general-vulnerabilities-5-access-control-vulnerabiliti-004` (9/21) 5. Access Control Vulnerabilities - lines [647, 720]
- [ ] `bridge-cross-chain-general-vulnerabilities-6-slippage-mev-issues-005` (7/21) 6. Slippage & MEV Issues - lines [721, 803]
- [ ] `bridge-cross-chain-general-vulnerabilities-7-message-ordering-timing-006` (7/21) 7. Message Ordering & Timing - lines [804, 864]

Progress: 4/7 cards source-enriched for this file.

### `DB/bridge/custom/defihacklabs-bridge-2022-patterns.md`

- [ ] `bridge-defihacklabs-bridge-2022-patterns-high-signal-grep-seeds-004` (6/21) High-Signal Grep Seeds - lines [382, 395]

Progress: 0/1 cards source-enriched for this file.

### `DB/bridge/custom/defihacklabs-bridge-l2-replay-2022-patterns.md`

- [ ] `bridge-defihacklabs-bridge-l2-replay-2022-patte-high-signal-grep-seeds-004` (6/21) High-Signal Grep Seeds - lines [385, 400]

Progress: 0/1 cards source-enriched for this file.

### `DB/bridge/custom/defihacklabs-bridge-patterns.md`

- [ ] `bridge-defihacklabs-bridge-patterns-high-signal-grep-seeds-004` (6/21) High-Signal Grep Seeds - lines [404, 415]

Progress: 0/1 cards source-enriched for this file.

### `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`

- [x] `bridge-hyperlane-integration-vulnerabilities-1-ism-validation-vulnerabiliti-000` (15/21) 1. ISM Validation Vulnerabilities - lines [119, 299]
- [x] `bridge-hyperlane-integration-vulnerabilities-2-message-replay-attacks-001` (11/21) 2. Message Replay Attacks - lines [300, 464]
- [ ] `bridge-hyperlane-integration-vulnerabilities-3-router-configuration-issues-002` (7/21) 3. Router Configuration Issues - lines [465, 546]
- [ ] `bridge-hyperlane-integration-vulnerabilities-4-handle-function-vulnerabilit-003` (8/21) 4. Handle Function Vulnerabilities - lines [547, 625]
- [ ] `bridge-hyperlane-integration-vulnerabilities-5-gas-payment-issues-004` (7/21) 5. Gas Payment Issues - lines [626, 700]

Progress: 2/5 cards source-enriched for this file.

### `DB/bridge/layerzero/layerzero-integration-vulnerabilities.md`

- [x] `bridge-layerzero-integration-vulnerabilities-1-channel-blocking-vulnerabili-000` (17/21) 1. Channel Blocking Vulnerabilities - lines [399, 578]
- [x] `bridge-layerzero-integration-vulnerabilities-10-cross-chain-payload-validat-009` (10/21) 10. Cross-Chain Payload Validation Vulnerabilities - lines [1326, 1424]
- [x] `bridge-layerzero-integration-vulnerabilities-11-insufficient-gas-limit-calc-010` (11/21) 11. Insufficient Gas Limit Calculation - lines [1425, 1519]
- [x] `bridge-layerzero-integration-vulnerabilities-2-minimum-gas-validation-vulne-001` (12/21) 2. Minimum Gas Validation Vulnerabilities - lines [579, 689]
- [x] `bridge-layerzero-integration-vulnerabilities-3-gas-estimation-fee-calculati-002` (10/21) 3. Gas Estimation & Fee Calculation - lines [690, 796]
- [x] `bridge-layerzero-integration-vulnerabilities-4-fee-refund-handling-003` (10/21) 4. Fee Refund Handling - lines [797, 878]
- [x] `bridge-layerzero-integration-vulnerabilities-5-payload-size-address-validat-004` (8/21) 5. Payload Size & Address Validation - lines [879, 924]
- [x] `bridge-layerzero-integration-vulnerabilities-6-composed-message-vulnerabili-005` (14/21) 6. Composed Message Vulnerabilities (LayerZero V2) - lines [925, 1027]
- [x] `bridge-layerzero-integration-vulnerabilities-7-oft-onft-specific-vulnerabil-006` (12/21) 7. OFT/ONFT Specific Vulnerabilities - lines [1028, 1141]
- [x] `bridge-layerzero-integration-vulnerabilities-8-peer-trust-configuration-vul-007` (9/21) 8. Peer & Trust Configuration Vulnerabilities - lines [1142, 1203]
- [x] `bridge-layerzero-integration-vulnerabilities-9-stargate-sgreceive-integrati-008` (12/21) 9. Stargate/sgReceive Integration Vulnerabilities - lines [1204, 1325]

Progress: 11/11 cards source-enriched for this file.

### `DB/bridge/stargate/stargate-integration-vulnerabilities.md`

- [x] `bridge-stargate-integration-vulnerabilities-1-sgreceive-out-of-gas-000` (14/21) 1. sgReceive Out-of-Gas - lines [132, 250]
- [ ] `bridge-stargate-integration-vulnerabilities-2-router-swap-slippage-001` (7/21) 2. Router Swap Slippage - lines [251, 326]
- [ ] `bridge-stargate-integration-vulnerabilities-3-pool-credit-imbalance-002` (7/21) 3. Pool Credit Imbalance - lines [327, 373]
- [x] `bridge-stargate-integration-vulnerabilities-4-stargate-v2-compose-failures-003` (8/21) 4. Stargate V2 Compose Failures - lines [374, 434]
- [x] `bridge-stargate-integration-vulnerabilities-5-dstgasforcall-misconfigurati-004` (8/21) 5. dstGasForCall Misconfiguration - lines [435, 491]
- [x] `bridge-stargate-integration-vulnerabilities-6-destination-address-mismatch-005` (9/21) 6. Destination Address Mismatch - lines [492, 548]
- [ ] `bridge-stargate-integration-vulnerabilities-7-fee-layer-exploitation-006` (8/21) 7. Fee Layer Exploitation - lines [549, 616]
- [x] `bridge-stargate-integration-vulnerabilities-8-amount-trimming-decimal-dust-007` (10/21) 8. Amount Trimming & Decimal Dust - lines [617, 672]

Progress: 5/8 cards source-enriched for this file.

### `DB/bridge/wormhole/wormhole-integration-vulnerabilities.md`

- [x] `bridge-wormhole-integration-vulnerabilities-1-vaa-parsing-vulnerabilities-000` (16/21) 1. VAA Parsing Vulnerabilities - lines [129, 294]
- [x] `bridge-wormhole-integration-vulnerabilities-2-guardian-set-vulnerabilities-001` (12/21) 2. Guardian Set Vulnerabilities - lines [295, 382]
- [x] `bridge-wormhole-integration-vulnerabilities-3-message-replay-attacks-002` (8/21) 3. Message Replay Attacks - lines [383, 448]
- [x] `bridge-wormhole-integration-vulnerabilities-4-token-bridge-integration-003` (9/21) 4. Token Bridge Integration - lines [449, 557]
- [x] `bridge-wormhole-integration-vulnerabilities-5-gas-limit-issues-004` (8/21) 5. Gas Limit Issues - lines [558, 613]

Progress: 5/5 cards source-enriched for this file.

### `DB/cosmos/app-chain/abci-lifecycle/abci-lifecycle-vulnerabilities.md`

- [x] `cosmos-abci-lifecycle-vulnerabilities-1-abci-endblock-error-000` (15/21) 1. Abci Endblock Error - lines [99, 223]
- [x] `cosmos-abci-lifecycle-vulnerabilities-2-abci-checktx-bypass-001` (11/21) 2. Abci Checktx Bypass - lines [224, 288]
- [x] `cosmos-abci-lifecycle-vulnerabilities-3-abci-vote-extension-abuse-002` (12/21) 3. Abci Vote Extension Abuse - lines [289, 409]
- [x] `cosmos-abci-lifecycle-vulnerabilities-4-abci-finalize-block-003` (12/21) 4. Abci Finalize Block - lines [410, 485]
- [ ] `cosmos-abci-lifecycle-vulnerabilities-keywords-004` (8/21) Keywords - lines [500, 523]

Progress: 4/5 cards source-enriched for this file.

### `DB/cosmos/app-chain/access-control/authorization-vulnerabilities.md`

- [x] `cosmos-authorization-vulnerabilities-1-access-missing-control-000` (15/21) 1. Access Missing Control - lines [162, 346]
- [x] `cosmos-authorization-vulnerabilities-10-access-module-authority-013` (11/21) 10. Access Module Authority - lines [919, 973]
- [ ] `cosmos-authorization-vulnerabilities-2-access-role-assignment-001` (9/21) 2. Access Role Assignment - lines [347, 372]
- [x] `cosmos-authorization-vulnerabilities-3-access-antehandler-bypass-004` (11/21) 3. Access Antehandler Bypass - lines [411, 475]
- [ ] `cosmos-authorization-vulnerabilities-4-access-allowlist-bypass-005` (9/21) 4. Access Allowlist Bypass - lines [476, 501]
- [x] `cosmos-authorization-vulnerabilities-5-access-cosmwasm-bypass-007` (14/21) 5. Access Cosmwasm Bypass - lines [533, 606]
- [x] `cosmos-authorization-vulnerabilities-6-access-amino-signing-008` (13/21) 6. Access Amino Signing - lines [607, 675]
- [x] `cosmos-authorization-vulnerabilities-7-access-predecessor-misuse-009` (11/21) 7. Access Predecessor Misuse - lines [676, 734]
- [ ] `cosmos-authorization-vulnerabilities-8-access-owner-privilege-010` (8/21) 8. Access Owner Privilege - lines [735, 760]
- [x] `cosmos-authorization-vulnerabilities-9-access-msg-sender-validation-012` (12/21) 9. Access Msg Sender Validation - lines [843, 918]
- [ ] `cosmos-authorization-vulnerabilities-description-006` (8/21) Description - lines [502, 532]
- [ ] `cosmos-authorization-vulnerabilities-di-culty-n-a-011` (12/21) Diculty: N/A - lines [761, 842]
- [ ] `cosmos-authorization-vulnerabilities-keywords-014` (8/21) Keywords - lines [1000, 1023]
- [ ] `cosmos-authorization-vulnerabilities-severity-high-risk-003` (6/21) Severity: High Risk - lines [384, 410]
- [ ] `cosmos-authorization-vulnerabilities-upgrades-002` (7/21) Upgrades - lines [373, 383]

Progress: 7/15 cards source-enriched for this file.

### `DB/cosmos/app-chain/accounting/balance-tracking-errors.md`

- [x] `cosmos-balance-tracking-errors-1-accounting-balance-not-updat-000` (15/21) 1. Accounting Balance Not Updated - lines [173, 317]
- [x] `cosmos-balance-tracking-errors-2-accounting-double-counting-001` (13/21) 2. Accounting Double Counting - lines [318, 462]
- [x] `cosmos-balance-tracking-errors-3-accounting-tvl-error-002` (12/21) 3. Accounting Tvl Error - lines [463, 543]
- [x] `cosmos-balance-tracking-errors-4-accounting-state-corruption-003` (12/21) 4. Accounting State Corruption - lines [544, 626]
- [ ] `cosmos-balance-tracking-errors-5-accounting-missing-deduction-004` (12/21) 5. Accounting Missing Deduction - lines [627, 685]
- [x] `cosmos-balance-tracking-errors-6-accounting-cross-module-006` (11/21) 6. Accounting Cross Module - lines [724, 775]
- [x] `cosmos-balance-tracking-errors-7-accounting-pending-tracking-007` (13/21) 7. Accounting Pending Tracking - lines [776, 896]
- [x] `cosmos-balance-tracking-errors-8-accounting-negative-value-008` (13/21) 8. Accounting Negative Value - lines [897, 1022]
- [x] `cosmos-balance-tracking-errors-9-accounting-fee-deduction-009` (13/21) 9. Accounting Fee Deduction - lines [1023, 1107]
- [ ] `cosmos-balance-tracking-errors-keywords-010` (8/21) Keywords - lines [1132, 1155]
- [ ] `cosmos-balance-tracking-errors-lombard-transfer-signing-strat-005` (9/21) Lombard Transfer Signing Strategy - lines [686, 723]

Progress: 8/11 cards source-enriched for this file.

### `DB/cosmos/app-chain/accounting/exchange-rate-vulnerabilities.md`

- [x] `cosmos-exchange-rate-vulnerabilities-1-accounting-exchange-rate-man-000` (17/21) 1. Accounting Exchange Rate Manipulation - lines [127, 293]
- [x] `cosmos-exchange-rate-vulnerabilities-2-accounting-exchange-rate-sta-001` (13/21) 2. Accounting Exchange Rate Stale - lines [294, 376]
- [x] `cosmos-exchange-rate-vulnerabilities-3-accounting-exchange-rate-err-002` (13/21) 3. Accounting Exchange Rate Error - lines [377, 489]
- [ ] `cosmos-exchange-rate-vulnerabilities-4-accounting-share-price-infla-003` (9/21) 4. Accounting Share Price Inflation - lines [490, 515]
- [x] `cosmos-exchange-rate-vulnerabilities-5-accounting-conversion-roundi-005` (13/21) 5. Accounting Conversion Rounding - lines [545, 672]
- [ ] `cosmos-exchange-rate-vulnerabilities-keywords-006` (8/21) Keywords - lines [689, 712]
- [ ] `cosmos-exchange-rate-vulnerabilities-vulnerability-overview-004` (8/21) Vulnerability Overview - lines [516, 544]

Progress: 4/7 cards source-enriched for this file.

### `DB/cosmos/app-chain/accounting/integer-precision-vulnerabilities.md`

- [x] `cosmos-integer-precision-vulnerabilities-1-accounting-integer-overflow-000` (15/21) 1. Accounting Integer Overflow - lines [120, 283]
- [x] `cosmos-integer-precision-vulnerabilities-2-accounting-integer-underflow-001` (13/21) 2. Accounting Integer Underflow - lines [284, 375]
- [x] `cosmos-integer-precision-vulnerabilities-3-accounting-unsafe-casting-002` (13/21) 3. Accounting Unsafe Casting - lines [376, 455]
- [x] `cosmos-integer-precision-vulnerabilities-4-accounting-precision-loss-003` (12/21) 4. Accounting Precision Loss - lines [456, 520]
- [x] `cosmos-integer-precision-vulnerabilities-5-accounting-decimal-mismatch-004` (13/21) 5. Accounting Decimal Mismatch - lines [521, 637]
- [ ] `cosmos-integer-precision-vulnerabilities-keywords-005` (8/21) Keywords - lines [654, 677]

Progress: 5/6 cards source-enriched for this file.

### `DB/cosmos/app-chain/bridge/cross-chain-bridge-vulnerabilities.md`

- [x] `cosmos-cross-chain-bridge-vulnerabilities-1-bridge-replay-attack-000` (13/21) 1. Bridge Replay Attack - lines [124, 181]
- [x] `cosmos-cross-chain-bridge-vulnerabilities-2-bridge-token-accounting-002` (13/21) 2. Bridge Token Accounting - lines [236, 327]
- [x] `cosmos-cross-chain-bridge-vulnerabilities-3-bridge-relayer-exploit-003` (13/21) 3. Bridge Relayer Exploit - lines [328, 412]
- [x] `cosmos-cross-chain-bridge-vulnerabilities-4-bridge-freeze-halt-004` (12/21) 4. Bridge Freeze Halt - lines [413, 484]
- [x] `cosmos-cross-chain-bridge-vulnerabilities-5-bridge-observer-exploit-005` (13/21) 5. Bridge Observer Exploit - lines [485, 600]
- [x] `cosmos-cross-chain-bridge-vulnerabilities-6-bridge-denom-handling-006` (12/21) 6. Bridge Denom Handling - lines [601, 672]
- [ ] `cosmos-cross-chain-bridge-vulnerabilities-keywords-007` (8/21) Keywords - lines [691, 714]
- [ ] `cosmos-cross-chain-bridge-vulnerabilities-vulnerability-report-001` (8/21) Vulnerability Report - lines [182, 235]

Progress: 6/8 cards source-enriched for this file.

### `DB/cosmos/app-chain/btc-staking/btc-staking-vulnerabilities.md`

- [x] `cosmos-btc-staking-vulnerabilities-1-btc-staking-tx-validation-000` (13/21) 1. Btc Staking Tx Validation - lines [135, 192]
- [x] `cosmos-btc-staking-vulnerabilities-2-btc-unbonding-handling-002` (12/21) 2. Btc Unbonding Handling - lines [235, 337]
- [x] `cosmos-btc-staking-vulnerabilities-3-btc-delegation-finality-003` (12/21) 3. Btc Delegation Finality - lines [338, 464]
- [ ] `cosmos-btc-staking-vulnerabilities-4-btc-change-output-004` (9/21) 4. Btc Change Output - lines [465, 490]
- [x] `cosmos-btc-staking-vulnerabilities-5-btc-slashable-stake-006` (13/21) 5. Btc Slashable Stake - lines [518, 600]
- [x] `cosmos-btc-staking-vulnerabilities-6-btc-covenant-signature-007` (11/21) 6. Btc Covenant Signature - lines [601, 675]
- [ ] `cosmos-btc-staking-vulnerabilities-7-btc-staking-indexer-008` (11/21) 7. Btc Staking Indexer - lines [676, 708]
- [x] `cosmos-btc-staking-vulnerabilities-8-btc-timestamp-verification-010` (12/21) 8. Btc Timestamp Verification - lines [761, 813]
- [ ] `cosmos-btc-staking-vulnerabilities-babylon-deposit-mfa-request-va-001` (8/21) Babylon Deposit MFA Request Validation - lines [193, 234]
- [ ] `cosmos-btc-staking-vulnerabilities-babylon-deposit-mfa-request-va-009` (7/21) Babylon Deposit MFA Request Validation - lines [709, 760]
- [ ] `cosmos-btc-staking-vulnerabilities-keywords-011` (8/21) Keywords - lines [836, 859]
- [ ] `cosmos-btc-staking-vulnerabilities-lombard-transfer-signing-strat-005` (6/21) Lombard Transfer Signing Strategy - lines [491, 517]

Progress: 6/12 cards source-enriched for this file.

### `DB/cosmos/app-chain/consensus/consensus-finality-vulnerabilities.md`

- [x] `cosmos-consensus-finality-vulnerabilities-1-consensus-proposer-dos-000` (14/21) 1. Consensus Proposer Dos - lines [158, 234]
- [x] `cosmos-consensus-finality-vulnerabilities-2-consensus-finality-bypass-002` (11/21) 2. Consensus Finality Bypass - lines [338, 398]
- [x] `cosmos-consensus-finality-vulnerabilities-3-consensus-reorg-003` (12/21) 3. Consensus Reorg - lines [399, 466]
- [ ] `cosmos-consensus-finality-vulnerabilities-4-consensus-vote-extension-004` (11/21) 4. Consensus Vote Extension - lines [467, 548]
- [x] `cosmos-consensus-finality-vulnerabilities-5-consensus-block-sync-006` (13/21) 5. Consensus Block Sync - lines [597, 662]
- [ ] `cosmos-consensus-finality-vulnerabilities-6-consensus-non-determinism-007` (9/21) 6. Consensus Non Determinism - lines [663, 688]
- [x] `cosmos-consensus-finality-vulnerabilities-7-consensus-proposer-selection-009` (12/21) 7. Consensus Proposer Selection - lines [741, 856]
- [ ] `cosmos-consensus-finality-vulnerabilities-8-consensus-equivocation-010` (12/21) 8. Consensus Equivocation - lines [857, 945]
- [ ] `cosmos-consensus-finality-vulnerabilities-9-consensus-liveness-012` (9/21) 9. Consensus Liveness - lines [979, 1004]
- [ ] `cosmos-consensus-finality-vulnerabilities-comet-bft-s-view-of-validators-005` (9/21) Comet BFT's View of Validators - lines [549, 596]
- [ ] `cosmos-consensus-finality-vulnerabilities-di-culty-high-001` (12/21) Diculty: High - lines [235, 337]
- [ ] `cosmos-consensus-finality-vulnerabilities-di-culty-medium-011` (8/21) Diculty: Medium - lines [946, 978]
- [ ] `cosmos-consensus-finality-vulnerabilities-keywords-014` (8/21) Keywords - lines [1056, 1079]
- [ ] `cosmos-consensus-finality-vulnerabilities-medium-risk-severity-report-008` (9/21) Medium Risk Severity Report - lines [689, 740]
- [ ] `cosmos-consensus-finality-vulnerabilities-severity-medium-risk-013` (6/21) Severity: Medium Risk - lines [1005, 1031]

Progress: 5/15 cards source-enriched for this file.

### `DB/cosmos/app-chain/dos/chain-halt-consensus-dos.md`

- [x] `cosmos-chain-halt-consensus-dos-1-dos-block-production-halt-000` (15/21) 1. Dos Block Production Halt - lines [156, 328]
- [x] `cosmos-chain-halt-consensus-dos-2-dos-consensus-halt-001` (13/21) 2. Dos Consensus Halt - lines [329, 482]
- [x] `cosmos-chain-halt-consensus-dos-3-dos-state-machine-002` (12/21) 3. Dos State Machine - lines [483, 651]
- [x] `cosmos-chain-halt-consensus-dos-4-dos-unbounded-beginblock-003` (12/21) 4. Dos Unbounded Beginblock - lines [652, 779]
- [x] `cosmos-chain-halt-consensus-dos-5-dos-unbounded-array-004` (13/21) 5. Dos Unbounded Array - lines [780, 876]
- [x] `cosmos-chain-halt-consensus-dos-6-dos-panic-crash-005` (12/21) 6. Dos Panic Crash - lines [877, 929]
- [x] `cosmos-chain-halt-consensus-dos-7-dos-message-flooding-006` (11/21) 7. Dos Message Flooding - lines [930, 981]
- [ ] `cosmos-chain-halt-consensus-dos-8-dos-deposit-spam-007` (11/21) 8. Dos Deposit Spam - lines [982, 1027]
- [ ] `cosmos-chain-halt-consensus-dos-keywords-009` (8/21) Keywords - lines [1134, 1157]
- [ ] `cosmos-chain-halt-consensus-dos-severity-medium-risk-008` (10/21) Severity: Medium Risk - lines [1028, 1111]

Progress: 7/10 cards source-enriched for this file.

### `DB/cosmos/app-chain/dos/gas-resource-exhaustion.md`

- [x] `cosmos-gas-resource-exhaustion-1-dos-gas-limit-exploit-000` (15/21) 1. Dos Gas Limit Exploit - lines [123, 335]
- [x] `cosmos-gas-resource-exhaustion-2-dos-gas-metering-bypass-001` (13/21) 2. Dos Gas Metering Bypass - lines [336, 452]
- [x] `cosmos-gas-resource-exhaustion-3-dos-memory-exhaustion-002` (11/21) 3. Dos Memory Exhaustion - lines [453, 524]
- [x] `cosmos-gas-resource-exhaustion-4-dos-storage-exhaustion-003` (12/21) 4. Dos Storage Exhaustion - lines [525, 602]
- [ ] `cosmos-gas-resource-exhaustion-5-dos-large-payload-004` (12/21) 5. Dos Large Payload - lines [603, 696]
- [ ] `cosmos-gas-resource-exhaustion-keywords-006` (8/21) Keywords - lines [750, 773]
- [ ] `cosmos-gas-resource-exhaustion-medium-risk-report-005` (11/21) Medium Risk Report - lines [697, 733]

Progress: 4/7 cards source-enriched for this file.

### `DB/cosmos/app-chain/dos/griefing-revert-dos.md`

- [x] `cosmos-griefing-revert-dos-1-dos-function-revert-000` (15/21) 1. Dos Function Revert - lines [113, 301]
- [x] `cosmos-griefing-revert-dos-2-dos-frontrun-grief-001` (12/21) 2. Dos Frontrun Grief - lines [302, 364]
- [x] `cosmos-griefing-revert-dos-3-dos-dust-grief-002` (11/21) 3. Dos Dust Grief - lines [365, 420]
- [ ] `cosmos-griefing-revert-dos-4-dos-external-call-revert-003` (9/21) 4. Dos External Call Revert - lines [421, 445]
- [x] `cosmos-griefing-revert-dos-5-dos-loop-revert-005` (11/21) 5. Dos Loop Revert - lines [484, 545]
- [ ] `cosmos-griefing-revert-dos-keywords-006` (8/21) Keywords - lines [562, 585]
- [ ] `cosmos-griefing-revert-dos-recommendation-004` (7/21) Recommendation - lines [446, 483]

Progress: 4/7 cards source-enriched for this file.

### `DB/cosmos/app-chain/evm/evm-gas-handling-vulnerabilities.md`

- [x] `cosmos-evm-gas-handling-vulnerabilities-1-evm-intrinsic-gas-missing-000` (13/21) 1. Evm Intrinsic Gas Missing - lines [103, 187]
- [x] `cosmos-evm-gas-handling-vulnerabilities-2-evm-gas-refund-error-001` (12/21) 2. Evm Gas Refund Error - lines [188, 245]
- [x] `cosmos-evm-gas-handling-vulnerabilities-3-evm-precompile-gas-hardcode-002` (12/21) 3. Evm Precompile Gas Hardcode - lines [246, 315]
- [x] `cosmos-evm-gas-handling-vulnerabilities-4-evm-gas-not-consumed-error-003` (12/21) 4. Evm Gas Not Consumed Error - lines [316, 400]
- [x] `cosmos-evm-gas-handling-vulnerabilities-5-evm-gas-mismatch-call-004` (11/21) 5. Evm Gas Mismatch Call - lines [401, 455]
- [ ] `cosmos-evm-gas-handling-vulnerabilities-keywords-005` (8/21) Keywords - lines [472, 495]

Progress: 5/6 cards source-enriched for this file.

### `DB/cosmos/app-chain/evm/precompile-state-vulnerabilities.md`

- [x] `cosmos-precompile-state-vulnerabilities-1-evm-dirty-state-precompile-000` (11/21) 1. Evm Dirty State Precompile - lines [142, 231]
- [x] `cosmos-precompile-state-vulnerabilities-2-evm-precompile-panic-001` (11/21) 2. Evm Precompile Panic - lines [232, 286]
- [ ] `cosmos-precompile-state-vulnerabilities-3-evm-delegatecall-precompile-002` (9/21) 3. Evm Delegatecall Precompile - lines [287, 312]
- [x] `cosmos-precompile-state-vulnerabilities-4-evm-bank-balance-sync-004` (12/21) 4. Evm Bank Balance Sync - lines [354, 431]
- [x] `cosmos-precompile-state-vulnerabilities-5-evm-nonce-manipulation-005` (11/21) 5. Evm Nonce Manipulation - lines [432, 489]
- [x] `cosmos-precompile-state-vulnerabilities-6-evm-tx-disguise-006` (12/21) 6. Evm Tx Disguise - lines [490, 558]
- [x] `cosmos-precompile-state-vulnerabilities-7-evm-precompile-outdated-007` (11/21) 7. Evm Precompile Outdated - lines [559, 611]
- [x] `cosmos-precompile-state-vulnerabilities-8-evm-state-revert-008` (12/21) 8. Evm State Revert - lines [612, 676]
- [x] `cosmos-precompile-state-vulnerabilities-9-evm-address-conversion-009` (13/21) 9. Evm Address Conversion - lines [677, 777]
- [ ] `cosmos-precompile-state-vulnerabilities-keywords-010` (8/21) Keywords - lines [802, 825]
- [ ] `cosmos-precompile-state-vulnerabilities-security-report-003` (7/21) Security Report - lines [313, 353]

Progress: 8/11 cards source-enriched for this file.

### `DB/cosmos/app-chain/fund-safety/fund-locking-insolvency.md`

- [x] `cosmos-fund-locking-insolvency-1-funds-lock-permanent-000` (15/21) 1. Funds Lock Permanent - lines [177, 309]
- [x] `cosmos-fund-locking-insolvency-2-funds-lock-conditional-001` (13/21) 2. Funds Lock Conditional - lines [310, 440]
- [x] `cosmos-fund-locking-insolvency-3-funds-insolvency-protocol-002` (13/21) 3. Funds Insolvency Protocol - lines [441, 609]
- [x] `cosmos-fund-locking-insolvency-4-funds-insolvency-slash-003` (13/21) 4. Funds Insolvency Slash - lines [610, 698]
- [x] `cosmos-fund-locking-insolvency-5-funds-insolvency-rebase-004` (13/21) 5. Funds Insolvency Rebase - lines [699, 834]
- [x] `cosmos-fund-locking-insolvency-6-funds-bad-debt-005` (13/21) 6. Funds Bad Debt - lines [835, 928]
- [ ] `cosmos-fund-locking-insolvency-7-funds-withdrawal-blocked-006` (12/21) 7. Funds Withdrawal Blocked - lines [929, 992]
- [x] `cosmos-fund-locking-insolvency-8-funds-unsafe-casting-loss-008` (11/21) 8. Funds Unsafe Casting Loss - lines [1052, 1103]
- [ ] `cosmos-fund-locking-insolvency-description-007` (12/21) Description - lines [993, 1051]
- [ ] `cosmos-fund-locking-insolvency-keywords-009` (8/21) Keywords - lines [1126, 1149]

Progress: 7/10 cards source-enriched for this file.

### `DB/cosmos/app-chain/fund-safety/fund-theft-vulnerabilities.md`

- [x] `cosmos-fund-theft-vulnerabilities-1-funds-theft-auth-bypass-000` (15/21) 1. Funds Theft Auth Bypass - lines [158, 375]
- [x] `cosmos-fund-theft-vulnerabilities-2-funds-theft-manipulation-001` (13/21) 2. Funds Theft Manipulation - lines [376, 542]
- [ ] `cosmos-fund-theft-vulnerabilities-3-funds-theft-reentrancy-002` (11/21) 3. Funds Theft Reentrancy - lines [543, 594]
- [ ] `cosmos-fund-theft-vulnerabilities-4-funds-theft-delegatecall-004` (9/21) 4. Funds Theft Delegatecall - lines [627, 652]
- [x] `cosmos-fund-theft-vulnerabilities-5-funds-theft-replay-006` (11/21) 5. Funds Theft Replay - lines [680, 731]
- [ ] `cosmos-fund-theft-vulnerabilities-6-funds-theft-frontrunning-007` (11/21) 6. Funds Theft Frontrunning - lines [732, 779]
- [x] `cosmos-fund-theft-vulnerabilities-7-funds-theft-surplus-009` (13/21) 7. Funds Theft Surplus - lines [825, 886]
- [x] `cosmos-fund-theft-vulnerabilities-8-funds-missing-slippage-010` (13/21) 8. Funds Missing Slippage - lines [887, 1004]
- [ ] `cosmos-fund-theft-vulnerabilities-keywords-011` (8/21) Keywords - lines [1027, 1050]
- [ ] `cosmos-fund-theft-vulnerabilities-lines-of-code-003` (7/21) Lines of code - lines [595, 626]
- [ ] `cosmos-fund-theft-vulnerabilities-lines-of-code-008` (7/21) Lines of code - lines [780, 824]
- [ ] `cosmos-fund-theft-vulnerabilities-security-report-005` (6/21) Security Report - lines [653, 679]

Progress: 5/12 cards source-enriched for this file.

### `DB/cosmos/app-chain/governance/governance-voting-vulnerabilities.md`

- [x] `cosmos-governance-voting-vulnerabilities-1-governance-voting-power-mani-000` (14/21) 1. Governance Voting Power Manipulation - lines [186, 328]
- [ ] `cosmos-governance-voting-vulnerabilities-10-governance-timelock-bypass-010` (12/21) 10. Governance Timelock Bypass - lines [1177, 1265]
- [ ] `cosmos-governance-voting-vulnerabilities-2-governance-proposal-exploit-001` (11/21) 2. Governance Proposal Exploit - lines [329, 384]
- [x] `cosmos-governance-voting-vulnerabilities-3-governance-quorum-manipulati-003` (13/21) 3. Governance Quorum Manipulation - lines [452, 534]
- [x] `cosmos-governance-voting-vulnerabilities-4-governance-voting-lock-004` (13/21) 4. Governance Voting Lock - lines [535, 705]
- [x] `cosmos-governance-voting-vulnerabilities-5-governance-ballot-spam-005` (11/21) 5. Governance Ballot Spam - lines [706, 757]
- [x] `cosmos-governance-voting-vulnerabilities-6-governance-bribe-manipulatio-006` (12/21) 6. Governance Bribe Manipulation - lines [758, 810]
- [x] `cosmos-governance-voting-vulnerabilities-7-governance-offboard-exploit-007` (12/21) 7. Governance Offboard Exploit - lines [811, 920]
- [x] `cosmos-governance-voting-vulnerabilities-8-governance-voting-zero-weigh-008` (13/21) 8. Governance Voting Zero Weight - lines [921, 1042]
- [x] `cosmos-governance-voting-vulnerabilities-9-governance-parameter-change-009` (13/21) 9. Governance Parameter Change - lines [1043, 1176]
- [ ] `cosmos-governance-voting-vulnerabilities-di-culty-high-002` (10/21) Diculty: High - lines [385, 451]
- [ ] `cosmos-governance-voting-vulnerabilities-keywords-012` (8/21) Keywords - lines [1352, 1375]
- [ ] `cosmos-governance-voting-vulnerabilities-recommendation-011` (12/21) Recommendation - lines [1270, 1325]

Progress: 8/13 cards source-enriched for this file.

### `DB/cosmos/app-chain/hooks-callbacks/hook-callback-vulnerabilities.md`

- [x] `cosmos-hook-callback-vulnerabilities-1-hooks-before-after-000` (14/21) 1. Hooks Before After - lines [82, 194]
- [x] `cosmos-hook-callback-vulnerabilities-2-hooks-reentrancy-via-hook-001` (13/21) 2. Hooks Reentrancy Via Hook - lines [195, 293]
- [ ] `cosmos-hook-callback-vulnerabilities-keywords-002` (8/21) Keywords - lines [304, 327]

Progress: 2/3 cards source-enriched for this file.

### `DB/cosmos/app-chain/ibc/ibc-protocol-vulnerabilities.md`

- [x] `cosmos-ibc-protocol-vulnerabilities-1-ibc-channel-verification-000` (14/21) 1. Ibc Channel Verification - lines [114, 244]
- [x] `cosmos-ibc-protocol-vulnerabilities-2-ibc-packet-handling-001` (11/21) 2. Ibc Packet Handling - lines [245, 304]
- [x] `cosmos-ibc-protocol-vulnerabilities-3-ibc-version-negotiation-002` (11/21) 3. Ibc Version Negotiation - lines [305, 380]
- [x] `cosmos-ibc-protocol-vulnerabilities-4-ibc-middleware-bypass-003` (12/21) 4. Ibc Middleware Bypass - lines [381, 475]
- [ ] `cosmos-ibc-protocol-vulnerabilities-5-ibc-authentication-004` (11/21) 5. Ibc Authentication - lines [476, 564]
- [x] `cosmos-ibc-protocol-vulnerabilities-6-ibc-timeout-006` (12/21) 6. Ibc Timeout - lines [603, 670]
- [ ] `cosmos-ibc-protocol-vulnerabilities-keywords-007` (8/21) Keywords - lines [689, 712]
- [ ] `cosmos-ibc-protocol-vulnerabilities-vulnerability-report-005` (9/21) Vulnerability Report - lines [565, 602]

Progress: 5/8 cards source-enriched for this file.

### `DB/cosmos/app-chain/infrastructure/security-infrastructure-vulnerabilities.md`

- [x] `cosmos-security-infrastructure-vulnerabilities-1-infra-ssrf-000` (15/21) 1. Infra Ssrf - lines [120, 184]
- [ ] `cosmos-security-infrastructure-vulnerabilities-2-infra-private-key-002` (9/21) 2. Infra Private Key - lines [212, 237]
- [ ] `cosmos-security-infrastructure-vulnerabilities-3-infra-tss-004` (9/21) 3. Infra Tss - lines [265, 290]
- [x] `cosmos-security-infrastructure-vulnerabilities-4-infra-keyring-007` (13/21) 4. Infra Keyring - lines [337, 409]
- [ ] `cosmos-security-infrastructure-vulnerabilities-5-infra-error-handling-008` (12/21) 5. Infra Error Handling - lines [410, 441]
- [x] `cosmos-security-infrastructure-vulnerabilities-6-infra-deprecated-usage-010` (11/21) 6. Infra Deprecated Usage - lines [482, 550]
- [ ] `cosmos-security-infrastructure-vulnerabilities-description-005` (10/21) Description - lines [291, 305]
- [ ] `cosmos-security-infrastructure-vulnerabilities-description-006` (8/21) Description - lines [306, 336]
- [ ] `cosmos-security-infrastructure-vulnerabilities-di-culty-high-001` (6/21) Diculty: High - lines [185, 211]
- [ ] `cosmos-security-infrastructure-vulnerabilities-di-culty-high-003` (6/21) Diculty: High - lines [238, 264]
- [ ] `cosmos-security-infrastructure-vulnerabilities-keywords-011` (8/21) Keywords - lines [569, 592]
- [ ] `cosmos-security-infrastructure-vulnerabilities-vulnerability-report-009` (10/21) Vulnerability Report - lines [442, 481]

Progress: 3/12 cards source-enriched for this file.

### `DB/cosmos/app-chain/lifecycle/upgrade-migration-vulnerabilities.md`

- [x] `cosmos-upgrade-migration-vulnerabilities-1-lifecycle-upgrade-error-000` (15/21) 1. Lifecycle Upgrade Error - lines [141, 217]
- [ ] `cosmos-upgrade-migration-vulnerabilities-2-lifecycle-migration-failure-002` (11/21) 2. Lifecycle Migration Failure - lines [250, 292]
- [ ] `cosmos-upgrade-migration-vulnerabilities-3-lifecycle-init-error-004` (11/21) 3. Lifecycle Init Error - lines [325, 394]
- [x] `cosmos-upgrade-migration-vulnerabilities-4-lifecycle-storage-gap-006` (11/21) 4. Lifecycle Storage Gap - lines [441, 495]
- [x] `cosmos-upgrade-migration-vulnerabilities-5-lifecycle-module-registratio-007` (12/21) 5. Lifecycle Module Registration - lines [496, 581]
- [x] `cosmos-upgrade-migration-vulnerabilities-6-lifecycle-genesis-error-008` (12/21) 6. Lifecycle Genesis Error - lines [582, 634]
- [x] `cosmos-upgrade-migration-vulnerabilities-7-lifecycle-deployment-param-009` (13/21) 7. Lifecycle Deployment Param - lines [635, 699]
- [x] `cosmos-upgrade-migration-vulnerabilities-8-lifecycle-state-export-010` (13/21) 8. Lifecycle State Export - lines [700, 774]
- [x] `cosmos-upgrade-migration-vulnerabilities-9-lifecycle-version-compat-011` (12/21) 9. Lifecycle Version Compat - lines [775, 869]
- [ ] `cosmos-upgrade-migration-vulnerabilities-error-reporting-001` (6/21) Error Reporting - lines [218, 249]
- [ ] `cosmos-upgrade-migration-vulnerabilities-error-reporting-003` (6/21) Error Reporting - lines [293, 324]
- [ ] `cosmos-upgrade-migration-vulnerabilities-keywords-012` (8/21) Keywords - lines [894, 917]
- [ ] `cosmos-upgrade-migration-vulnerabilities-upgrades-005` (8/21) Upgrades - lines [395, 440]

Progress: 7/13 cards source-enriched for this file.

### `DB/cosmos/app-chain/liquidation/liquidation-auction-vulnerabilities.md`

- [x] `cosmos-liquidation-auction-vulnerabilities-1-auction-manipulation-000` (15/21) 1. Auction Manipulation - lines [124, 229]
- [x] `cosmos-liquidation-auction-vulnerabilities-2-auction-cdp-dust-001` (11/21) 2. Auction Cdp Dust - lines [230, 281]
- [x] `cosmos-liquidation-auction-vulnerabilities-3-debt-accounting-error-002` (13/21) 3. Debt Accounting Error - lines [282, 361]
- [x] `cosmos-liquidation-auction-vulnerabilities-4-lien-exploit-003` (13/21) 4. Lien Exploit - lines [362, 491]
- [ ] `cosmos-liquidation-auction-vulnerabilities-5-liquidation-accounting-004` (10/21) 5. Liquidation Accounting - lines [492, 519]
- [ ] `cosmos-liquidation-auction-vulnerabilities-around-11-2-price-manipulation-005` (12/21) Around 11.2% Price Manipulation with 14.5k ETH used - lines [520, 560]
- [ ] `cosmos-liquidation-auction-vulnerabilities-keywords-006` (8/21) Keywords - lines [577, 600]

Progress: 4/7 cards source-enriched for this file.

### `DB/cosmos/app-chain/liquidity/liquidity-pool-vulnerabilities.md`

- [x] `cosmos-liquidity-pool-vulnerabilities-1-liquidity-pool-manipulation-000` (14/21) 1. Liquidity Pool Manipulation - lines [92, 196]
- [ ] `cosmos-liquidity-pool-vulnerabilities-2-liquidity-imbalance-002` (11/21) 2. Liquidity Imbalance - lines [248, 294]
- [ ] `cosmos-liquidity-pool-vulnerabilities-around-11-2-price-manipulation-001` (12/21) Around 11.2% Price Manipulation with 14.5k ETH used - lines [197, 247]
- [ ] `cosmos-liquidity-pool-vulnerabilities-description-003` (8/21) Description - lines [295, 327]
- [ ] `cosmos-liquidity-pool-vulnerabilities-keywords-004` (8/21) Keywords - lines [338, 361]

Progress: 1/5 cards source-enriched for this file.

### `DB/cosmos/app-chain/mev/frontrunning-mev-vulnerabilities.md`

- [x] `cosmos-frontrunning-mev-vulnerabilities-1-mev-staking-frontrun-000` (15/21) 1. Mev Staking Frontrun - lines [145, 254]
- [x] `cosmos-frontrunning-mev-vulnerabilities-2-mev-slippage-exploit-001` (13/21) 2. Mev Slippage Exploit - lines [255, 423]
- [x] `cosmos-frontrunning-mev-vulnerabilities-3-mev-sandwich-002` (13/21) 3. Mev Sandwich - lines [424, 492]
- [x] `cosmos-frontrunning-mev-vulnerabilities-4-mev-block-stuffing-003` (11/21) 4. Mev Block Stuffing - lines [493, 548]
- [x] `cosmos-frontrunning-mev-vulnerabilities-5-mev-arbitrage-004` (13/21) 5. Mev Arbitrage - lines [549, 683]
- [ ] `cosmos-frontrunning-mev-vulnerabilities-6-mev-priority-005` (9/21) 6. Mev Priority - lines [684, 709]
- [ ] `cosmos-frontrunning-mev-vulnerabilities-7-mev-jit-liquidity-007` (12/21) 7. Mev Jit Liquidity - lines [756, 804]
- [ ] `cosmos-frontrunning-mev-vulnerabilities-data-validation-008` (6/21) Data Validation - lines [812, 843]
- [ ] `cosmos-frontrunning-mev-vulnerabilities-keywords-009` (8/21) Keywords - lines [864, 887]
- [ ] `cosmos-frontrunning-mev-vulnerabilities-umee-security-assessment-006` (5/21) Umee Security Assessment - lines [710, 755]

Progress: 5/10 cards source-enriched for this file.

### `DB/cosmos/app-chain/module-accounting/cosmos-module-vulnerabilities.md`

- [x] `cosmos-cosmos-module-vulnerabilities-1-module-bank-error-000` (15/21) 1. Module Bank Error - lines [161, 316]
- [x] `cosmos-cosmos-module-vulnerabilities-2-module-auth-error-001` (13/21) 2. Module Auth Error - lines [317, 439]
- [x] `cosmos-cosmos-module-vulnerabilities-3-module-distribution-002` (13/21) 3. Module Distribution - lines [440, 544]
- [x] `cosmos-cosmos-module-vulnerabilities-4-module-staking-specific-003` (13/21) 4. Module Staking Specific - lines [545, 695]
- [x] `cosmos-cosmos-module-vulnerabilities-5-module-slashing-specific-004` (13/21) 5. Module Slashing Specific - lines [696, 812]
- [x] `cosmos-cosmos-module-vulnerabilities-6-module-evidence-005` (13/21) 6. Module Evidence - lines [813, 899]
- [x] `cosmos-cosmos-module-vulnerabilities-7-module-crisis-006` (11/21) 7. Module Crisis - lines [900, 970]
- [x] `cosmos-cosmos-module-vulnerabilities-8-module-capability-007` (12/21) 8. Module Capability - lines [971, 1029]
- [ ] `cosmos-cosmos-module-vulnerabilities-keywords-008` (8/21) Keywords - lines [1052, 1075]

Progress: 8/9 cards source-enriched for this file.

### `DB/cosmos/app-chain/node-operator/minipool-node-vulnerabilities.md`

- [x] `cosmos-minipool-node-vulnerabilities-1-minipool-deposit-theft-000` (13/21) 1. Minipool Deposit Theft - lines [149, 253]
- [x] `cosmos-minipool-node-vulnerabilities-2-minipool-cancel-error-001` (11/21) 2. Minipool Cancel Error - lines [254, 319]
- [x] `cosmos-minipool-node-vulnerabilities-3-minipool-slash-avoidance-002` (12/21) 3. Minipool Slash Avoidance - lines [320, 400]
- [x] `cosmos-minipool-node-vulnerabilities-4-minipool-finalization-003` (12/21) 4. Minipool Finalization - lines [401, 496]
- [x] `cosmos-minipool-node-vulnerabilities-5-minipool-replay-004` (11/21) 5. Minipool Replay - lines [497, 548]
- [x] `cosmos-minipool-node-vulnerabilities-6-operator-registration-frontr-005` (12/21) 6. Operator Registration Frontrun - lines [549, 604]
- [x] `cosmos-minipool-node-vulnerabilities-7-operator-reward-leak-006` (11/21) 7. Operator Reward Leak - lines [605, 656]
- [ ] `cosmos-minipool-node-vulnerabilities-8-operator-key-fundable-007` (9/21) 8. Operator Key Fundable - lines [657, 682]
- [x] `cosmos-minipool-node-vulnerabilities-9-operator-deregistration-010` (13/21) 9. Operator Deregistration - lines [734, 867]
- [ ] `cosmos-minipool-node-vulnerabilities-critical-risk-report-008` (8/21) Critical Risk Report - lines [683, 706]
- [ ] `cosmos-minipool-node-vulnerabilities-keywords-011` (8/21) Keywords - lines [892, 915]
- [ ] `cosmos-minipool-node-vulnerabilities-severity-medium-risk-009` (6/21) Severity: Medium Risk - lines [707, 733]

Progress: 8/12 cards source-enriched for this file.

### `DB/cosmos/app-chain/oracle/oracle-price-vulnerabilities.md`

- [x] `cosmos-oracle-price-vulnerabilities-1-oracle-stale-price-000` (15/21) 1. Oracle Stale Price - lines [144, 272]
- [x] `cosmos-oracle-price-vulnerabilities-2-oracle-price-manipulation-001` (13/21) 2. Oracle Price Manipulation - lines [273, 341]
- [ ] `cosmos-oracle-price-vulnerabilities-3-oracle-dos-002` (11/21) 3. Oracle Dos - lines [342, 393]
- [x] `cosmos-oracle-price-vulnerabilities-4-oracle-deviation-exploit-004` (12/21) 4. Oracle Deviation Exploit - lines [463, 521]
- [x] `cosmos-oracle-price-vulnerabilities-5-oracle-frontrunning-005` (13/21) 5. Oracle Frontrunning - lines [522, 583]
- [x] `cosmos-oracle-price-vulnerabilities-6-oracle-missing-stake-006` (11/21) 6. Oracle Missing Stake - lines [584, 663]
- [x] `cosmos-oracle-price-vulnerabilities-7-oracle-chainlink-specific-007` (11/21) 7. Oracle Chainlink Specific - lines [664, 716]
- [x] `cosmos-oracle-price-vulnerabilities-8-oracle-wrong-price-usage-008` (12/21) 8. Oracle Wrong Price Usage - lines [717, 783]
- [ ] `cosmos-oracle-price-vulnerabilities-keywords-009` (8/21) Keywords - lines [806, 829]
- [ ] `cosmos-oracle-price-vulnerabilities-umee-security-assessment-003` (9/21) Umee Security Assessment - lines [394, 462]

Progress: 7/10 cards source-enriched for this file.

### `DB/cosmos/app-chain/reentrancy/reentrancy-vulnerabilities.md`

- [x] `cosmos-reentrancy-vulnerabilities-1-reentrancy-classic-000` (14/21) 1. Reentrancy Classic - lines [82, 165]
- [x] `cosmos-reentrancy-vulnerabilities-2-reentrancy-callback-002` (13/21) 2. Reentrancy Callback - lines [198, 296]
- [ ] `cosmos-reentrancy-vulnerabilities-keywords-003` (8/21) Keywords - lines [307, 330]
- [ ] `cosmos-reentrancy-vulnerabilities-lines-of-code-001` (7/21) Lines of code - lines [166, 197]

Progress: 2/4 cards source-enriched for this file.

### `DB/cosmos/app-chain/rewards/reward-calculation-vulnerabilities.md`

- [x] `cosmos-reward-calculation-vulnerabilities-1-reward-calculation-incorrect-000` (15/21) 1. Reward Calculation Incorrect - lines [149, 326]
- [x] `cosmos-reward-calculation-vulnerabilities-2-reward-per-share-error-001` (15/21) 2. Reward Per Share Error - lines [327, 473]
- [x] `cosmos-reward-calculation-vulnerabilities-3-reward-delayed-balance-002` (13/21) 3. Reward Delayed Balance - lines [474, 606]
- [x] `cosmos-reward-calculation-vulnerabilities-4-reward-decimal-mismatch-003` (11/21) 4. Reward Decimal Mismatch - lines [607, 658]
- [x] `cosmos-reward-calculation-vulnerabilities-5-reward-weight-error-004` (13/21) 5. Reward Weight Error - lines [659, 769]
- [x] `cosmos-reward-calculation-vulnerabilities-6-reward-historical-loss-005` (11/21) 6. Reward Historical Loss - lines [770, 822]
- [ ] `cosmos-reward-calculation-vulnerabilities-7-reward-pool-share-006` (11/21) 7. Reward Pool Share - lines [823, 869]
- [ ] `cosmos-reward-calculation-vulnerabilities-description-007` (8/21) Description - lines [870, 902]
- [ ] `cosmos-reward-calculation-vulnerabilities-keywords-008` (8/21) Keywords - lines [923, 946]

Progress: 6/9 cards source-enriched for this file.

### `DB/cosmos/app-chain/rewards/reward-distribution-failures.md`

- [x] `cosmos-reward-distribution-failures-1-reward-stuck-locked-000` (15/21) 1. Reward Stuck Locked - lines [167, 343]
- [x] `cosmos-reward-distribution-failures-2-reward-distribution-dos-001` (13/21) 2. Reward Distribution Dos - lines [344, 513]
- [x] `cosmos-reward-distribution-failures-3-reward-missing-update-002` (13/21) 3. Reward Missing Update - lines [514, 647]
- [x] `cosmos-reward-distribution-failures-4-reward-after-removal-003` (15/21) 4. Reward After Removal - lines [648, 816]
- [x] `cosmos-reward-distribution-failures-5-reward-unclaimed-loss-004` (13/21) 5. Reward Unclaimed Loss - lines [817, 960]
- [x] `cosmos-reward-distribution-failures-6-reward-distribution-unfair-005` (13/21) 6. Reward Distribution Unfair - lines [961, 1083]
- [x] `cosmos-reward-distribution-failures-7-reward-epoch-timing-006` (13/21) 7. Reward Epoch Timing - lines [1084, 1217]
- [ ] `cosmos-reward-distribution-failures-keywords-007` (8/21) Keywords - lines [1238, 1261]

Progress: 7/8 cards source-enriched for this file.

### `DB/cosmos/app-chain/rewards/reward-theft-manipulation.md`

- [x] `cosmos-reward-theft-manipulation-1-reward-flashloan-theft-000` (15/21) 1. Reward Flashloan Theft - lines [164, 302]
- [ ] `cosmos-reward-theft-manipulation-2-reward-frontrunning-001` (12/21) 2. Reward Frontrunning - lines [303, 363]
- [x] `cosmos-reward-theft-manipulation-3-reward-orphaned-capture-003` (12/21) 3. Reward Orphaned Capture - lines [400, 477]
- [x] `cosmos-reward-theft-manipulation-4-reward-dilution-004` (13/21) 4. Reward Dilution - lines [478, 576]
- [x] `cosmos-reward-theft-manipulation-5-reward-gauge-exploit-005` (13/21) 5. Reward Gauge Exploit - lines [577, 705]
- [x] `cosmos-reward-theft-manipulation-6-reward-vault-interaction-006` (13/21) 6. Reward Vault Interaction - lines [706, 907]
- [x] `cosmos-reward-theft-manipulation-7-reward-escrow-assignment-007` (13/21) 7. Reward Escrow Assignment - lines [908, 1000]
- [x] `cosmos-reward-theft-manipulation-8-reward-commission-error-008` (13/21) 8. Reward Commission Error - lines [1001, 1076]
- [ ] `cosmos-reward-theft-manipulation-description-002` (10/21) Description - lines [364, 399]
- [ ] `cosmos-reward-theft-manipulation-keywords-009` (8/21) Keywords - lines [1099, 1122]

Progress: 7/10 cards source-enriched for this file.

### `DB/cosmos/app-chain/signature/signature-replay-vulnerabilities.md`

- [x] `cosmos-signature-replay-vulnerabilities-1-signature-verification-missi-000` (15/21) 1. Signature Verification Missing - lines [150, 332]
- [x] `cosmos-signature-replay-vulnerabilities-2-signature-replay-001` (12/21) 2. Signature Replay - lines [333, 390]
- [ ] `cosmos-signature-replay-vulnerabilities-3-signature-cross-chain-replay-002` (9/21) 3. Signature Cross Chain Replay - lines [391, 416]
- [x] `cosmos-signature-replay-vulnerabilities-4-signature-forgery-004` (12/21) 4. Signature Forgery - lines [450, 558]
- [x] `cosmos-signature-replay-vulnerabilities-5-signature-duplicate-005` (11/21) 5. Signature Duplicate - lines [559, 631]
- [ ] `cosmos-signature-replay-vulnerabilities-6-signature-eip155-missing-006` (11/21) 6. Signature Eip155 Missing - lines [632, 664]
- [ ] `cosmos-signature-replay-vulnerabilities-7-signature-key-management-008` (11/21) 7. Signature Key Management - lines [730, 766]
- [x] `cosmos-signature-replay-vulnerabilities-8-signature-malleability-010` (13/21) 8. Signature Malleability - lines [794, 956]
- [ ] `cosmos-signature-replay-vulnerabilities-di-culty-high-009` (6/21) Diculty: High - lines [767, 793]
- [ ] `cosmos-signature-replay-vulnerabilities-keywords-011` (8/21) Keywords - lines [979, 1002]
- [ ] `cosmos-signature-replay-vulnerabilities-validator-issues-in-liquid-sta-007` (12/21) Validator Issues in Liquid Staking - lines [665, 729]
- [ ] `cosmos-signature-replay-vulnerabilities-vulnerability-report-003` (7/21) Vulnerability Report - lines [417, 449]

Progress: 5/12 cards source-enriched for this file.

### `DB/cosmos/app-chain/slashing/slashing-accounting-errors.md`

- [x] `cosmos-slashing-accounting-errors-1-slashing-amount-incorrect-000` (15/21) 1. Slashing Amount Incorrect - lines [166, 360]
- [x] `cosmos-slashing-accounting-errors-2-slashing-share-dilution-001` (11/21) 2. Slashing Share Dilution - lines [361, 412]
- [x] `cosmos-slashing-accounting-errors-3-slashing-balance-update-erro-002` (13/21) 3. Slashing Balance Update Error - lines [413, 547]
- [x] `cosmos-slashing-accounting-errors-4-slashing-reward-interaction-003` (13/21) 4. Slashing Reward Interaction - lines [548, 686]
- [x] `cosmos-slashing-accounting-errors-5-slashing-pending-operations-004` (15/21) 5. Slashing Pending Operations - lines [687, 818]
- [x] `cosmos-slashing-accounting-errors-6-slashing-principal-error-005` (12/21) 6. Slashing Principal Error - lines [819, 887]
- [x] `cosmos-slashing-accounting-errors-7-slashing-penalty-system-006` (13/21) 7. Slashing Penalty System - lines [888, 989]
- [x] `cosmos-slashing-accounting-errors-8-slashing-double-punishment-007` (13/21) 8. Slashing Double Punishment - lines [990, 1077]
- [ ] `cosmos-slashing-accounting-errors-keywords-008` (8/21) Keywords - lines [1100, 1123]

Progress: 8/9 cards source-enriched for this file.

### `DB/cosmos/app-chain/slashing/slashing-evasion-frontrunning.md`

- [ ] `cosmos-slashing-evasion-frontrunning-1-slashing-frontrun-exit-001` (9/21) 1. Slashing Frontrun Exit - lines [209, 234]
- [x] `cosmos-slashing-evasion-frontrunning-2-slashing-cooldown-exploit-003` (15/21) 2. Slashing Cooldown Exploit - lines [325, 445]
- [x] `cosmos-slashing-evasion-frontrunning-3-slashing-delegation-bypass-004` (13/21) 3. Slashing Delegation Bypass - lines [446, 530]
- [x] `cosmos-slashing-evasion-frontrunning-4-slashing-insufficient-deposi-005` (11/21) 4. Slashing Insufficient Deposit - lines [531, 589]
- [x] `cosmos-slashing-evasion-frontrunning-5-slashing-external-block-006` (11/21) 5. Slashing External Block - lines [590, 654]
- [x] `cosmos-slashing-evasion-frontrunning-6-slashing-queued-excluded-007` (13/21) 6. Slashing Queued Excluded - lines [655, 776]
- [x] `cosmos-slashing-evasion-frontrunning-7-slashing-unregistered-operat-008` (11/21) 7. Slashing Unregistered Operator - lines [777, 863]
- [ ] `cosmos-slashing-evasion-frontrunning-8-slashing-mechanism-abuse-009` (9/21) 8. Slashing Mechanism Abuse - lines [864, 889]
- [ ] `cosmos-slashing-evasion-frontrunning-description-002` (11/21) Description - lines [235, 324]
- [ ] `cosmos-slashing-evasion-frontrunning-description-010` (12/21) Description - lines [890, 1002]
- [ ] `cosmos-slashing-evasion-frontrunning-slashing-evasion-frontrunning--000` (11/21) Slashing Evasion & Frontrunning Vulnerabilities - lines [154, 195]

Progress: 6/11 cards source-enriched for this file.

### `DB/cosmos/app-chain/staking/delegation-redelegation-vulnerabilities.md`

- [x] `cosmos-delegation-redelegation-vulnerabilities-1-delegation-self-manipulation-000` (14/21) 1. Delegation Self Manipulation - lines [162, 235]
- [ ] `cosmos-delegation-redelegation-vulnerabilities-2-delegation-dos-revert-002` (11/21) 2. Delegation Dos Revert - lines [297, 339]
- [x] `cosmos-delegation-redelegation-vulnerabilities-3-delegation-state-inconsisten-005` (13/21) 3. Delegation State Inconsistency - lines [410, 479]
- [ ] `cosmos-delegation-redelegation-vulnerabilities-4-delegation-to-inactive-006` (9/21) 4. Delegation To Inactive - lines [480, 505]
- [x] `cosmos-delegation-redelegation-vulnerabilities-5-delegation-frontrunning-008` (11/21) 5. Delegation Frontrunning - lines [589, 640]
- [x] `cosmos-delegation-redelegation-vulnerabilities-6-delegation-reward-manipulati-009` (13/21) 6. Delegation Reward Manipulation - lines [641, 777]
- [x] `cosmos-delegation-redelegation-vulnerabilities-7-delegation-redelegation-erro-010` (13/21) 7. Delegation Redelegation Error - lines [778, 948]
- [x] `cosmos-delegation-redelegation-vulnerabilities-8-delegation-unbonding-exploit-011` (12/21) 8. Delegation Unbonding Exploit - lines [949, 1068]
- [ ] `cosmos-delegation-redelegation-vulnerabilities-denial-of-service-vulnerabilit-003` (6/21) Denial of Service Vulnerability - lines [340, 350]
- [ ] `cosmos-delegation-redelegation-vulnerabilities-denial-of-service-vulnerabilit-007` (10/21) Denial of Service Vulnerability - lines [506, 588]
- [ ] `cosmos-delegation-redelegation-vulnerabilities-keywords-012` (8/21) Keywords - lines [1091, 1114]
- [ ] `cosmos-delegation-redelegation-vulnerabilities-validator-issues-in-liquid-sta-001` (12/21) Validator Issues in Liquid Staking - lines [236, 296]
- [ ] `cosmos-delegation-redelegation-vulnerabilities-vulnerability-details-004` (11/21) Vulnerability Details - lines [358, 409]

Progress: 6/13 cards source-enriched for this file.

### `DB/cosmos/app-chain/staking/stake-deposit-vulnerabilities.md`

- [x] `cosmos-stake-deposit-vulnerabilities-1-staking-deposit-amount-track-000` (15/21) 1. Staking Deposit Amount Tracking Errors - lines [186, 359]
- [x] `cosmos-stake-deposit-vulnerabilities-2-missing-or-insufficient-depo-001` (13/21) 2. Missing or Insufficient Deposit Validation - lines [360, 494]
- [ ] `cosmos-stake-deposit-vulnerabilities-3-staking-deposit-frontrunning-002` (12/21) 3. Staking Deposit Frontrunning - lines [495, 538]
- [x] `cosmos-stake-deposit-vulnerabilities-4-staking-balance-desynchroniz-004` (13/21) 4. Staking Balance Desynchronization - lines [633, 774]
- [x] `cosmos-stake-deposit-vulnerabilities-5-deposit-queue-processing-err-005` (13/21) 5. Deposit Queue Processing Errors - lines [775, 901]
- [ ] `cosmos-stake-deposit-vulnerabilities-6-first-depositor-share-inflat-006` (9/21) 6. First Depositor / Share Inflation Attack - lines [902, 927]
- [x] `cosmos-stake-deposit-vulnerabilities-7-incorrect-staking-calculatio-009` (13/21) 7. Incorrect Staking Calculation Logic - lines [1023, 1180]
- [x] `cosmos-stake-deposit-vulnerabilities-8-broken-staking-invariants-010` (11/21) 8. Broken Staking Invariants - lines [1181, 1337]
- [ ] `cosmos-stake-deposit-vulnerabilities-description-003` (14/21) Description - lines [539, 632]
- [ ] `cosmos-stake-deposit-vulnerabilities-description-007` (14/21) Description - lines [928, 982]
- [ ] `cosmos-stake-deposit-vulnerabilities-keywords-011` (8/21) Keywords - lines [1360, 1383]
- [ ] `cosmos-stake-deposit-vulnerabilities-severity-008` (11/21) Severity - lines [983, 1022]

Progress: 6/12 cards source-enriched for this file.

### `DB/cosmos/app-chain/staking/unstake-withdrawal-vulnerabilities.md`

- [x] `cosmos-unstake-withdrawal-vulnerabilities-1-unstake-cooldown-bypass-000` (17/21) 1. Unstake Cooldown Bypass - lines [187, 389]
- [ ] `cosmos-unstake-withdrawal-vulnerabilities-2-unstake-withdrawal-dos-001` (12/21) 2. Unstake Withdrawal Dos - lines [390, 445]
- [x] `cosmos-unstake-withdrawal-vulnerabilities-3-unstake-withdrawal-accountin-003` (13/21) 3. Unstake Withdrawal Accounting - lines [517, 625]
- [x] `cosmos-unstake-withdrawal-vulnerabilities-4-unstake-queue-manipulation-004` (13/21) 4. Unstake Queue Manipulation - lines [626, 772]
- [x] `cosmos-unstake-withdrawal-vulnerabilities-5-unstake-before-slash-005` (13/21) 5. Unstake Before Slash - lines [773, 886]
- [x] `cosmos-unstake-withdrawal-vulnerabilities-6-unstake-emergency-006` (13/21) 6. Unstake Emergency - lines [887, 1028]
- [x] `cosmos-unstake-withdrawal-vulnerabilities-7-unstake-pending-not-tracked-007` (13/21) 7. Unstake Pending Not Tracked - lines [1029, 1170]
- [x] `cosmos-unstake-withdrawal-vulnerabilities-8-unstake-lock-funds-008` (13/21) 8. Unstake Lock Funds - lines [1171, 1300]
- [ ] `cosmos-unstake-withdrawal-vulnerabilities-description-002` (11/21) Description - lines [446, 516]
- [ ] `cosmos-unstake-withdrawal-vulnerabilities-keywords-009` (8/21) Keywords - lines [1323, 1346]

Progress: 7/10 cards source-enriched for this file.

### `DB/cosmos/app-chain/staking/validator-management-vulnerabilities.md`

- [x] `cosmos-validator-management-vulnerabilities-1-validator-registration-bypas-000` (15/21) 1. Validator Registration Bypass - lines [192, 399]
- [x] `cosmos-validator-management-vulnerabilities-10-validator-can-skip-exit-012` (13/21) 10. Validator Can Skip Exit - lines [1341, 1414]
- [x] `cosmos-validator-management-vulnerabilities-11-validator-governance-power-013` (13/21) 11. Validator Governance Power - lines [1415, 1477]
- [ ] `cosmos-validator-management-vulnerabilities-2-validator-removal-failure-001` (12/21) 2. Validator Removal Failure - lines [400, 470]
- [x] `cosmos-validator-management-vulnerabilities-3-validator-set-manipulation-003` (13/21) 3. Validator Set Manipulation - lines [522, 712]
- [x] `cosmos-validator-management-vulnerabilities-4-validator-key-rotation-004` (12/21) 4. Validator Key Rotation - lines [713, 817]
- [x] `cosmos-validator-management-vulnerabilities-5-validator-commission-exploit-005` (12/21) 5. Validator Commission Exploit - lines [818, 921]
- [ ] `cosmos-validator-management-vulnerabilities-6-validator-status-transition-006` (12/21) 6. Validator Status Transition - lines [922, 983]
- [x] `cosmos-validator-management-vulnerabilities-7-validator-dust-collateral-008` (13/21) 7. Validator Dust Collateral - lines [1015, 1116]
- [x] `cosmos-validator-management-vulnerabilities-8-validator-score-manipulation-009` (13/21) 8. Validator Score Manipulation - lines [1117, 1271]
- [ ] `cosmos-validator-management-vulnerabilities-9-validator-operator-mismatch-010` (9/21) 9. Validator Operator Mismatch - lines [1272, 1297]
- [ ] `cosmos-validator-management-vulnerabilities-description-011` (11/21) Description - lines [1298, 1340]
- [ ] `cosmos-validator-management-vulnerabilities-issue-with-validator-removal-a-007` (8/21) Issue with Validator Removal and State Desynchronization - lines [984, 1014]
- [ ] `cosmos-validator-management-vulnerabilities-keywords-014` (8/21) Keywords - lines [1504, 1527]
- [ ] `cosmos-validator-management-vulnerabilities-severity-002` (10/21) Severity - lines [471, 521]

Progress: 8/15 cards source-enriched for this file.

### `DB/cosmos/app-chain/state-management/state-store-vulnerabilities.md`

- [x] `cosmos-state-store-vulnerabilities-1-state-store-error-000` (14/21) 1. State Store Error - lines [101, 164]
- [x] `cosmos-state-store-vulnerabilities-2-state-iterator-error-002` (11/21) 2. State Iterator Error - lines [243, 308]
- [x] `cosmos-state-store-vulnerabilities-3-state-snapshot-error-003` (12/21) 3. State Snapshot Error - lines [309, 394]
- [ ] `cosmos-state-store-vulnerabilities-4-state-migration-error-004` (9/21) 4. State Migration Error - lines [395, 420]
- [ ] `cosmos-state-store-vulnerabilities-error-reporting-005` (6/21) Error Reporting - lines [421, 452]
- [ ] `cosmos-state-store-vulnerabilities-keywords-006` (8/21) Keywords - lines [467, 490]
- [ ] `cosmos-state-store-vulnerabilities-medium-risk-severity-report-001` (9/21) Medium Risk Severity Report - lines [165, 242]

Progress: 3/7 cards source-enriched for this file.

### `DB/cosmos/app-chain/timing/epoch-timing-vulnerabilities.md`

- [x] `cosmos-epoch-timing-vulnerabilities-1-timing-epoch-snapshot-000` (14/21) 1. Timing Epoch Snapshot - lines [151, 259]
- [x] `cosmos-epoch-timing-vulnerabilities-2-timing-cooldown-bypass-001` (15/21) 2. Timing Cooldown Bypass - lines [260, 388]
- [x] `cosmos-epoch-timing-vulnerabilities-3-timing-timestamp-boundary-002` (12/21) 3. Timing Timestamp Boundary - lines [389, 475]
- [x] `cosmos-epoch-timing-vulnerabilities-4-timing-unbonding-change-003` (11/21) 4. Timing Unbonding Change - lines [476, 545]
- [x] `cosmos-epoch-timing-vulnerabilities-5-timing-epoch-duration-break-004` (12/21) 5. Timing Epoch Duration Break - lines [546, 600]
- [x] `cosmos-epoch-timing-vulnerabilities-6-timing-expiration-bypass-005` (12/21) 6. Timing Expiration Bypass - lines [601, 687]
- [x] `cosmos-epoch-timing-vulnerabilities-7-timing-block-time-006` (13/21) 7. Timing Block Time - lines [688, 758]
- [ ] `cosmos-epoch-timing-vulnerabilities-8-timing-race-condition-007` (9/21) 8. Timing Race Condition - lines [759, 784]
- [ ] `cosmos-epoch-timing-vulnerabilities-keywords-009` (8/21) Keywords - lines [928, 951]
- [ ] `cosmos-epoch-timing-vulnerabilities-medium-risk-severity-report-008` (10/21) Medium Risk Severity Report - lines [785, 905]

Progress: 7/10 cards source-enriched for this file.

### `DB/cosmos/app-chain/tokens/token-handling-vulnerabilities.md`

- [x] `cosmos-token-handling-vulnerabilities-1-token-fee-on-transfer-000` (13/21) 1. Token Fee On Transfer - lines [188, 245]
- [x] `cosmos-token-handling-vulnerabilities-10-token-supply-tracking-011` (12/21) 10. Token Supply Tracking - lines [1237, 1314]
- [x] `cosmos-token-handling-vulnerabilities-11-token-denom-handling-012` (13/21) 11. Token Denom Handling - lines [1315, 1477]
- [ ] `cosmos-token-handling-vulnerabilities-2-token-rebasing-002` (12/21) 2. Token Rebasing - lines [369, 419]
- [x] `cosmos-token-handling-vulnerabilities-3-token-approval-error-004` (12/21) 3. Token Approval Error - lines [459, 553]
- [x] `cosmos-token-handling-vulnerabilities-4-token-unlimited-mint-005` (12/21) 4. Token Unlimited Mint - lines [554, 646]
- [x] `cosmos-token-handling-vulnerabilities-5-token-burn-error-006` (12/21) 5. Token Burn Error - lines [647, 780]
- [x] `cosmos-token-handling-vulnerabilities-6-token-transfer-hook-007` (13/21) 6. Token Transfer Hook - lines [781, 916]
- [x] `cosmos-token-handling-vulnerabilities-7-token-nft-handling-008` (13/21) 7. Token Nft Handling - lines [917, 1078]
- [x] `cosmos-token-handling-vulnerabilities-8-token-decimal-handling-009` (13/21) 8. Token Decimal Handling - lines [1079, 1184]
- [x] `cosmos-token-handling-vulnerabilities-9-token-zrc20-bypass-010` (11/21) 9. Token Zrc20 Bypass - lines [1185, 1236]
- [ ] `cosmos-token-handling-vulnerabilities-keywords-013` (8/21) Keywords - lines [1504, 1527]
- [ ] `cosmos-token-handling-vulnerabilities-lines-of-code-001` (9/21) Lines of code - lines [246, 368]
- [ ] `cosmos-token-handling-vulnerabilities-superform-audit-summary-003` (9/21) Superform Audit Summary - lines [420, 458]

Progress: 10/14 cards source-enriched for this file.

### `DB/cosmos/app-chain/validation/input-validation-vulnerabilities.md`

- [x] `cosmos-input-validation-vulnerabilities-1-validation-zero-check-missin-000` (15/21) 1. Validation Zero Check Missing - lines [197, 370]
- [ ] `cosmos-input-validation-vulnerabilities-10-validation-logic-error-010` (9/21) 10. Validation Logic Error - lines [1167, 1192]
- [x] `cosmos-input-validation-vulnerabilities-11-validation-msg-missing-012` (11/21) 11. Validation Msg Missing - lines [1273, 1337]
- [x] `cosmos-input-validation-vulnerabilities-12-validation-length-check-013` (13/21) 12. Validation Length Check - lines [1338, 1492]
- [x] `cosmos-input-validation-vulnerabilities-2-validation-bounds-missing-001` (11/21) 2. Validation Bounds Missing - lines [371, 425]
- [x] `cosmos-input-validation-vulnerabilities-3-validation-state-check-missi-002` (13/21) 3. Validation State Check Missing - lines [426, 571]
- [x] `cosmos-input-validation-vulnerabilities-4-validation-percentage-overfl-003` (11/21) 4. Validation Percentage Overflow - lines [572, 632]
- [x] `cosmos-input-validation-vulnerabilities-5-validation-address-normaliza-004` (12/21) 5. Validation Address Normalization - lines [633, 696]
- [x] `cosmos-input-validation-vulnerabilities-6-validation-duplicate-missing-005` (12/21) 6. Validation Duplicate Missing - lines [697, 817]
- [x] `cosmos-input-validation-vulnerabilities-7-validation-config-bypass-006` (11/21) 7. Validation Config Bypass - lines [818, 877]
- [ ] `cosmos-input-validation-vulnerabilities-8-validation-input-general-007` (11/21) 8. Validation Input General - lines [878, 952]
- [x] `cosmos-input-validation-vulnerabilities-9-validation-incorrect-check-009` (13/21) 9. Validation Incorrect Check - lines [1027, 1166]
- [ ] `cosmos-input-validation-vulnerabilities-keywords-014` (8/21) Keywords - lines [1519, 1542]
- [ ] `cosmos-input-validation-vulnerabilities-lombard-transfer-signing-strat-008` (8/21) Lombard Transfer Signing Strategy - lines [953, 1026]
- [ ] `cosmos-input-validation-vulnerabilities-severity-011` (9/21) Severity - lines [1193, 1272]

Progress: 10/15 cards source-enriched for this file.

### `DB/cosmos/app-chain/vault/vault-share-vulnerabilities.md`

- [x] `cosmos-vault-share-vulnerabilities-1-vault-share-inflation-000` (17/21) 1. Vault Share Inflation - lines [162, 365]
- [x] `cosmos-vault-share-vulnerabilities-2-vault-share-calculation-001` (13/21) 2. Vault Share Calculation - lines [366, 500]
- [x] `cosmos-vault-share-vulnerabilities-3-vault-deposit-theft-002` (13/21) 3. Vault Deposit Theft - lines [501, 575]
- [ ] `cosmos-vault-share-vulnerabilities-4-vault-withdrawal-error-003` (9/21) 4. Vault Withdrawal Error - lines [576, 600]
- [x] `cosmos-vault-share-vulnerabilities-5-vault-tvl-manipulation-006` (11/21) 5. Vault Tvl Manipulation - lines [636, 722]
- [x] `cosmos-vault-share-vulnerabilities-6-vault-strategy-loss-007` (13/21) 6. Vault Strategy Loss - lines [723, 809]
- [x] `cosmos-vault-share-vulnerabilities-7-vault-griefing-008` (13/21) 7. Vault Griefing - lines [810, 899]
- [x] `cosmos-vault-share-vulnerabilities-8-vault-insolvency-009` (13/21) 8. Vault Insolvency - lines [900, 1014]
- [ ] `cosmos-vault-share-vulnerabilities-keywords-010` (8/21) Keywords - lines [1037, 1060]
- [ ] `cosmos-vault-share-vulnerabilities-superform-audit-summary-005` (6/21) Superform Audit Summary - lines [609, 635]

Progress: 7/10 cards source-enriched for this file.

### `DB/general/access-control/access-control-vulnerabilities.md`

- [ ] `general-security-access-control-vulnerabilities-fix-3-validate-external-calls-011` (7/21) Fix 3: Validate External Calls - lines [577, 608]
- [ ] `general-security-access-control-vulnerabilities-fix-4-validate-msg-sender-auth-012` (8/21) Fix 4: Validate msg.sender Authority - lines [609, 639]
- [ ] `general-security-access-control-vulnerabilities-fix-5-protect-critical-paramet-013` (9/21) Fix 5: Protect Critical Parameter Updates - lines [640, 678]
- [ ] `general-security-access-control-vulnerabilities-pattern-1-unprotected-mint-bur-001` (6/21) Pattern 1: Unprotected Mint/Burn Functions (CRITICAL) - lines [142, 181]
- [ ] `general-security-access-control-vulnerabilities-pattern-2-unprotected-initiali-002` (6/21) Pattern 2: Unprotected Initialization (CRITICAL) - lines [182, 222]
- [ ] `general-security-access-control-vulnerabilities-pattern-3-arbitrary-external-c-003` (6/21) Pattern 3: Arbitrary External Call (CRITICAL) - lines [223, 275]
- [ ] `general-security-access-control-vulnerabilities-pattern-4-missing-msg-sender-v-004` (6/21) Pattern 4: Missing msg.sender Validation (HIGH) - lines [276, 325]
- [ ] `general-security-access-control-vulnerabilities-pattern-5-unprotected-critical-005` (6/21) Pattern 5: Unprotected Critical Parameter Updates (HIGH) - lines [326, 367]
- [ ] `general-security-access-control-vulnerabilities-pattern-6-unprotected-internal-006` (6/21) Pattern 6: Unprotected Internal Functions Made External (HIGH) - lines [368, 399]
- [ ] `general-security-access-control-vulnerabilities-pattern-7-mev-bot-access-contr-007` (6/21) Pattern 7: MEV Bot Access Control (HIGH) - lines [400, 422]

Progress: 0/10 cards source-enriched for this file.

### `DB/general/access-control/defihacklabs-access-control-2021-2022-patterns.md`

- [ ] `general-security-defihacklabs-access-control-2021-2022-pa-invariant-checks-004` (8/21) Invariant Checks - lines [656, 670]
- [ ] `general-security-defihacklabs-access-control-2021-2022-pa-static-analysis-003` (4/21) Static Analysis - lines [628, 655]

Progress: 0/2 cards source-enriched for this file.

### `DB/general/access-control/defihacklabs-access-control-2023-patterns.md`

- [ ] `general-security-defihacklabs-access-control-2023-pattern-1-public-mint-public-burn-on-t-001` (9/21) 1. Public Mint + Public Burn on Token Contract (SafeMoon $8.9M) - lines [129, 198]
- [ ] `general-security-defihacklabs-access-control-2023-pattern-2-public-fee-transfer-function-002` (8/21) 2. Public Fee Transfer Function on DEX Pair (LeetSwap $630K) - lines [199, 254]
- [ ] `general-security-defihacklabs-access-control-2023-pattern-3-aggregator-arbitrary-sender--003` (8/21) 3. Aggregator Arbitrary-Sender Swap (SwapX $1M) - lines [255, 312]
- [ ] `general-security-defihacklabs-access-control-2023-pattern-4-token-lock-claim-with-migrat-004` (8/21) 4. Token Lock/Claim with Migration Vulnerability (SHIDO $230K) - lines [313, 358]
- [ ] `general-security-defihacklabs-access-control-2023-pattern-5-router-bot-authorization-fai-005` (8/21) 5. Router/Bot Authorization Failures (Maestro $630K, UniBot $84K) - lines [359, 394]

Progress: 0/5 cards source-enriched for this file.

### `DB/general/access-control/defihacklabs-access-control-2024-2025.md`

- [ ] `general-security-defihacklabs-access-control-2024-2025-1-missing-access-control-on-mo-001` (9/21) 1. Missing Access Control on Module Initialization - lines [112, 164]
- [ ] `general-security-defihacklabs-access-control-2024-2025-2-missing-caller-restriction-o-002` (9/21) 2. Missing Caller Restriction on Core Execution Function - lines [165, 220]
- [ ] `general-security-defihacklabs-access-control-2024-2025-3-public-mint-function-on-coll-003` (9/21) 3. Public Mint Function on Collateral Token - lines [221, 274]
- [ ] `general-security-defihacklabs-access-control-2024-2025-4-unverified-contract-with-ext-004` (8/21) 4. Unverified Contract with External Transfer Proxy - lines [275, 310]
- [ ] `general-security-defihacklabs-access-control-2024-2025-5-missing-msg-sender-validatio-005` (9/21) 5. Missing msg.sender Validation in Pool Exit - lines [311, 365]

Progress: 0/5 cards source-enriched for this file.

### `DB/general/access-control/defihacklabs-access-control-patterns.md`

- [ ] `general-security-defihacklabs-access-control-patterns-1-unprotected-token-mint-burn-001` (9/21) 1. Unprotected Token Mint / Burn - lines [106, 166]
- [ ] `general-security-defihacklabs-access-control-patterns-2-unprotected-migration-functi-002` (8/21) 2. Unprotected Migration Function - lines [167, 204]
- [ ] `general-security-defihacklabs-access-control-patterns-3-unprotected-configuration-se-003` (8/21) 3. Unprotected Configuration Setter - lines [205, 251]
- [ ] `general-security-defihacklabs-access-control-patterns-4-missing-token-registry-valid-004` (8/21) 4. Missing Token Registry Validation - lines [252, 297]

Progress: 0/4 cards source-enriched for this file.

### `DB/general/arbitrary-call/arbitrary-external-call-vulnerabilities.md`

- [ ] `general-security-arbitrary-external-call-vulnerabilities-critical-exploits-1m-008` (6/21) Critical Exploits ($1M+) - lines [978, 991]
- [ ] `general-security-arbitrary-external-call-vulnerabilities-fix-1-target-address-whitelist-001` (7/21) Fix 1: Target Address Whitelist - lines [824, 840]
- [ ] `general-security-arbitrary-external-call-vulnerabilities-fix-2-function-selector-whitel-002` (7/21) Fix 2: Function Selector Whitelist - lines [841, 857]
- [ ] `general-security-arbitrary-external-call-vulnerabilities-high-severity-exploits-100k-1m-009` (6/21) High-Severity Exploits ($100K-$1M) - lines [992, 1004]
- [ ] `general-security-arbitrary-external-call-vulnerabilities-medium-severity-exploits-100k-010` (6/21) Medium-Severity Exploits (<$100K) - lines [1005, 1020]

Progress: 0/5 cards source-enriched for this file.

### `DB/general/arbitrary-call/defihacklabs-arbitrary-call-2024-2025.md`

- [ ] `general-security-defihacklabs-arbitrary-call-2024-2025-1-unvalidated-callto-calldata--001` (9/21) 1. Unvalidated callTo/callData in Swap/Route Structs - lines [119, 193]
- [ ] `general-security-defihacklabs-arbitrary-call-2024-2025-2-unrestricted-external-call-a-002` (8/21) 2. Unrestricted External Call Actions (OPERATION_CALL) - lines [194, 266]
- [ ] `general-security-defihacklabs-arbitrary-call-2024-2025-3-bridge-signer-validation-byp-003` (8/21) 3. Bridge Signer Validation Bypass - lines [267, 309]
- [ ] `general-security-defihacklabs-arbitrary-call-2024-2025-4-yul-integer-overflow-calldat-004` (8/21) 4. Yul Integer Overflow Calldata Corruption - lines [310, 365]
- [ ] `general-security-defihacklabs-arbitrary-call-2024-2025-5-unverified-aggregator-proxy--005` (8/21) 5. Unverified Aggregator Proxy Forwarding - lines [366, 400]

Progress: 0/5 cards source-enriched for this file.

### `DB/general/arbitrary-call/defihacklabs-arbitrary-call-patterns.md`

- [ ] `general-security-defihacklabs-arbitrary-call-patterns-1-unvalidated-router-address-c-001` (9/21) 1. Unvalidated Router Address + Calldata in Swap Functions - lines [108, 276]
- [ ] `general-security-defihacklabs-arbitrary-call-patterns-2-additional-arbitrary-call-pa-002` (6/21) 2. Additional Arbitrary Call Patterns (2022) - lines [277, 404]

Progress: 0/2 cards source-enriched for this file.

### `DB/general/arbitrary-call/dex-aggregator-unvalidated-call-data.md`

- [ ] `general-security-dex-aggregator-unvalidated-call-data-root-cause-analysis-001` (8/21) Root Cause Analysis - lines [150, 177]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/bonding-curve/BONDING_CURVE_ACCESS_CONTROL_STATE_VULNERABILITIES.md`

- [x] `general-defi-bonding-curve-access-control-state-vulne-1-freeze-authority-not-revoked-000` (13/21) 1. Freeze Authority Not Revoked After Pool Creation - lines [137, 234]
- [x] `general-defi-bonding-curve-access-control-state-vulne-10-registry-admin-can-override-009` (10/21) 10. Registry Admin Can Override Upgrade Contract - lines [595, 631]
- [x] `general-defi-bonding-curve-access-control-state-vulne-11-converter-isactive-before-f-010` (8/21) 11. Converter isActive Before Full Configuration - lines [632, 664]
- [x] `general-defi-bonding-curve-access-control-state-vulne-13-frontrunning-reduceweight-v-012` (8/21) 13. Frontrunning reduceWeight via Marketcap Manipulation - lines [682, 714]
- [x] `general-defi-bonding-curve-access-control-state-vulne-14-force-sent-native-token-dos-013` (9/21) 14. Force-Sent Native Token DOS Graduation - lines [715, 762]
- [x] `general-defi-bonding-curve-access-control-state-vulne-2-unvalidated-edition-in-sam-c-001` (11/21) 2. Unvalidated Edition in SAM create() Drains All Funds - lines [235, 299]
- [x] `general-defi-bonding-curve-access-control-state-vulne-3-reentrancy-during-cred-creat-002` (9/21) 3. Reentrancy During Cred Creation Steals All Ether - lines [300, 367]
- [x] `general-defi-bonding-curve-access-control-state-vulne-4-denom-change-while-active-bi-003` (10/21) 4. Denom Change While Active Bids Exist - lines [368, 412]
- [ ] `general-defi-bonding-curve-access-control-state-vulne-5-missing-access-control-on-or-004` (8/21) 5. Missing Access Control on Oracle/Manager Address Setters - lines [413, 443]
- [ ] `general-defi-bonding-curve-access-control-state-vulne-6-unprotected-orderbook-functi-005` (7/21) 6. Unprotected Orderbook Functions Enable Manipulation - lines [444, 478]
- [x] `general-defi-bonding-curve-access-control-state-vulne-7-golden-egg-state-drift-via-n-006` (9/21) 7. Golden Egg State Drift via Non-Frozen editionMaxMintable - lines [479, 524]
- [x] `general-defi-bonding-curve-access-control-state-vulne-8-inconsistent-bond-curve-upda-007` (10/21) 8. Inconsistent Bond Curve Update Breaks Deposit Accounting - lines [525, 557]
- [x] `general-defi-bonding-curve-access-control-state-vulne-9-race-condition-between-buyer-008` (8/21) 9. Race Condition Between Buyer and Owner Withdrawal - lines [558, 594]

Progress: 11/13 cards source-enriched for this file.

### `DB/general/bonding-curve/BONDING_CURVE_DOS_GRIEFING_VULNERABILITIES.md`

- [ ] `general-defi-bonding-curve-dos-griefing-vulnerabiliti-vulnerability-title-000` (15/21) Vulnerability Title - lines [96, 561]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/bonding-curve/BONDING_CURVE_FEE_ROUNDING_VULNERABILITIES.md`

- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-1-fee-calculated-on-wrong-base-000` (13/21) 1. Fee Calculated on Wrong Base Amount - lines [129, 217]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-10-fee-reward-dust-permanently-009` (9/21) 10. Fee Reward Dust Permanently Stuck in Contract - lines [536, 579]
- [ ] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-11-fee-on-transfer-token-accou-010` (7/21) 11. Fee-on-Transfer Token Accounting Mismatch - lines [580, 610]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-2-last-buy-fee-mismatch-on-bon-001` (9/21) 2. Last Buy Fee Mismatch on Bonding Curve - lines [218, 250]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-3-swap-fee-omitted-in-order-re-002` (8/21) 3. Swap Fee Omitted in Order Reflections - lines [251, 280]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-4-inconsistent-fee-between-quo-003` (9/21) 4. Inconsistent Fee Between Quoter and Execution - lines [281, 326]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-5-expansion-mint-precision-los-004` (8/21) 5. Expansion Mint Precision Loss Causes DOS - lines [327, 358]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-6-root-exponent-library-trunca-005` (9/21) 6. Root/Exponent Library Truncation Compounds Error - lines [359, 404]
- [ ] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-7-invariant-rounding-direction-006` (7/21) 7. Invariant Rounding Direction Mismatch - lines [405, 437]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-8-underpriced-quote-via-intege-007` (9/21) 8. Underpriced Quote via Integer Division Truncation - lines [438, 495]
- [x] `general-defi-bonding-curve-fee-rounding-vulnerabiliti-9-invariant-check-invalidated--008` (8/21) 9. Invariant Check Invalidated by Rent Inclusion - lines [496, 535]

Progress: 9/11 cards source-enriched for this file.

### `DB/general/bonding-curve/BONDING_CURVE_MATH_FORMULA_VULNERABILITIES.md`

- [ ] `general-defi-bonding-curve-math-formula-vulnerabiliti-vulnerability-title-000` (14/21) Vulnerability Title - lines [102, 712]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/bonding-curve/BONDING_CURVE_MISC_VULNERABILITIES.md`

- [x] `general-defi-bonding-curve-misc-vulnerabilities-1-oracle-price-denomination-mi-000` (13/21) 1. Oracle Price Denomination Mismatch (USD vs DAI) - lines [135, 222]
- [ ] `general-defi-bonding-curve-misc-vulnerabilities-10-protocol-fees-stuck-after-g-009` (8/21) 10. Protocol Fees Stuck After Graduation - lines [575, 604]
- [ ] `general-defi-bonding-curve-misc-vulnerabilities-11-token-supply-not-correctly--010` (8/21) 11. Token Supply Not Correctly Burned on Graduation - lines [605, 638]
- [ ] `general-defi-bonding-curve-misc-vulnerabilities-12-graduation-stuck-due-to-thi-011` (7/21) 12. Graduation Stuck Due to Third-Party Contract Interference - lines [639, 680]
- [x] `general-defi-bonding-curve-misc-vulnerabilities-2-stale-twap-oracle-due-to-unp-001` (9/21) 2. Stale TWAP Oracle Due to Unpoked Metapool - lines [223, 267]
- [x] `general-defi-bonding-curve-misc-vulnerabilities-3-flash-loan-protection-bypass-002` (9/21) 3. Flash Loan Protection Bypass via Self-Liquidation - lines [268, 327]
- [x] `general-defi-bonding-curve-misc-vulnerabilities-4-rebalance-rate-limiting-miss-003` (10/21) 4. Rebalance Rate Limiting Missing - Vault Drainage - lines [328, 382]
- [x] `general-defi-bonding-curve-misc-vulnerabilities-5-wash-trading-to-steal-keeper-004` (10/21) 5. Wash Trading to Steal Keeper/Spot Trading Rewards - lines [383, 436]
- [x] `general-defi-bonding-curve-misc-vulnerabilities-6-batch-operation-fails-atomic-005` (9/21) 6. Batch Operation Fails Atomically on Single Asset - lines [437, 480]
- [ ] `general-defi-bonding-curve-misc-vulnerabilities-7-unsafe-downcast-breaks-suppl-006` (7/21) 7. Unsafe Downcast Breaks Supply Invariant - lines [481, 517]
- [ ] `general-defi-bonding-curve-misc-vulnerabilities-8-collateral-depeg-cascading-t-007` (6/21) 8. Collateral Depeg Cascading to Bonding Curve - lines [518, 543]
- [ ] `general-defi-bonding-curve-misc-vulnerabilities-9-asymmetric-base-quote-treatm-008` (6/21) 9. Asymmetric Base/Quote Treatment in Virtual Bonding Curve - lines [544, 574]

Progress: 6/12 cards source-enriched for this file.

### `DB/general/bonding-curve/BONDING_CURVE_SLIPPAGE_PROTECTION_VULNERABILITIES.md`

- [x] `general-defi-bonding-curve-slippage-protection-vulner-vulnerability-title-000` (14/21) Vulnerability Title - lines [93, 752]

Progress: 1/1 cards source-enriched for this file.

### `DB/general/bonding-curve/BONDING_CURVE_TOKEN_LAUNCH_GRADUATION_VULNERABILITIES.md`

- [x] `general-defi-bonding-curve-token-launch-graduation-vu-1-premature-launch-via-default-000` (13/21) 1. Premature Launch via Default Value Bypass - lines [136, 224]
- [x] `general-defi-bonding-curve-token-launch-graduation-vu-11-presale-tokens-grant-premat-010` (12/21) 11. Presale Tokens Grant Premature Voting Power - lines [656, 686]
- [ ] `general-defi-bonding-curve-token-launch-graduation-vu-12-dutch-auction-price-manipul-011` (7/21) 12. Dutch Auction Price Manipulation - lines [687, 715]
- [ ] `general-defi-bonding-curve-token-launch-graduation-vu-13-crowdfund-rug-pull-via-zero-012` (7/21) 13. Crowdfund Rug Pull via Zero MaxPrice NFT Listing - lines [716, 741]
- [x] `general-defi-bonding-curve-token-launch-graduation-vu-2-flash-loan-genesis-graduatio-001` (12/21) 2. Flash Loan Genesis / Graduation Exploit - lines [225, 305]
- [x] `general-defi-bonding-curve-token-launch-graduation-vu-3-flash-loan-premature-graduat-002` (11/21) 3. Flash Loan Premature Graduation with Atomic Unwrap - lines [306, 357]
- [ ] `general-defi-bonding-curve-token-launch-graduation-vu-4-new-bonding-curve-launch-vol-003` (8/21) 4. New Bonding Curve Launch Volatility Arbitrage - lines [358, 404]
- [x] `general-defi-bonding-curve-token-launch-graduation-vu-7-early-pair-creation-breaks-f-006` (13/21) 7. Early Pair Creation Breaks Fair Launch - lines [512, 568]
- [ ] `general-defi-bonding-curve-token-launch-graduation-vu-8-donation-guard-bypass-via-wr-007` (7/21) 8. Donation Guard Bypass via Wrong Pair Address - lines [569, 595]

Progress: 5/9 cards source-enriched for this file.

### `DB/general/bonding-curve/SANDWICH_ATTACK_MEV_BONDING_CURVE_VULNERABILITIES.md`

- [x] `general-defi-sandwich-attack-mev-bonding-curve-vulner-vulnerability-title-000` (17/21) Vulnerability Title - lines [95, 983]

Progress: 1/1 cards source-enriched for this file.

### `DB/general/bridge/cross-chain-bridge-vulnerabilities.md`

- [ ] `general-infrastructure-cross-chain-bridge-vulnerabilities-1-merkle-proof-validation-fail-000` (15/21) 1. Merkle Proof Validation Failures - lines [152, 415]
- [ ] `general-infrastructure-cross-chain-bridge-vulnerabilities-2-signature-verification-issue-001` (10/21) 2. Signature Verification Issues - lines [416, 606]
- [ ] `general-infrastructure-cross-chain-bridge-vulnerabilities-3-message-validation-bypasses-002` (8/21) 3. Message Validation Bypasses - lines [607, 783]
- [ ] `general-infrastructure-cross-chain-bridge-vulnerabilities-4-centralization-key-managemen-003` (10/21) 4. Centralization / Key Management Risks - lines [784, 993]
- [ ] `general-infrastructure-cross-chain-bridge-vulnerabilities-5-token-validation-in-bridge-d-004` (8/21) 5. Token Validation in Bridge Deposits - lines [994, 1169]
- [ ] `general-infrastructure-cross-chain-bridge-vulnerabilities-6-replay-attacks-across-chains-005` (10/21) 6. Replay Attacks Across Chains - lines [1170, 1285]
- [ ] `general-infrastructure-cross-chain-bridge-vulnerabilities-7-arbitrary-call-vulnerabiliti-006` (10/21) 7. Arbitrary Call Vulnerabilities - lines [1286, 1512]

Progress: 0/7 cards source-enriched for this file.

### `DB/general/business-logic/defi-business-logic-flaws.md`

- [ ] `general-defi-defi-business-logic-flaws-defi-business-logic-flaw-vulne-000` (11/21) DeFi Business Logic Flaw Vulnerabilities - lines [78, 138]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/business-logic/defihacklabs-business-logic-2023-patterns.md`

- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-1-donate-to-reserves-self-liqu-001` (9/21) 1. Donate-to-Reserves Self-Liquidation (Euler $200M) - lines [138, 215]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-2-tick-boundary-precision-erro-002` (9/21) 2. Tick Boundary Precision Error (KyberSwap $48M) - lines [216, 297]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-3-unprotected-burnfrom-transfe-003` (8/21) 3. Unprotected burnFrom + transferFrom (DEI $5.4M) - lines [298, 342]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-4-duplicate-array-elements-in--004` (9/21) 4. Duplicate Array Elements in Reward Claiming (Level $1M) - lines [343, 404]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-5-emergency-withdraw-without-n-005` (8/21) 5. Emergency Withdraw Without NFT Unstake (BNO $505K) - lines [405, 462]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-6-flash-loan-liquidity-manipul-006` (8/21) 6. Flash Loan Liquidity Manipulation (Palmswap $900K) - lines [463, 514]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-7-convertdusttoearned-price-ma-007` (8/21) 7. convertDustToEarned Price Manipulation (BEARNDAO $769K) - lines [515, 559]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-8-flash-loan-bad-debt-creation-008` (8/21) 8. Flash Loan Bad Debt Creation (Platypus $10.5M Total, 3 Exploits) - lines [560, 594]
- [ ] `general-defi-defihacklabs-business-logic-2023-pattern-secure-implementations-009` (8/21) Secure Implementations - lines [595, 650]

Progress: 0/9 cards source-enriched for this file.

### `DB/general/business-logic/defihacklabs-business-logic-2024-2025.md`

- [ ] `general-defi-defihacklabs-business-logic-2024-2025-1-dangling-approval-after-oper-001` (9/21) 1. Dangling Approval After Operation Cancellation - lines [109, 167]
- [ ] `general-defi-defihacklabs-business-logic-2024-2025-2-repeated-withdrawal-without--002` (9/21) 2. Repeated Withdrawal Without State Invalidation - lines [168, 219]
- [ ] `general-defi-defihacklabs-business-logic-2024-2025-3-uninitialized-uups-proxy-tak-003` (9/21) 3. Uninitialized UUPS Proxy Takeover - lines [220, 275]

Progress: 0/3 cards source-enriched for this file.

### `DB/general/business-logic/defihacklabs-share-accounting-patterns.md`

- [ ] `general-defi-defihacklabs-share-accounting-patterns-root-cause-categories-000` (8/21) Root Cause Categories - lines [104, 114]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/business-logic/defihacklabs-solvency-business-logic-patterns.md`

- [ ] `general-defi-defihacklabs-solvency-business-logic-pat-1-missing-solvency-check-on-do-001` (9/21) 1. Missing Solvency Check on Donation Functions - lines [105, 171]
- [ ] `general-defi-defihacklabs-solvency-business-logic-pat-2-precision-loss-in-concentrat-002` (8/21) 2. Precision Loss in Concentrated Liquidity Tick Math - lines [172, 236]
- [ ] `general-defi-defihacklabs-solvency-business-logic-pat-3-internal-vs-actual-balance-d-003` (8/21) 3. Internal vs Actual Balance Divergence - lines [237, 289]
- [ ] `general-defi-defihacklabs-solvency-business-logic-pat-4-unchecked-swap-router-callba-004` (8/21) 4. Unchecked Swap Router Callback Trust - lines [290, 341]

Progress: 0/4 cards source-enriched for this file.

### `DB/general/calculation/defihacklabs-reward-calculation-2022-patterns.md`

- [ ] `general-defi-defihacklabs-reward-calculation-2022-pat-invariant-checks-004` (8/21) Invariant Checks - lines [514, 526]
- [ ] `general-defi-defihacklabs-reward-calculation-2022-pat-static-analysis-003` (6/21) Static Analysis - lines [492, 513]

Progress: 0/2 cards source-enriched for this file.

### `DB/general/dao-governance-vulnerabilities/defihacklabs-governance-attack-patterns.md`

- [ ] `general-governance-defihacklabs-governance-attack-patterns-1-flash-loan-governance-takeov-001` (9/21) 1. Flash Loan Governance Takeover - lines [108, 162]
- [ ] `general-governance-defihacklabs-governance-attack-patterns-2-low-quorum-governance-exploi-002` (8/21) 2. Low Quorum Governance Exploitation - lines [163, 212]
- [ ] `general-governance-defihacklabs-governance-attack-patterns-3-proxy-re-initialization-atta-003` (8/21) 3. Proxy Re-Initialization Attack - lines [213, 266]
- [ ] `general-governance-defihacklabs-governance-attack-patterns-4-dao-module-oracle-self-answe-004` (8/21) 4. DAO Module Oracle Self-Answer Attack - lines [267, 321]
- [ ] `general-governance-defihacklabs-governance-attack-patterns-5-governance-treasury-drain-vi-005` (8/21) 5. Governance Treasury Drain via Token Acquisition - lines [322, 372]

Progress: 0/5 cards source-enriched for this file.

### `DB/general/dao-governance-vulnerabilities/governance-takeover.md`

- [x] `general-governance-governance-takeover-1-51-attack-via-arbitrary-exec-000` (15/21) 1. 51% Attack via Arbitrary Execution - lines [114, 292]
- [x] `general-governance-governance-takeover-2-loss-of-veto-power-enabling--001` (10/21) 2. Loss of Veto Power Enabling Takeover - lines [293, 391]
- [x] `general-governance-governance-takeover-3-centralized-governance-contr-002` (14/21) 3. Centralized Governance Control - lines [392, 521]
- [x] `general-governance-governance-takeover-4-emergency-function-abuse-003` (10/21) 4. Emergency Function Abuse - lines [522, 620]
- [x] `general-governance-governance-takeover-5-unrestricted-deployment-elec-004` (11/21) 5. Unrestricted Deployment/Election Takeover - lines [621, 703]

Progress: 5/5 cards source-enriched for this file.

### `DB/general/dao-governance-vulnerabilities/proposal-lifecycle-manipulation.md`

- [x] `general-governance-proposal-lifecycle-manipulation-1-unrestricted-proposal-cancel-000` (15/21) 1. Unrestricted Proposal Cancellation - lines [116, 268]
- [x] `general-governance-proposal-lifecycle-manipulation-2-proposal-threshold-bypass-fo-001` (11/21) 2. Proposal Threshold Bypass for Griefing - lines [269, 373]
- [x] `general-governance-proposal-lifecycle-manipulation-3-proposal-expiration-logic-er-002` (10/21) 3. Proposal Expiration Logic Errors - lines [374, 472]
- [ ] `general-governance-proposal-lifecycle-manipulation-4-state-machine-transition-vul-003` (12/21) 4. State Machine Transition Vulnerabilities - lines [473, 541]
- [ ] `general-governance-proposal-lifecycle-manipulation-5-proposal-execution-vulnerabi-004` (10/21) 5. Proposal Execution Vulnerabilities - lines [542, 617]

Progress: 3/5 cards source-enriched for this file.

### `DB/general/dao-governance-vulnerabilities/quorum-manipulation.md`

- [x] `general-governance-quorum-manipulation-1-quorum-lowering-via-delegati-000` (15/21) 1. Quorum Lowering via Delegation Abuse - lines [111, 269]
- [ ] `general-governance-quorum-manipulation-2-dynamic-quorum-manipulation-001` (10/21) 2. Dynamic Quorum Manipulation - lines [270, 332]
- [x] `general-governance-quorum-manipulation-3-quorum-threshold-miscalculat-002` (12/21) 3. Quorum Threshold Miscalculation - lines [333, 427]
- [x] `general-governance-quorum-manipulation-4-quorum-not-enforced-in-state-003` (11/21) 4. Quorum Not Enforced in State Transitions - lines [428, 510]
- [x] `general-governance-quorum-manipulation-5-tie-handling-vulnerabilities-004` (12/21) 5. Tie Handling Vulnerabilities - lines [511, 598]

Progress: 4/5 cards source-enriched for this file.

### `DB/general/dao-governance-vulnerabilities/timelock-bypass.md`

- [x] `general-governance-timelock-bypass-1-timelock-bypass-via-privileg-000` (15/21) 1. Timelock Bypass via Privileged Functions - lines [116, 281]
- [x] `general-governance-timelock-bypass-2-zero-minimal-delay-vulnerabi-001` (11/21) 2. Zero/Minimal Delay Vulnerabilities - lines [282, 347]
- [x] `general-governance-timelock-bypass-3-timelock-reduction-during-ac-002` (11/21) 3. Timelock Reduction During Active Lock - lines [348, 410]
- [x] `general-governance-timelock-bypass-4-canceled-proposal-still-exec-003` (11/21) 4. Canceled Proposal Still Executable - lines [411, 501]
- [x] `general-governance-timelock-bypass-5-storage-collision-attacks-004` (11/21) 5. Storage Collision Attacks - lines [502, 580]

Progress: 5/5 cards source-enriched for this file.

### `DB/general/dao-governance-vulnerabilities/voting-power-manipulation.md`

- [x] `general-governance-voting-power-manipulation-1-double-voting-via-delegation-000` (15/21) 1. Double Voting via Delegation Abuse - lines [118, 325]
- [x] `general-governance-voting-power-manipulation-2-flash-loan-voting-attacks-001` (12/21) 2. Flash Loan Voting Attacks - lines [326, 422]
- [x] `general-governance-voting-power-manipulation-3-unlimited-vote-minting-002` (13/21) 3. Unlimited Vote Minting - lines [423, 510]
- [x] `general-governance-voting-power-manipulation-4-missing-voting-power-snapsho-003` (11/21) 4. Missing Voting Power Snapshots - lines [511, 591]
- [ ] `general-governance-voting-power-manipulation-5-delegation-logic-errors-004` (6/21) 5. Delegation Logic Errors - lines [592, 618]

Progress: 4/5 cards source-enriched for this file.

### `DB/general/dao-governance/DAO_GOVERNANCE_VULNERABILITIES.md`

- [ ] `general-governance-dao-governance-vulnerabilities-contract-call-graph-signals-011` (8/21) Contract / Call Graph Signals - lines [713, 725]
- [ ] `general-governance-dao-governance-vulnerabilities-high-signal-grep-seeds-012` (6/21) High-Signal Grep Seeds - lines [726, 755]
- [ ] `general-governance-dao-governance-vulnerabilities-section-1-flash-loan-snapshot--001` (11/21) Section 1: Flash Loan & Snapshot-Less Voting Power Manipulation - lines [225, 287]
- [ ] `general-governance-dao-governance-vulnerabilities-section-2-quorum-manipulation--002` (11/21) Section 2: Quorum Manipulation & Threshold Bypass - lines [288, 351]
- [ ] `general-governance-dao-governance-vulnerabilities-section-3-timelock-bypass-unau-003` (11/21) Section 3: Timelock Bypass & Unauthorized Execution - lines [352, 418]
- [ ] `general-governance-dao-governance-vulnerabilities-section-4-delegation-checkpoin-004` (11/21) Section 4: Delegation & Checkpoint Accounting Bugs - lines [419, 481]
- [ ] `general-governance-dao-governance-vulnerabilities-section-5-proposal-cancellatio-005` (10/21) Section 5: Proposal Cancellation & Execution Abuse - lines [482, 535]
- [ ] `general-governance-dao-governance-vulnerabilities-section-6-quadratic-voting-tal-006` (10/21) Section 6: Quadratic Voting & Tally Errors - lines [536, 576]
- [ ] `general-governance-dao-governance-vulnerabilities-section-7-multisig-safe-module-007` (10/21) Section 7: Multisig & Safe Module Exploits - lines [577, 618]
- [ ] `general-governance-dao-governance-vulnerabilities-section-8-governance-takeover--008` (10/21) Section 8: Governance Takeover via Deployment/Factory Bugs - lines [619, 650]
- [ ] `general-governance-dao-governance-vulnerabilities-vulnerability-title-000` (11/21) Vulnerability Title - lines [143, 224]

Progress: 0/11 cards source-enriched for this file.

### `DB/general/diamond-proxy/DIAMOND_PROXY_VULNERABILITIES.md`

- [x] `general-infrastructure-diamond-proxy-vulnerabilities-vulnerability-title-000` (17/21) Vulnerability Title - lines [90, 599]

Progress: 1/1 cards source-enriched for this file.

### `DB/general/erc7702-integration/erc7702-integration-vulnerabilities.md`

- [x] `general-infrastructure-erc7702-integration-vulnerabilities-1-iscontract-extcodesize-logic-001` (14/21) 1. isContract/extcodesize Logic Broken - lines [211, 404]
- [x] `general-infrastructure-erc7702-integration-vulnerabilities-2-reentrancy-via-eip-7702-dele-002` (13/21) 2. Reentrancy via EIP-7702 Delegated EOAs - lines [405, 553]
- [x] `general-infrastructure-erc7702-integration-vulnerabilities-3-missing-token-receiver-callb-003` (13/21) 3. Missing Token Receiver Callbacks - lines [554, 724]
- [x] `general-infrastructure-erc7702-integration-vulnerabilities-4-cross-chain-address-mismatch-004` (13/21) 4. Cross-Chain Address Mismatch - lines [725, 875]
- [x] `general-infrastructure-erc7702-integration-vulnerabilities-5-tx-origin-exploitation-with--005` (13/21) 5. tx.origin Exploitation with Smart Wallets - lines [876, 1021]
- [x] `general-infrastructure-erc7702-integration-vulnerabilities-6-fallback-receive-function-is-006` (13/21) 6. Fallback/Receive Function Issues - lines [1022, 1145]
- [x] `general-infrastructure-erc7702-integration-vulnerabilities-7-session-key-impersonation-in-007` (13/21) 7. Session Key Impersonation in Smart Wallets - lines [1146, 1289]
- [x] `general-infrastructure-erc7702-integration-vulnerabilities-8-nft-permit-function-exploita-008` (13/21) 8. NFT Permit Function Exploitation - lines [1290, 1494]
- [ ] `general-infrastructure-erc7702-integration-vulnerabilities-understanding-eip-7702-000` (11/21) Understanding EIP-7702 - lines [162, 210]

Progress: 8/9 cards source-enriched for this file.

### `DB/general/flash-loan/FLASH_LOAN_VULNERABILITIES.md`

- [x] `general-defi-flash-loan-vulnerabilities-vulnerability-title-000` (16/21) Vulnerability Title - lines [88, 408]

Progress: 1/1 cards source-enriched for this file.

### `DB/general/integer-overflow/defihacklabs-overflow-patterns.md`

- [ ] `general-defi-defihacklabs-overflow-patterns-general-overflow-pattern-001` (6/21) General Overflow Pattern - lines [236, 259]
- [ ] `general-defi-defihacklabs-overflow-patterns-keywords-002` (6/21) Keywords - lines [373, 389]
- [ ] `general-defi-defihacklabs-overflow-patterns-root-cause-000` (6/21) Root Cause - lines [115, 124]

Progress: 0/3 cards source-enriched for this file.

### `DB/general/integer-overflow/integer-overflow-vulnerabilities.md`

- [ ] `general-defi-integer-overflow-vulnerabilities-manual-checklist-004` (6/21) Manual Checklist - lines [469, 478]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/lending-rate-model/LENDING_RATE_MODEL_VULNERABILITIES.md`

- [ ] `general-defi-lending-rate-model-vulnerabilities-high-signal-grep-seeds-009` (6/21) High-Signal Grep Seeds - lines [518, 535]
- [ ] `general-defi-lending-rate-model-vulnerabilities-section-1-utilization-formula--001` (11/21) Section 1: Utilization Formula Errors - lines [173, 230]
- [ ] `general-defi-lending-rate-model-vulnerabilities-section-2-chain-specific-const-002` (10/21) Section 2: Chain-Specific Constant Errors - lines [231, 271]
- [ ] `general-defi-lending-rate-model-vulnerabilities-section-3-utilization-manipula-003` (11/21) Section 3: Utilization Manipulation & Rate Gaming - lines [272, 349]
- [ ] `general-defi-lending-rate-model-vulnerabilities-section-4-debt-token-scaling-r-004` (10/21) Section 4: Debt Token Scaling & Rate Accounting Errors - lines [350, 399]
- [ ] `general-defi-lending-rate-model-vulnerabilities-section-5-rate-model-dos-syste-005` (10/21) Section 5: Rate Model DoS & System Halt - lines [400, 442]
- [ ] `general-defi-lending-rate-model-vulnerabilities-vulnerability-title-000` (11/21) Vulnerability Title - lines [111, 172]

Progress: 0/7 cards source-enriched for this file.

### `DB/general/malicious/rug-pull-detection-patterns.md`

- [ ] `general-governance-rug-pull-detection-patterns-rug-pull-malicious-contract-de-000` (12/21) Rug Pull & Malicious Contract Detection Patterns - lines [76, 138]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/missing-validations/MISSING_VALIDATION_TEMPLATE.md`

- [ ] `general-security-missing-validation-template-2-numeric-bounds-validation-pa-002` (10/21) 2. NUMERIC BOUNDS VALIDATION PATTERNS - lines [218, 351]
- [ ] `general-security-missing-validation-template-5-signature-nonce-validation-p-005` (9/21) 5. SIGNATURE & NONCE VALIDATION PATTERNS - lines [582, 636]
- [ ] `general-security-missing-validation-template-6-oracle-external-data-validat-006` (10/21) 6. ORACLE & EXTERNAL DATA VALIDATION PATTERNS - lines [637, 684]

Progress: 0/3 cards source-enriched for this file.

### `DB/general/nft-marketplace/NFT_MARKETPLACE_VULNERABILITIES.md`

- [x] `general-defi-nft-marketplace-vulnerabilities-1-reentrancy-via-onerc721recei-001` (10/21) 1. Reentrancy via onERC721Received / safeMint Callbacks - lines [174, 240]
- [x] `general-defi-nft-marketplace-vulnerabilities-10-nft-wrap-unwrap-airdrop-id--010` (11/21) 10. NFT Wrap/Unwrap Airdrop & ID Swap Exploitation - lines [720, 784]
- [x] `general-defi-nft-marketplace-vulnerabilities-2-residual-allowance-vault-dep-002` (9/21) 2. Residual Allowance & Vault Deposit Exploitation - lines [241, 293]
- [x] `general-defi-nft-marketplace-vulnerabilities-3-marketplace-fee-bypass-royal-003` (11/21) 3. Marketplace Fee Bypass & Royalty Calculation Errors - lines [294, 361]
- [x] `general-defi-nft-marketplace-vulnerabilities-4-nft-rental-griefing-via-call-004` (10/21) 4. NFT Rental Griefing via Callback Revert & Blocklist - lines [362, 437]
- [x] `general-defi-nft-marketplace-vulnerabilities-5-gnosis-safe-guard-bypass-via-005` (9/21) 5. Gnosis Safe Guard Bypass via Fallback Handler - lines [438, 493]
- [x] `general-defi-nft-marketplace-vulnerabilities-6-auction-manipulation-frontru-006` (10/21) 6. Auction Manipulation, Frontrunning & Debt Shortfall - lines [494, 563]
- [x] `general-defi-nft-marketplace-vulnerabilities-7-nft-bridge-one-way-lock-migr-007` (9/21) 7. NFT Bridge One-Way Lock & Migration Burn - lines [564, 623]
- [x] `general-defi-nft-marketplace-vulnerabilities-8-merkle-criteria-resolution-o-008` (12/21) 8. Merkle Criteria Resolution & Order Matching Bypass - lines [624, 669]
- [x] `general-defi-nft-marketplace-vulnerabilities-9-flash-loan-pool-token-theft-009` (10/21) 9. Flash Loan & Pool Token Theft - lines [670, 719]
- [ ] `general-defi-nft-marketplace-vulnerabilities-vulnerability-title-000` (11/21) Vulnerability Title - lines [129, 173]

Progress: 10/11 cards source-enriched for this file.

### `DB/general/perpetuals-derivatives/PERPETUALS_DERIVATIVES_VULNERABILITIES.md`

- [x] `general-defi-perpetuals-derivatives-vulnerabilities-1-liquidation-mechanism-failur-000` (16/21) 1. Liquidation Mechanism Failures - lines [250, 425]
- [x] `general-defi-perpetuals-derivatives-vulnerabilities-2-funding-rate-vulnerabilities-001` (11/21) 2. Funding Rate Vulnerabilities - lines [426, 533]
- [x] `general-defi-perpetuals-derivatives-vulnerabilities-3-position-leverage-accounting-002` (13/21) 3. Position & Leverage Accounting Bugs - lines [534, 635]
- [x] `general-defi-perpetuals-derivatives-vulnerabilities-4-order-execution-vulnerabilit-003` (13/21) 4. Order Execution Vulnerabilities - lines [636, 722]
- [ ] `general-defi-perpetuals-derivatives-vulnerabilities-5-fee-reward-system-exploits-004` (9/21) 5. Fee & Reward System Exploits - lines [723, 733]
- [x] `general-defi-perpetuals-derivatives-vulnerabilities-6-lp-vault-exploitation-005` (11/21) 6. LP Vault Exploitation - lines [798, 884]
- [x] `general-defi-perpetuals-derivatives-vulnerabilities-7-bad-debt-protocol-insolvency-006` (11/21) 7. Bad Debt & Protocol Insolvency - lines [885, 965]

Progress: 6/7 cards source-enriched for this file.

### `DB/general/precision/defihacklabs-precision-share-manipulation-2024-2025.md`

- [ ] `general-defi-defihacklabs-precision-share-manipulatio-1-empty-market-exchange-rate-i-001` (9/21) 1. Empty Market Exchange Rate Inflation via Donation - lines [128, 209]
- [ ] `general-defi-defihacklabs-precision-share-manipulatio-2-elastic-base-rebase-math-rou-002` (9/21) 2. Elastic/Base Rebase Math Rounding Exploitation - lines [210, 264]
- [ ] `general-defi-defihacklabs-precision-share-manipulatio-3-liquidityindex-inflation-via-003` (9/21) 3. LiquidityIndex Inflation via Recursive Flash Loans - lines [265, 323]
- [ ] `general-defi-defihacklabs-precision-share-manipulatio-4-scaling-factor-precision-los-004` (9/21) 4. Scaling Factor Precision Loss in StableMath - lines [324, 381]
- [ ] `general-defi-defihacklabs-precision-share-manipulatio-5-share-price-inflation-via-di-005` (8/21) 5. Share Price Inflation via Direct Contract Donation - lines [382, 466]
- [ ] `general-defi-defihacklabs-precision-share-manipulatio-6-virtual-balance-math-manipul-006` (6/21) 6. Virtual Balance Math Manipulation - lines [467, 510]

Progress: 0/6 cards source-enriched for this file.

### `DB/general/proxy-vulnerabilities/PROXY_PATTERN_VULNERABILITIES.md`

- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-1-missing-disableiniti-001` (7/21) Pattern 1: Missing disableInitializers in Implementation Constructor - lines [150, 190]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-10-clone-validation-ch-010` (7/21) Pattern 10: Clone Validation Checking Insufficient Bytes - lines [570, 631]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-11-metamorphic-impleme-011` (7/21) Pattern 11: Metamorphic Implementation Contract Risk - lines [632, 689]
- [x] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-12-plugin-selector-col-012` (10/21) Pattern 12: Plugin Selector Collision Override - lines [690, 741]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-13-persisted-msg-value-013` (7/21) Pattern 13: Persisted msg.value in Batch Delegatecalls - lines [742, 798]
- [x] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-14-module-upgrade-with-014` (8/21) Pattern 14: Module Upgrade Without State Migration - lines [799, 863]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-15-storage-layout-chan-015` (7/21) Pattern 15: Storage Layout Change on Upgrade Breaks Roles - lines [864, 915]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-16-missing-contract-ex-016` (7/21) Pattern 16: Missing Contract Existence Check Before Delegatecall - lines [916, 955]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-17-proxy-shadowing-imp-017` (7/21) Pattern 17: Proxy Shadowing Implementation Functions - lines [956, 1012]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-18-permissions-allowan-018` (8/21) Pattern 18: Permissions/Allowances Not Reset on Proxy Ownership Transfer - lines [1013, 1061]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-19-temporary-owner-cha-019` (7/21) Pattern 19: Temporary Owner Change During Delegatecall - lines [1062, 1118]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-2-implementation-destr-002` (8/21) Pattern 2: Implementation Destruction via Selfdestruct - lines [191, 235]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-20-proxy-reuse-without-020` (9/21) Pattern 20: Proxy Reuse Without Implementation Version Check - lines [1119, 1185]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-21-create2-salt-predic-021` (8/21) Pattern 21: CREATE2 Salt Predictability/Front-Running - lines [1186, 1235]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-22-counterfactual-wall-022` (7/21) Pattern 22: Counterfactual Wallet Deployment Hijacking - lines [1236, 1296]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-23-variable-initializa-023` (7/21) Pattern 23: Variable Initialization at Declaration in Upgradeable Contract - lines [1297, 1340]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-24-beacon-implementati-024` (7/21) Pattern 24: Beacon Implementation Without Contract Existence Check - lines [1341, 1386]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-25-approval-set-in-con-025` (7/21) Pattern 25: Approval Set in Constructor for Proxy Contract - lines [1387, 1444]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-26-proxy-cannot-redepl-026` (7/21) Pattern 26: Proxy Cannot Redeploy After Selfdestruct - lines [1445, 1500]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-27-whitelist-bypass-vi-027` (7/21) Pattern 27: Whitelist Bypass via Upgradeable Proxy - lines [1501, 1559]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-28-re-initializable-pr-028` (7/21) Pattern 28: Re-Initializable Proxy Due to Missing Modifier - lines [1560, 1609]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-3-unprotected-uups-upg-003` (7/21) Pattern 3: Unprotected UUPS Upgrade Function - lines [236, 279]
- [x] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-4-no-storage-gap-in-up-004` (8/21) Pattern 4: No Storage Gap in Upgradeable Base Contract - lines [280, 320]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-5-storage-collision-no-005` (8/21) Pattern 5: Storage Collision - Non-EIP1967 Implementation Slot - lines [321, 367]
- [x] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-6-initialization-front-006` (8/21) Pattern 6: Initialization Front-Running - lines [368, 417]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-7-wrong-ownable-librar-007` (7/21) Pattern 7: Wrong Ownable Library in Upgradeable Contract - lines [418, 455]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-8-delegatecall-nonce-r-008` (7/21) Pattern 8: Delegatecall Nonce Reset Allowing Re-initialization - lines [456, 515]
- [x] `general-infrastructure-proxy-pattern-vulnerabilities-pattern-9-constructor-state-no-009` (9/21) Pattern 9: Constructor State Not Available in Proxy - lines [516, 569]
- [ ] `general-infrastructure-proxy-pattern-vulnerabilities-proxy-pattern-implementation-v-000` (11/21) Proxy Pattern Implementation Vulnerabilities - lines [83, 145]

Progress: 5/29 cards source-enriched for this file.

### `DB/general/randomness/weak-randomness-vulnerabilities.md`

- [ ] `general-governance-weak-randomness-vulnerabilities-manual-checklist-004` (6/21) Manual Checklist - lines [594, 603]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/reentrancy/defi-reentrancy-patterns.md`

- [ ] `general-infrastructure-defi-reentrancy-patterns-critical-exploits-10m-006` (6/21) Critical Exploits ($10M+) - lines [626, 636]
- [ ] `general-infrastructure-defi-reentrancy-patterns-high-severity-exploits-1m-10m-007` (6/21) High-Severity Exploits ($1M-$10M) - lines [637, 647]
- [ ] `general-infrastructure-defi-reentrancy-patterns-lower-severity-exploits-100k-009` (6/21) Lower-Severity Exploits (<$100K) - lines [665, 676]
- [ ] `general-infrastructure-defi-reentrancy-patterns-medium-severity-exploits-100k--008` (6/21) Medium-Severity Exploits ($100K-$1M) - lines [648, 664]

Progress: 0/4 cards source-enriched for this file.

### `DB/general/reentrancy/defihacklabs-callback-reentrancy-2022-patterns.md`

- [ ] `general-infrastructure-defihacklabs-callback-reentrancy-2022-pa-1-erc-677-ontokentransfer-reen-001` (9/21) 1. ERC-677 `onTokenTransfer` Reentrancy During Liquidation - lines [112, 181]
- [ ] `general-infrastructure-defihacklabs-callback-reentrancy-2022-pa-2-flash-loan-callback-reentran-002` (8/21) 2. Flash Loan Callback Reentrancy - Deposit-in-Callback - lines [182, 240]
- [ ] `general-infrastructure-defihacklabs-callback-reentrancy-2022-pa-3-erc-1155-onerc1155received-r-003` (8/21) 3. ERC-1155 `onERC1155Received` Reentrancy During NFT Mint - lines [241, 298]
- [ ] `general-infrastructure-defihacklabs-callback-reentrancy-2022-pa-4-native-eth-avax-receive-reen-004` (8/21) 4. Native ETH/AVAX `receive()` Reentrancy - exitMarket/State Bypass - lines [299, 395]

Progress: 0/4 cards source-enriched for this file.

### `DB/general/reentrancy/defihacklabs-readonly-reentrancy-patterns.md`

- [ ] `general-infrastructure-defihacklabs-readonly-reentrancy-pattern-1-curve-pool-read-only-reentra-001` (9/21) 1. Curve Pool Read-Only Reentrancy - lines [108, 230]
- [ ] `general-infrastructure-defihacklabs-readonly-reentrancy-pattern-2-balancer-pool-read-only-reen-002` (8/21) 2. Balancer Pool Read-Only Reentrancy - lines [231, 306]

Progress: 0/2 cards source-enriched for this file.

### `DB/general/reentrancy/defihacklabs-reentrancy-2023-patterns.md`

- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-1-read-only-reentrancy-via-cur-001` (9/21) 1. Read-Only Reentrancy via Curve LP Withdrawal - lines [137, 225]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-2-read-only-reentrancy-via-cur-002` (8/21) 2. Read-Only Reentrancy via Curve Callback (Conic $3.25M) - lines [226, 267]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-3-balancer-view-reentrancy-via-003` (6/21) 3. Balancer View Reentrancy via LP Price Oracle (Sentiment $1M) - lines [268, 315]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-4-fake-token-reentrancy-in-dex-004` (8/21) 4. Fake Token Reentrancy in DEX Swap (Orion $645K) - lines [316, 372]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-5-native-token-receive-reentra-005` (8/21) 5. Native Token Receive() Reentrancy (StarsArena $3M) - lines [373, 423]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-6-curve-reentrancy-in-read-onl-006` (8/21) 6. Curve Reentrancy in Read-Only Oracle (Sturdy $800K) - lines [424, 455]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-secure-implementations-007` (10/21) Secure Implementations - lines [456, 506]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2023-patterns-static-analysis-009` (6/21) Static Analysis - lines [522, 536]

Progress: 0/8 cards source-enriched for this file.

### `DB/general/reentrancy/defihacklabs-reentrancy-2024-patterns.md`

- [ ] `general-infrastructure-defihacklabs-reentrancy-2024-patterns-1-fake-token-reward-harvesting-001` (9/21) 1. Fake Token Reward Harvesting Callback Reentrancy - lines [110, 176]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2024-patterns-2-empty-market-phantom-collate-002` (9/21) 2. Empty Market Phantom Collateral Attack - lines [177, 231]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2024-patterns-3-erc-3156-flash-loan-callback-003` (9/21) 3. ERC-3156 Flash Loan Callback Re-deposit Loop - lines [232, 299]
- [ ] `general-infrastructure-defihacklabs-reentrancy-2024-patterns-4-strategy-callback-reentrancy-004` (9/21) 4. Strategy Callback Reentrancy via Attacker-Controlled Hook - lines [300, 379]

Progress: 0/4 cards source-enriched for this file.

### `DB/general/reentrancy/reentrancy.md`

- [ ] `general-infrastructure-reentrancy-example-1-read-only-reentrancy-001` (8/21) Example 1: Read-Only Reentrancy in Oracle (HIGH - Blueberry) - lines [94, 108]
- [ ] `general-infrastructure-reentrancy-example-2-classic-reentrancy-i-002` (6/21) Example 2: Classic Reentrancy in Settlement (HIGH - Cega) - lines [109, 120]
- [ ] `general-infrastructure-reentrancy-keywords-010` (8/21) Keywords - lines [191, 214]

Progress: 0/3 cards source-enriched for this file.

### `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`

- [x] `general-defi-eigenpod-beacon-chain-vulnerabilities-1-proof-forgery-via-missing-bo-000` (16/21) 1. Proof Forgery via Missing Bounds Checks - lines [147, 343]
- [x] `general-defi-eigenpod-beacon-chain-vulnerabilities-2-beacon-state-root-upgrade-br-001` (16/21) 2. Beacon State Root Upgrade Breakage - lines [344, 510]
- [x] `general-defi-eigenpod-beacon-chain-vulnerabilities-3-stakedbutunverifiednativeeth-002` (15/21) 3. stakedButUnverifiedNativeETH Accounting Bugs - lines [511, 644]
- [x] `general-defi-eigenpod-beacon-chain-vulnerabilities-4-permissionless-proof-verific-003` (13/21) 4. Permissionless Proof Verification Bypass - lines [645, 718]
- [x] `general-defi-eigenpod-beacon-chain-vulnerabilities-5-slashing-factor-miscalculati-004` (12/21) 5. Slashing Factor Miscalculation - lines [719, 802]
- [x] `general-defi-eigenpod-beacon-chain-vulnerabilities-6-timestamp-boundary-errors-005` (9/21) 6. Timestamp Boundary Errors - lines [803, 888]

Progress: 6/6 cards source-enriched for this file.

### `DB/general/restaking/LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md`

- [x] `general-defi-lrt-exchange-rate-oracle-vulnerabilities-1-lst-oracle-manipulation-via--000` (14/21) 1. LST Oracle Manipulation via Upgradeable Proxies - lines [132, 252]
- [x] `general-defi-lrt-exchange-rate-oracle-vulnerabilities-2-exchange-rate-sandwich-front-001` (13/21) 2. Exchange Rate Sandwich / Frontrunning - lines [253, 347]
- [x] `general-defi-lrt-exchange-rate-oracle-vulnerabilities-3-stale-or-divergent-rate-prov-002` (12/21) 3. Stale or Divergent Rate Providers - lines [348, 397]
- [x] `general-defi-lrt-exchange-rate-oracle-vulnerabilities-4-exchange-rate-calculation-er-003` (10/21) 4. Exchange Rate Calculation Errors - lines [398, 476]
- [x] `general-defi-lrt-exchange-rate-oracle-vulnerabilities-5-withdrawal-pricing-during-be-004` (11/21) 5. Withdrawal Pricing During Beacon Chain Exits - lines [477, 523]
- [x] `general-defi-lrt-exchange-rate-oracle-vulnerabilities-6-share-value-appreciation-blo-005` (12/21) 6. Share Value Appreciation Blocking Settlement - lines [524, 642]

Progress: 6/6 cards source-enriched for this file.

### `DB/general/restaking/LRT_SHARE_ACCOUNTING_VULNERABILITIES.md`

- [x] `general-defi-lrt-share-accounting-vulnerabilities-1-first-depositor-donation-att-000` (15/21) 1. First Depositor / Donation Attacks - lines [153, 292]
- [x] `general-defi-lrt-share-accounting-vulnerabilities-2-tvl-calculation-errors-001` (10/21) 2. TVL Calculation Errors - lines [293, 395]
- [x] `general-defi-lrt-share-accounting-vulnerabilities-3-transfer-before-calculation--002` (11/21) 3. Transfer-Before-Calculation (CEI Violations) - lines [396, 448]
- [x] `general-defi-lrt-share-accounting-vulnerabilities-4-share-accounting-desynchroni-003` (11/21) 4. Share Accounting Desynchronization - lines [449, 551]
- [x] `general-defi-lrt-share-accounting-vulnerabilities-5-slashing-induced-accounting--004` (12/21) 5. Slashing-Induced Accounting Breakage - lines [552, 626]
- [x] `general-defi-lrt-share-accounting-vulnerabilities-6-supply-inflation-via-unaccou-005` (12/21) 6. Supply Inflation via Unaccounted Operations - lines [627, 681]
- [x] `general-defi-lrt-share-accounting-vulnerabilities-7-rounding-and-precision-failu-006` (11/21) 7. Rounding and Precision Failures - lines [682, 791]

Progress: 7/7 cards source-enriched for this file.

### `DB/general/restaking/RESTAKING_OPERATOR_DELEGATION_VULNERABILITIES.md`

- [x] `general-defi-restaking-operator-delegation-vulnerabil-1-operator-censorship-via-forc-000` (15/21) 1. Operator Censorship via Forced Undelegation - lines [144, 253]
- [x] `general-defi-restaking-operator-delegation-vulnerabil-2-minipool-state-machine-hijac-001` (14/21) 2. Minipool State Machine Hijacking - lines [254, 343]
- [x] `general-defi-restaking-operator-delegation-vulnerabil-3-undelegation-breaking-lrt-ex-002` (14/21) 3. Undelegation Breaking LRT Exchange Rate - lines [344, 439]
- [x] `general-defi-restaking-operator-delegation-vulnerabil-4-heap-corruption-from-operato-003` (12/21) 4. Heap Corruption from Operator Removal - lines [440, 501]
- [x] `general-defi-restaking-operator-delegation-vulnerabil-5-delegation-enforcer-bypasses-004` (10/21) 5. Delegation Enforcer Bypasses - lines [502, 578]
- [x] `general-defi-restaking-operator-delegation-vulnerabil-6-stakes-not-forwarded-post-de-005` (11/21) 6. Stakes Not Forwarded Post-Delegation - lines [579, 633]
- [x] `general-defi-restaking-operator-delegation-vulnerabil-7-front-running-operator-regis-006` (12/21) 7. Front-Running Operator Registration - lines [634, 723]

Progress: 7/7 cards source-enriched for this file.

### `DB/general/restaking/RESTAKING_REWARD_DISTRIBUTION_VULNERABILITIES.md`

- [x] `general-defi-restaking-reward-distribution-vulnerabil-1-sandwich-front-running-rewar-000` (14/21) 1. Sandwich / Front-Running Reward Claims - lines [141, 272]
- [x] `general-defi-restaking-reward-distribution-vulnerabil-2-msg-sender-confusion-in-rewa-001` (11/21) 2. msg.sender Confusion in Reward Re-Staking - lines [273, 332]
- [x] `general-defi-restaking-reward-distribution-vulnerabil-3-reward-accounting-double-cou-002` (12/21) 3. Reward Accounting Double-Counting - lines [333, 404]
- [x] `general-defi-restaking-reward-distribution-vulnerabil-4-stale-snapshot-data-after-un-003` (11/21) 4. Stale Snapshot Data After Unstaking - lines [405, 468]
- [x] `general-defi-restaking-reward-distribution-vulnerabil-5-rewards-lost-missing-impleme-004` (12/21) 5. Rewards Lost - Missing Implementations - lines [469, 563]
- [x] `general-defi-restaking-reward-distribution-vulnerabil-6-reentrancy-based-reward-thef-005` (13/21) 6. Reentrancy-Based Reward Theft - lines [564, 651]
- [x] `general-defi-restaking-reward-distribution-vulnerabil-7-reward-dilution-via-just-in--006` (12/21) 7. Reward Dilution via Just-In-Time Staking - lines [652, 784]

Progress: 7/7 cards source-enriched for this file.

### `DB/general/restaking/RESTAKING_SLASHING_VULNERABILITIES.md`

- [x] `general-defi-restaking-slashing-vulnerabilities-1-unslashable-vault-creation-000` (16/21) 1. Unslashable Vault Creation - lines [135, 271]
- [x] `general-defi-restaking-slashing-vulnerabilities-2-over-slashing-and-double-red-001` (13/21) 2. Over-Slashing and Double-Reduction - lines [272, 357]
- [x] `general-defi-restaking-slashing-vulnerabilities-3-slashing-bypass-via-timing-002` (12/21) 3. Slashing Bypass via Timing - lines [358, 411]
- [x] `general-defi-restaking-slashing-vulnerabilities-4-protocol-insolvency-from-lst-003` (14/21) 4. Protocol Insolvency from LST Slashing - lines [412, 497]
- [x] `general-defi-restaking-slashing-vulnerabilities-5-unfair-penalty-distribution-004` (12/21) 5. Unfair Penalty Distribution - lines [498, 556]
- [x] `general-defi-restaking-slashing-vulnerabilities-6-slashing-accounting-errors-005` (12/21) 6. Slashing Accounting Errors - lines [557, 664]

Progress: 6/6 cards source-enriched for this file.

### `DB/general/restaking/RESTAKING_WITHDRAWAL_VULNERABILITIES.md`

- [x] `general-defi-restaking-withdrawal-vulnerabilities-1-withdrawal-queue-manipulatio-000` (17/21) 1. Withdrawal Queue Manipulation - lines [163, 354]
- [x] `general-defi-restaking-withdrawal-vulnerabilities-2-share-amount-calculation-err-001` (17/21) 2. Share/Amount Calculation Errors During Withdrawal - lines [355, 527]
- [x] `general-defi-restaking-withdrawal-vulnerabilities-3-fund-lockup-during-withdrawa-002` (16/21) 3. Fund Lockup During Withdrawal - lines [528, 726]
- [x] `general-defi-restaking-withdrawal-vulnerabilities-4-slashing-interaction-with-wi-003` (15/21) 4. Slashing Interaction with Withdrawals - lines [727, 853]
- [x] `general-defi-restaking-withdrawal-vulnerabilities-5-withdrawal-delay-bypass-004` (13/21) 5. Withdrawal Delay Bypass - lines [854, 939]
- [x] `general-defi-restaking-withdrawal-vulnerabilities-6-missing-slippage-deadline-pr-005` (10/21) 6. Missing Slippage/Deadline Protection - lines [940, 1001]
- [x] `general-defi-restaking-withdrawal-vulnerabilities-7-partial-failure-handling-006` (9/21) 7. Partial Failure Handling - lines [1002, 1046]
- [x] `general-defi-restaking-withdrawal-vulnerabilities-8-reentrancy-and-access-contro-007` (10/21) 8. Reentrancy and Access Control in Withdrawal Flows - lines [1047, 1159]

Progress: 8/8 cards source-enriched for this file.

### `DB/general/rounding-precision-loss/rounding-precision-loss.md`

- [ ] `general-defi-rounding-precision-loss-example-1-division-before-mult-001` (9/21) Example 1: Division Before Multiplication (MEDIUM - Virtuals Protocol) - lines [97, 116]
- [ ] `general-defi-rounding-precision-loss-example-2-rounding-causes-lock-002` (8/21) Example 2: Rounding Causes Locked Funds (HIGH - Fabric) - lines [117, 132]
- [ ] `general-defi-rounding-precision-loss-example-3-share-calculation-ro-003` (8/21) Example 3: Share Calculation Rounding (MEDIUM - ERC4626) - lines [133, 152]
- [ ] `general-defi-rounding-precision-loss-fix-2-use-high-precision-libra-005` (7/21) Fix 2: Use High-Precision Libraries - lines [163, 173]
- [ ] `general-defi-rounding-precision-loss-keywords-012` (8/21) Keywords - lines [251, 274]

Progress: 0/5 cards source-enriched for this file.

### `DB/general/slippage-protection/slippage-protection.md`

- [ ] `general-defi-slippage-protection-example-1-unused-slippage-para-001` (7/21) Example 1: Unused Slippage Parameters (HIGH - Vader Protocol) - lines [145, 171]
- [ ] `general-defi-slippage-protection-example-2-zero-slippage-in-swa-002` (7/21) Example 2: Zero Slippage in Swap Operations (MEDIUM - Kaizen) - lines [172, 198]
- [ ] `general-defi-slippage-protection-example-3-missing-withdrawal-s-003` (8/21) Example 3: Missing Withdrawal Slippage Protection (MEDIUM - Sentiment V2) - lines [199, 224]
- [ ] `general-defi-slippage-protection-example-4-block-timestamp-as-d-004` (7/21) Example 4: block.timestamp as Deadline (MEDIUM - Particle Protocol) - lines [225, 251]
- [ ] `general-defi-slippage-protection-example-5-zero-slippage-in-lev-005` (9/21) Example 5: Zero Slippage in Leverage Operations (HIGH - Peapods) - lines [252, 274]

Progress: 0/5 cards source-enriched for this file.

### `DB/general/stablecoin-vulnerabilities/STABLECOIN_VULNERABILITIES.md`

- [x] `general-governance-stablecoin-vulnerabilities-vulnerability-title-000` (17/21) Vulnerability Title - lines [81, 307]

Progress: 1/1 cards source-enriched for this file.

### `DB/general/token-compatibility/defihacklabs-reflection-token-2023-2024-patterns.md`

- [ ] `general-defi-defihacklabs-reflection-token-2023-2024--dynamic-analysis-runtime-check-009` (6/21) Dynamic Analysis / Runtime Checks - lines [677, 694]
- [ ] `general-defi-defihacklabs-reflection-token-2023-2024--reflection-tax-token-exploit-p-000` (11/21) Reflection & Tax Token Exploit Patterns (2023-2024) - lines [101, 183]
- [ ] `general-defi-defihacklabs-reflection-token-2023-2024--variant-1-deliver-skim-pattern-001` (8/21) Variant 1: deliver() + skim() Pattern (7/15 exploits) - lines [184, 329]
- [ ] `general-defi-defihacklabs-reflection-token-2023-2024--variant-2-burn-sync-pattern-2--002` (8/21) Variant 2: burn() + sync() Pattern (2/15 exploits) - lines [330, 390]
- [ ] `general-defi-defihacklabs-reflection-token-2023-2024--variant-3-self-transfer-balanc-003` (8/21) Variant 3: Self-Transfer Balance Doubling (3/15 exploits) - lines [391, 459]
- [ ] `general-defi-defihacklabs-reflection-token-2023-2024--variant-4-deflationary-pair-bu-004` (8/21) Variant 4: Deflationary Pair Burn (2/15 exploits) - lines [460, 523]
- [ ] `general-defi-defihacklabs-reflection-token-2023-2024--variant-5-tax-reflection-to-pa-005` (9/21) Variant 5: Tax Reflection to Pair (1/15 exploits) - lines [524, 575]

Progress: 0/7 cards source-enriched for this file.

### `DB/general/token-compatibility/non-standard-token-vulnerabilities.md`

- [ ] `general-defi-non-standard-token-vulnerabilities-3-erc777-erc667-callback-reent-014` (9/21) 3. ERC777/ERC667 Callback Reentrancy - lines [473, 601]
- [ ] `general-defi-non-standard-token-vulnerabilities-5-self-transfer-edge-cases-020` (7/21) 5. Self-Transfer Edge Cases - lines [733, 867]
- [ ] `general-defi-non-standard-token-vulnerabilities-6-low-no-decimals-token-issues-021` (6/21) 6. Low/No Decimals Token Issues - lines [868, 902]
- [ ] `general-defi-non-standard-token-vulnerabilities-7-pausable-blacklistable-token-022` (6/21) 7. Pausable/Blacklistable Token Risks - lines [903, 938]
- [ ] `general-defi-non-standard-token-vulnerabilities-vulnerable-pattern-deflationar-009` (6/21) Vulnerable Pattern (Deflationary + Skim Loop) [HIGH] - lines [357, 383]
- [ ] `general-defi-non-standard-token-vulnerabilities-vulnerable-pattern-example-amm-003` (6/21) Vulnerable Pattern Example (AMM Pair with Reflection Token) [CRITICAL] - lines [232, 257]
- [ ] `general-defi-non-standard-token-vulnerabilities-vulnerable-pattern-rebasing-st-016` (6/21) Vulnerable Pattern (Rebasing Staking) [HIGH] - lines [625, 643]

Progress: 0/7 cards source-enriched for this file.

### `DB/general/uups-proxy/UUPS_PROXY_VULNERABILITIES.md`

- [x] `general-infrastructure-uups-proxy-vulnerabilities-vulnerability-title-000` (17/21) Vulnerability Title - lines [81, 481]

Progress: 1/1 cards source-enriched for this file.

### `DB/general/validation/slippage-input-validation-vulnerabilities.md`

- [x] `general-security-slippage-input-validation-vulnerabilitie-slippage-input-validation-vuln-000` (18/21) Slippage & Input Validation Vulnerabilities - lines [69, 758]

Progress: 1/1 cards source-enriched for this file.

### `DB/general/vault-inflation-attack/defihacklabs-vault-inflation-patterns.md`

- [ ] `general-defi-defihacklabs-vault-inflation-patterns-1-empty-market-exchange-rate-i-001` (9/21) 1. Empty Market Exchange Rate Inflation - lines [106, 216]
- [ ] `general-defi-defihacklabs-vault-inflation-patterns-2-share-price-inflation-via-do-002` (9/21) 2. Share Price Inflation via Donation - lines [217, 331]

Progress: 0/2 cards source-enriched for this file.

### `DB/general/vault-inflation-attack/vault-inflation-attack.md`

- [ ] `general-defi-vault-inflation-attack-known-exploits-findings-004` (6/21) Known Exploits & Findings - lines [668, 679]

Progress: 0/1 cards source-enriched for this file.

### `DB/general/vetoken-governance/VETOKEN_VOTING_ESCROW_VULNERABILITIES.md`

- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-high-signal-grep-seeds-012` (6/21) High-Signal Grep Seeds - lines [840, 861]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-section-1-bribe-reward-theft-e-001` (11/21) Section 1: Bribe Reward Theft & Epoch Accounting Exploits - lines [202, 302]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-section-2-voting-power-manipul-002` (11/21) Section 2: Voting Power Manipulation & Lock Accounting Bugs - lines [303, 398]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-section-3-gauge-voting-emissio-003` (11/21) Section 3: Gauge Voting & Emission Distribution Exploits - lines [399, 479]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-section-5-boost-mechanism-expl-005` (11/21) Section 5: Boost Mechanism Exploits - lines [537, 594]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-section-6-reward-emission-dist-006` (11/21) Section 6: Reward & Emission Distribution Bugs - lines [595, 669]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-section-7-checkpoint-voting-po-007` (10/21) Section 7: Checkpoint & Voting Power Decay Bugs - lines [670, 713]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-section-8-delegation-nft-opera-008` (10/21) Section 8: Delegation & NFT Operation Exploits - lines [714, 757]
- [ ] `general-governance-vetoken-voting-escrow-vulnerabilities-vulnerability-title-000` (11/21) Vulnerability Title - lines [135, 201]

Progress: 0/9 cards source-enriched for this file.

### `DB/general/yield-strategy-vulnerabilities/yield-strategy-vulnerabilities.md`

- [x] `general-defi-yield-strategy-vulnerabilities-1-first-depositor-inflation-at-000` (15/21) 1. First Depositor / Inflation Attack - lines [209, 377]
- [x] `general-defi-yield-strategy-vulnerabilities-10-state-machine-hijacking-009` (11/21) 10. State Machine Hijacking - lines [888, 951]
- [x] `general-defi-yield-strategy-vulnerabilities-11-penalty-and-fee-bypass-via--010` (11/21) 11. Penalty and Fee Bypass via Secondary Markets - lines [952, 1011]
- [x] `general-defi-yield-strategy-vulnerabilities-12-claim-function-arithmetic-u-011` (11/21) 12. Claim Function Arithmetic Underflow - lines [1012, 1075]
- [ ] `general-defi-yield-strategy-vulnerabilities-13-missing-slippage-protection-012` (8/21) 13. Missing Slippage Protection in Yield Operations - lines [1076, 1124]
- [ ] `general-defi-yield-strategy-vulnerabilities-14-incorrect-share-calculation-013` (7/21) 14. Incorrect Share Calculation on Edge Cases - lines [1125, 1167]
- [ ] `general-defi-yield-strategy-vulnerabilities-15-reward-lockup-on-period-tra-014` (6/21) 15. Reward Lockup on Period Transitions - lines [1168, 1194]
- [ ] `general-defi-yield-strategy-vulnerabilities-16-vault-accounting-desync-015` (8/21) 16. Vault Accounting Desync - lines [1195, 1229]
- [x] `general-defi-yield-strategy-vulnerabilities-17-external-call-context-confu-016` (12/21) 17. External Call Context Confusion - lines [1230, 1282]
- [ ] `general-defi-yield-strategy-vulnerabilities-18-deposit-withdrawal-same-blo-017` (7/21) 18. Deposit/Withdrawal Same-Block Arbitrage - lines [1283, 1324]
- [ ] `general-defi-yield-strategy-vulnerabilities-19-strategy-migration-token-lo-018` (7/21) 19. Strategy Migration Token Loss - lines [1325, 1358]
- [x] `general-defi-yield-strategy-vulnerabilities-2-exchange-rate-manipulation-v-001` (11/21) 2. Exchange Rate Manipulation via Donation - lines [378, 450]
- [ ] `general-defi-yield-strategy-vulnerabilities-20-compound-interest-manipulat-019` (7/21) 20. Compound Interest Manipulation - lines [1359, 1392]
- [ ] `general-defi-yield-strategy-vulnerabilities-21-time-weighted-voting-power--020` (7/21) 21. Time-Weighted Voting Power Exploitation - lines [1393, 1424]
- [ ] `general-defi-yield-strategy-vulnerabilities-22-emergency-withdrawal-accoun-021` (7/21) 22. Emergency Withdrawal Accounting Errors - lines [1425, 1459]
- [ ] `general-defi-yield-strategy-vulnerabilities-23-yield-aggregator-fund-isola-022` (8/21) 23. Yield Aggregator Fund Isolation Failures - lines [1460, 1496]
- [x] `general-defi-yield-strategy-vulnerabilities-24-vote-manipulation-via-dupli-023` (11/21) 24. Vote Manipulation via Duplicate Pool Entries - lines [1497, 1561]
- [x] `general-defi-yield-strategy-vulnerabilities-25-vesting-contract-interface--024` (11/21) 25. Vesting Contract Interface Spoofing - lines [1562, 1618]
- [x] `general-defi-yield-strategy-vulnerabilities-26-unbounded-reward-accrual-af-025` (11/21) 26. Unbounded Reward Accrual After Period End - lines [1619, 1677]
- [x] `general-defi-yield-strategy-vulnerabilities-27-precision-library-mismatch-026` (11/21) 27. Precision Library Mismatch - lines [1678, 1732]
- [x] `general-defi-yield-strategy-vulnerabilities-28-unbounded-loop-dos-via-arra-027` (13/21) 28. Unbounded Loop DoS via Array Growth - lines [1733, 1791]
- [x] `general-defi-yield-strategy-vulnerabilities-29-minimum-deposit-bypass-via--028` (11/21) 29. Minimum Deposit Bypass via Withdrawal - lines [1792, 1851]
- [x] `general-defi-yield-strategy-vulnerabilities-3-reward-distribution-edge-cas-002` (12/21) 3. Reward Distribution Edge Cases - lines [451, 510]
- [x] `general-defi-yield-strategy-vulnerabilities-30-strategy-migration-state-lo-029` (11/21) 30. Strategy Migration State Loss - lines [1852, 1911]
- [x] `general-defi-yield-strategy-vulnerabilities-31-double-subtraction-accounti-030` (11/21) 31. Double Subtraction Accounting Error - lines [1912, 1968]
- [x] `general-defi-yield-strategy-vulnerabilities-32-reentrancy-lock-bypass-via--031` (9/21) 32. Reentrancy Lock Bypass via Storage Mode Switch - lines [1969, 2032]
- [x] `general-defi-yield-strategy-vulnerabilities-33-timestamp-boundary-conditio-032` (9/21) 33. Timestamp Boundary Condition in Activity Checks - lines [2033, 2087]
- [x] `general-defi-yield-strategy-vulnerabilities-34-first-depositor-market-bric-033` (11/21) 34. First Depositor Market Bricking - lines [2088, 2151]
- [x] `general-defi-yield-strategy-vulnerabilities-35-collateral-rebalancing-gaps-034` (11/21) 35. Collateral Rebalancing Gaps - lines [2152, 2219]
- [ ] `general-defi-yield-strategy-vulnerabilities-4-stale-reward-accumulator-sta-003` (7/21) 4. Stale Reward Accumulator State - lines [511, 551]
- [x] `general-defi-yield-strategy-vulnerabilities-5-flash-loan-lp-fee-extraction-004` (11/21) 5. Flash Loan LP Fee Extraction - lines [552, 613]
- [x] `general-defi-yield-strategy-vulnerabilities-6-cross-function-reentrancy-in-005` (12/21) 6. Cross-Function Reentrancy in Token Hooks - lines [614, 685]
- [x] `general-defi-yield-strategy-vulnerabilities-7-read-only-reentrancy-in-orac-006` (11/21) 7. Read-Only Reentrancy in Oracle Integration - lines [686, 741]
- [x] `general-defi-yield-strategy-vulnerabilities-8-partial-withdrawal-token-fre-007` (11/21) 8. Partial Withdrawal Token Freeze - lines [742, 814]
- [x] `general-defi-yield-strategy-vulnerabilities-9-reward-multiplication-via-me-008` (11/21) 9. Reward Multiplication via Merge Operations - lines [815, 887]

Progress: 24/35 cards source-enriched for this file.

### `DB/oracle/chainlink/CHAINLINK_AUTOMATION_VULNERABILITIES.md`

- [x] `oracle-chainlink-automation-vulnerabilities-1-checkupkeep-performupkeep-mi-000` (14/21) 1. CheckUpkeep/PerformUpkeep Mismatch - lines [120, 307]
- [x] `oracle-chainlink-automation-vulnerabilities-2-gas-limit-issues-001` (12/21) 2. Gas Limit Issues - lines [308, 408]
- [x] `oracle-chainlink-automation-vulnerabilities-3-unbounded-operations-002` (9/21) 3. Unbounded Operations - lines [409, 454]
- [ ] `oracle-chainlink-automation-vulnerabilities-4-callback-safety-003` (7/21) 4. Callback Safety - lines [455, 494]
- [x] `oracle-chainlink-automation-vulnerabilities-5-authentication-missing-004` (13/21) 5. Authentication Missing - lines [495, 561]
- [x] `oracle-chainlink-automation-vulnerabilities-6-response-validation-005` (9/21) 6. Response Validation - lines [562, 621]

Progress: 5/6 cards source-enriched for this file.

### `DB/oracle/chainlink/CHAINLINK_CCIP_VULNERABILITIES.md`

- [x] `oracle-chainlink-ccip-vulnerabilities-1-message-decoding-vulnerabili-000` (14/21) 1. Message Decoding Vulnerabilities - lines [133, 288]
- [x] `oracle-chainlink-ccip-vulnerabilities-2-router-configuration-issues-001` (11/21) 2. Router Configuration Issues - lines [289, 358]
- [x] `oracle-chainlink-ccip-vulnerabilities-3-extra-args-configuration-002` (11/21) 3. Extra Args Configuration - lines [359, 424]
- [x] `oracle-chainlink-ccip-vulnerabilities-4-source-sender-validation-003` (11/21) 4. Source/Sender Validation - lines [425, 492]
- [x] `oracle-chainlink-ccip-vulnerabilities-5-callback-receive-handling-004` (12/21) 5. Callback/Receive Handling - lines [493, 580]
- [x] `oracle-chainlink-ccip-vulnerabilities-6-gas-limit-configuration-005` (8/21) 6. Gas Limit Configuration - lines [581, 631]

Progress: 6/6 cards source-enriched for this file.

### `DB/oracle/chainlink/CHAINLINK_PRICE_FEED_VULNERABILITIES.md`

- [x] `oracle-chainlink-price-feed-vulnerabilities-1-staleness-vulnerabilities-000` (16/21) 1. Staleness Vulnerabilities - lines [163, 351]
- [x] `oracle-chainlink-price-feed-vulnerabilities-2-l2-sequencer-uptime-vulnerab-001` (16/21) 2. L2 Sequencer Uptime Vulnerabilities - lines [352, 469]
- [x] `oracle-chainlink-price-feed-vulnerabilities-3-circuit-breaker-min-max-pric-002` (14/21) 3. Circuit Breaker / Min-Max Price Vulnerabilities - lines [470, 582]
- [x] `oracle-chainlink-price-feed-vulnerabilities-4-deprecated-api-usage-003` (14/21) 4. Deprecated API Usage - lines [583, 647]
- [x] `oracle-chainlink-price-feed-vulnerabilities-5-access-denial-revert-handlin-004` (10/21) 5. Access Denial / Revert Handling - lines [648, 704]
- [x] `oracle-chainlink-price-feed-vulnerabilities-6-decimal-precision-handling-005` (13/21) 6. Decimal/Precision Handling - lines [705, 766]
- [x] `oracle-chainlink-price-feed-vulnerabilities-7-phase-id-round-id-handling-006` (12/21) 7. Phase ID / Round ID Handling - lines [767, 823]
- [ ] `oracle-chainlink-price-feed-vulnerabilities-8-price-manipulation-front-run-007` (10/21) 8. Price Manipulation / Front-Running - lines [824, 854]

Progress: 7/8 cards source-enriched for this file.

### `DB/oracle/chainlink/CHAINLINK_VRF_VULNERABILITIES.md`

- [x] `oracle-chainlink-vrf-vulnerabilities-1-vrf-re-roll-manipulation-att-000` (15/21) 1. VRF Re-Roll / Manipulation Attacks - lines [130, 287]
- [x] `oracle-chainlink-vrf-vulnerabilities-2-subscription-drain-vulnerabi-001` (13/21) 2. Subscription Drain Vulnerabilities - lines [288, 416]
- [x] `oracle-chainlink-vrf-vulnerabilities-3-callback-revert-issues-002` (13/21) 3. Callback Revert Issues - lines [417, 587]
- [ ] `oracle-chainlink-vrf-vulnerabilities-4-vrf-version-deprecation-003` (7/21) 4. VRF Version Deprecation - lines [588, 651]
- [x] `oracle-chainlink-vrf-vulnerabilities-5-weak-randomness-sources-004` (10/21) 5. Weak Randomness Sources - lines [652, 701]
- [x] `oracle-chainlink-vrf-vulnerabilities-6-request-configuration-issues-005` (9/21) 6. Request Configuration Issues - lines [702, 746]

Progress: 5/6 cards source-enriched for this file.

### `DB/oracle/price-manipulation/defihacklabs-bsc-oracle-manipulation-2022.md`

- [ ] `oracle-defihacklabs-bsc-oracle-manipulation-202-invariant-checks-004` (8/21) Invariant Checks - lines [624, 638]

Progress: 0/1 cards source-enriched for this file.

### `DB/oracle/price-manipulation/defihacklabs-flashloan-oracle-2022-patterns.md`

- [ ] `oracle-defihacklabs-flashloan-oracle-2022-patte-1-amm-reserve-based-price-orac-001` (9/21) 1. AMM Reserve-Based Price Oracle - Direct LP Pool Manipulation - lines [127, 223]
- [ ] `oracle-defihacklabs-flashloan-oracle-2022-patte-2-curve-lp-virtual-price-oracl-002` (9/21) 2. Curve LP / Virtual Price Oracle Manipulation - lines [224, 297]
- [ ] `oracle-defihacklabs-flashloan-oracle-2022-patte-3-solidly-lp-oracle-weak-signa-003` (8/21) 3. Solidly LP Oracle + Weak Signature Validation - lines [298, 372]
- [ ] `oracle-defihacklabs-flashloan-oracle-2022-patte-4-vault-share-price-inflation--004` (8/21) 4. Vault Share Price Inflation via Donation - lines [373, 448]

Progress: 0/4 cards source-enriched for this file.

### `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md`

- [ ] `oracle-defihacklabs-oracle-manipulation-2023-pa-1-low-cost-oracle-reporter-man-001` (9/21) 1. Low-Cost Oracle Reporter Manipulation (BonqDAO $88M) - lines [160, 255]
- [ ] `oracle-defihacklabs-oracle-manipulation-2023-pa-2-concentrated-liquidity-bin-m-002` (8/21) 2. Concentrated Liquidity Bin Manipulation (Jimbo $8M) - lines [256, 329]
- [ ] `oracle-defihacklabs-oracle-manipulation-2023-pa-3-curve-lp-token-price-manipul-003` (8/21) 3. Curve LP Token Price Manipulation (Zunami $2M) - lines [330, 361]
- [ ] `oracle-defihacklabs-oracle-manipulation-2023-pa-4-vtoken-collateral-oracle-man-004` (8/21) 4. vToken Collateral Oracle Manipulation (0vix $2M) - lines [362, 393]
- [ ] `oracle-defihacklabs-oracle-manipulation-2023-pa-5-flash-loan-spot-price-compou-005` (8/21) 5. Flash Loan + Spot Price (CompounderFinance $27.2M, Gamma $6.3M, Allbridge $550K) - lines [394, 431]
- [ ] `oracle-defihacklabs-oracle-manipulation-2023-pa-6-lending-protocol-oracle-mani-006` (8/21) 6. Lending Protocol Oracle Manipulation (RodeoFinance $888K) - lines [432, 461]
- [ ] `oracle-defihacklabs-oracle-manipulation-2023-pa-secure-implementations-007` (10/21) Secure Implementations - lines [462, 520]

Progress: 0/7 cards source-enriched for this file.

### `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2024-2025.md`

- [ ] `oracle-defihacklabs-oracle-manipulation-2024-20-1-curve-pool-based-oracle-mani-001` (9/21) 1. Curve Pool-Based Oracle Manipulation for Lending Liquidation - lines [139, 200]
- [ ] `oracle-defihacklabs-oracle-manipulation-2024-20-2-self-referencing-oracle-spmm-002` (8/21) 2. Self-Referencing Oracle (sPMM) Manipulation - lines [201, 245]
- [ ] `oracle-defihacklabs-oracle-manipulation-2024-20-3-concentrated-liquidity-vault-003` (6/21) 3. Concentrated Liquidity Vault Deposit/Withdraw Cycling - lines [246, 297]
- [ ] `oracle-defihacklabs-oracle-manipulation-2024-20-4-defective-token-transfer-hoo-004` (8/21) 4. Defective Token Transfer Hook Price Disruption - lines [298, 340]
- [ ] `oracle-defihacklabs-oracle-manipulation-2024-20-5-broken-vault-mint-ratio-005` (8/21) 5. Broken Vault Mint Ratio - lines [341, 374]
- [ ] `oracle-defihacklabs-oracle-manipulation-2024-20-6-faulty-chainlink-oracle-pric-006` (8/21) 6. Faulty Chainlink Oracle Price Feed - lines [375, 422]

Progress: 0/6 cards source-enriched for this file.

### `DB/oracle/price-manipulation/defihacklabs-price-manipulation-patterns.md`

- [ ] `oracle-defihacklabs-price-manipulation-patterns-root-cause-categories-000` (8/21) Root Cause Categories - lines [137, 147]

Progress: 0/1 cards source-enriched for this file.

### `DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md`

- [x] `oracle-flash-loan-oracle-manipulation-flash-loan-oracle-manipulation-000` (17/21) Flash Loan Oracle Manipulation - lines [85, 849]

Progress: 1/1 cards source-enriched for this file.

### `DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md`

- [x] `oracle-pyth-oracle-vulnerabilities-1-staleness-vulnerabilities-000` (16/21) 1. Staleness Vulnerabilities - lines [165, 367]
- [x] `oracle-pyth-oracle-vulnerabilities-10-integration-configuration-v-009` (11/21) 10. Integration & Configuration Vulnerabilities - lines [1402, 1501]
- [x] `oracle-pyth-oracle-vulnerabilities-2-confidence-interval-vulnerab-001` (13/21) 2. Confidence Interval Vulnerabilities - lines [368, 499]
- [x] `oracle-pyth-oracle-vulnerabilities-3-exponent-handling-vulnerabil-002` (14/21) 3. Exponent Handling Vulnerabilities - lines [500, 658]
- [x] `oracle-pyth-oracle-vulnerabilities-4-same-transaction-price-manip-003` (16/21) 4. Same-Transaction Price Manipulation - lines [659, 859]
- [x] `oracle-pyth-oracle-vulnerabilities-5-pull-based-oracle-exploitati-004` (16/21) 5. Pull-Based Oracle Exploitation - lines [860, 1015]
- [x] `oracle-pyth-oracle-vulnerabilities-6-price-update-fee-vulnerabili-005` (12/21) 6. Price Update Fee Vulnerabilities - lines [1016, 1119]
- [x] `oracle-pyth-oracle-vulnerabilities-7-self-liquidation-attacks-006` (12/21) 7. Self-Liquidation Attacks - lines [1120, 1226]
- [x] `oracle-pyth-oracle-vulnerabilities-8-timestamp-validation-vulnera-007` (10/21) 8. Timestamp Validation Vulnerabilities - lines [1227, 1303]
- [x] `oracle-pyth-oracle-vulnerabilities-9-pyth-entropy-vrf-vulnerabili-008` (10/21) 9. Pyth Entropy (VRF) Vulnerabilities - lines [1304, 1401]

Progress: 10/10 cards source-enriched for this file.

### `DB/tokens/erc20/ERC20_TOKEN_VULNERABILITIES.md`

- [x] `tokens-erc20-token-vulnerabilities-1-transfer-transferfrom-vulner-001` (16/21) 1. Transfer & TransferFrom Vulnerabilities - lines [196, 378]
- [ ] `tokens-erc20-token-vulnerabilities-10-comprehensive-keyword-index-010` (8/21) 10. Comprehensive Keyword Index - lines [2257, 2328]
- [x] `tokens-erc20-token-vulnerabilities-2-approval-allowance-vulnerabi-002` (15/21) 2. Approval & Allowance Vulnerabilities - lines [379, 542]
- [x] `tokens-erc20-token-vulnerabilities-3-decimals-precision-vulnerabi-003` (14/21) 3. Decimals & Precision Vulnerabilities - lines [543, 739]
- [x] `tokens-erc20-token-vulnerabilities-4-fee-on-transfer-token-vulner-004` (15/21) 4. Fee-on-Transfer Token Vulnerabilities - lines [740, 984]
- [x] `tokens-erc20-token-vulnerabilities-5-rebasing-token-vulnerabiliti-005` (16/21) 5. Rebasing Token Vulnerabilities - lines [985, 1242]
- [x] `tokens-erc20-token-vulnerabilities-6-erc777-reentrancy-vulnerabil-006` (13/21) 6. ERC777 Reentrancy Vulnerabilities - lines [1243, 1505]
- [x] `tokens-erc20-token-vulnerabilities-7-blacklist-pausable-token-vul-007` (14/21) 7. Blacklist & Pausable Token Vulnerabilities - lines [1506, 1812]
- [x] `tokens-erc20-token-vulnerabilities-8-inflation-first-depositor-at-008` (16/21) 8. Inflation & First Depositor Attack Vulnerabilities - lines [1813, 2107]
- [x] `tokens-erc20-token-vulnerabilities-9-mint-burn-vulnerabilities-009` (13/21) 9. Mint & Burn Vulnerabilities - lines [2108, 2256]
- [ ] `tokens-erc20-token-vulnerabilities-summary-quick-reference-011` (6/21) Summary & Quick Reference - lines [2329, 2360]

Progress: 9/11 cards source-enriched for this file.

### `DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md`

- [x] `tokens-erc4626-vault-vulnerabilities-1-first-depositor-inflation-at-000` (16/21) 1. First Depositor / Inflation Attack Vulnerabilities - lines [219, 537]
- [ ] `tokens-erc4626-vault-vulnerabilities-10-access-control-state-manage-009` (7/21) 10. Access Control & State Management - lines [1386, 1433]
- [x] `tokens-erc4626-vault-vulnerabilities-2-erc4626-compliance-issues-001` (14/21) 2. ERC4626 Compliance Issues - lines [538, 714]
- [x] `tokens-erc4626-vault-vulnerabilities-3-rounding-direction-vulnerabi-002` (14/21) 3. Rounding Direction Vulnerabilities - lines [715, 842]
- [x] `tokens-erc4626-vault-vulnerabilities-4-fee-handling-vulnerabilities-003` (11/21) 4. Fee Handling Vulnerabilities - lines [843, 934]
- [x] `tokens-erc4626-vault-vulnerabilities-5-slippage-protection-issues-004` (9/21) 5. Slippage Protection Issues - lines [935, 1039]
- [x] `tokens-erc4626-vault-vulnerabilities-6-exchange-rate-manipulation-005` (11/21) 6. Exchange Rate Manipulation - lines [1040, 1129]
- [x] `tokens-erc4626-vault-vulnerabilities-7-decimal-handling-issues-006` (9/21) 7. Decimal Handling Issues - lines [1130, 1198]
- [x] `tokens-erc4626-vault-vulnerabilities-8-reentrancy-vulnerabilities-007` (9/21) 8. Reentrancy Vulnerabilities - lines [1199, 1323]
- [x] `tokens-erc4626-vault-vulnerabilities-9-token-compatibility-issues-008` (8/21) 9. Token Compatibility Issues - lines [1324, 1385]

Progress: 9/10 cards source-enriched for this file.

### `DB/tokens/erc721/ERC721_NFT_VULNERABILITIES.md`

- [x] `tokens-erc721-nft-vulnerabilities-1-1-using-transferfrom-instead-001` (9/21) 1.1 Using `transferFrom` Instead of `safeTransferFrom` - lines [148, 185]
- [x] `tokens-erc721-nft-vulnerabilities-1-2-using-mint-instead-of-safe-002` (9/21) 1.2 Using `_mint` Instead of `_safeMint` - lines [186, 230]
- [x] `tokens-erc721-nft-vulnerabilities-2-reentrancy-via-nft-callbacks-003` (12/21) 2. Reentrancy via NFT Callbacks - lines [231, 386]
- [x] `tokens-erc721-nft-vulnerabilities-3-approval-and-access-control--004` (9/21) 3. Approval and Access Control Issues - lines [387, 478]
- [x] `tokens-erc721-nft-vulnerabilities-4-1-double-voting-through-self-005` (10/21) 4.1 Double Voting Through Self-Delegation - lines [481, 535]
- [x] `tokens-erc721-nft-vulnerabilities-4-2-delegation-disables-nft-tr-006` (9/21) 4.2 Delegation Disables NFT Transfers - lines [536, 569]
- [x] `tokens-erc721-nft-vulnerabilities-4-3-double-voting-via-managed--007` (10/21) 4.3 Double Voting via Managed NFTs - lines [570, 611]
- [x] `tokens-erc721-nft-vulnerabilities-5-royalty-manipulation-008` (10/21) 5. Royalty Manipulation - lines [612, 673]
- [x] `tokens-erc721-nft-vulnerabilities-6-erc-721-standard-compliance--009` (13/21) 6. ERC-721 Standard Compliance Issues - lines [674, 755]
- [ ] `tokens-erc721-nft-vulnerabilities-7-nft-liquidation-and-collater-010` (9/21) 7. NFT Liquidation and Collateral Issues - lines [756, 797]
- [ ] `tokens-erc721-nft-vulnerabilities-8-self-transfer-edge-cases-011` (7/21) 8. Self-Transfer Edge Cases - lines [798, 849]

Progress: 9/11 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/BURVE_UNRESTRICTED_CALLBACK.md`

- [ ] `unique-burve-unrestricted-callback-keywords-005` (6/21) Keywords - lines [198, 221]
- [ ] `unique-burve-unrestricted-callback-vulnerable-code-pattern-001` (6/21) Vulnerable Code Pattern - lines [111, 128]

Progress: 0/2 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/LAMBO_DETERMINISTIC_ADDRESS_DOS.md`

- [ ] `unique-lambo-deterministic-address-dos-keywords-009` (6/21) Keywords - lines [250, 273]

Progress: 0/1 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/SENTIMENT_CURVE_READONLY_REENTRANCY.md`

- [ ] `unique-sentiment-curve-readonly-reentrancy-keywords-009` (6/21) Keywords - lines [309, 332]
- [ ] `unique-sentiment-curve-readonly-reentrancy-vulnerable-code-pattern-003` (6/21) Vulnerable Code Pattern - lines [133, 169]

Progress: 0/2 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/SPARTAN_DIVIDEND_GAMING.md`

- [ ] `unique-spartan-dividend-gaming-keywords-007` (6/21) Keywords - lines [219, 242]

Progress: 0/1 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/SPARTAN_LP_BURN_HIJACK.md`

- [ ] `unique-spartan-lp-burn-hijack-keywords-008` (6/21) Keywords - lines [306, 329]
- [ ] `unique-spartan-lp-burn-hijack-vulnerable-code-pattern-002` (6/21) Vulnerable Code Pattern - lines [119, 162]

Progress: 0/2 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/STAKEHOUSE_REENTRANCY_FUND_FREEZE.md`

- [ ] `unique-stakehouse-reentrancy-fund-freeze-keywords-010` (6/21) Keywords - lines [324, 347]
- [ ] `unique-stakehouse-reentrancy-fund-freeze-state-machine-corruption-flow-005` (6/21) State Machine Corruption Flow - lines [211, 239]

Progress: 0/2 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/TRADERJOE_FEE_DEBT_THEFT.md`

- [ ] `unique-traderjoe-fee-debt-theft-keywords-008` (6/21) Keywords - lines [294, 317]

Progress: 0/1 cards source-enriched for this file.

### `DB/unique/amm/constantproduct/VADER_IL_PROTECTION_DRAIN.md`

- [ ] `unique-vader-il-protection-drain-keywords-008` (6/21) Keywords - lines [282, 305]

Progress: 0/1 cards source-enriched for this file.

### `DB/unique/defihacklabs/compiler-level-vulnerabilities.md`

- [ ] `unique-compiler-level-vulnerabilities-compiler-level-vulnerability-p-000` (12/21) Compiler-Level Vulnerability Patterns - lines [56, 136]

Progress: 0/1 cards source-enriched for this file.

### `DB/unique/defihacklabs/defihacklabs-novel-attack-patterns-2025-2026.md`

- [ ] `unique-defihacklabs-novel-attack-patterns-2025--1-transient-storage-eip-1153-a-001` (9/21) 1. Transient Storage (EIP-1153) Authorization Bypass via CREATE2 - lines [125, 201]
- [ ] `unique-defihacklabs-novel-attack-patterns-2025--2-fee-on-transfer-token-overch-002` (9/21) 2. Fee-On-Transfer Token Overcharge + AMM Sync Drain - lines [202, 265]
- [ ] `unique-defihacklabs-novel-attack-patterns-2025--3-staking-reward-farming-via-c-003` (9/21) 3. Staking Reward Farming via CREATE2 Identity Rotation - lines [266, 337]
- [ ] `unique-defihacklabs-novel-attack-patterns-2025--4-batch-array-refund-multiplic-004` (9/21) 4. Batch Array Refund Multiplication - lines [338, 405]
- [ ] `unique-defihacklabs-novel-attack-patterns-2025--5-bonding-curve-arithmetic-ove-005` (9/21) 5. Bonding Curve Arithmetic Overflow in Price Calculation - lines [406, 478]
- [ ] `unique-defihacklabs-novel-attack-patterns-2025--6-fee-unit-mismatch-between-sy-006` (7/21) 6. Fee Unit Mismatch Between Systems - lines [479, 543]
- [ ] `unique-defihacklabs-novel-attack-patterns-2025--7-permissionless-aum-oracle-ma-007` (9/21) 7. Permissionless AUM Oracle Manipulation - lines [544, 611]

Progress: 0/7 cards source-enriched for this file.

### `DB/unique/erc4626/CONVERTTOSHARES_MANIPULATION_DOS.md`

- [ ] `unique-converttoshares-manipulation-dos-converttoshares-manipulation-b-000` (12/21) ConvertToShares Manipulation: Blocking Deposits via Direct Token Transfers - lines [73, 399]

Progress: 0/1 cards source-enriched for this file.

### `DB/unique/erc4626/CROSS_CONTRACT_REENTRANCY_YIELD_TOKEN_THEFT.md`

- [ ] `unique-cross-contract-reentrancy-yield-token-th-cross-contract-reentrancy-allo-000` (14/21) Cross-Contract Reentrancy Allows YIELD_TOKEN Theft in Multi-Vault ERC4626 Systems - lines [70, 392]

Progress: 0/1 cards source-enriched for this file.

### `DB/unique/erc4626/FLASH_LOAN_VAULT_DEFLATION_ATTACK.md`

- [x] `unique-flash-loan-vault-deflation-attack-flash-loan-vault-deflation-att-000` (15/21) Flash Loan Vault Deflation Attack: Draining Accumulated Yield via Share Price Reset - lines [75, 509]

Progress: 1/1 cards source-enriched for this file.

### `DB/zk-rollup/batch-processing.md`

- [ ] `zk-rollup-batch-processing-batch-hashing-and-commitment-b-001` (9/21) Batch Hashing and Commitment Bugs - lines [95, 106]
- [ ] `zk-rollup-batch-processing-pattern-1-batcher-frame-decodi-002` (11/21) Pattern 1: Batcher Frame Decoding Inconsistency Causes Consensus Split - lines [161, 203]
- [ ] `zk-rollup-batch-processing-pattern-2-eip-4844-blob-incomp-003` (12/21) Pattern 2: EIP-4844 Blob Incompatibility Halts Block Processing - lines [204, 250]
- [ ] `zk-rollup-batch-processing-pattern-3-rollup-cannot-split--004` (9/21) Pattern 3: Rollup Cannot Split Batches Across Blobs -> Block Stuffing - lines [251, 291]
- [ ] `zk-rollup-batch-processing-pattern-4-malformed-blob-trans-005` (6/21) Pattern 4: Malformed Blob Transaction Crashes Validator Nodes - lines [292, 315]
- [ ] `zk-rollup-batch-processing-pattern-5-memory-corruption-ca-006` (12/21) Pattern 5: Memory Corruption Causing Incorrect Batch Hashes (Scroll) - lines [316, 366]
- [ ] `zk-rollup-batch-processing-pattern-6-incorrect-basefee-ca-007` (8/21) Pattern 6: Incorrect basefee Calculation on Taiko Rollup - lines [367, 394]
- [ ] `zk-rollup-batch-processing-pattern-7-inchallenge-incorrec-008` (12/21) Pattern 7: inChallenge Incorrectly Reset in revertBatch - lines [395, 431]

Progress: 0/8 cards source-enriched for this file.

### `DB/zk-rollup/bridge-vulnerabilities.md`

- [ ] `zk-rollup-bridge-vulnerabilities-message-channel-dos-and-censor-003` (9/21) Message Channel DoS and Censorship - lines [114, 124]
- [ ] `zk-rollup-bridge-vulnerabilities-pattern-1-token-bridge-reentra-005` (11/21) Pattern 1: Token Bridge Reentrancy Corrupts Accounting - lines [189, 246]
- [ ] `zk-rollup-bridge-vulnerabilities-pattern-2-wrong-token-order-in-006` (9/21) Pattern 2: Wrong Token Order in Bridge Causes Incorrect Routing - lines [247, 295]
- [ ] `zk-rollup-bridge-vulnerabilities-pattern-3-router-signatures-re-007` (11/21) Pattern 3: Router Signatures Replay Across Chains - lines [296, 350]
- [ ] `zk-rollup-bridge-vulnerabilities-pattern-4-wrong-erc1155-select-008` (10/21) Pattern 4: Wrong ERC1155 Selector Locks Tokens in Bridge - lines [351, 390]
- [ ] `zk-rollup-bridge-vulnerabilities-pattern-5-usdc-blacklist-perma-009` (11/21) Pattern 5: USDC Blacklist Permanently Locks Bridge Funds - lines [391, 440]
- [ ] `zk-rollup-bridge-vulnerabilities-pattern-6-single-reverting-wit-010` (11/21) Pattern 6: Single Reverting Withdrawal Blocks Entire Queue - lines [441, 482]
- [ ] `zk-rollup-bridge-vulnerabilities-token-accounting-and-token-map-000` (9/21) Token Accounting and Token Mapping Errors - lines [86, 97]

Progress: 0/8 cards source-enriched for this file.

### `DB/zk-rollup/circuit-constraints.md`

- [ ] `zk-rollup-circuit-constraints-missing-pil-air-constraints-000` (9/21) Missing PIL / AIR Constraints - lines [83, 92]
- [ ] `zk-rollup-circuit-constraints-pattern-1-missing-pil-constrai-004` (12/21) Pattern 1: Missing PIL Constraint for SMT Inclusion - lines [175, 208]
- [ ] `zk-rollup-circuit-constraints-pattern-2-underconstrained-car-005` (8/21) Pattern 2: Underconstrained Carry Value in Binary State Machine - lines [209, 240]
- [ ] `zk-rollup-circuit-constraints-pattern-3-missing-range-constr-006` (10/21) Pattern 3: Missing Range Constraint on Division Remainder (zkEVM Opcode) - lines [241, 292]
- [ ] `zk-rollup-circuit-constraints-pattern-4-isltarraysubair-soun-007` (10/21) Pattern 4: IsLtArraySubAir Soundness Issue (RISC-V Circuit) - lines [293, 324]
- [ ] `zk-rollup-circuit-constraints-pattern-5-sha256-air-unconstra-008` (9/21) Pattern 5: SHA256 AIR Unconstrained final_hash at Last Block - lines [325, 353]
- [ ] `zk-rollup-circuit-constraints-pattern-6-partial-sha256-var-i-009` (8/21) Pattern 6: partial_sha256_var_interstitial Hash Collision (Undersized Input) - lines [354, 377]
- [ ] `zk-rollup-circuit-constraints-pattern-7-jalr-imm-sign-uncons-010` (11/21) Pattern 7: JALR imm_sign Unconstrained (RISC-V zkVM) - lines [378, 404]

Progress: 0/8 cards source-enriched for this file.

### `DB/zk-rollup/evm-incompatibilities.md`

- [ ] `zk-rollup-evm-incompatibilities-bytecode-compression-004` (6/21) Bytecode Compression - lines [129, 138]
- [ ] `zk-rollup-evm-incompatibilities-create-create2-create3-incompa-000` (9/21) CREATE / CREATE2 / CREATE3 Incompatibilities - lines [87, 97]
- [ ] `zk-rollup-evm-incompatibilities-msg-sender-and-context-differe-003` (9/21) msg.sender and Context Differences - lines [119, 128]
- [ ] `zk-rollup-evm-incompatibilities-opcode-and-precompile-divergen-001` (9/21) Opcode and Precompile Divergences - lines [98, 109]
- [ ] `zk-rollup-evm-incompatibilities-pattern-1-create2-address-deri-005` (9/21) Pattern 1: CREATE2 Address Derivation Differs on ZKSync - lines [192, 241]
- [ ] `zk-rollup-evm-incompatibilities-pattern-2-ecrecover-discrepanc-006` (11/21) Pattern 2: ecrecover Discrepancy in delegatecall Context on ZKSync - lines [242, 286]
- [ ] `zk-rollup-evm-incompatibilities-pattern-3-unauthorized-precomp-007` (8/21) Pattern 3: Unauthorized Precompile Authorization Bypass via delegatecall - lines [287, 312]
- [ ] `zk-rollup-evm-incompatibilities-pattern-4-nonce-doesn-t-increm-008` (8/21) Pattern 4: Nonce Doesn't Increment for Reverted Child Deployments - lines [313, 340]
- [ ] `zk-rollup-evm-incompatibilities-pattern-5-block-number-returns-009` (11/21) Pattern 5: block.number Returns L1 Block Number on Arbitrum (Not L2) - lines [341, 385]

Progress: 0/9 cards source-enriched for this file.

### `DB/zk-rollup/fraud-proofs.md`

- [ ] `zk-rollup-fraud-proofs-dispute-game-manipulation-000` (9/21) Dispute Game Manipulation - lines [86, 96]
- [ ] `zk-rollup-fraud-proofs-pattern-1-attacker-freezes-cha-002` (10/21) Pattern 1: Attacker Freezes Chain via Fake prevStateRoot - lines [165, 218]
- [ ] `zk-rollup-fraud-proofs-pattern-2-challenger-misses-di-003` (8/21) Pattern 2: Challenger Misses Discrepancy Events -> Malicious Execution - lines [219, 253]
- [ ] `zk-rollup-fraud-proofs-pattern-3-opfaultverifier-inge-004` (11/21) Pattern 3: opFaultVerifier Ingests Games That Resolve Incorrectly - lines [254, 301]
- [ ] `zk-rollup-fraud-proofs-pattern-4-mips-vm-panic-causes-005` (12/21) Pattern 4: MIPS VM Panic Causes Unchallengeable Output Root - lines [302, 343]
- [ ] `zk-rollup-fraud-proofs-pattern-5-bond-slashed-for-cor-006` (6/21) Pattern 5: Bond Slashed for Correct/Honest Assertion - lines [344, 369]
- [ ] `zk-rollup-fraud-proofs-pattern-6-batches-committed-du-007` (8/21) Pattern 6: Batches Committed During Challenge Avoid Being Challenged - lines [370, 399]
- [ ] `zk-rollup-fraud-proofs-state-root-and-batch-challenge-001` (9/21) State Root and Batch Challenge Issues - lines [97, 110]

Progress: 0/8 cards source-enriched for this file.

### `DB/zk-rollup/gas-accounting.md`

- [ ] `zk-rollup-gas-accounting-fee-theft-and-manipulation-001` (9/21) Fee Theft and Manipulation - lines [96, 108]
- [ ] `zk-rollup-gas-accounting-gas-calculation-errors-000` (9/21) Gas Calculation Errors - lines [86, 95]
- [ ] `zk-rollup-gas-accounting-pattern-1-paymaster-refunds-sp-002` (12/21) Pattern 1: Paymaster Refunds spentOnPubdata Instead of Burning - lines [163, 195]
- [ ] `zk-rollup-gas-accounting-pattern-2-operator-steals-all--003` (10/21) Pattern 2: Operator Steals All Gas Provided for L1->L2 Transactions - lines [196, 238]
- [ ] `zk-rollup-gas-accounting-pattern-3-gas-calculation-uses-004` (8/21) Pattern 3: Gas Calculation Uses Unchecked Free Variables - lines [239, 265]
- [ ] `zk-rollup-gas-accounting-pattern-4-burning-user-gas-in--005` (8/21) Pattern 4: Burning User Gas in sendCompressedBytecode - lines [266, 289]
- [ ] `zk-rollup-gas-accounting-pattern-5-incorrect-commitscal-006` (10/21) Pattern 5: Incorrect commitScalar Underpays Sequencer - lines [290, 326]
- [ ] `zk-rollup-gas-accounting-pattern-6-batch-fees-multiplie-007` (9/21) Pattern 6: Batch Fees Multiplier Cap Bypassed with Multiple Calls - lines [327, 368]
- [ ] `zk-rollup-gas-accounting-pattern-7-bytecode-compression-008` (8/21) Pattern 7: Bytecode Compression Bypass Completeness Checks - lines [369, 395]

Progress: 0/9 cards source-enriched for this file.

### `DB/zk-rollup/l1-l2-messaging.md`

- [ ] `zk-rollup-l1-l2-messaging-l1-l2-transaction-failures-000` (9/21) L1 -> L2 Transaction Failures - lines [86, 96]
- [ ] `zk-rollup-l1-l2-messaging-l2-l1-withdrawal-issues-003` (9/21) L2 -> L1 Withdrawal Issues - lines [111, 126]
- [ ] `zk-rollup-l1-l2-messaging-pattern-1-loss-of-funds-when-l-004` (9/21) Pattern 1: Loss of Funds When L1->L2 Transaction Fails in Bootloader - lines [181, 232]
- [ ] `zk-rollup-l1-l2-messaging-pattern-2-msgvaluesimulator-no-005` (8/21) Pattern 2: MsgValueSimulator Non-Zero Value Calls Sender Itself - lines [233, 262]
- [ ] `zk-rollup-l1-l2-messaging-pattern-3-address-aliasing-loc-006` (11/21) Pattern 3: Address Aliasing Locks ETH - lines [263, 311]
- [ ] `zk-rollup-l1-l2-messaging-pattern-4-attacker-fills-l2tol-007` (8/21) Pattern 4: Attacker Fills L2ToL1MessagePasser Merkle Tree - lines [312, 338]
- [ ] `zk-rollup-l1-l2-messaging-pattern-5-paymaster-refunds-sp-008` (12/21) Pattern 5: Paymaster Refunds spentOnPubdata to User - lines [339, 380]
- [ ] `zk-rollup-l1-l2-messaging-pattern-6-crossdomainmessenger-009` (6/21) Pattern 6: CrossDomainMessenger Cannot Guarantee Replayability - lines [381, 411]

Progress: 0/8 cards source-enriched for this file.

### `DB/zk-rollup/proof-verification.md`

- [ ] `zk-rollup-proof-verification-cryptographic-weaknesses-in-pr-001` (9/21) Cryptographic Weaknesses in Proof Systems - lines [86, 98]
- [ ] `zk-rollup-proof-verification-pattern-1-missing-on-chain-zk--002` (9/21) Pattern 1: Missing On-Chain ZK Proof Verification - lines [154, 195]
- [ ] `zk-rollup-proof-verification-pattern-2-incorrect-randomness-003` (11/21) Pattern 2: Incorrect Randomness Computation Allows Proof Forgery - lines [196, 247]
- [ ] `zk-rollup-proof-verification-pattern-3-plonk-groth16-verifi-004` (10/21) Pattern 3: Plonk/Groth16 Verifiers Accept Untrusted Recursion VK Root - lines [248, 289]
- [ ] `zk-rollup-proof-verification-pattern-4-weak-fiat-shamir-in--005` (8/21) Pattern 4: Weak Fiat-Shamir in LogUp Phase Enables Backdoored Circuits - lines [290, 313]
- [ ] `zk-rollup-proof-verification-pattern-5-verifier-side-dos-vi-006` (12/21) Pattern 5: Verifier-Side DoS via Unbounded Public Inputs - lines [314, 347]
- [ ] `zk-rollup-proof-verification-pattern-6-malicious-verifier-r-007` (8/21) Pattern 6: Malicious Verifier Recovers Private Witness Values - lines [348, 374]

Progress: 0/7 cards source-enriched for this file.

### `DB/zk-rollup/reorg-attacks.md`

- [ ] `zk-rollup-reorg-attacks-factory-reorg-attacks-000` (9/21) Factory Reorg Attacks - lines [85, 95]
- [ ] `zk-rollup-reorg-attacks-pattern-1-questfactory-reorg-a-002` (10/21) Pattern 1: questFactory Reorg Attack - lines [165, 220]
- [ ] `zk-rollup-reorg-attacks-pattern-2-stealing-liquidity-p-003` (8/21) Pattern 2: Stealing Liquidity Pool Funds via Reorg - lines [221, 277]
- [ ] `zk-rollup-reorg-attacks-pattern-3-general-factory-crea-004` (8/21) Pattern 3: General Factory.create Reorg (Multiple Protocols) - lines [278, 322]
- [ ] `zk-rollup-reorg-attacks-pattern-4-create-vs-create2-re-005` (8/21) Pattern 4: CREATE vs CREATE2 Reorg Risk Comparison - lines [323, 349]

Progress: 0/5 cards source-enriched for this file.

### `DB/zk-rollup/sequencer-issues.md`

- [ ] `zk-rollup-sequencer-issues-pattern-1-access-controlled-fu-003` (9/21) Pattern 1: Access-Controlled Functions Fail During Sequencer Downtime - lines [170, 226]
- [ ] `zk-rollup-sequencer-issues-pattern-2-dutch-auctions-and-o-004` (9/21) Pattern 2: Dutch Auctions and Options Expire at Bad Prices During Downtime - lines [227, 277]
- [ ] `zk-rollup-sequencer-issues-pattern-3-linea-sequencer-cens-005` (9/21) Pattern 3: Linea / Sequencer Censorship Locking User Funds - lines [278, 320]
- [ ] `zk-rollup-sequencer-issues-pattern-4-sequencer-underpaid--006` (11/21) Pattern 4: Sequencer Underpaid Due to Incorrect commitScalar - lines [321, 357]
- [ ] `zk-rollup-sequencer-issues-pattern-5-front-running-finali-007` (12/21) Pattern 5: Front-Running finalizeBlocks in Decentralized Sequencer Mode - lines [358, 401]
- [ ] `zk-rollup-sequencer-issues-protocol-functions-breaking-du-000` (9/21) Protocol Functions Breaking During Sequencer Downtime - lines [83, 93]
- [ ] `zk-rollup-sequencer-issues-sequencer-economic-issues-002` (9/21) Sequencer Economic Issues - lines [103, 115]

Progress: 0/7 cards source-enriched for this file.
