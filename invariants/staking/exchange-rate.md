# Staking: Exchange Rate Invariants

> Canonical invariants for LST/LRT exchange rate correctness and oracle integrity.
> Mined from production protocols (EigenLayer, Lido, Kelp, Renzo, Tokemak, Napier, Puffer),
> EIP-4626 spec, Certora CVL rules, Echidna/Medusa property suites, and the Vulnerability Database.
> Language-agnostic and protocol-agnostic.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: exchange-rate
- **Sources**: EigenLayer, Lido, Kelp DAO, Renzo, Tokemak, Puffer, Napier, Vector Reserve, RestakeFi, EIP-4626, Crytic/Properties ERC4626
- **Last updated**: 2026-03-13
- **Invariant count**: 12

---

## Invariants

### STAKING-EXCHANGE-RATE-001: Exchange Rate Monotonicity (Non-Decreasing Under Normal Operations)

**Property (English):**
The exchange rate of staking derivative tokens (shares-to-assets) must be non-decreasing across any state transition that does not involve a slashing event or protocol-approved loss. Deposits, withdrawals, and reward accruals must never decrease the exchange rate.

**Property (Formal):**
$$\forall t, t+1: \neg \text{slashingEvent}(t, t+1) \implies \frac{\text{totalAssets}(t+1)}{\text{totalShares}(t+1)} \geq \frac{\text{totalAssets}(t)}{\text{totalShares}(t)}$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any staking derivative (stETH, rETH, rsETH, ezETH, pufETH, etc.)
- Slashing events are the only permitted cause of rate decrease
- Must hold across arbitrary deposit/withdrawal sequences

**Source Evidence:**
- Protocol: Lido | stETH rebase mechanism — rate only increases from consensus rewards
- Protocol: Renzo | File: ezETH exchange rate design
- Protocol: EigenLayer/Kelp | Report: `reports/eigenlayer_findings/h-3-malicious-operators-can-undelegate-themselves-to-manipulate-the-lrt-exchange-.md`
- Tool: Crytic/Properties | ERC4626 SecurityProps — share price inflation attack verification

**Why This Matters:**
If the exchange rate decreases without slashing, depositors lose value. Attackers can manipulate the rate downward to acquire shares cheaply, then restore it to extract other depositors' funds.

**Known Violations (from DB):**
- `general-defi-restaking-operator-delegation-vulnerabil-3-undelegation-breaking-lrt-ex-002` — Operator undelegation artificially drops exchange rate
- `general-defi-lrt-exchange-rate-oracle-vulnerabilities-4-exchange-rate-calculation-er-003` — Calculation errors cause rate drops

---

### STAKING-EXCHANGE-RATE-002: Exchange Rate Bounded Within Sane Range

**Property (English):**
The exchange rate between staking shares and underlying assets must remain within protocol-defined bounds. For LSTs pegged close to the underlying (e.g., stETH:ETH), the rate must not deviate beyond a maximum threshold (e.g., ±30% from 1:1).

**Property (Formal):**
$$\forall t: \text{MIN\_RATE} \leq \frac{\text{totalAssets}(t)}{\text{totalShares}(t)} \leq \text{MAX\_RATE}$$

**Mode:** DUAL
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- MIN_RATE and MAX_RATE are protocol-specific but must exist
- For LSTs: typically 0.9–1.3× the underlying
- Must hold even when queried by external integrations (lending, AMMs)

**Source Evidence:**
- Protocol: Kelp DAO | Report: `reports/eigenlayer_findings/no-checks-on-lst-price-oracles.md` — no bounds on rate queries
- Protocol: Tokemak | Report: `reports/eigenlayer_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md`
- Tool: Certora | General rate-of-change verification patterns

**Why This Matters:**
Without bounds, a compromised oracle or upgradeable proxy admin can set the rate to an extreme value, draining all funds in a single transaction.

**Known Violations (from DB):**
- `general-defi-lrt-exchange-rate-oracle-vulnerabilities-1-lst-oracle-manipulation-via--000` — LST proxy admin manipulates rate without any bounds check

---

### STAKING-EXCHANGE-RATE-003: Rate-of-Change Circuit Breaker

**Property (English):**
The exchange rate must not change by more than a maximum delta per time period. Any rate change exceeding the threshold must trigger a circuit breaker (pause or fallback).

