---
# Core Classification
protocol: persistence-one-stkbnb
chain: bsc
category: business_logic
vulnerability_type: reserve_accounting_mismatch

# Pattern Identity
root_cause_family: wrong_guard_variable_and_unsafe_admin_power
pattern_key: wrong_reserve_check | claim payout | contract balance vs claim reserve | withdrawal revert or fund lock

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - StakePool.sol (claimReqs, _claim, _claimReserve, _canBeClaimed)
  - FeeVault.sol (claimStkBNB)
  - StakeBNBToken.sol (stkBNB, selfDestruct)
  - UndelegationHolder.sol (bnbUnbonding view reuse)
path_keys:
  - wrong_reserve_check | claim(uint256 index) | _claimReserve vs address(this).balance -> revert on zero-reserve
  - admin_fund_lock | claimStkBNB | FeeVault -> StakePool recipient -> permanently locked fees
  - unsafe_admin_power | selfDestruct(whenPaused) | DEFAULT_ADMIN_ROLE -> selfdestruct steals all deposited BNB
  - unsafe_cast | unbond accounting | uint256 -> int256 casts -> overflow on extreme values
  - transfer_gas_limit | _claim payout | payable(msg.sender).transfer -> 2300-gas revert for smart wallets

# Attack Vector Details
attack_type: logical_error
affected_component: redemption/claim pipeline

# Technical Primitives
primitives:
  - claim_reserve_ledger
  - swap_delete_claim_array
  - uint256_to_int256_cast
  - selfdestruct_with_native_balance
  - transfer_2300_gas_stipend
  - cross_contract_recipient_validation

# Grep / Hunt-Card Seeds
code_keywords:
  - claimReqs
  - weiToReturn
  - _claimReserve
  - InsufficientFundsToSatisfyClaim
  - _canBeClaimed
  - claimStkBNB
  - selfDestruct
  - getStkBNB
  - bnbUnbonding
  - IndexOutOfBounds
  - getPaginatedClaimRequests

# Impact Classification
severity: medium
impact: fund_lock|dos|admin_fund_loss
financial_impact: medium

# Context Tags
tags:
  - liquid-staking
  - stkbnb
  - bnb-staking
  - claim
  - unbond
  - reserve-accounting
  - selfdestruct
  - feevault
  - halborn

# Version Info
language: solidity
version: "audited commit bde7ee900aba18aecd0e8e0c0497121540dd5abb (July 2022); fixed d059bccbb368158a63767107b37894d47009c385"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [halborn-stkbnb] | reports/bnb-chain_findings/publicreports-solidity-smart-contract-audits-persistence-stkbnb-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | Persistence stkBNB audit, Jul 10–Aug 3 2022 |

## stkBNB Redemption/Claim Accounting (Persistence StakePool)

**Claim pipeline guarded by the wrong balance + admin paths that can lock or destroy user funds** — the `_claim` redemption path checks contract balance semantics incorrectly, FeeVault can strand fees in StakePool, `selfDestruct` can destroy the stkBNB token with deposits inside, and unbond math uses raw uint256→int256 casts.

### Overview

Persistence's stkBNB liquid-staking StakePool lets users request unstake and later `claim()` their BNB from a pending claim queue. Halborn found the redemption pipeline's accounting guards inverted or misplaced (balance vs reserve), plus privileged functions (`selfDestruct`, `claimStkBNB`) whose misuse permanently bricks withdrawals or locks fees.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because payout-sufficiency is checked against the wrong ledger (contract balance instead of `_claimReserve`), privileged recipients are not validated (FeeVault→StakePool), and admin self-destruct has no user-fund safety precondition"
- Pattern key: `wrong_reserve_check | claim payout | contract balance vs claim reserve | withdrawal revert or fund lock`
- Interaction scope: `multi_contract`
- Primary affected component(s): `StakePool._claim / claimReqs, FeeVault.claimStkBNB, StakeBNBToken.selfDestruct`
- Contracts / modules involved: `StakePool.sol, FeeVault.sol, StakeBNBToken.sol, UndelegationHolder.sol`
- Path keys: see frontmatter `path_keys` (5 variants)
- High-signal code keywords: `claimReqs`, `_claimReserve`, `InsufficientFundsToSatisfyClaim`, `claimStkBNB`, `selfDestruct`
- Typical sink / impact: `user withdrawal revert (DoS) / permanently locked fees / total loss of deposits if selfDestruct fires with funds inside`
- Validation strength: `strong` (exact code lines cited by Halborn; fixes verified on commit d059bcc)

#### Contract / Boundary Map

