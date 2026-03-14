# Staking: Reward Distribution Invariants

> Canonical invariants for staking reward distribution correctness, frontrunning resistance,
> and accounting integrity. Mined from production protocols (EigenLayer, Lido, Rio Network,
> Renzo, GMX, Synthetix), audit reports, and the Vulnerability Database.
> Language-agnostic and protocol-agnostic.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: reward-distribution
- **Sources**: EigenLayer, Lido, Rio Network, Renzo, Puffer, CAP Labs, Notional, Synthetix, GMX
- **Last updated**: 2026-03-13
- **Invariant count**: 11

---

## Invariants

### STAKING-REWARD-001: Reward Conservation

**Property (English):**
The total rewards distributed across all stakers must equal the total rewards received by the protocol. No rewards may be created, destroyed, or permanently locked during distribution.

**Property (Formal):**
$$\forall t: \sum_{u \in \text{stakers}} \text{rewardsClaimed}(u, t) + \text{rewardsUnclaimed}(t) = \text{totalRewardsReceived}(t)$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any staking reward distribution mechanism
- Must hold across arbitrary stake/unstake/claim sequences
- Rounding errors must be bounded and accounted for

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/m-16-execution-layer-rewards-are-lost.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/inability-to-claim-protocol-rewards-missing-implementation.md`

**Why This Matters:**
Lost rewards represent direct financial loss to stakers. Locked or unclaimable rewards accumulate as protocol debt.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-5-rewards-lost-missing-impleme-004`

---

### STAKING-REWARD-002: Time-Weighted Reward Distribution

**Property (English):**
Rewards must be distributed proportionally to stake-weighted time. A staker who deposits immediately before reward distribution must not capture the same per-share reward as a staker who has been deposited for the full reward period.

**Property (Formal):**
$$\forall u: \text{reward}(u) \propto \int_{t_{\text{deposit}}(u)}^{t_{\text{current}}} \text{stake}(u, \tau) \, d\tau$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any staking system distributing yield/rewards over time
- JIT (just-in-time) staking is the primary attack vector

**Source Evidence:**
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/m-06-sandwiching-claimdelayedwithdrawals-to-steal-eth-rewards.md`
- Protocol: CAP Labs | Report: `reports/eigenlayer_findings/reward-distribution-enables-front-running-attacks-and-reward-siphoning.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/m-03-no-cooldown-in-recoverunstaking-enables-reward-siphoning.md`

**Why This Matters:**
Without time-weighting, MEV bots extract ~50% of every reward distribution by sandwiching the claim transaction.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-1-sandwich-front-running-rewar-000`
- `general-defi-restaking-reward-distribution-vulnerabil-7-reward-dilution-via-just-in--006`

---

### STAKING-REWARD-003: Reward Claim Frontrunning Resistance

**Property (English):**
Permissionless reward claim functions that instantly increase TVL must have protections against sandwich attacks. Either: (a) rewards are distributed over time, (b) a cooldown prevents instant withdrawal after deposit, or (c) the claim updates a per-share accumulator.

**Property (Formal):**
$$\forall \text{claim}(c, t): \text{TVL}(t+1) > \text{TVL}(t) \implies \text{withdrawalDelay}(t) > 0 \lor \text{rewardsVested}(c) = \text{true}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol where reward claims change the exchange rate
- Permissionless claims require stronger protection than access-controlled claims

**Source Evidence:**
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/m-06-sandwiching-claimdelayedwithdrawals-to-steal-eth-rewards.md`
- Protocol: Redacted Cartel | Report: `reports/eigenlayer_findings/m-sandwich-attack-on-autopxgmx-compound.md`

**Why This Matters:**
Each permissionless claim without sandwich protection transfers a portion of long-term staker rewards to MEV bots.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-1-sandwich-front-running-rewar-000`

---

### STAKING-REWARD-004: msg.sender Correctness in Reward Staking

**Property (English):**
When rewards are re-staked (compounded) on behalf of a user, the `msg.sender` and the reward beneficiary must be correctly tracked. The function must credit rewards to the actual staker, not the transaction caller.

**Property (Formal):**
$$\forall \text{restake}(r): \text{beneficiary}(r) = \text{originalStaker}(r) \neq \text{msg.sender}(r)$$

(unless msg.sender is the staker themselves)

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires permissionless restaking functions)

**Conditions:**
- Applies to any protocol where a third party can trigger reward restaking
- Common pattern: keeper/operator calls `restakeRewards()` on behalf of stakers

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/critical-direct-loss-of-rewards-on-restaking-msg-sender-confusion.md`

**Why This Matters:**
msg.sender confusion means the keeper/attacker receives the restaked rewards instead of the actual staker — direct loss of user funds.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-2-msg-sender-confusion-in-rewa-001`

---

### STAKING-REWARD-005: No Reward Double-Counting

**Property (English):**
Rewards must not be counted more than once in the accounting system. Delayed rewards, pending rewards, and restaked rewards must each be tracked in exactly one bucket.

**Property (Formal):**
$$\forall r \in \text{rewards}: |\{b \in \text{buckets} : r \in b\}| = 1$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol with multiple reward tracking states (pending, delayed, claimed, restaked)
- State transitions between buckets must be atomic

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-delayed-balance-or-rewards-a.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/delayed-rewards-can-be-claimed-without-updating-internal-accounting.md`

**Why This Matters:**
Double-counting inflates the reward pool, causing the protocol to distribute more than it received and eventually becoming insolvent.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-3-reward-accounting-double-cou-002`

