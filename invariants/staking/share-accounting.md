# Staking: Share Accounting Invariants

> Canonical invariants for share/TVL accounting correctness in staking and liquid
> restaking protocols. Mined from production protocols (EigenLayer, Kelp, Renzo,
> RestakeFi, Napier, Puffer, Cabal), EIP-4626 spec, Crytic/Properties, and the
> Vulnerability Database. Language-agnostic and protocol-agnostic.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: share-accounting
- **Sources**: EigenLayer, Kelp DAO, Renzo, RestakeFi, Napier, Puffer, Cabal, Tagus V2, Elytra, EIP-4626, Crytic/Properties
- **Last updated**: 2026-03-13
- **Invariant count**: 11

---

## Invariants

### STAKING-SHARE-001: Total Supply Equals Sum of All Balances

**Property (English):**
The total supply of staking derivative shares must exactly equal the sum of all individual holder balances at every reachable state.

**Property (Formal):**
$$\forall t: \text{totalSupply}(t) = \sum_{u \in \text{holders}} \text{balanceOf}(u, t)$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any ERC20-based staking derivative token
- Must hold across all state transitions: mint, burn, transfer

**Source Evidence:**
- EIP-20 specification — mandatory property
- Tool: Crytic/Properties | ERC20 property tests
- Protocol: Cabal | Report: `reports/eigenlayer_findings/m-07-desynchronization-of-cabals-internal-accounting-with-actual-staked-init-amou.md`

**Why This Matters:**
Supply-balance desynchronization means the exchange rate is calculated incorrectly, enabling theft.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-4-share-accounting-desynchroni-003`

---

### STAKING-SHARE-002: First Depositor Inflation Resistance

**Property (English):**
The first depositor must not be able to manipulate the share price to cause subsequent depositors to receive zero or near-zero shares. Minimum share requirements, virtual offsets, or dead shares must prevent inflation attacks.

**Property (Formal):**
$$\forall \text{deposit}(a) \text{ where } a \geq \text{MIN\_DEPOSIT}: \text{sharesMinted} > 0$$

Alternative: $\text{totalShares} \geq \text{VIRTUAL\_OFFSET}$ always

**Mode:** NEGATIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any share-based vault or staking system
- Especially critical when totalSupply can be 0 or 1

**Source Evidence:**
- Protocol: Kelp DAO | Report: `reports/eigenlayer_findings/h-03-the-price-of-rseth-could-be-manipulated-by-the-first-staker.md`
- Protocol: Napier | Report: `reports/eigenlayer_findings/h-4-victims-fund-can-be-stolen-due-to-rounding-error-and-exchange-rate-manipulati.md`
- Protocol: RestakeFi | Report: `reports/eigenlayer_findings/attacker-can-downscale-all-protocol-shares-by-18-decimals.md`
- Protocol: Tagus V2 | Report: `reports/eigenlayer_findings/vaults-are-vulnerable-to-a-donation-attack.md`
- Tool: Crytic/Properties | ERC4626 SecurityProps — `verify_sharePriceInflationAttack`
- EIP-4626 | OpenZeppelin implementation — virtual shares offset

**Why This Matters:**
First-depositor inflation is the single most common vault exploit pattern (5+ independent findings across 5 protocols). Attacker steals 100% of subsequent deposits.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-1-first-depositor-donation-att-000`
- `DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md`

---

### STAKING-SHARE-003: Shares Must Be Burned on Redemption

**Property (English):**
When a user redeems or withdraws assets, the corresponding shares must be burned atomically in the same transaction. No path may transfer assets without burning shares, or burn shares without transferring assets.

**Property (Formal):**
$$\forall \text{redeem}(u, s): \text{totalSupply}' = \text{totalSupply} - s \land \text{balanceOf}(u)' = \text{balanceOf}(u) - s$$

$$\forall \text{withdraw}(u, a): \exists s : \text{burned}(u, s) \land a \leq s \times \text{rate}$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any share-based staking system
- Must be atomic — no intermediate state where assets are transferred but shares unburned

**Source Evidence:**
- Protocol: RestakeFi | Report: `reports/eigenlayer_findings/shares-not-burned-after-redemption-of-underlying-assets.md`

