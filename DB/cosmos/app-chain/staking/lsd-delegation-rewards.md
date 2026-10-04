---
# Core Classification
protocol: generic
chain: cosmos
category: staking
vulnerability_type: delegation_reward_accounting
root_cause_family: accounting_error

# Pattern Identity
pattern_key: delegation-accounting-gap | staking/LSD module | epoch transition or claim | wrong rewards or stuck funds

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - staking module / LSD vault contracts

# Attack Vector Details
attack_type: logical_error
affected_component: staking module / LSD vault contracts

# Technical Primitives
primitives:
  - account
  - accounting
  - accrued
  - accruing
  - acknowledged
  - actionamount

# Grep / Hunt-Card Seeds
code_keywords:
  - account
  - accounting
  - accrued
  - accruing
  - acknowledged
  - actionamount
  - active
  - adding
  - address
  - advantages

severity: critical
impact: fund_loss
language: rust
tags:
  - staking
  - l1
  - cosmos
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [k1] | reports/cosmos-l1-nodes_findings/audit-reports-all-in-bits-2022-04-04-audit-report-budget-and-farming-cosmos-sdk-modules-v1-0-pdf.md | CRITICAL | Oak Security | Iteration over queued stakings in end blocker can be exploited to halt block production |
| [k2] | reports/cosmos-l1-nodes_findings/audit-reports-all-in-bits-2022-04-04-audit-report-budget-and-farming-cosmos-sdk-modules-v1-0-pdf.md | CRITICAL | Oak Security | Unbounded staking and epoch amount coins can be exploited to halt block production |
| [k3] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | CRITICAL | Oak Security | The delegation slot is not decreased when losses are detected |
| [k4] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Incorrect UnbondReadyStatusResponse returned causes the vault contract to fail to start unbonding |
| [k5] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Rewards are not increased for zero fees or empty fee recipient |
| [k6] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Delegation rewards computed will be zero if MsgUndelegate is called |
| [k7] | reports/cosmos-l1-nodes_findings/audit-reports-amulet-2024-02-07-audit-report-amulet-neutron-pos-strategy-v1-0-pdf.md | HIGH | Oak Security | Incorrect claim amount calculation |
| [k8] | reports/cosmos-l1-nodes_findings/audit-reports-autonomy-2023-03-06-audit-report-autonomy-osmosis-v1-1-pdf.md | HIGH | Oak Security | Unstake transactions are likely to fail if more than one of them is processed in the same block |
| [k9] | reports/cosmos-l1-nodes_findings/audit-reports-babylon-2025-06-12-audit-report-babylon-v1-0-pdf.md | HIGH | Oak Security | Retrieving staking transactions using incorrect page increments results in skipped transactions |
| [k10] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-10-28-audit-report-comdex-locking-and-vesting-contracts-v1-0-pdf.md | CRITICAL | Oak Security | Multiple rounding issues may cause zero rewards being distributed |
| [k11] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | CRITICAL | Oak Security | Permissionless Rewards module Whitelisting process allows attackers to manipulate the Asset Whitelist and App Vault Whitelist |
| [k12] | reports/cosmos-l1-nodes_findings/audit-reports-comdex-2022-12-07-audit-report-comdex-v1-0-pdf.md | HIGH | Oak Security | Whitelisted assets for rewards get overwritten when adding new assets, which may cause unexpected behavior |
| [k13] | reports/cosmos-l1-nodes_findings/audit-reports-cosmos-2023-06-23-audit-report-cosmos-interchain-security-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can DOS attack consumer chains by sending multiple coins to the provider chain's reward address |
| [k14] | reports/cosmos-l1-nodes_findings/audit-reports-croncat-2023-03-14-audit-report-croncat-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Agents can bypass task delegation mechanism |
| [k15] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | ClaimProof does not include beneficiary address, which allows front-running of airdrops |
| [k16] | reports/cosmos-l1-nodes_findings/audit-reports-ibcx-2023-04-29-audit-report-ibcx-v1-0-pdf.md | CRITICAL | Oak Security | The same claim proof can be used multiple times |
| [k17] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Tokenization of a delegation and selling the shares allows evasion of slashes |
| [k18] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Withdrawal of tokenized share record rewards is unbounded, owner can be grieved by an attacker |
| [k19] | reports/cosmos-l1-nodes_findings/audit-reports-interchain-foundation-2022-07-20-audit-report-liquidity-staking-cosmos-sdk-modules-v1-0-pdf.md | HIGH | Oak Security | Tokenize share record reward query does not include automatically withdrawn rewards |
| [k20] | reports/cosmos-l1-nodes_findings/audit-reports-lido-finance-2022-05-16-audit-report-lido-finance-statom-on-cosmos-hub-v1-0-pdf.md | HIGH | Oak Security | Unbounded unbond history entries may cause all deposited funds stuck in the hub contract |
| [k21] | reports/cosmos-l1-nodes_findings/audit-reports-lido-finance-2022-05-16-audit-report-lido-finance-statom-on-cosmos-hub-v1-0-pdf.md | HIGH | Oak Security | Unbounded unbond wait entities may cause user funds to be stuck in hub contract |
| [k22] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-02-17-audit-report-fields-of-mars-v1-0-pdf.md | HIGH | Oak Security | Harvest message can be sandwiched to skim rewards |
| [k23] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2022-02-17-audit-report-mars-v1-0-pdf.md | CRITICAL | Oak Security | Staking xMars rewards can be sandwiched by an attacker, skimming its value before accruing to stakers |
| [k24] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-01-13-audit-report-mars-outposts-v1-0-pdf.md | HIGH | Oak Security | Swapping assets in the reward collector contract are vulnerable to sandwich attack |
| [k25] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-02-03-audit-report-mars-periphery-v1-0-pdf.md | HIGH | Oak Security | Smart contracts holding tokens on Terra classic cannot claim their airdrop |
| [k51] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | HIGH | Oak Security | Removing whitelisted denoms causes leftover rewards to get stuck |
| [k52] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2023-08-01-audit-report-mars-red-bank-updates-v1-0-pdf.md | HIGH | Oak Security | Incentive rewards might be distributed to depositors outside the epoch period |
| [k53] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | CRITICAL | Oak Security | Total liquidity tokens are incorrectly increased, causing lower rewards |
| [k54] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | HIGH | Oak Security | Liquidatee's staking rewards are lost |
| [k55] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-07-15-audit-report-mars-v2-on-neutron-v1-0-pdf.md | HIGH | Oak Security | Incorrect liquidity tokens unstaked for ActionAmount::Exact |
| [k56] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-12-04-audit-report-mars-perps-v1-0-pdf.md | CRITICAL | Oak Security | Incorrect migration guard unlock causes failed migration and loss of rewards |
| [k57] | reports/cosmos-l1-nodes_findings/audit-reports-mars-2024-12-04-audit-report-mars-perps-v1-0-pdf.md | CRITICAL | Oak Security | Users will lose accrued rewards when withdrawing liquidity |
| [k58] | reports/cosmos-l1-nodes_findings/audit-reports-milkyway-2024-12-16-audit-report-milkyway-celestia-restaking-v1-0-pdf.md | CRITICAL | Oak Security | Vesting tokens will not be burnt if the user performs full undelegation |
| [k59] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | CRITICAL | Oak Security | Validators receive lesser rewards due to incorrect reward denom |
| [k60] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validator rewards are lost if the payment schedule is updated |
| [k61] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Failure to update user stake may cause excess reward distribution |
| [k62] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Incorrect stake retrieval for LST protocols leads to zero rewards |
| [k63] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validators with significant voting power could censor others to prevent them from receiving rewards |
| [k64] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2025-03-25-audit-report-neutron-independent-chain-v1-0-pdf.md | HIGH | Oak Security | Validators can manipulate oracle prices to maximize rewards |
| [k65] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | ValidatorDstAddress may equal ValidatorSrcAddress in redelegation messages, causing upgrade failure |
| [k66] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | calcRedelegations uses delegation shares as token amounts, producing incorrect results when validators have been slashed |
| [k67] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-2-pdf.md | HIGH | Oak Security | Incorrect BeginBlocker ordering leading to inconsistent reward accounting |
| [k68] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2022-01-20-audit-report-persistence-bridge-v1-0-pdf.md | CRITICAL | Oak Security | Unbonding of all funds will fail |
| [k69] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | CRITICAL | Oak Security | Incorrect bookkeeping of validator's delegated amount upon redelegation |
| [k70] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | CRITICAL | Oak Security | Attackers can prevent users from liquid-staking funds by removing the Deposit entry |
| [k71] | reports/cosmos-l1-nodes_findings/audit-reports-persistence-2024-01-26-audit-report-pstake-native-auto-compounding-and-rebalancing-v1-0-pdf.md | HIGH | Oak Security | The rewards account balance is not updated on OnChanOpenAck |
| [k72] | reports/cosmos-l1-nodes_findings/audit-reports-sei-2023-05-19-audit-report-sei-chain-and-cosmwasm-v1-0-pdf.md | HIGH | Oak Security | Contract claiming is not possible due to a logic error |
| [k73] | reports/cosmos-l1-nodes_findings/audit-reports-starterra-audit-report-starterra-pdf.md | HIGH | Oak Security | Missing input validation on staking config update might lead to inconsistent state |
| [k74] | reports/cosmos-l1-nodes_findings/audit-reports-structured-2025-12-24-audit-report-structured-cosmwasm-and-solana-updates-v1-0-pdf.md | HIGH | Oak Security | Oversized unlocks allow overpayment and cross-batch imbalance in claim logic |
| [k75] | reports/cosmos-l1-nodes_findings/audits-celestia-celestia-q2-2025-cip-31-audit-report-final-pdf.md | HIGH | Informal Systems | Celestia Q2 2025 Vesting Schedule Not Updated on Reward Claim After Unbonding |
| [k76] | reports/cosmos-l1-nodes_findings/audits-cosmos-hub-2023-02-10-audit-report-ics-replicated-security-pdf.md | HIGH | Informal Systems | Interchain Security v.1.0 A byzantine consumer can tombstone, slash, or jail an innocent validator |
| [k77] | reports/cosmos-l1-nodes_findings/audits-evmos-informal-evmos-report-2021q4-pdf.md | HIGH | Informal Systems | Delegating 10ˆ6 * 2ˆ63 - x for a small x halts consensus |
| [k78] | reports/cosmos-l1-nodes_findings/gaia-contrib-audits-liquid-zellic-audit-25-pdf.md | MEDIUM | Informal Systems | Missing enforcement of MinSelfDelegation allows zero self-delegation for validators |
| [k79] | reports/cosmos-l1-nodes_findings/gaia-contrib-audits-liquid-zellic-audit-25-pdf.md | MEDIUM | Informal Systems | Blacklist bypass in reward withdrawal via TransferTokenizeShareRecord |
| [k80] | reports/cosmos-l1-nodes_findings/interchain-security-docs-audits-informal-ics-2023-pdf.md | HIGH | Informal Systems | Interchain Security v.1.0 A byzantine consumer can tombstone, slash, or jail an innocent validator |
| [k81] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Slashed finality provider restoring voting power through pending delegations |
| [k82] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Arbitrary Deduction of T otal Bond Satoshi from Expiring Delegation Handling |
| [k83] | reports/cosmos-l1-nodes_findings/publications-babylon-genesis-chain-zellic-audit-report-pdf.md | CRITICAL | Zellic | Incorrect Delegation Status Check Leading to Chain Halt |
| [k84] | reports/cosmos-l1-nodes_findings/publications-babylon-zellic-audit-report-pdf.md | MEDIUM | Zellic | Invalid creation of unbonding TX leads to loss of gas |
| [k85] | reports/cosmos-l1-nodes_findings/publications-trufin-injective-staker-zellic-audit-report-pdf.md | MEDIUM | Zellic | Unstake could be blocked for certain users |
| [k86] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-amm-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | UPDATING A CONFIG PARAMETER AFFECTS PAST REWARDS |
| [k87] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-astroport-fi-periphery-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO WITHDRAW TERRASWAP LP TOKENS AFTER CLAIMING REWARDS |
| [k88] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | BBRO TOKENS ARE LOST WHEN UNSTAKING OR CLAIMING REWARDS |
| [k89] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | BBRO REWARDS SCHEMA COULD PRODUCE UNFAIR ADVANTAGES |
| [k90] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | REWARDS BONDING FUNCTIONALITY IS UNAVAILABLE |
| [k91] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | HIGH | Halborn | WITHOUT POSSIBILITY TO SWAP ALL NATIVE TOKENS TO REWARD DENOMINATION |
| [k92] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | INADEQUATE TRACKING OF PENDING REDELEGATIONS |
| [k93] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-kryptonite-protocol-cosmwasm-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | REDELEGATION IS NOT RESTRICTED TO ACTIVE VALIDATORS |
| [k94] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-mars-protocol-core-contracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | TOTAL MARS FOR CLAIMERS IS MISCALCULATED WHEN TRANSFERRING MARS TOKENS |
| [k95] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-nexus-protocol-cosmwasm-smart-contract-security-audit-report-halborn-v1-1-pdf.md | HIGH | Halborn | MISCALCULATION OF BALANCE LEADS TO OVERRATED REWARDS DISTRIBUTION |
| [k96] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | REWARDS CANNOT BE CLAIMED WHEN REWARD POOLS ARE CLOSED |
| [k97] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-sienna-network-rewards-v3-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | POSSIBILITY TO TRANSFER AN ARBITRARY AMOUNT OF TOKENS OUT OF REWARD POOLS |
| [k98] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | WITHDRAWAL OF ARBITRARY PARTICIPATION REWARDS WITHOUT DEPOSITING COLLATERALS |
| [k99] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | BALANCE DOES NOT UPDATE WHEN USERS CLAIM REWARDS |
| [k100] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | USERS CAN PARTICIPATE IN CAMPAIGNS EVEN IF THERE ARE NOT ENOUGH REWARDS |
| [k101] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-valkyrie-protocol-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | FUNCTION TO UPDATE STAKING CONFIG DOES NOT WORK PROPERLY |
| [k102] | reports/cosmos-l1-nodes_findings/v4-chain-audits-informal-systems-audit-report-phase-iii-pdf.md | MEDIUM | Informal Systems | Missing validation of x/rewards parameters in MsgUpdateParams |
| [k103] | reports/cosmos-l1-nodes_findings/audits-apex-apex-q1-2025-reactor-skyline-critical-path-audit-report-final-pdf.md | MEDIUM | Informal Systems | The system heavily depends on external Gouroboros library Implementation High Patched Without Reaudit Quorum may be reached for multiple refund reques |
| [k104] | reports/cosmos-l1-nodes_findings/audits-babylon-babylon-q2-2025-genesis-v2-upgrade-audit-report-final-pdf.md | MEDIUM | Informal Systems | VIG - Suggestion to track UNBONDED and EXPIRED delegation statuses in Vigilante Protocol Informational Acknowledged BAB - Missing validation for halti |
| [k105] | reports/cosmos-l1-nodes_findings/audits-ibc-go-report-pdf.md | MEDIUM | auditor | Wrong usage of unbonding period |
| [k106] | reports/cosmos-l1-nodes_findings/audits-ibc-go-report-pdf.md | HIGH | auditor | Malicious IBC app module can claim any port or channel capability |
| [k107] | reports/cosmos-l1-nodes_findings/audits-neutron-2024-03-21-liquidity-migration-audit-report-pdf.md | HIGH | Informal Systems | Reward amounts in lockdrop-pcl contract are miscalculated in case of time-extended migration Type Implementation Severity 3 High Impact 3 |
| [z108] | reports/cosmos-l1-nodes_findings/publicreports-cosmwasm-smart-contract-audits-stader-labs-lunax-contrracts-cosmwasm-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MANAGER ADDRESS CANNOT BE TRANSFERRED |
| [z109] | reports/cosmos-l1-nodes_findings/publicreports-solidity-smart-contract-audits-persistence-stkbnb-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | USAGE OF SELF-DESTRUCT MAY LEAD TO FUNDS LOSS |
| [q110] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | LOW | Oak Security | tick_period_seconds can be set too low  risking unbonding entry exhaustion and denial of undelegation |
| [q111] | reports/cosmos-l1-nodes_findings/audit-reports-neutron-2026-04-09-audit-report-neutron-auction-and-undelegations-contract-chain-upgrade-phase-2-report-1-pdf.md | INFO | Oak Security | Incomplete pagination handling leads to delegation starvation and state inconsistency |

