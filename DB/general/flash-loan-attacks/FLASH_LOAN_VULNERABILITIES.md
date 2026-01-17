---
# Core Classification (Required)
protocol: generic
chain: everychain
category: economic
vulnerability_type: flash_loan_abuse

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error
affected_component: flash_loan|repayment_validation|fee_logic|state_transition

# Technical Primitives (Required - list all applicable)
primitives:
  - flash_loan
  - repayment_check
  - fee_calculation
  - allowance
  - pool_status
  - liquidation
  - callback
  - tx_origin
  - erc3156
  - oracle_price
  - governance_vote

# Impact Classification (Required)
severity: medium
impact: fund_loss|manipulation|dos
exploitability: 0.65
financial_impact: medium

# Context Tags (Optional but recommended)
tags:
  - defi
  - lending
  - flash_loan
  - liquidity
  - governance

# Version Info (Optional)
language: solidity
version: all
---

## Reference
- [blend] : reports/flash_loan_findings/m-01-flash-loans-allow-borrowing-from-frozen-pools-bypassing-security-controls.md
- [astrolab] : reports/flash_loan_findings/h-02-flash-loan-wrong-balance-check.md
- [caviar] : reports/flash_loan_findings/m-03-flash-loan-fee-is-incorrect-in-private-pool-contract.md
- [dyad] : reports/flash_loan_findings/h-10-flash-loan-protection-mechanism-can-be-bypassed-via-self-liquidations.md
- [tapioca] : reports/flash_loan_findings/h-15-attacker-can-specify-any-receiver-in-usd0flashloan-to-drain-receiver-balanc.md
- [fx] : reports/flash_loan_findings/flashloan-functionality-does-not-follow-erc-3156-standard.md
- [sharwafinance] : reports/flash_loan_findings/m-13-free-flashloans-due-to-the-lack-of-fee-or-interest-charges.md
- [putty] : reports/flash_loan_findings/m-09-the-contract-serves-as-a-flashloan-pool-without-fee.md
- [vader] : reports/flash_loan_findings/m-04-flashproof-is-not-flash-proof.md
- [dexe] : reports/flash_loan_findings/attacker-can-combine-flashloan-with-delegated-voting-to-decide-a-proposal-and-wi.md
- [stakedao] : reports/flash_loan_findings/m-08-oracles-are-vulnerable-to-flash-loan-attack-vectors.md

## Vulnerability Title

Flash Loan Abuse via Missing Validation, Incorrect Fees, or Bypassed Safeguards

### Overview

This vulnerability exists because flash loan flows skip critical validations (pool status, allowance, repayment deltas, or fee scaling), or allow alternative state transitions (like liquidation) to bypass protections, enabling fund loss, unauthorized borrowing, or manipulation in a single transaction or block.

### Vulnerability Description

#### Root Cause

Flash loan handlers are often implemented as “special-case” entry points. When the flash loan path does not reuse the same validation logic as normal borrow/withdraw paths, or when fee/repayment checks are miscomputed, the protocol can be drained or manipulated. Common root causes include:
- Missing pool/reserve status checks on flash loan path
- Incorrect balance delta validation before/after callback
- Fee calculation using unscaled or wrong units
- Allowance checks that permit charging arbitrary receivers
- Anti-flash-loan checks tied to a single state transition, bypassable via liquidation or transfer

#### Attack Scenario

1. Attacker initiates a flash loan (or any callback-enabled operation).
2. The flash loan path skips or miscomputes validation (e.g., incorrect repayment delta, fee scaling, or pool status checks).
3. Attacker manipulates state during callback (self-liquidation, price manipulation, or unauthorized receiver selection).
4. Protocol accepts the operation despite invalid repayment or disallowed status.
5. Attacker exits with profit, or the system accrues bad debt or becomes insolvent.

#### Vulnerable Pattern Examples

**Example 1: Wrong Balance Delta Check** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: balanceBefore recorded before transfer; repayment check requires extra funds
uint256 fee = exemptionList[msg.sender] ? 0 : amount.bp(fees.flash);
uint256 toRepay = amount + fee;