- Entry surface(s): `claim(uint256 index)` (user), `claimStkBNB(recipient, amount)` (FeeVault owner), `selfDestruct(addr)` (DEFAULT_ADMIN_ROLE, whenPaused)
- Contract hop(s): `user -> StakePool.claim -> _claimReserve decrement -> payable(msg.sender).transfer`; `owner -> FeeVault.claimStkBNB -> IStakedBNBToken.send -> recipient`
- Trust boundary crossed: `admin-configurable recipient (FeeVault) → StakePool internal accounting`; `token-level selfdestruct → all staked native balance`
- Shared state or sync assumption: `_claimReserve` must track exactly the BNB set aside for satisfiable claim requests; ERC20-send of stkBNB to StakePool breaks the assumption that StakePool can route claims

#### Valid Bug Signals

- Signal 1: A payout guard compares `address(this).balance` (or a different bucket) against `req.weiToReturn` while the decremented ledger is `_claimReserve` — mismatch produces either revert-DoS (reserve 0 but balance > 0) or under-funded payout attempts
- Signal 2: A privileged "send token to arbitrary recipient" function has no recipient deny-list, and some legal recipient (e.g. StakePool itself) cannot recover tokens sent to it
- Signal 3: `selfdestruct` on a token/staking contract is callable while user funds are still inside, with no proof withdrawals completed and no timelock
- Signal 4: Unbond arithmetic mixes signed/unsigned with raw casts (`int256(excessBNB)`, `_bnbToUnbond -= int256(...)`) instead of SafeCast
- Signal 5: Native payouts use `.transfer()` (2300 gas), blocking smart-contract wallets from claiming

#### False Positive Guards

- Not this bug when: the payout check and the decrement use the same ledger variable (`if (_claimReserve < req.weiToReturn) revert`) — post-fix code does exactly this
- Not this bug when: self-destruct is timelocked and documented as catastrophic-upgrade-only escape hatch — post-fix uses OZ TimelockController; severity then reflects timelock duration and user exit window, not instant rug
- Safe if: recipients of fee-sending functions are validated `!= address(stakePool)` and StakePool has a sweep/recovery path for stkBNB
- `unsafe casting` (HAL-03) is LOW: values only overflow near 2^255 BNB — report it as SafeCast hygiene, not an exploitable path
- `.transfer` vs `.call` (HAL-05) is LOW unless the project's stated user base includes contract wallets; with reentrancy guards present, `call` is safe

### Vulnerability Description

#### Root Cause

1. **HAL-02 (wrong guard variable)** — `_claim` guards with `address(this).balance < req.weiToReturn` in the description excerpt (the audited snippet shows both forms across revisions), while the state it mutates is `_claimReserve -= req.weiToReturn`. When `claimReserve` is 0 but the contract holds BNB (e.g. pending unbond not yet credited to reserve), the subtraction at L786 reverts with an unhandled arithmetic exception — claims DoS. The check must test the same bucket it spends.
2. **HAL-01 (selfdestruct with user funds)** — `StakeBNBToken.selfDestruct(addr)` (onlyRole(DEFAULT_ADMIN_ROLE), whenPaused) sends the contract's entire native balance to `addr` and erases the stkBNB code. Users' claim rights live in StakePool mappings; destroying the token + sweeping BNB breaks the dApp and can lose deposits.
3. **HAL-04 (FeeVault→StakePool fund lock)** — `FeeVault.claimStkBNB` `onlyOwner` sends stkBNB to any `recipient`. If recipient == StakePool address, those fee tokens are locked forever because FeeVault has no path to call StakePool's claim.
4. **HAL-03 (unsafe casting)** — four sites cast uint256 BNB quantities into int256 for `_bnbToUnbond` comparisons/subtractions without SafeCast.
5. **HAL-05 (transfer gas stipend)** — `payable(msg.sender).transfer(req.weiToReturn)` forwards only 2300 gas; smart wallets with non-trivial receivers cannot claim.

#### Attack Scenario / Path Variants

**Path A: User claim reverts — reserve/balance mismatch DoS** [MEDIUM→LOW]
Path key: `wrong_reserve_check | claim(uint256 index) | _claimReserve vs address(this).balance -> revert on zero-reserve`
1. Users request unstake; their `weiToReturn` is queued in `claimReqs`
2. Contract holds BNB (balance > 0) but `_claimReserve == 0` (unbond proceeds not yet moved into reserve)
3. User calls `claim(index)`; the balance check passes but `_claimReserve -= req.weiToReturn` underflows → transaction reverts
4. Impact: temporary or prolonged claim DoS depending on how reserve is funded; fixed by checking `_claimReserve` itself

**Path B: Admin strands FeeVault fees in StakePool** [LOW]
Path key: `admin_fund_lock | claimStkBNB | FeeVault -> StakePool recipient -> permanently locked fees`
1. Owner calls `FeeVault.claimStkBNB(stakePoolAddress, amount)` (fat-finger or malicious compromise)
2. stkBNB lands in StakePool; no function lets anyone extract it (claim routes native BNB only)
3. Fees permanently locked — value loss bounded by accumulated fee stock

