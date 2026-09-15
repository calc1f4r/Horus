---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: chain_halt
vulnerability_type: denial_of_service

# Attack Vector Details
attack_type: chain_halt
affected_component: abci_consensus

# Technical Primitives
primitives:
  - BeginBlock
  - EndBlocker
  - FinalizeBlock
  - ProcessProposal
  - PrepareProposal
  - linear_iteration

# Impact Classification
severity: critical
impact: chain_halt
exploitability: 0.8
financial_impact: critical

# Context Tags
tags:
  - cosmos_sdk
  - cometbft
  - chain_halt
  - dos
  - non_determinism
  - BeginBlock
  - EndBlocker
  - division_by_zero
  - negative_amount
  
language: go
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | abci_consensus | denial_of_service

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - BeginBlock
  - EndBlocker
  - FinalizeBlock
  - PrepareProposal
  - ProcessProposal
  - linear_iteration
---

## References & Source Reports

| Report | Path | Severity | Signal |
|--------|------|----------|--------|
| Groups module malicious proposal chain halt | `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md` | HIGH | Division-by-zero or invalid group state in consensus path |
| BeginBlock rewards plan iteration halt | `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md` | HIGH | Permissionless state growth consumed by BeginBlock |
| MsgRemoveDelegates arbitrary halt | `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md` | HIGH | User message creates later consensus panic |
| FinalizeBlock non-determinism | `reports/cosmos_cometbft_findings/potential-non-determinism-issue-in-finalizeblock.md` | HIGH | Validator-dependent result in consensus execution |
| CometBFT block sync DoS | `reports/cosmos_cometbft_findings/dos-in-cometbft-block-sync-githubcomcometbftcometbftblocksync.md` | MEDIUM | Peer-controlled resource exhaustion |
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-all-in-bits-2022-04-04-audit-report-budget-and-farming-cosmos-sdk-modules-v1-0-pdf.md | CRITICAL | Oak Security | Iteration over farming plans in end blocker can be exploited to halt block production |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-all-in-bits-2022-04-04-audit-report-budget-and-farming-cosmos-sdk-modules-v1-0-pdf.md | CRITICAL | Oak Security | Iteration over queued stakings in end blocker can be exploited to halt block production |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-all-in-bits-2022-04-04-audit-report-budget-and-farming-cosmos-sdk-modules-v1-0-pdf.md | CRITICAL | Oak Security | Unbounded staking and epoch amount coins can be exploited to halt block production |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-all-in-bits-2022-04-04-audit-report-budget-and-farming-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Farming plans are unbounded, which increases gas consumption of plan creation/updates/deletion and may be exploited by an attacker |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2025-03-17-audit-report-astroport-pcl-neutron-duality-orderbook-integration-v1-0-pdf.md | HIGH | Oak Security | Excessive gas consumption in pool operations |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Unvalidated RFF publication enables P2P network spam and resource exhaustion |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Unbounded pending settlements are processed during the PreBlocker , which can cause consensus delays |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | Disabling libp2p limits enables remote DoS |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-10-28-audit-report-comdex-locking-and-vesting-contracts-v1-0-pdf.md | HIGH | Oak Security | Unbounded iterations may cause calculate_rebase_reward to run out of gas |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-10-28-audit-report-comdex-locking-and-vesting-contracts-v1-0-pdf.md | HIGH | Oak Security | Unbounded data structures processed in loops make several features prohibitively expensive or even unusable |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-11-23-audit-report-comdex-lend-and-liquidation-modules-v1-0-pdf.md | CRITICAL | Oak Security | Gas is not consumed if the transaction returns an error |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-11-23-audit-report-comdex-lend-and-liquidation-modules-v1-0-pdf.md | CRITICAL | Oak Security | Input-dependent iteration in Lend module's BeginBlocker may slow down or stop block production |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Unbounded iteration allows attackers to attack validators, slowing down or even halting block production |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Transaction gas price is not related to execution complexity |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Computationally heavy operations in BeginBlocker and EndBlocker may slow down or stop block production |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Gas is not consumed if the transaction returns an error |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | HIGH | Oak Security | Base gas fee is insufficient for functions with iteration |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | CRITICAL | Oak Security | A validator updating its ConsumerKey to the same key causes a panic in the related consumer chain |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can DOS attack consumer chains by sending multiple coins to the provider chain's reward address |
| [k20] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | HIGH | Oak Security | The provider chain halts on failure to send packets to a single consumer chain |
| [k21] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-sdk-2024-01-23-audit-report-cosmos-sdk-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can perform an inexpensive DoS attack by spamming Deposit transactions |
| [k22] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-sdk-2024-01-23-audit-report-cosmos-sdk-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can perform an inexpensive DoS attack by spamming Grant transactions |
| [k23] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-sdk-2024-01-23-audit-report-cosmos-sdk-v1-0-pdf.md | HIGH | Oak Security | The PrepareProposal function could silently fail due to deferred panic handling |
| [k24] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-03-27-audit-report-cosmwasm-v1-0-pdf.md | CRITICAL | Oak Security | Cache hit counters can be used to crash nodes and halt a chain |
| [k25] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-03-27-audit-report-wasmvm-v1-0-pdf.md | CRITICAL | Oak Security | Unlimited iterator stack might allow an attacker to crash the node, halting block production |
| [k26] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-10-17-audit-report-wasmd-v1-0-pdf.md | CRITICAL | Oak Security | Gzipped wasm binaries with invalid CRC could be used to DOS the chain |
| [k27] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-10-17-audit-report-wasmd-v1-0-pdf.md | HIGH | Oak Security | IBC Querier plugin's unbounded loop could lead to DoS |
| [k28] | reports/cosmos-l1-nodes_findings/audit-reports-croncat-2023-03-14-audit-report-croncat-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | AGENTS_PENDING is not resistant to spam attack |
| [k29] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-03-08-audit-report-dymension-point-0d-v1-0-pdf.md | CRITICAL | Oak Security | The invariant checking the last stream ID will break over time, potentially causing the chain to halt |
| [k30] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-03-08-audit-report-dymension-point-0d-v1-0-pdf.md | CRITICAL | Oak Security | Unbounded loop in PowApprox can be exploited to halt the chain |
| [k31] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-07-09-audit-report-dymension-point-1d-stream-3-dymint-v1-1-pdf.md | HIGH | Oak Security | HTTP server misconfiguration allows Slowloris DoS attacks |
| [k32] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-07-09-audit-report-dymension-point-1d-stream-3-dymint-v1-1-pdf.md | HIGH | Oak Security | CONTINUATION frames flood vulnerability in x/net allows attackers to DoS the node |
| [k33] | reports/cosmos-l1-nodes_findings/audit-reports-injective-2023-01-20-audit-report-injective-v1-0-pdf.md | CRITICAL | Oak Security | Contract creators can update the gas price into invalid integer value in order to disable the wasmx 's BeginBlocker execution |
| [k34] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Withdrawal of tokenized share record rewards is unbounded, owner can be grieved by an attacker |
| [k35] | reports/cosmos-l1-nodes_findings/audit-reports-lido-finance-2022-05-16-audit-report-lido-finance-statom-on-cosmos-hub-v1-0-pdf.md | HIGH | Oak Security | Unbounded unbond history entries may cause all deposited funds stuck in the hub contract |
| [k36] | reports/cosmos-l1-nodes_findings/audit-reports-lido-finance-2022-05-16-audit-report-lido-finance-statom-on-cosmos-hub-v1-0-pdf.md | HIGH | Oak Security | Unbounded unbond wait entities may cause user funds to be stuck in hub contract |
| [k37] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-12-04-audit-report-mars-perps-v1-0-pdf.md | HIGH | Oak Security | Withdrawal may fail due to out-of-gas error when iterating positions |
| [k38] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | CRITICAL | Oak Security | An error triggered during the handling of an Ack IBC message will make the channel unusable and spam the network |
| [k39] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Attackers are able to spam the network with IBC messages using the ibc-transfer module |
| [k40] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Unbounded iteration in ValidateBasic may cause node timeout |
| [k41] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Unbounded iteration in PerformSubmitTx could be used by an attacker to slow down or halt the chain |
| [k42] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Unbounded iteration in EndBlocker when calculating vote power could be used by an attacker to slow down or halt the chain |
| [k43] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | CRITICAL | Oak Security | Misconfigured governance module permissions causing consensus-halting panic on deposit burn |
| [k44] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can halt the chain by performing numerous minimal unstaking requests from different accounts |
| [k45] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | CRITICAL | Oak Security | Risk of gas exhaustion for unbounded ICA messages |
| [k46] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | CRITICAL | Oak Security | The AfterEpochStart hook consumes excessive computational resources |
| [k47] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | HIGH | Oak Security | The BeforeEpochStart hook consumes excessive computational resources |
| [k48] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | HIGH | Oak Security | The DoRedeemLSMTokens function consumes excessive computational resources in the BeginBlocker |
| [k49] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-15-audit-report-sei-cosmos-v1-0-pdf.md | CRITICAL | Oak Security | Non-deterministic iteration in BuildDependencyDag may break consensus |
| [k50] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-15-audit-report-sei-cosmos-v1-0-pdf.md | HIGH | Oak Security | RegisterWasmDependency allows anyone to register contract dependency mappings that can increase gas consumption |
| [k51] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-19-audit-report-sei-chain-and-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | MsgContractDepositRent should set a minimum amount to avoid potential spamming |
| [k52] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-19-audit-report-sei-chain-and-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Processing of MsgPlaceOrders and MsgSend messages in EndBlocker may be exploited to halt the chain if mispriced |
| [k53] | reports/cosmos-l1-nodes_findings/audit-reports-stride-2022-09-26-audit-report-stride-v1-0-pdf.md | CRITICAL | Oak Security | Non-deterministic iterations can cause consensus failures |
| [k54] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Permissionless burn enables denom recreation failure and withdrawal DoS |
| [k55] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Unchecked unwrap on optional cap field causes panic |
| [k56] | reports/cosmos-l1-nodes_findings/audit-reports-volta-2024-09-18-audit-report-volta-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Malicious owners or users spamming messages could prevent the admin from executing ProposalType::Configuration proposals |
| [k57] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-04-30-namada-abci-replay-protection-fee-and-gas-metering-final-report-pdf.md | CRITICAL | Informal Systems | Block could be rejected due to proposer and validators using different minimum gas price |
| [k58] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-12-11-namada-governance-pgf-pdf.md | CRITICAL | Informal Systems | Adding an incomplete proposal may cause panic in finalize_block |
| [k59] | reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md | HIGH | Informal Systems | The function verifyLeafHashes will panic if called from VerifyInclusion function over an empty proof |
| [k60] | reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md | HIGH | Informal Systems | Wrapper Push function will panic if the data is invalid |
| [k61] | reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md | HIGH | Informal Systems | ValidateInclusion function can panic if it is called with an invalid nid |
| [k62] | reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md | HIGH | Informal Systems | VerifyNamespace panics if called on an empty range, but with non- empty nodes |
| [k63] | reports/cosmos-l1-nodes_findings/audits-cosmos-hub-2023-02-10-audit-report-ics-replicated-security-pdf.md | MEDIUM | Informal Systems | Interchain Security v.1.0 Panics on failure to send IBC packets |
| [k64] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | CRITICAL | Informal Systems | Repetetive exponentiation in price computation may lead to DOS |
| [k65] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | CRITICAL | Informal Systems | A byzantine consumer can cause chain halt via pricing tick |
| [k66] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | HIGH | Informal Systems | Wasteful usage of storage creates a potential for DOS attacks |
| [k67] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | MEDIUM | Informal Systems | Invalid Multi Hop Swap routes cause panic |
| [k68] | reports/cosmos-l1-nodes_findings/audits-evmos-informal-evmos-report-2021q4-pdf.md | HIGH | Informal Systems | Delegating 10ˆ6 * 2ˆ63 - x for a small x halts consensus |
| [k69] | reports/cosmos-l1-nodes_findings/audits-mars-protocol-2023-02-03-audit-report-mars-protocol-envoy-module-pdf.md | HIGH | Informal Systems | Mars Protocol Envoy module Iterate over all Interchain Accounts |
| [k70] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-04-06-audit-report-neutron-sdk-dao-wasmd-tge-pdf.md | HIGH | Informal Systems | Neutron Non-validated IBC acknowledgement/timeout fees can lead to drainage of relayers funds and spamming of the network |
| [k71] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | CRITICAL | Informal Systems | Unbounded iteration over Incentives stakes may lead to chain halt |
| [k72] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | HIGH | Informal Systems | Quadratic scaling for multi-amount deposits may lead to DOS |
| [k73] | reports/cosmos-l1-nodes_findings/audits-stride-2022-11-30-audit-report-stride-stakeibc-icacallbacks-pdf.md | HIGH | Informal Systems | Stride StakeIBC and ICACallbacks Modules One chain redemption out-of-bounds may halt all chains |
| [k74] | reports/cosmos-l1-nodes_findings/celestia-app-docs-audit-informal-systems-pdf.md | MEDIUM | Informal Systems | Iteration over all transactions when building the datasquare |
| [k75] | reports/cosmos-l1-nodes_findings/interchain-security-docs-audits-informal-ics-2023-pdf.md | MEDIUM | Informal Systems | Interchain Security v.1.0 Panics on failure to send IBC packets |
| [k76] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Panic triggered by incorrect logic in finality module's EndBlock |
| [k77] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | The btclightclient module design flaw after Babylon chain halt |
| [k78] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Incorrect Delegation Status Check Leading to Chain Halt |
| [k79] | reports/cosmos-l1-nodes_findings/publications-babylon-zellic-audit-report-pdf.md | MEDIUM | Zellic | Invalid creation of unbonding TX leads to loss of gas |
| [k80] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | NON-DETERMINISTIC ITERATIONS CAN CAUSE CONSENSUS FAILURES |
| [k81] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-umee-wasm-integration-cosmos-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | VULNERABLE WASM SMART CONTRACT LEADS TO CHAIN HALT |
| [k82] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-nexus-protocol-cosmwasm-smart-contract-security-audit-report-halborn-v1-1-pdf.md | HIGH | Halborn | MISCALCULATION OF NASSET TOKENS TO MINT LEADS TO UNFAIR WITHDRAWING / DOS |
| [k83] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNRESTRICTED CHANGES IN FEE RATES LEAD TO TOKENS LOSS / DOS |
| [k84] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-2023-q4-pdf.md | MEDIUM | Informal Systems | Potential Network Degradation Caused by Short-Term Order Spamming |
| [k85] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-2023-q4-pdf.md | CRITICAL | Informal Systems | Potential Chain Halt due to Panic in ABCI Phases |
| [k86] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-2024-q1-pdf.md | HIGH | Informal Systems | Proposed operations tx has no size limitation leading to possible withdrawal halting being postponed |
| [k87] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-2024-q1-pdf.md | HIGH | Informal Systems | Withdrawal halting could be postponed as long as malicious validators and daemons are selected for the proposer consecutively |
| [k88] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-2024-q2-pdf.md | MEDIUM | Informal Systems | Potential state bloating may occur as a result of invalid vaults being included on the chain |
| [k89] | reports/cosmos-l1-nodes_findings/audits-anoma-namada-q2-2025-e2e-shielded-transaction-balance-consistency-audit-report-final-pdf.md | MEDIUM | Informal Systems | Namada T ransactions doing masp fee payment may be executed an unbounded number of times for free |
| [k90] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | VIG - Suggestion to track UNBONDED and EXPIRED delegation statuses in Vigilante Protocol Informational Acknowledged BAB - Missing validation for halti |
| [k91] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-high-throughput-recovery-audit-report-final-v2-pdf.md | HIGH | Informal Systems | High Throughput Recovery Calling SetHave and SetWant method could trigger a panic |
| [k92] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-high-throughput-recovery-audit-report-final-v2-pdf.md | MEDIUM | Informal Systems | High Throughput Recovery Race condition in syncData causes a runtime panic |
| [k93] | reports/cosmos-l1-nodes_findings/celestia-app-docs-audit-informal-systems-recovery-pdf.md | HIGH | Informal Systems | High Throughput Recovery Calling SetHave and SetWant method could trigger a panic |
| [k94] | reports/cosmos-l1-nodes_findings/celestia-app-docs-audit-informal-systems-recovery-pdf.md | MEDIUM | Informal Systems | High Throughput Recovery Race condition in syncData causes a runtime panic |
| [k95] | reports/cosmos-l1-nodes_findings/audits-ibc-go-report-pdf.md | HIGH | auditor | Model-based Testing for Token Transfer Set of new artifacts to facilitate rigorous testing Informative Code IF-IBC-14 Panic on receiving multi-chain d |
| [k191] | reports/cosmos-l1-nodes_findings/audits-injective-informal-report-injective-audit-202106-pdf.md | HIGH | Informal Systems | Systems Injective Protocol Audit IF-INJECTIVE-10 A sequence of transactions leads to a complete halt of con- sensus #323 Status: Resolved |
| [k192] | reports/cosmos-l1-nodes_findings/audits-injective-informal-report-injective-audit-202106-pdf.md | HIGH | Informal Systems | Systems Injective Protocol Audit IF-INJECTIVE-12 Recommendation for recovery in EndBlocker #301 Status: Unresolved (as of June 11, 2021) |
| [q193] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-04-30-audit-report-dymension-point-1d-stream-2-virtual-frontier-contract-v1-1-pdf.md | LOW | Oak Security | Long-term DenomMetaData accumulation can DoS the chain |
| [q194] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-04-30-audit-report-dymension-point-1d-stream-2-virtual-frontier-contract-v1-1-pdf.md | LOW | Oak Security | Faulty DenomMetadata halts VirtualFrontierContracts deployment |
| [q195] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | LOW | Oak Security | Unbounded loops could render main features unusable |

