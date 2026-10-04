---
# Core Classification
protocol: Cooler Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26354
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/107
source_link: none
github_link: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/119

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
finders_count: 10
finders:
  - Negin
  - jkoppel
  - klaus
  - bitx0x
  - pengun
---

## Vulnerability Title

H-2: At claimDefaulted, the lender may not receive the token because the Unclaimed token is not processed

### Overview


A bug has been identified in the `claimDefaulted` function of the Cooler smart contract. This bug prevents the lender from receiving the debt repayment in the form of unclaimed tokens. The code snippet in which the bug occurs is located at https://github.com/sherlock-audit/2023-08-cooler/blob/6d34cd12a2a15d2c92307d44782d6eae1474ab25/Cooler/src/Cooler.sol#L318-L320. The bug is caused by the fact that the `loan.unclaimed` is not checked before the loan data is deleted. As a result, if `claimDefaulted` is called while there are unclaimed tokens, the lender will not be able to get the unclaimed tokens.

The bug was identified by 0xMAKEOUTHILL, Chinmay, Negin, banditx0x, deadrxsezzz, jkoppel, klaus, mahdikarimi, pengun, and xAlismx. The bug was found through manual review. The recommended solution is to process the unclaimed tokens before deleting the loan data. This was approved by jkoppel. The fix for the bug can be found at https://github.com/ohmzeus/Cooler/pull/54 and https://github.com/ohmzeus/Cooler/pull/47.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/119 

## Found by 
0xMAKEOUTHILL, Chinmay, Negin, banditx0x, deadrxsezzz, jkoppel, klaus, mahdikarimi, pengun, xAlismx

`claimDefaulted` does not handle `loan.unclaimed`  . This preventing the lender from receiving the debt repayment.

## Vulnerability Detail

```solidity
function claimDefaulted(uint256 loanID_) external returns (uint256, uint256, uint256) {
  Loan memory loan = loans[loanID_];
  delete loans[loanID_];
```

 Loan data is deletead in `claimDefaulted` function. `loan.unclaimed` is not checked before data deletead. So, if `claimDefaulted` is called while there are unclaimed tokens, the lender will not be able to get the unclaimed tokens.

## Impact

Lender cannot get unclaimed token.

## Code Snippet

[https://github.com/sherlock-audit/2023-08-cooler/blob/6d34cd12a2a15d2c92307d44782d6eae1474ab25/Cooler/src/Cooler.sol#L318-L320](https://github.com/sherlock-audit/2023-08-cooler/blob/6d34cd12a2a15d2c92307d44782d6eae1474ab25/Cooler/src/Cooler.sol#L318-L320)

## Tool used

Manual Review

## Recommendation

Process unclaimed tokens before deleting loan data.

```diff
function claimDefaulted(uint256 loanID_) external returns (uint256, uint256, uint256) {
+   claimRepaid(loanID_)
    Loan memory loan = loans[loanID_];
    delete loans[loanID_];
```



## Discussion

**0xRusowsky**

- fix: https://github.com/ohmzeus/Cooler/pull/54
- https://github.com/ohmzeus/Cooler/pull/47

**jkoppel**

Fix approved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler Update |
| Report Date | N/A |
| Finders | Negin, jkoppel, klaus, bitx0x, pengun, mahdikarimi, deadrxsezzz, 0xMAKEOUTHILL, xAlismx, Chinmay |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/119
- **Contest**: https://app.sherlock.xyz/audits/contests/107

### Keywords for Search

`vulnerability`

