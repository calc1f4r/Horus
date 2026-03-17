---
# Core Classification (Required)
protocol: generic
chain: everychain
category: economic
vulnerability_type: vault_share_inflation

# Attack Vector Details (Required)
attack_type: economic_exploit|donation_attack|first_depositor
affected_component: share_calculation|vault_deposit|token_minting

# Technical Primitives (Required)
primitives:
  - share_calculation
  - first_deposit
  - donation
  - totalAssets
  - totalSupply
  - convertToShares
  - convertToAssets
  - mulDiv
  - rounding_down
  - ERC4626
  - vault_exchange_rate
  - price_per_share

# Impact Classification (Required)
severity: medium
impact: fund_loss|share_dilution|zero_share_minting
exploitability: 0.65
financial_impact: high

# Context Tags
tags:
  - defi
  - vault
  - erc4626
  - yield
  - staking
  - lending
  - first_depositor
  - inflation_attack
  - donation_attack
  - share_manipulation

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: first_depositor_attack
pattern_key: first_depositor_attack | share_calculation | vault_share_inflation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - ERC4626
  - _convertToAssets
  - _convertToShares
  - _decimalsOffset
  - _deposit
  - _mint_shares
  - _withdraw
  - balanceOf
  - burn
  - convertToAssets
  - convertToShares
  - deposit
  - depositExactAmount
  - donation
  - execute
  - finalizeStake
  - first_deposit
  - mint
  - msg.sender
  - mulDiv
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### First Depositor / Vault Inflation Attack Reports
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Mach Finance - First Depositor Attack | `reports/yield_protocol_findings/m-02-first-depositor-attack-is-possible.md` | MEDIUM | Sherlock |
| Wise Lending - PendlePowerFarmToken Inflation | `reports/yield_protocol_findings/m-03-first-depositor-inflation-attack-in-pendlepowerfarmtoken.md` | MEDIUM | Sherlock |
| Curve Finance - Inflation Attack on Empty Ticks | `reports/yield_protocol_findings/inflation-attack-on-empty-ticks.md` | HIGH | MixBytes |
| Resolv - StUSR Inflation Attack | `reports/yield_protocol_findings/stusr-inflation-attack.md` | HIGH | MixBytes |
| Conic Finance - ExchangeRate Manipulation | `reports/yield_protocol_findings/exchangerate-can-be-manipulated.md` | MEDIUM | MixBytes |
| Vaultka - First Deposit Attack via Share Manipulation | `reports/yield_protocol_findings/first-deposit-attack-via-share-price-manipulation.md` | HIGH | Pashov Audit Group |
| Blend Capital - Backstop Deposit Inflation | `reports/yield_protocol_findings/backstop-deposit-inflation.md` | MEDIUM | Cantina |
| Cryptex - Pocket Inflation Attack | `reports/yield_protocol_findings/depositing-to-pocket-is-vulnerable-to-inﬂation-attacks.md` | HIGH | Cantina |
| Coinflip - Zero Share Minting via Balance Inflation | `reports/yield_protocol_findings/m-06-zero-share-minting-via-token-balance-inflation.md` | MEDIUM | Pashov Audit Group |
| Morpho Blue - Sandwich Attacks During Market Addition | `reports/yield_protocol_findings/m-3-malicious-actors-can-execute-sandwich-attacks-during-market-addition-with-ex.md` | MEDIUM | Sherlock |
| Kelp DAO - rsETH Price Manipulation | `reports/yield_protocol_findings/unexpected-amount-of-supported-assets-could-increase-rseth-price.md` | MEDIUM | Code4rena |
| Staking Vault - Initial Grief Attack | `reports/yield_protocol_findings/m-01-staking-vault-is-susceptible-to-initial-grief-attack.md` | MEDIUM | Sherlock |
| xERC4626 - First Deposit Exploit | `reports/yield_protocol_findings/m-02-first-xerc4626-deposit-exploit-can-break-share-calculation.md` | MEDIUM | Sherlock |

