---
# Core Classification (Required)
protocol: generic
chain: everychain
category: yield
vulnerability_type: yield_strategy_integration

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error|data_manipulation|reentrancy
affected_component: vault|staking|rewards|liquidity_pool|share_calculation

# Technical Primitives (Required)
primitives:
  - share_price
  - exchange_rate
  - total_supply
  - total_assets
  - reward_distribution
  - staking_mechanism
  - deposit_withdrawal
  - inflation_attack
  - flash_loan
  - reentrancy
  - reward_accrual
  - fee_calculation
  - slippage_protection
  - liquidity_provision

# Impact Classification (Required)
severity: critical
impact: fund_loss|theft_of_yield|dos|manipulation|price_manipulation
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - yield
  - vault
  - staking
  - rewards
  - erc4626
  - liquidity_pool
  - flash_loan
  - reentrancy

# Version Info
language: solidity|rust|move
version: all

# Pattern Identity (Required)
root_cause_family: callback_reentrancy
pattern_key: callback_reentrancy | vault | yield_strategy_integration

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - __activateTstore
  - _afterTokenTransfer
  - _beforeTokenTransfer
  - _claimableAmount
  - _convertToShares
  - _decimalsOffset
  - _getUserManagerState
  - _offer
  - _rewardPerToken
  - _setTreasuryRewardCutRate
  - _transfer
  - _updateRewardsPerToken
  - _useTstore
  - _wasActiveAt
  - approve
  - balanceOf
  - batchOffer
  - block.number
  - block.timestamp
  - borrow
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### First Depositor / Inflation Attack Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Wise Lending - First Depositor Attack | `reports/yield_protocol_findings/m-03-first-depositor-inflation-attack-in-pendlepowerfarmtoken.md` | MEDIUM | Code4rena |
| Exchange Rate Manipulation | `reports/yield_protocol_findings/exchangerate-manipulation-via-donation.md` | HIGH | Zokyo |
| VotiumStrategy Inflation Attack | `reports/yield_protocol_findings/m-08-inflation-attack-in-votiumstrategy.md` | MEDIUM | Code4rena |
| NoopVault Donation Attack | `reports/yield_protocol_findings/h-7-an-attacker-can-drain-assets-from-a-closure-by-exploiting-the-noopvault-via-.md` | HIGH | Sherlock |
| First Depositor Market Bricking | `reports/yield_protocol_findings/m-2-first-depositor-can-brick-market-by-forcing-very-large-borrow-rate.md` | MEDIUM | Sherlock |

### Reward Distribution Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Yield - Wrong Rewards No Tokens | `reports/yield_protocol_findings/h-02-erc20rewards-returns-wrong-rewards-if-no-tokens-initially-exist.md` | HIGH | Code4rena |
| Claim Reverts After Period | `reports/yield_protocol_findings/claim-reward-function-reverts-after-distribution-period-ends.md` | MEDIUM | Cantina |
| Infinite FLUX Minting via Merge | `reports/yield_protocol_findings/infinite-minting-of-flux-through-merge.md` | HIGH | Immunefi |
| Unbounded Reward Accrual | `reports/yield_protocol_findings/unbounded-reward-accrual-after-period-end-enables-reward-manipulation-attacks.md` | MEDIUM | Codehawks |
| Timestamp Boundary Reward Dilution | `reports/yield_protocol_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md` | HIGH | Cyfrin |

### Reentrancy Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Cross-Function Reentrancy | `reports/yield_protocol_findings/1-cross-function-reentrancy-leading-to-double-delegation.md` | HIGH | Hexens |
| Balancer Read-Only Reentrancy | `reports/yield_protocol_findings/h-13-balancerpairoracle-can-be-manipulated-using-read-only-reentrancy.md` | HIGH | Sherlock |
| Reentrancy Lock Bypass | `reports/yield_protocol_findings/attacker-can-bypass-reentrancy-lock-to-double-spend-deposit.md` | MEDIUM | Spearbit |

### Flash Loan Attack Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| SwapPool Flash Loan Attack | `reports/yield_protocol_findings/m-09-swappools-are-vulnerable-to-flashloan-attacks.md` | MEDIUM | Pashov Audit Group |

### Provider/Strategy Integration Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Yearn Provider Frozen Tokens | `reports/yield_protocol_findings/h-4-yearnprovider-freezes-yearn-tokens-on-partial-withdrawal.md` | HIGH | Sherlock |
| Strategy Migration State Loss | `reports/yield_protocol_findings/m-04-persistent-inflation-from-uninitialized-rates.md` | MEDIUM | Pashov Audit Group |
| Collateral Rebalancing Gaps | `reports/yield_protocol_findings/m-01-afeth-collaterals-cannot-be-balanced-after-ratio-is-changed.md` | MEDIUM | Code4rena |

### State Machine / Access Control Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Minipool Hijacking | `reports/yield_protocol_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md` | HIGH | Code4rena |
| Vesting Interface Spoofing | `reports/yield_protocol_findings/c-01-complete-drainage-of-vested-tokens-from-claim-in-daovesting.md` | CRITICAL | Shieldify |

### Fee Bypass Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Penalty Circumvention | `reports/yield_protocol_findings/users-can-circumvent-penalty-and-fees.md` | MEDIUM | Quantstamp |

### Vote/Governance Manipulation Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Vote Manipulation in PoolVoter | `reports/yield_protocol_findings/votes-manipulation-in-poolvoter.md` | HIGH | Immunefi |

### Precision/Accounting Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Precision Library Mismatch | `reports/yield_protocol_findings/h-01-underflow-in-updatetranscoderwithfees-can-cause-corrupted-data-and-loss-of-.md` | HIGH | Code4rena |
| Double Subtraction Error | `reports/yield_protocol_findings/m-17-comptrollerwithdrawrewards-accounting-error-results-in-incorrect-inflation-.md` | MEDIUM | Sherlock |

### DoS Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Unbounded Timelock Loop | `reports/yield_protocol_findings/h-08-unable-to-claim-vesting-due-to-unbounded-timelock-loop.md` | HIGH | Code4rena |
| DoS Deposit and Withdraw | `reports/yield_protocol_findings/gg-4-dos-deposit-and-withdraw.md` | MEDIUM | Guardian Audits |

### Minimum Deposit Bypass Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Bypassing MIN_INITIAL_DEPOSIT | `reports/yield_protocol_findings/m-06-bypassing-min_initial_deposit.md` | MEDIUM | Pashov Audit Group |