**Why This Matters:**
Unburned shares after redemption allow the redeemer to withdraw again, creating infinite withdrawal attacks.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-4-share-accounting-desynchroni-003`

---

### STAKING-SHARE-004: TVL Calculation Consistency

**Property (English):**
The total value locked (TVL) calculation must include all asset locations consistently: deposited in protocol, deposited in strategies, in queued withdrawals, in transit, and pending rewards. Every component must be counted exactly once.

**Property (Formal):**
$$\text{TVL}(t) = \sum_{s \in \text{strategies}} \text{assets}(s, t) + \text{queuedAssets}(t) + \text{bufferAssets}(t) + \text{pendingRewards}(t)$$

$$\forall a \in \text{assets}: |\{c \in \text{components} : a \in c\}| = 1$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any multi-strategy staking protocol
- Strategy additions/removals must atomically update TVL tracking
- Loop indices in multi-strategy iteration must be correct

**Source Evidence:**
- Protocol: Renzo | Report: `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md`
- Protocol: Renzo | Report: `reports/eigenlayer_findings/h-08-incorrect-withdraw-queue-balance-in-tvl-calculation.md`
- Protocol: Elytra | Report: `reports/eigenlayer_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`

**Why This Matters:**
Incorrect TVL directly corrupts the exchange rate, enabling depositors or withdrawers to extract value at the expense of existing holders.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-2-tvl-calculation-errors-001`

---

### STAKING-SHARE-005: Strategy Cap Changes Must Synchronize State

**Property (English):**
When a strategy's deposit cap is changed (especially set to zero), all related accounting must be updated atomically: total shares held, withdrawal queue state, and TVL calculations.

**Property (Formal):**
$$\forall \text{setStrategyCap}(s, 0): \text{totalShares}' = \text{totalShares} - \text{shares}(s) \land \text{queuedWithdrawals}' \mathrel{+=} \text{shares}(s)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires strategy-based asset allocation)

**Conditions:**
- Applies to multi-strategy protocols (Rio Network, Renzo, etc.)
- Cap changes to 0 trigger EigenLayer withdrawal but must also update internal state

**Source Evidence:**
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/h-2-setting-the-strategy-cap-to-0-does-not-update-the-total-shares-held-or-the-w.md`

**Why This Matters:**
Users see stale (inflated) share counts, leading to incorrect exchange rates and failed withdrawals.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-4-share-accounting-desynchroni-003`

---

### STAKING-SHARE-006: Slashing-Induced Share Accounting Update

**Property (English):**
When a slashing event reduces the underlying assets, the share accounting must be updated to reflect the reduced TVL. The exchange rate must decrease proportionally to the slashing amount.

**Property (Formal):**
$$\forall \text{slash}(a, t): \text{totalAssets}(t+1) = \text{totalAssets}(t) - a \land \text{rate}(t+1) = \frac{\text{totalAssets}(t) - a}{\text{totalShares}(t)}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires slashing mechanism)

**Conditions:**
- Must synchronize across all accounting surfaces: internal balance, EigenLayer state, oracle reports
- Must handle concurrent slashing + withdrawal without double-accounting the loss

**Source Evidence:**
- Protocol: Puffer | Report: `reports/eigenlayer_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`

**Why This Matters:**
If slashing doesn't update share accounting, the protocol becomes insolvent — it promises more assets than it has.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-5-slashing-induced-accounting--004`

---

### STAKING-SHARE-007: Supply Inflation Prevention

**Property (English):**
The total supply of staking shares must only increase through authorized mint operations (deposits) and decrease through authorized burn operations (withdrawals). No unaccounted operation may inflate supply.

**Property (Formal):**
$$\Delta \text{totalSupply}(t, t+1) = \text{minted}(t, t+1) - \text{burned}(t, t+1)$$

$$\text{minted}(t, t+1) = \sum_{\text{deposits}} \text{sharesMinted} \quad \text{burned}(t, t+1) = \sum_{\text{withdrawals}} \text{sharesBurned}$$

**Mode:** DUAL
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Must account for: merge/split operations, migration functions, rescue functions
- Any function that mints shares must be access-controlled and properly accounted

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/the-lockers-supply-can-be-arbitrarily-inflated-by-an-attacker-due-to-unaccounted.md`

**Why This Matters:**
Supply inflation dilutes all holders' shares, reducing the exchange rate and enabling attacker profit.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-6-supply-inflation-via-unaccou-005`

---

### STAKING-SHARE-008: stakedButUnverifiedNativeETH Tracking

