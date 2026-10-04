---
# Core Classification
protocol: hydradx
chain: polkadot
category: arithmetic
vulnerability_type: rounding_error_exploitation
root_cause_family: rounding_error

# Pattern Identity
pattern_key: rounding-direction-error | Omnipool liquidity/swap math | trade or LP operation | pool drain / invariant break

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - pallet-omnipool
  - LRNA hub asset accounting
path_keys:
  - rounding-direction-error | sell/buy | rounding favoring user over pool | incremental pool drain
  - rounding-direction-error | add/remove liquidity | excess LRNA minted/burned | LIQUIDITY_EQUIVALENCE break
  - rounding-direction-error | refund_refused_asset | withdraw to any caller via AddTokenOrigin | LRNA theft
  - rounding-direction-error | same-asset swap | asset_in == asset_out | unlimited price inflation

# Attack Vector Details
attack_type: arithmetic_exploit
affected_component: AMM swap and liquidity state transitions (pallet-omnipool)

# Technical Primitives
primitives:
  - fixed_point_math
  - hub_reserve (LRNA)
  - LIQUIDITY_EQUIVALENCE
  - add_liquidity
  - remove_liquidity
  - refund_refused_asset
  - TVLCap
  - stablecoin_price
  - asset_in == asset_out

# Grep / Hunt-Card Seeds
code_keywords:
  - hub_reserve
  - LIQUIDITY_EQUIVALENCE
  - refund_refused_asset
  - AddTokenOrigin
  - add_liquidity
  - remove_liquidity
  - sell
  - TVLCap