### External Links
- [ERC-4626 Tokenized Vault Standard](https://eips.ethereum.org/EIPS/eip-4626)
- [OpenZeppelin ERC4626 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol)
- [Solodit Horus](https://solodit.cyfrin.io/)

---

# Yield Strategy Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Yield Protocol Security Audits**

---

## Table of Contents

1. [First Depositor / Inflation Attack](#1-first-depositor--inflation-attack)
2. [Exchange Rate Manipulation via Donation](#2-exchange-rate-manipulation-via-donation)
3. [Reward Distribution Edge Cases](#3-reward-distribution-edge-cases)
4. [Stale Reward Accumulator State](#4-stale-reward-accumulator-state)
5. [Flash Loan LP Fee Extraction](#5-flash-loan-lp-fee-extraction)
6. [Cross-Function Reentrancy in Token Hooks](#6-cross-function-reentrancy-in-token-hooks)
7. [Read-Only Reentrancy in Oracle Integration](#7-read-only-reentrancy-in-oracle-integration)
8. [Partial Withdrawal Token Freeze](#8-partial-withdrawal-token-freeze)
9. [Reward Multiplication via Merge Operations](#9-reward-multiplication-via-merge-operations)
10. [State Machine Hijacking](#10-state-machine-hijacking)
11. [Penalty and Fee Bypass via Secondary Markets](#11-penalty-and-fee-bypass-via-secondary-markets)
12. [Claim Function Arithmetic Underflow](#12-claim-function-arithmetic-underflow)
13. [Missing Slippage Protection in Yield Operations](#13-missing-slippage-protection-in-yield-operations)
14. [Incorrect Share Calculation on Edge Cases](#14-incorrect-share-calculation-on-edge-cases)
15. [Reward Lockup on Period Transitions](#15-reward-lockup-on-period-transitions)
16. [Vault Accounting Desync](#16-vault-accounting-desync)
17. [External Call Context Confusion](#17-external-call-context-confusion)
18. [Deposit/Withdrawal Same-Block Arbitrage](#18-depositwithdrawal-same-block-arbitrage)
19. [Strategy Migration Token Loss](#19-strategy-migration-token-loss)
20. [Compound Interest Manipulation](#20-compound-interest-manipulation)
21. [Time-Weighted Voting Power Exploitation](#21-time-weighted-voting-power-exploitation)
22. [Emergency Withdrawal Accounting Errors](#22-emergency-withdrawal-accounting-errors)
23. [Yield Aggregator Fund Isolation Failures](#23-yield-aggregator-fund-isolation-failures)
24. [Vote Manipulation via Duplicate Pool Entries](#24-vote-manipulation-via-duplicate-pool-entries)
25. [Vesting Contract Interface Spoofing](#25-vesting-contract-interface-spoofing)
26. [Unbounded Reward Accrual After Period End](#26-unbounded-reward-accrual-after-period-end)
27. [Precision Library Mismatch](#27-precision-library-mismatch)
28. [Unbounded Loop DoS via Array Growth](#28-unbounded-loop-dos-via-array-growth)
29. [Minimum Deposit Bypass via Withdrawal](#29-minimum-deposit-bypass-via-withdrawal)
30. [Strategy Migration State Loss](#30-strategy-migration-state-loss)
31. [Double Subtraction Accounting Error](#31-double-subtraction-accounting-error)
32. [Reentrancy Lock Bypass via Storage Mode Switch](#32-reentrancy-lock-bypass-via-storage-mode-switch)
33. [Timestamp Boundary Condition in Activity Checks](#33-timestamp-boundary-condition-in-activity-checks)
34. [First Depositor Market Bricking](#34-first-depositor-market-bricking)
35. [Collateral Rebalancing Gaps](#35-collateral-rebalancing-gaps)

---

## 1. First Depositor / Inflation Attack

### Overview

The first depositor in a vault can manipulate share pricing by depositing a minimal amount followed by a direct token transfer (donation), causing subsequent depositors to receive vastly fewer shares than expected due to rounding.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/m-03-first-depositor-inflation-attack-in-pendlepowerfarmtoken.md` (Wise Lending - Code4rena)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of callback_reentrancy"
- Pattern key: `callback_reentrancy | vault | yield_strategy_integration`
- Interaction scope: `multi_contract`
- Primary affected component(s): `vault|staking|rewards|liquidity_pool|share_calculation`
- High-signal code keywords: `__activateTstore`, `_afterTokenTransfer`, `_beforeTokenTransfer`, `_claimableAmount`, `_convertToShares`, `_decimalsOffset`, `_getUserManagerState`, `_offer`
- Typical sink / impact: `fund_loss|theft_of_yield|dos|manipulation|price_manipulation`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `2.function -> StakedINTX.function -> as.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: External call (`.call`, `.transfer`, token transfer) occurs before state variable update
- Signal 2: Token implements callback hooks (ERC-777, ERC-721) and protocol doesn't use `nonReentrant`
- Signal 3: User-supplied token address passed to `transferFrom` without callback protection
- Signal 4: Read-only function's return value consumed cross-contract during an active callback window

#### False Positive Guards

- Not this bug when: Contract uses `ReentrancyGuard` (`nonReentrant`) on all entry points
- Safe if: All state updates complete before any external call (strict CEI)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

ERC4626 and similar vault implementations calculate shares as `assets * totalSupply / totalAssets`. When totalSupply is small (e.g., 1 share) and totalAssets is inflated via donation, this formula rounds down aggressively for subsequent depositors.

#### Attack Scenario

1. Attacker deposits minimal amount (2 wei) getting 2 shares
2. Attacker donates large amount directly to vault (inflating totalAssets)
3. Victim deposits significant amount
4. `shares = victimDeposit * 2 / (inflatedTotalAssets)` rounds to near-zero
5. Attacker redeems shares, extracting victim's funds

### Vulnerable Pattern Examples

**Example 1: Basic ERC4626 Without Protection** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/m-03-first-depositor-inflation-attack-in-pendlepowerfarmtoken.md`
```solidity
// ❌ VULNERABLE: No protection against first depositor attack
function previewMintShares(uint256 _underlyingAssetAmount, uint256 _underlyingLpAssetsCurrent)
    public
    view
    returns (uint256)
{
    return _underlyingAssetAmount * totalSupply() / _underlyingLpAssetsCurrent;
    // If totalSupply = 3 and _underlyingLpAssetsCurrent = 1e18, 
    // depositing 1e18 gives only 3 shares!
}
```

**Example 2: Vault Without Virtual Shares** [HIGH]
```solidity
// ❌ VULNERABLE: Uses raw ratios
function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
}
```

**Example 3: Missing Minimum Deposit Check** [MEDIUM]
```solidity
// ❌ VULNERABLE: No minimum deposit requirement
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    shares = convertToShares(assets);
    require(shares > 0, "ZERO_SHARES");  // Only checks non-zero, not minimum
    _mint(receiver, shares);
    asset.safeTransferFrom(msg.sender, address(this), assets);
}
```

### Impact Analysis

#### Technical Impact
- Share price manipulation to near-zero value per share
- Rounding causes significant token loss
- Vault becomes unusable after attack

#### Business Impact
- Complete loss of deposited funds for victims
- Protocol reputation damage
- Potential legal liability

#### Affected Scenarios
- New vault deployments
- Vaults resetting after full withdrawals
- Any ERC4626-based implementation without mitigations

### Secure Implementation

**Fix 1: Virtual Shares/Assets Pattern (OpenZeppelin)**
```solidity
// ✅ SECURE: Virtual offset makes inflation expensive
function _decimalsOffset() internal view virtual returns (uint8) {
    return 3;  // 1000 virtual shares
}

function _convertToShares(uint256 assets, Math.Rounding rounding) internal view returns (uint256) {
    return assets.mulDiv(totalSupply() + 10 ** _decimalsOffset(), totalAssets() + 1, rounding);
}
```

**Fix 2: Minimum Initial Deposit**
```solidity
// ✅ SECURE: Large initial deposit prevents inflation
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    if (totalSupply() == 0) {
        require(assets >= MIN_INITIAL_DEPOSIT, "Below minimum");
        // Burn a small portion of initial shares to dead address
        uint256 deadShares = 1000;
        _mint(address(0xdead), deadShares);
    }
    shares = convertToShares(assets);
    _mint(receiver, shares);
    asset.safeTransferFrom(msg.sender, address(this), assets);
}
```

**Fix 3: Admin First Deposit**
```solidity
// ✅ SECURE: Admin seeds vault with initial liquidity
function initialize(uint256 seedAmount) external onlyOwner {
    require(totalSupply() == 0, "Already initialized");
    asset.safeTransferFrom(msg.sender, address(this), seedAmount);
    _mint(address(0xdead), seedAmount);  // Dead shares prevent manipulation
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- ERC4626 implementation without virtual offsets
- convertToShares using raw totalSupply/totalAssets ratio
- No minimum deposit checks
- Missing dead share mechanism
- Vault can reach zero supply state
```

#### Audit Checklist
- [ ] Check for virtual shares/assets implementation
- [ ] Verify minimum initial deposit requirements
- [ ] Ensure vault cannot be reset to zero supply state
- [ ] Check for dead share burning on initialization
- [ ] Verify rounding direction favors the vault

---

## 2. Exchange Rate Manipulation via Donation

### Overview

Privileged or external users can manipulate vault exchange rates through direct token donations, affecting share pricing and reward distributions.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/exchangerate-manipulation-via-donation.md` (Heurist - Zokyo)

### Vulnerability Description

#### Root Cause

Vault exchange rates are calculated from on-chain balances that can be artificially inflated through direct token transfers. Functions that allow "donations" without proper access control can be abused.

#### Attack Scenario

1. Owner/privileged user calls donate() function
2. Large token amount inflates totalAssets
3. Exchange rate increases dramatically
4. Attacker claims vested tokens at inflated rate
5. Receives more underlying tokens than entitled to

### Vulnerable Pattern Examples

**Example 1: Unrestricted Donate Function** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/exchangerate-manipulation-via-donation.md`
```solidity
// ❌ VULNERABLE: Owner can manipulate exchange rate
function donate(uint256 amount) external onlyOwner {
    token.safeTransferFrom(msg.sender, address(this), amount);
    totalHEU += amount;  // Directly affects exchange rate
}
```

**Example 2: Direct Balance Dependency** [MEDIUM]
```solidity
// ❌ VULNERABLE: Exchange rate based on actual balance
function exchangeRate() public view returns (uint256) {
    return token.balanceOf(address(this)) * 1e18 / totalShares;
}
// Anyone can transfer tokens directly to inflate rate
```

### Secure Implementation

**Fix 1: Restrict Donations to Specific Modes**
```solidity
// ✅ SECURE: Only allow donations during migration
function donate(uint256 amount) external onlyOwner {
    require(migrationMode, "Donations only in migration mode");
    token.safeTransferFrom(msg.sender, address(this), amount);
    totalAssets += amount;
}
```

**Fix 2: Internal Accounting Over Balance**
```solidity
// ✅ SECURE: Track deposits internally, ignore donations
uint256 private _internalAssets;

function totalAssets() public view returns (uint256) {
    return _internalAssets;  // Not affected by direct transfers
}

function deposit(uint256 assets) external {
    _internalAssets += assets;
    // ...
}
```

---

## 3. Reward Distribution Edge Cases

### Overview

Reward distribution mechanisms fail when edge cases occur, such as zero token supply at reward start, causing first claimers to receive all historical rewards unfairly.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/h-02-erc20rewards-returns-wrong-rewards-if-no-tokens-initially-exist.md` (Yield - Code4rena)

### Vulnerability Description

#### Root Cause

Reward-per-token calculations use `lastUpdated` timestamps that aren't updated when `totalSupply == 0`, causing reward accumulation to be retroactively applied to the first staker.

#### Attack Scenario

1. Reward period starts but no tokens are staked
2. `lastUpdated` stays at period start time
3. First user mints/stakes tokens
4. `_updateRewardsPerToken` calculates rewards for entire past period
5. First staker receives all accumulated rewards

### Vulnerable Pattern Examples

**Example 1: Early Exit on Zero Supply** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/h-02-erc20rewards-returns-wrong-rewards-if-no-tokens-initially-exist.md`
```solidity
// ❌ VULNERABLE: lastUpdated not updated when totalSupply is 0
function _updateRewardsPerToken() internal {
    if (_totalSupply == 0) {
        return;  // BUG: lastUpdated stays stale!
    }
    
    uint256 timeSinceLastUpdated = block.timestamp - rewardsPerToken_.lastUpdated;
    rewardsPerToken_.accumulated += timeSinceLastUpdated * rewardRate / _totalSupply;
    rewardsPerToken_.lastUpdated = block.timestamp;
}
```

### Secure Implementation

**Fix 1: Always Update Timestamp**
```solidity
// ✅ SECURE: Update timestamp even with zero supply
function _updateRewardsPerToken() internal {
    uint256 end = Math.min(block.timestamp, periodFinish);
    
    if (_totalSupply > 0) {
        uint256 timeSinceLastUpdated = end - rewardsPerToken_.lastUpdated;
        rewardsPerToken_.accumulated += timeSinceLastUpdated * rewardRate / _totalSupply;
    }
    
    // Always update timestamp
    rewardsPerToken_.lastUpdated = end;
}
```

---

## 4. Stale Reward Accumulator State

### Overview

Reward accumulators not updated before balance-changing operations cause incorrect reward calculations, allowing users to claim more or fewer rewards than entitled.

### Vulnerable Pattern Examples

**Example 1: Missing Update Before Balance Change** [HIGH]
```solidity
// ❌ VULNERABLE: Rewards not updated before stake change
function stake(uint256 amount) external {
    balances[msg.sender] += amount;
    totalStaked += amount;
    // BUG: Should call _updateRewards() first!
}
```

### Secure Implementation

**Fix 1: Update Before Any Balance Change**
```solidity
// ✅ SECURE: Always update before balance changes
modifier updateReward(address account) {
    rewardPerTokenStored = rewardPerToken();
    lastUpdateTime = lastTimeRewardApplicable();
    if (account != address(0)) {
        rewards[account] = earned(account);
        userRewardPerTokenPaid[account] = rewardPerTokenStored;
    }
    _;
}

function stake(uint256 amount) external updateReward(msg.sender) {
    balances[msg.sender] += amount;
    totalStaked += amount;
}
```

---

## 5. Flash Loan LP Fee Extraction

### Overview

Liquidity pools allowing same-block deposit/withdraw enable flash loan attackers to extract LP fees without genuine liquidity provision.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/m-09-swappools-are-vulnerable-to-flashloan-attacks.md` (Nabla - Pashov)

### Vulnerability Description

#### Root Cause

No timelock between deposits and withdrawals allows attackers to front-run legitimate transactions with flash-loaned deposits, claiming a share of fees for minimal risk.

#### Attack Scenario

1. Attacker observes pending large deposit in mempool
2. Takes flash loan, deposits before victim
3. Victim's deposit generates fees
4. Attacker withdraws immediately with portion of fees
5. Repays flash loan with profit

### Vulnerable Pattern Examples

**Example 1: No Deposit Delay** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-09-swappools-are-vulnerable-to-flashloan-attacks.md`
```solidity
// ❌ VULNERABLE: Deposit and withdraw in same block
function deposit(uint256 amount, uint256 min, uint256 deadline) external {
    (uint256 lpTokens,) = _deposit(amount);
    _mint(msg.sender, lpTokens);
}

function withdraw(uint256 shares, uint256 minOut, uint256 deadline) external {
    // No check for deposit time - can be same block!
    _burn(msg.sender, shares);
    _withdraw(shares);
}
```

### Secure Implementation

**Fix 1: Minimum Lock Period**
```solidity
// ✅ SECURE: Enforce minimum holding period
mapping(address => uint256) public depositTimestamp;

function deposit(uint256 amount) external {
    depositTimestamp[msg.sender] = block.timestamp;
    // ...
}

function withdraw(uint256 shares) external {
    require(block.timestamp >= depositTimestamp[msg.sender] + MIN_LOCK_PERIOD, 
            "Lock period not elapsed");
    // ...
}
```

---

## 6. Cross-Function Reentrancy in Token Hooks

### Overview

Token transfer hooks (_beforeTokenTransfer, _afterTokenTransfer) can be reentered through external calls, allowing state manipulation mid-operation.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/1-cross-function-reentrancy-leading-to-double-delegation.md` (1Inch - Hexens)

### Vulnerability Description

#### Root Cause

Hooks read state at start of transfer but external calls allow that state to be modified before the hook completes processing, causing double-counting or missed updates.

#### Attack Scenario

1. Transfer triggers _beforeTokenTransfer hook
2. Hook reads pod membership arrays for from/to addresses
3. Hook makes external call to pod.updateBalances()
4. Attacker reenters through callback, calls addPod()
5. Pod array is modified while hook iterates
6. Double delegation tokens minted

### Vulnerable Pattern Examples

**Example 1: Unsafe Hook Iteration** [CRITICAL]
> 📖 Reference: `reports/yield_protocol_findings/1-cross-function-reentrancy-leading-to-double-delegation.md`
```solidity
// ❌ VULNERABLE: External calls during array iteration
function _beforeTokenTransfer(address from, address to, uint256 amount) internal override {
    address[] memory a = _pods[from].items.get();  // State snapshot
    address[] memory b = _pods[to].items.get();
    
    for (uint256 i = 0; i < a.length; i++) {
        address pod = a[i];
        // External call - can reenter and modify _pods mapping!
        _updateBalances(pod, from, address(0), amount);
    }
    
    for (uint256 j = 0; j < b.length; j++) {
        // Uses stale snapshot - doesn't see modifications
        _updateBalances(b[j], address(0), to, amount);
    }
}
```

### Secure Implementation

**Fix 1: Use _afterTokenTransfer with Reentrancy Lock**
```solidity
// ✅ SECURE: Move logic to after hook with reentrancy protection
uint256 private _reentrancyGuard = 1;

modifier nonReentrant() {
    require(_reentrancyGuard == 1, "Reentrancy");
    _reentrancyGuard = 2;
    _;
    _reentrancyGuard = 1;
}

function _afterTokenTransfer(address from, address to, uint256 amount) 
    internal 
    override 
    nonReentrant 
{
    // Safe to make external calls now
}
```

---

## 7. Read-Only Reentrancy in Oracle Integration

### Overview

View functions called during reentrancy can return stale/inconsistent data (e.g., BPT supply updated but balances not), leading to oracle manipulation.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/h-13-balancerpairoracle-can-be-manipulated-using-read-only-reentrancy.md` (Blueberry - Sherlock)

### Vulnerability Description

#### Root Cause

Balancer (and similar AMMs) update BPT supply before updating token balances during joins. Read-only reentrancy allows reading supply after update but balances before, causing price miscalculation.

#### Attack Scenario

1. Attacker calls joinPool with ETH
2. During ETH receive callback, Vault has updated BPT supply but not token balances
3. Attacker triggers liquidation check using manipulated price
4. Oracle calculates: f(old_balances) / new_supply = artificially low price
5. Healthy position liquidated unfairly

### Vulnerable Pattern Examples

**Example 1: Oracle Without Reentrancy Check** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/h-13-balancerpairoracle-can-be-manipulated-using-read-only-reentrancy.md`
```solidity
// ❌ VULNERABLE: No reentrancy guard check on Balancer Vault
function getPrice() public view returns (uint256) {
    (address[] memory tokens, uint256[] memory balances,) = 
        balancerVault.getPoolTokens(poolId);  // Can return stale balances
    uint256 totalSupply = pool.totalSupply();  // Already updated
    
    return calculatePrice(balances, totalSupply);  // Price is wrong!
}
```

### Secure Implementation

**Fix 1: Check Vault Reentrancy Guard**
```solidity
// ✅ SECURE: Verify Vault is not mid-operation
import {VaultReentrancyLib} from "@balancer/VaultReentrancyLib.sol";

function getPrice() public view returns (uint256) {
    VaultReentrancyLib.ensureNotInVaultContext(balancerVault);
    // Safe to read now
    (address[] memory tokens, uint256[] memory balances,) = 
        balancerVault.getPoolTokens(poolId);
    return calculatePrice(balances, pool.totalSupply());
}
```

---

## 8. Partial Withdrawal Token Freeze

### Overview

When underlying protocols (Yearn, Aave, etc.) perform partial withdrawals, unconsumed shares remain stuck in provider contracts without return mechanism.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/h-4-yearnprovider-freezes-yearn-tokens-on-partial-withdrawal.md` (Derby - Sherlock)

### Vulnerability Description

#### Root Cause

Provider contracts transfer full requested share amount from user but underlying withdrawal may only consume partial shares (due to liquidity constraints). Remaining shares stay in provider with no recovery path.

#### Attack Scenario

1. User requests withdrawal of 1000 yTokens
2. Provider transfers all 1000 from user
3. Yearn vault only has liquidity for 700 tokens worth
4. 300 share value of yTokens stuck in provider
5. No mechanism to return unused shares

### Vulnerable Pattern Examples

**Example 1: No Partial Withdrawal Handling** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/h-4-yearnprovider-freezes-yearn-tokens-on-partial-withdrawal.md`
```solidity
// ❌ VULNERABLE: Doesn't return unused shares
function withdraw(uint256 _amount, address _yToken, address _uToken) 
    external 
    returns (uint256) 
{
    // Takes all shares from user
    require(IYearn(_yToken).transferFrom(msg.sender, address(this), _amount));
    
    // Only partial amount may be withdrawn
    uint256 uAmountReceived = IYearn(_yToken).withdraw(_amount);
    IERC20(_uToken).safeTransfer(msg.sender, uAmountReceived);
    
    // BUG: Remaining shares stuck in this contract!
    return uAmountReceived;
}
```

### Secure Implementation

**Fix 1: Return Unused Shares**
```solidity
// ✅ SECURE: Track and return unused shares
function withdraw(uint256 _amount, address _yToken, address _uToken) 
    external 
    returns (uint256) 
{
    uint256 sharesBefore = IERC20(_yToken).balanceOf(address(this));
    
    require(IYearn(_yToken).transferFrom(msg.sender, address(this), _amount));
    
    uint256 uAmountReceived = IYearn(_yToken).withdraw(_amount);
    IERC20(_uToken).safeTransfer(msg.sender, uAmountReceived);
    
    // Return any unused shares
    uint256 sharesAfter = IERC20(_yToken).balanceOf(address(this));
    if (sharesAfter > sharesBefore) {
        IERC20(_yToken).safeTransfer(msg.sender, sharesAfter - sharesBefore);
    }
    
    return uAmountReceived;
}
```

---

## 9. Reward Multiplication via Merge Operations

### Overview

Merging staking positions or NFTs can allow users to claim rewards multiple times by merging already-claimed positions into unclaimed positions, increasing claimable balance.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/infinite-minting-of-flux-through-merge.md` (Alchemix - Immunefi)

### Vulnerability Description

#### Root Cause

Claimable rewards are calculated based on current balance at claim time. Merging positions increases balance of destination, allowing it to claim rewards based on combined balance even though source already claimed.

#### Attack Scenario

1. User has 4 tokens, each entitled to X rewards
2. Claims rewards for token1 (gets X)
3. Merges token1 into token2 (token2 now has 2x balance)
4. Claims token2 (gets 2X instead of X)
5. Repeats: merge token2→token3, claim gets 4X
6. User receives 10X total instead of 4X

### Vulnerable Pattern Examples

**Example 1: Balance-Based Claim Without Merge Tracking** [CRITICAL]
> 📖 Reference: `reports/yield_protocol_findings/infinite-minting-of-flux-through-merge.md`
```solidity
// ❌ VULNERABLE: Claims based on current balance, not claim history
function claimableFlux(uint256 _tokenId) public view returns (uint256) {
    if (block.timestamp > locked[_tokenId].end) {
        return 0;
    }
    // Uses current balance - inflated after merge!
    return (_balanceOfTokenAt(_tokenId, block.timestamp) * fluxPerVeALCX) / BPS;
}

function merge(uint256 _from, uint256 _to) external {
    // Increases _to balance
    locked[_to].amount += locked[_from].amount;
    // _from already claimed, but _to's claimable now includes _from's balance
}
```

### Secure Implementation

**Fix 1: Track Claims Per Token**
```solidity
// ✅ SECURE: Track claimed rewards independently
mapping(uint256 => uint256) public claimedRewards;

function claimFlux(uint256 tokenId) external {
    uint256 totalEarned = calculateTotalEarned(tokenId);
    uint256 claimable = totalEarned - claimedRewards[tokenId];
    
    claimedRewards[tokenId] = totalEarned;
    _mint(msg.sender, claimable);
}

function merge(uint256 from, uint256 to) external {
    // Claim remaining rewards before merge
    claimFlux(from);
    claimFlux(to);
    
    // Now safe to merge
    locked[to].amount += locked[from].amount;
    claimedRewards[to] += claimedRewards[from];
}
```

---

## 10. State Machine Hijacking

### Overview

Improper state transition validation allows attackers to take ownership of positions in certain states (Withdrawable, Error) by re-creating them with their address as owner.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md` (GoGoPool - Code4rena)

### Vulnerability Description

#### Root Cause

State machines allow transitions from completed/error states back to initial states, and the function allowing re-initialization doesn't verify caller is the original owner.

#### Attack Scenario

1. NodeOp creates minipool with nodeID-123
2. Validation period completes, state = Withdrawable
3. Attacker calls createMinipool(nodeID-123)
4. State allows Withdrawable → Prelaunch transition
5. Attacker becomes new owner of minipool
6. Original NodeOp cannot withdraw funds

### Vulnerable Pattern Examples

**Example 1: Missing Owner Check on Re-creation** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/h-04-hijacking-of-node-operators-minipool-causes-loss-of-staked-funds.md`
```solidity
// ❌ VULNERABLE: Anyone can take over existing pools
function createMinipool(address nodeID, uint256 duration, ...) external payable {
    int256 minipoolIndex = getIndexOf(nodeID);
    
    if (minipoolIndex != -1) {
        // Only checks state transition, not ownership!
        requireValidStateTransition(minipoolIndex, MinipoolStatus.Prelaunch);
        resetMinipoolData(minipoolIndex);
    }
    
    // Sets new owner as msg.sender - hijack complete!
    setAddress(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner")), msg.sender);
}
```

### Secure Implementation

**Fix 1: Verify Original Owner**
```solidity
// ✅ SECURE: Only original owner can re-create
function createMinipool(address nodeID, uint256 duration, ...) external payable {
    int256 minipoolIndex = getIndexOf(nodeID);
    
    if (minipoolIndex != -1) {
        onlyOwner(minipoolIndex);  // Add ownership check
        requireValidStateTransition(minipoolIndex, MinipoolStatus.Prelaunch);
        resetMinipoolData(minipoolIndex);
    }
    
    setAddress(keccak256(abi.encodePacked("minipool.item", minipoolIndex, ".owner")), msg.sender);
}
```

---

## 11. Penalty and Fee Bypass via Secondary Markets

### Overview

Staking mechanisms with penalties for early withdrawal can be circumvented by transferring staked tokens on secondary markets where penalties don't apply.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/users-can-circumvent-penalty-and-fees.md` (IntentX - Quantstamp)

### Vulnerability Description

#### Root Cause

transfer() and transferFrom() functions not disabled or overridden to apply penalties/fees, allowing penalty-free exit via secondary market sales.

#### Attack Scenario

1. User stakes INTX, receives xINTX with reward boost
2. Instead of unstaking (incurs penalty), creates secondary market listing
3. Buyer purchases xINTX at fair price (no penalty applied)
4. Seller avoided penalty, buyer gets staked tokens with existing boost
5. Protocol loses expected penalty revenue

### Vulnerable Pattern Examples

**Example 1: Unrestricted Token Transfer** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/users-can-circumvent-penalty-and-fees.md`
```solidity
// ❌ VULNERABLE: Standard ERC20 transfer bypasses penalty
contract StakedINTX is ERC20 {
    function unstake(uint256 amount) external {
        uint256 penalty = calculatePenalty(msg.sender, amount);
        _burn(msg.sender, amount);
        underlying.transfer(msg.sender, amount - penalty);
    }
    
    // transfer() and transferFrom() inherited from ERC20
    // No penalty applied - can sell on secondary market!
}
```

### Secure Implementation

**Fix 1: Override Transfers to Apply Penalty**
```solidity
// ✅ SECURE: Apply penalties on transfer
function _transfer(address from, address to, uint256 amount) internal override {
    // Reset reward boost on transfer
    _resetRewardBoost(from);
    _resetRewardBoost(to);
    
    // Optionally apply transfer fee
    uint256 fee = amount * TRANSFER_FEE_BPS / 10000;
    super._transfer(from, address(this), fee);
    super._transfer(from, to, amount - fee);
}
```

---

## 12. Claim Function Arithmetic Underflow

### Overview

Reward claim functions can underflow when distribution periods end and multiple users attempt to claim, due to improper time boundary handling.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/claim-reward-function-reverts-after-distribution-period-ends.md` (Usual - Cantina)

### Vulnerability Description

#### Root Cause

After the first user claims post-period, `lastUpdateTime` is set beyond `periodFinish`. Subsequent calculations of `min(block.timestamp, periodFinish) - lastUpdateTime` underflow.

#### Attack Scenario

1. Reward period ends at time T
2. User A claims at T+1, sets lastUpdateTime = T+1
3. User B tries to claim
4. Calculation: min(T+2, T) - (T+1) = T - T - 1 underflows
5. Transaction reverts, User B cannot claim

### Vulnerable Pattern Examples

**Example 1: Unchecked Time Subtraction** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/claim-reward-function-reverts-after-distribution-period-ends.md`
```solidity
// ❌ VULNERABLE: Can underflow after period ends
function _rewardPerToken() internal view returns (uint256) {
    if (totalSupply() == 0) {
        return rewardPerTokenStored;
    }
    
    // BUG: If lastUpdateTime > periodFinish, this underflows
    uint256 timeElapsed = Math.min(block.timestamp, periodFinish) - lastUpdateTime;
    
    return rewardPerTokenStored + (rewardRate * timeElapsed * 1e24 / totalSupply());
}
```

### Secure Implementation

**Fix 1: Guard Against Underflow**
```solidity
// ✅ SECURE: Check before subtraction
function _rewardPerToken() internal view returns (uint256) {
    if (totalSupply() == 0) {
        return rewardPerTokenStored;
    }
    
    uint256 end = Math.min(block.timestamp, periodFinish);
    uint256 timeElapsed = 0;
    
    if (lastUpdateTime < end) {
        timeElapsed = end - lastUpdateTime;
    }
    
    return rewardPerTokenStored + (rewardRate * timeElapsed * 1e24 / totalSupply());
}
```

---

## 13. Missing Slippage Protection in Yield Operations

### Overview

Yield harvest, compound, and swap operations lacking slippage controls allow sandwich attacks to extract MEV from protocol operations.

### Vulnerable Pattern Examples

**Example 1: Harvest Without Slippage** [MEDIUM]
```solidity
// ❌ VULNERABLE: No minimum output specified
function harvest() external {
    uint256 rewards = strategy.claim();
    
    // Swaps rewards to base token with no slippage protection
    router.swapExactTokensForTokens(
        rewards,
        0,  // Zero minimum output!
        path,
        address(this),
        block.timestamp
    );
}
```

### Secure Implementation

**Fix 1: Use Oracle-Based Minimum**
```solidity
// ✅ SECURE: Calculate minimum from oracle with tolerance
function harvest(uint256 minOutput) external {
    uint256 rewards = strategy.claim();
    
    uint256 expectedOutput = oracle.getExpectedOutput(rewards);
    uint256 minAcceptable = expectedOutput * (10000 - SLIPPAGE_BPS) / 10000;
    require(minOutput >= minAcceptable, "Slippage too high");
    
    router.swapExactTokensForTokens(
        rewards,
        minOutput,
        path,
        address(this),
        block.timestamp + DEADLINE
    );
}
```

---

## 14. Incorrect Share Calculation on Edge Cases

### Overview

Share calculations fail on edge cases like zero supply, zero assets, or mismatched decimal handling between vault and underlying tokens.

### Vulnerable Pattern Examples

**Example 1: Division by Zero on Empty Vault** [HIGH]
```solidity
// ❌ VULNERABLE: Division by zero possible
function convertToShares(uint256 assets) public view returns (uint256) {
    return assets * totalSupply() / totalAssets();  // Reverts if totalAssets == 0
}
```

**Example 2: Decimal Mismatch** [MEDIUM]
```solidity
// ❌ VULNERABLE: Assumes 18 decimals
function deposit(uint256 assets) external {
    uint256 shares = assets * 1e18 / sharePrice();
    // If underlying has 6 decimals (USDC), calculation is wrong
}
```

### Secure Implementation

**Fix 1: Handle Edge Cases**
```solidity
// ✅ SECURE: Handle all edge cases
function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    if (supply == 0) return assets;  // 1:1 for first deposit
    
    uint256 assets_ = totalAssets();
    if (assets_ == 0) return 0;
    
    return assets.mulDiv(supply, assets_, Math.Rounding.Floor);
}
```

---

## 15. Reward Lockup on Period Transitions

### Overview

Rewards can become permanently locked when transitioning between reward periods if accumulated rewards aren't claimed or properly carried over.

### Vulnerable Pattern Examples

**Example 1: Lost Rewards on New Period** [MEDIUM]
```solidity
// ❌ VULNERABLE: Old rewards potentially lost
function notifyRewardAmount(uint256 reward) external onlyOwner {
    if (block.timestamp >= periodFinish) {
        rewardRate = reward / DURATION;
    } else {
        // BUG: Only adds remaining, doesn't account for unclaimed
        uint256 remaining = (periodFinish - block.timestamp) * rewardRate;
        rewardRate = (reward + remaining) / DURATION;
    }
    
    lastUpdateTime = block.timestamp;
    periodFinish = block.timestamp + DURATION;
}
```

---

## 16. Vault Accounting Desync

### Overview

Vault internal accounting can desync from actual token balances due to rebasing tokens, direct transfers, or fee-on-transfer tokens.

### Vulnerable Pattern Examples

**Example 1: Rebasing Token Desync** [HIGH]
```solidity
// ❌ VULNERABLE: Doesn't account for rebases
uint256 private _totalDeposited;

function deposit(uint256 amount) external {
    _totalDeposited += amount;  // Fixed value
    rebasingToken.transferFrom(msg.sender, address(this), amount);
}

function totalAssets() public view returns (uint256) {
    return _totalDeposited;  // Wrong after rebase!
}
```

### Secure Implementation

**Fix 1: Use Actual Balance**
```solidity
// ✅ SECURE: Use actual balance for rebasing tokens
function totalAssets() public view returns (uint256) {
    return rebasingToken.balanceOf(address(this));
}
```

---

## 17. External Call Context Confusion

### Overview

Using `this.function()` instead of internal calls changes msg.sender, causing access control and token approval issues.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/h-05-rubiconmarket-batchoffer-and-batchrequote-make-offers-as-self-complete-loss.md` (Rubicon - Code4rena)

### Vulnerability Description

#### Root Cause

`this.function()` makes an external call with the contract as msg.sender instead of the original caller, bypassing intended access controls.

### Vulnerable Pattern Examples

**Example 1: Self-Call Changes Context** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/h-05-rubiconmarket-batchoffer-and-batchrequote-make-offers-as-self-complete-loss.md`
```solidity
// ❌ VULNERABLE: this.offer() makes msg.sender = RubiconMarket address
function batchOffer(...) external {
    for (uint i = 0; i < payAmts.length; i++) {
        // BUG: External call - msg.sender in offer() is this contract!
        this.offer(payAmts[i], payGems[i], buyAmts[i], buyGems[i]);
    }
}

function offer(uint256 pay_amt, address pay_gem, ...) external {
    // Transfers FROM msg.sender - which is now the contract!
    pay_gem.transferFrom(msg.sender, address(this), pay_amt);
}
```

### Secure Implementation

**Fix 1: Use Internal Calls**
```solidity
// ✅ SECURE: Internal call preserves original msg.sender context
function batchOffer(...) external {
    for (uint i = 0; i < payAmts.length; i++) {
        _offer(payAmts[i], payGems[i], buyAmts[i], buyGems[i]);
    }
}

function _offer(uint256 pay_amt, address pay_gem, ...) internal {
    // msg.sender is still the original caller
    pay_gem.transferFrom(msg.sender, address(this), pay_amt);
}
```

---

## 18. Deposit/Withdrawal Same-Block Arbitrage

### Overview

Allowing deposits and withdrawals in the same block enables arbitrage when yield accrues or prices change intra-block.

### Vulnerable Pattern Examples

**Example 1: No Cooldown Between Operations** [MEDIUM]
```solidity
// ❌ VULNERABLE: Same block operations allowed
function deposit(uint256 amount) external {
    _mint(msg.sender, convertToShares(amount));
}

function withdraw(uint256 shares) external {
    _burn(msg.sender, shares);
    asset.transfer(msg.sender, convertToAssets(shares));
}
// Attacker: deposit → trigger yield → withdraw (same block)
```

### Secure Implementation

**Fix 1: Block-Based Cooldown**
```solidity
// ✅ SECURE: Different block required
mapping(address => uint256) public lastActionBlock;

function deposit(uint256 amount) external {
    lastActionBlock[msg.sender] = block.number;
    // ...
}

function withdraw(uint256 shares) external {
    require(block.number > lastActionBlock[msg.sender], "Same block");
    // ...
}
```

---

## 19. Strategy Migration Token Loss

### Overview

Migrating from old to new strategies without proper balance handling can leave tokens stranded in old contracts.

### Vulnerable Pattern Examples

**Example 1: Incomplete Withdrawal Before Migration** [HIGH]
```solidity
// ❌ VULNERABLE: May leave tokens in old strategy
function migrateStrategy(address newStrategy) external onlyOwner {
    // Doesn't withdraw all tokens first!
    strategy = IStrategy(newStrategy);
}
```

### Secure Implementation

**Fix 1: Full Exit Before Migration**
```solidity
// ✅ SECURE: Withdraw everything before migration
function migrateStrategy(address newStrategy) external onlyOwner {
    uint256 balance = oldStrategy.withdrawAll();
    require(balance == oldStrategy.totalAssets(), "Incomplete withdrawal");
    
    asset.approve(newStrategy, balance);
    IStrategy(newStrategy).deposit(balance);
    strategy = IStrategy(newStrategy);
}
```

---

## 20. Compound Interest Manipulation

### Overview

Compound interest calculations that can be triggered frequently allow attackers to compound more often than intended, earning excess yield.

### Vulnerable Pattern Examples

**Example 1: Unlimited Compound Frequency** [MEDIUM]
```solidity
// ❌ VULNERABLE: No limit on compound frequency
function compound() external {
    uint256 interest = calculateInterest();
    principal += interest;
    lastUpdate = block.timestamp;
}
// Attacker calls every block, compounding interest faster
```

### Secure Implementation

**Fix 1: Minimum Compound Interval**
```solidity
// ✅ SECURE: Rate-limited compounding
function compound() external {
    require(block.timestamp >= lastUpdate + MIN_COMPOUND_INTERVAL, "Too soon");
    uint256 interest = calculateInterest();
    principal += interest;
    lastUpdate = block.timestamp;
}
```

---

## 21. Time-Weighted Voting Power Exploitation

### Overview

Voting escrow systems can be exploited by acquiring tokens just before votes to maximize voting power, then selling immediately after.

### Vulnerable Pattern Examples

**Example 1: Flash Lock for Votes** [MEDIUM]
```solidity
// ❌ VULNERABLE: Can lock and vote in same transaction
function createLock(uint256 amount, uint256 duration) external {
    locked[msg.sender] = Lock(amount, block.timestamp + duration);
    _updateVotingPower(msg.sender);
}
// Flash loan → lock → vote → unlock next block
```

### Secure Implementation

**Fix 1: Require Lock Before Vote**
```solidity
// ✅ SECURE: Lock must exist before voting
function vote(uint256 proposalId, bool support) external {
    require(locked[msg.sender].start < proposal.startTime, 
            "Lock created after proposal");
    // ... 
}
```

---

## 22. Emergency Withdrawal Accounting Errors

### Overview

Emergency withdrawal functions that bypass normal accounting can leave protocol state inconsistent with actual balances.

### Vulnerable Pattern Examples

**Example 1: Emergency Exit Skips Updates** [MEDIUM]
```solidity
// ❌ VULNERABLE: Accounting not updated
function emergencyWithdraw() external {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;
    // BUG: totalStaked not decreased!
    token.transfer(msg.sender, amount);
}
```

### Secure Implementation

**Fix 1: Update All State**
```solidity
// ✅ SECURE: Update all relevant state
function emergencyWithdraw() external {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;
    totalStaked -= amount;  // Update totals
    rewardDebt[msg.sender] = 0;  // Clear pending rewards
    token.transfer(msg.sender, amount);
}
```

---

## 23. Yield Aggregator Fund Isolation Failures

### Overview

Yield aggregators must isolate funds between users/vaults to prevent cross-contamination; failures allow one strategy's losses to affect others.

### Vulnerable Pattern Examples

**Example 1: Shared Strategy Without Isolation** [HIGH]
```solidity
// ❌ VULNERABLE: All vaults share same strategy balance
mapping(address => uint256) public vaultShares;

function deposit(address vault, uint256 amount) external {
    strategy.deposit(amount);  // Shared strategy
    vaultShares[vault] += amount;  // But tracked separately
}

// If strategy reports loss, all vaults affected disproportionately
```

### Secure Implementation

**Fix 1: Isolated Strategy Per Vault**
```solidity
// ✅ SECURE: Each vault has own strategy instance
mapping(address => IStrategy) public vaultStrategy;

function createVault(address strategyFactory) external returns (address) {
    address vault = createNewVault();
    vaultStrategy[vault] = IStrategy(strategyFactory.clone());
    return vault;
}
```

---

## 24. Vote Manipulation via Duplicate Pool Entries

### Overview

Voting systems that don't check for duplicate pool entries in vote arrays allow users to inflate their voting power by voting for the same gauge multiple times with different weights.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/votes-manipulation-in-poolvoter.md` (ZeroLend - Immunefi)

### Vulnerability Description

#### Root Cause

Vote function doesn't validate that pools in the array are unique. It stores only the last weight but increments totalWeight for each entry, allowing the difference to accumulate with reset cycles.

#### Attack Scenario

1. Attacker has 19 ETH voting power
2. Calls vote([gauge, gauge], [19 ether, 1e8])
3. totalWeight incremented by both 19 ether AND 1e8
4. votes[attacker][gauge] stores only 1e8 (last weight)
5. Calls reset() - deducts only 1e8 from totalWeight
6. 19 ETH of "phantom votes" remain in totalWeight
7. Repeat 100x: attacker's effective voting power = 1900 ETH

### Vulnerable Pattern Examples

**Example 1: Missing Duplicate Check** [CRITICAL]
> 📖 Reference: `reports/yield_protocol_findings/votes-manipulation-in-poolvoter.md`
```solidity
// ❌ VULNERABLE: No duplicate pool check
function vote(address[] calldata _poolVote, uint256[] calldata _weights) external {
    for (uint256 i = 0; i < _poolVote.length; i++) {
        address _pool = _poolVote[i];
        uint256 _poolWeight = _weights[i];
        
        if (_gauge != address(0x0)) {
            _usedWeight += _poolWeight;
            totalWeight += _poolWeight;  // Incremented each time
            weights[_pool] += _poolWeight;
            poolVote[msg.sender].push(_pool);
            votes[msg.sender][_pool] = _poolWeight;  // Only last stored!
        }
    }
}
```

### Secure Implementation

**Fix 1: Track Seen Pools**
```solidity
// ✅ SECURE: Prevent duplicate entries
function vote(address[] calldata _poolVote, uint256[] calldata _weights) external {
    mapping(address => bool) seenPools;
    
    for (uint256 i = 0; i < _poolVote.length; i++) {
        require(!seenPools[_poolVote[i]], "Duplicate pool");
        seenPools[_poolVote[i]] = true;
        // ... rest of logic
    }
}
```

---

## 25. Vesting Contract Interface Spoofing

### Overview

Vesting contracts that trust user-provided DAO addresses to read claim parameters can be exploited by deploying fake contracts that return manipulated values.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/c-01-complete-drainage-of-vested-tokens-from-claim-in-daovesting.md` (Daoslive - Shieldify)

### Vulnerability Description

#### Root Cause

Claim function accepts any address as "DAO contract" and reads token address, contribution amounts, and vesting schedules from it without validating the contract is legitimate.

#### Attack Scenario

1. Attacker deploys fake IDaosLive contract
2. Sets token address to legitimate DAO's token
3. Implements getContributionTokenAmount() to return full vesting contract balance
4. Sets vesting schedule with 100% immediate unlock
5. Calls claim() with fake DAO address
6. Receives all tokens from vesting contract

### Vulnerable Pattern Examples

**Example 1: Trusting User-Provided Interface** [CRITICAL]
> 📖 Reference: `reports/yield_protocol_findings/c-01-complete-drainage-of-vested-tokens-from-claim-in-daovesting.md`
```solidity
// ❌ VULNERABLE: Trusts arbitrary contract as data source
function claim(address dao, address user, uint256 index) external {
    IDaosLive daosLive = IDaosLive(dao);  // Attacker-controlled!
    address token = daosLive.token();  // Fake returns legit token
    
    uint256 maxPercent = getClaimablePercent(dao, index);  // Fake schedule
    uint256 totalAmount = daosLive.getContributionTokenAmount(user);  // Inflated
    
    uint256 amount = calculateAmount(totalAmount, maxPercent);
    TransferHelper.safeTransfer(token, user, amount);  // Drains real tokens
}
```

### Secure Implementation

**Fix 1: Whitelist Valid DAOs**
```solidity
// ✅ SECURE: Only allow registered DAOs
mapping(address => bool) public registeredDAOs;

function claim(address dao, address user, uint256 index) external {
    require(registeredDAOs[dao], "Invalid DAO");
    // ... rest of logic
}
```

---

## 26. Unbounded Reward Accrual After Period End

### Overview

Reward systems that continue calculating rewards after the distribution period ends allow exploitation through strategic deposit/withdrawal timing.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/unbounded-reward-accrual-after-period-end-enables-reward-manipulation-attacks.md` (Core Contracts - Codehawks)

### Vulnerability Description

#### Root Cause

getRewardPerToken() continues calculating rewards when `lastUpdateTime < periodFinish` regardless of whether `block.timestamp > periodFinish`, causing rewards to keep accumulating.

#### Attack Scenario

1. Reward period ends but rewards keep accruing
2. Attacker deposits small amount (triggers update)
3. Rewards doubled due to time delta calculation
4. Repeats deposit → withdraw cycle
5. Each cycle multiplies claimable rewards

### Vulnerable Pattern Examples

**Example 1: Unbounded Time Calculation** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/unbounded-reward-accrual-after-period-end-enables-reward-manipulation-attacks.md`
```solidity
// ❌ VULNERABLE: Keeps calculating after period ends
function getRewardPerToken() public view returns (uint256) {
    if (totalSupply() == 0) {
        return rewardPerTokenStored;
    }
    // BUG: lastTimeRewardApplicable() returns periodFinish
    // But (periodFinish - lastUpdateTime) keeps adding rewards
    return rewardPerTokenStored + (
        (lastTimeRewardApplicable() - lastUpdateTime) * rewardRate * 1e18 / totalSupply()
    );
}
```

### Secure Implementation

**Fix 1: Stop Rewards After Period**
```solidity
// ✅ SECURE: Return 0 after period ends
function getRewardPerToken() public view returns (uint256) {
    if (block.timestamp >= periodFinish) {
        return rewardPerTokenStored;  // Stop calculating
    }
    if (totalSupply() == 0) {
        return rewardPerTokenStored;
    }
    return rewardPerTokenStored + (...);
}
```

---

## 27. Precision Library Mismatch

### Overview

Using different precision libraries (MathUtils vs PreciseMathUtils) for related calculations causes severe miscalculations due to divisor differences.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/h-01-underflow-in-updatetranscoderwithfees-can-cause-corrupted-data-and-loss-of-.md` (Livepeer - Code4rena)

### Vulnerability Description

#### Root Cause

Rate is set using PreciseMathUtils (10^27 divisor) but calculated using MathUtils (10^6 divisor), causing result to be 10^21 times larger than expected.

#### Attack Scenario

1. Treasury cut rate set to 10% using PreciseMathUtils (1e26)
2. treasuryRewards calculated using MathUtils
3. MathUtils.percOf divides by 1e6 instead of 1e27
4. Result is massive, causing underflow in subtraction
5. Function reverts, blocking all reward claims

### Vulnerable Pattern Examples

**Example 1: Mixed Precision Libraries** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/h-01-underflow-in-updatetranscoderwithfees-can-cause-corrupted-data-and-loss-of-.md`
```solidity
// Setting uses PreciseMathUtils (PREC_DIVISOR = 10**27)
function _setTreasuryRewardCutRate(uint256 _cutRate) internal {
    require(PreciseMathUtils.validPerc(_cutRate));  // Valid if < 10**27
    treasuryRewardCutRate = _cutRate;
}

// Calculation uses MathUtils (PREC_DIVISOR = 1000000)
function updateTranscoderWithFees(...) external {
    // BUG: cutRate is ~1e26, but divided by only 1e6!
    uint256 treasuryRewards = MathUtils.percOf(rewards, treasuryRewardCutRate);
    rewards = rewards.sub(treasuryRewards);  // Underflow!
}
```

### Secure Implementation

**Fix 1: Consistent Precision Library**
```solidity
// ✅ SECURE: Use same precision library
function updateTranscoderWithFees(...) external {
    uint256 treasuryRewards = PreciseMathUtils.percOf(rewards, treasuryRewardCutRate);
    rewards = rewards.sub(treasuryRewards);
}
```

---

## 28. Unbounded Loop DoS via Array Growth

### Overview

Functions that iterate over unbounded user arrays can be DoS'd by an attacker growing the array until gas limits are exceeded.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/h-08-unable-to-claim-vesting-due-to-unbounded-timelock-loop.md` (Boot Finance - Code4rena)

### Vulnerability Description

#### Root Cause

vest() allows anyone to create vestments for any beneficiary without minimum amount. claim() loops through all timelocks. Attacker can push millions of tiny vestments.

#### Attack Scenario

1. Attacker calls vest(victim, 1 wei) thousands of times
2. timelocks[victim] array grows very large
3. When victim calls claim(), loop exceeds block gas limit
4. Victim's funds permanently locked

### Vulnerable Pattern Examples

**Example 1: Unbounded Vestment Loop** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/h-08-unable-to-claim-vesting-due-to-unbounded-timelock-loop.md`
```solidity
// ❌ VULNERABLE: Anyone can vest for anyone, no minimum
function vest(address beneficiary, uint256 amount) external {
    timelocks[beneficiary].push(Timelock(amount, block.timestamp));
    // No minimum amount check!
    // beneficiary != msg.sender check missing!
}

function _claimableAmount(address beneficiary) internal view returns (uint256) {
    uint256 total;
    // Loops through ALL timelocks - can exceed gas limit
    for (uint i = 0; i < timelocks[beneficiary].length; i++) {
        total += calculateVested(timelocks[beneficiary][i]);
    }
    return total;
}
```

### Secure Implementation

**Fix 1: Restrict Vestment Creation**
```solidity
// ✅ SECURE: Minimum amount and self-vest only
uint256 public constant MIN_VEST_AMOUNT = 1e18;

function vest(uint256 amount) external {
    require(amount >= MIN_VEST_AMOUNT, "Below minimum");
    timelocks[msg.sender].push(Timelock(amount, block.timestamp));
}
```

---

## 29. Minimum Deposit Bypass via Withdrawal

### Overview

First depositor protections that only check minimum on deposit can be bypassed by depositing then withdrawing to reduce supply below minimum.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/m-06-bypassing-min_initial_deposit.md` (AegisVault - Pashov)

### Vulnerability Description

#### Root Cause

Deposit function checks MIN_INITIAL_DEPOSIT when totalSupply == 0, but withdraw doesn't prevent reducing supply below minimum, enabling return to vulnerable state.

#### Attack Scenario

1. Attacker deposits MIN_INITIAL_DEPOSIT + 1
2. Total supply now equals minimum
3. Attacker withdraws all but 1 share
4. Total supply now below minimum
5. First depositor attack now possible

### Vulnerable Pattern Examples

**Example 1: Missing Withdraw Check** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-06-bypassing-min_initial_deposit.md`
```solidity
// ❌ VULNERABLE: Deposit checks minimum but withdraw doesn't
function deposit(uint256 assets) external returns (uint256 shares) {
    if (totalSupply() == 0) {
        require(shares >= MIN_INITIAL_DEPOSIT, "VTS");
    }
    _mint(msg.sender, shares);
}

function withdraw(uint256 shares) external {
    // No check that remaining supply >= MIN_INITIAL_DEPOSIT!
    _burn(msg.sender, shares);
}
```

### Secure Implementation

**Fix 1: Check Supply After Withdraw**
```solidity
// ✅ SECURE: Prevent reduction below minimum
function withdraw(uint256 shares) external {
    _burn(msg.sender, shares);
    
    uint256 newSupply = totalSupply();
    require(
        newSupply == 0 || newSupply >= MIN_INITIAL_DEPOSIT,
        "Would reduce supply below minimum"
    );
}
```

---

## 30. Strategy Migration State Loss

### Overview

Updating strategy contracts without migrating internal state causes incorrect calculations due to uninitialized parameters.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/m-04-persistent-inflation-from-uninitialized-rates.md` (Hyperstable - Pashov)

### Vulnerability Description

#### Root Cause

setInterestRateStrategy() replaces strategy contract but new contract has zeroed vault-specific parameters (targetUtilization, lastUpdate, etc).

#### Attack Scenario

1. Protocol updates to new interest rate strategy
2. New strategy has no vault state initialized
3. Interest calculations use zero/default values
4. Results in artificially high or zero interest rates
5. Lenders/borrowers affected unfairly

### Vulnerable Pattern Examples

**Example 1: Strategy Swap Without State** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-04-persistent-inflation-from-uninitialized-rates.md`
```solidity
// ❌ VULNERABLE: No state migration
function setInterestRateStrategy(address _newStrategy) external onlyOwner {
    if (_newStrategy == address(0)) revert ZeroAddress();
    
    emit NewInterestRateStrategy(address(interestRateStrategy), _newStrategy);
    
    // BUG: No migration of vault states!
    interestRateStrategy = IInterestRateStrategy(_newStrategy);
}
```

### Secure Implementation

**Fix 1: Migrate State on Strategy Update**
```solidity
// ✅ SECURE: Copy state to new strategy
function setInterestRateStrategy(address _newStrategy) external onlyOwner {
    IInterestRateStrategy oldStrategy = interestRateStrategy;
    IInterestRateStrategy newStrategy = IInterestRateStrategy(_newStrategy);
    
    // Migrate state for each vault
    for (uint i = 0; i < vaults.length; i++) {
        VaultState memory state = oldStrategy.getVaultState(vaults[i]);
        newStrategy.initializeVaultState(vaults[i], state);
    }
    
    interestRateStrategy = newStrategy;
}
```

---

## 31. Double Subtraction Accounting Error

### Overview

Retrieving already-adjusted values and subtracting adjustment again causes incorrect state and potential underflows.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/m-17-comptrollerwithdrawrewards-accounting-error-results-in-incorrect-inflation-.md` (Union Finance - Sherlock)

### Vulnerability Description

#### Root Cause

Function retrieves totalStaked which already has totalFrozen subtracted, then subtracts totalFrozen again, resulting in double deduction.

#### Attack Scenario

1. totalStaked = 100, totalFrozen = 60
2. _getUserManagerState returns 100 - 60 = 40
3. withdrawRewards subtracts frozen again: 40 - 60 = underflow!
4. If > 50% frozen, function reverts
5. Users cannot stake/unstake/claim

### Vulnerable Pattern Examples

**Example 1: Redundant Subtraction** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-17-comptrollerwithdrawrewards-accounting-error-results-in-incorrect-inflation-.md`
```solidity
// _getUserManagerState already subtracts totalFrozen
function _getUserManagerState() returns (UserManagerState memory state) {
    state.totalStaked = userManager.totalStaked() - userManager.totalFrozen();
    // ...
}

// ❌ VULNERABLE: Subtracts again
function withdrawRewards() external {
    UserManagerState memory state = _getUserManagerState();
    // BUG: state.totalStaked already has frozen removed!
    uint256 totalStaked_ = state.totalStaked - state.totalFrozen;  // Double subtraction
    // Use totalStaked_ for calculations...
}
```

### Secure Implementation

**Fix 1: Use Pre-Adjusted Value**
```solidity
// ✅ SECURE: Don't subtract twice
function withdrawRewards() external {
    UserManagerState memory state = _getUserManagerState();
    uint256 totalStaked_ = state.totalStaked;  // Already adjusted
    // Use totalStaked_ for calculations...
}
```

---

## 32. Reentrancy Lock Bypass via Storage Mode Switch

### Overview

Contracts that can switch between regular and transient storage for reentrancy locks allow one-time bypass when the switch occurs mid-execution.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/attacker-can-bypass-reentrancy-lock-to-double-spend-deposit.md` (Uniswap Compact - Spearbit)

### Vulnerability Description

#### Root Cause

Lock set in regular storage before activation. Attacker triggers storage mode switch mid-call. Inner call checks transient storage (empty). Lock bypassed, reentrancy enabled.

#### Attack Scenario

1. Attacker calls deposit(), lock set in sstore
2. During callback, attacker calls __activateTstore()
3. Now lock checks tload (returns 0, not locked!)
4. Attacker reenters deposit()
5. Same tokens counted twice

### Vulnerable Pattern Examples

**Example 1: Storage Mode Switch** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/attacker-can-bypass-reentrancy-lock-to-double-spend-deposit.md`
```solidity
// ❌ VULNERABLE: External activation changes lock storage
function __activateTstore() external {
    require(msg.sender == tx.origin);  // Bypassable with EIP-7702
    if (!_testTload(_tloadTestContract)) revert TStoreNotSupported();
    _tstoreSupport = true;  // Switches all future checks to tstore!
}

// Lock was set in sstore, but now checks tload
modifier nonReentrant() {
    require(_getTstorish(LOCK_SLOT) == 0);  // Checks new storage!
    _setTstorish(LOCK_SLOT, 1);
    _;
    _clearTstorish(LOCK_SLOT);
}
```

### Secure Implementation

**Fix 1: Atomic Storage Switch**
```solidity
// ✅ SECURE: Switch takes effect next block
uint256 public activationBlock;

function __activateTstore() external {
    require(!_tstoreSupport);
    if (!_testTload(_tloadTestContract)) revert TStoreNotSupported();
    activationBlock = block.number + 1;  // Next block
}

function _useTstore() internal view returns (bool) {
    return activationBlock > 0 && block.number >= activationBlock;
}
```

---

## 33. Timestamp Boundary Condition in Activity Checks

### Overview

Using `>=` instead of `>` for disabled time checks causes entities disabled at exact epoch start to be incorrectly counted as active for that epoch.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md` (Suzaku Core - Cyfrin)

### Vulnerability Description

#### Root Cause

`_wasActiveAt()` returns true when `disabledTime >= timestamp`. At exact equality (disabled at epoch start), entity should be inactive but is counted as active.

#### Attack Scenario

1. Operator disabled exactly at epoch start timestamp
2. _wasActiveAt(enabledTime, disabledTime, epochStart) returns true
3. Operator's stake included in totalStake calculation
4. Active operators' reward share diluted
5. Disabled operator can't claim (no uptime)
6. Rewards stuck in contract

### Vulnerable Pattern Examples

**Example 1: Off-by-One Boundary** [HIGH]
> 📖 Reference: `reports/yield_protocol_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md`
```solidity
// ❌ VULNERABLE: >= includes exact disable time
function _wasActiveAt(uint48 enabledTime, uint48 disabledTime, uint48 timestamp) 
    private pure returns (bool) 
{
    return enabledTime != 0 
        && enabledTime <= timestamp 
        && (disabledTime == 0 || disabledTime >= timestamp);  // BUG: >= should be >
}
```

### Secure Implementation

**Fix 1: Use Strict Inequality**
```solidity
// ✅ SECURE: Disabled at timestamp means inactive
function _wasActiveAt(uint48 enabledTime, uint48 disabledTime, uint48 timestamp) 
    private pure returns (bool) 
{
    return enabledTime != 0 
        && enabledTime <= timestamp 
        && (disabledTime == 0 || disabledTime > timestamp);  // Strict >
}
```

---

## 34. First Depositor Market Bricking

### Overview

First depositor can manipulate lending markets to force utilization > 100%, causing borrow rate to exceed maximum and brick all market operations.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/m-2-first-depositor-can-brick-market-by-forcing-very-large-borrow-rate.md` (Malda - Sherlock)

### Vulnerability Description

#### Root Cause

Utilization rate formula allows results > 100% when `borrows > cash + borrows - reserves`. Interest rate calculations use unbounded utilization, exceeding maximums.

#### Attack Scenario

1. Alice deposits 1e18, borrows all
2. Waits for interest: borrows = 1e18 + 1e12, reserves = 5e11
3. Repays all but (reserves + 1)
4. Redeems total supply
5. State: cash=0, borrows=5e11+1, reserves=5e11
6. Utilization = 5e11 * 1e18 / 1 = 5e29 (massive)
7. Borrow rate exceeds max, _accrueInterest always reverts

### Vulnerable Pattern Examples

**Example 1: Unbounded Utilization** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-2-first-depositor-can-brick-market-by-forcing-very-large-borrow-rate.md`
```solidity
// ❌ VULNERABLE: Utilization can exceed 100%
function utilizationRate(uint256 cash, uint256 borrows, uint256 reserves) 
    public pure returns (uint256) 
{
    if (borrows == 0) return 0;
    // Can return > 1e18 when cash + borrows - reserves < borrows
    return borrows * 1e18 / (cash + borrows - reserves);
}

function getBorrowRate(uint256 cash, uint256 borrows, uint256 reserves) 
    public view returns (uint256) 
{
    uint256 util = utilizationRate(cash, borrows, reserves);
    // Massive util causes massive rate, exceeding max
    return baseRate + util * multiplier / 1e18;
}
```

### Secure Implementation

**Fix 1: Cap Utilization**
```solidity
// ✅ SECURE: Bound utilization to 100%
function utilizationRate(uint256 cash, uint256 borrows, uint256 reserves) 
    public pure returns (uint256) 
{
    if (borrows == 0) return 0;
    uint256 util = borrows * 1e18 / (cash + borrows - reserves);
    return util > 1e18 ? 1e18 : util;  // Cap at 100%
}
```

---

## 35. Collateral Rebalancing Gaps

### Overview

Multi-collateral systems that change allocation ratios provide no mechanism to rebalance existing deposits to the new ratio.

> **📚 Source Reports for Deep Dive:**
> - `reports/yield_protocol_findings/m-01-afeth-collaterals-cannot-be-balanced-after-ratio-is-changed.md` (Asymmetry - Code4rena)

### Vulnerability Description

#### Root Cause

setRatio() changes target allocation but only affects new deposits. Existing TVL remains at old ratio with no rebalancing function.

#### Attack Scenario

1. Protocol starts with 30% SafEth / 70% Votium ratio
2. $10M TVL accumulates: $3M SafEth, $7M Votium
3. Admin changes ratio to 50% / 50%
4. Existing $4M gap cannot be corrected
5. New deposits follow new ratio but existing imbalance persists
6. Years may be needed for organic rebalancing

### Vulnerable Pattern Examples

**Example 1: Ratio Without Rebalance** [MEDIUM]
> 📖 Reference: `reports/yield_protocol_findings/m-01-afeth-collaterals-cannot-be-balanced-after-ratio-is-changed.md`
```solidity
// ❌ VULNERABLE: Changes ratio without rebalancing
function setRatio(uint256 _newRatio) public onlyOwner {
    ratio = _newRatio;
    // No mechanism to move funds between collaterals!
}

function deposit() external payable {
    uint256 safEthAmount = msg.value * ratio / 1e18;
    uint256 votiumAmount = msg.value - safEthAmount;
    // Only new deposits follow ratio, not existing TVL
}
```

### Secure Implementation

**Fix 1: Add Rebalancing Function**
```solidity
// ✅ SECURE: Allow admin to rebalance
function rebalance(uint256 minSafEthOut, uint256 minVotiumOut) external onlyOwner {
    uint256 currentSafEth = safEthBalance();
    uint256 currentVotium = votiumBalance();
    uint256 total = currentSafEth + currentVotium;
    
    uint256 targetSafEth = total * ratio / 1e18;
    
    if (currentSafEth > targetSafEth) {
        uint256 excess = currentSafEth - targetSafEth;
        _withdrawSafEth(excess);
        _depositVotium(excess);
    } else {
        uint256 deficit = targetSafEth - currentSafEth;
        _withdrawVotium(deficit);
        _depositSafEth(deficit);
    }
}
```

---

## Detection Patterns Summary

### Code Patterns to Look For
```
- ERC4626 without virtual shares/assets
- Reward calculations with early return on zero supply
- External calls in token hooks without reentrancy guards
- State machines allowing public re-initialization
- Missing slippage parameters (0 or type(uint).max)
- Balance-based accounting for rebasing tokens
- this.function() calls that should be internal
- Same-block deposit/withdrawal allowed
- Merge operations without reward claim
- Vote arrays without duplicate entry checks
- Functions trusting user-provided interface addresses
- Reward accrual continuing after periodFinish
- Mixed precision libraries in calculations
- Unbounded loops over user-controlled arrays
- MIN_INITIAL_DEPOSIT only checked on deposit, not withdraw
- Strategy updates without state migration
- Double subtraction in accounting functions
- Reentrancy lock using switchable storage modes
- Timestamp boundary using >= instead of > for disabled checks
- Utilization rate unbounded (can exceed 100%)
- Ratio changes without rebalancing mechanism
```

### Audit Checklist
- [ ] First depositor attack mitigations in place
- [ ] Reward distribution handles zero supply periods
- [ ] All token hooks are reentrancy-safe
- [ ] State transitions verify ownership
- [ ] Slippage protection on all swaps
- [ ] Balance tracking matches token behavior
- [ ] Emergency functions update all state
- [ ] Strategy migrations are atomic with state transfer
- [ ] Vote functions validate unique pool entries
- [ ] Interface addresses are whitelisted
- [ ] Reward periods bounded correctly
- [ ] Consistent precision libraries throughout
- [ ] Array loops have gas limits or pagination
- [ ] Minimum supply maintained on withdrawals
- [ ] Timestamp comparisons use correct boundary conditions
- [ ] Utilization rates capped at sensible maximums

---

## Keywords for Search

`yield`, `vault`, `strategy`, `staking`, `rewards`, `ERC4626`, `share_price`, `exchange_rate`, `inflation_attack`, `first_depositor`, `flash_loan`, `reentrancy`, `read_only_reentrancy`, `reward_distribution`, `penalty_bypass`, `fee_circumvention`, `share_calculation`, `deposit`, `withdrawal`, `liquidity_pool`, `compound_interest`, `voting_escrow`, `emergency_withdraw`, `yield_aggregator`, `strategy_migration`, `slippage`, `sandwich_attack`, `oracle_manipulation`, `Balancer`, `Yearn`, `Curve`, `Aave`, `Compound`, `vote_manipulation`, `vesting`, `unbounded_loop`, `DoS`, `gas_limit`, `precision_mismatch`, `double_subtraction`, `timestamp_boundary`, `utilization_rate`, `rebalancing`, `interface_spoofing`, `tstore`, `transient_storage`

---

## Related Vulnerabilities

- [Oracle Manipulation Vulnerabilities](../oracle/)
- [ERC20 Token Vulnerabilities](../tokens/)
- [Access Control Issues](../general/access-control.md)
- [Reentrancy Patterns](../general/reentrancy.md)

---

## DeFiHackLabs Real-World Exploits (1 incidents)

**Category**: Yield Strategy | **Total Losses**: $10K | **Sub-variants**: 1

### Sub-variant Breakdown

#### Yield-Strategy/Generic (1 exploits, $10K)

- **Thena** (2023-03, $10K, bsc) | PoC: `DeFiHackLabs/src/test/2023-03/Thena_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| Thena | 2023-03-28 | $10K | Yield Protocol Flaw | bsc |

### Top PoC References

- **Thena** (2023-03, $10K): `DeFiHackLabs/src/test/2023-03/Thena_exp.sol`

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

`__activateTstore`, `_afterTokenTransfer`, `_beforeTokenTransfer`, `_claimableAmount`, `_convertToShares`, `_decimalsOffset`, `_getUserManagerState`, `_offer`, `_rewardPerToken`, `_setTreasuryRewardCutRate`, `_transfer`, `_updateRewardsPerToken`, `_useTstore`, `_wasActiveAt`, `approve`, `balanceOf`, `batchOffer`, `block.number`, `block.timestamp`, `borrow`, `defi`, `deposit_withdrawal`, `erc4626`, `exchange_rate`, `fee_calculation`, `flash_loan`, `inflation_attack`, `liquidity_pool`, `liquidity_provision`, `reentrancy`, `reward_accrual`, `reward_distribution`, `rewards`, `share_price`, `slippage_protection`, `staking`, `staking_mechanism`, `total_assets`, `total_supply`, `vault`, `yield`, `yield_strategy_integration`
