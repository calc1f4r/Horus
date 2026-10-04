---
# Core Classification
protocol: generic
chain: flare
category: fassets
vulnerability_type: fassets_vault_flare
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: fassets-vault-flare | fassets vault flare | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - fassets vault flare

# Attack Vector Details
attack_type: varies
affected_component: fassets vault flare

# Technical Primitives
primitives:
  - agent
  - agents
  - agentvault
  - allowed
  - always
  - asset

# Grep / Hunt-Card Seeds
code_keywords:
  - agent
  - agents
  - agentvault
  - allowed
  - always
  - asset
  - because
  - blocking

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
| [f1] | reports/flare-l1_findings/45514-sc-medium-malicious-agents-can-trap-stakers-by-raising-the-exit-collateral-ratio.md | MEDIUM | Immunefi (escrow) | #45514 \[SC-Medium] malicious agents can trap stakers by raising the exit collateral ratio |
| [f2] | reports/flare-l1_findings/45554-sc-medium-fee-loss-during-agents-feebips-reduction-in-selfmint-function.md | MEDIUM | Immunefi (holydevoti0n) | #45554 \[SC-Medium] Fee loss during Agent's feeBIPS reduction in \`selfMint\` function |
| [f3] | reports/flare-l1_findings/45769-sc-medium-permanent-blocking-of-agents-fund-by-allowed-minters.md | MEDIUM | Immunefi (pseudoArtist) | #45769 \[SC-Medium] Permanent blocking of Agent's fund by allowed minters |
| [f4] | reports/flare-l1_findings/45910-sc-medium-changing-collateral-ratio-makes-agents-prone-to-liquidation.md | MEDIUM | Immunefi (pseudoArtist) | #45910 \[SC-Medium] Changing collateral ratio makes Agents prone to liquidation |
| [f5] | reports/flare-l1_findings/45979-sc-high-agent-can-steal-funds-from-flr-holders-who-have-deposited-in-agents-collateral-pool.md | HIGH | Immunefi (a090325) | #45979 \[SC-High] Agent can steal funds from FLR holders who have deposited in agent's collateral pool |
| [f6] | reports/flare-l1_findings/45987-sc-medium-a-malicious-user-can-fill-up-the-redemption-queue-with-the-minimum-size-1-lot-making.md | MEDIUM | Immunefi (avoloder) | #45987 \[SC-Medium] A malicious user can fill up the redemption queue with the minimum size (1 lot)  making legitimate redeemers to redeem always mult |
| [f7] | reports/flare-l1_findings/46081-sc-medium-wrong-check-in-redeemfromcorevault-will-result-in-unnecessary-revert.md | MEDIUM | Immunefi (aman) | #46081 \[SC-Medium] Wrong check in \`redeemFromCoreVault\` will result in unnecessary revert |
| [f8] | reports/flare-l1_findings/46121-sc-high-malicious-agent-can-manipulate-the-totalcollateral-to-cause-damage-to-the-protocol.md | HIGH | Immunefi (Cryptor) | #46121 \[SC-High] Malicious agent can manipulate the totalCollateral to cause damage to the protocol |
| [f9] | reports/flare-l1_findings/46247-sc-medium-token-transfer-can-revert-in-unstickminting-because-of-insufficient-funds-in-the-vau.md | MEDIUM | Immunefi (ni8mare) | #46247 \[SC-Medium] Token transfer can revert in unstickMinting because of insufficient funds in the vault. |
| [f10] | reports/flare-l1_findings/46282-sc-high-wrong-implementation-of-payout-would-lead-to-loss-of-fee-share-of-agentvault.md | HIGH | Immunefi (farman1094) | #46282 \[SC-High] Wrong implementation of \`payout\` would lead to loss of fee share of \`AgentVault\` |
| [f11] | reports/flare-l1_findings/46378-sc-high-unconditional-f-asset-burn-during-partial-collateral-redemptions-enables-direct-theft.md | HIGH | Immunefi (DSbeX) | #46378 \[SC-High] Unconditional F-Asset burn during partial collateral redemptions enables direct theft of user funds |
| [f12] | reports/flare-l1_findings/46437-sc-high-agent-can-circumvent-double-payment-challenge-on-xrp-chain-using-other-types-of-transa.md | HIGH | Immunefi (nnez) | #46437 \[SC-High] Agent can circumvent double payment challenge on XRP chain using other types of transaction |
| [f13] | reports/flare-l1_findings/46541-sc-high-historical-payment-transaction-exploitation-leading-to-instant-agent-liquidation.md | HIGH | Immunefi (Bluedragon) | #46541 \[SC-High] Historical Payment Transaction Exploitation Leading to Instant Agent Liquidation |
| [f14] | reports/flare-l1_findings/46592-sc-high-the-return-value-of-redeemfromagent-redeemfromagentincollateral-in-the-selfcloseexitto.md | HIGH | Immunefi (ox9527) | #46592 \[SC-High] The return value of redeemFromAgent/redeemFromAgentInCollateral in the selfCloseExitTo is not checked |
| [f15] | reports/flare-l1_findings/46714-sc-medium-agent-can-frontrun-executor-to-steal-unclaimed-executor-fee-in-minting-process.md | MEDIUM | Immunefi (avoloder) | #46714 \[SC-Medium] Agent can frontrun executor to steal unclaimed executor fee in minting process |
| [f16] | reports/flare-l1_findings/46858-sc-high-the-agent-owner-can-exploit-a-malicious-rewardmanager-to-steal-tokens-from-the-protoco.md | HIGH | Immunefi (ayden) | #46858 \[SC-High] The agent owner can exploit a malicious rewardManager to steal tokens from the protocol |
| [f17] | reports/flare-l1_findings/46943-sc-medium-agents-can-prevent-user-corevault-redemptions-by-sandwiching-them-with-a-requestretu.md | MEDIUM | Immunefi (niroh) | #46943 \[SC-Medium] Agents can prevent user CoreVault redemptions by sandwiching them with a requestReturnFromCoreVault and a cancelReturnFromCoreVaul |
| [f18] | reports/flare-l1_findings/46953-sc-high-agents-who-create-agents-with-prior-transactions-can-be-instantly-unfairly-liquidated.md | HIGH | Immunefi (io10) | #46953 \[SC-High] agents who create agents with prior transactions can be instantly unfairly liquidated |
| [f19] | reports/flare-l1_findings/47020-sc-high-a-malicious-agent-can-extract-funds-from-the-collateral-pool-by-diluting-the-value-of.md | HIGH | Immunefi (a090325) | #47020 \[SC-High] A malicious agent can extract funds from the collateral pool by diluting the value of existing collateral providers' shares. |
| [q20] | reports/flare-l1_findings/45336-sc-low-malicious-agent-could-repeatedly-create-and-destroy-vaults-reserving-different-suffixes.md | LOW | Immunefi (avoloder) | #45336 \[SC-Low] Malicious Agent could repeatedly create and destroy vaults reserving different suffixes and grief other agents |
| [q21] | reports/flare-l1_findings/45450-sc-insight-outdated-underlying-chain-data-lead-to-shortened-minting-windows-or-dos-when-mintin.md | INFO | Immunefi (holydevoti0n) | #45450 \[SC-Insight] Outdated underlying chain data lead to shortened minting windows or DoS when minting fAssets |
| [q22] | reports/flare-l1_findings/45499-sc-low-malicious-user-can-prevent-agent-to-be-destroyed-and-lock-up-his-funds.md | LOW | Immunefi (holydevoti0n) | #45499 \[SC-Low] Malicious user can prevent agent to be destroyed and lock up his funds |
| [q23] | reports/flare-l1_findings/45674-sc-insight-executeminting-allows-impersonation-of-minter-during-chain-reorg-due-to-determinist.md | INFO | Immunefi (warden) | #45674 \[SC-Insight] \`executeMinting()\` allows impersonation of minter during chain-reorg due to deterministic \`crtId\` and lack of minter binding |
| [q24] | reports/flare-l1_findings/45864-sc-insight-minters-underlying-token-can-get-stuck-if-the-agent-calls-mintingdefault-before-the.md | INFO | Immunefi (ni8mare) | #45864 \[SC-Insight] Minter's underlying token can get stuck if the agent calls mintingDefault before the minter’s transaction is recorded on the unde |
| [q25] | reports/flare-l1_findings/45943-sc-low-rejectinvalidredemption-fee-is-not-awarded-to-agent-resulting-in-stuck-or-misallocated.md | LOW | Immunefi (magtentic) | #45943 \[SC-Low] rejectInvalidRedemption fee is not awarded to agent  resulting in stuck or misallocated funds |
| [q26] | reports/flare-l1_findings/45961-sc-insight-selfmint-can-lead-to-permanent-loss-of-agents-funds-during-emergency-pause.md | INFO | Immunefi (warden) | #45961 \[SC-Insight] \`selfMint()\` Can Lead to Permanent Loss of Agents' Funds During Emergency Pause |
| [q27] | reports/flare-l1_findings/45978-sc-insight-failed-transactions-trigger-invalid-double-payment-challenges-causing-loss-of-funds.md | INFO | Immunefi (Bluedragon) | #45978 \[SC-Insight] Failed Transactions Trigger Invalid Double Payment Challenges Causing Loss of Funds for Legitimate Agents |
| [q28] | reports/flare-l1_findings/46092-sc-insight-agentvault-destroy-mismatch-between-comment-documentation-and-contract-behavior.md | INFO | Immunefi (hunter0xweb3) | #46092 \[SC-Insight] AgentVault::destroy mismatch between comment documentation and contract behavior |
| [q29] | reports/flare-l1_findings/46122-sc-insight-incorrect-minimum-lots-validation-in-corevault-redemption.md | INFO | Immunefi (aman) | #46122 \[SC-Insight] Incorrect Minimum Lots Validation in CoreVault Redemption |
| [q30] | reports/flare-l1_findings/46198-sc-insight-redemption-blocked-if-agent-refuses-to-confirm-core-vault-payment.md | INFO | Immunefi (warden) | #46198 \[SC-Insight] Redemption Blocked if Agent Refuses to Confirm Core Vault Payment |
| [q31] | reports/flare-l1_findings/46210-sc-insight-incorrect-timestamp-comparison-in-function-beforecollateralwithdrawal-allows-agent.md | INFO | Immunefi (dldLambda) | #46210 \[SC-Insight] Incorrect timestamp comparison in function "beforeCollateralWithdrawal" allows agent to withdraw at last second without being cha |
| [q32] | reports/flare-l1_findings/46218-sc-insight-documentation-implementation-discrepancy-in-agent-vault-access-control.md | INFO | Immunefi (warden) | #46218 \[SC-Insight] Documentation-Implementation Discrepancy in Agent Vault Access Control |
| [q33] | reports/flare-l1_findings/46241-sc-insight-misleading-definition-in-core-vault-documentation-cv-operators-submit-proof.md | INFO | Immunefi (Paludo0x) | #46241 \[SC-Insight] Misleading definition in Core-Vault documentation (“CV operators submit proof”) |
| [q34] | reports/flare-l1_findings/46311-sc-insight-unbacked-redemptions-due-to-donation-attack-on-corevault-can-freeze-agent-collatera.md | INFO | Immunefi (warden) | #46311 \[SC-Insight] Unbacked Redemptions Due to Donation- Attack on CoreVault Can Freeze Agent Collateral |
| [q35] | reports/flare-l1_findings/46442-sc-low-agent-collateral-pool-is-vulnerable-to-inflation-attack.md | LOW | Immunefi (a090325) | #46442 \[SC-Low] Agent collateral pool is vulnerable to inflation attack |
| [q36] | reports/flare-l1_findings/46462-sc-low-malicious-collateral-provider-can-steal-funds-from-agent-collateral-pool-by-donating-a.md | LOW | Immunefi (a090325) | #46462 \[SC-Low] Malicious collateral provider can steal funds from agent collateral pool by donating a large amount of native token to the pool (infl |
| [q37] | reports/flare-l1_findings/46520-sc-low-eth-loss-on-selfcloseexitto-when-redeeming-to-collateral.md | LOW | Immunefi (Rhaydden) | #46520 \[SC-Low] ETH loss on \`selfCloseExitTo\` when redeeming to collateral |
| [q38] | reports/flare-l1_findings/46643-sc-low-destroyagent-in-agentscreatedestroy-is-prone-to-dos.md | LOW | Immunefi (ni8mare) | #46643 \[SC-Low] \`destroyAgent\` in \`AgentsCreateDestroy\` is prone to DOS |
| [q39] | reports/flare-l1_findings/46681-sc-low-malicious-actor-can-prevent-agent-from-being-destroyed.md | LOW | Immunefi (rick137) | #46681 \[SC-Low] malicious actor can prevent agent from being destroyed |
| [q40] | reports/flare-l1_findings/46721-sc-insight-inconsistencies-for-agenttimelockedoperationwindowseconds-value-checks-between-sett.md | INFO | Immunefi (hunter0xweb3) | #46721 \[SC-Insight] Inconsistencies for agentTimelockedOperationWindowSeconds value checks between SettingsInitializer.sol::\_validateSettings and Se |
| [q41] | reports/flare-l1_findings/46838-sc-low-agent-destruction-can-be-blocked-by-malicious-collateral-pool-entries.md | LOW | Immunefi (Bluedragon) | #46838 \[SC-Low] Agent Destruction Can Be Blocked by Malicious Collateral Pool Entries |
| [q42] | reports/flare-l1_findings/46848-sc-insight-minters-can-grief-agents-by-deliberately-fragmenting-the-agents-redemption-ticket-q.md | INFO | Immunefi (niroh) | #46848 \[SC-Insight] Minters can grief agents by deliberately fragmenting the agent's redemption ticket queue with minimal size tickets  preventing or |
| [q43] | reports/flare-l1_findings/46976-sc-low-agent-destruction-can-permanently-lock-unclaimed-transfer-fees.md | LOW | Immunefi (Bluedragon) | #46976 \[SC-Low] Agent Destruction Can Permanently Lock Unclaimed Transfer Fees |
| [q44] | reports/flare-l1_findings/46993-sc-low-malicious-agent-with-large-capital-can-abuse-cancelreturnfromcorevault-to-block-access.md | LOW | Immunefi (nnez) | #46993 \[SC-Low] Malicious agent with large capital can abuse \`cancelReturnFromCoreVault\` to block access to core vault liquidity during high redemp |
| [q45] | reports/flare-l1_findings/47033-sc-low-incorrect-calculation-of-total-available-amount-in-core-vault-in-a-certain-case-when-a.md | LOW | Immunefi (swarun) | #47033 \[SC-Low] Incorrect calculation of total available amount in core vault in a certain case when a user redeems from the core vault |
| [q46] | reports/flare-l1_findings/47053-sc-low-transfertocorevault-allows-agents-to-have-unbacked-synthetic-assets-by-extracting-under.md | LOW | Immunefi (warden) | #47053 \[SC-Low] \`transferToCoreVault()\` allows agents to have unbacked synthetic assets by extracting underlying value without burning |
| [q47] | reports/flare-l1_findings/47082-sc-low-zero-collateral-payout-despite-burned-fassets.md | LOW | Immunefi (dldLambda) | #47082 \[SC-Low] Zero collateral payout despite burned fAssets |
| [q48] | reports/flare-l1_findings/47094-sc-insight-missing-event-emission-in-agentvault-and-collateralpooltoken-factory-contracts.md | INFO | Immunefi (blackgrease) | #47094 \[SC-Insight] Missing Event Emission in \`AgentVault\` and \`CollateralPoolToken\` Factory Contracts |

