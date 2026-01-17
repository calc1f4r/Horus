---
# Core Classification (Required)
protocol: generic
chain: everychain
category: token_handling
vulnerability_type: fee_on_transfer_incompatibility

# Attack Vector Details (Required)
attack_type: accounting_error|token_incompatibility
affected_component: token_transfer|deposit_logic|withdrawal_logic

# Technical Primitives (Required)
primitives:
  - transferFrom
  - transfer
  - balanceOf
  - token_accounting
  - fee_deduction
  - deflationary_token
  - rebasing_token
  - ERC20
  - deposit
  - withdraw
  - actual_amount

# Impact Classification (Required)
severity: medium
impact: incorrect_accounting|fund_loss|transaction_revert
exploitability: 0.70
financial_impact: medium

# Context Tags
tags:
  - defi
  - vault
  - erc20
  - token
  - fee_on_transfer
  - deflationary
  - rebasing
  - accounting
  - deposit
  - withdraw

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Fee-on-Transfer Token Vulnerability Reports
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| PoolTogether - Deposits Don't Work with FoT Tokens | `reports/yield_protocol_findings/m-01-deposits-dont-work-with-fee-on-transfer-tokens.md` | MEDIUM | Code4rena |
| prePO - Free Collateral Token with FoT | `reports/yield_protocol_findings/m-02-the-recipient-receives-free-collateral-token-if-an-erc20-token-that-deducts.md` | MEDIUM | Code4rena |
| As4626 - Fee on Transfer Token Breaks Accounting | `reports/yield_protocol_findings/m-06-fee-on-transfer-token-will-break-accounting.md` | MEDIUM | Code4rena |
| Tradable - Contracts Don't Support Fees/Rebasing | `reports/yield_protocol_findings/contracts-do-not-support-tokens-with-fees-or-rebasing-tokens.md` | HIGH | Spearbit |
| Variable Balance Token Causing Fund Lock | `reports/yield_protocol_findings/m-06-variable-balance-token-causing-fund-lock-and-loss.md` | MEDIUM | Sherlock |

