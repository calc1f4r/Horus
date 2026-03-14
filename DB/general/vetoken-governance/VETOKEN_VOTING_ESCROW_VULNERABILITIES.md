---
# Core Classification
protocol: generic
chain: everychain
category: vetoken_governance
vulnerability_type: voting_escrow_exploits

# Pattern Identity
root_cause_family: vetoken_accounting_and_governance
pattern_key: missing_guard | voting_escrow | lock_vote_bribe_boost | fund_theft_governance_corruption

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - VotingEscrow
  - Voter
  - GaugeController
  - Bribe
  - RewardsDistributor
  - Minter
  - BoostController
  - Gauge
path_keys:
  - missing_epoch_check | bribe_claim | Voter→Bribe | reward_theft
  - missing_balance_decay | poke_voting | VotingEscrow→Voter→Bribe | inflated_rewards
  - missing_weight_tracking | gauge_vote | GaugeController→Gauge | emission_misallocation
  - missing_accounting_symmetry | bribe_deposit_withdraw | Voter→Bribe | totalVoting_desync
  - missing_lock_validation | lock_increase_merge_split | VotingEscrow | voting_power_inflation
  - missing_killed_check | gauge_distribution | Voter→Minter→Gauge | reward_theft_from_active_gauges
  - missing_ongoing_collateral_check | boost_delegation | BoostController→VotingEscrow | unbacked_boost
  - missing_access_control | poke_function | Voter→FluxToken | unlimited_token_minting

# Attack Vector Details
attack_type: economic_exploit
affected_component: voting_escrow_gauge_bribe_system

# Technical Primitives
primitives:
  - voting_power_decay
  - lock_duration
  - epoch_checkpoint
  - gauge_weight
  - bribe_distribution
  - boost_delegation
  - veNFT_accounting
  - rebase_emissions
  - totalSupply_checkpoint
  - reward_rate

# Grep / Hunt-Card Seeds
code_keywords:
  - balanceOfNFT
  - _checkpoint
  - totalVoting
  - claimBribes
  - getRewardForOwner
  - notifyRewardAmount
  - poke
  - _vote
  - accrueFlux
  - depositManaged
  - lockEnd
  - createLock
  - increase_amount
  - merge
  - split
  - killGauge
  - delegateBoost
  - getBoostMultiplier
  - _writeVotingCheckpoint
  - _writeSupplyCheckpoint
  - distributeEx
  - gaugeWeight
  - userGaugeVotes

# Impact Classification
severity: high
impact: fund_theft_governance_corruption
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - governance
  - vetoken
  - voting_escrow
  - gauge
  - bribe
  - ve3_3
  - solidly
  - velodrome
  - curve

# Version Info
language: solidity
version: ">=0.8.0"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [bribe-epoch-claim] | reports/vetoken_findings/claiming-bribes-for-epochs-you-didnt-vote-for-leading-to-protocol-insolvency.md | HIGH | Immunefi | 38154 |
| [bribe-totalvoting-deflation] | reports/vetoken_findings/deflating-the-total-amount-of-votes-in-a-checkpoint-to-steal-bribes-and-create-s.md | HIGH | Immunefi | 38163 |
| [expired-lock-rewards] | reports/vetoken_findings/expired-locks-can-be-used-to-claim-rewards.md | HIGH | Immunefi | 38155 |
| [double-voting-power] | reports/vetoken_findings/attackers-can-double-voting-power-and-vetoken-amount-by-locking-and-increasing.md | HIGH | Codehawks | 57208 |
| [carry-vote-double] | reports/vetoken_findings/c-01-carryvoteforward-enables-double-voting.md | HIGH | Pashov Audit Group | 61950 |
| [gauge-weight-underflow] | reports/vetoken_findings/faulty-gauge-weight-update-formula-voting-power-delta-not-considered-leading-to-.md | HIGH | Codehawks | 57142 |
| [reward-distributeEx-theft] | reports/vetoken_findings/all-reward-tokens-can-be-stolen-by-an-attacker-due-to-misaccounting-in-distribut.md | HIGH | Immunefi | 38315 |
| [reward-distribution-theft] | reports/vetoken_findings/bug-in-reward-distribution-logic-leads-to-theft-of-rewards.md | HIGH | Immunefi | 38313 |
| [boost-persists-withdrawn] | reports/vetoken_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md | MEDIUM | Codehawks | 57246 |
| [checkpoint-rounding] | reports/vetoken_findings/checkpoints-wont-update-block-number-in-point-because-of-a-rounding-issue.md | MEDIUM | Immunefi | 38252 |
| [gauge-gaming-stakewithdraw] | reports/vetoken_findings/gauge-reward-system-can-be-gamed-with-repeatedly-stakewithdraw.md | HIGH | Codehawks | 57302 |
| [boost-always-max] | reports/vetoken_findings/flawed-boost-multiplier-calculation-always-yields-maximum-boost.md | MEDIUM | Codehawks | 57270 |
| [split-arbitrary-amount] | reports/vetoken_findings/c-01-split-can-be-abused-to-create-locked-data-with-an-arbitrary-amount.md | HIGH | Pashov Audit Group | 58150 |
| [flashloan-voting-power] | reports/vetoken_findings/h-03-users-can-use-flashloan-to-increase-voting-power-of-expired-positions-and-e.md | HIGH | Shieldify | 45551 |
| [gauge-misallocation] | reports/vetoken_findings/gauge-voting-misallocation-vulnerability.md | HIGH | Codehawks | 57213 |
| [poke-unlimited-flux] | reports/vetoken_findings/lack-of-access-control-in-poke-function-allows-in-unlimited-minting-of-flux-toke.md | HIGH | Immunefi | 38189 |
| [totalvoting-freeze] | reports/vetoken_findings/incorrect-accounting-of-totalvoting-leads-to-permanent-freeze-of-funds-in-bribe-.md | HIGH | Immunefi | 38237 |
| [killgauge-emission-leak] | reports/vetoken_findings/h-01-killgauge-will-lead-to-wrong-calculation-of-emission.md | HIGH | Code4rena | 41460 |
| [killed-gauge-steals] | reports/vetoken_findings/killed-gauge-continue-to-accrue-and-steal-rewards-from-minter-contract.md | HIGH | Immunefi | 38201 |
| [bribe-emission-gaming] | reports/vetoken_findings/bribe-and-fee-token-emissions-can-be-gamed-by-users.md | MEDIUM | Spearbit | 21385 |
| [bribe-desync] | reports/vetoken_findings/desync-between-bribes-being-paid-and-gauge-distribution-allows-voters-to-receive.md | MEDIUM | Spearbit | 21386 |
| [rebase-unvested] | reports/vetoken_findings/depositmanaged-can-be-used-by-locks-to-receive-unvested-velo-rebase-rewards.md | MEDIUM | Spearbit | 21419 |
| [poke-dos] | reports/vetoken_findings/h-3-poke-may-be-dos.md | MEDIUM | Immunefi | — |
| [reward-rate-loss] | reports/vetoken_findings/m-05-rollover-rewards-are-permanently-lost-due-to-flawed-rewardrate-calculation.md | MEDIUM | Immunefi | — |
| [dust-vote-poke-dos] | reports/vetoken_findings/m-04-dust-vote-on-one-pool-prevents-poke.md | MEDIUM | Code4rena | 63711 |
| [delegates-dos] | reports/vetoken_findings/dos-attack-by-delegating-tokens-at-max_delegates-1024-in-voting-escrow.md | MEDIUM | Immunefi | 38106 |
| [duplicate-gauge] | reports/vetoken_findings/adding-the-same-gauge-multiple-times-will-lead-to-incorrect-sum-of-weights.md | MEDIUM | TrailOfBits | 17767 |
| [emission-stuck-first-epoch] | reports/vetoken_findings/alchemix-the-first-epochs-alcx-emissions-of-voter-contract-will-be-stuck-forever.md | HIGH | Immunefi | 38229 |
| [gauge-emission-revert] | reports/vetoken_findings/gauge-emissions-revert-when-emissions-are-higher-than-the-leftover-buffer-instea.md | MEDIUM | Codehawks | 57214 |
| [extending-expired-break] | reports/vetoken_findings/extending-the-duration-of-an-expired-position-can-break-protocol-accounting.md | MEDIUM | TrailOfBits | 33148 |

