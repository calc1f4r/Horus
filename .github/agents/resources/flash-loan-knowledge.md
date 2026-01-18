# Flash Loan - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `flash-loan-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Balance Delta Check | ✓ | Pool draining |
| Authorized Repayment | ✓ | Allowance theft |
| Fee Scaling | ✓ | Fee bypass / Loss |
| Solvency Check | ✓ | Insolvent pool |
| Pool Status Check | ✓ | Bypassing pauses |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Wrong Balance Delta Check

**One-liner**: Incorrectly accounting for the principal transfer leads to requiring less repayment than borrowed.

**Quick Checks:**
- [ ] Is `balanceBefore` snapshot taken BEFORE or AFTER the transfer?
- [ ] If BEFORE: `final >= initial + fee`
- [ ] If AFTER: `final >= initial + amount + fee`
- [ ] Does it use `transferFrom` (Pull) or assume `transfer` (Push)?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Wrong accounting
uint256 balBefore = token.balanceOf(this);
token.transfer(receiver, amount);
// ... callback ...
// ERROR: Should ensure balAfter >= balBefore + fee
// But if logic expects balAfter >= balBefore, we lost the principal!
require(token.balanceOf(this) >= balBefore + fee, "repay failed");
```

**Reasoning Prompt:**
> "If I borrow 100 and pay back 1, does the logic pass?"

---

### ⚠️ Category 2: Arbitrary Receiver / Allowance Theft

**One-liner**: Attacker initiates flash loan specifying a victim's address as receiver, forcing them to pay back the loan using their allowance.

**Quick Checks:**
- [ ] Can `msg.sender` specify `receiver`?
- [ ] Does repayment happen via `transferFrom(receiver, ...)`?
- [ ] Is there a check `receiver == msg.sender` or `allowance(receiver, msg.sender)`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Unchecked receiver
function flashLoan(address receiver, uint256 amount) {
    // ... callback ...
    // Force receiver to pay
    token.transferFrom(receiver, address(this), amount + fee); 
}
```

**Reasoning Prompt:**
> "Can I force the Whale who approved this protocol to pay my debt?"

---

### ⚠️ Category 3: Free Flash Loans (Zero Interest)

**One-liner**: Time-based interest models calculate 0 interest when `timeElapsed == 0` (same block).

**Quick Checks:**
- [ ] Is the fee strictly defined as `amount * feeRate`?
- [ ] Or is it `amount * rate * timeDelta`?
- [ ] Is there a minimum fee floor?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Zero-time interest
uint256 time = block.timestamp - lastUpdate; // 0 in same tx
uint256 interest = principal * rate * time; // 0
```

---

### ⚠️ Category 4: Anti-Flashloan Bypass

**One-liner**: Guards that prevent "deposit and withdraw in same block" often miss edge cases like liquidation or transfer.

**Quick Checks:**
- [ ] Does `deposit` set `lastBlock[user] = block.number`?
- [ ] Does `withdraw` check `lastBlock[user] != block.number`?
- [ ] Do `liquidate`, `transfer`, `transferFrom` ALSO check/set this?
- [ ] Is the guard explicitly based on `tx.origin`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Incomplete Guard
modifier antiFlash {
    require(lastDeposit[tx.origin] < block.number, "flash");
    _;
}
// Bypass: Use 2 separate contracts/EOAs
```

---

### ⚠️ Category 5: ERC-3156 Non-Compliance

**One-liner**: Implementing the interface but failing to enforce the "Lender Pulls" pattern.

**Quick Checks:**
- [ ] Does the `flashLoan` function call `transferFrom` at the end?
- [ ] Or does it expect the receiver to transfer back manually?
- [ ] If manual, how is the correct amount verified?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Flash Loan Flow
function flashLoan(IERC3156FlashBorrower receiver, address token, uint256 amount, bytes calldata data) external override returns (bool) {
    require(supportedTokens[token], "Token not supported");
    
    uint256 fee = flashFee(token, amount);
    uint256 balanceBefore = IERC20(token).balanceOf(address(this));
    
    // 1. Transfer to receiver
    IERC20(token).safeTransfer(address(receiver), amount);
    
    // 2. Callback
    require(
        receiver.onFlashLoan(msg.sender, token, amount, fee, data) == CALLBACK_SUCCESS,
        "Callback failed"
    );
    
    // 3. Pull repayment + fee (The Standard Way)
    uint256 repayment = amount + fee;
    IERC20(token).safeTransferFrom(address(receiver), address(this), repayment);
    
    // 4. Final verification (Redundant but safe)
    uint256 balanceAfter = IERC20(token).balanceOf(address(this));
    require(balanceAfter >= balanceBefore + fee, "Solvency check");
    
    return true;
}
```

## Keywords for Code Search

```bash
# Core logic
rg -n "flashLoan|flashFee|onFlashLoan|executeOperation"

# Balance checks
rg -n "balanceBefore|balanceOf.*this"

# Repayment
rg -n "transferFrom|allowance"

# Safeguards
rg -n "tx\.origin|block\.number|same block"
```

---

## References

- Use the [Flash Loan Agent](../flash-loan-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/flash-loan-attacks/`
