---
# Core Classification
protocol: Fuji Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16526
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dominik Muhs
  -  Martin Ortner

---

## Vulnerability Title

Unchecked Return Values - ICErc20 repayBorrow

### Overview


This bug report is about the `ICErc20.repayBorrow` method of multiple providers, which may return a non-zero uint on error. The problem is that multiple providers do not check for this error condition and might return `success` even though `repayBorrow` failed, returning an error code. This could potentially allow a malicious user to call `paybackAndWithdraw()` without actually repaying, causing an error in the sub-call to `Compound.repayBorrow()` that is silently ignored.

The code snippets provided in the report show the `ICErc20.repayBorrow` method, the `CToken.repayBorrowInternal` method, and examples of the `ProviderCream.repayBorrow`, `ProviderScream.repayBorrow`, and `ProviderCompound.repayBorrow` methods. The report recommends that the providers check for `cyToken.repayBorrow(_amount) != 0` or `Error.NO_ERROR` in order to avoid this bug from occurring.

### Original Finding Content

#### Description


`ICErc20.repayBorrow` returns a non-zero uint on error. Multiple providers do not check for this error condition and might return `success` even though `repayBorrow` failed, returning an error code.


This can potentially allow a malicious user to call `paybackAndWithdraw()` while not repaying by causing an error in the sub-call to `Compound.repayBorrow()`, which ends up being silently ignored. Due to the missing success condition check, execution continues normally with `_internalWithdraw()`.


Also, see [issue 4.5](#unchecked-return-values---icomptroller-exitmarket-entermarket).


**code/contracts/interfaces/compound/ICErc20.sol:L11-L12**



```

function repayBorrow(uint256 repayAmount) external returns (uint256);

```
The method may return an error due to multiple reasons:


**contracts/CToken.sol:L808-L816**



```
function repayBorrowInternal(uint repayAmount) internal nonReentrant returns (uint, uint) {
 uint error = accrueInterest();
 if (error != uint(Error.NO\_ERROR)) {
 // accrueInterest emits logs on errors, but we still want to log the fact that an attempted borrow failed
 return (fail(Error(error), FailureInfo.REPAY\_BORROW\_ACCRUE\_INTEREST\_FAILED), 0);
 }
 // repayBorrowFresh emits repay-borrow-specific logs on errors, so we don't need to
 return repayBorrowFresh(msg.sender, msg.sender, repayAmount);
}

```
**contracts/CToken.sol:L855-L873**



```
if (allowed != 0) {
 return (failOpaque(Error.COMPTROLLER\_REJECTION, FailureInfo.REPAY\_BORROW\_COMPTROLLER\_REJECTION, allowed), 0);
}

/\* Verify market's block number equals current block number \*/
if (accrualBlockNumber != getBlockNumber()) {
 return (fail(Error.MARKET\_NOT\_FRESH, FailureInfo.REPAY\_BORROW\_FRESHNESS\_CHECK), 0);
}

RepayBorrowLocalVars memory vars;

/\* We remember the original borrowerIndex for verification purposes \*/
vars.borrowerIndex = accountBorrows[borrower].interestIndex;

/\* We fetch the amount the borrower owes, with accumulated interest \*/
(vars.mathErr, vars.accountBorrows) = borrowBalanceStoredInternal(borrower);
if (vars.mathErr != MathError.NO\_ERROR) {
 return (failOpaque(Error.MATH\_ERROR, FailureInfo.REPAY\_BORROW\_ACCUMULATED\_BALANCE\_CALCULATION\_FAILED, uint(vars.mathErr)), 0);
}

```
#### Examples


Multiple providers, here are some examples:


**code/contracts/fantom/providers/ProviderCream.sol:L168-L173**



```

 // Check there is enough balance to pay
 require(erc20token.balanceOf(address(this)) >= \_amount, "Not-enough-token");
 erc20token.univApprove(address(cyTokenAddr), \_amount);
 cyToken.repayBorrow(\_amount);
}

```
**code/contracts/fantom/providers/ProviderScream.sol:L170-L172**



```
require(erc20token.balanceOf(address(this)) >= \_amount, "Not-enough-token");
erc20token.univApprove(address(cyTokenAddr), \_amount);
cyToken.repayBorrow(\_amount);

```
**code/contracts/mainnet/providers/ProviderCompound.sol:L139-L155**



```
if (\_isETH(\_asset)) {
 // Create a reference to the corresponding cToken contract
 ICEth cToken = ICEth(cTokenAddr);

 cToken.repayBorrow{ value: msg.value }();
} else {
 // Create reference to the ERC20 contract
 IERC20 erc20token = IERC20(\_asset);

 // Create a reference to the corresponding cToken contract
 ICErc20 cToken = ICErc20(cTokenAddr);

 // Check there is enough balance to pay
 require(erc20token.balanceOf(address(this)) >= \_amount, "Not-enough-token");
 erc20token.univApprove(address(cTokenAddr), \_amount);
 cToken.repayBorrow(\_amount);
}

```
#### Recommendation


Check for `cyToken.repayBorrow(_amount) != 0` or `Error.NO_ERROR`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fuji Protocol |
| Report Date | N/A |
| Finders | Dominik Muhs,  Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/03/fuji-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

