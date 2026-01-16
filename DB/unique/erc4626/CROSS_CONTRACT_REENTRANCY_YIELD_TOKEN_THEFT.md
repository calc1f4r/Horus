---
# Core Classification
protocol: Notional Exponent
chain: everychain
category: reentrancy
vulnerability_type: cross_contract_reentrancy

# Attack Vector Details
attack_type: yield_token_theft
affected_component: WithdrawalRequestManager

# Technical Primitives
primitives:
  - cross_contract_reentrancy
  - balance_accounting
  - multi_vault_architecture
  - uniswap_callback
  - erc4626_deposit
  - erc4626_withdraw

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - erc4626
  - reentrancy
  - cross_contract
  - yield_strategy
  - withdrawal_manager
  - uniswap_v3

# Version Info
language: solidity
version: ">=0.8.0"
---

## Reference
- [Source Report]: reports/erc4626_findings/h-1-cross-contract-reentrancy-allows-yield_token-theft-for-the-genericerc4626-wi.md

## Cross-Contract Reentrancy Allows YIELD_TOKEN Theft in Multi-Vault ERC4626 Systems

**Case Study: Notional Exponent - Sherlock 2025**

### Overview

A sophisticated cross-contract reentrancy vulnerability in ERC4626-based yield strategies where a shared `WithdrawalRequestManager` serves multiple vault strategies. The attacker exploits the timing gap between balance snapshot and state update during staking operations, using a Uniswap V3 swap callback to reenter and manipulate the yield token balance accounting.

This represents a novel attack vector combining:
1. Multi-vault architecture with shared withdrawal manager
2. Balance-based accounting before external calls
3. Uniswap V3 swap callbacks as reentrancy vectors
4. Pending withdrawal requests as "free" yield tokens

### Vulnerability Description

#### Root Cause

The `WithdrawalRequestManager.stakeTokens()` function captures the initial `YIELD_TOKEN` balance **before** executing a potentially reentrant trade operation (`_preStakingTrade`). This creates a window where:

1. The initial balance is recorded
2. An external call is made (Uniswap swap) that can trigger reentrancy
3. During reentrancy, another vault can call `initiateWithdraw()` which transfers yield tokens OUT
4. When execution returns, the final balance minus initial balance is calculated
5. The "delta" appears larger than it should be because the initial balance included tokens that were later withdrawn

```solidity
// ❌ VULNERABLE: Balance captured before reentrant trade
function stakeTokens(
    address depositToken,
    uint256 amount,
    bytes calldata data
) external override onlyApprovedVault returns (uint256 yieldTokensMinted) {
    // VULNERABILITY: Balance snapshot taken BEFORE external call
    uint256 initialYieldTokenBalance = ERC20(YIELD_TOKEN).balanceOf(address(this));
    
    ERC20(depositToken).safeTransferFrom(msg.sender, address(this), amount);
    
    // External call that can trigger reentrancy via Uniswap swap
    (uint256 stakeTokenAmount, bytes memory stakeData) = _preStakingTrade(depositToken, amount, data);
    
    _stakeTokens(stakeTokenAmount, stakeData);
    
    // Inflated delta due to tokens withdrawn during reentrancy
    yieldTokensMinted = ERC20(YIELD_TOKEN).balanceOf(address(this)) - initialYieldTokenBalance;
    ERC20(YIELD_TOKEN).safeTransfer(msg.sender, yieldTokensMinted);
}
```

#### Why This is Unique

1. **Multi-Vault Requirement**: Exploitation requires the `WithdrawalRequestManager` to serve multiple vaults (whitelisted via `isApprovedVault`)
2. **Pending Requests as Attack Vector**: Other users' pending withdrawal requests temporarily hold `YIELD_TOKEN` in the manager - these become the theft target
3. **Uniswap as Reentrancy Vector**: The Uniswap V3 multihop path allows inserting a malicious token/pool that executes arbitrary code during swap
4. **Balance Accounting Flaw**: The vulnerability isn't a simple reentrancy but a timing issue with balance-based accounting

#### Attack Scenario

**Prerequisites:**
- `WithdrawalRequestManager` manages multiple vault strategies
- Other users have pending withdrawal requests (yield tokens sitting in manager)
- Attacker can control a vault that is whitelisted OR exploit via EIP-7702

