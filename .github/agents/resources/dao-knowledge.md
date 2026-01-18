# DAO Governance - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `dao-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Past Block Snapshot | ✓ | Flash loan voting |
| Voting Delay | ✓ | Proposal spam / flash attacks |
| Delegation Cleanup | ✓ | Double voting |
| Timelock Delay | ✓ | Admin abuse / takeover |
| 51% Attack Guard | ✓ | Protocol looting |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Double Voting / Vote Multiplication

**One-liner**: Users can vote multiple times with the same tokens via delegation abuse or transfer loopholes.

**Quick Checks:**
- [ ] Does `delegate(new)` subtract votes from `delegate(old)`?
- [ ] Are checkpoints updated correctly during `transfer`?
- [ ] Can a user vote, withdraw, transfer, and vote again?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Delegation overwrite without cleanup
function delegate(address delegatee) {
    // Missing: removeVotingPower(delegates[msg.sender]);
    delegates[msg.sender] = delegatee;
    addVotingPower(delegatee, balance);
}
```

**Reasoning Prompt:**
> "If I delegate to Alice, then delegate to Bob, does Alice lose my votes?"

---

### ⚠️ Category 2: Flash Loan Voting

**One-liner**: Attacker borrows tokens, votes, and repays in one transaction to manipulate governance.

**Quick Checks:**
- [ ] Is `getVotes` using a snapshot from `block.number - 1` or earlier?
- [ ] Is there a `votingDelay` between proposal and voting start?
- [ ] Does `propose()` also require past-block threshold?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Uses current balance or current block
function getVotes(address account) view returns (uint256) {
    return balanceOf(account); // Flash loanable!
}
// OR
snapshot = block.number; // Flash loanable in same block!
```

**Reasoning Prompt:**
> "Can I borrow 1M tokens, propose/vote, and repay all in one transaction?"

---

### ⚠️ Category 3: Timelock Bypass

**One-liner**: Admin or Proposer can bypass the execution delay, negating the purpose of the Timelock.

**Quick Checks:**
- [ ] Is `minDelay` enforced?
- [ ] Can `execute` be called without queuing?
- [ ] Does the definition of `admin` allow instant execution?
- [ ] Are `cancel` permissions robust?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Admin bypass
if (msg.sender == admin) {
    target.call(data); // Bypass delay!
    return;
}
```

**Reasoning Prompt:**
> "If the admin key is compromised, can they drain the treasury instantly?"

---

### ⚠️ Category 4: Quorum Manipulation

**One-liner**: Quorum calculation is flawed, allowing proposals to pass with insufficient support.

**Quick Checks:**
- [ ] Is quorum a fixed number or percentage?
- [ ] If percentage, does it account for `totalSupply` changes (mint/burn)?
- [ ] Do `abstain` votes count towards quorum?

**Reasoning Prompt:**
> "If I burn half the supply, does the quorum requirement drop immediately?"

---

### ⚠️ Category 5: Proposal Lifecycle Griefing

**One-liner**: Attacker cancels legitimate proposals or spams proposals to DOS the system.

**Quick Checks:**
- [ ] Who has the right to `cancel(proposalId)`?
- [ ] Is the `proposalThreshold` high enough to prevent spam?
- [ ] Does `state()` transition correctly (e.g., Canceled -> Defeated)?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Unrestricted cancellation
function cancel(uint256 proposalId) external {
    state[proposalId] = Canceled; // Anyone can cancel!
}
```

---

## Secure Delegation Pattern

```solidity
// ✅ SECURE: Move voting power atomicaly
function _moveVotingPower(
    address src,
    address dst,
    uint256 amount
) internal {
    if (src != address(0) && src != dst) {
        uint256 srcOld = _checkpoints[src][high].votes;
        uint256 srcNew = srcOld - amount;
        _writeCheckpoint(src, srcNew);
    }
    if (dst != address(0) && src != dst) {
        uint256 dstOld = _checkpoints[dst][high].votes;
        uint256 dstNew = dstOld + amount;
        _writeCheckpoint(dst, dstNew);
    }
}
```

## Keywords for Code Search

```bash
# Voting power
rg -n "getVotes|getPastVotes|delegat|checkpoints"

# Timelock
rg -n "Timelock|queue|execute|minDelay|delay"

# Governance
rg -n "propose|cancel|state|quorum|threshold"

# Vulnerable patterns
rg -n "block\.number|balanceOf" # Look for non-snapshot usage in voters
```

---

## References

- Use the [DAO Governance Agent](../dao-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/dao-governance-vulnerabilities/`