### External Links
- [OpenZeppelin ERC4626 Inflation Attack Analysis](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3706)
- [Uniswap V2 Minimum Liquidity Pattern](https://github.com/Uniswap/v2-core/blob/ee547b17853e71ed4e0101ccfd52e70d5acded58/contracts/UniswapV2Pair.sol#L120)
- [OpenZeppelin ERC4626 Virtual Shares Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol)

---

# Vault Inflation Attack / First Depositor Attack - Comprehensive Database

**A Complete Pattern-Matching Guide for ERC4626 and Vault Share Security Audits**

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

The Vault Inflation Attack (also known as First Depositor Attack, Share Price Manipulation, or Donation Attack) is a critical vulnerability affecting vault-based protocols that use share-based accounting. This attack exploits the mathematical relationship between deposited assets and minted shares, allowing an attacker to manipulate the exchange rate and steal funds from subsequent depositors through precision loss during integer division.

> **Root Cause Statement**: This vulnerability exists because the share calculation formula `shares = assets * totalShares / totalAssets` rounds down to zero when an attacker inflates `totalAssets` via donation while keeping `totalShares` minimal, leading to subsequent depositors receiving zero or negligible shares while their assets are effectively stolen.

**Observed Frequency**: 20+ reports analyzed across major audit firms
**Consensus Severity**: MEDIUM to HIGH (context-dependent)
**Attack Cost**: Minimal (donation amount + gas fees)
**Affected Protocols**: ERC4626 vaults, staking pools, lending vaults, LP token systems, any share-based accounting

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of first_depositor_attack"
- Pattern key: `first_depositor_attack | share_calculation | vault_share_inflation`
- Interaction scope: `single_contract`
- Primary affected component(s): `share_calculation|vault_deposit|token_minting`
- High-signal code keywords: `ERC4626`, `_convertToAssets`, `_convertToShares`, `_decimalsOffset`, `_deposit`, `_mint_shares`, `_withdraw`, `balanceOf`
- Typical sink / impact: `fund_loss|share_dilution|zero_share_minting`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `3.function -> DonationImmuneVault.function -> MinimumDepositVault.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: First deposit to vault with zero total supply has manipulable share calculation
- Signal 2: Direct asset transfer (donation) changes exchange rate before victim's deposit
- Signal 3: No minimum initial deposit or dead shares mechanism
- Signal 4: Share price can be inflated atomically in a single transaction

#### False Positive Guards

- Not this bug when: Vault uses virtual offset (ERC4626 `_decimalsOffset()`) to prevent inflation
- Safe if: Dead shares mechanism: minimum initial deposit burned to address(dead)
- Requires attacker control of: specific conditions per pattern

## Vulnerability Description

### Root Cause

The fundamental issue stems from the share minting formula used in vault-based systems:

```solidity
shares = (depositAmount * totalShares) / totalAssets
```

When `totalAssets` is much larger than `depositAmount * totalShares`, integer division rounds down to zero. An attacker can artificially inflate `totalAssets` by:

1. Being the first depositor and minting minimal shares (e.g., 1 wei)
2. Donating a large amount of tokens directly to the vault contract
3. This creates a state where `totalAssets >> totalShares`

Subsequent depositors receive zero or negligible shares due to rounding, while their deposited assets inflate the value of the attacker's shares.

### Attack Scenario

**Classic First Depositor Attack Flow:**

1. **Initial State**: Vault has 0 shares and 0 assets
2. **Attacker Deposits**: Attacker deposits 1 wei, receives 1 share
3. **Donation**: Attacker donates `D` tokens directly to the vault (via `transfer()`)
4. **State After Donation**: 
   - `totalShares = 1`
   - `totalAssets = 1 + D` (e.g., 1 + 1e18 = ~1e18)
5. **Victim Deposits**: Victim deposits `V` tokens
   - Calculated shares = `V * 1 / (1 + D)`
   - If `V <= D`, shares round down to 0
6. **Victim Receives 0 Shares**: Victim's deposit goes to the vault but they get nothing
7. **Attacker Withdraws**: Attacker withdraws 1 share and receives `totalAssets` (original + victim's deposit)

**Numerical Example (from Resolv StUSR Report):**

| Step | totalShares + 1 | totalAssets + 1 | 1 Share Value | Attacker Profit |
|------|----------------|-----------------|---------------|-----------------|
| 1 | 0 | 0 | - | - |
| 2 | 1001 | 1001 wei | 1 wei | 0 |
| 3 | 1001 | 1,001,000e18 | 1000 USR | -1000 USD |
| 4 | 1002 | 1,002,999e18 | ~1001 USR | 0 |
| 5 | 1003 | 1,004,998e18 | ~1002 USR | +1000 USD |

---

## Vulnerable Pattern Examples

**Example 1: Basic ERC4626 Without Protection** [MEDIUM to HIGH]
> 📖 Reference: `reports/yield_protocol_findings/m-02-first-depositor-attack-is-possible.md`
```solidity
// ❌ VULNERABLE: Standard ERC4626 without inflation protection
contract VulnerableVault is ERC4626 {
    constructor(IERC20 asset) ERC4626(asset) ERC20("Vault", "vTKN") {}
    
    // Inherited _convertToShares is vulnerable to inflation attack
    function _convertToShares(uint256 assets, Math.Rounding rounding) 
        internal view override returns (uint256) 
    {
        uint256 supply = totalSupply();
        // When attacker donates, totalAssets() >> assets * supply
        // Result: shares rounds down to 0
        return assets.mulDiv(supply, totalAssets(), rounding);
    }
}
```

**Example 2: Custom Share Calculation Without Virtual Offset** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-06-zero-share-minting-via-token-balance-inflation.md`
```solidity
// ❌ VULNERABLE: Staking contract using balance for share calculation
function finalizeStake(address token) external nonReentrant {
    uint256 depositAmount = pendingDeposits[msg.sender][token];
    
    uint256 totalBalance = IERC20(token).balanceOf(address(this));
    uint256 currentShares = tokenInfo[token].totalShares;

    uint256 mintedShares;
    if (currentShares == 0 || totalBalance == 0) {
        mintedShares = depositAmount;  // First depositor gets 1:1
    } else {
        // VULNERABLE: Attacker can inflate totalBalance via donation
        mintedShares = (depositAmount * currentShares) / totalBalance;
    }
    
    tokenInfo[token].totalShares += mintedShares;
    shares[msg.sender][token] += mintedShares;
}
```

**Example 3: Pocket/Vault with pricePerShare Manipulation** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/depositing-to-pocket-is-vulnerable-to-inﬂation-attacks.md`
```solidity
// ❌ VULNERABLE: Pocket contract using direct balance
function registerDeposit(uint256 collateralAmount) external {
    uint256 totalAssets = IERC20(collateral).balanceOf(address(this));
    uint256 totalShares = $.totalShares;
    
    uint256 sharesToMint;
    if (totalShares == 0) {
        sharesToMint = collateralAmount;
    } else {
        // VULNERABLE: shares = collateralAmount * totalShares / totalAssets
        // If attacker donated, totalAssets is inflated
        sharesToMint = collateralAmount * totalShares / totalAssets;
    }
    
    $.sharesOf[msg.sender] += sharesToMint;
    $.totalShares += sharesToMint;
}
```

**Example 4: LP Token Minting Vulnerable to Exchange Rate Manipulation** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/exchangerate-can-be-manipulated.md`
```solidity
// ❌ VULNERABLE: LP minting without minimum liquidity lock
function deposit(uint256 amount, uint256 minLPReceived, bool stake) external {
    uint256 lpReceived;
    
    if (totalSupply == 0) {
        lpReceived = amount;  // First depositor sets rate
    } else {
        // VULNERABLE: exchangeRate can be manipulated via donation
        lpReceived = amount * totalSupply / totalUnderlying;
    }
    
    require(lpReceived >= minLPReceived, "Slippage");
    _mint(msg.sender, lpReceived);
}
```

**Example 5: Rust/Soroban Vault Inflation** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/backstop-deposit-inflation.md`
```rust
// ❌ VULNERABLE: Soroban vault without virtual shares
pub fn execute_deposit(e: &Env, from: &Address, amount: i128) {
    let pool_balance = TokenClient::new(e, &pool.backstop_token).balance(&e.current_contract_address());
    let total_shares = pool.shares;
    
    let to_mint: i128;
    if total_shares == 0 {
        to_mint = amount;
    } else {
        // VULNERABLE: Uses fixed_mul_floor which rounds down
        to_mint = amount.fixed_mul_floor(total_shares, pool_balance).unwrap();
    }
    
    pool.shares += to_mint;
    user_balance.shares += to_mint;
}
```

**Example 6: AMM Tick Inflation (Curve crvUSD)** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/inflation-attack-on-empty-ticks.md`
```solidity
// ❌ VULNERABLE: AMM tick share calculation
function _mint_shares(uint256 collateral, uint256 tickIndex) internal returns (uint256) {
    Tick storage tick = ticks[tickIndex];
    uint256 tickShares = tick.totalShares;
    uint256 tickCollateral = tick.totalCollateral;
    
    if (tickShares == 0) {
        return collateral;
    }
    
    // VULNERABLE: Attacker can inflate tickCollateral via create_loan + repay cycles
    // Shares calculation: collateral * tickShares / tickCollateral
    return collateral * tickShares / tickCollateral;
}
```

**Example 7: Reward Token Compounding Inflation** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-03-first-depositor-inflation-attack-in-pendlepowerfarmtoken.md`
```solidity
// ❌ VULNERABLE: PowerFarmToken using reward compounding for inflation
function depositExactAmount(uint256 _underlyingLpAssetAmount) external returns (uint256) {
    uint256 totalLpAssetsToDistribute = _getCurrentSharePriceInWei() * _getTotalTokensInWei() / PRECISION_FACTOR_E18;
    
    uint256 shares = _underlyingLpAssetAmount * _getTotalTokensInWei() / totalLpAssetsToDistribute;
    
    // VULNERABLE: Attacker can call exchangeRewardsForCompoundingWithIncentive()
    // to donate rewards and inflate totalLpAssetsToDistribute
    _mint(msg.sender, shares);
    return shares;
}
```

---

## Impact Analysis

### Technical Impact

- **Zero Share Minting**: Victims receive 0 shares while losing entire deposit
- **Share Dilution**: Victims receive significantly fewer shares than expected
- **Exchange Rate Manipulation**: Permanent distortion of price-per-share
- **State Corruption**: Vault accounting becomes permanently skewed
- **Griefing Vector**: Even without profit, attacker can prevent vault usage

### Business Impact

- **Direct Fund Loss**: Victims lose deposited assets to attacker (up to 100%)
- **Protocol Insolvency Risk**: Accumulated losses can exceed protocol reserves
- **Loss of User Trust**: High-profile exploitation damages reputation
- **Regulatory Concerns**: Fund loss may trigger regulatory scrutiny
- **Market Impact**: Token price can crash if vault is core to protocol

### Affected Scenarios

| Scenario | Risk Level | Notes |
|----------|------------|-------|
| New vault deployment | CRITICAL | Empty vault is most vulnerable |
| New token pair addition | HIGH | Fresh pools have 0 liquidity |
| After total withdrawal | HIGH | Vault returns to vulnerable state |
| Low liquidity periods | MEDIUM | Easier to manipulate exchange rate |
| Rebasing token vaults | MEDIUM | Balance changes enable attacks |
| Multi-asset vaults | MEDIUM | Each asset pool may be vulnerable |

### Severity Distribution Across Reports

- **CRITICAL**: 0 reports (usually rated lower due to first-depositor constraint)
- **HIGH**: 5 reports (when attack is profitable with low cost)
- **MEDIUM**: 12 reports (most common rating)
- **LOW**: 3 reports (when mitigations partially in place)

---

## Secure Implementation

**Fix 1: Virtual Shares and Assets (OpenZeppelin Pattern)** ✅ RECOMMENDED
```solidity
// ✅ SECURE: OpenZeppelin's virtual shares/assets approach
abstract contract SecureERC4626 is ERC4626 {
    // Virtual offset - increases effective decimal precision
    uint8 private immutable _decimalsOffset;
    
    constructor(uint8 decimalsOffset_) {
        _decimalsOffset = decimalsOffset_;
    }
    
    function _convertToShares(uint256 assets, Math.Rounding rounding)
        internal view override returns (uint256)
    {
        // Add virtual shares (10^offset) to denominator
        // This makes inflation attack prohibitively expensive
        return assets.mulDiv(
            totalSupply() + 10 ** _decimalsOffset(),  // Add virtual shares
            totalAssets() + 1,                         // Add virtual asset
            rounding
        );
    }
    
    function _convertToAssets(uint256 shares, Math.Rounding rounding)
        internal view override returns (uint256)
    {
        return shares.mulDiv(
            totalAssets() + 1,
            totalSupply() + 10 ** _decimalsOffset(),
            rounding
        );
    }
    
    function _decimalsOffset() internal view virtual returns (uint8) {
        return 3;  // Typical offset, makes attack cost 1000x more
    }
}
```

**Fix 2: Dead Shares (Uniswap V2 Pattern)** ✅ RECOMMENDED
```solidity
// ✅ SECURE: Burn initial shares to address(0) like Uniswap V2
contract SecureVaultWithDeadShares is ERC4626 {
    uint256 public constant MINIMUM_LIQUIDITY = 1000;
    bool private _initialized;
    
    function _deposit(
        address caller,
        address receiver,
        uint256 assets,
        uint256 shares
    ) internal override {
        if (!_initialized) {
            // First deposit: burn MINIMUM_LIQUIDITY to address(0)
            require(shares > MINIMUM_LIQUIDITY, "Insufficient initial deposit");
            
            super._deposit(caller, receiver, assets, shares - MINIMUM_LIQUIDITY);
            _mint(address(0), MINIMUM_LIQUIDITY);  // Permanently locked
            _initialized = true;
        } else {
            super._deposit(caller, receiver, assets, shares);
        }
    }
}
```

**Fix 3: Internal Asset Tracking (Donation Immunity)**
```solidity
// ✅ SECURE: Track assets internally, ignore direct transfers
contract DonationImmuneVault is ERC4626 {
    uint256 private _trackedAssets;
    
    function totalAssets() public view override returns (uint256) {
        // Use internal tracking instead of balanceOf
        // Donations don't affect share calculation
        return _trackedAssets;
    }
    
    function _deposit(
        address caller,
        address receiver,
        uint256 assets,
        uint256 shares
    ) internal override {
        _trackedAssets += assets;  // Only track actual deposits
        super._deposit(caller, receiver, assets, shares);
    }
    
    function _withdraw(
        address caller,
        address receiver,
        address owner,
        uint256 assets,
        uint256 shares
    ) internal override {
        _trackedAssets -= assets;  // Only track actual withdrawals
        super._withdraw(caller, receiver, owner, assets, shares);
    }
}
```

**Fix 4: Minimum Deposit Requirement**
```solidity
// ✅ SECURE: Enforce minimum deposit to make attack expensive
contract MinimumDepositVault is ERC4626 {
    uint256 public constant MIN_DEPOSIT = 1e18;  // 1 full token minimum
    
    function deposit(uint256 assets, address receiver) 
        public override returns (uint256) 
    {
        require(assets >= MIN_DEPOSIT, "Deposit too small");
        return super.deposit(assets, receiver);
    }
    
    function mint(uint256 shares, address receiver) 
        public override returns (uint256) 
    {
        uint256 assets = previewMint(shares);
        require(assets >= MIN_DEPOSIT, "Deposit too small");
        return super.mint(shares, receiver);
    }
}
```

**Fix 5: Initial Seeding by Protocol**
```solidity
// ✅ SECURE: Protocol seeds initial liquidity at deployment
contract SeededVault is ERC4626 {
    constructor(IERC20 asset_, uint256 seedAmount) ERC4626(asset_) {
        // Protocol provides initial liquidity
        asset_.transferFrom(msg.sender, address(this), seedAmount);
        _mint(address(0), seedAmount);  // Burn initial shares
    }
}
```

**Fix 6: Rust/Soroban Virtual Shares Implementation**
```rust
// ✅ SECURE: Soroban vault with virtual shares
pub fn execute_deposit(e: &Env, from: &Address, amount: i128) -> i128 {
    let pool_balance = get_pool_balance(e);
    let total_shares = pool.shares;
    
    // Add virtual offset (1000) to make inflation prohibitively expensive
    const VIRTUAL_SHARES: i128 = 1000;
    const VIRTUAL_ASSETS: i128 = 1;
    
    let to_mint = amount
        .fixed_mul_floor(total_shares + VIRTUAL_SHARES, pool_balance + VIRTUAL_ASSETS)
        .unwrap();
    
    require!(to_mint > 0, Error::ZeroShares);
    
    pool.shares += to_mint;
    user_balance.shares += to_mint;
    to_mint
}
```

---

## Detection Patterns

### Code Patterns to Look For

```
Anti-Patterns (VULNERABLE):
- totalSupply() == 0 ? assets : assets * totalSupply() / totalAssets()
- balanceOf(address(this)) used in share calculation
- First depositor receives shares == depositAmount
- No virtual offset in _convertToShares
- No MINIMUM_LIQUIDITY or dead shares mechanism
- No minimum deposit requirement
- mulDiv without virtual offset protection

Safe Patterns (SECURE):
- _decimalsOffset() implementation
- MINIMUM_LIQUIDITY constant with burn to address(0)
- Internal asset tracking separate from balanceOf
- Virtual shares/assets in conversion formulas
- require(shares > 0) after calculation
```

### Static Analysis Signatures

```yaml
# Semgrep rule for detecting vulnerable vault patterns
rules:
  - id: vault-inflation-attack
    patterns:
      - pattern-either:
          - pattern: |
              if ($TOTAL_SUPPLY == 0) {
                $SHARES = $ASSETS;
              } else {
                $SHARES = $ASSETS * $TOTAL_SUPPLY / $TOTAL_ASSETS;
              }
          - pattern: |
              $SHARES = $ASSETS.mulDiv($TOTAL_SUPPLY, $TOTAL_ASSETS, ...)
    pattern-not:
      - pattern: |
          $SHARES = $ASSETS.mulDiv($TOTAL_SUPPLY + 10 ** ..., ...)
    message: "Potential vault inflation vulnerability - no virtual offset protection"
    severity: WARNING
```

### Audit Checklist

- [ ] Does the vault use virtual shares/assets offset in conversion?
- [ ] Is there a MINIMUM_LIQUIDITY mechanism with dead shares?
- [ ] Does the vault use internal asset tracking vs balanceOf?
- [ ] Is there a minimum deposit requirement?
- [ ] What happens when the vault is completely emptied?
- [ ] Are there any donation vectors (direct transfer, rewards)?
- [ ] Does the first depositor receive special treatment?
- [ ] Is totalAssets() manipulable by external actors?
- [ ] Are there slippage protections (minSharesOut) in deposit?
- [ ] Is the vault vulnerable after protocol pause/unpause?

---

## Real-World Examples

### Known Exploits & Findings

| Protocol | Year | Audit Firm | Severity | Status |
|----------|------|------------|----------|--------|
| Curve Finance (crvUSD) | 2023 | MixBytes | HIGH | Fixed |
| Resolv (StUSR) | 2024 | MixBytes | HIGH | Fixed |
| Conic Finance | 2023 | MixBytes | MEDIUM | Fixed |
| Cryptex (Pocket) | 2024 | Cantina | HIGH | Fixed |
| Wise Lending | 2024 | Sherlock | MEDIUM | Fixed |
| Vaultka | 2024 | Pashov | HIGH | Fixed |
| Blend Capital | 2024 | Cantina | MEDIUM | Fixed |

### Attack Cost Analysis

For a vault without protection:
- **Minimum Attack Cost**: Gas fees only (~$1-10)
- **Donation Required**: Slightly more than victim's expected deposit
- **Profit Margin**: Up to 100% of victim's deposit minus donation
- **With 1000 Virtual Offset**: Attack cost multiplied by 1000x
- **With Dead Shares (1000)**: Initial donation worth ~1000x less

---

## Prevention Guidelines

### Development Best Practices

1. **Always use virtual shares/assets offset** (minimum 3 decimals)
2. **Implement dead shares mechanism** for new vaults
3. **Use internal asset tracking** instead of balanceOf
4. **Enforce minimum deposit amounts** appropriate for token decimals
5. **Add slippage protection** (minSharesOut parameter)
6. **Seed initial liquidity** before public deposit opening
7. **Document the protection mechanism** in comments

### Testing Requirements

```solidity
// Required test cases for vault security
function testFirstDepositorInflationAttack() public {
    // 1. Attacker deposits minimal amount
    vault.deposit(1, attacker);
    
    // 2. Attacker donates large amount
    token.transfer(address(vault), 1e18);
    
    // 3. Victim deposits
    uint256 victimShares = vault.deposit(1e18, victim);
    
    // 4. Assert victim receives fair shares (not 0)
    assertGt(victimShares, 0);
    assertGe(victimShares, 1e18 * 99 / 100);  // At least 99%
}

function testEmptyVaultReinitialization() public {
    // Test that vault remains safe after all withdrawals
}

function testDonationDoesNotAffectExchangeRate() public {
    // Test that direct transfers don't manipulate share price
}
```

### Fuzzing Targets

- Share calculation edge cases with extreme values
- First deposit scenarios with minimal amounts
- Donation attacks with various amounts
- Sequential deposit/withdraw cycles
- Empty vault reinitialization scenarios

---

## References

### Technical Documentation
- [OpenZeppelin ERC4626 Documentation](https://docs.openzeppelin.com/contracts/4.x/erc4626)
- [EIP-4626: Tokenized Vault Standard](https://eips.ethereum.org/EIPS/eip-4626)
- [Uniswap V2 Core Whitepaper](https://uniswap.org/whitepaper.pdf)

### Security Research
- [OpenZeppelin: Inflation Attack with Virtual Shares](https://blog.openzeppelin.com/a]inflation-attack-erc4626-vaults)
- [ToB: ERC4626 Security Considerations](https://blog.trailofbits.com/2023/03/23/erc4626-security/)
- [MixBytes: Share Inflation Attacks Analysis](https://mixbytes.io/blog/share-inflation-attacks)

---

## Keywords for Search

`vault inflation attack`, `first depositor attack`, `share price manipulation`, `donation attack`, `ERC4626 vulnerability`, `share dilution`, `zero share minting`, `exchange rate manipulation`, `virtual shares`, `dead shares`, `MINIMUM_LIQUIDITY`, `totalAssets manipulation`, `convertToShares`, `convertToAssets`, `mulDiv rounding`, `first deposit exploit`, `price per share inflation`, `vault griefing`, `staking inflation`, `LP token manipulation`, `pool share attack`, `rounding down exploit`, `integer division attack`

---

## Related Vulnerabilities

- [Fee-on-Transfer Token Incompatibility](../token-handling/fee-on-transfer.md) - Compounds with inflation attack
- [Reentrancy in Vault Operations](../reentrancy/vault-reentrancy.md) - Can enable atomic inflation
- [Flash Loan Attacks](../flash-loan/FLASH_LOAN_VULNERABILITIES.md) - Can fund inflation attack
- [Rounding Errors](../arithmetic/rounding-errors.md) - Root cause of share loss

---

## DeFiHackLabs Real-World Exploits (9 incidents)

**Category**: Inflation Attack | **Total Losses**: $11.1M | **Sub-variants**: 2

### Sub-variant Breakdown

#### Inflation-Attack/Donate Inflation (6 exploits, $10.7M)

- **HundredFinance** (2023-04, $7.0M, optimism) | PoC: `DeFiHackLabs/src/test/2023-04/HundredFinance_2_exp.sol`
- **Raft_fi** (2023-11, $3.2M, ethereum) | PoC: `DeFiHackLabs/src/test/2023-11/Raft_exp.sol`
- **WiseLending** (2023-10, $260K, ethereum) | PoC: `DeFiHackLabs/src/test/2023-10/WiseLending_exp.sol`
- *... and 3 more exploits*

#### Inflation-Attack/Compound V2 (3 exploits, $332K)

- **ChannelsFinance** (2023-12, $320K, bsc) | PoC: `DeFiHackLabs/src/test/2023-12/ChannelsFinance_exp.sol`
- **kTAF** (2023-10, $8K, ethereum) | PoC: `DeFiHackLabs/src/test/2023-10/kTAF_exp.sol`
- **MetaLend** (2023-11, $4K, ethereum) | PoC: `DeFiHackLabs/src/test/2023-11/MetaLend_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| HundredFinance | 2023-04-15 | $7.0M | Donate Inflation ExchangeRate && Rounding Error | optimism |
| Raft_fi | 2023-11-10 | $3.2M | Donate Inflation ExchangeRate & Rounding Error | ethereum |
| ChannelsFinance | 2023-12-30 | $320K | CompoundV2 Inflation Attack | bsc |
| WiseLending | 2023-10-13 | $260K | Donate Inflation ExchangeRate && Rounding Error | ethereum |
| bZxProtocol | 2023-12-02 | $208K | Inflation Attack | ethereum |
| BaoCommunity | 2023-07-04 | $46K | Donate Inflation ExchangeRate && Rounding Error | None |
| MahaLend | 2023-11-11 | $20K | Donate Inflation ExchangeRate & Rounding Error | ethereum |
| kTAF | 2023-10-19 | $8K | CompoundV2 Inflation Attack | ethereum |
| MetaLend | 2023-11-25 | $4K | CompoundV2 Inflation Attack | ethereum |

### Top PoC References

- **HundredFinance** (2023-04, $7.0M): `DeFiHackLabs/src/test/2023-04/HundredFinance_2_exp.sol`
- **Raft_fi** (2023-11, $3.2M): `DeFiHackLabs/src/test/2023-11/Raft_exp.sol`
- **ChannelsFinance** (2023-12, $320K): `DeFiHackLabs/src/test/2023-12/ChannelsFinance_exp.sol`
- **WiseLending** (2023-10, $260K): `DeFiHackLabs/src/test/2023-10/WiseLending_exp.sol`
- **bZxProtocol** (2023-12, $208K): `DeFiHackLabs/src/test/2023-12/bZx_exp.sol`
- **MahaLend** (2023-11, $20K): `DeFiHackLabs/src/test/2023-11/MahaLend_exp.sol`
- **kTAF** (2023-10, $8K): `DeFiHackLabs/src/test/2023-10/kTAF_exp.sol`
- **MetaLend** (2023-11, $4K): `DeFiHackLabs/src/test/2023-11/MetaLend_exp.sol`

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

`ERC4626`, `_convertToAssets`, `_convertToShares`, `_decimalsOffset`, `_deposit`, `_mint_shares`, `_withdraw`, `balanceOf`, `burn`, `convertToAssets`, `convertToShares`, `defi`, `deposit`, `depositExactAmount`, `donation`, `donation_attack`, `economic`, `erc4626`, `execute`, `finalizeStake`, `first_deposit`, `first_depositor`, `inflation_attack`, `lending`, `mint`, `msg.sender`, `mulDiv`, `price_per_share`, `rounding_down`, `share_calculation`, `share_manipulation`, `staking`, `totalAssets`, `totalSupply`, `vault`, `vault_exchange_rate`, `vault_share_inflation`, `yield`
