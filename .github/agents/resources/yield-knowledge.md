# Yield Strategy - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `yield-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures extracted from the full database.

---

## Core Invariants to Verify

| Invariant | Formula | Attack If Violated |
|-----------|---------|-------------------|
| Share Price | `totalAssets / totalSupply` | First depositor inflation |
| Reward Accumulator | `rewardPerToken += Δtime * rate / supply` | Reward theft via stale state |
| Balance Sync | `sum(balances) == totalSupply` | Accounting desync |
| Claim Limit | `claimed[user] <= earned[user]` | Over-claim via merge |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: First Depositor / Inflation Attacks

**One-liner**: First depositor manipulates share price by donating to vault after minimal deposit.

**Quick Checks:**
- [ ] Is there a virtual shares/assets offset?
- [ ] Is MINIMUM_DEPOSIT enforced for first deposit?
- [ ] Are dead shares burned to address(0xdead)?
- [ ] Can vault reach zero supply state after initialization?

**Exploit Signature:**
```
totalSupply = 1 + totalAssets >> 1e18 = share price explosion
deposit rounds to 0 shares
```

**Reasoning Prompt:**
> "If I'm the first depositor and donate tokens directly, can I make subsequent deposits round to zero?"

---

### ⚠️ Category 2: Exchange Rate Manipulation via Donation

**One-liner**: Direct token transfers to vault inflate exchange rate, affecting vesting/claims.

**Quick Checks:**
- [ ] Does `totalAssets()` use `balanceOf()` or internal tracking?
- [ ] Can privileged users call donate() functions?
- [ ] Are critical calculations based on current exchange rate?

**Exploit Signature:**
```solidity
function totalAssets() returns (token.balanceOf(this));  // ❌ Manipulatable
```

**Reasoning Prompt:**
> "If someone donates tokens directly to the vault, what calculations break?"

---

### ⚠️ Category 3: Reward Distribution Edge Cases

**One-liner**: First staker gets all historical rewards when no one was staking.

**Quick Checks:**
- [ ] What happens when `totalSupply == 0` during reward period?
- [ ] Is `lastUpdateTime` updated even with zero stakers?
- [ ] Can reward period start before any deposits?

**Exploit Signature:**
```solidity
if (totalSupply == 0) return;  // ❌ lastUpdateTime stays stale!
```

**Reasoning Prompt:**
> "If rewards accrue for 7 days with no stakers, who gets them when I stake?"

---

### ⚠️ Category 4: Stale Reward Accumulator

**One-liner**: Balance changes before reward update cause incorrect reward distribution.

**Quick Checks:**
- [ ] Is `_updateReward()` called BEFORE every `_mint()` and `_burn()`?
- [ ] Is there an `updateReward(address)` modifier on stake/unstake?
- [ ] Any code path skipping the accumulator update?

**Exploit Signature:**
```solidity
function stake(uint256 amount) external {
    balances[msg.sender] += amount;  // ❌ Balance first
    _updateRewards();                 // ❌ Update second = wrong rewards
}
```

**Reasoning Prompt:**
> "Are rewards calculated BEFORE or AFTER my balance changes?"

---

### ⚠️ Category 5: Flash Loan LP Fee Extraction

**One-liner**: Same-block deposit/withdraw extracts fees without genuine liquidity provision.

**Quick Checks:**
- [ ] Can users deposit and withdraw in the same block?
- [ ] Is there a minimum lock period?
- [ ] Can flash loan front-run legitimate deposits?

**Exploit Signature:**
```
Block N: flashLoan → deposit → [victim tx generates fees] → withdraw → repay
```

**Reasoning Prompt:**
> "If I deposit and withdraw atomically, can I extract any yield?"

---

### ⚠️ Category 6: Cross-Function Reentrancy

**One-liner**: Token hooks allow state modification during transfer execution.

**Quick Checks:**
- [ ] Do `_beforeTokenTransfer` or `_afterTokenTransfer` make external calls?
- [ ] Can pods/delegates be modified during transfer iteration?
- [ ] Is there reentrancy protection on hooks?

**Exploit Signature:**
```solidity
function _beforeTokenTransfer(...) {
    for (pod in pods[from]) {
        pod.updateBalance();  // ❌ External call during iteration
    }
}
```

