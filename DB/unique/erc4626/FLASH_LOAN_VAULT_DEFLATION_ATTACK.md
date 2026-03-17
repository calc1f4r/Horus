---
# Core Classification
protocol: Spectra
chain: everychain
category: economic
vulnerability_type: flash_loan_vault_deflation

# Attack Vector Details
attack_type: yield_drain
affected_component: PrincipalToken

# Technical Primitives
primitives:
  - flash_loan
  - erc4626_share_price
  - vault_deflation
  - share_price_reset
  - yield_extraction
  - ibt_vault

# Impact Classification
severity: medium
impact: yield_theft
exploitability: 0.5
financial_impact: high

# Context Tags
tags:
  - erc4626
  - flash_loan
  - vault_deflation
  - share_price_manipulation
  - yield_theft
  - principal_token
  - ibt

# Version Info
language: solidity
version: ">=0.8.0"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | PrincipalToken | flash_loan_vault_deflation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _convertToAssets
  - approve
  - balanceOf
  - borrow
  - borrowing
  - complete
  - deposit
  - erc4626_share_price
  - flashLoan
  - flash_loan
  - ibt_vault
  - maxFlashLoan
  - mint
  - msg.sender
  - onFlashLoan
  - receive
  - safeTransferFrom
  - share_price_reset
  - totalSupply
  - transferFrom
---

## Reference
- [Source Report]: reports/erc4626_findings/m-02-all-yield-generated-in-the-ibt-vault-can-be-drained-by-performing-a-vault-d.md

## Flash Loan Vault Deflation Attack: Draining Accumulated Yield via Share Price Reset

**Case Study: Spectra Protocol - Code4rena 2024**

### Overview

A novel economic attack exploiting ERC4626 vault share price mechanics combined with flash loan functionality. When a protocol's Principal Token contract holds the majority of an Interest-Bearing Token (IBT) vault's supply and offers flash loans, an attacker can borrow the entire IBT supply, redeem all shares to reset the vault's share price to its default value, then re-mint shares at the deflated price—effectively extracting all accumulated yield at the cost of only a flash loan fee.

This attack is unique because:
1. It exploits the mathematical property that empty ERC4626 vaults return to default pricing
2. Flash loans provide the capital needed to drain an entire vault
3. The attack is profitable when accumulated yield exceeds the flash loan fee
4. It leaves legitimate users with permanent losses



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | PrincipalToken | flash_loan_vault_deflation`
- Interaction scope: `single_contract`
- Primary affected component(s): `PrincipalToken`
- High-signal code keywords: `_convertToAssets`, `approve`, `balanceOf`, `borrow`, `borrowing`, `complete`, `deposit`, `erc4626_share_price`
- Typical sink / impact: `yield_theft`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `SecureIBTVault.function -> VaultDeflationExploit.function -> demonstrating.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Most ERC4626 implementations calculate share price using:

$$sharePrice = \frac{totalAssets}{totalShares}$$

When `totalAssets = 0` and `totalShares = 0`, the vault falls back to a default price (typically 1:1). This mathematical discontinuity can be exploited when:

1. A flash loan allows borrowing the entire vault's share supply
2. The attacker redeems ALL shares, making `totalAssets = totalShares = 0`
3. The vault resets to default 1:1 pricing
4. Attacker re-mints the same number of shares at the deflated price
5. The difference between old price and new price is pure profit

```solidity
// OpenZeppelin ERC4626 implementation showing default price behavior
function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view virtual returns (uint256) {
    // When totalSupply() == 0, this returns shares * 1 = shares (default 1:1)
    return shares.mulDiv(totalAssets() + 1, totalSupply() + 10 ** _decimalsOffset(), rounding);
}
```

#### The Mathematical Attack

**Before Attack:**
- IBT Vault has 100 shares backed by 200 underlying tokens
- Share price = 200/100 = 2:1 (each share worth 2 tokens)
- Accumulated yield = 100 tokens (depositors put in 100, earned 100)

**Attack Execution:**
1. Flash borrow all 100 shares from PrincipalToken
2. Redeem 100 shares → receive 200 tokens, vault now empty
3. Mint 100 + fee shares at 1:1 price → deposit ~101 tokens
4. Repay flash loan (100 shares + fee)
5. **Profit**: 200 - 101 = ~99 tokens (minus flash loan fee)

