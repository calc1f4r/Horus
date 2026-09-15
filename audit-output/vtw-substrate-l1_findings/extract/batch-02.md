# VTW Phase 1 + Phase 3 Extraction — substrate-l1_findings — batch-02

## FILE: chainflip-backend-audits-2023-04-trailofbits-securityreview-pdf.md
- classification: finding
- classification_reason: Body contains a full "Detailed Findings" section with 26 numbered TOB-CHFL-N issues, each with Severity/Difficulty/Type/Target, description, exploit scenario and recommendations; Appendix G adds a fix review of the same issues.
- protocol: Chainflip Protocol (chainflip-io/chainflip-backend State Chain + engine, and chainflip-io/chainflip-eth-contracts)
- auditor: Trail of Bits
- date: Engagement March 6 – April 28, 2023; report dated July 17, 2023; fix review June 26–30, 2023
- findings_count: 26

### F: Step 2 of the handover protocol can be forged
- severity: Medium
- component: Bitcoin key handover protocol (FROST/threshold key handover, step 2 Schnorr-like proof of knowledge)
- root_cause: The Fiat-Shamir hash in the step-2 proof of knowledge omits the commitment N, so the "proof" is not bound to the commitment and can be satisfied by picking z at random and deriving N.
- missing_control: The commitment N is not included in the Fiat–Shamir hash input (should be `z = n - bH(N || l || T)` rather than `z = n - bH(l || T)`)
- interaction_scope: multi_contract
- contract_set: Bitcoin key handover protocol participants; ceremony/blame + slashing path
- entry_surface: P2P ceremony message (step 2 of handover protocol) / broadcast protocol
- trigger_primitive: Malicious participant 𝔸 skips step 1 correctly, generates random z, derives N, then jumps to step 3 and publishes k = t - a, then claims 𝔹 signaled agreement
- preconditions: internal — attacker is a handover-protocol participant (𝔸); external — none
- sink: Proof of knowledge of secret share b does not actually prove knowledge; blame attribution between 𝔸 and 𝔹 becomes undecidable by validators
- impact: Honest participant 𝔹 may be slashed; validators cannot determine who misbehaved
- code: |
    NO_CODE_IN_REPORT
- code_keywords: handover protocol, Fiat-Shamir, Schnorr proof of knowledge, commitment N, secret share, slashing

### F: Hash function is used as KDF in handover protocol
- severity: Informational
- component: Bitcoin key handover protocol, step 1 (DH key exchange + hash-as-keystream)
- root_cause: A plain cryptographic hash of a DH shared secret is used as a keystream to XOR-encrypt the ephemeral key t, i.e. the hash function is repurposed as a KDF.
- missing_control: No dedicated KDF (e.g. HKDF) and no authenticated encryption; plain XOR with hash output used instead
- interaction_scope: multi_contract
- contract_set: Bitcoin key handover protocol (step 1)
- entry_surface: P2P ceremony message (step 1 of handover protocol)
- trigger_primitive: Protocol design/implementation choice — no active attacker step stated
- preconditions: internal — handover ceremony executed; external — none
- sink: Key-derivation security property is not guaranteed by a general-purpose hash function
- impact: Weakened key derivation / encryption of the ephemeral key t
- code: |
    NO_CODE_IN_REPORT
- code_keywords: DH key exchange, KDF, HKDF, ephemeral key t, XSalsa20+Poly1305, keystream

### F: Ceremony participants can send many delayed messages
- severity: Informational
- component: `engine/src/multisig/client/ceremony_runner.rs` — CeremonyRunner delayed-message handling
- root_cause: The ceremony runner accepts ceremony data one round early and stores it via `BTreeMap::insert`, so repeated early messages from the same participant silently overwrite previously stored data.
- missing_control: No rejection/limit on repeated delayed messages from the same participant; `insert` overwrite is neither prevented nor logged
- interaction_scope: single_contract
- contract_set: CeremonyRunner (engine multisig client)
- entry_surface: P2P ceremony data message routed through `CeremonyRunner::process_or_delay_message`
- trigger_primitive: Malicious participant sends many messages containing ceremony data for the next round
- preconditions: internal — attacker is a ceremony participant; external — none
- sink: Previously stored delayed ceremony data is discarded/replaced
- impact: Enables unbounded resubmission of future-round data; strong indicator of malicious behavior that goes unnoticed
- code: |
    fn  add_delayed  (&  mut  self  ,  id:  AccountId  ,  m:  Ceremony  ::Data)  {
    // ...
    self  .delayed_messages.insert(id,  m);
    }
- code_keywords: add_delayed, delayed_messages, process_or_delay_message, CeremonyRunner, BTreeMap::insert, Ceremony::Data

### F: Binding value can be zero
- severity: Informational
- component: `engine/src/multisig/client/signing/signing_detail.rs` — FROST binding value `gen_rho_i`
- root_cause: `gen_rho_i` hashes signer index, message and commitments and reduces modulo the curve order without checking the result is in the multiplicative group Z_q*, so rho_i may be zero.
- missing_control: No check that the return value of `gen_rho_i` lies in [1, q) (FROST requires H_1 to take values in Z_q*)
- interaction_scope: single_contract
- contract_set: FROST signing implementation (engine multisig client)
- entry_surface: Threshold signing ceremony (signing share generation)
- trigger_primitive: Hash output happens to reduce to zero (vanishingly small probability in practice)
- preconditions: internal — signing ceremony running; external — none
- sink: Binding value rho_i = 0 breaks the binding of message/participants/commitments to the signature share (Drijvers et al. two-round multi-signature attack protection)
- impact: Loss of the FROST binding property in the degenerate case
- code: |
    fn  gen_rho_i  <P:  ECPoint  >(
    index:  AuthorityCount  ,
    msg:  &  [  u8  ],
    signing_commitments:  &  BTreeMap  <AuthorityCount,  SigningCommitment<P>>,
    all_idxs:  &  BTreeSet  <AuthorityCount>,
    )  ->  P  ::Scalar  {
    let  mut  hasher  =  Sha256::new();
    hasher.update(  b"I"  );
    hasher.update(index.to_be_bytes());
    hasher.update(msg);
    // This needs to be processed in order!
    for  idx  in  all_idxs  {
    let  com  =  &signing_commitments[idx];
    hasher.update(idx.to_be_bytes());
    hasher.update(com.d.as_bytes());
    hasher.update(com.e.as_bytes());
    }
    let  result  =  hasher.finalize();
    let  x: [  u8  ;  32  ]  =  result.as_slice().try_into().expect(  "Invalid  hash size"  );
    P::Scalar::from_bytes_mod_order(&x)
    }
- code_keywords: gen_rho_i, from_bytes_mod_order, SigningCommitment, AuthorityCount, ECPoint, Sha256, binding value, FROST

### F: The Chainflip back end and smart contracts have vulnerable dependencies
- severity: Medium
- component: Chainflip back end (Rust/Cargo) and Ethereum smart contracts (yarn/npm) dependency trees
- root_cause: The back end depends on `openssl` 0.10.45 (via `web3`/`reqwest`), `remove_dir_all` 0.5.3, `time` 0.1.45 and several unmaintained crates; the contract repo has 34 vulnerable npm dependencies including `@openzeppelin/contracts` < 4.4.1 and `minimist` < 1.2.6.
- missing_control: `cargo-audit` and `yarn audit` are not run in the CI pipeline; no alerting on vulnerable dependencies
- interaction_scope: cross_protocol
- contract_set: chainflip-backend (web3, reqwest, Substrate indirect deps), chainflip-eth-contracts (OpenZeppelin, minimist)
- entry_surface: Node RPC/TLS interface (openssl X.509 parsing); local filesystem (remove_dir_all)
- trigger_primitive: Node operator points the engine at an external HTTPS RPC endpoint (e.g. Infura), exposing the openssl attack surface to a privileged network attacker
- preconditions: internal — vulnerable versions pinned; external — attacker with privileged network position, or local filesystem write access
- sink: Arbitrary file read / null pointer dereference / TOCTOU race via dependency vulnerabilities
- impact: Information disclosure — e.g. reading the State Chain private key file over the network
- code: |
    NO_CODE_IN_REPORT
- code_keywords: openssl, web3, reqwest, remove_dir_all, time, ansi_term, mach, parity-util-mem, parity-wasm, RUSTSEC-2023-0022, RUSTSEC-2023-0023, RUSTSEC-2023-0024, RUSTSEC-2023-0018, RUSTSEC-2020-0071, CVE-2021-46320, CVE-2021-44906, minimist, http-rustls-tls, cargo-audit, yarn audit

