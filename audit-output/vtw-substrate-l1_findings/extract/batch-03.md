# VTW Extract — batch-03 (substrate-l1_findings)

## FILE: phala-c4-2401.md
- classification: finding
- classification_reason: Body is a Code4rena "Findings & Analysis Report" with 4 numbered Medium-risk findings (M-01..M-04) each carrying description, PoC, mitigation and judge/sponsor severity debate, plus 7 Low/Non-Critical issues.
- protocol: Phat Contract Runtime (Pink Runtime / Phala Network)
- auditor: Code4rena (judged by Lambda; findings by 0xTheC0der, DadeKuma, zhaojie, Koolex, Cryptor et al.)
- date: Audit March 1 — March 22, 2024; report dated 2024-04-11
- findings_count: 11

### F: [M-01] Limited availability of balance_of(...) method
- severity: Medium
- component: pink runtime chain extension — `PinkExtBackend::balance_of` / `ensure_system` (crates/pink/runtime/src/runtime/extension.rs)
- root_cause: The `balance_of(...)` chain-extension method is gated behind `self.ensure_system()?`, restricting it to the system contract, while both the online and in-line documentation state availability should be "any contract" — an implementation/spec mismatch on an access-control guard.
- missing_control: The `ensure_system` origin check should not be present on `balance_of`; there is no availability check matching the documented "any contract" contract-level permission.
- interaction_scope: single_contract
- contract_set: pink runtime chain extension (`extension.rs`), `PalletPink` (system_contract storage), `crate::runtime::Balances`
- entry_surface: ink! chain-extension call from a user contract (chain_extension intrinsic, extension ID 0) into `balance_of`
- trigger_primitive: Any non-system user contract invoking `balance_of` — the call is rejected with `DispatchError::BadOrigin`
- preconditions: internal — caller contract address != `PalletPink::system_contract()`
- sink: Documented chain-extension availability invariant violated: a method documented as callable by any contract is callable only by the system contract
- impact: User contracts relying on `balance_of` inevitably fail with `BadOrigin`; broken functionality / DoS of dependent contracts
- code: |
    fnbalance_of(
        &self,
        account: ext::AccountId,
    ) -> Result<(pink::Balance, pink::Balance), Self::Error> {
    self.ensure_system()?;    // @audit Availability should be 'any contra
    let account: AccountId32 = account.convert_to();
    let total = crate::runtime::Balances::total_balance(&account);
    let free = crate::runtime::Balances::free_balance(&account);
        Ok((total, free))
    }
    fnensure_system(&self) -> Result<(), DispatchError> {
    let contract: AccountId32 = self.address.convert_to();
    if Some(contract) != PalletPink::system_contract() {
    return Err(DispatchError::BadOrigin);
        }
        Ok(())
    }
- code_keywords: balance_of, ensure_system, DispatchError::BadOrigin, PalletPink::system_contract, Balances::total_balance, Balances::free_balance, AccountId32, convert_to, import_latest_system_code, direct_balance_of

### F: [M-02] An attacker can bloat the Pink runtime storage with zero costs
- severity: Medium
- component: pink runtime configuration — `ExistentialDeposit` parameter in `crates/pink/runtime/src/runtime.rs` (pallet_balances Config)
- root_cause: The Substrate Existential Deposit for the Pink runtime is set to `1` unit of a `u128` Balance where 1 PHA = 1_000_000_000_000, so the anti-dust threshold is effectively zero-cost and cannot reap dust accounts meaningfully.
- missing_control: A economically meaningful `ExistentialDeposit` (e.g. `1 * CENTS` = 1_000_000_000) that makes account creation costly enough to prevent dust-account storage bloat
- interaction_scope: single_contract
- contract_set: pink runtime (`runtime.rs` parameter_types), `pallet_balances`, `types.rs` Balance alias
- entry_surface: Balance transfer / account creation path (deposit into new accounts); anyone able to move balance
- trigger_primitive: Attacker splits a tiny amount of PHA across an unbounded number of dust accounts, each above the ED of 1 unit
- preconditions: external — attacker holds a trivial amount of PHA (report computes ~$0.20 for 1 trillion accounts)
- sink: State-bloat / storage-growth bound invariant: number of live accounts must be bounded by economic cost of the existential deposit
- impact: Unbounded storage state growth at near-zero attacker cost; increased storage and fee overhead borne by all users; potential fill-all-storage DoS
- code: |
    pubconst ExistentialDeposit: Balance = 1;

    pubtypeBalance = u128;

    pubconst PHAS: Balance = 1_000_000_000_000;
    pubconst DOLLARS: Balance = PHAS;
    pubconst CENTS: Balance = DOLLARS / 100;
    pubconst MILLICENTS: Balance = CENTS / 1_000;

    -    pub const ExistentialDeposit: Balance = 1;
    +    pub const ExistentialDeposit: Balance = 1 * CENTS;
- code_keywords: ExistentialDeposit, Balance, u128, PHAS, DOLLARS, CENTS, MILLICENTS, pallet_balances, parameter_types, runtime.rs, types.rs

