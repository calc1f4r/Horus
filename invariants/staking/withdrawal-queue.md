# Staking: Withdrawal Queue Invariants

> Canonical invariants for staking withdrawal queue correctness, fund accessibility,
> and slippage protection. Mined from production protocols (EigenLayer, Lido, Renzo,
> Rio Network, Puffer, Kelp, Karak), audit reports, and the Vulnerability Database.
> Language-agnostic and protocol-agnostic.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: withdrawal-queue
- **Sources**: EigenLayer, Lido, Renzo, Rio Network, Puffer, Kelp DAO, Karak, Tagus V2, RestakeFi, Ethena
- **Last updated**: 2026-03-13
- **Invariant count**: 14

---

## Invariants

### STAKING-WITHDRAWAL-001: Withdrawal Queue Conservation of Value

**Property (English):**
The total value across all states (deposited, queued for withdrawal, claimable, claimed) must equal the total assets controlled by the protocol. No value may be created or destroyed during state transitions.

**Property (Formal):**
$$\forall t: \text{depositedAssets}(t) + \text{queuedWithdrawals}(t) + \text{claimableAssets}(t) = \text{totalControlledAssets}(t)$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol with asynchronous withdrawal
- Must hold across all state transitions: request, processing, claim, cancellation
- Slashing events may reduce total controlled assets proportionally

**Source Evidence:**
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/h-1-creating-new-withdrawal-requests-in-conjunction-with-settleepochfromeigenlay.md`
- Protocol: Tagus V2 | Report: `reports/eigenlayer_findings/_pendingwithdrawalamount-can-be-arbitrarily-reset.md`
- Protocol: Lido | Withdrawal queue accounting design

**Why This Matters:**
If value is lost during state transitions, some users cannot withdraw. If value is created, the protocol becomes insolvent.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-1-withdrawal-queue-manipulatio-000`

---

### STAKING-WITHDRAWAL-002: Epoch/Queue State Atomicity

**Property (English):**
Withdrawal epoch or queue state transitions must be atomic with the underlying settlement process. New withdrawal requests must not target an epoch/batch that is already being settled or has been consumed.

**Property (Formal):**
$$\forall \text{request}(r, t): \text{epoch}(r) > \text{lastSettledEpoch}(t) \land \text{epoch}(r) \neq \text{settlingEpoch}(t)$$

**Mode:** NEGATIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires epoch-based withdrawal queue)

**Conditions:**
- Applies to protocols using epoch-based batch withdrawals (Rio Network, Renzo with EigenLayer)
- Settlement initiation must increment the epoch counter atomically

**Source Evidence:**
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/h-1-creating-new-withdrawal-requests-in-conjunction-with-settleepochfromeigenlay.md`
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/h-2-setting-the-strategy-cap-to-0-does-not-update-the-total-shares-held-or-the-w.md`

**Why This Matters:**
Requests targeting an already-settling epoch create system deadlock: withdrawal tokens are burned but the underlying assets are consumed by the prior batch.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-1-withdrawal-queue-manipulatio-000`

---

### STAKING-WITHDRAWAL-003: Share-to-Asset Conversion Correctness at Withdrawal

**Property (English):**
When converting shares to assets during withdrawal, the conversion must use a consistent rate that accounts for the current protocol state. The rate must not differ from the rate visible to the user at request time beyond acceptable slippage.

**Property (Formal):**
$$\forall \text{withdrawal}(w): \left| \frac{\text{assetsReceived}(w)}{\text{sharesBurned}(w)} - \text{rate}(t_{\text{request}}) \right| \leq \text{MAX\_SLIPPAGE}$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any 2-step withdrawal where rate may change between request and settlement
- MAX_SLIPPAGE should be user-configurable or protocol-bounded

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/eig-7-direct-loss-of-user-principal-funds-when-processing-a-full-withdrawal-of-p.md`
- Protocol: Ethena | Report: `reports/eigenlayer_findings/m-14-value-of-ethernas-withdrawal-request-is-incorrect.md`
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/m-9-requestwithdrawal-doesnt-estimate-accurately-the-available-shares-for-withdr.md`

**Why This Matters:**
Incorrect conversion causes direct loss of user principal. Users burn shares but receive fewer assets than the exchange rate promises.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-2-share-amount-calculation-err-001`

