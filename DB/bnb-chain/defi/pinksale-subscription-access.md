---
# Core Classification
protocol: pinksale-subscriptionpool
chain: bsc
category: access_control
vulnerability_type: privileged_input_rewrite

# Pattern Identity
root_cause_family: ungoverned_admin_rewrite_of_user_state
pattern_key: admin_state_rewrite | governance setter | post-commitment user allocations | allocation theft or sale rigging

# Interaction Scope
interaction_scope: single_contract_family
involved_contracts:
  - SubscriptionPool (contributeCustomCurrency/contribute, updateCalculatedData, setCalculationStage, setCanFinalize, _lockLiquidity)
  - LaunchPadLibrary (addLiquidity, raw IERC20.approve)
path_keys:
  - admin_state_rewrite | updateCalculatedData | purchasedOf rewrite -> allocation rigging
  - non_compliant_token_transfer | IERC20.approve / contributeCustomCurrency | USDT no-bool / deflationary -> revert or book desync
  - missing_event | silent admin setters -> untraceable parameter changes

# Attack Vector Details
attack_type: logical_error
affected_component: subscription/allocation accounting + liquidity lock flow

# Technical Primitives
primitives:
  - ratio_based_allocation (committed/total committed)
  - arbitrary_admin_array_write (users[], amounts[])
  - stage_state_machine (calculationStage)
  - raw_erc20_approve_assumptions
  - balance_delta_bookkeeping
  - indexed_event_coverage

# Grep / Hunt-Card Seeds
code_keywords:
  - contributeCustomCurrency
  - updateCalculatedData
  - purchasedOf
  - totalVolumePurchased
  - setCalculationStage
  - setCanFinalize
  - onlyGovernance
  - calculationStage
  - poolSettings
  - poolStates
  - _lockLiquidity
  - addLiquidity
  - safeApprove

# Impact Classification
severity: medium
impact: allocation_manipulation|fund_loss|book_desync
financial_impact: medium

# Context Tags
tags:
  - launchpad
  - presale
  - subscription
  - fair-launch
  - allocation
  - admin-keys
  - governance
  - deflationary-token
  - pinksale
  - peckshield

# Version Info
language: solidity
version: "audited SubscriptionPool-09072022.sol (MD5 c0412b28); fixed SubscriptionPool-09292022.sol (MD5 799c117f)"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [peckshield-pink] | reports/bnb-chain_findings/publications-audit-reports-peckshield-audit-report-pinksale-subscriptionpool-v1-0-pdf.md | MEDIUM | PeckShield | PeckShield Report #2022-348, Oct 8 2022 |

## PinkSale SubscriptionPool: Admin Allocation Rewrite & Token-Compliance Gaps

**Governance can silently rewrite any user's committed/purchased state after commitments land** — `updateCalculatedData(users[], amounts[])` writes arbitrary per-user allocations with only a length check, no timelock, no DAO mediation, and no events; raw `IERC20.approve` breaks USDT-style tokens; deflationary currencies desync the books.

### Overview

PinkSale's SubscriptionPool lets users commit assets toward a token sale with final allocation = user's committed / total committed. PeckShield's Medium finding (PVE-004): the privileged governance account can overwrite `purchasedOf[user]` and `totalVolumePurchased` wholesale (CWE-287 trust issue) — a compromised key rigs every allocation silently. Supporting lows: raw-approve USDT revert in `addLiquidity`/`_lockLiquidity` (PVE-002, fixed), deflationary/rebasing currency desync (PVE-001, confirmed-wontfix), missing events on admin setters (PVE-003).

#### Agent Quick View

- Root cause statement: "This vulnerability exists because post-commitment user state (`purchasedOf`, `totalVolumePurchased`) is writable in bulk by a single governance key with only a `users.length == amounts.length` check — no range validation, no event, no timelock, no DAO — so allocation outcomes are entirely trust-based"
- Pattern key: `admin_state_rewrite | governance setter | post-commitment user allocations | allocation rigging`
- Interaction scope: `single_contract_family`
- Primary affected component(s): `SubscriptionPool admin setters + contribute flow`
- Contracts / modules involved: `SubscriptionPool, LaunchPadLibrary`
- Path keys: see frontmatter `path_keys`
- High-signal code keywords: `updateCalculatedData`, `purchasedOf`, `onlyGovernance`, `setCalculationStage`, `contributeCustomCurrency`
- Typical sink / impact: `rigged allocations / stolen commitments / sale finalize manipulation`
- Validation strength: `strong` (PeckShield line-cited; PVE-002 verified fixed by MD5)