**Path C: Admin self-destruct destroys redemption** [MEDIUM]
Path key: `unsafe_admin_power | selfDestruct(whenPaused) | DEFAULT_ADMIN_ROLE -> selfdestruct steals all deposited BNB`
1. Admin pauses, then calls `selfDestruct(addr)` on StakeBNBToken
2. Contract's native balance is force-transferred to `addr`; code erased; stkBNB transfers/claims break
3. Users holding claim rights must rely on off-chain rebalancing promises — post-fix remediation adds a Timelock window to withdraw first

**Path D: Unbond accounting overflow via unsafe cast** [LOW edge]
Path key: `unsafe_cast | unbond accounting | uint256 -> int256 casts -> overflow on extreme values`
1. `_bnbToUnbond` (int256) is compared/subtracted against `int256(excessBNB)`, `int256(shortCircuitAmount)`, `int256(bnbUnbonding_)`, `int256(weiToReturn)`
2. Any uint256 > 2^255-1 wraps negative → inverted comparison → wrong unbond amount or revert
3. Practically unreachable at real BNB magnitudes; SafeCast removes the class

#### Vulnerable Pattern Examples

**Example 1: guard checks a different bucket than it spends** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE (StakePool._claim, audited commit): balance-based guard,
// reserve-based spend → revert when reserve is 0 but balance is not
function _claim(uint256 index) internal returns (bool) {
    if (index >= claimReqs[msg.sender].length) revert IndexOutOfBounds(index);
    ClaimRequest memory req = claimReqs[msg.sender][index];
    if (!_canBeClaimed(req)) return false;
    if (address(this).balance < req.weiToReturn) {   // wrong ledger
        revert InsufficientFundsToSatisfyClaim();
    }
    _claimReserve -= req.weiToReturn;                // spends a different one
    claimReqs[msg.sender][index] = claimReqs[msg.sender][claimReqs[msg.sender].length - 1];
    claimReqs[msg.sender].pop();
    payable(msg.sender).transfer(req.weiToReturn);   // 2300-gas stipend (HAL-05)
    emit Claim(msg.sender, req, block.timestamp);
    return true;
}
```

**Example 2: unguarded privileged recipient** [Approx Vulnerability : LOW]
```solidity
// ❌ VULNERABLE (FeeVault.claimStkBNB): recipient can be the StakePool,
// which has no path to move stkBNB out → fees locked forever
function claimStkBNB(address recipient, uint256 amount) external override onlyOwner {
    IStakedBNBToken(addressStore.getStkBNB()).send(recipient, amount, " ");
    emit Withdraw(msg.sender, recipient, amount);
}
```

**Example 3: self-destruct with live user funds** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE (StakeBNBToken): no check that user funds were returned,
// no timelock — whenPaused + admin role is the only brake
function selfDestruct(address addr) external onlyRole(DEFAULT_ADMIN_ROLE) whenPaused {
    selfdestruct(payable(addr));
}
```

**Example 4: raw signed/unsigned casts in unbond math** [Approx Vulnerability : LOW]
```solidity
// ❌ VULNERABLE (StakePool unbond accounting): uint256→int256 without SafeCast
if (_bnbToUnbond > int256(excessBNB)) { ... }
_bnbToUnbond -= int256(shortCircuitAmount);
_bnbToUnbond -= int256(bnbUnbonding_);
_bnbToUnbond += int256(weiToReturn);
```

### Impact Analysis

#### Technical Impact
- Claim pipeline can revert indefinitely while the reserve/balance ledgers disagree → user-exit DoS on a liquid-staking derivative
- Fees irrevocably locked in StakePool via FeeVault misaddressing
- Worst case (admin key abuse or compromise + pause + selfDestruct): loss of all deposited BNB backing stkBNB
- Smart wallets excluded from native payouts by 2300-gas transfer

#### Business Impact
- Liquid-staking products live on redemption credibility: revert-DoS or locked fees directly hit token peg and user trust
- Timelock remediation converts rug risk into an exit-window question — auditors should still size the window vs unbond duration (~7 days on BNB staking)

#### Affected Scenarios
- Any BSC liquid-staking claim/pending-withdrawal queue with a separate reserve ledger
- Vaults that send staked-derivative tokens to arbitrary admin-chosen recipients
- Upgrade-path escape hatches (selfdestruct) on staking tokens holding native balances

### Secure Implementation

