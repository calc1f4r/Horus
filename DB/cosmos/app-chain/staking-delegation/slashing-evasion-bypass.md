---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: staking
vulnerability_type: slashing_evasion

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_slashing_module

# Technical Primitives
primitives:
  - slash
  - withdrawalDelay
  - cooldown
  - unstake
  - requestWithdrawal
  - fullClaimAndExit
  - frontrunning
  - checkpoint_protection
  - decreaseStakeLockupDuration
  - votingPeriod

# Impact Classification
severity: medium_to_high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - slashing
  - frontrunning
  - timing_attack
  - cooldown_bypass
  - withdrawal_delay
  - penalty_evasion
  - economic_security
  
language: go
version: all
---

## References
- [m-5-slash-can-be-frontrunned-to-avoid-the-penalty-imposed-on-them.md](../../../reports/cosmos_cometbft_findings/m-5-slash-can-be-frontrunned-to-avoid-the-penalty-imposed-on-them.md)
- [m-2-slash-calls-can-be-blocked-allowing-malicious-users-to-bypass-the-slashing-m.md](../../../reports/cosmos_cometbft_findings/m-2-slash-calls-can-be-blocked-allowing-malicious-users-to-bypass-the-slashing-m.md)
- [m03-users-can-avoid-some-slashing-penalties-by-front-running.md](../../../reports/cosmos_cometbft_findings/m03-users-can-avoid-some-slashing-penalties-by-front-running.md)
- [m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md](../../../reports/cosmos_cometbft_findings/m-03-stakers-can-activate-cooldown-during-the-pause-and-try-to-evade-slashing.md)
- [h09-slash-process-can-be-bypassed.md](../../../reports/cosmos_cometbft_findings/h09-slash-process-can-be-bypassed.md)
- [m-5-withdraw-delay-can-be-bypassed.md](../../../reports/cosmos_cometbft_findings/m-5-withdraw-delay-can-be-bypassed.md)
- [m-1-account-that-is-affiliated-with-a-plugin-can-sometimes-evade-slashing.md](../../../reports/cosmos_cometbft_findings/m-1-account-that-is-affiliated-with-a-plugin-can-sometimes-evade-slashing.md)
- [m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md](../../../reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md)
- [m-7-stakers-can-avoid-validator-penalties.md](../../../reports/cosmos_cometbft_findings/m-7-stakers-can-avoid-validator-penalties.md)
- [m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md](../../../reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md)
- [denial-of-slashing.md](../../../reports/cosmos_cometbft_findings/denial-of-slashing.md)
- [elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md](../../../reports/cosmos_cometbft_findings/elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md)
- [m-5-agents-can-evade-the-full-extent-of-a-slash.md](../../../reports/cosmos_cometbft_findings/m-5-agents-can-evade-the-full-extent-of-a-slash.md)

## Vulnerability Title

**Slashing Evasion and Bypass Vulnerabilities in Staking Protocols**

### Overview

Staking protocols implementing slashing mechanisms to penalize malicious or negligent validators frequently contain vulnerabilities that allow malicious actors to evade or bypass slashing penalties. Common attack vectors include frontrunning slash transactions with withdrawal requests, blocking slash execution using checkpoint protection modifiers, exploiting misaligned timing parameters between withdrawal delays and governance voting periods, activating cooldowns during protocol pauses, transferring tokens to bypass cooldown restrictions, and exploiting insufficient deposit checks. These vulnerabilities undermine the fundamental economic security guarantees that slashing mechanisms are designed to provide.

### Root Cause

The fundamental issues stem from:

