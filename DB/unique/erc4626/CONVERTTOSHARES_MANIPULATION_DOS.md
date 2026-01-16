---
# Core Classification
protocol: GSquared
chain: everychain
category: denial_of_service
vulnerability_type: deposit_blocking

# Attack Vector Details
attack_type: economic_griefing
affected_component: ERC4626_vault

# Technical Primitives
primitives:
  - convertToShares_manipulation
  - balanceOf_dependency
  - donation_attack
  - zero_share_minting
  - deposit_dos

# Impact Classification
severity: medium
impact: denial_of_service
exploitability: 0.7
financial_impact: medium

# Context Tags
tags:
  - erc4626
  - dos
  - griefing
  - deposit_blocking
  - share_manipulation
  - donation_attack

# Version Info
language: solidity
version: ">=0.8.0"
---

## Reference
- [Source Report]: reports/erc4626_findings/converttoshares-can-be-manipulated-to-block-deposits.md

## ConvertToShares Manipulation: Blocking Deposits via Direct Token Transfers

**Case Study: GSquared - Trail of Bits 2022**

### Overview

An economic denial-of-service attack where an attacker manipulates the `convertToShares()` calculation in ERC4626 vaults by directly transferring tokens to the vault contract. This exploits the fact that most ERC4626 implementations use `balanceOf(address(this))` in their asset calculations, which can be manipulated externally. The attack can either:
1. Block all deposits by making shares calculate to zero
2. Make deposits prohibitively expensive by inflating the share price

This is distinct from the classic inflation attack because:
- The goal is **denial of service**, not fund theft
- Can be executed **after** the vault has legitimate deposits
- Affects the `deposit()` function while `mint()` may still work

### Vulnerability Description

#### Root Cause

ERC4626 vaults typically calculate total assets using:

```solidity
function _totalAssets() internal view returns (uint256) {
    return asset.balanceOf(address(this)) + vaultTotalDebt;
}
```

Since `balanceOf` includes ANY tokens held by the contract—including those transferred directly without using `deposit()`—an attacker can manipulate the share price calculation by "donating" tokens to the vault.

The `convertToShares` function then produces unexpected results:

```solidity
function convertToShares(uint256 assets) public view returns (uint256 shares) {
    uint256 freeFunds_ = _freeFunds();
    // When freeFunds is artificially inflated, shares rounds to 0
    return freeFunds_ == 0 ? assets : (assets * totalSupply) / freeFunds_;
}
```

#### Why This Attack Works

**Scenario 1: Zero Shares (Small Donation)**

When `totalSupply > 0` but small:
- Alice deposits, gets 1 share for 1 wei
- Eve donates minimal tokens (e.g., 1000 wei)
- `freeFunds` = donated amount + original = 1001 wei
- Bob deposits 500 wei: `shares = (500 * 1) / 1001 = 0`
- Bob's deposit fails or he gets 0 shares

**Scenario 2: Expensive Deposits (Large Donation)**

- Eve donates massive tokens (e.g., 1M)
- `freeFunds` = donated amount = 1M
- New depositors must deposit >1M to get even 1 share
- Effectively prices out normal users

#### Attack Scenario

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCENARIO 1: BLOCKING DEPOSITS                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    
Time T0: Fresh Vault Deployment
┌─────────────────────────────────────────────────────────────────────────────┐
│  Vault State:                                                               │
│  - totalSupply: 0                                                           │
│  - balanceOf(vault): 0                                                      │
│  - freeFunds: 0                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Time T1: Eve Front-runs First Deposit
┌─────────────────────────────────────────────────────────────────────────────┐
│  Eve's Action:                                                              │
│  1. Calls deposit(1 wei) → receives 1 share                                │
│  2. Directly transfers 1,000,000 tokens to vault                           │
│                                                                             │
│  Vault State After:                                                         │
│  - totalSupply: 1                                                           │
│  - balanceOf(vault): 1,000,001                                             │
│  - freeFunds: 1,000,001                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Time T2: Alice Tries to Deposit
┌─────────────────────────────────────────────────────────────────────────────┐
│  Alice's Action:                                                            │
│  - Calls deposit(10,000 tokens)                                            │
│                                                                             │
│  Share Calculation:                                                         │
│  shares = (10,000 * 1) / 1,000,001 = 0 (rounds down!)                      │
│                                                                             │
│  Result: Alice gets ZERO shares despite depositing 10,000 tokens           │
│  Attack Cost to Eve: ~1M tokens (may recover later)                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCENARIO 2: GRIEFING EXISTING VAULT                     │
└─────────────────────────────────────────────────────────────────────────────┘

