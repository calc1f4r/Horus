---
# Core Classification
protocol: flare-fassets
chain: flare
category: bridge
vulnerability_type: attestation_criteria_bypass

# Pattern Identity
root_cause_family: flawed_boolean_validation
pattern_key: degenerate_source_address_proof | mintingPaymentDefault | agent_forges_checkSourceAddresses_proof | false_default -> user_payment_burned

# Interaction Scope
interaction_scope: cross_chain
involved_contracts:
  - CollateralReservations.sol (CollateralReservationsFacet)
  - Flare FDC (referenced-payment-nonexistence attestation)
  - AssetManager (minting flow)
path_keys:
  - degenerate_source_address_proof | mintingPaymentDefault | AssetManager -> FDC attestation -> reservation teardown
  - degenerate_source_address_proof | underlying_chain_payment_window | minter pays -> executor fails -> agent defaults

# Attack Vector Details
attack_type: logical_error
affected_component: attestation_verification_logic

# Technical Primitives
primitives:
  - referenced_payment_nonexistence_attestation
  - checkSourceAddresses
  - sourceAddressesRoot
  - paymentReference
  - boolean_disjunction_validation
  - collateral_reservation_teardown

# Grep / Hunt-Card Seeds
code_keywords:
  - mintingPaymentDefault
  - checkSourceAddresses
  - sourceAddressesRoot
  - standardPaymentReference
  - firstOverflowBlockNumber
  - PaymentReference.minting
  - minting non-payment mismatch

# Impact Classification
severity: high
impact: fund_loss
financial_impact: high

# Context Tags
tags:
  - bridge
  - attestation
  - cross_chain
  - agent_role
  - fdc
  - payment_default
  - boolean_logic

# Version Info
language: solidity
version: ">=0.8.0"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [45904] | reports/flare-l1_findings/45904-sc-high-malicious-agent-can-forge-a-non-payment-proof-despite-users-valid-payment-and-fraudule.md | HIGH | immunefi | https://reports.immunefi.com/flare-fassets-or-mainnet-audit-comp/45904-sc-high-malicious-agent-can-forge-a-non-payment-proof-despite-users-valid-payment-and-fraudule.md |

## Forged non-payment attestation lets agent force mintingPaymentDefault despite valid user payment

### Overview

Flare FAssets `mintingPaymentDefault` validates a "referenced payment non-existence" FDC attestation with a boolean-disjunction check that accepts a proof with `checkSourceAddresses = true` and `sourceAddressesRoot = bytes32(0)` for a non-handshake reservation. The agent can therefore obtain a proof that "no payment from address 0x00…0 exists" — trivially true — and use it to default a reservation whose user actually paid, burning the user's minted value and keeping the underlying payment plus reservation fee.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the source-address validation in `mintingPaymentDefault` uses `(!checkSourceAddresses && root==0) || (checkSourceAddresses && root==crt.root)` — the second branch degenerately matches when the reservation root is the zero bytes32, so a proof over the impossible source address 0x00…0 passes."
- Pattern key: `degenerate_source_address_proof | mintingPaymentDefault | agent_forges_checkSourceAddresses_proof | false_default -> user_payment_burned`
- Interaction scope: `cross_chain`
- Primary affected component(s): `CollateralReservations.mintingPaymentDefault attestation verification`
- Contracts / modules involved: `CollateralReservations.sol, CollateralReservationsFacet, Flare FDC verifier (referenced-payment-nonexistence)`
- Path keys: `degenerate_source_address_proof | mintingPaymentDefault | AssetManager -> FDC attestation -> reservation teardown`, `degenerate_source_address_proof | underlying_chain_payment_window | minter pays -> executor fails -> agent defaults`
- High-signal code keywords: `mintingPaymentDefault, checkSourceAddresses, sourceAddressesRoot, standardPaymentReference, firstOverflowBlockNumber`
- Typical sink / impact: `fund loss — user's underlying payment retained by agent + reservation fee; minting torn down`
- Validation strength: `strong` (working integration-test PoC in report [45904])

#### Contract / Boundary Map

- Entry surface(s): `CollateralReservationsFacet.mintingPaymentDefault(proof, crtId)` — agent-callable
- Contract hop(s): `underlying chain payment (user) -> FDC attestation request (agent-controlled criteria) -> mintingPaymentDefault verification -> reservation default/teardown`
- Trust boundary crossed: `cross-chain attestation (FDC proof) whose request criteria are chosen by the proof submitter`
- Shared state or sync assumption: `proof search criteria must exactly mirror the reservation's payment terms; source address restriction must only be bypassable when it genuinely doesn't apply`

#### Valid Bug Signals

