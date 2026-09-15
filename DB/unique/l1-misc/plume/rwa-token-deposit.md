---
# Core Classification
protocol: generic
chain: plume
category: rwa
vulnerability_type: rwa_token_plume
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: rwa-token-plume | rwa token plume | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - rwa token plume

# Attack Vector Details
attack_type: varies
affected_component: rwa token plume

# Technical Primitives
primitives:
  - access
  - accrued
  - accumulation
  - active
  - added
  - address

# Grep / Hunt-Card Seeds
code_keywords:
  - access
  - accrued
  - accumulation
  - active
  - added
  - address
  - admin
  - after

severity: critical
impact: varies
language: varies
tags:
  - plume
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [p1] | reports/plume-l1_findings/49731-sc-high-theft-on-re-added-tokens.md | HIGH | Immunefi (oswald23321) | sc high theft on re added tokens |
| [p2] | reports/plume-l1_findings/49732-sc-medium-malicious-token-admin-can-permanently-block-setpurchasetoken.md | MEDIUM | Immunefi (magtentic) | sc medium malicious token admin can permanently block setpurchasetoken |
| [p3] | reports/plume-l1_findings/49854-sc-critical-dex-aggregator-partial-fill-token-loss.md | CRITICAL | Immunefi (Blobism) | sc critical dex aggregator partial fill token loss |
| [p4] | reports/plume-l1_findings/49863-sc-critical-dex-aggregator-erc20-token-theft.md | CRITICAL | Immunefi (Blobism) | sc critical dex aggregator erc20 token theft |
| [p5] | reports/plume-l1_findings/50252-sc-high-rounding-excess-yield-tokens-become-permanently-stuck-when-last-holder-is-yield-restri.md | HIGH | Immunefi (KlosMitSoss) | sc high rounding excess yield tokens become permanently stuck when last holder is yield restricted |
| [p6] | reports/plume-l1_findings/50340-sc-medium-any-arctoken-admin-can-block-the-setting-update-of-the-purchase-token-indefinitely.md | MEDIUM | Immunefi (avoloder) | sc medium any arctoken admin can block the setting update of the purchase token indefinitely&#x20; |
| [p7] | reports/plume-l1_findings/50735-sc-high-some-yield-tokens-will-be-stuck-in-contract-due-to-incorrect-lastprocessedindex-calcul.md | HIGH | Immunefi (maggie) | sc high some yield tokens will be stuck in contract due to incorrect lastprocessedindex calculation&#x20; |
| [p8] | reports/plume-l1_findings/50784-sc-high-any-arc-token-creator-can-upgrade-the-implementation.md | HIGH | Immunefi (jovi) | sc high any arc token creator can upgrade the implementation&#x20; |
| [p9] | reports/plume-l1_findings/50916-sc-high-token-creators-can-bypass-factory-upgrade-controls-via-wrong-code-implementation-of-de.md | HIGH | Immunefi (demonhat) | sc high token creators can bypass factory upgrade controls via wrong code implementation of default admin role in arctokenfactory sol&#x20; |
| [p10] | reports/plume-l1_findings/50937-sc-medium-non-zero-approve-pattern-causes-permanent-freeze-of-token-deposits-e-g-usdt-due-to-e.md | MEDIUM | Immunefi (Bug82427) | sc medium non zero approve pattern causes permanent freeze of token deposits e g usdt due to erc20 incompatibility |
| [p11] | reports/plume-l1_findings/51043-sc-medium-core-deposit-and-depositandbridge-functionality-in-tellerwithmultiassetsupportpredic.md | MEDIUM | Immunefi (perseverance) | sc medium core deposit and depositandbridge functionality in tellerwithmultiassetsupportpredicateproxy is non functional due to flawed sharelockperiod |
| [p12] | reports/plume-l1_findings/51197-sc-high-arc-token-owner-can-take-upgrader-role-for-themselves-lockout-the-factory-and-upgrade.md | HIGH | Immunefi (TeamJosh) | sc high arc token owner can take upgrader role for themselves lockout the factory and upgrade the contract without the knowledge of the factory |
| [p13] | reports/plume-l1_findings/51218-sc-high-oracle-callback-timing-vulnerability-causes-jackpot-prize-loss.md | HIGH | Immunefi (KlosMitSoss) | sc high oracle callback timing vulnerability causes jackpot prize loss |
| [p14] | reports/plume-l1_findings/51283-sc-critical-permanent-freeze-of-user-token-due-to-unhandled-partial-fill-refunds-for-swap-via.md | CRITICAL | Immunefi (perseverance) | sc critical permanent freeze of user token due to unhandled partial fill refunds for swap via 1inch in dexaggregatorwrapperwithpredicateproxy&#x20; |
| [p15] | reports/plume-l1_findings/51414-sc-high-attacker-can-drain-yield-by-transferring-tokens-to-other-address-in-yield-batch-distri.md | HIGH | Immunefi (TeamJosh) | sc high attacker can drain yield by transferring tokens to other address in yield batch distributions |
| [p16] | reports/plume-l1_findings/51456-sc-high-token-creator-can-revoke-the-upgrader-role-from-the-factory-in-order-to-avoid-upgrades.md | HIGH | Immunefi (warden) | sc high token creator can revoke the upgrader role from the factory in order to avoid upgrades |
| [p17] | reports/plume-l1_findings/51589-sc-high-tokencreator-retains-upgrade-rights-fix-remains-insufficient-finding-01-immunefi-repor.md | HIGH | Immunefi (Boraicho) | sc high tokencreator retains upgrade rights fix remains insufficient finding 01 immunefi report |
| [p18] | reports/plume-l1_findings/51613-sc-medium-yield-tokens-can-be-stuck-in-arctokenpurchase-plumestakingrewardtreasury-or-other-de.md | MEDIUM | Immunefi (WinSec) | sc medium yield tokens can be stuck in arctokenpurchase plumestakingrewardtreasury or other defi protocols when distributeyield is called&#x20; |
| [p19] | reports/plume-l1_findings/51754-sc-high-double-yield-distribution-via-token-transfers-between-distributeyieldwithlimit-calls.md | HIGH | Immunefi (KlosMitSoss) | sc high double yield distribution via token transfers between distributeyieldwithlimit calls |
| [p20] | reports/plume-l1_findings/51777-sc-medium-denial-of-service-on-depositandbridge-function-for-sharelockperiod-is-non-zero.md | MEDIUM | Immunefi (kaysoft) | sc medium denial of service on depositandbridge function for sharelockperiod is non zero |
| [p21] | reports/plume-l1_findings/51887-sc-medium-safeapprove-will-cause-revert-of-usdt-and-similar-erc20-token.md | MEDIUM | Immunefi (SAAJ) | sc medium safeapprove will cause revert of usdt and similar erc20 token |
| [p22] | reports/plume-l1_findings/51941-sc-high-token-creator-can-revoke-factory-s-upgrade-capability-permanently-blocking-upgrades.md | HIGH | Immunefi (Am3nh3l) | sc high token creator can revoke factory s upgrade capability permanently blocking upgrades |
| [p23] | reports/plume-l1_findings/52031-sc-medium-insufficient-access-control-in-token-sales-management-leads-to-permanent-griefing-at.md | MEDIUM | Immunefi (OxPrince) | sc medium insufficient access control in token sales management leads to permanent griefing attack |
| [p24] | reports/plume-l1_findings/52075-sc-medium-arctokenpurchase-contract-is-a-token-holder-and-may-be-yield-recipient.md | MEDIUM | Immunefi (Finlooz4) | sc medium arctokenpurchase contract is a token holder and may be yield recipient&#x20; |
| [p25] | reports/plume-l1_findings/52290-sc-medium-deposit-function-in-tellerwithmultiassetsupportpredicateproxy-is-completely-broken-d.md | MEDIUM | Immunefi (avoloder) | sc medium deposit function in tellerwithmultiassetsupportpredicateproxy is completely broken due to wrong share lock |
| [p51] | reports/plume-l1_findings/52397-sc-medium-repeated-approve-without-zero-reset-can-revert-on-nonstandard-erc20s-blocking-deposi.md | MEDIUM | Immunefi (Khay3) | sc medium repeated approve without zero reset can revert on nonstandard erc20s blocking deposits |
| [p52] | reports/plume-l1_findings/52439-sc-high-dust-accumulation-in-batched-yield-payouts-leaves-tokens-stranded.md | HIGH | Immunefi (Afriauditor) | sc high dust accumulation in batched yield payouts leaves tokens stranded |
| [p53] | reports/plume-l1_findings/52572-sc-high-a-legitimate-arc-token-holder-can-be-denied-his-yield.md | HIGH | Immunefi (swarun) | sc high a legitimate arc token holder can be denied his yield&#x20; |
| [p54] | reports/plume-l1_findings/52649-sc-high-token-creator-can-seize-upgrade-control-bypassing-factory-whitelist-and-enabling-theft.md | HIGH | Immunefi (hulkvision) | sc high token creator can seize upgrade control bypassing factory whitelist and enabling theft of funds |
| [p55] | reports/plume-l1_findings/52732-sc-medium-permanent-dos-of-purchase-token-change.md | MEDIUM | Immunefi (Afriauditor) | sc medium permanent dos of purchase token change |
| [p56] | reports/plume-l1_findings/52833-sc-high-bypass-the-fix-of-immunefi-audit-imm-crit-01-token-creator-can-upgrade-arctoken-implem.md | HIGH | Immunefi (r1ver) | sc high bypass the fix of immunefi audit imm crit 01 token creator can upgrade arctoken implementation |
| [p57] | reports/plume-l1_findings/52841-sc-medium-token-admin-can-dos-admin-to-not-let-admin-change-purchase-token.md | MEDIUM | Immunefi (ladboy233) | sc medium token admin can dos admin to not let admin change purchase token |
| [p58] | reports/plume-l1_findings/52923-sc-critical-partial-fill-traps-source-token-residual-inside-the-wrapper-and-leaves-unsafe-resi.md | CRITICAL | Immunefi (LoopGhost007) | sc critical partial fill traps source token residual inside the wrapper and leaves unsafe residual allowance |
| [p59] | reports/plume-l1_findings/52974-sc-medium-when-the-approval-to-the-okxapprover-is-not-fully-spent-the-deposit-function-will-be.md | MEDIUM | Immunefi (TeamJosh) | sc medium when the approval to the okxapprover is not fully spent the deposit function will be blocked |
| [p60] | reports/plume-l1_findings/52980-sc-critical-partial-fills-strand-source-tokens-in-the-wrapper-and-leave-dangerous-residual-all.md | CRITICAL | Immunefi (RevertLord) | sc critical partial fills strand source tokens in the wrapper and leave dangerous residual allowances |
| [p61] | reports/plume-l1_findings/52988-sc-medium-deposit-function-dos.md | MEDIUM | Immunefi (frolic) | sc medium deposit function dos |
| [p62] | reports/plume-l1_findings/53001-sc-high-yield-tokens-become-stuck-in-arctokenpurchase-contract-when-distributing-yield-during.md | HIGH | Immunefi (KlosMitSoss) | sc high yield tokens become stuck in arctokenpurchase contract when distributing yield during active sales |
| [p63] | reports/plume-l1_findings/53016-sc-high-arctokenpurchase-doesn-t-allow-rwa-token-owners-to-recover-accrued-yield-from-stored-a.md | HIGH | Immunefi (valkvalue) | sc high arctokenpurchase doesn t allow rwa token owners to recover accrued yield from stored arctokens waiting for sale&#x20; |
| [p64] | reports/plume-l1_findings/53021-sc-medium-deposit-and-bridge-workflow-bricked-by-immediate-share-lock-users-cannot-bridge-imme.md | MEDIUM | Immunefi (farman1094) | sc medium deposit and bridge workflow bricked by immediate share lock users cannot bridge immediately after deposit |
| [p65] | reports/plume-l1_findings/53025-sc-high-commission-on-removed-tokens-is-unclaimable.md | HIGH | Immunefi (axolot) | sc high commission on removed tokens is unclaimable |
| [q66] | reports/plume-l1_findings/50027-sc-insight-missing-validation-of-okx-swap-output-token-in-function-okxhelper.md | INFO | Immunefi (Paludo0x) | sc insight missing validation of okx swap output token in function okxhelper&#x20; |
| [q67] | reports/plume-l1_findings/50040-sc-low-missing-pause-controls-eth-refund-flaws-and-miscalculated-shares-enable-fund-loss-and-p.md | LOW | Immunefi (Sharky) | sc low missing pause controls eth refund flaws and miscalculated shares enable fund loss and protocol inconsistency in depositandbridge |
| [q68] | reports/plume-l1_findings/50461-sc-insight-incorrect-deposit-event-receiver-logged-in-bridge-functions-of-dexaggregatorwrapper.md | INFO | Immunefi (Rhaydden) | sc insight incorrect deposit event receiver logged in bridge functions of dexaggregatorwrapperwithpredicateproxy sol&#x20; |
| [q69] | reports/plume-l1_findings/50675-sc-insight-re-entrant-eth-refund-can-emit-mismatched-shares-in-deposit-event.md | INFO | Immunefi (Paludo0x) | sc insight re entrant eth refund can emit mismatched shares in deposit event |
| [q70] | reports/plume-l1_findings/51001-sc-insight-inaccurate-share-calculation-in-emitted-event-for-non-bridge-deposits.md | INFO | Immunefi (warden) | sc insight inaccurate share calculation in emitted event for non bridge deposits |
| [q71] | reports/plume-l1_findings/51034-sc-low-sales-information-is-lost-when-enabling-token.md | LOW | Immunefi (holydevoti0n) | sc low sales information is lost when enabling token |
| [q72] | reports/plume-l1_findings/51146-sc-low-getmaxnumberoftokens-returns-wrong-max-number-of-tokens-available-to-buy.md | LOW | Immunefi (Oxgritty) | sc low getmaxnumberoftokens returns wrong max number of tokens available to buy |
| [q73] | reports/plume-l1_findings/51276-sc-low-arctokenpurchase-re-enabling-active-token-sales-causes-accounting-corruption-and-token.md | LOW | Immunefi (rilwan99) | sc low arctokenpurchase re enabling active token sales causes accounting corruption and token loss |
| [q74] | reports/plume-l1_findings/51412-sc-low-token-admin-can-withdraw-the-token-from-the-purchase-contract-making-the-token-balance.md | LOW | Immunefi (TeamJosh) | sc low token admin can withdraw the token from the purchase contract making the token balance to be less than the totalamountforsale |
| [q75] | reports/plume-l1_findings/51451-sc-low-token-freezing-via-whitelist-restriction-bypass.md | LOW | Immunefi (technicalattri) | sc low token freezing via whitelist restriction bypass |
| [q76] | reports/plume-l1_findings/51457-sc-low-getaccruedcommission-reverts-when-token-was-removed-instead-of-returning-the-accrued-co.md | LOW | Immunefi (warden) | sc low getaccruedcommission reverts when token was removed instead of returning the accrued commission |
| [q77] | reports/plume-l1_findings/51746-sc-low-depositandbridge-function-of-tellerwithmultiassetsupportpredicateproxy-sol-can-not-be-p.md | LOW | Immunefi (warden) | sc low depositandbridge function of tellerwithmultiassetsupportpredicateproxy sol can not be paused |
| [q78] | reports/plume-l1_findings/51776-sc-low-streak-system-breaks-despite-timely-user-action-due-to-delayed-supra-oracle-callback.md | LOW | Immunefi (light279) | sc low streak system breaks despite timely user action due to delayed supra oracle callback |
| [q79] | reports/plume-l1_findings/51850-sc-low-upgradetoken-can-not-initialize-an-upgraded-token-because-the-data-variable-of-upgradet.md | LOW | Immunefi (kaysoft) | sc low upgradetoken can not initialize an upgraded token because the data variable of upgradetoandcall is hardcoded to empty string |
| [q80] | reports/plume-l1_findings/51910-sc-low-inconsistent-yield-token-transfer-logic-causes-permanent-loss-of-yield-in-distributeyie.md | LOW | Immunefi (warden) | sc low inconsistent yield token transfer logic causes permanent loss of yield in distributeyield&#x20; |
| [q81] | reports/plume-l1_findings/51970-sc-low-spin-streak-computation-relies-on-oracle-callback-time-any-third-party-delay-can-reset.md | LOW | Immunefi (jovi) | sc low spin streak computation relies on oracle callback time any third party delay can reset the user s streak and block jackpot eligibility&#x20; |
| [q82] | reports/plume-l1_findings/52129-sc-low-previewyielddistribution-reverts-instead-of-returning-zero-when-no-tokens-are-in-circul.md | LOW | Immunefi (Afriauditor) | sc low previewyielddistribution reverts instead of returning zero when no tokens are in circulation |
| [q83] | reports/plume-l1_findings/52314-sc-low-unsold-token-withdrawal-causes-permanent-inventory-mismatch.md | LOW | Immunefi (itsravin0x) | sc low unsold token withdrawal causes permanent inventory mismatch |
| [q84] | reports/plume-l1_findings/52446-sc-low-withdrawing-unsold-tokens-desynchronizes-sale-accounting.md | LOW | Immunefi (Afriauditor) | sc low withdrawing unsold tokens desynchronizes sale accounting |
| [q85] | reports/plume-l1_findings/52519-sc-low-missing-eligibility-check-before-fund-transfer-in-distributeyield-leads-to-permanent-lo.md | LOW | Immunefi (vivekd) | sc low missing eligibility check before fund transfer in distributeyield leads to permanent loss of yield tokens |
| [q86] | reports/plume-l1_findings/52669-sc-low-token-minting-is-blocked-for-whitelisted-addresses-when-transfersallowed-is-false.md | LOW | Immunefi (magtentic) | sc low token minting is blocked for whitelisted addresses when transfersallowed is false |
| [q87] | reports/plume-l1_findings/52890-sc-low-no-recipient-yield-distribution-locks-yield-tokens-on-arctoken-efftotal-0.md | LOW | Immunefi (nitinaimshigh) | sc low no recipient yield distribution locks yield tokens on arctoken efftotal 0&#x20; |
| [q88] | reports/plume-l1_findings/52998-sc-low-minor-delays-from-oracle-can-unfairly-reset-users-streak.md | LOW | Immunefi (forgebyola) | sc low minor delays from oracle can unfairly reset users streak |
| [q89] | reports/plume-l1_findings/51352-sc-critical-user-will-lose-the-unspent-amount-when-executing-partial-swaps-via-1inch.md | CRITICAL | Immunefi (holydevoti0n) | User will lose the unspent amount when executing partial swaps via 1inch escrow |
## Rwa Token Plume

