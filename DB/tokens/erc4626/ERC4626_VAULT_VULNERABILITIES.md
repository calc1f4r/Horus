# ERC4626 Tokenized Vault Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for ERC4626 Vault Security Audits**

---

## Frontmatter

```yaml
# Core Classification (Required)
protocol: generic
chain: everychain
category: vault
vulnerability_type: erc4626_vault_integration

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error|data_manipulation
affected_component: share_calculation|deposit_logic|withdrawal_logic|fee_handling|access_control

# Vault-Specific Fields
vault_standard: erc4626
vault_attack_vector: inflation|first_depositor|rounding|slippage|reentrancy|fee_manipulation|compliance

# Technical Primitives (Required)
primitives:
  - convertToShares
  - convertToAssets
  - previewDeposit
  - previewMint
  - previewWithdraw
  - previewRedeem
  - maxDeposit
  - maxMint
  - maxWithdraw
  - maxRedeem
  - totalAssets
  - deposit
  - mint
  - withdraw
  - redeem
  - share_price
  - exchange_rate
  - virtual_shares
  - decimal_offset

# Impact Classification (Required)
severity: critical|high|medium|low
impact: fund_loss|share_manipulation|dos|incorrect_accounting|integration_failure
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - defi
  - vault
  - yield
  - lending
  - tokenized_shares
  - erc4626
  - first_depositor_attack
  - inflation_attack

# Version Info
language: solidity
version: all
```

---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### First Depositor / Inflation Attack Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Florence Finance - First Depositor Attack | `reports/erc4626_findings/h-01-stakersvault-depositors-can-be-front-run-and-lose-their-funds.md` | HIGH | Pashov Audit Group |
| prePO - Share Minting Manipulation | `reports/erc4626_findings/h-02-first-depositor-can-break-minting-of-shares.md` | HIGH | Code4rena |
| Liquorice - Inflation Attack | `reports/erc4626_findings/inflation-attack.md` | HIGH | MixBytes |
| Treehouse - Share Inflation | `reports/erc4626_findings/erc4626-vault-share-inflation.md` | MEDIUM | SigmaPrime |
| Steadefi - Vault Inflation | `reports/erc4626_findings/vault-is-vulnerable-to-inflation-attack.md` | HIGH | Zokyo |
| BakerFi - First Depositor Attack | `reports/erc4626_findings/h-02-vault-is-vulnerable-to-first-depositor-inflation-attack.md` | HIGH | Code4rena |
| Peapods - Incorrect Dead Shares | `reports/erc4626_findings/h-2-vault-inflation-attack-in-autocompoundingpodlp-is-possible-due-to-incorrectl.md` | HIGH | Sherlock |

### ERC4626 Compliance Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Y2K Finance - Not EIP-4626 Compliant | `reports/erc4626_findings/h-08-vaultsol-is-not-eip-4626-compliant.md` | HIGH | Code4rena |
| BakerFi - VaultBase Not Compliant | `reports/erc4626_findings/m-01-vaultbase-is-not-erc4626-compliant.md` | MEDIUM | Code4rena |
| Ethos Reserve - Not EIP-4626 Compliant | `reports/erc4626_findings/m-12-reapervaulterc4626-is-not-eip-4626-compliant-and-integrations-can-result-in.md` | MEDIUM | Code4rena |
| Astaria - Deposit/Mint Logic Differ | `reports/erc4626_findings/h-02-erc4626cloned-deposit-and-mint-logic-differ-on-first-deposit.md` | HIGH | Code4rena |

### Rounding Direction Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Notional - Rounding Issues | `reports/erc4626_findings/h-01-rounding-issues-in-certain-functions.md` | HIGH | Code4rena |
| Tribe - ERC4626 Mint Wrong Amount | `reports/erc4626_findings/h-01-erc4626-mint-uses-wrong-amount.md` | HIGH | Code4rena |

### Fee Handling Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Burve - Incorrect Fee Handling | `reports/erc4626_findings/h-1-incorrect-handling-of-erc4626-vaults-with-fees.md` | HIGH | Sherlock |
| Astrolab - Fee Calculation Mismatch | `reports/erc4626_findings/h-05-fee-calculation-mismatch-in-mint-deposit-redeem-and-withdraw.md` | HIGH | Pashov Audit Group |
| Fee-on-Transfer Tokens | `reports/erc4626_findings/fee-on-transfer-tokens.md` | MEDIUM | Spearbit |

### Slippage Protection Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| NashPoint - Missing Slippage Control | `reports/erc4626_findings/missing-slippage-control-for-erc4626-deposits-and-withdrawals-in-the-underlying-.md` | MEDIUM | Cantina |
| Multipli Vault - No Slippage Protection | `reports/erc4626_findings/m-03-lack-of-slippage-protection-in-deposit-and-mint-functions.md` | MEDIUM | Shieldify |

### Exchange Rate Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Heurist - Direct Transfer Manipulation | `reports/erc4626_findings/exchange-rate-manipulation-via-direct-transfers.md` | MEDIUM | Zokyo |
| GSquared - convertToShares Manipulation | `reports/erc4626_findings/converttoshares-can-be-manipulated-to-block-deposits.md` | MEDIUM | Trail of Bits |

### Decimal Handling Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Sublime - Yearn Token Decimal Issue | `reports/erc4626_findings/h-04-yearn-token-shares-conversion-decimal-issue.md` | HIGH | Code4rena |

### Reentrancy Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| JPEG'd - Reentrancy in Deposit | `reports/erc4626_findings/h-04-reentrancy-issue-in-yvaultdeposit.md` | HIGH | Code4rena |
| Notional Exponent - Cross-Contract Reentrancy | `reports/erc4626_findings/h-1-cross-contract-reentrancy-allows-yield_token-theft-for-the-genericerc4626-wi.md` | HIGH | Sherlock |