**Reasoning Prompt:**
> "If the token has a callback during transfer, can I modify state mid-execution?"

---

### ⚠️ Category 7: Read-Only Reentrancy

**One-liner**: Oracle reads stale data during Balancer/Curve pool operations.

**Quick Checks:**
- [ ] Does the protocol read prices from Balancer or Curve pools?
- [ ] Is `VaultReentrancyLib.ensureNotInVaultContext()` used?
- [ ] Can BPT supply update before token balances sync?

**Exploit Signature:**
```solidity
function getPrice() view returns (balances / totalSupply);  // ❌ No reentrancy check
```

**Reasoning Prompt:**
> "If I call joinPool with ETH, can I trigger a liquidation mid-operation?"

---

### ⚠️ Category 8: Partial Withdrawal Token Freeze

**One-liner**: Provider partial withdrawals leave unused shares stuck in contract.

**Quick Checks:**
- [ ] Do Yearn/Aave withdrawals handle partial returns?
- [ ] Are unused yTokens/aTokens returned to user?
- [ ] Is there a recovery mechanism for stuck tokens?

**Exploit Signature:**
```solidity
function withdraw(amount) {
    yToken.transferFrom(user, address(this), amount);
    yToken.withdraw(amount);  // Only partial amount withdrawn
    // ❌ Remaining yTokens stuck in contract!
}
```

**Reasoning Prompt:**
> "If the underlying vault can only partially fulfill my withdrawal, where do the remaining shares go?"

---

### ⚠️ Category 9: Reward Multiplication via Merge

**One-liner**: Merging claimed positions into unclaimed ones multiplies claimable rewards.

**Quick Checks:**
- [ ] Can staking positions/NFTs be merged?
- [ ] Are claimed rewards tracked per position?
- [ ] Does merge consolidate claim history properly?

**Exploit Signature:**
```
claim(token1) → merge(token1 → token2) → claim(token2)  // ❌ Double reward
```

**Reasoning Prompt:**
> "If I merge a claimed position into an unclaimed one, do I get to claim again?"

---

### ⚠️ Category 10: State Machine Hijacking

**One-liner**: Non-owners can take over positions in certain states.

**Quick Checks:**
- [ ] Can positions be re-created by non-original-owners?
- [ ] Are state transitions access-controlled?
- [ ] Can Withdrawable/Error states transition back to Initial?

**Exploit Signature:**
```solidity
function createPosition(nodeId) {
    if (exists(nodeId)) {
        requireValidTransition(status);  // ❌ No owner check!
        setOwner(msg.sender);            // ❌ Hijacked!
    }
}
```

**Reasoning Prompt:**
> "If a position completes, can someone else claim it by re-initializing?"

---

### ⚠️ Category 11: Penalty/Fee Bypass via Secondary Market

**One-liner**: Transfer staked tokens to avoid unstaking penalties.

**Quick Checks:**
- [ ] Are `transfer()` and `transferFrom()` overridden?
- [ ] Do penalties apply on secondary market sales?
- [ ] Is reward boost reset on transfer?

**Exploit Signature:**
```solidity
// ❌ Standard ERC20 transfer bypasses unstake penalty
function unstake() { applyPenalty(); }
function transfer() { /* no penalty */ }
```

**Reasoning Prompt:**
> "Instead of unstaking with penalty, can I just sell my staked tokens?"

---

### ⚠️ Category 12: Claim Function Arithmetic Underflow

**One-liner**: Claims revert after period ends due to time calculation underflow.

**Quick Checks:**
- [ ] Is there protection when `lastUpdateTime > periodFinish`?
- [ ] Can `min(block.timestamp, periodFinish) - lastUpdateTime` underflow?
- [ ] Does first post-period claim break subsequent claims?

**Exploit Signature:**
```solidity
uint256 elapsed = min(now, periodFinish) - lastUpdateTime;  // ❌ Underflows if lastUpdateTime > periodFinish
```

**Reasoning Prompt:**
> "After the reward period ends, can everyone still claim their rewards?"

---

### ⚠️ Category 13: Missing Slippage in Yield Operations

**One-liner**: Harvest/compound swaps with zero slippage are sandwiched.