Established Vault with Normal Activity:
┌─────────────────────────────────────────────────────────────────────────────┐
│  Vault State:                                                               │
│  - totalSupply: 1000 shares                                                 │
│  - balanceOf(vault): 1000 tokens                                           │
│  - Share Price: 1:1                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Eve Donates Large Amount:
┌─────────────────────────────────────────────────────────────────────────────┐
│  Eve's Action:                                                              │
│  - Directly transfers 1,000,000 tokens to vault                            │
│                                                                             │
│  Vault State After:                                                         │
│  - totalSupply: 1000 shares (unchanged)                                    │
│  - balanceOf(vault): 1,001,000 tokens                                      │
│  - Share Price: 1001 tokens per share                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
New Depositors Blocked:
┌─────────────────────────────────────────────────────────────────────────────┐
│  Bob's Attempted Action:                                                    │
│  - Calls deposit(100 tokens)                                               │
│                                                                             │
│  Share Calculation:                                                         │
│  shares = (100 * 1000) / 1,001,000 = 0.0999... → rounds to 0              │
│                                                                             │
│  Result: Bob must deposit >1001 tokens to receive even 1 share             │
│  Existing holders: Their shares now worth more (windfall)                  │
│  Eve: Can withdraw her "donation" if she holds shares                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vulnerable Pattern Examples

**Example 1: Direct balanceOf Usage in Total Assets** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: balanceOf can be manipulated by direct transfers
function _totalAssets() private view returns (uint256) {
    // Anyone can increase this by transferring tokens directly
    return asset.balanceOf(address(this)) + vaultTotalDebt;
}

function _freeFunds() internal view returns (uint256) {
    return _totalAssets() - _calculateLockedProfit();
}

function convertToShares(uint256 _assets) public view override returns (uint256 shares) {
    uint256 freeFunds_ = _freeFunds();
    // Manipulated freeFunds causes incorrect share calculations
    return freeFunds_ == 0 ? _assets : (_assets * totalSupply) / freeFunds_;
}
```

**Example 2: Deposit Without Share Minimum Check** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: No check for zero shares minted
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = convertToShares(assets);
    // Should revert if shares == 0 but doesn't
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);  // Mints 0 shares!
    
    emit Deposit(msg.sender, receiver, assets, shares);
    return shares;
}
```

**Example 3: Exchange Rate Dependent on External State** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: _exchangeRate based on manipulable balance
function _exchangeRate() internal view returns (uint256) {
    uint256 totalHEU = heu.balanceOf(address(this));  // Manipulable!
    uint256 totalSupply_ = totalSupply();
    
    if (totalSupply_ == 0) return 1e18;
    return (totalHEU * 1e18) / totalSupply_;  // Can be inflated by donations
}
```

### Impact Analysis

#### Technical Impact
- **Zero Share Minting**: Deposits return 0 shares, users lose funds
- **Price Manipulation**: Share price can be arbitrarily inflated
- **Function Divergence**: `deposit()` broken while `mint()` may still work

#### Business Impact
- **Protocol Unusability**: New users cannot deposit
- **Reputation Damage**: Users losing funds to zero-share minting
- **Economic Warfare**: Competitors could attack to disrupt protocol

#### Affected Scenarios
- Newly deployed vaults (most vulnerable)
- Vaults during low-activity periods
- Permissionless vault creation systems
- Yield aggregators and auto-compounders

### Secure Implementation

**Fix 1: Track Internal Balance State**
```solidity
// ✅ SECURE: Use tracked balance instead of balanceOf
contract SecureVault is ERC4626 {
    uint256 private _trackedAssets;
    
    function _totalAssets() internal view override returns (uint256) {
        // Cannot be manipulated by external transfers
        return _trackedAssets + vaultTotalDebt;
    }
    
    function deposit(uint256 assets, address receiver) public override returns (uint256 shares) {
        shares = convertToShares(assets);
        require(shares > 0, "Zero shares");
        
        asset.safeTransferFrom(msg.sender, address(this), assets);
        _trackedAssets += assets;  // Update tracked balance
        _mint(receiver, shares);
        
        return shares;
    }
    
    function withdraw(uint256 assets, address receiver, address owner) 
        public override returns (uint256 shares) 
    {
        // ... withdrawal logic
        _trackedAssets -= assets;  // Update tracked balance
        // ...
    }
}
```

**Fix 2: Minimum Share Requirement**
```solidity
// ✅ SECURE: Require non-zero shares
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = convertToShares(assets);
    require(shares > 0, "Deposit would mint zero shares");
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
    
    return shares;
}
```

**Fix 3: Virtual Shares and Offset (OpenZeppelin Pattern)**
```solidity
// ✅ SECURE: Virtual shares make donation attacks unprofitable
function _convertToShares(uint256 assets, Math.Rounding rounding) 
    internal view virtual returns (uint256) 
{
    return assets.mulDiv(
        totalSupply() + 10 ** _decimalsOffset(),  // Virtual shares
        totalAssets() + 1,                         // Virtual assets
        rounding
    );
}