**After Attack:**
- Vault is back to 100 shares, ~101 tokens
- Share price reset to ~1:1
- All accumulated yield extracted by attacker
- Original depositors lost 100 tokens of yield

#### Attack Scenario

**Prerequisites:**
- ERC4626 IBT vault with accumulated yield (share price > 1)
- PrincipalToken contract holds majority/all of IBT supply
- PrincipalToken offers permissionless flash loans of IBT
- Flash loan fee is less than accumulated yield

**Step-by-Step Attack:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INITIAL STATE                                       │
│  IBT Vault: 100 shares, 200 underlying (price = 2:1)                       │
│  PrincipalToken: Holds all 100 IBT shares                                  │
│  Accumulated Yield: 100 underlying tokens                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: Flash Loan                                                         │
│  Attacker calls principalToken.flashLoan(100 shares)                       │
│  Attacker now holds: 100 IBT shares                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: Redeem All Shares                                                  │
│  Attacker calls ibt.redeem(100 shares)                                     │
│  Attacker receives: 200 underlying tokens                                   │
│  IBT Vault state: 0 shares, 0 underlying                                   │
│  ⚠️ SHARE PRICE RESETS TO DEFAULT (1:1)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: Re-Mint at Deflated Price                                          │
│  Attacker calls ibt.mint(100 + fee shares)                                 │
│  Attacker deposits: ~101 underlying tokens (at 1:1 price)                  │
│  IBT Vault state: ~101 shares, ~101 underlying                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 4: Repay Flash Loan                                                   │
│  Attacker returns 100 + fee IBT shares to PrincipalToken                   │
│  Attacker profit: 200 - 101 - fees ≈ 99 underlying tokens                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FINAL STATE                                         │
│  IBT Vault: ~101 shares, ~101 underlying (price ≈ 1:1)                     │
│  PrincipalToken users: Lost all 100 tokens of accumulated yield            │
│  Attacker: Gained ~99 underlying tokens                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vulnerable Pattern Examples

**Example 1: Permissionless Flash Loan of Entire IBT Balance** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Allows borrowing entire IBT supply without rate protection
function flashLoan(
    IERC3156FlashBorrower _receiver,
    address _token,
    uint256 _amount,
    bytes calldata _data
) external override returns (bool) {
    if (_amount > maxFlashLoan(_token)) revert FlashLoanExceedsMaxAmount();

    uint256 fee = flashFee(_token, _amount);
    _updateFees(fee);

    // Lend the entire IBT balance - enables vault deflation
    IERC20(ibt).safeTransfer(address(_receiver), _amount);

    // Callback where attack occurs
    if (_receiver.onFlashLoan(msg.sender, _token, _amount, fee, _data) != ON_FLASH_LOAN)
        revert FlashLoanCallbackFailed();

    // No check that IBT share price hasn't decreased
    IERC20(ibt).safeTransferFrom(address(_receiver), address(this), _amount + fee);

    return true;
}

