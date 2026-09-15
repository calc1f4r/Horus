---
# Core Classification
protocol: generic
chain: everychain
category: liquidation
vulnerability_type: liquidation_evasion

# Pattern Identity
root_cause_family: liquidation_dos
pattern_key: revertible_liquidation_path | liquidation_engine | borrower_action | uncollectable_bad_debt

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - LiquidationEngine / LendingPool
  - StabilityPool
  - ERC721 collateral receiver (borrower contract)
  - StakingRewards / cooldown logic
  - Auction / DutchAuction module
  - PosManager debt-tracking module
path_keys:
  - revertible_liquidation_path | liquidate() | LiquidationEngine→ERC721_receiver | callback_revert_blocks_seizure
  - revertible_liquidation_path | depositCollateral() | StakingRewards→LiquidationEngine | cooldown_rearm_blocks_liquidation
  - revertible_liquidation_path | buyLoan() | Lender→Auction | auction_timestamp_reset_blocks_seizure
  - revertible_liquidation_path | self-liquidate(1 wei) | PosManager→LendingPool | monotonic_debt_assumption_revert
  - revertible_liquidation_path | liquidation trigger | StabilityPool→LendingPool | missing_funds_revert

# Attack Vector Details
attack_type: denial_of_service
affected_component: liquidation_engine

# Technical Primitives
primitives:
  - onERC721Received
  - safeTransferFrom
  - cooldownExpiration
  - auctionStartTimestamp
  - seizeLoan
  - buyLoan
  - debtShareToAmtCurrent
  - whole-NFT rounding
  - precisionDelta
  - StabilityPool balance check
  - InsufficientBalance

# Grep / Hunt-Card Seeds
code_keywords:
  - onERC721Received
  - safeTransferFrom
  - auctionStartTimestamp
  - seizeLoan
  - liquidateBorrower
  - cooldownExpiration
  - liquidateUser
  - batchLiquidateBorrow
  - InsufficientBalance
  - oneNFTAmount

# Impact Classification
severity: high
impact: dos
financial_impact: high

# Context Tags
tags:
  - lending
  - liquidation
  - dos
  - bad_debt
  - nft_collateral
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [E1] | reports/lending_borrowing_findings/borrower-can-prevent-hisher-loan-from-being-liquidated.md | HIGH | Codehawks (Beedle) | solodit 34504 / https://github.com/Cyfrin/2023-07-beedle |
| [E2] | reports/lending_borrowing_findings/fng-16-loans-with-cerc721-collateral-can-be-made-unliquidatable.md | HIGH | Hexens (Fungify) | solodit 62382 / https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-11-06-Fungify.md |
| [E3] | reports/lending_borrowing_findings/h-05-user-can-evade-liquidation-by-depositing-the-minimum-of-tokens-and-gain-tim.md | HIGH | Code4rena (Salty.IO) | solodit 31110 / https://github.com/code-423n4/2024-01-salty-findings/issues/312 |
| [E4] | reports/lending_borrowing_findings/h-01-liquidations-can-be-prevented-by-frontrunning-and-liquidating-1-debt-or-mor.md | HIGH | Code4rena (INIT Capital) | solodit 29589 / https://github.com/code-423n4/2023-12-initcapital-findings/issues/42 |
| [E5] | reports/lending_borrowing_findings/h-06-owner-of-a-position-can-prevent-liquidation-due-to-the-onerc721received-cal.md | HIGH | Code4rena (Revert Lend) | solodit 32266 / https://github.com/code-423n4/2024-03-revert-lend-findings/issues/54 |
| [E6] | reports/lending_borrowing_findings/any-attempt-to-liquidate-a-user-will-fail-because-stabilitypool-does-not-hold-cr.md | HIGH | Codehawks (RAAC) | solodit 57187 / https://github.com/Cyfrin/2025-02-raac |
| [E7] | reports/lending_borrowing_findings/c-01-liquidations-prevented-for-non-18-decimal-collaterals.md | HIGH | Pashov Audit Group (Gains Network) | solodit 37788 |
| [E8] | reports/lending_borrowing_findings/a-malicious-collateralized-nft-token-can-block-liquidation-and-also-epoch-proces.md | MEDIUM | Spearbit (Astaria) | solodit 21851 |

## Liquidation Evasion — Borrower Makes Their Own Position Unliquidatable

**A borrower-controlled action (callback revert, dust deposit, auction reset, wei self-liquidation, fractional collateral) makes the liquidation transaction itself revert, so underwater debt can never be collected and bad debt accrues unchecked.**