## Fassets Vault Flare

**fassets-vault-flare patterns mined from uncited L1 audit reports** - 19 sec-tier findings (0 critical / 10 high / 9 medium) across 19 files from Immunefi (Bluedragon), Immunefi (Cryptor), Immunefi (DSbeX), Immunefi (a090325), Immunefi (aman), Immunefi (avoloder).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- agent
- agents
- agentvault
- allowed
- always
- asset
- because
- blocking
```

### Vulnerability Description

#### Root Cause

The cited reports describe fassets vault flare paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `fassets-vault-flare | fassets vault flare | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `fassets-vault-flare | fassets vault flare | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `fassets-vault-flare | fassets vault flare | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: #45979 \[SC-High] Agent can steal funds from FLR holders who have deposited in agent's collateral pool** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #45979 \[SC-High] Agent can steal funds from FLR holders who have deposited in agent's collateral pool
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #45979 \[SC-High] Agent can steal funds from FLR holders who have deposited in agent's collateral po
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: #46121 \[SC-High] Malicious agent can manipulate the totalCollateral to cause damage to the protocol** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #46121 \[SC-High] Malicious agent can manipulate the totalCollateral to cause damage to the protocol
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #46121 \[SC-High] Malicious agent can manipulate the totalCollateral to cause damage to the protocol
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: #46282 \[SC-High] Wrong implementation of \`payout\` would lead to loss of fee share of \`AgentVault\`** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// #46282 \[SC-High] Wrong implementation of \`payout\` would lead to loss of fee share of \`AgentVault\`
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: #46282 \[SC-High] Wrong implementation of \`payout\` would lead to loss of fee share of \`AgentVault
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

`agent, agents, agentvault, allowed, always, asset, because, blocking, burn, cancelreturnfromcorevault`

### Related Vulnerabilities

- Sibling entries under the same category folder