#### Contract / Boundary Map

- Entry surface(s): `contribute()/contributeCustomCurrency(amount)` (users), `updateCalculatedData`, `setCalculationStage`, `setCanFinalize` (governance), `_lockLiquidity → LaunchPadLibrary.addLiquidity`
- Contract hop(s): `user → contribute (safeTransferFrom, _contribute bookkeeping) → [governance rewrite window] → finalize/claim`; `SubscriptionPool → IERC20(token).approve(router) → router.addLiquidity*`
- Trust boundary crossed: `EOA/multisig governance → on-chain allocation truth`; `arbitrary sale currency → bookkeeping assumption (amount == received)`
- Shared state or sync assumption: `purchasedOf/totalCommitted must reflect actual committed assets; internal books must match external token balances`

#### Valid Bug Signals

- Signal 1: An admin function accepts parallel `address[]`/`uint256[]` and writes per-user state directly, gated only by a length-equality require — no per-value bounds, no event, no delay
- Signal 2: Stage/state machine (`calculationStage`) advances via one-key setters with no event emission → finalization can be forced (`setCanFinalize` hard-sets `CALCULATED`)
- Signal 3: `IERC20(token).approve(router, x)` raw calls (not safeApprove) on user-selected or listing-selected tokens
- Signal 4: Commitment accounting uses the requested `amount` rather than measured balance delta (deflationary desync)
- Signal 5: Key parameter/state setters emit no events (CWE-563-class observability gap)

#### False Positive Guards

- Not this bug when: admin rewrites are timelocked, evented, restricted to correction windows before finalize, or behind a DAO/timelock contract — PeckShield's own remediation path; severity then drops to config hygiene
- Not this bug when: allocation is computed purely on-chain from commitments (ratio formula) with NO admin-override entry point
- Deflationary incompatibility (PVE-001) is LOW when currency set is protocol-curated (PinkSale confirmed no need to support such tokens); escalate only if arbitrary currencies are accepted — and remember USDT can *become* fee-on via its control switch
- Raw-approve (PVE-002) only bites for non-bool-returning tokens (USDT); fixed via safeApprove in 09292022 version — verify which tokens the router path actually touches
- Missing events (PVE-003) is Informational on its own; it amplifies the Medium because admin rewrites become untraceable

### Vulnerability Description

#### Root Cause

1. **PVE-004 (Medium) — ungoverned admin keys.** `updateCalculatedData(totalVolumePurchased, users[], amounts[])` (onlyGovernance) overwrites every listed user's `purchasedOf` and the global `totalVolumePurchased` with arbitrary values. `setCalculationStage(stage)` and `setCanFinalize()` mutate the sale state machine freely. All are un-evented and un-timelocked. A compromised governance key = full allocation rigging + finalize manipulation with zero on-chain trace.
2. **PVE-002 (Low, fixed) — raw approve on USDT-style tokens.** `LaunchPadLibrary.addLiquidity` line 2693/2709 and `SubscriptionPool::_lockLiquidity` call `IERC20(token).approve(...)` directly. USDT's approve returns no bool → interface-expecting call reverts → liquidity lock path DoS for that token. Fixed with safeApprove-style wrappers in MD5 799c117f.
3. **PVE-001 (Low, wontfix) — deflationary/rebasing currency desync.** `contributeCustomCurrency` books the *requested* `amount` after `safeTransferFrom`; fee-on-transfer currencies make internal books exceed actual balances.
4. **PVE-003 (Info) — missing events.** The three admin setters above emit nothing, so off-chain monitors cannot detect rewrites.

#### Attack Scenario / Path Variants

**Path A: Compromised governance rigs allocations** [MEDIUM]
Path key: `admin_state_rewrite | updateCalculatedData | purchasedOf rewrite -> allocation rigging`
1. Sale collects commitments from N users; `purchasedOf[u]` reflects their contributions
2. Attacker with the governance key (phished multisig signer, key theft) calls `updateCalculatedData(hugeTotal, [victim1, victim2, attackerAddr], [0, 0, hugeAmount])`
3. No event fires; subgraph/indexers see nothing until finalization
4. `setCanFinalize()` forces the stage to CALCULATED; finalize distributes tokens per rewritten allocations — victims' committed BNB buys nothing, attacker claims everything
5. No on-chain resistance; detection only via manual state diffing

