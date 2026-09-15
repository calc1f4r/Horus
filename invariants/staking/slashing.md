# Staking: Slashing Mechanism Invariants

> Canonical invariants for slashing correctness, penalty distribution, and protocol
> solvency under slashing. Mined from production protocols (EigenLayer, Karak, Lido,
> Puffer, Renzo), audit reports, and Horus.
> Language-agnostic and protocol-agnostic.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: slashing
- **Sources**: EigenLayer, Karak, Lido, Puffer, Nexus, Renzo, Casimir, Babylon
- **Last updated**: 2026-03-13
- **Invariant count**: 12

---

## Invariants

### STAKING-SLASHING-001: All Vaults Must Be Slashable

**Property (English):**
Every vault or staking position that claims to be part of the slashable set must actually be slashable when a slashing event occurs. No configuration, deployment parameter, or state transition may create a vault that silently evades slashing.

**Property (Formal):**
$$\forall v \in \text{registeredVaults}: \text{slashable}(v) = \text{true}$$

$$\text{slashable}(v) \iff \text{slash}(v, \text{amount}) \implies \text{balance}(v)' = \text{balance}(v) - \text{amount}$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any restaking protocol with slashing guarantees
- Must hold regardless of vault type (native, ERC20, delegated)
- Deployment parameters must be validated to prevent unslashable configurations

**Source Evidence:**
- Protocol: Karak | Report: `reports/eigenlayer_findings/h-02-the-operator-can-create-a-nativevault-that-can-be-silently-unslashable.md`
- Protocol: Karak | Report: `reports/eigenlayer_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md`

**Why This Matters:**
If operators can create unslashable vaults, they face zero risk for misbehavior — completely undermining the economic security model.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-1-unslashable-vault-creation-000`

---

### STAKING-SLASHING-002: No Over-Slashing (Slash ≤ Slashable Balance)

**Property (English):**
A slashing event must not reduce a position's balance below zero or slash more than the slashable amount. The total penalty must be bounded by the position's available slashable balance.

**Property (Formal):**
$$\forall \text{slash}(v, a): a \leq \text{slashableBalance}(v) \land \text{balance}(v)' \geq 0$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Must hold even when multiple slashing events occur in sequence
- Must handle combined AVS + beacon chain slashing without double-reduction
- Concurrent slashing from multiple sources must not exceed total balance

**Source Evidence:**
- Protocol: Karak | Report: `reports/eigenlayer_findings/h-01-slashing-nativevault-will-lead-to-locked-eth-for-the-users.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`

**Why This Matters:**
Over-slashing creates accounting deadlock — the protocol believes more was slashed than existed, making subsequent withdrawals impossible (underflow/revert).

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-2-over-slashing-and-double-red-001`

---

### STAKING-SLASHING-003: No Double-Reduction from Combined Slashing Sources

**Property (English):**
When a position is subject to slashing from multiple sources (e.g., AVS slashing + beacon chain slashing), the total reduction must be computed correctly. Applying both independently must not result in more than the intended total penalty.

**Property (Formal):**
$$\text{totalPenalty} = \min\left(\text{avsPenalty} + \text{beaconPenalty}, \text{slashableBalance}\right)$$

