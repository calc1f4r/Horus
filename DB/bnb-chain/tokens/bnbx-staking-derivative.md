---
# Core Classification
protocol: stader-labs-bnbx
chain: bsc
category: arithmetic
vulnerability_type: share_mint_accounting_corruption

# Pattern Identity
root_cause_family: oracleless_share_minting_with_unsynced_pool_totals
pattern_key: stale_pool_total | deposit conversion | operator reward bump | share mint revert or zero shares

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - StakeManager.sol (requestWithdraw, startUndelegation, convertBnbToBnbX, convertBnbXToBnb, getTotalPooledBnb, increaseTotalRedelegated/addRestakingRewards, startDelegation)
  - BnbX.sol (ERC20Upgradeable share token, totalSupply, burn)
  - TokenHub (cross-chain transferOut to BNB Beacon Chain staking wallet)
path_keys:
  - stale_pool_total | startUndelegation (bot) | totalDeposited -= totalBnbToWithdraw -> underflow revert locks exits
  - reward_inflation_before_first_deposit | increaseTotalRedelegated -> convertBnbToBnbX | first depositor mints 0 shares
  - init_gap | uninitialized implementation | missing _disableInitializers -> takeover risk

# Attack Vector Details
attack_type: logical_error
affected_component: exchange-rate conversion between BNB and BnbX shares

# Technical Primitives
primitives:
  - share_price_as_totalPooledBnb_over_totalSupply
  - operator_adjustable_pool_total (totalRedelegated)
  - underflow_revert_as_dos
  - zero_share_first_deposit
  - reentrancy_resistant_local_caching (bnbXToBurn copied before burn)
  - uninitialized_implementation
  - cross_chain_transferOut_native_value

# Grep / Hunt-Card Seeds
code_keywords:
  - convertBnbToBnbX
  - convertBnbXToBnb
  - getTotalPooledBnb
  - totalRedelegated
  - addRestakingRewards
  - increaseTotalRedelegated
  - totalDeposited
  - totalBnbToWithdraw
  - totalBnbXToBurn
  - startUndelegation
  - requestWithdraw
  - startDelegation
  - claimWithdraw
  - disableInitializers
  - setStakeManager
  - setBotAddress
  - tokenHub

# Impact Classification
severity: high
impact: exit_dos|zero_share_loss|fund_loss
financial_impact: medium

# Context Tags
tags:
  - liquid-staking
  - bnbx
  - stader
  - share-minting
  - exchange-rate
  - first-depositor
  - underflow
  - upgradeable
  - bsc
  - halborn

# Version Info
language: solidity
version: "audited commit 2ddf3e2c30321587742630de90a1414434ff256f (Jun-Jul 2022); fixed d56ab580231c56531edbb780387e1c711236c85d + 4e04e467"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [halborn-bnbx] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-staderlabs-bnbx-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | Staderlabs BnbX audit, Jun 29–Jul 5 2022 |

## BnbX Liquid-Staking Share Accounting (Stader StakeManager)

**Pool-total state mutated by operator reward bumps desynchronizes mint/burn conversions** — `increaseTotalRedelegated` inflates `getTotalPooledBnb()` without corresponding deposits, so `startUndelegation` underflows (`totalDeposited -= totalBnbToWithdraw`) and locks all withdrawals, and the first depositor can mint 0 BnbX for real BNB.

### Overview

Stader's BnbX is an ERC1967-style upgradeable liquid-staking token where `convertBnbToBnbX = amount * totalSupply / getTotalPooledBnb()` and `getTotalPooledBnb = totalDeposited + totalRedelegated`. Halborn's HIGH shows the operator-only `increaseTotalRedelegated` (post-fix `addRestakingRewards`) can push `totalRedelegated` beyond `totalDeposited`, corrupting every conversion: withdrawal accounting then subtracts an inflated BNB amount from a smaller `totalDeposited` → Solidity ≥0.8 panic revert → **no user can exit**.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because a privileged function inflates the pool-total term (`totalRedelegated`) of the share-price ratio without moving corresponding assets in, so withdrawal conversions compute BNB amounts backed by nothing and the settlement subtraction `totalDeposited -= totalBnbToWithdraw` underflows, permanently reverting exits"
- Pattern key: `stale_pool_total | deposit conversion | operator reward bump | share mint revert or zero shares`
- Interaction scope: `multi_contract`
- Primary affected component(s): `StakeManager conversion + delegation/undelegation settlement`
- Contracts / modules involved: `StakeManager.sol, BnbX.sol, TokenHub (cross-chain staking transfers)`
- Path keys: see frontmatter `path_keys`
- High-signal code keywords: `getTotalPooledBnb`, `totalRedelegated`, `addRestakingRewards`, `convertBnbToBnbX`, `startUndelegation`, `totalDeposited`
- Typical sink / impact: `all-user exit DoS (HIGH) / first-depositor 0-share loss (MEDIUM) / implementation init takeover (LOW)`
- Validation strength: `strong` (Halborn cites exact lines; fixes verified on remediation commit d56ab58)