**Property (Formal):**
$$\forall t, t+1: \left| \frac{\text{rate}(t+1) - \text{rate}(t)}{\text{rate}(t)} \right| \leq \text{MAX\_RATE\_CHANGE\_PER\_PERIOD}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires oracle-based rate updates)

**Conditions:**
- Applies to protocols that query external rate providers
- MAX_RATE_CHANGE_PER_PERIOD is protocol-defined (e.g., 5% per day)
- Does not apply to internal vault accounting with atomic deposit/withdraw

**Source Evidence:**
- Protocol: Kelp DAO | Report: `reports/eigenlayer_findings/no-checks-on-lst-price-oracles.md`
- Protocol: Tokemak | Report: `reports/eigenlayer_findings/m-5-malicious-or-compromised-admin-of-certain-lsts-could-manipulate-the-price.md`

**Why This Matters:**
Sudden rate jumps (from oracle manipulation or proxy upgrade) enable instant arbitrage draining the protocol.

**Known Violations (from DB):**
- `general-defi-lrt-exchange-rate-oracle-vulnerabilities-1-lst-oracle-manipulation-via--000`

---

### STAKING-EXCHANGE-RATE-004: Deposit Must Not Decrease Exchange Rate

**Property (English):**
A deposit operation must not decrease the exchange rate (share price) for existing holders. The newly minted shares must be priced at or below the current rate.

**Property (Formal):**
$$\forall \text{deposit}(a): \frac{\text{totalAssets}' }{\text{totalShares}'} \geq \frac{\text{totalAssets}}{\text{totalShares}}$$

where $\text{totalAssets}' = \text{totalAssets} + a$ and $\text{totalShares}' = \text{totalShares} + \text{mintedShares}$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any share-based staking system
- Rounding must favor existing holders (round shares down on deposit)

**Source Evidence:**
- Tool: Crytic/Properties | ERC4626 RoundingProps — `verify_depositRoundingDirection`
- Protocol: EigenLayer/Kelp | Report: `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md`
- EIP-4626 specification — rounding direction requirements

**Why This Matters:**
If deposits decrease the rate, existing depositors are diluted. This is the basis of first-depositor/donation attacks.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-1-first-depositor-donation-att-000`

---

### STAKING-EXCHANGE-RATE-005: Withdrawal Must Not Increase Exchange Rate for Withdrawer

**Property (English):**
A withdrawal operation must not grant the withdrawer more assets per share than the current exchange rate. Rounding must favor the protocol (round assets down on withdrawal/redeem).

**Property (Formal):**
$$\forall \text{redeem}(s): \text{assetsReceived} \leq s \times \frac{\text{totalAssets}}{\text{totalShares}}$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any share-based staking system
- Rounding must favor the vault/protocol (round down on redeem, round up on withdraw)

**Source Evidence:**
- Tool: Crytic/Properties | ERC4626 RoundingProps — `verify_redeemRoundingDirection`, `verify_withdrawRoundingDirection`
- EIP-4626 specification — rounding direction requirements

**Why This Matters:**
If withdrawals overpay, attackers extract value from remaining depositors through repeated deposit-withdraw cycles.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-7-rounding-and-precision-failu-006`

---

### STAKING-EXCHANGE-RATE-006: Exchange Rate Immune to Direct Token Transfers (Donation Resistance)

**Property (English):**
The exchange rate calculation must not be influenced by direct token transfers (donations) to the contract address. The rate must be derived from tracked internal accounting, not raw `balanceOf` queries.

**Property (Formal):**
$$\text{rate}(\text{state}) = f(\text{internalAccounting}) \neq g(\text{balanceOf}(\text{contract}))$$

**Mode:** NEGATIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol where `totalAssets` or TVL affects share pricing
- Internal accounting must track deposits/withdrawals explicitly
- External balance must not directly determine share price

**Source Evidence:**
- Protocol: Kelp DAO | Report: `reports/eigenlayer_findings/h-03-the-price-of-rseth-could-be-manipulated-by-the-first-staker.md`
- Protocol: Napier | Report: `reports/eigenlayer_findings/h-4-victims-fund-can-be-stolen-due-to-rounding-error-and-exchange-rate-manipulati.md`
- Protocol: RestakeFi | Report: `reports/eigenlayer_findings/attacker-can-downscale-all-protocol-shares-by-18-decimals.md`
- Tool: Crytic/Properties | ERC4626 SecurityProps — `verify_sharePriceInflationAttack`