1. **Mempool visibility**: Slash transactions are visible in the mempool before execution, allowing malicious actors to frontrun with withdrawal or exit transactions
2. **Checkpoint protection conflicts**: Same-block stake modification checks intended to prevent flash loan attacks inadvertently block slash execution
3. **Timing parameter misalignment**: Withdrawal lockup durations shorter than governance voting periods allow stake removal before governance slashing completes
4. **Missing pause-state checks**: Cooldown activation not blocked during protocol pauses, enabling slashing anticipation
5. **Incomplete state coverage**: Slash functions don't decrement from pending withdrawals or queued operations
6. **Plugin/external dependency exploitation**: External contracts can block slash execution by reverting required calls
7. **Insufficient deposit validation**: Elected nodes can have deposits reduced below slashing amounts after initial validation
8. **Reward/share mechanism abuse**: Converting stake to rewards bypasses unstaking cooldowns

### Attack Scenarios

#### Scenario 1: Direct Frontrunning of Slash Transaction [Common Pattern - 5+ reports]

1. Malicious staker commits slashable offense
2. SLASHER role holder submits `slash(account)` transaction
3. Malicious staker monitors mempool and sees pending slash
4. Staker submits `fullClaimAndExit()` with higher gas price
5. Exit transaction executes first, withdrawing all funds
6. Slash transaction executes on empty account - no penalty applied

#### Scenario 2: Checkpoint Protection Exploit [Approx Severity: MEDIUM]

1. Malicious user has stake in protocol with checkpoint protection
2. SLASHER initiates slash on user's account
3. User frontruns with `stake(1)` to update checkpoint in same block
4. Slash calls `_claimAndExit()` internally, which checks checkpoint
5. Checkpoint protection reverts: "Cannot exit in same block as stake"
6. User repeats indefinitely until withdrawal window opens
7. User successfully withdraws, bypassing slashing entirely

#### Scenario 3: Governance Timing Bypass [Approx Severity: HIGH]

1. `decreaseStakeLockupDuration` = 14 days
2. `votingPeriod` = 21 days
3. Malicious service provider commits offense
4. Governance submits slashing proposal
5. Provider immediately requests stake withdrawal
6. After 14 days, provider withdraws all stake
7. After 21 days, slashing proposal passes but executes on empty account

#### Scenario 4: Pause-Period Cooldown Activation [Approx Severity: MEDIUM]

1. Protocol experiences issue requiring emergency pause
2. During pause, slashing event likely to occur
3. Staker activates cooldown (missing `whenNotPaused` modifier)
4. Protocol unpauses and slash event occurs
5. If within unstake window, staker exits before slash executes
6. Staker evades slash; other stakers bear increased penalty

#### Scenario 5: Pending Withdrawal Evasion [Approx Severity: MEDIUM]

1. User has 100 tokens staked and sees potential slash coming
2. User calls `revokePending()` and `revokeActive()` on votes
3. User calls `unlock()` to convert to `PendingWithdrawal` objects
4. Slash function only decrements locked gold balance
5. PendingWithdrawals are not touched by slash
6. User waits for withdrawal completion and exits with funds

### Vulnerable Pattern Examples

**Example 1: Frontrunnable Slash Function** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Slash can be frontrun with exit
function slash(address account, uint256 amount, address to) external onlyRole(SLASHER_ROLE) {
    _claimAndExit(account, amount, to);  // Can be frontrun
    emit Slashed(account, amount);
}

function fullClaimAndExit() external {
    // No slashing lock check - user can exit anytime
    uint256 balance = balanceOf(msg.sender);
    _withdraw(msg.sender, balance);
}
```

**Example 2: Checkpoint Protection Blocking Slash** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Checkpoint protection blocks slash execution
modifier checkpointProtection(address account) {
    uint256 numCheckpoints = _stakes[account]._checkpoints.length;
    require(
        numCheckpoints == 0 || 
        _stakes[account]._checkpoints[numCheckpoints - 1]._blockNumber != block.number,
        "Cannot exit in same block as stake"
    );
    _;
}

function slash(address account, uint256 amount) external onlyRole(SLASHER_ROLE) {
    _claimAndExit(account, amount);  // Uses checkpointProtection
}

// Attacker frontruns with stake(1) to block slash
function stake(uint256 amount) external {
    _stake(msg.sender, amount);  // Updates checkpoint
}
```

