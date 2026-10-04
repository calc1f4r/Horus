---
# Core Classification
protocol: Arcade.xyz V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26450
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-arcade-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-arcade-securityreview.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Alexander Remie
  - Guillermo Larregay
  - Robert Schneider
---

## Vulnerability Title

Malicious borrowers can use forceRepay to grief lenders

### Overview


A bug report has been filed for the Arcade.xyz V3 Security Assessment. The malicious borrower can exploit a loophole in the RepaymentController contract by calling the forceRepay function instead of the repay function. This allows the borrower to pay less in gas fees and require the lender to perform a separate transaction to retrieve their funds (using the redeemNote function) and to pay a redeem fee. The lender must call the redeemNote function in RepaymentController, which in turn calls LoanCore.redeemNote, which transfers the tokens to an address set by the lender in the call. The borrower can save on gas fees and the lender has to pay an additional fee (LENDER_REDEEM_FEE) to get back their own tokens. 

The recommendation to mitigate this bug is to remove the incentive (the lower gas cost) for the borrower to call forceRepay instead of repay. This can be done by either removing the repay function and requiring the borrower to call forceRepay or removing the forceRepay function and modifying the repay function so that it transfers the funds to the lender in a try/catch statement and creates a redeem note which the lender can exchange for their funds using the redeemNote function.

In the long term, when designing a smart contract protocol, it is important to consider the incentives for each party to perform actions in the protocol and avoid making an actor pay for the mistakes or maliciousness of others. By thoroughly documenting the incentives structure, flaws can be spotted and mitigated before the protocol goes live.

### Original Finding Content

## Description

A malicious borrower can grief a lender by calling the `forceRepay` function instead of the `repay` function; doing so would allow the borrower to pay less in gas fees and require the lender to perform a separate transaction to retrieve their funds (using the `redeemNote` function) and to pay a redeem fee.

At any time after the loan is set and before the lender claims the collateral if the loan is past its due date, the borrower has to pay their full debt back in order to recover their assets. For doing so, there are two functions in `RepaymentController`: `repay` and `forceRepay`. The difference between them is that the latter transfers the tokens to the `LoanCore` contract instead of directly to the lender. It is meant to allow the borrower to pay their obligations when the lender cannot receive tokens for any reason.

For the lender to get their tokens back in this scenario, they must call the `redeemNote` function in `RepaymentController`, which in turn calls `LoanCore.redeemNote`, which transfers the tokens to an address set by the lender in the call.

Because the borrower is free to decide which function to call to repay their debt, they can arbitrarily decide to do so via `forceRepay`, obligating the lender to send a transaction (with its associated gas fees) to recover their tokens. Additionally, depending on the configuration of the protocol, it is possible that the lender has to pay an additional fee (`LENDER_REDEEM_FEE`) to get back their own tokens, cutting their profits with no chance to opt out.

```solidity
RC_InvalidState(data.state);
```

```solidity
function redeemNote(uint256 loanId, address to) external override {
    LoanLibrary.LoanData memory data = loanCore.getLoan(loanId);
    (, uint256 amountOwed) = loanCore.getNoteReceipt(loanId);
    if (data.state != LoanLibrary.LoanState.Repaid) revert;
    address lender = lenderNote.ownerOf(loanId);
    if (lender != msg.sender) revert RC_OnlyLender(lender, msg.sender);
    uint256 redeemFee = (amountOwed * feeController.get(FL_09)) /
}
```

```solidity
loanCore.redeemNote(loanId, redeemFee, to);
```

*Figure 16.1: The redeemNote function in `arcade-protocol/contracts/RepaymentController.sol`*

Note that, from the perspective of the borrower, it is actually cheaper to call `forceRepay` than `repay` because of the gas saved by not transferring the tokens to the lender and not burning one of the promissory notes.

## Exploit Scenario

Bob has to pay back his loan, and he decides to do so via `forceRepay` to save gas in the transaction. Lucy, the lender, wants her tokens back. She is now forced to call `redeemNote` to get them. In this transaction, she lost the gas fees that the borrower would have paid to send the tokens directly to her, and she has to pay an additional fee (`LENDER_REDEEMER_FEE`), causing her to receive less value from the loan than she originally expected.

## Recommendations

Short term, remove the incentive (the lower gas cost) for the borrower to call `forceRepay` instead of `repay`. Consider taking one of the following actions:

- Force the lender to always pull their funds using the `redeemNote` function. This can be achieved by removing the `repay` function and requiring the borrower to call `forceRepay`.
- Remove the `forceRepay` function and modify the `repay` function so that it transfers the funds to the lender in a try/catch statement and creates a redeem note (which the lender can exchange for their funds using the `redeemNote` function) only if that transfer fails.

Long term, when designing a smart contract protocol, always consider the incentives for each party to perform actions in the protocol, and avoid making an actor pay for the mistakes or maliciousness of others. By thoroughly documenting the incentives structure, flaws can be spotted and mitigated before the protocol goes live.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Arcade.xyz V3 |
| Report Date | N/A |
| Finders | Alexander Remie, Guillermo Larregay, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-arcade-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-07-arcade-securityreview.pdf

### Keywords for Search

`vulnerability`

