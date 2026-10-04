# Staking: Operator & Delegation Invariants

> Canonical invariants for operator management, delegation correctness, and minipool
> security in staking and restaking protocols. Mined from production protocols
> (EigenLayer, GoGoPool, Rio Network, Karak, Casimir), audit reports, and the
> Horus. Language-agnostic and protocol-agnostic.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: operator-delegation
- **Sources**: EigenLayer, GoGoPool, Rio Network, Karak, Casimir, Avail, Renzo, Kelp DAO
- **Last updated**: 2026-03-13
- **Invariant count**: 10

---

## Invariants

### STAKING-OPERATOR-001: Operator Cannot Censorship-Lock Staker Funds

**Property (English):**
Operators must not be able to unilaterally lock staker funds indefinitely. If operators can initiate undelegation, the staker must have either: (a) the ability to immediately re-delegate elsewhere, or (b) a time-bounded path to full withdrawal without operator cooperation.

**Property (Formal):**
$$\forall u \in \text{stakers}: \exists \text{path}(u): \text{canWithdraw}(u, t + \text{MAX\_DELAY}) = \text{true} \quad \text{without operator cooperation}$$

**Mode:** DUAL
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires delegation model)

**Conditions:**
- Applies to protocols where operators can force undelegation
- Repeated undelegation every cooldown period = permanent censorship

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/eig-17-operator-or-delegation-approver-have-the-power-to-censor-delegated-stakers.md`

**Why This Matters:**
An operator who can repeatedly force undelegation can lock staker funds forever, extorting stakers for their own capital.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-1-operator-censorship-via-forc-000`

---

### STAKING-OPERATOR-002: Minipool State Machine Integrity

**Property (English):**
Minipool or node operator state machines must enforce valid state transitions. A minipool in a terminal state (Withdrawable, Error, Finished) must not allow re-initialization or ownership changes.

**Property (Formal):**
$$\forall m \in \text{minipools}: \text{state}(m) \in \text{TERMINAL} \implies \neg \text{canReinitialize}(m) \land \neg \text{canChangeOwner}(m)$$

**Mode:** NEGATIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires minipool/node operator pattern)

**Conditions:**
- Applies to protocols with reusable minipool addresses (GoGoPool, Rocket Pool)
- Key re-creation after terminal state must validate no existing ownership

**Source Evidence:**
- Protocol: GoGoPool | Report: `reports/eigenlayer_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md`

**Why This Matters:**
Hijacking a minipool lets the attacker claim the staked ETH and rewards associated with the original operator.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-2-minipool-state-machine-hijac-001`

---

### STAKING-OPERATOR-003: Undelegation Must Not Break Exchange Rate

**Property (English):**
When an operator is undelegated (voluntarily or by the protocol), the LRT exchange rate must be preserved. The undelegation process must not create a window where the rate drops below the true value.

**Property (Formal):**
$$\forall \text{undelegate}(o, t): \text{rate}(t+1) \geq \text{rate}(t) - \epsilon$$

where $\epsilon$ accounts for gas costs and rounding

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires delegation with LRT)

**Conditions:**
- Applies to LRT protocols where operator undelegation triggers EigenLayer withdrawal
- Must handle the transition period where assets move from strategies to pending withdrawal

**Source Evidence:**
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/h-3-malicious-operators-can-undelegate-themselves-to-manipulate-the-lrt-exchange-.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/malicious-operator-undelegation-can-break-the-ratio.md`

**Why This Matters:**
Operators can profit by shorting the LRT, triggering undelegation to crash the rate, buying cheap, then re-delegating.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-3-undelegation-breaking-lrt-ex-002`

---

### STAKING-OPERATOR-004: Operator Registry Data Structure Integrity

**Property (English):**
Data structures tracking operators (heaps, arrays, mappings) must remain consistent after operator additions and removals. Removing an operator must not corrupt the data structure or leave stale references.

**Property (Formal):**
$$\forall \text{remove}(o): \text{heapInvariant}(t+1) = \text{true} \land \neg \exists \text{ref}(o) \in \text{activeOperators}(t+1)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires ordered operator data structures)

**Conditions:**
- Applies to protocols using heaps or sorted structures for operator allocation
- Common pattern: min-heap for load balancing across operators

**Source Evidence:**
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/h-8-heap-incorrectly-stores-the-removed-operator-id-leading-to-division-by-zero.md`