### External Links
- [Weird ERC20 Tokens - Fee-on-Transfer](https://github.com/d-xo/weird-erc20#fee-on-transfer)
- [OpenZeppelin SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol)

---

# Fee-on-Transfer Token Incompatibility - Comprehensive Database

**A Complete Pattern-Matching Guide for Token Transfer Security Audits**

---

## Table of Contents

1. [Overview](#overview)
2. [Vulnerability Description](#vulnerability-description)
3. [Vulnerable Pattern Examples](#vulnerable-pattern-examples)
4. [Impact Analysis](#impact-analysis)
5. [Secure Implementation](#secure-implementation)
6. [Detection Patterns](#detection-patterns)
7. [Real-World Examples](#real-world-examples)
8. [Prevention Guidelines](#prevention-guidelines)

---

## Overview

Fee-on-Transfer (FoT) token incompatibility occurs when protocols assume that the amount specified in a `transfer()` or `transferFrom()` call equals the amount actually received by the destination. Many ERC20 tokens (deflationary tokens, tax tokens, rebasing tokens) deduct fees on transfer, causing the received amount to be less than the specified amount. This leads to accounting discrepancies, transaction reverts, and potential fund loss.

> **Root Cause Statement**: This vulnerability exists because protocols use the transfer amount parameter for internal accounting without measuring the actual received amount, leading to over-accounting of assets when fee-on-transfer tokens deduct fees during transfer.

**Observed Frequency**: 30+ reports analyzed across major audit firms
**Consensus Severity**: MEDIUM (can be HIGH if protocol claims FoT support)
**Common Tokens**: USDT (potential), PAXG, SAFEMOON, deflationary meme tokens
**Affected Protocols**: Vaults, DEXs, lending pools, staking contracts, any token-handling contract

---

## Vulnerability Description

### Root Cause

The fundamental issue is the assumption that:
```
amount_sent == amount_received
```

For fee-on-transfer tokens:
```
amount_received = amount_sent - fee
```

When protocols use `amount_sent` for accounting but only receive `amount_received`, they over-account assets by the fee amount.

### Token Types Affected

| Token Type | Behavior | Example Tokens |
|------------|----------|----------------|
| Deflationary | Burns/redirects % on transfer | SAFEMOON, many meme coins |
| Fee-on-Transfer | Takes fee to treasury/holders | USDT (can enable), PAXG |
| Rebasing Up | Balance increases over time | aTokens, stETH |
| Rebasing Down | Balance decreases over time | Ampleforth during contraction |
| Elastic Supply | Adjusts supply dynamically | OHM, AMPL |

### Attack/Failure Scenarios

**Scenario 1: Deposit Over-Accounting**
1. User deposits 1000 SAFEMOON (5% fee)
2. Protocol records 1000 SAFEMOON received
3. Actually receives 950 SAFEMOON
4. User credited with 1000 worth of shares
5. Protocol becomes insolvent by 50 SAFEMOON

**Scenario 2: Transaction Revert**
1. User deposits 1000 FoT tokens
2. Protocol tries to use full 1000 for downstream operation
3. Only 950 available
4. Transaction reverts with insufficient balance

**Scenario 3: Withdrawal Drain**
1. Multiple users deposit with FoT tokens
2. Each deposit over-accounts by fee amount
3. Early withdrawers get full credited amount
4. Later withdrawers face insufficient funds

---

## Vulnerable Pattern Examples

**Example 1: Direct Amount Usage in Deposit** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-01-deposits-dont-work-with-fee-on-transfer-tokens.md`
```solidity
// ❌ VULNERABLE: Uses _amount for accounting without measuring actual received
function deposit(uint256 _amount) external {
    // Transfer tokens from user
    token.transferFrom(msg.sender, address(this), _amount);
    
    // VULNERABLE: Assumes full _amount was received
    // With FoT token, actual received = _amount - fee
    balances[msg.sender] += _amount;  // Over-credits user
    totalDeposits += _amount;          // Over-accounts total
}
```

**Example 2: Vault Share Calculation with FoT** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-06-fee-on-transfer-token-will-break-accounting.md`
```solidity
// ❌ VULNERABLE: ERC4626 vault without FoT support
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = previewDeposit(assets);  // Calculates based on assets param
    
    // Transfer may receive less than 'assets' for FoT tokens
    asset.transferFrom(msg.sender, address(this), assets);
    
    // VULNERABLE: Mints shares based on 'assets', not actual received
    _mint(receiver, shares);
    
    emit Deposit(msg.sender, receiver, assets, shares);
}
```

**Example 3: Hook/Callback with Wrong Amount** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-02-the-recipient-receives-free-collateral-token-if-an-erc20-token-that-deducts.md`
```solidity
// ❌ VULNERABLE: Passes original amount to hook, not actual received
function deposit(uint256 _amount, address _recipient) external {
    baseToken.transferFrom(msg.sender, address(this), _amount);
    
    // VULNERABLE: Hook receives _amount, but contract has less
    depositHook.hook(_recipient, _amount);
    
    // Calculate collateral based on wrong amount
    uint256 collateralMintAmount = (_amount - fee) * 1e18 / baseTokenDenominator;
    _mint(_recipient, collateralMintAmount);
}
```

**Example 4: Protocol Fee Calculation Error** [MEDIUM]
```solidity
// ❌ VULNERABLE: Protocol fee calculated on assumed amount
function depositWithFee(uint256 _amount) external {
    token.transferFrom(msg.sender, address(this), _amount);
    
    // VULNERABLE: Protocol fee calculated on _amount, not actual
    uint256 protocolFee = _amount * PROTOCOL_FEE_BPS / 10000;
    uint256 userCredit = _amount - protocolFee;
    
    // FoT already took fee, now protocol takes another
    // User gets double-charged: FoT fee + protocol fee on inflated amount
    balances[msg.sender] += userCredit;
}
```

**Example 5: Downstream Call with Insufficient Balance** [MEDIUM]
```solidity
// ❌ VULNERABLE: Uses _amount for downstream call
function depositAndStake(uint256 _amount) external {
    token.transferFrom(msg.sender, address(this), _amount);
    
    // VULNERABLE: Tries to stake full _amount, but have less due to FoT fee
    // This will REVERT with insufficient balance
    stakingPool.stake(_amount);
    
    // Even if it doesn't revert, over-credits stake amount
    stakedBalance[msg.sender] += _amount;
}
```

**Example 6: Rebasing Token Balance Mismatch** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-06-variable-balance-token-causing-fund-lock-and-loss.md`
```solidity
// ❌ VULNERABLE: Doesn't track rebasing token changes
contract RebasingVault {
    mapping(address => uint256) public deposits;
    uint256 public totalDeposits;
    
    function deposit(uint256 _amount) external {
        rebasingToken.transferFrom(msg.sender, address(this), _amount);
        deposits[msg.sender] += _amount;
        totalDeposits += _amount;
    }
    
    function withdraw() external {
        uint256 userDeposit = deposits[msg.sender];
        deposits[msg.sender] = 0;
        totalDeposits -= userDeposit;
        
        // VULNERABLE: If rebase DOWN occurred, this may revert
        // Contract has less tokens than recorded
        rebasingToken.transfer(msg.sender, userDeposit);
    }
}
```

---

## Impact Analysis

### Technical Impact

- **Over-Accounting**: Internal records exceed actual token balance
- **Transaction Reverts**: Operations fail due to insufficient balance
- **Share Inflation**: Users receive more shares than deserved
- **Accounting Drift**: Cumulative errors compound over time
- **State Corruption**: Protocol state becomes inconsistent

### Business Impact

- **Protocol Insolvency**: Liabilities exceed assets
- **Last Withdrawer Loss**: Final users cannot withdraw
- **Fee Revenue Loss**: Protocol fees calculated on wrong amounts
- **Integration Failures**: Downstream protocols receive wrong amounts
- **Reputation Damage**: Users lose funds unexpectedly

### Affected Scenarios

| Scenario | Risk Level | Notes |
|----------|------------|-------|
| Protocol claims any ERC20 support | HIGH | Must handle FoT correctly |
| USDT as base token | MEDIUM | Can enable fee any time |
| Multi-token vaults | HIGH | Different tokens, different behaviors |
| Cross-chain bridges | HIGH | Amount mismatch causes issues |
| Yield aggregators | MEDIUM | Compounds accounting errors |

### Severity Factors

- **Higher Severity**: Protocol explicitly supports FoT tokens
- **Higher Severity**: Critical financial operations (lending, liquidation)
- **Lower Severity**: Protocol documentation excludes FoT tokens
- **Lower Severity**: Whitelist-only token support

---

## Secure Implementation

**Fix 1: Balance Difference Measurement (Recommended)**
```solidity
// ✅ SECURE: Measure actual received amount
function deposit(uint256 _amount) external returns (uint256 actualReceived) {
    uint256 balanceBefore = token.balanceOf(address(this));
    token.transferFrom(msg.sender, address(this), _amount);
    uint256 balanceAfter = token.balanceOf(address(this));
    
    // Calculate actual received amount
    actualReceived = balanceAfter - balanceBefore;
    
    // Use actualReceived for all accounting
    balances[msg.sender] += actualReceived;
    totalDeposits += actualReceived;
    
    emit Deposit(msg.sender, actualReceived);
}
```

**Fix 2: ERC4626 with FoT Support**
```solidity
// ✅ SECURE: ERC4626 vault with fee-on-transfer support
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    uint256 balanceBefore = asset.balanceOf(address(this));
    asset.transferFrom(msg.sender, address(this), assets);
    uint256 actualAssets = asset.balanceOf(address(this)) - balanceBefore;
    
    // Calculate shares based on ACTUAL received, not requested
    shares = previewDeposit(actualAssets);
    
    require(shares > 0, "Zero shares");
    _mint(receiver, shares);
    
    emit Deposit(msg.sender, receiver, actualAssets, shares);
}
```

**Fix 3: Explicit FoT Token Rejection**
```solidity
// ✅ SECURE: Explicitly reject FoT tokens
function deposit(uint256 _amount) external {
    uint256 balanceBefore = token.balanceOf(address(this));
    token.transferFrom(msg.sender, address(this), _amount);
    uint256 balanceAfter = token.balanceOf(address(this));
    
    uint256 actualReceived = balanceAfter - balanceBefore;
    
    // Reject if fee was deducted (FoT token detected)
    require(actualReceived == _amount, "Fee-on-transfer tokens not supported");
    
    balances[msg.sender] += _amount;
}
```

**Fix 4: Whitelist Approach**
```solidity
// ✅ SECURE: Only allow vetted tokens
mapping(address => bool) public approvedTokens;

function deposit(address tokenAddress, uint256 _amount) external {
    require(approvedTokens[tokenAddress], "Token not approved");
    
    IERC20(tokenAddress).transferFrom(msg.sender, address(this), _amount);
    balances[msg.sender][tokenAddress] += _amount;
}

// Admin adds only non-FoT tokens after verification
function approveToken(address tokenAddress) external onlyAdmin {
    // Verify token behavior off-chain before approving
    approvedTokens[tokenAddress] = true;
}
```

**Fix 5: Share-Based Tracking for Rebasing Tokens**
```solidity
// ✅ SECURE: Use shares for rebasing token tracking
contract RebasingVault {
    uint256 public totalShares;
    mapping(address => uint256) public userShares;
    
    function deposit(uint256 _amount) external returns (uint256 shares) {
        uint256 balanceBefore = rebasingToken.balanceOf(address(this));
        rebasingToken.transferFrom(msg.sender, address(this), _amount);
        uint256 actualReceived = rebasingToken.balanceOf(address(this)) - balanceBefore;
        
        // Convert to shares (proportional ownership)
        if (totalShares == 0) {
            shares = actualReceived;
        } else {
            shares = actualReceived * totalShares / balanceBefore;
        }
        
        userShares[msg.sender] += shares;
        totalShares += shares;
    }
    
    function withdraw(uint256 shares) external returns (uint256 assets) {
        // Calculate proportional assets at current balance
        assets = shares * rebasingToken.balanceOf(address(this)) / totalShares;
        
        userShares[msg.sender] -= shares;
        totalShares -= shares;
        
        rebasingToken.transfer(msg.sender, assets);
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For

```
Anti-Patterns (VULNERABLE):
- transferFrom(sender, address(this), amount) followed by direct amount usage
- amount parameter used for accounting without balance check
- No balanceBefore/balanceAfter measurement
- Downstream calls using transfer amount, not actual received
- Hook/callback receives transfer amount parameter
- totalDeposits += amount without verification

Safe Patterns (SECURE):
- balanceBefore = balanceOf(address(this)) before transfer
- balanceAfter = balanceOf(address(this)) after transfer
- actualReceived = balanceAfter - balanceBefore
- All accounting uses actualReceived
- require(actualReceived == amount) for FoT rejection
- Token whitelist with verification process
```

### Semgrep Detection Rule

```yaml
rules:
  - id: fee-on-transfer-vulnerability
    patterns:
      - pattern: |
          $TOKEN.transferFrom($SENDER, $RECEIVER, $AMOUNT);
          ...
          $VAR = $AMOUNT;
      - pattern-not: |
          $BEFORE = $TOKEN.balanceOf(...);
          $TOKEN.transferFrom(...);
          $AFTER = $TOKEN.balanceOf(...);
    message: "Potential fee-on-transfer vulnerability - amount used without balance check"
    severity: WARNING
```

### Audit Checklist

- [ ] Does the protocol claim to support any ERC20 token?
- [ ] Is balance-before/balance-after pattern used for transfers?
- [ ] Are downstream operations using actual received amount?
- [ ] Is there explicit FoT token rejection if not supported?
- [ ] Is there a token whitelist mechanism?
- [ ] Are rebasing tokens handled with share-based accounting?
- [ ] What happens if USDT enables its fee switch?
- [ ] Are protocol fees calculated on actual received amounts?
- [ ] Do hooks/callbacks receive correct amounts?
- [ ] Are withdrawal amounts checked against actual balance?

---

## Real-World Examples

### Known Exploits & Findings

| Protocol | Year | Audit Firm | Severity | Resolution |
|----------|------|------------|----------|------------|
| PoolTogether | 2021 | Code4rena | MEDIUM | Acknowledged (won't support) |
| prePO | 2022 | Code4rena | MEDIUM | Fixed |
| Tradable | 2023 | Spearbit | HIGH | Acknowledged |
| Multiple Vaults | 2023-2024 | Various | MEDIUM | Various |

### Common Problematic Tokens

| Token | Type | Risk |
|-------|------|------|
| USDT | Potential FoT | Can enable fee anytime |
| PAXG | FoT | Has transfer fee |
| SAFEMOON | Deflationary | Burns on transfer |
| stETH | Rebasing | Balance changes |
| aTokens | Rebasing | Balance increases |
| AMPL | Elastic | Supply adjusts |

---

## Prevention Guidelines

### Development Best Practices

1. **Always use balance difference pattern** for token transfers
2. **Document token support** clearly (FoT supported or not)
3. **Implement token whitelists** for critical protocols
4. **Test with FoT mock tokens** in test suite
5. **Consider USDT's fee switch** even if currently disabled
6. **Use share-based accounting** for rebasing token support

### Testing Requirements

```solidity
// Required tests for FoT token handling
contract FoTTokenTest {
    // Mock FoT token with 5% fee
    MockFoTToken fotToken;
    
    function testDepositWithFoTToken() public {
        uint256 depositAmount = 1000e18;
        uint256 expectedReceived = 950e18; // 5% fee
        
        fotToken.approve(address(vault), depositAmount);
        vault.deposit(depositAmount);
        
        // Should account for actual received, not requested
        assertEq(vault.balanceOf(address(this)), expectedReceived);
    }
    
    function testWithdrawWithFoTToken() public {
        // Ensure withdrawal doesn't over-withdraw
    }
    
    function testFoTTokenRejection() public {
        // If protocol doesn't support FoT, should revert
        vm.expectRevert("Fee-on-transfer tokens not supported");
        vault.deposit(depositAmount);
    }
}
```

---

## Keywords for Search

`fee on transfer`, `fee-on-transfer`, `FoT token`, `deflationary token`, `rebasing token`, `transfer fee`, `token fee`, `balance difference`, `actual received`, `accounting error`, `over-accounting`, `token incompatibility`, `USDT fee`, `PAXG`, `SAFEMOON`, `elastic supply`, `aTokens`, `stETH`, `AMPL`, `balanceOf check`, `transferFrom accounting`, `deposit amount`, `withdraw amount`, `token whitelist`

---

## Related Vulnerabilities

- [Vault Inflation Attack](../vault-inflation-attack/vault-inflation-attack.md) - Can compound with FoT issues
- [Reentrancy](../reentrancy/) - Token transfers can trigger callbacks
- [Flash Loan Attacks](../economic/) - Token behavior during flash operations
