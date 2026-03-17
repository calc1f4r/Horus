---
title: Bonding Curve Reentrancy and Flash Loan Vulnerabilities
protocol: Multi-Protocol (Phi, Sudoswap, Sound.xyz, DYAD, PartyDAO, Virtuals, Fei, Bunni)
chain: Ethereum, Multi-Chain
category: Reentrancy, Flash Loans
vulnerability_type: Reentrancy, Flash Loan Bypass, Callback Exploitation, Atomic Arbitrage
attack_type: Reentrancy, Flash Loan Attack, Self-Liquidation, Callback Manipulation
primitives: Bonding Curve, NFT AMM, Crowdfund, Genesis Launch, Rebalance Orders
severity: critical
impact: Fund Theft, Protocol Drain, Flash Loan Protection Bypass, Unfair Token Distribution
tags:
  - bonding-curve
  - reentrancy
  - flash-loan
  - callback-exploitation
  - nonReentrant
  - balance-caching
  - self-liquidation
  - atomic-arbitrage
  - genesis-launch
  - graduation
  - rebalance-callback
  - nft-amm
  - crowdfund
  - fake-edition

# Pattern Identity (Required)
root_cause_family: callback_reentrancy
pattern_key: callback_reentrancy | unknown | Reentrancy, Flash Loan Bypass, Callback Exploitation, Atomic Arbitrage

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - Atomic
  - Bonding Curve
  - Crowdfund
  - Genesis Launch
  - NFT AMM
  - Rebalance Orders
  - _createCredInternal
  - approve
  - balanceOf
  - block.number
  - borrow
  - create
  - createCred
  - deposit
  - launch
  - liquidate
  - mint
  - mintConcluded
  - msg.sender
  - receive
---

# Bonding Curve Reentrancy and Flash Loan Vulnerabilities

## Overview

Bonding curve protocols are particularly susceptible to reentrancy and flash loan attacks because price is a function of state (supply, reserves) that changes during execution. Reentrancy allows an attacker to interact with the protocol mid-state-change, while flash loans enable atomic manipulation of the state variables that drive pricing. This entry covers 10 validated patterns across 8 protocols and 7+ independent auditors.

**Pattern Frequency:** Common — 10/131 bonding curve reports (7.6%)
**Cross-Auditor Validation:** Strong — confirmed by Code4rena, Cyfrin, Spearbit, Sherlock, Pashov, OpenZeppelin, Obront



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of callback_reentrancy"
- Pattern key: `callback_reentrancy | unknown | Reentrancy, Flash Loan Bypass, Callback Exploitation, Atomic Arbitrage`
- Interaction scope: `multi_contract`
- Primary affected component(s): `unknown`
- High-signal code keywords: `Atomic`, `Bonding Curve`, `Crowdfund`, `Genesis Launch`, `NFT AMM`, `Rebalance Orders`, `_createCredInternal`, `approve`
- Typical sink / impact: `Fund Theft, Protocol Drain, Flash Loan Protection Bypass, Unfair Token Distribution`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
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

## Root Cause

These vulnerabilities exist because **state changes are not finalized before external calls**, or because **flash loan protection mechanisms have bypass paths**. Bonding curves are especially vulnerable because price depends on supply/reserves — any reentrancy or same-block manipulation that alters these variables before checks are complete allows exploitation.

## Vulnerability Description

1. **Reentrancy via ETH Refunds**: Excess payment refunds give control to attackers who re-enter creation/trading functions
2. **Reentrancy via Callback/Router**: Malicious pools or routers re-enter the protocol during token transfers or royalty callbacks
3. **Balance Caching**: Cached balance snapshots become stale during reentrancy, passing validation twice
4. **Flash Loan Protection Bypass**: Self-liquidation or `move()` operations bypass same-block deposit-withdraw checks
5. **Atomic Genesis/Graduation**: Purchase → launch → redeem all callable in one transaction
6. **Rebalance Callback Arbitrage**: Protocol enters inconsistent state during rebalance; callback allows deposits at deflated prices

