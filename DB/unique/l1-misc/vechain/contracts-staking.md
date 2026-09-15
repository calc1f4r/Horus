---
# Core Classification
protocol: generic
chain: vechain
category: vechain
vulnerability_type: vechain_contracts
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: vechain-contracts | vechain contracts | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - vechain contracts

# Attack Vector Details
attack_type: varies
affected_component: vechain contracts

# Technical Primitives
primitives:
  - accounting
  - accrue
  - accumulate
  - accumulation
  - active
  - after

# Grep / Hunt-Card Seeds
code_keywords:
  - accounting
  - accrue
  - accumulate
  - accumulation
  - active
  - after
  - allows
  - attacker

severity: high
impact: varies
language: varies
tags:
  - vechain
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [v1] | reports/vechain-l1_findings/59316-sc-high-off-by-one-unlocks-infinite-vtho-reward-drain-from-ghost-stakes.md | HIGH | Immunefi (flora) | sc high off by one unlocks infinite vtho reward drain from ghost stakes |
| [v2] | reports/vechain-l1_findings/59361-sc-high-off-by-one-in-claimabledelegationperiods-allows-claimrewards-to-pay-for-periods-after.md | HIGH | Immunefi (daxun) | sc high off by one in claimabledelegationperiods allows claimrewards to pay for periods after delegation end over claim theft of unclaimed yield |
| [v3] | reports/vechain-l1_findings/59615-sc-high-off-by-one-error-in-period-boundary-check-allows-theft-of-unclaimed-yield-after-delega.md | HIGH | Immunefi (csanuragjain) | sc high off by one error in period boundary check allows theft of unclaimed yield after delegation exit |
| [v4] | reports/vechain-l1_findings/59665-sc-high-delegators-can-claim-rewards-beyond-delegation-end.md | HIGH | Immunefi (warden) | sc high delegators can claim rewards beyond delegation end |
| [v5] | reports/vechain-l1_findings/59709-sc-high-post-exit-rewards-overpayment-theft-of-unclaimed-yield-due-to-misclamped-claim-window.md | HIGH | Immunefi (Queerantagonism) | sc high post exit rewards overpayment theft of unclaimed yield due to misclamped claim window in stargate |
| [v6] | reports/vechain-l1_findings/59776-sc-high-exited-delegators-can-over-claim-vtho-rewards-for-post-exit-periods-due-to-off-by-one.md | HIGH | Immunefi (jayx) | sc high exited delegators can over claim vtho rewards for post exit periods due to off by one error in claimabledelegationperiods |
| [v7] | reports/vechain-l1_findings/59809-sc-high-user-balances-are-permanently-frozen-in-specific-delegation-scenarios.md | HIGH | Immunefi (hrmneffdii) | sc high user balances are permanently frozen in specific delegation scenarios |
| [v8] | reports/vechain-l1_findings/59850-sc-high-users-funds-stuck-in-the-contract-permanently.md | HIGH | Immunefi (warden) | sc high users funds stuck in the contract permanently |
| [v9] | reports/vechain-l1_findings/59863-sc-high-over-claim-of-delegation-rewards-after-exit.md | HIGH | Immunefi (jo13) | sc high over claim of delegation rewards after exit |
| [v10] | reports/vechain-l1_findings/59919-sc-high-loss-of-funds-delegators-can-claim-rewards-for-periods-where-they-had-no-stake.md | HIGH | Immunefi (warden) | sc high loss of funds delegators can claim rewards for periods where they had no stake |
| [v11] | reports/vechain-l1_findings/59951-sc-high-in-special-cases-delegatorseffectivestake-may-decrease-twice-and-cause-staked-funds-to.md | HIGH | Immunefi (shaflow1) | sc high in special cases delegatorseffectivestake may decrease twice and cause staked funds to become locked |
| [v12] | reports/vechain-l1_findings/60027-sc-high-stuck-funds-for-the-later-delegators-due-to-an-edge-case-led-to-double-decreasing-effe.md | HIGH | Immunefi (rzizah) | sc high stuck funds for the later delegators due to an edge case led to double decreasing effective stakes |
| [v13] | reports/vechain-l1_findings/60028-sc-high-a-delegator-who-has-requested-an-exit-continues-to-accumulate-rewards.md | HIGH | Immunefi (shaflow1) | sc high a delegator who has requested an exit continues to accumulate rewards |
| [v14] | reports/vechain-l1_findings/60049-sc-high-double-effective-stake-decrement-locks-delegators-unstake-reverts-due-to-duplicate-eff.md | HIGH | Immunefi (Johnyfwesh) | sc high double effective stake decrement locks delegators unstake reverts due to duplicate effectivestake decrements in exit flow |
| [v15] | reports/vechain-l1_findings/60069-sc-high-incorrect-claimable-period-calculation-leading-to-attacker-keep-claiming-even-after-ex.md | HIGH | Immunefi (Bizarro) | sc high incorrect claimable period calculation leading to attacker keep claiming even after exiting the delegation&#x20; |
| [v16] | reports/vechain-l1_findings/60081-sc-high-exited-delegator-can-continue-to-accrue-and-claim-delegation-rewards.md | HIGH | Immunefi (Diavol0) | sc high exited delegator can continue to accrue and claim delegation rewards&#x20; |
| [v17] | reports/vechain-l1_findings/60102-sc-high-exited-delegator-could-keep-claiming-rewards-stealing-them-from-active-delegators-whic.md | HIGH | Immunefi (rzizah) | sc high exited delegator could keep claiming rewards stealing them from active delegators which would then lead to freeze of funds |
| [v18] | reports/vechain-l1_findings/60151-sc-high-double-reduction-of-effective-stake-can-lead-to-stuck-delegations.md | HIGH | Immunefi (Bizarro) | sc high double reduction of effective stake can lead to stuck delegations&#x20; |
| [v19] | reports/vechain-l1_findings/60154-sc-high-exited-delegations-can-continue-claiming-vtho-rewards-for-future-periods.md | HIGH | Immunefi (incogknito) | sc high exited delegations can continue claiming vtho rewards for future periods |
| [v20] | reports/vechain-l1_findings/60169-sc-high-exited-delegations-can-continue-to-claim-rewards-due-to-logic-fall-through-in-claimabl.md | HIGH | Immunefi (ihtishamsudo) | sc high exited delegations can continue to claim rewards due to logic fall through in claimabledelegationperiods&#x20; |
| [v21] | reports/vechain-l1_findings/60173-sc-high-the-phantom-claimable-periods-can-permanently-lock-the-staked-vet-for-ended-delegation.md | HIGH | Immunefi (XDZIBECX) | sc high the phantom claimable periods can permanently lock the staked vet for ended delegations |
| [v22] | reports/vechain-l1_findings/60192-sc-high-users-can-claim-delegation-rewards-after-exit-endperiod-has-passed.md | HIGH | Immunefi (Rhaydden) | sc high users can claim delegation rewards after exit endperiod has passed |
| [v23] | reports/vechain-l1_findings/60241-sc-medium-permanent-freezing-of-staked-funds-caused-by-accumulation-with-zero-rewards.md | MEDIUM | Immunefi (Paludo0x) | sc medium permanent freezing of staked funds caused by accumulation with zero rewards |
| [v24] | reports/vechain-l1_findings/60298-sc-high-duplicate-effectivestake-decrement-path-bricks-unstake-re-delegate.md | HIGH | Immunefi (Rhaydden) | sc high duplicate effectivestake decrement path bricks unstake re delegate |
| [v25] | reports/vechain-l1_findings/60310-sc-high-incorrect-boundary-check-in-claimabledelegationperiods-allows-claiming-rewards-beyond.md | HIGH | Immunefi (Oxodus) | sc high incorrect boundary check in claimabledelegationperiods allows claiming rewards beyond delegation end period |
| [v51] | reports/vechain-l1_findings/60426-sc-high-rewards-accounting-off-by-one-skipped-double-period-exploit-leads-to-direct-loss-of-us.md | HIGH | Immunefi (decabrsky02) | sc high rewards accounting off by one skipped double period exploit leads to direct loss of user funds via incorrect reward distribution theft of uncl |
| [v52] | reports/vechain-l1_findings/60429-sc-high-double-decrease-of-effective-stake-prevents-delegators-from-unstaking.md | HIGH | Immunefi (Dliteofficial) | sc high double decrease of effective stake prevents delegators from unstaking |
| [v53] | reports/vechain-l1_findings/60431-sc-high-unauthorized-vtho-reward-claims-after-delegation-exit.md | HIGH | Immunefi (Dliteofficial) | sc high unauthorized vtho reward claims after delegation exit |
| [v54] | reports/vechain-l1_findings/60466-sc-medium-maxclaimableperiodsexceeded-lock-zero-reward-backlog-permanently-locks-nfts.md | MEDIUM | Immunefi (arunabha003) | sc medium maxclaimableperiodsexceeded lock zero reward backlog permanently locks nfts |
| [v55] | reports/vechain-l1_findings/60506-sc-high-double-delegatorseffectivestake-decrease-permanently-prevents-single-nft-from-unstakin.md | HIGH | Immunefi (cmds) | sc high double delegatorseffectivestake decrease permanently prevents single nft from unstaking |
| [v56] | reports/vechain-l1_findings/60516-sc-high-incorrect-boundary-check-in-claimabledelegationperiods-allows-claiming-rewards-beyond.md | HIGH | Immunefi (Oxodus) | sc high incorrect boundary check in claimabledelegationperiods allows claiming rewards beyond delegation end period |
| [v57] | reports/vechain-l1_findings/60575-sc-high-double-subtraction-of-delegator-effective-stake-on-exit-can-freeze-vet-and-break-rewar.md | HIGH | Immunefi (unineko) | sc high double subtraction of delegator effective stake on exit can freeze vet and break reward distribution |
| [v58] | reports/vechain-l1_findings/55957-sc-medium-checkstake-does-not-check-for-uint64-overflow.md | MEDIUM | Immunefi (Haxatron) | sc medium checkstake does not check for uint64 overflow |
| [v59] | reports/vechain-l1_findings/56611-bc-medium-remote-p2p-crash-during-sync-thor-default-configuration.md | MEDIUM | Immunefi (notGoku) | bc medium remote p2p crash during sync thor default configuration&#x20; |
| [v60] | reports/vechain-l1_findings/57055-bc-medium-dos-via-p2p-during-block-header-validation-using-bad-proof.md | MEDIUM | Immunefi (emarai) | bc medium dos via p2p during block header validation using bad proof |
| [v61] | reports/vechain-l1_findings/59421-sc-high-theft-of-unclaimed-yield-via-incorrect-period-range-calculation-and-lack-of-per-user-e.md | HIGH | Immunefi (oxadwa) | sc high theft of unclaimed yield via incorrect period range calculation and lack of per user effective stake tracking |
| [v62] | reports/vechain-l1_findings/59443-sc-high-rithmetic-underflow-in-effective-stake-accounting-causes-permanent-loss-of-funds.md | HIGH | Immunefi (flora) | sc high rithmetic underflow in effective stake accounting causes permanent loss of funds |
| [v63] | reports/vechain-l1_findings/59570-sc-medium-access-control-bypass-in-unstake-leads-to-permanent-freezing-of-funds.md | MEDIUM | Immunefi (Pelican26237) | sc medium access control bypass in unstake leads to permanent freezing of funds |
| [v64] | reports/vechain-l1_findings/59727-sc-high-double-decrease-dos-on-exit-permanent-unstake-revert.md | HIGH | Immunefi (OxPrince) | sc high double decrease dos on exit permanent unstake revert |
| [v65] | reports/vechain-l1_findings/59730-sc-high-permanent-dos-users-cannot-unstake-after-double-exit-scenario.md | HIGH | Immunefi (Max36935) | sc high permanent dos users cannot unstake after double exit scenario |
| [v66] | reports/vechain-l1_findings/59752-sc-high-off-by-one-bug-in-claimabledelegationperiods-allows-claiming-yield-for-periods-after-e.md | HIGH | Immunefi (Paludo0x) | sc high off by one bug in claimabledelegationperiods allows claiming yield for periods after exit |
| [v67] | reports/vechain-l1_findings/59997-sc-medium-claimrewards-fails-to-update-state-for-zero-value-periods-causing-permanent-fund-fre.md | MEDIUM | Immunefi (hunraj) | sc medium claimrewards fails to update state for zero value periods causing permanent fund freeze in unstake&#x20; |
| [v68] | reports/vechain-l1_findings/60004-sc-high-double-decrease-effective-stake-bug-in-unstake.md | HIGH | Immunefi (jo13) | sc high double decrease effective stake bug in unstake&#x20; |
| [v69] | reports/vechain-l1_findings/60372-sc-high-double-decrement-bug-effective-stake-underflow-permanently-locks-funds.md | HIGH | Immunefi (arunabha003) | sc high double decrement bug effective stake underflow permanently locks funds |
| [v70] | reports/vechain-l1_findings/60400-sc-high-off-by-one-in-claimabledelegationperiods-lets-claims-beyond-exit.md | HIGH | Immunefi (AgentJacker) | sc high off by one in claimabledelegationperiods lets claims beyond exit |
| [v71] | reports/vechain-l1_findings/60533-sc-high-overlap-which-will-lead-to-loss-of-fund.md | HIGH | Immunefi (Demelew) | sc high overlap which will lead to loss of fund |
| [v72] | reports/vechain-l1_findings/60557-sc-high-double-decrement-of-effective-stake-in-unstake-leads-to-dos-and-permanent-fund-lock.md | HIGH | Immunefi (xanony) | sc high double decrement of effective stake in unstake leads to dos and permanent fund lock |
| [v73] | reports/vechain-l1_findings/60586-sc-high-incorrect-double-reduction-of-effective-stake-in-stargate-sol.md | HIGH | Immunefi (T0nraq) | sc high incorrect double reduction of effective stake in stargate sol |
| [v74] | reports/vechain-l1_findings/60592-sc-high-users-are-unable-to-unstake-under-certain-conditions.md | HIGH | Immunefi (Filippo) | sc high users are unable to unstake under certain conditions |
| [w75] | reports/vechain-l1_findings/55806-bc-insight-critical-missing-input-validation-in-governance-parameter-allows-malicious-underflo.md | CRITICAL | Immunefi (warden) | bc insight critical missing input validation in governance parameter allows malicious underflow leading to permanent freeze of all dpos rewards |
| [q76] | reports/vechain-l1_findings/55524-bc-insight-null-body-transaction-submission-crashes-rpc-handler.md | INFO | Immunefi (humanitia) | bc insight null body transaction submission crashes rpc handler |
| [q77] | reports/vechain-l1_findings/55925-bc-insight-underpriced-supply-queries-enable-cheap-cpu-dos.md | INFO | Immunefi (spongebob) | bc insight underpriced supply queries enable cheap cpu dos |
| [q78] | reports/vechain-l1_findings/55926-bc-insight-totalsupply-overstates-circulating-vtho.md | INFO | Immunefi (spongebob) | bc insight totalsupply overstates circulating vtho |
| [q79] | reports/vechain-l1_findings/56045-bc-insight-block-packing-starvation-via-oversized-priority-transactions.md | INFO | Immunefi (OxPrince) | bc insight block packing starvation via oversized priority transactions |
| [q80] | reports/vechain-l1_findings/56403-bc-insight-there-is-a-problem-in-the-dpos-threshold-switch-undercounts-votes-at-hayabusa-activ.md | INFO | Immunefi (XDZIBECX) | bc insight there is a problem in the dpos threshold switch undercounts votes at hayabusa activation&#x20; |
| [q81] | reports/vechain-l1_findings/56626-bc-insight-trivial-renewallist-bloat-attack-exploits-unmetered-database-writes-to-increase-blo.md | INFO | Immunefi (OadeHack) | bc insight trivial renewallist bloat attack exploits unmetered database writes to increase block processing time risking bft disruption |
| [q82] | reports/vechain-l1_findings/56761-bc-insight-the-check-for-integer-overflow-in-the-function-staker-go-checkstake-is-incorrect.md | INFO | Immunefi (LeoFlint) | bc insight the check for integer overflow in the function staker go checkstake is incorrect |
| [q83] | reports/vechain-l1_findings/56946-bc-insight-the-code-comparing-two-big-in-pointers-for-equality-not-their-numeric-values.md | INFO | Immunefi (jesse03) | bc insight the code comparing two big in pointers for equality not their numeric values |
| [q84] | reports/vechain-l1_findings/57021-bc-insight-lack-of-panic-recovery-in-housekeeping-goroutine-creates-potential-for-denial-of-se.md | INFO | Immunefi (rionnaldi) | bc insight lack of panic recovery in housekeeping goroutine creates potential for denial of service |
| [q85] | reports/vechain-l1_findings/57468-bc-insight-there-is-an-issue-about-zero-vtho-generation-during-hayabusa-transition-period.md | INFO | Immunefi (XDZIBECX) | #57468 \[BC-Insight] there is an issue about zero vtho generation during hayabusa transition period |
| [q86] | reports/vechain-l1_findings/59244-sc-insight-missing-event-emission-on-critical-state-change.md | INFO | Immunefi (akioniace) | sc insight missing event emission on critical state change |
| [q87] | reports/vechain-l1_findings/59411-sc-insight-inconsistency-in-migratetokenmanager-in-terms-of-the-permitted-caller.md | INFO | Immunefi (Oxodus) | sc insight inconsistency in migratetokenmanager in terms of the permitted caller |
| [q88] | reports/vechain-l1_findings/59795-sc-low-free-boosts-for-levels-added-after-v3.md | LOW | Immunefi (OxPrince) | sc low free boosts for levels added after v3 |
| [q89] | reports/vechain-l1_findings/59814-sc-low-stargatenft-sol-addlevel-function-not-implement-updatelevelboostpriceperblock.md | LOW | Immunefi (ox9527) | sc low stargatenft sol addlevel function not implement updatelevelboostpriceperblock |
| [q90] | reports/vechain-l1_findings/59841-sc-low-the-newly-added-level-cannot-have-its-boost-price-set-because-the-updatelevelboostprice.md | LOW | Immunefi (shaflow1) | sc low the newly added level cannot have its boost price set because the updatelevelboostpriceperblock function is not exposed |
| [q91] | reports/vechain-l1_findings/59844-sc-insight-incorrect-and-misleading-events-when-adding-levels-in-stargatenft.md | INFO | Immunefi (blackgrease) | sc insight incorrect and misleading events when adding levels in stargatenft&#x20; |
| [q92] | reports/vechain-l1_findings/59993-sc-insight-unnecessary-call-to-get-balance-in-mintinglogic-boostonbehalfof.md | INFO | Immunefi (JJSOnChain) | sc insight unnecessary call to get balance in mintinglogic boostonbehalfof&#x20; |
| [q93] | reports/vechain-l1_findings/60079-sc-low-critical-historical-state-corruption-via-stale-checkpoints-leads-to-permanent-loss-of-f.md | LOW | Immunefi (kind0dev) | sc low critical historical state corruption via stale checkpoints leads to permanent loss of future yield |
| [q94] | reports/vechain-l1_findings/60149-sc-insight-revised-missing-input-validation-in-addlevels-can-break-multiple-staking-tier-invar.md | INFO | Immunefi (blackgrease) | sc insight revised missing input validation in addlevels can break multiple staking tier invariant in startgatenft&#x20; |
| [q95] | reports/vechain-l1_findings/60171-sc-low-levels-added-after-deployment-lack-boost-price-initialization-resulting-in-free-boostin.md | LOW | Immunefi (aman) | sc low levels added after deployment lack boost price initialization resulting in free boosting |
| [q96] | reports/vechain-l1_findings/60259-sc-low-malicious-user-can-bypass-maturity-period-for-newly-added-levels.md | LOW | Immunefi (warden) | sc low malicious user can bypass maturity period for newly added levels |
| [q97] | reports/vechain-l1_findings/60289-sc-low-misconfigured-level-with-maturityblocks-0-allows-skip-of-maturity-requirements-and-back.md | LOW | Immunefi (MoZi) | sc low misconfigured level with maturityblocks 0 allows skip of maturity requirements and backrun minting |
| [q98] | reports/vechain-l1_findings/60318-sc-low-zero-cost-boost-bypass-for-new-levels.md | LOW | Immunefi (dray) | sc low zero cost boost bypass for new levels |
| [q99] | reports/vechain-l1_findings/60335-sc-insight-missing-or-misleading-code-comments-causes-confusion-and-may-lead-to-unnecessary-co.md | INFO | Immunefi (KKam86) | sc insight missing or misleading code comments causes confusion and may lead to unnecessary code changes |
| [q100] | reports/vechain-l1_findings/60386-sc-low-missing-setter-for-boostpriceperblock-after-adding-new-nft-levels-can-allow-users-to-by.md | LOW | Immunefi (sedare) | sc low missing setter for boostpriceperblock after adding new nft levels can allow users to bypass intended staking boost |
| [q101] | reports/vechain-l1_findings/60525-sc-insight-levelcirculatingsupplyupdated-not-emitted-during-supply-changes.md | INFO | Immunefi (Rhaydden) | sc insight levelcirculatingsupplyupdated not emitted during supply changes |
| [q102] | reports/vechain-l1_findings/60527-sc-insight-delegationexitrequested-event-emits-inconsistent-exit-period-values.md | INFO | Immunefi (warden) | sc insight delegationexitrequested event emits inconsistent exit period values |
| [q103] | reports/vechain-l1_findings/60578-sc-low-zero-boost-fee-for-newly-added-levels-lets-users-skip-maturity-for-free-and-avoid-payin.md | LOW | Immunefi (unineko) | sc low zero boost fee for newly added levels lets users skip maturity for free and avoid paying intended vtho boost cost |
| [q104] | reports/vechain-l1_findings/60593-sc-low-no-mechanism-to-set-boostpriceperblock-for-levels-added-after-initialization.md | LOW | Immunefi (Brainiac5) | sc low no mechanism to set boostpriceperblock for levels added after initialization |
| [q105] | reports/vechain-l1_findings/60597-sc-low-hasrequestedexit-returns-true-for-not-just-requested-exits-but-also-delegations-that-ar.md | LOW | Immunefi (Brainiac5) | sc low hasrequestedexit returns true for not just requested exits but also delegations that are already exited |
| [q106] | reports/vechain-l1_findings/56256-bc-insight-redundant-sload-for-global-endorsement-parameter.md | INFO | Immunefi (warden) | Redundant sload for global endorsement parameter |
## Vechain Contracts