**Why This Matters:**
Donation attacks (first-depositor + donation) are the most common vault exploit pattern. If `balanceOf` determines rate, a 1-wei deposit + large donation steals all subsequent deposits.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-1-first-depositor-donation-att-000`
- `DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md` — vault inflation patterns

---

### STAKING-EXCHANGE-RATE-007: Transfer-Before-Calculation Prohibition (CEI for Rate)

**Property (English):**
Asset transfers must not occur before share calculations that depend on the current balance. The exchange rate snapshot must be taken before any state-modifying transfers within the same function.

**Property (Formal):**
$$\forall f \in \{\text{deposit}, \text{mint}, \text{withdraw}, \text{redeem}\}: \text{rateSnapshot}(f) \prec \text{transfer}(f)$$

where $\prec$ denotes "happens before"

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any function that both transfers assets and calculates shares
- Must follow Checks-Effects-Interactions pattern for rate integrity

**Source Evidence:**
- Protocol: Kelp DAO | Report: `reports/eigenlayer_findings/h-02-protocol-mints-less-rseth-on-deposit-than-intended.md` — transfer inflates balance before rate calculation
- DB: `general-defi-lrt-share-accounting-vulnerabilities-3-transfer-before-calculation--002`

**Why This Matters:**
Transferring assets before reading the balance inflates the rate, causing the depositor to receive fewer shares than intended. The surplus is captured by existing holders.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-3-transfer-before-calculation--002`

---

### STAKING-EXCHANGE-RATE-008: Exchange Rate Must Account for Queued Withdrawals

**Property (English):**
TVL and exchange rate calculations must correctly account for assets in queued (pending) withdrawal state. Assets that have been committed to withdrawal but not yet transferred must be included in or excluded from TVL consistently.

**Property (Formal):**
$$\text{effectiveTVL}(t) = \text{depositedAssets}(t) - \text{queuedWithdrawals}(t) + \text{pendingRewards}(t)$$

$$\text{rate}(t) = \frac{\text{effectiveTVL}(t)}{\text{totalShares}(t)}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires withdrawal queue mechanism)

**Conditions:**
- Applies to protocols with asynchronous multi-step withdrawals (EigenLayer, Lido, etc.)
- Queued withdrawal assets must be consistently counted or excluded across all rate queries