---

### Vulnerable Pattern Examples

#### **Pattern 1: Cred Creation Reentrancy via Refund** [HIGH]

**Source:** Phi — Code4rena (CAUsr, 0xCiphky, and 25 others)
**File:** `reports/bonding_curve_findings/phi_c4rena_reentrancy_cred_creation.md`

```solidity
function _createCredInternal(...) internal {
    creds[credIdCounter].bondingCurve = bondingCurve_;
    buyShareCred(credIdCounter, 1, 0); // refund → reentrancy
    credIdCounter += 1; // NOT reached yet during reentry
}
// Reentrant call overwrites creds[credIdCounter] with expensive curve
```

**Attack:** Create cred with cheap curve → excess ETH refund → re-enter → buy shares at cheap price → re-enter again → `createCred` with expensive curve (overwrites `creds[credIdCounter].bondingCurve`) → sell shares at expensive curve prices. PoC: >45 ETH drained from 50 ETH balance.

---

#### **Pattern 2: VeryFastRouter Re-Entry via Malicious Pair** [HIGH]

**Source:** Sudoswap — Cyfrin (Hans, Alex Roan, 0kage, Giovanni Di Siena)
**File:** `reports/bonding_curve_findings/sudoswap_cyfrin_veryfastrouter_reentry.md`

```solidity
// VeryFastRouter.sol#L296 — outputAmount from malicious pair
// VeryFastRouter.sol#L301-L302 — ethAmount += outputAmount (inflated)
// VeryFastRouter.sol#L482-L486 — transfers ethAmount to attacker
// Malicious pair re-enters swap() during royalty/NFT callbacks
```

**Attack:** Include attacker's malicious pair in swap orders → pair re-enters `swap()` during NFT interaction → places fake sell order → inflates `ethAmount` via fake `outputAmount` → excess ETH transferred to attacker. Original caller's buy orders fail, losing their ETH.

---

#### **Pattern 3: Router NFT Theft via Balance Cache** [MEDIUM]

**Source:** Sudoswap — Spearbit (Max Goodman, Mudit Gupta, Gerard Persoon)
**File:** `reports/bonding_curve_findings/sudoswap_spearbit_router_nft_theft.md`

```solidity
// Balance cached before router.pairTransferERC20From()
// Malicious router re-enters swapTokenForAnyNFTs() during transfer
// Cached balance used for both original and re-entrant call validation
// Result: 2 NFTs received for 1 token transfer
```

**Attack:** Factory owner approves malicious router. Router calls `swapTokenForAnyNFTs(isRouter=true)` → during `pairTransferERC20From`, re-enters same function → second call performs real transfer → both calls' `_validateTokenInput` pass against pre-reentrancy cached balance → attacker gets 2 NFTs for price of 1.

---

#### **Pattern 4: SAM Fund Theft via Fake Edition** [HIGH]

**Source:** Sound.xyz — Zach Obront
**File:** `reports/bonding_curve_findings/soundxyz_obront_sam_fake_edition.md`

```solidity
contract EvilEdition {
    address public owner;
    constructor() { owner = msg.sender; }
    function mintConcluded() public view returns (bool) { return false; }
    function samMint(address to, uint quantity) public returns (uint) { return 1; }
    function samBurn(address from, uint[] memory tokenIds) public {} // no-ops
}
// sam.create() doesn't validate editions are genuine Sound contracts
```

**Attack:** Deploy `EvilEdition` → register via `sam.create()` with very low `inflectionPrice` → buy 1 token at near-zero cost → call `sam.setInflectionPrice(500 ether)` + `sam.setInflectionPoint(1)` → sell token → receive entire SAM balance. PoC: 1000 ETH drained.

---

#### **Pattern 5: Flash Loan Protection Bypass via Self-Liquidation** [HIGH]

**Source:** DYAD — Code4rena (carrotsmuggler, Al-Qa-qa, ZanyBonzy, TheFabled, Emmanuel)
**File:** `reports/bonding_curve_findings/dyad_c4rena_flash_loan_bypass.md`