**Example 3: Missing Pause Check on Cooldown** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Missing whenNotPaused allows cooldown during emergency
function cooldown() external override {
    // Missing: whenNotPaused modifier
    if (balanceOf(msg.sender) == 0) {
        revert StakedToken_ZeroBalanceAtCooldown();
    }
    if (isInPostSlashingState) {
        revert StakedToken_CooldownDisabledInPostSlashingState();
    }
    _stakersCooldowns[msg.sender] = block.timestamp;
    emit Cooldown(msg.sender);
}
```

**Example 4: Withdrawal Delay Bypass via Pre-Request** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Withdrawal request timestamp not reset on new stake
function requestWithdrawal() external {
    // No check: staked > 0
    // No relationship to actual stake amount
    withdrawalRequestTimestamps[msg.sender] = block.timestamp;
}

function stake(uint256 amount) external {
    // Missing: withdrawalRequestTimestamps[msg.sender] = 0;
    _stake(msg.sender, amount);
}

// Attack: Call requestWithdrawal() BEFORE staking
// Wait for withdrawalDelay, then stake and immediately exit
```

**Example 5: Insufficient Deposit After Election** [Approx Severity: HIGH]
```solidity
// ❌ VULNERABLE: Deposit check only at staking, not at slashing
function staking() external payable {
    require(msg.value >= MINIMUM_DEPOSIT, "Insufficient deposit");
    deposits[msg.sender] += msg.value;
}

function slash(address node, uint256 penalty) external {
    // Reverts if deposits[node] < penalty
    require(deposits[node] >= penalty, "Insufficient for slash");
    deposits[node] -= penalty;
}

// Node can be elected, then partially slashed, then re-elected
// with insufficient remaining deposit for future slashing
```

**Example 6: Plugin Blocking Slash Execution** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: External plugin can block slash
function _notifyStakeChangeAllPlugins(address account, uint256 before, uint256 after) private {
    for (uint256 i = 0; i < nPlugins; i++) {
        // Plugin can revert this call to block slash
        if (IPlugin(plugins[i]).requiresNotification()) {
            try IPlugin(plugins[i]).notifyStakeChange(account, before, after) {}
            catch { emit StakeChangeNotificationFailed(plugins[i]); }
        }
    }
}

function slash(address account, uint256 amount) external onlyRole(SLASHER_ROLE) {
    _claimAndExit(account, amount);  // Calls _notifyStakeChangeAllPlugins
}
```

**Example 7: Gas Griefing Denial of Slashing** [Approx Severity: HIGH]
```solidity
// ❌ VULNERABLE: Unbounded iteration allows gas griefing
function verifyDoubleSigning(address operator, Evidence memory e) external {
    // O(N) complexity - can exceed block gas limit
    for (uint256 i = 0; i < delegatedValidators.length; i++) {
        // Attacker inflates array by calling updateDelegation repeatedly
        if (compareStrings(delegatedValidators[i].validatorPubkey, e.validatorPubkey)) {
            // ...
        }
    }
}
```

### Impact Analysis

#### Technical Impact
- Complete bypass of slashing mechanism
- Economic security guarantees invalidated
- Proof-of-stake security model undermined
- Honest participants bear disproportionate penalties
- Protocol unable to punish malicious behavior

#### Business Impact
- Loss of deterrence against validator misbehavior
- Sophisticated actors can exploit with impunity
- Increased centralization risk (honest actors penalized more)
- Reduced trust in protocol security
- Potential regulatory concerns about security claims

#### Affected Scenarios
- Validator double-signing detection and punishment
- Governance-initiated slashing proposals
- Automated slashing for downtime/inactivity
- Emergency response to malicious behavior
- Any stake-based security mechanism

### Secure Implementation Examples

**Fix 1: Time-Locked Slash with No Exit During Slash Period**
```solidity
// ✅ SECURE: Slash lock prevents exit during slashing window
mapping(address => uint256) public slashLockUntil;
uint256 public constant SLASH_LOCK_DURATION = 7 days;