---

### STAKING-WITHDRAWAL-004: No Permanent Fund Lockup

**Property (English):**
A user who has requested withdrawal must be able to eventually claim their assets within a bounded time period. No combination of protocol states, third-party actions, or queue conditions may permanently lock user funds.

**Property (Formal):**
$$\forall \text{request}(r): \exists t_{\text{claim}} : t_{\text{claim}} - t_{\text{request}} \leq \text{MAX\_WITHDRAWAL\_DELAY} \land \text{canClaim}(r, t_{\text{claim}}) = \text{true}$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Must hold regardless of: contract recipient types, queue ordering, other users' actions
- Failed individual requests in a batch must not block other requests
- Protocol must handle edge cases: last holder exit, zero supply, dust amounts

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/h-01-withdrawals-can-be-locked-forever-if-recipient-is-a-contract.md`
- Protocol: Kelp | Report: `reports/eigenlayer_findings/h-13-kelp_finalizecooldown-cannot-claim-the-withdrawal-if-adversary-would-reques.md`
- Protocol: RestakeFi | Report: `reports/eigenlayer_findings/m-21-funds-stuck-if-one-of-the-withdrawal-requests-cannot-be-finalized.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md`

**Why This Matters:**
Permanent fund lockup is the most severe staking vulnerability — users lose all deposited capital with no recourse.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-3-fund-lockup-during-withdrawa-002`

---

### STAKING-WITHDRAWAL-005: Withdrawal Delay Integrity

**Property (English):**
The minimum withdrawal delay must be enforced for all withdrawal paths. No action sequence (including re-staking, strategy changes, or L1 operation batching) may reduce the effective delay below the minimum.

**Property (Formal):**
$$\forall \text{withdrawal}(w): t_{\text{claim}}(w) - t_{\text{request}}(w) \geq \text{MIN\_WITHDRAWAL\_DELAY}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires enforced withdrawal delay)

**Conditions:**
- Applies to protocols with mandatory withdrawal cooldown periods
- Must survive: re-staking with shorter lockup, strategy cap changes, L1 operation batching
- Delay must be properly initialized during protocol upgrades

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/lockup-period-for-unstaking-can-be-decreased-by-staking-again-with-shorter-locku.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/withdrawaldelayblocks-cannot-be-initialised-after-m2-upgrade.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/withdrawal-delay-can-be-bypassed-when-l1-operations-processed-more-than-once-per.md`

**Why This Matters:**
Withdrawal delays serve as a security guarantee allowing the protocol to respond to slashing events. Bypassing the delay enables frontrunning slashing and escaping with unslashed funds.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-5-withdrawal-delay-bypass-004`

---

### STAKING-WITHDRAWAL-006: Slippage and Deadline Protection on Withdrawals

**Property (English):**
Withdrawal operations must include user-specified slippage protection (minimum assets received) and deadline parameters. The operation must revert if the received amount falls below the minimum or the deadline has passed.

**Property (Formal):**
$$\forall \text{withdraw}(w): \text{assetsReceived}(w) \geq \text{minAssetsOut}(w) \land \text{block.timestamp} \leq \text{deadline}(w)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any withdrawal that converts shares to assets at a variable rate
- Especially critical for protocols with MEV exposure

**Source Evidence:**
- Protocol: Renzo | Report: `reports/eigenlayer_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero-.md`
- Protocol: Various | Report: `reports/eigenlayer_findings/m-07-lack-of-slippage-and-deadline-during-withdraw-and-deposit.md`