### F: Potential panic in KeyId::from_bytes
- severity: Informational
- component: `state-chain/primitives/src/lib.rs` — `KeyId::from_bytes`
- root_cause: `from_bytes` slices `bytes[..size_of_epoch_index]` and calls `.unwrap()` on the `try_into`, so any input shorter than `size_of::<EpochIndex>()` panics.
- missing_control: No length validation on the input slice; no fallible `TryFrom<&[u8]>` conversion returning an error
- interaction_scope: single_contract
- contract_set: state-chain primitives (KeyId)
- entry_surface: Deserialization of key IDs read from persistent storage (and any future untrusted-source reuse)
- trigger_primitive: A short byte slice is passed to `KeyId::from_bytes`
- preconditions: internal — developer reuses `from_bytes` on untrusted input; external — attacker supplies short input
- sink: Panic in the node process
- impact: Denial of service against the node
- code: |
    pub  fn  from_bytes  (bytes:  &  [  u8  ])  ->  Self  {
    let  size_of_epoch_index  =  sp_std::mem::size_of::<EpochIndex>();
    let  epoch_index  = EpochIndex::from_be_bytes(
    bytes[..size_of_epoch_index].try_into().unwrap()
    );
    let  public_key_bytes  =  bytes[size_of_epoch_index..].to_vec();
    Self  {  epoch_index,  public_key_bytes  }
    }
- code_keywords: KeyId::from_bytes, size_of_epoch_index, EpochIndex::from_be_bytes, public_key_bytes, TryFrom, unwrap

### F: Solidity compiler optimizations can be problematic
- severity: Undetermined
- component: Solidity codebase (compiler configuration for chainflip-eth-contracts)
- root_cause: Optional Solidity compiler optimizations are enabled; the optimizer is disabled by default, historically under-tested, and has produced high-severity miscompilation bugs.
- missing_control: No measurement of gas savings weighed against optimizer risk; no monitoring of optimizer maturity
- interaction_scope: single_contract
- contract_set: All Chainflip Ethereum contracts (Vault, KeyManager, StakeManager, FLIP, Deposit, TokenVesting)
- entry_surface: Build/compilation configuration
- trigger_primitive: A latent or future optimizer / emscripten `solc-js` transpilation bug
- preconditions: internal — optimizer enabled; external — compiler bug exists
- sink: Compiled bytecode semantics diverge from source semantics
- impact: Security vulnerability introduced into deployed Chainflip contracts
- code: |
    NO_CODE_IN_REPORT
- code_keywords: solc, optimizer, solc-js, emscripten, Keccak-256 caching, bit shift optimization bug

### F: ERC-20 token transfer fails for certain tokens
- severity: High
- component: `contracts/Vault.sol` — internal `_transfer` (used by `transfer`, `transferBatch`, `govWithdraw`)
- root_cause: The hand-rolled safeTransfer equivalent decodes the low-level call return data to `bool` *before* checking its length, so the `abi.decode` reverts for nonstandard ERC-20 tokens (e.g. USDT) that return no data.
- missing_control: `returndata.length == 0` is not checked before `abi.decode(returndata, (bool))` — the Boolean short-circuit order is inverted versus OpenZeppelin `safeTransfer`
- interaction_scope: multi_contract
- contract_set: Vault.sol, arbitrary ERC-20 token contracts, Deposit.sol flow
- entry_surface: `transfer` / `transferBatch` / `govWithdraw` on Vault (aggregate-key gated calls)
- trigger_primitive: Protocol adds support for a no-return-value ERC-20 (USDT); any transfer out of the Vault of that token
- preconditions: internal — token added to supported set; external — token does not return a bool on transfer
- sink: Egress transfer out of the Vault always reverts for that token
- impact: User funds stuck in the protocol (recoverable only via governance through `executexSwapAndCall`/`executeActions`)
- code: |
    // solhint-disable-next-line avoid-low-level-calls
    (  bool  success  ,  bytes  memory  returndata)  =  token.call(
    abi.encodeWithSelector(IERC20(token).transfer.selector,  recipient,  amount)
    );
    // No need to check token.code.length since it comes from a gated call
    bool  transferred  =  success  &&  (
    abi.decode(returndata,  (  bool  ))  ||  returndata.length  ==  uint256  (  0  )
    );
    if  (!transferred)  emit  TransferTokenFailed(recipient,  amount,  token,  returndata);
- code_keywords: _transfer, Vault.sol, abi.decode, returndata.length, TransferTokenFailed, safeTransfer, transferBatch, govWithdraw, executexSwapAndCall, executeActions, USDT

### F: addGasNative is missing check for nonzero value
- severity: Informational
- component: `contracts/Vault.sol` — `addGasNative`
- root_cause: `addGasNative` emits an event for `msg.value` without validating that it is nonzero, inconsistent with every other value-taking function which uses the `nzUint` modifier.
- missing_control: Missing `nzUint(msg.value)` modifier
- interaction_scope: single_contract
- contract_set: Vault.sol
- entry_surface: External payable function `addGasNative(bytes32 swapID)`
- trigger_primitive: Any caller submits `addGasNative` with zero `msg.value`
- preconditions: internal — contract not suspended; external — none
- sink: Zero-value `AddGasNative` events emitted and consumed downstream
- impact: Inconsistent validation assumptions; spurious events for the engine to process
- code: |
    function  addGasNative  (  bytes32  swapID  )  external  payable  override  onlyNotSuspended  {
    emit  AddGasNative(swapID,  msg.value  );
    }
- code_keywords: addGasNative, nzUint, AddGasNative, onlyNotSuspended, addGasToken, safeTransferFrom

### F: StakeManager contains unnecessary receive function
- severity: Informational
- component: `contracts/StakeManager.sol` — `receive()`
- root_cause: The contract defines a payable `receive` function despite not requiring ether interactions, so accidental ETH sends are accepted instead of reverting by default.
- missing_control: Absence of the default reject behavior — the contract should have no `receive`/`fallback`
- interaction_scope: single_contract
- contract_set: StakeManager.sol (recovery via `govWithdrawNative`)
- entry_surface: Plain ETH transfer to StakeManager
- trigger_primitive: User accidentally sends ETH to the StakeManager address
- preconditions: internal — receive function present; external — user error
- sink: ETH accumulates in a contract with no intended ether flow
- impact: User ETH recoverable only by the governor calling `govWithdrawNative`
- code: |
    /**
    *  @notice Allows this contract to receive native tokens
    */
    receive()  external  payable  {}
- code_keywords: receive, StakeManager.sol, govWithdrawNative, fallback