**Why This Matters:**
Heap corruption from operator removal causes division by zero on subsequent operations, permanently breaking deposit/withdrawal flows.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-4-heap-corruption-from-operato-003`

---

### STAKING-OPERATOR-005: Delegation Enforcer Integrity

**Property (English):**
Delegation enforcers (contracts that validate delegation conditions) must not be bypassable through frontrunning, state modification, or exploiting the evaluation order. Conditions checked by enforcers must still hold after the delegation executes.

**Property (Formal):**
$$\forall \text{delegate}(u, o): \text{enforcerCondition}(u, o, t_{\text{check}}) \implies \text{enforcerCondition}(u, o, t_{\text{execute}})$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires delegation enforcer pattern)

**Conditions:**
- Applies to protocols with programmable delegation conditions
- Must handle: state-modifying enforcers, TOCTOU between check and execution

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/open-delegations-nativetokenpaymentenforcer-front-running-bypass.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/totalbalanceenforcer-validation-bypass-with-state-modifying-enforcers.md`

**Why This Matters:**
Bypassed enforcers allow delegation without meeting required conditions (e.g., payment, balance), undermining the protocol's delegation marketplace.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-5-delegation-enforcer-bypasses-004`

---

### STAKING-OPERATOR-006: Stakes Must Be Forwarded After Delegation

**Property (English):**
When a user delegates to an operator, the staked assets must be forwarded to the appropriate strategy or validator. Stakes that remain unfunded after delegation create accounting discrepancies.

**Property (Formal):**
$$\forall \text{delegate}(u, o, a): \text{strategyBalance}(o)' = \text{strategyBalance}(o) + a \quad \text{within bounded time}$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires stake forwarding after delegation)

**Conditions:**
- Applies to protocols with lazy stake forwarding (buffer → strategy → validator)
- Forwarding failure must be detectable and recoverable

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md`

**Why This Matters:**
Unforwarded stakes earn no rewards and may become permanently locked if the withdrawal path expects them in a strategy.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-6-stakes-not-forwarded-post-de-005`

---

### STAKING-OPERATOR-007: Operator Registration Frontrunning Prevention

**Property (English):**
Operator registration must not be frontrunnable in a way that allows an adversary to register as an operator before a legitimate registrant, stealing their delegated stake or configured parameters.

**Property (Formal):**
$$\forall \text{register}(o): \text{commitment}(o) \lor \text{accessControl}(o) \lor \text{uniqueIdentifier}(o)$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires open operator registration)

**Conditions:**
- Applies to protocols with permissionless operator registration
- Must use commit-reveal, whitelisting, or unique identifiers

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/deposits-front-run-by-malicious-operator.md`
- DB: `general-defi-restaking-operator-delegation-vulnerabil-7-front-running-operator-regis-006`

**Why This Matters:**
Frontrunning registration captures delegated stake intended for a different operator.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-7-front-running-operator-regis-006`

---

### STAKING-OPERATOR-008: Operator Undelegation Gas Bounds

**Property (English):**
Operator undelegation processes must have bounded gas costs. Linear iteration over unbounded delegations or token transfers during undelegation must not exceed block gas limits.

**Property (Formal):**
$$\forall \text{undelegate}(o): \text{gasCost}(\text{undelegate}(o)) \leq \text{BLOCK\_GAS\_LIMIT}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires multi-delegator undelegation)

**Conditions:**
- Applies when undelegation processes all delegators in a single transaction
- Requires pagination or per-delegator undelegation

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-chain-halt.md`

**Why This Matters:**
Unbounded gas consumption during undelegation can cause chain halt (on appchains) or permanent inability to undelegate.

---

### STAKING-OPERATOR-009: Validator Activation Guard

**Property (English):**
New stakes must only be delegated to active validators. Stakes delegated to inactive, exiting, or jailed validators earn no rewards and may be permanently locked.

**Property (Formal):**
$$\forall \text{delegate}(s, v): \text{isActive}(v) = \text{true}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol that selects validators for delegation
- Must check validator status at delegation time, not just registration time

**Source Evidence:**
- Protocol: Various | Report: `reports/lst_restaking_findings/m-04-new-stakes-delegated-even-when-validator-is-inactive.md`

**Why This Matters:**
Delegating to inactive validators wastes user capital — funds are locked without generating any rewards.

---

### STAKING-OPERATOR-010: Node Withdrawal Address Integrity

**Property (English):**
A node's withdrawal address must only be changeable by the node owner through an authenticated process. No external contract or third party may change a node's withdrawal address without proper authorization.

**Property (Formal):**
$$\forall \text{setWithdrawalAddr}(n, a): \text{msg.sender} = \text{owner}(n) \lor \text{authorizedBy}(\text{owner}(n))$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any staking protocol with configurable withdrawal addresses
- Change must require multi-step verification or timelock

**Source Evidence:**
- Protocol: Various | Report: `reports/lst_restaking_findings/any-network-contract-can-change-any-nodes-withdrawal-address.md`

**Why This Matters:**
Stolen withdrawal address means all future rewards and the principal go to the attacker.
