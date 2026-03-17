---
# Core Classification
protocol: generic
chain: everychain
category: reentrancy
vulnerability_type: multi_type

# Attack Vector Details
attack_type: state_manipulation
affected_component: external_calls

# Technical Primitives
primitives:
  - external_call
  - callback_function
  - state_update
  - balance_check
  - receive_function
  - fallback_function
  - flash_loan_callback
  - ERC777_hooks
  - ERC1155_hooks
  - ERC721_onReceived
  - Curve_remove_liquidity
  - Balancer_pool_state

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.8
financial_impact: critical

# Context Tags
tags:
  - defi
  - lending
  - dex
  - vault
  - staking
  - nft
  - real_exploit
  - DeFiHackLabs

# Version Info
language: solidity
version: all

# Source
source: DeFiHackLabs

# Pattern Identity (Required)
root_cause_family: callback_reentrancy
pattern_key: callback_reentrancy | external_calls | multi_type

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - Balancer_pool_state
  - Curve_remove_liquidity
  - ERC1155_hooks
  - ERC721_onReceived
  - ERC777_hooks
  - approve
  - attack
  - balanceOf
  - balance_check
  - batchHarvestMarketRewards
  - block.timestamp
  - borrow
  - burn
  - burnHook
  - callback_function
  - checkCurveReentrancy
  - claimRewards
  - deposit
  - deposits
  - exitMarket
---

# DeFi Reentrancy Vulnerability Patterns

## Overview

Reentrancy vulnerabilities occur when a contract makes an external call to an untrusted address before updating its state, allowing the external contract to call back into the vulnerable contract and exploit the stale state. This comprehensive database entry documents **real-world reentrancy patterns** extracted from 50+ DeFiHackLabs exploit PoCs spanning 2021-2025, categorized by attack vector type.

**Total Historical Losses from Analyzed Exploits: >$300M USD**

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of callback_reentrancy"
- Pattern key: `callback_reentrancy | external_calls | multi_type`
- Interaction scope: `multi_contract`
- Primary affected component(s): `external_calls`
- High-signal code keywords: `Balancer_pool_state`, `Curve_remove_liquidity`, `ERC1155_hooks`, `ERC721_onReceived`, `ERC777_hooks`, `approve`, `attack`, `balanceOf`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `CloberAttacker.function -> DFXAttacker.function -> NFTReentrancyAttacker.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: External call (`.call`, `.transfer`, token transfer) occurs before state variable update
- Signal 2: Token implements callback hooks (ERC-777, ERC-721) and protocol doesn't use `nonReentrant`
- Signal 3: User-supplied token address passed to `transferFrom` without callback protection
- Signal 4: Read-only function's return value consumed cross-contract during an active callback window

#### False Positive Guards

- Not this bug when: Contract uses `ReentrancyGuard` (`nonReentrant`) on all entry points
- Safe if: All state updates complete before any external call (strict CEI)
- Requires attacker control of: specific conditions per pattern

## Vulnerability Categories

### 1. Classic Reentrancy (CEI Violation)
State updates occur AFTER external calls, allowing recursive exploitation.

### 2. Cross-Function Reentrancy
Attacker re-enters through a different function that shares state.

### 3. Cross-Contract Reentrancy
Attacker re-enters through a related contract that modifies shared state.

### 4. Read-Only Reentrancy
View functions return stale/manipulated values during reentrancy window.

### 5. Callback-Based Reentrancy
Exploitation through legitimate callback mechanisms (ERC777, flash loans, hooks).

---

## Vulnerable Pattern Examples

### Example 1: Classic ETH Transfer Reentrancy [CRITICAL]

**Real Exploit: Rari Capital/Fei Protocol (2022-04) - $80M Lost**

```solidity
// ❌ VULNERABLE: State update AFTER external call
contract VulnerableLending {
    mapping(address => uint256) public balances;
    
    function borrow(uint256 amount) external {
        require(getCollateralValue(msg.sender) >= amount, "Undercollateralized");
        
        // External call BEFORE state update
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        // State update AFTER - attacker can re-enter during call above
        balances[msg.sender] += amount;
    }
    
    function exitMarket(address token) external {
        // Can be called during reentrancy to remove collateral
        collateral[msg.sender][token] = 0;
    }
}