#### Contract / Boundary Map

- Entry surface(s): `deposit-side: deposit()/convertBnbToBnbX`, `exit-side: requestWithdraw(_amount) → bot startUndelegation() → claimWithdraw(idx)`, `operator: increaseTotalRedelegated/addRestakingRewards, startDelegation (BOT role)`
- Contract hop(s): `user -> StakeManager.requestWithdraw -> convertBnbXToBnb(getTotalPooledBnb) -> totals accumulate -> BOT startUndelegation -> totalDeposited -= totalBnbToWithdraw + BnbX.burn`
- Trust boundary crossed: `operator role (BOT/admin) → accounting invariants consumed by user-facing conversions`; `BSC → TokenHub.transferOut → BNB Beacon Chain bcDepositWallet (cross-chain staking)`
- Shared state or sync assumption: `getTotalPooledBnb() == totalDeposited + totalRedelegated must reflect only real, withdrawable BNB; any inflator breaks both mint and burn directions`

#### Valid Bug Signals

- Signal 1: An exchange-rate function divides by a pool total that ANY privileged setter can increase without transferring assets in (`increaseTotalRedelegated(amount)` with no bound)
- Signal 2: A settlement path subtracts a conversion output from a DIFFERENT accumulator than the one the conversion input was added to (`totalBnbToWithdraw` computed from `totalPooledBnb`, subtracted from `totalDeposited`)
- Signal 3: Conversion denominators clamp `x == 0 ? 1 : x` (both totalSupply and totalPooledBnb) — the `? 1` seed lets tiny rewards dominate a real first deposit, minting 0 shares for nonzero BNB
- Signal 4: Upgradeable contracts (BnbX, StakeManager) whose constructors don't call `_disableInitializers()`
- Signal 5: Slither reentrancy flags on `requestWithdraw` (state written after safeTransferFrom) and `claimWithdraw` (event after sendValue) — verify ordering or CEI

#### False Positive Guards

- Not this bug when: reward-accumulator bumps are bounded (post-fix `addRestakingRewards` requires amount > 0 and startUndelegation **recalculates the ratio at execution time** instead of consuming queued conversions) — check whether the fix re-derives amounts or only adds a `> 0` guard
- Not this bug when: the operator bump is provably backed by restaking rewards already custodied by the contract (balance-delta proof), not merely asserted
- Zero-share mint needs: `totalDeposited == 0` AND reward bump > first deposit amount. If a bootstrap deposit or share-seeding (mint 1 wei to dead address, or virtual shares) exists, downgrade to LOW/QA
- `_disableInitializers` gap is LOW when proxies are deployed atomically with initialization in the same script/tx; HIGH only if implementations are deployed and left uninitialized on-chain (verify deployment txs)
- The int256→uint256 underflow panic itself is not reentrancy — it is a plain Solidity 0.8 checked-math revert; do not conflate with the Slither reentrancy-2/3 noise in the same report

### Vulnerability Description

#### Root Cause