function initiateSlash(address account) external onlyRole(SLASHER_ROLE) {
    slashLockUntil[account] = block.timestamp + SLASH_LOCK_DURATION;
    emit SlashInitiated(account);
}

function executeSlash(address account, uint256 amount) external onlyRole(SLASHER_ROLE) {
    require(slashLockUntil[account] > 0, "Slash not initiated");
    _slash(account, amount);
    delete slashLockUntil[account];
}

function exit() external {
    require(slashLockUntil[msg.sender] < block.timestamp, "Account locked for slashing");
    _exit(msg.sender);
}
```

**Fix 2: Separate Slash Logic Without Checkpoint Protection**
```solidity
// ✅ SECURE: Slash bypasses checkpoint protection
function slash(address account, uint256 amount) external onlyRole(SLASHER_ROLE) {
    // Use internal function that doesn't have checkpointProtection
    _slashInternal(account, amount);
}

function _slashInternal(address account, uint256 amount) internal {
    // Direct state modification without modifiers that can be gamed
    uint256 balance = stakes[account];
    uint256 slashAmount = amount > balance ? balance : amount;
    stakes[account] -= slashAmount;
    emit Slashed(account, slashAmount);
}
```

**Fix 3: Pause-Aware Cooldown**
```solidity
// ✅ SECURE: Cooldown blocked during pause
function cooldown() external override whenNotPaused {
    if (balanceOf(msg.sender) == 0) {
        revert StakedToken_ZeroBalanceAtCooldown();
    }
    if (isInPostSlashingState) {
        revert StakedToken_CooldownDisabledInPostSlashingState();
    }
    _stakersCooldowns[msg.sender] = block.timestamp;
    emit Cooldown(msg.sender);
}
```

**Fix 4: Reset Withdrawal Timestamp on Stake**
```solidity
// ✅ SECURE: New stake resets withdrawal request
function stake(uint256 amount) external {
    _stake(msg.sender, amount);
    // Reset withdrawal timestamp - user must wait full delay again
    withdrawalRequestTimestamps[msg.sender] = 0;
}

function requestWithdrawal() external {
    require(balanceOf(msg.sender) > 0, "No stake");
    withdrawalRequestTimestamps[msg.sender] = block.timestamp;
}
```

**Fix 5: Enforce Minimum Deposit at Slash Time**
```solidity
// ✅ SECURE: Validate deposit sufficiency at election
function setTssGroupMember(address[] memory members) external {
    for (uint i = 0; i < members.length; i++) {
        require(
            deposits[members[i]] >= MINIMUM_SLASH_AMOUNT,
            "Insufficient deposit for group membership"
        );
    }
    // ... rest of logic
}
```

**Fix 6: Slash Pending Withdrawals**
```solidity
// ✅ SECURE: Slash covers pending withdrawals
function slash(address account, uint256 penalty) external onlyRole(SLASHER_ROLE) {
    uint256 remaining = penalty;
    
    // First, slash from active stake
    uint256 activeStake = lockedGold[account];
    uint256 slashFromActive = remaining > activeStake ? activeStake : remaining;
    lockedGold[account] -= slashFromActive;
    remaining -= slashFromActive;
    
    // Then, slash from pending withdrawals
    if (remaining > 0) {
        for (uint i = 0; i < pendingWithdrawals[account].length && remaining > 0; i++) {
            uint256 pwAmount = pendingWithdrawals[account][i].amount;
            uint256 slashFromPw = remaining > pwAmount ? pwAmount : remaining;
            pendingWithdrawals[account][i].amount -= slashFromPw;
            remaining -= slashFromPw;
        }
    }
    
    emit Slashed(account, penalty - remaining);
}
```

**Fix 7: Bounded Iteration with Length Limit**
```solidity
// ✅ SECURE: Bounded array prevents gas griefing
uint256 public constant MAX_DELEGATIONS = 100;