**Step-by-Step Attack:**

1. **Attacker identifies target**: Pending withdrawal requests hold `YIELD_TOKEN` in the manager
2. **Prepare malicious Uniswap path**: Create a fake token and pool that calls back to attacker during swap
3. **Initiate deposit via `enterPosition`**:
   ```
   LendingRouter.enterPosition() 
   → YieldStrategy.mintShares()
   → WithdrawalRequestManager.stakeTokens()
   ```
4. **Balance snapshot taken**: `initialYieldTokenBalance` includes pending withdrawal tokens
5. **Malicious swap executed**: During `_preStakingTrade`, Uniswap calls attacker's fake token
6. **Reentrancy trigger**: Fake token calls `initiateWithdraw` from a DIFFERENT whitelisted vault
7. **Yield tokens transferred out**: `YIELD_TOKEN.safeTransferFrom(manager, vault, amount)`
8. **Execution returns**: Final balance - initial balance = inflated delta
9. **Attacker receives extra shares**: More `YIELD_TOKEN` minted than legitimate deposit value

```
                                    WithdrawalRequestManager
                                    ┌────────────────────────────────┐
                                    │  YIELD_TOKEN Balance: 100      │
                                    │  (50 from Vault A pending)     │
                                    │  (50 from Vault B pending)     │
                                    └────────────────────────────────┘
                                                  │
         ┌────────────────────────────────────────┼────────────────────────────────────────┐
         │                                        │                                        │
         ▼                                        ▼                                        ▼
   ┌───────────┐                           ┌───────────┐                           ┌───────────┐
   │  Vault A  │                           │  Vault B  │                           │ Attacker  │
   │(Whitelisted)                          │(Whitelisted)                          │  Vault C  │
   └───────────┘                           └───────────┘                           └───────────┘
                                                                                         │
                                                                                         │ 1. Call stakeTokens()
                                                                                         │    (initial balance = 100)
                                                                                         ▼
                                                                                   ┌───────────┐
                                                                                   │ Uniswap   │
                                                                                   │ Swap      │
                                                                                   └───────────┘
                                                                                         │
                                                                                         │ 2. Callback to fake token
                                                                                         ▼
                                                                                   ┌───────────┐
                                                                                   │ Fake Token│
                                                                                   │ Reenter   │
                                                                                   └───────────┘
                                                                                         │
                                                                                         │ 3. Call initiateWithdraw
                                                                                         │    from Vault A
                                                                                         ▼
                                                                          ┌────────────────────────────────┐
                                                                          │  YIELD_TOKEN transferred from  │
                                                                          │  Manager to Vault A: 50        │
                                                                          │  New Balance: 50               │
                                                                          └────────────────────────────────┘
                                                                                         │
                                                                                         │ 4. Swap completes
                                                                                         │    Final - Initial = 
                                                                                         │    (50 + new) - 100
                                                                                         │    = inflated delta
                                                                                         ▼
                                                                          ┌────────────────────────────────┐
                                                                          │  Attacker gets credited for    │
                                                                          │  tokens they didn't deposit    │
                                                                          └────────────────────────────────┘
```

### Vulnerable Pattern Examples

**Example 1: Balance Snapshot Before External Call** [Severity: HIGH]
```solidity
// ❌ VULNERABLE: Classic balance accounting before reentrancy
function stakeTokens(
    address depositToken,
    uint256 amount,
    bytes calldata data
) external override onlyApprovedVault returns (uint256 yieldTokensMinted) {
    // Balance captured BEFORE potential reentrancy
    uint256 initialYieldTokenBalance = ERC20(YIELD_TOKEN).balanceOf(address(this));
    
    ERC20(depositToken).safeTransferFrom(msg.sender, address(this), amount);
    
    // External call - reentrancy point via Uniswap callback
    (uint256 stakeTokenAmount, bytes memory stakeData) = _preStakingTrade(depositToken, amount, data);
    
    _stakeTokens(stakeTokenAmount, stakeData);
    
    // Delta calculation is corrupted if balance changed during external call
    yieldTokensMinted = ERC20(YIELD_TOKEN).balanceOf(address(this)) - initialYieldTokenBalance;
    ERC20(YIELD_TOKEN).safeTransfer(msg.sender, yieldTokensMinted);
}
```