```solidity
// Deposit sets: idToBlockOfLastDeposit[id] = block.number;
// Withdraw checks: if (idToBlockOfLastDeposit[id] == block.number) revert;
// BUT liquidate→move doesn't update idToBlockOfLastDeposit for recipient
function liquidate(uint id, uint to) {
    vault.move(id, to, collateral); // no deposit tracking on 'to'
}
```

**Attack:** Flash-loan USDC → deposit to vault A → mint DYAD (inflate kerosene price) → manipulate kerosene price down → self-liquidate A→B → collateral moves (bypasses flash protection on B) → withdraw from B repay flash loan. Account D's DYAD minted at inflated kerosene = bad debt.

---

#### **Pattern 6: NFT Crowdfund Flash Manipulation** [MEDIUM]

**Source:** PartyDAO — Code4rena (Trust, smiling_heretic)
**File:** `reports/bonding_curve_findings/partydao_c4rena_nft_crowdfund_flash.md`

```solidity
// BuyCrowdfund allows maximumPrice = 0 (unlimited)
// Attacker can contribute atomically via flash loan
// Takes >99.99% voting power → passes ArbitraryCallsProposal immediately
```

**Attack:** List own NFT → crowdfund has `maximumPrice=0` → flash-loan 10,000× existing contributions → contribute → buy own NFT (sale proceeds return) → create `ArbitraryCallsProposal` to `approve(attacker, tokenId)` → passes unanimously → transfer NFT back; keep contributions; repay loan.

---

#### **Pattern 7: Flash-Forced Premature Graduation** [MEDIUM]

**Source:** Virtuals Protocol — Code4rena
**File:** `reports/bonding_curve_findings/virtuals_c4rena_flashloan_graduation.md`

```solidity
function unwrapToken(address srcTokenAddress, address[] memory accounts) public {
    Token memory info = tokenInfo[srcTokenAddress];
    require(info.tradingOnUniswap, "Token is not graduated yet");
    // No time restriction — atomic conversion possible
    FERC20 token = FERC20(srcTokenAddress);
    IERC20 agentToken = IERC20(info.agentToken);
    for (uint i = 0; i < accounts.length; i++) {
        uint256 balance = token.balanceOf(accounts[i]);
        if (balance > 0) {
            token.burnFrom(accounts[i], balance);
            agentToken.transferFrom(pairAddress, accounts[i], balance);
        }
    }
}
```

**Attack:** Flash-borrow virtual tokens → `buy()` enough to trigger graduation (`gradThreshold`) → immediately `unwrapToken()` to convert memecoins to agent tokens → sell on Uniswap → repay flash loan. Token graduates with no real community support; rewards manipulated.

---

#### **Pattern 8: Atomic Genesis Profit via Flash Loan** [CRITICAL/HIGH]

**Source:** Fei Protocol — OpenZeppelin
**File:** `reports/bonding_curve_findings/fei_openzeppelin_flash_genesis_profit.md`

```solidity
// GenesisGroup: purchase(), launch(), and redeem() all callable atomically
// No same-block restriction between operations
// Flash loan: deposit ETH → launch bonding curve → redeem FEI + TRIBE
// → sell TRIBE for FEI → sell FEI for ETH → repay loan → ~$800K profit
```

**Attack:** Flash-borrow ETH to reach `maxGenesisPrice` → `purchase()` → `launch()` (initializes oracle + adds Uniswap liquidity) → `redeem()` (get FEI + TRIBE) → sell TRIBE→FEI→ETH on newly created pools → repay flash loan. Estimated ~$800K profit per execution.

---

#### **Pattern 9: Fulfiller Arbitrage During Rebalance Callback** [HIGH]

**Source:** Bunni (August) — Pashov Audit Group
**File:** `reports/bonding_curve_findings/bunni_pashov_rebalance_callback_arbitrage.md`