function _decimalsOffset() internal view virtual returns (uint8) {
    return 3;  // Adds 1000 virtual shares
}
```

**Fix 4: Dead Shares on Initialization**
```solidity
// ✅ SECURE: Permanent dead shares prevent empty vault manipulation
constructor(IERC20 asset_) ERC4626(asset_) {
    // Mint dead shares to prevent first depositor attacks
    uint256 deadShares = 1000;
    _mint(address(0xdead), deadShares);
    
    // Transfer corresponding assets
    asset_.safeTransferFrom(msg.sender, address(this), deadShares);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- _totalAssets() using asset.balanceOf(address(this))
- convertToShares without minimum check
- No dead shares or virtual offset in share calculations
- Missing require(shares > 0) in deposit()
- Exchange rate calculations using direct balance reads
```

#### Static Analysis Rules
```yaml
# Semgrep rule for vulnerable pattern
rules:
  - id: erc4626-balanceof-manipulation
    pattern: |
      function $FUNC() ... {
        ...
        $TOKEN.balanceOf(address(this))
        ...
      }
    message: "ERC4626 using balanceOf may be vulnerable to donation attacks"
    severity: WARNING
    
  - id: erc4626-zero-shares
    pattern: |
      function deposit($ASSETS, $RECEIVER) ... {
        $SHARES = convertToShares($ASSETS);
        ...
        _mint($RECEIVER, $SHARES);
        ...
      }
    pattern-not: |
      function deposit($ASSETS, $RECEIVER) ... {
        ...
        require($SHARES > 0, ...);
        ...
      }
    message: "Deposit may mint zero shares"
    severity: WARNING
```

#### Audit Checklist
- [ ] Does `_totalAssets()` use `balanceOf(address(this))`?
- [ ] Can users receive 0 shares from `deposit()`?
- [ ] Is there a virtual offset or dead shares mechanism?
- [ ] Does `mint()` work when `deposit()` would return 0?
- [ ] Are there minimum deposit requirements?

### Real-World Context

#### Discovery
- **Protocol**: GSquared (GVault)
- **Audit Firm**: Trail of Bits
- **Date**: 2022
- **Finders**: Damilola Edwards, Gustavo Grieco, Anish Naik, Michael Colburn

#### Key Insight from Report
> "It is important to note that although Alice cannot use the `deposit` function, she can still call `mint` to bypass the exploit."

This highlights that `deposit()` and `mint()` can have different vulnerability profiles due to their inverse calculations.

### Comparison: deposit() vs mint()

| Function | Calculation | Manipulation Effect |
|----------|-------------|---------------------|
| `deposit(assets)` | `shares = assets * supply / totalAssets` | Donations ↑ totalAssets → ↓ shares (to 0) |
| `mint(shares)` | `assets = shares * totalAssets / supply` | Donations ↑ totalAssets → ↑ required assets |

**Important**: `mint()` may still work when `deposit()` is broken because it calculates the required assets rather than the resulting shares.

### Prevention Guidelines

#### Development Best Practices
1. Use internal balance tracking instead of `balanceOf()`
2. Implement virtual shares/offset per OpenZeppelin
3. Always check `shares > 0` before minting
4. Consider dead shares on vault initialization
5. Implement minimum deposit requirements

#### Testing Requirements
- Unit tests for donation attacks
- Fuzz testing with random direct transfers
- Edge case tests for zero-share scenarios
- Comparison tests between `deposit()` and `mint()`

### References

#### Technical Documentation
- [OpenZeppelin ERC4626 Security](https://docs.openzeppelin.com/contracts/4.x/erc4626)
- [EIP-4626: Tokenized Vault Standard](https://eips.ethereum.org/EIPS/eip-4626)

#### Security Research
- [Trail of Bits GSquared Audit](https://github.com/trailofbits/publications/blob/master/reviews/2022-10-GSquared-securityreview.pdf)
- [OpenZeppelin Virtual Offset Discussion](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3800)

### Keywords for Search

`convertToShares manipulation`, `ERC4626 donation attack`, `deposit blocking`, `zero shares minting`, `balanceOf manipulation`, `share price inflation`, `vault DoS attack`, `freeFunds manipulation`, `totalAssets manipulation`, `direct transfer attack`, `deposit griefing`, `ERC4626 DoS`, `share calculation manipulation`, `vault deposit blocking`, `exchange rate manipulation`, `virtual shares`, `dead shares`, `first depositor DoS`, `mint vs deposit vulnerability`, `economic griefing attack`

### Related Vulnerabilities

- [ERC4626 First Depositor Attack](../ERC4626_VAULT_VULNERABILITIES.md#first-depositor-attack)
- [Exchange Rate Manipulation via Direct Transfers](../ERC4626_VAULT_VULNERABILITIES.md#exchange-rate-manipulation)
- [Flash Loan Vault Deflation](./FLASH_LOAN_VAULT_DEFLATION_ATTACK.md)
