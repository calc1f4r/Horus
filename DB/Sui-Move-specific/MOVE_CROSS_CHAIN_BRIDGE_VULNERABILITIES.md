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

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | cross_chain_messaging, bridge, validator_set, payload_processing, cross_chain_claim | payload_frontrunning, validator_set_integrity, signature_replay, message_validation_bypass, fund_loss_to_object

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - assert_and_configure_validator_set
  - block.timestamp
  - borrow
  - burn
  - burn_and_bridge
  - claim_on_behalf
  - complete_swap
  - cross_chain_bridge
  - cross_chain_messaging
  - decode_message
  - deposit
  - execute_transfer
  - fulfill_order
  - layerzero
  - lz_receive
  - mint
  - payload_validation
  - process_incoming_asset
  - receive
  - receive_message
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



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | cross_chain_messaging, bridge, validator_set, payload_processing, cross_chain_claim | payload_frontrunning, validator_set_integrity, signature_replay, message_validation_bypass, fund_loss_to_object`
- Interaction scope: `multi_contract`
- Primary affected component(s): `cross_chain_messaging, bridge, validator_set, payload_processing, cross_chain_claim`
- High-signal code keywords: `assert_and_configure_validator_set`, `block.timestamp`, `borrow`, `burn`, `burn_and_bridge`, `claim_on_behalf`, `complete_swap`, `cross_chain_bridge`
- Typical sink / impact: `fund_loss, message_spoofing, denial_of_service`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

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

## Pattern 7: Missing Version Check in Admin Functions — move-bridge-007

**Severity**: HIGH  
**ID**: move-bridge-007  
**References**: Wormhole NTT (OS-NTT-ADV-00)

### Attack Scenario
Bridge contracts use versioned upgrades, but admin functions (like setting peers, transceivers, or rate limits) don't check the current package version. If an admin calls a function designed for version N while the contract is at version N-1 (or N+1), the storage layout mismatch can corrupt state, disable the bridge, or allow unauthorized operations from an old version.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No version gate on admin function
public fun set_peer(admin: &signer, chain_id: u16, peer_address: vector<u8>) {
    // ❌ Missing: assert!(state.version == CURRENT_VERSION)
    let state = borrow_global_mut<BridgeState>(@bridge);
    table::upsert(&mut state.peers, chain_id, peer_address);
}
```

### Secure Implementation
```move
// ✅ SECURE: Version-gated admin function
public fun set_peer(admin: &signer, chain_id: u16, peer_address: vector<u8>) {
    let state = borrow_global_mut<BridgeState>(@bridge);
    assert!(state.version == CURRENT_VERSION, E_VERSION_MISMATCH);
    assert!(signer::address_of(admin) == state.admin, E_UNAUTHORIZED);
    table::upsert(&mut state.peers, chain_id, peer_address);
}
```

---

## Pattern 8: Cross-Chain Replay from Missing Chain ID — move-bridge-008

**Severity**: CRITICAL  
**ID**: move-bridge-008  
**References**: Wormhole NTT (OS-NTT-ADV-01), Mayan Sui (OS-MFI-ADV-01)