### Overview

Liquidation only protects lenders if the liquidation call succeeds. Across 8 unique findings (7 HIGH, 1 MEDIUM) from 6 audit firms and 8 protocols, borrowers or protocol design make the liquidation path revertible: ERC721 collateral return callbacks under borrower control revert, a dust collateral deposit re-arms a withdrawal cooldown that liquidation respects, borrowers reset their own Dutch auction timestamp, a 1-wei self-liquidation breaks a monotonic-debt assumption so the next liquidation reverts, whole-NFT rounding underflows on fractional NFT collateral, and a stability pool checks a balance it never holds. In every case the sink is identical: undercollateralized debt that cannot be liquidated, interest keeps accruing, and insolvency is socialized onto lenders.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because a borrower-controllable action on the liquidation code path can force a revert (callback, cooldown re-arm, timestamp reset, underflow, div-by-zero, insufficient-balance check), so undercollateralized positions become permanently unliquidatable and bad debt accrues to lenders."
- Pattern key: `revertible_liquidation_path | liquidation_engine | borrower_action | uncollectable_bad_debt`
- Interaction scope: `multi_contract`
- Primary affected component(s): `liquidation execution path (seize, collateral return, auction finalize, stability-pool trigger)`
- Contracts / modules involved: `LendingPool, StabilityPool, ERC721 collateral vault, Auction/Lender module, StakingRewards cooldown, PosManager`
- Path keys: `callback_revert_blocks_seizure`, `cooldown_rearm_blocks_liquidation`, `auction_timestamp_reset_blocks_seizure`, `monotonic_debt_assumption_revert`, `missing_funds_revert`
- High-signal code keywords: `onERC721Received`, `safeTransferFrom`, `auctionStartTimestamp`, `seizeLoan`, `cooldownExpiration`, `InsufficientBalance`
- Severity: HIGH — 7/8 unique findings rated HIGH, 1 MEDIUM (lowest unique rating MEDIUM; family rated HIGH by dominant consensus)
- Typical sink / impact: `uncollectable bad debt, protocol insolvency, borrower retains collateral upside risk-free`
- Validation strength: `strong` (8 unique findings, 6 independent audit firms — Codehawks, Code4rena, Hexens, Pashov, Spearbit — across 8 protocols)

#### Contract / Boundary Map

- Entry surface(s): `liquidate()`, `liquidateUser()`, `liquidateBorrower()`, `seizeLoan()`, borrower's `depositCollateral()`, `buyLoan()`, self-`liquidate(1)`
- Contract hop(s): `Liquidator -> LendingPool.liquidate -> ERC721.safeTransferFrom -> borrower.onERC721Received`; `Borrower.depositCollateral -> StakingRewards._increaseUserShare -> cooldown set`; `Borrower.buyLoan -> Lender.auctionStartTimestamp reset`; `StabilityPool.liquidateBorrower -> LendingPool.finalizeLiquidation`
- Trust boundary crossed: `ERC721 callback into borrower-controlled contract`, `cooldown state shared between staking and liquidation`, `auction state writable by the borrower`
- Shared state or sync assumption: `liquidation must be executable whenever HF < 1`; `auctionStartTimestamp only moves forward`; `debtShareToAmtCurrent monotonically increasing`; `stability pool holds the debt asset`

#### Valid Bug Signals

- Signal 1: Any external call inside the liquidation path whose recipient/callback is controlled by the liquidated borrower (NFT return, token with hook, recipient of seized asset) and whose revert propagates.
- Signal 2: Any borrower-writable state that the liquidation path reads as a precondition (cooldown, auction timestamp, last debt snapshot, share balance) and that can be re-armed after the position becomes unsafe.
- Signal 3: The position can become unsafe while the blocking precondition is active — i.e. evading liquidation is profitable (borrower keeps collateral upside, downside socialized).

#### False Positive Guards

- Not this bug when: collateral seizure uses `transfer()` instead of `safeTransferFrom()` for the final collateral push, or the callback return value is not required to succeed (try/catch with fallback).
- Not this bug when: cooldown/auction state can only be set by admin or keeper, not by the borrower being liquidated.
- Safe if: liquidation path performs only calls to trusted contracts (pool, oracle, treasury) and all borrower-controlled interactions are deferred to a post-seizure, non-reverting claim step.
- Dust-only impact guard: if the revert is only reachable for dust positions below the min-profit threshold of liquidators anyway, severity collapses — here the blockers affect ANY position size (2/8 findings explicitly demonstrate full-size positions).