## Vulnerability Title

**veToken / Voting Escrow Governance Vulnerabilities** — Comprehensive patterns across Solidly/ve(3,3)-style governance systems covering lock accounting, gauge voting, bribe distribution, boost mechanics, and reward emission exploits.

### Overview

veToken governance systems (Curve, Solidly, Velodrome, Aerodrome, and their forks) share a common architecture where users lock tokens for voting power (veNFTs), vote on gauges to direct emissions, claim bribes for their votes, and receive boost multipliers. This entry covers 8 vulnerability families with 30+ unique findings from 10+ independent auditors across 15+ protocols. The core patterns arise from accounting desynchronization between the tightly coupled VotingEscrow ↔ Voter ↔ Gauge ↔ Bribe ↔ Minter contracts.

#### Agent Quick View

- Root cause statement: "These vulnerabilities exist because veToken governance systems fail to maintain accounting consistency across the VotingEscrow, Voter, Gauge, Bribe, and Minter contracts — missing epoch guards, asymmetric deposit/withdraw accounting, stale voting power references, and lack of killed-gauge exclusion allow reward theft, governance manipulation, and protocol insolvency."
- Pattern key: `missing_guard | voting_escrow | lock_vote_bribe_boost | fund_theft_governance_corruption`
- Interaction scope: `multi_contract`
- Primary affected component(s): `VotingEscrow, Voter, Bribe, GaugeController, RewardsDistributor, Minter, BoostController`
- Contracts / modules involved: `VotingEscrow, Voter, GaugeController, Bribe, RewardsDistributor, Minter, BoostController, Gauge`
- Path keys: `bribe_claim | Voter→Bribe`, `poke_voting | VotingEscrow→Voter→Bribe`, `gauge_vote | GaugeController→Gauge`, `deposit_withdraw | Voter→Bribe`, `lock_ops | VotingEscrow`, `gauge_distribution | Voter→Minter→Gauge`, `boost_delegation | BoostController→VotingEscrow`, `poke | Voter→FluxToken`
- High-signal code keywords: `balanceOfNFT, _checkpoint, totalVoting, claimBribes, getRewardForOwner, notifyRewardAmount, poke, killGauge, delegateBoost, split, merge, distributeEx`
- Typical sink / impact: `bribe theft / emission misallocation / governance manipulation / protocol insolvency / voting power inflation`
- Validation strength: `strong` (30+ unique findings, 10+ auditors, 15+ protocols)

#### Contract / Boundary Map

```
VotingEscrow ─── lock/unlock/merge/split/increase ──→ veNFT balances & checkpoints
     │
     ├──→ Voter ─── vote/poke/reset ──→ pool weights & gauge allocation
     │       │
     │       ├──→ Bribe ─── deposit/withdraw/getRewardForOwner ──→ bribe rewards per epoch
     │       │
     │       ├──→ Gauge ─── notifyRewardAmount/stake/withdraw ──→ LP emission rewards
     │       │
     │       └──→ Minter ─── update_period/distribute ──→ epoch emissions
     │
     ├──→ GaugeController ─── vote/addGauge/killGauge ──→ gauge weights & emission splits
     │
     ├──→ BoostController ─── delegateBoost/getBoostMultiplier ──→ yield boost
     │
     └──→ RewardsDistributor ─── claim ──→ rebase rewards
```

- Entry surface(s): `VotingEscrow.createLock()`, `Voter.vote()`, `Voter.poke()`, `Bribe.getRewardForOwner()`, `GaugeController.vote()`, `BoostController.delegateBoost()`, `VotingEscrow.split()`, `VotingEscrow.merge()`
- Contract hop(s): `Voter.vote → Bribe.deposit`, `Voter.poke → Bribe.withdraw → Bribe.deposit`, `Voter.distribute → Minter → Gauge.notifyRewardAmount`
- Trust boundary crossed: `epoch boundary (timing)`, `VotingEscrow → Voter state sync`, `Bribe totalVoting ↔ actual votes`, `BoostController → veToken balance sync`
- Shared state or sync assumption: `totalVoting in Bribe must equal sum of active vote deposits`, `gauge weights must exclude killed gauges`, `voting power must reflect current veNFT decay`

#### Valid Bug Signals

- Signal 1: Bribe.withdraw() does not decrement totalVoting while Bribe.deposit() does increment it
- Signal 2: claimBribes/getRewardForOwner does not check if the tokenId voted in the claimed epoch
- Signal 3: poke() calls accrueFlux/deposit without onlyNewEpoch modifier
- Signal 4: GaugeController.vote() does not track cumulative weight per user across multiple gauges
- Signal 5: killGauge() does not zero the killed gauge's weight in totalWeight or stop reward accrual
- Signal 6: VotingEscrow.increase() double-counts the increased amount in bias calculation
- Signal 7: split() does not validate that _amount <= locked.amount
- Signal 8: BoostController.delegateBoost() only checks balance once at delegation time, never re-validates

#### False Positive Guards