- Signal 1: A boolean validation where one branch can be satisfied by a degenerate/zero value of the very field it is supposed to constrain
- Signal 2: The proof submitter (adversary) controls attestation request parameters such as `checkSourceAddresses` / `sourceAddressesRoot`
- Signal 3: Accepting the forged proof changes reservation state destructively (default, fee retention, collateral release) despite a valid on-chain payment existing

#### False Positive Guards

- Not this bug when: `crt.sourceAddressesRoot != bytes32(0)` (handshake reservations) — then branch two requires an exact root match, and a zero-root proof fails
- Safe if: the require additionally enforces `crt.sourceAddressesRoot != bytes32(0)` whenever `checkSourceAddresses == true`, or forbids `sourceAddressesRoot == bytes32(0)` in proofs entirely
- Requires attacker control of: the Agent role (agent must submit the forged proof and benefit from the default)

### Vulnerability Description

#### Root Cause

For non-handshake reservations, `crt.sourceAddressesRoot == bytes32(0)`. The guard:

```solidity
require(!_nonPayment.data.requestBody.checkSourceAddresses && crt.sourceAddressesRoot == bytes32(0) ||
        _nonPayment.data.requestBody.checkSourceAddresses &&
        crt.sourceAddressesRoot == _nonPayment.data.requestBody.sourceAddressesRoot, ...);
```

intends "either no source restriction applies, or the proof's root matches the reservation's root." But because the reservation root is zero for non-handshake mints, an agent requests an attestation with `checkSourceAddresses = true, sourceAddressesRoot = bytes32(0)`. The FDC verifier searches for a payment *from source address 0x00…0* — which can never exist — and confirms non-existence. The guard's second branch passes (`0 == 0`), and the remaining criteria (paymentReference, destination, amount, block window) all genuinely match the reservation, so a valid-looking non-payment proof exists despite the user's real payment.

#### Attack Scenario / Path Variants

**Path A: Forged default after valid payment + executor failure** [Approx Vulnerability : HIGH]
Path key: `degenerate_source_address_proof | mintingPaymentDefault | AssetManager -> FDC -> reservation teardown`
1. User reserves collateral (non-handshake; `crt.sourceAddressesRoot = bytes32(0)`), delegating execution to a bot as `crt.executor`.
2. User performs a valid underlying-chain payment (correct amount, memo paymentReference) but the executor bot fails to submit the proof (downtime/late payment near window end).
3. Payment window (e.g. 15 min / 225 blocks for fXRP) expires; a real non-payment proof would fail since a matching transaction exists.
4. Agent instead requests a proof with `checkSourceAddresses = true, sourceAddressesRoot = bytes32(0)`; FDC finds no payment *from the zero address* and confirms.
5. Agent calls `mintingPaymentDefault` with this proof: guard passes, reservation defaults, agent keeps the reservation fee, user's paid underlying funds stay with the agent, and no fAssets are minted to the user.

**Path B: Systematic fee farming by malicious agent** [Approx Vulnerability : MID]
Path key: `degenerate_source_address_proof | underlying_chain_payment_window | repeated defaults`
1. Agent waits for payments landing late in the window (network delays on underlying chain make this recurring).
2. Repeatedly forces defaults on paid-but-unproven reservations, harvesting reservation fees and underlying payments while users lose everything.

#### Vulnerable Pattern Examples

**Example 1: degenerate boolean guard in mintingPaymentDefault** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: when crt.sourceAddressesRoot == bytes32(0) (non-handshake),
// branch 2 passes with a proof whose sourceAddressesRoot is also zero —
// i.e. "no payment from address 0x00..0" is trivially provable
require(!_nonPayment.data.requestBody.checkSourceAddresses && crt.sourceAddressesRoot == bytes32(0) ||
        _nonPayment.data.requestBody.checkSourceAddresses &&
        crt.sourceAddressesRoot == _nonPayment.data.requestBody.sourceAddressesRoot,
        "invalid check or source addresses root");
```

**Example 2: criteria that legitimately match, making the forged proof indistinguishable** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE (context): these all match the real reservation, so the only
// flawed discriminator is the source-address guard above
require(_nonPayment.data.requestBody.standardPaymentReference == PaymentReference.minting(_crtId) &&
        _nonPayment.data.requestBody.destinationAddressHash == agent.underlyingAddressHash &&
        _nonPayment.data.requestBody.amount == underlyingValueUBA + crt.underlyingFeeUBA,
        "minting non-payment mismatch");
```

