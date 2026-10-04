---
# Core Classification
protocol: generic
chain: cosmos
category: tokens
vulnerability_type: denom_handling_error
root_cause_family: missing_validation

# Pattern Identity
pattern_key: denom-validation-gap | token handling | transfer/mint | wrong asset accounting

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - token/denom validation paths

# Attack Vector Details
attack_type: input_validation_bypass
affected_component: token/denom validation paths

# Technical Primitives
primitives:
  - account
  - actionamount
  - adding
  - address
  - addresses
  - affected

# Grep / Hunt-Card Seeds
code_keywords:
  - account
  - actionamount
  - adding
  - address
  - addresses
  - affected
  - after
  - airdrop
  - alignment
  - allow

severity: critical
impact: fund_loss
language: rust
tags:
  - tokens
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-all-in-bits-2022-04-04-audit-report-budget-and-farming-cosmos-sdk-modules-v1-0-pdf.md | CRITICAL | Oak Security | Unbounded staking and epoch amount coins can be exploited to halt block production |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-01-29-audit-report-astroport-on-osmosis-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can swap any token and drain funds from pools |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2024-05-22-audit-report-astroport-hub-neutron-migration-v1-0-pdf.md | HIGH | Oak Security | IBC transfers can be grieved, preventing old ASTRO tokens from being burned |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-axelar-audit-report-axelar-pdf.md | HIGH | Oak Security | Gateway contract address depend on token symbol only and might clash |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-10-28-audit-report-comdex-locking-and-vesting-contracts-v1-0-pdf.md | CRITICAL | Oak Security | PeriodicVesting is unintendedly releasing tokens to users |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | CosmWasm - Deposited funds of other denom will be stuck in the contract |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | HIGH | Oak Security | UpdateAssetsRecords is not enforcing a unique Denom for an Asset |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can DOS attack consumer chains by sending multiple coins to the provider chain's reward address |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Inability to inflate an asset caused by using the wrong coin denomination for swapping the reserve to asset |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Total supply is not correctly computed |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Inability to mint, burn and rebalance index tokens following the initial deflate rebalance trade |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | Burning index tokens via the periphery contract yields substantially fewer asset tokens |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | HIGH | Oak Security | Minting and burning index tokens interferes with rebalancing and can render rebalance finalization unachievable |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | HIGH | Oak Security | Tokens that are sent by mistake are not refunded when minting |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Tokenization of a delegation and selling the shares allows evasion of slashes |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Withdrawal of tokenized share record rewards is unbounded, owner can be grieved by an attacker |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Tokenize share record reward query does not include automatically withdrawn rewards |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-02-03-audit-report-mars-periphery-v1-0-pdf.md | HIGH | Oak Security | Smart contracts holding tokens on Terra classic cannot claim their airdrop |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-02-03-audit-report-mars-rover-updates-v1-0-pdf.md | HIGH | Oak Security | Vault deposits are not affected by delisted coins |
| [k20] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-02-03-audit-report-mars-rover-updates-v1-0-pdf.md | HIGH | Oak Security | account-nft 's contract UpdateConfig message cannot be executed after the minter role is transferred to credit-manager |
| [k21] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | CRITICAL | Oak Security | Missing denom validation when adding incentives could lead to insufficient funds error |
| [k22] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | HIGH | Oak Security | Removing whitelisted denoms causes leftover rewards to get stuck |
| [k23] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | HIGH | Oak Security | Updating base denom would cause incorrect price results |
| [k24] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | CRITICAL | Oak Security | Total liquidity tokens are incorrectly increased, causing lower rewards |
| [k25] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | HIGH | Oak Security | Users cannot stake new liquidity tokens on Astroport |
| [k52] | reports/cosmos-l1-nodes_findings/audit-reports-milkyway-2024-12-16-audit-report-milkyway-celestia-restaking-v1-0-pdf.md | CRITICAL | Oak Security | Vesting tokens will not be burnt if the user performs full undelegation |
| [k53] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | CRITICAL | Oak Security | Validators receive lesser rewards due to incorrect reward denom |
| [k54] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | CRITICAL | Oak Security | Misconfigured governance module permissions causing consensus-halting panic on deposit burn |
| [k55] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | calcRedelegations uses delegation shares as token amounts, producing incorrect results when validators have been slashed |
| [k56] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2022-01-20-audit-report-persistence-bridge-v1-0-pdf.md | CRITICAL | Oak Security | Mnemonic/seed phrase as well as a bearer token exists in the codebase |
| [k57] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2022-01-20-audit-report-persistence-bridge-v1-0-pdf.md | HIGH | Oak Security | Otherwise, we recommend returning an error. Status: Resolved 8. CASP API token can be read by any user on the machine |
| [k58] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | HIGH | Oak Security | Outdated validator exchange rates could result in inflated minting of liquid-staked tokens |
| [k59] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | HIGH | Oak Security | Incorrect comparison between shares and tokens |
| [k60] | reports/cosmos-l1-nodes_findings/audit-reports-stride-2022-09-26-audit-report-stride-v1-0-pdf.md | CRITICAL | Oak Security | GetHostZoneFromHostDenom incorrectly uppercases user input, which can be used to mint invalid assets |
| [k61] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Permissionless burn enables denom recreation failure and withdrawal DoS |
| [k62] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Minted fee amount can be manipulated in both directions |
| [k63] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Lack of exchange rate liveliness checks allows over-minting of MaxBTC |
| [k64] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Missing mint alignment check may cause a miscalculated AUM |
| [k65] | reports/cosmos-l1-nodes_findings/audit-reports-terra-liquidity-bootstrapping-pool-2021-12-23-audit-report-terra-liquidity-bootstrapping-pool-v1-0-pdf.md | CRITICAL | Oak Security | Pools with big but different token amounts allow attackers to extract free value with minimal cost |
| [k66] | reports/cosmos-l1-nodes_findings/audit-reports-yieldmos-2024-05-17-audit-report-yieldmos-outposts-osmosis-v1-0-pdf.md | HIGH | Oak Security | Incorrect denom validation in Compound message |
| [k67] | reports/cosmos-l1-nodes_findings/audit-reports-yieldmos-2024-05-17-audit-report-yieldmos-outposts-osmosis-v1-0-pdf.md | HIGH | Oak Security | Incorrect token_in parameter during simulations causes compounding to fail |
| [k68] | reports/cosmos-l1-nodes_findings/audits-anoma-2024-08-16-ibc-and-masp-integrations-final-report-pdf.md | CRITICAL | Informal Systems | Potential Token Loss Due to Refund Transaction Failures |
| [k69] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | HIGH | Informal Systems | Denom collisions can be exploited to steal user funds |
| [k70] | reports/cosmos-l1-nodes_findings/audits-duality-2023-05-16-audit-report-duality-dex-and-incentives-modules-pdf.md | MEDIUM | Informal Systems | Stakes querying not handling stakes with multiple coins |
| [k71] | reports/cosmos-l1-nodes_findings/publications-reviews-umee-pdf.md | HIGH | Trail of Bits | Risk of token/uToken exchange rate manipulation |
| [k72] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-a41-supernova-cosmos-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING VALIDATION ON THE HOST DENOM AND IBC DENOM |
| [k73] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-boostylabs-tricorn-bridge-server-golang-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | TOKENID IS HARD-CODED IN TRANSFERS |
| [k74] | reports/cosmos-l1-nodes_findings/publicreports-cosmos-audits-pocket-network-validator-wpokt-golang-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | POTENTIAL RISK OF int64 Nonce OVERFLOW IN FINDNONCE FUNCTION OF MintSignerRunner |
| [k75] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-periphery-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO WITHDRAW TERRASWAP LP TOKENS AFTER CLAIMING REWARDS |
| [k76] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO TRANSFER AN ARBITRARY AMOUNT OF TOKENS OUT OF SOME CONTRACTS |
| [k77] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | BBRO TOKENS ARE LOST WHEN UNSTAKING OR CLAIMING REWARDS |
| [k78] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | LOANS CAN BE REPAID WITHOUT SPENDING COINS |
| [k79] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | ARBITRARY MINTING OF COINS WITHOUT DEPOSITING COLLATERALS |
| [k80] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | ARBITRARY MINTING OF COINS USING FAKE CW20 TOKENS |
| [k81] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | ARBITRARY REPAYMENT OF COINS FROM LIQUIDATIONS |
| [k82] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | MISCALCULATION OF MAX LOAN TO VALUE WHEN MINTING COINS |
| [k83] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | WITHOUT POSSIBILITY TO SWAP ALL NATIVE TOKENS TO REWARD DENOMINATION |
| [k84] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | SOME FUNCTIONS RECEIVE MULTIPLE NATIVE COINS INSTEAD OF ONE |
| [k85] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS |
| [k86] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | SLASH EVENTS CAN BE OVERWRITTEN WHEN TRANSFERRING MARS TOKENS |
| [k87] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MARS TOKENS CAN GET LOCKED IN CONTRACT WHEN UNSTAKING |
| [k88] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | TOTAL MARS FOR CLAIMERS IS MISCALCULATED WHEN TRANSFERRING MARS TOKENS |
| [k89] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | TOKENS GET LOCKED WHEN TRANSFERRING TO UPPER-CASE ADDRESSES |
| [k90] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | RESTRICTION TO NOT SWAP MARS TOKENS CAN BE BYPASSED |
| [k91] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | POSSIBILITY TO DEPOSIT, REPAY OR LIQUIDATE WITH NATIVE COINS NOT REGISTERED IN STORAGE |
| [k92] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-nexus-protocol-cosmwasm-smart-contract-security-audit-report-halborn-v1-1-pdf.md | HIGH | Halborn | MISCALCULATION OF NASSET TOKENS TO MINT LEADS TO UNFAIR WITHDRAWING / DOS |
| [k93] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UNRESTRICTED CHANGES IN FEE RATES LEAD TO TOKENS LOSS / DOS |
| [k94] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | USERS CAN INCREASE THEIR STAKED TOKENS WITHOUT DEPOSITING |
| [k95] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO TRANSFER AN ARBITRARY AMOUNT OF TOKENS OUT OF REWARD POOLS |
| [k96] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | DEPOSITS GET LOCKED IN CAMPAIGN IF COLLATERAL DENOM IS NOT SPECIFIED |
| [k97] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO TRANSFER AN ARBITRARY AMOUNT OF VKR TOKENS FROM DISTRIBUTOR |
| [k98] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | COLLUDED STAKERS CAN TRANSFER VKR TOKENS OUTSIDE GOVERNANCE CONTRACT |
| [k99] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | NOT ENFORCING SLIPPAGE TOLERANCE COULD LEAD TOKENS LOSS |
| [k100] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-2024-q2-pdf.md | HIGH | Informal Systems | Shares should not be minted in case of depositing to a vault containing negative shares |
| [k101] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | Genesis v2 Upgrade GEN - Missing Minter validation in InitGenesis of x/mint module |
| [k102] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | GEN - Missing Minter validation in InitGenesis of x/mint module |
| [k103] | reports/cosmos-l1-nodes_findings/audits-interlay-informal-report-interlay-audit-2021q3-pdf.md | MEDIUM | Informal Systems | IF-INTERLAY2- MINTING Vault not banned precondition not enforced on minting tokens |
| [k104] | reports/cosmos-l1-nodes_findings/audits-ibc-go-report-pdf.md | HIGH | auditor | Token lost issue in the crossing hellos scenario |
| [k105] | reports/cosmos-l1-nodes_findings/audits-ibc-go-report-pdf.md | HIGH | auditor | Model-based Testing for Token Transfer Set of new artifacts to facilitate rigorous testing Informative Code IF-IBC-14 Panic on receiving multi-chain d |
| [k106] | reports/cosmos-l1-nodes_findings/audits-injective-informal-report-injective-audit-202106-pdf.md | MEDIUM | Informal Systems | Audit IF-INJECTIVE-08 When a spot market is demolished the outstanding sell or- ders (and their coins) are frozen #304 Status: Resolved |
| [q107] | reports/cosmos-l1-nodes_findings/audit-reports-astroport-2023-07-13-audit-report-astroport-concentrated-liquidity-pool-with-injective-orderbook-integration-v1-0-pdf.md | LOW | Oak Security | Lack of denom validation |
| [q108] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | LOW | Oak Security | tick_undelegation_amount accepts zero  causing undelegation messages with a zero coin amount |
| [q109] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-08-18-audit-report-cosmwasm-wbtc-v1-0-pdf.md | LOW | Oak Security | Approving mint requests does not ensure the requestor still holds the merchant role |
| [q110] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-08-18-audit-report-cosmwasm-wbtc-v1-0-pdf.md | INFO | Oak Security | GetMintRequestsCount and GetBurnRequestsCount query fails when there are no mint or burn requests |
| [q111] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | LOW | Oak Security | Lack of denom validation |
| [q112] | reports/cosmos-l1-nodes_findings/audit-reports-osmosis-labs-2023-10-09-audit-report-osmosis-transmuter-v1-0-pdf.md | INFO | Oak Security | Unoptimized zero amount burning or minting |
| [q113] | reports/cosmos-l1-nodes_findings/audits-axelar-2023-08-04-audit-report-axelar-axelarnet-pdf.md | INFO | Informal Systems | IF-AXELAR-08: Hardcoded denom issue on the devnets |
| [q114] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-cw-asset-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | LACK OF DENOM VALIDATION ON CHECKED ASSET |
| [q115] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-updated-code-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | LOW | Halborn | EQUIVALENCE BETWEEN MARS AND XMARS TOKENS CAN BE BROKEN |