- Not this bug when: Protocol uses time-weighted voting with automatic decay in Bribe deposits
- Safe if: Epoch guard modifier (onlyNewEpoch) is applied to all vote/poke/claim paths
- Safe if: totalVoting is symmetrically updated in both deposit() and withdraw()
- Safe if: GaugeController tracks cumulative user weight and enforces sum ≤ WEIGHT_PRECISION
- Safe if: killGauge properly zeros gauge weight and excludes it from notifyRewardAmount distribution
- Requires attacker control of: veNFT (lock/vote timing), or ability to call poke() repeatedly, or knowledge of epoch boundary timing

---

## Section 1: Bribe Reward Theft & Epoch Accounting Exploits

### Root Cause

Bribe contracts distribute rewards based on voting checkpoints recorded per epoch. When the claim function does not verify that a tokenId actually voted during the epoch being claimed, or when deposit/withdraw accounting is asymmetric (deposit increments totalVoting but withdraw doesn't decrement it), attackers can steal bribes they never earned or inflate their share.

### Attack Scenario / Path Variants

**Path A: Claiming Bribes for Unvoted Epochs**
Path key: `missing_epoch_check | bribe_claim | Voter→Bribe | reward_theft`
Entry surface: `Voter.claimBribes() → Bribe.getRewardForOwner()`
Contracts touched: `Voter → Bribe`
Boundary crossed: `epoch boundary (timing)`
1. Alice votes in epoch 1, Bob votes in epoch 1
2. Epoch 2 starts — Alice claims epoch 1 bribes correctly
3. Bob votes in epoch 2, then claims epoch 1 bribes — this also resets his checkpoint
4. Alice calls claimBribes for epoch 2 — she did NOT vote in epoch 2 but `getRewardForOwner` reads her checkpoint balance from the previous recording and sends rewards
5. Bob tries to claim epoch 2 bribes → reverts with "transfer amount exceeds balance" — Alice stole his share
6. **Impact**: Protocol insolvency, honest voters cannot claim their earned bribes

**Path B: Deflating totalVoting to Inflate Bribe Share**
Path key: `missing_accounting_symmetry | bribe_deposit_withdraw | Voter→Bribe | totalVoting_desync`
Entry surface: `Voter.poke()` → `Bribe.withdraw()` + `Bribe.deposit()`
Contracts touched: `Voter → Bribe`
Boundary crossed: `internal (Voter ↔ Bribe state sync)`
1. Bribe.deposit() increments both `balanceOf[tokenId]` and `totalVoting`, writes voting checkpoint
2. Bribe.withdraw() decrements `balanceOf[tokenId]` but does NOT decrement `totalVoting` nor write a voting checkpoint
3. Attacker repeatedly calls poke() which triggers withdraw → deposit cycles
4. Each cycle: withdraw doesn't reduce totalVoting, but the new deposit checkpoint records lowered balance
5. Attacker exploits deflated totalVoting to claim disproportionate bribe rewards
6. **Impact**: Direct theft of bribe rewards from other voters, solvency issues

**Path C: Expired Lock Bribe Claims**
Path key: `missing_lock_validation | bribe_claim | Voter→Bribe→VotingEscrow | stale_reward_theft`
Entry surface: `Voter.claimBribes()`
Contracts touched: `Voter → Bribe → VotingEscrow`
Boundary crossed: `VotingEscrow lock expiry ↔ Bribe eligibility`
1. User creates a lock for minimum 1 epoch duration
2. Lock expires — user does NOT withdraw
3. User continues calling claimBribes() every epoch — function doesn't check lock expiry
4. **Impact**: Permanent reward drain using zero-power expired positions

### Vulnerable Pattern Examples

**Example 1: Missing Epoch Vote Check in Bribe Claim** [HIGH]
```solidity
// ❌ VULNERABLE: No check that tokenId voted in the target epoch
// Source: reports/vetoken_findings/claiming-bribes-for-epochs-you-didnt-vote-for-leading-to-protocol-insolvency.md
function getRewardForOwner(uint256 tokenId, address[] memory tokens) external {
    // Reads balance from previously recorded checkpoint
    // Does NOT verify tokenId actually voted in this epoch
    for (uint256 i = 0; i < tokens.length; i++) {
        uint256 _reward = earned(tokens[i], tokenId);
        if (_reward > 0) {
            lastEarn[tokens[i]][tokenId] = block.timestamp;
            _safeTransfer(tokens[i], msg.sender, _reward);
        }
    }
}
```

**Example 2: Asymmetric totalVoting in Deposit vs Withdraw** [HIGH]
```solidity
// ❌ VULNERABLE: deposit increments totalVoting, withdraw does not decrement it
// Source: reports/vetoken_findings/deflating-the-total-amount-of-votes-in-a-checkpoint-to-steal-bribes-and-create-s.md
function deposit(uint256 amount, uint256 tokenId) external {
    require(msg.sender == voter);
    totalSupply += amount;
    balanceOf[tokenId] += amount;
    totalVoting += amount;  // ← incremented
    _writeCheckpoint(tokenId, balanceOf[tokenId]);
    _writeSupplyCheckpoint();
    _writeVotingCheckpoint();
}

function withdraw(uint256 amount, uint256 tokenId) external {
    require(msg.sender == voter);
    totalSupply -= amount;
    balanceOf[tokenId] -= amount;
    // totalVoting NOT decremented ← BUG
    // No voting checkpoint written ← BUG
    _writeCheckpoint(tokenId, balanceOf[tokenId]);
    _writeSupplyCheckpoint();
}
```

**Example 3: Expired Lock Claiming Bribes** [HIGH]
```solidity
// ❌ VULNERABLE: No expiry check on lock before claiming bribes
// Source: reports/vetoken_findings/expired-locks-can-be-used-to-claim-rewards.md
function claimBribes(address[] memory _bribes, address[][] memory _tokens, uint256 _tokenId) external {
    require(IVotingEscrow(veALCX).isApprovedOrOwner(msg.sender, _tokenId));
    // Missing: require(IVotingEscrow(veALCX).lockEnd(_tokenId) > block.timestamp, "expired");
    for (uint256 i = 0; i < _bribes.length; i++) {
        IBribe(_bribes[i]).getRewardForOwner(_tokenId, _tokens[i]);
    }
}
```

---

## Section 2: Voting Power Manipulation & Lock Accounting Bugs

### Root Cause

VotingEscrow contracts manage veNFT positions with lock amount and duration tracking. Bugs in `increase()`, `merge()`, `split()`, and lock extension functions can inflate voting power, create positions with arbitrary amounts, or allow double voting through state desynchronization between the VotingEscrow and Voter contracts.

### Attack Scenario / Path Variants

**Path A: Double Voting Power via Lock Increase**
Path key: `missing_lock_validation | lock_increase | VotingEscrow | voting_power_inflation`
Entry surface: `VotingEscrow.increase()`
Contracts touched: `VotingEscrow (internal)`
1. User creates a lock with a small initial amount (e.g., 1 wei)
2. User calls increase() with the full amount they want to lock
3. `_lockState.increaseLock()` adds amount to lock — `userLock.amount` now includes the increase
4. `calculateAndUpdatePower()` is called with `userLock.amount + amount` — the increase is counted TWICE
5. `newBias = (existingAmount + increasedAmount * 2) * duration / MAX_LOCK_DURATION`
6. **Impact**: Nearly 2x the intended voting power and veToken minting

**Path B: Arbitrary Amount via Split Underflow**
Path key: `missing_lock_validation | lock_split | VotingEscrow | voting_power_inflation`
Entry surface: `VotingEscrow.split()`
Contracts touched: `VotingEscrow (internal)`
1. User has a veNFT with locked.amount = X
2. User calls split with _amount > X (or carefully chosen to exploit int128 behavior)
3. `_locked.amount = value - _splitAmount` underflows or creates unexpected value
4. `_locked.amount = _splitAmount` creates second NFT with full arbitrary amount
5. **Impact**: Free voting power creation, gauge/bribe manipulation

**Path C: Double Voting via carryVoteForward**
Path key: `missing_voted_flag | carry_vote_forward | Voter→VotingEscrow | double_vote`
Entry surface: `Voter.carryVoteForward()`
Contracts touched: `Voter → VotingEscrow`
Boundary crossed: `Voter voted flag ↔ VotingEscrow notVoted modifier`
1. Voter.carryVoteForward() reuses previous period votes for next period via internal _vote()
2. Function does NOT set `period[nextPeriod].voted[_tokenId] = true`
3. VotingEscrow.notVoted modifier checks `IVoter(voter).checkPeriodVoted()` — returns false
4. User can merge/split/withdraw/transfer the veNFT despite having active votes
5. **Impact**: Double voting, circumventing voting locks, governance manipulation

**Path D: Flashloan Voting Power Amplification**
Path key: `missing_lock_duration_check | increase_stake | VotingEscrow | flashloan_governance`
Entry surface: `VotingEscrow.increaseAndStake()`
Contracts touched: `VotingEscrow (internal)`
1. User has an expired lock position (lockUntil <= block.timestamp)
2. User flashloans a large amount of governance tokens
3. Calls increaseAndStake() — increases amount without requiring lock extension
4. Voting power formula still grants nonzero power even with zero remaining duration (1x base)
5. User executes governance proposal and votes in same transaction
6. Unstakes and repays flashloan
7. **Impact**: Single-transaction governance takeover

### Vulnerable Pattern Examples

**Example 4: Double-Count in Lock Increase** [HIGH]
```solidity
// ❌ VULNERABLE: amount is double-counted — added in increaseLock AND in calculateAndUpdatePower
// Source: reports/vetoken_findings/attackers-can-double-voting-power-and-vetoken-amount-by-locking-and-increasing.md
function increase(uint256 amount) external {
    _lockState.increaseLock(msg.sender, amount);  // amount already added to lock
    _updateBoostState(msg.sender, locks[msg.sender].amount);

    LockManager.Lock memory userLock = _lockState.locks[msg.sender];
    (int128 newBias, int128 newSlope) = _votingState.calculateAndUpdatePower(
        msg.sender,
        userLock.amount + amount,  // ← amount added AGAIN
        userLock.end
    );
}
```

**Example 5: Split Without Amount Validation** [HIGH]
```solidity
// ❌ VULNERABLE: No check that _amount <= locked.amount, allows arbitrary veNFT creation
// Source: reports/vetoken_findings/c-01-split-can-be-abused-to-create-locked-data-with-an-arbitrary-amount.md
function split(uint _from, uint _amount) external returns (uint _tokenId1, uint _tokenId2) {
    require(_isApprovedOrOwner(msg.sender, _from));
    require(_amount > 0, "Zero Split");

    LockedBalance memory _locked = locked[_from];
    int128 value = _locked.amount;
    locked[_from] = LockedBalance(0, 0);
    _checkpoint(_from, _locked, LockedBalance(0, 0));
    _burn(_from);

    int128 _splitAmount = int128(uint128(_amount));
    _locked.amount = value - _splitAmount;  // ← can underflow with int128
    _tokenId1 = _createSplitNFT(msg.sender, _locked);

    _locked.amount = _splitAmount;          // ← arbitrary amount NFT
    _tokenId2 = _createSplitNFT(msg.sender, _locked);
}
```

---

## Section 3: Gauge Voting & Emission Distribution Exploits

### Root Cause

GaugeController contracts allow users to allocate voting weight across gauges to direct token emissions. Failures include: not tracking cumulative user weight across gauges (allowing over-allocation), not handling killed gauges properly (allowing dead gauges to steal emissions), and gauge weight formula errors that cause underflow when voting power changes.

### Attack Scenario / Path Variants

**Path A: Gauge Over-Voting (No Cumulative Weight Tracking)**
Path key: `missing_weight_tracking | gauge_vote | GaugeController→Gauge | emission_misallocation`
Entry surface: `GaugeController.vote()`
Contracts touched: `GaugeController → Gauge`
1. GaugeController.vote() allows setting weight per gauge but doesn't track total weight across all gauges
2. User votes 100% weight on gauge A, then 100% weight on gauge B
3. Total allocated: 200% of their voting power
4. **Impact**: Emission misallocation, unfair reward distribution, governance manipulation

**Path B: Killed Gauge Steals Emissions**
Path key: `missing_killed_check | gauge_distribution | Voter→Minter→Gauge | reward_theft_from_active_gauges`
Entry surface: `Voter.distribute()` / `Voter.updateFor()`
Contracts touched: `Voter → Minter → killed Gauge`
Boundary crossed: `Voter claimable accounting ↔ gauge alive/killed state`
1. Admin calls killGauge() — sets `isAlive[gauge] = false`
2. killGauge() does NOT delete `claimable[gauge]` or zero the gauge's weight
3. Minter emissions continue accruing to killed gauge via updateFor()
4. Already-accrued claimable is never redistributed to active gauges
5. **Impact**: Active gauges receive fewer rewards; killed gauge's share is effectively stolen or locked

**Path C: Gauge Weight Underflow on Power Change**
Path key: `stale_voting_power | gauge_vote | GaugeController | arithmetic_underflow_dos`
Entry surface: `GaugeController.vote()`
Contracts touched: `GaugeController (internal)`
1. User votes with weight=100 and votingPower=100000e18 → gaugeWeight = 1000e18
2. User's veToken balance increases to 10_000_000e18 (new lock or time)
3. User re-votes with weight=5000
4. Formula: `newWeight = oldWeight - (oldVoteWeight * currentPower / PRECISION) + (newVoteWeight * currentPower / PRECISION)`
5. Subtraction underflows because currentPower >> original power when vote was cast
6. **Impact**: DoS — user cannot change vote; gauge weight becomes corrupted

### Vulnerable Pattern Examples

**Example 6: No Cumulative Weight Tracking** [HIGH]
```solidity
// ❌ VULNERABLE: No check that total user weight across all gauges <= WEIGHT_PRECISION
// Source: reports/vetoken_findings/gauge-voting-misallocation-vulnerability.md
function vote(address gauge, uint256 weight) external override whenNotPaused {
    if (!isGauge(gauge)) revert GaugeNotFound();
    if (weight > WEIGHT_PRECISION) revert InvalidWeight();  // per-gauge check only

    uint256 votingPower = veRAACToken.balanceOf(msg.sender);
    if (votingPower == 0) revert NoVotingPower();

    uint256 oldWeight = userGaugeVotes[msg.sender][gauge];
    userGaugeVotes[msg.sender][gauge] = weight;
    // Missing: totalUserWeight[msg.sender] tracking and enforcement
    _updateGaugeWeight(gauge, oldWeight, weight, votingPower);
}
```

**Example 7: Killed Gauge Still Accrues Rewards** [HIGH]
```solidity
// ❌ VULNERABLE: updateFor does not check isAlive before accruing claimable rewards
// Source: reports/vetoken_findings/killed-gauge-continue-to-accrue-and-steal-rewards-from-minter-contract.md
function notifyRewardAmount(uint256 amount) external {
    require(msg.sender == minter);
    require(totalWeight > 0);
    _safeTransferFrom(base, msg.sender, address(this), amount);
    uint256 _ratio = (amount * 1e18) / totalWeight;  // totalWeight includes killed gauges
    index += _ratio;
}

function _updateFor(address _gauge) internal {
    uint256 _supplied = weights[_gauge];  // killed gauge still has weight
    uint256 _delta = index - supplyIndex[_gauge];
    claimable[_gauge] += (_supplied * _delta) / 1e18;  // keeps accruing
    supplyIndex[_gauge] = index;
}
```

---

## Section 4: Poke Function Exploits

### Root Cause

The `poke()` function updates a user's vote weights based on their current (potentially decayed) veNFT balance. When `poke()` lacks the same access control modifiers as `vote()` (e.g., `onlyNewEpoch`), it can be called repeatedly within an epoch to trigger side effects like flux token minting, totalVoting inflation in Bribe contracts, or voting weight manipulation.

### Attack Scenario / Path Variants

**Path A: Unlimited Flux Token Minting via Poke**
Path key: `missing_access_control | poke_function | Voter→FluxToken | unlimited_token_minting`
Entry surface: `Voter.poke()`
Contracts touched: `Voter → FluxToken`
1. vote() and reset() have `onlyNewEpoch` modifier — can only be called once per epoch
2. poke() calls internal `_vote()` which calls `FluxToken.accrueFlux()`
3. poke() does NOT have `onlyNewEpoch` modifier
4. Attacker calls poke() repeatedly within same epoch
5. Each call accrues flux tokens for the tokenId
6. **Impact**: Unlimited FLUX minting, breaking `"user should never claim more rewards than earned"` invariant

**Path B: totalVoting Inflation via Repeated Poke**
Path key: `missing_accounting_symmetry | poke_repeated | Voter→Bribe | totalVoting_inflation`
Entry surface: `Voter.poke()`
Contracts touched: `Voter → Bribe`
1. poke() calls Bribe.withdraw() then Bribe.deposit()
2. If withdraw doesn't decrement totalVoting but deposit does increment it (Section 1 Path B)
3. Each poke() inflates totalVoting by the vote amount
4. Results in other voters' rewards being diluted
5. **Impact**: Permanent fund freeze in Bribe, incorrect reward distribution for all participants

**Path C: Dust Vote Prevents Poke (DoS)**
Path key: `missing_dust_guard | poke_function | Voter→Gauge | dos_via_dust`
Entry surface: `Voter.poke()`
Contracts touched: `Voter → Gauge`
1. Attacker votes full weight minus 1 wei on pool A, 1 wei on pool B
2. Becomes inactive, letting ve weight decay
3. When someone tries to poke() the attacker to update decayed weight, the dust vote on pool B causes revert (division or rounding issues)
4. **Impact**: Attacker retains inflated vote weight forever, unpokeable

### Vulnerable Pattern Examples

**Example 8: Poke Without Epoch Guard** [HIGH]
```solidity
// ❌ VULNERABLE: poke() lacks onlyNewEpoch modifier, can be called repeatedly
// Source: reports/vetoken_findings/lack-of-access-control-in-poke-function-allows-in-unlimited-minting-of-flux-toke.md
function poke(uint256 _tokenId) public {
    // Missing: onlyNewEpoch(_tokenId) modifier
    address[] memory _poolVote = poolVote[_tokenId];
    uint256[] memory _weights = new uint256[](_poolVote.length);
    for (uint256 i = 0; i < _poolVote.length; i++) {
        _weights[i] = votes[_tokenId][_poolVote[i]];
    }
    _vote(_tokenId, _poolVote, _weights, _boost);  // calls accrueFlux internally
}
```

---

## Section 5: Boost Mechanism Exploits

### Root Cause

Boost controllers calculate reward multipliers based on veToken holdings. Bugs include: delegation only checking balance at delegation time (not ongoing), broken math that always returns maximum boost, and hardcoded values that exclude small holders.

### Attack Scenario / Path Variants

**Path A: Unbacked Boost via Withdraw After Delegation**
Path key: `missing_ongoing_collateral_check | boost_delegation | BoostController→VotingEscrow | unbacked_boost`
Entry surface: `BoostController.delegateBoost()`
Contracts touched: `BoostController → VotingEscrow`
Boundary crossed: `BoostController state ↔ VotingEscrow balance`
1. User has veTokens and calls delegateBoost(to, amount, duration)
2. Contract checks user's veToken balance ≥ amount at delegation time
3. User immediately withdraws or reduces their veToken lock
4. Delegation persists for entire duration with full amount — no re-validation
5. **Impact**: Unbacked boost inflates rewards for delegate; breaks reward distribution fairness

**Path B: Always-Max Boost Multiplier**
Path key: `flawed_math | boost_calculation | BoostController | maximum_boost_always`
Entry surface: `BoostController.getBoostMultiplier()`
Contracts touched: `BoostController (internal)`
1. `baseAmount = userBoost.amount * 10000 / MAX_BOOST`
2. `result = userBoost.amount * 10000 / baseAmount`
3. Algebraically simplifies to `result = MAX_BOOST` for any nonzero amount
4. **Impact**: Every user gets maximum boost regardless of actual contribution; incentive structure broken

### Vulnerable Pattern Examples

**Example 9: Unbacked Boost Delegation** [MEDIUM]
```solidity
// ❌ VULNERABLE: Balance only checked once at delegation time, never re-validated
// Source: reports/vetoken_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md
function delegateBoost(address to, uint256 amount, uint256 duration) external {
    uint256 userBalance = veRAACToken.balanceOf(msg.sender);
    if (userBalance < amount) revert InsufficientVeBalance();  // one-time check
    delegation.amount = amount;
    delegation.expiry = block.timestamp + duration;
    // After this: user can withdraw veTokens, delegation persists unbacked
}
```

**Example 10: Always-Maximum Boost Math** [MEDIUM]
```solidity
// ❌ VULNERABLE: Math simplifies to always returning MAX_BOOST for any nonzero amount
// Source: reports/vetoken_findings/flawed-boost-multiplier-calculation-always-yields-maximum-boost.md
function getBoostMultiplier(address user, address pool) external view returns (uint256) {
    if (!supportedPools[pool]) revert PoolNotSupported();
    UserBoost storage userBoost = userBoosts[user][pool];
    if (userBoost.amount == 0) return MIN_BOOST;
    uint256 baseAmount = userBoost.amount * 10000 / MAX_BOOST;
    return userBoost.amount * 10000 / baseAmount;  // always == MAX_BOOST
}
```

---

## Section 6: Reward & Emission Distribution Bugs

### Root Cause

Minter → Voter → Gauge reward pipelines can fail when: distribution functions don't track per-gauge amounts already sent, epoch ordering between minter.updatePeriod() and distribute() is wrong, gauge.notifyRewardAmount() returns false but claimable is already zeroed, or reward rate calculations lose rollover rewards.

### Attack Scenario / Path Variants

**Path A: Repeated distributeEx Drains All Rewards**
Path key: `missing_distribution_tracking | distributeEx | Voter→Gauge | reward_theft`
Entry surface: `Voter.distributeEx(start, finish)`
Contracts touched: `Voter → Gauge`
1. distributeEx() distributes rewards to gauges based on weight ratios
2. If a gauge's notifyRewardAmount() returns false, claimable is added back
3. Attacker calls distributeEx() with only their gauge repeatedly
4. Each call re-dispatches from remaining balance, compounding their gauge's share
5. **Impact**: Single gauge steals almost all rewards

**Path B: First-Epoch Emissions Stuck Forever**
Path key: `missing_ordering_check | distribute_before_updatePeriod | Voter→Minter | emission_loss`
Entry surface: `Voter.distribute()`
Contracts touched: `Voter → Minter`
1. distribute() is called before minter.updatePeriod() in the first epoch
2. Emissions for epoch 1 are sent to Voter but cannot be distributed to gauges
3. No mechanism to recover or redistribute stuck emissions
4. **Impact**: Permanent loss of first-epoch rewards

**Path C: Rollover Rewards Lost in Reward Rate**
Path key: `flawed_rewardrate | reward_rollover | Gauge | emission_loss`
Entry surface: `Gauge.notifyRewardAmount()`
Contracts touched: `Gauge (internal)`
1. When new rewards are notified mid-period, leftover from previous period should roll over
2. Flawed calculation: `rewardRate = reward / duration` — discards unfinished period's remaining amount
3. **Impact**: Accumulated rollover rewards permanently lost

### Vulnerable Pattern Examples

**Example 11: Repeated distributeEx Theft** [HIGH]
```solidity
// ❌ VULNERABLE: No tracking of already-distributed amounts per gauge per epoch
// Source: reports/vetoken_findings/all-reward-tokens-can-be-stolen-by-an-attacker-due-to-misaccounting-in-distribut.md
function distributeEx(address token, uint start, uint finish) public {
    for (uint x = start; x < finish; x++) {
        address _gauge = allGauges[x];
        uint256 _claimable = claimable[_gauge];
        claimable[_gauge] = 0;
        if (!IGauge(_gauge).notifyRewardAmount(token, _claimable)) {
            claimable[_gauge] = _claimable;  // put back if failed
            // Can be called again with same gauge to repeat distribution
        }
    }
}
```

**Example 12: Gauge Staking Gamed via Repeated Stake/Withdraw** [HIGH]
```solidity
// ❌ VULNERABLE: No minimum staking period or time-weighted balance
// Source: reports/vetoken_findings/gauge-reward-system-can-be-gamed-with-repeatedly-stakewithdraw.md
function stake(uint256 amount) external nonReentrant updateReward(msg.sender) {
    if (amount == 0) revert InvalidAmount();
    _totalSupply += amount;
    _balances[msg.sender] += amount;  // instant full balance
    stakingToken.safeTransferFrom(msg.sender, address(this), amount);
}

function withdraw(uint256 amount) external nonReentrant updateReward(msg.sender) {
    if (amount == 0) revert InvalidAmount();
    _totalSupply -= amount;
    _balances[msg.sender] -= amount;  // instant withdrawal
    stakingToken.safeTransfer(msg.sender, amount);
}
```

---

## Section 7: Checkpoint & Voting Power Decay Bugs

### Root Cause

VotingEscrow uses checkpoint systems to record point-in-time voting power that decays linearly over lock duration. Bugs include: block slope rounding errors that prevent checkpoint block number updates, stale voting power used in gauge weight calculations, and lack of automatic decay propagation to Bribe deposit records.

### Attack Scenario / Path Variants

**Path A: Checkpoint Block Number Never Updates**
Path key: `rounding_error | checkpoint | VotingEscrow | stale_block_reference`
Entry surface: `VotingEscrow._checkpoint()`
Contracts touched: `VotingEscrow (internal)`
1. Block slope calculation: `blockSlope = (MULTIPLIER * (block.number - lastPoint.blk)) / (block.timestamp - lastPoint.ts)`
2. MULTIPLIER = 2, block time ~12 seconds → numerator < denominator → blockSlope = 0
3. `lastPoint.blk = initialLastPoint.blk + (blockSlope * deltaTime) / MULTIPLIER` → never changes
4. **Impact**: All checkpoint point.blk values are stale; any logic depending on block-based lookups is broken

**Path B: Non-Decaying Bribe Deposits**
Path key: `missing_balance_decay | poke_voting | VotingEscrow→Voter→Bribe | inflated_rewards`
Entry surface: `Voter.vote()` (initial), then passive
Contracts touched: `VotingEscrow → Voter → BribeVotingReward`
1. User votes once after creating lock — Bribe records full veNFT balance as deposit amount
2. veNFT balance decays linearly over time, but Bribe deposit does NOT auto-decay
3. User avoids re-voting in subsequent epochs to keep inflated deposit weight
4. User calls poke() on others to lower THEIR weight while keeping own weight high
5. **Impact**: Unfair reward distribution — passive voters earn more than active contributors

### Vulnerable Pattern Examples

**Example 13: Block Slope Rounding to Zero** [MEDIUM]
```solidity
// ❌ VULNERABLE: MULTIPLIER=2 is too small — blockSlope always rounds to zero
// Source: reports/vetoken_findings/checkpoints-wont-update-block-number-in-point-because-of-a-rounding-issue.md
function _checkpoint(...) internal {
    // block time ~12s: MULTIPLIER * 1 / 12 = 2/12 = 0
    blockSlope = (MULTIPLIER * (block.number - lastPoint.blk)) / (block.timestamp - lastPoint.ts);
    // ...
    lastPoint.blk = initialLastPoint.blk + (blockSlope * (_time - initialLastPoint.ts)) / MULTIPLIER;
    // lastPoint.blk NEVER changes because blockSlope = 0
}
```

---

## Section 8: Delegation & NFT Operation Exploits

### Root Cause

veNFT-based systems allow delegation, merging, and managed deposits. When these operations don't properly interact with voting state or impose gas limits, they enable DoS attacks via delegate flooding, extraction of unvested rebase rewards, or broken accounting from expired-position operations.

### Attack Scenario / Path Variants

**Path A: MAX_DELEGATES DoS**
Path key: `missing_delegate_limit | delegation | VotingEscrow | dos_gas_limit`
Entry surface: `VotingEscrow.delegate()`
1. Attacker creates 1024 (MAX_DELEGATES) small veNFTs and delegates them all to a target
2. Target's transfer/withdraw operations must iterate through all delegations
3. On chains with <25M gas limit (e.g., Optimism at 15M), operations revert
4. **Impact**: Permanent freezing of target's veNFTs

**Path B: Managed Lock Extracts Unvested Rebase Rewards**
Path key: `missing_vesting_check | deposit_managed | VotingEscrow→RewardsDistributor | unvested_reward_theft`
Entry surface: `VotingEscrow.depositManaged()`
Contracts touched: `VotingEscrow → RewardsDistributor`
1. RewardsDistributor.claim() sends rewards via depositFor if lock is active, or transfers directly if expired
2. depositManaged() changes lock state such that the expiry check passes for non-expired locks
3. User calls depositManaged → claim extracts unvested VELO as direct transfer
4. **Impact**: Extraction of unvested rebase rewards every other week

### Vulnerable Pattern Examples

**Example 14: Extending Expired Position Breaks Accounting** [MEDIUM]
```solidity
// ❌ VULNERABLE: Extending expired position uses wrong dailyUnlockedAmounts key
// Source: reports/vetoken_findings/extending-the-duration-of-an-expired-position-can-break-protocol-accounting.md
function _extendDuration(uint256 lockId, uint256 newDuration) internal {
    LockedPosition storage lock = locks[lockId];
    if (block.timestamp >= lock.expiry) {
        // Uses incorrect mapping key for dailyUnlockedAmounts
        // Breaks protocol accounting for daily reward calculations
        dailyUnlockedAmounts[lock.expiry] -= lock.amount;  // wrong key when expired
    }
    lock.expiry = block.timestamp + newDuration;
}
```

---

## Impact Analysis

### Technical Impact
- **Bribe insolvency**: Legitimate voters unable to claim earned bribes when attackers drain the pool (Common — 8/30 unique findings)
- **Emission misallocation**: Gauges receive incorrect share of token emissions (Common — 6/30 unique findings)
- **Voting power inflation**: Users obtain more governance power than their lock justifies (Common — 5/30 unique findings)
- **Protocol accounting corruption**: totalVoting, gauge weights, or checkpoint data become permanently desynchronized (Common — 7/30 unique findings)
- **DoS via gas exhaustion**: veNFT operations become impossible on limited-gas chains (Moderate — 2/30 unique findings)

### Business Impact
- **Financial**: Direct theft of bribe rewards and emission tokens; Alchemix, ZeroLend, Velodrome, RAAC all affected
- **Governance integrity**: Inflated voting power enables malicious proposals; flashloan attacks enable single-tx governance takeover
- **Trust**: Users lose confidence when earned rewards are stolen or emissions are misallocated

### Affected Scenarios
- All Solidly/ve(3,3) forks: Velodrome, Aerodrome, Thena, Fenix, etc.
- All Curve-style gauge systems with veToken voting
- Any protocol using epoch-based bribe distribution with checkpoint-based claims
- Managed veNFT systems (Velodrome v2+)
- Protocols with boost delegation mechanics

---

## Secure Implementation

**Fix 1: Epoch-Validated Bribe Claims**
```solidity
// ✅ SECURE: Verify tokenId voted in the epoch before allowing claims
function claimBribes(address[] memory _bribes, address[][] memory _tokens, uint256 _tokenId) external {
    require(IVotingEscrow(veALCX).isApprovedOrOwner(msg.sender, _tokenId));
    require(IVotingEscrow(veALCX).lockEnd(_tokenId) > block.timestamp, "token expired");
    for (uint256 i = 0; i < _bribes.length; i++) {
        IBribe(_bribes[i]).getRewardForOwner(_tokenId, _tokens[i]);
    }
}
```

**Fix 2: Symmetric Bribe Accounting**
```solidity
// ✅ SECURE: Both deposit and withdraw update totalVoting and write checkpoints
function withdraw(uint256 amount, uint256 tokenId) external {
    require(msg.sender == voter);
    totalSupply -= amount;
    balanceOf[tokenId] -= amount;
    totalVoting -= amount;  // ← properly decremented
    _writeCheckpoint(tokenId, balanceOf[tokenId]);
    _writeSupplyCheckpoint();
    _writeVotingCheckpoint();  // ← voting checkpoint written
}
```

**Fix 3: Cumulative Gauge Weight Tracking**
```solidity
// ✅ SECURE: Track and enforce total user weight across all gauges
function vote(address gauge, uint256 weight) external override whenNotPaused {
    if (!isGauge(gauge)) revert GaugeNotFound();
    uint256 votingPower = veRAACToken.balanceOf(msg.sender);
    if (votingPower == 0) revert NoVotingPower();

    uint256 oldWeight = userGaugeVotes[msg.sender][gauge];
    totalUserWeight[msg.sender] = totalUserWeight[msg.sender] - oldWeight + weight;
    require(totalUserWeight[msg.sender] <= WEIGHT_PRECISION, "exceeds total weight");
    userGaugeVotes[msg.sender][gauge] = weight;
    _updateGaugeWeight(gauge, oldWeight, weight, votingPower);
}
```

---

## Detection Patterns

### Contract / Call Graph Signals
```
- Bribe.deposit() and Bribe.withdraw() with asymmetric state updates (totalVoting, checkpoints)
- poke() without epoch guard modifier while vote() has one
- GaugeController.vote() without cumulative weight tracking per user
- killGauge() that doesn't zero gauge weight or exclude from distribution
- VotingEscrow.increase() adding amount to already-increased lock state
- BoostController delegation without ongoing balance re-validation
- distributeEx() callable with arbitrary (start, finish) without per-epoch distribution tracking
```

### High-Signal Grep Seeds
```
- totalVoting
- claimBribes
- getRewardForOwner
- poke
- killGauge
- accrueFlux
- onlyNewEpoch
- _writeVotingCheckpoint
- distributeEx
- notifyRewardAmount
- delegateBoost
- balanceOfNFT
- _checkpoint
- blockSlope
- MULTIPLIER
- MAX_DELEGATES
- depositManaged
- carryVoteForward
```

### Code Patterns to Look For
```
- Pattern 1: Bribe.withdraw() missing `totalVoting -= amount` while deposit() has `totalVoting += amount`
- Pattern 2: poke() calling _vote() or accrueFlux() without onlyNewEpoch modifier
- Pattern 3: GaugeController allowing vote() on multiple gauges without cumulative weight cap
- Pattern 4: killGauge() only setting isAlive=false without touching weights or claimable
- Pattern 5: VotingEscrow.increase() passing (userLock.amount + amount) after amount already added to lock
- Pattern 6: split() not validating _amount <= locked.amount
- Pattern 7: Boost multiplier math that algebraically simplifies to a constant
- Pattern 8: Checkpoint blockSlope with MULTIPLIER too small for block time (e.g., 2 for 12s blocks)
```

### Audit Checklist
- [ ] Verify Bribe.deposit() and Bribe.withdraw() symmetrically update totalVoting and write checkpoints
- [ ] Verify claimBribes checks that tokenId voted in the claimed epoch AND lock is not expired
- [ ] Verify poke() has same epoch guard as vote()
- [ ] Verify GaugeController tracks cumulative user weight across all gauges <= 100%
- [ ] Verify killGauge() zeros gauge weight and excludes from emission distribution
- [ ] Verify VotingEscrow.increase() does not double-count added amount
- [ ] Verify split() validates amount <= locked.amount
- [ ] Verify BoostController re-validates delegator's veToken balance on claim/use
- [ ] Verify distributeEx() tracks per-gauge per-epoch distribution amounts
- [ ] Verify checkpoint MULTIPLIER is large enough to produce nonzero blockSlope
- [ ] Verify delegation count is bounded reasonably for target chain gas limit
- [ ] Verify rebase claim path handles managed/deposited locks correctly

---

## Real-World Examples

### Known Exploits & Audit Findings
- **Alchemix v2 DAO** — Bribe epoch claim theft + totalVoting desync + poke unlimited flux + killed gauge reward steal — Immunefi Bug Bounty (2024)
- **Velodrome Finance** — Non-decaying bribe deposits + rebase unvested extraction + bribe-emission desync — Spearbit Security Review
- **ZeroLend** — distributeEx reward theft + distribution logic bugs — Immunefi Bug Bounty (2024)
- **RAAC/Cyfrin** — Double voting power on increase + gauge weight underflow + always-max boost — Codehawks (2025)
- **KittenSwap** — carryVoteForward double voting + split arbitrary amount — Pashov Audit Group (2025)
- **Fenix Finance** — killGauge emission calculation errors — Code4rena (2024)
- **Curve DAO** — Duplicate gauge addition weight corruption — Trail of Bits
- **Lisk** — Expired position extension breaks accounting — Trail of Bits (2024)
- **Guanciale Stake** — Flashloan voting power amplification — Shieldify
- **Hybra Finance** — Dust vote prevents poke DoS — Code4rena (2025)

---

## Prevention Guidelines

### Development Best Practices
1. Always update totalVoting, checkpoints, and balances symmetrically in deposit/withdraw pairs
2. Apply epoch guard modifiers (onlyNewEpoch) to ALL functions that trigger reward accrual or vote state changes
3. Track cumulative gauge weight per user and enforce sum ≤ WEIGHT_PRECISION (typically 10000)
4. On killGauge: zero the gauge weight, exclude from totalWeight, and redistribute or burn accrued claimable
5. In VotingEscrow.increase(): pass only the NEW total amount, not (total + increment)
6. Validate split amount boundaries: `require(_amount > 0 && _amount <= uint256(int256(locked.amount)))`
7. Re-validate delegator's veToken balance when boost is consumed, not only at delegation time
8. Use MULTIPLIER ≥ 10000 for checkpoint block slope calculations
9. Cap MAX_DELEGATES to a value safe for the target chain's gas limit (128 for L2s)
10. Implement time-weighted average balances for gauge staking to prevent flash-stake attacks

### Testing Requirements
- Unit tests for: Bribe claim with unvoted epochs, expired locks, repeated poke within epoch
- Integration tests for: killGauge → distribute → active gauge reward integrity
- Fuzz tests for: split amount boundaries, gauge weight arithmetic across power changes, delegation + withdrawal sequences
- Invariant tests for: `sum(balanceOf) == totalVoting in Bribe`, `sum(userGaugeWeights) <= WEIGHT_PRECISION`, `killed gauge claimable == 0`

---

## Keywords for Search

`vetoken`, `voting escrow`, `veNFT`, `ve3,3`, `solidly`, `velodrome`, `aerodrome`, `curve gauge`, `gauge controller`, `gauge weight`, `bribe`, `bribe claim`, `totalVoting`, `epoch`, `checkpoint`, `poke`, `killGauge`, `boost`, `boost delegation`, `boost multiplier`, `lock duration`, `lock increase`, `merge`, `split`, `voting power decay`, `rebase`, `emission distribution`, `distributeEx`, `notifyRewardAmount`, `reward rate`, `flux token`, `accrueFlux`, `managed deposit`, `delegate`, `MAX_DELEGATES`, `blockSlope`, `MULTIPLIER`, `carryVoteForward`, `double voting`, `expired lock`, `protocol insolvency`, `reward theft`, `governance manipulation`

---

## Related Vulnerabilities

- [DB/general/dao-governance/](../../general/) — DAO governance manipulation patterns
- [DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md](../../tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md) — Vault share accounting (related reward distribution)
- [DB/general/perpetuals-derivatives/PERPETUALS_DERIVATIVES_VULNERABILITIES.md](../../general/perpetuals-derivatives/PERPETUALS_DERIVATIVES_VULNERABILITIES.md) — Fee/reward distribution patterns