// Attack Contract
contract RariAttacker {
    VulnerableLending target;
    
    receive() external payable {
        // Re-enter through different function during ETH transfer
        target.exitMarket(address(collateralToken));
        // Now borrow more without collateral check
    }
}
```

**Attack Flow:**
1. Attacker deposits collateral
2. Calls `borrow()` to receive ETH
3. During ETH transfer, `receive()` triggers
4. Inside callback, attacker calls `exitMarket()` to remove collateral
5. Original `borrow()` completes with stale collateral state
6. Repeat to drain funds

---

### Example 2: Read-Only Reentrancy via Curve Pool [CRITICAL]

**Real Exploits:**
- dForce (2023-02) - $3.65M Lost
- Conic Finance (2023-07) - $3.25M Lost  
- Sturdy Finance (2023-06) - $800K Lost
- Sentiment (2023-04) - $1M Lost
- Midas Capital (2023-01) - $650K Lost

```solidity
// ❌ VULNERABLE: Oracle queries pool during withdrawal callback
contract VulnerableLending {
    ICurvePool public curvePool;
    IOracle public oracle;
    
    function liquidate(address user, address collateral) external {
        // This price query is VULNERABLE during remove_liquidity
        uint256 collateralPrice = oracle.getUnderlyingPrice(collateral);
        uint256 collateralValue = collateralPrice * balances[user];
        
        require(collateralValue < threshold, "Cannot liquidate");
        // Proceed with liquidation...
    }
}

contract VulnerableOracle {
    ICurvePool public pool;
    
    function getUnderlyingPrice(address lpToken) external view returns (uint256) {
        // Uses get_virtual_price() which is manipulable during reentrancy
        uint256 virtualPrice = pool.get_virtual_price();
        return virtualPrice * lpToken.totalSupply();
    }
}

// Attack via Curve's remove_liquidity
contract ReadOnlyReentrancyAttacker {
    function attack() external {
        // 1. Deposit into Curve pool to get LP tokens
        curvePool.add_liquidity{value: amount}([amount, 0], 0);
        
        // 2. Remove liquidity - triggers ETH transfer with callback
        curvePool.remove_liquidity(lpBalance, [0, 0]);
    }
    
    receive() external payable {
        // During removal, pool balances updated but totalSupply NOT YET
        // get_virtual_price() returns INCORRECT (inflated) value
        
        // Oracle returns wrong price - exploit window
        lending.liquidate(victimUser, lpToken);
        // OR: Borrow against inflated collateral value
    }
}
```

**Why Read-Only Reentrancy Works:**
- Curve's `remove_liquidity` sends ETH before burning LP tokens
- `get_virtual_price() = pool_balance / total_supply`
- During callback: balance updated, supply NOT YET updated
- Price appears artificially HIGH or LOW depending on direction

---

### Example 3: Vyper Compiler Bug + Reentrancy [CRITICAL]

**Real Exploit: Curve (2023-07) - $41M Lost**

```python
# ❌ VULNERABLE Vyper code - reentrancy lock was silently removed by compiler bug
@external
@nonreentrant('lock')  # Vyper 0.2.15-0.3.0 SILENTLY IGNORES this decorator
def remove_liquidity(token_amount: uint256, min_amounts: uint256[N_COINS]) -> uint256[N_COINS]:
    # ... calculations ...
    
    # ETH sent here - triggers fallback
    raw_call(msg.sender, b"", value=amounts[0])
    
    # LP tokens burned AFTER ETH sent
    self.totalSupply -= token_amount
```

```solidity
// Attacker contract
contract CurveAttacker {
    ICurvePool pool;
    uint256 nonce;
    
    function attack() external payable {
        pool.add_liquidity{value: 40000 ether}([40000 ether, 0], 0);
        pool.remove_liquidity(lpBalance, [0, 0]); // Enter reentrancy
        nonce++;
        pool.remove_liquidity(extraLP, [0, 0]); // Second withdrawal
    }
    
    receive() external payable {
        if (msg.sender == address(pool) && nonce == 0) {
            // Re-enter during first removal
            pool.add_liquidity{value: 40000 ether}([40000 ether, 0], 0);
            // Receives MORE LP tokens than entitled (price manipulation)
        }
    }
}
```

**Key Insight:** Vyper versions 0.2.15, 0.2.16, 0.3.0 had a compiler bug that silently removed `@nonreentrant` protection under certain conditions.

---

### Example 4: Flash Loan Callback Reentrancy [HIGH]

**Real Exploit: DFXFinance (2022-11) - $4M Lost**

```solidity
// ❌ VULNERABLE: Flash loan callback allows deposit during loan
contract VulnerableDFXPool {
    function flash(address recipient, uint256 amount0, uint256 amount1, bytes calldata data) external {
        // Send tokens to recipient
        token0.transfer(recipient, amount0);
        token1.transfer(recipient, amount1);
        
        // Callback - attacker can manipulate pool state here
        IFlashCallback(recipient).flashCallback(fee0, fee1, data);
        
        // Check repayment
        require(token0.balanceOf(address(this)) >= preBalance0 + fee0, "Not repaid");
    }
    
    function deposit(uint256 amount, uint256 deadline) external returns (uint256 lpTokens) {
        // Normal deposit - but can be called during flash callback!
        uint256 shares = calculateShares(amount);
        _mint(msg.sender, shares);
        return shares;
    }
}