severity: high
impact: fund_loss
language: rust
tags:
  - substrate
  - amm
  - hydradx
  - omnipool
  - rounding
  - invariant
  - lorna
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [rv3] | reports/substrate-l1_findings/hydradx-rv-omnipool-2022.md | HIGH | Runtime Verification | #3 rounding errors drain pool |
| [rv4] | reports/substrate-l1_findings/hydradx-rv-omnipool-2022.md | MEDIUM | Runtime Verification | #4 excess LRNA burned on remove liquidity breaking LIQUIDITY_EQUIVALENCE (#448/#445) |
| [rv5] | reports/substrate-l1_findings/hydradx-rv-omnipool-2022.md | MEDIUM | Runtime Verification | #5 `refund_refused_asset()` withdraws LRNA to anyone via `AddTokenOrigin` (#447/#451) |
| [rv6] | reports/substrate-l1_findings/hydradx-rv-omnipool-2022.md | LOW/INFO | Runtime Verification | #6 HDX hub-reserve overwrite |
| [rv7] | reports/substrate-l1_findings/hydradx-rv-omnipool-2022.md | HIGH | Runtime Verification | #7 sell allows asset_in == asset_out → unlimited price inflation (#436/#437) |
| [rv2] | reports/substrate-l1_findings/hydradx-rv-omnipool-2022.md | HIGH | Runtime Verification | #2 stablecoin-price TVL manipulation hits TVLCap |
| [x8] | reports/substrate-l1_findings/hydradx-c4-2401.md | HIGH | Code4rena | [H-01] An attacker possesses the capability to exhaust the entirety of liquidity within the stable swap pools by manipulating the buy function, speciﬁ |
| [x9] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-01] Users can MAKE EMA-Oracle price outdated with direct transfers to StableSwap |
| [x10] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-02] Malicious liquidity provider can put pool into highly manipulatable state |
| [x11] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-03] No slippage check in remove_liquidity function in omnipool can lead to slippage losses during liquidity withdrawal. |
| [x12] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-04] Complete liquidity removals fail from stableswap pools |
| [x13] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-05] No safe_withdrawal option in withdraw_protocol_liquidity function in omnipool can be abused by frontrunners to cause losses to the admin when r |
| [x14] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-06] complete liquidity removal will result in permanent disable of the liquidity addition and prevent minting shares for the liquidity providers. |
| [x15] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-07] Re-adding assets to the omnipool can cause a problem with the oracle |
| [x16] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-08] Storage can be bloated with low value liquidity positions |
| [x17] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-10] A huge loss of funds for all the users who try to remove liquidity after swapping got disabled at manipulated price. |
| [x18] | reports/substrate-l1_findings/chainflip-backend-audits-chainflip-backend-zellic-audit-report-pdf.md | CRITICAL | Zellic | Broker fees are not taken from swap amount |
| [x19] | reports/substrate-l1_findings/zeitgeist-audit-chaintroopers-audit-report-of-zeitgeist-pm-2022-pdf.md | MEDIUM | Chaintroopers | [swaps ] Minimum amount not required in "pool_join_subsidy" |
| [x20] | reports/substrate-l1_findings/composable-audits-halborn-audit20220730-pallets-pablov2-pdf.md | HIGH | Halborn | 3.1 (HAL-01) USERS CAN CREATE SAME PAIR POOLS WITHOUT LIMITS - HIGH Description: It was observed that, an account can create configured pool |
| [x21] | reports/substrate-l1_findings/composable-audits-halborn-audit20221129-pallet-pablo-refactoring-pdf.md | MEDIUM | Halborn | 3.1 (HAL-01) MISSING PAUSE FUNCTIONALITY - MEDIUM Description: It was observed that, pools do not have a pause functionality to protect user |
| [x22] | reports/substrate-l1_findings/composable-audits-halborn-audit20221129-pallet-pablo-refactoring-pdf.md | MEDIUM | Halborn | 3.2 (HAL-02) MULTIPLE POOLS WITH IDENTICAL CONFIGURATION ALLOWED - MEDIUM Description: It was observed that an account can create configured |
| [x23] | reports/substrate-l1_findings/composable-halborn-pablo-v2.md | HIGH | Halborn | 3.1 (HAL-01) USERS CAN CREATE SAME PAIR POOLS WITHOUT LIMITS - HIGH Description: It was observed that, an account can create configured pool |
| [x24] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Attackers can steal funds by being the ﬁrst depositor of the pool |
| [x25] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Unauthorized pool liquidation threshold modiﬁcation |
| [x26] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | The manager contract does not implement required entry points to call the controller and pool contract |
| [x27] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | Unimplemented functions in the pool contract cannot be called |
| [x48] | reports/substrate-l1_findings/hydradx-rv-stableswap-2023.md | HIGH | auditor | The asset balance of a pool can drop below the existential deposit |
| [x49] | reports/substrate-l1_findings/acala-c4-2401.md | HIGH | Code4rena | Early user can break pool via inﬂation attack due to no minimum liquidity check in the incentive contract |
| [x50] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Storage can be bloated with low liquidity positions • Low Risk and Non-Critical Issues • 01 Admin is a single point of failure • 02 Consider adding be |
| [x51] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Claiming rewards while the deduction rate is ! = 0, allows for repeated withdrawal of redistributed rewards fnpayout_reward_and_reaccumulate_reward( p |
| [x52] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Storage can be bloated with low liquidity positions Acala https://code4rena.com/reports/2024-03-acala 22 of 52 09/06/2024, 14:14 Submitted by ZanyBonz |
| [x53] | reports/substrate-l1_findings/centrifuge-srl-baseline-2022.md | MEDIUM | SRLabs | Out of bounds access could lead to DoS We discovered one case of out of bounds access in the pools pallet [5] |

## Rounding-Direction Errors and Missing Swap Guards Drain the Omnipool

**HydraDX's Omnipool rounds trade and liquidity math in the user's favor, burns excess LRNA on remove-liquidity (breaking LIQUIDITY_EQUIVALENCE), exposes an LRNA-withdraw refund path to any caller, and allows same-asset swaps that inflate price without bound** - representative of AMM pools whose rounding direction and edge-case guards are not aligned with pool-preservation invariants.

### Overview

Runtime Verification's 2022 Omnipool review found: #3 (High) rounding errors that cumulatively drain the pool; #7 (High) `sell` with `asset_in == asset_out` enables unlimited price inflation (#436/#437); #2 (High) stablecoin price manipulation to hit TVLCap; #4 excess LRNA burned on remove liquidity breaks LIQUIDITY_EQUIVALENCE (#448/#445); #5 `refund_refused_asset()` withdraws LRNA to anyone holding `AddTokenOrigin` (#447/#451); #6 HDX hub-reserve overwrite.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because fixed-point trade/LP math rounds toward the user instead of the pool, LP exits burn LRNA beyond the invariant's requirement, refund paths are callable by unprivileged origins, and swap inputs are not checked for asset_in == asset_out."
- Pattern key: `rounding-direction-error | Omnipool liquidity/swap math | trade or LP operation | pool drain / invariant break`
- Interaction scope: `single_contract`
- Primary affected component(s): `swap (sell/buy), add/remove liquidity, refund paths, hub-reserve (LRNA) accounting`
- Contracts / modules involved: `pallet-omnipool, LRNA hub asset accounting`
- Path keys: `rounding favoring user`, `excess LRNA burn`, `refund_refused_asset via AddTokenOrigin`, `same-asset swap inflation`
- High-signal code keywords: `hub_reserve, LIQUIDITY_EQUIVALENCE, refund_refused_asset, AddTokenOrigin, TVLCap`
- Typical sink / impact: `pool drain / LRNA imbalance / unbounded price inflation / TVL cap evasion`
- Validation strength: `strong` (auditor-confirmed with PR references #436/#437, #445/#447/#448/#451)

#### Contract / Boundary Map

- Entry surface(s): `sell()`, `buy()`, `add_liquidity()`, `remove_liquidity()`, `refund_refused_asset()`
- Contract hop(s): `trader -> pallet-omnipool swap/LP math -> LRNA (hub) reserve updates`
- Trust boundary crossed: `origin boundary on refund paths (AddTokenOrigin); AMM math boundary between user balance and pool reserves`
- Shared state or sync assumption: `LIQUIDITY_EQUIVALENCE invariant between asset reserves and hub (LRNA) reserves must hold across add/remove; prices derive from both`

#### Valid Bug Signals

- Signal 1: Trade math uses `div_floor`/`mul_floor` (or the equivalent fixed-point ops) such that the user's output is rounded UP or their input rounded DOWN at the pool's expense in every step ([rv3]).
- Signal 2: `remove_liquidity` burns more LRNA than the position change requires, drifting LIQUIDITY_EQUIVALENCE ([rv4], PRs #448/#445).
- Signal 3: A refund/withdraw function checks only a weak origin (`AddTokenOrigin`) rather than the position owner, letting any caller extract LRNA ([rv5], PRs #447/#451).
- Signal 4: Swap entry does not `ensure!(asset_in != asset_out)`, so same-asset trades update state without transferring value ([rv7], PRs #436/#437).

#### False Positive Guards

- Not this bug when: rounding consistently favors the pool (user rounded down) in outputs and up in inputs, verified on both sell and buy paths.
- Safe if: refund paths require the original position owner or a governance origin, and same-asset swaps are explicitly rejected.
- Requires attacker control of: ordinary trader/LP accounts (no privileged roles needed) plus, for #2, stablecoin price influence.
- Dust-only exemption does NOT apply: #3 is cumulative over many operations — repeated dust-extractions compound.

### Vulnerability Description

#### Root Cause

The Omnipool's fixed-point math chose the wrong rounding direction at several steps, so every trade leaks a tiny amount of value from the pool to the trader ([rv3]). LP exits burned excess LRNA, violating LIQUIDITY_EQUIVALENCE ([rv4]). `refund_refused_asset` trusted `AddTokenOrigin` as if it proved position ownership ([rv5]). `sell` never rejected `asset_in == asset_out`, so state updates could be driven without genuine asset exchange, inflating price without bound ([rv7]). Stablecoin-derived TVL could be manipulated to hit TVLCap ([rv2]). HDX's hub reserve could be overwritten ([rv6]).

#### Attack Scenario / Path Variants

**Path A: Cumulative rounding drain**
Path key: `rounding-direction-error | sell/buy | rounding favoring user over pool | incremental pool drain`
Entry surface: `sell()` / `buy()`
Contracts touched: `pallet-omnipool math -> asset + LRNA reserves`
1. Attacker executes many small swaps where each rounds a unit of value in the trader's favor.
2. Each trade is individually dust-sized and passes sanity checks.
3. Repeated at scale, value flows from pool reserves to the attacker — pool drain.

**Path B: Same-asset swap price inflation**
Path key: `rounding-direction-error | sell with asset_in == asset_out | no same-asset guard | unlimited price inflation`
Entry surface: `sell(asset_in = X, asset_out = X)`
1. Attacker calls `sell` with `asset_in == asset_out` (#436/#437).
2. The pool's reserve/state math executes as if a real trade occurred, without transferring value.
3. Repeated calls inflate the recorded price of X without bound — poisoning every price-dependent mechanism.

**Path C: LRNA theft via refund_refused_asset**
Path key: `rounding-direction-error | refund_refused_asset | withdraw to any caller via AddTokenOrigin | LRNA theft`
Entry surface: `refund_refused_asset()` (#447/#451)
1. Attacker invokes `refund_refused_asset` with an origin that satisfies `AddTokenOrigin` (weak check).
2. The pallet releases LRNA reserved for a token-add refusal to the caller.
3. Attacker extracts LRNA they never owned.

**Path D: TVL cap evasion via stablecoin price**
Path key: `rounding-direction-error | TVLCap valuation | manipulated stablecoin price | cap hit/evasion`
1. Attacker manipulates the stablecoin price used in TVL computation.
2. The (mis)priced TVL crosses TVLCap thresholds.
3. Protocol-level limits engage or evade, distorting risk controls ([rv2]).

#### Vulnerable Pattern Examples

**Example 1: Rounding in the trader's favor (from [rv3])** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: every step rounds toward the user, leaking pool value
let amount_out = calculate_amount_out(amount_in, reserve_in, reserve_out)
    .mul_floor(FixedU128::from_float(1.0))  // fixed-point ops
    ; // result rounded UP for the trader (or amount_in rounded DOWN at pool's expense)
// repeated dust trades compound into a pool drain
```

**Example 2: Same-asset swap accepted (from [rv7])** [Approx Vulnerability : HIGH]
```rust
// ❌ VULNERABLE: sell() lacks the asset_in != asset_out guard (#436/#437)
pub fn sell(origin: OriginFor<T>, asset_in: AssetId, asset_out: AssetId, amount: Balance) -> DispatchResult {
    let who = ensure_signed(origin)?;
    // MISSING: ensure!(asset_in != asset_out, Error::SameAsset);
    let state = load_state(asset_in, asset_out)?; // X -> X passes
    apply_trade(&who, asset_in, asset_out, amount, state)?; // state churns without value transfer
    Ok(())
}
```

**Example 3: Excess LRNA burned on remove (from [rv4])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: remove_liquidity burns more LRNA than required (#448/#445)
let lrna_to_burn = position.lrna.amount + rounding_slack; // 'slack' burned too
T::Currency::withdraw(&who, lrna_to_burn)?;               // LIQUIDITY_EQUIVALENCE drifts
// after N exits, hub reserve accounting no longer matches asset reserves
```

**Example 4: Weak-origin refund path (from [rv5])** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: refund_refused_asset trusts AddTokenOrigin (#447/#451)
pub fn refund_refused_asset(origin: T::AddTokenOrigin, asset_id: AssetId) -> DispatchResult {
    // origin proves "someone allowed to add tokens", NOT the position owner
    let lrna = RefusedAssets::<T>::take(&asset_id);
    T::Currency::deposit(&origin_account, lrna)?; // any AddTokenOrigin caller extracts LRNA
    Ok(())
}
```

### Impact Analysis

#### Technical Impact

- Cumulative pool drain via rounding ([rv3]); unbounded price corruption via same-asset swaps ([rv7]).
- LIQUIDITY_EQUIVALENCE broken across LP lifecycle ([rv4]); direct LRNA extraction ([rv5]).
- TVLCap risk controls distorted by manipulable stablecoin pricing ([rv2]).

#### Business Impact

- High severity: direct, repeatable loss of pool/LRNA value by ordinary users; price integrity failure undermines every downstream product (oracle, liquidations) using Omnipool prices.

#### Affected Scenarios

- Any AMM pallet where rounding direction is not systematically pool-favoring.
- Refund/reserved-fund paths gated by weak or wrong origins.
- Swap dispatchers missing degenerate pair checks (same asset, zero amounts).

### Secure Implementation

**Fix 1: Round toward the pool everywhere; reject degenerate pairs**
```rust
// ✅ SECURE: user outputs rounded down, inputs rounded up; same-asset rejected
pub fn sell(origin: OriginFor<T>, asset_in: AssetId, asset_out: AssetId, amount: Balance) -> DispatchResult {
    ensure!(asset_in != asset_out, Error::<T>::SameAssetSwap);       // #436 fix
    ensure!(amount > Zero::zero(), Error::<T>::ZeroAmount);
    let amount_out = calc_out(amount, reserve_in, reserve_out);       // math
    let amount_out = amount_out.floor();                              // round DOWN for user
    ensure!(amount_out > Zero::zero(), Error::<T>::InsufficientOutput);
    Ok(())
}
```

**Fix 2: Owner-gated refunds; invariant-preserving LP exits**
```rust
// ✅ SECURE: refund only to the position owner; burn exactly the invariant amount
pub fn refund_refused_asset(origin: OriginFor<T>, asset_id: AssetId) -> DispatchResult {
    let who = ensure_signed(origin)?;
    ensure!(PositionOwner::<T>::get(&asset_id) == Some(who), Error::<T>::NotOwner); // #447 fix
    let lrna = RefusedAssets::<T>::take(&asset_id);
    T::Currency::deposit(&who, lrna)
}
// remove_liquidity: burn EXACTLY position.lrna.amount — never rounding slack (#448 fix)
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- hub_reserve
- LIQUIDITY_EQUIVALENCE
- refund_refused_asset
- AddTokenOrigin
- add_liquidity
- remove_liquidity
- TVLCap
```

#### Code Patterns to Look For
```
- Pattern 1: mul_floor/div_floor applied so trader output rounds up or input rounds down at pool expense
- Pattern 2: swap entry points without ensure!(asset_in != asset_out)
- Pattern 3: refund/withdraw functions whose origin check proves a role, not asset ownership
- Pattern 4: burn/mint quantities derived from rounded intermediates rather than exact position state
```

#### Audit Checklist
- [ ] For every swap direction: does rounding favor the pool in ALL steps (sell AND buy)?
- [ ] Are same-asset and zero-amount swaps rejected at dispatch?
- [ ] Does remove_liquidity burn exactly the LRNA the position records?
- [ ] Who can call refund paths — the position owner, or any origin satisfying a role type?

### Keywords for Search

`Omnipool`, `HydraDX`, `rounding error`, `pool drain`, `LRNA`, `hub reserve`, `LIQUIDITY_EQUIVALENCE`, `same asset swap`, `asset_in == asset_out`, `refund_refused_asset`, `AddTokenOrigin`, `remove liquidity`, `TVL cap`, `stablecoin manipulation`, `AMM invariant`, `fixed point rounding`, `Runtime Verification`

### Related Vulnerabilities

- DB/substrate/oracle/ema-oracle-manipulation.md (same Omnipool, oracle side)
- DB/substrate/pallets/origin-authorization-bypass.md (weak origin gating family)