function maxFlashLoan(address _token) public view override returns (uint256) {
    if (_token != ibt) return 0;
    // VULNERABLE: Entire balance can be borrowed
    return IERC4626(ibt).balanceOf(address(this));
}
```

**Example 2: ERC4626 Default Price Behavior** [Severity: Context-Dependent]
```solidity
// Standard ERC4626 behavior - resets to default when empty
function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view virtual returns (uint256) {
    // When vault is empty (totalSupply = 0), defaults to 1:1 pricing
    // This is correct behavior but exploitable in certain contexts
    return shares.mulDiv(
        totalAssets() + 1,                    // +1 for virtual assets
        totalSupply() + 10 ** _decimalsOffset(), // +offset for precision
        rounding
    );
}
```

**Example 3: Attacker's Flash Loan Callback** [Severity: HIGH]
```solidity
// Attack contract demonstrating the exploit
contract VaultDeflationExploit is IERC3156FlashBorrower {
    function onFlashLoan(
        address initiator,
        address token,
        uint256 amount,
        uint256 fee,
        bytes calldata data
    ) external returns (bytes32) {
        IERC4626 ibt = IERC4626(token);
        
        // Step 1: Redeem ALL shares - empties the vault
        uint256 underlying = ibt.redeem(amount, address(this), address(this));
        
        // Step 2: Vault is now empty, share price reset to 1:1
        // Re-mint shares at deflated price
        IERC20(ibt.asset()).approve(address(ibt), type(uint256).max);
        ibt.mint(amount + fee, address(this));
        
        // Step 3: Approve repayment
        ibt.approve(msg.sender, amount + fee);
        
        // Attacker keeps: underlying - (amount + fee) = profit
        return keccak256("ERC3156FlashBorrower.onFlashLoan");
    }
}
```

### Impact Analysis

#### Technical Impact
- **Share Price Reset**: Vault's share price forcibly returned to default value
- **Yield Extraction**: All accumulated yield transferred to attacker
- **State Manipulation**: Vault appears healthy but has lost all growth

#### Financial Impact
- **Yield Loss**: Users lose 100% of accumulated yield
- **Potential Principal Loss**: If users deposited at higher share prices, they may lose principal too
- **Attack Profitability**: `profit = accumulated_yield - flash_loan_fee`

#### Affected Scenarios
- Interest-bearing token vaults with yield accumulation
- Principal token protocols holding IBT reserves
- Any protocol offering flash loans of ERC4626 shares
- Yield aggregators and structured products

### Secure Implementation

**Fix 1: Validate IBT Rate Post-Flash Loan**
```solidity
// ✅ SECURE: Verify share price hasn't decreased after flash loan
function flashLoan(
    IERC3156FlashBorrower _receiver,
    address _token,
    uint256 _amount,
    bytes calldata _data
) external override returns (bool) {
    if (_amount > maxFlashLoan(_token)) revert FlashLoanExceedsMaxAmount();

    uint256 fee = flashFee(_token, _amount);
    _updateFees(fee);

    // Capture IBT rate before flash loan
    uint256 initialIBTRate = IERC4626(ibt).convertToAssets(ibtUnit);

    IERC20(ibt).safeTransfer(address(_receiver), _amount);

    if (_receiver.onFlashLoan(msg.sender, _token, _amount, fee, _data) != ON_FLASH_LOAN)
        revert FlashLoanCallbackFailed();

    IERC20(ibt).safeTransferFrom(address(_receiver), address(this), _amount + fee);

    // Verify rate hasn't decreased - prevents vault deflation
    uint256 postLoanIBTRate = IERC4626(ibt).convertToAssets(ibtUnit);
    if (postLoanIBTRate < initialIBTRate) revert FlashLoanDecreasedIBTRate();

    return true;
}
```

**Fix 2: Limit Flash Loan Amount**
```solidity
// ✅ SECURE: Prevent borrowing amounts that could empty underlying vault
function maxFlashLoan(address _token) public view override returns (uint256) {
    if (_token != ibt) return 0;
    
    uint256 balance = IERC4626(ibt).balanceOf(address(this));
    uint256 totalIBTSupply = IERC4626(ibt).totalSupply();
    
    // Never allow borrowing more than would leave vault with minimum liquidity
    uint256 minVaultReserve = totalIBTSupply / 10; // 10% minimum
    if (balance > minVaultReserve) {
        return balance - minVaultReserve;
    }
    return 0;
}
```

**Fix 3: Dead Shares in Underlying Vault**
```solidity
// ✅ SECURE: IBT vault with permanent dead shares preventing full drain
contract SecureIBTVault is ERC4626 {
    uint256 private constant DEAD_SHARES = 1000;
    
    constructor(IERC20 asset_) ERC4626(asset_) ERC20("Secure IBT", "sIBT") {
        // Mint dead shares on deployment - can never be redeemed
        _mint(address(0xdead), DEAD_SHARES);
        // Deposit corresponding assets
        IERC20(asset_).transferFrom(msg.sender, address(this), DEAD_SHARES);
    }
    
    // Vault can never be fully emptied due to dead shares
    // Share price maintains continuity
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Flash loan of ERC4626 shares without rate validation
- maxFlashLoan returning entire balance
- IBT/yield token vaults without dead shares
- Principal tokens holding majority of IBT supply
- No minimum reserve requirements in flash loans
```

#### Mathematical Conditions for Exploitability
```
attack_profitable = (share_price - 1) * total_shares > flash_loan_fee
where:
  - share_price = current_assets / total_shares
  - flash_loan_fee = borrowed_amount * fee_rate
```

#### Audit Checklist
- [ ] Does the protocol offer flash loans of ERC4626 shares?
- [ ] Can the flash loan drain the entire underlying vault?
- [ ] Is there rate/price validation after flash loan repayment?
- [ ] Does the IBT vault have dead shares or minimum liquidity?
- [ ] Is accumulated yield significant enough to make attack profitable?

### Real-World Context

#### Discovery
- **Protocol**: Spectra (Principal Token)
- **Audit Firm**: Code4rena
- **Date**: 2024
- **Finders**: blutorque, Arabadzhiev, ArmedGoose
- **Severity**: Medium (due to edge case requirements)

#### Prerequisites for Exploitation
1. PrincipalToken holds all/most of IBT supply (uncommon in active markets)
2. IBT vault uses standard share pricing (falls to default when empty)
3. Accumulated yield exceeds flash loan fee (profitable attack)

#### Sponsor Response
> "Having all the IBTs concentrated in our PTs is a very uncommon scenario. In particular, the usefulness of Spectra also relies on markets and if most of the IBTs are in our vaults then that would imply none or few are used as liquidity in the markets."

### Prevention Guidelines

#### Development Best Practices
1. Always validate underlying vault state after flash loan operations
2. Implement rate/price checks before and after flash loan callbacks
3. Use dead shares in ERC4626 vaults to prevent complete drainage
4. Consider minimum reserve requirements for flash loans
5. Document concentration risks in protocol design

#### Testing Requirements
- Test flash loan with entire vault balance
- Verify behavior when underlying vault is fully drained
- Fuzz test with various yield accumulation levels
- Integration tests with actual ERC4626 implementations

#### DeFi Architecture Considerations
```
┌────────────────────────────────────────────────────────────────┐
│                    SAFE ARCHITECTURE                            │
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │ IBT Vault    │     │ PT Contract  │     │ AMM Pool     │   │
│  │ (dead shares)│────▶│ (rate check) │────▶│ (liquidity)  │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
│         │                    │                    │            │
│         │   DISTRIBUTED IBT SUPPLY                │            │
│         └────────────────────┴────────────────────┘            │
│                                                                 │
│  - No single contract holds majority of IBT                    │
│  - Dead shares prevent vault from being emptied                │
│  - Rate validation prevents deflation attacks                  │
└────────────────────────────────────────────────────────────────┘
```

### References

#### Technical Documentation
- [OpenZeppelin ERC4626 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol)
- [EIP-3156: Flash Loans](https://eips.ethereum.org/EIPS/eip-3156)
- [ERC4626 Security Considerations](https://docs.openzeppelin.com/contracts/4.x/erc4626)

#### Security Research
- [OpenZeppelin Issue #3800: ERC4626 Inflation Attack](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3800)
- [Vault Inflation Attack Mitigations](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/3979)
- [ToB Yearn Vault Audit - First Depositor Attack](https://github.com/yearn/yearn-security/blob/master/audits/20210719_ToB_yearn_vaultsv2/)

### Keywords for Search

`flash loan vault deflation`, `ERC4626 flash loan attack`, `share price reset attack`, `yield drain attack`, `IBT vault manipulation`, `principal token exploit`, `vault deflation attack`, `flash loan yield theft`, `ERC4626 share price manipulation`, `empty vault attack`, `accumulated yield extraction`, `flash loan rate validation`, `dead shares protection`, `vault total supply drain`, `convertToAssets manipulation`, `ERC3156 flash loan vulnerability`, `interest bearing token attack`, `yield aggregator exploit`, `share price discontinuity`, `vault price reset`

### Related Vulnerabilities

- [ERC4626 First Depositor Attack](../ERC4626_VAULT_VULNERABILITIES.md#first-depositor-attack)
- [Exchange Rate Manipulation via Direct Transfers](../ERC4626_VAULT_VULNERABILITIES.md#exchange-rate-manipulation)
- [Flash Loan Economic Attacks](../../economic/FLASH_LOAN_ATTACKS.md)

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

`_convertToAssets`, `approve`, `balanceOf`, `borrow`, `borrowing`, `complete`, `deposit`, `economic`, `erc4626`, `erc4626_share_price`, `flashLoan`, `flash_loan`, `flash_loan_vault_deflation`, `ibt`, `ibt_vault`, `maxFlashLoan`, `mint`, `msg.sender`, `onFlashLoan`, `principal_token`, `receive`, `safeTransferFrom`, `share_price_manipulation`, `share_price_reset`, `totalSupply`, `transferFrom`, `vault_deflation`, `yield_extraction`, `yield_theft`
