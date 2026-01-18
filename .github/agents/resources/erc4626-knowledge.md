# ERC4626 - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `erc4626-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Inflation Protection | ✓ | First Depositor Theft |
| Rounding Direction | ✓ | Vault Drainage |
| Preview Consistency | ✓ | Integration Failure / Theft |
| Max Limits | ✓ | DOS / Forced Revert |
| TotalAssets Integrity | ✓ | Share Price Manipulation |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: First Depositor / Inflation Attack

**One-liner**: Attacker mints 1 share, donates huge assets, making 1 share worth more than next user's deposit (causing it to round to 0).

**Quick Checks:**
- [ ] Is `decimalOffset` used? (Virtual shares)
- [ ] Or are dead shares minted to `address(0)`?
- [ ] Or is there a minimum deposit constant?
- [ ] Does `totalAssets` use `balanceOf(this)`? (Easier to attack)

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Naive share calculation
function convertToShares(uint256 assets) public view returns (uint256) {
    return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
}
```

**Reasoning Prompt:**
> "If supply is 0, I deposit 1 wei. Then I donate 100k USDC. Next user deposits 100 USDC. Do they get 0 shares?"

---

### ⚠️ Category 2: Rounding Direction Errors

**One-liner**: Implementations often default to rounding down, but Mint/Withdraw must round UP to favor the vault.

**Quick Checks:**
- [ ] `previewMint` (Shares -> Assets): Round **UP**?
- [ ] `previewWithdraw` (Assets -> Shares): Round **UP**?
- [ ] `previewRedeem` (Shares -> Assets): Round **DOWN**?
- [ ] `previewDeposit` (Assets -> Shares): Round **DOWN**?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: previewWithdraw rounding down
function previewWithdraw(uint256 assets) public view returns (uint256) {
    // Should be mulDivUp
    return assets.mulDivDown(totalSupply(), totalAssets());
}
```

---

### ⚠️ Category 3: Fee Inconsistency

**One-liner**: Fees taken in `deposit` but not shown in `previewDeposit`, or calculated differently.

**Quick Checks:**
- [ ] Compare `previewDeposit` code vs `deposit` code.
- [ ] Is fee calculated on Gross (input) or Net (after fee)?
- [ ] Does `previewMint` include the fee burden in the assets returned?

---

### ⚠️ Category 4: Compliance / Max Limits

**One-liner**: `maxDeposit` returns `uint256.max` even when the vault is paused.

**Quick Checks:**
- [ ] `maxDeposit`: Check `paused()` state?
- [ ] `maxMint`: Check global supply caps?
- [ ] `maxWithdraw`: Check user balance?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Lying about limits
function maxDeposit(address) external pure returns (uint256) {
    return type(uint256).max; // Even if paused!
}
```

---

## Secure Implementation Pattern (OpenZeppelin 4.9+)

```solidity
// ✅ SECURE: Virtual Shares
function _convertToShares(uint256 assets, Math.Rounding rounding) internal view virtual returns (uint256) {
    return assets.mulDiv(
        totalSupply() + 10 ** _decimalsOffset(), // Virtual Supply
        totalAssets() + 1,                        // Virtual Assets
        rounding
    );
}

function _decimalsOffset() internal view virtual override returns (uint8) {
    return 9; // Offset for safety
}
```

## Keywords for Code Search

```bash
# Core logic
rg -n "convertToShares|convertToAssets|previewDeposit|totalAssets"

# Rounding
rg -n "mulDivDown|mulDivUp|rounding"

# Limits
rg -n "maxDeposit|maxMint|maxWithdraw"

# Inflation checks
rg -n "totalSupply\(\) == 0|min_liquidity|dead shares"
```

---

## References

- Use the [ERC4626 Agent](../erc4626-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/tokens/erc4626/`