## Vulnerability Title

**Chain Halt and DoS Attack Vectors in Cosmos SDK Appchains**

### Overview

Cosmos SDK appchains are susceptible to various chain halt and denial of service attacks due to unmetered linear iteration in BeginBlock/EndBlocker, division by zero in governance modules, negative amount validation failures causing panics, and non-determinism in consensus-critical code. These vulnerabilities allow attackers to halt the chain with relatively low cost, breaking security guarantees for all validators and users.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | abci_consensus | denial_of_service`
- Interaction scope: `single_contract`
- Primary affected component(s): `abci_consensus`
- High-signal code keywords: `BeginBlock`, `EndBlocker`, `FinalizeBlock`, `PrepareProposal`, `ProcessProposal`, `linear_iteration`
- Typical sink / impact: `chain_halt`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: `BeginBlock`, `EndBlocker`, `FinalizeBlock`, `PrepareProposal`, or `ProcessProposal` iterates over permissionlessly growable state.
- Signal 2: A normal user message can store malformed state that later panics in consensus code, even if the original transaction succeeds.
- Signal 3: Consensus-critical code depends on map iteration order, wall-clock time, local node state, peer input, floating point, or nondeterministic sorting.
- Signal 4: Arithmetic in consensus paths can divide by zero, create negative coins, overflow counters, or call SDK constructors that panic on attacker-controlled values.

#### False Positive Guards

- Not this bug when: The loop is over validator-set, module-constant, governance-bounded, or paginated state with enforced caps.
- Safe if: Malformed user input is rejected at message handling time and consensus paths treat stored state as already validated without panic-prone recomputation.
- Requires attacker control of: proposal contents, delegation/group/reward-plan state, mempool ordering, peer block-sync input, or any state read by ABCI lifecycle hooks.

### Root Cause

1. **Unmetered linear iteration**: BeginBlock/EndBlocker iterate over unbounded collections without gas limits
2. **Division by zero**: Missing validation allows crafted proposals to cause arithmetic panics
3. **Negative amount panics**: Integer types without non-negative validation cause sdk.NewCoin to panic
4. **Non-determinism**: Different validator nodes computing different results, breaking consensus
5. **Unbounded block sync**: Malicious peers can overwhelm syncing nodes during block sync

### Impact Analysis

#### Technical Impact
- Complete chain halt (no new blocks produced)
- Consensus failure from non-determinism
- Validator nodes crash or hang
- Block sync disruption for new nodes
- All AVS security guarantees broken

#### Business Impact
- Network completely unavailable
- Emergency governance required to patch
- Validator slashing during downtime
- User funds inaccessible
- Massive reputation damage

### Audit Checklist[text](../../../DeFiHackLabs)
- BeginBlock/EndBlocker have bounded iteration
- All user-supplied amounts validated as positive
- Division operations check for zero divisor
- Map iterations converted to sorted deterministic order
- No system time or random in consensus code
- Plan/proposal creation has scaling fees

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| MilkyWay | Cantina | HIGH | Linear iteration over rewards plans |
| Allora | Sherlock | HIGH | Negative amount causes chain halt |
| SEDA/Cosmos | Sherlock | HIGH | Groups module division by zero (ASA-2025-003) |
| Various | OtterSec | HIGH | Non-determinism in FinalizeBlock |
| CometBFT | Security Audit | MEDIUM | Block sync DoS |

### Keywords

chain_halt, BeginBlock, EndBlocker, FinalizeBlock, linear_iteration, unbounded_loop, sdk.NewCoin, division_by_zero, negative_amount, non_determinism, consensus_failure, map_iteration, time.Now, panic, DoS, ASA-2025-003, groups_module

### Detection Patterns

#### Code Patterns to Look For
```
- `for _, x := range keeper.GetAll...` inside BeginBlocker, EndBlocker, FinalizeBlock, PrepareProposal, or ProcessProposal
- `sdk.NewCoin`, `Quo`, `QuoInt`, `Int64`, division, or percentage math in consensus paths without zero/negative validation
- map iteration or unsorted key traversal used to build proposals, votes, commitments, or state roots
- message handlers that append unbounded plans/delegates/groups consumed globally each block
- panics, `Must*` helpers, or unchecked errors reachable from ABCI lifecycle hooks
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`BeginBlock`, `EndBlocker`, `FinalizeBlock`, `PrepareProposal`, `ProcessProposal`, `chain_halt`, `cometbft`, `cosmos_sdk`, `denial_of_service`, `division_by_zero`, `dos`, `linear_iteration`, `negative_amount`, `non_determinism`
