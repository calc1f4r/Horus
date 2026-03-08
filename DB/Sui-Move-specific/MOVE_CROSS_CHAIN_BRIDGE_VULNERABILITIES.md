---
protocol: generic
chain: sui, aptos, movement
category: bridge_crosschain
vulnerability_type: payload_frontrunning, validator_set_integrity, signature_replay, message_validation_bypass, fund_loss_to_object
attack_type: fund_theft, messaging_spoofing, denial_of_service, replay
affected_component: cross_chain_messaging, bridge, validator_set, payload_processing, cross_chain_claim
primitives:
  - cross_chain_bridge
  - layerzero
  - wormhole
  - payload_validation
  - validator_set
  - signature_verification
  - cross_chain_messaging
severity: critical
impact: fund_loss, message_spoofing, denial_of_service
exploitability: 0.7
financial_impact: critical
tags:
  - move
  - sui
  - aptos
  - bridge
  - cross_chain
  - layerzero
  - wormhole
  - payload
  - validator
  - signature
  - replay
  - messaging
  - front_running
  - defi
language: move
version: all
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/lombard_finance_move_audit_final.md | Lombard SUI | OtterSec | HIGH |
| [R2] | reports/ottersec_move_audits/markdown/canopy_audit_final.md | Canopy | OtterSec | CRITICAL |
| [R3] | reports/ottersec_move_audits/markdown/mayan_sui_audit_final.md | Mayan Sui | OtterSec | HIGH |

## Move Cross-Chain and Bridge Vulnerabilities

**Comprehensive patterns for cross-chain messaging, bridge validation, payload front-running, validator set integrity, and signature replay vulnerabilities in Move-based bridge and cross-chain protocols across Sui and Aptos chains.**

### Overview

Cross-chain vulnerabilities appeared in 3/29 OtterSec Move audit reports (10%), but carry disproportionately high severity — 1 CRITICAL, 5 HIGH. Bridge protocols on Move chains face unique challenges: Sui's object-based addressing can cause fund loss when gas is sent to object IDs instead of user addresses, and Move's abort-on-error means payload front-running permanently blocks legitimate operations.

### Vulnerability Description

#### Root Cause Categories

1. **Payload front-running** — Public validation marks payloads as used before legitimate mint
2. **Validator set integrity** — Missing checks on validator keys, duplicates, and threshold
3. **Message validation bypass** — No verification on incoming cross-chain message content
4. **Unrestricted messaging** — Any user can send cross-chain messages via OApp
5. **Signature replay** — Valid signatures resubmittable within deadline window
6. **Fund loss to object ID** — Sui `transfer::public_transfer` to object ID instead of address

---

## Pattern 1: Payload Front-Running via Public Validation — move-bridge-001

**Frequency**: 1/29 reports (Lombard SUI [R1])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but HIGH severity with broad applicability

### Attack Scenario
1. Legitimate user submits a valid payload + proof for token minting
2. `validate_and_store_payload` is a public function that marks payloads as used
3. Attacker monitors mempool, front-runs with same payload + proof
4. Payload is marked as used by attacker's transaction
5. Legitimate user's minting transaction now fails (payload already consumed)
6. Tokens never minted — user loses bridged funds

### Vulnerable Pattern Example

**Lombard SUI — Public Payload Marking** [HIGH] [R1]
```move
// ❌ VULNERABLE: Anyone can call validate_and_store_payload
public fun validate_and_store_payload(
    consortium: &mut Consortium,
    payload: vector<u8>,
    proof: vector<u8>,
) {
    // Signature validation passes — proof is valid
    let hash = validate_consortium_signature(consortium, payload, proof);
    
    // ❌ Any caller marks payload as used
    // Front-runner calls this before legitimate mint
    assert!(!table::contains(&consortium.used_payloads, hash), E_ALREADY_USED);
    table::add(&mut consortium.used_payloads, hash, true);
    
    // ❌ No minting happens — just marks payload as consumed
    // Legitimate user's subsequent mint call finds payload already used
}

// Separate mint function checks payload was validated
public fun mint(treasury: &mut Treasury, consortium: &Consortium, payload_hash: vector<u8>) {
    // ❌ This can never be called for front-run payloads
    assert!(table::contains(&consortium.used_payloads, payload_hash), E_NOT_VALIDATED);
    // ...
}
```