**Quick Checks:**
- [ ] Is `amountOutMin` enforced on harvest swaps?
- [ ] Are there hardcoded `0` minimums?
- [ ] Is oracle-based slippage protection used?

**Exploit Signature:**
```solidity
router.swap(rewards, 0, path);  // ❌ Zero minimum output
```

**Reasoning Prompt:**
> "When the vault harvests and swaps rewards, can MEV bots sandwich it?"

---

### ⚠️ Category 18: Same-Block Deposit/Withdraw Arbitrage

**One-liner**: Deposit before yield accrual, withdraw after, same block.

**Quick Checks:**
- [ ] Is there a minimum holding period?
- [ ] Is `lastActionBlock` tracked per user?
- [ ] Can flash loans exploit yield timing?

**Exploit Signature:**
```
Block N: deposit → triggerYield → withdraw (all atomic)
```

**Reasoning Prompt:**
> "Can I deposit, trigger a yield event, and withdraw in the same block?"

---

### ⚠️ Category 24: Vote Manipulation via Duplicate Pools

**One-liner**: Voting for same pool multiple times inflates voting power.

**Quick Checks:**
- [ ] Does vote function check for duplicate pool entries?
- [ ] Is totalWeight correctly decremented on reset?
- [ ] Can phantom votes accumulate over reset cycles?

**Exploit Signature:**
```solidity
vote([gaugeA, gaugeA], [10 ether, 1 wei]);  // ❌ No duplicate check
// totalWeight += 10 ether + 1 wei
// votes[user][gaugeA] = 1 wei (only last stored)
// reset() only decrements 1 wei
```

**Reasoning Prompt:**
> "If I vote for the same pool twice, what happens to my total voting power?"

---

### ⚠️ Category 25: Vesting Interface Spoofing

**One-liner**: Attacker deploys fake DAO contract to claim all vested tokens.

**Quick Checks:**
- [ ] Does claim function accept arbitrary DAO addresses?
- [ ] Are DAO contracts whitelisted?
- [ ] Is interface data (token, amounts) validated?

**Exploit Signature:**
```solidity
function claim(address dao) {
    IDaosLive(dao).token();  // ❌ Attacker's fake contract
    IDaosLive(dao).getAmount();  // Returns vault's entire balance
}
```

**Reasoning Prompt:**
> "If I deploy a contract implementing the expected interface, can I drain the vesting contract?"

---

## Summary Attack Surface Matrix

| Target | Flash Loan | Front-Run | Donation | Reentrancy |
|--------|:----------:|:---------:|:--------:|:----------:|
| First Deposit | ⚠️ | ⚠️ | ⚠️ | - |
| Reward Claim | - | ⚠️ | - | ⚠️ |
| Vault Deposit | ⚠️ | ⚠️ | ⚠️ | - |
| Strategy Harvest | ⚠️ | ⚠️ | - | - |
| Position Merge | - | - | - | ⚠️ |
| Voting | ⚠️ | ⚠️ | - | - |
| Vesting Claim | - | - | - | ⚠️ |

---

## Keywords for Code Search

When reasoning suggests an area to investigate, search for:

```bash
# First depositor patterns
rg -n "totalSupply\s*==\s*0|convertToShares|_decimalsOffset|MINIMUM"

# Reward accumulator patterns
rg -n "rewardPerToken|lastUpdateTime|_updateReward|earned\("

# Flash loan / timing patterns
rg -n "lastActionBlock|depositTimestamp|MIN_LOCK|sameBlock"

# Reentrancy patterns
rg -n "_beforeTokenTransfer|_afterTokenTransfer|nonReentrant"

# Provider integration
rg -n "yToken|aToken|withdraw.*transferFrom|provider"

# Vesting patterns
rg -n "vesting|claim\(.*address|IDaos|getContribution"

# Merge patterns
rg -n "merge\(|combine\(|claimedRewards\[|claimableFlux"
```

---

## References

- Full Database: [yield-strategy-vulnerabilities.md](../../DB/general/yield-strategy-vulnerabilities/yield-strategy-vulnerabilities.md)
- Main Agent: [yield-reasoning-agent.md](../yield-reasoning-agent.md)
- Context Builder: [audit-context-building.md](../audit-context-building.md)
- ERC4626 Patterns: [DB/tokens/erc4626/](../../DB/tokens/erc4626/)