**Source Evidence:**
- Protocol: Renzo | Report: `reports/eigenlayer_findings/h-02-incorrect-calculation-of-queued-withdrawals-can-deflate-tvl-and-increase-eze.md`
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/h-08-incorrect-withdraw-queue-balance-in-tvl-calculation.md`

**Why This Matters:**
Incorrect queued withdrawal accounting inflates or deflates the rate, enabling arbitrage between the actual and reported rate.

**Known Violations (from DB):**
- `general-defi-lrt-share-accounting-vulnerabilities-2-tvl-calculation-errors-001`

---

### STAKING-EXCHANGE-RATE-009: Exchange Rate Sandwich Protection

**Property (English):**
Deposit and withdrawal operations must not be exploitable via atomic sandwich attacks. The exchange rate used for a deposit must not differ from the rate used for an immediate withdrawal within the same block.

**Property (Formal):**
$$\forall \text{block } b: \text{profitFromSandwich}(b) \leq \text{depositFee} + \text{withdrawFee}$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any protocol with permissionless deposit + instant or same-block withdrawal
- Fees, cooldown periods, or withdrawal delays serve as protection mechanisms

**Source Evidence:**
- Protocol: Renzo | Report: `reports/eigenlayer_findings/h-04-withdrawals-logic-allows-mev-exploits-of-tvl-changes-and-zero-slippage-zero-.md`
- Protocol: Rio Network | Report: `reports/eigenlayer_findings/m-06-sandwiching-claimdelayedwithdrawals-to-steal-eth-rewards.md`
- Protocol: Vector Reserve | Report: `reports/eigenlayer_findings/stealing-funds-when-rates-change.md`

**Why This Matters:**
Without fees or cooldowns, MEV bots sandwich every reward distribution, extracting value from long-term stakers.

**Known Violations (from DB):**
- `general-defi-lrt-exchange-rate-oracle-vulnerabilities-2-exchange-rate-sandwich-front-001`
- `general-defi-restaking-reward-distribution-vulnerabil-1-sandwich-front-running-rewar-000`

---

### STAKING-EXCHANGE-RATE-010: Rate Provider Staleness Check

**Property (English):**
When the exchange rate is sourced from an external oracle or rate provider, the rate must have a freshness check. Stale rates (older than a maximum age) must not be used for pricing.

**Property (Formal):**
$$\forall \text{rateQuery}(t): t - \text{lastUpdateTime}(\text{rateSource}) \leq \text{MAX\_STALENESS}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires external rate source)

**Conditions:**
- Applies when exchange rate comes from an oracle, off-chain report, or separate contract
- MAX_STALENESS depends on the rate update frequency

**Source Evidence:**
- Protocol: Kelp DAO | Report: `reports/eigenlayer_findings/m-12-incorrect-exchange-rate-provided-to-balancer-pools.md`
- DB: `general-defi-lrt-exchange-rate-oracle-vulnerabilities-3-stale-or-divergent-rate-prov-002`

**Why This Matters:**
Stale rates diverge from actual asset values, enabling arbitrage between the protocol's stale price and the true market price.

**Known Violations (from DB):**
- `general-defi-lrt-exchange-rate-oracle-vulnerabilities-3-stale-or-divergent-rate-prov-002`

---

### STAKING-EXCHANGE-RATE-011: Share Appreciation Must Not Block Withdrawal Settlement

**Property (English):**
When withdrawal requests are valued in shares at request time and settled in assets later, the settlement must not fail if shares have appreciated. The protocol must handle the case where more assets are needed than originally estimated.

**Property (Formal):**
$$\forall \text{withdrawal}(w): \text{canSettle}(w, t_{\text{settle}}) = \text{true} \quad \text{regardless of} \quad \text{rate}(t_{\text{settle}}) > \text{rate}(t_{\text{request}})$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires asynchronous withdrawal with EigenLayer or similar)

**Conditions:**
- Applies to 2-step withdrawal processes where request and settlement occur at different times
- Share-to-asset conversion rate may change between request and settlement

**Source Evidence:**
- Protocol: Renzo/Rio | Report: `reports/eigenlayer_findings/h-6-requested-withdrawal-can-be-impossible-to-settle-due-to-eigenlayer-shares-val.md`
- DB: `general-defi-lrt-exchange-rate-oracle-vulnerabilities-6-share-value-appreciation-blo-005`

**Why This Matters:**
If shares appreciate during the withdrawal delay, the settlement may require more assets than available, permanently locking user funds.

**Known Violations (from DB):**
- `general-defi-lrt-exchange-rate-oracle-vulnerabilities-6-share-value-appreciation-blo-005`

---

### STAKING-EXCHANGE-RATE-012: Withdrawal Pricing During Beacon Chain Exits

**Property (English):**
When validators exit the beacon chain, the exchange rate must account for the transition period where assets move from the consensus layer to the execution layer. Withdrawals during this transition must not be mispriced.

**Property (Formal):**
$$\forall t \in \text{validatorExit}: \text{totalAssets}(t) = \text{executionLayerAssets}(t) + \text{consensusLayerAssets}(t) - \text{exitingValidatorAssets}(t) \times \text{exitDiscount}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires beacon chain native staking integration)

**Conditions:**
- Applies to protocols with native ETH staking (Lido, Rocket Pool, EigenLayer pods)
- Must handle the multi-day delay between validator exit initiation and fund availability

**Source Evidence:**
- DB: `general-defi-lrt-exchange-rate-oracle-vulnerabilities-5-withdrawal-pricing-during-be-004`
- Protocol: Lido | stETH rebasing during validator exits

**Why This Matters:**
Mispricing during validator exits creates arbitrage windows: depositors enter at a discount, or withdrawers extract at a premium, diluting honest participants.

**Known Violations (from DB):**
- `general-defi-lrt-exchange-rate-oracle-vulnerabilities-5-withdrawal-pricing-during-be-004`
