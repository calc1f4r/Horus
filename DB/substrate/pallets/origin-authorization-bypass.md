---
# Core Classification
protocol: generic
chain: polkadot
category: access_control
vulnerability_type: privilege_escalation
root_cause_family: authorization_logic_flaw
pattern_key: broken-role-check | pallet extrinsic dispatch | privileged extrinsic call | unauthorized role impersonation

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - pallet_circuit
  - Authorization storage
path_keys:
  - broken-role-check | pallet extrinsic dispatch | privileged extrinsic call | unauthorized role impersonation | bid_sfx | Circuit->Authorization
  - broken-role-check | pallet extrinsic dispatch | privileged extrinsic call | unauthorized role impersonation | gateway escrow takeover | Circuit->Gateways

# Attack Vector Details
attack_type: access_control_bypass
affected_component: extrinsic_origin_validation

# Technical Primitives
primitives:
  - ensure_signed
  - role_registry
  - authorize_function
  - CircuitRole
  - dispatchable_extrinsic

# Grep / Hunt-Card Seeds
code_keywords:
  - authorize
  - CircuitRole
  - ensure_role
  - bid_sfx
  - ensure_signed
  - Authorization
  - take_escrow

severity: high
impact: unauthorized_access
language: rust
tags:
  - substrate
  - pallet
  - access_control
  - role_check
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [t3rn1] | reports/substrate-l1_findings/t3rn-srl-2401.md | HIGH | SRLabs | 6.1 CircuitRole impersonation (Open) |
| [t3rn2] | reports/substrate-l1_findings/t3rn-srl-2401.md | HIGH | SRLabs | 6.2 gateway escrow account takeover |
| [t3rn10] | reports/substrate-l1_findings/t3rn-srl-2401.md | MEDIUM | SRLabs | 6.10 lack of authorization enables spam |
| [nodle3] | reports/substrate-l1_findings/nodle-halborn.md | MEDIUM | Halborn | HAL-03 emergency shutdown missing in critical functions |
| [oz7] | reports/substrate-l1_findings/polkadot-runtime-templates-oz-2024-07.md | HIGH | SRLabs | 4.1 stringent filtering for proxy calls |
| [x8] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-05] No safe_withdrawal option in withdraw_protocol_liquidity function in omnipool can be abused by frontrunners to cause losses to the admin when r |
| [x9] | reports/substrate-l1_findings/zenlink-peckshield.md | MEDIUM | Peckshield | Trust Issue of Admin Keys |
| [x10] | reports/substrate-l1_findings/publications-audit-reports-peckshield-audit-report-zenlink-v1-0-pdf.md | MEDIUM | Peckshield | Trust Issue of Admin Keys |
| [x11] | reports/substrate-l1_findings/zeitgeist-audit-chaintroopers-audit-report-of-zeitgeist-pm-2022-pdf.md | HIGH | Chaintroopers | [authorized] Lack of support for common authorized user in multiple markets at "authorize_market_outcome" call |
| [x12] | reports/substrate-l1_findings/zeitgeist-audit-chaintroopers-audit-report-of-zeitgeist-pm-2022-pdf.md | HIGH | Chaintroopers | [prediction-markets] A permissionless market can be rejected in "reject_market" |
| [x13] | reports/substrate-l1_findings/audit-reports-snowbridge-2024-05-24-audit-report-snowbridge-v1-1-pdf.md | HIGH | auditor | Administrative Commands are not implemented on Polkadot side |
| [x20] | reports/substrate-l1_findings/manta-veridise-chain.md | MEDIUM | Veridise | Audit Report: Manta Network ©2023 Veridise Inc. 12 4 Vulnerability Report 4.1.2 V-MANC-VUL-002: Users can use any previously seen Merkle root |
| [x21] | reports/substrate-l1_findings/publications-audit-reports-peckshield-audit-report-zenlinkdex-v1-0-pdf.md | MEDIUM | PeckShield | Status This issue has been fixed in the following commit:d656a11. 3.4 T rust Issue of Admin Keys • ID: PVE-004 • |
| [x22] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Storage can be bloated with low liquidity positions • Low Risk and Non-Critical Issues • 01 Admin is a single point of failure • 02 Consider adding be |

