---
# Core Classification
protocol: generic
chain: everychain
category: oracle
vulnerability_type: liquidation_price_misuse

# Pattern Identity
root_cause_family: unvalidated_price_input
pattern_key: bad_price_input_to_liquidation | liquidation_engine | price_feed_read | unfair_or_avoided_liquidation

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - LiquidationEngine / MarginAccount
  - Oracle / PriceAggregator / CoreSaltyFeed
  - PythOracle
  - BetaOracleUniswapV2
  - NFTPairWithOracle (user-supplied oracle)
path_keys:
  - bad_price_input_to_liquidation | liquidate() | Oracle→MarginAccount | stale_price_forced_liquidation
  - bad_price_input_to_liquidation | loan creation | NFTPairWithOracle→Lender | malicious_oracle_evasion
  - bad_price_input_to_liquidation | liquidate() | CoreSaltyFeed→PriceAggregator | spot_manipulation_unfair_liquidation
  - bad_price_input_to_liquidation | liquidate() | BetaOracleUniswapV2→BetaBank | twap_reciprocal_underpayment

# Attack Vector Details
attack_type: data_manipulation
affected_component: liquidation_engine

# Oracle-Specific Fields
oracle_provider: pyth
oracle_attack_vector: staleness

# Technical Primitives
primitives:
  - getPriceUnsafe
  - latestRoundData
  - TWAP reciprocal
  - PriceAggregator averaging
  - staleness check
  - oracle whitelist
  - liquidation threshold
  - health factor recalculation
  - spot price

# Grep / Hunt-Card Seeds
code_keywords:
  - getPriceUnsafe
  - getUnderlyingPrice
  - latestRoundData
  - PriceAggregator
  - oracle.get
  - isLiquidatable
  - _getLiquidationInfo
  - calculate_max_liquidation
  - removeCollateral

# Impact Classification
severity: medium
impact: incorrect_pricing
financial_impact: high

