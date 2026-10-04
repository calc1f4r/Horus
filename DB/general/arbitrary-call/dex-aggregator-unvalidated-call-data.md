---
# Core Classification
protocol: generic
chain: everychain
category: arbitrary_call
vulnerability_type: dex_aggregator_unvalidated_calldata

# Attack Vector Details
attack_type: fund_theft
affected_component: dex_aggregator_integration

# Technical Primitives
primitives:
  - dex_aggregator
  - swap_calldata
  - unvalidated_bytes
  - arbitrary_router
  - low_level_call
  - cpi_validation
  - reentrancy_via_swap
  - liquidation_callback
  - oneinch
  - paraswap
  - 0x_protocol
  - prism_aggregator
  - swap_executor

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.85
financial_impact: high

# Context Tags
tags:
  - defi
  - dex
  - aggregator
  - swap
  - router
  - calldata
  - liquidation
  - reentrancy
  - oneinch
  - paraswap
  - arbitrary_call
  - fund_theft
  - cpi

# Version Info
language: solidity
version: all

# Source
source: solodit + audit-reports

# Pattern Identity (Required)
root_cause_family: unvalidated_external_call
pattern_key: unvalidated_external_call | dex_aggregator_integration | dex_aggregator_unvalidated_calldata

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - 0x_protocol
  - _directDepositIntoVault
  - approve
  - arbitrary_router
  - balanceOf
  - callback
  - cpi_validation
  - deposit
  - dex_aggregator
  - execute
  - liquidate
  - liquidatePosition
  - liquidateWithSwap
  - liquidation_callback
  - low_level_call
  - oneinch
  - paraswap
  - performActionWithOneInch
  - prism_aggregator
  - receive
---

## Reference

| # | Report File | Protocol | Severity | Auditor |
|---|-------------|----------|----------|---------|
| 1 | [h-01-user-can-call-liquidate-and-steal-all-collateral-due-to-arbitrary-router-ca.md](reports/dex_aggregator_findings/h-01-user-can-call-liquidate-and-steal-all-collateral-due-to-arbitrary-router-ca.md) | Mimo DeFi | HIGH | Code4rena |
| 2 | [h-03-liquidateposition-liquidator-can-construct-malicious-data-to-steal-the-borr.md](reports/dex_aggregator_findings/h-03-liquidateposition-liquidator-can-construct-malicious-data-to-steal-the-borr.md) | Particle Protocol | HIGH | Code4rena |
| 3 | [h-01-loss-of-user-funds-as-leveragemacroreferences-cant-do-an-arbitrary-system-c.md](reports/dex_aggregator_findings/h-01-loss-of-user-funds-as-leveragemacroreferences-cant-do-an-arbitrary-system-c.md) | eBTC Protocol | HIGH | Code4rena |
| 4 | [buy-state-fund-drain.md](reports/dex_aggregator_findings/buy-state-fund-drain.md) | Symmetry (Solana) | HIGH | OtterSec |
| 5 | [fund-token-manipulation.md](reports/dex_aggregator_findings/fund-token-manipulation.md) | Symmetry (Solana) | HIGH | OtterSec |
| 6 | [dependency-on-third-party-apis-to-create-the-right-payload.md](reports/dex_aggregator_findings/dependency-on-third-party-apis-to-create-the-right-payload.md) | Socket | MEDIUM | ConsenSys Diligence |
| 7 | [inconsistency-in-api-and-swap-payloads-in-delegationmetaswapadapter-can-potentia.md](reports/dex_aggregator_findings/inconsistency-in-api-and-swap-payloads-in-delegationmetaswapadapter-can-potentia.md) | DelegationMetaSwap | MEDIUM | solodit |
| 8 | [erc5115form_directdepositintovault-rewards-can-be-stolen-when-reward-token-is-al.md](reports/dex_aggregator_findings/erc5115form_directdepositintovault-rewards-can-be-stolen-when-reward-token-is-al.md) | Superform | HIGH | Cantina |
| 9 | [h-1-attacker-can-steal-the-accumulated-topup-fees-in-the-topupproxy-contracts-ba.md](reports/dex_aggregator_findings/h-1-attacker-can-steal-the-accumulated-topup-fees-in-the-topupproxy-contracts-ba.md) | TopupProxy | HIGH | solodit |

---

# DEX Aggregator Unvalidated Call Data — Fund Theft via Arbitrary Swap Routing