```solidity
// Step 2: preHook — tokenIn balance decreased (pool deflated)
// Step 4: sourceConsideration — fulfiller's callback (BunniHub INCONSISTENT)
// Step 6: postHook — tokenOut balance credited
// During step 4, fulfiller can deposit liquidity at deflated pool state
```

**Attack:** Rebalance order submitted to FloodPlain → fulfiller executes → during `sourceConsideration` callback (between preHook and postHook), BunniHub is in inconsistent state → fulfiller deposits liquidity at deflated state → mints more shares than deserved.

---

#### **Pattern 10: Rebalance Token Collision with am-AMM Fees** [MEDIUM]

**Source:** Bunni — Cyfrin
**File:** `reports/bonding_curve_findings/bunni_cyfrin_rebalance_token_collision.md`

```solidity
// Pre-hook: cache output balance
tstore(REBALANCE_OUTPUT_BALANCE_SLOT, outputBalanceBefore)
// Post-hook: compute delta
orderOutputAmount = args.currency.balanceOfSelf() - outputBalanceBefore;
// If am-AMM bid deposited Bunni tokens between pre/post, orderOutputAmount is inflated
```

**Attack:** Pool's underlying token IS a Bunni token → fulfiller performs am-AMM bid during `sourceConsideration` → deposits Bunni tokens as rent → post-hook computes inflated `orderOutputAmount` due to additional Bunni tokens → core accounting corrupted.

---

## Impact Analysis

| Impact | Frequency | Severity |
|--------|-----------|----------|
| Direct fund theft | 7/10 patterns | HIGH-CRITICAL |
| Flash loan protection bypass | 2/10 patterns | HIGH |
| Unfair token distribution | 2/10 patterns | MEDIUM |
| Share dilution/overminting | 2/10 patterns | MEDIUM-HIGH |
| Accounting corruption | 1/10 patterns | MEDIUM |

**Financial Impact Range:** From share dilution (Patterns 9-10) to complete protocol drain (Patterns 1, 4, 8: >$800K per execution).

## Secure Implementation

### Add Reentrancy Guards to All State-Changing Functions

```solidity
// SECURE: nonReentrant on creation, buy, and sell
function createCred(...) external payable nonReentrant {
    creds[credIdCounter].bondingCurve = bondingCurve_;
    credIdCounter += 1; // increment BEFORE external call
    buyShareCred(credIdCounter - 1, 1, 0);
}
```

### Enforce Flash Loan Protection on All Transfer Paths

```solidity
// SECURE: Update deposit tracking on ALL collateral movements
function liquidate(uint id, uint to) external {
    vault.move(id, to, collateral);
    idToBlockOfLastDeposit[to] = block.number; // ← track the recipient too
}
```

### Validate External Contract Authenticity

```solidity
// SECURE: Only allow registered, verified edition contracts
function create(address edition, ...) external {
    require(ISoundEditionFactory(factory).isEdition(edition), "Not genuine");
    // Additional: lock curve parameters after first sale
}
```

### Prevent Atomic Genesis/Graduation

```solidity
// SECURE: Require launch and redeem in different blocks
function launch() external {
    require(block.number > genesisBlock + LAUNCH_DELAY, "Too soon");
    launchBlock = block.number;
}
function redeem() external {
    require(block.number > launchBlock, "Same block as launch");
}
```

---

### Detection Patterns

#### Code Patterns to Look For

```
# Missing reentrancy guards
function.*buy|sell|create|mint.*\{(?!.*nonReentrant)
# External calls before state updates
\.call\{value|\.transfer\(|\.send\(.*\n.*counter\+\+|\.set\(
# Cached balances before external calls
balanceOf.*before.*\n.*external_call.*\n.*balanceOf.*after
# Flash loan protection gaps
idToBlockOfLastDeposit.*(?!.*liquidate|move)
# Atomic multi-step operations
purchase.*launch.*redeem|buy.*graduate.*unwrap
# Unvalidated external contracts
_getMakingAmount|samMint|samBurn.*(?!isEdition|isRegistered)
```

#### Preconditions

