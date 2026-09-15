# VTW Extract — substrate-l1_findings — batch-04

## FILE: zeitgeist-audit-chaintroopers-audit-report-of-zeitgeist-pm-2022-pdf.md
- classification: finding
- classification_reason: Body contains 14 originally-discovered, severity-rated vulnerabilities in Substrate pallets (`zrml/authorized`, `zrml/prediction-markets`, `zrml/swaps`) with descriptions, code, PoC tests and CVSS vectors; a retest section is appended but the bulk is original discovery.
- protocol: Zeitgeist (ZRML pallets — prediction-markets, swaps, authorized, simple-disputes, market-commons, runtime)
- auditor: Chaintroopers
- date: June 28th, 2022 (Version 1.2; assessment April 6th–April 28th 2022; retests May 14th/18th and June 28th 2022)
- findings_count: 14 (4 HIGH, 3 MEDIUM, 4 LOW, 3 INFO)

### F: [authorized] Lack of support for common authorized user in multiple markets at "authorize_market_outcome" call
- severity: HIGH
- component: `zrml/authorized` pallet — `authorize_market_outcome` dispatchable; `Outcomes` storage map; `MarketDisputeMechanism::Authorized`
- root_cause: The extrinsic does not accept a `market_id` parameter; instead it resolves the market by scanning storage with `markets.iter().find()` and unconditionally takes the *first* match on the caller's account id, so an account authorized on more than one disputed market can only ever address one of them.
- missing_control: Missing explicit `market_id` argument plus a per-market authorization check (`ensure!` that the caller is the authorized account *for the supplied market*); no bounds on how many markets may bind the same authorized account.
- interaction_scope: multi_contract
- contract_set: zrml/authorized, zrml/market-commons (Markets storage), zrml/prediction-markets (dispute lifecycle)
- entry_surface: Signed extrinsic `Authorized::authorize_market_outcome(origin, outcome)`
- trigger_primitive: Attacker creates (or mutates) a second market whose `mdm` is `MarketDisputeMechanism::Authorized(victim)` with a lower market id than the victim's legitimate market, so `iter().find()` resolves to the attacker-controlled market.
- preconditions: internal — same account authorized on >1 market; external — service permits selecting arbitrary accounts as the authorized dispute resolver
- sink: Dispute-resolution liveness invariant: an authorized resolver must always be able to write the outcome of every market it is authorized for. `Outcomes::<T>::insert(market_id, who, outcome)` writes to the wrong `market_id`.
- impact: Denial of service — the authorized user cannot set an outcome for any but one market; no event is emitted so the caller receives no feedback on which market was actually mutated; attacker-controlled market insertion can deliberately block a victim resolver.
- code: |
    File: zeitgeist/zrml/authorized/src/lib.rs
    45:     #[pallet::call]
    46:     impl<T: Config> Pallet<T> {
               ...
    50:        pub fn authorize_market_outcome(
                  ...
    53:         ) -> DispatchResult {
                       ...
    56:             let market_id = if let Some(rslt) = markets.iter().find(|el| {
    57:                 if let MarketDisputeMechanism::Authorized(ref account_id) = el.1.mdm {
    58:                     account_id == &who
    59:                 } else {
    60:                     false
    61:                 }
    62:             }) {
    63:                 rslt.0
    64:             } else {
    65:                 return Err(Error::<T>::AccountIsNotLinkedToAnyAuthorizedMarket.into());
    66:             };
    67:
    68:             Outcomes::<T>::insert(market_id, who, outcome);
- code_keywords: authorize_market_outcome, markets.iter().find, MarketDisputeMechanism::Authorized, Outcomes::<T>::insert, AccountIsNotLinkedToAnyAuthorizedMarket, market_mock, MarketIdOf, OutcomeReport, AuthorizedOutcomeReports, NotAuthorizedForThisMarket

### F: [prediction-markets] A permissionless market can be rejected in "reject_market"
- severity: HIGH
- component: `zrml/prediction-markets` pallet — `reject_market` dispatchable; `T::ApprovalOrigin`; `MarketCreation` enum
- root_cause: `reject_market` is documented as rejecting a *Proposed market of Advised type* awaiting advisory-committee approval, but it performs only an origin check and never validates `market.creation`, so the Approval Origin can reject `MarketCreation::Permissionless` markets it was never granted authority over.
- missing_control: `ensure!(m.creation == MarketCreation::Advised, Error::<T>::MarketIsNotAdvised);`
- interaction_scope: multi_contract
- contract_set: zrml/prediction-markets, zrml/market-commons (`market`, `remove_market`), Currency (`slash_reserved_named`), `T::Slash` OnUnbalanced
- entry_surface: `ApprovalOrigin`-gated extrinsic `PredictionMarkets::reject_market(origin, market_id)` (advisory committee / SUDO path)
- trigger_primitive: Holder of the Approval Origin calls `reject_market` on any permissionless market id, including an active market already carrying user positions
- preconditions: internal — market exists with `MarketCreation::Permissionless`; external — caller holds the ApprovalOrigin role
- sink: Privilege-scope invariant: the advisory committee's rejection authority must be confined to Advised markets it was asked to approve. Slashing + `remove_market` executes on out-of-scope markets.
- impact: Privilege escalation and DoS — a role holder can forcibly destroy other users' permissionless markets, slashing the creator's `AdvisoryBond` and removing the market from storage.
- code: |
    File: zeitgeist/zrml/prediction-markets/src/lib.rs
    906:
    907:         /// Rejects a market that is waiting for approval from the advisory committee.
    908:         #[pallet::weight(T::WeightInfo::reject_market())]
    909:         pub fn reject_market(origin: OriginFor<T>, market_id: MarketIdOf<T>) -> DispatchResult {
    910:             T::ApprovalOrigin::ensure_origin(origin)?;
    911:
    912:             let market = T::MarketCommons::market(&market_id)?;
    913:             let creator = market.creator;
    914:             let (imbalance, _) = CurrencyOf::<T>::slash_reserved_named(
    915:                 &RESERVE_ID,
    916:                 &creator,
    917:                 T::AdvisoryBond::get(),
    918:             );
    919:             // Slashes the imbalance.
    920:             T::Slash::on_unbalanced(imbalance);
    921:             T::MarketCommons::remove_market(&market_id)?;
    922:             Self::deposit_event(Event::MarketRejected(market_id));
    923:             Self::deposit_event(Event::MarketDestroyed(market_id));
    924:             Ok(())
    925:         }
- code_keywords: reject_market, ApprovalOrigin::ensure_origin, MarketCreation::Permissionless, MarketCreation::Advised, slash_reserved_named, AdvisoryBond, remove_market, MarketRejected, MarketDestroyed, MarketIsNotAdvised, RESERVE_ID

### F: [prediction-markets] Market state is ignored in "Report" function
- severity: HIGH
- component: `zrml/prediction-markets` pallet — `report` dispatchable; `MarketStatus` state machine; `cancel_pending_market`
- root_cause: `report` validates only that no report exists and that the *period* is closed (`ensure_market_is_closed(&market.period)`); it never checks `market.status`, so a market still in `Proposed` (Advised, never approved) can be transitioned straight to `Reported`.
- missing_control: `ensure!(m.status == MarketStatus::Active, Error::<T>::MarketIsNotActive);` — status-based state-machine guard, not just period-based
- interaction_scope: multi_contract
- contract_set: zrml/prediction-markets, zrml/market-commons (`mutate_market`, `now`), frame_system (block_number), `MarketIdsPerReportBlock`
- entry_surface: Signed extrinsic `PredictionMarkets::report(origin, market_id, outcome)`
- trigger_primitive: Any account reports an outcome on a market still in `Proposed` state, flipping `market.status` to `Reported`
- preconditions: internal — Advised market in `Proposed` state whose period has elapsed; external — none (permissionless caller when `should_check_origin` is false)
- sink: Market lifecycle invariant — only Active/closed markets may be reported; `Proposed` markets must remain cancellable by their proposer. `cancel_pending_market` then fails with "Market must be pending approval."
- impact: Griefing / DoS — the market proposer is permanently blocked from cancelling their market and reclaiming the reserved deposit; state transitions that presuppose an Active market can be circumvented.
- code: |
    File: zeitgeist/zrml/prediction-markets/src/lib.rs
    927:         /// Reports the outcome of a market.
    928:         ///
    929:         #[pallet::weight(T::WeightInfo::report())]
    930:         #[transactional]
    931:         pub fn report(
    932:             origin: OriginFor<T>,
    933:             market_id: MarketIdOf<T>,
    934:             outcome: OutcomeReport,
    935:         ) -> DispatchResult {
    936:             let sender = ensure_signed(origin.clone())?;
    937:
    938:             let current_block = <frame_system::Pallet<T>>::block_number();
    939:             let market_report = Report { at: current_block, by: sender.clone(), outcome };
    940:
    941:             T::MarketCommons::mutate_market(&market_id, |market| {
    942:                 // TODO make this a conditional check
    943:                 // ensure!(outcome <= market.outcomes(), Error::<T>::OutcomeOutOfRange);
    944:                 ensure!(market.report.is_none(), Error::<T>::MarketAlreadyReported);
    945:
    946:                 Self::ensure_market_is_closed(&market.period)?;
    947:
    948:                 let mut should_check_origin = false;
    949:                 match market.period {
    950:                     MarketPeriod::Block(ref range) => {
    951:                         if current_block <= range.end + T::ReportingPeriod::get().into() {
    952:                             should_check_origin = true;
    953:                         }
    954:                     }
    ...
    964:                 if should_check_origin {
    965:                     let sender_is_oracle = sender == market.oracle;
    966:                     let origin_has_permission = T::ResolveOrigin::ensure_origin(origin).is_ok();
    967:                     ensure!(
    968:                         sender_is_oracle || origin_has_permission,
    969:                         Error::<T>::ReporterNotOracle
    970:                     );
    971:                 }
    972:
    973:                 market.report = Some(market_report.clone());
    974:                 market.status = MarketStatus::Reported;
- code_keywords: report, ensure_market_is_closed, MarketStatus::Proposed, MarketStatus::Reported, MarketStatus::Active, cancel_pending_market, mutate_market, MarketAlreadyReported, ReporterNotOracle, ResolveOrigin, MarketIdsPerReportBlock, MarketIsNotClosed

### F: [prediction-markets] Missing transactional annotation in "create_categorical_market"
- severity: HIGH
- component: `zrml/prediction-markets` pallet — `create_categorical_market` dispatchable; `#[transactional]` macro; `reserve_named`
- root_cause: The dispatchable reserves the creator's bond via `CurrencyOf::<T>::reserve_named` and then performs further fallible work (`push_market`, `start_subsidy`) without the `#[transactional]` annotation, so on a later error the storage writes already performed are not rolled back.
- missing_control: Missing `#[transactional]` attribute on the dispatchable (atomic storage-transaction wrapper); no compensating unreserve on the error path.
- interaction_scope: multi_contract
- contract_set: zrml/prediction-markets, zrml/market-commons (`push_market`), Currency (`reserve_named`), subsidy start path
- entry_surface: Signed extrinsic `PredictionMarkets::create_categorical_market(origin, oracle, period, metadata, creation, categories, mdm, scoring_rule)`
- trigger_primitive: Any user calls the extrinsic in a configuration where a post-reserve step (`push_market` or `start_subsidy`) returns `Err`
- preconditions: internal — a fallible call after `reserve_named` fails; external — none
- sink: Atomicity invariant: a failed dispatch must leave no storage/balance effects. Reserved `ValidityBond + OracleBond` (or `AdvisoryBond + OracleBond`) stays reserved after failure.
- impact: Legitimate users' assets remain permanently reserved after a failed market creation.
- code: |
    File: zeitgeist/zrml/prediction-markets/src/lib.rs
    377:         #[pallet::weight(T::WeightInfo::create_categorical_market())]
    378:         pub fn create_categorical_market(
    379:             origin: OriginFor<T>,
    380:             oracle: T::AccountId,
    381:             period: MarketPeriod<T::BlockNumber, MomentOf<T>>,
    382:             metadata: MultiHash,
    383:             creation: MarketCreation,
    384:             categories: u16,
    385:             mdm: MarketDisputeMechanism<T::AccountId>,
    386:             scoring_rule: ScoringRule,
    387:         ) -> DispatchResultWithPostInfo {
    388:             let sender = ensure_signed(origin)?;
    389:             Self::ensure_market_is_active(&period)?;
    ...
    402:             let status: MarketStatus = match creation {
    403:                 MarketCreation::Permissionless => {
    404:                     let required_bond = T::ValidityBond::get() + T::OracleBond::get();
    405:                     CurrencyOf::<T>::reserve_named(&RESERVE_ID, &sender, required_bond)?;
    ...
    413:                 MarketCreation::Advised => {
    414:                     let required_bond = T::AdvisoryBond::get() + T::OracleBond::get();
    415:                     CurrencyOf::<T>::reserve_named(&RESERVE_ID, &sender, required_bond)?;
    416:                     MarketStatus::Proposed
    417:                 }
    418:             };
    ...
    434:             let market_id = T::MarketCommons::push_market(market.clone())?;
    435:             let mut extra_weight = 0;
    436:
    437:             if market.status == MarketStatus::CollectingSubsidy {
    438:                 extra_weight = Self::start_subsidy(&market, market_id)?;
    439:             }
- code_keywords: create_categorical_market, #[transactional], reserve_named, RESERVE_ID, ValidityBond, OracleBond, AdvisoryBond, push_market, start_subsidy, DispatchResultWithPostInfo, InvalidMultihash, MinCategories, MaxCategories

### F: [prediction-markets] Market state ignored in "reject_market" function
- severity: MEDIUM
- component: `zrml/prediction-markets` pallet — `reject_market` vs `approve_market`; `MarketStatus` guard asymmetry
- root_cause: `approve_market` enforces `ensure!(m.status == MarketStatus::Proposed, ...)` but the mirror function `reject_market` performs no status check at all, so an already-approved, actively traded, or `Reported` market can be rejected and destroyed.
- missing_control: `ensure!(m.status == MarketStatus::Proposed, Error::<T>::MarketIsNotProposed);` in `reject_market` — mirror-function guard parity with `approve_market`
- interaction_scope: multi_contract
- contract_set: zrml/prediction-markets (`reject_market`, `approve_market`), zrml/market-commons, Currency slash path
- entry_surface: `ApprovalOrigin`-gated extrinsic `PredictionMarkets::reject_market(origin, market_id)`
- trigger_primitive: ApprovalOrigin holder calls `reject_market` on a market already approved, traded (`buy_complete_set` executed by ALICE/BOB/CHARLIE) or in `Reported` phase
- preconditions: internal — market in any status other than `Proposed`; external — caller holds ApprovalOrigin
- sink: State-machine invariant: reject is only legal from `Proposed`. Approved/Reported markets get slashed and removed.
- impact: DoS — an already-approved advised market with outstanding user positions can be forcibly destroyed, including accidentally by the role holder.
- code: |
    File: zeitgeist/zrml/prediction-markets/src/lib.rs
    250:         #[pallet::weight(T::WeightInfo::approve_market())]
    251:         pub fn approve_market(
    252:             origin: OriginFor<T>,
    253:             market_id: MarketIdOf<T>,
    254:         ) -> DispatchResultWithPostInfo {
    255:             T::ApprovalOrigin::ensure_origin(origin)?;
     ...
    259:             T::MarketCommons::mutate_market(&market_id, |m| {
    260:                 ensure!(m.status == MarketStatus::Proposed, Error::<T>::MarketIsNotProposed);
       ...
    272:             })?;
- code_keywords: reject_market, approve_market, MarketStatus::Proposed, MarketIsNotProposed, InvalidMarketStatus, ApprovalOrigin, mutate_market, buy_complete_set

### F: [prediction-markets] Reject market does not manage the related outcome assets
- severity: MEDIUM
- component: `zrml/prediction-markets` pallet — `reject_market` vs `admin_destroy_market`; `T::Shares` outcome-asset accounting
- root_cause: `reject_market` removes the market from storage but, unlike `admin_destroy_market`, never iterates the market's outcome assets to destroy balances / release reserved funds — an asymmetry that becomes exploitable once a non-Proposed market (which *can* hold outcome assets) is rejectable.
- missing_control: Missing outcome-asset teardown in `reject_market` (`accounts_by_currency_id` + `T::Shares::destroy_all`) equivalent to `admin_destroy_market`'s `manage_outcome_asset` closure
- interaction_scope: multi_contract
- contract_set: zrml/prediction-markets (`reject_market`, `admin_destroy_market`), `T::Shares` (orml tokens), zrml/market-commons, zrml/swaps pool
- entry_surface: `ApprovalOrigin`-gated extrinsic `PredictionMarkets::reject_market(origin, market_id)`
- trigger_primitive: Reject a market that already has `CategoricalOutcome` / `ScalarOutcome` balances held by users (reachable via findings 5.1.2, 5.1.3, 5.2.1)
- preconditions: internal — market removed while outcome assets still outstanding; external — ApprovalOrigin caller
- sink: Asset-conservation invariant: destroying a market must destroy/settle all of its derived outcome assets and release the backing collateral. PoC shows `Tokens::free_balance(*asset, &CHARLIE) == 3 * BASE` after rejection.
- impact: Funds backing the market remain locked/reserved and orphaned outcome-asset balances survive market destruction.
- code: |
    File: zeitgeist/zrml/prediction-markets/src/lib.rs
    134:         pub fn admin_destroy_market(
    135:             origin: OriginFor<T>,
    136:             market_id: MarketIdOf<T>,
    137:         ) -> DispatchResultWithPostInfo {
    138:             T::DestroyOrigin::ensure_origin(origin)?;
    139:
                     ...
    150:             let mut outcome_assets_iter = outcome_assets.into_iter();
    151:
    152:             // Delete of this market's outcome assets.
    153:             let mut manage_outcome_asset = |asset: Asset<_>| -> usize {
    154:                 let (total_accounts, accounts) = T::Shares::accounts_by_currency_id(asset);
    155:                 share_accounts = share_accounts.saturating_add(accounts.len());
    156:                 T::Shares::destroy_all(asset, accounts.iter().cloned());
    157:                 total_accounts
    158:             };
- code_keywords: reject_market, admin_destroy_market, outcome_assets, accounts_by_currency_id, destroy_all, T::Shares, DestroyOrigin, Asset::CategoricalOutcome, Tokens::free_balance, remove_market

### F: [swaps ] Minimum amount not required in "pool_join_subsidy"
- severity: MEDIUM
- component: `zrml/swaps` pallet — `pool_join_subsidy` dispatchable; `SubsidyProviders` storage double-map; `Pools` storage
- root_cause: The dispatchable reserves `amount` of the base asset and inserts an entry into `SubsidyProviders` without requiring `amount > 0`, so a zero-value call creates a persistent storage entry backed by no reserved assets.
- missing_control: `ensure!(amount > 0, Error::<T>::NotEnoughAssets);` — zero-amount rejection before storage insertion (fixed as `ensure!(amount != Zero::zero(), Error::<T>::ZeroAmount);` plus a `MinSubsidyPerAccount` floor)
- interaction_scope: single_contract
- contract_set: zrml/swaps (`Pools`, `SubsidyProviders`), `T::Shares::reserve`
- entry_surface: Signed extrinsic `Swaps::pool_join_subsidy(origin, pool_id, amount)`
- trigger_primitive: Attacker repeatedly calls `pool_join_subsidy(pool_id, 0)` from many accounts to spam `SubsidyProviders` with empty entries
- preconditions: internal — pool uses `ScoringRule::RikiddoSigmoidFeeMarketEma` and exists; external — attacker pays only transaction fees
- sink: Storage-growth / accounting invariant: every subsidy-provider record must correspond to non-zero reserved collateral, and per-entry work must be paid for.
- impact: Resource exhaustion — unbounded empty entries in the liquidity pool that must later be iterated/processed, plus misleading `PoolJoinSubsidy` deposit events.
- code: |
    File: /zeitgeist/zrml/swaps/src/lib.rs
    396:         #[pallet::weight(T::WeightInfo::pool_join_subsidy())]
    397:         pub fn pool_join_subsidy(
    398:             origin: OriginFor<T>,
    399:             pool_id: PoolId,
    400:             amount: BalanceOf<T>,
    401:         ) -> DispatchResult {
    402:             let who = ensure_signed(origin)?;
    403:
    404:             <Pools<T>>::try_mutate(pool_id, |pool_opt| {
    405:                 let pool = pool_opt.as_mut().ok_or(Error::<T>::PoolDoesNotExist)?;
    406:
    407:                 ensure!(
    408:                     pool.scoring_rule == ScoringRule::RikiddoSigmoidFeeMarketEma,
    409:                     Error::<T>::InvalidScoringRule
    410:                 );
    411:                 let base_asset = pool.base_asset.ok_or(Error::<T>::BaseAssetNotFound)?;
    412:                 T::Shares::reserve(base_asset, &who, amount)?;
    413:
    414:                 let total_subsidy = pool.total_subsidy.ok_or(Error::<T>::PoolMissingSubsidy)?;
    415:                 let _ = <SubsidyProviders<T>>::mutate(&pool_id, &who, |user_subsidy| {
    416:                     if let Some(prev_val) = user_subsidy {
    417:                         *prev_val += amount;
    418:                     } else {
    419:                         *user_subsidy = Some(amount);
    420:                     }
    421:
    422:                     pool.total_subsidy = Some(total_subsidy + amount);
    423:                 });
- code_keywords: pool_join_subsidy, SubsidyProviders, total_subsidy, T::Shares::reserve, ScoringRule::RikiddoSigmoidFeeMarketEma, ZeroAmount, MinSubsidyPerAccount, InvalidSubsidyAmount, PoolJoinSubsidy, PoolDoesNotExist

### F: [swaps ] User defined market type in "admin_set_pool_as_stale" at "swaps"
- severity: LOW
- component: `zrml/swaps` pallet — `admin_set_pool_as_stale` / `set_pool_as_stale`; `MarketType` parameter
- root_cause: The security-relevant `market_type` is taken as a *caller-supplied parameter* rather than read from the pool entity, so the branch that retains winning/base assets (`if let MarketType::Categorical(_) = market_type`) can be skipped by passing a mismatched type.
- missing_control: Missing derivation of `market_type` from stored state (as `pool_account_id` is derived) and missing consistency check between supplied `market_type` and `outcome_report`
- interaction_scope: single_contract
- contract_set: zrml/swaps (`Pools`, `PoolStatus`), zrml/prediction-markets `MarketType`/`OutcomeReport` primitives
- entry_surface: Root-gated extrinsic `Swaps::admin_set_pool_as_stale(origin, market_type, pool_id, outcome_report)` (`ensure_root`)
- trigger_primitive: Root calls with `MarketType::Scalar(1..=2)` while supplying `OutcomeReport::Categorical(idx)`, so the categorical asset-retention branch never runs and `winning_asset` stays `Err`
- preconditions: internal — pool in `PoolStatus::Active`; external — caller is Root
- sink: Data-provenance invariant: security decisions must be made on stored state, not user-provided parameters. Result is an unexpected `WinningAssetNotFound` instead of a defined error condition.
- impact: Severity limited to Root; incorrectly typed call yields an unhandled/unexpected error path during pool staling.
- code: |
    File: zeitgeist/zrml/swaps/src/lib.rs
    085:     #[pallet::call]
    086:     impl<T: Config> Pallet<T> {
    087:         #[pallet::weight(T::WeightInfo::admin_set_pool_as_stale())]
    088:         #[frame_support::transactional]
    089:         pub fn admin_set_pool_as_stale(
    090:             origin: OriginFor<T>,
    091:             market_type: MarketType,
    092:             pool_id: PoolId,
    093:             outcome_report: OutcomeReport,
    094:         ) -> DispatchResult {
    095:             ensure_root(origin)?;
    096:             Self::set_pool_as_stale(
    097:                 &market_type,
    098:                 pool_id,
    099:                 &outcome_report,
    100:                 &Self::pool_account_id(pool_id),
    101:             )?;
    102:             Ok(())
    103:         }
- code_keywords: admin_set_pool_as_stale, set_pool_as_stale, admin_set_pool_to_stale, ensure_root, MarketType::Categorical, MarketType::Scalar, OutcomeReport::Categorical, WinningAssetNotFound, PoolStatus::Stale, InvalidStateTransition, pool_account_id

### F: [prediction-markets] Minimum amount not required in "buy_complete_set"
- severity: LOW
- component: `zrml/prediction-markets` pallet — `buy_complete_set` / `do_buy_complete_set`
- root_cause: `do_buy_complete_set` checks balance, scoring rule and market status but never rejects `amount == 0`, so a zero-amount purchase performs a full transfer + per-asset `deposit` loop and emits an event for nothing.
- missing_control: `ensure!(amount > 0, Error::<T>::NotEnoughAssets);` (fixed as `ensure!(amount != BalanceOf::<T>::zero(), Error::<T>::ZeroAmount);`)
- interaction_scope: multi_contract
- contract_set: zrml/prediction-markets, zrml/market-commons, `T::Shares::deposit`, CurrencyOf transfer
- entry_surface: Signed extrinsic `PredictionMarkets::buy_complete_set(origin, market_id, #[pallet::compact] amount)`
- trigger_primitive: Any user submits `buy_complete_set(market_id, 0)` repeatedly
- preconditions: internal — market Active with `ScoringRule::CPMM`; external — none
- sink: Weight/economic invariant: work performed per extrinsic must be paid for by a corresponding non-zero economic effect.
- impact: Limited if weights are correctly calculated; otherwise free per-asset iteration work and spurious `BoughtCompleteSet` events.
- code: |
    File: zeitgeist/zrml/prediction-markets/src/lib.rs
    1396:         pub(crate) fn do_buy_complete_set(
    1397:             who: T::AccountId,
    1398:             market_id: MarketIdOf<T>,
    1399:             amount: BalanceOf<T>,
    1400:         ) -> DispatchResultWithPostInfo {
    1401:             ensure!(CurrencyOf::<T>::free_balance(&who) >= amount, Error::<T>::NotEnoughBalance);
    1402:
    1403:             let market = T::MarketCommons::market(&market_id)?;
    1404:             ensure!(market.scoring_rule == ScoringRule::CPMM, Error::<T>::InvalidScoringRule);
    1405:             Self::ensure_market_is_active(&market.period)?;
    1406:             // The check below is primarily to ensure that the market is
    1407:             // not a pending advised market.
    1408:             ensure!(market.status == MarketStatus::Active, Error::<T>::MarketIsNotActive);
    ...
    1418:             let assets = Self::outcome_assets(market_id, &market);
    1419:             for asset in assets.iter() {
    1420:                 T::Shares::deposit(*asset, &who, amount)?;
    1421:             }
- code_keywords: buy_complete_set, do_buy_complete_set, ZeroAmount, NotEnoughBalance, NotEnoughAssets, outcome_assets, T::Shares::deposit, calculate_actual_weight, MaxCategories, ScoringRule::CPMM

### F: [prediction-markets] Admin functions without "deposit_event"
- severity: LOW
- component: `zrml/prediction-markets` pallet — `admin_move_market_to_closed`, `admin_move_market_to_resolved`; `#[pallet::event]` / `generate_deposit`
- root_cause: Privileged state-transition extrinsics mutate `market.period` / market status without calling `Self::deposit_event(...)`, and the corresponding event variants (e.g. `MarketClosed`) are not even declared in the `Event<T>` enum.
- missing_control: Missing `Self::deposit_event(Event::MarketClosed(market_id))` / `Event::MarketResolved(...)` emission on admin-triggered state transitions
- interaction_scope: single_contract
- contract_set: zrml/prediction-markets (`Event<T>` enum, admin dispatchables), zrml/market-commons `mutate_market`
- entry_surface: `CloseOrigin`-gated extrinsic `admin_move_market_to_closed(origin, market_id)`; `ResolveOrigin`-gated `admin_move_market_to_resolved`
- trigger_primitive: Admin invokes the close/resolve path; off-chain indexers observe a silent state change
- preconditions: internal — admin-origin transition executed; external — off-chain consumers rely on events
- sink: Observability invariant: every successful runtime state transition must be announced to the off-chain world via an event.
- impact: Chain explorers, dApps and users cannot detect admin-driven market lifecycle changes, undermining auditability of privileged actions.
- code: |
    File: /zeitgeist/zrml/prediction-markets/src/lib.rs
    187:         /// Allows the `CloseOrigin` to immediately move an open market to closed.
    188:         //
    189:         // ***** IMPORTANT *****
    190:         //
    191:         // Within the same block, operations that interact with the activeness of the same
    192:         // market will behave differently before and after this call.
    193:         #[pallet::weight(T::WeightInfo::admin_move_market_to_closed())]
    194:         pub fn admin_move_market_to_closed(
    195:             origin: OriginFor<T>,
    196:             market_id: MarketIdOf<T>,
    197:         ) -> DispatchResult {
    198:             T::CloseOrigin::ensure_origin(origin)?;
    199:             T::MarketCommons::mutate_market(&market_id, |m| {
    200:                 m.period = match m.period {
    201:                     MarketPeriod::Block(ref range) => {
    202:                         let current_block = <frame_system::Pallet<T>>::block_number();
    203:                         MarketPeriod::Block(range.start..current_block)
    204:                     }
    205:                     MarketPeriod::Timestamp(ref range) => {
    206:                         let now = T::MarketCommons::now();
    207:                         MarketPeriod::Timestamp(range.start..now)
    208:                     }
    209:                 };
    210:                 Ok(())
    211:             })?;
    212:             Ok(())
    213:         }
- code_keywords: admin_move_market_to_closed, admin_move_market_to_resolved, deposit_event, #[pallet::generate_deposit], Event::MarketClosed, Event::MarketResolved, CloseOrigin, ResolveOrigin, mutate_market, MarketPeriod::Block, MarketPeriod::Timestamp

### F: [prediction-markets] Market Period Upper Limits not checked
- severity: INFO
- component: `zrml/prediction-markets` pallet — market creation period validation; `report` reporting-period arithmetic; `primitives/src/constants.rs`
- root_cause: No upper bound is enforced on `range.end` at market creation, while `report` computes `range.end + reporting_period_in_ms` (where `reporting_period_in_ms = ReportingPeriod * MILLISECS_PER_BLOCK = 86_400_000`), so any `range.end > u64::MAX - 86_400_000` overflows and skips the origin validation branch.
- missing_control: `ensure_market_period_is_valid` — `ensure!(start < end, ...)` and `ensure!(end <= T::MaxMarketPeriod::get(), Error::<T>::InvalidMarketPeriod);` at creation time; saturating arithmetic in `report`
- interaction_scope: single_contract
- contract_set: zrml/prediction-markets (`create_categorical_market`, `report`), zeitgeist/primitives/src/constants.rs (`MILLISECS_PER_BLOCK`, `ReportingPeriod`)
- entry_surface: Signed extrinsic `create_categorical_market` with `MarketPeriod::Timestamp(0..u64::MAX-86400000)` or `MarketPeriod::Block(0..u64::MAX-7200)`
- trigger_primitive: User creates a market with a near-`u64::MAX` period end, then reporting arithmetic overflows
- preconditions: internal — unbounded `range.end`; external — none
- sink: Arithmetic-safety invariant: `range.end + reporting_period` must not overflow; the oracle-origin check must not be silently skipped.
- impact: Reporting can become impossible due to overflow, or the `should_check_origin` oracle-authorization branch can be bypassed when the market is closed.
- code: |
    File: zeitgeist/zrml/prediction-markets/src/lib.rs
    955:                     MarketPeriod::Timestamp(ref range) => {
    956:                         let rp_moment: MomentOf<T> = T::ReportingPeriod::get().into();
    957:                         let reporting_period_in_ms = rp_moment * MILLISECS_PER_BLOCK.into();
    958:                         if T::MarketCommons::now() <= range.end + reporting_period_in_ms {
    959:                             should_check_origin = true;
    960:                         }
    961:                     }

    File: zeitgeist/primitives/src/constants.rs
    18: pub const MILLISECS_PER_BLOCK: u32 = 12000;
    79:     pub const ReportingPeriod: u32 = BLOCKS_PER_DAY as _;
- code_keywords: MarketPeriod::Timestamp, MarketPeriod::Block, range.end, ReportingPeriod, MILLISECS_PER_BLOCK, should_check_origin, ensure_market_period_is_valid, MaxMarketPeriod, InvalidMarketPeriod, u64::MAX, saturated_into

---

## FILE: chainflip-backend-audits-multisig-kudelski-q1-2022-pdf.md
- classification: finding
- classification_reason: Body is an original code audit of Chainflip's FROST threshold-Schnorr multisig implementation with 7 severity-rated security findings plus 7 informational observations, each with location, description, recommendation and remediation status.
- protocol: Chainflip (chainflip-backend, `multisig` directory — FROST threshold Schnorr / DKG engine; state-chain pallets referenced)
- auditor: Kudelski Security (Kudelski Security Research Team, Nagravision SA)
- date: 04 May 2022 (Version 2.0; audit performed February 2022)
- findings_count: 14 (7 security-rated: 5 Medium + 2 Low; plus 7 Informational observations)

### F: Possible DoS Attack in FROST KeyGen
- severity: Medium
- component: `src/multisig/client/keygen/keygen_stages.rs` — FROST 2-round distributed key generation (Pedersen DKG + ZKP)
- root_cause: The ZKP protects only the degree-zero coefficient of each participant's local polynomial; higher-degree coefficients are unverified, so a single malicious participant can broadcast shares disconnected from the committed coefficients and complete keygen with corrupted shares.
- missing_control: Missing commitment/verification over all polynomial coefficients (e.g. broadcast `H(a1,0 || … || a i,(t-1))`), a post-DKG dummy-signing test round with culprit revelation, and a local check that the product of all `Φj(t-1)` is not the identity point.
- interaction_scope: cross_protocol
- contract_set: multisig keygen engine (`keygen_stages.rs`), FROST signing module, state-chain ceremony orchestration/banning logic
- entry_surface: DKG ceremony broadcast messages between validator nodes (keygen round 1 / round 2 share distribution)
- trigger_primitive: One malicious ceremony participant crafts arbitrary shares for other players that do not match its broadcast coefficient commitments
- preconditions: internal — participant admitted to the keygen ceremony; external — none beyond validator membership
- sink: Key-usability invariant: at the end of DKG, any authorized threshold subset must be able to produce a valid signature. Corrupted shares make correct signing impossible for every combination of parties.
- impact: Denial of service on the threshold-signing key with no immediate detection and no attribution of the culprit; the same key-generation engine is reused across other MPC protocols and products.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: keygen_stages.rs, FROST, Pedersen DKG, ZKP, rogue-key attack, polynomial coefficients, identity point, CeremonyId, dummy signing round

### F: Unsuccessful Zeroization of Random Values
- severity: Medium
- component: `src/multisig/crypto.rs` @ line 128 — `random()` scalar generator
- root_cause: `random()` creates an intermediate copy of the freshly generated secret scalar; the caller can zeroize the returned value but the temporary binding is dropped without zeroization, leaving secret material in memory.
- missing_control: Missing zeroization of (or elimination of) the temporary secret copy before the function returns
- interaction_scope: single_contract
- contract_set: multisig crypto module (scalar generation used by keygen and signing nonces)
- entry_surface: Internal API `Scalar::random(&mut Rng)` invoked during key/nonce generation
- trigger_primitive: Attacker with memory-read access to the validator node process/host recovers the un-zeroized scalar
- preconditions: internal — secret scalar copied to a stack/heap temporary; external — memory disclosure or host access
- sink: Secret-hygiene invariant: secret scalars must not outlive their scope in readable memory.
- impact: Secret values (key shares / nonces) may remain recoverable in process memory.
- code: |
    pub fn random(mut rng: &mut Rng) -> Self {
        use curv::elliptic::curves::secp256_k1::SK;

        let scalar = secp256k1::SecretKey::new(&mut rng);

        let scalar = Secp256k1Scalar::from_underlying(Some(SK(scalar)));
        Scalar(scalar)
    }
- code_keywords: crypto.rs, random(), Secp256k1Scalar, from_underlying, secp256k1::SecretKey::new, zeroize, Scalar

### F: Secret Key Shares Stored in Cleartext in Database
- severity: Medium
- component: `src/multisig/client/key_store.rs` @ line 37 — `KeyDB` / `set_key`
- root_cause: `set_key` persists `KeygenResultInfo` (the node's secret key share) into the database without encryption or authentication.
- missing_control: Missing encryption-at-rest and authentication of key shares before `db.update_key(...)`
- interaction_scope: single_contract
- contract_set: multisig `key_store.rs`, persistent DB layer (`src/multisig/db/persistent.rs`)
- entry_surface: Internal persistence path after a successful keygen ceremony
- trigger_primitive: Attacker obtains file-system/host access to the validator node machine and reads the key database
- preconditions: internal — plaintext persistence of `KeygenResultInfo`; external — node machine compromise or backup exfiltration
- sink: Key-confidentiality invariant: a node's threshold secret share must never be readable at rest.
- impact: An attacker with access to the node machine recovers the node's secret share, eroding the threshold security assumption.
- code: |
    // Save `key` under key `key_id` overwriting if exists
    pub fn set_key(&mut self, key_id: KeyId, key: KeygenResultInfo) {
        self.db.update_key(&key_id, &key);
        self.keys.insert(key_id, key);
    }
- code_keywords: key_store.rs, KeyDB, set_key, KeyId, KeygenResultInfo, update_key, persistent.rs, encryption at rest

### F: Various Vulnerabilities Found by cargo-audit
- severity: Medium
- component: Dependency tree (various) — `chrono`, `hyper`, `lru`, `time`, `tokio`, `wasmtime`
- root_cause: The project pins dependency versions carrying published RustSec advisories, including memory-safety (use-after-free, segfault), request-smuggling and data-race bugs.
- missing_control: Missing dependency-advisory gating in CI (`cargo-audit`) and missing upgrades to the advisory-recommended versions
- interaction_scope: multi_contract
- contract_set: whole chainflip-backend dependency graph (engine + state-chain node; `wasmtime` underpins the Substrate runtime executor)
- entry_surface: Any code path reaching the vulnerable crate (HTTP parsing, async channels, WASM execution, time handling)
- trigger_primitive: Attacker supplies input reaching a vulnerable dependency (e.g. crafted `Transfer-Encoding`/`Content-Length` headers into `hyper` 0.10.16)
- preconditions: internal — vulnerable versions vendored; external — reachable code path
- sink: Supply-chain integrity invariant: no dependency with a known exploitable advisory may ship.
- impact: Segfaults, use-after-free, request smuggling, data races and multiple Wasmtime vulnerabilities, severity dependent on reachability.
- code: |
    • https://rustsec.org/advisories/RUSTSEC-2021-0079
    Crate:         hyper
    Version:       0.10.16
    Title:         Integer overflow in `hyper`'s parsing of the `Transfer-Encoding` header leads to data loss
    Date:          2021-07-07
    ID:            RUSTSEC-2021-0079
    URL:           https://rustsec.org/advisories/RUSTSEC-2021-0079
    Solution:      Upgrade to >=0.14.10
    Dependency tree:
    hyper 0.10.16
    • https://rustsec.org/advisories/RUSTSEC-2021-0130
    Crate:         lru
    Version:       0.6.6
    Title:         Use after free in lru crate
    Date:          2021-12-21
    ID:            RUSTSEC-2021-0130
    URL:           https://rustsec.org/advisories/RUSTSEC-2021-0130
    Solution:      Upgrade to >=0.7.1
    • https://rustsec.org/advisories/RUSTSEC-2021-0110
    Crate:         wasmtime
    Version:       0.27.0
    Title:         Multiple Vulnerabilities in Wasmtime
    Date:          2021-09-17
    ID:            RUSTSEC-2021-0110
    URL:           https://rustsec.org/advisories/RUSTSEC-2021-0110
    Solution:      Upgrade to >=0.30.0
- code_keywords: cargo-audit, RUSTSEC-2020-0159, RUSTSEC-2021-0079, RUSTSEC-2021-0078, RUSTSEC-2021-0130, RUSTSEC-2020-0071, RUSTSEC-2021-0124, RUSTSEC-2021-0110, chrono, hyper, lru, time, tokio, wasmtime

### F: Use of Outdated, Unmaintained, or Deprecated Crates
- severity: Medium
- component: `Cargo.toml` — `tempdir`, `net2`, `failure`, `difference`, `sha2`
- root_cause: The manifest depends on crates that are officially deprecated/unmaintained (and a yanked `sha2` 0.9.5), so future vulnerabilities in them will never be patched upstream.
- missing_control: Missing dependency-maintenance policy / replacement of deprecated crates (`tempfile` for `tempdir`, `socket2` for `net2`) and pinning to non-yanked `sha2`
- interaction_scope: multi_contract
- contract_set: chainflip-backend dependency manifest (engine + multisig, incl. the `sha2` hash used by FROST)
- entry_surface: Build/dependency resolution
- trigger_primitive: Future unpatched vulnerability in an unmaintained dependency
- preconditions: internal — deprecated crates vendored; external — upstream vulnerability disclosure with no fix
- sink: Supply-chain maintainability invariant: cryptographic and infrastructure dependencies must be actively maintained.
- impact: Persistent unpatched vulnerabilities; impact severity depends on the criticality of the functions used (notably `sha2`, used cryptographically).
- code: |
    • tempdir
    Crate:         tempdir
    Version:       0.3.7
    Warning:       unmaintained
    Title:         `tempdir` crate has been deprecated; use `tempfile` instead
    Date:          2018-02-13
    ID:            RUSTSEC-2018-0017
    URL:           https://rustsec.org/advisories/RUSTSEC-2018-0017
    • net2
    Crate:         net2
    Version:       0.2.37
    Warning:       unmaintained
    Title:         `net2` crate has been deprecated; use `socket2` instead
    Date:          2020-05-01
    ID:            RUSTSEC-2020-0016
    URL:           https://rustsec.org/advisories/RUSTSEC-2020-0016
- code_keywords: Cargo.toml, tempdir, tempfile, net2, socket2, failure, difference, sha2 0.9.5, RUSTSEC-2018-0017, RUSTSEC-2020-0016, RUSTSEC-2020-0036, RUSTSEC-2020-0095, yanked

### F: 64-bit Values Clipped to 32-bit Values
- severity: Low
- component: `src/multisig/crypto.rs` @ line 141 and `src/multisig/client/common/broadcast_verification.rs` @ line 50 — `from_usize`
- root_cause: A `usize` (64-bit) argument is downcast with `a as u32` before being converted to a scalar/bigint, silently truncating values above `u32::MAX`.
- missing_control: Missing use of the full `usize` width (or an explicit bounded/checked conversion) instead of the lossy `as u32` cast
- interaction_scope: multi_contract
- contract_set: multisig `crypto.rs` scalar conversion, `broadcast_verification.rs` participant indexing
- entry_surface: Internal conversion `Scalar::from_usize(a: usize)` used in participant-index and broadcast-verification arithmetic
- trigger_primitive: Any value exceeding 32 bits passed to `from_usize`
- preconditions: internal — value > `u32::MAX`; external — none
- sink: Numeric-fidelity invariant: index-to-scalar conversions must be injective and lossless.
- impact: Unexpected behavior from silent truncation of 64-bit values.
- code: |
    pub fn from_usize(a: usize) -> Self {
        Scalar(ECScalar::from_bigint(&BigInt::from(a as u32)))
    }
- code_keywords: from_usize, ECScalar::from_bigint, BigInt::from, as u32, broadcast_verification.rs, crypto.rs

### F: Hash Values Not Mapped to Correct Group
- severity: Low
- component: `src/multisig/client/keygen/keygen_frost.rs` @ line 78 and `src/multisig/client/signing/frost.rs` @ line 151
- root_cause: 256-bit hash outputs are used directly as group elements without reduction into `Zq` / `Z*q`, so the resulting values carry modular bias.
- missing_control: Missing modular reduction of a larger hash value into the scalar field (hash-to-curve / modulo-bias avoidance procedure) before use
- interaction_scope: multi_contract
- contract_set: FROST keygen (`keygen_frost.rs`) and signing (`frost.rs`) challenge/commitment derivation
- entry_surface: Internal challenge/nonce derivation during keygen and signing ceremonies
- trigger_primitive: Statistical exploitation of biased scalar distribution
- preconditions: internal — unreduced 256-bit hash used as a field element; external — curve order not close to 2^256 (not the case for secp256k1)
- sink: Uniformity invariant: derived challenges/scalars must be uniformly distributed over the group order.
- impact: Modular bias in derived scalars; Client acknowledged and retained the approach because secp256k1's order is close enough to 2^256 for the bias to be unobservable.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: keygen_frost.rs, signing/frost.rs, Zq, Z*q, modulo bias, hash-to-curve, secp256k1 CURVE_ORDER, rejection sampling

### F: Parameters Control Left to Blockchain Governance Layer
- severity: Informational
- component: Multisig ceremony engine — participant-count limits, `CeremonyId` reuse, signer deduplication
- root_cause: Safety properties of the ceremony engine are enforced only by the higher-level blockchain governance layer rather than locally: no local cap on participants, no rejection of previously used `CeremonyId`s, and no deduplication of a signer joining a ceremony multiple times.
- missing_control: Missing lower-level enforcement — participant-count bound, monotonic/uniqueness check on `CeremonyId`, and signer-set deduplication inside the engine
- interaction_scope: cross_protocol
- contract_set: multisig ceremony engine, state-chain governance pallets (`cf-governance`, `cf-witnesser`)
- entry_surface: Ceremony requests originating from the State Chain (governance-controlled) and chain reorganizations
- trigger_primitive: A governance decision (or a local chain fork/reorg) issues a ceremony with a previously used `CeremonyId`, an excessive participant count, or a duplicated signer
- preconditions: internal — no local validation of ceremony parameters; external — governance misconfiguration or chain reorg
- sink: Ceremony-context uniqueness invariant: the ceremony context hash must be unique per ceremony; validator liveness must not depend on external parameter hygiene.
- impact: A large participant count crashes the validator; `CeremonyId` reuse makes the ceremony context hash non-unique; duplicate signers can join.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: CeremonyId, ceremony context hash, participant count, deduplication, state chain governance, validator crash

### F: On Error Management
- severity: Informational
- component: `src/multisig/client/signing/frost.rs:257`, `src/multisig/db/persistent.rs:67`, `src/multisig/client/state_runner.rs:59`
- root_cause: `expect`/`unwrap`/`assert` are used inside functions that return `Result`, so unexpected input panics the process instead of being handled; notably a State Chain request carrying a `ceremony id` different from the one previously set crashes the validator.
- missing_control: Missing error propagation via `Result` (and persistent logging of critical events) instead of panicking on attacker-influenceable input
- interaction_scope: cross_protocol
- contract_set: multisig signing module, persistent DB layer, `state_runner` ceremony state machine, State Chain request path
- entry_surface: State Chain-originated ceremony requests processed by `state_runner`
- trigger_primitive: A request with a mismatched `ceremony id` reaches `state_runner.rs:59` and triggers a panic
- preconditions: internal — unhandled panic path reachable from external input; external — malformed/unsynchronized ceremony request
- sink: Node-liveness invariant: unexpected input must not terminate the validator process or destroy in-flight ceremony state.
- impact: Validator restart, loss of all current ceremony states, and node banning/suspension by the protocol — a temporary DoS that can be applied selectively to validators.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: state_runner.rs, ceremony id, expect, unwrap, assert, panic, Result, persistent.rs, frost.rs, cf-witnesser, cf-governance

---

## FILE: composable-audits-solana-restaking-vaults-restaking-vaults-audit-pdf.md
- classification: finding
- classification_reason: Body is an original OtterSec assessment of the `emulated-light-client` / restaking Anchor program with 6 severity-rated vulnerabilities (3 CRITICAL, 2 HIGH, 1 LOW) plus 4 general findings, each with description, remediation and fix commit.
- protocol: Composable Finance — `emulated-light-client` restaking program (Solana↔Cosmos IBC bridge guest chain; `restaking/programs/restaking`)
- auditor: OtterSec (Otter Audits LLC) — Akash Gurugunti, Robert Chen
- date: February 14th, 2024 (assessment conducted January 16th–19th, 2024)
- findings_count: 10 (3 CRITICAL, 2 HIGH, 0 MEDIUM, 1 LOW, 4 INFO)

### F: Ability To Initialize Multiple Times
- severity: CRITICAL
- component: `Initialize` instruction / `staking_params` account (Anchor account constraints)
- root_cause: The `Initialize` instruction declares the staking-parameters account with `init_if_needed` instead of `init`, so the initialization path stays permanently open and anyone can re-run it with new values.
- missing_control: Missing one-shot initialization guard — use `init` (or an explicit `is_initialized` check) rather than `init_if_needed`
- interaction_scope: single_contract
- contract_set: restaking program (`Initialize` context, staking params account)
- entry_surface: Permissionless `Initialize` instruction
- trigger_primitive: Attacker repeatedly calls `Initialize` with attacker-chosen staking parameters
- preconditions: internal — account declared `init_if_needed`; external — none (no authority check)
- sink: Configuration-integrity invariant: protocol staking parameters must be settable exactly once, by the intended authority.
- impact: Unauthorized alteration of the staking configuration, affecting the entire protocol.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: Initialize, init_if_needed, init, staking_params, staking parameters, Anchor account constraint

### F: Discrepancy In Deposit Functionality
- severity: CRITICAL
- component: `deposit` instruction — `remaining_accounts`, `CpiContext`, `solana_ibc::cpi::set_stake`
- root_cause: `deposit` pulls CPI accounts straight out of `ctx.remaining_accounts` (including `remaining_accounts[3]` as the CPI program) and invokes the guest chain program with no validation of those accounts' identity or ownership; the callee `set_stake` likewise does not validate the accounts passed in `CpiContext`.
- missing_control: Missing explicit validation that the accounts in `remaining_accounts` / `CpiContext` are present, of the expected type, and correctly owned (program-id check on the CPI target)
- interaction_scope: cross_protocol
- contract_set: restaking program (`deposit`), guest chain program `solana_ibc` (`set_stake`)
- entry_surface: `deposit` instruction with attacker-supplied `remaining_accounts`
- trigger_primitive: Attacker passes substituted accounts (including a substituted CPI program at index 3) to `deposit`
- preconditions: internal — guest chain initialized (`guest_chain_program_id.is_some()`); external — attacker controls `remaining_accounts` ordering/content
- sink: Account-authenticity invariant: every account consumed by a CPI must be validated for owner and address before invocation.
- impact: Unvalidated cross-program invocation into an attacker-chosen program/accounts with the vault PDA's signer seeds.
- code: |
    pub fn deposit<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Deposit<'info>>,
    service: Option<Service>,
    amount: u64,
    ) -> Result<()> {
    [...]
    // Call Guest chain program to update the stake if the chain is initialized
    if guest_chain_program_id.is_some() {
    [...]
    let cpi_program = ctx.remaining_accounts[3].clone();
    let cpi_ctx =
    CpiContext::new_with_signer(cpi_program, cpi_accounts, seeds);
    solana_ibc::cpi::set_stake(cpi_ctx, amount as u128)?;
    }
    Ok(())
    }
- code_keywords: deposit, remaining_accounts, CpiContext::new_with_signer, solana_ibc::cpi::set_stake, guest_chain_program_id, validate_remaining_accounts, restaking/programs/restaking/src/lib.rs

### F: Missing Receipt Token Balance Check
- severity: CRITICAL
- component: `set_service` instruction — `vault_params`, `receipt_token_account`, `stake_amount`
- root_cause: `set_service` sets the service for a stake deposited before guest-chain initialization while only assuming — never checking — that the depositor's `receipt_token_account` holds a non-zero balance, so the caller is not proven to own the `vault_params` being mutated.
- missing_control: Missing explicit non-zero-balance check on the depositor's `receipt_token_account` (ownership proof) before setting the stake
- interaction_scope: single_contract
- contract_set: restaking program (`set_service`, `vault_params`, receipt token account), guest chain `set_stake` CPI
- entry_surface: `set_service` instruction
- trigger_primitive: Malicious user calls `set_service` with a genuine user's `vault_params` and an arbitrary `Service`
- preconditions: internal — stake deposited before guest chain initialization; external — attacker knows the victim's `vault_params` address
- sink: Ownership invariant: only the holder of the receipt token for a vault may set that vault's service/stake.
- impact: Attacker sets an arbitrary service and an unauthorized stake using the original depositor's `vault_params`.
- code: |
    pub fn set_service<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, SetService<'info>>,
    service: Service,
    ) -> Result<()> {
    [...]
    vault_params.service = Some(service);
    let guest_chain_program_id =
    staking_params.guest_chain_program_id.unwrap(); // Infallible
    let amount = vault_params.stake_amount;
    [...]
    }
- code_keywords: set_service, receipt_token_account, vault_params, stake_amount, guest_chain_program_id, SetService, Service

### F: Stake Mint Differentiation
- severity: HIGH
- component: `deposit` instruction → `solana_ibc::cpi::set_stake`; SPL mint decimals
- root_cause: `set_stake` is invoked with a raw `amount` and no parameter identifying the mint of the staked amount, so tokens with different decimal scales update the same stake value as if they were equivalent.
- missing_control: Missing mint identifier (or decimal normalization / decimal whitelist) in the `set_stake` CPI signature
- interaction_scope: cross_protocol
- contract_set: restaking program (`deposit`), guest chain `solana_ibc` (`set_stake`), SPL token mints
- entry_surface: `deposit` instruction with a token mint of non-standard decimals
- trigger_primitive: Deposit 10 tokens of a 2-decimal mint vs 10 tokens of a 6-decimal mint — both update the same stake value
- preconditions: internal — multiple supported mints with differing decimals; external — attacker deposits the cheapest/low-decimal mint
- sink: Stake-accounting invariant: recorded stake must be denominated consistently across mints.
- impact: Stake amount incorrectly represented (over- or under-counted) for tokens with differing decimal scales. Fixed by requiring `token_mint` to have exactly 9 decimals.
- code: |
    pub fn deposit<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Deposit<'info>>,
    service: Option<Service>,
    amount: u64,
    ) -> Result<()> {
    [...]
    // Call Guest chain program to update the stake if the chain is initialized
    if guest_chain_program_id.is_some() {
    [...]
    let cpi_program = ctx.remaining_accounts[3].clone();
    let cpi_ctx =
    CpiContext::new_with_signer(cpi_program, cpi_accounts, seeds);
    solana_ibc::cpi::set_stake(cpi_ctx, amount as u128)?;
    }
    Ok(())
    }
- code_keywords: set_stake, token_mint, decimals, deposit, solana_ibc::cpi::set_stake, amount as u128, CpiContext

### F: Lack Of Sysvar Account Validation
- severity: HIGH
- component: `deposit` and `set_service` instructions; `validate_remaining_accounts`; `solana_ibc::cpi::set_stake`
- root_cause: The instructions-sysvar account is passed through to both instructions and into the CPI, but neither `validate_remaining_accounts` nor `set_stake` validates that it is the real sysvar, so it can be replaced with an attacker-controlled account.
- missing_control: Missing explicit address check on the instructions sysvar account in `validation::validate_remaining_accounts` and in `solana_ibc::cpi::set_stake`
- interaction_scope: cross_protocol
- contract_set: restaking program (`deposit`, `set_service`, `validation::validate_remaining_accounts`), guest chain `solana_ibc::set_stake`
- entry_surface: `deposit` / `set_service` instructions carrying a spoofed instructions-sysvar account
- trigger_primitive: Attacker substitutes the instructions sysvar account to forge the introspected instruction set
- preconditions: internal — sysvar identity unchecked; external — attacker crafts a fake sysvar-shaped account
- sink: Introspection-integrity invariant: sysvar accounts used for instruction introspection must be address-verified.
- impact: Unauthorized instructions may be injected into the cross-program invocation calls.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: instructions sysvar, validate_remaining_accounts, validation::validate_remaining_accounts, solana_ibc::cpi::set_stake, deposit, set_service

### F: Potential Fund Lockup
- severity: LOW
- component: `deposit` (`service: Option<Service>`) vs `withdraw` (`is_some()` condition); `vault_params.service`
- root_cause: `deposit` stores `vault_params.service` as `None` when the caller passes `None`, while the withdrawal path assumes the service is always `Some(service)` (an `is_some()` condition), producing an unsatisfiable exit condition — a deposit/withdraw asymmetry on an optional field.
- missing_control: Missing `None`-handling in `withdraw` (or mandatory `Service` type / post-deposit `set_service` path) so every deposited state remains withdrawable
- interaction_scope: single_contract
- contract_set: restaking program (`deposit`, `withdraw`, `set_service`, `vault_params`)
- entry_surface: `deposit` instruction called with `service = None`
- trigger_primitive: User deposits without specifying a service, then attempts to withdraw
- preconditions: internal — `vault_params.service == None`; external — none
- sink: Exit-liveness invariant: every reachable deposited state must have a valid withdrawal path.
- impact: User funds locked in the vault until an additional `set_service` instruction is introduced.
- code: |
    pub fn deposit<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Deposit<'info>>,
    service: Option<Service>,
    amount: u64,
    ) -> Result<()> {
    [...]
    vault_params.service =
    if guest_chain_program_id.is_some() { service } else { None };
    [...]
    }
- code_keywords: deposit, withdraw, Option<Service>, vault_params.service, is_some(), guest_chain_program_id, set_service

### F: Missing Constraint
- severity: INFO
- component: `Withdraw` account context vs `Claim` account context — `staking_params` / `rewards_token_mint`
- root_cause: `Claim` declares `has_one = rewards_token_mint` on the `staking_params` account to bind it to the correct mint, but the parallel `Withdraw` context omits the same constraint.
- missing_control: Missing `has_one = rewards_token_mint` constraint on `staking_params` in `Withdraw`
- interaction_scope: single_contract
- contract_set: restaking program (`Withdraw`, `Claim`, `staking_params`, `rewards_token_mint`)
- entry_surface: `Withdraw` instruction account set
- trigger_primitive: Caller supplies a `rewards_token_mint` not bound to the `staking_params` account during withdrawal
- preconditions: internal — constraint present on one sibling instruction but not the other; external — none
- sink: Account-relationship invariant: the one-to-one binding between `staking_params` and `rewards_token_mint` must hold on every instruction that touches both.
- impact: Inconsistent account validation between sibling instructions (anti-pattern that may become exploitable).
- code: |
    NO_CODE_IN_REPORT
- code_keywords: Withdraw, Claim, has_one, rewards_token_mint, staking_params, Anchor constraint

---

## FILE: audit-reports-snowbridge-2025-01-07-audit-report-snowbridge-updates-3-v1-0-pdf.md
- classification: finding
- classification_reason: Body is an original delta audit of Snowbridge updates (scoped to a diff between two commits across polkadot-sdk `bridges/snowbridge` and the Snowfork Solidity contracts) with 8 severity-rated findings, recommendations and per-finding resolution status.
- protocol: Snowbridge (Snowfork) — Polkadot↔Ethereum bridge; `polkadot-sdk:bridges/snowbridge` pallets/primitives/router + `snowbridge:contracts/src` Solidity Gateway
- auditor: Oak Security GmbH
- date: January 7, 2025 (v1.0)
- findings_count: 8 (1 Major, 2 Minor, 5 Informational)

### F: Unauthorized minting of PNA assets due to missing origin validation
- severity: Major
- component: `bridges/snowbridge/primitives/router/src/outbound/mod.rs` (lines 109, 126), `bridges/snowbridge/primitives/core/src/outbound.rs:262-267`, `contracts/src/Assets.sol` mint path, Gateway `onlyGateway` modifier
- root_cause: The XCM message exporter resolves `agent_id` from the XCM origin and has it available as `self.agent_id`, but never includes it in the mint message; the `channel_id` is instead inferred directly from the XCM origin's parachain ID, so the Solidity side has no knowledge of the true origin location and can only enforce `onlyGateway` — which every agent-triggered path satisfies.
- missing_control: Missing propagation of `agent_id` into the mint command and missing origin validation against that `agent_id` on the Ethereum side (`onlyGateway` alone is insufficient)
- interaction_scope: cross_chain
- contract_set: snowbridge router `outbound/mod.rs`, primitives `core/src/outbound.rs`, Solidity `Gateway.sol` / `Assets.sol` / Gateway Proxy, per-parachain channels and agents
- entry_surface: XCM message exported from a parachain through the Snowbridge exporter → inbound command dispatched to the Gateway contract on Ethereum
- trigger_primitive: Any parachain holding a governance-created channel and agent constructs and dispatches a mint message to the Gateway contract
- preconditions: internal — channel already registered at export time; external — attacker controls a parachain with a governance-created channel/agent
- sink: Cross-chain origin-authenticity invariant: only the agent that legitimately custodies a Polkadot-native asset (PNA) may authorize minting of its Ethereum representation.
- impact: Unauthorized minting of PNA assets — any agent can trigger the mint code path and exploit Gateway Proxy permissions to execute the mint.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: agent_id, self.agent_id, channel_id, onlyGateway, Assets.sol, Gateway Proxy, PNA, outbound/mod.rs, primitives/core/src/outbound.rs, XCM origin, parachain ID

### F: Potential asset lock on AssetHub due to failure in creating wrapped token on Ethereum after token registration
- severity: Minor
- component: `polkadot-sdk:bridges/snowbridge/pallets/system/src/lib.rs:621` — `register_token`; Ethereum-side `registerForeignToken`
- root_cause: `register_token` marks a token as registered on the Snowbridge (Substrate) side immediately, assuming the corresponding wrapped-token creation will succeed on Ethereum; there is no confirmation that the Ethereum leg completed, so transfers can be accepted for a token that does not yet exist on the destination chain.
- missing_control: Missing two-phase confirmation — registration should only be considered complete once the wrapped token has been successfully created on Ethereum
- interaction_scope: cross_chain
- contract_set: snowbridge `pallets/system` (`register_token`, `AssetMetadata`), Ethereum Gateway `registerForeignToken`, relayer queue, AssetHub
- entry_surface: Root-gated extrinsic `register_token(origin, AssetMetadata)` on BridgeHub, followed by a user transfer from AssetHub
- trigger_primitive: User transfers the newly registered token from AssetHub before the registration message is executed on Ethereum, or the registration message is missed in the relayer queue
- preconditions: internal — token registered on the Substrate side only; external — relayer ordering/omission
- sink: Cross-chain registration-ordering invariant: a token must not be transferable until its wrapped representation exists on the destination chain.
- impact: User assets remain locked on AssetHub until relayers re-execute the minting transaction after proper registration on Ethereum. Status: Acknowledged — client argues `registerForeignToken` has minimal failure risk and users do not interact with Bridge Hub directly.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: register_token, AssetMetadata, registerForeignToken, pallets/system/src/lib.rs, AssetHub, relayer queue, wrapped token

### F: OPERATOR cannot be updated
- severity: Minor
- component: `snowbridge:contracts/src/Shell.sol` — `OPERATOR` role; `contracts/scripts/Deploy.sol:15`
- root_cause: The `OPERATOR` role, which can perform an upgrade of the Ethereum side of the bridge, is assigned only at deployment time and there is no rotation/update path controllable by the bridge or by Polkadot governance.
- missing_control: Missing governance-controlled setter to rotate the `OPERATOR` address (key-rotation path for a privileged upgrade role)
- interaction_scope: single_contract
- contract_set: `Shell.sol`, `Deploy.sol`, Gateway upgrade path
- entry_surface: Ethereum-side upgrade function gated by the `OPERATOR` role
- trigger_primitive: Compromise of the private key (or collusion/multi-key compromise of the MPC/multisig) controlling the `OPERATOR` account
- preconditions: internal — `OPERATOR` immutable after deployment; external — key compromise or collusion
- sink: Privileged-role rotatability invariant: any role that can upgrade the bridge must be revocable/rotatable by governance.
- impact: A malicious party with the `OPERATOR` key can upgrade the Ethereum side of the bridge to any contract, with no way to rotate the operator account. Status: Acknowledged — client states Shell is only used for initial trusted bootstrapping.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: OPERATOR, Shell.sol, Deploy.sol, upgrade, key rotation, Polkadot governance, MPC, multi-signature

### F: Unused code should be removed
- severity: Informational
- component: `contracts/src/Gateway.sol:114-121` (`onlyAgent` modifier), `Gateway.sol:586-592` (`_ensureAgentAddress`), `storage/CoreStorage.sol:16` (`agentAddresses` mapping), `Assets.sol:344` (`_isTokenRegistered`), `AgentExecutor.sol:10`, `primitives/router/src/inbound/mod.rs:135` (`UnsupportedFeeAsset`)
- root_cause: An access-control modifier (`onlyAgent`) is declared but never applied anywhere, and the entire supporting machinery (`_ensureAgentAddress`, the `agentAddresses` mapping written on lines 653 and 666) exists solely to serve that unused modifier — dead authorization scaffolding alongside unused errors and imports.
- missing_control: Either application of the `onlyAgent` modifier to the paths that require agent-level authorization, or removal of the dead code; also unused errors `AgentExecutionFailed`, `AlreadyInitialized` and `UnsupportedFeeAsset`
- interaction_scope: single_contract
- contract_set: `Gateway.sol`, `CoreStorage.sol`, `Assets.sol`, `AgentExecutor.sol`, `primitives/router/src/inbound/mod.rs`
- entry_surface: Gateway functions that write `agentAddresses` (lines 653, 666) but never gate on it
- trigger_primitive: N/A — dead code; the pattern is that declared-but-unapplied access control gives a false impression of enforcement
- preconditions: internal — modifier defined but unused; external — none
- sink: Access-control completeness invariant: a declared authorization modifier must actually gate the functions it was written for.
- impact: No direct security impact reported; reusable anti-pattern — unenforced access-control scaffolding and unused state/errors that mislead reviewers. Status: Resolved.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: onlyAgent, _ensureAgentAddress, agentAddresses, CoreStorage.sol, _isTokenRegistered, AgentExecutionFailed, AlreadyInitialized, UnsupportedFeeAsset, AgentExecutor.sol, Gateway.sol

---

## FILE: composable-audits-solana-ibc-avs-codezen-pdf.md
- classification: finding
- classification_reason: Body is an original 4-day security audit of the `cf-guest-cw` CosmWasm 08-wasm light client with 8 severity-rated findings (3 HIGH, 2 MEDIUM, 3 LOW), each with source location, description, recommendation and resolution status.
- protocol: Composable Finance — Guest Chain Light Client (`composable-ibc`, `light-clients/cf-guest-cw`; references `emulated-light-client`)
- auditor: Codezen SRLS (Christian Vari — Security Researcher; Maria Iacobelli — Technical Writer)
- date: 02/05/2024 (Rev 1.0)
- findings_count: 8 (3 HIGH, 2 MEDIUM, 3 LOW)

### F: Misbehaviours cannot be detected or reported
- severity: HIGH
- component: `light-clients/cf-guest-cw/src/contract.rs:82-85` and `:49-53` — `query_check_for_misbehaviour_msg` / `CheckForMisbehaviour` handler
- root_cause: The contract's `CheckForMisbehaviour` query handler is a `todo()!` stub, so the ibc-go `02-client` `CheckForMisbehaviour` method always returns `false` for this 08-wasm client type.
- missing_control: Missing implementation of the `CheckForMisbehaviour` message handler (removal of the `todo()!` instruction) — i.e. missing misbehaviour/equivocation detection on state updates
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` CosmWasm light client, ibc-go core `02-client` module (`UpdateClient`, `UpdateStateOnMisbehaviour`), guest chain
- entry_surface: `MsgUpdateClient` handled by `UpdateClient` → 08-wasm `CheckForMisbehaviour` contract query
- trigger_primitive: A misbehaving/equivocating guest-chain validator set submits conflicting headers; the misbehaviour is neither detected automatically nor actionable when explicitly reported
- preconditions: internal — stubbed handler; external — validator misbehaviour on the tracked chain
- sink: Light-client safety invariant: detected misbehaviour must freeze the client (`UpdateStateOnMisbehaviour` → `Frozen` status).
- impact: Misbehaviours cannot be detected and reported ones are overlooked; the client can never transition to `Frozen`, so a compromised counterparty chain keeps being trusted. Status: Resolved.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: query_check_for_misbehaviour_msg, CheckForMisbehaviour, UpdateStateOnMisbehaviour, MsgUpdateClient, UpdateClient, todo()!, 08-wasm, Frozen, contract.rs

### F: Expired clients cannot be recovered
- severity: HIGH
- component: `light-clients/cf-guest-cw/src/contract.rs` (Status query at `:133`) — `trusting_period_ns`, client `Status`
- root_cause: `UpdateClient` requires the client `Status` to be `Active`, but once `trusting_period_ns` has elapsed since the latest state update the Status query returns `Expired` and updates revert; the contract implements no recovery/substitution path (`RecoverClient`).
- missing_control: Missing `RecoverClient` (client recovery/substitution) method to restore or replace an expired client
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` light client, ibc-go core `02-client` (`UpdateClient`, `RecoverClient`)
- entry_surface: `MsgUpdateClient` after the trusting period has elapsed; governance client-recovery path (absent)
- trigger_primitive: Relayer liveness gap longer than `trusting_period_ns`
- preconditions: internal — no recovery method implemented; external — no update relayed within the trusting period
- sink: Client-liveness invariant: an expired light client must be recoverable so the IBC connection can resume.
- impact: The client is permanently stuck with no possibility of being recovered, bricking the channel/connection built on it. Status: Resolved.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: trusting_period_ns, Status, Expired, Active, UpdateClient, RecoverClient, 02-client, contract.rs:133

### F: Missing validation of state updates enables attackers to store arbitrary state
- severity: HIGH
- component: `light-clients/cf-guest-cw/src/contract.rs:58-72` — `UpdateStateMsg` / `process_update_state_msg`
- root_cause: `process_update_state_msg` accepts a new `Header` and writes the updated client state without verifying that its commitments, proofs and signatures are valid and applicable to the existing state.
- missing_control: Missing header validation (commitment/proof/signature verification against the stored consensus state) inside `process_update_state_msg`
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` light client (`contract.rs`, `state.rs`), ibc-go core 02-client, downstream connection/channel/packet verification
- entry_surface: `UpdateStateMsg` submitted via `MsgUpdateClient` to the 08-wasm contract
- trigger_primitive: Attacker submits an arbitrary/malicious `Header` that is accepted and persisted as consensus state
- preconditions: internal — no header validation; external — attacker can relay an update message
- sink: Light-client soundness invariant: stored consensus state must be cryptographically derived from the counterparty chain's actual canonical chain.
- impact: Attackers can store malicious headers in the light client and successfully prove states that are not included in the blockchain — arbitrary forged cross-chain proofs. Status: Resolved.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: UpdateStateMsg, process_update_state_msg, Header, consensus_state, client_state, contract.rs:58-72, commitments, proofs, signatures

### F: The state pruning mechanism can suffer DoS depending on the trusting period length
- severity: MEDIUM
- component: `light-clients/cf-guest-cw/src/state.rs:129-146` — `prune_oldest_consensus_state`
- root_cause: `prune_oldest_consensus_state` iterates every stored consensus state with O(n) complexity during `UpdateState` processing, and the number of entries is unbounded — it grows with the configured trusting period.
- missing_control: Missing bound on the iteration (constant-time removal of the oldest consensus state, e.g. an ordered index/pointer) — no unbounded loop in a message handler
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` light client `state.rs` (consensus-state store), `UpdateState` message path
- entry_surface: `UpdateState` message processing (every client update triggers pruning)
- trigger_primitive: Accumulated consensus states (driven by a long trusting period and frequent updates) push the pruning loop past the gas limit
- preconditions: internal — unbounded O(n) pruning loop; external — long `trusting_period_ns` / high update frequency
- sink: Gas-bounded-execution invariant: per-message work must be bounded independent of accumulated storage.
- impact: `UpdateState` transactions run out of gas and can no longer be executed, leaving a stuck and unrecoverable client. Status: Resolved.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: prune_oldest_consensus_state, consensus_state, UpdateState, state.rs:129-146, trusting period, O(n), out of gas, unbounded loop

### F: Lack of VerifyMembership and VerifyNonMembership messages implementation disables core IBC features
- severity: MEDIUM
- component: `light-clients/cf-guest-cw/src/contract.rs` — `VerifyMembership` / `VerifyNonMembership` message handlers
- root_cause: The `cf-guest-cw` light client does not implement the `VerifyMembership` and `VerifyNonMembership` messages or their proof-verification mechanisms, which ibc-go relies on to verify commitments against the consensus state.
- missing_control: Missing `VerifyMembership` and `VerifyNonMembership` handler implementations (commitment proof verification against consensus state)
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` light client, ibc-go connection/channel/packet handlers
- entry_surface: `VerifyMembership` / `VerifyNonMembership` sudo/query messages dispatched by ibc-go 08-wasm
- trigger_primitive: Any IBC handshake or packet operation that requires proof verification
- preconditions: internal — handlers unimplemented; external — none
- sink: IBC functional-completeness invariant: a light client must be able to verify membership/non-membership proofs for connections, channels and packets.
- impact: Core IBC operations for handling connections, channels and packets cannot be executed successfully — broken main feature. Status: Resolved.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: VerifyMembership, VerifyNonMembership, cf-guest-cw, ibc-go, consensus state, commitment proof, contract.rs

### F: Missing CW2 migration support
- severity: LOW
- component: `light-clients/cf-guest-cw/src/contract.rs` — contract versioning / migration entry point
- root_cause: Recent ibc-go versions allow migrating 08-wasm light-client code via `MsgMigrateContract`, but the contract does not implement the CW2 contract-version specification, so migrations proceed without version handling.
- missing_control: Missing CW2 `set_contract_version` / version check in the migrate entry point
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` contract, ibc-go 08-wasm `MsgMigrateContract` path
- entry_surface: `MsgMigrateContract` governance/admin migration message
- trigger_primitive: A light-client code update executed without version handling
- preconditions: internal — no CW2 support; external — migration performed
- sink: Upgrade-safety invariant: contract migrations must be gated on the stored contract name/version to prevent incompatible state reinterpretation.
- impact: Light-client code updates could lead to unexpected issues due to missing handling of the contract version. Status: Acknowledged.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: CW2, set_contract_version, MsgMigrateContract, 08-wasm, migrate, cf-guest-cw, contract.rs

### F: Lack of validation for client_state during contract instantiation
- severity: LOW
- component: `light-clients/cf-guest-cw/src/contract.rs:25-42` — `instantiate`, `client_state`
- root_cause: The `client_state` supplied to `instantiate` is written straight to storage with no validation, so a defective client state (e.g. `is_frozen == true`, or a degenerate `trusting_period_ns`) can be persisted at creation time.
- missing_control: Missing validation of `client_state` at instantiation — specifically `is_frozen == false` and `trusting_period_ns` greater than a minimum delta time
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` contract `instantiate`, client state storage
- entry_surface: `instantiate` entry point (client creation via ibc-go 08-wasm)
- trigger_primitive: Client created with a malformed/defective `client_state`
- preconditions: internal — no instantiation-time validation; external — client creator supplies bad parameters
- sink: Initialization-validity invariant: a client must never be instantiated into an unusable or pre-frozen state.
- impact: Malformed states stored, potentially leading to unusable clients. Status: Acknowledged.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: instantiate, client_state, is_frozen, trusting_period_ns, contract.rs:25-42, cf-guest-cw

### F: Lack of validation for consensus_state during contract instantiation
- severity: LOW
- component: `light-clients/cf-guest-cw/src/contract.rs:25-43` — `instantiate`, `consensus_state`
- root_cause: The `consensus_state` supplied to `instantiate` is written straight to storage with no validation, so defective values — notably a `timestamp_ns` set in the future — can be persisted.
- missing_control: Missing validation of `consensus_state` at instantiation, specifically verifying that `timestamp_ns` is not in the future
- interaction_scope: cross_chain
- contract_set: `cf-guest-cw` contract `instantiate`, consensus state storage, trusting-period/Status computation
- entry_surface: `instantiate` entry point (client creation via ibc-go 08-wasm)
- trigger_primitive: Client created with a future-dated `timestamp_ns`
- preconditions: internal — no instantiation-time validation; external — client creator supplies bad parameters
- sink: Timestamp-monotonicity invariant: the initial consensus timestamp must not be in the future (it drives expiry/trusting-period logic).
- impact: Defective consensus states stored, potentially leading to unusable clients. Status: Acknowledged.
- code: |
    NO_CODE_IN_REPORT
- code_keywords: instantiate, consensus_state, timestamp_ns, contract.rs:25-43, cf-guest-cw, trusting_period_ns