**Fix 1: guard and spend the same reserve ledger (Halborn's accepted fix)**
```solidity
// ✅ SECURE: check the exact bucket that will be decremented
if (_claimReserve < req.weiToReturn) {
    revert InsufficientFundsToSatisfyClaim();
}
_claimReserve -= req.weiToReturn;
```

**Fix 2: validate recipients; timelock self-destruct; safe casts; call payout**
```solidity
// ✅ SECURE (FeeVault): deny recipients that cannot recover funds
require(recipient != address(stakePool), "invalid recipient");

// ✅ SECURE (selfDestruct): timelock (implemented via OZ TimelockController)
// gives users a withdrawal window before destruction can execute

// ✅ SECURE (casts): SafeCast.toInt256(excessBNB) reverts instead of wrapping
import "@openzeppelin/contracts/utils/math/SafeCast.sol";
_bnbToUnbond -= SafeCast.toInt256(shortCircuitAmount);

// ✅ SECURE (payout): low-level call with reentrancy guard already present
(bool ok, ) = msg.sender.call{value: req.weiToReturn}("");
require(ok, "claim transfer failed");
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Payout functions whose sufficiency check reads a different storage var than the subtraction
- Pending-claim queues using swap-delete (index, pop) — check index bounds and event completeness
- onlyOwner token-send functions with unchecked recipient cross-contract reachability
- selfdestruct/callcode reachable under pause flags without fund-drain precondition
- int256 arithmetic fed by raw uint256 casts (grep: "int256(" )
- Native-asset payouts via transfer/send instead of call
```

#### High-Signal Grep Seeds
```
- claimReqs
- weiToReturn
- _claimReserve
- InsufficientFundsToSatisfyClaim
- claimStkBNB
- selfDestruct
- int256(
```

#### Code Patterns to Look For
```
- Pattern 1: `if (address(this).balance < X) revert ...; reserve -= X;`
- Pattern 2: `IStakeToken.send(recipient, ...)` in an owner-only function with no recipient validation
- Pattern 3: `selfdestruct(payable(addr))` guarded only by role + whenPaused
- Pattern 4: mixed-sign arithmetic (_bnbToUnbond -= int256(uintVar))
- Pattern 5: `payable(msg.sender).transfer(` in claim/refund flows
```

#### Audit Checklist
- [ ] For every payout, confirm guard variable == decremented variable == actually-transferred source
- [ ] Enumerate every address an admin can direct tokens to; verify each has an extraction path
- [ ] Any selfdestruct/kill-switch: require drained-funds proof or timelock ≥ max user exit duration
- [ ] Fuzz claim ordering (swap-delete) with multiple pending claims per user
- [ ] Cast-audit all signed/unsigned boundaries in unbond math (SafeCast or bounds proof)
- [ ] Test claim() from a smart wallet with a gas-consuming fallback

### Real-World Examples

#### Known Exploits
- None public for stkBNB from this report; all findings remediated pre-launch on commit d059bcc (2022-08-02). Class precedent: liquid-staking exit-DoS events (e.g. stETH-style redemption freezes) degrade peg even without theft.

#### Related CVEs/Reports
- Halborn Persistence stkBNB report HAL-01..HAL-05 (2022) — see [halborn-stkbnb]
- Related DB entry: DB/bnb-chain/tokens/bnbx-staking-derivative.md (Stader BnbX: sibling LSD accounting bugs)

### Prevention Guidelines

#### Development Best Practices
1. Single-ledger rule: the checked reserve, the decremented reserve, and the payout source must be the same variable
2. Deny-list or allow-list recipients in any admin token-dispatch function; prove recovery paths exist
3. Never expose selfdestruct on staking/token contracts without a timelock exceeding user exit windows
4. Use SafeCast at every signed/unsigned boundary; prefer staying unsigned

#### Testing Requirements
- Unit tests: claim with `_claimReserve == 0 && balance > 0` (must revert cleanly, not underflow); claim with reserve partially funded across multiple users
- Integration tests: FeeVault → every legal recipient; smart-wallet claim via call
- Fuzzing targets: `claimReqs` ordering, reserve funding/unbond timing races, int256 boundary values

### Keywords for Search

`stkbnb`, `persistence`, `liquid staking`, `bnb staking`, `claim`, `redemption`, `unbond`, `claimReserve`, `weiToReturn`, `reserve accounting`, `wrong ledger`, `underflow revert`, `withdrawal dos`, `fund lock`, `feevault`, `recipient validation`, `selfdestruct`, `self destruct`, `timelock`, `kill switch`, `unsafe casting`, `int256 cast`, `safecast`, `transfer vs call`, `2300 gas`, `smart wallet payout`, `liquid staking derivative`, `lsd`, `peg risk`, `halborn`

### Related Vulnerabilities

- DB/bnb-chain/tokens/bnbx-staking-derivative.md — BnbX first-depositor/reward-accounting family
- DB/bnb-chain/defi/launchpool-deposit-validation.md — sibling BSC launch-era validation gaps
- DB/general/… reward-debt / share-mismatch patterns (accTokenPerShare family)