**Why This Matters:**
Without slippage protection, MEV bots manipulate TVL before user transactions, extracting value through sandwich attacks.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-6-missing-slippage-deadline-pr-005`

---

### STAKING-WITHDRAWAL-007: Partial Failure Isolation

**Property (English):**
In batch withdrawal processing, failure of any single withdrawal request in the batch must not block other requests from being processed. Each request must be independently claimable.

**Property (Formal):**
$$\forall \text{batch}(B), \forall w_i, w_j \in B: \neg \text{canClaim}(w_i) \centernot\implies \neg \text{canClaim}(w_j)$$

**Mode:** NEGATIVE
**Priority:** MEDIUM
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires batch withdrawal processing)

**Conditions:**
- Applies to protocols that process multiple withdrawals in a single settlement
- Individual request failures (e.g., token transfer revert) must be caught and isolated

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/insufficient-handling-of-partial-failures-in-withdrawal-requests.md`
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/m-21-funds-stuck-if-one-of-the-withdrawal-requests-cannot-be-finalized.md`

**Why This Matters:**
A single poisoned withdrawal request (e.g., reverting ERC20 transfer) can permanently DOS all other requests in the same batch.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-7-partial-failure-handling-006`

---

### STAKING-WITHDRAWAL-008: Reentrancy Protection on Withdrawal Flows

**Property (English):**
All withdrawal functions (request, claim, finalize) must be protected against reentrancy. State updates must precede external calls (CEI pattern), and reentrancy guards must cover all state-modifying paths.

**Property (Formal):**
$$\forall f \in \{\text{requestWithdrawal}, \text{claimWithdrawal}, \text{finalizeWithdrawal}\}: \text{reentrancyGuard}(f) = \text{true} \lor \text{CEI}(f) = \text{true}$$

**Mode:** NEGATIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Especially critical for native ETH withdrawal flows (ETH transfers enable reentrancy)
- Must cover both user-initiated and permissionless claim paths

**Source Evidence:**
- Protocol: EigenLayer/Karak | Report: `reports/eigenlayer_findings/vlts3-13-direct-theft-of-surplus-balance-when-unstaking-sthype.md` — CRITICAL reentrancy during unstaking
- Protocol: Various | Report: `reports/eigenlayer_findings/h-redeemnative-reentrancy-enables-permanent-fund-freeze.md`

**Why This Matters:**
Reentrancy in withdrawal flows enables direct fund theft — attacker re-enters during ETH transfer to claim multiple times.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-8-reentrancy-and-access-contro-007`

---

### STAKING-WITHDRAWAL-009: Withdrawal Pausability

**Property (English):**
Withdrawal and claim functions must be pausable by authorized governance in emergency situations. The pause mechanism must be tested and functional.

**Property (Formal):**
$$\exists \text{pause}(): \text{isPaused}(t) \implies \forall \text{withdraw}(w, t): \text{reverts}(w)$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to all protocols — emergency pause is a fundamental safety mechanism
- Must cover all withdrawal paths including claim and finalize

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/m-02-withdrawals-and-claims-are-meant-to-be-pausable-but-it-is-not-possible-in-p.md`

**Why This Matters:**
If withdrawals cannot be paused during an exploit, the protocol cannot prevent fund drainage.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-8-reentrancy-and-access-contro-007`

---

### STAKING-WITHDRAWAL-010: Pending Withdrawal Amount Consistency

**Property (English):**
The tracked pending withdrawal amount must accurately reflect the sum of all unclaimed withdrawal requests. No permissionless function may reset or arbitrarily modify this value.

**Property (Formal):**
$$\forall t: \text{pendingWithdrawalAmount}(t) = \sum_{w \in \text{unclaimed}(t)} \text{amount}(w)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires withdrawal amount tracking)

**Conditions:**
- Applies to protocols that track aggregate pending withdrawal state
- Must be updated atomically with request creation, cancellation, and claim

**Source Evidence:**
- Protocol: Tagus V2 | Report: `reports/eigenlayer_findings/_pendingwithdrawalamount-can-be-arbitrarily-reset.md`

**Why This Matters:**
If the pending amount can be reset, `getTotalDeposited()` returns incorrect values, causing exchange rate manipulation.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-1-withdrawal-queue-manipulatio-000`