contract DFXAttacker {
    function attack() external {
        // Initiate flash loan
        dfxPool.flash(address(this), borrowAmount0, borrowAmount1, "");
        // Withdraw extra LP tokens received
        dfxPool.withdraw(extraLP, block.timestamp + 60);
    }
    
    function flashCallback(uint256 fee0, uint256 fee1, bytes calldata) external {
        // During flash loan, deposit to mint LP tokens at favorable rate
        // Pool state is inconsistent - balances don't match expected
        dfxPool.deposit(200000e18, block.timestamp + 60);
    }
}
```

---

### Example 5: Hook-Based Reentrancy (Custom Callbacks) [HIGH]

**Real Exploit: CloberDEX (2024-12) - $501K Lost**

```solidity
// ❌ VULNERABLE: Custom hook called during burn with stale state
contract VulnerableRebalancer {
    function burn(bytes32 key, uint256 amount, uint256 minA, uint256 minB) external {
        Pool storage pool = pools[key];
        
        // Call external hook BEFORE state finalization
        IStrategy(pool.strategy).burnHook(msg.sender, key, amount, pool.totalSupply);
        
        // State updates happen after hook returns
        pool.totalSupply -= amount;
        // Transfer assets...
    }
}

contract CloberAttacker {
    IRebalancer rebalancer;
    bool public reEntry = false;
    uint256 public amountToSteal;
    
    function attack() external {
        // Setup fake token pool
        bytes32 key = rebalancer.open(bookKeyA, bookKeyB, "1", address(this));
        
        // Add liquidity then burn
        rebalancer.mint(key, amount, amount, 0);
        rebalancer.burn(key, amountToSteal, 0, 0);
    }
    
    // Called by rebalancer during burn
    function burnHook(address receiver, bytes32 key, uint256 burnAmount, uint256 lastTotalSupply) external {
        if (!reEntry) {
            reEntry = true;
            // Re-enter burn while state is stale
            IRebalancer(rebalancer).burn(key, amountToSteal, 0, 0);
        }
    }
}
```

---

### Example 6: ERC721/ERC1155 Callback Reentrancy [HIGH]

**Real Exploits:**
- Omni NFT (2022-07) - $1.4M Lost
- NFTTrader (2023-12) - $3M Lost

```solidity
// ❌ VULNERABLE: ERC721 safeTransferFrom triggers onERC721Received callback
contract VulnerableNFTStaking {
    mapping(address => uint256) public rewards;
    mapping(uint256 => address) public stakedBy;
    
    function unstake(uint256 tokenId) external {
        require(stakedBy[tokenId] == msg.sender, "Not owner");
        
        // Calculate and transfer rewards BEFORE clearing state
        uint256 reward = calculateReward(tokenId);
        rewards[msg.sender] = 0;
        
        // safeTransferFrom triggers onERC721Received - REENTRANCY POINT
        nft.safeTransferFrom(address(this), msg.sender, tokenId);
        
        // State cleared AFTER transfer
        stakedBy[tokenId] = address(0);
    }
}

