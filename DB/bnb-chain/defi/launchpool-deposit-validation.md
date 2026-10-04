---
# Core Classification
protocol: bscstation-startpools
chain: bsc
category: business_logic
vulnerability_type: internal_ledger_desync

# Pattern Identity
root_cause_family: dual_ledger_without_transfer_hook
pattern_key: unhooked_lp_transfer | staking LP token | ERC20 transfer of position | withdraw blocked and rewards lost

# Interaction Scope
interaction_scope: single_contract_family
involved_contracts:
  - BSCSBaseStartPool (inherits ERC20 "BSCS-BSCS"; deposit()/withdraw() with userInfo.amount + _mint/_burn)
  - MasterChef-style reward accounting (accTokenPerShare[], rewardDebt[], _updatePool(), addRewardToken(), updateRewardPerBlock())
path_keys:
  - unhooked_lp_transfer | transfer()/transferFrom() on LP | _transfer not overridden -> userInfo.amount desync -> withdraw() revert
  - reward_config_without_checkpoint | addRewardToken/updateRewardPerBlock | missing _updatePool() -> unfair reward distribution
  - non_reverting_unsafe_transfer | raw transfer() calls | ZRX/USDT-style tokens -> silent failure or revert
  - unvalidated_admin_args | updateUnstakingFee/updateFeeCollector | fee > 10000 or 0x0 collector -> withdraw revert or fee loss

# Attack Vector Details
attack_type: logical_error
affected_component: staking position accounting + multi-token reward accrual

# Technical Primitives
primitives:
  - erc20_inherited_position_token
  - userInfo_amount_shadow_ledger
  - accTokenPerShare_checkpoint
  - rewardDebt_migration_on_transfer
  - non_compliant_erc20_returns
  - precision_factor_per_token
  - fee_bps_validation

# Grep / Hunt-Card Seeds
code_keywords:
  - BSCSBaseStartPool
  - userInfo
  - accTokenPerShare
  - rewardDebt
  - _updatePool
  - addRewardToken
  - updateRewardPerBlock
  - updateUnstakingFee
  - updateFeeCollector
  - unStakingFee
  - safeERC20Transfer
  - collectFee
  - emergencyWithdraw
  - recoverWrongTokens
  - poolCap
  - poolLimitPerUser

# Impact Classification
severity: medium
impact: fund_lock|reward_theft|dos
financial_impact: medium

# Context Tags
tags:
  - masterchef
  - staking-pool
  - lp-token
  - erc20-position
  - reward-accrual
  - checkpoint
  - deflationary-token
  - launchpad
  - bscstation
  - peckshield

# Version Info
language: solidity
version: "audited commit 56bc0d3 (2021); fixes to 1dd2057 (+7d905b7 for _updatePool in addRewardToken)"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [peckshield-bscs] | reports/bnb-chain_findings/publications-audit-reports-peckshield-audit-report-bscstationstartpools-v1-0-pdf.md | MEDIUM | PeckShield | PeckShield Report #2021-301, Oct 8 2021 |
| [peckshield-pink] | reports/bnb-chain_findings/publications-audit-reports-peckshield-audit-report-pinksale-subscriptionpool-v1-0-pdf.md | LOW | PeckShield | PeckShield Report #2022-348 (deflationary-token sibling finding) |
| [q1] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-bscex-launchpadx-smartcontract-report-halborn-v1-pdf.md | LOW | Halborn | MISSING ADDRESS CHECK (bscex launchpadx v1) |
| [q2] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-bscex-launchpadx-smartcontract-report-halborn-v1-pdf.md | INFO | Halborn | IGNORE RETURN VALUES (bscex launchpadx v1) |
| [q3] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-bscex-launchpadx-smartcontract-report-halborn-v1-pdf.md | INFO | Halborn | STATIC ANALYSIS findings (bscex launchpadx v1) |
| [q4] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-bscex-launchpoolx-smartcontract-report-halborn-v1-pdf.md | LOW | Halborn | (HAL-01) FLOATING PRAGMA (bscex launchpoolx v1) |
| [q5] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-bscex-launchpoolx-smartcontract-report-halborn-v1-pdf.md | LOW | Halborn | (HAL-02) PRAGMA VERSION DEPRECATED (bscex launchpoolx v1) |
| [q6] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-bscex-launchpoolx-smartcontract-report-halborn-v1-pdf.md | LOW | Halborn | (HAL-03) FOR LOOP OVER DYNAMIC ARRAY (bscex launchpoolx v1) |
| [q7] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-bscex-launchpoolx-smartcontract-report-halborn-v1-pdf.md | LOW | Halborn | (HAL-04) IGNORE RETURN VALUES (bscex launchpoolx v1) |
## Launchpool/Staking-Pool Deposit Validation & Dual-Ledger Sync (BSCStation Start Pools)

