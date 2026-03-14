# Staking: General Staking Invariants

> Universal staking properties that apply across all staking protocol types (PoS,
> liquid staking, restaking, delegated staking). These are protocol-agnostic safety
> properties capturing fundamental staking correctness guarantees. Mined from
> production protocols, EIP specs, Cosmos SDK, and the Vulnerability Database.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: general-staking
- **Sources**: Lido, EigenLayer, Cosmos SDK, Rocket Pool, Babylon, GoGoPool, Casimir, Solana SPL Stake Pool
- **Last updated**: 2026-03-13
- **Invariant count**: 14

---

## Invariants

### STAKING-GENERAL-001: Stake Conservation

**Property (English):**
The total value of all staked assets must be conserved across all protocol states. Every unit of value entering the protocol must be accounted for as either: actively staked, in a pending state (withdrawal queue, activation queue), or in an earned rewards pool.

**Property (Formal):**
$$\sum \text{deposits}(0..t) = \text{activeStake}(t) + \text{pendingWithdrawals}(t) + \text{pendingActivations}(t) + \text{claimedWithdrawals}(0..t) + \text{claimedRewards}(0..t) + \text{slashingLosses}(0..t)$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to every staking protocol
- Must hold across all reachable states, including edge cases (zero deposits, max validators)

**Source Evidence:**
- Protocol: Lido | Property: stETH total supply == total pooled ether
- Protocol: Cosmos SDK | Module: x/staking, bonded + unbonding + unbonded = total staked
- Cross-reference: STAKING-SHARE-001 (supply = sum of balances)

**Why This Matters:**
Violation means the protocol has either created or destroyed value — direct fund loss or permanent insolvency.

---

### STAKING-GENERAL-002: Minimum Deposit Threshold

**Property (English):**
Every deposit must meet the protocol's minimum deposit threshold. Deposits below the minimum must be rejected to prevent dust attacks, share rounding exploitation, and validator activation failures.

**Property (Formal):**
$$\forall \text{deposit}(u, a): a \geq \text{MIN\_DEPOSIT} \lor \text{revert}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- MIN_DEPOSIT must be large enough to prevent first-depositor inflation attacks
- For validator-based staking (Ethereum PoS), minimum is 32 ETH for full validators

**Source Evidence:**
- Protocol: Lido | Min deposit: 1 wei (but uses virtual shares for inflation protection)
- Protocol: EigenLayer | Min deposit enforced per strategy
- Cross-reference: STAKING-SHARE-002 (first depositor inflation resistance)

**Why This Matters:**
Sub-minimum deposits enable share price inflation attacks and waste gas through impractical validators.

---

### STAKING-GENERAL-003: Epoch Boundary Consistency

**Property (English):**
Protocol state transitions tied to epochs or time periods must execute atomically. If a state transition begins, it must complete fully. Partial epoch transitions leave the protocol in an inconsistent state.

**Property (Formal):**
$$\forall \text{epochTransition}(e): \text{state}(\text{pre}(e)) \in \text{VALID} \implies \text{state}(\text{post}(e)) \in \text{VALID}$$

No intermediate state during the transition is observable by external calls.

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol with time-based state transitions
- EVM: single-transaction epoch transitions are atomic by default
- Multi-transaction epoch transitions (e.g., batched oracle reports) require careful ordering

**Source Evidence:**
- Protocol: Lido | Oracle reports update stETH supply atomically
- Protocol: Cosmos SDK | EndBlocker processes all epoch transitions atomically

**Why This Matters:**
Partial epoch transitions can be exploited: attacker observes partial state and extracts value before transition completes.

---

### STAKING-GENERAL-004: Access Control on Configuration Functions

**Property (English):**
All protocol configuration functions (fee changes, operator registration parameters, oracle addresses, pausing, strategy caps, withdrawal delays) must be restricted to authorized roles. No permissionless path may exist to modify protocol parameters.

**Property (Formal):**
$$\forall f \in \text{configFunctions}: \text{caller}(f) \in \text{authorizedRoles}(f)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Authorized roles should use multi-sig or timelock for critical parameters
- Fee changes, oracle updates, and pause toggles are common attack surfaces

**Source Evidence:**
- Protocol: Lido (DAO governance for parameter changes)
- Protocol: EigenLayer (multisig for pausable functions)
- Cross-reference: ACCESS-CONTROL-ROLE-001

**Why This Matters:**
Unauthorized parameter changes can drain the protocol (setting fees to 100%, redirecting oracle, disabling slashing).

---

### STAKING-GENERAL-005: Emergency Pause Effectiveness

**Property (English):**
When the protocol is paused, all value-moving operations (deposits, withdrawals, claims, rewards, delegations) must be blocked. Pausing must not leave the protocol in a state where locked funds become permanently inaccessible.

**Property (Formal):**
$$\text{paused} = \text{true} \implies \forall f \in \text{valueMovingFunctions}: \text{revert}(f)$$
$$\text{unpause}() \implies \forall \text{locked}(u): \text{canWithdraw}(u, t + \text{DELAY})$$