**Example 2: Uniswap Path Validation Insufficient** [Severity: HIGH]
```solidity
// ❌ VULNERABLE: Only validates first and last tokens, not middle path
function _exactInBatch(address from, Trade memory trade) private pure returns (bytes memory) {
    UniV3BatchData memory data = abi.decode(trade.exchangeData, (UniV3BatchData));

    // Only checks start and end tokens - middle path can be malicious
    require(32 <= data.path.length);
    require(_toAddress(data.path, 0) == _getTokenAddress(trade.sellToken));
    require(_toAddress(data.path, data.path.length - 20) == _getTokenAddress(trade.buyToken));
    
    // Attacker can insert: [token, fee, MALICIOUS_TOKEN, fee, token]
    ISwapRouter.ExactInputParams memory params = ISwapRouter.ExactInputParams(
        data.path, from, trade.deadline, trade.amount, trade.limit
    );

    return abi.encodeWithSelector(ISwapRouter.exactInput.selector, params);
}
```

**Example 3: Missing Reentrancy Guard on Cross-Contract Functions** [Severity: HIGH]
```solidity
// ❌ VULNERABLE: No reentrancy protection on initiateWithdraw
function initiateWithdraw(
    address account,
    uint256 yieldTokenAmount,
    uint256 sharesAmount,
    bytes calldata data
) external override onlyApprovedVault returns (uint256 requestId) {  // No nonReentrant!
    WithdrawRequest storage accountWithdraw = s_accountWithdrawRequest[msg.sender][account];
    if (accountWithdraw.requestId != 0) revert ExistingWithdrawRequest(...);

    // This transfer can happen during stakeTokens() reentrancy
    ERC20(YIELD_TOKEN).safeTransferFrom(msg.sender, address(this), yieldTokenAmount);
    
    requestId = _initiateWithdrawImpl(account, yieldTokenAmount, data);
    // ... state updates
}
```

### Impact Analysis

#### Technical Impact
- **Inflated Share Minting**: Attacker receives more vault shares than their deposit value
- **Yield Token Theft**: Other users' pending withdrawal tokens effectively stolen
- **Accounting Corruption**: Balance-based accounting becomes unreliable

#### Financial Impact
- **Direct Fund Loss**: Estimated at value of all pending withdrawal requests
- **Attack Amplification**: Can be maximized by targeting `forceWithdraw` operations
- **Minimal Attacker Cost**: Only requires gas and temporary liquidity for malicious pool

#### Affected Scenarios
- Multi-vault yield aggregators with shared withdrawal managers
- ERC4626 vaults using DEX swaps for deposits/withdrawals
- Any protocol using balance deltas across external calls

### Secure Implementation

**Fix 1: Capture Balance After External Calls**
```solidity
// ✅ SECURE: Balance snapshot after all external calls
function stakeTokens(
    address depositToken,
    uint256 amount,
    bytes calldata data
) external override onlyApprovedVault returns (uint256 yieldTokensMinted) {
    ERC20(depositToken).safeTransferFrom(msg.sender, address(this), amount);
    
    // External call first
    (uint256 stakeTokenAmount, bytes memory stakeData) = _preStakingTrade(depositToken, amount, data);
    
    // Balance captured AFTER reentrancy window
    uint256 initialYieldTokenBalance = ERC20(YIELD_TOKEN).balanceOf(address(this));
    
    _stakeTokens(stakeTokenAmount, stakeData);
    
    yieldTokensMinted = ERC20(YIELD_TOKEN).balanceOf(address(this)) - initialYieldTokenBalance;
    ERC20(YIELD_TOKEN).safeTransfer(msg.sender, yieldTokensMinted);
}
```

**Fix 2: Cross-Contract Reentrancy Lock**
```solidity
// ✅ SECURE: Shared reentrancy lock across contracts
abstract contract CrossContractReentrancyGuard {
    bytes32 private constant REENTRANCY_SLOT = keccak256("reentrancy.lock");
    
    modifier crossNonReentrant() {
        bytes32 slot = REENTRANCY_SLOT;
        uint256 locked;
        assembly { locked := sload(slot) }
        require(locked == 0, "Reentrant");
        assembly { sstore(slot, 1) }
        _;
        assembly { sstore(slot, 0) }
    }
}

// Apply to both stakeTokens and initiateWithdraw
function stakeTokens(...) external crossNonReentrant { ... }
function initiateWithdraw(...) external crossNonReentrant { ... }
```