contract NFTReentrancyAttacker is IERC721Receiver {
    function onERC721Received(address, address, uint256 tokenId, bytes calldata) external returns (bytes4) {
        // Re-enter unstake for same token (stakedBy not yet cleared)
        if (stakedBy[tokenId] != address(0)) {
            staking.unstake(tokenId);
        }
        return IERC721Receiver.onERC721Received.selector;
    }
}
```

---

### Example 7: Cross-Contract Read-Only Reentrancy (Balancer) [HIGH]

**Real Exploits:**
- Sentiment (2023-04) - $1M Lost
- Market.xyz (2022-10) - $220K Lost

```solidity
// ❌ VULNERABLE: Queries Balancer during join/exit reentrancy window
contract VulnerableLending {
    IBalancerVault vault;
    
    function getCollateralValue(address token) public view returns (uint256) {
        // getPoolTokens returns manipulated values during join/exit
        (address[] memory tokens, uint256[] memory balances, ) = vault.getPoolTokens(poolId);
        
        // totalSupply NOT YET updated during join callback
        uint256 lpSupply = IERC20(lpToken).totalSupply();
        
        // Price = balances / supply (WRONG during reentrancy)
        return (balances[0] * 1e18) / lpSupply;
    }
    
    function borrow(uint256 amount) external {
        require(getCollateralValue(msg.sender) >= amount, "Undercollateralized");
        // ...
    }
}

// Protected pattern using Balancer's VaultReentrancyLib
contract SecureLending {
    function borrow(uint256 amount) external {
        // MUST check reentrancy state before using Balancer values
        VaultReentrancyLib.ensureNotInVaultContext(balancerVault);
        uint256 collateral = getCollateralValue(msg.sender);
        // ...
    }
}
```

---

### Example 8: Reward Manipulation via Reentrancy [CRITICAL]

**Real Exploit: Penpiexyz (2024-09) - $27M Lost**

```solidity
// ❌ VULNERABLE: Reward distribution exploitable via custom market creation
contract VulnerablePendleStaking {
    function batchHarvestMarketRewards(address[] calldata markets) external {
        for (uint i = 0; i < markets.length; i++) {
            // Calls external market contract - attacker controlled
            IMarket(markets[i]).redeemRewards(msg.sender);
        }
    }
}

