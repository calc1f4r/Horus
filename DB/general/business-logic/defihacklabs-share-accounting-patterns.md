---
protocol: generic
chain: ethereum, bsc
category: business_logic
vulnerability_type: share_fee_accounting_error

# Pattern Identity (Required)
root_cause_family: stale_accounting
pattern_key: share_fee_accounting_error | share_accounting | accounting_manipulation | fund_loss

# Interaction Scope
interaction_scope: single_contract

attack_type: accounting_manipulation
affected_component: share_accounting, fee_distribution, balance_tracking

primitives:
  - fee_not_reset_on_transfer
  - emergency_withdraw_no_burn
  - deposit_withdraw_mismatch
  - donation_inflated_balance
  - self_transfer_duplication
  - stale_accumulator

severity: critical
impact: fund_loss
exploitability: 0.8
financial_impact: critical

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "from"
  - "amount"
  - "deposit"
  - "exploit"
  - "mintFor"
  - "pending"
  - "withdraw"
  - "_transfer"
  - "balanceOf"
  - "collectFees"
  - "totalShares"
  - "userFeeDebt"
  - "claimRewards"
  - "transferFrom"
  - "emergencyBurn"
path_keys:
  - "bearn_finance"
  - "bzx_itoken"
  - "cover_protocol"
  - "eleven_finance"
  - "pancakehunny"

tags:
  - share_accounting
  - fee_distribution
  - reward_accumulator
  - balance_duplication
  - deposit_mismatch
  - emergency_withdraw
  - self_transfer
  - donation
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 6
total_losses: "$35M+"
---

## DeFiHackLabs Share & Fee Accounting Errors Compendium


## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [BEARN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-05/bEarn_exp.sol` |
| [BZX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2020-09/bZx_exp.sol` |
| [COVER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2020-12/Cover_exp.sol` |
| [ELEVEN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-06/Eleven_exp.sol` |
| [PANCAKEHUNNY-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-10/PancakeHunny_exp.sol` |
| [POPSICLE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-08/Popsicle_exp.sol` |

---

### Overview

Share and fee accounting errors occur when protocols incorrectly track ownership, rewards, or balances during transfers, withdrawals, or state transitions. This entry catalogs **6 real-world exploits** from 2020-2021 totaling **$35M+ in losses**. The core patterns: fee accumulators not reset on LP transfer, emergency withdraw bypassing share burns, deposit/withdraw accounting asymmetry, and self-transfer balance duplication.


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `stale_accounting` |
| Pattern Key | `share_fee_accounting_error | share_accounting | accounting_manipulation | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, bsc |


### Root Cause Categories

1. **Fee Not Reset on Transfer** — LP tokens carry accumulated fee rights that aren't reset when transferred
2. **Emergency Withdraw Doesn't Burn Shares** — User can withdraw funds but keep their LP/share tokens
3. **Deposit/Withdraw Accounting Mismatch** — Different pools used for deposit vs. withdrawal calculation
4. **Donation-Inflated balanceOf() for Minting** — Protocol uses `balanceOf()` to determine mint amount
5. **Stale Reward Accumulator** — Reward calculation uses cached/stale multiplier after state change
6. **Self-Transfer Balance Duplication** — Token implementation allows `from == to` transfer to increase balance

---

### Vulnerable Pattern Examples

#### Category 1: Fee Not Reset on Transfer [CRITICAL]

> **pathShape**: `atomic`

**Example 1: Popsicle Finance — Fee Replay Across Transfers ($20M, 2021-08)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Sorbetto Fragola (concentrated liquidity optimizer)
// Fee rewards are calculated per-LP-token but NOT reset when LP tokens transfer

contract SorbettoFragola {
    mapping(address => uint256) public userFeeDebt0;
    mapping(address => uint256) public userFeeDebt1;

    // @audit collectFees() distributes accrued trading fees to LP holders
    function collectFees(uint256 tokenId) external {
        uint256 owed0 = _computeFeesOwed0(msg.sender);
        uint256 owed1 = _computeFeesOwed1(msg.sender);

        // Pay fees
        token0.transfer(msg.sender, owed0);
        token1.transfer(msg.sender, owed1);

        // Update debt
        userFeeDebt0[msg.sender] = feeGrowthGlobal0;
        userFeeDebt1[msg.sender] = feeGrowthGlobal1;
    }

    // @audit CRITICAL: _transfer does NOT reset fee debt for recipient
    function _transfer(address from, address to, uint256 amount) internal override {
        super._transfer(from, to, amount);
        // @audit MISSING: userFeeDebt0[to] = feeGrowthGlobal0;
        // @audit MISSING: userFeeDebt1[to] = feeGrowthGlobal1;
        // New holder inherits ZERO debt → claims ALL accumulated fees
    }
}

// Attack:
// 1. Alice holds 1000 LP, accumulates 10 ETH in fees
// 2. Alice collects 10 ETH fees → debt updated
// 3. Alice transfers 1000 LP to Bob (attacker)
// 4. Bob's fee debt = 0 → Bob collects 10 ETH fees AGAIN
// 5. Bob transfers to Carol (attacker) → Carol collects AGAIN
// Repeat N times: drain ALL accumulated fees

contract PopsicleExploit {
    address[] recipients;

    function exploit() external {
        // Step 1: Flash loan → deposit to get LP tokens
        sorbetto.deposit(amount);

        // Step 2: Transfer LP between attacker addresses, collecting at each step
        for (uint i = 0; i < recipients.length; i++) {
            sorbetto.transfer(recipients[i], sorbetto.balanceOf(address(this)));
            address(recipients[i]).call(
                abi.encodeWithSignature("collectFees()")
            );
            // @audit Each recipient collects the SAME fees — unlimited replay
        }
    }
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-08/Popsicle_exp.sol`
- **Root Cause**: LP token `_transfer()` did not reset `userFeeDebt` for the recipient. Each new holder could claim all accumulated protocol fees since inception, creating unlimited fee replay.

---

#### Category 2: Emergency Withdraw Doesn't Burn Shares [HIGH]

> **pathShape**: `atomic`

**Example 2: Eleven Finance — emergencyBurn Without Share Burn ($4.5M, 2021-06)** [HIGH]
```solidity
// ❌ VULNERABLE: emergencyBurn() withdraws funds but doesn't burn user's vault shares

contract ElevenVault {
    mapping(address => uint256) public shares;

    function deposit(uint256 amount) external {
        uint256 sharesMinted = amount * totalShares / totalBalance;
        shares[msg.sender] += sharesMinted;
        totalShares += sharesMinted;
        token.transferFrom(msg.sender, address(this), amount);
    }

    function emergencyBurn() external {
        // @audit Withdraws proportional tokens to user
        uint256 userShare = shares[msg.sender];
        uint256 amount = userShare * totalBalance / totalShares;
        token.transfer(msg.sender, amount);

        // @audit MISSING: shares[msg.sender] = 0;
        // @audit MISSING: totalShares -= userShare;
        // User keeps their shares! Can call again!
    }
}

// Attack:
// 1. Deposit tokens → receive shares
// 2. Call emergencyBurn() → receive tokens back BUT keep shares
// 3. Call emergencyBurn() again → receive tokens AGAIN (other users' deposits)
// 4. Repeat until vault is drained
```
- **PoC**: `DeFiHackLabs/src/test/2021-06/Eleven_exp.sol`
- **Root Cause**: `emergencyBurn()` returned funds to the user proportional to their shares but never decremented `shares[msg.sender]` or `totalShares`. Repeated calls drained the entire vault.

---

#### Category 3: Deposit/Withdraw Accounting Mismatch [CRITICAL]

> **pathShape**: `atomic`

**Example 3: bEarn Finance — Cross-Strategy Balance Error ($11M, 2021-05)** [CRITICAL]
```solidity
// ❌ VULNERABLE: deposit() and withdraw() reference DIFFERENT underlying balances
// bEarn vault routes deposits to Strategy A but withdraws from Strategy B

contract bEarnVault {
    IStrategy public strategyA;  // Active strategy
    IStrategy public strategyB;  // Old strategy (still has funds)

    function deposit(uint256 amount) external {
        // @audit Uses strategyA.balanceOf() to calculate shares
        uint256 poolBal = strategyA.balanceOf();
        uint256 shares = totalSupply == 0 ? amount : amount * totalSupply / poolBal;
        _mint(msg.sender, shares);
        token.transferFrom(msg.sender, address(strategyA), amount);
    }

    function withdraw(uint256 shares) external {
        // @audit Uses strategyB.balanceOf() to calculate withdrawal!
        uint256 poolBal = strategyB.balanceOf(); // @audit DIFFERENT strategy!
        uint256 amount = shares * poolBal / totalSupply;
        _burn(msg.sender, shares);
        strategyB.withdraw(amount);
        token.transfer(msg.sender, amount);
    }
}

// Attack: If strategyB has more funds than strategyA:
// 1. Deposit small amount → calculate shares against strategyA (small base)
// 2. Receive many shares relative to deposit
// 3. Withdraw → calculate amount against strategyB (large base)
// 4. Receive more tokens than deposited
// Net: Arbitrage between the two strategies' balance discrepancy
```
- **PoC**: `DeFiHackLabs/src/test/2021-05/bEarn_exp.sol`
- **Root Cause**: The vault's `deposit()` and `withdraw()` functions referenced different strategies for balance calculation. When strategy balances diverged, attackers could exploit the accounting asymmetry to extract excess funds.

---

#### Category 4: Donation-Inflated balanceOf() for Minting [HIGH]

> **pathShape**: `atomic`

**Example 4: PancakeHunny — Inflated balanceOf() Mints Excess Tokens ($2.2M, 2021-10)** [HIGH]
```solidity
// ❌ VULNERABLE: Mint calculation uses balanceOf(this) which can be inflated via donation

contract HunnyMinter {
    function mintFor(address recipient) external {
        // @audit Uses current balance to determine mint amount
        uint256 balance = IERC20(hunnyBNBLP).balanceOf(address(this));
        uint256 toMint = balance * rewardRate / PRECISION;
        // @audit balance inflated by direct transfer (donation)
        HUNNY.mint(recipient, toMint);
    }
}

// Attack:
// 1. Flash loan large amount of HUNNY-BNB LP
// 2. Transfer LP tokens directly to HunnyMinter contract (donation)
//    hunnyBNBLP.transfer(address(minter), flashLoanedAmount);
// 3. Call mintFor(attacker) → mints HUNNY based on inflated balance
// 4. Sell excess HUNNY → repay flash loan → profit
```
- **PoC**: `DeFiHackLabs/src/test/2021-10/PancakeHunny_exp.sol`
- **Root Cause**: `mintFor()` used `balanceOf(address(this))` to determine how many tokens to mint. Flash-loaned LP tokens donated to the minter contract inflated the balance, causing excess HUNNY minting.

---

#### Category 5: Stale Reward Accumulator [HIGH]

> **pathShape**: `atomic`

**Example 5: Cover Protocol — Stale Rewards After Pool Transition ($4.4M, 2020-12)** [HIGH]
```solidity
// ❌ VULNERABLE: Reward accumulator cached from old pool applies to new deposits

contract CoverMining {
    uint256 public accRewardsPerShare;

    function deposit(uint256 poolId, uint256 amount) external {
        PoolInfo storage pool = poolInfo[poolId];
        UserInfo storage user = userInfo[poolId][msg.sender];

        updatePool(poolId);
        // @audit rewardDebt calculated from OLD accRewardsPerShare
        // After pool migration: accRewardsPerShare >> actual accumulated
        user.rewardDebt = user.amount * pool.accRewardsPerShare / 1e12;
        user.amount += amount;
    }

    function claimRewards(uint256 poolId) external {
        UserInfo storage user = userInfo[poolId][msg.sender];
        uint256 pending = user.amount * pool.accRewardsPerShare / 1e12 - user.rewardDebt;
        // @audit `pending` is massively inflated because accRewardsPerShare
        // accumulated from old pool was not reset during migration
        COVER.transfer(msg.sender, pending);
    }
}

// Attack timing: During pool migration/transition
// 1. Deposit into new pool → rewardDebt = 0 (fresh deposit)
// 2. accRewardsPerShare still carries old accumulated value
// 3. claimRewards() → pending = amount * staleAccumulator - 0 = MASSIVE
// Result: Drain entire COVER reward allocation in one claim
```
- **PoC**: `DeFiHackLabs/src/test/2020-12/Cover_exp.sol`
- **Root Cause**: When Cover Protocol migrated pools, the `accRewardsPerShare` accumulator retained its old value. New deposits had `rewardDebt = 0`, so `pending` rewards equaled the entire accumulated history.

---

#### Category 6: Self-Transfer Balance Duplication [HIGH]

> **pathShape**: `atomic`

**Example 6: bZx iToken — Self-Transfer Doubles Balance ($8M, 2020-09)** [HIGH]
```solidity
// ❌ VULNERABLE: _internalTransferFrom allows from == to, doubling balance

contract iToken {
    mapping(address => uint256) internal balances;

    function _internalTransferFrom(
        address from, address to, uint256 amount
    ) internal {
        require(balances[from] >= amount, "insufficient");

        // @audit When from == to: both operations execute on same address
        balances[from] -= amount;   // Deduct from sender
        balances[to] += amount;     // Credit to receiver
        // @audit If from == to: net effect = balances[from] += 0 (no change)
        // BUT: The require check already passed for the ORIGINAL balance
        // Wait... actually with from == to:
        // balances[addr] -= amount  →  balances[addr] = originalBal - amount
        // balances[addr] += amount  →  balances[addr] = originalBal
        // This seems neutral... but bZx had additional logic:
    }

    // The actual bZx vulnerability was more nuanced:
    function transferFrom(address from, address to, uint256 amount) public {
        require(balances[from] >= amount);
        // @audit Checkpoint balance for from
        uint256 fromBalance = balances[from];
        // @audit Checkpoint balance for to
        uint256 toBalance = balances[to];  // @audit Same as fromBalance when from==to!

        balances[from] = fromBalance - amount;
        balances[to] = toBalance + amount;
        // @audit When from == to:
        // balances[addr] = toBalance + amount
        // = originalBal + amount (using STALE checkpoint)
        // Instead of originalBal, balance INCREASES by `amount`!
    }
}

// Attack:
// 1. Hold 100 iETH
// 2. transferFrom(self, self, 100)
// 3. Checkpoint: fromBalance = 100, toBalance = 100
// 4. balances[self] = fromBalance - 100 = 0
// 5. balances[self] = toBalance + 100 = 200  ← DOUBLED!
// 6. Repeat: 200 → 400 → 800 → ... → drain lending pool
```
- **PoC**: `DeFiHackLabs/src/test/2020-09/bZx_exp.sol`
- **Root Cause**: `transferFrom` checkpointed both `from` and `to` balances before modifying them. When `from == to`, both checkpoints captured the same original balance. The subtraction used one checkpoint and the addition used the other, resulting in a net increase equal to the transfer amount.

---

### Impact Analysis

#### Technical Impact
- **Unlimited fee extraction**: Transfer-based fee replay has no natural limit
- **Complete vault drainage**: Emergency withdraw loops drain 100% of deposits
- **Balance inflation**: Self-transfer duplication enables exponential growth

#### Business Impact
| Protocol | Loss | Accounting Flaw |
|----------|------|----------------|
| Popsicle Finance | $20M | Fee accumulator not reset on LP transfer |
| bEarn Finance | $11M | Deposit/withdraw reference different strategies |
| bZx | $8M | Self-transfer balance duplication via stale checkpoints |
| Eleven Finance | $4.5M | emergencyBurn doesn't burn shares |
| Cover Protocol | $4.4M | Stale reward accumulator after pool migration |
| PancakeHunny | $2.2M | Donation-inflated balanceOf() for minting |

---

### Secure Implementation

**Fix 1: Reset Fee Debt on Transfer**
```solidity
// ✅ SECURE: Update fee accounting on every transfer
function _transfer(address from, address to, uint256 amount) internal override {
    // @audit Settle pending fees for BOTH sender and receiver before transfer
    _settleFees(from);
    _settleFees(to);

    super._transfer(from, to, amount);

    // @audit Reset fee debt for new holder
    userFeeDebt0[to] = feeGrowthGlobal0;
    userFeeDebt1[to] = feeGrowthGlobal1;
    userFeeDebt0[from] = feeGrowthGlobal0;
    userFeeDebt1[from] = feeGrowthGlobal1;
}
```

**Fix 2: Burn Shares in Emergency Withdraw**
```solidity
// ✅ SECURE: Always burn shares when withdrawing
function emergencyBurn() external {
    uint256 userShare = shares[msg.sender];
    require(userShare > 0, "no shares");

    uint256 amount = userShare * totalBalance / totalShares;

    // @audit MUST burn shares BEFORE transferring funds (CEI pattern)
    shares[msg.sender] = 0;
    totalShares -= userShare;

    token.transfer(msg.sender, amount);
}
```

**Fix 3: Block Self-Transfers**
```solidity
// ✅ SECURE: Prevent from == to in transfers
function _transfer(address from, address to, uint256 amount) internal {
    require(from != to, "self-transfer not allowed");  // @audit Block self-transfer
    require(balances[from] >= amount, "insufficient");
    balances[from] -= amount;
    balances[to] += amount;
}
```

---

### Detection Patterns

```bash
# LP transfers that don't update fee/reward accountinggrep -rn "function _transfer\|function transfer" --include="*.sol" | \
  xargs grep -A 10 "super._transfer\|super.transfer" | \
  grep -L "feeDebt\|rewardDebt\|accumulat"

# Emergency withdraw without share burn
grep -rn "function emergency" --include="*.sol" | \
  xargs grep -A 15 "transfer\|send" | \
  grep -L "_burn\|shares.*=.*0\|balanceOf.*=.*0"

# Self-transfer vulnerability
grep -rn "function _transfer\|function transferFrom" --include="*.sol" | \
  xargs grep -L "from.*!=.*to\|require.*different"

# Stale balance checkpoints
grep -rn "fromBalance.*=.*balances\|toBalance.*=.*balances" --include="*.sol"

# balanceOf used for minting calculations
grep -rn "mint\|_mint" --include="*.sol" | \
  xargs grep -B 5 "balanceOf(address(this))"
```

---

### Audit Checklist

1. **Does the LP/share token `_transfer()` update fee/reward accounting for both sender and receiver?**
2. **Does emergency withdraw burn shares AND decrement totalShares?**
3. **Do deposit and withdraw reference the SAME underlying balance for share calculation?**
4. **Can `from == to` in transfer? If so, are balances checkpointed safely?**
5. **Does any mint/reward function use `balanceOf(address(this))`?** — Donors can inflate this
6. **Are reward accumulators reset during pool migrations or transitions?**
7. **Does the protocol follow Checks-Effects-Interactions (CEI) pattern for withdrawals?**

---

### Keywords

- share_accounting
- fee_replay
- balance_duplication
- self_transfer
- emergency_withdraw
- reward_accumulator
- fee_debt_reset
- deposit_withdraw_mismatch
- donation_inflation
- checkpoint_stale
- balanceOf_manipulation
- DeFiHackLabs

---

### Related Vulnerabilities

- [Vault Inflation Attack](../../general/vault-inflation-attack/vault-inflation-attack.md)
- [Reentrancy Patterns](../../general/reentrancy/defihacklabs-reentrancy-patterns.md)
- [Business Logic Vulnerabilities](../../general/business-logic/business-logic-vulnerabilities.md)