### F: [M-03] A cache that times out can be recovered
- severity: Medium
- component: pink chain-extension local cache — `LocalCache::set_expire` / `maybe_clear_expired` / `get` (crates/pink/chain-extension/src/local_cache.rs), exposed via `cache_set_expiration` / `set_expiration`
- root_cause: `set_expire` calls `maybe_clear_expired` (which only garbage-collects every `gc_interval` sets) and then re-writes `expire_at` on an entry without first checking whether that entry has already expired — so an already-expired key can be resurrected with a fresh expiry.
- missing_control: An expiry check on the target key inside `set_expire` (or an unconditional `clear_expired()` instead of `maybe_clear_expired()`) before updating `expire_at`
- interaction_scope: single_contract
- contract_set: `LocalCache` / `Storage` in pink chain-extension, `set_expiration` wrapper, `with_global_cache`
- entry_surface: Contract-facing chain-extension ocall `cache_set_expiration` → `set_expiration(contract, key, expiration)` → `LocalCache::set_expire`
- trigger_primitive: Attacker (or malicious contract) calls `set_expire` on a key that has already passed `expire_at` but has not yet been GC'd, resetting `expire_at = now() + expire`
- preconditions: internal — the key's `expire_at <= now()` and `sets_since_last_gc != gc_interval` so `clear_expired` has not run
- sink: Cache expiry invariant violated: `get` must return `None` for any key whose `expire_at <= now()`, and an expired key must never become live again
- impact: Inconsistent cached state between `get` (reports gone) and `set_expire` (restores it); attacker can make a value appear/disappear or live indefinitely — e.g. two different cached prices enabling price manipulation on cached API/oracle responses; judge accepted Medium (downgraded from High)
- code: |
    pubfnset_expire(&mutself, id: Cow<[u8]>, key: Cow<[
    //@audit key values that have timed out may not be deleted
    self.maybe_clear_expired();
    if expire == 0 {
    let _ = self.remove(id.as_ref(), key.as_ref());
            } elseiflet Some(v) = self
                .storages
                .get_mut(id.as_ref())
                .and_then(|storage| storage.kvs.get_mut(key.as_ref
            {
    //@audit You can increase the timeout period of a key value th
                v.expire_at = now().saturating_add(expire)
            }
        }
    fnmaybe_clear_expired(&mutself) {
    self.sets_since_last_gc += 1;
    @>      ifself.sets_since_last_gc == self.gc_interval {
    self.clear_expired();
            }
        }

    pubfnget(&self, id: &[u8], key: &[u8]) -> Option<Vec
    let entry = self.storages.get(id)?.kvs.get(key)?;
    @>      if entry.expire_at <= now() {
                None
            } else {
                Some(entry.value.to_owned())
            }
        }

    pubfnset_expiration(contract: &[u8], key: &[u8], expiration:
    with_global_cache(|cache| cache.set_expire(contract.into
    }
- code_keywords: LocalCache, set_expire, set_expiration, cache_set_expiration, maybe_clear_expired, clear_expired, sets_since_last_gc, gc_interval, expire_at, with_global_cache, storages, kvs, saturating_add

### F: [M-04] An attacker can crash the cluster system by sending an HTTP request with a huge timeout
- severity: Medium
- component: pink chain-extension — `batch_http_request` (crates/pink/chain-extension/src/lib.rs)
- root_cause: `Duration::from_millis(timeout_ms + 200)` uses unchecked `+` on a caller-supplied `u64`; in Rust this overflows and panics when `timeout_ms > u64::MAX - 200`.
- missing_control: Saturating/checked arithmetic (`timeout_ms.saturating_add(200)`) or an upper bound validation on the caller-supplied `timeout_ms`
- interaction_scope: single_contract
- contract_set: pink chain-extension `lib.rs` (`batch_http_request`, `async_http_request`, `block_on`), worker OCalls
- entry_surface: Contract-initiated chain-extension call `batch_http_request(requests, timeout_ms)` from a Phat contract
- trigger_primitive: Any user submits a batch HTTP request with `timeout_ms` greater than `u64::MAX - 200` (PoC uses `u64::MAX`)
- preconditions: external — a worker that forwards the raw timeout without clamping (the sponsor notes the current worker OCall clamps against MAXQUERYTIME, which is why severity was reduced from High to Medium)
- sink: Liveness invariant: no user-supplied input may panic the worker/runtime; arithmetic must never overflow on attacker-controlled values
- impact: Worker panics ("attempt to add with overflow"); repeating the request across workers results in DoS of the whole cluster system at zero cost to the attacker
- code: |
    pubfnbatch_http_request(requests: Vec<HttpRequest>, timeout_ms:
    const MAX_CONCURRENT_REQUESTS: usize = 5;
    if requests.len() > MAX_CONCURRENT_REQUESTS {
    return Err(ext::HttpRequestError::TooManyRequests);
            }
    block_on(asyncmove {
    let futs = requests
                    .into_iter()
                    .map(|request| async_http_request(request, timeout_ms));
                tokio::time::timeout(
    @>              Duration::from_millis(timeout_ms + 200),
                    futures::future::join_all(futs),
                )
                .await
            })
            .or(Err(ext::HttpRequestError::Timeout))
        }

        tokio::time::timeout(
    -        Duration::from_millis(timeout_ms + 200),
    +        Duration::from_millis(timeout_ms.saturating_add(200)),
             futures::future::join_all(futs),
        )
- code_keywords: batch_http_request, timeout_ms, Duration::from_millis, saturating_add, MAX_CONCURRENT_REQUESTS, async_http_request, tokio::time::timeout, block_on, HttpRequestError::Timeout, MAXQUERYTIME, http_timeout_panics

### F: [05] Masking deposit calculation can lead to unexpected results in certain circumstances
- severity: Low
- component: pink runtime — `mask_deposit` / `mask_low_bits128` / `coarse_grained` in `crates/pink/runtime/src/contract.rs` (referenced at runtime/extension.rs#L439-L441 region)
- root_cause: The bit-masking used to coarse-grain storage deposits (a side-channel mitigation) does not preserve the intended property `masked_deposit >= deposit` for all `deposit_per_byte` values; a specific large `deposit_per_byte` breaks the invariant.
- missing_control: A bound/validation on `deposit_per_byte` (set by the cluster creator) and/or an explicit post-condition asserting `masked_deposit >= deposit`
- interaction_scope: single_contract
- contract_set: `contract.rs` (`mask_deposit`, `mask_gas`, `mask_low_bits64`, `mask_low_bits128`, `coarse_grained`), `pallet_pink` (`DepositPerByte`)
- entry_surface: Admin/cluster-creator path setting `deposit_per_byte`, consumed on every contract query/estimation result masking
- trigger_primitive: Cluster creator sets `deposit_per_byte = 664613997892457936451903530140172289`
- preconditions: internal — malicious or careless cluster creator controlling `deposit_per_byte`
- sink: Masking invariant `masked_deposit >= deposit` (Property 1 in the fuzz test) is violated
- impact: Opens the side-channel attack that the coarse-graining function is designed to prevent; sponsor counters that such a `deposit_per_byte` would make the cluster unusable
- code: |
    #[test]
    fn test_mask_deposit_properties(deposit in 1u128..=u128::MAX, deposit_per_
        let masked_deposit = mask_deposit(deposit, deposit_per_byte);
        // Property 1: Masked deposit should be greater than or equal to the o
        prop_assert!(masked_deposit >= deposit);
    }
- code_keywords: mask_deposit, mask_gas, mask_low_bits64, mask_low_bits128, coarse_grained, deposit_per_byte, DepositPerByte, prop_assert, ContractResult

### F: [06] is_in_transaction return value can be misleading
- severity: Low
- component: pink runtime chain extension — `is_in_transaction` / `ExecutionMode` (crates/pink/runtime/src/runtime/extension.rs#L439-L441, crates/pink/capi/src/types.rs)
- root_cause: `is_in_transaction` treats `ExecutionMode::Estimating` identically to `ExecutionMode::Transaction`, so a call in estimating mode reports `true` when it should report `false`; there is no separate accessor for estimating mode.
- missing_control: A distinct mode predicate (e.g. `is_in_estimating`) so contracts can distinguish Query / Estimating / Transaction rather than conflating Estimating with Transaction
- interaction_scope: single_contract
- contract_set: `extension.rs`, `capi/src/types.rs` (`ExecutionMode`, `deterministic_required`)
- entry_surface: Chain-extension call `is_in_transaction` from a Phat contract; gas/deposit estimation path
- trigger_primitive: Invoking a contract in Estimating mode and branching on `is_in_transaction`
- preconditions: internal — contract logic branches on `is_in_transaction`
- sink: Execution-mode reporting invariant: the mode predicate exposed to contracts must match the actual `ExecutionMode`
- impact: Contracts take transaction-mode code paths during estimation, producing misleading behavior/results; confirmed by the sponsor as "on the plan"
- code: |
    pubenumExecutionMode {
    /// In this mode, the runtime is executing an RPC query. Any state changes are
    /// after execution. Indeterministic operations like HTTP requests are allowed
     Query,
    /// In this mode, the runtime is simulating a transaction but state changes are
     #[default]
     Estimating,
    /// In this mode, the runtime is executing a real transaction. State changes wi
    /// Indeterministic operations like HTTP requests aren't allowed in this mode.
     Transaction,
     }

    pubfndeterministic_required(&self) -> bool {
    matchself {
                ExecutionMode::Query => false,
                ExecutionMode::Estimating => true,
                ExecutionMode::Transaction => true,
          }
       }
- code_keywords: is_in_transaction, ExecutionMode, Query, Estimating, Transaction, deterministic_required, CallInCommand, CallInQuery, exec_context

### F: [07] No code size limit check in function put_sidevm_code
- severity: Non-Critical
- component: `pallet_pink` — `put_sidevm_code` / `upload_sidevm_code` (crates/pink/runtime/src/runtime/pallet_pink.rs#L134-L146, capi/ecall_impl.rs)
- root_cause: `put_sidevm_code` stores caller-supplied SideVM WASM code into the `SidevmCodes` storage map without checking the code length, unlike the ink! `upload_code` path which enforces `MaxCodeLen` / `estimate_wasmi_memory_cost`.
- missing_control: A maximum code-size / length check inside `put_sidevm_code` before writing to storage
- interaction_scope: single_contract
- contract_set: `pallet_pink` (`SidevmCodes`, `put_sidevm_code`), `ecall_impl.rs` (`upload_sidevm_code`), `runtime.rs` (`MaxCodeLen`)
- entry_surface: ECall `upload_sidevm_code(account, code)` → `PalletPink::put_sidevm_code`
- trigger_primitive: Uploading an arbitrarily large SideVM code blob
- preconditions: internal — sponsor notes there is already an on-chain limit check outside this function
- sink: Bounded-storage-write invariant: all caller-supplied blobs written to runtime storage must be length-bounded at the point of write
- impact: Unbounded storage write / state bloat if the external on-chain limit is ever bypassed or removed; sponsor confirmed "might be good to have"
- code: |
    NO_CODE_IN_REPORT
- code_keywords: put_sidevm_code, upload_sidevm_code, SidevmCodes, MaxCodeLen, Twox64Concat, WasmCode, pallet_pink, estimate_wasmi_memory_cost, DecompressedCodeTooLarge

---

## FILE: chainflip-backend-audits-chainflip-backend-zellic-audit-report-pdf.md
- classification: finding
- classification_reason: Body contains a "3. Detailed Findings" section with three individually-rated findings (Target / Category / Severity / Likelihood / Impact blocks) plus remediation commits, followed by a Discussion and a per-pallet Threat Model.
- protocol: Chainflip Backend (Chainflip Labs) — state-chain Substrate pallets cf-lp, cf-pools, cf-swapping, cf-witnesser + off-chain Engine
- auditor: Zellic
- date: Report December 8, 2023; review period November 6 — December 8, 2023
- findings_count: 3

### F: Witnesser rotation may queue call multiple times
- severity: High
- component: `cf-witnesser` pallet — `witness_at_epoch`, `on_idle`, `force_witness`, `dispatch_call`
- root_cause: Replay protection (the `CallHashExecuted` check) is enforced in `witness_at_epoch` but not in the `on_idle` dispatch path that drains `WitnessedCallsScheduledForDispatch`, so a call queued while SafeMode was paused can be dispatched more than once.
- missing_control: A `CallHashExecuted` "already dispatched" check inside `on_idle` before dispatching queued calls (mirroring the check in `witness_at_epoch`)
- interaction_scope: multi_contract
- contract_set: `cf-witnesser` pallet, SafeMode pallet, `Votes` / `CallHashExecuted` / `WitnessedCallsScheduledForDispatch` storage, downstream dispatched calls
- entry_surface: `witness_at_epoch` extrinsic (validator witnessers), `on_idle` block hook, `force_witness` root extrinsic
- trigger_primitive: (1) Safe mode enabled while a witnesser rotation is imminent — the same event is witnessed by two different majority sets in two different epochs and pushed to the queue twice; (2) root calls `force_witness` on a call that is already scheduled, bypassing replay protections
- preconditions: internal — SafeMode paused the witnesser; epoch rotation in flight; or root origin invoking `force_witness`
- sink: Exactly-once witnessing invariant: "the state chain is guaranteed to witness every event exactly once" — a scheduled call must never be dispatched twice
- impact: The same call is dispatched twice, duplicating the effects of an external-chain event (e.g. duplicated deposit crediting); unintended replay of scheduled calls
- code: |
    NO_CODE_IN_REPORT
- code_keywords: cf-witnesser, witness_at_epoch, on_idle, force_witness, dispatch_call, WitnessedCallsScheduledForDispatch, CallHashExecuted, Votes, epoch_index, SafeMode, authority_index, UnauthorisedWitness, InvalidEpoch

### F: Seized funds are locked in the protocol
- severity: Medium
- component: `cf-swapping` pallet — `schedule_swap_from_contract`, `ccm_deposit` / `on_ccm_deposit` / `principal_and_gas_amounts`, `CollectedRejectedFunds`, `MinimumSwapAmount`
- root_cause: Deposits failing validation (below `MinimumSwapAmount`, non-Ethereum CCM destination, deposit below gas budget) are confiscated into `CollectedRejectedFunds` with no refund path; non-native ERC-20 seizures are then permanently stuck in the vault contract.
- missing_control: A refund/retrieval mechanism for seized funds (with the seized user paying the retrieval gas to avoid DoS); no atomic commit binding a deposit to the configuration it was made under
- interaction_scope: cross_chain
- contract_set: `cf-swapping` pallet, `cf-ingress-egress` pallet (egress handler), Ethereum Vault contract, governance (`set_minimum_swap_amount`)
- entry_surface: Deposit to a swap/CCM deposit channel on an external chain, witnessed into `schedule_swap_from_channel` / `schedule_swap_from_contract` / `ccm_deposit`
- trigger_primitive: A user deposits an amount below `MinimumSwapAmount`, or a CCM whose destination chain is not Ethereum, or a CCM whose deposit is below the gas budget; also governance changing `MinimumSwapAmount` between a user's signed Ethereum tx and its on-chain recording
- preconditions: external — user or integrator bypasses the dApp front-end, or a governance parameter change races the user's in-flight deposit
- sink: User fund conservation: user assets must be refundable or usable; seized ERC-20 balances are permanently unretrievable
- impact: Permanent user fund loss; potentially large amounts when the CCM destination chain is misconfigured; only native-coin seizures are reusable (as gas in the vault contract)
- code: |
    if amount < MinimumSwapAmount::<T>::get(from) {
    // If the swap amount is less than the minimum required,
    // confiscate the fund and emit an event
    CollectedRejectedFunds::<T>::mutate(from, |fund| {
    *fund = fund.saturating_add(amount)
    });

    let gas_budget = channel_metadata.gas_budget;
    let principal_swap_amount = deposit_amount.saturating_sub(gas_budget);
    if ForeignChain::Ethereum != destination_asset.into() {
    return Err(CcmFailReason::UnsupportedForTargetChain)
    } else if deposit_amount < gas_budget {
    return Err(CcmFailReason::InsufficientDepositAmount)
    } else if source_asset != destination_asset &&
    !principal_swap_amount.is_zero() &&
    principal_swap_amount < MinimumSwapAmount::<T>::get(source_asset)
    {
    // If the CCM's principal requires a swap and is non-zero,
    // then the principal swap amount must be above minimum swap amount
    required.
    return Err(CcmFailReason::PrincipalSwapAmountTooLow)
    }
- code_keywords: cf-swapping, CollectedRejectedFunds, MinimumSwapAmount, set_minimum_swap_amount, schedule_swap_from_channel, schedule_swap_from_contract, ccm_deposit, on_ccm_deposit, principal_and_gas_amounts, CcmFailReason, UnsupportedForTargetChain, InsufficientDepositAmount, PrincipalSwapAmountTooLow, ForeignChain::Ethereum, gas_budget, cf-ingress-egress

### F: Broker fees are not taken from swap amount
- severity: Critical
- component: `cf-swapping` pallet — `schedule_swap_from_channel`, `EarnedBrokerFees`, `schedule_swap_with_check`
- root_cause: The broker commission is computed from `amount` and accrued into `EarnedBrokerFees`, but it is never subtracted from `amount` before the swap is scheduled — the same value is both paid out as fee and swapped for the user.
- missing_control: Subtracting `fee` from `amount` before calling `schedule_swap_with_check`; also no cap on `broker_commission_bps` below 100%
- interaction_scope: multi_contract
- contract_set: `cf-swapping` pallet, `EarnedBrokerFees` storage, broker registration (`register_as_broker`), `withdraw` (broker fee egress), liquidity pools
- entry_surface: `request_swap_deposit_address` by a self-registered broker, then a deposit into that channel triggering `schedule_swap_from_channel`; fees claimed via the broker `withdraw` extrinsic
- trigger_primitive: Any user registers as a broker, sets `broker_commission_bps` to 100%, then performs repeated no-op swaps (e.g. X USDC → X USDC) through their own deposit channel
- preconditions: internal — broker registration is permissionless and fee choice is unconstrained (only `Permill` caps it at 100%)
- sink: Value conservation invariant: swap output + accrued broker fees must never exceed the deposited amount
- impact: Attacker receives 2X for an X deposit (X from the regular swap egress plus X from the 100% broker commission); repeated no-op swaps drain all protocol liquidity — total protocol insolvency
- code: |
    fn schedule_swap_from_channel(
    deposit_address: ForeignChainAddress,
    deposit_block_height: u64,
    from: Asset,
    to: Asset,
    amount: AssetAmount,
    destination_address: ForeignChainAddress,
    broker_id: Self::AccountId,
    broker_commission_bps: BasisPoints,
    channel_id: ChannelId,
    ) {
    let fee = Permill::from_parts(broker_commission_bps as u32
    * BASIS_POINTS_PER_MILLION) *
    amount;
    EarnedBrokerFees::<T>::mutate(&broker_id, from, |earned_fees| {
    earned_fees.saturating_accrue(fee)
    });
    let encoded_destination_address =
    T::AddressConverter::to_encoded_address(destination_address.clone());
    let swap_origin = SwapOrigin::DepositChannel {
    deposit_address:
    T::AddressConverter::to_encoded_address(deposit_address),
    channel_id,
    deposit_block_height,
    };
    if let Some(swap_id) = Self::schedule_swap_with_check(
    from,
    to,
    amount,
    destination_address.clone(),
    &swap_origin,
    ) {
- code_keywords: schedule_swap_from_channel, EarnedBrokerFees, broker_commission_bps, BASIS_POINTS_PER_MILLION, Permill::from_parts, saturating_accrue, schedule_swap_with_check, SwapOrigin::DepositChannel, register_as_broker, request_swap_deposit_address, AddressConverter, cf-swapping

---

## FILE: publications-audit-reports-peckshield-audit-report-zenlink-v1-0-pdf.md
- classification: finding
- classification_reason: Body is a PeckShield audit with a Key Findings table (PVE-001..PVE-004) and a Detailed Results section giving per-issue ID/Severity/Likelihood/Impact/Target/CWE plus code listings and resolution status.
- protocol: Zenlink Hybrid AMM (Zenlink — Polkadot/Substrate cross-chain DEX; audited target is the EVM/Solidity implementation: StableSwapRouter.sol, SwapRouterV1.sol, StableSwapStorage.sol, StableSwap.sol)
- auditor: PeckShield (Audit Report #2022-195)
- date: May 19, 2022 (Final Release; RC1 May 12, 2022)
- findings_count: 4

### F: Trust Issue of Admin Keys
- severity: Medium
- component: Multiple Contracts — `StableSwap` privileged setters `setFee`, `rampA` (`onlyAdmin` modifier)
- root_cause: A single privileged `admin` account governs protocol-wide parameters (swap/admin fee, amplification coefficient A ramping) and can control or govern the flow of assets managed by the protocol, creating counter-party risk for users.
- missing_control: Decentralized governance (DAO/timelock) over the admin role; explicit disclosure of privileges. Mitigated by moving `admin` to a multi-sig.
- interaction_scope: multi_contract
- contract_set: StableSwap, StableSwapStorage, StableSwapRouter, SwapRouterV1
- entry_surface: Admin path — `setFee(newSwapFee, newAdminFee)` and `rampA(futureA, futureATime)` external functions guarded by `onlyAdmin`
- trigger_primitive: Compromised or malicious admin key invoking privileged parameter setters
- preconditions: internal — attacker controls (or admin misuses) the `admin` account
- sink: Trust-minimization invariant: no single account should be able to unilaterally change fee and curve parameters that govern user asset flows
- impact: Protocol-wide parameter manipulation and counter-party risk to contract users; status: Mitigated via multi-sig admin
- code: |
    74 fu nc ti on setFee ( uint256 newSwapFee , uint256 n e w A d m i n F e e ) ex ter na l o n l y A d m i n {
    75 require ( n e w S w a p F e e <= MAX_SWAP_FEE , " > m a x S w a p F e e " ) ;
    76 require ( n e w A d m i n F e e <= MAX_ADMIN_FEE , " > m a x A d m i n F e e " ) ;
    77 s w a p S t o r a g e . ad mi nF ee = n e w A d m i n F e e ;
    78 s w a p S t o r a g e . fee = n e w S w a p F e e ;
    79 emit NewFee ( newSwapFee , n e w A d m i n F e e ) ;
    80 }
    89 fu nc ti on rampA ( uint256 futureA , uint256 f u t u r e A T i m e ) ex ter na l o n l y A d m i n {
    90 require ( block . t i m e s t a m p >= s w a p S t o r a g e . i n i t i a l A T i m e + (1 days ) , " < r a m p D e l a y " ) ;
    91 require ( f u t u r e A T i m e >= block . t i m e s t a m p + ( M I N _ R A M P _ T I M E ) , " < m i n R a m p T i m e " ) ;
    92 require (0 < futureA && futureA < MAX_A , " o u t O f R a n g e " ) ;
    94 uint256 i n i t i a l A P r e c i s e = s w a p S t o r a g e . g e t A P r e c i s e () ;
    95 uint256 f u t u r e A P r e c i s e = futureA * S t a b l e S w a p S t o r a g e . A _ P R E C I S I O N ;
    97 if ( f u t u r e A P r e c i s e < i n i t i a l A P r e c i s e ) {
    98 require ( f u t u r e A P r e c i s e * ( M A X _ A _ C H A N G E ) >= initialAPrecise , " > m a x C h a n g e " ) ;
    99 } else {
    100 require ( f u t u r e A P r e c i s e <= i n i t i a l A P r e c i s e * ( M A X _ A _ C H A N G E ) , " > m a x C h a n g e " ) ;
    101 }
    103 s w a p S t o r a g e . in it ia lA = i n i t i a l A P r e c i s e ;
    104 s w a p S t o r a g e . futureA = f u t u r e A P r e c i s e ;
    105 s w a p S t o r a g e . i n i t i a l A T i m e = block . t i m e s t a m p ;
    106 s w a p S t o r a g e . f u t u r e A T i m e = f u t u r e A T i m e ;
    108 emit RampA ( initialAPrecise , futureAPrecise , block . timestamp , f u t u r e A T i m e ) ;
    109 }
- code_keywords: onlyAdmin, setFee, rampA, MAX_SWAP_FEE, MAX_ADMIN_FEE, adminFee, MIN_RAMP_TIME, MAX_A, MAX_A_CHANGE, A_PRECISION, initialATime, futureATime, getAPrecise, swapStorage

### F: Implicit Assumption Enforcement In AddLiquidity()
- severity: Low
- component: Router — `addLiquidity()` / `_addLiquidity()` (SwapRouterV1 / Router)
- root_cause: `_addLiquidity()` performs asymmetric checks on the desired/min amount pairs, so the implicit conditions `amount0Desired >= amount0Min` and `amount1Desired >= amount1Min` are never enforced and can silently hold false without reverting.
- missing_control: Explicit `require(amount0Desired >= amount0Min)` and `require(amount1Desired >= amount1Min)` in `addLiquidity()`
- interaction_scope: multi_contract
- contract_set: Router (`addLiquidity`, `_addLiquidity`), Factory (`getPair`, `createPair`), Pair (`mint`), Helper (`quote`, `getReserves`, `safeTransferFrom`)
- entry_surface: Public `addLiquidity(token0, token1, amount0Desired, amount1Desired, amount0Min, amount1Min, to, deadline)`
- trigger_primitive: Caller supplies `amountXMin > amountXDesired`; the asymmetric branch skips the slippage assertion
- preconditions: internal — pool reserves non-zero so the `quote` branch is taken
- sink: Slippage-protection invariant: the min-amount parameters must constrain every liquidity-add path
- impact: Slippage control for some Router trades may not be checked at all in certain scenarios; confirmed, planned fix in next release
- code: |
    217 ) private returns ( uint256 amount0 , uint256 amount1 ) {
    218 if ( IF ac tor y ( factory ) . getPair ( token0 , token1 ) == address (0) ) {
    219 IF ac to ry ( factory ) . c r e a t e P a i r ( token0 , token1 ) ;
    220 }
    221 ( uint256 reserve0 , uint256 r es er ve1 ) = Helper . g e t R e s e r v e s (
    222 factory ,
    223 token0 ,
    224 token1
    225 ) ;
    226 if ( re se rve 0 == 0 && r es er ve 1 == 0) {
    227 ( amount0 , amount1 ) = ( amount0Desired , a m o u n t 1 D e s i r e d ) ;
    228 } else {
    229 uint256 a m o u n t 1 O p t i m a l = Helper . quote (
    230 amount0Desired ,
    231 reserve0 ,
    232 re se rv e1
    233 ) ;
    234 if ( a m o u n t 1 O p t i m a l <= a m o u n t 1 D e s i r e d ) {
    235 require (
    236 a m o u n t 1 O p t i m a l >= amount1Min ,
    237 " Router : I N S U F F I C I E N T _ 1 _ A M O U N T "
    238 ) ;
    239 ( amount0 , amount1 ) = ( amount0Desired , a m o u n t 1 O p t i m a l ) ;
    240 } else {
    241 uint256 a m o u n t 0 O p t i m a l = Helper . quote (
    242 amount1Desired ,
    243 reserve1 ,
    244 re se rv e0
    245 ) ;
    246 require ( a m o u n t 0 O p t i m a l <= a m o u n t 0 D e s i r e d ) ;
    247 require (
    248 a m o u n t 0 O p t i m a l >= amount0Min ,
    249 " Router : I N S U F F I C I E N T _ 0 _ A M O U N T "
    250 ) ;
    251 ( amount0 , amount1 ) = ( amount0Optimal , a m o u n t 1 D e s i r e d ) ;
    252 }
    253 }
    254 }
- code_keywords: addLiquidity, _addLiquidity, amount0Desired, amount1Desired, amount0Min, amount1Min, amount0Optimal, amount1Optimal, Helper.quote, getReserves, createPair, INSUFFICIENT_1_AMOUNT, INSUFFICIENT_0_AMOUNT, ensure, deadline

### F: Revisited removeLiquidityImbalance Logic in StableSwapStorage
- severity: Low
- component: `StableSwapStorage::removeLiquidityImbalance()` — `burnAmount` computation
- root_cause: Mixed multiplication/division in the `burnAmount = ((D0 - D1) * totalSupply) / D0` calculation rounds down; without a round-up (`burnAmount += 1`) the LP burns slightly less than the value withdrawn.
- missing_control: Round-up on the `burnAmount` calculation (add 1) to protect the remaining liquidity providers from rounding-in-the-withdrawer's-favor
- interaction_scope: single_contract
- contract_set: StableSwapStorage, StableSwap, lpToken
- entry_surface: `removeLiquidityImbalance(amounts, maxBurnAmount, deadline)` external call on StableSwap → StableSwapStorage
- trigger_primitive: Repeated imbalanced liquidity removals exploiting the downward rounding of `burnAmount`
- preconditions: internal — non-zero `totalSupply`, imbalanced removal path
- sink: LP value-conservation invariant: burned LP must be at least the value of assets removed, protecting remaining LPs
- impact: Precision loss favouring the withdrawer at the expense of the pool's remaining liquidity providers; fixed in commit ee3c510
- code: |
    272 ) ex te rn al returns ( uint256 b u r n A m o u n t ) {
    273 uint256 nCoins = self . p o o l e d T o k e n s . length ;
    274 require ( amounts . length == nCoins , " i n v a l i d A m o u n t s L e n g t h " ) ;
    275 uint256 t o t a l S u p p l y = self . lpToken . t o t a l S u p p l y () ;
    276 require ( t o t a l S u p p l y != 0 , " t o t a l S u p p l y = 0 " ) ;
    277 uint256 _fee = _ f e e P e r T o k e n ( self ) ;
    278 uint256 amp = _ g e t A P r e c i s e ( self ) ;
    280 uint256 [] memory n e w B a l a n c e s = self . ba la nce s ;
    281 uint256 D0 = _getD ( _xp ( self ) , amp ) ;
    283 for ( uint256 i = 0; i < nCoins ; i ++) {
    284 n e w B a l a n c e s [ i ] -= amounts [ i ];
    285 }
    287 uint256 D1 = _getD ( _xp ( newBalances , self . t o k e n M u l t i p l i e r s ) , amp ) ;
    288 uint256 [] memory fees = new uint256 []( nCoins ) ;
    290 for ( uint256 i = 0; i < nCoins ; i ++) {
    291 uint256 i d e a l B a l a n c e = ( D1 * self . b al an ce s [ i ]) / D0 ;
    292 uint256 diff = _ d i s t a n c e ( n e w B a l a n c e s [ i ] , i d e a l B a l a n c e ) ;
    293 fees [ i ] = ( _fee * diff ) / F E E _ D E N O M I N A T O R ;
    294 self . ba la nce s [ i ] = n e w B a l a n c e s [ i ] - (( fees [ i ] * self . a dm in Fee ) /
    F E E _ D E N O M I N A T O R ) ;
    295 n e w B a l a n c e s [ i ] -= fees [ i ];
    296 }
    298 // r e c a l c u l a t e i n v a r i a n t with fee charged ba la nce s
    299 D1 = _getD ( _xp ( newBalances , self . t o k e n M u l t i p l i e r s ) , amp ) ;
    300 b u r n A m o u n t = (( D0 - D1 ) * t o t a l S u p p l y ) / D0 ;
    301 assert ( b u r n A m o u n t > 0) ;
    302 require ( b u r n A m o u n t <= maxBurnAmount , " > sl ip pa ge " ) ;
    304 self . lpToken . bu rnF ro m ( msg . sender , b u r n A m o u n t ) ;
- code_keywords: removeLiquidityImbalance, burnAmount, maxBurnAmount, _getD, _xp, _feePerToken, _getAPrecise, FEE_DENOMINATOR, tokenMultipliers, idealBalance, adminFee, lpToken.burnFrom, totalSupply, _distance

### F: Consistent Use of whenNotPaused Modifier in StableSwap
- severity: Low
- component: `StableSwap` — `removeLiquidity()`, `removeLiquidityOneToken()`, `removeLiquidityImbalance()` modifier set
- classification_note: listed as "Informational" in the Key Findings table (Table 2.1) but the detailed section 3.1 states "Severity: Low, Likelihood: Low, Impact: Medium"
- root_cause: The pausable kill-switch is applied inconsistently: `removeLiquidity()` lacks the `whenNotPaused` modifier while `removeLiquidityOneToken()` and `removeLiquidityImbalance()` have it.
- missing_control: Consistent application of the `whenNotPaused` modifier across the paired liquidity-removal entry points
- interaction_scope: single_contract
- contract_set: StableSwap, StableSwapStorage
- entry_surface: External `removeLiquidity` / `removeLiquidityOneToken` / `removeLiquidityImbalance` calls
- trigger_primitive: Calling the unguarded removal path while the protocol is paused
- preconditions: internal — protocol in paused state
- sink: Kill-switch invariant: while paused, state-changing pool operations of the same class must be uniformly blocked
- impact: Inconsistent pause semantics; resolved as intentional — LPs always keep the ability to remove liquidity while paused, and the other two keep `whenNotPaused` to mitigate arbitrage from imbalanced removal
- code: |
    109 fu nc ti on r e m o v e L i q u i d i t y (
    110 uint256 lpAmount ,
    111 uint256 [] memory minAmounts ,
    112 uint256 dea dl in e
    113 ) ex te rn al o ve rr ide n o n R e e n t r a n t d e a d l i n e C h e c k ( d ea dl in e ) returns ( uint256 [] memory )
    {
    114 return s w a p S t o r a g e . r e m o v e L i q u i d i t y ( lpAmount , m i n A m o u n t s ) ;
    115 }
    117 fu nc ti on r e m o v e L i q u i d i t y O n e T o k e n (
    118 uint256 lpAmount ,
    119 uint8 index ,
    120 uint256 minAmount ,
    121 uint256 dea dl in e
    122 ) ex te rn al o ve rr ide n o n R e e n t r a n t w h e n N o t P a u s e d d e a d l i n e C h e c k ( de ad li ne ) returns (
    uint256 ) {
    123 return s w a p S t o r a g e . r e m o v e L i q u i d i t y O n e T o k e n ( lpAmount , index , m i n A m o u n t ) ;
    124 }
    126 fu nc ti on r e m o v e L i q u i d i t y I m b a l a n c e (
    127 uint256 [] memory amounts ,
    128 uint256 maxBurnAmount ,
    129 uint256 dea dl in e
    130 ) ex te rn al o ve rr ide n o n R e e n t r a n t w h e n N o t P a u s e d d e a d l i n e C h e c k ( de ad li ne ) returns (
    uint256 ) {
    131 return s w a p S t o r a g e . r e m o v e L i q u i d i t y I m b a l a n c e ( amounts , m a x B u r n A m o u n t ) ;
    132 }
- code_keywords: whenNotPaused, nonReentrant, deadlineCheck, removeLiquidity, removeLiquidityOneToken, removeLiquidityImbalance, swapStorage, lpAmount, minAmounts, maxBurnAmount

---

## FILE: publications-thorchain-bifrost-utxo-client-zellic-audit-report-pdf.md
- classification: analysis
- classification_reason: Body explicitly states "During our assessment on the scoped THORChain Bifrost UTXO Client modules, there were no security vulnerabilities discovered" with a 0/0/0/0/0 impact breakdown; the substantive content is a Discussion note and a System Design walkthrough of the Bifrost observer/signer, not rated findings.
- protocol: THORChain Bifrost UTXO Client (thornode — Go; BTC/BCH/LTC/DOGE chain clients)
- auditor: Zellic
- date: January 27, 2025 (review period January 6 — January 14, 2025)
- findings_count: 0

Note (non-finding, Discussion section 3.1 — "Potential insolvency issues arising from losses due to chain reorgs"): required confirmation count is derived from total transaction value via `getBlockRequiredConfirmation` / `GetConfMulBasisPoint` / `MaxConfAdjustment` so that a malicious reorg costs more than it gains, but losses from reorgs are socialized across LPs and could make backing vaults insolvent. Reorged-out transactions are reported to THORChain as an `ErrataTx` and their state changes reversed. No severity was assigned by the auditor, so no finding is emitted.

---

## FILE: parallel-halborn-loans.md
- classification: finding
- classification_reason: Body is a Halborn assessment of the Parallel.fi Money Market (loans) Substrate pallet with a Findings & Tech Details section containing two rated issues (HAL-01, HAL-02), each with Description / Code Location / Risk Level / Recommendation / Remediation Plan.
- protocol: Parallel.fi — Money Market (loans) Substrate pallet
- auditor: Halborn
- date: Date of Engagement April 29th, 2022 - May 28th, 2022 (remediation plan June 13-17, 2022)
- findings_count: 2

### F: (HAL-01) THRESHOLDS MIN VALUES NOT ENFORCED
- severity: Informational
- component: `pallets/loans` — `update_market` extrinsic (`close_factor` parameter)
- root_cause: `update_market` validates `collateral_factor`, `reserve_factor` and `supply_cap` with `ensure!` guards but writes `close_factor` (and `liquidate_incentive`, `borrow_cap`) into the stored `Market` without any range validation, permitting values below the minimum expected — including zero.
- missing_control: An `ensure!(close_factor > Ratio::zero() && close_factor < Ratio::one(), Error::<T>::InvalidFactor)` style range check on `close_factor` inside `update_market`
- interaction_scope: single_contract
- contract_set: `pallets/loans` (loans pallet), `Markets` storage via `mutate_market`, liquidation path
- entry_surface: `update_market` extrinsic guarded by `T::UpdateOrigin::ensure_origin(origin)` (admin/governance path)
- trigger_primitive: UpdateOrigin sets `close_factor` to zero (or another out-of-range value)
- preconditions: internal — caller satisfies `T::UpdateOrigin`
- sink: Liquidation-liveness invariant: `close_factor` defines the maximum liquidation limit at a time; a zero value makes it impossible to liquidate any borrow
- impact: If `close_factor` is zero, no user is able to liquidate their borrowings — protocol-wide liquidation DoS and bad-debt accumulation. Marked NOT APPLICABLE by Parallel (close factor set at 50%).
- code: |
    559 pub fn update_market (
    560 origin : OriginFor <T > ,
    561 asset_id : AssetIdOf <T > ,
    562 col la te ra l_f ac to r : Ratio ,
    563 reserve_factor : Ratio ,
    564 close_factor : Ratio ,
    565 li q u i d a t e _ i n c e n t i v e: Rate ,
    566 #[ pallet :: compact ] supply_cap : BalanceOf <T > ,
    567 #[ pallet :: compact ] borrow_cap : BalanceOf <T > ,
    568 ) -> D i s p a t c h R e s u l t W i t h P o s t I n f o{
    569 T :: UpdateOrigin :: ensure_origin ( origin ) ?;
    570
    571 ensure! (
    572 col la te ra l_f ac to r > Ratio :: zero () && col la te ra l_f ac to r <
    ë Ratio :: one () ,
    573 Error :: <T >:: InvalidFactor
    574 ) ;
    575 ensure! (
    576 reserve_factor > Ratio :: zero () && reserve_factor < Ratio ::
    ë one () ,
    577 Error :: <T >:: InvalidFactor
    578 ) ;
    579 ensure! ( supply_cap > Zero :: zero () , Error :: <T >::
    ë InvalidS upplyCap ) ;
    580
    581 let market = Self :: mutate_market ( asset_id , | stored_market | {
    582 * stored_market = Market {
    583 state : stored_market . state ,
    584 ptoken_id : stored_market . ptoken_id ,
    585 rate_model : stored_market . rate_model ,
    586 collateral_factor ,
    587 reserve_factor ,
    588 close_factor ,
    589 liquidate_incentive ,
    590 supply_cap ,
    591 borrow_cap ,
    592 };
    593 stored_market . clone ()
    594 }) ?;
    595 Self :: deposit_event ( Event :: <T >:: UpdatedMarket ( market ) ) ;
    596
    597 Ok (() . into () )
    598 }
- code_keywords: update_market, close_factor, collateral_factor, reserve_factor, liquidate_incentive, supply_cap, borrow_cap, UpdateOrigin, ensure_origin, mutate_market, Market, Ratio, InvalidFactor, InvalidSupplyCap, UpdatedMarket, ptoken_id, rate_model

### F: (HAL-02) MISSING ZERO CHECK
- severity: Informational
- component: `pallets/loans` — `borrow` extrinsic (`borrow_amount` parameter)
- root_cause: `borrow` performs market-active, allowance, interest-accrual and overflow checks but never validates that `borrow_amount` is non-zero, so a zero-value borrow proceeds through the entire state-update and transfer path.
- missing_control: A `borrow_amount != 0` / non-zero validation at the start of `borrow`
- interaction_scope: single_contract
- contract_set: `pallets/loans`, `AccountBorrows` / `TotalBorrows` storage, `T::Assets` (Currency/fungibles transfer)
- entry_surface: `borrow(origin, asset_id, borrow_amount)` extrinsic, `ensure_signed(origin)`
- trigger_primitive: Any signed account calls `borrow` with `borrow_amount = 0`
- preconditions: internal — market is active
- sink: Input-hygiene invariant: state-mutating extrinsics must reject no-op amounts before performing storage writes and events
- impact: No-op borrows write `BorrowSnapshot`/`TotalBorrows` and emit `Borrowed` events with zero amounts, wasting weight and polluting event/indexer state. Marked NOT APPLICABLE by Parallel (zero borrow blocked at the front end).
- code: |
    845 pub fn borrow (
    846 origin : OriginFor <T > ,
    847 asset_id : AssetIdOf <T > ,
    848 #[ pallet :: compact ] borrow_amount : BalanceOf <T > ,
    849 ) -> D i s p a t c h R e s u l t W i t h P o s t I n f o{
    850 let who = ensure_signed ( origin ) ?;
    851 Self :: e n s u r e _ a c t i v e _ m a r k e t( asset_id ) ?;
    852
    853 Self :: borrow_allowed ( asset_id , & who , borrow_amount ) ?;
    854 Self :: accrue_interest ( asset_id ) ?;
    855
    856 // update borrow index after accureInterest .
    857 Self :: u p d a t e _ r e w a r d _ b o r r o w _ i n d e x( asset_id ) ?;
    858 Self :: d i s t r i b u t e _ b o r r o w e r _ r e w a r d( asset_id , & who ) ?;
    859
    860 let account_borrows = Self :: c u r r e n t _ b o r r o w _ b a l a n c e(& who ,
    ë asset_id ) ?;
    861 let a c c o u n t _ b o r r o w s _ n e w= account_borrows
    862 . checked_add ( borrow_amount )
    863 . ok_or ( ArithmeticError :: Overflow ) ?;
    864 let total_borrows = Self :: total_borrows ( asset_id ) ;
    865 let tot al _b or row s_ ne w = total_borrows
    866 . checked_add ( borrow_amount )
    867 . ok_or ( ArithmeticError :: Overflow ) ?;
    868 AccountBorrows :: <T >:: insert (
    869 asset_id ,
    870 & who ,
    871 BorrowSnapshot {
    872 principal : account_borrows_new ,
    873 borrow_index : Self :: borrow_index ( asset_id ) ,
    874 } ,
    875 ) ;
    876 TotalBorrows :: <T >:: insert ( asset_id , tot al _b or row s_ ne w ) ;
    877 T :: Assets :: transfer ( asset_id , & Self :: account_id () , & who ,
    ë borrow_amount , false ) ?;
    878
    879 Self :: deposit_event ( Event :: <T >:: Borrowed ( who , asset_id ,
    ë borrow_amount ) ) ;
    880 Ok (() . into () )
    881 }
- code_keywords: borrow, borrow_amount, ensure_signed, ensure_active_market, borrow_allowed, accrue_interest, update_reward_borrow_index, distribute_borrower_reward, current_borrow_balance, AccountBorrows, TotalBorrows, BorrowSnapshot, borrow_index, ArithmeticError::Overflow, T::Assets::transfer, Borrowed

---

## FILE: zeitgeist-docs-review-checklist-md.md
- classification: noise
- classification_reason: Body is a pull-request review checklist and events-documentation convention guide (TODO refs, labels, docstrings, benchmarks, try-runtime sanity tests, formatting, storage-migration checklist, event-emission policy) with no vulnerability, severity rating, or finding of any kind.
- protocol: Zeitgeist (Substrate parachain)
- auditor: n/a — internal repository process document (zeitgeistpm/zeitgeist)
- date: unknown
- findings_count: 0