**Example 3: PoC proof request with zero source (from report [45904])** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE (exploit side): proof over impossible source address passes FDC
// const proof = await context.attestationProvider.proveReferencedPaymentNonexistence(
//     agent.underlyingAddress, crt.paymentReference, crt.valueUBA.add(crt.feeUBA),
//     crt.firstUnderlyingBlock, crt.lastUnderlyingBlock, crt.lastUnderlyingTimestamp,
//     "0x0000000000000000000000000000000000000000000000000000000000000000");
// await context.assetManager.mintingPaymentDefault(proof, crt.collateralReservationId, { from: agent.ownerWorkAddress });
```

### Impact Analysis

#### Technical Impact
- Reservation state torn down (default) despite a matching on-chain payment existing — cross-chain state desync
- User's underlying payment becomes unclaimable through the minting path; agent retains it
- Reservation fee (kept by agent on default) harvested per attack

#### Business Impact
- Direct loss of user funds (underlying payment + fee) — report classified under "direct theft"
- Erodes trust in executor delegation model; agents are financially incentivized to grief late-window payments

#### Affected Scenarios
- fXRP and any non-handshake minting on FAssets where the user delegates executeMinting to a bot
- Payments made near the end of the window; executor bot malfunction/downtime
- Compounds with executor gas-griefing (see related entry) which increases unproven-payment windows

### Secure Implementation

**Fix 1: forbid the degenerate zero-root proof branch**
```solidity
// ✅ SECURE (mitigation from report [45904]): reject proofs that claim a source
// restriction matching a zero root — a non-handshake reservation must only be
// defaulted by proofs WITHOUT source-address checking
require(!_nonPayment.data.requestBody.checkSourceAddresses && crt.sourceAddressesRoot == bytes32(0) ||
        _nonPayment.data.requestBody.checkSourceAddresses &&
        crt.sourceAddressesRoot == _nonPayment.data.requestBody.sourceAddressesRoot &&
        crt.sourceAddressesRoot != bytes32(0),
        "invalid check or source addresses root");
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Boolean disjunction (`||`) guards over attestation request fields where one operand can be a sentinel/zero value
- Proof-submitter-controlled request parameters validated by equality against stored state
- Default/penalty state transitions gated solely by attestation acceptance
```

#### High-Signal Grep Seeds
```
- mintingPaymentDefault
- checkSourceAddresses
- sourceAddressesRoot
- standardPaymentReference
- firstOverflowBlockNumber
- PaymentReference.minting
```

#### Code Patterns to Look For
```
- Pattern 1: `x == bytes32(0) || x == y` style guards (sentinel-equality confusion)
- Pattern 2: attestation request bodies compared field-by-field without binding optional-field presence to reservation type
- Pattern 3: default flows where the adversarial role both requests the proof and benefits from acceptance
```

#### Audit Checklist
- [ ] For every optional attestation field, check whether a degenerate value (zero/empty) can satisfy the guard
- [ ] Verify proof request criteria are fully determined by on-chain reservation state, not submitter choice
- [ ] Trace who profits from each default/penalty path and whether they can trigger it

### Real-World Examples

#### Known Exploits
- **Flare FAssets (audit finding, not exploited on mainnet)** - Immunefi Audit Comp May 2025 - Report #45904
  - Link: https://reports.immunefi.com/flare-fassets-or-mainnet-audit-comp/45904-sc-high-malicious-agent-can-forge-a-non-payment-proof-despite-users-valid-payment-and-fraudule.md
  - Root cause: `checkSourceAddresses`/`sourceAddressesRoot` guard degenerately satisfied by zero root

### Prevention Guidelines

#### Development Best Practices
1. Bind optional attestation fields to reservation type: optional field present ⟺ reservation stores a non-sentinel value
2. Never allow proof-submitter-chosen criteria to widen the acceptance set (request body should be reconstructible from on-chain state)
3. Property-test attestation guards with degenerate inputs (zero roots, empty arrays, max windows)

#### Testing Requirements
- Unit tests: zero-root proof against non-handshake reservation must revert
- Integration tests: valid payment + executor failure + malicious agent → default must be impossible
- Fuzzing: `checkSourceAddresses` × `sourceAddressesRoot` × reservation type truth table

### Keywords for Search

`flare`, `fassets`, `mintingpaymentdefault`, `checksourceaddresses`, `sourceaddressesroot`, `referencedpaymentnonexistence`, `fdc`, `attestation`, `nonpaymentproof`, `paymentdefault`, `zero_root`, `sentinel_value`, `boolean_logic_flaw`, `cross_chain_bridge`, `xrp`, `agent_fraud`, `reservation_fee`

### Related Vulnerabilities

- DB/unique/l1-misc/flare/fassets-execute-minting-executor-fee-hijack.md (same minting-flow race cluster; widens the unproven-payment window this bug feeds on)
- DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md (same malicious-agent trust cluster)