**vechain-contracts patterns mined from uncited L1 audit reports** - 32 sec-tier findings (0 critical / 30 high / 2 medium) across 32 files from Immunefi (Bizarro), Immunefi (Diavol0), Immunefi (Dliteofficial), Immunefi (Johnyfwesh), Immunefi (Oxodus), Immunefi (Paludo0x).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- accounting
- accrue
- accumulate
- accumulation
- active
- after
- allows
- attacker
```

### Vulnerability Description

#### Root Cause

The cited reports describe vechain contracts paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `vechain-contracts | vechain contracts | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `vechain-contracts | vechain contracts | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `vechain-contracts | vechain contracts | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: sc high off by one unlocks infinite vtho reward drain from ghost stakes** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high off by one unlocks infinite vtho reward drain from ghost stakes
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high off by one unlocks infinite vtho reward drain from ghost stakes
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: sc high off by one in claimabledelegationperiods allows claimrewards to pay for periods after delegation end over claim ** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high off by one in claimabledelegationperiods allows claimrewards to pay for periods after delegation end over claim theft of unclaimed yield
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high off by one in claimabledelegationperiods allows claimrewards to pay for periods after delega
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: sc high off by one error in period boundary check allows theft of unclaimed yield after delegation exit** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high off by one error in period boundary check allows theft of unclaimed yield after delegation exit
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high off by one error in period boundary check allows theft of unclaimed yield after delegation e
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

`accounting, accrue, accumulate, accumulation, active, after, allows, attacker, backlog, balances`

### Related Vulnerabilities

- Sibling entries under the same category folder
