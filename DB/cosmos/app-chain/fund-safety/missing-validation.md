---
# Core Classification
protocol: generic
chain: polkadot
category: validation
vulnerability_type: missing_input_validation
root_cause_family: missing_validation

# Pattern Identity
pattern_key: validation-gap | extrinsic | crafted input | invalid state accepted

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - extrinsic input validation

# Attack Vector Details
attack_type: input_validation_bypass
affected_component: extrinsic input validation

# Technical Primitives
primitives:
  - accepts
  - account
  - accounting
  - acknowledged
  - acknowledgement
  - active

# Grep / Hunt-Card Seeds
code_keywords:
  - accepts
  - account
  - accounting
  - acknowledged
  - acknowledgement
  - active
  - adaptor
  - adddistributor
  - adding
  - addresses

severity: critical
impact: fund_loss
language: rust
tags:
  - validation
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-05-22-audit-report-astroport-hub-neutron-migration-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can bypass self-migration validation to control assembly contract |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | CRITICAL | Oak Security | ProcessProposal accepts all proposals without validating vote extensions |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-avail-2026-01-15-audit-report-avail-cosmos-and-backend-changes-v1-0-pdf.md | HIGH | Oak Security | External RPC dependencies in consensus logic allow validators to be stalled |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Unbounded iteration allows attackers to attack validators, slowing down or even halting block production |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | CRITICAL | Oak Security | A validator updating its ConsumerKey to the same key causes a panic in the related consumer chain |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | HIGH | Oak Security | Validators can slow down the provider chain by submitting multiple AssignConsumerKey messages in the same block |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-sdk-2024-01-23-audit-report-cosmos-sdk-v1-0-pdf.md | HIGH | Oak Security | Inefficiencies in block capacity validation within the PrepareProposal function |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-cosmwasm-2023-10-17-audit-report-wasmd-v1-0-pdf.md | HIGH | Oak Security | Contract admins can bypass code ID instantiation permission when migrating contracts |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-croncat-2023-03-14-audit-report-croncat-cosmwasm-v1-0-pdf.md | CRITICAL | Oak Security | Attacker can bypass self-call validation |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-croncat-2023-03-14-audit-report-croncat-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Agents can bypass task delegation mechanism |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-03-08-audit-report-dymension-point-0d-v1-0-pdf.md | CRITICAL | Oak Security | MsgEthereumTx EVM messages can be nested within a MsgExec message to bypass Ante handlers and steal transaction fees or perform a Denial-of-Service at |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | CRITICAL | Oak Security | Missing denom validation when adding incentives could lead to insufficient funds error |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-12-04-audit-report-mars-perps-v1-0-pdf.md | HIGH | Oak Security | Missing account ID validation allows removal of other user's trigger orders |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2022-12-07-audit-report-neutron-v1-0-pdf.md | HIGH | Oak Security | Unbounded iteration in ValidateBasic may cause node timeout |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | CRITICAL | Oak Security | Validators receive lesser rewards due to incorrect reward denom |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validator rewards are lost if the payment schedule is updated |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validators with significant voting power could censor others to prevent them from receiving rewards |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validators can manipulate oracle prices to maximize rewards |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | Any CosmWasm contract can add cron schedules, bypassing authorization |
| [k20] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | ValidatorDstAddress may equal ValidatorSrcAddress in redelegation messages, causing upgrade failure |
| [k21] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | calcRedelegations uses delegation shares as token amounts, producing incorrect results when validators have been slashed |
| [k22] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | CRITICAL | Oak Security | Incorrect bookkeeping of validator's delegated amount upon redelegation |
| [k23] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | HIGH | Oak Security | Outdated validator exchange rates could result in inflated minting of liquid-staked tokens |
| [k24] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | HIGH | Oak Security | Validators are incorrectly set to non-delegable for default bond factor values |
| [k25] | reports/cosmos-l1-nodes_findings/audit-reports-starterra-audit-report-starterra-pdf.md | HIGH | Oak Security | Missing input validation on staking config update might lead to inconsistent state |
| [k51] | reports/cosmos-l1-nodes_findings/audit-reports-stride-2022-09-26-audit-report-stride-v1-0-pdf.md | HIGH | Oak Security | RegisterHostZone does not validate Bech32Prefix which will lead to staked funds being unredeemable if misconfigured |
| [k52] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Missing oracle staleness validation before using price data in Solana programs |
| [k53] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Lack of AUM Oracle state validation can lead to incorrect deposit flow tracking |
| [k54] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Waitasaurus does not validate oracle data timestamp |
| [k55] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Unchecked unwrap on optional cap field causes panic |
| [k56] | reports/cosmos-l1-nodes_findings/audit-reports-yieldmos-2024-05-17-audit-report-yieldmos-outposts-osmosis-v1-0-pdf.md | HIGH | Oak Security | Incorrect denom validation in Compound message |
| [k57] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-04-30-namada-abci-replay-protection-fee-and-gas-metering-final-report-pdf.md | CRITICAL | Informal Systems | Block could be rejected due to proposer and validators using different minimum gas price |
| [k58] | reports/cosmos-l1-nodes_findings/audits-celestia-2023-03-30-celestia-namespaced-merkle-tree-library-audit-pdf.md | HIGH | Informal Systems | ValidateInclusion function can panic if it is called with an invalid nid |
| [k59] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-cip-31-audit-report-final-pdf.md | HIGH | Informal Systems | Celestia Q2 2025 Vesting Restriction Bypass Through Custom Withdrawal Addresses |
| [k60] | reports/cosmos-l1-nodes_findings/audits-cosmos-hub-2023-02-10-audit-report-ics-replicated-security-pdf.md | HIGH | Informal Systems | Interchain Security v.1.0 A byzantine consumer can tombstone, slash, or jail an innocent validator |
| [k61] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | HIGH | Informal Systems | Tick and Fee inputs are not validated |
| [k62] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | MEDIUM | Informal Systems | Incomplete validation of MsgDeposit |
| [k63] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | MEDIUM | Informal Systems | Number of epochs for gauge creation is not validated |
| [k64] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-04-06-audit-report-neutron-sdk-dao-wasmd-tge-pdf.md | HIGH | Informal Systems | Neutron Non-validated IBC acknowledgement/timeout fees can lead to drainage of relayers funds and spamming of the network |
| [k65] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | MEDIUM | Informal Systems | Incomplete validation of MsgMultiHopSwap may lead to user fund loss and frustration |
| [k66] | reports/cosmos-l1-nodes_findings/audits-neutron-2023-11-11-audit-report-neutron-duality-v0-5-0-integration-of-cosmos-sdk-0-47-pdf.md | HIGH | Informal Systems | Tick and Fee inputs are not completely validated |
| [k67] | reports/cosmos-l1-nodes_findings/audits-osmosis-2023-06-23-audit-report-osmosis-q2-pdf.md | MEDIUM | Informal Systems | Insufficient validation on gauge creation |
| [k68] | reports/cosmos-l1-nodes_findings/gaia-contrib-audits-liquid-zellic-audit-25-pdf.md | MEDIUM | Informal Systems | Missing enforcement of MinSelfDelegation allows zero self-delegation for validators |
| [k69] | reports/cosmos-l1-nodes_findings/gaia-contrib-audits-liquid-zellic-audit-25-pdf.md | MEDIUM | Informal Systems | Blacklist bypass in reward withdrawal via TransferTokenizeShareRecord |
| [k70] | reports/cosmos-l1-nodes_findings/interchain-security-docs-audits-informal-ics-2023-pdf.md | HIGH | Informal Systems | Interchain Security v.1.0 A byzantine consumer can tombstone, slash, or jail an innocent validator |
| [k71] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | CosmWasm Stargate/Any messages bypass AnteHandler checks |
| [k72] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Incorrect parity check in adaptor signatures |
| [k73] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Incorrect Delegation Status Check Leading to Chain Halt |
| [k74] | reports/cosmos-l1-nodes_findings/publications-cosmos-sdk-liquid-stake-module-zellic-audit-report-pdf.md | HIGH | Informal Systems | Accounting validator bonds share could be broken |
| [k75] | reports/cosmos-l1-nodes_findings/publications-ibc-eureka-zellic-audit-report-pdf.md | CRITICAL | Zellic | Merkle verification could be bypassed |
| [k76] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | HIGH | Trail of Bits | Validators can crash other nodes by triggering an integer overflow |
| [k77] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-bot-golang-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | BOT INCONSISTENTLY CAN FAIL DUE TO MISSING CHECK |
| [k78] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | UNIQUENESS OF ZONES ARE NOT VALIDATED |
| [k79] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MISSING VALIDATION LEADS TO LOST OF FUNDS |
| [k80] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING VALIDATION ON THE HOST DENOM AND IBC DENOM |
| [k81] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-entangle-blockchain-cosmos-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | MISSING VALIDATION FOR END TIME IN ADDDISTRIBUTOR FUNCTION LEADS TO EXPIRED DISTRIBUTOR |
| [k82] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | UNCHECKED BALANCE CHANGE COULD LEAD TO UNFAIR WITHDRAWALS |
| [k83] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | REDELEGATION IS NOT RESTRICTED TO ACTIVE VALIDATORS |
| [k84] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS |
| [k85] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | RESTRICTION TO NOT SWAP MARS TOKENS CAN BE BYPASSED |
| [k86] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | SIGNATURE VALIDATION CAN BE BYPASSED |
| [k87] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-2024-q1-pdf.md | HIGH | Informal Systems | Withdrawal halting could be postponed as long as malicious validators and daemons are selected for the proposer consecutively |
| [k88] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-phase-iii-pdf.md | MEDIUM | Informal Systems | Missing validation of x/rewards parameters in MsgUpdateParams |
| [k89] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | Genesis v2 Upgrade GEN - Missing Minter validation in InitGenesis of x/mint module |
| [k90] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | VIG - Suggestion to track UNBONDED and EXPIRED delegation statuses in Vigilante Protocol Informational Acknowledged BAB - Missing validation for halti |
| [k91] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | GEN - Missing Minter validation in InitGenesis of x/mint module |
| [k92] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | Babylon Q2 2025 Genesis v2 Upgrade Finding Type Severity Status GEN - x/btcstaking genesis state is not entirely validated with ValidateGenesis |
| [k93] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-high-throughput-recovery-audit-report-final-v2-pdf.md | MEDIUM | Informal Systems | High Throughput Recovery The parts retrieved from mempool are not being validated |
| [k94] | reports/cosmos-l1-nodes_findings/audits-neutron-2025-07-18-neutron-timewave-q2-2025-valence-protocol-audit-report-final-pdf.md | MEDIUM | Informal Systems | Valence Protocol Lack of proper validation for withdraw request receiver |
| [k95] | reports/cosmos-l1-nodes_findings/audits-neutron-2025-07-18-neutron-timewave-q2-2025-valence-protocol-audit-report-final-pdf.md | MEDIUM | Informal Systems | Valence Protocol Missing validation of redemption rate in contract initialisation |
| [k96] | reports/cosmos-l1-nodes_findings/celestia-app-docs-audit-informal-systems-recovery-pdf.md | MEDIUM | Informal Systems | High Throughput Recovery The parts retrieved from mempool are not being validated |
| [k97] | reports/cosmos-l1-nodes_findings/audits-injective-informal-report-injective-audit-202106-pdf.md | HIGH | Informal Systems | Injective Protocol Audit IF-INJECTIVE-11 Price feed does not validate prices, may crash consensus #331 Status: resolved (as of June 15, 2021) |
| [k98] | reports/cosmos-l1-nodes_findings/publications-osmosis-authentication-abstraction-zellic-audit-report-pdf.md | CRITICAL | Zellic | Zellic 12 OsmosisLabs 3.2 Bypassfeepayerauthentication • Target:x/authenticator/ante/ante.go • Category:CodingMistakes • Likelihood:High • |
| [z99] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-haqq-vesting-cosmos-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | PROJECT VULNERABLE TO BARBERRY VULNERABILITY |
| [q100] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | LOW | Oak Security | Variable names and comments differ from the implementation |
| [q101] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | LOW | Oak Security | Market tick size parameters cannot be updated |
| [q102] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | INFO | Oak Security | No attributes are added to some message handlers' responses |
| [q103] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | INFO | Oak Security | Unnecessary duplicate asset validation |
| [q104] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | INFO | Oak Security | Misleading behavior in case of unexpected match branch |
| [q105] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | INFO | Oak Security | Duplicated code |
| [q106] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | INFO | Oak Security | TODO comments in the codebase |
| [q107] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-08-13-audit-report-dymension-point-1d-stream-6-rollapp-white-box-pentest-v1-1-pdf.md | LOW | Oak Security | Expensive RPC methods are allowed |
| [q108] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-08-13-audit-report-dymension-point-1d-stream-6-rollapp-white-box-pentest-v1-1-pdf.md | INFO | Oak Security | Usage of deprecated functionality |
| [q109] | reports/cosmos-l1-nodes_findings/audit-reports-dymension-2024-08-13-audit-report-dymension-point-1d-stream-6-rollapp-white-box-pentest-v1-1-pdf.md | INFO | Oak Security | Multiple subprocesses launched directly on the OS |
| [q110] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | LOW | Oak Security | USDC budget is declared but never verified to be held by the contract |
| [q111] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | INFO | Oak Security | README instantiation example contains incorrect and missing fields |
| [q112] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | INFO | Oak Security | README misleads users about when claiming becomes available |
| [q113] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | INFO | Oak Security | Direct ownership transfer allows accidental loss of contract control |
| [q114] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-1-pdf.md | INFO | Oak Security | Contract name in cw2 metadata does not match the crate name |
| [q115] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | LOW | Oak Security | Overly permissive message dispatch enabling privilege escalation via arbitrary CosmosMsg execution |
| [q116] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | INFO | Oak Security | Multiple entry points emit insufficient event attributes |
| [q117] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | INFO | Oak Security | Direct ownership transfer in auth-proxy and undelegations-manager allows accidental loss of contract control |
| [q118] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | INFO | Oak Security | Tick and Burn messages can be called by any address |
| [q119] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-08-18-audit-report-cosmwasm-wbtc-v1-0-pdf.md | LOW | Oak Security | Incorrect governor attribute value emitted |
| [q120] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-08-18-audit-report-cosmwasm-wbtc-v1-0-pdf.md | LOW | Oak Security | Separation of privileged addresses is not enforced |
| [q121] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-08-18-audit-report-cosmwasm-wbtc-v1-0-pdf.md | INFO | Oak Security | Attributes are not properly emitted during contract instantiation |
| [q122] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-08-18-audit-report-cosmwasm-wbtc-v1-0-pdf.md | INFO | Oak Security | Contracts should implement a two-step ownership transfer |
| [q123] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | LOW | Oak Security | Missing validation steps when registering limiters |
| [q124] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Missing Division invariant check |
| [q125] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Redundant query function |
| [q126] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Lack of role-based access controls for the pausing mechanism |
| [q127] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Default value conceals unexpected state |
| [q128] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Usage of vulnerable dependencies |
| [q129] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase2-pdf.md | INFO | Informal Systems | Unprincipled use of OOP concepts has likely created technical debt |
| [q130] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase2-pdf.md | INFO | Informal Systems | Make the code in gc-actions.js easier to understand |
| [q131] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase2-pdf.md | INFO | Informal Systems | Do not overload isReachableFlag |
| [q132] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase2-pdf.md | INFO | Informal Systems | retireImports dispatch does not have any effect on liveslots |
| [q133] | reports/cosmos-l1-nodes_findings/audits-agoric-informal-agoric-report-phase2-pdf.md | INFO | Informal Systems | Check the correctness of the retireImports syscall code with respect to timing |
| [q134] | reports/cosmos-l1-nodes_findings/audits-axelar-2023-08-04-audit-report-axelar-axelarnet-pdf.md | INFO | Informal Systems | IF-AXELAR-01: Various Minor Code Improvements |
| [q135] | reports/cosmos-l1-nodes_findings/audits-axelar-2023-08-04-audit-report-axelar-axelarnet-pdf.md | INFO | Informal Systems | IF-AXELAR-02: Event is not emitted for executed RouteMessage |
| [q136] | reports/cosmos-l1-nodes_findings/audits-axelar-2023-08-04-audit-report-axelar-axelarnet-pdf.md | LOW | Informal Systems | IF-AXELAR-04: Additional queries over nexus module for better UX |
| [q137] | reports/cosmos-l1-nodes_findings/audits-axelar-2023-08-04-audit-report-axelar-axelarnet-pdf.md | LOW | Informal Systems | IF-AXELAR-07: Current rate limits design could be improved |
| [q138] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-haqq-coinomics-module-cosmos-security-assessment-report-halborn-final-pdf.md | LOW | Halborn | USE OF VULNERABLE DEPENDENCIES |
| [q139] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-maker-contract-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISUSE OF HELPER METHODS |
| [q140] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-delta-neutral-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | LACK OF ADDRESS NORMALIZATION |
| [q141] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-delta-neutral-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | MISSING BOUNDS ON CONFIGURATION VARIABLES |
| [q142] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-delta-neutral-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | MISSING DEDICATED ROLES TO MANAGE CONTRACT STATUS |
| [q143] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-delta-neutral-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | UNUSED CONFIG VARIABLE |
| [q144] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-delta-neutral-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | NO CONVENTION IN VARIABLE TYPES |
| [q145] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-delta-neutral-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | UNMANTAINED DEPENDENCY |
| [q146] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-long-term-bonding-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | LACK OF ADDRESS NORMALIZATION |
| [q147] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-long-term-bonding-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | UNMANTAINED DEPENDENCY |
| [q148] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-stader-labs-sd-token-staking-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | LACK OF MANAGER TRANSFER FUNCTIONALITY |
| [q149] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-stader-labs-sd-token-staking-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | MISSING BOUNDS ON CONFIGURATION VARIABLES |
| [q150] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-stader-labs-sd-token-staking-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | LACK OF ADDRESS NORMALIZATION |
| [q151] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-stader-labs-sd-token-staking-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | INFO | Halborn | CONFIGURATION PARAMETER NOT SET UPON INSTANTIATION |
| [q152] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-hana-library-audit-report-final-v2-pdf.md | LOW | Informal Systems | Hana Library Unnecessary panic upon failed verification |
| [q153] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-hana-library-audit-report-final-v2-pdf.md | INFO | Informal Systems | Hana Library Blob header not fully verified |
| [q154] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-hana-library-audit-report-final-v2-pdf.md | INFO | Informal Systems | Hana Library Miscellaneous code findings |
| [q155] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-hana-library-audit-report-final-v2-pdf.md | LOW | Informal Systems | Unnecessary panic upon failed verification |
| [q156] | reports/cosmos-l1-nodes_findings/audits-thorchain-coinfabrik-thorchain-audit-2024-01-pdf.md | LOW | CoinFabrik | Regtest App Denial Of Service |
| [q157] | reports/cosmos-l1-nodes_findings/publicauditreports-nm0405-final-gaia-network-token-pdf.md | LOW | Nethermind | Summary of Issues Finding Severity Update 1 Cancellation in GaiaTimelock can’t be called from the GaiaGovernor |
| [q158] | reports/cosmos-l1-nodes_findings/publicauditreports-nm0405-final-gaia-network-token-pdf.md | LOW | Nethermind | Safeguarding Contract Operations by Disabling Ownership Renouncement |
| [q159] | reports/cosmos-l1-nodes_findings/publicauditreports-nm0405-final-gaia-network-token-pdf.md | LOW | Nethermind | GaiaToken cannot be paused |
| [q160] | reports/cosmos-l1-nodes_findings/publicauditreports-nm0405-final-gaia-network-token-pdf.md | LOW | Nethermind | GaiaToken extendsPausable but does not add pausable functionality |