## Broken Extrinsic Role Authorization Allows CircuitRole Impersonation

**A coding error in the role-check helper lets any signed user pass privileged extrinsic authorization, enabling infrastructure-role impersonation and gateway escrow takeover** - representative of Substrate pallets where `authorize()`-style helpers are consulted but their result (or caller binding) is mishandled.

### Overview

t3rn's Circuit pallet gates executor/relayer/requester extrinsics behind a `CircuitRole` check, but an implementation error lets any user impersonate any role; combined with a second issue, an attacker can take over the gateway's escrow account itself.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the authorization helper's role lookup is buggy (wrong subject checked or result ignored), so role-gated extrinsics accept arbitrary signed origins."
- Pattern key: `broken-role-check | pallet extrinsic dispatch | privileged extrinsic call | unauthorized role impersonation`
- Interaction scope: `single_contract`
- Primary affected component(s): `extrinsic origin validation, role registries, escrow-governance extrinsics`
- Contracts / modules involved: `pallet_circuit, Authorization storage`
- Path keys: `broken-role-check | bid_sfx | Circuit->Authorization`, `broken-role-check | gateway escrow takeover | Circuit->Gateways`
- High-signal code keywords: `authorize, CircuitRole, bid_sfx, ensure_signed, Authorization`
- Typical sink / impact: `unauthorized privileged execution / escrow takeover / spam`
- Validation strength: `moderate` (single auditor; issue Open at publication)

#### Contract / Boundary Map

- Entry surface(s): `bid_sfx()`, escrow-management extrinsics, any `authorize()`-gated dispatchable
- Contract hop(s): `Circuit dispatchable -> Authorization storage (role lookup)`
- Trust boundary crossed: `origin trust boundary (signed user vs infrastructure role)`
- Shared state or sync assumption: `role registry must fully determine permission; no fallback to plain ensure_signed`

#### Valid Bug Signals

- Signal 1: A dispatchable calls an `authorize(origin, Role::X)`-style helper but the helper checks the wrong account, wrong role constant, or ignores its boolean result.
- Signal 2: Any signed account can successfully execute an extrinsic reserved for Relayer/Executor/Manager roles.
- Signal 3: Role-gated path leads to value movement (escrow, bids) or state reserved to operators.

#### False Positive Guards

- Not this bug when: role checks use `ensure_role!`-style macros that revert on failure and bind to the actual origin.
- Safe if: the pallet additionally requires a multisig/governance origin for the destructive path.
- Requires attacker control of: any funded account (no special role).

### Vulnerability Description

#### Root Cause

In `bid_sfx` (and siblings), the `authorize` function is invoked to verify the caller is an Executor, but the implementation error lets arbitrary signers satisfy the check — any user can impersonate infrastructure-critical roles and run permissioned transactions.

#### Attack Scenario / Path Variants

**Path A: Impersonate an Executor to bid on side-effects**
Path key: `broken-role-check | bid_sfx | Circuit->Authorization`
Entry surface: `bid_sfx()`
Contracts touched: `Circuit -> Authorization`
1. Attacker submits `bid_sfx` with their own account.
2. Buggy `authorize()` passes; attacker bids on/intercepts cross-chain side-effect execution.
3. Attacker influences execution ordering/fees reserved for operators.

**Path B: Escrow account takeover**
Path key: `broken-role-check | gateway escrow takeover | Circuit->Gateways`
1. Attacker reaches an escrow-governance extrinsic without holding the required role.
2. Attacker re-points or drains the gateway escrow account.
3. User funds bridged through gateways become attacker-controlled.

#### Vulnerable Pattern Examples