**Property (English):**
For beacon chain staking protocols, the `stakedButUnverifiedNativeETH` (or equivalent) tracker must be incremented on ETH deposit and decremented on both successful verification and failed verification. The tracker must not only increase.

**Property (Formal):**
$$\forall \text{deposit}(d): \text{unverified}' = \text{unverified} + d$$
$$\forall \text{verify}(v): \text{unverified}' = \text{unverified} - v$$

$$\text{unverified}(t) \geq 0 \quad \forall t$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires beacon chain integration)

**Conditions:**
- Applies to EigenPod-based or native ETH staking protocols
- Must be decremented on both successful verification and validator exit

**Source Evidence:**
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/incorrect-accounting-for-stakedbutunverifiednativeeth.md`
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/variable-stakedbutunverifiednativeeth-is-never-decremented.md`

**Why This Matters:**
A monotonically increasing tracker inflates TVL permanently, making the exchange rate higher than reality and eventual insolvency.

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-3-stakedbutunverifiednativeeth-002`

---

### STAKING-SHARE-009: Rounding Direction Consistency

**Property (English):**
All share/asset conversion functions must round in the direction that favors the protocol (existing holders). Deposits: round shares down. Withdrawals: round assets down. Mints: round assets up. Redeems: round shares up.

**Property (Formal):**
$$\text{deposit}(a): \text{shares} = \lfloor a \times \text{totalShares} / \text{totalAssets} \rfloor$$
$$\text{redeem}(s): \text{assets} = \lfloor s \times \text{totalAssets} / \text{totalShares} \rfloor$$
$$\text{mint}(s): \text{assets} = \lceil s \times \text{totalAssets} / \text{totalShares} \rceil$$
$$\text{withdraw}(a): \text{shares} = \lceil a \times \text{totalShares} / \text{totalAssets} \rceil$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any share-based vault following EIP-4626 conventions
- Must be consistent across preview functions and actual operations

**Source Evidence:**
- EIP-4626 specification — rounding direction requirements
- Tool: Crytic/Properties | ERC4626 RoundingProps — all rounding direction verifications
- Protocol: EigenLayer | Report: `reports/eigenlayer_findings/m-1-depositing-to-eigenlayer-can-revert-due-to-round-downs-in-converting-shares-a.md`

**Why This Matters:**
Incorrect rounding allows free share minting or free asset extraction through repeated small operations.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-7-rounding-and-precision-failu-006`

---

### STAKING-SHARE-010: Reentrancy Safety in Share Accounting

**Property (English):**
Share accounting state (totalSupply, balances, TVL trackers) must be updated before any external calls. Reentrancy during share operations must not corrupt accounting state.

**Property (Formal):**
$$\forall f \in \{\text{mint}, \text{burn}, \text{deposit}, \text{withdraw}\}: \text{stateUpdate}(f) \prec \text{externalCall}(f)$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Especially critical for native ETH operations (send/call enables reentrancy)
- Must cover: redeemNative, claimWithdrawal, any function with ETH transfer + state update

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/h-redeemnative-reentrancy-enables-permanent-fund-freeze.md`
- Protocol: EigenLayer/Karak | Report: `reports/eigenlayer_findings/vlts3-13-direct-theft-of-surplus-balance-when-unstaking-sthype.md`

**Why This Matters:**
Reentrancy in share accounting enables double-withdrawal — attacker re-enters during ETH transfer while shares haven't been burned yet.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-4-share-accounting-desynchroni-003`

---

### STAKING-SHARE-011: NodeDelegator Balance Verification on Removal

**Property (English):**
Before removing a NodeDelegator (or equivalent strategy container) from the protocol, its native ETH balance and staking balance must be verified as zero. Removal with non-zero balance loses those assets permanently.

**Property (Formal):**
$$\forall \text{remove}(n): \text{nativeBalance}(n) = 0 \land \text{stakingBalance}(n) = 0$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires delegator/strategy container pattern)

**Conditions:**
- Applies to multi-operator protocols that can add/remove delegation targets
- Balance must be fully withdrawn before removal

**Source Evidence:**
- Protocol: Various | Report: `reports/eigenlayer_findings/lack-of-verification-for-the-native-eth-balance-and-staking-balance-in-the-eigen.md`

**Why This Matters:**
Removing a delegator with residual balance permanently locks those funds — they become unaccounted and unrecoverable.
