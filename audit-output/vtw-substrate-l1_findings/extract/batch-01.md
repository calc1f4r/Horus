# VTW Extract — substrate-l1_findings — batch-01

Source dir: `/home/calc1f4r/Horus/reports/substrate-l1_findings/`

---

## FILE: hydradx-c4-2401.md
- classification: finding
- classification_reason: Body is a Code4rena contest findings & analysis report with numbered severity-rated issues (H-01, M-01..M-10), each with Impact / PoC / Recommended Mitigation Steps plus sponsor and judge adjudication comments.
- protocol: HydraDX (HydraDX-node — Omnipool, Stableswap, EMA Oracle, Circuit Breaker pallets, Rust/Substrate)
- auditor: Code4rena (C4), judged by Lambda, 27 wardens; report assembled by thebrittfactor
- date: Audit took place February 2 — March 1, 2024; report published 2024-04-10
- findings_count: 11 (1 HIGH + 10 MEDIUM with explicit risk ratings; plus one aggregated "Low Risk and Non-Critical Issues" QA report containing 9 separately-numbered items with no individual severity string)

### F: [H-01] An attacker possesses the capability to exhaust the entirety of liquidity within the stable swap pools by manipulating the buy function, speciﬁcally by setting the asset_in parameter equal to the asset_out parameter
- severity: HIGH
- component: `pallets/stableswap/src/lib.rs` `buy()` extrinsic (L787-L842); `math/src/stableswap/math.rs` `calculate_in_given_out` / `calculate_in_given_out_with_fee` / `calculate_in_amount`
- root_cause: The stableswap `buy` extrinsic never rejects `asset_in == asset_out`. When the same index is used for in and out, `new_reserve_in` equals the unchanged `reserves[idx_in]`, so the computed `amount_in` (the difference between new and old reserve) is zero and only the hard-coded `+1` and the fee remain.
- missing_control: `ensure!(asset_out != asset_in, Error::<T>::Invalid...)` at the top of `buy()` (equivalently a same-asset guard in the math layer)
- interaction_scope: single_contract
- contract_set: pallet-stableswap, hydra-dx-math stableswap math module
- entry_surface: extrinsic `Stableswap::buy(origin, pool_id, asset_out, asset_in, amount_out, max_sell_amount)` called by any signed origin (`ensure_signed`)
- trigger_primitive: Attacker submits `buy` with `asset_in` set to the same registered pool asset as `asset_out` and a large `amount_out`; repeats in a loop
- preconditions: internal — pool exists with the chosen asset registered and funded; no external precondition, no permissions required
- sink: Stableswap pool reserve conservation invariant — user receives `amount_out` while paying ~1 unit plus fee; pool reserve of that asset is drained toward zero
- impact: Complete drain of all liquidity of every asset in every stableswap pool; PoC shows BOB profiting 99999999999999999972 of asset_a from a pool of 100000000000000000000
- code: |
    let (amount_in, fee_amount) = Self
    let new_reserve_in = calculate_y_given_out::<D, Y>(amount_out, idx

    let amount_in = new_reserve_in.checked_sub(reserves[idx_in])?;
    let amount_in = normalize_value(
                    amount_in,
                    TARGET_PRECISION,
                    initial_reserves[idx_in].decimals,
                    Rounding::Up,
            );
            Some(amount_in.saturating_add(1u128))

    // Recommended Mitigation Steps
                    pub fn buy(
                            origin: OriginFor<T>,
                            pool_id: T::AssetId,
                            asset_out: T::AssetId,
                            asset_in: T::AssetId,
                            amount_out: Balance,
                            max_sell_amount: Balance,
                    ) -> DispatchResult {
                            let who = ensure_signed(origin)?;
    +                        ensure!(
    +                 asset_out != asset_in, Error::<T>::Invalid
    +                );
- code_keywords: buy, asset_in, asset_out, pool_id, max_sell_amount, ensure_signed, calculate_in_amount, calculate_in_given_out, calculate_in_given_out_with_fee, calculate_y_given_out, new_reserve_in, reserves, idx_in, normalize_value, TARGET_PRECISION, Rounding::Up, saturating_add, Permill, PoolInfo, Stableswap

### F: [M-01] Users can MAKE EMA-Oracle price outdated with direct transfers to StableSwap
- severity: Medium (judge Lambda first decreased to Low, then increased severity back to Medium)
- component: HydraDX runtime call filter (`RuntimeCall::Tokens` / `RuntimeCall::Currencies` / `RuntimeCall::Balances` transfer filter) + pallet-stableswap + pallet-ema-oracle
- root_cause: The EMA oracle is only updated through the StableSwap/Omnipool hooks (`on_trade`, `on_liquidity_changed`). The runtime transfer filter blocks direct token transfers to `Omnipool::protocol_account()` but has no equivalent rule for the StableSwap pool accounts, so donations silently change the AMM pool ratio without any hook firing.
- missing_control: Runtime call-filter branch denying `transfer` / `transfer_keep_alive` / `transfer_all` / `transfer_native_currency` whose `dest` is a StableSwap pool account (mirroring the existing Omnipool guard)
- interaction_scope: cross_protocol
- contract_set: hydradx runtime `BaseFilter`/call filter, pallet-stableswap pool accounts, pallet-ema-oracle, orml_tokens, pallet_currencies, pallet_balances; plus downstream external consumers (lending protocols)
- entry_surface: plain balance-transfer extrinsics (`orml_tokens::Call::transfer`, `transfer_keep_alive`, `transfer_all`, `pallet_currencies::Call::transfer`) addressed to the StableSwap pool account
- trigger_primitive: Attacker directly transfers assets into the StableSwap pool account, especially during network congestion, to move the AMM price without an oracle update
- preconditions: internal — asset listed on a StableSwap pool; external — third-party protocols (e.g. lending) consume the EMA oracle price
- sink: Oracle-tracks-AMM invariant: "oracle should always return the current price of the assets at stableswap/omnipool" is violated; oracle price becomes stale/incorrect relative to pool state
- impact: Misleading exchange rates for oracle consumers; arbitrage/liquidation interference — "could unjustly prevent necessary liquidations within lending protocols"
- code: |
    // filter transfers of LRNA and omnipool assets to the omnipool account
    iflet RuntimeCall::Tokens(orml_tokens::Call::transfer { dest, currency_id
    | RuntimeCall::Tokens(orml_tokens::Call::transfer_keep_alive { dest, curre
    | RuntimeCall::Tokens(orml_tokens::Call::transfer_all { dest, currency_id,
    | RuntimeCall::Currencies(pallet_currencies::Call::transfer { dest, curren
    {
    // Lookup::lookup() is not necessary thanks to IdentityLookup
    if dest == &Omnipool::protocol_account() && (*currency_id == hub_a
    {
    returnfalse;
    }
    }
    // filter transfers of HDX to the omnipool account
    iflet RuntimeCall::Balances(pallet_balances::Call::transfer { dest, .. })
    | RuntimeCall::Balances(pallet_balances::Call::transfer_keep_alive { dest,
    | RuntimeCall::Balances(pallet_balances::Call::transfer_all { dest, .. })
    | RuntimeCall::Currencies(pallet_currencies::Call::transfer_native_currenc
    {
    // Lookup::lookup() is not necessary thanks to IdentityLookup
    if dest == &Omnipool::protocol_account() {
    returnfalse;
    }
    }
- code_keywords: RuntimeCall, orml_tokens::Call::transfer, transfer_keep_alive, transfer_all, pallet_currencies::Call::transfer, transfer_native_currency, pallet_balances::Call::transfer, Omnipool::protocol_account, IdentityLookup, dest, currency_id, hub_asset, EmaOracle, on_trade, on_liquidity_changed

### F: [M-02] Malicious liquidity provider can put pool into highly manipulatable state
- severity: Medium (sponsor confirmed but disagreed with severity; judge Lambda kept Medium)
- component: `pallets/stableswap` — `withdraw_asset_amount()` vs `remove_liquidity_one_asset()`
- root_cause: `remove_liquidity_one_asset()` enforces both a per-user share check and a pool-wide `total_issuance` check, while `withdraw_asset_amount()` only enforces the per-user check. Because share tokens are transferable, a user can move 1 share to a second address he controls and then "withdraw all" his remaining shares, bypassing the pool-level `MinPoolLiquidity` floor.
- missing_control: The `share_issuance == share_amount || share_issuance.saturating_sub(share_amount) >= T::MinPoolLiquidity` check (`Error::<T>::InsufficientLiquidityRemaining`) is absent from `withdraw_asset_amount()`
- interaction_scope: single_contract
- contract_set: pallet-stableswap, share-asset currency (transferable LP share token)
- entry_surface: extrinsics `Stableswap::withdraw_asset_amount`, `Stableswap::remove_liquidity_one_asset`, plus a plain share-token `transfer`
- trigger_primitive: LP deposits `MinPoolLiquidity`, transfers 1 share to a self-controlled address, then calls `withdraw_asset_amount()` to drain the rest — the "withdraw all my shares" branch passes
- preconditions: internal — attacker is (or is one of few) LPs in the pool; share token transferable
- sink: Documented invariant `totalPoolIssuance(poolId) >= MinPoolLiquidity || totalPoolIssuance(poolId) == 0` is broken; pool can sit at 1 share
- impact: (1) pool left with ~1 share of liquidity → trivially price-manipulatable; (2) DoS of `remove_liquidity_one_asset()` for remaining LPs (notably contract LPs hard-coded to that path), who are forced to keep liquidity in the pool
- code: |
    // remove_liquidity_one_asset() — both checks present
    let current_share_balance = T::Currency::free_balance(pool_id, &who);
    ensure!(
    current_share_balance == share_amount
    || current_share_balance.saturating_sub(share_amount) >= T
    Error::<T>::InsufficientShareBalance
    );

    let share_issuance = T::Currency::total_issuance(pool_id);
    ensure!(
    share_issuance == share_amount
    || share_issuance.saturating_sub(share_amount) >= T::MinPo
    Error::<T>::InsufficientLiquidityRemaining
    );

    // withdraw_asset_amount() — pool-wide check omitted
    let current_share_balance = T::Currency::free_balance(pool_id, &who);
    ensure!(
    current_share_balance == shares
    || current_share_balance.saturating_sub(shares) >= T::MinP
    Error::<T>::InsufficientShareBalance
    );

    // Recommended Mitigation Steps
    letshare_issuance = T::Currency::total_issuance(pool_id);
    ensure!(
    share_issuance == share_amount
    || share_issuance.saturating_sub(share_amount
    Error::<T>::InsufficientLiquidityRemaining
    );
- code_keywords: withdraw_asset_amount, remove_liquidity_one_asset, MinPoolLiquidity, T::Currency::free_balance, T::Currency::total_issuance, share_issuance, current_share_balance, saturating_sub, InsufficientShareBalance, InsufficientLiquidityRemaining, pool_id, totalPoolIssuance

### F: [M-03] No slippage check in remove_liquidity function in omnipool can lead to slippage losses during liquidity withdrawal.
- severity: Medium (sponsor confirmed but disagreed with severity; judge: "Valid medium because there is a hypothetical path to leak values")
- component: `pallets/omnipool` — `remove_liquidity()`
- root_cause: The Omnipool liquidity-removal extrinsic takes no `minimum_amount_out` / slippage parameter. The only bound is the `ensure_price` barrier which allows ±1% deviation from the oracle price, so a frontrunner can move the spot price and force the withdrawer to realize the whole permitted band.
- missing_control: A user-supplied minimum-output / slippage limit parameter on `remove_liquidity` (the built-in 2% `ensure_price` band is too wide)
- interaction_scope: single_contract
- contract_set: pallet-omnipool, pallet-ema-oracle (price barrier source), LRNA hub asset swap path
- entry_surface: extrinsic `Omnipool::remove_liquidity`; adversary uses public `sell`/`buy` extrinsics in the same block
- trigger_primitive: MEV frontrunner sandwiches the LP's `remove_liquidity` by swapping token→DAI (devalue, burns LP shares) or DAI→token (inflate, LP paid in LRNA which is then sandwiched on the LRNA→token swap)
- preconditions: internal — trading enabled on the asset; external — mempool visibility / block-builder ordering (MEV)
- sink: LP withdrawal-value conservation — LP receives materially less than the deposit-time value even though she withdraws "at the same price"
- impact: Measured PoC losses of ~1% per scenario vs a 0.1% fee-only baseline (4990e12 baseline vs 4961892744479493 and 4958579804661321); losses capped at ~2% by `ensure_price`, still above the 0.5% industry standard
- code: |
    NO_CODE_IN_REPORT
    (PoC body collapsed as "▸ Details"; only run logs published, e.g.
     lrna_init: 2000000000000000 / token_init: 5000000000000000 /
     token_remove: 4961892744479493 and token_end: 4958579804661321)
- code_keywords: remove_liquidity, minimum_amount_out, ensure_price, PriceBarrier, EmaPrice, LRNA, hub_reserve, withdrawal fee, Omnipool

### F: [M-04] Complete liquidity removals fail from stableswap pools
- severity: Medium (sponsor disputed; judge Lambda ruled Medium — "(temporary) locked funds in edge cases")
- component: `pallets/stableswap/src/lib.rs` L551 (`remove_liquidity_one_asset`) and L638 (`withdraw_asset_amount`); stableswap curve math (`calculate_d` / `calculate_withdraw_one_asset`)
- root_cause: Stableswap only supports single-asset redemption; it omits Curve's `remove_liquidity` (proportional multi-token withdrawal). Redeeming the last shares requires converting all composing tokens into one token against liquidity that no longer exists, so the curve math overflows and the extrinsic reverts.
- missing_control: A proportional multi-token `remove_liquidity` path (or an explicit zero-liquidity branch in the D/Y math) for the final/complete withdrawal case
- interaction_scope: single_contract
- contract_set: pallet-stableswap, hydra-dx-math stableswap math (D invariant, Y reserve)
- entry_surface: extrinsic `Stableswap::remove_liquidity_one_asset(origin, pool_id, asset_a, received_shares, 0)`
- trigger_primitive: Sole/last LP attempts to redeem the full share balance of the pool
- preconditions: internal — attempting to redeem the entire outstanding share issuance of the pool
- sink: Liquidity-redeemability invariant — initial liquidity cannot be removed from the system
- impact: Extrinsic panics with `Arithmetic(Overflow)`; the initial/complete liquidity is (temporarily) locked in the pool
- code: |
    assert_ok!(Stableswap::remove_liquidity_one_asset
                    RuntimeOrigin::signed(ALICE),
                    pool_id,
                    asset_a,
                    received,
    0
                ));

    running 1 test
    LP tokens received: 23786876415280195891619
    thread 'tests::add_liquidity::test_Attack_min_shares' panicked at 'Expecte
        Arithmetic(
            Overflow,
        ),
    )', pallets/stableswap/src/tests/add_liquidity.rs:889:13
    note: run with `RUST_BACKTRACE=1` environment variable to display a backtr
    test tests::add_liquidity::test_Attack_min_shares ... FAILED
- code_keywords: remove_liquidity_one_asset, withdraw_asset_amount, remove_liquidity, calculate_d, calculate_withdraw_one_asset, ArithmeticError::Overflow, Arithmetic(Overflow), pool_id, PoolInfo, InitialLiquidity, Stableswap

### F: [M-05] No safe_withdrawal option in withdraw_protocol_liquidity function in omnipool can be abused by frontrunners to cause losses to the admin when removing liquidity
- severity: Medium (submitted as high by warden; sponsor confirmed but disagreed; judge Lambda decreased severity to Medium)
- component: `pallets/omnipool` — `withdraw_protocol_liquidity()` (paired with `sacrifice_position()` and `remove_liquidity()`)
- root_cause: `remove_liquidity` guards non-safe withdrawals with `T::PriceBarrier::ensure_price(...)` (1% band). `withdraw_protocol_liquidity` has no equivalent barrier and no minimum-out, so the admin-supplied price parameter can be invalidated by a frontrunner moving the spot price.
- missing_control: `safe_withdrawal` flag / `ensure_price` barrier / `minimum_out` parameter on `withdraw_protocol_liquidity`
- interaction_scope: single_contract
- contract_set: pallet-omnipool (`withdraw_protocol_liquidity`, `sacrifice_position`, `remove_liquidity`), price barrier `EnsurePriceWithin`, EMA oracle
- entry_surface: admin path — `Omnipool::withdraw_protocol_liquidity` (privileged origin) with an admin-passed `price` parameter
- trigger_primitive: Frontrunner manipulates the Omnipool spot price away from the admin-passed price in the same block before the admin extrinsic executes
- preconditions: internal — protocol holds sacrificed positions; trading not paused (sponsor claims it "usually" is paused, but this is not enforced in code)
- sink: Protocol-owned-liquidity value conservation — protocol withdraws at a manipulated price with no deviation bound
- impact: Slippage losses to the protocol/admin that are unbounded, explicitly larger than the ~2% cap that applies to `remove_liquidity`
- code: |
    // remove_liquidity
    if !safe_withdrawal {
            T::PriceBarrier::ensure_price(
                &who,
                T::HubAssetId::get(),
                asset_id,
                EmaPrice::new(asset_state.hub_reserve, asset_state.reserve),
            )
            .map_err(|_| Error::<T>::PriceDifferenceTooHigh)?;
        }
- code_keywords: withdraw_protocol_liquidity, sacrifice_position, remove_liquidity, safe_withdrawal, PriceBarrier, ensure_price, EmaPrice, HubAssetId, hub_reserve, asset_state.reserve, PriceDifferenceTooHigh, protocol_shares

### F: [M-06] complete liquidity removal will result in permanent disable of the liquidity addition and prevent minting shares for the liquidity providers.
- severity: Medium (judge Lambda decreased severity to Medium; sponsor disputed as desired behavior)
- component: `pallets/omnipool/src/lib.rs` L612-L621 — `add_liquidity()` / `calculate_add_liquidity_state_changes`; reached via `remove_liquidity()` and `add_token()`
- root_cause: `remove_liquidity` allows burning 100% of shares, leaving `asset_reserve == 0` and `shares == 0`. `calculate_add_liquidity_state_changes` then divides by `reserve_hp` (zero) — there is no zero-liquidity bootstrap branch equivalent to `add_token()`.
- missing_control: A zero-state branch in `add_liquidity` — when total shares are zero, mint shares equal to the added asset value (as `add_token()` does) — and/or a guard preventing the last share from being burned
- interaction_scope: single_contract
- contract_set: pallet-omnipool (`add_liquidity`, `remove_liquidity`, `add_token`, `Positions`, `Assets`), hydra_dx_math omnipool math
- entry_surface: extrinsics `Omnipool::remove_liquidity` (any position owner, including the initial `position_owner` created by `add_token`), then `Omnipool::add_liquidity`
- trigger_primitive: Sole/initial LP (or all LPs collectively) removes 100% of shares; optionally an attacker then dusts the pool account with 1 unit of the asset
- preconditions: internal — token previously added via `add_token`, then all liquidity removed; no privileges needed
- sink: Pool-bootstrap invariant — a pool with a registered asset must remain able to accept liquidity; `delta_shares_hp` division by zero reserve
- impact: Permanent DoS of `add_liquidity` (and thereby `sell`/`buy`) for that asset with `ArithmeticError::Overflow`; if someone donates a non-zero amount, `add_liquidity` succeeds but mints 0 shares → permanent loss/lock of funds for the LP (PoC: reserve 401000000000000, hub_reserve 0, shares 0, position shares 0)
- code: |
    let delta_shares_hp = shares_hp
                    .checked_mul(amount_hp)
                    .and_then(|v| v.checked_div(reserve_hp))?;

    let state_changes = hydra_dx_math::omnipool::
                                    &(&asset_state).into(),
                                    amount,
                                    &(&position).into(),
                                    I129 {
                                            value: current_imbalance.value,
                                            negative: current_imbalance.negati
                                    },
                                    current_hub_asset_liquidity,
                                    withdrawal_fee,
                            )
                            .ok_or(ArithmeticError::Overflow)?;
    let new_asset_state = asset_state
                                    .clone()
                                    .delta_update(&state_changes.asset)
                                    .ok_or(ArithmeticError::Overflow)?;
- code_keywords: add_liquidity, remove_liquidity, add_token, calculate_add_liquidity_state_changes, calculate_remove_liquidity_state_changes, delta_shares_hp, shares_hp, reserve_hp, checked_div, checked_mul, ArithmeticError::Overflow, AssetReserveState, Positions, NextPositionId, protocol_shares, delta_update, I129

### F: [M-07] Re-adding assets to the omnipool can cause a problem with the oracle
- severity: Medium (sponsor acknowledged but disagreed with severity; judge Lambda: Medium)
- component: `pallets/omnipool/src/lib.rs` L1541-L1574 (`remove_token`), `pallets/omnipool/src/traits.rs` L164-L190, `pallets/ema-oracle/src/lib.rs` L558-L566 / L153-L162 (`Oracles` StorageNMap)
- root_cause: `remove_token` deletes all Omnipool records and LP positions for an asset but leaves the corresponding entries in the EMA oracle `Oracles` StorageNMap. On re-adding the asset at a different price, the EMA integrates pre-removal entries with post-re-add entries.
- missing_control: Deletion/reset of the `Oracles` storage entries for the asset pair when `remove_token` executes
- interaction_scope: multi_contract
- contract_set: pallet-omnipool (`remove_token`, `add_token`, `sacrifice_position`, `set_asset_tradable_state`), pallet-ema-oracle (`Oracles` StorageNMap, `OracleEntry`), `EnsurePriceWithin`/`PriceBarrier`
- entry_surface: admin path — root/`AuthorityOrigin` `Omnipool::remove_token` then `Omnipool::add_token`; consumed by `EmaOracle::get_price` and by `add_liquidity`'s `ensure_price`
- trigger_primitive: Governance removes a token (freeze → sacrifice_position → remove_token) and later re-adds it at a changed price (PoC: 1.0 → 10.0)
- preconditions: internal — asset frozen and fully protocol-owned so `remove_token` passes; external — third-party protocols read the oracle
- sink: Oracle freshness/consistency invariant — EMA blends stale pre-removal price history into the re-added asset's price
- impact: Incorrect price returned to all oracle consumers for the length of the short period; `ensure_price` in `add_liquidity` can fail so no liquidity can be added (short DoS)
- code: |
    pubtypeOracles<T: Config> = StorageNMap<
                    _,
                    (
                            NMapKey<Twox64Concat, Source>,
                            NMapKey<Twox64Concat, (AssetId, AssetId)>,
                            NMapKey<Twox64Concat, OraclePeriod>,
                    ),
                    (OracleEntry<BlockNumberFor<T>>, BlockNumberFor<T>),
                    OptionQuery,
            >;

    T::PriceBarrier::ensure_price(
    &who,
          T::HubAssetId::get(),
      asset,
        EmaPrice::new(asset_state.hub_reserve, asset_state.reserve),
    )
    .map_err(|_| Error::<T>::PriceDifferenceTooHigh)?;
- code_keywords: remove_token, add_token, sacrifice_position, set_asset_tradable_state, Tradability::FROZEN, Oracles, StorageNMap, NMapKey, Twox64Concat, OraclePeriod, OracleEntry, EmaOracle, get_price, PriceBarrier, ensure_price, EmaPrice, PriceDifferenceTooHigh, Source, AssetId

### F: [M-08] Storage can be bloated with low value liquidity positions
- severity: Medium (sponsor disputed as publicly known; judge Lambda: not ruled out of scope, valid)
- component: `pallets/omnipool` — `add_liquidity()` / `remove_liquidity()` and the `Positions` StorageMap (+ NFT instance per position)
- root_cause: `MinimumPoolLiquidity` (1,000,000 in the runtime config) is enforced only at deposit time; `remove_liquidity` has no floor on the *remaining* position amount, so a user can deposit the minimum and immediately withdraw all-but-1, leaving a dust `Positions` entry and a live NFT.
- missing_control: `ensure!(updated_position.amount >= T::MinimumPoolLiquidity..., Error::<T>::InsufficientLiquidity)` on the post-withdrawal position in `remove_liquidity()`
- interaction_scope: single_contract
- contract_set: pallet-omnipool (`Positions`, `NextPositionId`, `NFTHandler`, `NFTCollectionId`), runtime weight config (`omnipool/src/weights.rs`)
- entry_surface: extrinsics `Omnipool::add_liquidity` then `Omnipool::remove_liquidity` with `amount - 1`
- trigger_primitive: Attacker repeatedly adds exactly `MinimumPoolLiquidity` of a very low-value asset and removes all but 1 unit, creating unbounded dust positions
- preconditions: internal — permissionless `add_liquidity`; attacker pays only extrinsic weight fees
- sink: Chain state-growth bound — the economic floor that is supposed to gate a `Positions` write is bypassed; storage cost is borne by chain maintainers, not the user
- impact: Cheap unbounded state bloat (~1/1,000,000 of intended cost) → rising maintenance cost and potential chain DoS; per the warden, computation weight is charged to the user but the recurring storage cost is not
- code: |
    let instance_id = Self::create_and_mint_position_instance
    <Positions<T>>::insert(instance_id, lp_position);

    ensure!(
    amount >= T::MinimumPoolLiquidity::get() && amount > 
    Error::<T>::MissingBalance
    );

    if updated_position.shares == Balance::zero() {
    // All liquidity removed, remove position and burn NFT instance
    <Positions<T>>::remove(position_id);
    T::NFTHandler::burn(&T::NFTCollectionId::get(), &position_id, Some
    Self::deposit_event(Event::PositionDestroyed {
    position_id,
    owner: who.clone(),
    });
    }

    // Recommended Mitigation Steps
    ensure!(
    updated_position.amount >= T::MinimumPoolLiquidity
    Error::<T>::InsufficientLiquidity
    );
- code_keywords: add_liquidity, remove_liquidity, MinimumPoolLiquidity, Positions, NextPositionId, create_and_mint_position_instance, NFTHandler, NFTCollectionId, PositionDestroyed, MissingBalance, InsufficientLiquidity, updated_position, weights.rs, DbWeight, Weight::from_parts

### F: [M-09] Missing hook call will lead to incorrect oracle results
- severity: Medium (sponsor disputed via duplicate #141; judge Lambda agreed with warden — `remove_token` does change liquidity)
- component: `pallets/omnipool` — `remove_token()` (call_index 12) vs `withdraw_protocol_liquidity()` / `add_token()`; `OmnipoolHooks::on_liquidity_changed`
- root_cause: `remove_token` transfers all protocol-owned liquidity to a beneficiary (a real liquidity change) but never invokes `T::OmnipoolHooks::on_liquidity_changed`, unlike `add_token` and `withdraw_protocol_liquidity`. The EMA oracle and circuit breaker therefore never see the change.
- missing_control: `T::OmnipoolHooks::on_liquidity_changed(origin, info)?;` at the end of `remove_token`
- interaction_scope: multi_contract
- contract_set: pallet-omnipool (`remove_token`, `add_token`, `withdraw_protocol_liquidity`, `sacrifice_position`), pallet-ema-oracle (`on_liquidity_changed`), pallet-circuit-breaker (`ensure_and_update_remove_liquidity_limit`)
- entry_surface: admin path — `Omnipool::remove_token(origin, asset_id, beneficiary)` gated by `T::AuthorityOrigin::ensure_origin`
- trigger_primitive: Authority removes a frozen, fully protocol-owned token; the beneficiary receives the reserve without any hook accounting
- preconditions: internal — `asset_state.tradable == Tradability::FROZEN` and `asset_state.shares == asset_state.protocol_shares`
- sink: Hook-completeness invariant — every liquidity mutation must notify oracle + circuit breaker; here the per-block liquidity-change budget and the oracle liquidity series both miss the withdrawal
- impact: Oracle computes prices from an outdated Omnipool liquidity state; circuit-breaker limits are under-counted (warden example: 90 tokens removed uncounted, a later 20-token withdrawal wrongly passes a 100-token/block cap)
- code: |
    #[pallet::call_index(12)]
    #[pallet::weight(<T as Config>::WeightInfo::remove_token())]
    #[transactional]
    pubfnremove_token(origin: OriginFor<T>, asset_id: T::AssetId, beneficiar
    T::AuthorityOrigin::ensure_origin(origin)?;
    let asset_state = Self::load_asset_state(asset_id)?;
    // Allow only if no shares are owned by LPs and the asset is froze
    ensure!(asset_state.tradable == Tradability::FROZEN, Error::<T>::A
    ensure!(
    asset_state.shares == asset_state.protocol_shares,
    Error::<T>::SharesRemaining
    );
    // Imbalance update
    let imbalance = <HubAssetImbalance<T>>::get();
    let hub_asset_liquidity = Self::get_hub_asset_balance_of_protocol_
    let delta_imbalance = hydra_dx_math::omnipool::calculate_delta_imb
    asset_state.hub_reserve,
    I129 {
    value: imbalance.value,
    negative: imbalance.negative,
    },
    hub_asset_liquidity,
    )
    .ok_or(ArithmeticError::Overflow)?;
    Self::update_imbalance(BalanceUpdate::Increase(delta_imbalance))?;
    T::Currency::withdraw(T::HubAssetId::get(), &Self
    T::Currency::transfer(asset_id, &Self::protocol_account
    <Assets<T>>::remove(asset_id);
    Self::deposit_event(Event::TokenRemoved {
    asset_id,
    amount: asset_state.reserve,
    hub_withdrawn: asset_state.hub_reserve,
    });
    Ok(())
    }

    // present in withdraw_protocol_liquidity, absent here:
    T::OmnipoolHooks::on_liquidity_changed(origin, info)?;
- code_keywords: remove_token, add_token, withdraw_protocol_liquidity, sacrifice_position, OmnipoolHooks, on_liquidity_changed, on_trade, pallet::call_index, transactional, AuthorityOrigin, ensure_origin, Tradability::FROZEN, AssetNotFrozen, SharesRemaining, protocol_shares, HubAssetImbalance, calculate_delta_imbalance, BalanceUpdate::Increase, TokenRemoved, circuit-breaker

### F: [M-10] A huge loss of funds for all the users who try to remove liquidity after swapping got disabled at manipulated price.
- severity: Medium (judge Lambda decreased severity to Low, then increased severity to Medium; sponsor acknowledged)
- component: `pallets/omnipool/src/lib.rs` L1330-L1360 (`set_asset_tradable_state`) and L759-L764 (`remove_liquidity` / `is_safe_withdrawal`); `calculate_withdrawal_fee` in omnipool math
- root_cause: `is_safe_withdrawal()` returns true when tradability is exactly `ADD_LIQUIDITY | REMOVE_LIQUIDITY`, which skips `ensure_price`. `set_asset_tradable_state` never validates that spot and oracle price are close before entering that state, so the state can be entered while the price is manipulated. `calculate_withdrawal_fee` then clamps to `FixedU128::one()` (100%).
- missing_control: A price-deviation check (`T::PriceBarrier::ensure_price(...)`) inside `set_asset_tradable_state` before allowing the swap-disabled "safe withdrawal" state — and/or a user-supplied minimum-out on `remove_liquidity`
- interaction_scope: single_contract
- contract_set: pallet-omnipool (`set_asset_tradable_state`, `remove_liquidity`, `Tradability`, `HubAssetTradability`), hydra_dx_math omnipool `calculate_withdrawal_fee`, EMA oracle price source
- entry_surface: admin path — `Omnipool::set_asset_tradable_state` gated by `T::TechnicalOrigin::ensure_origin`; then any LP's `Omnipool::remove_liquidity`
- trigger_primitive: Attacker manipulates spot price far from oracle price and frontruns/anticipates the tradability change to `ADD_LIQUIDITY | REMOVE_LIQUIDITY`; victims then withdraw
- preconditions: internal — technical origin sets the swap-disabled tradability state while the price deviation is large; no cap on which non-hub asset can be set
- sink: Withdrawal-fee bound invariant — `withdrawal_fee` is clamped at 1.0 so `fee_complement` is zero and all delta amounts sent to the LP are zero, while the transaction still succeeds
- impact: 100% of a withdrawing LP's liquidity is taken as `withdrawal_fee` and redistributed to the remaining LPs; the call does not revert and there is no slippage parameter to protect the user
- code: |
    let safe_withdrawal = asset_state.tradable.
    pub(crate) fnis_safe_withdrawal(&self) -> bool {
                    *self == Tradability::ADD_LIQUIDITY | Tradability::REMOVE_
            }
    }

    pubfncalculate_withdrawal_fee(
            spot_price: FixedU128,
            oracle_price: FixedU128,
            min_withdrawal_fee: Permill,
    ) -> FixedU128 {
    let price_diff = if oracle_price <= spot_price {
                    spot_price.saturating_sub(oracle_price)
            } else {
                    oracle_price.saturating_sub(spot_price)
            };
    let min_fee: FixedU128 = min_withdrawal_fee.into();
    debug_assert!(min_fee <= FixedU128::one());
    if oracle_price.is_zero() {
    return min_fee;
            }
    // fee can be set to 100% 
      ->    price_diff.div(oracle_price).clamp(min_fee, FixedU128::
    }

    // fee_complement = 0 ; 
    let fee_complement = FixedU128::one().saturating_sub
    // Apply withdrawal fee
    let delta_reserve = fee_complement.checked_mul_int
    let delta_hub_reserve = fee_complement.checked_mul_int
    let hub_transferred = fee_complement.checked_mul_int
    let delta_imbalance = calculate_delta_imbalance(delta_hub_reserve,

    // Recommended Mitigation Steps (added to set_asset_tradable_state)
    + if (state == Tradability::ADD_LIQUIDITY | Tradability::REMOVE_LIQUIDITY 
    +
    +      T::PriceBarrier::ensure_price(
    +& w h o ,
    +T : : H u b A s s e t I d : : get
    +a s s e t _ i d ,
    +E m a P r i c e : : new(asset_state.hub_rese
    +)
    +. map_err(|_| Error::<T>::PriceDifferenceTo
- code_keywords: set_asset_tradable_state, Tradability, ADD_LIQUIDITY, REMOVE_LIQUIDITY, is_safe_withdrawal, safe_withdrawal, calculate_withdrawal_fee, min_withdrawal_fee, fee_complement, FixedU128, Permill, clamp, price_diff, oracle_price, spot_price, PriceBarrier, ensure_price, PriceDifferenceTooHigh, TechnicalOrigin, HubAssetTradability, InvalidHubAssetTradabilityState, checked_mul_int, calculate_delta_imbalance

### F: (QA) 2. Huge loss of funds for the users and the protocol, if the pool is created with share_asset that does have a diﬀerent decimals from 18 decimals
- severity: Low Risk and Non-Critical (section-level rating; sponsor marked "Stableswap 2 - Invalid")
- component: `pallets/stableswap` — `create_pool` / `do_create_pool`, normalization used by `calculate_d` and `calculate_y`
- root_cause: The stableswap implementation assumes the pool share asset has 18 decimals, but `create_pool` never validates the registered decimals of `share_asset`; the normalization function scales all reserves to 18 decimals for D and Y.
- missing_control: `ensure!(T::AssetInspection::decimals(share_asset) == 18, Error::<T>::Invalid_decimals)` in `do_create_pool`
- interaction_scope: multi_contract
- contract_set: pallet-stableswap (`create_pool`, `do_create_pool`), asset registry (`T::AssetInspection::decimals`), hydra-dx-math stableswap normalization
- entry_surface: extrinsic `Stableswap::create_pool` (requires `AuthorityOrigin`)
- trigger_primitive: Pool is created with a share asset registered at non-18 decimals
- preconditions: internal — authority creates the pool; asset registry permits arbitrary decimals
- sink: Decimal-normalization invariant for the D/Y curve math
- impact: Wrong D and Y computation across the whole pool — "huge loss of funds for the user and the protocol"
- code: |
    +                ensure!(
    +                        T::AssetInspection::decimals(share_asset)== 18,
    +                        Error::<T>::Invalid_decimals
    +                );
- code_keywords: create_pool, do_create_pool, share_asset, AssetInspection, decimals, normalize_reserves, normalize_value, calculate_d, calculate_y, TARGET_PRECISION, Invalid_decimals

### F: (QA) 1. Prevent calling the funtcions on_trade and on_liquidity_changed with asset_in = asset_out, to prevent storing invalid prices
- severity: Low Risk and Non-Critical (section-level rating; sponsor marked "Oracle 1 - Okay")
- component: `pallets/ema-oracle` — `on_trade`, `on_liquidity_changed` (OnActivityHandler); fed by `pallets/stableswap` `buy`
- root_cause: The oracle activity handlers do not check `asset_in != asset_out`, and the stableswap `buy` extrinsic does not prevent equal in/out assets, so a self-swap writes a degenerate price entry.
- missing_control: `asset_in != asset_out` guard in `on_trade` / `on_liquidity_changed` (and in the calling extrinsic)
- interaction_scope: multi_contract
- contract_set: pallet-ema-oracle (`on_trade`, `on_liquidity_changed`, `Oracles` accumulator), pallet-stableswap (`buy`)
- entry_surface: extrinsic `Stableswap::buy` → oracle hook `on_trade`
- trigger_primitive: Attacker executes a same-asset trade so the adapter records a self-pair price
- preconditions: internal — same root cause as H-01 (no same-asset guard in `buy`)
- sink: Oracle entry validity — invalid/self-referential price pairs persisted in the `Oracles` store
- impact: Invalid prices stored in the EMA oracle
- code: |
    pubfnbuy(
                            origin: OriginFor<T>,
                            pool_id: T::AssetId,
                            asset_out: T::AssetId,
                            asset_in: T::AssetId,
                            amount_out: Balance,
                            max_sell_amount: Balance,
                    ) -> DispatchResult {
    let who = ensure_signed(origin)?;
    ensure!(
    Self::is_asset_allowed(pool_id, asset_in, 
                                            && Self::is_asset_allowed
                                    Error::<T>::NotAllowed
                            );
    ensure!(
                                    amount_out >= T::MinTradingLimit::
                                    Error::<T>::InsufficientTradingAmount
                            );
- code_keywords: on_trade, on_liquidity_changed, OnActivityHandler, asset_in, asset_out, is_asset_allowed, MinTradingLimit, InsufficientTradingAmount, NotAllowed, ensure_signed, EmaOracle

### F: (QA) 2. Prevent store prices from on_trade function with amount_a and amount_b equal to zero
- severity: Low Risk and Non-Critical (section-level rating; sponsor marked "Oracle 2 - Okay")
- component: `pallets/ema-oracle` — `on_trade`
- root_cause: `on_trade` accepts zero trade amounts and records them as a valid price observation.
- missing_control: Zero-amount rejection in `on_trade` before the oracle entry is accumulated
- interaction_scope: single_contract
- contract_set: pallet-ema-oracle
- entry_surface: oracle hook `on_trade` invoked by the AMM adapter
- trigger_primitive: A trade with `amount_a == 0 && amount_b == 0` reaching the oracle adapter
- preconditions: internal — caller adapter passes zero amounts
- sink: Oracle input-validity invariant — zero-volume observations pollute the EMA
- impact: Invalid price entries stored from zero-amount trades
- code: |
    // We assume that zero liquidity values are not valid and 
    if amount_a.is_zero() && amount_b.is_zero
                            log::warn!(
                                    target: LOG_TARGET,
    "trade amounts should not be zero. Source:
                            );
    return Err((Self::on_trade_weight
                    }
- code_keywords: on_trade, on_trade_weight, amount_a, amount_b, is_zero, LOG_TARGET, log::warn, Source

### F: (QA) 1. Should check that the amounts to be added or subtracted are greater than zero before executing the rest of the function and update the values
- severity: Low Risk and Non-Critical (section-level rating; sponsor marked "Circuit breaker 1 - Okay")
- component: `pallets/circuit-breaker` — `ensure_and_update_trade_volume_limit`, `ensure_and_update_add_liquidity_limit`
- root_cause: Circuit-breaker accounting functions mutate the per-block allowed ranges without first validating that `amount_in`/`amount_out`/`liquidity_added` are non-zero.
- missing_control: `ensure!(!amount_out.is_zero() && !amount_in.is_zero(), Error::<T>::invalidValues)` before updating limits
- interaction_scope: single_contract
- contract_set: pallet-circuit-breaker (`AllowedTradeVolumeLimitPerAsset`, `LiquidityLimitNotStored`), pallet-omnipool hub asset
- entry_surface: internal trait calls invoked from Omnipool/Stableswap trade and liquidity hooks
- trigger_primitive: Zero-amount trade or liquidity operation reaching the circuit breaker
- preconditions: internal — a caller path that can produce zero amounts
- sink: Circuit-breaker accounting correctness — limits updated on non-events
- impact: Incorrect/degenerate limit accounting (reported as QA, no demonstrated loss)
- code: |
    fnensure_and_update_trade_volume_limit(
                    asset_in: T::AssetId,
                    amount_in: T::Balance,
                    asset_out: T::AssetId,
                    amount_out: T::Balance,
            ) -> DispatchResult {
    // liquidity in
    // ignore Omnipool's hub asset
    if asset_in != T::OmnipoolHubAsset::get() {
    letmut allowed_liquidity_range = Pallet::<T>::
                                    .ok_or(Error::<T>::LiquidityLimitNotStored
                            allowed_liquidity_range.update_amounts
                            allowed_liquidity_range.check_limits
                            <AllowedTradeVolumeLimitPerAsset<T>>::
                    }

    ensure!(
    !amount_out.is_zero() && !amount_in.
    Error::<T>::invalidValues
    );
- code_keywords: ensure_and_update_trade_volume_limit, ensure_and_update_add_liquidity_limit, ensure_and_update_remove_liquidity_limit, AllowedTradeVolumeLimitPerAsset, LiquidityLimitNotStored, OmnipoolHubAsset, update_amounts, check_limits, invalidValues

### F: (QA) 2. Potential liquidity addition freeze in Omnipool due to limited add functionality by the circuit breaker
- severity: Low Risk and Non-Critical (section-level rating; sponsor marked "Circuit breaker 1 - Not clear")
- component: `pallets/circuit-breaker` — `calculate_and_store_liquidity_limits` / `calculate_limit`; interacts with Omnipool `MinimumPoolLiquidity`
- root_cause: Omnipool enforces a flat 1,000,000 minimum for add/remove liquidity, while the circuit breaker derives its per-block add-liquidity cap as a percentage (default 5%) of current liquidity. With a pool seeded at exactly `MinimumPoolLiquidity`, the derived cap (5,000) is below the minimum any LP is allowed to add, so no add-liquidity call can ever succeed.
- missing_control: A floor on the computed circuit-breaker limit (`if max_limit < 1_000_000 { max_limit = 1_000_000 }`) — i.e. reconciling the two independent limit systems
- interaction_scope: multi_contract
- contract_set: pallet-circuit-breaker (`AllowedAddLiquidityAmountPerAsset`, `DefaultMaxAddLiquidityLimitPerBlock`), pallet-omnipool (`MinimumPoolLiquidity`, `add_liquidity`)
- entry_surface: extrinsic `Omnipool::add_liquidity` gated by the circuit-breaker limit initialized at `add_token` time
- trigger_primitive: Token added with initial liquidity equal to `MinimumPoolLiquidity`, making the derived per-block add cap smaller than the per-call minimum
- preconditions: internal — default 5% add-liquidity limit and 1,000,000 minimum pool liquidity
- sink: Limit-system compatibility invariant — the two independent bounds create an empty feasible region
- impact: Liquidity addition permanently frozen for that asset (DoS of `add_liquidity`)
- code: |
            fn calculate_and_store_liquidity_limits(asset_id: T::AssetId, init
                    // we don't track liquidity limits for the Omnipool Hub as
                    if asset_id == T::OmnipoolHubAsset::get() {
                            return Ok(());
                    }
                    // add liquidity
                    if let Some(limit) = Pallet::<T>::add_liquidity_limit_per_
                            if !<AllowedAddLiquidityAmountPerAsset<T>>::contai
                                    let max_limit = Self::calculate_limit(init
    +                 if (max_limit < 1_000_000) {
    +                  max_limit = 1_000_000 ; 
    +                 }
                                    <AllowedAddLiquidityAmountPerAsset<T>>::in
                                            asset_id,
                                            LiquidityLimit::<T> {
                                                    limit: max_limit,
                                                    liquidity: Zero::zero(),
                                            },
                                    );
                            }
                    }
- code_keywords: calculate_and_store_liquidity_limits, calculate_limit, AllowedAddLiquidityAmountPerAsset, LiquidityLimit, add_liquidity_limit_per_asset, DefaultMaxAddLiquidityLimitPerBlock, MinimumPoolLiquidity, OmnipoolHubAsset, max_limit

### F: (QA) 4. Should add require_transactional macro for the function that should perform storage update to make sure that storage mutated successfully
- severity: Low Risk and Non-Critical (section-level rating; sponsor marked "Omnipool 4 - Okay")
- component: `pallets/omnipool` — `sell_hub_asset()`
- root_cause: `sell_hub_asset` performs storage mutations and asset transfers but is not annotated `#[require_transactional]`, so per the FRAME docs there is no compile/runtime assertion that it executes inside a storage transaction.
- missing_control: `#[require_transactional]` attribute on `sell_hub_asset`
- interaction_scope: single_contract
- contract_set: pallet-omnipool
- entry_surface: internal dispatch path `sell_hub_asset(origin, who, asset_out, amount, limit)` reached from hub-asset sells
- trigger_primitive: Execution of the hub-asset sell path outside a storage transaction
- preconditions: internal — call site not wrapped in `with_transaction`/`#[transactional]`
- sink: Atomicity invariant — partial state mutation without the corresponding asset transfers
- impact: Per the warden, execution could complete "without send[ing] the assets to the protocol and to the user, which is considered loss of funds for the user and the protocol"
- code: |
    +       #[require_transactional]
            fn sell_hub_asset(
                    origin: T::RuntimeOrigin,
                    who: &T::AccountId,
                    asset_out: T::AssetId,
                    amount: Balance,
                    limit: Balance,
            ) -> DispatchResult {
- code_keywords: require_transactional, transactional, sell_hub_asset, buy_asset_for_hub_asset, buy_hub_asset, sell_asset_for_hub_asset, RuntimeOrigin, DispatchResult

---

## FILE: composable-audits-halborn-audit20221003-pallet-grandpa-light-client-bridge-pdf.md
- classification: finding
- classification_reason: Body is a Halborn security assessment with an Assessment Summary table (0 Critical / 0 High / 3 Medium / 0 Low / 0 Informational) and three fully detailed HAL-NN findings each carrying Description, Code Location, Risk Level, Recommendation, and a Remediation Plan.
- protocol: Composable Finance — Grandpa Light Client Bridge (Rust, `ComposableFi/centauri` master branch; packages `ics10-grandpa`, `light-client-common`, `grandpa-prover`, `grandpa-light-client`)
- auditor: Halborn (engineer Hossam Mohamed; reviewed by Gabi Urrutia)
- date: Date of Engagement: October 3rd, 2022 - October 27th, 2022 (remediation plan 01/13/2023; all three SOLVED - 11/03/2022)
- findings_count: 3

### F: (HAL-01) GRANDPA JUSTIFICATION - MISSING COMMIT VALIDATION
- severity: Medium (Likelihood - 3, Impact - 4)
- component: `grandpa/src/justification.rs` — `GrandpaJustification::verify` / `verify_with_voter_set`; consumes `finality_grandpa::validate_commit` and `CommitValidationResult`
- root_cause: `verify_with_voter_set` inspects only the `valid: bool` member of the `CommitValidationResult` returned by `validate_commit`. The other members that flag anomalies — `num_duplicated_precommits`, `num_equivocations`, `num_invalid_voters` — are ignored, so a commit that carries duplicated precommits, equivocations, or votes from non-set voters is still accepted as long as the precommit ghost matches the commit target.
- missing_control: Post-`validate_commit` checks rejecting the justification when `num_duplicated_precommits > 0`, `num_invalid_voters > 0` (and, by extension, `num_equivocations > 0`)
- interaction_scope: cross_chain
- contract_set: `ics10-grandpa` / `grandpa-light-client` justification verification, `finality_grandpa` crate (`validate_commit`, `CommitValidationResult`, `round::Round::import_precommit`), `AncestryChain`, `VoterSet`
- entry_surface: GRANDPA justification submitted to the light client (relayed finality proof / IBC client update message)
- trigger_primitive: Relayer/attacker submits a justification whose commit contains duplicated precommits, equivocating voters, or voters outside the authority set
- preconditions: external — attacker controls or influences the relayed justification payload
- sink: Finality-verification soundness — "just ignores possible invalid commits"; the light client accepts a commit with detected-but-unchecked defects
- impact: Invalid GRANDPA commits accepted by the bridge light client (finality/consensus verification bypass at the bridge boundary)
- code: |
    50 pub fn verify < Host >(& self , set_id : u64 , authorities : &
    ë AuthorityList ) -> Result <() , error :: Error >
    51 where
    52 Host : HostFunctions ,
    53 {
    54 let voters =
    55 VoterSet :: new ( authorities . iter () . cloned () ) .ok_or (
    ë anyhow! ( " Invalid AuthoritiesSet " ) ) ?;
    56
    57 self . v e r i f y _ w i t h _ v o t e r _ s e t:: < Host >( set_id , & voters )
    58 }
    ...
    71 let ancestry_chain = AncestryChain :: <H >:: new (& self .
    ë votes_an cestries ) ;
    72
    73 match finality_ grandpa :: validate_commit (& self . commit ,
    ë voters , & ancestry_chain ) {
    74 Ok ( ref result ) if result . is_valid () = > {} ,
    75 err = > {
    76 let result = err ?;
    77 Err ( anyhow! ( " invalid commit in grandpa
    ë justification : { result :?} " ) ) ?
    78 } ,
    79 }

    382 pub struct C o m m i t V a l i d a t i o n R e s u l t{
    383 valid : bool ,
    384 num_precommits : usize ,
    385 n u m _ d u p l i c a t e d _ p r e c o m m i t s: usize ,
    386 num _e qu iv oca ti on s : usize ,
    387 nu m _i n v al i d _v o t er s: usize ,
    388 }

    // Recommendation (Listing 4)
    1 match finality_ grandpa :: validate_commit (& self . commit ,
    ë voters , & ancestry_chain ) {
    2 Ok ( ref result ) if result . is_valid () = > {
    3 if co m mi t s _v a l id a t io n. n u m _ d u p l i c a t e d _ p r e c o m m i t s>
    ë 0 { Err ( anyhow! ( " duplicated commit in grandpa justification : {
    ë result :?} ") ) ?}
    4 if co m mi t s _v a l id a t io n. nu m _i n v al i d _v o t er s> 0 { Err (
    ë anyhow! ( " invalid voters in grandpa justification : { result :?} ") ) ?}
    5 } ,
    6 err = > {
    7 let result = err ?;
    8 Err ( anyhow! ( " invalid commit in grandpa
    ë justification : { result :?} " ) ) ?
    9 } ,
    10 }
- code_keywords: GrandpaJustification, verify, verify_with_voter_set, finality_grandpa, validate_commit, CommitValidationResult, is_valid, num_duplicated_precommits, num_equivocations, num_invalid_voters, num_precommits, AncestryChain, VoterSet, AuthorityList, AuthorityId, set_id, HostFunctions, votes_ancestries, precommit_ghost, import_precommit, SignedPrecommit, ImportResult, justification.rs

### F: (HAL-02) GRANDPA JUSTIFICATION - MISSING VOTERS VALIDATION
- severity: Medium (Likelihood - 3, Impact - 4)
- component: `grandpa/src/justification.rs` — `GrandpaJustification::verify`, construction of `VoterSet::new(authorities.iter().cloned())`
- root_cause: The `verify` function builds a `VoterSet` directly from the supplied `AuthorityList`. `VoterSet::new` does not deduplicate — it inserts entries straight into a `BTreeMap` — so a duplicated authority inflates the set's `total_weight`.
- missing_control: Duplicate-authority validation on `AuthorityList` before `VoterSet::new` is called
- interaction_scope: cross_chain
- contract_set: `ics10-grandpa` / `grandpa-light-client` justification verification, `finality_grandpa::VoterSet`, `AuthorityList`
- entry_surface: Authority-set data fed into light-client justification verification (client update / authority-set change message)
- trigger_primitive: An `AuthorityList` containing duplicate voter entries reaching `verify`
- preconditions: external — attacker can influence the authority list supplied to the light client
- sink: Voter-set weight integrity — `total_weight` no longer reflects the true distinct authority set, so the supermajority threshold is miscomputed
- impact: "Having duplicate voters could manipulate the total_weight and affect the protocol" — distorted finality threshold in the bridge light client
- code: |
    50 pub fn verify < Host >(& self , set_id : u64 , authorities : &
    ë AuthorityList ) -> Result <() , error :: Error >
    51 where
    52 Host : HostFunctions ,
    53 {
    54 let voters =
    55 VoterSet :: new ( authorities . iter () . cloned () ) .ok_or (
    ë anyhow! ( " Invalid AuthoritiesSet " ) ) ?;
    56
    57 self . v e r i f y _ w i t h _ v o t e r _ s e t:: < Host >( set_id , & voters )
    58 }
- code_keywords: GrandpaJustification, verify, VoterSet::new, AuthorityList, AuthorityId, total_weight, BTreeMap, set_id, HostFunctions, Invalid AuthoritiesSet, verify_with_voter_set, justification.rs

### F: (HAL-03) GRANDPA PROVER - DENIAL OF SERVICE
- severity: Medium (Likelihood - 2, Impact - 5)
- component: `prover/src/lib.rs` — `GrandpaProver::query_finalized_parachain_headers_with_proof`
- root_cause: The function walks the relay-chain header parent chain in a `while current != previous_finalized_hash` loop, pushing every header into an unbounded `unknown_headers` vector. There is no bound on the number of iterations and no cap on the vector size, so a malicious or compromised RPC returning bogus headers can make the loop never terminate or exhaust memory.
- missing_control: An upper bound on the header range `(B; F]` — i.e. a maximum iteration count / maximum `unknown_headers` length for the parent-chain walk
- interaction_scope: cross_chain
- contract_set: `grandpa-prover` (`GrandpaProver`), relay-chain RPC client (`relay_client.rpc().header`), `GrandpaApiClient::prove_finality`, `FinalityProof`
- entry_surface: RPC — light client's relay-chain RPC connection feeding `header()` and `prove_finality` responses
- trigger_primitive: Light client connects to a malicious RPC, or an already-connected RPC is compromised, and serves invalid headers / an unbounded parent chain
- preconditions: external — malicious or compromised relay-chain RPC endpoint (auditor notes likelihood is low because it requires this)
- sink: Prover liveness/termination — the parent-hash walk never reaches `previous_finalized_hash`
- impact: Denial of Service of the light client prover via (1) infinite loop on invalid headers or (2) Out-Of-Memory from filling `unknown_headers`
- code: |
    103 pub async fn q u e r y _ f i n a l i z e d _ p a r a c h a i n _ h e a d e r s _ w i t h _ p r o o f<H >(
    104 & self ,
    105 l a t e s t _ f i n a l i z e d _ h a s h: T :: Hash ,
    106 p r e v i o u s _ f i n a l i z e d _ h a s h: T :: Hash ,
    107 header_numbers : Vec < T :: BlockNumber > ,
    108 ) -> Result < Option < Para cha inHe ade rsWi thF ina lity Pro of <H > > ,
    ë anyhow :: Error >
    ...
    114 let header = self
    115 . relay_client
    116 . rpc ()
    117 . header ( Some ( l a t e s t _ f i n a l i z e d _ h a s h) )
    118 . await ?
    119 . ok_or_else (|| anyhow! ( " Header not found! " ) ) ?;
    120
    121 let client = unsafe { u n s a f e _ c a s t _ t o _ j s o n r p s e e _ c l i e n t(&
    ë self . relay_client ) };
    122 let encoded = GrandpaAp iClient :: < JustificationNotification
    ë , H256 , u32 >:: prove_finality (
    123 &* client ,
    124 u32 :: from (* header . number () ) ,
    125 )
    126 . await ?
    127 . ok_or_else (|| anyhow! ( " No justification found for block :
    ë {:?} " , header . hash () ) ) ?
    128 .0;
    129 let mut finality_proof = FinalityProof :: <H >:: decode (& mut &
    ë encoded [..]) ?;
    130 finality_proof . unknown_headers = {
    131 let mut unknown_headers = vec! [ H :: decode (& mut & header .
    ë encode () [..]) ?];
    132 let mut current = * header . parent_hash () ;
    133 while current != p r e v i o u s _ f i n a l i z e d _ h a s h{
    134 let header = self
    135 . relay_client
    136 . rpc ()
    137 . header ( Some ( current ) )
    138 . await ?
    139 . ok_or_else (|| anyhow! ( " Header with hash : {
    ë current :?} not found! " ) ) ?;
    140 unknown_headers . push ( H :: decode (& mut & header . encode
    ë () [..]) ?) ;
    141 current = * header . parent_hash () ;
    142 }
    143 unknown_headers
    144 };
- code_keywords: GrandpaProver, query_finalized_parachain_headers_with_proof, latest_finalized_hash, previous_finalized_hash, header_numbers, ParachainHeadersWithFinalityProof, unknown_headers, FinalityProof, parent_hash, relay_client, rpc().header, GrandpaApiClient, prove_finality, JustificationNotification, unsafe_cast_to_jsonrpsee_client, prover/src/lib.rs

---

## FILE: audit-reports-snowbridge-2024-08-10-audit-report-snowbridge-updates-2-v1-0-pdf.md
- classification: finding
- classification_reason: Body is an Oak Security audit of a scoped PR diff with a Summary of Findings table listing three numbered issues, each with an explicit `Severity:` line, a Recommendation, and a Status (Resolved / Acknowledged); no Critical/Major/Minor issues were found — all three are Informational.
- protocol: Snowbridge (Snowfork) — Polkadot↔Ethereum trustless bridge; `ethereum-client` Substrate pallet (Altair-compliant Ethereum Beacon light client) plus the Solidity BEEFY light client; repo `paritytech/polkadot-sdk`, commit `5d9826c2620aff205811edf0e6a07b55a52cbf50`, scope limited to PR #3761; fixes verified at commit `94147079c3d5a8d4e2334b346eb29850ec21e917`
- auditor: Oak Security GmbH
- date: August 10, 2024
- findings_count: 3 (all Informational — 0 Critical, 0 Major, 0 Minor)

### F: 1. Ineﬃciency in verify_execution_proof function
- severity: Informational
- component: `ethereum-client` pallet — `verify_execution_proof` in `bridges/snowbridge/parachain/pallets/ethereum-client/src/impls.rs:73-129` (refactor of the former `process_execution_header_update` in `.../src/lib.rs`)
- root_cause: The PR #3761 refactor changed the data flow so that the branch handling a missing ancestry proof (`impls.rs:116-129`) performs a full Merkle proof verification before the slot-number comparison, when only `beacon_block_root` needs to be computed to decide the case.
- missing_control: Early-exit ordering — compute `beacon_block_root` first, then check ancestry-proof presence and slot equality before doing the second Merkle proof verification
- interaction_scope: cross_chain
- contract_set: `ethereum-client` pallet (`impls.rs`, `lib.rs`), beacon header / execution header verification path
- entry_surface: Message verification path — execution headers now sent contextually with the message (`verify`), rather than pre-imported into pallet storage
- trigger_primitive: Verification of a message whose ancestry proof is absent and whose slot numbers do not match
- preconditions: internal — refactored contextual execution-header flow enabled by the Deneb Ethereum upgrade
- sink: No security invariant violated — redundant hash-tree-root / Merkle proof work (verification weight)
- impact: One unnecessary Merkle proof verification per such message; extra on-chain computation/weight
- code: |
    NO_CODE_IN_REPORT
- code_keywords: verify_execution_proof, process_execution_header_update, beacon_block_root, ancestry proof, hash tree root, Merkle proof, ethereum-client, impls.rs, slot

### F: 2. Incorrect error message
- severity: Informational
- component: `ethereum-client` pallet — `bridges/snowbridge/parachain/pallets/ethereum-client/src/impls.rs:143`, `HeaderNotFinalized` error
- root_cause: The finality check raises `HeaderNotFinalized` whenever `block_slot >= state.slot`. The `>=` folds together two distinct cases: when the slots are exactly equal the header is in fact already finalized, so the error semantics are wrong for that boundary.
- missing_control: Separate handling (and a distinct error) for the `block_slot == state.slot` boundary case, so it is rejected with the correct error message
- interaction_scope: cross_chain
- contract_set: `ethereum-client` pallet finality verification
- entry_surface: Message/header verification path in the beacon light client pallet
- trigger_primitive: Submission of a header whose `block_slot` equals `state.slot`
- preconditions: internal — equal slot numbers in the finality comparison
- sink: Error-semantics correctness at an inclusive comparison boundary (`>=` vs `>`); no exploitable impact identified by the auditor
- impact: Misleading error reported to callers in the equal-slot case; the header is already finalized
- code: |
    NO_CODE_IN_REPORT
- code_keywords: HeaderNotFinalized, block_slot, state.slot, impls.rs, ethereum-client, finalized

### F: 3. Outdated comment
- severity: Informational
- component: `ethereum-client` pallet — comment block for the `verify` function at `bridges/snowbridge/parachain/pallets/ethereum-client/src/impls.rs:14-17`
- root_cause: The doc comment still states "The execution header containing the log should be in the beacon client storage." after the audited changes removed execution-header storage entirely.
- missing_control: N/A — documentation hygiene only
- interaction_scope: single_contract
- contract_set: `ethereum-client` pallet
- entry_surface: N/A (source comment)
- trigger_primitive: N/A
- preconditions: internal — storage for execution headers removed by PR #3761
- sink: N/A — no invariant involved
- impact: Misleading documentation for maintainers/integrators
- code: |
    NO_CODE_IN_REPORT
- code_keywords: verify, impls.rs, ethereum-client, execution header, beacon client storage