function updateDelegation(address operator) external {
    require(
        delegatedValidators[operator].length < MAX_DELEGATIONS,
        "Max delegations reached"
    );
    // ... update logic
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- slash() function callable externally without time-lock
- exit/withdraw functions without slash-lock check
- Checkpoint protection on functions called by slash
- Missing whenNotPaused on cooldown activation
- withdrawalRequestTimestamp not reset on new stake
- decreaseStakeLockupDuration <= votingPeriod
- Slash function not covering pendingWithdrawals
- External calls in slash path that can revert
- Unbounded iteration in slash verification logic
- Deposit checks only at staking, not at election/slash
```

#### Audit Checklist
- [ ] Can slash be frontrun with withdrawal?
- [ ] Does checkpoint/flash-loan protection block slash?
- [ ] Is cooldown blocked during protocol pause?
- [ ] Is withdrawal timestamp reset on new stake?
- [ ] Is lockup duration > voting period?
- [ ] Does slash cover pending withdrawals?
- [ ] Can external contracts block slash execution?
- [ ] Is iteration in slash verification bounded?
- [ ] Are deposits validated at slash time?
- [ ] Can tokens be transferred to bypass cooldown?

### Real-World Examples

| Protocol | Audit Firm | Severity | Pattern |
|----------|------------|----------|---------|
| Telcoin | Sherlock | MEDIUM | Frontrunning slash with exit |
| Telcoin | Sherlock | MEDIUM | Checkpoint protection blocking slash |
| Celo | OpenZeppelin | MEDIUM | Pending withdrawals not slashed |
| Increment | Pashov | MEDIUM | Cooldown during pause |
| Increment | Pashov | MEDIUM | Transfer bypass of cooldown |
| Audius | OpenZeppelin | HIGH | Lockup < voting period |
| Telcoin | Sherlock | MEDIUM | Withdrawal delay bypass |
| Telcoin | Sherlock | MEDIUM | Plugin blocking slash |
| Rio Network | Sherlock | MEDIUM | Frontrunning penalties/slashing |
| Covalent | Sherlock | MEDIUM | Cooldown bypass via rewards |
| Ethos | OtterSec | HIGH | Gas griefing denial of slash |
| Mantle | SigmaPrime | HIGH | Insufficient deposit after election |
| Cap | Sherlock | MEDIUM | SlashTimestamp manipulation |

### Frequency Analysis

**Pattern Frequency Across 13+ Reports:**
- Frontrunning slash with withdrawal: 5 reports
- Checkpoint/modifier blocking slash: 2 reports
- Timing parameter misalignment: 2 reports
- Cooldown during pause: 1 report
- Pending withdrawal not slashed: 1 report
- Plugin/external blocking: 1 report
- Gas griefing DoS: 1 report
- Insufficient deposit validation: 1 report

### Related Vulnerabilities

**Compounds With:**
- Flash loan attacks (checkpoint protection conflict)
- Governance timing attacks
- MEV/frontrunning vulnerabilities
- DoS via gas griefing

**Enables:**
- Validator misbehavior without penalty
- Economic attacks on protocol
- Double-signing without consequence

**Pattern Variants:**
- [Staking State Management](./staking-state-management.md) - Related state consistency issues
- [Chain Halt DoS Vectors](../unique/chain-halt-dos-vectors.md) - Gas griefing patterns

### Keywords for Search

slashing_evasion, frontrun_slash, bypass_slashing, evade_penalty, withdrawal_delay_bypass, cooldown_bypass, checkpoint_protection_exploit, slash_frontrunning, unstake_before_slash, pending_withdrawal_slash, lockup_period_bypass, governance_timing_attack, denial_of_slashing, gas_griefing_slash, insufficient_deposit_slash, plugin_blocking_slash, economic_security_bypass, validator_penalty_evasion, stake_exit_slash, claim_and_exit_frontrun
