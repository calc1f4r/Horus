---
# Core Classification
protocol: Backed Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1860
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backed-protocol-contest
source_link: https://code4rena.com/reports/2022-04-backed
github_link: https://github.com/code-423n4/2022-04-backed-findings/issues/27

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-05] Borrowers lose funds if they call `repayAndCloseLoan` instead of `closeLoan`

### Overview


This bug report concerns a vulnerability in the `repayAndCloseLoan` function of the `NFTLoanFacilitator.sol` contract. The vulnerability is that the function does not revert if there has not been a lender for a loan. This means that users can lose funds if they ever approved the contract, as the function performs a `ERC20(loan.loanAssetContractAddress).safeTransferFrom(msg.sender, lender, interest + loan.loanAmount)` call where `interest` will be a high value accumulated from timestamp 0 and the `loan.loanAmount` is the initially desired min loan amount `minLoanAmount` set in `createLoan`.

The recommended mitigation step for this vulnerability is to add a check that there actually is something to repay. This can be done by adding a `require` statement that checks if `loan.lastAccumulatedTimestamp > 0`, and if not, to revert the transaction with an error message that states to use `closeLoan` instead.

### Original Finding Content

_Submitted by cmichel_

[NFTLoanFacilitator.sol#L241](https://github.com/code-423n4/2022-04-backed/blob/e8015d7c4b295af131f017e646ba1b99c8f608f0/contracts/NFTLoanFacilitator.sol#L241)<br>

The `repayAndCloseLoan` function does not revert if there has not been a lender for a loan (matched with `lend`).
Users should use `closeLoan` in this case but the contract should disallow calling `repayAndCloseLoan` because users can lose funds.

It performs a `ERC20(loan.loanAssetContractAddress).safeTransferFrom(msg.sender, lender, interest + loan.loanAmount)` call where `interest` will be a high value accumulated from timestamp 0 and the `loan.loanAmount` is the initially desired min loan amount `minLoanAmount` set in `createLoan`.
The user will lose these funds if they ever approved the contract (for example, for another loan).

### Recommended Mitigation Steps

Add a check that there actually is something to repay.

```solidity
require(loan.lastAccumulatedTimestamp > 0, "loan was never matched by a lender. use closeLoan instead");
```

**[wilsoncusack (Backed Protocol) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/27#issuecomment-1090191862):**
 > ownerOf query here will fail if there is no lender, [NFTLoanFacilitator.sol#L239](https://github.com/code-423n4/2022-04-backed/blob/e8015d7c4b295af131f017e646ba1b99c8f608f0/contracts/NFTLoanFacilitator.sol#L239).

**[wilsoncusack (Backed Protocol) confirmed and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/27#issuecomment-1090376185):**
> Actually this is wrong, we switched to solmate and this ownerOf will not fail. Is a legit issue.
>
> Not an attack, but funds can be lost some. Medium probably makes sense? 

**[wilsoncusack (Backed Protocol) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/27#issuecomment-1091694388):**
 > Requires borrow to have approved the facilitator to move this erc20 and to call the wrong method.

**[wilsoncusack (Backed Protocol) resolved and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/27#issuecomment-1099377787):**
 > Yooo just discovered solmate had not followed the ERC721 standard on [this ownerOf](https://github.com/code-423n4/2022-04-backed/blob/main/contracts/NFTLoanFacilitator.sol#L239) and it should have reverted, updated here 
> 
> [Rari-Capital/solmate@921a9ad](https://github.com/Rari-Capital/solmate/commit/921a9ad4e22b995bd3d7b5464bcda294dd977209)

**[gzeon (judge) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/27#issuecomment-1100098358):**
 > Sponsor confirmed with fix.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backed
- **GitHub**: https://github.com/code-423n4/2022-04-backed-findings/issues/27
- **Contest**: https://code4rena.com/contests/2022-04-backed-protocol-contest

### Keywords for Search

`vulnerability`