### Secure Implementation
```move
// ✅ SECURE: Combine validation and minting into single atomic operation
public fun validate_and_mint(
    treasury: &mut Treasury,
    consortium: &mut Consortium,
    payload: vector<u8>,
    proof: vector<u8>,
    recipient: address,
    ctx: &mut TxContext,
) {
    let hash = validate_consortium_signature(consortium, payload, proof);
    assert!(!table::contains(&consortium.used_payloads, hash), E_ALREADY_USED);
    table::add(&mut consortium.used_payloads, hash, true);
    
    // ✅ Atomic: validation + minting in one transaction
    let (_, amount) = decode_mint_payload(payload);
    let minted = coin::mint(&mut treasury.cap, amount, ctx);
    transfer::public_transfer(minted, recipient);
}
```

---

## Pattern 2: Missing Validator Set Integrity Checks — move-bridge-002

**Frequency**: 1/29 reports (Lombard SUI [R1])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but critical for any bridge

### Vulnerable Pattern Example

**Lombard SUI — Incomplete Validator Configuration** [HIGH] [R1]
```move
// ❌ VULNERABLE: Multiple missing checks
public fun assert_and_configure_validator_set(
    consortium: &mut Consortium,
    validators: vector<ValidatorInfo>,
    threshold: u64,
) {
    // ❌ Missing check 1: No duplicate validator detection
    // Same validator counted twice → artificially meets threshold
    
    // ❌ Missing check 2: No key length validation
    // Expected 65 bytes (uncompressed secp256k1), but any length accepted
    // Short keys → signature verification is meaningless
    
    // ❌ Missing check 3: No threshold sanity check
    // threshold > total_weight → no valid signature set can meet threshold
    // threshold == 0 → all messages pass with no signatures
    
    consortium.validators = validators;
    consortium.threshold = threshold;
}
```

### Secure Implementation
```move
// ✅ SECURE: Complete validator set validation
public fun assert_and_configure_validator_set(
    consortium: &mut Consortium,
    validators: vector<ValidatorInfo>,
    threshold: u64,
) {
    let total_weight = 0u64;
    let seen = table::new<vector<u8>, bool>();
    let i = 0;
    
    while (i < vector::length(&validators)) {
        let v = vector::borrow(&validators, i);
        
        // ✅ Check 1: No duplicate validators
        assert!(!table::contains(&seen, &v.public_key), E_DUPLICATE_VALIDATOR);
        table::add(&mut seen, v.public_key, true);
        
        // ✅ Check 2: Valid key length (65 bytes for uncompressed secp256k1)
        assert!(vector::length(&v.public_key) == 65, E_INVALID_KEY_LENGTH);
        
        total_weight = total_weight + v.weight;
        i = i + 1;
    };
    
    // ✅ Check 3: Threshold sanity
    assert!(threshold > 0, E_ZERO_THRESHOLD);
    assert!(threshold <= total_weight, E_THRESHOLD_EXCEEDS_TOTAL);
    
    table::destroy_empty(seen);
    consortium.validators = validators;
    consortium.threshold = threshold;
}
```

---

## Pattern 3: Cross-Chain Message Validation Bypass — move-bridge-003

**Frequency**: 1/29 reports (Canopy [R2])
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but CRITICAL impact

### Attack Scenario
1. Protocol receives cross-chain messages via LayerZero/Wormhole integration
2. Incoming message content is not validated (no schema, no source verification)
3. Attacker sends malformed or empty messages from a configured peer chain
4. Messages are processed — causing fund misallocation or asset theft
5. Fake `timelocked_asset_dump` messages via matching resource_account_addr

### Vulnerable Pattern Example

**Canopy — No Incoming Message Validation** [CRITICAL] [R2]
```move
// ❌ VULNERABLE: No validation on incoming cross-chain message
public fun lz_receive(
    oapp: &mut OApp,
    src_eid: u32,
    sender: vector<u8>,
    message: vector<u8>,
    _extra_data: vector<u8>,
) {
    // ❌ No message schema validation
    // ❌ No minimum length check
    // ❌ No source address verification beyond peer config
    
    let decoded = decode_message(message);
    // ❌ If message is malformed, decode produces garbage values
    // Garbage values processed as legitimate operations
    
    match decoded.action {
        ACTION_DEPOSIT => process_deposit(oapp, decoded),
        ACTION_WITHDRAW => process_withdraw(oapp, decoded),
        // ❌ Attacker's crafted message triggers unauthorized withdraw
        _ => abort E_UNKNOWN_ACTION,
    };
}
```

