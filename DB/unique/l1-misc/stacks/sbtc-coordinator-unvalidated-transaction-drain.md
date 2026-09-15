---
# Core Classification
protocol: sbtc
chain: stacks
category: access_control
vulnerability_type: trusted_coordinator_fee_and_tx_validation_bypass

# Pattern Identity
root_cause_family: missing_validation
pattern_key: missing_tx_fee_and_content_validation | coordinator_initiated_transactions | empty_or_duplicate_tx_construction | multi_sign_wallet_drain

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - sBTC signer coordinator (transaction_coordinator, bitcoin validation)
  - signer/src/bitcoin/validation.rs (to_input_rows, deposit validate)
  - transaction_signer (handle_stacks_transaction_sign_request, assert_valid_stacks_tx_sign_request)
  - signers' multi-sign wallet (BTC UTXO pool + STX balance)
path_keys:
  - depositless_btc_tx | coordinator sweep construction | deposit fee checks bypassed | btc drain to miners
  - unchecked_stx_fee | stacks contract call sign request | no fee bound | stx drain
  - replayed_contract_call | handle_stacks_transaction_sign_request | no duplicate check | fee bleed
  - unannounced_sweep_execution | coordinator deposit handling | signers unaware | funds locked without mint

# Attack Vector Details
attack_type: privilege_abuse
affected_component: coordinator_transaction_validation

# Technical Primitives
primitives:
  - rotating coordinator role (any signer takes turns)
  - deposit-backed BTC sweep transactions (tx_in = signers UTXO + deposits)
  - per-deposit fee validation (report.validate(chain_tip_height, tx, tx_fee, max_deposit_amount))
  - StacksTxSignRequest with coordinator-set fee
  - multi-sign wallet (threshold BTC wallet + STX account)
  - sweep signature reuse

# Grep / Hunt-Card Seeds
code_keywords:
  - to_input_rows
  - is_valid_tx
  - reports.deposits
  - handle_stacks_transaction_sign_request
  - assert_valid_stacks_tx_sign_request
  - tx_fee
  - sighash
  - deposit_sighashes

# Impact Classification
severity: critical
impact: direct_loss_of_funds
exploitability: 0.6
financial_impact: critical

# Context Tags
tags:
  - l1
  - rust
  - sbtc
  - bitcoin-bridge
  - coordinator
  - fee-validation
  - multi-sign-wallet
  - collusion

# Version Info
language: rust
version: "stacks-network/sbtc signer, immunefi_attackaton_0.9 (Stacks Attackathon I, Dec 2024 - Jan 2025)"
---

## References & Source Reports