## Overview

Protocols that integrate DEX aggregators (1inch, Paraswap, 0x, Prism, custom routers) often pass user-controlled `bytes calldata` directly to an external aggregator contract via a low-level `.call()`. When the receiving contract fails to validate that this calldata actually executes the intended swap on behalf of the protocol — and not an arbitrary action — attackers can redirect funds, trigger reentrancy callbacks, manipulate swap accounting, or steal collateral/fees.

**Root Cause Statement**: This vulnerability exists because DEX aggregator integration points accept user-controlled calldata or swap route parameters without on-chain validation that the swap path, recipient, token amounts, or function signature match the protocol's intent, allowing attackers to hijack execution flow and steal protocol or user funds.

**Pattern Frequency**: Very common — 9/32 DEX aggregator reports (28%)
**Consensus Severity**: HIGH (lowest: MEDIUM, highest: HIGH; 7/9 HIGH)
**Cross-Auditor Validation**: STRONG — 5+ independent auditors across different protocols

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of unvalidated_external_call"
- Pattern key: `unvalidated_external_call | dex_aggregator_integration | dex_aggregator_unvalidated_calldata`
- Interaction scope: `multi_contract`
- Primary affected component(s): `dex_aggregator_integration`
- High-signal code keywords: `0x_protocol`, `_directDepositIntoVault`, `approve`, `arbitrary_router`, `balanceOf`, `callback`, `cpi_validation`, `deposit`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `fails.function -> function.function -> reentrancy.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Function accepts user-controlled target and calldata for low-level `.call()`
- Signal 2: Delegatecall to user-supplied address with contract's storage context
- Signal 3: Token approval granted to contract that forwards arbitrary calls
- Signal 4: Router executes user-supplied swap path without validating intermediate targets

#### False Positive Guards

- Not this bug when: Target address validated against whitelist of approved contracts
- Safe if: Function selector validated against allowlist before forwarding call
- Requires attacker control of: specific conditions per pattern

## Root Cause Analysis

### Variant A — Liquidation with Arbitrary Router Call (5 reports)

The protocol calls a DEX aggregator as part of a liquidation or position-close flow, passing user-supplied `bytes dexTxnData` without validating the target function signature. This allows the liquidator to trigger an ETH-callback (e.g., via `swapExactTokensForETH`), enabling reentrancy into the protocol.

**Affected Reports**: Mimo DeFi (Code4rena, HIGH), Particle Protocol (Code4rena, HIGH), eBTC/Badger (Code4rena, HIGH)

### Variant B — Swap CPI/Call Without Account & Data Validation (2 reports)

In Solana programs using CPI to an aggregator (Prism Aggregator), the program passes `remaining_accounts` and instruction data directly without verifying the instruction type or that the PDA token accounts actually change. Fees are still deducted even when no actual swap occurs.

**Affected Reports**: Symmetry buy-state-fund-drain (OtterSec, HIGH), Symmetry fund-token-manipulation (OtterSec, HIGH)

### Variant C — Off-Chain Generated Calldata Not Validated On-Chain (2 reports)

Protocols rely entirely on external APIs (e.g., 1inch API, Socket API) to generate swap calldata. The explicit arguments (`fromToken`, `toToken`, `amount`, `receiver`) passed to the contract function are not verified to match the embedded calldata. A mismatch causes the wrong amount/token to be swapped or funds to be sent to the wrong recipient.

**Affected Reports**: Socket ConsenSys (MEDIUM), DelegationMetaSwapAdapter (MEDIUM)

### Variant D — Cross-Contract Reentrancy via Custom Swap Executor (1 report)

A 1inch custom executor is used during a direct deposit swap. The executor, controlled by the attacker, calls a permissionless `claimRewards()` on the vault mid-swap, inflating the deposit amount by accumulated rewards, which are then stolen.

**Affected Reports**: Superform ERC5115Form (Cantina, HIGH)

---

## Attack Scenarios

### Scenario 1 — Collateral Theft via ETH Callback During Liquidation (Mimo DeFi)

1. Attacker identifies an unhealthy position in `PARMinerV2.sol`
2. Attacker calls `liquidate()` supplying `dexTxnData` encoding `UniswapV2Router.swapExactTokensForETH(amountIn, amountOutMin, path, attackerContract, deadline)`
3. `PARMinerV2` approves and calls the router with the attacker's calldata
4. Router transfers ETH to `attackerContract`, triggering `attackerContract.receive()`
5. Inside the callback: attacker swaps ETH back to PAR, deposits PAR into `PARMinerV2`
6. Final balance check in `liquidate()` passes (PAR balance increased)
7. Attacker withdraws their deposited PAR — effectively stealing all liquidated collateral

### Scenario 2 — Borrower Profit Theft via Fake Pool During Liquidation (Particle Protocol)

1. Collateral + tokenPremium = 120 tokens; minimum repayment = 100
2. Liquidator deploys `FakeErc20` and `FakePool` (token0 = FakeErc20, token1 = WETH)
3. Liquidator calls `liquidatePosition()` with `pool = fakePool`, `swapAmount = 120`
4. During `Base.swap(params.data)`, `FakeErc20.transfer()` re-enters protocol and transfers 100 WETH to `ParticlePositionManager`
5. `liquidatePosition()` succeeds — but 20 tokens (120–100) are stolen from borrower profit

### Scenario 3 — Fee Drain Without Actual Swap (Symmetry / Solana)

1. Attacker invokes `buy_state_rebalance` with malicious CPI instruction to Prism Aggregator
2. CPI succeeds but does not modify `pda_usdc_account` or `pda_token_account` balances
3. `from_amount = 0`, `to_amount = 0`, slippage check passes (0 <= 0)
4. Rebalance fee (0.01% of unspent amount) is still deducted and sent to fee account
5. Attacker repeats to drain entire BuyState balance

### Scenario 4 — Reward Theft via Custom 1inch Executor (Superform)

1. Attacker creates direct deposit with `liqData.bridgeId = 1inch Aggregator`, custom executor
2. During swap: executor correctly swaps USDC → USDD, but also calls `PendleCurveUsdd3CrvSY.claimRewards(ERC5115Form)`
3. Unclaimed USDD rewards are transferred to `ERC5115Form` mid-swap
4. Deposit accounting counts these rewards as part of the deposit → attacker's shares inflated
5. Attacker receives excess vault shares representing stolen protocol rewards

---

## Vulnerable Pattern Examples

**Example 1: Arbitrary Router in Liquidation** [HIGH — Mimo DeFi, Code4rena]

Reference: [h-01-user-can-call-liquidate...](reports/dex_aggregator_findings/h-01-user-can-call-liquidate-and-steal-all-collateral-due-to-arbitrary-router-ca.md)

```solidity
// ❌ VULNERABLE: attacker controls dexTxnData — can encode swapExactTokensForETH
// triggering ETH callback before balance check
function liquidate(
    address _vaultId,
    uint256 _amount,
    address _router,
    bytes calldata dexTxnData  // ← entirely attacker-controlled
) external {
    uint256 par_balance_start = PAR.balanceOf(address(this));

    // Step 1: liquidate, receive collateral
    _a.parallel().core().liquidatePartial(_vaultId, _amount);

    // Step 2: ❌ No validation on _router or dexTxnData content
    IERC20(collateral).approve(_router, collateralBalance);
    _router.call(dexTxnData);  // attacker triggers ETH transfer → gets callback

    // Step 3: balance check — passes if attacker deposited PAR during callback
    require(PAR.balanceOf(address(this)) > par_balance_start, "not enough PAR");
}
```

**Example 2: Malicious swap data in `liquidatePosition()`** [HIGH — Particle Protocol, Code4rena]

Reference: [h-03-liquidateposition...](reports/dex_aggregator_findings/h-03-liquidateposition-liquidator-can-construct-malicious-data-to-steal-the-borr.md)

```solidity
// ❌ VULNERABLE: params.data passed to Base.swap() without validation
// Liquidator can use any fake pool/token pair
function liquidatePosition(
    DataTypes.LiquidatePositionParams calldata params
) external {
    // ...close position logic...
    // params.data is entirely controlled by the liquidator
    uint256 amountReceived = Base.swap(params.data);  // ← arbitrary swap target
    // only checks amountReceived >= repayAmount, not the swap source/target
    require(amountReceived >= repayAmount, "insufficient repay");
    uint256 borrowerProfit = amountReceived - repayAmount;
    // attacker can construct fake pool that steals borrowerProfit
}
```

**Example 3: Prism Aggregator CPI without instruction validation** [HIGH — Symmetry, OtterSec]

Reference: [buy-state-fund-drain.md](reports/dex_aggregator_findings/buy-state-fund-drain.md)

```rust
// ❌ VULNERABLE (Solana/Rust): CPI to prism aggregator with no instruction validation
// Attacker can pass an instruction that does NOT move tokens but still deducts fee
pub fn buy_state_rebalance(ctx: Context<BuyStateRebalance>, ...) -> Result<()> {
    // No validation of instruction_id or instruction_data content
    let (from_amount, to_amount) = swap(
        ctx.remaining_accounts,   // ← attacker-provided accounts
        &ctx.accounts.pda_usdc_account,
        &ctx.accounts.pda_token_account,
        &instruction_id,          // ← not validated against allowed set
        &instruction_data[..],    // ← attacker-controlled
        amount_to_spend,
        0,
        bump,
    )?;
    // from_usd_value = 0 when no actual swap → slippage check passes!
    if mul_div(from_usd_value, BPS_DIVIDER - rebalance_slippage, BPS_DIVIDER)
        > to_usd_value  // 0 > 0 is false → no revert
    { return Err(ErrorCode::SlippageError.into()); }
    // Fee is still deducted from unspent amount
    charge_rebalance_fee(unspent_amount)?;
}
```

**Example 4: Off-chain calldata not validated on-chain** [MEDIUM — Socket, ConsenSys Diligence]

Reference: [dependency-on-third-party-apis...](reports/dex_aggregator_findings/dependency-on-third-party-apis-to-create-the-right-payload.md)

```solidity
// ❌ VULNERABLE: explicit args (toToken, amount, receiverAddress) are never
// verified against the actual swap encoded in swapExtraData
function performActionWithOneInch(
    address fromToken,
    address toToken,          // ← only declared, not enforced
    uint256 amount,
    address receiverAddress,  // ← only declared, not enforced  
    bytes calldata swapExtraData  // ← the REAL instructions; generated off-chain
) external {
    IERC20(fromToken).approve(ONEINCH_AGGREGATOR, amount);
    // toToken, receiverAddress, actual swap amount are ONLY determined by swapExtraData
    (bool success,) = ONEINCH_AGGREGATOR.call(swapExtraData);
    // Event still emits the explicit args, not what actually executed
    emit Swap(fromToken, toToken, amount, receiverAddress);  // ← misleading
}
```

**Example 5: Cross-contract reentrancy via 1inch custom executor** [HIGH — Superform, Cantina]

Reference: [erc5115form_directdepositintovault...](reports/dex_aggregator_findings/erc5115form_directdepositintovault-rewards-can-be-stolen-when-reward-token-is-al.md)

```solidity
// ❌ VULNERABLE: liqData.bridgeId can be 1inch with custom executor
// Custom executor can call permissionless claimRewards() mid-swap
function _directDepositIntoVault(
    InitSingleVaultData memory singleVaultData,
    address srcSender
) internal {
    // attacker sets bridgeId = 1inch, uses custom executor
    // executor swap path: USDC → USDD AND calls PendleCurveUsdd3CrvSY.claimRewards(this)
    _dispatchTokens(singleVaultData.liqData, ...);  // ← calls 1inch with attacker executor

    // After custom executor runs, ERC5115Form now holds rewards + deposit amount
    uint256 depositAmount = IERC20(tokenIn).balanceOf(address(this));  // inflated!
    // Attacker receives excess vault shares
    vault.deposit(depositAmount, receiver);
}
// Fix: claim rewards BEFORE processing the swap
```

---

## Impact Analysis

### Technical Impact
- Complete theft of liquidated collateral (3/9 reports — liquidation context)
- Theft of borrower profit / protocol surplus (2/9 reports)
- Drain of fee reserves via zero-effect swaps (2/9 reports — Solana)
- Incorrect swap amounts and wrong recipients (2/9 reports — off-chain calldata mismatch)
- Reentrancy into protocol state during swap execution (3/9 reports)
- Protocol reward token theft via deposit inflation (1/9 reports)

### Business Impact
- Direct financial loss proportional to position sizes or fee accumulation
- Loss of user trust when liquidations become hostile acts
- Protocol insolvency if collateral backing is systematically drained

### Affected Scenarios
- Any DEX aggregator integration where `bytes calldata swapData` is user-controlled
- Liquidation flows that pass aggregator bytes without validating function selector
- Solana programs using CPI to aggregators without validating instruction type
- Protocols relying solely on off-chain APIs to generate on-chain calldata
- Direct deposit/withdrawal flows using 1inch custom executors

---

## Secure Implementation

**Fix 1: Validate Function Selector and Swap Recipient** [Recommended]

```solidity
// ✅ SECURE: whitelist allowed function selectors and validate swap recipient
function liquidateWithSwap(
    address _vaultId,
    uint256 _amount,
    address _router,
    bytes calldata dexTxnData
) external {
    require(allowedRouters[_router], "router not whitelisted");

    // Extract and validate function selector from calldata
    bytes4 selector = bytes4(dexTxnData[:4]);
    require(allowedSelectors[selector], "function not allowed");
    // Disallow swapExactTokensForETH and similar ETH-output functions
    // to prevent callback reentrancy

    uint256 par_balance_start = PAR.balanceOf(address(this));
    _a.parallel().core().liquidatePartial(_vaultId, _amount);

    IERC20(collateral).approve(_router, collateralBalance);
    (bool success,) = _router.call(dexTxnData);
    require(success, "swap failed");

    // Check delta, not absolute balance
    require(
        PAR.balanceOf(address(this)) >= par_balance_start + minimumPARReceived,
        "insufficient PAR received"
    );
}
```

**Fix 2: Validate On-Chain Arguments Match Embedded Calldata** [For Off-Chain Calldata Patterns]

```solidity
// ✅ SECURE: decode and cross-check critical fields in swapExtraData
function performActionWithOneInch(
    address fromToken,
    address toToken,
    uint256 amount,
    address receiverAddress,
    bytes calldata swapExtraData
) external {
    // Decode the 1inch swap call: first 4 bytes = selector, rest = args
    // Validate the receiver encoded in swapExtraData matches receiverAddress
    (address encodedReceiver, address encodedDstToken, uint256 encodedAmount)
        = _decode1inchCalldata(swapExtraData);
    require(encodedReceiver == receiverAddress, "receiver mismatch");
    require(encodedDstToken == toToken, "destination token mismatch");
    require(encodedAmount >= amount, "amount below minimum");

    IERC20(fromToken).approve(ONEINCH_AGGREGATOR, amount);
    (bool success,) = ONEINCH_AGGREGATOR.call(swapExtraData);
    require(success, "1inch call failed");
}
```

**Fix 3: Reentrancy Guard + Claim Rewards Before Deposit** [For Reentrancy Variant]

```solidity
// ✅ SECURE: claim rewards before the swap so they are not counted as deposit
function _directDepositIntoVault(
    InitSingleVaultData memory singleVaultData,
    address srcSender
) internal nonReentrant {  // ← reentrancy guard
    // Claim rewards FIRST so accumulated rewards aren't counted in deposit
    IStandardYield(underlying).claimRewards(address(this));
    _processAndDistributeRewards();  // account for claimed rewards

    // Now execute the swap — even if executor calls claimRewards again, 
    // there are no pending rewards left to steal
    _dispatchTokens(singleVaultData.liqData, ...);

    uint256 depositAmount = IERC20(tokenIn).balanceOf(address(this));
    vault.deposit(depositAmount, receiver);
}
```

**Fix 4: Solana — Validate CPI Instruction Data** [For Solana/Rust Variant]

```rust
// ✅ SECURE: validate instruction_id against allowed set and skip fee if no swap
pub fn buy_state_rebalance(ctx: Context<BuyStateRebalance>, ...) -> Result<()> {
    // Validate the instruction_id is an allowed swap operation
    require!(
        ALLOWED_SWAP_INSTRUCTIONS.contains(&instruction_id),
        ErrorCode::InvalidInstruction
    );

    let from_before = token::accessor::amount(&ctx.accounts.pda_usdc_account.to_account_info())?;
    let (from_amount, to_amount) = swap(...)?;

    // Only charge fee if actual rebalancing occurred
    require!(from_amount > 0 && to_amount > 0, ErrorCode::NoSwapOccurred);
    charge_rebalance_fee(unspent_amount)?;
    Ok(())
}
```

---

## Detection Patterns

### Code Patterns to Search For

```
# Solidity — arbitrary aggregator call with user bytes
grep -rn "\.call(.*Data\|\.call(.*Payload\|\.call(.*bytes" --include="*.sol"