**Path B: USDT sale currency bricks liquidity lock** [LOW]
Path key: `non_compliant_token_transfer | IERC20.approve / contributeCustomCurrency | USDT no-bool / deflationary -> revert or book desync`
1. Sale uses USDT (or any no-bool-return approve token) as currency or sale token
2. `_lockLiquidity → addLiquidity` executes raw `IERC20(token).approve(router, amt)`
3. ABI-decode expects bool; USDT returns nothing → revert; liquidity locking (and thus finalize) fails for that pool
   — variant: fee-on-transfer currency in `contributeCustomCurrency` books amount > received, leaving the pool structurally underfunded at finalize

**Path C: Silent stage manipulation** [LOW]
Path key: `missing_event | silent admin setters -> untraceable parameter changes`
1. `setCalculationStage(Stage.CALCULATED)` or `setCanFinalize()` called out-of-band (e.g., before legit calculation completes)
2. No event emitted; frontends/indexers serve stale assumptions
3. Users interact with a pool they believe is in an earlier stage; claims/finalize behavior diverges from displayed state

#### Vulnerable Pattern Examples

**Example 1: bulk arbitrary per-user state write** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE (SubscriptionPool): governance can rewrite any user's
// allocation post-commitment; length check is the only validation
function updateCalculatedData(
    uint256 totalVolumePurchased,
    address[] memory users,
    uint256[] memory amounts
) external onlyGovernance {
    require(users.length == amounts.length, "Invalid length");
    poolStates.totalVolumePurchased = totalVolumePurchased; // arbitrary
    for (uint256 i = 0; i < users.length; i++) {
        purchasedOf[users[i]] = amounts[i];                 // arbitrary per-user
    }
    // no event — rewrite is invisible to indexers
}
```

**Example 2: one-key stage forcing, un-evented** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: stage machine advanced/reversed by a single key, silently
function setCalculationStage(Stage stage) external onlyGovernance {
    calculationStage.stage = stage;      // no validation, no event
}
function setCanFinalize() external onlyGovernance {
    calculationStage.stage = Stage.CALCULATED; // force-finalize path
}
```

**Example 3: raw approve breaks non-compliant tokens** [Approx Vulnerability : LOW]
```solidity
// ❌ VULNERABLE (LaunchPadLibrary::addLiquidity, audited MD5): USDT-style
// approve (no bool return) reverts under IERC20 ABI expectations
IERC20(token).approve(address(router), liquidityToken);          // line 2693
...
IERC20(currency).approve(address(router), type(uint256).max);    // line 2709
// SubscriptionPool::_lockLiquidity() shared the same issue
```

### Impact Analysis

#### Technical Impact
- Full allocation integrity loss on key compromise: arbitrary winners/losers per sale, finalize forced
- Book desync with fee-on-transfer currencies → finalize underfunding, disputed claims
- Liquidity-lock revert path for USDT-class tokens → sale cannot complete listing flow

#### Business Impact
- Launchpad allocation fairness is the product; a single unaccountable key rewriting it silently is the core risk PeckShield flags (CWE-287)
- Un-evented mutations break indexers/dashboards users rely on at exactly the moment of attack

#### Affected Scenarios
- Any subscription/over-subscription sale where final allocations are settable by admins after commitments
- Any launchpad routing through AMM addLiquidity with uncurated token lists
- Tokens with dormant control switches (USDT blacklist/fee toggles) — "compliant today" ≠ "compliant at finalize"

### Secure Implementation

**Fix 1: bound, delay, and observe admin rewrites**
```solidity
// ✅ SECURE: corrections are evented, windowed before finalize, and ideally
// timelocked / DAO-gated
event CalculatedDataUpdated(address indexed caller, uint256 totalVolume,
                            address[] users, uint256[] amounts);

function updateCalculatedData(uint256 totalVolumePurchased,
    address[] memory users, uint256[] memory amounts
) external onlyGovernance {
    require(calculationStage.stage != Stage.CALCULATED, "window closed");
    require(users.length == amounts.length, "Invalid length");
    poolStates.totalVolumePurchased = totalVolumePurchased;
    for (uint256 i = 0; i < users.length; i++) {
        purchasedOf[users[i]] = amounts[i];
    }
    emit CalculatedDataUpdated(msg.sender, totalVolumePurchased, users, amounts);
}
// stronger: route through TimelockController; compute allocations on-chain
// from commitments so no rewrite entry exists at all
```

