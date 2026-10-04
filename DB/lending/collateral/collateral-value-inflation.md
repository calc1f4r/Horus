---
# Core Classification
protocol: generic
chain: everychain
category: collateral
vulnerability_type: collateral_value_inflation

# Pattern Identity
root_cause_family: collateral_accounting_error
pattern_key: inflated_collateral_accounting | collateral_ledger | zero_deposit_or_double_count | over_borrowing_or_collateral_theft

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - LoanManager / UserLoanLogic
  - Position (CDP)
  - Vault registry / licensing
  - Collateral token (double-entrypoint ERC20)
  - OracleManager
path_keys:
  - inflated_collateral_accounting | deposit(0) | UserLoanLogic→colPools | null_deposit_array_inflation
  - inflated_collateral_accounting | increaseCollateral() | UserLoanLogic | double_count_effective_collateral
  - inflated_collateral_accounting | withdraw(token) | Position→legacyToken | double_entrypoint_collateral_exit
  - inflated_collateral_accounting | repayWithCollateral() | LoanManagerLogic→PoolData | totalAmount_underflow_inflation

# Attack Vector Details
attack_type: logical_error
affected_component: collateral_ledger

# Technical Primitives
primitives:
  - colPools array
  - effectiveCollateralValue
  - increaseCollateral
  - zero-amount deposit
  - double-entrypoint token
  - depositData.totalAmount
  - repayWithCollateral
  - collateral balance check
  - isLoanOverCollateralized

# Grep / Hunt-Card Seeds
code_keywords:
  - increaseCollateral
  - colPools
  - effectiveCollateralValue
  - getLoanLiquidity
  - isLoanOverCollateralized
  - updateWithRepayWithCollateral
  - depositData.totalAmount
  - withdrawCollateral
  - Position.withdraw

# Impact Classification
severity: high
impact: fund_loss
financial_impact: high

# Context Tags
tags:
  - lending
  - collateral
  - accounting
  - over_borrowing
  - defi

# Version Info
language: solidity
version: all
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [V1] | reports/lending_borrowing_findings/zero-deposits-can-be-used-to-artificially-inflate-a-users-collateral-value-allow.md | HIGH | Immunefi (Folks Finance) | solodit 61048 |
| [V2] | reports/lending_borrowing_findings/collateral-inflation-exploit-via-zero-amount-deposits-allows-an-attacker-to-drai.md | HIGH | Immunefi (Folks Finance) | solodit 61040 |
| [V3] | reports/lending_borrowing_findings/attacker-can-inflate-effectivecollateralvalue.md | HIGH | Immunefi (Folks Finance) | solodit 61063 |
| [V4] | reports/lending_borrowing_findings/logic-flaw-in-userloanincreasecollateral-leads-to-double-counting-of-effectiveco.md | HIGH | Immunefi (Folks Finance) | solodit 61016 |
| [V5] | reports/lending_borrowing_findings/incorrect-updates-to-pooldepositdatatotalamount-and-loancollateralused-during-re.md | HIGH | Immunefi (Folks Finance) | solodit 61090 |
| [V6] | reports/lending_borrowing_findings/h-02-double-entrypoint-collateral-token-allows-position-owner-to-withdraw-underl.md | HIGH | Code4rena (Frankencoin) | solodit 20017 |
| [V7] | reports/lending_borrowing_findings/h-01-design-flaw-and-mismanagement-in-vault-licensing-leads-to-double-counting-i.md | HIGH | Code4rena (DYAD) | solodit 33457 |
| [V8] | reports/lending_borrowing_findings/collateral-owner-can-steal-funds-by-taking-liens-while-asset-is-listed-for-sale-.md | HIGH | Spearbit (Astaria) | solodit 7281 |

## Collateral Value Inflation and Double-Counting

**Bugs that let a user count the same collateral multiple times — via zero-amount deposits growing iteration lists, double-counting in effective-collateral math, double-entrypoint tokens bypassing collateral-exit checks, or bad repay-with-collateral ledger updates — inflate borrowing power and drain pools.**

### Overview