uint256 balanceBefore = asset.balanceOf(address(this));
totalLent += amount;

asset.safeTransferFrom(address(this), address(receiver), amount);
receiver.executeOperation(address(asset), amount, fee, msg.sender, params);

if ((asset.balanceOf(address(this)) - balanceBefore) < toRepay)
    revert FlashLoanDefault(msg.sender, amount);
```
Reference: `reports/flash_loan_findings/h-02-flash-loan-wrong-balance-check.md` (Astrolab, HIGH)

**Example 2: Incorrect Flash Loan Fee Scaling** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: returns unscaled changeFee as flash loan fee
function flashFee(address, uint256) public view returns (uint256) {
    return changeFee; // should be scaled to base token decimals
}
```
Reference: `reports/flash_loan_findings/m-03-flash-loan-fee-is-incorrect-in-private-pool-contract.md` (Caviar, MEDIUM)

**Example 3: Arbitrary Receiver Charged for Repayment** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: receiver specified by caller, allowance checked against contract
uint256 _allowance = allowance(address(receiver), address(this));
require(_allowance >= (amount + fee), "USDO: repay not approved");
_approve(address(receiver), address(this), _allowance - (amount + fee));
_burn(address(receiver), amount + fee);
```
Reference: `reports/flash_loan_findings/h-15-attacker-can-specify-any-receiver-in-usd0flashloan-to-drain-receiver-balanc.md` (Tapioca DAO, HIGH)

**Example 4: Anti-Flashloan Guard Bypassed via Liquidation** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: anti-flashloan guard only tracks deposits
idToBlockOfLastDeposit[id] = block.number;

// Liquidation path moves collateral without updating idToBlockOfLastDeposit
function liquidate(uint id, uint to) {
    vault.move(id, to, collateral);
}
```
Reference: `reports/flash_loan_findings/h-10-flash-loan-protection-mechanism-can-be-bypassed-via-self-liquidations.md` (DYAD, HIGH)

**Example 5: Flash Loan Path Bypasses Pool Status Checks** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE: status checks exist for normal actions but are not enforced in flash loan
pub fn require_action_allowed(&self, e: &Env, action_type: u32) {
    if (self.config.status > 1 && (action_type == 4 || action_type == 9))
        || (self.config.status > 3 && (action_type == 2 || action_type == 0))
    {
        panic_with_error!(e, PoolError::InvalidPoolStatus);
    }
}
```
Reference: `reports/flash_loan_findings/m-01-flash-loans-allow-borrowing-from-frozen-pools-bypassing-security-controls.md` (Blend, MEDIUM)

**Example 6: ERC-3156 Noncompliant Flash Loan Flow** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: expects caller to return tokens instead of pulling from receiver
function flashLoan(...) external {
  // callback executes, but contract never pulls amount + fee from receiver
}

// ❌ VULNERABLE: flashFee does not revert when token unsupported
function flashFee(address token, uint256 amount) public view returns (uint256) {
  return amount * feeRate; // should revert for unsupported tokens
}
```
Reference: `reports/flash_loan_findings/flashloan-functionality-does-not-follow-erc-3156-standard.md` (f(x) v2, MEDIUM)

**Example 7: Free Flash Loans via Zero-Time Interest** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: interest accrues only over time, allowing same-tx borrow/repay
function getDebtWithAccruedInterest(uint id) external view returns (uint) {
  if (debtSharesSum == 0) return 0;
  return (totalBorrows() * shareOfDebt[id]) / debtSharesSum;
}

function totalBorrows() public view returns (uint) {
  uint ownershipTime = block.timestamp - totalBorrowsSnapshotTimestamp;
  // ownershipTime == 0 => no interest
}
```
Reference: `reports/flash_loan_findings/m-13-free-flashloans-due-to-the-lack-of-fee-or-interest-charges.md` (Sharwafinance, MEDIUM)

**Example 8: Flashloan Pool Without Fee via Re-entrable Flow** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: mid-execution asset transfer allows temporary use without protocol fee
function fillOrder(...) external {
  // custom baseAsset logic executes
  // attacker exercises and uses assets, then returns later in same execution
}
```
Reference: `reports/flash_loan_findings/m-09-the-contract-serves-as-a-flashloan-pool-without-fee.md` (Putty, MEDIUM)