### Attack Scenario
Cross-chain messages don't include or validate the destination chain ID. An attacker replays a message intended for one chain (e.g., Ethereum) on a different chain (e.g., Sui), claiming tokens twice. Without chain ID binding, any valid message on one chain is valid on every chain served by the bridge.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No chain ID in message verification
public fun receive_message(
    state: &mut BridgeState,
    payload: vector<u8>,
    signatures: vector<vector<u8>>
) {
    // ❌ Verifies signatures but doesn't check if message was intended for THIS chain
    verify_signatures(&state.validators, &payload, &signatures);
    let (sender, amount) = decode_transfer(payload);
    // Processes transfer regardless of destination chain
    mint_bridged_tokens(state, sender, amount);
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate destination chain ID
public fun receive_message(
    state: &mut BridgeState,
    payload: vector<u8>,
    signatures: vector<vector<u8>>
) {
    verify_signatures(&state.validators, &payload, &signatures);
    let (sender, amount, dest_chain) = decode_transfer(payload);
    // ✅ Reject messages not intended for this chain
    assert!(dest_chain == state.chain_id, E_WRONG_CHAIN);
    let nonce = extract_nonce(&payload);
    assert!(!table::contains(&state.used_nonces, nonce), E_REPLAY);
    table::add(&mut state.used_nonces, nonce, true);
    mint_bridged_tokens(state, sender, amount);
}
```

---

## Pattern 9: Transceiver ID Overflow Past Bitmap Limit — move-bridge-009

**Severity**: HIGH  
**ID**: move-bridge-009  
**References**: Wormhole NTT (OS-NTT-ADV-02)

### Attack Scenario
The bridge tracks registered transceivers using a bitmap (e.g., 64-bit). If the transceiver registration counter exceeds the bitmap capacity (64 for u64), new transceivers silently overflow and map to ID 0 or wrap around. This can cause false attestation matches, allowing messages attested by an unauthorized transceiver to be treated as validated.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No check that ID fits in bitmap
struct ManagerState has key {
    next_transceiver_id: u8,
    enabled_bitmap: u64,
}

public fun register_transceiver(state: &mut ManagerState) {
    let id = state.next_transceiver_id;
    // ❌ If id >= 64, the shift overflows: 1u64 << 64 is undefined
    state.enabled_bitmap = state.enabled_bitmap | (1u64 << (id as u8));
    state.next_transceiver_id = id + 1;
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate transceiver ID fits in bitmap
const MAX_TRANSCEIVERS: u8 = 64;

public fun register_transceiver(state: &mut ManagerState) {
    let id = state.next_transceiver_id;
    assert!(id < MAX_TRANSCEIVERS, E_MAX_TRANSCEIVERS);
    state.enabled_bitmap = state.enabled_bitmap | (1u64 << (id as u8));
    state.next_transceiver_id = id + 1;
}
```

---

## Pattern 10: Inconsistent Deadline Checks Across Chains — move-bridge-010

**Severity**: MEDIUM  
**ID**: move-bridge-010  
**References**: Mayan Sui (OS-MFI-ADV-02)

### Attack Scenario
Cross-chain swap orders have deadlines, but the deadline interpretation differs across chains. The source chain uses block.timestamp (seconds), while the destination chain uses epoch_timestamp_ms (milliseconds). An order that expired on one chain may still appear valid on another, allowing late execution of stale orders at outdated rates.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Deadline comparison uses wrong time unit
public fun fulfill_order(state: &mut State, order: &Order, clock: &Clock) {
    let current_time = clock::timestamp_ms(clock);  // Milliseconds on Sui
    // ❌ order.deadline was set in SECONDS on source chain (Ethereum)
    assert!(current_time < order.deadline, E_EXPIRED);
    // Passes check because ms >> seconds (e.g., 1700000000 ms < 1700000100 seconds)
    process_swap(state, order);
}
```

### Secure Implementation
```move
// ✅ SECURE: Normalize time units before comparison
public fun fulfill_order(state: &mut State, order: &Order, clock: &Clock) {
    let current_time_s = clock::timestamp_ms(clock) / 1000;  // Convert to seconds
    assert!(current_time_s < order.deadline, E_EXPIRED);
    process_swap(state, order);
}
```

---

## Pattern 11: Zero-Value Burn Without Supply Validation — move-bridge-011

**Severity**: MEDIUM  
**ID**: move-bridge-011  
**References**: Lombard SUI (OS-LSI-ADV-02)

### Attack Scenario
A bridge accepts zero-value burn instructions, emitting a cross-chain message that claims tokens were burned. The source chain processes the message and releases tokens despite no actual value being locked. Repeated zero-burns can exhaust bridge reserves or create accounting inconsistencies between chains.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Zero-value burn emits valid cross-chain message
public fun burn_and_bridge(
    state: &mut BridgeState,
    tokens: Coin<LBTC>,
    dest_chain: u16,
    ctx: &mut TxContext
) {
    let amount = coin::value(&tokens);
    // ❌ No minimum amount check — zero-value burns generate messages
    coin::burn(&mut state.burn_cap, tokens);
    emit_cross_chain_message(state, dest_chain, amount, tx_context::sender(ctx));
}
```

### Secure Implementation
```move
// ✅ SECURE: Require minimum burn amount
public fun burn_and_bridge(
    state: &mut BridgeState,
    tokens: Coin<LBTC>,
    dest_chain: u16,
    ctx: &mut TxContext
) {
    let amount = coin::value(&tokens);
    assert!(amount >= state.min_bridge_amount, E_BELOW_MINIMUM);
    coin::burn(&mut state.burn_cap, tokens);
    emit_cross_chain_message(state, dest_chain, amount, tx_context::sender(ctx));
}
```

---

## Pattern 12: Deserialization Access Control Bypass — move-bridge-012

**Severity**: HIGH  
**ID**: move-bridge-012  
**References**: LayerZero Aptos (OS-LZA-ADV-00)

### Attack Scenario
Cross-chain message deserialization functions are public and don't verify the caller. An attacker can craft arbitrary byte payloads, call the deserialization function directly, and produce structs that bypass the normal message validation pipeline. This decouples message creation from message authentication.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Public deserialization without authentication
public fun decode_message(payload: vector<u8>): TransferMessage {
    // ❌ Anyone can call this to create a TransferMessage struct
    let amount = bcs::peel_u64(&mut payload);
    let recipient = bcs::peel_address(&mut payload);
    TransferMessage { amount, recipient }
}

public fun execute_transfer(state: &mut State, msg: TransferMessage) {
    // ❌ Assumes msg was authenticated, but attacker created it via decode_message
    mint_tokens(state, msg.recipient, msg.amount);
}
```

### Secure Implementation
```move
// ✅ SECURE: Deserialization is friend-only; execution requires proof
public(friend) fun decode_message(payload: vector<u8>): TransferMessage {
    let amount = bcs::peel_u64(&mut payload);
    let recipient = bcs::peel_address(&mut payload);
    TransferMessage { amount, recipient }
}

public fun execute_transfer(state: &mut State, payload: vector<u8>, attestation: vector<u8>) {
    // ✅ Verify attestation first, then decode
    assert!(verify_attestation(&state.validators, &payload, &attestation), E_INVALID_ATTESTATION);
    let msg = decode_message(payload);
    mint_tokens(state, msg.recipient, msg.amount);
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
- Pattern 7: Admin functions without `assert!(state.version == CURRENT_VERSION)`
- Pattern 8: Message verification without destination chain_id check
- Pattern 9: `1u64 << (id as u8)` where id can exceed 63
- Pattern 10: `clock::timestamp_ms` compared directly to seconds-based deadline
- Pattern 11: `coin::burn` accepting zero-value coins
- Pattern 12: `public fun decode_message` callable by anyone without attestation
```

#### Audit Checklist
- [ ] Payload validation and minting are atomic (single function)
- [ ] Validator set checks: no duplicates, key length, threshold ≤ total weight
- [ ] All incoming cross-chain messages validated for schema and source
- [ ] Outgoing cross-chain messages require authorization
- [ ] All signatures include nonce, marked as used after verification
- [ ] Recipient addresses validated before transfer (not object IDs)
- [ ] Admin functions on bridge check package version
- [ ] Cross-chain messages include and validate destination chain ID
- [ ] Transceiver/relayer IDs bounded to bitmap capacity
- [ ] Deadline checks use consistent time units across chains
- [ ] Minimum burn/bridge amount enforced
- [ ] Message deserialization restricted to friend/internal modules

### Keywords for Search

> `cross-chain bridge`, `bridge vulnerability`, `payload front-running`, `validate_and_store_payload`, `validator set`, `configure_validator_set`, `message validation`, `lz_receive`, `layerzero`, `wormhole`, `cross-chain messaging`, `unrestricted messaging`, `signature replay`, `nonce`, `object ID`, `transfer::public_transfer`, `gas recipient`, `fund loss`, `move bridge`, `sui bridge`, `aptos bridge`, `version check`, `package version`, `chain ID`, `destination chain`, `cross-chain replay`, `transceiver`, `bitmap overflow`, `timestamp_ms`, `deadline`, `time unit`, `zero burn`, `minimum amount`, `deserialization`, `decode_message`, `attestation`, `NTT`

### Related Vulnerabilities

- [MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md](MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md) — Authorization patterns
- [MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md](MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md) — Verification bypass patterns
- [SUI_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md](SUI_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md) — Solodit-sourced bridge patterns

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`aptos`, `assert_and_configure_validator_set`, `block.timestamp`, `borrow`, `bridge`, `bridge_crosschain`, `burn`, `burn_and_bridge`, `claim_on_behalf`, `complete_swap`, `cross_chain`, `cross_chain_bridge`, `cross_chain_messaging`, `decode_message`, `defi`, `deposit`, `execute_transfer`, `front_running`, `fulfill_order`, `layerzero`, `lz_receive`, `messaging`, `mint`, `move`, `payload`, `payload_frontrunning, validator_set_integrity, signature_replay, message_validation_bypass, fund_loss_to_object`, `payload_validation`, `process_incoming_asset`, `receive`, `receive_message`, `replay`, `signature`, `signature_verification`, `sui`, `validator`, `validator_set`, `wormhole`