### Vulnerability Description

#### Root Cause

Liquidation paths contain revertible steps whose preconditions are attacker-influenced:

1. **Borrower-controlled ERC721 callback** [E5]: `Revert Lend._cleanUpLoan` returns the LP NFT to the owner via `nonfungiblePositionManager.safeTransferFrom(address(this), owner, tokenId)`; a malicious owner contract returns `bytes4(0xdeadbeef)` from `onERC721Received`, so `vault.liquidate()` reverts with "transfer to non ERC721Receiver implementer".
2. **Cooldown re-arm via dust deposit** [E3]: `Salty.depositCollateralAndIncreaseShare` sets `user.cooldownExpiration = block.timestamp + modificationCooldown()` for any nonzero deposit; `liquidateUser` must wait for cooldown expiry, so front-running any liquidation with a DUST+1 deposit reverts it.
3. **Auction timestamp reset** [E1]: `Beedle.buyLoan(loanId, samePoolId)` sets `loan.auctionStartTimestamp = type(uint256).max`; `seizeLoan` reverts while the timestamp is at max, so the borrower repeatedly buys their own loan to stay unseizable.
4. **Monotonic debt assumption broken by wei self-liquidation** [E4]: `INIT PosManager.updatePosDebtShares` assumes `debtShareToAmtCurrent` only grows; a 1-wei self-liquidation reduces it, and same-block (no accrual) follow-up liquidations revert — the borrower self-liquidates 1 wei to block every liquidation attempt.
5. **Fractional NFT collateral vs whole-NFT rounding** [E2]: `Fungify CErc721._seize` rounds `seizeTokens` up to a whole NFT; a borrower holding 0.9999 CNFT (after transferring 1 wei out) causes `accountTokens[borrower] - seizeTokens` underflow, permanently reverting liquidation.
6. **Design-level fund misplacement** [E6]: `RAAC StabilityPool.liquidateBorrower` requires `crvUSDToken.balanceOf(address(this)) >= scaledUserDebt`, but deposits/repays route crvUSD into `reserveRTokenAddress`, so the balance is always 0 and every liquidation reverts with `InsufficientBalance()`.
7. **Decimal truncation** [E7]: `GainsNetwork.triggerOrder` passes `collateralAmount / collateralPrecisionDelta / PRECISION` into `getTradeLiquidationPrice`; for USDC (6 decimals) this truncates to 0 for realistic amounts and the division by zero reverts the liquidation trigger.
8. **Malicious collateral token** [E8]: Astaria — a malicious collateralized NFT token blocks liquidation and epoch processing (hook-bearing collateral).

#### Attack Scenario / Path Variants

**Path A: Malicious receiver callback blocks seizure** [E5]
Path key: `revertible_liquidation_path | liquidate() | LiquidationEngine→ERC721_receiver | callback_revert_blocks_seizure`
Entry surface: `vault.liquidate(LiquidateParams)`
Contracts touched: `V3Vault -> NonfungiblePositionManager -> borrower contract`
Boundary crossed: `ERC721 receiver callback into borrower-controlled code`
1. Borrower is a contract that reverts/returns wrong selector from `onERC721Received` when `from == vault`.
2. Position becomes underwater (collateral price drop mocked via Chainlink).
3. Liquidator calls `liquidate`; `_cleanUpLoan` does `safeTransferFrom` back to owner.
4. Callback returns invalid selector → whole tx reverts.
5. **Impact**: bad debt accrues indefinitely; insolvency.

**Path B: Dust deposit re-arms cooldown** [E3]
Path key: `revertible_liquidation_path | depositCollateral() | StakingRewards→LiquidationEngine | cooldown_rearm_blocks_liquidation`
Entry surface: `depositCollateralAndIncreaseShare(DUST+1)`
Contracts touched: `CollateralAndLiquidity -> StakingRewards._increaseUserShare`
Boundary crossed: `shared cooldown state between staking module and liquidation`
1. Alice deposits, borrows max; collateral price crashes.
2. Alice front-runs liquidation with a DUST+1 deposit → `cooldownExpiration = now + modificationCooldown`.
3. `liquidateUser(alice)` reverts "Must wait for the cooldown to expire".
4. Repeat each cooldown window; debt keeps accruing.
5. **Impact**: indefinite evasion; system debt grows.