// Attacker creates malicious market that triggers reentrancy during reward claim
contract PenpieAttacker {
    function claimRewards(address user) external returns (uint256[] memory) {
        // Called by PendleStaking during harvest
        // Attacker can re-deposit legitimate tokens during this callback
        // Then claim rewards for the new deposit in same transaction
        
        IERC20(agETH).approve(PendleRouter, type(uint256).max);
        // Add liquidity to legitimate pool during callback
        PendleRouter.addLiquiditySingleTokenKeepYt(...);
        // Deposit into staking - receives rewards intended for others
        PendleMarketDepositHelper.depositMarket(legitimateMarket, amount);
        
        return new uint256[](0);
    }
}
```

---

## Secure Implementation Patterns

### Fix 1: Checks-Effects-Interactions (CEI) Pattern

```solidity
// ✅ SECURE: State updates BEFORE external calls
function withdraw(uint256 amount) external {
    // CHECKS
    require(balances[msg.sender] >= amount, "Insufficient balance");
    
    // EFFECTS (state changes FIRST)
    balances[msg.sender] -= amount;
    
    // INTERACTIONS (external calls LAST)
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### Fix 2: ReentrancyGuard Modifier

```solidity
// ✅ SECURE: Using OpenZeppelin's ReentrancyGuard
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureVault is ReentrancyGuard {
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
    }
}
```

### Fix 3: Read-Only Reentrancy Protection (Balancer/Curve)

```solidity
// ✅ SECURE: Check Balancer vault reentrancy state
import "@balancer-labs/v2-pool-utils/contracts/lib/VaultReentrancyLib.sol";

contract SecureLending {
    IBalancerVault public vault;
    
    function liquidate(address user) external {
        // MUST check before using any Balancer pool data
        VaultReentrancyLib.ensureNotInVaultContext(vault);
        
        uint256 price = oracle.getPrice(collateralToken);
        // Safe to proceed...
    }
}

// For Curve pools - use separate view-only call to detect reentrancy
function checkCurveReentrancy(ICurvePool pool) internal view {
    // This will revert if in reentrancy state (Curve-specific)
    pool.remove_liquidity(0, [uint256(0), uint256(0)]);
}
```

### Fix 4: Callback Whitelist / Validation

```solidity
// ✅ SECURE: Validate callback source
contract SecureFlashLoan {
    mapping(address => bool) public activeLoans;
    
    function flashLoan(uint256 amount) external {
        require(!activeLoans[msg.sender], "Loan already active");
        activeLoans[msg.sender] = true;
        
        token.transfer(msg.sender, amount);
        IFlashBorrower(msg.sender).onFlashLoan(amount);
        
        require(token.balanceOf(address(this)) >= preBalance + fee, "Not repaid");
        activeLoans[msg.sender] = false;
    }
    
    function deposit() external {
        // Prevent deposits during active flash loan
        require(!activeLoans[msg.sender], "Cannot deposit during flash loan");
        // ...
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For

```
- External calls (.call, .transfer, .send) before state updates
- safeTransferFrom with ERC721/ERC1155 before state updates  
- Callbacks (onERC721Received, onFlashLoan, etc.) in execution flow
- View functions querying external protocols (Curve, Balancer) for price
- Custom hooks/callbacks in protocol designs
- Missing nonReentrant modifiers on state-changing functions
- Vyper contracts using @nonreentrant with version 0.2.15-0.3.0
```

### Audit Checklist

- [ ] All external calls follow CEI pattern
- [ ] Functions with ETH/token transfers have nonReentrant modifier
- [ ] View functions querying external pools check reentrancy state
- [ ] Balancer/Curve integrations use VaultReentrancyLib or equivalent
- [ ] Flash loan callbacks don't allow arbitrary state manipulation
- [ ] Custom hooks/callbacks are validated and access-controlled
- [ ] ERC721/ERC1155 safeTransfer callbacks handled safely
- [ ] Vyper compiler version checked (avoid 0.2.15-0.3.0 for @nonreentrant)

---

## Real-World Examples

### Critical Exploits ($10M+)

| Protocol | Date | Loss | Type | Chain |
|----------|------|------|------|-------|
| Rari Capital/Fei | 2022-04-30 | $80M | Classic + Cross-function | Ethereum |
| Curve (Vyper bug) | 2023-07-30 | $41M | Compiler bug + Classic | Ethereum |
| Penpiexyz | 2024-09-03 | $27M | Reward manipulation | Ethereum |
| Grim Finance | 2021-12-18 | $30M | Flash loan + Classic | Fantom |
| Cream Finance | 2021-08-30 | $18M | Flash loan + Classic | Ethereum |
| Revest Finance | 2022-03-27 | $11.2M | ERC1155 callback | Ethereum |

### High-Severity Exploits ($1M-$10M)

| Protocol | Date | Loss | Type | Chain |
|----------|------|------|------|-------|
| DFXFinance | 2022-11-10 | $4M | Flash callback | Ethereum |
| dForce | 2023-02-10 | $3.65M | Read-only (Curve) | Arbitrum |
| Conic Finance | 2023-07-21 | $3.25M | Read-only (Curve) | Ethereum |
| NFTTrader | 2023-12-16 | $3M | ERC721 callback | Ethereum |
| StarsArena | 2023-10-07 | $3M | Classic | Avalanche |
| Orion Protocol | 2023-02-03 | $3M | Classic | Ethereum/BSC |

### Medium-Severity Exploits ($100K-$1M)

| Protocol | Date | Loss | Type | Chain |
|----------|------|------|------|-------|
| Sturdy Finance | 2023-06-12 | $800K | Read-only (Balancer) | Ethereum |
| Sentiment | 2023-04-05 | $1M | Read-only (Balancer) | Arbitrum |
| Midas Capital | 2023-01-16 | $650K | Read-only (Curve) | Polygon |
| CloberDEX | 2024-12-10 | $501K | Custom hook | Base |
| Libertify | 2023-07-11 | $452K | Classic | Polygon |
| ArcadiaFi | 2023-07-10 | $400K | Classic | Optimism |
| Minterest | 2024-07-14 | ~$1M (427 ETH) | Classic | Ethereum |
| SumerMoney | 2024-04-12 | $350K | Classic | Arbitrum |
| EarningFarm | 2023-08-09 | $286K | Classic | BSC |
| Market.xyz | 2022-10-24 | $220K | Read-only (Balancer) | Polygon |
| Defrost | 2022-12-23 | $170K | Classic | Avalanche |
| BarleyFinance | 2024-01-28 | $130K | Classic | Ethereum |

### Lower-Severity Exploits (<$100K)

| Protocol | Date | Loss | Type | Chain |
|----------|------|------|------|-------|
| CAROLProtocol | 2023-11-30 | $53K | Price manipulation via reentrancy | BSC |
| XSDWETHpool | 2023-09-26 | ~$33K (56.9 BNB) | Classic | BSC |
| N00d Token | 2022-10-26 | $29K | Classic | Ethereum |
| NBLGAME | 2024-01-25 | $180K | Classic | BSC |
| MRP | 2024-07-02 | ~$10K (17 BNB) | Classic | BSC |
| RuggedArt | 2024-02-19 | $10K | Classic | Ethereum |
| EGGX | 2024-02-20 | ~$5K (2 ETH) | Classic | Ethereum |

### Historical Exploits (2021)

| Protocol | Date | Loss | Type |
|----------|------|------|------|
| Visor Finance | 2021-12-21 | $8.2M | Classic |
| XSURGE | 2021-08-17 | $5M | Flash loan + Classic |
| BurgerSwap | 2021-05-27 | Undisclosed | Math flaw + Classic |

---

## Prevention Guidelines

### Development Best Practices

1. **Always use CEI pattern** - State changes before external calls
2. **Apply nonReentrant to ALL public/external state-changing functions**
3. **Audit callback flows** - Map all possible re-entry points
4. **Use read-only reentrancy guards** for Balancer/Curve integrations
5. **Validate Vyper compiler versions** - Avoid 0.2.15-0.3.0 for reentrancy guards
6. **Whitelist callback sources** for flash loans and custom hooks

### Testing Requirements

- Unit tests for reentrancy scenarios on all withdrawal functions
- Integration tests with mock attacker contracts using callbacks
- Fuzzing of callback functions with arbitrary re-entry attempts
- Static analysis with Slither's reentrancy detectors
- Manual review of all external call sites

---

## References

### Technical Documentation
- [OpenZeppelin ReentrancyGuard](https://docs.openzeppelin.com/contracts/4.x/api/security#ReentrancyGuard)
- [Balancer VaultReentrancyLib](https://github.com/balancer-labs/balancer-v2-monorepo/blob/master/pkg/pool-utils/contracts/lib/VaultReentrancyLib.sol)
- [Curve Read-Only Reentrancy Advisory](https://chainsecurity.com/curve-read-only-reentrancy/)

### Security Research
- [DeFiHackLabs Repository](https://github.com/SunWeb3Sec/DeFiHackLabs)
- [Vyper Compiler Bug Analysis](https://hackmd.io/@LlamaRisk/BJzSKHNjn)
- [Read-Only Reentrancy Explained](https://medium.com/coinmonks/theoretical-practical-balancer-and-read-only-reentrancy-part-1-d6a21792066c)

---

## Keywords for Search

`reentrancy`, `reentrant`, `nonReentrant`, `read-only reentrancy`, `CEI pattern`, `checks-effects-interactions`, `callback`, `Balancer`, `Curve`, `get_virtual_price`, `remove_liquidity`, `flash loan`, `onERC721Received`, `onERC1155Received`, `ERC777`, `receive function`, `fallback function`, `cross-function reentrancy`, `cross-contract reentrancy`, `Vyper compiler bug`, `VaultReentrancyLib`, `double spend`, `recursive call`, `state manipulation`, `hook reentrancy`, `burnHook`, `mintHook`, `safeTransferFrom callback`

---

## Related Vulnerabilities

- [Flash Loan Attacks](../flash-loan/FLASH_LOAN_VULNERABILITIES.md)
- [Price Oracle Manipulation](../../oracle/chainlink/CHAINLINK_PRICE_FEED_VULNERABILITIES.md)
- [Vault Inflation Attack](../vault-inflation-attack/vault-inflation-attack.md)
- [ERC4626 Vulnerabilities](../../tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md)

---

## DeFiHackLabs Real-World Exploits (56 incidents)

**Category**: Reentrancy | **Total Losses**: $258.3M | **Sub-variants**: 7

### Sub-variant Breakdown

#### Reentrancy/Classic (42 exploits, $220.3M)

- **Rari Capital/Fei Protocol** (2022-04, $80.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2022-04/Rari_exp.sol`
- **Curve** (2023-07, $41.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2023-07/Curve_exp01.sol`
- **Grim Finance** (2021-12, $30.0M, fantom) | PoC: `DeFiHackLabs/src/test/2021-12/Grim_exp.sol`
- *... and 39 more exploits*

#### Reentrancy/Erc777 Callback (2 exploits, $25.2M)

- **LendfMe** (2020-04, $25.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2020-04/LendfMe_exp.sol`
- **UniSwapV1** (2020-04, $220K, ethereum) | PoC: `DeFiHackLabs/src/test/2020-04/uniswap-erc777.sol`

#### Reentrancy/Read Only (6 exploits, $9.6M)

- **dForce** (2023-02, $3.6M, arbitrum) | PoC: `DeFiHackLabs/src/test/2023-02/dForce_exp.sol`
- **Conic Finance** (2023-07, $3.2M, ethereum) | PoC: `DeFiHackLabs/src/test/2023-07/Conic_exp.sol`
- **Sentiment** (2023-04, $1.0M, arbitrum) | PoC: `DeFiHackLabs/src/test/2023-04/Sentiment_exp.sol`
- *... and 3 more exploits*

#### Reentrancy/Erc667 Callback (2 exploits, $3.2M)

- **Hundred Finance** (2022-03, $1.7M, gnosis) | PoC: `DeFiHackLabs/src/test/2022-03/HundredFinance_exp.sol`
- **Agave Finance** (2022-03, $1.5M, gnosis) | PoC: `DeFiHackLabs/src/test/2022-03/Agave_exp.sol`

#### Reentrancy/Reward Manipulation (1 exploits, $11K)

- **Penpiexyz_io** (2024-09, $11K, None)

#### Reentrancy/Nft Sell Callback (1 exploits, $138)

- **StepHeroNFTs** (2025-02, $138, bsc) | PoC: `DeFiHackLabs/src/test/2025-02/StepHeroNFTs_exp.sol`

#### Reentrancy/Cross Contract (2 exploits, N/A)

- **RariCapital** (2021-05, N/A, ethereum) | PoC: `DeFiHackLabs/src/test/2021-05/RariCapital_exp.sol`
- **Value Defi** (2021-05, N/A, bsc) | PoC: `DeFiHackLabs/src/test/2021-05/ValueDefi_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| Rari Capital/Fei Protocol | 2022-04-30 | $80.0M | Flashloan Attack + Reentrancy | ethereum |
| Curve | 2023-07-30 | $41.0M | Vyper Compiler Bug && Reentrancy | ethereum |
| Grim Finance | 2021-12-18 | $30.0M | Flashloan & Reentrancy | fantom |
| LendfMe | 2020-04-19 | $25.0M | ERC777 Reentrancy | ethereum |
| Cream Finance | 2021-08-30 | $18.0M | Flashloan Attack + Reentrancy | ethereum |
| Revest Finance | 2022-03-27 | $11.2M | Reentrancy | ethereum |
| Visor Finance | 2021-12-21 | $8.2M | Reentrancy | ethereum |
| XSURGE | 2021-08-17 | $5.0M | Flashloan Attack + Reentrancy | bsc |
| DeltaPrime | 2024-11-11 | $4.8M | Reentrancy | arbitrum |
| DFXFinance | 2022-11-10 | $4.0M | Reentrancy | ethereum |
| dForce | 2023-02-10 | $3.6M | Read-Only-Reentrancy | arbitrum |
| Conic Finance | 2023-07-21 | $3.2M | Read-Only-Reentrancy && MisConfiguration | ethereum |
| NFTTrader | 2023-12-16 | $3.0M | Reentrancy | ethereum |
| StarsArena | 2023-10-07 | $3.0M | Reentrancy | avalanche |
| Orion Protocol | 2023-02-03 | $3.0M | Reentrancy | ethereum |
| GoodDollar | 2023-12-16 | $2.0M | Lack of Input Validation & Reentrancy | ethereum |
| Paraluni | 2022-03-13 | $1.7M | Flashloan & Reentrancy | bsc |
| Hundred Finance | 2022-03-13 | $1.7M | ERC667 Reentrancy | gnosis |
| Agave Finance | 2022-03-15 | $1.5M | ERC667 Reentrancy | gnosis |
| Omni NFT | 2022-07-10 | $1.4M | Reentrancy | ethereum |
| Bacon Protocol | 2022-03-05 | $1.0M | Reentrancy | ethereum |
| Sentiment | 2023-04-05 | $1.0M | Read-Only-Reentrancy | arbitrum |
| Sturdy Finance | 2023-06-12 | $800K | Read-Only-Reentrancy | ethereum |
| MidasCapital | 2023-01-16 | $650K | Read-only Reentrancy | polygon |
| CloberDEX | 2024-12-10 | $501K | Reentrancy | base |
| PredyFinance | 2024-05-14 | $464K | Reentrancy | arbitrum |
| Libertify | 2023-07-11 | $452K | Reentrancy | polygon |
| ArcadiaFi | 2023-07-10 | $400K | Reentrancy | optimism |
| SumerMoney | 2024-04-12 | $350K | Reentrancy | base |
| EarningFram | 2023-08-09 | $286K | Reentrancy | ethereum |
| UniSwapV1 | 2020-04-18 | $220K | ERC777 Reentrancy | ethereum |
| Market | 2022-10-24 | $220K | Read-only Reentrancy | polygon |
| NBLGAME | 2024-01-25 | $180K | Reentrancy | optimism |
| Defrost | 2022-12-23 | $170K | Reentrancy | avalanche |
| BarleyFinance | 2024-01-28 | $130K | Reentrancy | ethereum |
| Paribus | 2023-04-11 | $100K | Reentrancy | arbitrum |
| Bizness | 2024-12-27 | $16K | Reentrancy | base |
| Penpiexyz_io | 2024-09-03 | $11K | Reentrancy and Reward Manipulation | None |
| Unverified_35bc | 2025-02-22 | $7K | Reentrancy | bsc |
| PeapodsFinance | 2024-01-29 | $1K | Reentrancy | ethereum |
| Minterest | 2024-07-14 | $427 | Reentrancy | mantle |
| SpankChain | 2018-10-07 | $155 | Reentrancy | ethereum |
| StepHeroNFTs | 2025-02-21 | $138 | Reentrancy On Sell NFT | bsc |
| XSDWETHpool | 2023-09-26 | $57 | Reentrancy | bsc |
| Game | 2024-02-11 | $20 | Reentrancy && Business Logic Flaw | ethereum |
| MRP | 2024-07-02 | $17 | Reentrancy | bsc |
| JAY | 2022-12-29 | $15 | Insufficient validation + Reentrancy | ethereum |
| RuggedArt | 2024-02-19 | $5 | reentrancy | ethereum |
| EGGX | 2024-02-20 | $2 | reentrancy | ethereum |
| uniclyNFT | 2023-09-16 | $1 | Reentrancy | ethereum |
| ... | ... | ... | +6 more exploits | ... |

### Top PoC References

- **Rari Capital/Fei Protocol** (2022-04, $80.0M): `DeFiHackLabs/src/test/2022-04/Rari_exp.sol`
- **Curve** (2023-07, $41.0M): `DeFiHackLabs/src/test/2023-07/Curve_exp01.sol`
- **Grim Finance** (2021-12, $30.0M): `DeFiHackLabs/src/test/2021-12/Grim_exp.sol`
- **LendfMe** (2020-04, $25.0M): `DeFiHackLabs/src/test/2020-04/LendfMe_exp.sol`
- **Cream Finance** (2021-08, $18.0M): `DeFiHackLabs/src/test/2021-08/Cream_exp.sol`
- **Revest Finance** (2022-03, $11.2M): `DeFiHackLabs/src/test/2022-03/Revest_exp.sol`
- **Visor Finance** (2021-12, $8.2M): `DeFiHackLabs/src/test/2021-12/Visor_exp.sol`
- **XSURGE** (2021-08, $5.0M): `DeFiHackLabs/src/test/2021-08/XSURGE_exp.sol`
- **DeltaPrime** (2024-11, $4.8M): `DeFiHackLabs/src/test/2024-11/DeltaPrime_exp.sol`
- **DFXFinance** (2022-11, $4.0M): `DeFiHackLabs/src/test/2022-11/DFX_exp.sol`

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

`Balancer_pool_state`, `Curve_remove_liquidity`, `DeFiHackLabs`, `ERC1155_hooks`, `ERC721_onReceived`, `ERC777_hooks`, `approve`, `attack`, `balanceOf`, `balance_check`, `batchHarvestMarketRewards`, `block.timestamp`, `borrow`, `burn`, `burnHook`, `callback_function`, `checkCurveReentrancy`, `claimRewards`, `defi`, `deposit`, `deposits`, `dex`, `exitMarket`, `external_call`, `fallback_function`, `flash_loan_callback`, `lending`, `multi_type`, `nft`, `real_exploit`, `receive_function`, `reentrancy`, `staking`, `state_update`, `vault`