**ERC20-inherited staking position token with unhooked transfers desyncs the userInfo ledger** — moving the LP token via plain `transfer()` does not move `userInfo[addr].amount` or migrate `rewardDebt`, so withdrawals revert and rewards strand; reward-config admin calls skip `_updatePool()` checkpoints, enabling unfair distribution.

### Overview

BSCStation's `BSCSBaseStartPool` mints an ERC20 LP token on `deposit()` and tracks stakes in a parallel MasterChef-style `userInfo.amount` ledger. Because `_transfer()` is never overridden, transferring the LP token leaves the shadow ledger pointing at the old owner: neither party can withdraw the underlying, and reward debt is never migrated. PeckShield rates the class Medium (likelihood Low / impact High).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the staking receipt is a transferable ERC20 but the authoritative stake ledger (`userInfo.amount`, `rewardDebt`) is a separate mapping updated only in deposit/withdraw — `transfer()` moves the token without moving the ledger, so `_burn(msg.sender, _amount)` in withdraw() reverts for the recipient and rewards accrued by the transferred stake are lost/stranded"
- Pattern key: `unhooked_lp_transfer | staking LP token | ERC20 transfer of position | withdraw blocked and rewards lost`
- Interaction scope: `single_contract_family`
- Primary affected component(s): `BSCSBaseStartPool deposit/withdraw/_transfer, reward config admin fns`
- Contracts / modules involved: `BSCSBaseStartPool (+ inherited ERC20), MasterChef reward math`
- Path keys: see frontmatter `path_keys`
- High-signal code keywords: `userInfo`, `accTokenPerShare`, `rewardDebt`, `_updatePool`, `unStakingFee`
- Typical sink / impact: `withdraw() permanent revert for LP recipient / reward loss / admin-config DoS`
- Validation strength: `strong` (PeckShield line-cited; fix commit 1dd2057 overrides `_transfer`)

#### Contract / Boundary Map

- Entry surface(s): `deposit(_amount)`, `withdraw(_amount)`, inherited `transfer()/transferFrom()`, admin `addRewardToken/updateRewardPerBlock/updateUnstakingFee/updateFeeCollector`
- Contract hop(s): `user A --transfer(LP)--> user B`; `B.withdraw -> require(user.amount >= _amount) fails or _burn(B) underflows`
- Trust boundary crossed: `ERC20 public transfer surface → position ownership semantics`; `owner admin config → user payout math`
- Shared state or sync assumption: `ERC20 LP balance[addr] must mirror userInfo[addr].amount and rewardDebt at all times; accTokenPerShare must checkpoint before ANY reward-parameter mutation`

#### Valid Bug Signals

- Signal 1: Contract inherits/mints an ERC20 whose balances represent staked positions, and no `_transfer`/`_beforeTokenTransfer` hook updates the staking ledger or reward debt
- Signal 2: `withdraw()` does `_burn(msg.sender, _amount)` gated by `userInfo[msg.sender].amount` — any balance/ledger divergence is a revert or (worse) mismatched payout
- Signal 3: Reward-parameter mutators (`addRewardToken`, `updateRewardPerBlock`, `updateStartAndEndBlocks`) do NOT call `_updatePool()` first — retroactive accrual manipulation becomes possible
- Signal 4: Raw `ERC20(token).transfer(...)` (unchecked bool) in reward/payout paths while relying on IERC20 bool-return ABI — breaks on USDT-style (no return) or ZRX-style (returns false without revert) tokens
- Signal 5: `updateUnstakingFee(_newFee)` stores arbitrary uint with precision 10000 and no `<= 10000` bound; `updateFeeCollector` only requires `!= current` (0x0 accepted)