**Mode:** DUAL
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Pause must be immediate (no delay for emergency response)
- Unpause must not skip queued operations or corrupt state
- View functions must remain accessible during pause

**Source Evidence:**
- Protocol: EigenLayer (Pausable with granular function-level pausing)
- Protocol: Lido (pausable stETH)

**Why This Matters:**
Ineffective pause allows continued exploitation during incidents. Permanent pause causes fund lockup.

---

### STAKING-GENERAL-006: Validator Lifecycle State Machine

**Property (English):**
Validators must follow a strict lifecycle: Pending → Active → Exiting → Exited → Withdrawable. Invalid state transitions (e.g., Exited → Active without re-registration) must be rejected.

**Property (Formal):**
$$\forall v: \text{transition}(v, s_1, s_2) \in \text{VALID\_TRANSITIONS} \quad \text{where}$$
$$\text{VALID\_TRANSITIONS} = \{(\text{Pending}, \text{Active}), (\text{Active}, \text{Exiting}), (\text{Exiting}, \text{Exited}), (\text{Exited}, \text{Withdrawable})\}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol that tracks validator states
- Re-activation from Exited requires fresh registration and deposit

**Source Evidence:**
- Ethereum Beacon Chain Spec: Validator lifecycle
- Protocol: Cosmos SDK x/staking: Bonded/Unbonding/Unbonded states
- Cross-reference: STAKING-OPERATOR-002 (minipool state machine integrity)

**Why This Matters:**
Invalid state transitions allow validators to skip exit queues, avoid slashing, or re-enter without proper bonding.

---

### STAKING-GENERAL-007: Reward Rate Bounds

**Property (English):**
The staking reward rate must be bounded within configured min/max parameters. Sudden reward rate spikes (from oracle manipulation or incorrect calculation) must be capped to prevent inflation or share price manipulation.

**Property (Formal):**
$$\text{MIN\_RATE} \leq \text{rewardRate}(t) \leq \text{MAX\_RATE} \quad \forall t$$
$$|\text{rewardRate}(t+1) - \text{rewardRate}(t)| \leq \text{MAX\_RATE\_CHANGE}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- MAX_RATE_CHANGE prevents oracle manipulation from causing instant massive rewards
- Must account for both positive rewards and negative rewards (slashing penalties)

**Source Evidence:**
- Protocol: Lido | Oracle sanity checks: CL balance increase limit per report
- Cross-reference: STAKING-EXCHANGE-RATE-003 (circuit breaker)

**Why This Matters:**
Unbounded reward rate allows attacker to inflate share price by injecting fake rewards, then withdraw at inflated rate.

---

### STAKING-GENERAL-008: No Value Extraction During Identity Rotation

**Property (English):**
When a validator or operator rotates their signing key, withdrawal key, or commission rate, the rotation must not create a value extraction opportunity. Pending rewards must be settled before rotation; increased commission must not apply retroactively.

**Property (Formal):**
$$\forall \text{rotate}(v, \text{key}): \text{pendingRewards}(v, t) = \text{settled} \land \text{commission}(v, t+1) \text{ applies only to future rewards}$$

**Mode:** NEGATIVE
**Priority:** MEDIUM
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Key rotation is common in long-lived staking protocols
- Commission changes must have a delay or apply prospectively

**Source Evidence:**
- Protocol: Cosmos SDK | Commission change delay
- Protocol: Various | Report: `reports/lst_restaking_findings/commission-rate-change-findings.md`

**Why This Matters:**
Retroactive commission changes or unsettled rewards during rotation let operators steal staker earnings.

---

### STAKING-GENERAL-009: Rebasing Token Supply Consistency

**Property (English):**
For rebasing staking tokens (like stETH), the total supply must equal the total pooled value at all times. Any oracle update that changes the total pooled value must atomically update all derived quantities (share price, per-holder balances).

**Property (Formal):**
$$\text{totalSupply}(t) = \text{totalPooledAssets}(t)$$
$$\forall u: \text{balance}(u, t) = \text{shares}(u) \times \frac{\text{totalPooledAssets}(t)}{\text{totalShares}(t)}$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires rebasing token)

**Conditions:**
- Applies to rebasing liquid staking tokens (stETH, not wstETH)
- Oracle report that changes totalPooledAssets must be atomic with balance recalculation

**Source Evidence:**
- Protocol: Lido | stETH rebase mechanism
- Cross-reference: STAKING-SHARE-001 (supply = sum of balances)

**Why This Matters:**
Non-atomic rebase creates a window where share price differs from spot price, enabling MEV extraction.

---

### STAKING-GENERAL-010: Cooldown Period Integrity

**Property (English):**
Cooldown periods for unstaking, withdrawal, or undelegation must be enforced consistently. A user must not be able to bypass the cooldown through contract interactions, multiple accounts, or protocol state transitions.