1. **HAL-01 (HIGH) — underflow via unsynced accumulators.** `requestWithdraw` converts BnbX→BNB using `getTotalPooledBnb() = totalDeposited + totalRedelegated` and accumulates the BNB result into `totalBnbToWithdraw`. If `increaseTotalRedelegated` raised the pooled total (reward claims, operator error, or malice), `totalBnbToWithdraw` can exceed `totalDeposited`. `startUndelegation` then executes `totalDeposited -= _amount` → checked-math panic → every undelegation attempt reverts → **users cannot withdraw deposited BNB** (Halborn: likelihood 3, impact 5).
2. **HAL-02 (MEDIUM) — first depositor gets 0 shares.** With `totalDeposited == 0`, operator calls `increaseTotalRedelegated(10 BNB)`; `getTotalPooledBnb()` returns 10e18. First user deposits 1 BNB: `convertBnbToBnbX(1e18) = 1e18 * 1 / 10e18 = 0` (integer division). User's BNB is taken, 0 BnbX minted — deposit value transferred to existing (future) holders via ratio inflation.
3. **HAL-03 (LOW) — uninitialized implementations.** `BnbX` and `StakeManager` use OZ `Initializable` but constructors lacked `_disableInitializers()`, leaving the implementation contracts initializable by anyone.
4. **HAL-04 (INFO) — zero-address gaps.** `setStakeManager`, `initialize(...)`, `setBotAddress` accepted 0x0.
5. Slither supporting noise: ignored `ITokenHub(tokenHub).transferOut{value: ...}` return value; reentrancy-2/3 patterns on requestWithdraw/claimWithdraw (state/event after external call); timestamp-based comparisons in completeDelegation/claimWithdraw/isClaimable.

#### Attack Scenario / Path Variants

**Path A: Reward-bump underflow bricks withdrawals** [HIGH]
Path key: `stale_pool_total | startUndelegation (bot) | totalDeposited -= totalBnbToWithdraw -> underflow revert locks exits`
1. Contract has `totalDeposited = 90 BNB`, `totalRedelegated = 0`, `totalSupply = 90 BnbX`
2. Operator calls `increaseTotalRedelegated(20 BNB)` (anticipating restaking rewards not yet received)
3. User holding 90 BnbX calls `requestWithdraw(90 BnbX)` → `convertBnbXToBnb = 90 * 110/110 = 90... wait, ratio now 110 pooled for 90 shares → user gets 90 BnbX * (110/90) = 110 BNB` credited to `totalBnbToWithdraw`
4. Bot calls `startUndelegation()` → `totalDeposited (90) -= 110` → panic revert
5. Every subsequent startUndelegation reverts identically; withdrawals are frozen for all users; the unbacked 20 BNB is effectively claimable by whoever exits first once/if the operator re-syncs state

**Path B: First depositor mints zero shares** [MEDIUM]
Path key: `reward_inflation_before_first_deposit | increaseTotalRedelegated -> convertBnbToBnbX | first depositor mints 0 shares`
1. Fresh pool: `totalDeposited = 0`, `totalSupply = 0`
2. Operator calls `increaseTotalRedelegated(10 BNB)` → `getTotalPooledBnb() = 10e18`
3. Alice deposits 1 BNB → `convertBnbToBnbX(1e18) = 1e18 * max(totalShares=0→1, 1) / 10e18 = 0`
4. Alice receives 0 BnbX for 1 BNB; her deposit accrues to future minters' ratio