$$\neg \left(\text{balance}' = \text{balance} - \text{avsPenalty} - \text{beaconPenalty} \quad \text{when avsPenalty + beaconPenalty > slashableBalance}\right)$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires multiple slashing sources)

**Conditions:**
- Applies to restaking protocols where validators face slashing from both consensus layer and application layer
- Common in EigenLayer-based systems

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`

**Why This Matters:**
Double-reduction locks ETH for users — the accounting shows a negative balance that prevents all future withdrawals.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-2-over-slashing-and-double-red-001`

---

### STAKING-SLASHING-004: Slashing Bypass via Timing Prevention

**Property (English):**
No action sequence within a bounded time window before or after a slashing event may allow a staker to avoid the slashing penalty. Specifically, frontrunning a slash with an unstake/withdrawal must not shield funds.

**Property (Formal):**
$$\forall \text{slash}(s, t), \forall \text{unstake}(u, t'): |t - t'| \leq \text{SLASH\_LOOKBACK} \implies \text{affected}(u, s) = \text{true}$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires withdrawal delay + slashing)

**Conditions:**
- Applies to protocols with asynchronous withdrawal that overlaps with slashing windows
- Withdrawal delay must be longer than slash detection latency

**Source Evidence:**
- Protocol: Various | Reports related to timing-based slashing bypass
- DB: `general-defi-restaking-slashing-vulnerabilities-3-slashing-bypass-via-timing-002`

**Why This Matters:**
If stakers can frontrun slashing by unstaking before the slash executes, the economic security guarantee is voided — adversaries face no risk.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-3-slashing-bypass-via-timing-002`

---

### STAKING-SLASHING-005: Protocol Solvency Under LST Slashing (Rebasing Tokens)

**Property (English):**
When the underlying staking token is a rebasing token (e.g., stETH), the protocol must handle negative rebases (slashing events) without becoming insolvent. The protocol's tracked balance must stay synchronized with the actual rebasing token balance.

**Property (Formal):**
$$\forall t: \text{trackedBalance}(t) \leq \text{actualBalance}(t)$$

$$\text{negativeRebase}(t) \implies \text{trackedBalance}(t)' = \text{trackedBalance}(t) \times \frac{\text{actualBalance}(t)'}{\text{actualBalance}(t)}$$

**Mode:** DUAL
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires rebasing token integration)

**Conditions:**
- Applies to protocols that accept rebasing LSTs (stETH)
- Must handle both positive and negative rebases
- Internal accounting must not assume monotonically increasing balances

**Source Evidence:**
- Protocol: Nexus | Report: `reports/eigenlayer_findings/m-03-potential-protocol-insolvency-due-to-lido-slashing-events.md`
- Protocol: Puffer | Report: `reports/eigenlayer_findings/possibly-protocol-insolvency-during-a-lido-slashing-event-once-redeemwithdraw-is.md`

**Why This Matters:**
If the protocol tracks stETH at a fixed amount but stETH rebases downward, withdrawals attempt to transfer more than exists — creating insolvency.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-4-protocol-insolvency-from-lst-003`

---

### STAKING-SLASHING-006: Fair Penalty Distribution

**Property (English):**
Slashing penalties must be distributed proportionally among all affected stakers. No subset of stakers (e.g., the first withdrawal cohort) should bear a disproportionate share of the penalty.

**Property (Formal):**
$$\forall u \in \text{affectedStakers}: \frac{\text{penalty}(u)}{\text{stake}(u)} = \frac{\text{totalPenalty}}{\text{totalAffectedStake}} \pm \epsilon$$

where $\epsilon$ accounts for rounding

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol where multiple stakers share a slashing penalty
- Must not allow "first-to-exit" to escape with full value while latecomers absorb entire penalty

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/m-10-slashing-penalty-is-unfairly-paid-by-a-subset-of-users-if-a-deficit-is-accu.md`

**Why This Matters:**
Unfair distribution creates a bank-run incentive — informed stakers withdraw first to avoid penalties, exacerbating losses for remaining participants.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-5-unfair-penalty-distribution-004`

---

### STAKING-SLASHING-007: Slashing Accounting Consistency

**Property (English):**
Slashing accounting variables (slashing factor, recovered balance, penalty ledger) must be updated atomically and consistently. The reported effective balance and recoverable balance must reflect actual slashing state.

**Property (Formal):**
$$\forall t: \text{effectiveBalance}(t) = \text{originalBalance}(t) - \text{totalSlashed}(t) + \text{recovered}(t)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Must hold across all slashing-related operations (slash, recover, report)
- Concurrent slashing + recovery must not create inconsistencies

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/incorrect-accounting-of-reportrecoveredeffectivebalance-can-prevent-report-from-.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/m-02-a-snapshot-may-face-a-permanent-dos-if-both-a-slashing-event-occurs-in-the-.md`

**Why This Matters:**
Incorrect slashing accounting prevents future reports from being submitted, creating cascading failures in the protocol's oracle system.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-6-slashing-accounting-errors-005`

---

### STAKING-SLASHING-008: Slashing Handler Consistency

**Property (English):**
The slashing handler address used during slash execution must match the handler configured in the vault. Updates to handler addresses must propagate to all existing vaults.

**Property (Formal):**
$$\forall v \in \text{vaults}: \text{vault.slashHandler}(v) = \text{core.assetSlashingHandler}(v.\text{asset})$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires handler-based slashing architecture)