**rwa-token-plume patterns mined from uncited L1 audit reports** - 40 sec-tier findings (5 critical / 19 high / 16 medium) across 40 files from Immunefi (Afriauditor), Immunefi (Am3nh3l), Immunefi (Blobism), Immunefi (Boraicho), Immunefi (Bug82427), Immunefi (Finlooz4).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- access
- accrued
- accumulation
- active
- added
- address
- admin
- after
```

### Vulnerability Description

#### Root Cause

The cited reports describe rwa token plume paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `rwa-token-plume | rwa token plume | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `rwa-token-plume | rwa token plume | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `rwa-token-plume | rwa token plume | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: sc critical dex aggregator partial fill token loss** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc critical dex aggregator partial fill token loss
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc critical dex aggregator partial fill token loss
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: sc critical dex aggregator erc20 token theft** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc critical dex aggregator erc20 token theft
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc critical dex aggregator erc20 token theft
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: sc critical permanent freeze of user token due to unhandled partial fill refunds for swap via 1inch in dexaggregatorwrap** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc critical permanent freeze of user token due to unhandled partial fill refunds for swap via 1inch in dexaggregatorwrapperwithpredicateproxy&#x20;
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc critical permanent freeze of user token due to unhandled partial fill refunds for swap via 1inch 
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

`access, accrued, accumulation, active, added, address, admin, after, aggregator, allow`

### Related Vulnerabilities

- Sibling entries under the same category folder