**Path C: Borrower resets own auction** [E1]
Path key: `revertible_liquidation_path | buyLoan() | Lender→Auction | auction_timestamp_reset_blocks_seizure`
Entry surface: `Lender.buyLoan(loanId, poolId=same pool)`
Contracts touched: `Lender (Dutch auction)`
Boundary crossed: `auction state writable by loan borrower`
1. Loan enters Dutch auction liquidation.
2. Borrower calls `buyLoan` with their own `loanId` and the original `poolId`, timing `timeElapsed` to pass rate validation.
3. `loan.auctionStartTimestamp` resets to `type(uint256).max`.
4. `seizeLoan` reverts while timestamp == max; loan is never mature.
5. **Impact**: lender cannot seize collateral; free-ride on collateral upside.

**Path D: Wei self-liquidation breaks debt monotonicity** [E4]
Path key: `revertible_liquidation_path | self-liquidate(1 wei) | PosManager→LendingPool | monotonic_debt_assumption_revert`
Entry surface: `LendingPool.liquidate(posId, amount=1)` called by the borrower
Contracts touched: `PosManager -> LendingPool`
Boundary crossed: `cached debt snapshot vs live debt`
1. `updatePosDebtShares()` caches `lastDebtAmt` assuming debt only grows between updates.
2. Borrower self-liquidates 1 wei — current debt drops below the cached value.
3. Any same-block liquidation now reverts in the update path.
4. Repeat with small self-liquidations to keep blocking.
5. **Impact**: liquidations blocked until accrued interest re-exceeds the snapshot.

**Path E: Liquidator-side fund misplacement** [E6]
Path key: `revertible_liquidation_path | liquidation trigger | StabilityPool→LendingPool | missing_funds_revert`
Entry surface: `StabilityPool.liquidateBorrower(user)`
Contracts touched: `StabilityPool -> LendingPool.finalizeLiquidation`
Boundary crossed: `token custody split between pool and reserve token`
1. All crvUSD entering the system is forwarded to `reserveRTokenAddress`.
2. `liquidateBorrower` checks `crvUSDToken.balanceOf(address(this))` — always 0.
3. Every liquidation attempt reverts `InsufficientBalance()`.
4. **Impact**: system-wide liquidation impossibility; solvency invariants broken.

#### Vulnerable Pattern Examples

**Example 1: Collateral return to borrower-controlled receiver (Revert Lend)** [HIGH]
```solidity
// ❌ VULNERABLE: borrower's onERC721Received can revert the whole liquidation
function _cleanUpLoan(uint256 tokenId, IVault.Loan memory loan) internal {
    // ...
    nonfungiblePositionManager.safeTransferFrom(address(this), owner, tokenId); // @audit owner-controlled callback
}
// MaliciousBorrower:
function onERC721Received(address, address from, uint256, bytes calldata) external returns (bytes4) {
    if (from == vault) return bytes4(0xdeadbeef); // blocks liquidation
    return msg.sig;
}
```

**Example 2: Whole-NFT rounding vs fractional collateral (Fungify)** [HIGH]
```solidity
// ❌ VULNERABLE: rounds UP to a whole NFT the borrower may not own
function _seize(address liquidator, address borrower, uint seizeTokens) override external nonReentrant returns (uint) {
    uint oneNFTAmount = doubleScale / exchangeRateStoredInternal();
    if (seizeTokens % oneNFTAmount != 0) {
        seizeTokens = ((seizeTokens / oneNFTAmount) + 1) * oneNFTAmount; // @audit borrower holds 0.9999 NFT
    }
    accountTokens[borrower] = accountTokens[borrower] - seizeTokens; // underflow -> revert -> unliquidatable
    accountTokens[liquidator] = accountTokens[liquidator] + seizeTokens;
}
```

**Example 3: Self-balance check on a contract that never holds funds (RAAC)** [HIGH]
```solidity
// ❌ VULNERABLE: deposits are routed away, so this balance is always 0
function liquidateBorrower(address userAddress) external onlyManagerOrOwner nonReentrant whenNotPaused {
    _update();
    uint256 userDebt = lendingPool.getUserDebt(userAddress);
    uint256 scaledUserDebt = WadRayMath.rayMul(userDebt, lendingPool.getNormalizedDebt());
    uint256 crvUSDBalance = crvUSDToken.balanceOf(address(this));   // @audit always 0
    if (crvUSDBalance < scaledUserDebt) revert InsufficientBalance(); // every liquidation reverts
    lendingPool.finalizeLiquidation(userAddress);
}
```