**Conditions:**
- Applies to protocols where slashing is routed through handler contracts (Karak)
- Handler updates must be synchronized across all existing vaults

**Source Evidence:**
- Protocol: Karak | Report: `reports/eigenlayer_findings/h-02-the-operator-can-create-a-nativevault-that-can-be-silently-unslashable.md`
- Protocol: Karak | Report: `reports/eigenlayer_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md`

**Why This Matters:**
Handler mismatch silently disables slashing — the vault's check always fails because the addresses diverge.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-1-unslashable-vault-creation-000`

---

### STAKING-SLASHING-009: Slashing Must Not Be Avoidable via Over-Commitment

**Property (English):**
A staker who has over-committed (verified more validators than their actual balance supports) must not be able to use the over-commitment status to bypass or reduce slashing penalties.

**Property (Formal):**
$$\forall u: \text{overCommitted}(u) \centernot\implies \text{reducedSlashing}(u)$$

**Mode:** NEGATIVE
**Priority:** MEDIUM
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires beacon chain verification with over-commitment)

**Conditions:**
- Applies to EigenLayer-style protocols with beacon chain balance verification
- Over-committed stakers should be penalized, not exempted from slashing

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md`

**Why This Matters:**
Over-commitment bypass allows validators to misbehave while appearing to have fewer slashable assets than they actually committed.

---

### STAKING-SLASHING-010: Slashing Factor Must Reflect Current State

**Property (English):**
The beaconChainSlashingFactor or equivalent must be computed from the current (not stale) protocol state. It must be updated whenever slashing events or balance changes occur, not cached from a previous state.

**Property (Formal):**
$$\forall \text{slashExec}(t): \text{slashingFactor}(t) = \frac{\text{currentSlashedAmount}(t)}{\text{currentTotalStake}(t)}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires slashing factor computation)

**Conditions:**
- Must use latest state root, not a cached or stale value
- Must handle the interaction between slashing factor and delegation changes

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/beaconchainslashingfactor-is-negated-after-delegation.md`

**Why This Matters:**
Stale slashing factors cause over-slashing or under-slashing, both of which compromise protocol correctness.

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-5-slashing-factor-miscalculati-004`

---

### STAKING-SLASHING-011: Denied Slashing Prevention

**Property (English):**
Malicious actors must not be able to deny or prevent slashing execution through any mechanism, including insufficient deposits, strategic timing, or transaction ordering manipulation.

**Property (Formal):**
$$\forall \text{slashRequest}(s): \exists \text{execution}(e) : \text{completes}(e, s) = \text{true}$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any staking protocol with slashing
- Must resist: insufficient deposit griefing, frontrunning slash with withdrawal, gas manipulation

**Source Evidence:**
- Protocol: Various | Report: `reports/cosmos_cometbft_findings/denial-of-slashing.md`
- Protocol: Various | Report: `reports/cosmos_cometbft_findings/elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md`

**Why This Matters:**
If slashing can be denied, the entire proof-of-stake or restaking economic security model collapses.

**Known Violations (from DB):**
- DB/cosmos/app-chain/validation/input-validation-vulnerabilities.md — denial of slashing patterns

---

### STAKING-SLASHING-012: Slashing Transparency and Notification

**Property (English):**
When a slashing event is pending or has been executed, all affected stakers must have a transparent mechanism to detect the event before it impacts their positions. The delay between slashing announcement and execution must be sufficient for stakers to react if designed to allow it.

**Property (Formal):**
$$\forall \text{slash}(s): \exists \text{notification}(n, s): t_{\text{notification}}(n) \leq t_{\text{execution}}(s) - \text{MIN\_NOTICE\_PERIOD}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires delayed slashing execution)

**Conditions:**
- Applies to protocols with delayed slashing (e.g., 2-day finalization window)
- Stakers who joined after the slashing event was initiated should not be slashed unfairly

**Source Evidence:**
- Protocol: Various | Report: `reports/cosmos_cometbft_findings/m-04-delayed-slashing-window-and-lack-of-transparency-for-pending-slashes-could-.md`

**Why This Matters:**
Without transparency, new stakers join positions that are about to be slashed, suffering unfair losses.