---

### STAKING-REWARD-006: Stale Snapshot Cleanup on Unstaking

**Property (English):**
When a user unstakes, all associated reward snapshots, bucket entries, and accumulator states must be cleaned up or finalized. Stale snapshots from unstaked positions must not affect future reward calculations.

**Property (Formal):**
$$\forall \text{unstake}(u, t): \forall t' > t : \text{rewardSnapshot}(u, t') = \emptyset \lor \text{finalized}(\text{rewardSnapshot}(u, t))$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol using snapshot-based or accumulator-based reward tracking
- Old snapshots must not contaminate new staking positions after re-entry

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/h-rewardsmanager-doesnt-delete-old-bucket-snapshot-on-unstaking.md`

**Why This Matters:**
Stale snapshots cause reward miscalculation — users may receive inflated or zero rewards based on outdated state.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-4-stale-snapshot-data-after-un-003`

---

### STAKING-REWARD-007: Reentrancy Protection on Reward Claims

**Property (English):**
Reward claim functions must be protected against reentrancy. Reward state must be updated before any external calls (token transfers, ETH sends).

**Property (Formal):**
$$\forall \text{claimReward}(c): \text{rewardState.update}(c) \prec \text{externalCall}(c)$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any reward claim that transfers tokens or ETH
- Especially critical when multiple reward tokens or callback-enabled tokens are involved

**Source Evidence:**
- Protocol: Notional | Report: `reports/eigenlayer_findings/h-steal-reward-tokens-via-reentrancy-in-vaultrewarderlib.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/h-withdrawing-stake-before-claiming-rewards-permanent-loss.md`

**Why This Matters:**
Reentrancy in reward claims enables claiming the same rewards multiple times, draining the reward pool.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-6-reentrancy-based-reward-thef-005`

---

### STAKING-REWARD-008: Reward Claims Must Be Accessible

**Property (English):**
Reward claim functions must be implemented and callable by entitled users. Missing implementations, gas limits, or balance thresholds must not prevent legitimate reward claims.

**Property (Formal):**
$$\forall u \in \text{stakers}: \text{entitledRewards}(u) > 0 \implies \exists f : \text{callable}(f, u) \land \text{claimsRewards}(f, u)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Must not revert due to: unimplemented functions, low gas forwarding, balance thresholds
- Must handle edge cases: EigenPod balance exceeding thresholds, self-referral loops

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/inability-to-claim-protocol-rewards-missing-implementation.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/m-05-low-gas-limit-prevents-reward-receipt.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/h-reward-calculation-blocked-if-eigenpod-balance-exceeds-16-eth.md`

**Why This Matters:**
Unclaimable rewards represent permanent loss for stakers even though the protocol received them.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-5-rewards-lost-missing-impleme-004`

---

### STAKING-REWARD-009: Withdraw Stake Before Claim Protection

**Property (English):**
If a user withdraws their stake, any unclaimed rewards must either be auto-claimed to the user or preserved for later claim. Withdrawing must not cause permanent loss of accrued rewards.

**Property (Formal):**
$$\forall \text{withdraw}(u, t): \text{accruedRewards}(u, t) > 0 \implies \text{claimable}(u, t+1) \geq \text{accruedRewards}(u, t) \lor \text{autoClaimed}(u, t)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies when staking and reward systems are separate contracts/modules
- Must handle the ordering: unstake then claim vs claim then unstake

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/h-withdrawing-stake-before-claiming-rewards-permanent-loss.md`

**Why This Matters:**
Users who unstake without first claiming lose all accrued rewards permanently.

**Known Violations (from DB):**
- `general-defi-restaking-reward-distribution-vulnerabil-6-reentrancy-based-reward-thef-005`

---

### STAKING-REWARD-010: Reward Distribution Access Control

**Property (English):**
Functions that trigger reward distribution or modify reward accounting must have appropriate access control. Permissionless claim functions must not allow arbitrary modification of reward state.

**Property (Formal):**
$$\forall f \in \text{rewardModifiers}: \text{hasAccess}(\text{msg.sender}, f) = \text{true} \lor f \in \text{designedPermissionless}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Reward distribution triggers should be access-controlled or have economic protections
- If permissionless by design, must have sandwich/frontrunning protections

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/m-missing-access-control-for-claiming-rewards.md`

**Why This Matters:**
Unprotected reward modification functions allow attackers to redirect or drain rewards.

---

### STAKING-REWARD-011: Rewards Must Not Be Restaked on User Exit

**Property (English):**
When a user is exiting (withdrawing all stake), their rewards must be returned to them as liquid assets, not automatically restaked into the protocol. Exit must mean full exit including rewards.

**Property (Formal):**
$$\forall \text{exit}(u): \text{isFullExit}(u) \implies \text{rewardsDelivered}(u) = \text{liquid} \neq \text{restaked}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires reward restaking feature)

**Conditions:**
- Applies to protocols with auto-compound or forced restaking of rewards
- Exit path must override auto-compound behavior

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/m-user-rewards-restaked-on-exit-instead-of-withdrawn.md`

**Why This Matters:**
Restaking rewards on exit forces the user through another withdrawal cycle, defeating the purpose of exit.
