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
solodit_id: 26442
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

Risk of lost funds due to lack of zero-address check in functions

### Overview


This bug report describes a data validation issue in the VaultFactory.claimFees, RepaymentController.redeemNote, LoanCore.withdraw, and LoanCore.withdrawProtocolFees functions. The issue is that these functions are missing a check to ensure that the to argument does not equal the zero address. This means that these functions could transfer funds to the zero address. 

An exploit scenario is given where a script used to periodically withdraw the protocol fees is updated with a mistake that leaves the to argument uninitialized. When the script is executed, the to argument defaults to the zero address, causing the withdrawProtocolFees to transfer the protocol fees to the zero address. 

The recommendation is to add a check to verify that to does not equal the zero address to the functions mentioned above. Additionally, it is recommended to use the Slither static analyzer to catch common issues such as this one, and to consider integrating a Slither scan into the project’s CI pipeline, pre-commit hooks, or build scripts.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

**File Locations:**  
- `contracts/RepaymentController.sol`  
- `contracts/LoanCore.sol`

## Description

The `VaultFactory.claimFees` (figure 8.1), `RepaymentController.redeemNote` (figure 8.2), `LoanCore.withdraw`, and `LoanCore.withdrawProtocolFees` functions are all missing a check to ensure that the `to` argument does not equal the zero address. As a result, these functions could transfer funds to the zero address.

### Example Code

#### VaultFactory.claimFees
```solidity
function claimFees(address to) external onlyRole(FEE_CLAIMER_ROLE) {
    uint256 balance = address(this).balance;
    payable(to).transfer(balance);
    emit ClaimFees(to, balance);
}
```
**Figure 8.1:** The claimFees function in `arcade-protocol/contracts/vault/VaultFactory.sol`

#### RepaymentController.redeemNote
```solidity
function redeemNote(uint256 loanId, address to) external override {
    LoanLibrary.LoanData memory data = loanCore.getLoan(loanId);
    (, uint256 amountOwed) = loanCore.getNoteReceipt(loanId);
    if (data.state != LoanLibrary.LoanState.Repaid) revert RC_InvalidState(data.state);
    
    address lender = lenderNote.ownerOf(loanId);
    if (lender != msg.sender) revert RC_OnlyLender(lender, msg.sender);
    
    uint256 redeemFee = (amountOwed * feeController.get(FL_09)) / BASIS_POINTS_DENOMINATOR;
    loanCore.redeemNote(loanId, redeemFee, to);
}
```
**Figure 8.2:** The redeemNote function in `arcade-protocol/contracts/RepaymentController.sol`

## Exploit Scenario

A script that is used to periodically withdraw the protocol fees (calling `LoanCore.withdrawProtocolFees`) is updated. Due to a mistake, the `to` argument is left uninitialized. The script is executed, and the `to` argument defaults to the zero address, causing `withdrawProtocolFees` to transfer the protocol fees to the zero address.

## Recommendations

**Short term:** Add a check to verify that `to` does not equal the zero address to the following functions:
- `VaultFactory.claimFees`
- `RepaymentController.redeemNote`
- `LoanCore.withdraw`
- `LoanCore.withdrawProtocolFees`

**Long term:** Use the Slither static analyzer to catch common issues such as this one. Consider integrating a Slither scan into the project’s CI pipeline, pre-commit hooks, or build scripts.

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