**Example 4: Cooldown respected by liquidation (Salty)** [HIGH]
```solidity
// ❌ VULNERABLE: any dust deposit re-arms the cooldown that liquidation must respect
function _increaseUserShare(address wallet, bytes32 poolID, uint256 increaseShareAmount, bool useCooldown) internal {
    if (useCooldown)
        require(block.timestamp >= user.cooldownExpiration, "Must wait for the cooldown to expire");
        user.cooldownExpiration = block.timestamp + stakingConfig.modificationCooldown(); // @audit re-armed by attacker
    user.userShare += uint128(increaseShareAmount);
}
```

**Example 5: Truncated collateral feeds division (Gains Network)** [HIGH]
```solidity
// ❌ VULNERABLE: non-18-decimal collateral truncates to 0 -> div by 0 in liq price
uint256 liqPrice = _getMultiCollatDiamond().getTradeLiquidationPrice(
    IBorrowingFees.LiqPriceInput(
        ..., t.collateralAmount / collateralPrecisionDelta / PRECISION, // @audit 0 for USDC-sized trades
        t.leverage
    )
);
```

### Impact Analysis

#### Technical Impact

- Permanently unliquidatable underwater positions (8/8 unique findings)
- Bad debt accrues with interest; solvency invariants broken (5/8: E1, E3, E5, E6, E8)
- Borrower gets a free option: keep collateral upside, walk away on downside (2/8: E1, E2)

#### Business Impact

- Lender fund loss through socialized insolvency — the direct financial sink
- Protocol insolvency spiral: as unliquidatable debt grows, exchange rates/withdrawals break
- For Fungify the auditor noted a repeatable "always profit from the protocol" strategy

#### Affected Scenarios

- NFT-collateral lending where seized/returned collateral lands on a borrower-controlled receiver (E2, E5, E8)
- Protocols combining staking cooldowns or timelocks with liquidation triggers (E3)
- Dutch-auction liquidations where the borrower can bid on their own loan (E1)
- Cached debt/interest snapshots updated on an assumption of monotonic growth (E4)
- Stability-pool liquidators funded lazily or from a separate reserve (E6)
- Multi-decimal collateral with precision conversions inside the trigger path (E7)

### Secure Implementation

**Fix 1: Never call borrower-controlled code inside liquidation (pull over push)**
```solidity
// ✅ SECURE: record the returnable collateral as a claim instead of pushing it
function _cleanUpLoan(uint256 tokenId, IVault.Loan memory loan) internal {
    // seize first, complete all state changes:
    loans[tokenId].debtShares = 0;
    // leave NFT claimable by owner later — no external call on the liquidation path:
    pendingNFTClaims[loan.owner].push(tokenId);
    emit NFTClaimable(loan.owner, tokenId);
}
// If a push is unavoidable, use transfer() (no callback) to a non-contract-safe escrow,
// or try/catch with a fallback claim — but never let the revert unwind the seizure.
```

**Fix 2: Liquidation bypasses cooldown / cooldown cannot be re-armed while unsafe**
```solidity
// ✅ SECURE: liquidation is exempt from user-set cooldowns
function liquidateUser(address wallet) external {
    // no cooldown check on the liquidation path; cooldown only gates user withdrawals/deposits
    require(_isLiquidatable(wallet), "not liquidatable");
    _liquidate(wallet);
}
```

**Fix 3: Auction state only moves forward; borrower cannot bid on own loan**
```solidity
// ✅ SECURE: monotonic timestamps and self-bid ban
function buyLoan(uint256 loanId, uint256 poolId) external {
    Loan storage loan = loans[loanId];
    require(msg.sender != loan.borrower, "cannot buy own loan");
    // auctionStartTimestamp may only be set once (or strictly decrease in remaining time)
}
```

**Fix 4: Fund the liquidator path or pull from the reserve**
```solidity
// ✅ SECURE: pull the debt asset at liquidation time
uint256 scaledUserDebt = WadRayMath.rayMul(userDebt, lendingPool.getNormalizedDebt());
uint256 available = crvUSDToken.balanceOf(address(this)) + IReserve(reserveRTokenAddress).availableForPool();
require(available >= scaledUserDebt, "InsufficientBalance");
IReserve(reserveRTokenAddress).withdrawTo(address(this), scaledUserDebt - crvUSDToken.balanceOf(address(this)));
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Any external call on the liquidation path to an address derived from the borrower
  (owner, receiver, callback) where revert propagates
- Borrower-writable state read as a liquidation precondition (cooldown, auction timestamp,
  cached debt snapshot, share balance)
- Liquidator-side balance checks against contracts that custody funds elsewhere
- Precision divisions feeding the liquidation trigger with non-18-decimal collateral
- Rounding-up to indivisible units (whole NFT) before a subtraction from user balance
```