# Look for balance check AFTER call (but not before → delta check)
grep -rn "balanceOf.*>.*_min\|balanceOf.*>=.*min" --include="*.sol"

# Liquidation functions accepting bytes for swap
grep -rn "function liquidate.*bytes\|bytes.*dexData\|bytes.*swapData" --include="*.sol"

# 1inch integration without selector validation
grep -rn "ONEINCH_AGGREGATOR\.call\|ONE_INCH.*\.call\|oneinch.*\.call" --include="*.sol"

# Solana: CPI without instruction validation
grep -rn "remaining_accounts\|instruction_data\|prism_aggregator" --include="*.rs"
```

### Audit Checklist

- [ ] Does the protocol pass user-controlled `bytes` to an external DEX aggregator?
- [ ] Are function selectors in the calldata validated against an allowlist?
- [ ] Is the swap recipient validated to be the protocol contract, not the caller?
- [ ] Could the swap function trigger an ETH/token callback to the caller (reentrancy vector)?
- [ ] Is the swap output checked as a delta (before/after) rather than absolute balance?
- [ ] In liquidation contexts, does the flow preclude attackers from depositing during the callback window?
- [ ] For Solana: are CPI instruction IDs validated before executing?
- [ ] For off-chain calldata: are the embedded arguments cross-checked against explicit function parameters?
- [ ] Is there a `nonReentrant` guard on functions that invoke external aggregators?
- [ ] Are rewards/balance snapshots taken before invoking the aggregator call?

---

### Real-World Examples

- **Mimo DeFi** — Liquidation collateral theft via UniswapV2 `swapExactTokensForETH` callback — Code4rena 2022 — HIGH
- **Particle Protocol** — Borrower profit theft via fake ERC20 pool in `liquidatePosition` — Code4rena 2023 — HIGH
- **eBTC Protocol (Badger)** — LeverageMacro arbitrary system call — Code4rena 2023 — HIGH
- **Symmetry (Solana)** — buy_state_rebalance fee drain + fund manipulation via unvalidated Prism Aggregator CPI — OtterSec — HIGH
- **Socket Protocol** — Off-chain 1inch calldata not validated on-chain → wrong amount/recipient — ConsenSys Diligence 2023 — MEDIUM
- **Superform** — ERC5115Form reward theft via cross-contract reentrancy through custom 1inch executor — Cantina 2024 — HIGH

---

### Keywords for Search

`dex aggregator calldata`, `unvalidated swap bytes`, `arbitrary router call`, `liquidation collateral theft`, `1inch executor reentrancy`, `paraswap arbitrary call`, `swapExactTokensForETH callback`, `oneinch aggregator call`, `prism aggregator cpi`, `swap calldata validation`, `router whitelist bypass`, `dexTxnData`, `swapExtraData`, `arbitrary external call dex`, `liquidate arbitrary data`, `aggregator integration security`, `swap bytes exploit`, `custom executor reentrancy`, `off-chain calldata validation`, `socket protocol`, `fund drain aggregator`

### Related Vulnerabilities

- [DB/general/arbitrary-call/arbitrary-external-call-vulnerabilities.md](DB/general/arbitrary-call/arbitrary-external-call-vulnerabilities.md) — General arbitrary call patterns
- [DB/general/reentrancy/](DB/general/reentrancy/) — Reentrancy via callback patterns
- [DB/general/slippage-protection/slippage-protection.md](DB/general/slippage-protection/slippage-protection.md) — Output validation after swap
- [DB/general/slippage-protection/dex-aggregator-slippage-balance-bypass.md](DB/general/slippage-protection/dex-aggregator-slippage-balance-bypass.md) — Slippage check bypass via existing balance

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

`0x_protocol`, `_directDepositIntoVault`, `aggregator`, `approve`, `arbitrary_call`, `arbitrary_router`, `balanceOf`, `callback`, `calldata`, `cpi`, `cpi_validation`, `defi`, `deposit`, `dex`, `dex_aggregator`, `dex_aggregator_unvalidated_calldata`, `execute`, `fund_theft`, `liquidate`, `liquidatePosition`, `liquidateWithSwap`, `liquidation`, `liquidation_callback`, `low_level_call`, `oneinch`, `paraswap`, `performActionWithOneInch`, `prism_aggregator`, `receive`, `reentrancy`, `reentrancy_via_swap`, `router`, `swap`, `swap_calldata`, `swap_executor`, `unvalidated_bytes`