## Validation Missing

**Validation missing patterns mined from uncited L1 audit reports** - representative of 71 findings mined from 44 L1 audit reports (Halborn, Informal Systems, Oak Security, Trail of Bits, Zellic).

### Overview

71 sec-tier findings (14 critical, 38 high, 19 medium) from 44 audit reports by Halborn, Informal Systems, Oak Security, Trail of Bits, Zellic. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the extrinsic input validation path lacks the validation/bounding the cited reports identify."
- Pattern key: `validation-gap | extrinsic | crafted input | invalid state accepted`
- Interaction scope: `single_contract`
- Primary affected component(s): `extrinsic input validation`
- High-signal code keywords: `accepts, account, accounting, acknowledged, acknowledgement, active`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (extrinsic input validation)
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security, Trail of Bits, Zellic)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- accepts
- account
- accounting
- acknowledged
- acknowledgement
- active
- adaptor
- adddistributor
- adding
- addresses
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe extrinsic input validation paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `validation-gap | extrinsic | crafted input | invalid state accepted`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `validation-gap | extrinsic | crafted input | invalid state accepted | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `validation-gap | extrinsic | crafted input | invalid state accepted | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Attackers can bypass self-migration validation to control assembly contract** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can bypass self-migration validation to control assembly contract
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can bypass self-migration validation to control assembly contract
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: ProcessProposal accepts all proposals without validating vote extensions** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// ProcessProposal accepts all proposals without validating vote extensions
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: ProcessProposal accepts all proposals without validating vote extensions
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Unbounded iteration allows attackers to attack validators, slowing down or even halting block production** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Unbounded iteration allows attackers to attack validators, slowing down or even halting block production
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Unbounded iteration allows attackers to attack validators, slowing down or even halting block produc
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Wrong accounting / reward misallocation / stuck or double-counted funds (fund-loss class rows above)
- State inconsistency after partial failure (see error-handling references)
- Chain halt or node crash from unbounded work (see DoS rows)