**Canopy — Ambiguous Asset Processing** [CRITICAL] [R2]
```move
// ❌ VULNERABLE: Uses balance instead of message source for asset routing
public fun process_incoming_asset(
    pool: &mut Pool,
    asset: FungibleAsset,
    message: CrossChainMessage,
) {
    // ❌ Asset routing based on current balance, not message metadata
    // Interfering concurrent messages cause incorrect routing
    let balance = fungible_asset::balance(&pool.store);
    route_asset(pool, asset, balance);  // ❌ Wrong routing source
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate incoming message schema and source
public fun lz_receive(
    oapp: &mut OApp,
    src_eid: u32,
    sender: vector<u8>,
    message: vector<u8>,
    _extra_data: vector<u8>,
) {
    // ✅ Minimum message length
    assert!(vector::length(&message) >= MIN_MESSAGE_LENGTH, E_INVALID_MESSAGE);
    
    // ✅ Validate sender is expected peer for this chain
    let expected_peer = get_peer(oapp, src_eid);
    assert!(sender == expected_peer, E_UNAUTHORIZED_SENDER);
    
    // ✅ Structured decoding with validation
    let decoded = decode_and_validate_message(message);
    assert!(decoded.version == CURRENT_VERSION, E_VERSION_MISMATCH);
    
    match decoded.action {
        ACTION_DEPOSIT => process_deposit(oapp, decoded),
        ACTION_WITHDRAW => process_withdraw(oapp, decoded),
        _ => abort E_UNKNOWN_ACTION,
    };
}
```

---

## Pattern 4: Unrestricted Cross-Chain Message Sending — move-bridge-004

**Frequency**: 1/29 reports (Canopy [R2])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol

### Vulnerable Pattern Example

**Canopy — No Authorization on Outgoing Messages** [HIGH] [R2]
```move
// ❌ VULNERABLE: Any user can send arbitrary cross-chain messages
public fun send_message(
    oapp: &OApp,
    destination_eid: u32,
    message: vector<u8>,
) {
    // ❌ No signer check, no capability requirement
    // Any user can send messages that appear to come from this OApp
    // Destination chain processes message as legitimate protocol action
    layerzero_endpoint::send(
        oapp,
        destination_eid,
        get_peer(oapp, destination_eid),
        message,
        vector::empty(),
        vector::empty(),
    );
}
```

### Secure Implementation
```move
// ✅ SECURE: Capability-gated messaging
public fun send_message(
    oapp: &OApp,
    cap: &OAppAdminCap,
    destination_eid: u32,
    message: vector<u8>,
) {
    // ✅ Verify caller has OApp admin capability
    assert!(object::id(oapp) == cap.oapp_id, E_UNAUTHORIZED);
    
    layerzero_endpoint::send(
        oapp,
        destination_eid,
        get_peer(oapp, destination_eid),
        message,
        vector::empty(),
        vector::empty(),
    );
}
```

---

## Pattern 5: Signature Replay in Cross-Chain Claims — move-bridge-005

**Frequency**: 1/29 reports (Canopy [R2])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol

### Vulnerable Pattern Example

**Canopy — Claim Signature Resubmittable Within Window** [HIGH] [R2]
```move
// ❌ VULNERABLE: Valid signatures can be retransmitted
public fun claim_on_behalf(
    pool: &mut Pool,
    beneficiary: address,
    amount: u64,
    deadline: u64,
    signature: vector<u8>,
    clock: &Clock,
) {
    let now = clock::timestamp_ms(clock);
    assert!(now <= deadline, E_EXPIRED);
    
    // Verify signature from beneficiary
    let message = construct_claim_message(beneficiary, amount, deadline);
    assert!(verify_signature(beneficiary, message, signature), E_INVALID_SIG);
    
    // ❌ Signature not marked as used
    // Anyone who sees this signature can resubmit before deadline
    // Repeated claims + penalty imposition on beneficiary
    
    process_claim(pool, beneficiary, amount);
}
```

### Secure Implementation
```move
// ✅ SECURE: Track used signatures
public fun claim_on_behalf(
    pool: &mut Pool,
    beneficiary: address,
    amount: u64,
    deadline: u64,
    signature: vector<u8>,
    nonce: u64,
    clock: &Clock,
) {
    let now = clock::timestamp_ms(clock);
    assert!(now <= deadline, E_EXPIRED);
    
    // ✅ Include nonce in message to prevent replay
    let message = construct_claim_message(beneficiary, amount, deadline, nonce);
    assert!(verify_signature(beneficiary, message, signature), E_INVALID_SIG);
    
    // ✅ Mark nonce as used
    let user_nonces = table::borrow_mut(&mut pool.used_nonces, beneficiary);
    assert!(!table::contains(user_nonces, nonce), E_NONCE_USED);
    table::add(user_nonces, nonce, true);
    
    process_claim(pool, beneficiary, amount);
}
```