**Example 1: t3rn `bid_sfx` role check (from [t3rn1])** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: authorize() is called, but implementation error lets any user pass
pub fn bid_sfx(
    origin: OriginFor<T>,
    sfx_id: SideEffectId<T>,
    bid_amount: BalanceOf<T>,
) -> DispatchResultWithPostInfo {
    // Authorize: Retrieve sender of the transaction.
    // ... authorize(origin, CircuitRole::Executor) -- buggy lookup lets any signer through
    // -> any user can impersonate Executor role and bid on side effects
}
```

**Example 2: Result of authorization ignored** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: helper return value dropped, execution continues regardless
fn ensure_executor<T: Config>(origin: T::RuntimeOrigin) -> DispatchResult {
    let who = ensure_signed(origin)?;
    let _has_role = Authorization::<T>::get(&who, Role::Executor); // computed...
    Ok(()) // ...but never enforced: bool discarded, Ok(()) always returned
}
```

**Example 3: Wrong subject checked (role of someone else)** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: checks the target/sender stored in payload, not the extrinsic caller
pub fn manage_escrow(origin: OriginFor<T>, escrow_owner: T::AccountId) -> DispatchResult {
    let who = ensure_signed(origin)?;
    ensure!(
        Authorization::<T>::contains_key(&escrow_owner, Role::Manager), // checks the *described* owner
        Error::<T>::NotAuthorized
    );
    Self::take_escrow(&who, &escrow_owner); // caller 'who' was never verified
    Ok(())
}
```

### Impact Analysis

#### Technical Impact

- Complete bypass of role separation for affected extrinsics; attacker gains operator capabilities.
- Escrow account takeover = direct custody of bridged user funds.
- Enables spam attacks on rate-limited operator paths ([t3rn10]).

#### Business Impact

- Existential for an orchestrator network: unauthorized parties executing or bidding cross-chain work destroys trust and can drain escrow.

#### Affected Scenarios

- Pallets introducing custom `authorize` helpers instead of FRAME's `ensure_origin` with configured RuntimeOrigin.
- Escrow/gateway pallets where a single broken check yields fund custody.

### Secure Implementation

**Fix 1: Enforce the check at the call site**
```rust
// ✅ SECURE: authorization result must gate execution and bind to the actual caller
pub fn bid_sfx(origin: OriginFor<T>, sfx_id: SideEffectId<T>, bid: BalanceOf<T>) -> DispatchResult {
    let who = ensure_signed(origin)?;
    ensure!(Authorization::<T>::get(&who, Role::Executor), Error::<T>::NotExecutor);
    Self::do_bid(who, sfx_id, bid)
}
```

**Fix 2: Prefer FRAME origin primitives**
```rust
// ✅ SECURE: map roles to RuntimeOrigin call types and use ensure_origin
parameter_types! { pub ExecutorOrigin: RuntimeOrigin = ensure_executor_origin(); }
pub fn bid_sfx(origin: T::ExecutorOrigin, sfx_id: SideEffectId<T>, bid: BalanceOf<T>) -> DispatchResult {
    let who = origin.into_signer().ok_or(Error::<T>::BadOrigin)?;
    Self::do_bid(who, sfx_id, bid)   // dispatch-level guarantee, not helper convention
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- authorize(
- CircuitRole
- ensure_signed
- Authorization::get
- bid_sfx
```

#### Code Patterns to Look For
```
- Pattern 1: custom authorize helper whose bool result is discarded or whose subject is not the extrinsic origin
- Pattern 2: role lookup keyed by a payload-supplied account rather than ensure_signed output
- Pattern 3: privileged extrinsics that only call ensure_signed plus a soft logging path
```

#### Audit Checklist
- [ ] For every role-gated extrinsic: can a non-role signed account complete the call?
- [ ] Is the authorize helper's failure path a revert (not a log)?
- [ ] Are escrow-touching extrinsics double-gated (role + governance)?

### Keywords for Search

`CircuitRole`, `authorize`, `role impersonation`, `extrinsic origin check`, `ensure_signed`, `broken access control`, `escrow takeover`, `bid_sfx`, `executor role`, `relayer role`, `pallet authorization`, `runtime origin`, `privilege escalation substrate`, `t3rn circuit`

### Related Vulnerabilities

- DB/substrate/pallets/staking-unlock-relock-double-spend.md
- DB/substrate/pallets/emergency-shutdown-coverage.md