**Example 9: tx.origin-Based Flash Guard Bypass** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: guard checks tx.origin, bypassable with multiple EOAs in same block
modifier flashProof() {
  require(lastTxOriginBlock[tx.origin] < block.number, "flash");
  _;
  lastTxOriginBlock[tx.origin] = block.number;
}
```
Reference: `reports/flash_loan_findings/m-04-flashproof-is-not-flash-proof.md` (Vader, MEDIUM)

**Example 10: Flashloan-Backed Governance Manipulation** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: flashloaned voting power can be delegated, voted, and withdrawn in one tx
govPool.deposit(address(this), votingPower, new uint256[](0));
govPool.delegate(address(slave), votingPower, new uint256[](0));
slave.vote(govPool, proposalId);
govPool.undelegate(address(slave), votingPower, new uint256[](0));
govPool.withdraw(address(this), votingPower, new uint256[](0));
```
Reference: `reports/flash_loan_findings/attacker-can-combine-flashloan-with-delegated-voting-to-decide-a-proposal-and-wi.md` (Dexe, HIGH)

**Example 11: Oracle Price Manipulation via Flash Loans** [Approx Vulnerability : MEDIUM]
```solidity
// ❌ VULNERABLE: uses instantaneous pool price for LP valuation
uint256 priceLpInPeg = CURVE_POOL.get_virtual_price();
```
Reference: `reports/flash_loan_findings/m-08-oracles-are-vulnerable-to-flash-loan-attack-vectors.md` (StakeDAO, MEDIUM)

### Impact Analysis

#### Technical Impact
- Unauthorized borrowing or liquidity extraction
- Incorrect repayment accounting and fee bypasses
- Bypass of protocol safety states (frozen/paused)
- Flash-loan powered state manipulation (liquidations, oracle effects)
- Flashloan-inflated governance outcomes or oracle prices

#### Business Impact
- Direct fund loss or protocol insolvency
- Reduced trust in lending or treasury modules
- Increased exposure to MEV and manipulation strategies

#### Affected Scenarios
- Flash loan callbacks that skip core validations
- Protocols relying on block-level anti-flash-loan checks
- Systems where liquidation or transfer paths bypass safeguards
- Governance systems that allow same-block deposit/delegate/vote/withdraw
- Oracles using instantaneous pool state without TWAP

### Secure Implementation

**Fix 1: Unify Validation Logic Across Flash Loan and Borrow Paths**
```solidity
// ✅ SECURE: reuse the same status and reserve checks
function flashLoan(...) external nonReentrant {
    _requirePoolActive();
    _requireReserveActive(asset);
    _executeFlashLoan(...);
}
```

**Fix 2: Correct Repayment Delta and Fee Accounting**
```solidity
// ✅ SECURE: record balance after transfer, validate fee only
uint256 balanceBefore = asset.balanceOf(address(this));
asset.safeTransfer(address(receiver), amount);
receiver.executeOperation(address(asset), amount, fee, msg.sender, params);

uint256 repaid = asset.balanceOf(address(this)) - balanceBefore;
require(repaid >= fee, "insufficient fee");
```

**Fix 3: Receiver Authorization**
```solidity
// ✅ SECURE: ensure receiver authorizes caller or is caller
require(receiver == msg.sender || allowance(receiver, msg.sender) >= amount + fee, "unauthorized receiver");
```

### Detection Patterns

