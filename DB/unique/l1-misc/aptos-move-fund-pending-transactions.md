---
protocol: franklin-templeton-mmf
chain: aptos
category: fund_management
vulnerability_type: move_pending_transaction_logic

root_cause_family: missing_validation
pattern_key: unchecked_pending_request | self_service_transfer | disabled_self_service | unauthorized_transfer

interaction_scope: single_contract
involved_contracts:
  - funds/sources/fund_token.move
path_keys:
  - unchecked_pending_request | request_self_service_share_transfer | pending_transactions
  - zero_share_liquidation | request_full_liquidation | TX_TYPE_CASH_LIQUIDATION
  - cross_user_cancel | cancel_self_service_request | pending_transactions_removal
  - broken_batch_settlement | end_of_day | process_settlements

attack_type: logical_error
affected_component: fund_token pending-transaction lifecycle

primitives:
  - smart_table pending_transactions
  - request_ids vector
  - only_whitelisted admin
  - TX_TYPE constants
  - batch settlement (end_of_day)

code_keywords:
  - request_self_service_share_transfer
  - cancel_self_service_request
  - request_full_liquidation
  - TX_TYPE_CASH_LIQUIDATION
  - TX_TYPE_SHARE_TRANSFER
  - create_pending_transaction
  - end_of_day
  - process_settlements
  - only_when_account_not_frozen

severity: high
impact: dos
tags:
  - move
  - aptos
  - tokenization
  - fund_administration
language: move
version: "audit Aug-Oct 2024 (TOB-FT-APTOS-*)"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [FT] | reports/other-l1_findings/publications-reviews-2024-10-franklintempleton-aptos-securityreview-pdf.md | HIGH (2), MED+ (16 total) | Trail of Bits | Franklin Templeton Aptos MMF Security Assessment, Oct 2024 |

## Franklin Templeton Aptos MMF — Pending-Transaction Lifecycle Flaws in fund_token.move

### Overview

The on-chain fund share registry gates shareholder actions behind a pending-transaction queue settled by admins, but the request functions skip key state checks: `request_self_service_share_transfer` never checks that self-service is enabled, `request_full_liquidation` encodes type/amount wrongly so settled liquidations burn zero shares, and `cancel_self_service_request` lets any shareholder cancel anyone's requests (DoS).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because pending-request entry points validate account state but not protocol-mode state (self-service enabled/disabled) nor transaction-type/amount correctness, and the cancel path does not bind the request to its creator."
- Pattern key: `unchecked_pending_request | self_service_transfer | disabled_self_service | unauthorized_transfer`
- Interaction scope: `single_contract` (fund_token.move) with off-chain settlement dependency
- Primary affected component(s): `fund_token.move request/cancel/settlement functions`
- Contracts / modules involved: `fund_token.move (ManagedShareHolders, FundManagement resources)`
- Path keys: see `path_keys` above
- High-signal code keywords: `request_self_service_share_transfer`, `cancel_self_service_request`, `TX_TYPE_CASH_LIQUIDATION`, `end_of_day`
- Typical sink / impact: `unauthorized share transfers, unburned shares on liquidation (fund theft off-chain), request-griefing DoS, broken settlement ordering`
- Validation strength: `strong` (code line-level citations TOB-FT-APTOS-1/2/3/12)

#### Contract / Boundary Map

- Entry surface(s): `request_self_service_share_transfer()`, `request_full_liquidation()`, `cancel_self_service_request()`, admin `end_of_day()`
- Contract hop(s): `request_* -> create_pending_transaction -> admin settlement (process_settlements) / off-chain settlement systems`
- Trust boundary crossed: `on-chain pending queue <-> off-chain administrator settlement (TOB-FT-APTOS-2 severity depends on off-chain checks)`
- Shared state or sync assumption: `pending_transactions keyed by request_id; shareholder.request_ids vector; accounts_with_pending list must stay consistent`

#### Valid Bug Signals

- Signal 1: A `request_self_service_*` entry point lacks a `self_service_enabled` assert while sibling functions enforce it
- Signal 2: A full-liquidation request creates a pending tx with `TX_TYPE_CASH_LIQUIDATION` and amount `0`, and settlement only burns shares `if (tx.amount > 0)`
- Signal 3: `cancel_self_service_request(caller, request_id)` removes entries from `pending_transactions` without verifying the request belongs to `caller`

#### False Positive Guards

