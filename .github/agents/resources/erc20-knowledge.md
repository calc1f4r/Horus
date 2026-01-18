# ERC20 Integration - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `erc20-integration-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Balance Difference | ✓ | Insolvency via FoT/Deflation |
| SafeERC20 | ✓ | Revert on USDT / Silent Fail |
| Dynamic Decimals | ✓ | Calculation Errors |
| Atomic Approval | ✓ | Double Spend |
| Rebase Handling | ✓ | Stuck Funds / Accounting Drift |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Fee-on-Transfer Checks

**One-liner**: If the protocol accepts *Any* ERC20, it MUST measure actual received balance, otherwise users can credit themselves more than they deposit.

**Quick Checks:**
- [ ] Code uses `amount` param for `balance +=`?
- [ ] Code does NOT check `balanceOf(this) - oldBalance`?
- [ ] No whitelist mechanism?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: FoT Incompatibility
token.transferFrom(msg.sender, address(this), amount);
// If token takes fee, contract has < amount
balances[msg.sender] += amount; // User credited for Phantom tokens
```

---

### ⚠️ Category 2: USDT & Return Values

**One-liner**: USDT on Mainnet does NOT return a boolean for transfer. Standard `IERC20` interface expects a bool, so calls will REVERT.

**Quick Checks:**
- [ ] Direct `token.transfer` usage without `SafeERC20`?
- [ ] Interface definition: `function transfer(...) external returns (bool);`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: USDT Compatibility
interface IERC20 { function transfer(address, uint) external returns (bool); }
// Calling this on USDT will REVERT because USDT returns `void`
IERC20(usdt).transfer(to, amt);
```

---

### ⚠️ Category 3: Approval Race Condition

**One-liner**: Changing approval from N to M allows a front-runner to spend N + M.

**Quick Checks:**
- [ ] `approve(spender, value)` called where `value > 0`?
- [ ] No `approve(0)` call or check overlapping?

---

### ⚠️ Category 4: Hardcoded Decimals

**One-liner**: Assuming 18 decimals breaks USDC (6) and WBTC (8).

**Quick Checks:**
- [ ] `amount * 1e18` or `1e12` hardcoded scaling?
- [ ] Division by `1e18`?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Handling FoT and Weird Returns
using SafeERC20 for IERC20;

function deposit(uint256 amount) external {
    uint256 balBefore = token.balanceOf(address(this));
    token.safeTransferFrom(msg.sender, address(this), amount);
    uint256 balAfter = token.balanceOf(address(this));
    
    // Truth is what we received
    uint256 actual = balAfter - balBefore;
    require(actual > 0, "No tokens");
    
    balances[msg.sender] += actual;
}
```

## Keywords for Code Search

```bash
# FoT Vulnerability
grep -n "balance.*+=" . -r # manual check context

# Unsafe Transfers
grep -n ".transfer(" . -r | grep -v "safe"

# Decimals
grep -n "18" . -r | grep "decimal"

# Approvals
grep -n "approve" . -r
```

---

## References

- Use the [ERC20 Agent](../erc20-integration-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/tokens/erc20/`