**Property (Formal):**
$$\forall \text{unstake}(u, t_0): \text{canWithdraw}(u) = \text{false} \quad \forall t \in [t_0, t_0 + \text{COOLDOWN})$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Cooldown may be bypassed if: (a) secondary market for withdrawal NFTs exists, (b) protocol allows partial unstake + restake cycles, (c) flash loan can manipulate cooldown state
- Must be enforced per-position, not per-account

**Source Evidence:**
- Protocol: EigenLayer | 7-day withdrawal delay
- Protocol: Lido | Withdrawal queue turnaround time
- Protocol: Cosmos SDK | 21-day unbonding period

**Why This Matters:**
Cooldown bypass eliminates the time buffer needed for slashing enforcement — exiting before penalty application.

**Known Violations (from DB):**
- `general-defi-restaking-slashing-vulnerabilities-4-slashing-bypass-via-timing-003`

---

### STAKING-GENERAL-011: No Staking Reward Farming via CREATE2

**Property (English):**
Users must not be able to amplify staking rewards by creating multiple staking positions using deterministic address generation (CREATE2). The protocol must either verify uniqueness of staking entities or ensure rewards are proportional regardless of position splitting.

**Property (Formal):**
$$\text{rewards}(u, a) = \text{rewards}(\{u_1, u_2, ...\}, \{a_1, a_2, ...\}) \quad \text{where } \sum a_i = a$$

Splitting a stake $a$ across $n$ addresses must yield the same total reward as staking $a$ from one address.

**Mode:** NEGATIVE
**Priority:** MEDIUM
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires per-address reward bonuses or thresholds)

**Conditions:**
- Applies when reward calculation has non-linear per-address components
- Bootstrap programs, airdrops, or governance weight based on staker count are vulnerable

**Source Evidence:**
- DB: `unique` manifest | Pattern: Staking reward farming via CREATE2 address generation

**Why This Matters:**
Non-linear staking rewards incentivize Sybil attacks via CREATE2 address farming.

**Known Violations (from DB):**
- `unique-staking-reward-farming-via-create2-address-generation-000`

---

### STAKING-GENERAL-012: Protocol Fee Upper Bound

**Property (English):**
Protocol fees (management fee, performance fee, withdrawal fee) must have a hard-coded upper bound. Even privileged roles must not be able to set fees above the maximum.

**Property (Formal):**
$$\forall f \in \text{fees}: f \leq \text{MAX\_FEE}_f \quad \text{where MAX\_FEE is immutable}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- MAX_FEE should be reasonable (e.g., 50% max for performance fee, 2% for management)
- Must be enforced in the setter, not just documented
- Applies to: commission rates, protocol fees, treasury allocation percentages

**Source Evidence:**
- Protocol: Lido | 10% fee cap (5% treasury + 5% node operators)
- Protocol: Yearn V3 | Configurable fee caps

**Why This Matters:**
Without hard caps, a compromised governance can set fees to 100% and drain all staker rewards.

---

### STAKING-GENERAL-013: Cross-Contract Balance Synchronization

**Property (English):**
When a staking protocol consists of multiple contracts (deposit contract, strategy contract, withdrawal contract, reward distributor), the sum of balances across all contracts must equal the total protocol value. No value must exist in an untracked contract.

**Property (Formal):**
$$\text{totalValue}(t) = \sum_{c \in \text{protocolContracts}} \text{balance}(c, t) \quad \forall t$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Must include: deposit buffer, strategy deployments, withdrawal queue, reward pools
- ETH in transit (validator deposits not yet active) must be tracked in stakedButUnverified

**Source Evidence:**
- Protocol: EigenLayer (EigenPod + DelegationManager + StrategyManager)
- Protocol: Lido (stETH + Withdrawal Queue + Node Operator registry)
- Cross-reference: STAKING-BEACON-003 (stakedButUnverified tracking)

**Why This Matters:**
Untracked balances across contracts create exploitable discrepancies between reported and actual protocol value.

---

### STAKING-GENERAL-014: Delegation Proportional Reward Distribution

**Property (English):**
Rewards must be distributed to delegators proportionally to their stake weight and staking duration. No delegator should receive more or less than their fair share, regardless of when other delegators enter or exit.

**Property (Formal):**
$$\forall u \in \text{delegators}: \text{reward}(u) = \int_{t_{\text{stake}}}^{t_{\text{unstake}}} \frac{\text{stake}(u, t)}{\text{totalStake}(t)} \times \text{emissionRate}(t) \, dt$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Commonly implemented via reward-per-token accumulator pattern
- Must handle: late joiners (no retroactive rewards), early exiters (rewards up to exit only)
- Cosmos SDK: F1 fee distribution handles this natively

**Source Evidence:**
- Protocol: Synthetix (rewardPerToken accumulator)
- Protocol: Cosmos SDK (F1 distribution)
- Cross-reference: STAKING-REWARD-002 (time-weighted distribution)

**Why This Matters:**
Non-proportional distribution lets attackers time entries/exits to claim outsized rewards at others' expense.