# Context Tags
tags:
  - lending
  - liquidation
  - oracle
  - price_manipulation
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [O1] | reports/lending_borrowing_findings/h-01-avoidance-of-liquidation-via-malicious-oracle.md | HIGH | Code4rena (Abracadabra AbraNFT) | solodit 2126 / https://github.com/code-423n4/2022-04-abranft-findings/issues/136 |
| [O2] | reports/lending_borrowing_findings/m-1-missing-staleness-check-in-pythoracle-can-lead-to-forced-liquidations-and-th.md | MEDIUM | Sherlock (Mach Finance) | solodit 44330 / https://github.com/sherlock-audit/2024-12-mach-finance-judging/issues/41 |
| [O3] | reports/lending_borrowing_findings/h-03-the-use-of-spot-price-by-coresaltyfeed-can-lead-to-price-manipulation-and-u.md | HIGH | Code4rena (Salty.IO) | solodit 31108 / https://github.com/code-423n4/2024-01-salty-findings/issues/609 |
| [O4] | reports/lending_borrowing_findings/h01-incorrect-uniswap-price-use-discourages-liquidations.md | HIGH | OpenZeppelin (Beta Finance) | solodit 10834 |
| [O5] | reports/lending_borrowing_findings/m-01-liquidations-can-be-run-on-the-bogus-oracle-prices.md | MEDIUM | Code4rena (Hubble) | solodit 1518 / https://github.com/code-423n4/2022-02-hubble-findings/issues/46 |
| [O6] | reports/lending_borrowing_findings/h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md | HIGH | Sherlock (Sentiment Update #2) | solodit 5643 / https://github.com/sherlock-audit/2022-12-sentiment-judging/issues/ |

## Oracle-Driven Liquidation Mispricing in Lending Markets

**Liquidation and health-factor logic that consumes unvalidated, stale, manipulable, or mathematically wrong prices either liquidates healthy positions, lets borrowers dodge liquidation, or underpays liquidators until liquidations stop happening.**

### Overview

This entry covers the *lending-side consumption* of price data: how liquidation eligibility and liquidation payout math break when the price input itself is wrong. Six unique findings across 5 audit firms and 6 protocols show four failure shapes: (1) user-supplied oracles that never report a liquidatable price (evasion), (2) missing staleness checks on push-style feeds (Pyth `getPriceUnsafe`) letting an attacker cherry-pick stale-but-valid prices to force liquidations, (3) manipulable spot prices inside price aggregators making healthy positions liquidatable at attacker-chosen moments, and (4) TWAP reciprocal inversion (arithmetic vs harmonic mean) underpaying liquidators by up to 54%, discouraging liquidations. For the oracle-feed manipulation mechanics themselves (flash-loan spot pokes, LP-token pricing), see the cross-linked oracle entries — this entry is scoped to the liquidation/HF consumer.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because liquidation eligibility and payout math consume a price input without validating freshness, direction, source integrity, or manipulation cost, so attackers can trigger unfair liquidations of healthy positions, dodge their own liquidation, or make liquidation unprofitable."
- Pattern key: `bad_price_input_to_liquidation | liquidation_engine | price_feed_read | unfair_or_avoided_liquidation`
- Interaction scope: `multi_contract`
- Primary affected component(s): `liquidation trigger + liquidation payout conversion (Oracle consumer)`
- Contracts / modules involved: `Oracle/PriceAggregator, MarginAccount/LiquidationLogic, PythOracle, BetaOracleUniswapV2, NFTPairWithOracle`
- Path keys: `stale_price_forced_liquidation`, `malicious_oracle_evasion`, `spot_manipulation_unfair_liquidation`, `twap_reciprocal_underpayment`
- High-signal code keywords: `getPriceUnsafe`, `getUnderlyingPrice`, `latestRoundData`, `isLiquidatable`, `PriceAggregator`, `oracle.get`
- Severity: MEDIUM — 4/6 unique findings rated HIGH, 2 MEDIUM; family severity is the lowest unique rating (MEDIUM) per severity policy
- Typical sink / impact: `unfair liquidation of healthy accounts, liquidation evasion, liquidator underpayment, theft of collateral at non-market prices`
- Validation strength: `strong` (6 unique findings, 3+ independent audit firms — Code4rena, Sherlock, OpenZeppelin — across 6 protocols)

#### Contract / Boundary Map

- Entry surface(s): `liquidate()`, `isLiquidatable()`, `removeCollateral()` (auction-style), loan creation with oracle parameter
- Contract hop(s): `Oracle.getUnderlyingPrice -> MarginAccount.isLiquidatable -> liquidate`; `PythOracle.getPriceUnsafe -> lending core HF check`; `CoreSaltyFeed + Chainlink -> PriceAggregator average -> CollateralAndLiquidity.liquidateUser`; `BetaOracleUniswapV2.convert -> BetaBank.liquidate payout`
- Trust boundary crossed: `oracle feed read (external data)`, `user-supplied oracle address`, `TWAP direction semantics`
- Shared state or sync assumption: `liquidation threshold comparison uses a price that reflects real market value at execution time`

#### Valid Bug Signals

- Signal 1: A liquidation-eligibility or payout computation reads a price whose freshness, direction (base/quote), or source is not validated on that path.
- Signal 2: Manipulating the price input (spot poke, stale Pyth update, malicious oracle at loan creation) changes the liquidation outcome while the position's true health is unchanged.
- Signal 3: Liquidator payout computed from a derived price (e.g. `1 / TWAP`) differs materially from the true average price — check arithmetic vs harmonic mean divergence.

#### False Positive Guards

- Not this bug when: the finding is purely about the price feed being manipulated (flash-loan spot poke of a DEX pool) with no lending-side consumption flaw — that is `DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md`.
- Not this bug when: staleness/deviation checks, fallback oracles, and TWAP-vs-spot thresholds are already enforced on the liquidation path.
- Safe if: liquidation additionally requires the current price to be within a threshold of a TWAP, or uses a whitelisted oracle with heartbeat + deviation bounds.
- Requires attacker control of: a Pyth update (anyone can call `updatePriceFeeds`), the loan's oracle parameter, or enough capital to move a low-liquidity spot pool (~0.004 ETH in [O3]).

### Vulnerability Description

#### Root Cause

1. **User-supplied oracle, unagreed** [O1]: `NFTPairWithOracle` lets the borrower set `params.oracle` at loan request; `_lend` never checks `params.oracle == accepted.oracle`. A malicious oracle's `get()` never returns a rate below the liquidation threshold, so `removeCollateral` (the liquidation path) always fails its check at L288.
2. **Missing staleness check on push-style feed** [O2]: `Mach PythOracle.getPriceUnsafe()` returns any previously-posted price with its timestamp; the integration only checks `price > 0`. Unlike Chainlink (update-restricted), anyone can post a valid-but-outdated Pyth price, letting an attacker combine a Day-2 inflated borrow-asset price with a Day-3 deflated collateral price to force liquidations and extract the discount.
3. **Manipulable spot in the aggregate** [O3]: `Salty PriceAggregator` averages `CoreSaltyFeed` (an arbitrage-adjusted pool spot price) with Chainlink. Moving the spot price by ~3% costs ~0.0036 ETH at 1000 ETH pool liquidity, dragging the average below the true price so healthy pools become liquidatable — the attacker also front-runs honest liquidators for the reward (up to $500).
4. **TWAP reciprocal inversion** [O4]: `BetaOracleUniswapV2.convert` uses `1 / TWAP(WETH/toToken)` instead of `TWAP(toToken/WETH)`. The harmonic mean is below the arithmetic mean — up to 54% underpayment in volatile windows — so liquidators are systematically underpaid and stop liquidating (bad debt accrues). The Beta team accepted the risk citing small divergence in practice (~0.8% at 20% swings).
5. **Unvalidated latest answer** [O5]: `Hubble Oracle.getUnderlyingPrice` passes through `latestRoundData` answer with no nonzero/freshness/spike filtering; `isLiquidatable` and `_getLiquidationInfo` liquidate on any printed outlier (zero price, flash crash).
6. **LP-token collateral pricing** [O6]: Sentiment `wstETH/ETH` Curve LP token price is manipulable, causing unexpected liquidations of otherwise-healthy positions.

#### Attack Scenario / Path Variants

**Path A: Stale Pyth price forces liquidation of healthy positions** [O2]
Path key: `bad_price_input_to_liquidation | liquidate() | Oracle→MarginAccount | stale_price_forced_liquidation`
Entry surface: anyone calls Pyth `updatePriceFeeds` then `liquidate`
Contracts touched: `Pyth -> PythOracle -> Lending core HF -> LiquidationLogic`
Boundary crossed: `push-style oracle update (permissionless)`
1. Pyth feeds for both assets go un-updated for ~3 days (keeper outage, no sponsored feed on the chain).
2. Day 2 both assets +10%; Day 3 both -20% — attacker posts the Day-2 price for the borrow asset and the Day-3 price for the collateral.
3. HF computed from the mismatched pair drops below 1 although the true HF is above 1.
4. Attacker liquidates, extracting the liquidation discount.
5. **Impact**: theft of borrower collateral at non-market prices.

**Path B: Malicious oracle at loan creation dodges liquidation** [O1]
Path key: `bad_price_input_to_liquidation | loan creation | NFTPairWithOracle→Lender | malicious_oracle_evasion`
Entry surface: `requestLoan` with attacker-chosen oracle address
Contracts touched: `NFTPairWithOracle -> attacker oracle`
Boundary crossed: `user-supplied oracle address trusted by liquidation check`
1. Borrower requests a loan specifying their own oracle contract; lender accepts unknowingly.
2. The oracle never returns a liquidating rate on `oracle.get`.
3. `removeCollateral`'s L288 check always fails; the loan can never be liquidated.
4. **Impact**: bad debt; borrower keeps collateral upside.

**Path C: Spot-poked aggregator price triggers unfair liquidation** [O3]
Path key: `bad_price_input_to_liquidation | liquidate() | CoreSaltyFeed→PriceAggregator | spot_manipulation_unfair_liquidation`
Entry surface: swap in the underlying pool + `liquidateUser` in one tx
Contracts touched: `Pool -> CoreSaltyFeed -> PriceAggregator -> CollateralAndLiquidity.liquidateUser`
Boundary crossed: `spot pool price feeding the liquidation aggregate`
1. Real WBTC price falls 3%; Chainlink updates instantly, TWAP lags.
2. Attacker pokes CoreSaltyFeed down another ~3% (cost ~0.0036 ETH) below the lagging TWAP.
3. Aggregator average sits below true price; healthy pools read as liquidatable.
4. Attacker liquidates first and claims the liquidation reward (default max $500).
5. **Impact**: unfair liquidations; reward theft; honest liquidators outcompeted.

**Path D: Reciprocal TWAP underpays liquidators** [O4]
Path key: `bad_price_input_to_liquidation | liquidate() | BetaOracleUniswapV2→BetaBank | twap_reciprocal_underpayment`
Entry surface: `BetaBank.liquidate`
Contracts touched: `BetaOracleUniswapV2.convert -> BetaBank payout`
Boundary crossed: `price direction semantics (WETH/token vs token/WETH)`
1. Volatile window: WETH/collateral TWAP = 580, true collateral TWAP = 0.00314.
2. `convert` computes `1/580 = 0.00172` — only ~54% of the correct price.
3. Liquidator receives ~54% of intended collateral.
4. Rational liquidators stop liquidating.
5. **Impact**: undercollateralized positions unliquidated → bad debt.

#### Vulnerable Pattern Examples

**Example 1: Push-style price read with no staleness check (Mach Finance)** [MEDIUM]
```solidity
// ❌ VULNERABLE: getPriceUnsafe returns ANY previously posted price, freshness unverified
function getPrice(address priceFeed) public view returns (uint256) {
    PythStructs.Price memory price = pyth.getPriceUnsafe(priceFeed);
    // only a positivity check — no staleness, no fallback oracle
    if (price.price <= 0) revert InvalidPrice();
    return uint256(uint64(price.price)); // @audit stale price flows into HF + liquidation
}
```

**Example 2: User-supplied oracle never marks liquidatable (Abracadabra NFTPairWithOracle)** [HIGH]
```solidity
// ❌ VULNERABLE: the borrower's oracle address is trusted for liquidation checks
function _lend(...) internal {
    // no require(params.oracle == accepted.oracle)  @audit malicious oracle injection
}
function removeCollateral(...) external {
    require(oracle.get(... ) <= liquidationThreshold, "not liquidatable"); // @audit attacker oracle returns safe rate forever
}
```

**Example 3: Aggregator averages a manipulable spot (Salty)** [HIGH]
```solidity
// ❌ VULNERABLE: (manipulated spot + Chainlink) / 2 moves below true price
function getWBTCPriceInUSDS() external view returns (uint256) {
    uint256 saltyPrice = coreSaltyFeed.getPrice(...);      // pool spot, cheap to poke
    uint256 chainlinkPrice = chainlinkFeed.latestAnswer(); // instant on real moves
    return (saltyPrice + chainlinkPrice) / 2;              // @audit TWAP of nothing; attacker controls one leg
}
```

**Example 4: Reciprocal of a TWAP (Beta Finance)** [HIGH]
```solidity
// ❌ VULNERABLE: 1/TWAP(WETH/token) != TWAP(token/WETH) — harmonic vs arithmetic mean
function convert(...) external view returns (uint256) {
    uint256 wethPerToken = getTWAP(WETH, toToken);   // tracked direction only
    return amountWETH * 1e18 / wethPerToken;          // @audit underpays liquidator by up to 54%
}
```

**Example 5: Pass-through latest answer (Hubble)** [MEDIUM]
```solidity
// ❌ VULNERABLE: zero/spike prices flow straight into isLiquidatable
function getUnderlyingPrice(address token) public view returns (uint256) {
    (, int256 answer,,,) = aggregator.latestRoundData();
    return uint256(answer); // @audit no nonzero, freshness, or deviation filtering
}
```

### Impact Analysis

#### Technical Impact

- Healthy positions liquidated at non-market prices (3/6 unique findings: O2, O3, O5)
- Liquidation evasion via attacker-controlled or non-reporting price source (2/6: O1, and spot-poke variants)
- Systematic liquidator underpayment → liquidation markets stop clearing → bad debt accrual (1/6: O4)

#### Business Impact

- Direct borrower losses (collateral seized at manipulated discount; Mach fixed via staleness check + fallback oracle + push bot)
- Reward theft from honest liquidators (Salty, up to $500 per event)
- Protocol insolvency risk when liquidations are discouraged or dodged (Beta acknowledged-not-fixed; Abracadabra evasion)

#### Affected Scenarios

- Push-style oracles (Pyth) without sponsored feeds or reliable keepers
- P2P / order-book lending where loan parameters (including oracle address) are negotiated between parties
- Aggregators blending spot and feed prices
- UniswapV2 TWAP integrations converting across quote directions
- Low-liquidity early-stage pools where poke costs are dust (0.0004–0.036 ETH measured in [O3])

### Secure Implementation

**Fix 1: Staleness + fallback on push-style feeds (Mach fix)**
```solidity
// ✅ SECURE: reject stale prices; fall back rather than trust age
function getPrice(address priceFeed) public view returns (uint256) {
    PythStructs.Price memory price = pyth.getPriceNoOlderThan(priceFeed, STALENESS_THRESHOLD);
    if (price.price <= 0) revert InvalidPrice();
    return uint256(uint64(price.price));
    // plus: fallback API3 oracle when freshness criteria fail (as Mach shipped)
}
```

**Fix 2: Whitelist and pin the oracle at loan level (Abracadabra fix)**
```solidity
// ✅ SECURE: lender-approved oracle only; no per-borrower oracle injection
function _lend(...) internal {
    require(params.oracle == accepted.oracle, "oracle mismatch");
    // better: only whitelisted oracles selectable at market level
}
```

**Fix 3: Track both TWAP directions (Beta fix)**
```solidity
// ✅ SECURE: never invert a TWAP — read the actual counter-direction TWAP
uint256 tokenPerWeth = getTWAP(toToken, WETH);   // tracked separately
return amountWETH * tokenPerWeth / 1e18;
```

**Fix 4: Spike filtering on the liquidation path (Hubble recommendation)**
```solidity
// ✅ SECURE: current price must sit within a threshold of TWAP for state-changing actions
uint256 spot = getSpot(token);
uint256 twap = getTWAP(token, WINDOW);
require(spot <= twap * (1e18 + MAX_DEV) / 1e18 && spot >= twap * (1e18 - MAX_DEV) / 1e18, "price outlier");
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- liquidation eligibility reads an oracle function with "unsafe"/pass-through semantics
  (getPriceUnsafe, latestAnswer without updatedAt check)
- oracle address stored per-loan/per-position and writable by one side of the loan
- aggregator mixing a DEX spot price with a feed price by simple averaging
- TWAP values inverted (1/twap) or multiplied across different quote directions
- no deviation/staleness gate between the price read and the HF/liquidation comparison
```

#### High-Signal Grep Seeds
```
- getPriceUnsafe
- getUnderlyingPrice
- latestRoundData
- PriceAggregator
- oracle.get
- isLiquidatable
- _getLiquidationInfo
- removeCollateral
- updatePriceFeeds
```

#### Code Patterns to Look For
```
- Pattern 1: `getPriceUnsafe(` on any path feeding `liquidate` / health factor
- Pattern 2: `params.oracle` (or equivalent) stored from borrower calldata without whitelist check
- Pattern 3: `(priceA + priceB) / 2` where priceA derives from a pool spot
- Pattern 4: `1e18 / twap` or `amount / twap` where twap was fetched in the opposite direction
- Pattern 5: `latestRoundData()` return values used without checking `updatedAt`/`answer != 0`
```

#### Audit Checklist
- [ ] Who can influence every price input used at liquidation time (feed updater, pool trader, loan parameter setter)?
- [ ] Is freshness enforced per-read, with a fallback, for push-style oracles?
- [ ] Are TWAP reads always in the exact direction used, never inverted?
- [ ] Does the liquidation path have an outlier/spike filter (spot-vs-TWAP threshold) or delay mechanism?
- [ ] What is the measured manipulation cost of each spot component in the aggregate, at early-stage liquidity?

### Real-World Examples

#### Known Exploits
- Oracle-manipulation-driven lending exploits (price pokes before liquidation/borrow) are indexed in `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2023-patterns.md` and `flash-loan-oracle-manipulation.md` (122 incidents).

#### Related CVEs/Reports
- Cyfrin "Chainlink Oracle DeFi Attacks" reference cited by [O3] for stale-oracle liquidation abuse
- Mach Finance fix PR (staleness check + API3 fallback + push bot) — [O2]

### Prevention Guidelines

#### Development Best Practices
1. Treat every oracle read on the liquidation path as untrusted input: validate freshness, direction, nonzero, and deviation.
2. Never allow per-loan oracle selection by the borrower; use market-level whitelisted feeds.
3. Track TWAPs in both directions when conversions are needed; document that TWAP reciprocals are not TWAPs.
4. Measure manipulation cost of every spot-derived component against the liquidation reward it unlocks.

#### Testing Requirements
- Unit tests for: stale price rejected (Pyth `updatedAt` older than threshold); malicious oracle loan cannot dodge liquidation; liquidator payout vs true TWAP within tolerance
- Integration tests for: aggregator under spot-poke; zero-price outbreak does not trigger isLiquidatable
- Fuzzing targets: HF recomputation under adversarial (price, timestamp) pairs the attacker can post

### References

#### Technical Documentation
- Pyth `getPriceUnsafe` vs `getPriceNoOlderThan` semantics
- Chainlink OCR `latestRoundData` staleness guidance
- UniswapV2 TWAP fixed-point math (arithmetic mean caveat)

#### Security Research
- Code4rena 2024-01-salty issue #609 (spot-in-aggregator manipulation cost analysis)
- OpenZeppelin Beta Finance report (TWAP reciprocal underpayment)

### Keywords for Search

`oracle liquidation`, `stale price liquidation`, `getPriceUnsafe`, `forced liquidation`, `unfair liquidation`, `price manipulation lending`, `spot price aggregator`, `TWAP inversion`, `harmonic mean oracle`, `malicious oracle`, `oracle whitelist`, `liquidation evasion oracle`, `price spike filtering`, `Pyth staleness`, `liquidator underpayment`, `flash crash liquidation`

### Related Vulnerabilities

- [Liquidation Evasion and Borrower-Triggered Liquidation DoS](../liquidation/liquidation-evasion-dos.md)
- [Liquidation Seizure Economics Miscalculation](../liquidation/liquidation-seizure-economics.md)
- `DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md` (feed-side manipulation mechanics)
- `DB/oracle/chainlink/CHAINLINK_PRICE_FEED_VULNERABILITIES.md`