### F: Missing events for important operations
- severity: Low
- component: `contracts/Vault.sol` (`executexCall`, `executexSwapAndCall`) and `contracts/KeyManager.sol` (`govWithdrawNative`)
- root_cause: Cross-chain call execution functions and the KeyManager governance withdrawal do not emit events, unlike their peers (StakeManager's `govWithdrawNative` emits `GovernanceWithdrawal`).
- missing_control: No success/failure event emitted for `executexCall`/`executexSwapAndCall`; missing `GovernanceWithdrawal` event in `KeyManager.govWithdrawNative`
- interaction_scope: cross_chain
- contract_set: Vault.sol, KeyManager.sol, StakeManager.sol, ICFReceiver recipients
- entry_surface: Threshold-signature-gated `executexCall` / `executexSwapAndCall`; `onlyGovernor` `govWithdrawNative`
- trigger_primitive: Execution of a cross-chain message call or a governance native withdrawal
- preconditions: internal — contract not suspended, valid key nonce consumed; external — none
- sink: Off-chain monitoring/auditing cannot observe the execution of these operations
- impact: Reduced auditability and incident-response capability
- code: |
    function  executexCall  (
    SigData  calldata  sigData,
    address  recipient  ,
    uint32  srcChain  ,
    bytes  calldata  srcAddress,
    bytes  calldata  message
    )
    external
    override
    onlyNotSuspended
    nzAddr(recipient)
    consumesKeyNonce(
    // ...
    )
    {
    ICFReceiver(recipient).cfReceivexCall(srcChain,  srcAddress,  message);
    }
- code_keywords: executexCall, executexSwapAndCall, govWithdrawNative, GovernanceWithdrawal, consumesKeyNonce, ICFReceiver, cfReceivexCall, onlyGovernor

### F: Nonstandard ERC-20 tokens get stuck when depositing
- severity: High
- component: `contracts/Deposit.sol` — `fetch`, via `contracts/interfaces/IERC20Lite.sol`
- root_cause: `fetch` calls `token.transfer` through `IERC20Lite`, whose signature declares a `bool` return; the Solidity compiler therefore inserts a returndatasize >= 32 check and reverts for tokens (e.g. USDT) that return no data — the "not checking the return value" comment is wrong.
- missing_control: Interface declares `returns (bool)` instead of a no-return signature, and OpenZeppelin `safeTransfer` is not used
- interaction_scope: multi_contract
- contract_set: Deposit.sol, Vault.sol, IERC20Lite.sol, arbitrary ERC-20 tokens
- entry_surface: `fetch(IERC20Lite token)` called by the Vault (`require(msg.sender == vault)`), and Deposit constructor
- trigger_primitive: User deposits a nonstandard ERC-20 to a designated Deposit address; protocol attempts to fetch
- preconditions: internal — token supported by Chainflip; external — token's transfer returns no data
- sink: Ingress fetch always reverts; deposited tokens cannot be swept to the Vault
- impact: User funds permanently stuck in the Deposit contract
- code: |
    function  fetch  (IERC20Lite  token)  external  {
    require  (  msg.sender  ==  vault);
    // Slightly cheaper to use msg.sender instead  of Vault.
    if  (  address  (token)  ==  0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE  )  {
    // solhint-disable-next-line avoid-low-level-calls
    (  bool  success  ,  )  =  msg.sender  .call{value:  address  (  this  ).balance}(  ""  );
    require  (success);
    }  else  {
    // Not checking the return value to avoid  reverts for tokens with no return
    value.
    token.transfer(  msg.sender  ,  token.balanceOf(  address  (  this  )));
    }
    }
- code_keywords: Deposit.sol, fetch, IERC20Lite, token.transfer, balanceOf, 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE, safeTransfer, USDT

### F: transfer can fail due to a fixed gas stipend
- severity: Informational
- component: `contracts/KeyManager.sol` — `govWithdrawNative`
- root_cause: Ether is sent via `payable(recipient).transfer(amount)`, which forwards only a 2300 gas stipend, so a recipient requiring more gas (e.g. a proxy contract) causes the withdrawal to revert.
- missing_control: No use of `recipient.call{value: amount}("")` forwarding all remaining gas for a trusted, CEI-compliant privileged call
- interaction_scope: multi_contract
- contract_set: KeyManager.sol, Vault instance, governance key recipient contract
- entry_surface: `onlyGovernor` `govWithdrawNative()`
- trigger_primitive: Governance key is (or becomes) a contract whose receive logic exceeds 2300 gas
- preconditions: internal — governance key is a contract; external — none
- sink: Governance native-token withdrawal reverts with out-of-gas
- impact: Trusted recipient cannot withdraw ether held by the contract
- code: |
    function  govWithdrawNative  ()  external  override  onlyGovernor  {
    uint256  amount  =  address  (  this  ).balance;
    // Could use msg.sender or getGovernor() but hardcoding  the get call just for
    extra safety
    address  recipient  =  getKeyManager().getGovernanceKey();
    payable  (recipient).transfer(amount);
    emit  GovernanceWithdrawal(recipient,  amount);
    }
- code_keywords: govWithdrawNative, transfer, 2300 gas stipend, getGovernanceKey, getKeyManager, GovernanceWithdrawal, onlyGovernor, call{value:}

### F: Low number of block confirmations configured for external blockchains
- severity: Undetermined
- component: `state-chain/runtime/src/constants.rs` — `eth::BLOCK_SAFETY_MARGIN`, `btc::INGRESS_BLOCK_SAFETY_MARGIN`
- root_cause: The State Chain treats an external-chain transaction as final after a fixed, small number of block confirmations (4 for Ethereum, 3 for Bitcoin) rather than waiting for PoS finality, so reorged/uncle blocks can be witnessed as settled.
- missing_control: No check that the source Ethereum block is `finalized` per the PoS consensus mechanism (available over RPC); fixed confirmation counts used instead
- interaction_scope: cross_chain
- contract_set: state-chain runtime constants, cf-witnesser, cf-staking, StakeManager.sol
- entry_surface: Witnessing of external-chain events by the engine / cf-witnesser
- trigger_primitive: Attacker stakes on a forked Ethereum chain; witnessing starts after 4 blocks and the block later reverts
- preconditions: internal — BLOCK_SAFETY_MARGIN = 4 / INGRESS_BLOCK_SAFETY_MARGIN = 3; external — Ethereum reorg (seven-block reorgs have occurred)
- sink: State Chain balance credited without a corresponding locked stake on Ethereum
- impact: Attacker records stake value on the State Chain with no stake locked on Ethereum — value created from nothing across the bridge
- code: |
    pub  mod  eth  {
    use  cf_chains::{eth::Ethereum,  Chain};
    /// Number of blocks to wait until we deem the block  to be safe.
    pub  const  BLOCK_SAFETY_MARGIN: <Ethereum  as  Chain>::ChainBlockNumber  =  4  ;
    }
    pub  mod  btc  {
    use  cf_chains::{btc::Bitcoin,  Chain};
    /// Number of blocks to wait for until we deem a  BTC ingress to be safe.
    pub  const  INGRESS_BLOCK_SAFETY_MARGIN: <Bitcoin  as  Chain>::ChainBlockNumber  =
    3  ;
    }
- code_keywords: BLOCK_SAFETY_MARGIN, INGRESS_BLOCK_SAFETY_MARGIN, ChainBlockNumber, cf_chains, constants.rs, stake, uncle block, finalized

### F: Hard to diagnose error from default behavior during signer nomination
- severity: Informational
- component: `state-chain/runtime/src/chainflip/signer_nomination.rs` — `RandomSignerNomination::threshold_nomination_with_seed`
- root_cause: `Validator::authority_count_at_epoch(epoch_index).unwrap_or_default()` silently maps a missing `EpochAuthorityCount` to 0, and `success_threshold_from_share_count(0)` is 1, so a single signer is nominated for a threshold ceremony.
- missing_control: No `None` propagation when `authority_count_at_epoch` returns `None` (should abort with `SignersUnavailable` instead of defaulting to zero)
- interaction_scope: multi_contract
- contract_set: cf-threshold-signature pallet, cf-validator pallet, engine CeremonyManager
- entry_surface: Threshold signature request (pallet-internal) → engine `on_request_to_sign`
- trigger_primitive: `EpochAuthorityCount` storage is unset for the epoch (e.g. via a refactor introducing an uninitialized edge case)
- preconditions: internal — EpochAuthorityCount storage unset; external — none
- sink: Singleton signatories set produces a plain Schnorr signature with one key share rather than a valid threshold signature
- impact: Invalid threshold signatures generated in rare, hard-to-reproduce situations; rejected by `validate_unsigned` with a confusing error
- code: |
    fn  threshold_nomination_with_seed  <H:  Hashable  >(
    seed:  H  ,
    epoch_index:  EpochIndex  ,
    )  ->  Option  <BTreeSet<  Self  ::SignerId>>  {
    try_select_random_subset(
    seed_from_hashable(seed),
    cf_utilities::success_threshold_from_share_count(
    Validator::authority_count_at_epoch(epoch_index)  .unwrap_or_default()  ,
    )  as  usize  ,
    eligible_authorities(
    epoch_index,
    &Reputation::validators_suspended_for(&[
    Offence::ParticipateSigningFailed,
    Offence::MissedAuthorshipSlot,
    Offence::MissedHeartbeat,
    ]),
    ),
    )
    }
- code_keywords: threshold_nomination_with_seed, authority_count_at_epoch, unwrap_or_default, success_threshold_from_share_count, try_select_random_subset, EpochAuthorityCount, SignersUnavailable, single_party_signing, eligible_authorities, validate_unsigned

### F: Failed broadcast nominees are not punished if epoch ends during broadcast
- severity: Low
- component: `state-chain/pallets/cf-broadcast/src/lib.rs` — `FailedBroadcasters` storage, `clean_up_broadcast_storage`, `threshold_sign_and_broadcast`
- root_cause: When the epoch rotates mid-broadcast the aggregate key changes, threshold signature verification fails, and the retry path calls `clean_up_broadcast_storage` which empties `FailedBroadcasters` before any offence is reported.
- missing_control: No `OffenceReporter::report_many(PalletOffence::FailedToBroadcastTransaction, ...)` on the signature-verification-failure retry path (only on `SignatureAccepted`)
- interaction_scope: cross_chain
- contract_set: cf-broadcast pallet, cf-threshold-signature pallet, cf-validator (epoch rotation), external chain
- entry_surface: Broadcast nomination / transaction submission to external chain; epoch rotation `on_initialize` path
- trigger_primitive: Nominated validator deliberately delays the broadcast near the end of an epoch and waits for timeout
- preconditions: internal — epoch rotation occurs before the broadcast succeeds; external — attacker pseudo-randomly nominated at the right moment
- sink: Offence accounting for failed broadcasters is dropped — misbehavior goes unpunished
- impact: Malicious validators can delay user fund transfers near epoch boundaries with impunity
- code: |
    if  let  Some  (failed_signers)  =  FailedBroadcasters::<T,  I>::get(broadcast_id)  {
    T::OffenceReporter::report_many(
    PalletOffence::FailedToBroadcastTransaction,
    &failed_signers,
    );
    }
- code_keywords: FailedBroadcasters, clean_up_broadcast_storage, threshold_sign_and_broadcast, OffenceReporter, report_many, PalletOffence::FailedToBroadcastTransaction, RequestCallbacks, SignatureAccepted, broadcast_id

### F: Nominated broadcast signer does not always report failures in engine
- severity: Informational
- component: `engine/src/state_chain_observer/sc_observer/mod.rs` — TransactionBroadcastRequest handlers (Ethereum, Polkadot, Bitcoin)
- root_cause: Signing failures are reported via the `transaction_signing_failure` extrinsic, but transmission (RPC) failures are only logged with `info!` and never reported to the State Chain.
- missing_control: No `transaction_signing_failure` submission on the transmission-failure branch
- interaction_scope: cross_chain
- contract_set: Chainflip engine state-chain observer, cf-broadcast pallet, external chain RPC
- entry_surface: `TransactionBroadcastRequest` event handling in the engine; external-chain RPC API call
- trigger_primitive: The external-chain RPC transmission fails after successful signing
- preconditions: internal — node is the nominated signer; external — RPC failure
- sink: State Chain is never told the broadcast failed
- impact: All validators must wait for the timeout before a new nominee is selected — delayed broadcasts
- code: |
    Err  (e)  =>  {
    info!(  "TransmissionRequest {broadcast_attempt_id}  failed: {e:?}"  );
    },
- code_keywords: transaction_signing_failure, TransactionBroadcastRequest, TransmissionRequest, broadcast_attempt_id, submit_signed_extrinsic, EthereumBroadcaster, sc_observer

### F: Threshold signature liveness protection does not account for previously punished validators
- severity: Informational
- component: `state-chain/pallets/cf-threshold-signature/src/lib.rs` — `offenders` function / liveness threshold
- root_cause: The liveness cap is computed as `self.participant_count / 2` per ceremony without considering validators already suspended from earlier ceremonies, so successive ceremonies can cumulatively suspend two-thirds of the authority set.
- missing_control: Liveness threshold is not derived from the number of currently suspended/available validators in the authority set
- interaction_scope: single_contract
- contract_set: cf-threshold-signature pallet, Reputation/suspension subsystem
- entry_surface: `report_signature_failed` extrinsic / ceremony timeout offence reporting
- trigger_primitive: Punish half the participants in ceremony N, then a different half in ceremony N+1
- preconditions: internal — punished validators are suspended and thus excluded from the next ceremony; external — colluding reporters
- sink: More than the intended fraction of the authority set ends up suspended simultaneously
- impact: Protocol cannot progress — signing halted (per Chainflip's response, up to 15 minutes/heartbeat interval)
- code: |
    // The maximum number of offenders we are willing to report without risking the
    // liveness  of the network.
    let  liveness_threshold  =  self  .participant_count  /  2  ;
- code_keywords: liveness_threshold, participant_count, offenders, cf-threshold-signature, suspended validators, authority set

### F: A malicious minority can ruin liveness
- severity: Medium
- component: `engine/src/multisig/client/common/broadcast_verification.rs` — reliable broadcast verification / `find_frequent_element`
- root_cause: A party is reported whenever a two-thirds threshold majority of the ceremony's participants cannot agree on the value it broadcast; since ceremonies contain only two-thirds of the authority set, 34 colluding parties out of 100 participants can deny agreement and get 50 honest members punished.
- missing_control: Punishment threshold for reliable broadcast is set at the threshold majority rather than at least half the participants
- interaction_scope: multi_contract
- contract_set: engine broadcast_verification, cf-threshold-signature pallet (liveness protection TOB-CHFL-19), Reputation/suspension
- entry_surface: Reliable broadcast phase of a signing ceremony (P2P messages)
- trigger_primitive: Colluding validators claim they received no messages from a chosen set of honest participants
- preconditions: internal — attackers nominated into the ceremony (34 of 100 participants); external — 40–50 colluding validators (probability of 34+ selected ≈ 3 in 1,000 at 40 colluders, 2 in 3 at 50)
- sink: Honest validators are reported and suspended; colluders are then guaranteed selection for the ceremony repetition and repeat the attack
- impact: Network liveness destroyed — no ceremonies can be conducted until suspensions expire
- code: |
    // Check that the values are agreed on by the threshold majority.
    // A party is reported if we can't agree on the value they broadcast
    // or if the agreed upon value is `None` (i.e. they didn't broadcast)
    for  idx  in  &participating_idxs  {
    let  message_iter  =  verification_messages.values().map(|m|  m.data[idx].clone());
    if  let  Some  (  Some  (data))  =  find_frequent_element(message_iter,  threshold)  {
    agreed_on_values.insert(*idx,  data);
    }  else  {
    reported_parties.insert(*idx)  ;
    }
    }
- code_keywords: broadcast_verification, find_frequent_element, participating_idxs, verification_messages, agreed_on_values, reported_parties, threshold, reliable broadcast

### F: Validators can report nonparticipants in ceremonies
- severity: Medium
- component: `state-chain/pallets/cf-threshold-signature/src/lib.rs` (`blame_counts`) and `state-chain/pallets/cf-vaults/src/lib.rs` (`blame_votes`)
- root_cause: `report_signature_failed` (and the cf-vaults keygen equivalent) accumulate blame counts via `entry(id).or_default()` for arbitrary `ValidatorId` values without verifying the reported account was a ceremony participant or even a member of the current authority set.
- missing_control: No membership check that reported offenders participated in the ceremony / belong to the current authority set
- interaction_scope: multi_contract
- contract_set: cf-threshold-signature pallet, cf-vaults pallet, Reputation/suspension
- entry_surface: Signed extrinsic `report_signature_failed` (cf-threshold-signature); keygen failure reporting (cf-vaults)
- trigger_primitive: A colluding group (67 validators for cf-threshold-signature, 100 for cf-vaults) blames non-participants who are then reported on ceremony timeout
- preconditions: internal — blame counts keyed on an unvalidated BTreeSet; external — more than a third of the authority set colluding
- sink: Validators outside the ceremony (back-up or historical validators) are punished
- impact: Targeted validators lose reputation or are suspended
- code: |
    for  id  in  offenders  {
    (*context.blame_counts.entry(id).or_default())  +=  1  ;
    }
- code_keywords: report_signature_failed, blame_counts, blame_votes, or_default, ValidatorId, BTreeSet, blame_threshold, to_report, cf-vaults, cf-threshold-signature

### F: Staker funds can be locked via front-running
- severity: High
- component: `eth-contracts/contracts/StakeManager.sol` `stake` + `backend/state-chain/pallets/cf-staking/src/lib.rs` `check_withdrawal_address` / `WithdrawalAddresses`
- root_cause: The first stake for a node ID permanently binds a withdrawal (return) address; the Ethereum contract accepts any `returnAddr` from any caller, so an attacker can be first to bind a node ID to an address of their choosing, after which the legitimate staker's funds are taken by the contract but rejected by the pallet.
- missing_control: No binding of the withdrawal address to the staker (no double-map keyed by staker and node ID); no automatic refund on `WithdrawalAddressRestricted`
- interaction_scope: cross_chain
- contract_set: StakeManager.sol, FLIP token, cf-staking pallet (`WithdrawalAddresses`, `FailedStakeAttempts`), cf-witnesser
- entry_surface: Public `stake(bytes32 nodeID, uint256 amount, address returnAddr)` extrinsic-equivalent on Ethereum; witnessed into the cf-staking pallet
- trigger_primitive: Attacker front-runs a pending stake transaction (or pre-registers a known node ID) with the same node ID, the minimum stake amount, and a different return address
- preconditions: internal — WithdrawalAddresses entry already set for the node ID; external — attacker holds minimum stake amount of FLIP and watches the mempool
- sink: `check_withdrawal_address` returns `Err(WithdrawalAddressRestricted)`; tokens already transferred into the contract are not credited and not refunded
- impact: Legitimate staker's FLIP is locked in the contract until governance releases it; attack cost is only the minimum stake, enabling sustained DoS on validator onboarding
- code: |
    function  stake  (
    bytes32  nodeID  ,
    uint256  amount  ,
    address  returnAddr
    )  external  override  nzBytes32(nodeID)  nzAddr(returnAddr)  {
    IFLIP  flip  =  _FLIP;
    require  (  address  (flip)  !=  address  (  0  ),  "Staking:  Flip not set"  );
    require  (amount  >=  _minStake,  "Staking: stake  too small"  );
    // Assumption of set token allowance by the user
    flip.transferFrom(  msg.sender  ,  address  (  this  ),  amount);
    emit  Staked(nodeID,  amount,  msg.sender  ,  returnAddr);
    }
- code_keywords: stake, nodeID, returnAddr, WithdrawalAddresses, check_withdrawal_address, WithdrawalAddressRestricted, FailedStakeAttempts, FailedStakeAttempt, Staked, _minStake, nzBytes32, nzAddr

### F: Unbounded loop execution may result in out-of-gas errors
- severity: Informational
- component: `contracts/Vault.sol` — `allBatch`, `deployAndFetchBatch`, `_deployAndFetchBatch`, `fetchBatch`, `transferBatch`
- root_cause: Batch functions iterate over caller-supplied arrays deploying a `Deposit` contract per element and performing fetches/transfers, with no bound on array length or gas accounting.
- missing_control: No cap on `deployFetchParamsArray`/`fetchParamsArray`/`transferParamsArray` length and no gas estimation as a function of array size
- interaction_scope: multi_contract
- contract_set: Vault.sol, Deposit.sol (CREATE2 with `salt: swapID`)
- entry_surface: Aggregate-key-signed `allBatch` / `deployAndFetchBatch` (`consumesKeyNonce`)
- trigger_primitive: A batch call with a large params array
- preconditions: internal — contract not suspended, valid key nonce; external — sufficient array size
- sink: Transaction runs out of gas during execution
- impact: Batch fetch/transfer operations fail; egress/ingress processing stalls
- code: |
    function  _deployAndFetchBatch  (DeployFetchParams[]  calldata  deployFetchParamsArray)
    private  {
    // Deploy deposit contracts
    uint256  length  =  deployFetchParamsArray.length;
    for  (  uint256  i  =  0  ;  i  <  length;  )  {
    new  Deposit{salt:  deployFetchParamsArray[i].swapID}(
    IERC20Lite(deployFetchParamsArray[i].token)
    );
    unchecked  {
    ++i;
    }
    }
    }
- code_keywords: allBatch, deployAndFetchBatch, _deployAndFetchBatch, fetchBatch, transferBatch, DeployFetchParams, FetchParams, TransferParams, consumesKeyNonce, salt, swapID, Deposit

### F: Anyone can cause the Chainflip engine to panic
- severity: Medium
- component: `engine/src/eth/vault.rs` — `decode_log_closure` (SwapToken / xCallToken / addGasToken event decoding)
- root_cause: Event amounts are decoded as `ethabi::Uint` and converted with `.try_into().expect("SwapToken amount should fit into u128")`, while `Vault.xSwapToken` accepts any ERC-20 with any `uint256` amount and performs no upper-bound validation.
- missing_control: No validation that the token is supported/that the amount fits `u128` before decoding; a panicking `expect` instead of error propagation
- interaction_scope: cross_chain
- contract_set: Vault.sol (`xSwapToken`, `xCallToken`, `addGasToken`), Chainflip engine Ethereum vault witnesser, attacker-deployed ERC-20
- entry_surface: Public `xSwapToken(uint32,bytes,uint16,IERC20,uint256)` on Vault → `SwapToken` event consumed by the engine
- trigger_primitive: Attacker deploys a dummy token with supply greater than 2^128 - 1 and calls `xSwapToken` with a huge amount
- preconditions: internal — engine decodes all Vault events uniformly, panic unhandled; external — attacker can deploy an arbitrary ERC-20
- sink: `expect` panics in the engine's log decoding path
- impact: Engine halts — network-wide denial of service, cost of attack is a single token deployment
- code: |
    if  event_signature  ==  swap_token.signature  {
    let  log  =  swap_token.event.parse_log(raw_log)?;
    VaultEvent::SwapToken  {
    destination_chain:  utils  ::decode_log_param(&log,  "dstChain"  )?,
    destination_address:  utils  ::decode_log_param(&log,  "dstAddress"  )?,
    destination_token:  utils  ::decode_log_param(&log,  "dstToken"  )?,
    source_token:  utils  ::decode_log_param(&log,  "srcToken"  )?,
    amount:  utils  ::decode_log_param::<ethabi::Uint>(&log,  "amount"  )?
    .try_into()
    .expect(  "SwapToken amount should fit  into u128"  ),
    sender:  utils  ::decode_log_param(&log,  "sender"  )?,
    }
    }
- code_keywords: decode_log_closure, decode_log_param, VaultEvent::SwapToken, xSwapToken, xCallToken, addGasToken, ethabi::Uint, u128, expect, parse_log, call_from_event

### F: Failed deposits are incorrectly witnessed as having succeeded
- severity: High
- component: `engine/src/eth/ingress_witnesser.rs` `process_block` and `state-chain/pallets/cf-ingress-egress/src/lib.rs` `do_single_ingress`
- root_cause: The ingress witnesser enumerates transactions via `eth_getBlockByNumber` and filters by destination address without ever fetching the transaction receipt, so reverted transactions are witnessed as successful deposits and the LP account is credited.
- missing_control: No check of the transaction receipt status field (0 = failed, 1 = success); no verification the address actually received funds; no simulation of the subsequent `fetch` call
- interaction_scope: cross_chain
- contract_set: engine ingress_witnesser, cf-ingress-egress pallet, Deposit.sol, LpBalance/`try_credit_account`
- entry_surface: Ethereum transaction to a monitored ingress address, witnessed by the engine and dispatched through `do_single_ingress`
- trigger_primitive: Attacker sends a value-bearing transaction to the Deposit contract with a payload calling `fetch`, which reverts immediately
- preconditions: internal — witnesser uses `block_with_txs` with no receipt check; external — attacker can craft a reverting transaction to the ingress address
- sink: `IngressWitness` created for a failed transaction; `T::LpBalance::try_credit_account` credits value never actually received
- impact: Attacker is credited on the State Chain without transferring funds — free minting of protocol balance
- code: |
    let  ingress_witnesses  =  txs
    .iter()
    .filter_map(|tx|  {
    let  to_addr  =  core_h160(tx.to?);
    if  address_monitor.contains(&to_addr)  {
    Some  ((tx,  to_addr))
    }  else  {
    None
    }
    })
    .map(|(tx,  to_addr)|  IngressWitness  {
    ingress_address:  to_addr  ,
    asset:  eth  ::Asset::Eth,
    amount:  tx
    .value
    .try_into()
    .expect(  "Ingress witness transfer  value should fit u128"  ),
    tx_id:  core_h256  (tx.hash),
    })
- code_keywords: ingress_witnesser, process_block, block_with_txs, eth_getBlockByNumber, IngressWitness, address_monitor, do_single_ingress, IntentIngressDetails, ScheduledEgressFetchOrTransfer, FetchOrTransfer, IntentAction::LiquidityProvision, try_credit_account, IngressCompleted, InvalidIntent, IngressMismatchWithIntent

### F: Validators are not reimbursed for transactions submitted to external chains
- severity: Low
- component: `state-chain/pallets/cf-broadcast/src/lib.rs` — `signature_accepted` extrinsic / `TransactionFeeDeficit` storage
- root_cause: `TransactionFeeDeficit` accumulates the fee owed to each broadcasting signer but the storage item is only ever written, never read or settled.
- missing_control: No payout/credit path that reads `TransactionFeeDeficit` and reimburses validators
- interaction_scope: cross_chain
- contract_set: cf-broadcast pallet, external chain transaction submission, validator accounts
- entry_surface: `signature_accepted` extrinsic (witnessed external-chain acceptance)
- trigger_primitive: Any successful broadcast to an external chain
- preconditions: internal — reimbursement logic unimplemented; external — none
- sink: Validator economic accounting — fee deficit never discharged
- impact: Validators permanently bear the gas cost of outgoing external-chain transactions
- code: |
    TransactionFeeDeficit::<T,  I>::mutate(signer_id,  |fee_deficit|  {
    *fee_deficit  =  fee_deficit.saturating_add(to_refund);
    });
- code_keywords: TransactionFeeDeficit, signature_accepted, signer_id, to_refund, saturating_add, cf-broadcast

### F: MEV incentives are unclear and require further investigation
- severity: Undetermined
- component: `state-chain/pallets/cf-swapping/src/lib.rs` — JIT AMM (range orders + limit orders), batched swap execution
- root_cause: The AMM is a Uniswap-v3 derivative that removes slippage protection, price limits and deadlines, uses `tickSpacing = 1`, routes non-stable pairs through USDC, takes the network fee on the stable asset, and executes queued swaps as a single batch — creating unanalyzed economic and MEV incentives.
- missing_control: No slippage protection (price limits) and no swap deadlines; partial swaps disallowed; effects of `tickSpacing = 1` liquidity dust not analyzed
- interaction_scope: multi_contract
- contract_set: cf-swapping pallet, JIT AMM (range orders, limit orders), liquidity provisioning (cf-lp)
- entry_surface: Swap request extrinsics / queued batched swap execution
- trigger_primitive: An attacker includes a same-direction swap in the same batch as the victim and back-runs it; or a sole LP deploys capital at extreme price limits and initiates large trades in both directions; or an actor drains liquidity to stall swaps and re-provides liquidity at an unfavorable price
- preconditions: internal — no price limit, no deadline, batched execution, concentrated liquidity; external — attacker capital / LP position
- sink: Users receive an execution price arbitrarily far from the fair price; queued swaps can be stalled indefinitely
- impact: Value extracted from user trades (Eve receives the funds Alice lost); potential DoS of swaps via liquidity exhaustion; inaccurate price estimation
- code: |
    NO_CODE_IN_REPORT
- code_keywords: cf-swapping, JIT AMM, tickSpacing, range orders, limit orders, BTreeMap, slippage protection, deadline, batched swap, USDC, network fee, x * y = k, concentrated liquidity

---

## FILE: zenlink-peckshield.md
- classification: finding
- classification_reason: Body is a PeckShield audit report with a "Detailed Results" section containing four PVE-numbered issues, each with Severity/Likelihood/Impact/Target/CWE, description, code listings, recommendation and fix status.
- protocol: Zenlink Stable AMM & Swap Router (zenlink-stable-amm and zenlink-swap-router Substrate pallets, zenlinkpro/Zenlink-DEX-Module)
- auditor: PeckShield (Audit Report #: 2022-294)
- date: August 24, 2022 (Final Release); Release Candidate #1 August 1, 2022
- findings_count: 4

### F: Improved Implementation Logic for MetaPool
- severity: High
- component: `zenlink-stable-amm/src/lib.rs` — MetaPool swap math (`calculate_swap_amount`, `xp`, `get_y`) shared with BasePool
- root_cause: MetaPool and BasePool use the same implementation logic, but a MetaPool pairs a stablecoin against a BasePool LP token whose price steadily increases with accumulated fees; the swap math never scales the LP token amount by its virtual price.
- missing_control: The BasePool LP token's virtual price (obtainable via `calculate_virtual_price()`) is not applied to scale the LP token amount in MetaPool swap calculations
- interaction_scope: multi_contract
- contract_set: zenlink-stable-amm pallet — BasePool and MetaPool, zenlink-swap-router
- entry_surface: Swap extrinsics on a MetaPool (and other MetaPool functions with the same flaw)
- trigger_primitive: Swapping into/out of a MetaPool while the BasePool LP token virtual price has drifted above 1 due to accumulated fees
- preconditions: internal — MetaPool created against a BasePool LP token; external — fees accumulated in the BasePool
- sink: The LP token is valued as if it were a stablecoin — pool pricing invariant broken
- impact: The LP token value is underestimated: less stablecoin is swapped out (line 1501) or more LP tokens are swapped out (lines 1504-1507)
- code: |
    1487 pub fn c a l c u l a t e _ s w a p _ a m o u n t (
    1488 pool : & Pool < T :: CurrencyId , T :: AccountId , BoundedVec < u8 , T :: P o o l C u r r e n c y S y m b o l L i m i t
    > > ,
    1489 i : usize ,
    1490 j : usize ,
    1491 i n _ b a l a n c e : Balance ,
    1492 ) -> Option < Balance > {
    1493 let n _ c u r r e n c i e s = pool . c u r r e n c y _ i d s . len () ;
    1494 if i >= n _ c u r r e n c i e s || j >= n _ c u r r e n c i e s {
    1495 return None ;
    1496 }
    1497
    1498 let f e e _ d e n o m i n a t o r = F E E _ D E N O M I N A T O R ;
    1499
    1500 let n o r m a l i z e d _ b a l a n c e s = Self :: xp (& pool . balances , & pool . t o k e n _ m u l t i p l i e r s ) ?;
    1501 let n e w _ i n _ b a l a n c e = n o r m a l i z e d _ b a l a n c e s [ i ]. c h e c k e d _ a d d ( i n _ b a l a n c e . c h e c k e d _ m u l ( pool .
    t o k e n _ m u l t i p l i e r s [ i ]) ?) ?;
    1502
    1503 let o u t _ b a l a n c e = Self :: get_y ( pool , i , j , new_in_balance , & n o r m a l i z e d _ b a l a n c e s ) ?;
    1504 let mut o u t _ a m o u n t = n o r m a l i z e d _ b a l a n c e s [ j ]
    1505 . c h e c k e d _ s u b ( o u t _ b a l a n c e ) ?
    1506 . c h e c k e d _ s u b ( One :: one () ) ?
    1507 . c h e c k e d _ d i v ( pool . t o k e n _ m u l t i p l i e r s [ j ]) ?;
    1508
    1509 let fee = U256 :: from ( o u t _ a m o u n t )
    1510 . c h e c k e d _ m u l ( U256 :: from ( pool . fee ) ) ?
    1511 . c h e c k e d _ d i v ( U256 :: from ( f e e _ d e n o m i n a t o r ) )
    1512 . and _t he n (| n | TryInto :: < Balance >:: tr y_ in to ( n ) . ok () ) ?;
    1513
    1514 o u t _ a m o u n t = o u t _ a m o u n t . c h e c k e d _ s u b ( fee ) ?;
    1515
    1516 Some ( o u t _ a m o u n t )
    1517 }
- code_keywords: calculate_swap_amount, calculate_virtual_price, MetaPool, BasePool, xp, get_y, token_multipliers, normalized_balances, FEE_DENOMINATOR, lp_currency_id, StableSwap

### F: Revisited Logic in inner_remove_liquidity_imbalance()
- severity: Low
- component: `zenlink-stable-amm/src/lib.rs` — `remove_liquidity_imbalance()`, `inner_remove_liquidity_imbalance()`, `calculate_remove_liquidity_imbalance()`
- root_cause: `burn_amount` is computed with mixed multiplication and division (`(d0 - d1) * total_supply / d0`) which rounds down, and the result is used directly without rounding up.
- missing_control: No round-up (+1) applied to the `burn_amount` calculation before the slippage check and the LP withdraw
- interaction_scope: single_contract
- contract_set: zenlink-stable-amm pallet (Pools storage, MultiCurrency LP token)
- entry_surface: Public extrinsic `remove_liquidity_imbalance(origin, pool_id, amounts, max_burn_amount, to, deadline)` guarded by `ensure_signed`
- trigger_primitive: Repeated imbalanced liquidity removals exploiting the downward rounding of `burn_amount`
- preconditions: internal — pool has nonzero total supply and matching `amounts.len()`; external — none
- sink: Fewer LP tokens burned than economically correct — remaining LPs' share diluted
- impact: Precision loss at the expense of the pool's remaining liquidity providers
- code: |
    1600 fn c a l c u l a t e _ r e m o v e _ l i q u i d i t y _ i m b a l a n c e (
    1601 pool : & mut Pool < T :: CurrencyId , T :: AccountId , BoundedVec < u8 , T ::
    P o o l C u r r e n c y S y m b o l L i m i t > > ,
    1602 amounts : &[ Balance ] ,
    1603 t o t a l _ s u p p l y : Balance ,
    1604 ) -> Option <( Balance , Vec < Balance > , Balance ) > {
    1605 ...
    1606
    1607 let d1 = Self :: get_d (& Self :: xp (& new_balances , & pool . t o k e n _ m u l t i p l i e r s ) ? , amp ) ?;
    1608 let b u r n _ a m o u n t = d0
    1609 . c h e c k e d _ s u b ( U256 :: from ( d1 ) ) ?
    1610 . c h e c k e d _ m u l ( U256 :: from ( t o t a l _ s u p p l y ) ) ?
    1611 . c h e c k e d _ d i v ( d0 )
    1612 . and _t he n (| n | TryInto :: < Balance >:: tr y_ in to ( n ) . ok () ) ?;
    1613
    1614 Some (( burn_amount , fees , d1 ) )
    1615 }
- code_keywords: remove_liquidity_imbalance, inner_remove_liquidity_imbalance, calculate_remove_liquidity_imbalance, burn_amount, max_burn_amount, AmountSlippage, total_issuance, get_d, xp, try_mutate_exists, InsufficientLpReserve, MismatchParameter, Deadline, ensure_signed

### F: Improved Sanity Checks Of System/Function Parameters
- severity: Low
- component: `zenlink-stable-amm/src/lib.rs` — `remove_liquidity()` / `inner_remove_liquidity()` (and `inner_remove_liquidity_one_currency()`)
- root_cause: The `lp_amount` input argument is not constrained, so a user can call `remove_liquidity` with `lp_amount == 0`.
- missing_control: Missing `ensure!(lp_amount > 0, ...)` validation on the input argument
- interaction_scope: single_contract
- contract_set: zenlink-stable-amm pallet (Pools storage, MultiCurrency)
- entry_surface: Public extrinsic `remove_liquidity(origin, poo_id, lp_amount, min_amounts, to, deadline)` guarded by `ensure_signed`
- trigger_primitive: Calling the extrinsic with `lp_amount` set to 0
- preconditions: internal — none; external — none
- sink: A no-op state transition is accepted as valid
- impact: Waste of gas / pointless extrinsic execution
- code: |
    484 pub fn r e m o v e _ l i q u i d i t y (
    485 origin : OriginFor <T > ,
    486 poo_id : T :: PoolId ,
    487 l p _ a m o u n t : Balance ,
    488 m i n _ a m o u n t s : Vec < Balance > ,
    489 to : T :: AccountId ,
    490 de ad li ne : T :: BlockNumber ,
    491 ) -> D i s p a t c h R e s u l t {
    492 let who = e n s u r e _ s i g n e d ( origin ) ?;
    493
    494 let now = f r a m e _ s y s t e m :: Pallet :: < T >:: b l o c k _ n u m b e r () ;
    495 ensure! ( d ea dl in e > now , Error :: < T >:: De adl in e ) ;
    496
    497 Self :: i n n e r _ r e m o v e _ l i q u i d i t y ( poo_id , & who , lp_amount , & min_amounts , & to ) ?;
    498
    499 Ok (() )
    500 }
- code_keywords: remove_liquidity, inner_remove_liquidity, inner_remove_liquidity_one_currency, lp_amount, min_amounts, InsufficientReserve, MismatchParameter, ensure_signed, total_issuance, Deadline

### F: Trust Issue of Admin Keys
- severity: Medium
- component: `zenlink-stable-amm/src/lib.rs` — root-gated privileged extrinsics `create_pool`, `update_fee_receiver`, `set_fee`
- root_cause: A single privileged `root` origin governs system-wide operations (pool creation, admin fee receiver, swap/admin fee values), concentrating counter-party risk on that account.
- missing_control: Privileges of `root` are neither made explicit to users nor decentralized (`ensure_root(origin)?` with no timelock or multi-party gate)
- interaction_scope: single_contract
- contract_set: zenlink-stable-amm pallet (Pools storage, admin_fee_receiver, fee, admin_fee)
- entry_surface: Root-origin extrinsics `create_pool`, `update_fee_receiver`, `set_fee`
- trigger_primitive: Compromised or malicious root origin redirects admin fees or reconfigures pool parameters
- preconditions: internal — `ensure_root` gate only; external — root key compromise
- sink: Pool economic parameters and fee destination are unilaterally mutable (bounded only by MAX_A / MAX_SWAP_FEE / MAX_ADMIN_FEE)
- impact: Counter-party risk to Stable AMM users; admin fees can be diverted
- code: |
    147 pub fn c r e a t e _ p o o l (
    148 origin : OriginFor <T > ,
    149 c u r r e n c y _ i d s : Vec < T :: CurrencyId > ,
    150 c u r r e n c y _ d e c i m a l s : Vec < u32 > ,
    151 a : Number ,
    152 fee : Number ,
    153 a d m i n _ f e e : Number ,
    154 a d m i n _ f e e _ r e c e i v e r : T :: AccountId ,
    155 l p _ c u r r e n c y _ s y m b o l : Vec < u8 > ,
    156 ) -> D i s p a t c h R e s u l t {
    157 e n s u r e _ r o o t ( origin ) ?;
    158
    159 ensure! (
    160 T :: E n s u r e P o o l A s s e t :: v a l i d a t e _ p o o l e d _ c u r r e n c y (& c u r r e n c y _ i d s ) ,
    161 Error :: < T >:: I n v a l i d P o o l e d C u r r e n c y
    162 ) ;
    163
    164 ensure! (
    165 c u r r e n c y _ i d s . len () == c u r r e n c y _ d e c i m a l s . len () ,
    166 Error :: < T >:: M i s m a t c h P a r a m e t e r
    167 ) ;
    168 ensure! ( a < MAX_A , Error :: < T >:: E x c e e d M a x A ) ;
    169 ensure! ( fee <= MAX_SWAP_FEE , Error :: < T >:: E x c e e d M a x F e e ) ;
    170 ensure! ( a d m i n _ f e e <= MAX_ADMIN_FEE , Error :: < T >:: E x c e e d M a x A d m i n F e e ) ;
    171
    172 ...
    173 }
- code_keywords: ensure_root, create_pool, update_fee_receiver, set_fee, admin_fee_receiver, admin_fee, MAX_A, MAX_SWAP_FEE, MAX_ADMIN_FEE, ExceedThreshold, UpdateAdminFeeReceiver, NewFee, StaticLookup, try_mutate_exists

---

## FILE: acala-srl-2021-12.md
- classification: finding
- classification_reason: Body is a security assurance review with a threat model plus a "Findings summary" table of 6 severity-rated issues (1 high, 4 moderate, 1 low) each described in its own numbered subsection with affected pallet, exploit path and fix reference.
- protocol: Acala runtime (Acala/Karura parachain runtime modules, ORML community modules, stable-asset pallet)
- auditor: SRLabs (Security Research Labs) — Regina Bíró, Mostafa Sattari, Vincent Ulitzsch
- date: v1.1 – 12 January 2022 (second audit; first audit 2020)
- findings_count: 6

### F: Integer overflow in the xcm::v1 pallet could result in loss of asset tokens
- severity: high
- component: `Polkadot/xcm/src/v1/multiasset.rs` `from` function (Vec<MultiAsset> → MultiAssets), reachable via `orml/xtokens` `transfer_with_fee`
- root_cause: The XCM v1 `from` conversion adds asset amounts without overflow protection; Acala's `orml/xtokens::transfer_with_fee` passes attacker-chosen `amount` and `fee` into `WithdrawAsset(vec![asset, fee.clone()].into())`, triggering the overflow.
- missing_control: No sanity check in `orml/xtokens` that `assets.value + fee.value` does not overflow before calling `WithdrawAsset(vec![asset, fee.clone()].into())`
- interaction_scope: cross_chain
- contract_set: polkadot xcm v1 multiasset.rs, orml/xtokens pallet, Acala runtime
- entry_surface: Extrinsic `XTokens::transfer_with_fee { currency_id, amount, fee, dest, dest_weight }`
- trigger_primitive: Submitting `transfer_with_fee` with `amount` and `fee` whose sum overflows (e.g. amount 340282346643790096696078969353342681088, fee 1334440575053054371986284328509243391)
- preconditions: internal — Acala runtime at v0.9.13 (patch 676c4dab0769c82ebf6ff68fbab8870c29cafcb6 not yet released); external — attacker can submit any signed extrinsic
- sink: Asset value accounting wraps around — the sum of transferred asset values is not preserved
- impact: Crashes any node compiled in debug mode or with overflow checks enabled (node availability / DoS); on nodes built without overflow checks the asset value is underestimated, causing loss of asset tokens for the recipient
- code: |
    Call::XTokens(Call::transfer_with_fee { currency_id:
    CurrencyId::Token(TokenSymbol::KAR), amount:
    340282346643790096696078969353342681088, fee:
    1334440575053054371986284328509243391, dest: V1(MultiLocation { parents: 1,
    interior: X1(AccountId32 { network: Named([1, 1, 1, 142, 175, 4, 175, 175, 175, 175,
    175, 212, 0, 0, 0, 0, 0, 0, 0, 48, 20, 26, 189, 4, 169, 159, 214, 130, 44, 133, 88, 133, 76,
    205, 227, 154, 86, 132, 231, 165, 109, 162, 125, 0, 1, 0, 50, 50, 50, 49, 49, 49, 141, 18,
    63, 60, 33, 1, 0, 0, 0, 0, 1, 1]), id: [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 31,
    175, 175, 175, 175, 175, 175, 175, 175, 175, 175, 175, 175] }) }), dest_weight:
    12659530246663417775 })
- code_keywords: transfer_with_fee, MultiAsset, MultiAssets, multiasset.rs, WithdrawAsset, xtokens, CurrencyId::Token, TokenSymbol, MultiLocation, dest_weight, xcm::v1

### F: AURA collator selection opens up the possibility for DoS issue
- severity: moderate
- component: AURA block authorship / collator selection on Acala and Karura parachains (collator-selection module)
- root_cause: AURA makes the next block author completely predictable well in advance and provides no redundancy — only one collator is eligible per slot, with no fallback author if it fails.
- missing_control: No unpredictable leader election (e.g. Sassafras) and no redundancy/fallback author per slot
- interaction_scope: cross_protocol
- contract_set: collator-selection module, AURA consensus, parachain block production
- entry_surface: Network layer — targeted DoS against the collator node scheduled for the next slot
- trigger_primitive: Rolling denial of service that constantly switches targets to the next predictable block authors
- preconditions: internal — AURA round-robin selection in use; external — attacker with even limited financial resources can DoS a limited number of collators
- sink: Block production liveness for the parachain
- impact: Massively reduced parachain throughput / denial of service for the whole Acala parachain, affecting business and reputation; risk formally accepted by Acala until Sassafras is production-ready
- code: |
    NO_CODE_IN_REPORT
- code_keywords: AURA, Aura, collator-selection, Sassafras, block author, slot, collator, parachain

### F: Weight calculation of EVM extrinsics underestimates computational complexity
- severity: moderate
- component: `evm/src/lib.rs` — `eth_call`, `call`, `scheduled_call`, `create`, `create2`, `create_network_contract`, `create_predeploy_contract`
- root_cause: Every EVM-wrapping extrinsic uses `T::GasToWeight::convert(*gas_limit)` as its whole weight, ignoring the additional Substrate work (database reads/writes, other method calls) performed alongside the EVM Runner call.
- missing_control: The benchmarked weight of the surrounding Substrate operations is not added to `T::GasToWeight::convert(*gas_limit)`
- interaction_scope: single_contract
- contract_set: Acala evm pallet (all modules), Substrate block weight accounting
- entry_surface: EVM extrinsics (`eth_call`, `call`, `scheduled_call`, `create`, `create2`, `create_network_contract`, `create_predeploy_contract`); some require root origin
- trigger_primitive: Crafting EVM calls that reach their `gas_limit` when executed, so real execution time exceeds the declared weight
- preconditions: internal — weight equals only the converted gas limit; external — attacker can submit EVM extrinsics (or an accidental underweighted root call)
- sink: Declared extrinsic weight < actual execution time — the block weight invariant is violated
- impact: Attacker composes a block-filling transaction list that does not exceed max block weight yet times out; validator misses its slot and block production halts; for parachains, exceeding the 6-second block production time can stall block inclusion to the relay chain
- code: |
    NO_CODE_IN_REPORT
- code_keywords: GasToWeight::convert, gas_limit, eth_call, scheduled_call, create2, create_network_contract, create_predeploy_contract, evm/src/lib.rs, weight, benchmark, block timeout

### F: Missing storage deposit in claim_account and claim_default_account extrinsics
- severity: moderate
- component: `evm-accounts` pallet — `claim_account`, `claim_default_account` extrinsics
- root_cause: Both extrinsics write account-claim data on-chain without requiring any deposit, and they are callable by any Substrate account.
- missing_control: No storage deposit charged upon claiming accounts (mitigated in practice only by a sufficiently high Existential Deposit)
- interaction_scope: single_contract
- contract_set: evm-accounts pallet, chain storage
- entry_surface: Extrinsics `claim_account`, `claim_default_account` — callable by any Substrate account
- trigger_primitive: Creating an arbitrary number of accounts and calling these extrinsics repeatedly
- preconditions: internal — no deposit requirement on the extrinsics; external — attacker funds many accounts
- sink: Unbounded on-chain storage growth (storage-deposit invariant absent)
- impact: Blockchain storage fills up, leading to an infeasible amount of storage required to run a node — node availability compromised
- code: |
    NO_CODE_IN_REPORT
- code_keywords: claim_account, claim_default_account, evm-accounts, storage deposit, Existential Deposit, ED

### F: Missing storage deposit in set_alternative_fee_swap_path
- severity: moderate
- component: `transaction-payment` pallet — `set_alternative_fee_swap_path` extrinsic, `AlternativeFeeSwapPath` storage
- root_cause: The extrinsic appends a caller-supplied `fee_swap_path` vector into `AlternativeFeeSwapPath` storage with no deposit, and the record is not removed when the account is reaped (dust accounts keep their entry forever).
- missing_control: No deposit required for calling the extrinsic and no storage cleanup after an account is reaped / drops below the existential deposit
- interaction_scope: single_contract
- contract_set: transaction-payment pallet, AlternativeFeeSwapPath storage, account reaping
- entry_surface: Extrinsic `set_alternative_fee_swap_path(fee_swap_path: Vec<...>)` — callable by any Substrate account
- trigger_primitive: Creating an arbitrary number of accounts and calling the extrinsic; attackers do not even need to lock up funds because the record survives dusting
- preconditions: internal — no deposit and no cleanup on reap; external — attacker can create many accounts
- sink: Permanent, deposit-free on-chain storage growth
- impact: Blockchain storage bloat leading to an infeasible amount of storage required to run a node
- code: |
    NO_CODE_IN_REPORT
- code_keywords: set_alternative_fee_swap_path, AlternativeFeeSwapPath, fee_swap_path, transaction-payment, existential deposit, dust account, reaped

### F: Static weight calculation underestimates weights in the stable-asset pallet
- severity: low
- component: `stable-asset` pallet — `mint`, `redeem_proportion`, `redeem_multi` extrinsics; `create_pool` asset-count limit
- root_cause: These extrinsics accept a `Vec<T::Balance>` parameter that is iterated, making their complexity O(n), but the assigned weight functions are constant-plus-db-reads/writes and do not scale with the vector length.
- missing_control: Weight functions are not a dynamic function of the `Vec<T::Balance>` argument length
- interaction_scope: single_contract
- contract_set: stable-asset pallet (mint, redeem_proportion, redeem_multi, create_pool), Substrate block weight accounting
- entry_surface: Extrinsics `mint`, `redeem_proportion`, `redeem_multi` with a maximum-length `Vec<T::Balance>`
- trigger_primitive: Calling these extrinsics with the maximum allowed array length
- preconditions: internal — currently bounded because `create_pool` limits pools to a maximum of 3 assets, but the limit may change; external — attacker submits max-length arrays
- sink: Declared weight < actual O(n) execution time
- impact: Underweighted extrinsics let attackers cause block timeouts; for parachains, exceeding a 6-second block production time could stall block inclusion to the relay chain
- code: |
    NO_CODE_IN_REPORT
- code_keywords: stable-asset, mint, redeem_proportion, redeem_multi, create_pool, Vec<T::Balance>, weight function, db reads, db writes, O(n)

---

## FILE: composable-halborn-byog.md
- classification: finding
- classification_reason: Body is a Halborn Substrate pallet security audit with a "FINDINGS & TECH DETAILS" section containing two risk-rated issues (HAL-01 LOW, HAL-02 INFORMATIONAL) with code locations, risk levels and remediation plans, plus a cargo-audit appendix.
- protocol: Composable Finance — BYO Gas pallet (`asset-tx-payment` in `frame/transaction-payment`, ComposableFi/substrate)
- auditor: Halborn
- date: Engagement September 26th, 2022 – October 4th, 2022; remediation plan 11/24/2022
- findings_count: 2

### F: (HAL-01) CONFIGURATION ORIGIN CAN BE USED TO SET A PAYMENT ASSET FOR AN ARBITRARILY CHOSEN USER
- severity: LOW
- component: `substrate/frame/transaction-payment/asset-tx-payment/src/lib.rs` — `set_payment_asset` extrinsic (PaymentAssets storage, T::Lock)
- root_cause: `set_payment_asset` only enforces `who == payer` when `T::ConfigurationOrigin::try_origin` fails; if the caller satisfies `ConfigurationOrigin` the `payer` argument is completely unchecked, so that origin can set the fee-payment asset for any account.
- missing_control: No restriction preventing the `ConfigurationOrigin` bypass of the `ensure!(who == payer, DispatchError::BadOrigin)` check
- interaction_scope: single_contract
- contract_set: asset-tx-payment pallet — PaymentAssets storage, T::Lock (hold/release), T::BalanceConverter, ConfigurationExistentialDeposit
- entry_surface: Extrinsic `set_payment_asset(origin, payer: T::AccountId, asset_id: Option<ChargeAssetIdOf<T>>)`
- trigger_primitive: A holder of the `ConfigurationOrigin` calls `set_payment_asset` with an arbitrary `payer`
- preconditions: internal — ConfigurationOrigin is not sufficiently decentralized; external — none
- sink: A user's transaction fee payment asset (and their locked existential deposit in that asset) is changed without their consent
- impact: Arbitrary users' payment assets can be set by the configuration origin; the victim's previous asset lock is released and a new ED is held in the attacker-chosen asset
- code: |
    184 #[ pallet :: weight ( T :: WeightInfo :: set _p ay me nt_ as se t () )]
    185 pub fn set _p ay me nt_ as se t (
    186 origin : OriginFor <T > ,
    187 payer : T :: AccountId ,
    188 asset_id : Option < ChargeAssetIdOf <T > > ,
    189 ) -> DispatchResult {
    190 // either configuration origin or owner of configuration
    191 if let Err ( origin ) = T :: C o n f i g u r a t i o n O r i g i n:: try_origin ( origin
    ë ) {
    192 let who = ensure_signed ( origin ) ?;
    193 ensure! ( who == payer , DispatchError :: BadOrigin ,)
    194 };
    195
    196 // clean previous configuration
    197 if let Some (( asset_id , ed ) ) = < PaymentAssets <T > >:: get (& payer )
    ë {
    198 T :: Lock :: release ( asset_id , & payer , ed , true ) ?;
    199 < PaymentAssets <T > >:: remove (& payer ) ;
    200 }
    201
    202 // configure new payment asset and hold some ed
    203 if let Some ( asset_id ) = asset_id {
    204 let ed = T :: BalanceC onverter :: to_asset_ balance (
    205 T :: C o n f i g u r a t i o n E x i s t e n t i a l D e p o s i t:: get () ,
    206 asset_id ,
    207 )
    208 . map_err (| _| DispatchError :: Other ( " Cannot convert ED to
    ë asset balance " ) ) ?;
    209 T :: Lock :: hold ( asset_id , & payer , ed ) ?;
    210 < PaymentAssets <T > >:: insert ( payer , ( asset_id , ed ) ) ;
    211 }
    212
    213 Ok (() )
    214 }
- code_keywords: set_payment_asset, ConfigurationOrigin, try_origin, ensure_signed, BadOrigin, PaymentAssets, ChargeAssetIdOf, T::Lock, hold, release, BalanceConverter, to_asset_balance, ConfigurationExistentialDeposit, EnsureRootOrHalfNativeCouncil, WeightInfo

### F: (HAL-02) PRESENCE OF TESTING CODE
- severity: INFORMATIONAL
- component: `substrate/frame/transaction-payment/asset-tx-payment/src/lib.rs` — `ChargeAssetTxPayment::from` and `get_payment_asset`
- root_cause: The `from` constructor, which exists for testing and allows `self.asset_id` to be set manually, is compiled into production builds; `get_payment_asset` returns `self.asset_id` directly when it is `Some`, bypassing the `UseUserConfiguration` flag and the `PaymentAssets` storage lookup.
- missing_control: No `#[cfg(test)]` gating on the testing-only `from` function
- interaction_scope: single_contract
- contract_set: asset-tx-payment pallet — ChargeAssetTxPayment SignedExtension (validate, pre_dispatch), PaymentAssets storage, UseUserConfiguration
- entry_surface: SignedExtension fee calculation path (`validate` / `pre_dispatch`) via `get_payment_asset`
- trigger_primitive: Construction of a `ChargeAssetTxPayment` with a manually set `asset_id` in a production build
- preconditions: internal — `from` present in the production binary; external — none
- sink: The configured fee-payment asset resolution logic is short-circuited
- impact: Test-only code path present in the production environment affecting fee asset selection
- code: |
    240 pub fn from ( tip : BalanceOf <T > , asset_id : Option < ChargeAssetIdOf <T
    ë > >) -> Self {
    241 Self { tip , asset_id }
    242 }

    284 fn get _p ay me nt_ as se t (& self , who : & T :: AccountId , call : & T :: Call ) ->
    ë Option < ChargeAssetIdOf <T > > {
    285 if self . asset_id . is_some () || ! <T as Config >::
    ë U s e U s e r C o n f i g u r a t i o n:: get () {
    286 return self . asset_id
    287 }
    288
    289 let call = < T as Config >:: PayableCall :: from_ref ( call ) ;
    290 match call . is_sub_type () {
    291 Some ( Call :: set _p ay me nt_ as se t { asset_id , .. }) = > asset_id
    ë . to_owned () ,
    292 _ = > < PaymentAssets <T > >:: get ( who ) .map (| x | x .0) ,
    293 }
    294 }
- code_keywords: ChargeAssetTxPayment, from, get_payment_asset, asset_id, UseUserConfiguration, PayableCall, from_ref, is_sub_type, PaymentAssets, validate, pre_dispatch, cfg(test)