## Token Denom

**Token denom patterns mined from uncited L1 audit reports** - representative of 80 findings mined from 40 L1 audit reports (Halborn, Informal Systems, Oak Security, Trail of Bits, unknown).

### Overview

80 sec-tier findings (24 critical, 43 high, 13 medium) from 40 audit reports by Halborn, Informal Systems, Oak Security, Trail of Bits, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the token/denom validation paths path lacks the validation/bounding the cited reports identify."
- Pattern key: `denom-validation-gap | token handling | transfer/mint | wrong asset accounting`
- Interaction scope: `single_contract`
- Primary affected component(s): `token/denom validation paths`
- High-signal code keywords: `account, actionamount, adding, address, addresses, affected`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (token/denom validation paths)
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security, Trail of Bits, unknown)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- account
- actionamount
- adding
- address
- addresses
- affected
- after
- airdrop
- alignment
- allow
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe token/denom validation paths paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `denom-validation-gap | token handling | transfer/mint | wrong asset accounting`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `denom-validation-gap | token handling | transfer/mint | wrong asset accounting | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `denom-validation-gap | token handling | transfer/mint | wrong asset accounting | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Unbounded staking and epoch amount coins can be exploited to halt block production** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Unbounded staking and epoch amount coins can be exploited to halt block production
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Unbounded staking and epoch amount coins can be exploited to halt block production
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Attackers can swap any token and drain funds from pools** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can swap any token and drain funds from pools
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can swap any token and drain funds from pools
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: PeriodicVesting is unintendedly releasing tokens to users** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// PeriodicVesting is unintendedly releasing tokens to users
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: PeriodicVesting is unintendedly releasing tokens to users
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

`account, actionamount, adding, address, addresses, affected, after, airdrop, alignment, allow, allows, amount, amounts, arbitrary`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
