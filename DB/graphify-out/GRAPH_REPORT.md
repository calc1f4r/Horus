# Graph Report - DB  (2026-09-15)

## Corpus Check
- 297 files · ~274,766 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5843 nodes · 63963 edges · 163 communities (141 shown, 22 thin omitted)
- Extraction: 27% EXTRACTED · 73% INFERRED · 0% AMBIGUOUS · INFERRED: 46996 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- access-control
- general
- defi
- cosmos
- zk-rollup
- zk-rollup 2
- defi 2
- governance
- defi 3
- eth-l1
- bridge
- general 2
- cosmos 2
- cosmos 3
- cosmos 4
- cosmos 5
- amm
- cosmos 6
- proxy
- cosmos 7
- access-control 2
- zk-rollup 3
- defi 4
- cosmos 8
- substrate
- access-control 3
- defi 5
- zk-rollup 4
- eth-l1 2
- cosmos 9
- bridge 2
- defi 6
- defi 7
- defi 8
- defi 9
- oracle
- proxy 2
- cosmos 10
- protocol-specific
- cosmos 11
- lending
- token
- general 3
- cosmos 12
- oracle 2
- account-abstraction
- solana
- general 4
- substrate 2
- cosmos 13
- oracle 3
- cosmos 14
- substrate 3
- zk-rollup 5
- amm 2
- general 5
- cosmos 15
- general 6
- cosmos 16
- defi 10
- cosmos 17
- cosmos 18
- cosmos 19
- governance 2
- general 7
- amm 3
- bnb
- eth-l1 3
- bnb 2
- proxy 3
- eth-l1 4
- defi 11
- cosmos 20
- protocol-specific 2
- oracle 4
- proxy 4
- protocol-specific 3
- eth-l1 5
- protocol-specific 4
- protocol-specific 5
- protocol-specific 6
- protocol-specific 7
- protocol-specific 8
- protocol-specific 9
- lending 2
- protocol-specific 10
- defi 12
- protocol-specific 11
- oracle 5
- protocol-specific 12
- general 8
- cosmos 21
- bnb 3
- general 9
- cosmos 22
- lending 3
- bnb 4
- lending 4
- cosmos 23
- account-abstraction 2
- lending 5
- cosmos 24
- general 10
- lending 6
- general 11
- DB Community 105
- general 12
- protocol-specific 13
- protocol-specific 14
- protocol-specific 15
- cosmos 25
- protocol-specific 16
- lending 7
- DB Community 113
- protocol-specific 17
- general 13
- protocol-specific 18
- cosmos 26
- general 14
- general 15
- protocol-specific 19
- protocol-specific 20
- DB Community 122
- general 16
- protocol-specific 21
- DB Community 125
- cosmos 27
- general 17
- DB Community 128
- account-abstraction 3
- general 18
- protocol-specific 22
- protocol-specific 23
- protocol-specific 24
- general 19
- protocol-specific 25
- protocol-specific 26
- protocol-specific 27
- protocol-specific 28
- general 20
- protocol-specific 29
- DB Community 141
- DB Community 142
- DB Community 143
- DB Community 144
- DB Community 145
- DB Community 146
- DB Community 147
- DB Community 148
- DB Community 149
- DB Community 150
- DB Community 151
- DB Community 152
- DB Community 153
- DB Community 154
- DB Community 155
- DB Community 156
- DB Community 157
- DB Community 158
- DB Community 159
- DB Community 160
- DB Community 161
- DB Community 162

## God Nodes (most connected - your core abstractions)
1. `data_manipulation` - 334 edges
2. `arithmetic_error` - 320 edges
3. `reentrancy` - 262 edges
4. `state_manipulation` - 244 edges
5. `missing_access_control` - 228 edges
6. `missing access control` - 228 edges
7. `callback_reentrancy` - 222 edges
8. `reports/ottersec_move_audits/markdown/aftermath_marketmaking_v2_audit_final.md` - 194 edges
9. `access_control` - 160 edges
10. `fund_theft` - 152 edges
11. `staking` - 146 edges
12. `liquidity_pool` - 140 edges
13. `price_feed` - 138 edges
14. `_checkOnERC721Received` - 130 edges
15. `Slashing Evasion & Frontrunning Vulnerabilities [HIGH]` - 127 edges

## Surprising Connections (you probably didn't know these)
- `processWithdrawals` --keyword_expands_to_card--> `6. LP Vault Exploitation`  [INFERRED]
  DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md → DB/general/perpetuals-derivatives/PERPETUALS_DERIVATIVES_VULNERABILITIES.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 1: TWAP Oracle with Proper Configuration`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/price-oracle-manipulation.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 2: Dual Price Validation`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/price-oracle-manipulation.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 3: sqrtPrice-Based Tick Derivation`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/price-oracle-manipulation.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 4: Initialized Observation Check`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/price-oracle-manipulation.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Keywords`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 1: Proper Tick Validation`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 2: Fee Growth with unchecked{}`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 3: Correct TWAP Tick Calculation`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md
- `Secure Pattern 1: Atomic Liquidity Verification` --related_variant--> `Secure Pattern 4: Bounded Tick Tracking`  [INFERRED]
  DB/amm/concentrated-liquidity/liquidity-management-vulnerabilities.md → DB/amm/concentrated-liquidity/tick-range-position-vulnerabilities.md

## Communities (163 total, 22 thin omitted)

### Community 0 - "access-control"
Cohesion: 0.15
Nodes (245): access_control, account_validation, admin_functions, authorization_logic, callback_handler, capability_management, cpi, cross_chain_proxy (+237 more)

### Community 1 - "general"
Cohesion: 0.20
Nodes (201): bonding_curve_creation, calculation_logic, entry_points, epoch_management, exchange_rate, fee_computation, fee_logic, freeze_logic (+193 more)