Collateral accounting must guarantee one thing: the value a borrower can borrow against corresponds to assets actually locked. Eight unique HIGH findings from 3 audit firms (Immunefi, Code4rena, Spearbit) across 4 protocols show the ways that guarantee breaks. Five come from the Folks Finance x-chain engagement: zero-amount deposits push the same `poolId` into `colPools` repeatedly, and `getLoanLiquidity` then iterates the array counting the balance once per entry (`effectiveCollateralValue = deposit × N`); `userLoanIncreaseCollateral` double-counts; repay-with-collateral subtracts the wrong quantity, inflating `depositData.totalAmount` and corrupting utilization/indexes. Two more show exit-side failures: Frankencoin's double-entrypoint collateral token lets the owner withdraw the real collateral by passing the token's *legacy address* to `Position.withdraw` (bypassing `withdrawCollateral`'s debt check); DYAD's vault licensing double-counts collateral across positions. Astaria rounds it out with lien double-taking on listed-for-sale collateral.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the collateral ledger counts the same position or token multiple times (or lets it exit without the debt check), so effectiveCollateralValue exceeds the value of actually-locked assets and the borrower can extract more than they deposited."
- Pattern key: `inflated_collateral_accounting | collateral_ledger | zero_deposit_or_double_count | over_borrowing_or_collateral_theft`
- Interaction scope: `multi_contract`
- Primary affected component(s): `collateral ledger (increase/decrease), effective collateral valuation, collateral exit paths`
- Contracts / modules involved: `UserLoanLogic, LoanManagerLogic, Position, Vault registry, double-entrypoint ERC20`
- Path keys: `null_deposit_array_inflation`, `double_count_effective_collateral`, `double_entrypoint_collateral_exit`, `totalAmount_underflow_inflation`
- High-signal code keywords: `increaseCollateral`, `colPools`, `effectiveCollateralValue`, `getLoanLiquidity`, `updateWithRepayWithCollateral`
- Severity: HIGH — 8/8 unique findings rated HIGH by their source auditors
- Typical sink / impact: `over-borrowing beyond real collateral, pool drain (capped by borrow cap), unclaimed-yield theft, corrupted utilization/index`
- Validation strength: `strong, with concentration caveat` (3 firms, 4 protocols; 5/8 findings from one Immunefi engagement on Folks Finance)

#### Contract / Boundary Map

- Entry surface(s): `deposit()` (including amount = 0), `increaseCollateral()`, `repayWithCollateral()`, `Position.withdraw(token)`, lien/offer placement
- Contract hop(s): `SpokeToken.deposit -> router -> LoanManager.deposit -> UserLoanLogic.increaseCollateral (colPools.push)`; `executeBorrow -> isLoanOverCollateralized -> getLoanLiquidity (loop over colPools)`; `Position.withdraw(legacyToken) -> IERC20.transfer`
- Trust boundary crossed: `cross-chain spoke-to-hub messaging (amounts decoupled from locks)`, `ERC20 identity (double-entrypoint)`, `listing/offer state vs lien state`
- Shared state or sync assumption: `effectiveCollateralValue must equal the value of unique locked positions`; `collateral exit must imply debt check on the canonical token address`

#### Valid Bug Signals

- Signal 1: A data structure tracking which collaterals a user has (array/set) can grow without a value-increase, and valuation iterates the structure summing balances.
- Signal 2: Zero-amount actions (deposit 0, increase 0) are accepted and mutate structural state (array pushes, flag flips).
- Signal 3: Token-sweep/withdraw-by-address functions coexist with collateral exit that should require debt repayment — no check that the swept address shares storage with the collateral token.

#### False Positive Guards

- Not this bug when: the valuation reads a mapping keyed by pool (each pool counted once) rather than iterating a push-growable array, or zero-amount deposits revert.
- Not this bug when: collateral token set is restricted to vetted single-entry tokens by an enforced whitelist (Frankencoin acknowledged this residual risk).
- Safe if: repay-with-collateral updates `totalAmount` by `principalPaid` only after interest math, and invariant tests assert `totalAmount <= balance + totalBorrowed`.
- Dust guard: single-dust zero-deposits inflating by 1x are harmless; the exploit requires N repetition and a subsequent real deposit — check that the array growth is unbounded.

### Vulnerability Description

#### Root Cause

1. **Zero-amount deposit grows the iteration list** [V1][V2]: `UserLoanLogic.increaseCollateral` pushes `poolId` to `loan.colPools` whenever the balance was zero — including for `fAmount == 0`; N null deposits push N entries, and one real deposit then counts N times in `getLoanLiquidity`'s loop over `colPools`.
2. **Double-counting in effective collateral** [V3][V4]: `userLoanIncreaseCollateral` logic double-counts entries; effectiveCollateralValue inflated relative to real deposits.
3. **Repay-with-collateral ledger corruption** [V5]: `updateWithRepayWithCollateral` computes `pool.depositData.totalAmount -= principalPaid - interestPaid` (wrong quantity/direction), inflating totalAmount — utilization ratios, interest rates, and deposit indexes all become wrong; pools can become unable to operate for lack of tokens.
4. **Double-entrypoint token exit** [V6]: `Position.withdraw(token)` is meant for sweeping stray tokens and only routes to `withdrawCollateral` (with debt checks) when `token == collateral`; a TUSD-style double-entrypoint token lets the owner pass the legacy address (same balances, different address) and withdraw real collateral without repaying ZCHF debt.
5. **Licensing/registry double-count** [V7]: DYAD vault licensing mismanagement double-counts collateral across positions in collateral-ratio computation.
6. **Lien double-taking** [V8]: Astaria — collateral owner takes liens while the asset is listed for sale, stealing funds from the sale flow.

#### Attack Scenario / Path Variants

**Path A: Null-deposit array inflation** [V1][V2]
Path key: `inflated_collateral_accounting | deposit(0) | UserLoanLogic→colPools | null_deposit_array_inflation`
Entry surface: repeated `deposit(poolId, 0)` then one real `deposit(poolId, X)`
Contracts touched: `SpokeToken -> LoanManager -> UserLoanLogic.increaseCollateral -> getLoanLiquidity`
Boundary crossed: `cross-chain spoke-to-hub (amount decoupled from lock)`
1. Attacker calls deposit with fAmount = 0, N times — `loan.colPools` now holds N copies of poolId.
2. Attacker deposits X once: `loan.collaterals[poolId].balance = X`.
3. `getLoanLiquidity` loops over colPools, adding `balance` per entry → effectiveCollateralValue = N × X.
4. Attacker borrows up to N × X × LTV and walks away.
5. **Impact**: pool drain bounded only by each pool's borrow cap (flash loans supply the deposit X).

**Path B: Double-entrypoint collateral exit** [V6]
Path key: `inflated_collateral_accounting | withdraw(token) | Position→legacyToken | double_entrypoint_collateral_exit`
Entry surface: `Position.withdraw(legacyCollateralAddress, amount)`
Contracts touched: `Position -> legacy ERC20 (delegates to canonical token)`
Boundary crossed: `ERC20 address identity`
1. Collateral is a double-entrypoint token (e.g. TUSD-style: legacy address delegates to new address, shared balances).
2. Owner dusts the position with 1 wei of the LEGACY token so its `balanceOf(position) > 0`.
3. `Position.withdraw(legacyAddress, fullBalance)` — since `token != collateral`, it treats it as a stray-token sweep and transfers out.
4. The transfer moves the REAL collateral balance (shared storage) without repaying ZCHF debt.
5. **Impact**: unbacked minted ZCHF; bad debt.

**Path C: Repay-with-collateral inflates pool totals** [V5]
Path key: `inflated_collateral_accounting | repayWithCollateral() | LoanManagerLogic→PoolData | totalAmount_underflow_inflation`
Entry surface: `repayWithCollateral(loanId, amount)`
Contracts touched: `LoanManagerLogic -> HubPoolState.PoolData`
Boundary crossed: `internal ledger vs actual pool balance`
1. User repays using deposited collateral; handler updates `pool.depositData.totalAmount -= principalPaid - interestPaid`.
2. The subtracted quantity is wrong; totalAmount drifts UP against the invariant `totalAmount <= poolBalance + totalBorrowed`.
3. Utilization, rates, and deposit indexes compute from inflated totals.
4. **Impact**: incorrect rates/indexes; eventually withdrawals exceed actual tokens (yield theft, halted pool).

**Path D: Registry double-count and lien double-taking** [V7][V8]
Path key: `inflated_collateral_accounting | position/licensing ops | Registry→ratio math | double_count_effective_collateral`
Entry surface: vault licensing changes / lien placement during listing
1. The same underlying value is counted by two licensed positions (DYAD) or two liens (Astaria sale flow).
2. Collateral ratio passes checks it should not.
3. **Impact**: over-borrowing / stolen sale proceeds.

#### Vulnerable Pattern Examples

**Example 1: Zero-amount deposit pushes to the valuation list (Folks Finance)** [HIGH]
```solidity
// ❌ VULNERABLE: fAmount == 0 still grows colPools; valuation counts per entry
function increaseCollateral(LoanManagerState.UserLoan storage loan, uint8 poolId, uint256 fAmount) external {
    if (loan.collaterals[poolId].balance == 0) loan.colPools.push(poolId); // @audit pushed N times via deposit(0)
    loan.collaterals[poolId].balance += fAmount; // 0 for null deposits
}
// getLoanLiquidity later:
for (uint8 i = 0; i < loan.colPools.length; i++) {   // @audit same poolId counted N times
    poolId = loan.colPools[i];
    balance = loan.collaterals[poolId].balance;       // full balance per entry
    effectiveValue += ...;                            // -> deposit * N
}
```

**Example 2: Sweep path moves real collateral (Frankencoin)** [HIGH]
```solidity
// ❌ VULNERABLE: legacy address != collateral address, but shares balances
function withdraw(address token, address target) external onlyOwner {
    if (token == collateral) {
        withdrawCollateral(target); // debt-checked path
    } else {
        IERC20(token).transfer(target, IERC20(token).balanceOf(address(this))); // @audit sweep
    }
}
// Attacker: dust with legacy token -> withdraw(LEGACY, full) -> real collateral gone, debt remains
```

**Example 3: Wrong operand in repay-with-collateral (Folks Finance)** [HIGH]
```solidity
// ❌ VULNERABLE: totalAmount drifts upward — breaks pool invariant
function updateWithRepayWithCollateral(HubPoolState.PoolData storage pool, uint256 principalPaid, uint256 interestPaid, uint256 loanStableRate)
    external returns (DataTypes.RepayWithCollateralPoolParams memory) {
    pool.depositData.totalAmount -= principalPaid - interestPaid; // @audit wrong quantity
}
// Invariant that should hold: depositData.totalAmount <= poolBalance + totalBorrowed
```

### Impact Analysis

#### Technical Impact

- Borrowing power inflated by an unbounded multiplier (5/8 unique findings: V1-V5 family)
- Collateral exit without debt repayment via token-identity confusion (1/8: V6)
- Registry/lien-level double counting (2/8: V7, V8)
- Corrupted pool-level accounting propagating into utilization, rates, and indexes (1/8: V5)

#### Business Impact

- Direct pool drains bounded only by borrow caps (Folks Finance series — bounty-paid findings)
- Unbacked debt issuance (Frankencoin ZCHF)
- Yield theft and eventual inability to operate the pool (repay-with-collateral inflation)

#### Affected Scenarios

- Cross-chain or spoke-hub designs where deposit amounts arrive decoupled from lock state
- Protocols allowing arbitrary ERC20 collateral with sweep functions on the same contract
- CDPs with generic `withdraw(token)` escape hatches
- Registries licensing vaults/positions where the same value can back multiple entries

### Secure Implementation

**Fix 1: Validate amounts and de-duplicate structural state**
```solidity
// ✅ SECURE: reject zero amounts; never push duplicates
function increaseCollateral(LoanManagerState.UserLoan storage loan, uint8 poolId, uint256 fAmount) external {
    require(fAmount > 0, "zero amount");
    if (loan.collaterals[poolId].balance == 0 && !loan.colPoolsContains[poolId]) loan.colPools.push(poolId);
    loan.collaterals[poolId].balance += fAmount;
}
```

**Fix 2: Sweep functions cannot touch collateral-adjacent balances**
```solidity
// ✅ SECURE: verify the collateral balance is unchanged after any sweep (Frankencoin mitigation)
function withdraw(address token, address target) external onlyOwner {
    uint256 before = IERC20(collateral).balanceOf(address(this));
    if (token == collateral) revert("use withdrawCollateral");
    IERC20(token).transfer(target, IERC20(token).balanceOf(address(this)));
    require(IERC20(collateral).balanceOf(address(this)) == before, "collateral moved"); // double-entrypoint guard
}
```

**Fix 3: Ledger updates preserve the pool invariant**
```solidity
// ✅ SECURE: subtract exactly the principal consumed by the repay-with-collateral
pool.depositData.totalAmount -= principalPaid;
assert(pool.depositData.totalAmount <= IERC20(asset).balanceOf(address(pool)) + pool.borrowData.totalAmount);
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- valuation loops over push-growable per-user arrays/sets while balances live in a parallel mapping
- zero-amount acceptance on any state-mutating collateral function
- generic sweep/withdraw-by-address on a contract that also holds collateral
- ledger updates mixing principal and interest terms in one subtraction
- registries where the same underlying asset can be attached to multiple positions
```

#### High-Signal Grep Seeds
```
- increaseCollateral
- colPools
- effectiveCollateralValue
- getLoanLiquidity
- isLoanOverCollateralized
- updateWithRepayWithCollateral
- depositData.totalAmount
- withdrawCollateral
```

#### Code Patterns to Look For
```
- Pattern 1: `if (balance == 0) list.push(id)` with no `amount > 0` require earlier in the path
- Pattern 2: `for (i < loan.colPools.length) { value += balances[colPools[i]] }`
- Pattern 3: `token == collateral ? withdrawCollateral(...) : IERC20(token).transfer(...)` (sweep escape)
- Pattern 4: `totalAmount -= principalPaid - interestPaid` style mixed-operand updates
- Pattern 5: two positions/licensing entries able to reference one collateral balance
```

#### Audit Checklist
- [ ] Call every collateral state-changer with amount = 0: what structural state mutates?
- [ ] Is each pool/asset counted exactly once in effective collateral? Trace the iteration structure for duplicates.
- [ ] Can any sweep/withdraw-by-address path move the canonical collateral (including via delegate/legacy token addresses)?
- [ ] Do repay-with-collateral updates preserve `totalAmount <= balance + totalBorrowed`? Test the invariant.
- [ ] Can one underlying asset back two registered positions/liens simultaneously?

### Real-World Examples

#### Known Exploits
- Compound TUSD integration issue (double-entrypoint token retrospective, cited by [V6]) — OpenZeppelin blog
- Folks Finance x-chain series — Immunefi bounty findings (5 paid reports, same root-cause family)

#### Related CVEs/Reports
- OpenZeppelin "Compound TUSD Integration Issue Retrospective"
- Immunefi Folks Finance reports (solodit 61016, 61040, 61048, 61063, 61090)

### Prevention Guidelines

#### Development Best Practices
1. Reject zero-amount state mutations everywhere collateral structure changes; separate "register asset" from "deposit value".
2. Iterate mappings by key for valuation, or maintain a deduplicated set with membership flags.
3. Sweep functions must assert the collateral balance is unchanged across the call (identity-agnostic defense).
4. Invariant-test pool ledgers: `totalAmount <= balance + totalBorrowed` after every operation.

#### Testing Requirements
- Unit tests for: N × deposit(0) then deposit(X) → effective collateral == X (not N·X); withdraw(legacy) cannot move canonical collateral
- Property tests: effectiveCollateralValue == Σ value(unique locked positions) for arbitrary deposit/withdraw sequences
- Fuzzing targets: repay-with-collateral sequences asserting the pool invariant

### References

#### Technical Documentation
- ERC20 double-entrypoint pattern (TUSD/TrueUSD delegate architecture)
- Aave collateral listing (per-asset mapping, no per-user iteration)

#### Security Research
- Immunefi Folks Finance x-chain reports (zero-deposit inflation family)
- Code4rena 2023-04-frankencoin issue (double-entrypoint exit)

### Keywords for Search

`collateral inflation`, `zero deposit`, `null deposit`, `colPools`, `effectiveCollateralValue`, `double counting collateral`, `double-entrypoint token`, `TUSD`, `collateral sweep`, `withdraw without repay`, `repay with collateral`, `totalAmount inflation`, `over borrowing`, `borrowing power inflation`, `collateral ledger`, `lien double taking`, `vault licensing double count`

### Related Vulnerabilities

- [Bad Debt Socialization and Missing Write-Off](../bad-debt/bad-debt-socialization.md)
- [Health Factor and Collateral Ratio Miscalculation](../risk-params/health-factor-miscalculation.md)
- [Supply and Borrow Cap Enforcement Bypass](../caps/supply-borrow-cap-bypass.md)
- `DB/general/token-compatibility/non-standard-token-vulnerabilities.md`
