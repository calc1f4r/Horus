---
# Core Classification
protocol: generic
chain: flare
category: flare
vulnerability_type: flare_misc
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: flare-misc | flare misc | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - flare misc

# Attack Vector Details
attack_type: varies
affected_component: flare misc

# Technical Primitives
primitives:
  - allows
  - amount
  - arbitrary
  - asset
  - bypass
  - bypassed

# Grep / Hunt-Card Seeds
code_keywords:
  - allows
  - amount
  - arbitrary
  - asset
  - bypass
  - bypassed
  - bypassing
  - cause

severity: high
impact: varies
language: varies
tags:
  - flare
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [f1] | reports/flare-l1_findings/45478-sc-medium-minting-cap-check-doesnt-include-poolfeeuba-in-selfmint-and-mintfromunderlying.md | MEDIUM | Immunefi (ni8mare) | #45478 \[SC-Medium] Minting Cap Check Doesn't Include \`poolFeeUBA\` in \`selfMint\` and \`mintFromUnderlying\` |
| [f2] | reports/flare-l1_findings/45550-sc-medium-h-01-illegalpaymentchallenge-is-vulnerable-to-frontrunning-by-external-challengers-s.md | MEDIUM | Immunefi (warden) | #45550 \[SC-Medium] \[H-01] \`illegalPaymentChallenge\` is vulnerable to frontrunning by external challengers stealing the reward |
| [f3] | reports/flare-l1_findings/45665-sc-medium-h-02-minting-cap-bypass-via-pool-fee-exclusion-during-self-mint.md | MEDIUM | Immunefi (warden) | #45665 \[SC-Medium] \[H-02] Minting Cap Bypass via Pool Fee Exclusion during Self Mint |
| [f4] | reports/flare-l1_findings/45830-sc-medium-incorrect-amount-passed-to-checkmintingcap-in-self-minting-allows-bypassing-of-confi.md | MEDIUM | Immunefi (nnez) | #45830 \[SC-Medium] Incorrect amount passed to checkMintingCap in self-minting allows bypassing of config minting cap |
| [f5] | reports/flare-l1_findings/46108-sc-medium-minting-cap-can-by-bypassed-while-self-minting.md | MEDIUM | Immunefi (Oxgritty) | #46108 \[SC-Medium] Minting Cap can by bypassed while self minting |
| [f6] | reports/flare-l1_findings/46265-sc-medium-logic-flaw-in-transfertocorevault-allows-creation-of-zero-value-redemption-request.md | MEDIUM | Immunefi (nnez) | #46265 \[SC-Medium] Logic flaw in transferToCoreVault allows creation of zero-value redemption request |
| [f7] | reports/flare-l1_findings/46326-sc-medium-incorrect-minting-cap-check-in-minting-process.md | MEDIUM | Immunefi (aman) | #46326 \[SC-Medium] Incorrect Minting Cap Check in Minting Process |
| [f8] | reports/flare-l1_findings/46688-sc-high-claimairdropdistribution-allows-arbitrary-inflation-of-totalcollateral.md | HIGH | Immunefi (warden) | #46688 \[SC-High] \`claimAirdropDistribution()\` Allows Arbitrary Inflation of \`totalCollateral\` |
| [f9] | reports/flare-l1_findings/46929-sc-medium-incorrect-required-underlying-value-check-used-in-mintfromfreeunderlying-function.md | MEDIUM | Immunefi (swarun) | #46929 \[SC-Medium] Incorrect required underlying value check used in mintFromFreeUnderlying function |
| [f10] | reports/flare-l1_findings/46949-sc-high-top-up-discount-miscalculation-allows-minting-excess-pool-tokens-via-repeated-small-de.md | HIGH | Immunefi (NHristov) | #46949 \[SC-High] Top-up discount miscalculation allows minting excess pool tokens via repeated small deposits in \`CollateralPool::enter\` |
| [f11] | reports/flare-l1_findings/46985-sc-high-collateralpool-totalcollateral-can-be-increased-to-arbitrary-value.md | HIGH | Immunefi (rick137) | #46985 \[SC-High] CollateralPool::totalCollateral can be increased to arbitrary value |
| [f12] | reports/flare-l1_findings/47034-sc-medium-check-minting-cap-function-checks-on-incorrect-amount-in-mintfromfreeunderlying-func.md | MEDIUM | Immunefi (swarun) | #47034 \[SC-Medium] check minting cap function checks on incorrect amount in mintFromFreeUnderlying function |
| [f13] | reports/flare-l1_findings/47060-sc-high-unchecked-partial-payout-on-selfcloseexit-allows-user-underpayment.md | HIGH | Immunefi (RNemes) | #47060 \[SC-High] Unchecked Partial Payout on selfCloseExit Allows User Underpayment |
| [f14] | reports/flare-l1_findings/47108-sc-high-selfcloseexitto-can-cause-users-to-receive-partial-payments-without-validation-leading.md | HIGH | Immunefi (rilwan99) | #47108 \[SC-High] selfCloseExitTo() can cause users to receive partial payments without validation  leading to permanent asset loss |
| [q15] | reports/flare-l1_findings/45357-sc-insight-increase-in-the-usedtokens-array.md | INFO | Immunefi (vargalove) | #45357 \[SC-Insight] Increase in the usedTokens array |
| [q16] | reports/flare-l1_findings/45368-sc-insight-corruptible-upgradability-pattern.md | INFO | Immunefi (Anirruth) | #45368 \[SC-Insight] Corruptible Upgradability Pattern |
| [q17] | reports/flare-l1_findings/45377-sc-insight-missing-pause-modifier-in-beforecollateralwithdrawal-allows-collateral-theft-during.md | INFO | Immunefi (Rhaydden) | #45377 \[SC-Insight] Missing pause modifier in \`beforeCollateralWithdrawal\` allows collateral theft during a pause |
| [q18] | reports/flare-l1_findings/45379-sc-low-frontrunning-vulnerability-in-createagentvault-suffix-reservation.md | LOW | Immunefi (EFCCWEB3) | #45379 \[SC-Low] Frontrunning Vulnerability in createAgentVault Suffix Reservation |
| [q19] | reports/flare-l1_findings/45405-sc-insight-insufficient-documentation-for-governance-controlled-functions-and-critical-paramet.md | INFO | Immunefi (rusalka711) | #45405 \[SC-Insight] Insufficient Documentation for Governance-Controlled Functions and Critical Parameters in 'CoreVaultManager.sol' |
| [q20] | reports/flare-l1_findings/45485-sc-insight-comments-above-reservecollateral-indicate-collateral-reservation-fee-is-burned-whic.md | INFO | Immunefi (ni8mare) | #45485 \[SC-Insight] Comments above \`reserveCollateral\` indicate collateral reservation fee is burned  which is not the case |
| [q21] | reports/flare-l1_findings/45517-sc-insight-partial-documentation-for-self-close-exit-fee-handling-and-redemption-workflow-in-c.md | INFO | Immunefi (rusalka711) | #45517 \[SC-Insight] Partial Documentation for Self-Close Exit Fee Handling and Redemption Workflow in 'CollateralPool.sol' |
| [q22] | reports/flare-l1_findings/45533-sc-low-incorrect-gas-allowance-comparison-in-corevault-transfer-function-leads-to-user-fund-lo.md | LOW | Immunefi (DSbeX) | #45533 \[SC-Low] Incorrect gas allowance comparison in CoreVault transfer function leads to user fund loss |
| [q23] | reports/flare-l1_findings/45574-sc-insight-redundant-per-item-upper-bound-check-in-validateliquidationfactors.md | INFO | Immunefi (chista0x) | #45574 \[SC-Insight] Redundant Per‑Item Upper Bound Check in \`validateLiquidationFactors\` |
| [q24] | reports/flare-l1_findings/45604-sc-low-user-overpayment-in-transfertocorevault-fee-handling.md | LOW | Immunefi (lufP) | #45604 \[SC-Low] User Overpayment in \`transferToCoreVault\` Fee Handling |
| [q25] | reports/flare-l1_findings/45685-sc-insight-incorrect-comments-in-finishredemptionwithoutpayment.md | INFO | Immunefi (ni8mare) | #45685 \[SC-Insight] Incorrect comments in finishRedemptionWithoutPayment |
| [q26] | reports/flare-l1_findings/45731-sc-insight-off-by-one-logic-in-escrow-end-timestamp-calculation-may-cause-unintended-escrow-de.md | INFO | Immunefi (MRXSNOWDEN) | #45731 \[SC-Insight] Off-by-One Logic in Escrow End Timestamp Calculation May Cause Unintended Escrow Delay |
| [q27] | reports/flare-l1_findings/45772-sc-insight-natspec-mismatch-in-corevault-redemption-logic.md | INFO | Immunefi (MyssTeeQue) | #45772 \[SC-Insight] NatSpec Mismatch in CoreVault Redemption Logic |
| [q28] | reports/flare-l1_findings/45813-sc-insight-missing-setautoclaiming-function.md | INFO | Immunefi (warden) | #45813 \[SC-Insight] Missing \`setAutoClaiming\` Function |
| [q29] | reports/flare-l1_findings/45897-sc-low-executor-fee-lost-in-rejectinvalidredemption-due-to-missing-handling-logic.md | LOW | Immunefi (warden) | #45897 \[SC-Low] Executor Fee Lost in \`rejectInvalidRedemption()\` Due to Missing Handling Logic |
| [q30] | reports/flare-l1_findings/45949-sc-insight-mismatch-between-doc-and-implementation-for-confirmationbyothersafterseconds-minimu.md | INFO | Immunefi (Rhaydden) | #45949 \[SC-Insight] Mismatch between doc and implementation for \`confirmationByOthersAfterSeconds\` minimum on XRP |
| [q31] | reports/flare-l1_findings/45956-sc-insight-eoa-only-on-smart-contract-chains-bypassed-on-eth.md | INFO | Immunefi (Machicoulis) | #45956 \[SC-Insight] EOA only on smart contract chains bypassed on ETH |
| [q32] | reports/flare-l1_findings/46068-sc-low-selfcloseexitto-is-lack-of-slippage-protect.md | LOW | Immunefi (ox9527) | #46068 \[SC-Low] selfCloseExitTo is lack of slippage protect |
| [q33] | reports/flare-l1_findings/46071-sc-low-ultra-low-amount-of-total-shares-in-collateral-pool.md | LOW | Immunefi (Audittens) | #46071 \[SC-Low] Ultra-low amount of total shares in collateral pool |
| [q34] | reports/flare-l1_findings/46220-sc-insight-missing-documented-function-in-the-collateralpool-contract.md | INFO | Immunefi (warden) | #46220 \[SC-Insight] Missing Documented Function in the CollateralPool Contract |
| [q35] | reports/flare-l1_findings/46320-sc-low-executor-fee-will-be-stuck-in-the-contract-when-rejectinvalidredemption-is-called.md | LOW | Immunefi (Oxgritty) | #46320 \[SC-Low] Executor fee will be stuck in the contract when rejectInvalidRedemption is called |
| [q36] | reports/flare-l1_findings/46486-sc-low-faulty-logic-in-transfertocorevault-makes-users-pay-more-for-the-refund-transaction-tha.md | LOW | Immunefi (ni8mare) | #46486 \[SC-Low] Faulty logic in \`transferToCoreVault\` makes users pay more for the refund transaction than the amount being refunded. |
| [q37] | reports/flare-l1_findings/46534-sc-insight-missing-validation-to-prevent-self-assignment-of-work-address.md | INFO | Immunefi (elyas6126) | #46534 \[SC-Insight] Missing Validation to Prevent Self-Assignment of Work Address |
| [q38] | reports/flare-l1_findings/46587-sc-low-overpayment-loss-in-transfertocorevault-due-to-incorrect-refund-condition.md | LOW | Immunefi (nnez) | #46587 \[SC-Low] Overpayment loss in \`transferToCoreVault\` due to incorrect refund condition |
| [q39] | reports/flare-l1_findings/46702-sc-insight-executeminting-enables-cross-contract-reentrancy-to-manipulate-collateral-pool-pric.md | INFO | Immunefi (warden) | #46702 \[SC-Insight] \`executeMinting()\` Enables Cross-Contract Reentrancy to Manipulate Collateral Pool Pricing |
| [q40] | reports/flare-l1_findings/46758-sc-low-collateral-reservation-fee-calculation-inconsistent-with-actual-reserved-value.md | LOW | Immunefi (light279) | #46758 \[SC-Low] Collateral Reservation Fee Calculation Inconsistent with Actual Reserved Value |
| [q41] | reports/flare-l1_findings/46771-sc-insight-incorrect-collateral-ratio-check-due-to-rounding-error.md | INFO | Immunefi (TheCarrot) | #46771 \[SC-Insight] Incorrect Collateral Ratio Check Due to Rounding Error |
| [q42] | reports/flare-l1_findings/46836-sc-low-buybackagentcollateral-will-revert-due-to-overflow.md | LOW | Immunefi (rick137) | #46836 \[SC-Low] buybackAgentCollateral will revert due to overflow |
| [q43] | reports/flare-l1_findings/46847-sc-low-executor-fee-is-not-paid-or-burned-in-rejectinvalidredemption.md | LOW | Immunefi (pseudoArtist) | #46847 \[SC-Low] executor fee is not paid or burned in \`rejectInvalidRedemption\` |
| [q44] | reports/flare-l1_findings/46886-sc-low-destroyagent-functionality-can-easily-be-bricked-due-to-frontrunning-attack.md | LOW | Immunefi (warden) | #46886 \[SC-Low] \`destroyAgent()\` functionality can easily be bricked due to Frontrunning Attack |
| [q45] | reports/flare-l1_findings/46924-sc-low-last-user-may-exit-with-almost-all-of-his-values-but-hell-purposefully-leave-a-small-1e.md | LOW | Immunefi (onthehunt) | #46924 \[SC-Low] Last user may exit with almost all of his values  but he'll purposefully leave a small 1e18 or a little more to grief \`destroy()\` |
| [q46] | reports/flare-l1_findings/46930-sc-low-depositnat-in-collateralpool-fails-to-notify-asset-manager-by-not-calling-the-updatecol.md | LOW | Immunefi (warden) | #46930 \[SC-Low] \`depositNat()\` in \`CollateralPool\` Fails to Notify Asset Manager  By not calling the \`updateCollateral\` |
| [q47] | reports/flare-l1_findings/46969-sc-low-inconsistent-use-of-poolfeesharebips-between-collateral-reservation-and-distribution.md | LOW | Immunefi (Josh4324) | #46969 \[SC-Low] Inconsistent Use of poolFeeShareBIPS Between Collateral Reservation and Distribution |
| [q48] | reports/flare-l1_findings/46982-sc-insight-spread-calculation-discrepancy-allows-wildly-divergent-prices-to-be-accepted.md | INFO | Immunefi (dawn) | #46982 \[SC-Insight] Spread calculation discrepancy allows wildly divergent prices to be accepted |
| [q49] | reports/flare-l1_findings/46999-sc-insight-absence-of-event-emission-in-critical-functions.md | INFO | Immunefi (dldLambda) | #46999 \[SC-Insight] Absence of event emission in critical functions |
| [q50] | reports/flare-l1_findings/47010-sc-low-collateralpool-donatenat-manipulation-enables-arbitrary-pool-token-value-inflation-and.md | LOW | Immunefi (NHristov) | #47010 \[SC-Low] \`CollateralPool::donateNat\` manipulation enables arbitrary pool‐token value inflation and fee‐debt evasion |
| [q51] | reports/flare-l1_findings/47091-sc-insight-setworkaddress-enables-front-running-attacks-to-hijack-work-addresses.md | INFO | Immunefi (warden) | #47091 \[SC-Insight] \`setWorkAddress()\` enables front-running attacks to hijack work addresses |
| [q52] | reports/flare-l1_findings/47106-sc-low-collateral-reservation-fee-distribution-uses-current-poolfeesharebips-instead-of-value.md | LOW | Immunefi (rilwan99) | #47106 \[SC-Low] Collateral Reservation Fee distribution uses current poolFeeShareBips instead of value stored during during time of collateral reserv |
| [q53] | reports/flare-l1_findings/47116-sc-insight-undocumented-redemption-pool-fee-share-potentially-leading-to-confusion.md | INFO | Immunefi (a090325) | #47116 \[SC-Insight] Undocumented Redemption Pool Fee Share potentially leading to confusion |
| [q54] | reports/flare-l1_findings/47121-sc-insight-incorrect-documentation-on-pool-top-up-feature.md | INFO | Immunefi (a090325) | #47121 \[SC-Insight] Incorrect documentation on pool Top-up feature |
| [q55] | reports/flare-l1_findings/47150-sc-insight-xrp-deposit-authorization-griefing-attack-on-minting-process.md | INFO | Immunefi (Bluedragon) | #47150 \[SC-Insight] XRP Deposit Authorization Griefing Attack on Minting Process |
| [q56] | reports/flare-l1_findings/47159-sc-insight-lack-of-access-control-on-triggerinstructions-allows-unauthorized-transfers-post-de.md | INFO | Immunefi (Pig46940) | #47159 \[SC-Insight] Lack of Access Control on \`triggerInstructions()\` Allows Unauthorized Transfers Post-Deletion |