- Not this bug when: self-service toggle is checked in `create_pending_transaction` (not just entry points), settlement burns shares regardless of stored amount, and cancels verify ownership of the request id
- Safe if: off-chain settlement independently verifies share amounts before paying out (mitigates but does not fix TOB-FT-APTOS-2)
- Requires attacker control of: a shareholder account (Path A/C), or merely requesting a full liquidation (Path B)

### Vulnerability Description

#### Root Cause

1. TOB-FT-APTOS-1 (Medium): `request_self_service_share_transfer` checks accounts/frozen/shares but never `self_service_enabled`, so shareholder transfers bypass the allowlisted-admin requirement.
2. TOB-FT-APTOS-2 (Medium): `request_full_liquidation` calls `create_pending_transaction(account, @0x0, TX_TYPE_CASH_LIQUIDATION, 0, ...)` — amount 0 means settlement's `if (tx.amount > 0)` never burns shares; a shareholder could be paid cash off-chain while keeping shares.
3. TOB-FT-APTOS-3 (High): `cancel_self_service_request` removes any `request_id` from `pending_transactions` without checking the caller created it — a malicious shareholder cancels everyone's requests, DoSing the fund's operation.
4. TOB-FT-APTOS-12 (High): `end_of_day` passes a wrong date into `process_settlements` (uses a timestamp arg inconsistent with request creation times), so pending requests are not settled in the intended order/at all — "the end_of_day function is broken".

#### Attack Scenario / Path Variants

**Path A: Share transfer while self-service disabled** [MEDIUM]
Path key: `unchecked_pending_request | request_self_service_share_transfer | pending_transactions`
1. Admin disables self-service (transfers must go through allowlisted admins)
2. Shareholder calls `request_self_service_share_transfer` — no toggle check
3. Pending transfer created; admin settles it believing all self-service requests are legitimate
4. Unauthorized share transfer completes

**Path B: Full liquidation burns zero shares** [MEDIUM→HIGH]
Path key: `zero_share_liquidation | request_full_liquidation | TX_TYPE_CASH_LIQUIDATION`
1. Shareholder calls `request_full_liquidation` (amount stored = 0)
2. Settlement: `tx.amount > 0` false → `erc20_wrapper::burn` skipped
3. If off-chain payment executes without re-verification, shareholder keeps shares AND cash
4. Fund over-issues claims / direct loss

**Path C: Cross-user cancel DoS** [HIGH]
Path key: `cross_user_cancel | cancel_self_service_request | pending_transactions_removal`
1. Malicious shareholder watches mempool/pending queue
2. Calls `cancel_self_service_request(own_signer, victim_request_id)` — no ownership check
3. Victim's request removed from `pending_transactions`
4. Repeat for every request → fund operations (transfers, liquidations, purchases) frozen

**Path D: end_of_day settlement break** [HIGH]
Path key: `broken_batch_settlement | end_of_day | process_settlements`
1. Admin calls `end_of_day` with accounts batch
2. `process_settlements` receives a date argument inconsistent with pending-request timestamps
3. Requests settle out of order or not at all; dividends/settlement state diverges from intent

#### Vulnerable Pattern Examples

**Example 1: Missing mode check on self-service request** [Approx Vulnerability : MEDIUM]
```move
// ❌ VULNERABLE: TOB-FT-APTOS-1 — no self_service_enabled check
public entry fun request_self_service_share_transfer(
    caller: &signer, destination: address, shares: u64, memo: String,
) acquires ManagedShareHolders, FundManagement {
    only_when_initialized();
    only_when_account_exists(signer::address_of(caller));
    only_when_account_exists(destination);
    only_when_account_not_frozen(signer::address_of(caller));
    only_when_account_not_frozen(destination);
    only_when_shareholder_has_shares(signer::address_of(caller));
    only_higher_than_zero(shares);
    only_when_shareholder_has_enough_shares(signer::address_of(caller), shares);
    // ❌ missing: only_when_self_service_enabled();
    create_pending_transaction(signer::address_of(caller), destination, TX_TYPE_SHARE_TRANSFER, shares, false, memo);
}
```