#### False Positive Guards

- Not this bug when: `_transfer` is overridden to migrate `userInfo.amount` and settle/migrate `rewardDebt` for both sender and receiver (post-fix commit 1dd2057) — verify the hook handles BOTH sides, not just the sender
- Not this bug when: the position token is non-transferable (mint/burn to holder only) or transfers are disabled — then no desync surface exists
- Reward-checkpoint issue is Medium only if parameters are mutable AFTER pool start (pre-start-only mutation like `updateRewardPerBlock`'s `block.number < startBlock` guard reduces it); check each mutator's guards individually
- Deflationary/rebasing incompatibility (PVE-002): LOW when the protocol can whitelist staked/reward tokens; upgrade to MEDIUM+ only if arbitrary user-proposed tokens are accepted
- Non-ERC20-compliant token handling (PVE-005): confirmed-wontfix because non-compliant tokens excluded — if a fork accepts USDT/ZRX, the raw-transfer calls become live revert/failure paths
- Admin-argument validation (PVE-004) is Informational-grade config hygiene unless fee collector 0x0 + fee>0 is actually reachable in production config

### Vulnerability Description

#### Root Cause

1. **PVE-001 (Medium, L-likelihood/H-impact) — unhooked LP transfer.** `deposit()` does `user.amount += _amount; _mint(msg.sender, _amount)`; `withdraw()` does `user.amount -= _amount; _burn(msg.sender, _amount)`. The inherited ERC20 `transfer`/`transferFrom` move only ERC20 balances. After `A → B` LP transfer: `userInfo[A].amount` still holds the stake (A can withdraw while holding no LP → `_burn(A)` underflow revert), and B holds LP with `userInfo[B].amount == 0` (cannot withdraw at all). Reward debt likewise never migrates: rewards accrued by the moved stake are stranded/misattributed.
2. **PVE-006 (Medium) — missing reward checkpoint in config mutators.** `addRewardToken()` pushes a token, sets `rewardPerBlock`, and zeroes `accTokenPerShare` WITHOUT calling `_updatePool()` — so accrued-but-uncheckpointed rewards under old parameters get re-attributed after the change; `updateRewardPerBlock` is guarded pre-start (`block.number < startBlock`), limiting exposure; `updateStartAndEndBlocks()` also flagged.
3. **PVE-002/PVE-005 (Low) — token-compliance assumptions.** Deposit/reward paths use raw `transfer/transferFrom` assuming full-amount, ERC20-compliant behavior; deflationary tokens break the internal-balance assumption, USDT-style approve/no-bool and ZRX-style return-false break unchecked calls.
4. **PVE-004 (Info) — unvalidated admin args.** `updateUnstakingFee` accepts `_newFee > 10000` → subsequent `withdraw()` reverts during fee math; `updateFeeCollector` accepts 0x0 → fees lost.

#### Attack Scenario / Path Variants

**Path A: LP transfer bricks both parties' withdrawal** [MEDIUM]
Path key: `unhooked_lp_transfer | transfer()/transferFrom() on LP | _transfer not overridden -> userInfo.amount desync -> withdraw() revert`
1. Alice deposits 100 stakedToken → `userInfo[Alice].amount = 100`, LP balance[Alice] = 100
2. Alice `transfer(Bob, 100)` → LP balance[Bob] = 100; `userInfo[Alice].amount` STILL 100, `userInfo[Bob].amount = 0`
3. Bob calls `withdraw(100)`: `require(userInfo[Bob].amount >= 100)` fails → Bob permanently cannot withdraw (LP is a dead claim)
4. Alice calls `withdraw(100)`: `userInfo` check passes, `_burn(Alice, 100)` reverts (Alice holds 0 LP)
5. Underlying 100 tokens remain locked in the pool; pending rewards for that stake are stranded on Alice's rewardDebt
   — note economics: this is griefing/lock, not theft; a secondary-market buyer of the LP is the victim

**Path B: Reward-config change without checkpoint skews distribution** [MEDIUM]
Path key: `reward_config_without_checkpoint | addRewardToken/updateRewardPerBlock | missing _updatePool() -> unfair reward distribution`
1. Pool accrues rewards to block N; `accTokenPerShare` last checkpointed at block M < N
2. Owner calls `addRewardToken(newToken, rate)` which zeroes `accTokenPerShare[newToken]` (fine, new token) — but for the reward-rate path the missing `_updatePool()` means N..M accrual is computed under the NEW rate retroactively once someone triggers the update
3. Stakers who deposited before the change receive distorted shares of the interim rewards; timing the update lets a privileged/MEV actor shape distribution

**Path C: Non-compliant token breaks payout silently or loudly** [LOW]
Path key: `non_reverting_unsafe_transfer | raw transfer() calls | ZRX/USDT-style tokens -> silent failure or revert`
1. Pool adds USDT-as-reward or a deflationary stakedToken
2. `ERC20(rewardTokens[i]).transfer(to, pending)` — USDT: return-value ABI mismatch can revert; ZRX-style: returns false, caller ignores, reward silently lost; deflationary: contract balance < ledger → later withdrawals underfunded

**Path D: Admin misconfiguration bricks withdraw** [INFO]
Path key: `unvalidated_admin_args | updateUnstakingFee/updateFeeCollector | fee > 10000 or 0x0 collector -> withdraw revert or fee loss`
1. Owner sets `unStakingFee = 20000` (precision 10000) or feeCollector = 0x0
2. Every `withdraw()` now reverts in fee math / sends fees to 0x0 — pool-wide exit DoS by fat finger

#### Vulnerable Pattern Examples

**Example 1: dual-ledger deposit/withdraw without transfer hook** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE (BSCSBaseStartPool): ERC20 LP mint/burn paired with a
// shadow userInfo ledger that transfers never touch
function deposit(uint256 _amount) external nonReentrant {
    UserInfo storage user = userInfo[msg.sender];
    ...
    if (_amount > 0) {
        user.amount = user.amount.add(_amount);
        ERC20(stakedToken).transferFrom(msg.sender, address(this), _amount);
        _mint(msg.sender, _amount);          // LP mirrors deposit...
    }
    for (uint256 i = 0; i < rewardTokens.length; i++) {
        user.rewardDebt[i] = user.amount.mul(accTokenPerShare[i])
                             .div(PRECISION_FACTOR[i]);
    }
}
// transfer(LP) moves ERC20 balance only -> user.amount stale on both sides
```

**Example 2: burn-gated withdraw against the shadow ledger** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: recipient of transferred LP has balance but no userInfo,
// original owner has userInfo but no balance — both revert paths
function withdraw(uint256 _amount) external nonReentrant {
    UserInfo storage user = userInfo[msg.sender];
    require(user.amount >= _amount, "Amount to withdraw too high");
    ...
    if (_amount > 0) {
        user.amount = user.amount.sub(_amount);
        _burn(msg.sender, _amount);          // ❌ reverts for stale-ledger holder
        _amount = collectFee(_amount, user);
        ERC20(stakedToken).transfer(msg.sender, _amount);
    }
}
```

**Example 3: reward mutator skipping the checkpoint** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: no _updatePool() before changing reward economics
function addRewardToken(ERC20 _token, uint256 _rewardPerBlock) external onlyOwner {
    ...
    rewardTokens.push(_token);
    PRECISION_FACTOR[_token] = 10 ** (30 - decimals);
    rewardPerBlock[_token] = _rewardPerBlock;
    accTokenPerShare[_token] = 0;            // fresh token OK, but rate-change
}                                           // paths lack the checkpoint
```

**Example 4: unbounded fee + unchecked collector** [Approx Vulnerability : INFO]
```solidity
// ❌ VULNERABLE: precision-10000 fee with no upper bound; 0x0 accepted
function updateUnstakingFee(uint256 _newFee) external onlyOwner {
    unStakingFee = _newFee;                  // 20000 bricks withdraw()
}
function updateFeeCollector(address _newCollector) external onlyOwner {
    require(_newCollector != feeCollector, "Already the fee collector");
    feeCollector = _newCollector;            // 0x0 loses fees
}
```

### Impact Analysis

#### Technical Impact
- Transferred LP = permanently unwithdrawable stake: underlying + accrued rewards locked in pool for both transfer parties
- rewardDebt never migrates on transfer → reward misattribution between old/new holder
- Missing checkpoints let reward-parameter changes retroactively reprice interim accruals
- Raw transfer() on non-compliant tokens: silent loss (false-return) or revert DoS on payout paths

#### Business Impact
- Any secondary-market trading of the LP receipt guarantees buyer fund loss — reputationally equivalent to "position token is broken"
- Admin fat-finger (fee bound, collector 0x0) can pause all exits until governance reacts

#### Affected Scenarios
- All MasterChef/launchpool variants that mint transferable ERC20 receipts while keeping a parallel userInfo ledger (extremely common BSC fork pattern — Sushi-style chefs wrapped as ERC20)
- Multi-reward-token pools with post-start parameter mutation
- Pools whose token set is admin-curated vs user-proposed (changes deflationary-token severity)

### Secure Implementation

**Fix 1: hook transfers into the staking ledger (PeckShield's fix, commit 1dd2057)**
```solidity
// ✅ SECURE: override _transfer to migrate amount + rewardDebt on both sides
function _transfer(address from, address to, uint256 amount) internal override {
    UserInfo storage f = userInfo[from];
    UserInfo storage t = userInfo[to];
    _updatePool();
    // settle sender's pending rewards first (or checkpoint via debt)
    f.amount = f.amount.sub(amount);
    t.amount = t.amount.add(amount);
    for (uint256 i = 0; i < rewardTokens.length; i++) {
        f.rewardDebt[i] = f.amount.mul(accTokenPerShare[i]).div(PRECISION_FACTOR[i]);
        t.rewardDebt[i] = t.amount.mul(accTokenPerShare[i]).div(PRECISION_FACTOR[i]);
    }
    super._transfer(from, to, amount);
}
```

**Fix 2: checkpoint before config changes; bound admin args; safe transfers**
```solidity
// ✅ SECURE: every reward-parameter mutator checkpoints first
function addRewardToken(ERC20 _token, uint256 _rewardPerBlock) external onlyOwner {
    _updatePool();                            // team added this (commit 7d905b7)
    ...
}

// ✅ SECURE: bound the fee to its precision; reject zero collector
function updateUnstakingFee(uint256 _newFee) external onlyOwner {
    require(_newFee <= 10000, "fee too high");
    unStakingFee = _newFee;
}
function updateFeeCollector(address _newCollector) external onlyOwner {
    require(_newCollector != address(0), "zero address");
    require(_newCollector != feeCollector, "Already the fee collector");
    feeCollector = _newCollector;
}

// ✅ SECURE: SafeERC20 for every stake/reward movement (handles USDT/ZRX)
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
IERC20(token).safeTransfer(to, amount);
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Contract is ERC20 AND has deposit/withdraw with a separate userInfo ledger (dual-ledger smell)
- `_mint` in deposit, `_burn` in withdraw, no _transfer/_beforeTokenTransfer override
- Reward-parameter setters (add/remove token, rate, schedule) without a leading _updatePool()
- Raw transfer()/transferFrom() on tokens not guaranteed ERC20-compliant
- Precision-scaled admin-settable fees without <= precision bound
```

#### High-Signal Grep Seeds
```
- accTokenPerShare
- rewardDebt
- _updatePool
- addRewardToken
- updateRewardPerBlock
- unStakingFee
- updateFeeCollector
```

#### Code Patterns to Look For
```
- Pattern 1: `contract X is Ownable, ReentrancyGuard, ERC20(...)` + `userInfo` mapping
- Pattern 2: `_mint(msg.sender, _amount);` inside deposit() with no transfer hook
- Pattern 3: mutators that write rewardPerBlock/accTokenPerShare without calling _updatePool()
- Pattern 4: `ERC20(token).transfer(` (no bool check) in payout loops over rewardTokens[]
- Pattern 5: `require(x != current)` as the ONLY validation on an address setter
```

#### Audit Checklist
- [ ] If position token is ERC20: transfer LP between two accounts, then attempt withdraw from both — exactly the legal holder must succeed
- [ ] Verify rewardDebt migration for sender AND receiver on transfer (and on transferFrom)
- [ ] List every mutator touching reward math; confirm `_updatePool()` precedes each (or mutation is pre-start-only)
- [ ] Confirm SafeERC20 (or bool-checked) calls for all stake/reward token movements
- [ ] Bound-check every precision-scaled admin parameter; zero-check every address setter
- [ ] Test deflationary reward token: balance-delta bookkeeping vs amount assumption

### Real-World Examples

#### Known Exploits
- No public exploit for BSCStation from this report; class is endemic: MasterChef-fork LP-receipt desync has caused repeated locked-position incidents across BSC forks. PeckShield fixed via `_transfer` override (commit 1dd2057).

#### Related CVEs/Reports
- PeckShield #2021-301 BSCStation Start Pools PVE-001..PVE-007 — see [peckshield-bscs]
- PeckShield #2022-348 PinkSale SubscriptionPool (PVE-001 deflationary, same dual-book assumption) — see [peckshield-pink]
- Related DB entry: DB/bnb-chain/defi/pinksale-subscription-access.md

### Prevention Guidelines

#### Development Best Practices
1. Either make position tokens non-transferable OR migrate both ledgers (amount + rewardDebt) inside the transfer hook — never leave a shadow ledger
2. Checkpoint (`_updatePool`) before ANY reward-parameter mutation, or freeze parameters post-start
3. Use SafeERC20 everywhere; never assume full-amount transfers (deflationary) or bool returns (USDT/ZRX)
4. Bound precision-scaled admin inputs; reject zero addresses on collectors/recipients

#### Testing Requirements
- Unit tests: A deposits → transfers LP to B → withdraw from A (must revert) and from B (must succeed post-fix); rewardDebt continuity across transfer
- Integration tests: addRewardToken/updateRewardPerBlock mid-accrual; fee at 0, at bound, above bound
- Fuzzing targets: interleaved deposit/withdraw/transfer sequences against ledger invariant `ERC20.balanceOf(u) == userInfo[u].amount`

### Keywords for Search

`masterchef`, `staking pool`, `launchpool`, `bscstation`, `bscs`, `lp token`, `position token`, `erc20 receipt`, `unhooked transfer`, `_transfer override`, `userInfo`, `shadow ledger`, `dual ledger`, `reward debt`, `accTokenPerShare`, `checkpoint`, `updatePool`, `addRewardToken`, `reward per block`, `unstaking fee`, `fee collector`, `deflationary token`, `rebasing token`, `usdt approve`, `zrx transfer false`, `safeerc20`, `non-reverting call`, `silent failure`, `locked position`, `withdraw revert`, `reward stranding`, `peckshield`, `bsc defi`, `fork of sushiswap masterchef`

### Related Vulnerabilities

- DB/bnb-chain/defi/pinksale-subscription-access.md — sibling PeckShield launchpad audit (admin trust + token-compliance)
- DB/bnb-chain/tokens/stkbnb-redemption-accounting.md — LSD claim reserve accounting
- DB/bnb-chain/tokens/bnbx-staking-derivative.md — LSD share-mint accounting