## Flare Misc

**flare-misc patterns mined from uncited L1 audit reports** - 14 sec-tier findings (0 critical / 5 high / 9 medium) across 14 files from Immunefi (NHristov), Immunefi (Oxgritty), Immunefi (RNemes), Immunefi (aman), Immunefi (ni8mare), Immunefi (nnez).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- allows
- amount
- arbitrary
- asset
- bypass
- bypassed
- bypassing
- cause
```

### Vulnerability Description

#### Root Cause

The cited reports describe flare misc paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `flare-misc | flare misc | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `flare-misc | flare misc | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `flare-misc | flare misc | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: #46688 \[SC-High] \`claimAirdropDistribution()\` Allows Arbitrary Inflation of \`totalCollateral\`** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #46688 \[SC-High] \`claimAirdropDistribution()\` Allows Arbitrary Inflation of \`totalCollateral\`
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #46688 \[SC-High] \`claimAirdropDistribution()\` Allows Arbitrary Inflation of \`totalCollateral\`
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: #46949 \[SC-High] Top-up discount miscalculation allows minting excess pool tokens via repeated small deposits in \`Coll** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #46949 \[SC-High] Top-up discount miscalculation allows minting excess pool tokens via repeated small deposits in \`CollateralPool::enter\`
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #46949 \[SC-High] Top-up discount miscalculation allows minting excess pool tokens via repeated smal
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: #46985 \[SC-High] CollateralPool::totalCollateral can be increased to arbitrary value** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #46985 \[SC-High] CollateralPool::totalCollateral can be increased to arbitrary value
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #46985 \[SC-High] CollateralPool::totalCollateral can be increased to arbitrary value
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

`allows, amount, arbitrary, asset, bypass, bypassed, bypassing, cause, challengers, check`

### Related Vulnerabilities

- Sibling entries under the same category folder