#### Business Impact
- User fund loss and withdrawal freezes; validator downtime; consensus/partition risk for client-level bugs.

### Secure Implementation

**Fix 1: [Bound and validate at the entry surface]**
```rust
// ✅ SECURE: explicit bounds + validation before state mutation
fn handler(input: UntrustedInput) -> Result<(), Error> {
    ensure!(input.len() <= T::MaxInput::get(), Error::TooLarge);
    ensure!(is_valid(&input), Error::Invalid);
    state.update_checked(&input)?;
    Ok(())
}
```

**Fix 2: [Aggregate instead of iterate; cap growth]**
```rust
// ✅ SECURE: keep block-time work O(1) and cap attacker growth
fn on_block_end() {
    let aggregate = Aggregates::get();          // maintained incrementally
    distribute(&aggregate);                      // no unbounded iteration
}
fn create_plan(p: Plan) -> Result<(), Error> {
    ensure!(PlansCount::get() < T::MaxPlans::get(), Error::TooManyPlans);
    Ok(())
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Entry surface writes state before validating attacker-controlled fields
- Block-time hooks iterate collections whose size is attacker-influenceable
- Multi-step handlers where a mid-step failure leaves earlier writes committed
- Config setters without role checks or bounds
```

#### Audit Checklist
- [ ] Verify every attacker-reachable input is length/bounds-checked before state writes
- [ ] Verify block-time (end-blocker / on_finalize) iteration is O(1) or capped
- [ ] Verify failure paths roll back partial state mutations
- [ ] Cross-check the cited reports' fix status before re-reporting

### Keywords for Search

`accepts, account, accounting, acknowledged, acknowledgement, active, adaptor, adddistributor, adding, addresses, admins, agents, allow, allows`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