**Fix 2: safe approve + balance-delta bookkeeping (team's PVE-002 fix)**
```solidity
// ✅ SECURE: SafeERC20 tolerates no-bool tokens
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
IERC20(token).safeApprove(address(router), liquidityToken);

// ✅ SECURE (deflationary-safe contribute): book what actually arrived
uint256 before = IERC20(cur).balanceOf(address(this));
IERC20(cur).safeTransferFrom(msg.sender, address(this), amount);
uint256 received = IERC20(cur).balanceOf(address(this)) - before;
_contribute(received);
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- onlyOwner/onlyGovernance setters accepting address[]/uint256[] that write user-facing state
- Stage/enum state machines advanced by single-key setters with no event
- Raw .approve( on tokens not controlled by the protocol
- Contribution bookkeeping using requested amount instead of balance delta
- Silent (event-less) mutations of sale-wide parameters
```

#### High-Signal Grep Seeds
```
- updateCalculatedData
- purchasedOf
- onlyGovernance
- setCalculationStage
- setCanFinalize
- contributeCustomCurrency
- _lockLiquidity
```

#### Code Patterns to Look For
```
- Pattern 1: `purchasedOf[users[i]] = amounts[i];` inside an admin loop
- Pattern 2: `calculationStage.stage = Stage.CALCULATED;` from a no-arg setter
- Pattern 3: `IERC20(x).approve(` (no safe wrapper) on listing-provided tokens
- Pattern 4: `_contribute(amount)` directly after safeTransferFrom without delta check
- Pattern 5: setters with zero emit statements
```

#### Audit Checklist
- [ ] Inventory every admin-write to user state; require events + timelock/DAO or on-chain-derived values
- [ ] Check stage-machine setters for validation (legal transitions) and events
- [ ] Trace the liquidity-lock path token-by-token for raw approve/transfer
- [ ] For each accepted currency: assume fee-on-transfer and verify bookkeeping uses received-delta
- [ ] Confirm which "compliant" tokens have control switches (USDT) that could change behavior mid-sale

### Real-World Examples

#### Known Exploits
- No public exploit of PinkSale SubscriptionPool from this report; all findings confirmed or fixed. Class precedent: numerous launchpad allocation disputes and admin-key compromises on BSC launchpads (2021-2022 era).

#### Related CVEs/Reports
- PeckShield #2022-348 PinkSale SubscriptionPool PVE-001..PVE-004 — see [peckshield-pink]
- Related DB entry: DB/bnb-chain/defi/launchpool-deposit-validation.md (BSCStation sibling audit)

### Prevention Guidelines

#### Development Best Practices
1. Derive allocations on-chain from commitments; if admin correction is unavoidable, make it evented, windowed (pre-finalize only), and timelock/DAO-mediated
2. Emit events (with indexed key args) for every privileged state mutation
3. Use SafeERC20 wrappers on all listing/currency tokens; never assume bool returns
4. Book received-deltas, not requested amounts, wherever third-party tokens move

#### Testing Requirements
- Unit tests: USDT-mock approve path through addLiquidity/_lockLiquidity; fee-on-transfer currency contribution bookkeeping
- Integration tests: admin rewrite attempted post-CALCULATED must revert; indexer-visible event on every setter
- Fuzzing targets: users[]/amounts[] length and value bounds; stage transition legality

### Keywords for Search

`pinksale`, `subscription pool`, `launchpad`, `presale`, `subscription`, `allocation`, `fair launch`, `admin keys`, `governance key`, `privileged setter`, `updateCalculatedData`, `purchasedOf`, `onlyGovernance`, `stage machine`, `setCanFinalize`, `calculation stage`, `force finalize`, `timelock`, `dao governance`, `silent mutation`, `missing events`, `indexed events`, `usdt approve`, `non-compliant erc20`, `safeapprove`, `deflationary token`, `fee on transfer`, `rebasing`, `balance delta bookkeeping`, `liquidity lock`, `addliquidity`, `allocation rigging`, `compromised admin`, `peckshield`, `bsc launchpad`

### Related Vulnerabilities

- DB/bnb-chain/defi/launchpool-deposit-validation.md — dual-ledger/reward family from the sibling BSCStation audit
- DB/bnb-chain/tokens/stkbnb-redemption-accounting.md — FeeVault recipient-validation (admin dispatch) sibling
- General admin-key/trust entries (timelock, two-step ownership patterns)