**Path C: Uninitialized implementation takeover** [LOW]
Path key: `init_gap | uninitialized implementation | missing _disableInitializers -> takeover risk`
1. Deployer deploys `StakeManager`/`BnbX` implementations without constructor `_disableInitializers()`
2. Attacker initializes the raw implementation, becomes its owner
3. Impact on proxies is indirect (malicious impl can't swap proxy admin by itself) but enables honeypot/lookalike init and breaks upgrade safety assumptions

#### Vulnerable Pattern Examples

**Example 1: conversion denominator includes operator-inflatable term** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE (StakeManager): privileged bump inflates denominator;
// withdrawal conversion then exceeds the deposited accumulator
function getTotalPooledBnb() public view override returns (uint256) {
    return (totalDeposited + totalRedelegated); // totalRedelegated set by operator
}

function startUndelegation() external override whenNotPaused onlyRole(BOT)
    returns (uint256 _uuid, uint256 _amount)
{
    require(totalBnbToWithdraw > 0, "No Request to withdraw");
    _uuid = undelegateUUID++;
    _amount = totalBnbToWithdraw;           // computed from inflated ratio
    uuidToBotUndelegateRequestMap[_uuid] = BotUndelegateRequest(block.timestamp, 0, _amount);
    totalDeposited -= _amount;              // ❌ panic when _amount > totalDeposited
    uint256 bnbXToBurn = totalBnbXToBurn;   // cache vs reentrancy (good, insufficient)
    totalBnbXToBurn = 0;
    totalBnbToWithdraw = 0;
    IBnbX(bnbX).burn(address(this), bnbXToBurn);
}
```

**Example 2: zero-share first deposit via clamped seeds** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE (convertBnbToBnbX): with totalSupply==0 and operator-bumped
// pooled BNB, integer division floors to zero shares for a real deposit
function convertBnbToBnbX(uint256 _amount) public view override returns (uint256) {
    uint256 totalShares = IBnbX(bnbX).totalSupply();
    totalShares = totalShares == 0 ? 1 : totalShares;        // seed ≠ real shares
    uint256 totalPooledBnb = getTotalPooledBnb();
    totalPooledBnb = totalPooledBnb == 0 ? 1 : totalPooledBnb; // inflated by operator
    uint256 amountInBnbX = (_amount * totalShares) / totalPooledBnb;
    return amountInBnbX; // 1 BNB vs 10 BNB pooled → 0 shares
}
```

**Example 3: upgradeable contract without initializer lock** [Approx Vulnerability : LOW]
```solidity
// ❌ VULNERABLE: implementation left initializable
contract BnbX is Initializable, ERC20Upgradeable {
    // audited version: no constructor at all → anyone can initialize impl
}

// ✅ post-fix:
constructor() { _disableInitializers(); }
```

### Impact Analysis

#### Technical Impact
- Permanent revert of `startUndelegation` freezes the undelegation pipeline → all users' exits blocked until operator re-syncs accumulators or contract is upgraded
- Zero-share minting silently donates first deposits to the ratio (value loss without any transaction failing)
- Underflow also poisons `uuidToBotUndelegateRequestMap` accounting consistency if partially handled upstream
- Uninitialized implementations break the "impl can never be owned" assumption in OZ upgrade workflows

#### Business Impact
- Exit-freeze on a liquid-staking token is a peg-breaking event: BnbX would depeg to expected-recovery value on secondary markets
- Zero-share first-deposit is a launch-day fund-loss headline; mitigations must exist before any reward bump is possible

#### Affected Scenarios
- Any LSD/staking-derivative where a role can adjust the pooled-asset term of the exchange rate without asset inflow (reward anticipation, fee accrual, oracle-sync corrections)
- Any mint path seeded with `x == 0 ? 1 : x` clamps combined with pre-mint denominator inflation
- Cross-chain staking routers (TokenHub.transferOut) where BNB leaves to the Beacon Chain — underflow here also blocks rebalancing

### Secure Implementation

**Fix 1: recalculate ratio at settlement + bound reward bumps (Halborn's fix)**
```solidity
// ✅ SECURE: addRestakingRewards requires backed amount; startUndelegation
// re-derives BNB from CURRENT ratio rather than trusting queued conversions
function addRestakingRewards(uint256 _amount) external { // ex-increaseTotalRedelegated
    require(_amount > 0, "zero");
    // post-fix also ensures the rewards are actually received (backed):
    totalRedelegated += _amount;
}

function startUndelegation() external onlyRole(BOT) whenNotPaused
    returns (uint256 _uuid, uint256 _amount)
{
    require(totalBnbXToBurn > 0, "No Request to withdraw");
    _amount = convertBnbXToBnb(totalBnbXToBurn); // fresh ratio at execution time
    require(_amount <= totalDeposited, "insolvent"); // explicit solvency guard
    totalDeposited -= _amount;
    ...
}
```

**Fix 2: zero-share protection + initializer lock + zero-address checks**
```solidity
// ✅ SECURE (mint): fail on zero shares; seed with virtual shares/assets (ERC-4626 style)
uint256 shares = (_amount * totalShares) / totalPooledBnb;
require(shares > 0, "zero shares");

// ✅ SECURE (impl lock):
constructor() { _disableInitializers(); }

// ✅ SECURE (addresses): in initialize/setStakeManager/setBotAddress
require(_bnbX != address(0) && _tokenHub != address(0) &&
        _bcDepositWallet != address(0) && _bot != address(0), "zero address");
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Exchange-rate = f(totalSupply, poolTotal) where poolTotal has a privileged additive setter
- Withdrawal queue converts at request-time but settles from a different accumulator
- `x == 0 ? 1 : x` clamps in conversion math (first-user edge)
- Solidity >=0.8 subtraction panics used as accidental invariant enforcement (revert = DoS, not safety)
- Upgradeable contracts: constructor bodies without _disableInitializers()
- Cross-chain value exits (transferOut{value}) whose failure is unchecked
```

#### High-Signal Grep Seeds
```
- getTotalPooledBnb
- totalRedelegated
- addRestakingRewards
- convertBnbToBnbX
- convertBnbXToBnb
- startUndelegation
- totalDeposited
- _disableInitializers
```

#### Code Patterns to Look For
```
- Pattern 1: `return (totalDeposited + totalRedelegated);` as rate denominator with setter access on either term
- Pattern 2: `totalDeposited -= totalBnbToWithdraw;` where RHS passed through a conversion of the SUM
- Pattern 3: `totalShares = totalShares == 0 ? 1 : totalShares;`
- Pattern 4: `require(_amount > 0)` as the ONLY fix on a reward inflator (insufficient without backing proof or settlement-time recalc)
- Pattern 5: proxy-impl deployments without initializer-lock constructors
```

#### Audit Checklist
- [ ] Enumerate every writer of each pool-total term; for each, prove asset inflow (balance delta) or accept inflation risk
- [ ] Trace withdrawal path: is the BNB amount converted at request time or settlement time? Does settlement subtract from the same accumulator deposits added to?
- [ ] Test first-depositor share mint with (a) zero reward bump, (b) reward bump of 10x the deposit
- [ ] Force `totalBnbToWithdraw > totalDeposited` in a test and confirm graceful revert vs panic and post-state consistency
- [ ] Verify `_disableInitializers()` in every upgradeable implementation constructor
- [ ] Check TokenHub.transferOut return-value handling and timestamp comparison edges (completeDelegation/claimWithdraw)

### Real-World Examples

#### Known Exploits
- No public BnbX exploit; both issues fixed pre-mainnet-growth (remediation commit d56ab58, 2022-07-12). Same class precedents: ERC-4626 first-depositor inflation/theft advisories (OpenZeppelin 2022 guidance on decimal/rounding + virtual shares) and LSD exit freezes.

#### Related CVEs/Reports
- Halborn Staderlabs BnbX report HAL-01..HAL-04 (2022) — see [halborn-bnbx]
- OZ "Vault inflation attack" mitigation notes (virtual shares/assets) — same first-depositor economics
- Related DB entry: DB/bnb-chain/tokens/stkbnb-redemption-accounting.md

### Prevention Guidelines

#### Development Best Practices
1. Any accumulator feeding an exchange rate must only be mutable alongside verifiable asset movement (balance-delta checks)
2. Convert at settlement time, not request time, when the ratio can move between the two
3. Explicit solvency requires (`_amount <= totalDeposited`) beat accidental underflow panics for diagnosability and recovery
4. Seed empty pools with virtual shares/assets or revert on zero-share mints
5. Lock implementation initializers at deploy

#### Testing Requirements
- Unit tests: reward bump × [0, 1x, 10x deposit] matrix; withdrawal after each; first-depositor share count assertions
- Integration tests: full deposit → requestWithdraw → startUndelegation → claimWithdraw cycle with mid-cycle reward bumps
- Fuzzing targets: interleavings of addRestakingRewards/requestWithdraw/startUndelegation; conversion rounding at 1-wei amounts

### Keywords for Search

`bnbx`, `stader`, `liquid staking`, `lsd`, `share minting`, `exchange rate`, `conversion rate`, `totalPooledBnb`, `totalRedelegated`, `restaking rewards`, `underflow`, `checked math panic`, `withdrawal freeze`, `exit dos`, `first depositor`, `zero shares`, `integer division`, `rounding to zero`, `virtual shares`, `erc4626 inflation`, `initializable`, `disableInitializers`, `uninitialized implementation`, `proxy`, `erc1967`, `zero address check`, `tokenhub`, `cross chain staking`, `bnb beacon chain`, `bot role`, `operator risk`, `halborn`, `bsc liquid staking`

### Related Vulnerabilities

- DB/bnb-chain/tokens/stkbnb-redemption-accounting.md — sibling LSD claim/reserve accounting bugs
- DB/bnb-chain/defi/launchpool-deposit-validation.md — BSC launch-era validation gaps
- ERC-4626 vault inflation / zero-share family (general vault entries)