### External Links
- [EIP-4626 Specification](https://eips.ethereum.org/EIPS/eip-4626)
- [OpenZeppelin ERC4626 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol)
- [Solodit Vulnerability Database](https://solodit.cyfrin.io/)

---

## Table of Contents

1. [First Depositor / Inflation Attack Vulnerabilities](#1-first-depositor--inflation-attack-vulnerabilities)
2. [ERC4626 Compliance Issues](#2-erc4626-compliance-issues)
3. [Rounding Direction Vulnerabilities](#3-rounding-direction-vulnerabilities)
4. [Fee Handling Vulnerabilities](#4-fee-handling-vulnerabilities)
5. [Slippage Protection Issues](#5-slippage-protection-issues)
6. [Exchange Rate Manipulation](#6-exchange-rate-manipulation)
7. [Decimal Handling Issues](#7-decimal-handling-issues)
8. [Reentrancy Vulnerabilities](#8-reentrancy-vulnerabilities)
9. [Token Compatibility Issues](#9-token-compatibility-issues)
10. [Access Control & State Management](#10-access-control--state-management)

---

## 1. First Depositor / Inflation Attack Vulnerabilities

### Overview

The first depositor (inflation) attack is the most common and critical vulnerability affecting ERC4626 vaults. It exploits the share/asset conversion mechanism when the vault's total supply is zero or very low. An attacker can manipulate the share price to steal deposits from subsequent users.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/h-01-stakersvault-depositors-can-be-front-run-and-lose-their-funds.md` (Florence Finance - Pashov)
> - `reports/erc4626_findings/h-02-first-depositor-can-break-minting-of-shares.md` (prePO - Code4rena)
> - `reports/erc4626_findings/vault-is-vulnerable-to-inflation-attack.md` (Steadefi - Zokyo)
> - `reports/erc4626_findings/h-02-vault-is-vulnerable-to-first-depositor-inflation-attack.md` (BakerFi - Code4rena)

### Vulnerability Description

#### Root Cause

The ERC4626 share calculation formula is:
```
shares = (assets * totalSupply) / totalAssets
```

When `totalSupply` is 0, shares are typically minted 1:1 with assets. An attacker can:
1. Deposit a tiny amount (e.g., 1 wei) to mint 1 share
2. Donate a large amount directly to the vault (not through deposit)
3. The share price becomes extremely inflated
4. Subsequent depositors receive 0 shares due to rounding down

#### Attack Scenario

1. Vault is deployed with `totalAssets() = 0` and `totalSupply() = 0`
2. Attacker deposits 1 wei, receiving 1 share (owns 100% of vault)
3. Attacker directly transfers 20,000e18 tokens to the vault
4. Victim attempts to deposit 2,000e18 tokens
5. Shares calculation: `2_000e18 * 1 / ((20_000e18 + 1) - 2_000e18) = 0`
6. Victim receives 0 shares, attacker withdraws all funds

### Vulnerable Pattern Examples

**Example 1: Basic Unprotected Share Calculation** [CRITICAL]
> 📖 Reference: `reports/erc4626_findings/h-01-stakersvault-depositors-can-be-front-run-and-lose-their-funds.md`
```solidity
// ❌ VULNERABLE: No protection against first depositor attack
function _mintShares(uint256 assetAmt) internal returns (uint256) {
    uint256 _shares;

    if (totalSupply() == 0) {
        _shares = assetAmt * _to18ConversionFactor();
    } else {
        _shares = assetAmt * totalSupply() / (totalAsset() - assetAmt);
    }

    _mint(msg.sender, _shares);
    return _shares;
}
```

**Example 2: Balance-Based totalAssets Vulnerable to Donation** [CRITICAL]
> 📖 Reference: `reports/erc4626_findings/inflation-attack.md`
```solidity
// ❌ VULNERABLE: totalAssets relies on balanceOf which can be manipulated
function totalAssets() public view returns (uint256) {
    return asset.balanceOf(address(this));
}

function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    // First depositor gets 1:1, but donation inflates totalAssets
    return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
}
```

**Example 3: Missing Zero Share Check** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-02-first-depositor-can-break-minting-of-shares.md`
```solidity
// ❌ VULNERABLE: Does not check if shares minted are zero
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = previewDeposit(assets);
    // Missing: require(shares > 0, "Zero shares");
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
    
    return shares;
}
```

**Example 4: Incorrect Dead Shares Minting** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-2-vault-inflation-attack-in-autocompoundingpodlp-is-possible-due-to-incorrectl.md`
```solidity
// ❌ VULNERABLE: Dead shares minted to msg.sender instead of dead address
function _depositMin(address _aspAddy, IDecentralizedIndex _pod) internal {
    // ...
    // These shares can be withdrawn, defeating the purpose!
    AutoCompoundingPodLp(_aspAddy).deposit(minimumDepositAtCreation, _msgSender());
}
```

### Impact Analysis

#### Technical Impact
- Complete loss of depositor funds (0 shares minted)
- Permanent manipulation of share/asset ratio
- Vault becomes unusable for legitimate users

#### Business Impact
- Direct theft of user deposits (100% loss possible)
- Protocol reputation damage
- Potential protocol insolvency

#### Affected Scenarios
- New vault deployments
- Vaults with low TVL
- Vaults where total assets can be manipulated via donations
- Any vault using `balanceOf(address(this))` for totalAssets

### Secure Implementation

**Fix 1: Virtual Shares/Assets (OpenZeppelin 4.8+)** [RECOMMENDED]
```solidity
// ✅ SECURE: Use virtual shares to prevent inflation attack
abstract contract ERC4626 is ERC20, IERC4626 {
    uint8 private immutable _underlyingDecimals;

    constructor(IERC20 asset_) {
        (bool success, uint8 assetDecimals) = _tryGetAssetDecimals(asset_);
        _underlyingDecimals = success ? assetDecimals : 18;
        _asset = asset_;
    }

    function _decimalsOffset() internal view virtual returns (uint8) {
        return 0; // Override to add offset for protection
    }

    function _convertToShares(uint256 assets, Math.Rounding rounding) internal view returns (uint256) {
        return assets.mulDiv(
            totalSupply() + 10 ** _decimalsOffset(),  // Virtual shares
            totalAssets() + 1,                         // Virtual assets
            rounding
        );
    }

    function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view returns (uint256) {
        return shares.mulDiv(
            totalAssets() + 1,                         // Virtual assets
            totalSupply() + 10 ** _decimalsOffset(),  // Virtual shares
            rounding
        );
    }
}
```

**Fix 2: Dead Shares to Zero Address (UniswapV2 Style)**
```solidity
// ✅ SECURE: Mint initial shares to dead address
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = previewDeposit(assets);
    
    if (totalSupply() == 0) {
        uint256 deadShares = 1000; // MINIMUM_LIQUIDITY
        _mint(address(0), deadShares);
        shares -= deadShares;
    }
    
    require(shares > 0, "Zero shares minted");
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
    
    return shares;
}
```

**Fix 3: Minimum Deposit Requirement**
```solidity
// ✅ SECURE: Enforce minimum initial deposit
uint256 public constant MINIMUM_INITIAL_DEPOSIT = 1e18; // 1 token

function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    if (totalSupply() == 0) {
        require(assets >= MINIMUM_INITIAL_DEPOSIT, "Below minimum initial deposit");
    }
    
    shares = previewDeposit(assets);
    require(shares > 0, "Zero shares");
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
}
```

**Fix 4: Internal Accounting (Prevent Donation Attack)**
```solidity
// ✅ SECURE: Track assets internally, not via balanceOf
uint256 private _totalManagedAssets;

function totalAssets() public view returns (uint256) {
    return _totalManagedAssets; // Not balanceOf!
}

function _deposit(address caller, address receiver, uint256 assets, uint256 shares) internal {
    asset.safeTransferFrom(caller, address(this), assets);
    _totalManagedAssets += assets; // Update internal tracking
    _mint(receiver, shares);
}

function _withdraw(address caller, address receiver, address owner, uint256 assets, uint256 shares) internal {
    _burn(owner, shares);
    _totalManagedAssets -= assets; // Update internal tracking
    asset.safeTransfer(receiver, assets);
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- totalAssets() using balanceOf(address(this))
- Missing virtual shares/decimal offset
- No minimum deposit enforcement
- Zero share check missing
- First deposit minting to user instead of dead address
- convertToShares without protection when supply == 0
```

#### Audit Checklist
- [ ] Check if vault uses virtual shares (decimal offset)
- [ ] Verify totalAssets() doesn't rely solely on balanceOf
- [ ] Ensure zero shares cannot be minted
- [ ] Check for minimum initial deposit requirements
- [ ] Verify dead shares are sent to address(0), not user
- [ ] Test share calculation with extreme values (1 wei deposit, large donations)

### Real-World Examples

#### Known Exploits & Findings
- **Florence Finance** - First depositor can front-run and steal funds via share manipulation
- **prePO** - Attacker can donate to inflate share price and steal subsequent deposits
- **Steadefi** - Vault vulnerable to classic inflation attack with 0 share minting
- **Peapods Finance** - Dead shares minted to sender instead of dead address, enabling attack
- **BakerFi** - First depositor can manipulate share price via leverage deposit manipulation

---

## 2. ERC4626 Compliance Issues

### Overview

ERC4626 defines strict requirements for vault implementations. Non-compliance can break integrations with other protocols that expect standard behavior, leading to fund loss, incorrect calculations, or denial of service.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/h-08-vaultsol-is-not-eip-4626-compliant.md` (Y2K Finance - Code4rena)
> - `reports/erc4626_findings/m-01-vaultbase-is-not-erc4626-compliant.md` (BakerFi - Code4rena)
> - `reports/erc4626_findings/h-02-erc4626cloned-deposit-and-mint-logic-differ-on-first-deposit.md` (Astaria - Code4rena)

### Vulnerability Description

#### Root Cause

ERC4626 specifies exact behavior for all functions including:
- `maxDeposit/maxMint/maxWithdraw/maxRedeem` must return 0 when operations are disabled
- `previewDeposit/previewMint/previewWithdraw/previewRedeem` must match actual execution
- `deposit` and `mint` must have equivalent logic for first deposit
- Functions must account for fees in preview calculations

#### Key ERC4626 Requirements

1. **max* Functions**: Must return 0 when operations are disabled (paused, capped, etc.)
2. **preview* Functions**: Must reflect actual execution including fees and limits
3. **Rounding**: Favor the vault (round down for deposits/mints, round up for withdrawals/redeems)
4. **Consistency**: deposit/mint and withdraw/redeem pairs must be inverse operations

### Vulnerable Pattern Examples

**Example 1: maxDeposit Always Returns max uint256** [MEDIUM]
> 📖 Reference: `reports/erc4626_findings/m-01-vaultbase-is-not-erc4626-compliant.md`
```solidity
// ❌ VULNERABLE: Returns max even when deposits are limited
function maxDeposit(address) external pure override returns (uint256 maxAssets) {
    return type(uint256).max; // Should check getMaxDeposit() and pause state
}

function _depositInternal(uint256 assets, address receiver) private returns (uint256 shares) {
    // Actual deposit has limits!
    uint256 maxDepositLocal = getMaxDeposit();
    if (maxDepositLocal > 0) {
        uint256 depositInAssets = (balanceOf(msg.sender) * _ONE) / tokenPerAsset();
        uint256 newBalance = assets + depositInAssets;
        if (newBalance > maxDepositLocal) revert MaxDepositReached();
    }
    // ...
}
```

**Example 2: Missing Required Functions** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-08-vaultsol-is-not-eip-4626-compliant.md`
```solidity
// ❌ VULNERABLE: Missing mint and redeem functions
contract Vault is ERC4626 {
    // Only implements deposit and withdraw
    // Missing: mint(uint256, address) returns (uint256)
    // Missing: redeem(uint256, address, address) returns (uint256)
}
```

**Example 3: deposit vs mint Logic Differs on First Deposit** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-02-erc4626cloned-deposit-and-mint-logic-differ-on-first-deposit.md`
```solidity
// ❌ VULNERABLE: Different logic for deposit vs mint on first deposit
function previewDeposit(uint256 assets) public view returns (uint256) {
    return convertToShares(assets); // Standard conversion
}

function previewMint(uint256 shares) public view returns (uint256) {
    uint256 supply = totalSupply();
    // Different handling! Returns fixed amount on first mint
    return supply == 0 ? 10e18 : shares.mulDivUp(totalAssets(), supply);
}

// An attacker can use deposit() to mint arbitrary shares when supply == 0
// while mint() would require fixed 10e18 assets
```

**Example 4: previewDeposit Doesn't Account for Fees** [MEDIUM]
> 📖 Reference: EIP-4626 Specification
```solidity
// ❌ VULNERABLE: Preview doesn't include fees
function previewDeposit(uint256 assets) public view returns (uint256) {
    return convertToShares(assets); // Ignores deposit fee!
}

function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    uint256 fee = assets * depositFeeBps / 10000;
    uint256 netAssets = assets - fee;
    shares = convertToShares(netAssets); // Actual deposit uses fee
    // ...
}
```

### Impact Analysis

#### Technical Impact
- Integration failures with external protocols
- Incorrect share/asset calculations in aggregators
- User interfaces showing wrong values
- Failed transactions when using standard routers

#### Business Impact
- Loss of funds when integrating with other DeFi protocols
- Protocol incompatibility with yield aggregators
- Reduced composability in the DeFi ecosystem

### Secure Implementation

**Fix 1: Proper maxDeposit Implementation**
```solidity
// ✅ SECURE: Returns actual limits
function maxDeposit(address receiver) public view returns (uint256) {
    if (paused()) return 0;
    
    uint256 maxDepositLimit = getMaxDeposit();
    if (maxDepositLimit == 0) return type(uint256).max;
    
    uint256 currentDeposits = (balanceOf(receiver) * _ONE) / tokenPerAsset();
    if (currentDeposits >= maxDepositLimit) return 0;
    
    return maxDepositLimit - currentDeposits;
}
```

**Fix 2: Consistent deposit/mint Logic**
```solidity
// ✅ SECURE: Same logic for first deposit in both functions
uint256 public constant MINIMUM_INITIAL_ASSETS = 1e18;

function previewDeposit(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    if (supply == 0) {
        require(assets >= MINIMUM_INITIAL_ASSETS, "Below minimum");
        return assets; // 1:1 for first deposit
    }
    return assets.mulDivDown(supply, totalAssets());
}

function previewMint(uint256 shares) public view returns (uint256) {
    uint256 supply = totalSupply();
    if (supply == 0) {
        return shares; // 1:1 for first mint, same as deposit
    }
    return shares.mulDivUp(totalAssets(), supply);
}
```

**Fix 3: Preview Functions Including Fees**
```solidity
// ✅ SECURE: Preview matches actual execution with fees
function previewDeposit(uint256 assets) public view returns (uint256) {
    uint256 fee = _feeOnTotal(assets, depositFeeBps);
    uint256 netAssets = assets - fee;
    return convertToShares(netAssets);
}

function previewMint(uint256 shares) public view returns (uint256) {
    uint256 assets = convertToAssets(shares);
    uint256 fee = _feeOnRaw(assets, depositFeeBps);
    return assets + fee;
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Verify all 8 core functions are implemented (deposit, mint, withdraw, redeem + previews)
- [ ] Check max* functions return 0 when operations disabled
- [ ] Ensure preview* functions match actual execution including fees
- [ ] Verify deposit/mint have equivalent first-deposit logic
- [ ] Check withdraw/redeem handle owner != msg.sender correctly
- [ ] Test that totalAssets() includes all managed assets

---

## 3. Rounding Direction Vulnerabilities

### Overview

ERC4626 specifies strict rounding requirements to favor the vault over users. Incorrect rounding can be exploited to drain the vault through repeated small transactions.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/h-01-rounding-issues-in-certain-functions.md` (Notional - Code4rena)
> - `reports/erc4626_findings/h-01-erc4626-mint-uses-wrong-amount.md` (Tribe - Code4rena)

### Vulnerability Description

#### Root Cause

ERC4626 rounding rules:
- **Round DOWN** (favor vault): `convertToShares`, `previewDeposit`, `previewRedeem`
- **Round UP** (favor vault): `convertToAssets`, `previewMint`, `previewWithdraw`

When rounding favors the user instead of the vault, attackers can profit through rounding errors.

### Vulnerable Pattern Examples

**Example 1: previewWithdraw Rounds Down Instead of Up** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-01-rounding-issues-in-certain-functions.md`
```solidity
// ❌ VULNERABLE: Should round up, but rounds down
function previewWithdraw(uint256 assets) public view returns (uint256 shares) {
    if (hasMatured()) {
        shares = convertToShares(assets); // convertToShares rounds down!
        // Should use: shares.mulDivUp(totalSupply(), totalAssets())
    }
}
```

**Example 2: Mint Uses Wrong Amount** [CRITICAL]
> 📖 Reference: `reports/erc4626_findings/h-01-erc4626-mint-uses-wrong-amount.md`
```solidity
// ❌ VULNERABLE: Mints 'amount' instead of 'shares'
function mint(uint256 shares, address to) public returns (uint256 amount) {
    amount = previewMint(shares);
    
    asset.safeTransferFrom(msg.sender, address(this), amount);
    _mint(to, amount); // WRONG! Should be: _mint(to, shares);
    
    emit Deposit(msg.sender, to, amount, shares);
}
// When assets > shares (normal vault state), users receive more shares than they should
```

### Impact Analysis

#### Technical Impact
- Users can extract more assets than deposited
- Vault becomes undercollateralized over time
- Small but cumulative losses for the protocol

#### Exploitation Example
```
State: totalSupply = 1000, totalAssets = 1500 (shares worth 1.5 assets each)

Using vulnerable mint(1000):
- User pays: previewMint(1000) = 1000 assets
- User receives: 1000 shares (bug mints 'amount' not 'shares')
- New state: totalSupply = 2000, totalAssets = 2500

User redeems 1000 shares:
- User receives: (1000/2000) * 2500 = 1250 assets
- Profit: 250 assets

Repeat until vault drained.
```

### Secure Implementation

**Fix 1: Correct Rounding in All Functions**
```solidity
// ✅ SECURE: Proper rounding directions
function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    // Round DOWN - fewer shares for deposits
    return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
}

function convertToAssets(uint256 shares) public view returns (uint256) {
    uint256 supply = totalSupply();
    // Round DOWN - fewer assets for redemptions
    return supply == 0 ? shares : shares.mulDivDown(totalAssets(), supply);
}

function previewMint(uint256 shares) public view returns (uint256) {
    uint256 supply = totalSupply();
    // Round UP - more assets required to mint
    return supply == 0 ? shares : shares.mulDivUp(totalAssets(), supply);
}

function previewWithdraw(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    // Round UP - more shares required to withdraw
    return supply == 0 ? assets : assets.mulDivUp(supply, totalAssets());
}
```

**Fix 2: Correct Mint Implementation**
```solidity
// ✅ SECURE: Mint the correct number of shares
function mint(uint256 shares, address to) public returns (uint256 assets) {
    assets = previewMint(shares);
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(to, shares); // Correct: mint 'shares' not 'assets'
    
    emit Deposit(msg.sender, to, assets, shares);
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Verify convertToShares rounds DOWN
- [ ] Verify previewDeposit rounds DOWN
- [ ] Verify previewRedeem rounds DOWN
- [ ] Verify convertToAssets (for withdrawals) rounds DOWN
- [ ] Verify previewMint rounds UP
- [ ] Verify previewWithdraw rounds UP
- [ ] Check mint() mints 'shares' parameter, not calculated 'assets'

---

## 4. Fee Handling Vulnerabilities

### Overview

ERC4626 vaults with deposit/withdrawal fees must handle them consistently across all functions. Fee calculation mismatches between preview and actual execution, or between different entry/exit methods, can be exploited.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/h-1-incorrect-handling-of-erc4626-vaults-with-fees.md` (Burve - Sherlock)
> - `reports/erc4626_findings/h-05-fee-calculation-mismatch-in-mint-deposit-redeem-and-withdraw.md` (Astrolab - Pashov)

### Vulnerable Pattern Examples

**Example 1: Fee Calculation Mismatch Between Deposit and Mint** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-05-fee-calculation-mismatch-in-mint-deposit-redeem-and-withdraw.md`
```solidity
// ❌ VULNERABLE: Different fee calculations for deposit vs mint
// Fee = 10%

// mint(100 shares): User pays 110 assets, receives 100 shares, fee = 10 assets
function previewMint(uint256 shares) public view returns (uint256) {
    return convertToAssets(shares).addBp(feeRate); // 100 * 1.1 = 110
}

// deposit(110 assets): User pays 110 assets, receives 99 shares, fee = 11 assets!
function previewDeposit(uint256 assets) public view returns (uint256) {
    return convertToShares(assets).subBp(feeRate); // 110 * 0.9 = 99
}
// deposit() overcharges the user compared to mint() for equivalent operations
```

**Example 2: Not Transferring Enough to Cover Vault Fees** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-1-incorrect-handling-of-erc4626-vaults-with-fees.md`
```solidity
// ❌ VULNERABLE: Doesn't account for underlying vault's deposit fees
function addValue(address recipient, uint128 value) external returns (uint256[] memory) {
    // Calculate required tokens based on value
    uint256 realNeeded = AdjustorLib.toReal(token, requiredNominal, true);
    
    // Transfer exact amount
    TransferHelper.safeTransferFrom(token, msg.sender, address(this), realNeeded);
    
    // Deposit to ERC4626 vault with fees
    uint256 shares = IERC4626(vault).deposit(realNeeded, address(this));
    
    // If vault has 1% fee: deposited 100, but only 99 worth of shares minted
    // Internal accounting thinks we have 100 value, but actually have 99
}
```

### Secure Implementation

**Fix 1: Consistent Fee Calculation**
```solidity
// ✅ SECURE: Fee calculation is consistent
function _feeOnTotal(uint256 amount, uint256 feeBps) internal pure returns (uint256) {
    // Fee is calculated from total, so fee + net = total
    return amount * feeBps / (10000 + feeBps);
}

function previewDeposit(uint256 assets) public view returns (uint256) {
    uint256 fee = _feeOnTotal(assets, depositFeeBps);
    return convertToShares(assets - fee);
}

function previewMint(uint256 shares) public view returns (uint256) {
    uint256 assets = convertToAssets(shares);
    uint256 fee = _feeOnTotal(assets, depositFeeBps);
    return assets + fee;
}
// Now deposit(110) and mint(100) both result in 100 shares with 10 asset fee
```

**Fix 2: Account for Underlying Vault Fees**
```solidity
// ✅ SECURE: Check actual shares received and adjust accounting
function deposit(uint256 assets) external {
    uint256 sharesBefore = IERC4626(vault).balanceOf(address(this));
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    asset.approve(vault, assets);
    IERC4626(vault).deposit(assets, address(this));
    
    uint256 sharesReceived = IERC4626(vault).balanceOf(address(this)) - sharesBefore;
    uint256 actualValue = IERC4626(vault).convertToAssets(sharesReceived);
    
    // Use actualValue for accounting, not original assets
    _recordDeposit(msg.sender, actualValue);
}
```

---

## 5. Slippage Protection Issues

### Overview

ERC4626 deposit/mint and withdraw/redeem operations can be subject to sandwich attacks or unfavorable exchange rate changes. Direct EOA interactions particularly need slippage protection since users can't revert mid-transaction.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/missing-slippage-control-for-erc4626-deposits-and-withdrawals-in-the-underlying-.md` (NashPoint - Cantina)
> - `reports/erc4626_findings/m-03-lack-of-slippage-protection-in-deposit-and-mint-functions.md` (Multipli Vault - Shieldify)

### Vulnerable Pattern Examples

**Example 1: No Minimum Shares on Deposit** [MEDIUM]
> 📖 Reference: `reports/erc4626_findings/m-03-lack-of-slippage-protection-in-deposit-and-mint-functions.md`
```solidity
// ❌ VULNERABLE: User has no control over minimum shares received
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = previewDeposit(assets);
    // No minimum shares check!
    // If exchange rate changes between tx submission and execution,
    // user might receive far fewer shares than expected
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
}
```

**Example 2: No Maximum Assets on Mint** [MEDIUM]
```solidity
// ❌ VULNERABLE: User can't limit assets spent
function mint(uint256 shares, address receiver) public returns (uint256 assets) {
    assets = previewMint(shares);
    // No maximum assets check!
    // If exchange rate moves against user, they pay more than expected
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
}
```

### Secure Implementation

**Fix 1: Overloaded Functions with Slippage Parameters**
```solidity
// ✅ SECURE: Add slippage protection to deposit/mint
function deposit(
    uint256 assets, 
    address receiver,
    uint256 minShares
) public returns (uint256 shares) {
    shares = previewDeposit(assets);
    require(shares >= minShares, "Slippage: shares below minimum");
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
}

function mint(
    uint256 shares, 
    address receiver,
    uint256 maxAssets
) public returns (uint256 assets) {
    assets = previewMint(shares);
    require(assets <= maxAssets, "Slippage: assets above maximum");
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
}

// Similar for withdraw and redeem
function withdraw(
    uint256 assets,
    address receiver,
    address owner,
    uint256 maxShares
) public returns (uint256 shares) {
    shares = previewWithdraw(assets);
    require(shares <= maxShares, "Slippage: shares above maximum");
    
    _burn(owner, shares);
    asset.safeTransfer(receiver, assets);
}
```

**Fix 2: Deadline Parameter**
```solidity
// ✅ SECURE: Add deadline to prevent stale transactions
function deposit(
    uint256 assets, 
    address receiver,
    uint256 minShares,
    uint256 deadline
) public returns (uint256 shares) {
    require(block.timestamp <= deadline, "Transaction expired");
    
    shares = previewDeposit(assets);
    require(shares >= minShares, "Slippage too high");
    
    asset.safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
}
```

---

## 6. Exchange Rate Manipulation

### Overview

Vaults that rely on `balanceOf(address(this))` for total assets calculation are vulnerable to exchange rate manipulation through direct token transfers (donations). This can be used for DoS attacks or to extract value.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/exchange-rate-manipulation-via-direct-transfers.md` (Heurist - Zokyo)
> - `reports/erc4626_findings/converttoshares-can-be-manipulated-to-block-deposits.md` (GSquared - Trail of Bits)

### Vulnerable Pattern Examples

**Example 1: totalAssets Based on balanceOf** [MEDIUM]
> 📖 Reference: `reports/erc4626_findings/converttoshares-can-be-manipulated-to-block-deposits.md`
```solidity
// ❌ VULNERABLE: Donation can inflate totalAssets
function totalAssets() public view returns (uint256) {
    return asset.balanceOf(address(this)) + vaultTotalDebt;
}

function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    uint256 freeFunds = totalAssets() - lockedProfit;
    return freeFunds == 0 ? assets : (assets * supply) / freeFunds;
}

// Attack: Donate tokens to inflate freeFunds
// This reduces shares received by subsequent depositors
// Can be used to DoS deposits or extract value
```

**Example 2: Exchange Rate Manipulation for Unfair Claims** [MEDIUM]
> 📖 Reference: `reports/erc4626_findings/exchange-rate-manipulation-via-direct-transfers.md`
```solidity
// ❌ VULNERABLE: Exchange rate based on balance
function _exchangeRate() internal view returns (uint256) {
    uint256 totalHEU = heu.balanceOf(address(this));
    return (totalHEU * 1e18) / totalSupply();
}

// Attack:
// 1. Directly send HEU to contract (not via lock())
// 2. totalHEU increases but totalSupply unchanged
// 3. Exchange rate inflates
// 4. Call claim() to receive more HEU per stHEU
```

### Secure Implementation

**Fix: Internal Accounting**
```solidity
// ✅ SECURE: Track assets internally
uint256 private _internalAssets;

function totalAssets() public view returns (uint256) {
    return _internalAssets; // Not balanceOf!
}

function _deposit(address caller, address receiver, uint256 assets, uint256 shares) internal {
    asset.safeTransferFrom(caller, address(this), assets);
    _internalAssets += assets;
    _mint(receiver, shares);
}

function _withdraw(address caller, address receiver, address owner, uint256 assets, uint256 shares) internal {
    _burn(owner, shares);
    _internalAssets -= assets;
    asset.safeTransfer(receiver, assets);
}

// Optionally, allow sweeping of excess tokens to protocol
function sweep() external onlyOwner {
    uint256 excess = asset.balanceOf(address(this)) - _internalAssets;
    if (excess > 0) {
        asset.safeTransfer(treasury, excess);
    }
}
```

---

## 7. Decimal Handling Issues

### Overview

ERC4626 vaults must correctly handle the decimals of both the underlying asset and the vault shares. Mismatches can cause severe over/under-valuation of shares.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/h-04-yearn-token-shares-conversion-decimal-issue.md` (Sublime - Code4rena)

### Vulnerable Pattern Examples

**Example 1: Hardcoded 18 Decimals Assumption** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-04-yearn-token-shares-conversion-decimal-issue.md`
```solidity
// ❌ VULNERABLE: Assumes all tokens have 18 decimals
function getTokensForShares(uint256 shares, address asset) public view returns (uint256) {
    if (shares == 0) return 0;
    // WRONG! Should divide by 10**vault.decimals(), not 1e18
    return IyVault(liquidityToken[asset]).getPricePerFullShare().mul(shares).div(1e18);
}

// If underlying asset has 6 decimals (USDC):
// pricePerFullShare is in 6 decimals
// Dividing by 1e18 instead of 1e6 causes 1e12x undervaluation
```

**Example 2: Missing Decimal Scaling** [HIGH]
```solidity
// ❌ VULNERABLE: No scaling between different decimal tokens
function convertToShares(uint256 assets) public view returns (uint256) {
    // If vault shares are 18 decimals but asset is 6 decimals
    // This returns wrong values
    return (assets * totalSupply()) / totalAssets();
}
```

### Secure Implementation

**Fix: Dynamic Decimal Handling**
```solidity
// ✅ SECURE: Handle decimals dynamically
function decimals() public view override returns (uint8) {
    return IERC20Metadata(asset()).decimals();
}

function getTokensForShares(uint256 shares, address vaultAddress) public view returns (uint256) {
    IVault vault = IVault(vaultAddress);
    uint256 pricePerShare = vault.pricePerShare();
    uint8 vaultDecimals = vault.decimals();
    
    return (pricePerShare * shares) / (10 ** vaultDecimals);
}

// Or use scaling factor
uint256 private immutable _scalingFactor;

constructor(address asset_) {
    uint8 assetDecimals = IERC20Metadata(asset_).decimals();
    _scalingFactor = 10 ** assetDecimals;
}

function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    return supply == 0 ? assets : (assets * supply) / totalAssets();
}
```

---

## 8. Reentrancy Vulnerabilities

### Overview

ERC4626 vaults are susceptible to reentrancy attacks, especially when interacting with tokens that have callbacks (ERC777, ERC721, rebasing tokens) or when the vault integrates with external protocols.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/h-04-reentrancy-issue-in-yvaultdeposit.md` (JPEG'd - Code4rena)
> - `reports/erc4626_findings/h-1-cross-contract-reentrancy-allows-yield_token-theft-for-the-genericerc4626-wi.md` (Notional Exponent - Sherlock)

### Vulnerable Pattern Examples

**Example 1: Balance Cached Before Transfer** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-04-reentrancy-issue-in-yvaultdeposit.md`
```solidity
// ❌ VULNERABLE: Balance cached before transfer with ERC777 token
function deposit(uint256 amount) public returns (uint256 shares) {
    uint256 balanceBefore = totalAssets(); // Cached!
    
    // ERC777: tokensToSend hook gives control to sender
    token.transferFrom(msg.sender, address(this), amount);
    
    // Attacker reenters here with old balanceBefore
    shares = (amount * totalSupply()) / balanceBefore;
    _mint(msg.sender, shares);
}

// Attack with ERC777:
// balanceBefore = 1000, supply = 1000
// Outer deposit(500): balanceBefore cached as 1000
// During transfer, attacker calls inner deposit(500):
//   Inner: shares = 500 * 1000 / 1000 = 500 (correct)
// Outer continues: shares = 500 * 1500 / 1000 = 750 (inflated!)
// Attacker receives 500 + 750 = 1250 shares
// Withdrawing gives 1250 * 2000 / 2250 = 1111 assets (profit: 111)
```

**Example 2: Cross-Contract Reentrancy** [HIGH]
> 📖 Reference: `reports/erc4626_findings/h-1-cross-contract-reentrancy-allows-yield_token-theft-for-the-genericerc4626-wi.md`
```solidity
// ❌ VULNERABLE: Multiple approved vaults share state
modifier onlyApprovedVault() {
    if (!isApprovedVault[msg.sender]) revert Unauthorized();
    _;
}

// If VaultA and VaultB are both approved:
// 1. User calls VaultA.withdraw() which calls WithdrawalManager
// 2. During token transfer callback, attacker calls VaultB.deposit()
// 3. VaultB reads stale state from WithdrawalManager
// 4. Attacker extracts value through cross-contract reentrancy
```

### Secure Implementation

**Fix 1: Reentrancy Guard**
```solidity
// ✅ SECURE: Use ReentrancyGuard
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureVault is ERC4626, ReentrancyGuard {
    function deposit(uint256 assets, address receiver) 
        public 
        nonReentrant 
        returns (uint256 shares) 
    {
        shares = previewDeposit(assets);
        _deposit(msg.sender, receiver, assets, shares);
    }
    
    function withdraw(uint256 assets, address receiver, address owner)
        public
        nonReentrant
        returns (uint256 shares)
    {
        shares = previewWithdraw(assets);
        _withdraw(msg.sender, receiver, owner, assets, shares);
    }
}
```

**Fix 2: Check-Effects-Interactions Pattern**
```solidity
// ✅ SECURE: Update state before external calls
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = previewDeposit(assets);
    
    // Effects first
    _mint(receiver, shares);
    
    // Interactions last
    asset.safeTransferFrom(msg.sender, address(this), assets);
    
    emit Deposit(msg.sender, receiver, assets, shares);
}
```

**Fix 3: Cross-Contract Reentrancy Lock**
```solidity
// ✅ SECURE: Global lock across related contracts
contract GlobalLock {
    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;
    uint256 private _status = _NOT_ENTERED;
    
    modifier globalNonReentrant() {
        require(_status != _ENTERED, "ReentrancyGuard: reentrant call");
        _status = _ENTERED;
        _;
        _status = _NOT_ENTERED;
    }
}

// All vaults use same lock instance
contract VaultA is GlobalLock {
    function deposit(...) external globalNonReentrant { ... }
}

contract VaultB is GlobalLock {
    function deposit(...) external globalNonReentrant { ... }
}
```

---

## 9. Token Compatibility Issues

### Overview

ERC4626 vaults may fail to properly handle non-standard tokens including fee-on-transfer tokens, rebasing tokens, and tokens with hooks.

> **📚 Source Reports for Deep Dive:**
> - `reports/erc4626_findings/fee-on-transfer-tokens.md` (Polygon zkEVM - Spearbit)

### Vulnerable Pattern Examples

**Example 1: Fee-on-Transfer Token Not Handled** [MEDIUM]
> 📖 Reference: `reports/erc4626_findings/fee-on-transfer-tokens.md`
```solidity
// ❌ VULNERABLE: Assumes transferred amount equals requested amount
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = previewDeposit(assets);
    
    // If token has 1% transfer fee:
    // User approves 100, contract expects 100
    // But only 99 actually received!
    asset.safeTransferFrom(msg.sender, address(this), assets);
    
    _mint(receiver, shares); // Minting shares for 100, but only have 99
}
```

### Secure Implementation

**Fix 1: Measure Actual Received Amount**
```solidity
// ✅ SECURE: Handle fee-on-transfer tokens
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    uint256 balanceBefore = asset.balanceOf(address(this));
    asset.safeTransferFrom(msg.sender, address(this), assets);
    uint256 actualReceived = asset.balanceOf(address(this)) - balanceBefore;
    
    // Use actual received amount
    shares = _convertToShares(actualReceived, Math.Rounding.Down);
    require(shares > 0, "Zero shares");
    
    _mint(receiver, shares);
}
```

**Fix 2: Explicitly Disallow Fee-on-Transfer**
```solidity
// ✅ SECURE: Revert if fee-on-transfer detected
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    uint256 balanceBefore = asset.balanceOf(address(this));
    asset.safeTransferFrom(msg.sender, address(this), assets);
    uint256 balanceAfter = asset.balanceOf(address(this));
    
    require(balanceAfter - balanceBefore == assets, "Fee-on-transfer not supported");
    
    shares = previewDeposit(assets);
    _mint(receiver, shares);
}
```

---

## 10. Access Control & State Management

### Overview

Vaults must properly handle paused states, withdrawal limits, and ensure max* functions reflect actual limits.

### Vulnerable Pattern Examples

**Example 1: max* Functions Don't Reflect Pause State** [MEDIUM]
```solidity
// ❌ VULNERABLE: Returns max even when paused
function maxDeposit(address) public pure returns (uint256) {
    return type(uint256).max;
}

function deposit(uint256 assets, address receiver) public whenNotPaused returns (uint256) {
    // This will revert, but maxDeposit indicated deposits were possible
    // ...
}
```

### Secure Implementation

```solidity
// ✅ SECURE: max* reflects actual state
function maxDeposit(address receiver) public view returns (uint256) {
    if (paused()) return 0;
    if (depositsCapped && totalAssets() >= depositCap) return 0;
    
    uint256 userLimit = maxPerUser - balanceOf(receiver);
    uint256 globalLimit = depositCap - totalAssets();
    
    return min(userLimit, globalLimit);
}

function maxWithdraw(address owner) public view returns (uint256) {
    if (paused()) return 0;
    if (withdrawalsPaused) return 0;
    
    uint256 ownerAssets = convertToAssets(balanceOf(owner));
    uint256 availableLiquidity = asset.balanceOf(address(this));
    
    return min(ownerAssets, availableLiquidity);
}
```

---

## Detection Patterns Summary

### Code Patterns to Look For
```
- totalAssets() using balanceOf(address(this)) without internal tracking
- Missing virtual shares/decimal offset in share calculation
- No minimum deposit or zero share check
- Preview functions not matching actual execution
- Rounding in favor of user instead of vault
- max* functions returning type(uint256).max unconditionally
- Balance cached before external transfer call
- Missing reentrancy guards
- Hardcoded decimal assumptions (1e18)
- Fee calculations inconsistent between deposit/mint
```

### Comprehensive Audit Checklist

#### First Depositor Protection
- [ ] Virtual shares/decimal offset implemented
- [ ] OR dead shares minted to address(0)
- [ ] OR minimum initial deposit enforced
- [ ] Zero shares check in deposit/mint
- [ ] totalAssets uses internal tracking, not balanceOf

#### ERC4626 Compliance
- [ ] All 8 core functions implemented
- [ ] max* returns 0 when operations disabled
- [ ] preview* matches actual execution
- [ ] deposit/mint have equivalent first-deposit logic
- [ ] Rounding directions favor the vault

#### Security
- [ ] Reentrancy guards on all state-changing functions
- [ ] Check-effects-interactions pattern followed
- [ ] Slippage protection available
- [ ] Fee-on-transfer handling or explicit rejection
- [ ] Decimal handling is dynamic, not hardcoded

---

## Keywords for Search

`erc4626`, `vault`, `tokenized_vault`, `share_inflation`, `first_depositor_attack`, `inflation_attack`, `convertToShares`, `convertToAssets`, `previewDeposit`, `previewMint`, `previewWithdraw`, `previewRedeem`, `maxDeposit`, `maxMint`, `maxWithdraw`, `maxRedeem`, `totalAssets`, `virtual_shares`, `decimal_offset`, `dead_shares`, `exchange_rate_manipulation`, `donation_attack`, `rounding_direction`, `slippage_protection`, `fee_on_transfer`, `rebasing_token`, `reentrancy_vault`, `vault_compliance`, `eip4626`, `share_calculation`, `yield_vault`, `liquidity_pool`, `deposit_inflation`, `share_price_manipulation`

---

## Related Vulnerabilities

- [ERC20 Token Vulnerabilities](../erc20/) - Related token standard issues
- [Oracle Manipulation](../../oracle/) - Price feed manipulation affecting vault valuations
- [Flash Loan Attacks](../../general/flash-loan/) - Flash loans can amplify vault attacks
- [Reentrancy Patterns](../../general/reentrancy/) - Cross-contract reentrancy in DeFi

---

## Prevention Guidelines

### Development Best Practices

1. **Use OpenZeppelin's ERC4626 implementation** (v4.8+) with virtual shares
2. **Never rely on balanceOf for totalAssets** - use internal accounting
3. **Implement all 8 core ERC4626 functions** with proper compliance
4. **Add reentrancy guards** to all external functions
5. **Include slippage parameters** in deposit/mint/withdraw/redeem
6. **Test with extreme values** - 1 wei deposits, maximum uint256, empty vault
7. **Consider fee-on-transfer tokens** - either support or explicitly reject

### Testing Requirements

- Unit tests for first deposit scenarios
- Fuzz testing share/asset conversions
- Integration tests with fee-on-transfer tokens
- Reentrancy tests with ERC777 tokens
- Invariant tests: totalAssets >= sum of all user deposits minus withdrawals
- Edge case tests: zero supply, max uint256, rounding boundaries

---

*This database entry was synthesized from 1,324+ vulnerability reports analyzing ERC4626 vault implementations across multiple audit firms including Code4rena, Sherlock, Pashov Audit Group, Trail of Bits, Spearbit, and others.*