> All paths verified to exist under `reports/stacks-l1_findings/`. Both criticals in the Stacks index belong to this cluster (well, #38458 is one of the 2 criticals); includes the corpus's only direct-drain critical plus three high-severity fund-loss siblings.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [SC1] | reports/stacks-l1_findings/38458-bc-critical-the-coordinator-can-submit-empty-btc-transactions-to-drain-btc-tokens-in-the-multi.md | CRITICAL | Immunefi (Stacks Attackathon I) | Report #38458, signer/src/bitcoin/validation.rs |
| [SC2] | reports/stacks-l1_findings/38392-bc-high-signer-can-steal-stx-tokens-in-multi-sign-wallet-by-setting-a-high-stacks-tx-fee.md | HIGH | Immunefi | Report #38392, transaction_signer.rs |
| [SC3] | reports/stacks-l1_findings/38398-bc-high-malicious-signers-can-initiate-repeated-contract-calls-to-cause-the-multi-sign-wallet.md | HIGH | Immunefi | Report #38398, duplicate contract calls |
| [SC4] | reports/stacks-l1_findings/37479-bc-high-a-single-signer-can-lock-users-funds-by-not-notifying-other-signers-of-the-executed-sw.md | HIGH | Immunefi | Report #37479, unannounced sweep execution |

## sBTC Coordinator Drains Multi-Sign Wallet via Unvalidated Transaction Construction

### Overview

In sBTC, the coordinator role rotates through the signer set and *constructs* the transactions that the multi-sign wallet will sign: BTC sweeps aggregating deposits, and Stacks contract calls. The signer-side validation was built around **deposits** — each deposit is checked so its fee share doesn't exceed the user's expectation — but the transaction envelope itself is trusted: nothing bounds the coordinator-chosen BTC tx fee when there are no deposits, nothing bounds the STX fee on contract calls, nothing rejects already-executed duplicate calls, and sweep signatures can be executed without the other signers ever learning the tx landed. A malicious signer who becomes coordinator can therefore hand the wallet's entire BTC/STX balance to collaborating miners as fees, or lock user deposits by sweeping without minting. The cluster contains the corpus's critical direct-loss-of-funds finding (#38458).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because signers validate deposit-level constraints (per-deposit fee vs user expectation) but never validate transaction-level constraints — absolute fee bounds, non-empty deposit sets, duplicate/replayed contract calls — on coordinator-constructed transactions paid by the shared multi-sign wallet."
- Pattern key: `missing_tx_fee_and_content_validation | coordinator_initiated_transactions | empty_or_duplicate_tx_construction | multi_sign_wallet_drain`
- Interaction scope: `multi_contract` (coordinator ↔ bitcoin validation ↔ transaction_signer ↔ multi-sign wallet ↔ BTC/STX miners)
- Primary affected component(s): `bitcoin/validation.rs to_input_rows, handle_stacks_transaction_sign_request, sweep execution notification`
- Contracts / modules involved: `transaction_coordinator, bitcoin validation, transaction_signer, signers' multi-sign wallet`
- Path keys: `depositless_btc_tx | coordinator sweep construction | deposit fee checks bypassed | btc drain to miners` · `unchecked_stx_fee | stacks contract call sign request | no fee bound | stx drain` · `replayed_contract_call | handle_stacks_transaction_sign_request | no duplicate check | fee bleed` · `unannounced_sweep_execution | coordinator deposit handling | signers unaware | funds locked without mint`
- High-signal code keywords: `to_input_rows, is_valid_tx, reports.deposits, handle_stacks_transaction_sign_request, assert_valid_stacks_tx_sign_request, tx_fee, sighash, deposit_sighashes`
- Typical sink / impact: `direct loss of the multi-sign wallet's BTC/STX (drained as miner fees); user deposits permanently locked without sBTC mint`
- Validation strength: `strong` (#38458, #38392, #38398, #37479 read with code excerpts from validation.rs / transaction_signer.rs)

#### Contract / Boundary Map

- Entry surface(s): coordinator's BTC transaction proposal (sighash sign requests), coordinator's `StacksTransactionSignRequest` (fee field set by coordinator), sweep-signature handling for deposit requests
- Contract hop(s): `coordinator constructs tx -> signer validation (to_input_rows / assert_valid_stacks_tx_sign_request) -> threshold signatures -> BTC network / Stacks chain -> miners collect fee`
- Trust boundary crossed: `coordinator role — a peer signer crosses from participant to transaction *author*; nothing re-checks the author's work at the wallet level`
- Shared state or sync assumption: `all signers must know which wallet transactions have been executed (sweep notification) so mints and sweeps stay 1:1`

#### Valid Bug Signals

- Signal 1: Fee checks iterate `self.reports.deposits` only — "a malicious signer can initiate a BTC transaction without deposits, then all checks on deposits will be bypassed (including transaction fees)" (#38458, verified in `to_input_rows`).
- Signal 2: `handle_stacks_transaction_sign_request` validation has no fee bound — "signers do not check the tx fee set by the coordinator" (#38392); a huge fee sends wallet STX to the miner, recoverable via miner collusion.
- Signal 3: No duplicate-execution check — "signers do not check if the call have already been made" (#38398); re-initiated contract calls bleed tx fees per round.
- Signal 4: Sweep-signature flow lets the coordinator execute sweeps "without other signers being aware of it" — deposits swept with no sBTC minted on Stacks, "causing those funds to be permanently locked" (#37479, impact: "Permanent freezing of funds (fix requires hardfork)").

#### False Positive Guards

- Not this bug when: signer validation enforces an absolute fee ceiling (checked against wallet balance and a mempool-informed bound) on every sign request, depositless or not.
- Not this bug when: sign-request validation rejects duplicates (txid/nonce/sighash already executed) and enforces coordinator disclosure of executed sweeps.
- Safe if: the coordinator cannot select outputs/fees freely (fully deterministic tx construction from an agreed template).
- Requires attacker control of: one signer seat AND the coordinator rotation slot (all paths), plus miner collaboration to realize the stolen value (fees are collected by miners, so theft = collusion with a miner/mev recipient).
- Not a consensus bug: nothing here violates BTC/StackS consensus rules — the transactions are valid; the loss is economic (fee misallocation), which is why only signer-side validation can stop it.

### Vulnerability Description

#### Root Cause

1. **Deposit-scoped validation** (#38458): `to_input_rows` runs `report.validate(...)` over `self.reports.deposits`; with an empty deposit set there is nothing to validate, so a depositless BTC tx's fee is unchecked and paid by the signers' UTXO. "The attacker can use this to make the multi-sign wallet lose all BTC, which will be rewarded to BTC miners."
2. **Unbounded STX fee** (#38392): `assert_valid_stacks_tx_sign_request` checks request shape/origin but not the fee; the coordinator sets the fee for the wallet's sBTC contract calls.
3. **No replay/duplicate guard** (#38398): already-executed contract calls can be re-proposed and re-signed; each execution costs the wallet's fee.
4. **Asymmetric sweep knowledge** (#37479): the coordinator can execute a signed sweep and skip notifying peers, so the deposit-to-mint reconciliation never runs.

#### Attack Scenario / Path Variants

**Path A: Depositless BTC tx drains wallet (critical)**
Path key: `depositless_btc_tx | coordinator sweep construction | deposit fee checks bypassed | btc drain to miners`
Entry surface: coordinator-proposed BTC transaction (no deposit inputs)
Contracts touched: `transaction_coordinator -> bitcoin/validation.rs -> threshold signing -> BTC network`
Boundary crossed: `coordinator trust (tx author) over the shared wallet UTXO`
1. Malicious signer's turn as coordinator arrives; it constructs a BTC tx whose inputs are only the signers' UTXO and whose outputs pay a near-zero amount with an enormous fee ("empty BTC transactions").
2. `to_input_rows` iterates `reports.deposits` — empty — so "all checks on deposits will be bypassed (including transaction fees)".
3. Signers sign; the tx broadcasts; the fee goes to BTC miners.
4. Repeated until the wallet is empty; the attacker "can cooperate with BTC miners to steal all BTC" (colluding miner rebates the fee).

**Path B: High STX fee on contract calls**
Path key: `unchecked_stx_fee | stacks contract call sign request | no fee bound | stx drain`
Entry surface: `StacksTransactionSignRequest` with coordinator-chosen fee
1. Coordinator initiates routine sBTC Stacks contract calls and sets "a very large tx fee".
2. `handle_stacks_transaction_sign_request` validates everything except the fee.
3. Wallet STX is paid out to Stacks miners; attacker colludes with a miner to recover it.

**Path C: Duplicate contract calls bleed fees**
Path key: `replayed_contract_call | handle_stacks_transaction_sign_request | no duplicate check | fee bleed`
1. Coordinator re-initiates a contract call that already executed.
2. No executed-tx check exists, so signers sign again.
3. Each duplicate burns the wallet's tx fee — a slower but stealthier drain than Path B.

**Path D: Unannounced sweep locks deposits**
Path key: `unannounced_sweep_execution | coordinator deposit handling | signers unaware | funds locked without mint`
1. Coordinator holds valid sweep signatures from a prior signing round.
2. It executes the sweep BTC-side but never notifies the other signers.
3. Deposits move into the wallet with **no sBTC minted** on Stacks — users' BTC is gone from their control with no corresponding token.
4. Reconciliation is impossible without the execution record; funds permanently locked (hardfork-class fix per impact tags).

#### Vulnerable Pattern Examples

> Rust pseudocode reconstructed from verified report excerpts (sbtc 0.9).

**Example 1: Fee validation scoped to deposits only** [Approx Vulnerability : CRITICAL]
```rust
// ❌ VULNERABLE: #38458 — signer/src/bitcoin/validation.rs::to_input_rows
let validation_results = self.reports.deposits.iter().map(|(_, report)| {
    report.validate(                        // per-deposit fee/amount checks ONLY
        self.chain_tip_height,
        &self.tx,
        self.tx_fee,                        // fee is checked per deposit...
        self.max_deposit_amount,
    )
});
// ...but if reports.deposits is EMPTY, no check ever sees self.tx_fee.
// A depositless tx with fee == entire wallet UTXO signs cleanly. ❌
```

**Example 2: STX sign request without a fee ceiling** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: #38392 — transaction_signer.rs::handle_stacks_transaction_sign_request
let validation_status = self
    .assert_valid_stacks_tx_sign_request(request, bitcoin_chain_tip, origin_public_key)
    .await;
// assert_valid... checks origin, txid shape, chain tip — but never:
//   require!(request.fee <= MAX_WALLET_FEE && request.fee <= estimated_mempool_fee * BOUND)
// Coordinator sets fee; wallet STX flows to Stacks miners. ❌
```

**Example 3: Already-executed call re-signed** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: #38398 — duplicate contract calls
async fn handle_stacks_transaction_sign_request(&mut self, request: &StacksTransactionSignRequest, ..) {
    // no lookup: was request.txid (or its sighash) already broadcast/executed?
    // no lookup: is this contract call semantically a no-op re-run?
    self.sign_and_share(request);           // ❌ wallet pays the fee again
}
```

### Impact Analysis

#### Technical Impact
- Multi-sign wallet BTC balance fully exfiltrable via miner fees (Path A — critical, direct loss of funds)
- Wallet STX drained or bled via fees (Paths B/C)
- Deposit/mint reconciliation broken → users' BTC locked with no sBTC issued (Path D; "fix requires hardfork" per report impact tags)

#### Business Impact
- The signer set custodying the sBTC bridge can be bankrupted by one of its own members during a coordinator turn; attacker economics require miner collusion (fee rebate), which is realistic in MEV/fee markets
- Path D destroys the bridge's core promise (1:1 BTC backing): swept-but-unminted deposits are unrecoverable user loss

#### Affected Scenarios
- Any coordinator rotation including a malicious or coerced signer
- Periods of high mempool fees (masks abnormal fee values)
- Deposit queues with pending sweep signatures (Path D precondition)

### Secure Implementation

**Fix 1: Transaction-level validation envelope — absolute fee bounds, non-empty inputs, duplicate rejection, execution disclosure**
```rust
// ✅ SECURE: validate the ENVELOPE, not just the deposits
fn assert_valid_wallet_tx(&self, tx: &BitcoinTx, fee_rate: FeeRate) -> Result<(), Error> {
    let fee = tx.fee()?;
    let size = tx.vsize();
    // 1. absolute + relative fee bounds regardless of deposit count
    let bound = (fee_rate * size * MAX_FEE_MULTIPLIER).max(MIN_ABS_FEE);
    ensure!(fee <= bound.min(self.wallet_balance * MAX_FEE_BPS / 10_000),
            Error::FeeExceedsBound);                        // ✅ closes #38458 depositless path
    // 2. a wallet-spending tx must carry at least one acknowledged deposit or sweep intent
    ensure!(!self.reports.deposits.is_empty() || self.authorized_no_deposit_sweep(tx.txid()),
            Error::MissingDepositInputs);                   // ✅ no empty-input wallet spends
    ensure!(tx.outputs_pay_only(self.allowed_recipient_set()), Error::BadOutputs);
    Ok(())
}
async fn assert_valid_stacks_tx_sign_request(&mut self, request: &StacksTxSignRequest, ..) {
    ensure!(request.fee <= self.max_stx_fee(request.tx_kind()), Error::FeeExceedsBound); // ✅ #38392
    ensure!(!self.tx_execution_db.contains(&request.txid()),  Error::DuplicateExecution); // ✅ #38398
}
// ✅ #37479: coordinator must broadcast+disclose atomically; peers verify mint/sweep parity
fn on_sweep_signed(&mut self, sweep: SweepId) {
    self.execution_ledger.record_pending(sweep);       // every signer learns pre-execution
    self.notify_peers(sweep);                          // disclosure is part of the protocol
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
to_input_rows
is_valid_tx
reports.deposits
handle_stacks_transaction_sign_request
assert_valid_stacks_tx_sign_request
tx_fee
deposit_sighashes
sighash
```

#### Code Patterns to Look For
```
- Fee validation that iterates a (possibly empty) deposit/request list instead of bounding the tx envelope
- Sign-request validators that check origin/shape but never the fee field
- Wallet-spending paths with no non-empty-input / allowed-recipient assertion
- No executed-txid registry consulted before signing
- Sweep/execution flows where only the coordinator learns a transaction landed
```

#### Audit Checklist
- [ ] Is there an absolute fee ceiling on every wallet transaction, independent of deposit count?
- [ ] Can the coordinator construct a wallet spend with zero deposits / unexpected recipients?
- [ ] Is every STX sign request's fee bounded (memfee-informed, per tx_kind)?
- [ ] Are duplicate executions rejected via a shared execution ledger?
- [ ] Do all signers learn of executed sweeps in a way that forces deposit↔mint reconciliation?

### Real-World Examples

#### Known Exploits
- None public at time of writing; findings from Stacks Attackathon I (Dec 2024 – Jan 2025), triaged by Immunefi.

#### Related CVEs/Reports
- Immunefi #38458 (CRITICAL), #38392, #38398, #37479 — Stacks Attackathon I, sbtc immunefi_attackaton_0.9
- Contrast family in same corpus: signer liveness sabotage (see related entry) — same coordinator trust, liveness sink instead of theft

### Prevention Guidelines

#### Development Best Practices
1. Validate the transaction envelope (fee, inputs non-emptiness, recipients) at the wallet level — never scope fee checks to per-item business objects (deposits).
2. Bound every coordinator-chosen parameter (fee, nonce, recipient set) that moves wallet funds; deterministic tx templates are stronger than post-hoc checks.
3. Make execution disclosure a protocol obligation: no signer may learn of an executed wallet tx unilaterally.

#### Testing Requirements
- Unit: depositless BTC tx proposal must be rejected; fee > bound rejected
- Integration: coordinator-fee attack (Path B) and duplicate-call attack (Path C) sign-round tests
- Property: after every sweep, minted sBTC == swept deposits across restarts (Path D invariant)

### Keywords for Search

`stacks`, `sbtc`, `coordinator`, `multi-sign wallet`, `transaction fee`, `fee validation`, `empty transaction`, `depositless sweep`, `btc drain`, `stx fee`, `contract call`, `duplicate execution`, `replayed contract call`, `sweep signature`, `unannounced sweep`, `miner collusion`, `direct loss of funds`, `bitcoin bridge`, `validation.rs`, `to_input_rows`, `rust`, `attackathon`, `immunefi`

### Related Vulnerabilities

- DB/unique/l1-misc/stacks/sbtc-signer-liveness-wsts-round-sabotage.md (companion cluster: same signer/coordinator trust model, liveness sink)
- DB/unique/l1-misc/stacks-signer-validation.md (Coinfabrik signer audit: vote replay / ack status confusion)