**Example 2: Full liquidation stores amount 0** [Approx Vulnerability : HIGH]
```move
// ❌ VULNERABLE: TOB-FT-APTOS-2 — wrong tx_type semantics and zero amount
public entry fun request_full_liquidation(caller: &signer, account: address, memo: String) acquires ... {
    only_whitelisted(caller);
    // ...
    create_pending_transaction(account, @0x0, TX_TYPE_CASH_LIQUIDATION, 0 /* ❌ amount=0 */, false, memo);
}
// settlement later: if (tx.tx_type == TX_TYPE_CASH_LIQUIDATION) { if (tx.amount > 0) { burn(...) } }
// -> zero shares burned for a "full" liquidation
```

**Example 3: Cancel without request ownership** [Approx Vulnerability : HIGH]
```move
// ❌ VULNERABLE: TOB-FT-APTOS-3 — any shareholder can remove any pending request
public entry fun cancel_self_service_request(caller: &signer, request_id: u64, memo: String) acquires ManagedShareHolders {
    only_when_initialized();
    only_when_account_exists(signer::address_of(caller));
    let managed = borrow_global_mut<ManagedShareHolders>(@ft_funds);
    // ❌ no check that request_id was created by signer::address_of(caller)
    if (smart_table::contains(&managed.pending_transactions, request_id)) {
        smart_table::remove(&mut managed.pending_transactions, request_id);
    };
    // ...
}
```

### Impact Analysis

#### Technical Impact
- Pending-queue integrity broken (unauthorized creates, cross-user deletes)
- Share supply divergence from cash paid (Path B)
- Settlement ordering/execution failures at scale (Path D)

#### Business Impact
- Fund administration DoS (all shareholder operations)
- Potential double-claim: cash paid while shares retained
- Compliance breach: transfers executed while self-service disabled

#### Affected Scenarios
- Any Move (or other VM) tokenized-fund/registry using a pending-request + admin-settlement pattern
- Worse when off-chain settlement trusts on-chain amounts blindly

### Secure Implementation

**Fix 1: Centralize mode + ownership checks**
```move
// ✅ SECURE: enforce self-service toggle inside create_pending_transaction (or every
// request entry point), and bind request ownership on cancel
fun create_pending_transaction(sender: address, ...) acquires ... {
    only_when_self_service_enabled(); // or only_whitelisted for admin paths
    // ...
}
public entry fun cancel_self_service_request(caller: &signer, request_id: u64, ...) {
    let managed = borrow_global_mut<ManagedShareHolders>(@ft_funds);
    let tx = smart_table::borrow(&managed.pending_transactions, request_id);
    assert!(tx.sender == signer::address_of(caller), E_NOT_REQUEST_OWNER); // ✅
    // ...
}
```

**Fix 2: Correct liquidation encoding**
```text
// ✅ SECURE: introduce TX_TYPE_FULL_LIQUIDATION or store the shareholder's actual
// share balance as tx.amount so settlement burns the full position; have off-chain
// settlement re-verify on-chain share state before releasing cash
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- request_self_service_share_transfer
- cancel_self_service_request
- request_full_liquidation
- TX_TYPE_CASH_LIQUIDATION
- create_pending_transaction
- process_settlements
- end_of_day
- pending_transactions
```

#### Code Patterns to Look For
```
- "request_*" entry points whose validation set differs from sibling request functions
- Pending-transaction constructors taking literal 0 / @0x0 for value/destination
- Cancel/remove functions keyed by global id without sender-binding
- Settlement branching on tx.amount for types where amount is structurally zero
- Batch admin functions threading timestamps through more than one helper
```

#### Audit Checklist
- [ ] Enumerate every entry point that creates a pending transaction; diff their asserts
- [ ] For each TX_TYPE, trace amount semantics through settlement
- [ ] Can user A remove/modify user B's pending entry?
- [ ] Do batch settlement dates match request-creation semantics?

### Real-World Examples

#### Related Reports
- Trail of Bits, Franklin Templeton Aptos MMF (Oct 2024): TOB-FT-APTOS-1/2 Medium, TOB-FT-APTOS-3/12 High, plus 14 additional findings (ordering, frozen-holder dividends, multisig integrity gaps)

### Keywords for Search

`aptos`, `move`, `fund_token`, `pending transaction`, `self-service`, `share transfer`, `liquidation`, `smart_table`, `only_whitelisted`, `end_of_day`, `settlement`, `tokenized fund`, `franklin templeton`, `request cancellation`, `dos`, `burn shares`, `fa units`

### Related Vulnerabilities

- DB/unique/l1-misc/aptos-move-prover-notes.md (Move VM safety surface)
- DB/general/missing-validations/ entries (authorization-mode checks)