#### High-Signal Grep Seeds
```
- onERC721Received
- safeTransferFrom
- auctionStartTimestamp
- seizeLoan
- liquidateBorrower
- cooldownExpiration
- batchLiquidateBorrow
- InsufficientBalance
- oneNFTAmount
- debtShareToAmtCurrent
```

#### Code Patterns to Look For
```
- Pattern 1: `safeTransferFrom(..., owner, tokenId)` inside `liquidate`/`_cleanUp`/`_seize`
- Pattern 2: `require(block.timestamp >= user.cooldownExpiration)` reachable from `liquidate`
- Pattern 3: `loan.auctionStartTimestamp = ` assignment in a function the borrower can call
- Pattern 4: `if (seizeTokens % oneNFTAmount != 0) seizeTokens = (... + 1) * oneNFTAmount` before a subtraction
- Pattern 5: `balanceOf(address(this))` guard in the stability-pool/liquidator contract with deposits routed to another address
```

#### Audit Checklist
- [ ] Walk the liquidation function and list EVERY external call — which ones reach borrower-controlled code?
- [ ] Can any borrower action (deposit, bid, repay 1 wei, transfer 1 wei of share token) re-arm a precondition the liquidation path checks?
- [ ] Does the liquidator/stability pool actually hold (or pull) the debt asset at execution time?
- [ ] Do precision conversions on the liquidation trigger path survive the smallest realistic collateral amounts for every supported decimal?
- [ ] Is seized indivisible collateral (NFT) handled without rounding up beyond the borrower's balance?

### Real-World Examples

#### Known Exploits
- Undercollateralized-position freezes are a recurring precursor to lending insolvencies; the exploit-side analogue (self-liquidation extracting value) is covered in `DB/general/defihacklabs-business-logic-2023-patterns.md` (Euler donate-to-reserves).

#### Related CVEs/Reports
- Code4rena 2024-03-revert-lend issue #54 (callback-blocked liquidation) — [E5]
- Code4rena 2023-12-initcapital issue #42 (judge-confirmed wei self-liquidation DoS) — [E4]

### Prevention Guidelines

#### Development Best Practices
1. Design liquidation as an atomic seize with zero borrower-controlled external calls; make any collateral return a pull-based claim.
2. Audit every precondition of `liquidate*` for borrower-writable inputs; cooldowns, snapshots, and auction state must be monotonic or admin/keeper-only.
3. Stress-test liquidation for every supported collateral decimal and for fractional indivisible collateral.
4. Ensure liquidator contracts (stability pools, keepers) are funded or can pull funds atomically.

#### Testing Requirements
- Unit tests for: liquidation while borrower contract reverts callbacks; liquidation after dust deposit; repeated self-buyLoan; self-liquidate 1 wei then liquidate
- Integration tests for: stability pool balance vs reserve custody; non-18-decimal collateral trigger path
- Fuzzing targets: liquidation success as an invariant — `assert liquidate() succeeds for every HF < 1 state reachable by borrower actions`

### References

#### Technical Documentation
- ERC721 safe-transfer receiver spec (`onERC721Received` return-value requirement)
- Aave V3 liquidation flow (no borrower-controlled calls before state finalization)

#### Security Research
- Hexens Fungify audit 2023-11-06 (CErc721 `_seize` rounding)
- Spearbit Astaria review (malicious collateral NFT blocking epoch processing)

### Keywords for Search

`liquidation evasion`, `unliquidatable`, `block liquidation`, `onERC721Received revert`, `safeTransferFrom DoS`, `auction timestamp reset`, `buyLoan self bid`, `cooldown re-arm`, `dust deposit liquidation`, `self-liquidate 1 wei`, `fractional NFT collateral`, `whole NFT rounding`, `stability pool insufficient balance`, `precision delta division by zero`, `bad debt accrual`, `insolvency`, `liquidation DoS`, `borrower griefing`

### Related Vulnerabilities

- [Liquidation Seizure Economics Miscalculation](../liquidation/liquidation-seizure-economics.md)
- [Bad Debt Socialization and Missing Write-Off](../bad-debt/bad-debt-socialization.md)
- [Self-Liquidation Abuse](../liquidation/self-liquidation-abuse.md)
- `DB/general/reentrancy/defi-reentrancy-patterns.md` (callback-shaped trust boundaries)