---

## Pattern 6: Fund Loss via Object ID Transfer — move-bridge-006

**Frequency**: 1/29 reports (Mayan Sui [R3])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but Sui-specific universal pattern

### Attack Scenario
1. Bridge sends gas refund to a "recipient" address from cross-chain message
2. On Sui, object IDs and user addresses are both 32-byte values
3. Message contains object ID (e.g., Order object) instead of user address
4. `transfer::public_transfer` sends funds to object ID
5. Funds are permanently irretrievable — cannot be accessed by anyone

### Vulnerable Pattern Example

**Mayan Sui — Gas Sent to Object ID** [HIGH] [R3]
```move
// ❌ VULNERABLE: Gas recipient may be an object ID, not an address
public fun complete_swap(
    state: &mut State,
    order: &Order,
    gas_amount: u64,
    ctx: &mut TxContext,
) {
    // gas_recipient comes from cross-chain message payload
    let gas_recipient = order.gas_recipient;  // ❌ May be object::id_to_address(order_id)
    
    let gas_coin = coin::split(&mut state.gas_pool, gas_amount, ctx);
    // ❌ If gas_recipient is an object ID, funds are permanently lost
    transfer::public_transfer(gas_coin, gas_recipient);
    // No address validation — Sui doesn't distinguish address vs object ID
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate recipient is a user address, not object ID
public fun complete_swap(
    state: &mut State,
    order: &Order,
    gas_amount: u64,
    ctx: &mut TxContext,
) {
    let gas_recipient = order.gas_recipient;
    
    // ✅ Verify recipient is in the set of known user addresses
    // Or validate that it's not equal to any known object ID
    assert!(is_valid_user_address(state, gas_recipient), E_INVALID_RECIPIENT);
    
    let gas_coin = coin::split(&mut state.gas_pool, gas_amount, ctx);
    transfer::public_transfer(gas_coin, gas_recipient);
}
```

---

### Impact Analysis

#### Technical Impact
- Permanent blocking of bridge minting via payload front-running (1/29 reports)
- Invalid validator sets accepting forged signatures (1/29 reports)
- Unauthorized cross-chain message spoofing (1/29 reports) — CRITICAL
- Signature replay enabling repeated unauthorized claims (1/29 reports)
- Permanent fund loss via object ID transfer (1/29 reports)

#### Business Impact
- Bridged assets permanently locked (payload front-running)
- Bridge integrity compromised (validator set manipulation)
- Cross-chain fund theft via message spoofing
- User funds irretrievable on Sui (object ID transfer)

#### Affected Scenarios
- Token bridges with multi-sig/consortium validation (Lombard)
- Cross-chain DeFi protocols using LayerZero/LZ (Canopy)
- Cross-chain DEX with gas refund mechanisms (Mayan Sui)
- Any protocol processing cross-chain messages on Move chains

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `public fun validate_and_store_payload` separate from mint
- Pattern 2: `configure_validator_set` without duplicate/length/threshold checks
- Pattern 3: `lz_receive` without message schema validation
- Pattern 4: `public fun send_message` without signer or capability check
- Pattern 5: `verify_signature` without marking nonce/hash as used
- Pattern 6: `transfer::public_transfer(coin, address_from_message)` without address validation
```

#### Audit Checklist
- [ ] Payload validation and minting are atomic (single function)
- [ ] Validator set checks: no duplicates, key length, threshold ≤ total weight
- [ ] All incoming cross-chain messages validated for schema and source
- [ ] Outgoing cross-chain messages require authorization
- [ ] All signatures include nonce, marked as used after verification
- [ ] Recipient addresses validated before transfer (not object IDs)
- [ ] Admin functions on bridge check package version

### Keywords for Search

> `cross-chain bridge`, `bridge vulnerability`, `payload front-running`, `validate_and_store_payload`, `validator set`, `configure_validator_set`, `message validation`, `lz_receive`, `layerzero`, `wormhole`, `cross-chain messaging`, `unrestricted messaging`, `signature replay`, `nonce`, `object ID`, `transfer::public_transfer`, `gas recipient`, `fund loss`, `move bridge`, `sui bridge`, `aptos bridge`

### Related Vulnerabilities

- [MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md](MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md) — Authorization patterns
- [MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md](MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md) — Verification bypass patterns
- [SUI_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md](SUI_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md) — Solodit-sourced bridge patterns