1. ETH refunds or ERC777/callback tokens trigger external calls
2. State variables (counter, balance) updated after external calls
3. Flash loan protection only covers deposit/withdraw, not move/liquidate
4. Genesis/graduation operations callable atomically without block delays
5. External contracts (editions, pairs, routers) not validated for authenticity

---

## Keywords

bonding curve reentrancy, flash loan protection bypass, callback exploitation, nonReentrant missing, balance caching reentrancy, ETH refund reentrancy, self-liquidation flash loan, atomic genesis profit, flash loan graduation, rebalance callback arbitrage, fake edition fund theft, NFT crowdfund flash manipulation, VeryFastRouter re-entry, malicious pair reentrancy, router NFT theft, idToBlockOfLastDeposit bypass, sourceConsideration callback, am-AMM rent collision, FERC20 unwrap atomic, maximumPrice zero crowdfund

## Related Vulnerabilities

- [BONDING_CURVE_PRICE_MANIPULATION_VULNERABILITIES.md](BONDING_CURVE_PRICE_MANIPULATION_VULNERABILITIES.md) — Flash loan price manipulation (related precursor)
- [BONDING_CURVE_TOKEN_LAUNCH_GRADUATION_VULNERABILITIES.md](BONDING_CURVE_TOKEN_LAUNCH_GRADUATION_VULNERABILITIES.md) — Graduation-specific attacks
- [BONDING_CURVE_DOS_GRIEFING_VULNERABILITIES.md](BONDING_CURVE_DOS_GRIEFING_VULNERABILITIES.md) — DoS via pre-creation and front-running

## References

| # | Protocol | Auditor | Severity | Report |
|---|----------|---------|----------|--------|
| 1 | Phi | Code4rena | HIGH | `reports/bonding_curve_findings/phi_c4rena_reentrancy_cred_creation.md` |
| 2 | Sudoswap | Cyfrin | HIGH | `reports/bonding_curve_findings/sudoswap_cyfrin_veryfastrouter_reentry.md` |
| 3 | Sudoswap | Spearbit | MEDIUM | `reports/bonding_curve_findings/sudoswap_spearbit_router_nft_theft.md` |
| 4 | Sound.xyz | Obront | HIGH | `reports/bonding_curve_findings/soundxyz_obront_sam_fake_edition.md` |
| 5 | DYAD | Code4rena | HIGH | `reports/bonding_curve_findings/dyad_c4rena_flash_loan_bypass.md` |
| 6 | PartyDAO | Code4rena | MEDIUM | `reports/bonding_curve_findings/partydao_c4rena_nft_crowdfund_flash.md` |
| 7 | Virtuals | Code4rena | MEDIUM | `reports/bonding_curve_findings/virtuals_c4rena_flashloan_graduation.md` |
| 8 | Fei Protocol | OpenZeppelin | HIGH | `reports/bonding_curve_findings/fei_openzeppelin_flash_genesis_profit.md` |
| 9 | Bunni | Pashov | HIGH | `reports/bonding_curve_findings/bunni_pashov_rebalance_callback_arbitrage.md` |
| 10 | Bunni | Cyfrin | MEDIUM | `reports/bonding_curve_findings/bunni_cyfrin_rebalance_token_collision.md` |

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

`Atomic`, `Bonding Curve`, `Crowdfund`, `Genesis Launch`, `NFT AMM`, `Rebalance Orders`, `Reentrancy, Flash Loan Bypass, Callback Exploitation, Atomic Arbitrage`, `Reentrancy, Flash Loans`, `_createCredInternal`, `approve`, `atomic-arbitrage`, `balance-caching`, `balanceOf`, `block.number`, `bonding-curve`, `borrow`, `callback-exploitation`, `create`, `createCred`, `crowdfund`, `deposit`, `fake-edition`, `flash-loan`, `genesis-launch`, `graduation`, `launch`, `liquidate`, `mint`, `mintConcluded`, `msg.sender`, `nft-amm`, `nonReentrant`, `rebalance-callback`, `receive`, `reentrancy`, `self-liquidation`