**Fix 3: Strict Path Validation**
```solidity
// ✅ SECURE: Whitelist all tokens in swap path
function _exactInBatch(address from, Trade memory trade) private view returns (bytes memory) {
    UniV3BatchData memory data = abi.decode(trade.exchangeData, (UniV3BatchData));
    
    // Validate EVERY token in path
    uint256 pathLength = data.path.length;
    for (uint256 i = 0; i < pathLength; i += 23) {  // 20 bytes token + 3 bytes fee
        address token = _toAddress(data.path, i);
        require(whitelistedTokens[token], "Invalid path token");
    }
    
    // ... rest of implementation
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Balance snapshot before external calls: balanceOf() ... externalCall() ... balanceOf()
- Multi-vault architecture with shared managers: isApprovedVault[vault]
- Uniswap/DEX integration with user-controlled paths
- Missing nonReentrant on paired functions (stake + withdraw)
- Cross-contract state dependencies without locks
```

#### Static Analysis Rules
```yaml
# Semgrep rule for balance accounting before external calls
rules:
  - id: balance-before-external-call
    pattern-either:
      - pattern: |
          $BALANCE = $TOKEN.balanceOf($ADDR);
          ...
          $EXTERNAL_CALL(...);
          ...
          $DELTA = $TOKEN.balanceOf($ADDR) - $BALANCE;
    message: "Balance snapshot before external call - potential reentrancy"
    severity: WARNING
```

#### Audit Checklist
- [ ] Check if balance snapshots are taken before external calls
- [ ] Verify reentrancy guards on all state-modifying functions
- [ ] Review multi-vault/multi-contract dependencies
- [ ] Analyze DEX integration paths for callback vectors
- [ ] Test cross-contract reentrancy scenarios

### Real-World Context

#### Discovery
- **Protocol**: Notional Exponent
- **Audit Firm**: Sherlock
- **Date**: 2025
- **Finders**: talfao, KungFuPanda, 0xBoraichoT, Ragnarok

#### Similar Patterns
- Read-only reentrancy in Curve pools
- Cross-function reentrancy in lending protocols
- Flash loan + reentrancy combinations

### Prevention Guidelines

#### Development Best Practices
1. Always capture balance snapshots AFTER all external calls
2. Use cross-contract reentrancy guards for multi-contract systems
3. Strictly validate all tokens in DEX swap paths
4. Consider pull-over-push patterns for token accounting

#### Testing Requirements
- Unit tests for reentrancy via DEX callbacks
- Integration tests with malicious token contracts
- Fuzz testing with arbitrary swap paths

### References

#### Technical Documentation
- [EIP-7702: Set EOA account code](https://eips.ethereum.org/EIPS/eip-7702)
- [Uniswap V3 Swap Callbacks](https://docs.uniswap.org/contracts/v3/guides/swaps/single-swaps)
- [Cross-Contract Reentrancy Patterns](https://consensys.io/diligence/audits/)

#### Security Research
- [Read-Only Reentrancy](https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem/)
- [Balance-Based Accounting Vulnerabilities](https://samczsun.com/two-rights-might-make-a-wrong/)

### Keywords for Search

`cross-contract reentrancy`, `ERC4626 reentrancy`, `yield token theft`, `withdrawal manager`, `multi-vault reentrancy`, `balance accounting vulnerability`, `uniswap callback reentrancy`, `DEX swap reentrancy`, `cross-function reentrancy`, `shared manager vulnerability`, `balance delta manipulation`, `stakeTokens reentrancy`, `initiateWithdraw exploit`, `vault strategy reentrancy`, `EIP-7702 attack`, `pending withdrawal theft`, `yield strategy exploit`, `balance snapshot timing`, `external call ordering`, `cross-contract state manipulation`

### Related Vulnerabilities

- [ERC4626 First Depositor Attack](../ERC4626_VAULT_VULNERABILITIES.md#first-depositor-attack)
- [Read-Only Reentrancy](../../reentrancy/READ_ONLY_REENTRANCY.md)
- [Flash Loan Attacks](../../economic/FLASH_LOAN_ATTACKS.md)