---

### STAKING-WITHDRAWAL-011: Slashing Must Apply to Queued Withdrawals

**Property (English):**
Assets in queued withdrawal state must be subject to slashing. Queuing a withdrawal must not shield assets from pending or future slashing events during the withdrawal delay.

**Property (Formal):**
$$\forall \text{slash}(s, t), \forall w \in \text{queued}(t): t_{\text{request}}(w) < t \land t < t_{\text{claim}}(w) \implies \text{affected}(w, s) = \text{true}$$

**Mode:** DUAL
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires slashing mechanism with withdrawal queue)

**Conditions:**
- Applies to restaking protocols with both slashing and withdrawal delay
- Critical for maintaining the economic security guarantee

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
- Protocol: Puffer | Report: `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md`

**Why This Matters:**
If queued withdrawals escape slashing, adversaries can front-run slashing events by queuing withdrawals, undermining the protocol's economic security.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-4-slashing-interaction-with-wi-003`

---

### STAKING-WITHDRAWAL-012: Cancelled Withdrawal Must Not Affect Future Operations

**Property (English):**
Cancelling a withdrawal request must fully restore the user's staking position to its pre-request state. Cancelled withdrawal timestamps, delay periods, and state must not carry over to affect future operations.

**Property (Formal):**
$$\forall \text{cancel}(w, t): \text{stakingState}(\text{user}, t + 1) = \text{stakingState}(\text{user}, t_{\text{pre-request}}(w))$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires cancellable withdrawal requests)

**Conditions:**
- Applies to protocols that allow withdrawal cancellation (re-delegation after cancellation)
- Common in EigenLayer-based protocols

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/m-06-the-time-available-for-a-canceled-withdrawal-should-not-impact-future-unsta.md`

**Why This Matters:**
Residual state from cancelled withdrawals creates unexpected cooldowns or restrictions on future operations.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-1-withdrawal-queue-manipulatio-000`

---

### STAKING-WITHDRAWAL-013: Withdrawal Yield Continuity

**Property (English):**
Users waiting for withdrawal processing should either continue earning yield on their queued assets or be compensated for the yield-free waiting period. The protocol's design choice must be clearly documented and correctly implemented.

**Property (Formal):**
$$\forall w \in \text{queued}: \text{yieldAccrued}(w, t_{\text{request}}, t_{\text{claim}}) \geq 0 \quad \text{(if yield-bearing design)}$$
$$\lor \quad \text{compensationMechanism}(w) \neq \emptyset \quad \text{(if non-yield-bearing design)}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires yield-generating staking)

**Conditions:**
- Applies to protocols where staked assets generate yield continuously
- Design choice: either yield during queue or explicit acknowledge of no-yield

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/m-11-eth-withdrawers-do-not-earn-yield-while-waiting-for-a-withdrawal.md`

**Why This Matters:**
Users expecting yield during the withdrawal period may be unknowingly losing rewards, creating hidden costs that discourage legitimate withdrawals.

---

### STAKING-WITHDRAWAL-014: Shared Cooldown Isolation

**Property (English):**
Cooldown timers must be per-action or per-request, not shared globally. One user's withdrawal request must not block or extend the cooldown for another user's operations.

**Property (Formal):**
$$\forall u_1 \neq u_2: \text{cooldown}(u_1) \centernot\implies \text{blocked}(u_2)$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires cooldown mechanism)

**Conditions:**
- Applies to protocols with shared cooldown state (e.g., shared redeem cooldown timers)
- Per-user or per-request cooldown isolation is required

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/h-01-the-redeem-related-functions-are-likely-to-be-blocked.md`

**Why This Matters:**
Shared cooldowns create DoS vectors where one user's action blocks all other users from withdrawing.

**Known Violations (from DB):**
- `general-defi-restaking-withdrawal-vulnerabilities-6-missing-slippage-deadline-pr-005`
