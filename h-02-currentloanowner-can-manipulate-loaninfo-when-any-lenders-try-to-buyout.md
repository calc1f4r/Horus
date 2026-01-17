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
solodit_id: 1854
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backed-protocol-contest
source_link: https://code4rena.com/reports/2022-04-backed
github_link: https://github.com/code-423n4/2022-04-backed-findings/issues/88

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
  - rayn
---

## Vulnerability Title

[H-02] currentLoanOwner can manipulate loanInfo when any lenders try to buyout

### Overview


This bug report is about a vulnerability in the NFTLoanFacilitator.sol contract on the code-423n4/2022-04-backed repository. The vulnerability allows an attacker to manipulate the loanInfo data structure when a lender tries to buyout a loan that the attacker has already lent to. The attacker can set bad values of loanInfo, such as a very long duration and 0 interest rate, which the lender would not expect. The attack is successful when the loanAssetContractAddress is an ERC777, which is susceptible to reentrancy attacks. The attacker can call the lend() function again in reentrancy with the manipulated parameters. The recommended mitigation step is to use the nonReentrant modifier on the lend() function to prevent reentrancy attacks.

### Original Finding Content

_Submitted by rayn_

[NFTLoanFacilitator.sol#L205-L208](https://github.com/code-423n4/2022-04-backed/blob/main/contracts/NFTLoanFacilitator.sol#L205-L208)<br>
[NFTLoanFacilitator.sol#L215-L218](https://github.com/code-423n4/2022-04-backed/blob/main/contracts/NFTLoanFacilitator.sol#L215-L218)

If an attacker already calls `lend()` to lend to a loan, the attacker can manipulate `loanInfo` by reentrancy attack when any lenders try to buyout. The attacker can set bad values of `lendInfo` (e.g. very long duration, and 0 interest rate) that the lender who wants to buyout don't expect.

### Proof of Concept

An attacker lends a loan, and `loanAssetContractAddress` in `loanInfo` is ERC777 which is suffering from reentrancy attack. When a lender (victim) try to buyout the loan of the attacker:

1.  The victim called `lend()`.
2.  In `lend()`, it always call `ERC20(loanAssetContractAddress).safeTransfer` to send `accumulatedInterest + previousLoanAmount` to `currentLoanOwner` (attacker).
3.  The `transfer` of `loanAssetContractAddress` ERC777 will call `_callTokensReceived` so that the attacker can call `lend()` again in reentrancy with parameters:
    *   loanId: same loan Id
    *   interestRate: set to bad value (e.g. 0)
    *   amount: same amount
    *   durationSeconds: set to bad value (e.g. a long durationSeconds)
    *   sendLendTicketTo: same address of the attacker (`currentLoanOwner`)
4.  Now the variables in `loanInfo` are changed to bad value, and the victim will get the lend ticket but the loan term is manipulated, and can not set it back (because it requires a better term).

### Tools Used

vim

### Recommended Mitigation Steps

Use `nonReentrant` modifier on `lend()` to prevent reentrancy attack: [OpenZeppelin/ReentrancyGuard.sol](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/security/ReentrancyGuard.sol)<br>

**[wilsoncusack (Backed Protocol) acknowledged, but disagreed with High severity and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/88#issuecomment-1091992426):**
 > We should mitigate, but will think on this.

**[wilsoncusack (Backed Protocol) confirmed and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/88#issuecomment-1092333890):**
 > Not sure whether this should be Medium or High risk.

**[wilsoncusack (Backed Protocol) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/88#issuecomment-1092723962):**
 > Thinking more, again we should definitely mitigate, but I think this is less severe because I do not think ERC777 tokens will work with our contract? The on received call will revert? So this would need to be a malicious ERC20 designed just for this.

**[wilsoncusack (Backed Protocol) resolved and commented](https://github.com/code-423n4/2022-04-backed-findings/issues/88#issuecomment-1092733796):**
 > er erc777 does work because reception ack is not needed in the normal case.

**[gzeon (judge) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/88#issuecomment-1100056759):**
 > Sponsor confirmed with fix.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | rayn |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backed
- **GitHub**: https://github.com/code-423n4/2022-04-backed-findings/issues/88
- **Contest**: https://code4rena.com/contests/2022-04-backed-protocol-contest

### Keywords for Search

`vulnerability`