## Lsd Delegation Rewards

**Lsd delegation rewards patterns mined from uncited L1 audit reports** - representative of 81 findings mined from 46 L1 audit reports (Halborn, Informal Systems, Oak Security, Zellic, unknown).

### Overview

81 sec-tier findings (21 critical, 48 high, 12 medium) from 46 audit reports by Halborn, Informal Systems, Oak Security, Zellic, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the staking module / LSD vault contracts path lacks the validation/bounding the cited reports identify."
- Pattern key: `delegation-accounting-gap | staking/LSD module | epoch transition or claim | wrong rewards or stuck funds`
- Interaction scope: `multi_contract`
- Primary affected component(s): `staking module / LSD vault contracts`
- High-signal code keywords: `account, accounting, accrued, accruing, acknowledged, actionamount`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (staking module / LSD vault contracts)
- Signal 2: severity consensus across independent auditors (Halborn, Informal Systems, Oak Security, Zellic, unknown)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- account
- accounting
- accrued
- accruing
- acknowledged
- actionamount
- active
- adding
- address
- advantages
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe staking module / LSD vault contracts paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `delegation-accounting-gap | staking/LSD module | epoch transition or claim | wrong rewards or stuck funds`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `delegation-accounting-gap | staking/LSD module | epoch transition or claim | wrong rewards or stuck funds | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `delegation-accounting-gap | staking/LSD module | epoch transition or claim | wrong rewards or stuck funds | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Iteration over queued stakings in end blocker can be exploited to halt block production** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Iteration over queued stakings in end blocker can be exploited to halt block production
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Iteration over queued stakings in end blocker can be exploited to halt block production
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Unbounded staking and epoch amount coins can be exploited to halt block production** [Approx Vulnerability : CRITICAL]
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
**Example 3: The delegation slot is not decreased when losses are detected** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// The delegation slot is not decreased when losses are detected
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: The delegation slot is not decreased when losses are detected
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

`account, accounting, accrued, accruing, acknowledged, actionamount, active, adding, address, advantages, affects, after, agents, airdrop`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