### Community 2 - "defi"
Cohesion: 0.10
Nodes (155): accounting_math, AMM swap and liquidity state transitions (pallet-omnipool, balance/issuance computation paths, batch_transfer, ERC4626_vault, exchange_rate_calculation, liquidity_math, pool_initialization (+147 more)

### Community 3 - "cosmos"
Cohesion: 0.17
Nodes (144): abci_lifecycle_logic, checkpoint_system, consensus_logic, delegation_logic, governance_logic, signature_logic, state_management_logic, voting_system (+136 more)

### Community 4 - "zk-rollup"
Cohesion: 0.17
Nodes (141): adapter, batch_commitment, batch_submission, batcher, blob_submission, bridge_relay, finalization, forced_inclusion (+133 more)

### Community 5 - "zk-rollup 2"
Cohesion: 0.14
Nodes (138): admin_privileges, air_constraints, airdrop_claim, beacon_chain_proofs, binary_state_machine, callback, circuit_constraints, eigenpod (+130 more)

### Community 6 - "defi 2"
Cohesion: 0.12
Nodes (131): bonding_curves, buy_sell_functions, fee_calculation, liquidity_management, liquidity_operations, mev_logic, oracle_logic, precision (+123 more)

### Community 7 - "governance"
Cohesion: 0.14
Nodes (125): amm_liquidity, campaign_lifecycle, delay_enforcement, dynamic_quorum, governance_admin, governance_system, governance_voting, lending_protocol (+117 more)

### Community 8 - "defi 3"
Cohesion: 0.25
Nodes (115): accounting, configuration, coordinator_transaction_validation, delegation_manager, enforcer, events, global_storage, heap (+107 more)

### Community 9 - "eth-l1"
Cohesion: 0.10
Nodes (115): blob_tx_validation, blockchain_tree, bonding_state, discv4_packets, discv5_messages, enr_records, fork_choice, gas_calculation (+107 more)

### Community 10 - "bridge"
Cohesion: 0.23
Nodes (106): external_call_state_accounting, hook_callbacks, lzCompose, lzReceive, _lzSend, NonblockingLzApp, OFT, ONFT (+98 more)

### Community 11 - "general 2"
Cohesion: 0.30
Nodes (99): Bridge, bridge_committee, cctx, coin_type, cross_chain_claim, cross_chain_messaging, evm_state, flow_limiter (+91 more)

### Community 12 - "cosmos 2"
Cohesion: 0.18
Nodes (99): accounting_logic, module_accounting_logic, tokens_logic, 1. Accounting Balance Not Updated [HIGH], 2. Accounting Double Counting, 3. Accounting Tvl Error, 4. Accounting State Corruption, 5. Accounting Missing Deduction (+91 more)

### Community 13 - "cosmos 3"
Cohesion: 0.19
Nodes (97): staking_logic, 1. Staking Deposit Amount Tracking Errors [HIGH], 2. Missing or Insufficient Deposit Validation, 3. Staking Deposit Frontrunning, 4. Staking Balance Desynchronization, 5. Deposit Queue Processing Errors, 6. First Depositor / Share Inflation Attack, 7. Incorrect Staking Calculation Logic (+89 more)

### Community 14 - "cosmos 4"
Cohesion: 0.16
Nodes (95): bridge_logic, dos_logic, 1. Dos Block Production Halt [HIGH], 2. Dos Consensus Halt, 3. Dos State Machine, 4. Dos Unbounded Beginblock, 5. Dos Unbounded Array, 6. Dos Panic Crash (+87 more)

### Community 15 - "cosmos 5"
Cohesion: 0.14
Nodes (92): liquidation_logic, liquidity_logic, vault_logic, 1. Accounting Exchange Rate Manipulation [HIGH], 2. Accounting Exchange Rate Stale, 3. Accounting Exchange Rate Error, 4. Accounting Share Price Inflation, 5. Accounting Conversion Rounding (+84 more)

### Community 16 - "amm"
Cohesion: 0.18
Nodes (93): reserves, swap_router, 10. Decimal & Math Calculation Issues, 11. Liquidity Migration & Protocol Upgrade Attacks, 12. Flash Loan-Based Graduation/Threshold Manipulation, 13. Imbalanced Liquidity Addition Exploitation, 14. Rebasing Token Integration Issues, 15. Impermanent Loss Protection Abuse (+85 more)

### Community 17 - "cosmos 6"
Cohesion: 0.27
Nodes (89): cooldown_mechanism, delay_mechanism, fund_transfer, slashing_logic, withdrawal_queue, 1. Slashing Amount Incorrect [HIGH], 2. Slashing Share Dilution, 3. Slashing Balance Update Error (+81 more)

### Community 18 - "proxy"
Cohesion: 0.23
Nodes (87): proxy_contract_system, proxy_implementation, proxy_storage, implementation_exploit, Vulnerability Title, Pattern 1: Missing disableInitializers in Implementation Constructor [HIGH], Pattern 10: Clone Validation Checking Insufficient Bytes [HIGH], Pattern 11: Metamorphic Implementation Contract Risk [HIGH] (+79 more)

### Community 19 - "cosmos 7"
Cohesion: 0.10
Nodes (74): AMM/DEX modules and pool contracts, CosmWasm smart contracts (ExecuteMsg handlers, extrinsic input validation, fee/incentive distributor modules, IBC module (ics02/ics20/ics26, ICA host/controller, keys/signature verification paths, message handlers with multi-step state writes (+66 more)

### Community 20 - "access-control 2"
Cohesion: 0.02
Nodes (85): access-control, account-abstraction, amm, anchor, appchain, arbitrum, bad-debt, batch-processing (+77 more)

### Community 21 - "zk-rollup 3"
Cohesion: 0.35
Nodes (78): batch_fees, bootloader, bytecode_compression, fee_model, gas_tracking, ISM, l1_l2_bridge, l1_l2_gas (+70 more)

### Community 22 - "defi 4"
Cohesion: 0.46
Nodes (80): liquidity_pool, rewards, share_calculation, staking, vault, data_manipulation, reentrancy, 1. First Depositor / Inflation Attack [CRITICAL] (+72 more)

### Community 23 - "cosmos 8"
Cohesion: 0.28
Nodes (76): fund_safety_logic, 1. Funds Lock Permanent [HIGH], 2. Funds Lock Conditional, 3. Funds Insolvency Protocol, 4. Funds Insolvency Slash, 5. Funds Insolvency Rebase, 6. Funds Bad Debt, 7. Funds Withdrawal Blocked (+68 more)

### Community 24 - "substrate"
Cohesion: 0.07
Nodes (68): fee collection paths, lending pallets and liquidation logic, multi-step extrinsics, pallet loops / weight handling, price_feed (EMA oracle over Omnipool reserves, signature_verification (sr25519_verify, staking_ledger, token/issuance pallet paths (+60 more)

### Community 25 - "access-control 3"
Cohesion: 0.24
Nodes (69): aggregator_proxy, aggregator_router, balancer_pool, bridge_gateway, curve_pool, dex_aggregator_integration, dex_pair, diamond_facet (+61 more)

### Community 26 - "defi 5"
Cohesion: 0.42
Nodes (71): amm_integration, balance_tracking, ccip_router, lending_pool, message_handling, reflection_token_contract, token_transfer, message_manipulation (+63 more)

### Community 27 - "zk-rollup 4"
Cohesion: 0.28
Nodes (70): bytecode_compressor, call indices, create2_deployment, create2_opcode, create_opcode, deployment_addresses, ecrecover_precompile, extcodehash (+62 more)

### Community 28 - "eth-l1 2"
Cohesion: 0.10
Nodes (64): bridge_receipt_queue, connection_setup, gossipsub_topic_params, invalid_message_handling, p2p_request_handlers, peer_management, peer_scoring, rate_limiting (+56 more)

### Community 29 - "cosmos 9"
Cohesion: 0.20
Nodes (64): rewards_logic, 1. Reward Calculation Incorrect [HIGH], 2. Reward Per Share Error, 3. Reward Delayed Balance, 4. Reward Decimal Mismatch, 5. Reward Weight Error, 6. Reward Historical Loss, 7. Reward Pool Share (+56 more)

### Community 30 - "bridge 2"
Cohesion: 0.55
Nodes (63): AxelarExecutable, Client, GasService, Gateway, InterchainTokenService, ITS, OffRamp, OnRamp (+55 more)

### Community 31 - "defi 6"
Cohesion: 0.22
Nodes (63): funding_rate, liquidation_engine, order_execution, position_engine, supply_tracking, tvl_calculation, vault_accounting, donation_attack (+55 more)

### Community 32 - "defi 7"
Cohesion: 0.48
Nodes (59): marketplace_contracts, nft_contracts, multiple, 1. Reentrancy via onERC721Received / safeMint Callbacks, 10. NFT Wrap/Unwrap Airdrop & ID Swap Exploitation, 2. Residual Allowance & Vault Deposit Exploitation, 3. Marketplace Fee Bypass & Royalty Calculation Errors, 4. NFT Rental Griefing via Callback Revert & Blocklist [HIGH] (+51 more)

### Community 33 - "defi 8"
Cohesion: 0.29
Nodes (52): AMM_math, aum_oracle, bonding_curve, claim_function, fee_manager, invariant_calculation, pricing_formula, reward_distributor (+44 more)

### Community 34 - "defi 9"
Cohesion: 0.47
Nodes (52): batch_operations, flash_loan, nft_mint, rebalance, repayment_validation, share_trading, stablecoin, twap (+44 more)

### Community 35 - "oracle"
Cohesion: 0.29
Nodes (51): lending_market, lrt_pricing, price_oracle, rate_provider, slot0_price_feed, stablecoin_mint_redeem, twap_oracle, Secure Pattern 1: TWAP Oracle with Proper Configuration (+43 more)

### Community 36 - "proxy 2"
Cohesion: 0.29
Nodes (46): balancer_lp_oracle, curve_lp_oracle, dex_swap, lending_liquidation, oracle_manipulation, oracle_price_feed, pricing_logic, social_token_trading (+38 more)

### Community 37 - "cosmos 10"
Cohesion: 0.42
Nodes (49): validation_logic, 1. Validation Zero Check Missing [HIGH], 10. Validation Logic Error, 11. Validation Msg Missing, 12. Validation Length Check, 2. Validation Bounds Missing, 3. Validation State Check Missing, 4. Validation Percentage Overflow (+41 more)

### Community 38 - "protocol-specific"
Cohesion: 0.08
Nodes (45): delegation reward claim-window computation, effective-stake checkpoint accounting across delegation/validator exit flows, reward cursor initialization on delegation, boundary condition error, claimable delegation periods, completed periods snapshot, cursor over start boundary, delegation exit claimed through end (+37 more)

### Community 39 - "cosmos 11"
Cohesion: 0.50
Nodes (46): evm_logic, 1. Evm Intrinsic Gas Missing [HIGH], 2. Evm Gas Refund Error, 3. Evm Precompile Gas Hardcode, 4. Evm Gas Not Consumed Error, 5. Evm Gas Mismatch Call, Keywords, 1. Evm Dirty State Precompile [HIGH] (+38 more)

### Community 40 - "lending"
Cohesion: 0.09
Nodes (43): auction start timestamp, bad price input to liquidation, execute liquidation call, incentive design flaw, liquidation_grace_period, liquidation math error, liquidation seizure economics miscalculation, oracle driven liquidation mispricing lending markets (+35 more)

### Community 41 - "token"
Cohesion: 0.32
Nodes (45): approval, balance, decimals, mint_burn, inflation first depositor, adminRecoverStuckFunds, _convertToAssets, reports/erc20_token_findings/1-erc777-re-entrancy-attack.md (+37 more)

### Community 42 - "general 3"
Cohesion: 0.54
Nodes (44): math_operations, price_calculation, reward_calculation, share_accounting, type_casting, reward calculation rounding errors, share asset rounding direction, share price inflation first depositor (+36 more)

### Community 43 - "cosmos 12"
Cohesion: 0.26
Nodes (43): 1. Delegation Self Manipulation [HIGH], 2. Delegation Dos Revert, 3. Delegation State Inconsistency, 4. Delegation To Inactive, 5. Delegation Frontrunning, 6. Delegation Reward Manipulation, 7. Delegation Redelegation Error, 8. Delegation Unbonding Exploit (+35 more)

### Community 44 - "oracle 2"
Cohesion: 0.26
Nodes (43): latest round data, price manipulation front running, AggregatorV3Interface, _compareMinMax, getHistoricalPrice, sequencer_uptime_feed, setFeedHeartbeat, 1. Staleness Vulnerabilities [CRITICAL] (+35 more)

### Community 45 - "account-abstraction"
Cohesion: 0.41
Nodes (41): address_handling, callback_implementation, permit_function, reentrancy_guard, session_key_management, session_key_validation, signature_verification, session_key_abuse (+33 more)

### Community 46 - "solana"
Cohesion: 1.13
Nodes (41): extensions, mint, token_account, default account state, mint close authority, confidential_transfer, default_account_state, group_member_pointer (+33 more)

### Community 47 - "general 4"
Cohesion: 0.75
Nodes (41): flow_tracking, order_book, reward_system, stake_update, tank, unstaking, state_manipulation, exchange rate manipulation low tvl (+33 more)

### Community 48 - "substrate 2"
Cohesion: 0.10
Nodes (38): crowdloan_claim_refund_accounting, GRANDPA justification/finality verification, xcm_config_message_delivery, data_validation_bypass, logic_flaw, child storage kind contributed, commit with duplicates equivocations, contribution not decremented (+30 more)

### Community 49 - "cosmos 13"
Cohesion: 0.32
Nodes (37): hooks_callbacks_logic, ibc_logic, reentrancy_logic, 1. Hooks Before After [MEDIUM], 2. Hooks Reentrancy Via Hook, Keywords, 1. Ibc Channel Verification [HIGH], 2. Ibc Packet Handling (+29 more)

### Community 50 - "oracle 3"
Cohesion: 0.28
Nodes (38): price_feed, state_transition, pull based oracle exploitation, same transaction price manipulation, atomicSwapAndProvide, confidence_interval, _entropyCallback, 1. Staleness Vulnerabilities [CRITICAL] (+30 more)

### Community 51 - "cosmos 14"
Cohesion: 0.67
Nodes (37): access_control_logic, 1. Access Missing Control [HIGH], 10. Access Module Authority, 2. Access Role Assignment, 3. Access Antehandler Bypass, 4. Access Allowlist Bypass, 5. Access Cosmwasm Bypass, 6. Access Amino Signing (+29 more)

### Community 52 - "substrate 3"
Cohesion: 0.12
Nodes (35): agents, BeefyClient, bridge fund custody and message submission (Gateway, extrinsic_origin_validation, governance and administrative origin configuration, access_control_bypass, configuration_error, access control bypass (+27 more)

### Community 53 - "zk-rollup 5"
Cohesion: 0.62
Nodes (37): bisection_protocol, challenge_period, dispute_game, fault_game_factory, l2_output_oracle, mips_vm, output_root, chain_freeze (+29 more)

### Community 54 - "amm 2"
Cohesion: 0.47
Nodes (34): fee_accounting, fee_collection, fee_distribution, liquidity_manager, liquidity_positions, Keywords, Secure Pattern 1: TWAP-Based Fee Value Calculation, Secure Pattern 2: Per-User Fee Tracking (+26 more)

### Community 55 - "general 5"
Cohesion: 0.64
Nodes (35): bigvector, digest, dynamic_fields, kiosk, object_model, uid, verifier, sui move object security (+27 more)

### Community 56 - "cosmos 15"
Cohesion: 0.73
Nodes (32): lifecycle_logic, 1. Lifecycle Upgrade Error [HIGH], 2. Lifecycle Migration Failure, 3. Lifecycle Init Error, 4. Lifecycle Storage Gap, 5. Lifecycle Module Registration, 6. Lifecycle Genesis Error, 7. Lifecycle Deployment Param (+24 more)

### Community 57 - "general 6"
Cohesion: 1.06
Nodes (31): amm_pricing, collateral_valuation, oracle, tick_calculation, liquidation_exploit, faulty constant definition move oracle, incorrect price boundary checks move oracle, move oracle pricing (+23 more)

### Community 58 - "cosmos 16"
Cohesion: 0.59
Nodes (31): node_operator_logic, 1. Minipool Deposit Theft [HIGH], 2. Minipool Cancel Error, 3. Minipool Slash Avoidance, 4. Minipool Finalization, 5. Minipool Replay, 6. Operator Registration Frontrun, 7. Operator Reward Leak (+23 more)

### Community 59 - "defi 10"
Cohesion: 0.76
Nodes (31): swap_liquidity_operations, mev_sandwich_attack, Example 1: Unused Slippage Parameters (HIGH - Vader Protocol) [HIGH], Example 2: Zero Slippage in Swap Operations (MEDIUM - Kaizen) [HIGH], Example 3: Missing Withdrawal Slippage Protection (MEDIUM - Sentiment V2) [HIGH], Example 4: block.timestamp as Deadline (MEDIUM - Particle Protocol) [HIGH], Example 5: Zero Slippage in Leverage Operations (HIGH - Peapods) [HIGH], Fix 1: User-Specified Minimum Output (+23 more)

### Community 60 - "cosmos 17"
Cohesion: 0.79
Nodes (30): infrastructure_logic, 1. Infra Ssrf [HIGH], 2. Infra Private Key, 3. Infra Tss, 4. Infra Keyring, 5. Infra Error Handling, 6. Infra Deprecated Usage, Description (+22 more)

### Community 61 - "cosmos 18"
Cohesion: 0.90
Nodes (29): btc_staking_logic, 1. Btc Staking Tx Validation [HIGH], 2. Btc Unbonding Handling, 3. Btc Delegation Finality, 4. Btc Change Output, 5. Btc Slashable Stake, 6. Btc Covenant Signature, 7. Btc Staking Indexer (+21 more)

### Community 62 - "cosmos 19"
Cohesion: 0.45
Nodes (29): timing_logic, 1. Timing Epoch Snapshot [HIGH], 2. Timing Cooldown Bypass, 3. Timing Timestamp Boundary, 4. Timing Unbonding Change, 5. Timing Epoch Duration Break, 6. Timing Expiration Bypass, 7. Timing Block Time (+21 more)

### Community 63 - "governance 2"
Cohesion: 0.48
Nodes (29): voting_escrow_gauge_bribe_system, Section 1: Bribe Reward Theft & Epoch Accounting Exploits [HIGH], Section 2: Voting Power Manipulation & Lock Accounting Bugs [HIGH], Section 3: Gauge Voting & Emission Distribution Exploits [HIGH], Section 4: Poke Function Exploits [HIGH], Section 5: Boost Mechanism Exploits, Section 6: Reward & Emission Distribution Bugs, Section 7: Checkpoint & Voting Power Decay Bugs (+21 more)

### Community 64 - "general 7"
Cohesion: 0.64
Nodes (27): build_config, dapp_origin, key_derivation, snap_rpc, transaction_rendering, information_disclosure, injection, social_engineering (+19 more)

### Community 65 - "amm 3"
Cohesion: 0.46
Nodes (26): deposit_logic, position_accounting, range_validation, tick_math, withdrawal_logic, Keywords, Secure Pattern 1: Proper Tick Validation, Secure Pattern 2: Fee Growth with unchecked{} (+18 more)

### Community 66 - "bnb"
Cohesion: 0.14
Nodes (26): staking position accounting + multi-token reward accrual, subscription/allocation accounting + liquidity lock flow, Launchpool/Staking-Pool Deposit Validation & Dual-Ledger Sync (BSCStation Start Pools), PinkSale SubscriptionPool: Admin Allocation Rewrite & Token-Compliance Gaps, acc token per share checkpoint, admin state rewrite, arbitrary admin array write (users[], dual ledger without transfer hook (+18 more)

### Community 67 - "eth-l1 3"
Cohesion: 0.43
Nodes (25): fee_caps, intrinsic_gas, nonce_checks, txpool_validation, eip_violation, mempool_dos, spam_tx_acceptance, state_root_divergence (+17 more)

### Community 68 - "bnb 2"
Cohesion: 0.16
Nodes (23): block_processing, consensus_gossip, evm_interpreter, mempool_gossip, p2p_networking, rpc_http_interface, configuration_bypass, Geth-Inherited Audit Findings Relevant to BSC Clients (+15 more)

### Community 69 - "proxy 3"
Cohesion: 0.34
Nodes (22): collateral_accounting, flash_loan_callback, reward_harvest, strategy_callback, 1. Fake Token Reward Harvesting Callback Reentrancy [CRITICAL], 2. Empty Market Phantom Collateral Attack [CRITICAL], 3. ERC-3156 Flash Loan Callback Re-deposit Loop [CRITICAL], 4. Strategy Callback Reentrancy via Attacker-Controlled Hook [CRITICAL] (+14 more)

### Community 70 - "eth-l1 4"
Cohesion: 0.46
Nodes (23): host_allowlist, middleware, rpc_http_server, dns_rebinding, same_origin_bypass, unauthenticated_rpc, Detection & Hunt Strategy, Related files in corpus (L2 geth forks — same class check) (+15 more)

### Community 71 - "defi 11"
Cohesion: 0.56
Nodes (23): interest_rate_calculation, Section 1: Utilization Formula Errors, Section 2: Chain-Specific Constant Errors, Section 3: Utilization Manipulation & Rate Gaming [HIGH], Section 4: Debt Token Scaling & Rate Accounting Errors, Section 5: Rate Model DoS & System Halt, Vulnerability Title, base rate per block (+15 more)

### Community 72 - "cosmos 20"
Cohesion: 0.17
Nodes (21): evidence_pool, fork_accountability, light_block_supervisor, light_client, slashing, consensus_attack, Light-Client / Fork Accountability Vulnerabilities [HIGH], Light-Client Attack Detection Vulnerabilities [CRITICAL] (+13 more)

### Community 73 - "protocol-specific 2"
Cohesion: 0.21
Nodes (18): l1 consensus generic, l1 misc generic, l1 staking generic, l1 consensus generic, l1 misc generic, l1 staking generic, reports/other-l1_findings/audit-reports-animoca-2025-06-24-audit-report-animoca-staking-pool-v1-2-pdf.md, reports/other-l1_findings/audit-reports-dusk-2024-09-20-audit-report-rusk-consensus-pdf.md (+10 more)

### Community 74 - "oracle 4"
Cohesion: 0.74
Nodes (18): automation, functions, keepers, 1. CheckUpkeep/PerformUpkeep Mismatch [MEDIUM], 2. Gas Limit Issues, 3. Unbounded Operations, 4. Callback Safety, 5. Authentication Missing (+10 more)

### Community 75 - "proxy 4"
Cohesion: 1.25
Nodes (18): external_calls, Critical Exploits ($10M+) [CRITICAL], Fix 1: Checks-Effects-Interactions (CEI) Pattern, Fix 2: ReentrancyGuard Modifier, Fix 3: Read-Only Reentrancy Protection (Balancer/Curve), Fix 4: Callback Whitelist / Validation, High-Severity Exploits ($1M-$10M) [CRITICAL], Historical Exploits (2021) [CRITICAL] (+10 more)

### Community 76 - "protocol-specific 3"
Cohesion: 0.20
Nodes (18): native builtin gas accounting during PoA→PoS transition, resource_mispricing, endorsement balance check, env use gas explicit charging, fork conditional code paths (pre post hayabusa), missing sload charge, native builtin gas metering, native is endorsed (+10 more)

### Community 77 - "eth-l1 5"
Cohesion: 0.42
Nodes (17): gossip_decoding, reqresp_encoding, snappy_framing, integrity_check_bypass, resource_waste, spec_divergence, Real Reports, Vulnerable Code Pattern (generic) (+9 more)

### Community 78 - "protocol-specific 4"
Cohesion: 0.22
Nodes (16): vechain consensus nodes, vechain contracts, vechain consensus nodes, accounting, reports/vechain-l1_findings/59316-sc-high-off-by-one-unlocks-infinite-vtho-reward-drain-from-ghost-stakes.md, reports/vechain-l1_findings/59361-sc-high-off-by-one-in-claimabledelegationperiods-allows-claimrewards-to-pay-for-periods-after.md, reports/vechain-l1_findings/59386-sc-high-fund-freeze-from-double-stake-subtraction-when-validator-exits.md, reports/vechain-l1_findings/59615-sc-high-off-by-one-error-in-period-boundary-check-allows-theft-of-unclaimed-yield-after-delega.md (+8 more)

### Community 79 - "protocol-specific 5"
Cohesion: 0.24
Nodes (15): l1 dos generic, l1 math generic, l1 dos generic, l1 math generic, reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-network-omni-portal-security-assessment-report-v2-1-pdf.md, reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-solvernet-security-assessment-report-v2-0-pdf.md, reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-boringdao-1-0-2020-89-pdf.md, reports/other-l1_findings/publications-nimbora-zellic-audit-report-pdf.md (+7 more)

### Community 80 - "protocol-specific 6"
Cohesion: 0.23
Nodes (16): transaction_serialization_and_builder, encoding semantic gap, orchard note construction, serialization ambiguity and version gaps, transparent bundle serialization, tx builder serialization, txid sighash computation, unvalidated bundle fields (+8 more)

### Community 81 - "protocol-specific 7"
Cohesion: 0.23
Nodes (16): validator_commission_and_reward_settlement, ceil vs floor division in segment settlement, commission rate change, commission rate checkpoints per validator, get effective commission rate at fallback to current commission, missing commission checkpoint, reward per token cumulative indices, reward per token settlement (+8 more)

### Community 82 - "protocol-specific 8"
Cohesion: 0.24
Nodes (15): batched_yield_distribution, batched yield distribution, effective total supply recomputed per batch, enumerable set holders array with swap and pop removal, integer division remainder handling, inter batch transfer, live balance of reads per batch, missing balance snapshot (+7 more)

### Community 83 - "protocol-specific 9"
Cohesion: 0.58
Nodes (15): liquidity_token, 1. First Depositor / Inflation Attacks [CRITICAL], 13. Detection Patterns & Audit Checklist, 29. Detection Patterns & Audit Checklist, pool_hijack, calc liquidity units, first depositor inflation, reports/constantproduct/c-03-blocking-the-initial-liquidity-seed-with-a-1-wei-donation.md (+7 more)

### Community 84 - "lending 2"
Cohesion: 0.26
Nodes (14): collateral_ledger, col pools array, collateral accounting error, collateral value inflation double counting, double entrypoint token, effective collateral value, zero amount deposit, Collateral Value Inflation and Double-Counting (+6 more)

### Community 85 - "protocol-specific 10"
Cohesion: 0.27
Nodes (13): l1 bridge generic, near novel, l1 bridge generic, reports/other-l1_findings/audit-reports-brz-audit-report-brz-bridge-pdf.md, reports/other-l1_findings/audit-reports-router-2024-04-30-audit-report-router-asset-bridge-v1-2-pdf.md, reports/other-l1_findings/audit-reports-router-2024-05-29-audit-report-router-evm-and-near-gateway-contracts-and-wasm-bindings-v1-0-pdf.md, reports/other-l1_findings/audits-avalaunch-2021-11-allocationstaking-cooldown-feature-pdf.md, reports/other-l1_findings/public-audits-reports-omni-network-sigma-prime-omni-network-omni-chain-2-security-assessment-report-v2-1-pdf.md (+5 more)

### Community 86 - "defi 12"
Cohesion: 0.89
Nodes (13): callback_validation, collateral_calculation, flash_loan_mechanism, Fix 1: Validate Flash Loan Initiator, Fix 2: Reentrancy Guards on Callbacks, Fix 3: Governance Voting Timelock, Fix 4: Prevent Reinitialization, Fix 5: Snapshot-Based Airdrop Claims (+5 more)

### Community 87 - "protocol-specific 11"
Cohesion: 0.27
Nodes (13): executor_fee_distribution, agent front runs executor, call with gas cap, collateral reservation fee distribution, execute minting executor fee payout, executor fee nat gwei, gas capped nat transfer, hardcoded gas allowance (+5 more)

### Community 88 - "oracle 5"
Cohesion: 0.88
Nodes (13): oracle_integration, amm spot price, curve pool price, faulty chainlink oracle price feed, flash loan manipulation, s pmm oracle, self referencing oracle manipulation, 1. Curve Pool-Based Oracle Manipulation for Lending Liquidation [CRITICAL] (+5 more)

### Community 89 - "protocol-specific 12"
Cohesion: 0.29
Nodes (12): attestation_verification_logic, agent forges check source addresses proof, boolean disjunction validation, check source addresses, degenerate source address proof, flawed boolean validation, minting payment default, referenced payment nonexistence attestation (+4 more)

### Community 90 - "general 8"
Cohesion: 0.29
Nodes (12): block_execution_deserialization, batch write to da, block read back, malformed aptos payload, panic in tokio worker, serde json from slice, reports/movement-l1_findings/42934-bc-high-improper-input-validation-in-keylesssignature-causes-full-node-panic.md, reports/movement-l1_findings/42941-bc-critical-critical-network-wide-denial-of-service-through-unrecoverable-block-execution-fail.md (+4 more)

### Community 91 - "cosmos 21"
Cohesion: 0.29
Nodes (12): escrow, ibc_v2_router, light_client_interface, fund_lock, IBC-v2 / Eureka Client-Status & Router Vulnerabilities [HIGH], client status active frozen expired, consensus state storage keying, membership not frozen (+4 more)

### Community 92 - "bnb 3"
Cohesion: 0.29
Nodes (12): exchange-rate conversion between BNB and BnbX shares, BnbX Liquid-Staking Share Accounting (Stader StakeManager), operator adjustable pool total (total redelegated), operator reward bump, oracleless share minting with unsynced pool totals, reentrancy resistant local caching (bnb xto burn copied before burn), share price as total pooled bnb over total supply, stale pool total (+4 more)

### Community 93 - "general 9"
Cohesion: 0.29
Nodes (12): grpc_server_connection_handling, file descriptor limit, grpc service 0 0 0 0, max frame size, missing tcp timeout, reports/movement-l1_findings/43177-bc-critical-dos-vulnerability-in-da-light-node-via-unbounded-height-parameter.md, reports/movement-l1_findings/43244-bc-critical-lack-of-tcp-timeout-allows-attacker-to-crash-the-sequencer-via-the-light-node-serv.md, reports/movement-l1_findings/43246-bc-critical-lack-of-tcp-timeout-allows-attacker-to-crash-the-sequencer-via-the-maptos-opt-exec.md (+4 more)

### Community 94 - "cosmos 22"
Cohesion: 0.29
Nodes (12): ica_controller, ica_host, packet_execution, Interchain Accounts Host/Controller Control Vulnerabilities [HIGH], amino codec deserialization, controller packet creation, host execute tx, ica host controller (+4 more)

### Community 95 - "lending 3"
Cohesion: 0.29
Nodes (12): interest_accrual, accrual ordering bug, borrow repay liquidate withdraw, cumulative interest rate, stale index accounting, Missing Interest Accrual and Stale Index Accounting, reports/lending_borrowing_findings/h-01-borrow-must-accrueinterest-first.md, reports/lending_borrowing_findings/h-02-lendingpairliquidateaccount-does-not-accrue-and-update-cumulativeinterestra.md (+4 more)

### Community 96 - "bnb 4"
Cohesion: 0.29
Nodes (12): redemption/claim pipeline, stkBNB Redemption/Claim Accounting (Persistence StakePool), claim reserve ledger, contract balance vs claim reserve, selfdestruct with native balance, swap delete claim array, transfer 2300 gas stipend, uint256 to int256 cast (+4 more)

### Community 97 - "lending 4"
Cohesion: 0.29
Nodes (12): risk_engine, borrow or withdraw, health factor computation error, user collateral ratio mantissa, wrong collateralization math, Health Factor and Collateral Ratio Miscalculation, reports/lending_borrowing_findings/account-health-calculations-ignore-token-decimals.md, reports/lending_borrowing_findings/h-04-incorrect-solvency-check-because-it-multiplies-collateralizationrate-by-sha.md (+4 more)

### Community 98 - "cosmos 23"
Cohesion: 0.29
Nodes (12): wasm_light_client, wasmvm_boundary, WASM Light-Client (08-wasm) Validation Vulnerabilities [HIGH], 08 wasm client, client status transition, consensus state store, governance code approval, vm sandbox parameters (+4 more)

### Community 99 - "account-abstraction 2"
Cohesion: 0.32
Nodes (11): AA Paymaster Gas Accounting — Prefund Errors, Duplicate Snapshots, Stake Bypass, and Fee Escape [HIGH], paymaster_gas_validation, gas accounting error, paymaster gas validation, validate paymaster user op, verification gas limit, reports/account_abstraction_findings/h01-incorrect-prefund-calculation-core.md, reports/account_abstraction_findings/h02-duplicate-validation-gas-accounting-core.md (+3 more)

### Community 100 - "lending 5"
Cohesion: 0.32
Nodes (11): cap_validation, deposit or borrow, incomplete cap validation, wrong cap check, Supply / Borrow Cap Enforcement Bypass, reports/lending_borrowing_findings/funds-can-be-redirected-to-the-idle-market-by-reaching-the-metamorpho-supply-cap.md, reports/lending_borrowing_findings/improper-supply-cap-limitation-enforcement.md, reports/lending_borrowing_findings/m-03-bypassing-collateral-cap-check.md (+3 more)

### Community 101 - "cosmos 24"
Cohesion: 0.32
Nodes (11): da_inclusion_proofs, data_availability, Celestia NMT Inclusion-Proof Validation Vulnerabilities [HIGH], ignore max namespace option, inclusion proof verification, min ns max ns computation, namespace range proof, namespaced merkle tree (+3 more)

### Community 102 - "general 10"
Cohesion: 0.32
Nodes (11): da_light_node_rpc, resource_abuse, 0 0 0 0 bind, da light node batch write rpc, light node service, operator tia drain, stream write blob, unauthenticated grpc call (+3 more)

### Community 103 - "lending 6"
Cohesion: 0.32
Nodes (11): debt_share_accounting, debt shares rounding, dust rounding breakage loan closure liquidation, repay exceeds debt, Dust and Rounding Breakage of Loan Closure and Liquidation, reports/lending_borrowing_findings/allowing-the-creation-of-dust-cdps-could-lead-redeemersliquidators-to-be-not-pro.md, reports/lending_borrowing_findings/bigger-precision-loss-in-tokenamount-to-usd-conversion-will-lead-incorrect-liqui.md, reports/lending_borrowing_findings/h-1-fee-precision-loss-disrupts-liquidations-and-causes-loss-of-funds.md (+3 more)

### Community 104 - "general 11"
Cohesion: 0.32
Nodes (11): mempool_sequence_number_validation, mempool status code, missing zero sequence handling, sentinel value conflation, unwrap or default sentinel, used sequence number pool, reports/movement-l1_findings/42896-bc-high-attackers-can-exploit-sequence-number-tolerance-mechanism-to-to-cause-movement-network.md, reports/movement-l1_findings/42991-bc-high-user-can-reuse-sequence-number-causing-dos-and-breaking-core-invariant.md (+3 more)

### Community 105 - "DB Community 105"
Cohesion: 0.27
Nodes (12): amm, general-defi, lending, oracle, tokens, unique, dex_amm, lending_protocol (+4 more)

### Community 106 - "general 12"
Cohesion: 0.35
Nodes (10): block_ordering_execution, build next block, stream read from height, trusted external ordering, unverified external ordering, reports/movement-l1_findings/42298-bc-critical-blocks-from-celestia-are-not-executed-in-order-which-breaks-sequencer-logic-and-ap.md, reports/movement-l1_findings/42749-bc-critical-attacker-can-send-digests-directly-to-celestia-to-reorder-block-execution.md, reports/movement-l1_findings/43108-bc-critical-attackers-can-front-run-transactions-in-celestia-mempool-to-cause-transactions-of.md (+2 more)

### Community 107 - "protocol-specific 13"
Cohesion: 0.35
Nodes (10): consensus_boundary_validation, bor consensus bridging, sprint (producer rotation), state receiver state sync, unchecked milestone and span data, validator set changes, reports/other-l1_findings/bor-audit-audit-feature-milestones-pdf.md, reports/other-l1_findings/bor-claude-rules-consensus-security-md.md (+2 more)

### Community 108 - "protocol-specific 14"
Cohesion: 0.35
Nodes (10): delegation withdrawal path (staking exit edge case, aggregation pending reset on exit, consensus houskeeping hook, delegation added in validator exit period, incorrect state transition, period iteration accounting, unchecked pending subtraction, reports/vechain-l1_findings/55632-bc-critical-delegation-submitted-in-the-same-period-before-a-validator-exit-will-be-permanentl.md (+2 more)

### Community 109 - "protocol-specific 15"
Cohesion: 0.35
Nodes (10): move virtual machine, formal verification (boogie), missing_bounds_invariant, monomorphization code injection (prover pipeline), native function assumptions, vm_safety_invariants, reports/other-l1_findings/aptos-core-third-party-move-mono-move-docs-vm-security-and-correctness-md.md, reports/other-l1_findings/aptos-core-third-party-move-move-prover-doc-report-main-impl-pdf.md (+2 more)

### Community 110 - "cosmos 25"
Cohesion: 0.35
Nodes (10): proposer_selection, validator_set_composition, dYdX Proposer-Set Correctness Vulnerabilities [HIGH], cometbft fault assumption, msg set proposers, no correct proposer scenario, proposer selection updates, voting power bound (+2 more)

### Community 111 - "protocol-specific 16"
Cohesion: 0.35
Nodes (10): signer_message_validation, acknowledgment (ack) status machine, nonce-based replay prevention, reward distribution to signers, signer rotation signer set updates, signer votes (approve reject), stacks signer vote replay status confusion, reports/other-l1_findings/audits-stacks-coinfabrik-stacks-signer-audit-2025-04-pdf.md (+2 more)

### Community 112 - "lending 7"
Cohesion: 0.35
Nodes (10): solvency_accounting, missing bad debt settlement, unhandled bad debt, Bad Debt Socialization and Missing Write-Off, reports/lending_borrowing_findings/bad-debt-redistribution-not-happening-between-liquidations-in-batch-mode.md, reports/lending_borrowing_findings/collateral-can-be-withdrawn-without-repaying-usds-loan.md, reports/lending_borrowing_findings/h-02-liquidate-doesnt-mark-off-bad-debt-leading-to-a-last-lender-to-withdraw-los.md, reports/lending_borrowing_findings/h-05-bad-debt-is-never-handled-which-places-insolvency-risks-on-benddao.md (+2 more)

### Community 113 - "DB Community 113"
Cohesion: 0.22
Nodes (11): bnb-chain, bridge, cosmos, eth-l1-clients, general-infrastructure, zk-rollup, bnb_chain_l1, cosmos_appchain (+3 more)

### Community 114 - "protocol-specific 17"
Cohesion: 0.38
Nodes (9): aptos move core, aptos move core, reports/other-l1_findings/publications-reviews-2025-03-near-one-mpc-chain-signatures-securityreview-pdf.md, reports/other-l1_findings/publications-reviews-2026-02-near-one-robust-ecdsa-securityreview-pdf.md, reports/other-l1_findings/publications-reviews-dfinityconsensus-pdf.md, reports/other-l1_findings/publications-tortuga-liquid-staking-zellic-audit-report-pdf.md, reports/other-l1_findings/publicreports-l1-audits-taraxa-node-evm-l1-security-audit-report-halborn-final-pdf.md, see pattern_key (+1 more)

### Community 115 - "general 13"
Cohesion: 0.38
Nodes (9): block_execution_pipeline, block execution pipeline, has executed transaction opt, missing signature verification, signature verified transaction, unsigned da transaction, reports/movement-l1_findings/41794-bc-high-not-having-any-whitelisted-account-completely-disables-the-prevalidator-leading-to-tra.md, reports/movement-l1_findings/43307-bc-high-not-verifying-the-signatures-upon-execution-leads-to-direct-loss-of-funds.md (+1 more)

### Community 116 - "protocol-specific 18"
Cohesion: 0.38
Nodes (9): bridge_light_client, beacon chain light client, eth2 light client relayer, missing skip slot handling, skipped slot reorg, unhandled error state, reports/other-l1_findings/public-audits-reports-aurora-review-pdf.md, unhandled_error_state (+1 more)

### Community 117 - "cosmos 26"
Cohesion: 0.38
Nodes (9): channel_handshake, ibc_channel_upgrade, Channel Upgrade Validation Vulnerabilities [MEDIUM], channel upgrade handshake, channel upgrade validation, connection hops validation, ibc channel upgrade, validate basic ordering (+1 more)

### Community 118 - "general 14"
Cohesion: 0.38
Nodes (9): da_blob_deserialization, bcs from bytes, celestia blob ingress, into da blob, zstd decode all, zstd decode all bomb, reports/movement-l1_findings/42143-bc-critical-decompressing-a-maliciously-crafted-blob-leads-to-shutting-down-all-movement-da-li.md, reports/movement-l1_findings/42233-bc-critical-critical-dos-vulnerability-in-movement-network-s-da-layer-due-to-zstd-bomb-blob-ex.md (+1 more)

### Community 119 - "general 15"
Cohesion: 0.38
Nodes (9): da_light_node_prevalidator, bcs to bytes, client controlled priority or seqnum, da transaction envelope, unsigned wrapper mismatch, reports/movement-l1_findings/43017-bc-high-prevalidation-does-not-validate-application-priority-sequence-number-and-id.md, reports/movement-l1_findings/43323-bc-high-inadequate-sequence-number-validation-in-da-light-node-enables-transaction-censorship.md, reports/movement-l1_findings/43324-bc-high-insufficient-validation-in-da-light-node-allows-malicious-override-of-application-prio.md (+1 more)

### Community 120 - "protocol-specific 19"
Cohesion: 0.38
Nodes (9): fund_token pending-transaction lifecycle, disabled self service, request_full_liquidation, self service transfer, smart table pending transactions, tx_type_cash_liquidation, unchecked pending request, reports/other-l1_findings/publications-reviews-2024-10-franklintempleton-aptos-securityreview-pdf.md (+1 more)

### Community 121 - "protocol-specific 20"
Cohesion: 0.38
Nodes (9): rwa token plume, rwa token plume, varies by finding, reports/plume-l1_findings/49731-sc-high-theft-on-re-added-tokens.md, reports/plume-l1_findings/49732-sc-medium-malicious-token-admin-can-permanently-block-setpurchasetoken.md, reports/plume-l1_findings/49854-sc-critical-dex-aggregator-partial-fill-token-loss.md, reports/plume-l1_findings/49863-sc-critical-dex-aggregator-erc20-token-theft.md, reports/plume-l1_findings/50252-sc-high-rounding-excess-yield-tokens-become-permanently-stuck-when-last-holder-is-yield-restri.md (+1 more)

### Community 122 - "DB Community 122"
Cohesion: 0.20
Nodes (10): account-abstraction, general-governance, general-security, substrate, sui-move, governance_dao, smart_account_aa, substrate_parachain (+2 more)

### Community 123 - "general 16"
Cohesion: 0.42
Nodes (8): da blob consensus, da blob consensus, reports/movement-l1_findings/41437-bc-high-an-edge-case-allows-duplicate-transactions-to-be-added-to-the-mempool-of-the-sequencer.md, reports/movement-l1_findings/41489-bc-critical-blob-sizes-remain-unchecked-leading-to-chain-halt.md, reports/movement-l1_findings/41686-bc-high-the-passthrough-da-light-node-streams-transactions-instead-of-blocks-which-means-that.md, reports/movement-l1_findings/42761-bc-high-memseq-does-not-verify-client-specified-expiration-for-transactions-before-including-t.md, reports/movement-l1_findings/43110-bc-critical-validator-can-dos-the-da-layer-by-requesting-a-big-range-of-blobs.md, Da Blob Consensus

### Community 124 - "protocol-specific 21"
Cohesion: 0.42
Nodes (8): fassets vault flare, fassets vault flare, reports/flare-l1_findings/45514-sc-medium-malicious-agents-can-trap-stakers-by-raising-the-exit-collateral-ratio.md, reports/flare-l1_findings/45554-sc-medium-fee-loss-during-agents-feebips-reduction-in-selfmint-function.md, reports/flare-l1_findings/45769-sc-medium-permanent-blocking-of-agents-fund-by-allowed-minters.md, reports/flare-l1_findings/45910-sc-medium-changing-collateral-ratio-makes-agents-prone-to-liquidation.md, reports/flare-l1_findings/45979-sc-high-agent-can-steal-funds-from-flr-holders-who-have-deposited-in-agents-collateral-pool.md, Fassets Vault Flare

### Community 125 - "DB Community 125"
Cohesion: 0.42
Nodes (8): flare misc, varies, reports/flare-l1_findings/45478-sc-medium-minting-cap-check-doesnt-include-poolfeeuba-in-selfmint-and-mintfromunderlying.md, reports/flare-l1_findings/45550-sc-medium-h-01-illegalpaymentchallenge-is-vulnerable-to-frontrunning-by-external-challengers-s.md, reports/flare-l1_findings/45665-sc-medium-h-02-minting-cap-bypass-via-pool-fee-exclusion-during-self-mint.md, reports/flare-l1_findings/45830-sc-medium-incorrect-amount-passed-to-checkmintingcap-in-self-minting-allows-bypassing-of-confi.md, reports/flare-l1_findings/46108-sc-medium-minting-cap-can-by-bypassed-while-self-minting.md, Flare Misc

### Community 126 - "cosmos 27"
Cohesion: 0.42
Nodes (8): ics20_transfer, token_transfer_middleware, ICS20 v2 / Token-Transfer Validation Vulnerabilities [MEDIUM], denom trace validation, fungible token packet, ics20v2 transfer validation, reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-02-14-audit-report-astroport-ibc-v1-0-pdf.md, reports/cosmos-l1-nodes_findings/publications-celestia-packet-forward-middleware-zellic-audit-report-pdf.md

### Community 127 - "general 17"
Cohesion: 0.42
Nodes (8): mempool_ingress_fee_economics, light node prevalidate, missing balance check, unfunded tx submission, reports/movement-l1_findings/41531-bc-critical-attackers-can-drain-the-sequencers-wallet-and-dos-network-by-submitting-transactio.md, reports/movement-l1_findings/43191-bc-high-dos-attack-by-sending-transactions-that-pass-the-sufficient-balance-test-when-entering.md, reports/movement-l1_findings/43288-bc-critical-attackers-could-force-nodes-to-process-traattackers-could-force-nodes-to-process-t.md, Unfunded Transaction Ingress Drains Sequencer's TIA Wallet and Wedges the Network

### Community 128 - "DB Community 128"
Cohesion: 0.42
Nodes (8): misc plume, see pattern key, reports/plume-l1_findings/49705-sc-medium-two-vectors-for-unbounded-gas-consumption-due-to-the-normal-raffle-operations.md, reports/plume-l1_findings/49787-sc-high-batched-yield-distribution-doesn-t-account-for-transfers-purchases-between-batches-1.md, reports/plume-l1_findings/49787-sc-high-batched-yield-distribution-doesn-t-account-for-transfers-purchases-between-batches.md, reports/plume-l1_findings/49939-sc-high-initial-timestamp-mismatch-might-lead-to-users-being-able-to-spin-twice-in-the-same-da.md, reports/plume-l1_findings/49963-sc-medium-anyone-can-create-an-arctoken-and-block-the-setpurchasetoken-function.md, Misc Plume

### Community 129 - "account-abstraction 3"
Cohesion: 0.42
Nodes (8): module_installation, ERC-7579 Module System — Registry Bypass, moduleType Confusion, Hook PostCheck Skip, Fallback Flaws [HIGH], module system misconfiguration, reports/account_abstraction_findings/enable-mode-signature-ignores-module-type.md, reports/account_abstraction_findings/erc-7484-registry-checks-missing-on-calls-to-modules.md, reports/account_abstraction_findings/fallback-logic-prevents-hooks-postcheck-from-getting-executed.md, reports/account_abstraction_findings/installing-validators-with-enable-mode-in-validateuserop-doesnt-check-moduletype.md, reports/account_abstraction_findings/missing-call-type-validation-in-_installfallbackhandler.md

### Community 130 - "general 18"
Cohesion: 0.42
Nodes (8): move module bugs, move module bugs, reports/movement-l1_findings/41012-bc-critical-unintended-chain-split-in-movement-full-node.md, reports/movement-l1_findings/41334-bc-critical-attacker-can-publish-a-blob-that-cannot-be-deserialized-and-shut-down-the-movement.md, reports/movement-l1_findings/42102-bc-high-uncontrolled-resource-consumption-is-resulting-in-oom-via-rpc-public-one.md, reports/movement-l1_findings/42395-bc-high-movement-does-not-allow-overwriting-transactions-with-a-higher-priority-breaking-aptos.md, reports/movement-l1_findings/42513-bc-high-users-might-loose-storage-gas-fee-refund-due-to-governed-gas-pool-feature-of-movement.md, Move Module Bugs

### Community 131 - "protocol-specific 22"
Cohesion: 0.42
Nodes (8): PrincipalToken, yield_drain, erc4626 share price, flash loan vault deflation, max flash loan, share price reset, reports/erc4626_findings/m-02-all-yield-generated-in-the-ibt-vault-can-be-drained-by-performing-a-vault-d.md, Flash Loan Vault Deflation Attack: Draining Accumulated Yield via Share Price Reset [MEDIUM]

### Community 132 - "protocol-specific 23"
Cohesion: 0.42
Nodes (8): stacks signer stx, stacks signer stx, reports/stacks-l1_findings/37470-bc-medium-sbtc-signers-do-not-page-through-pending-deposit-requests-making-it-trivially-easy-t.md, reports/stacks-l1_findings/37811-bc-high-missing-length-check-when-parsing-signaturesharerequest-in-the-signers-allows-the-coor.md, reports/stacks-l1_findings/37861-bc-critical-sbtc-signer-wsts-implementation-allows-nonce-replays-such-that-a-malicious-signer.md, reports/stacks-l1_findings/38111-bc-high-attackers-can-send-a-very-large-event-in-a-stacks-block-so-that-the-signer-can-never-g.md, reports/stacks-l1_findings/38133-bc-medium-a-rogue-signer-can-censor-any-deposit-request-from-being-processed-and-fullfilled-on.md, Stacks Signer Stx

### Community 133 - "protocol-specific 24"
Cohesion: 0.42
Nodes (8): staking rewards plume, staking rewards plume, reports/plume-l1_findings/49616-sc-high-user-can-steal-rewards.md, reports/plume-l1_findings/49700-sc-high-validator-commission-can-be-blocked.md, reports/plume-l1_findings/49817-sc-medium-inactive-validators-are-prevented-to-claim-to-eligible-commission-rewards.md, reports/plume-l1_findings/50167-sc-high-retroactive-reward-drain-via-incomplete-reward-debt-reset.md, reports/plume-l1_findings/50350-sc-high-stakingfacet-stakeonbehalf-allows-to-prevent-withdraws.md, Staking Rewards Plume

### Community 134 - "general 19"
Cohesion: 0.42
Nodes (8): transaction_ingress_prevalidation, fail open validation, light node prevalidator, no whitelist config, reports/movement-l1_findings/41373-bc-high-premature-transaction-acceptance-to-mempool-da-without-signature-validation.md, reports/movement-l1_findings/41722-bc-high-the-passthrough-da-light-node-does-not-prevalidate-transactions-which-leads-to-non-des.md, fail_open_validation, Whitelist-Optional Prevalidator Fails Open: No Whitelist ⇒ No Signature Validation

### Community 135 - "protocol-specific 25"
Cohesion: 0.46
Nodes (7): margin_trading_module, divergent code paths, max_slippage_rate, min token d amount, reports/other-l1_findings/public-audits-reports-near-sigma-prime-burrow-finance-burrowland-security-assessment-report-v2-0-pdf.md, reports/other-l1_findings/public-audits-reports-near-sigma-prime-near-burrowland-security-assessment-report-v2-0-pdf.md, NEAR Burrow (Burrowland) — Margin-Module Check Divergence, Dust Bad-Debt, and Liquidator Slippage Extraction

### Community 136 - "protocol-specific 26"
Cohesion: 0.46
Nodes (7): polygon bor, reports/other-l1_findings/public-audits-reports-near-review-pdf.md, reports/other-l1_findings/public-audits-reports-polygon-sigma-prime-polygon-lxly-bridge-security-assessment-report-v2-1-pdf.md, reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debt-dao-p2p-loan-smart-contract-security-audit-report-halborn-final-pdf.md, reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-compound-vault-smart-contract-security-assessment-report-halborn-final-pdf.md, reports/other-l1_findings/publicreports-solidity-smart-contract-audits-tribal-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md, Polygon Bor

### Community 137 - "protocol-specific 27"
Cohesion: 0.95
Nodes (6): reserve_drain, impermanent_loss_manipulation, reports/constantproduct/h-06-lps-of-vaderpoolv2-can-manipulate-pool-reserves-to-extract-funds-from-the-r.md, reports/constantproduct/h-06-paying-il-protection-for-all-vaderpool-pairs-allows-the-reserve-to-be-drain.md, Keywords, Vulnerable Code Pattern

### Community 138 - "protocol-specific 28"
Cohesion: 1.29
Nodes (6): staking_lifecycle, reentrancy fund freeze, reports/constantproduct/h-11-protocol-insolvent-permanent-freeze-of-funds.md, Keywords, State Machine Corruption Flow [HIGH], Vulnerable Code Pattern

### Community 139 - "general 20"
Cohesion: 0.60
Nodes (5): da_blob_verification, inner signed blob v1, to signing bytes, reports/movement-l1_findings/42153-bc-critical-attackers-can-exploit-bug-in-blob-verification-to-execute-replay-attack-by-re-exec.md, Blob ID Not Bound to Computed ID — Replay-by-ID-Forgery Re-Executes Blobs

### Community 140 - "protocol-specific 29"
Cohesion: 0.60
Nodes (5): pool_factory, deterministic address dos, predict next address, reports/constantproduct/h-02-lambofactory-can-be-permanently-dos-ed-due-to-createpair-call-reversal.md, Keywords

## Knowledge Gaps
- **114 isolated node(s):** `account-abstraction`, `ERC-4337`, `ERC-7579`, `smart-wallet`, `paymaster` (+109 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 245 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `single_contract` connect `cosmos 7` to `defi`, `cosmos`, `protocol-specific 22`, `zk-rollup 2`, `defi 2`, `governance`, `defi 3`, `cosmos 5`, `substrate`, `cosmos 9`, `defi 6`, `oracle`, `proxy 2`, `cosmos 11`, `general 3`, `oracle 2`, `substrate 2`, `cosmos 13`, `substrate 3`, `cosmos 16`, `cosmos 17`, `protocol-specific 15`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `arithmetic_error` connect `general` to `zk-rollup`, `zk-rollup 2`, `defi 3`, `general 3`, `general 4`, `cosmos 7`, `zk-rollup 3`, `cosmos 8`, `cosmos 9`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `data_manipulation` connect `defi 4` to `access-control`, `general 19`, `substrate`, `lending`, `token`, `general 3`, `oracle 2`, `account-abstraction`, `solana`, `general 4`, `oracle 3`, `general 5`, `protocol-specific 6`, `general 8`, `general 9`, `general 12`, `protocol-specific 13`, `protocol-specific 15`, `general 14`, `general 15`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **What connects `account-abstraction`, `ERC-4337`, `ERC-7579` to the rest of the system?**
  _114 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `access-control` be split into smaller, more focused modules?**
  _Cohesion score 0.14736547259655783 - nodes in this community are weakly interconnected._
- **Should `defi` be split into smaller, more focused modules?**
  _Cohesion score 0.10193897918448816 - nodes in this community are weakly interconnected._
- **Should `zk-rollup 2` be split into smaller, more focused modules?**
  _Cohesion score 0.14403651903651904 - nodes in this community are weakly interconnected._