#### Code Patterns to Look For
```
- flashLoan/flashLoanSimple that does not call the same validation as borrow/withdraw
- balanceBefore taken before transfer, and repayment check uses amount + fee delta
- flashFee returns an unscaled or constant value
- receiver address supplied by caller without authorization check
- anti-flashloan checks tied to deposits only (liquidation/transfer paths bypass)
- flashProof or same-block guards that only check tx.origin
- oracle pricing uses instantaneous pool state (spot price or virtual_price)
- governance vote flows allowing deposit/delegate/vote/withdraw in one transaction
- ERC-3156 flashLoan implementations that do not pull amount + fee from receiver
```

#### Audit Checklist
- [ ] Flash loan path reuses pool/reserve status checks
- [ ] Repayment delta is computed from correct baseline
- [ ] Fee calculation uses proper scaling and units
- [ ] Receiver is authorized or equals caller
- [ ] Alternative state transitions (liquidation/move) cannot bypass anti-flashloan guards
- [ ] Flash guard logic is not based solely on tx.origin
- [ ] Governance vote flow prevents same-block flashloan vote and withdrawal
- [ ] Oracle prices use TWAP or manipulation-resistant sources
- [ ] ERC-3156 compliance: pull amount + fee from receiver and revert for unsupported tokens

### Real-World Examples

- **Blend** - Flash loans bypass frozen pool status (MEDIUM)
  - Reference: `reports/flash_loan_findings/m-01-flash-loans-allow-borrowing-from-frozen-pools-bypassing-security-controls.md`
- **Astrolab** - Wrong balance check forces overpayment (HIGH)
  - Reference: `reports/flash_loan_findings/h-02-flash-loan-wrong-balance-check.md`
- **Caviar** - Flash fee uses unscaled `changeFee` (MEDIUM)
  - Reference: `reports/flash_loan_findings/m-03-flash-loan-fee-is-incorrect-in-private-pool-contract.md`
- **DYAD** - Anti-flashloan guard bypass via liquidation (HIGH)
  - Reference: `reports/flash_loan_findings/h-10-flash-loan-protection-mechanism-can-be-bypassed-via-self-liquidations.md`
- **Tapioca DAO** - Arbitrary receiver can be drained (HIGH)
  - Reference: `reports/flash_loan_findings/h-15-attacker-can-specify-any-receiver-in-usd0flashloan-to-drain-receiver-balanc.md`
- **f(x) v2** - ERC-3156 flash loan noncompliance (MEDIUM)
  - Reference: `reports/flash_loan_findings/flashloan-functionality-does-not-follow-erc-3156-standard.md`
- **Sharwafinance** - Free flashloans via zero-time interest (MEDIUM)
  - Reference: `reports/flash_loan_findings/m-13-free-flashloans-due-to-the-lack-of-fee-or-interest-charges.md`
- **Putty** - Flashloan pool without fee (MEDIUM)
  - Reference: `reports/flash_loan_findings/m-09-the-contract-serves-as-a-flashloan-pool-without-fee.md`
- **Vader Protocol** - tx.origin-based flash guard bypass (MEDIUM)
  - Reference: `reports/flash_loan_findings/m-04-flashproof-is-not-flash-proof.md`
- **Dexe** - Flashloan-backed governance manipulation (HIGH)
  - Reference: `reports/flash_loan_findings/attacker-can-combine-flashloan-with-delegated-voting-to-decide-a-proposal-and-wi.md`
- **StakeDAO** - Oracle price manipulable via flash loans (MEDIUM)
  - Reference: `reports/flash_loan_findings/m-08-oracles-are-vulnerable-to-flash-loan-attack-vectors.md`

### Keywords for Search

`flash_loan`, `flashloan`, `flashLoan`, `flashFee`, `repayment_check`, `fee_scaling`, `receiver_authorization`, `anti_flashloan_guard`, `liquidation_bypass`, `pool_status`, `callback`, `erc3156`, `tx.origin`, `flashProof`, `governance_vote`, `delegation`, `oracle_manipulation`, `twap`, `spot_price`

### Related Vulnerabilities

- Reentrancy (callbacks during flash loan)
- Oracle manipulation (flash-loan-funded price changes)
- Missing validations in special-case code paths