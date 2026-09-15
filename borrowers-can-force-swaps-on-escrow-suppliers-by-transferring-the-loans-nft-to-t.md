---
# Core Classification
protocol: Collar Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45138
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - R0bert
  - Om Parikh
  - 0xDjango
  - MiloTruck
---

## Vulnerability Title

Borrowers can force swaps on escrow suppliers by transferring the loan's NFT to them

### Overview


The bug report discusses a medium risk issue in the LoansNFT smart contract. It states that there is a problem with the way the contract checks for keeper approval in the closeLoan() and forecloseLoan() functions. This allows borrowers to forcefully swap cash assets held by the escrow supplier without their permission. To exploit this, the borrower must transfer the loan NFT to the escrow supplier and the supplier must have a dangling cash asset approval and actively call setKeeperApproved(). The report recommends having separate mappings for borrower and escrow supplier approvals to fix this issue. The bug has been fixed in a recent commit by removing the forecloseLoan() function. The likelihood of this issue occurring is low and it has been verified and resolved by removing the function.

### Original Finding Content

## Severity: Medium Risk

## Context
- **LoansNFT.sol**: Lines 264-265, Lines 425-426

## Description
In `LoansNFT.closeLoan()`, `_isSenderOrKeeperFor()` is called to check if the borrower has approved the keeper to close the loan on their behalf:
```solidity
address borrower = ownerOf(loanId);
require(_isSenderOrKeeperFor(borrower, loanId), "loans: not NFT owner or allowed keeper");
```

Similarly, in `LoansNFT.forecloseLoan()`, `_isSenderOrKeeperFor()` is called to check if the escrow supplier allows the keeper to call `forecloseLoan()` on their behalf:
```solidity
address escrowOwner = escrowNFT.ownerOf(escrowId);
require(_isSenderOrKeeperFor(escrowOwner, loanId), "loans: not escrow owner or allowed keeper");
```

However, since both `closeLoan()` and `forecloseLoan()` use the same `keeperApprovedFor` mapping to check for keeper approval, borrowers can forcefully swap `cashAsset` held by the escrow supplier into `underlying` without their permission.

This is achieved by directly transferring the loan NFT to the escrow supplier. For example:
- Assume Bob has a dangling cashAsset allowance to the LoansNFT contract.
- Alice calls `openLoan()` to open an escrowed loan with Bob as the escrow supplier. The loan has a `loanId` of 1337.
- Bob calls `setKeeperApproved()` for `loanId = 1337` to allow the keeper to call `forecloseLoan()` on his behalf.
- Alice transfers her loan NFT to Bob.
- After loan expiry, the keeper automatically calls `closeLoan()` to close the loan on Bob's behalf:
  - The `_isSenderOrKeeperFor(borrower, loanId)` check passes as `keeperApprovedFor[Bob][1337] = true`.
  - `loanAmount` of `cashAsset` is pulled from Bob and swapped to `underlyingAsset` without his permission.

**Note:** For this exploit to occur, the following conditions must be met:
1. The escrow supplier has a dangling approval of `cashAsset` to the LoansNFT contract.
2. The loan must be escrowed, so the attacker pays interest for the loan.
3. The escrow supplier has to actively call `setKeeperApproved()` after the loan is created.

However, this scenario is still entirely plausible if the loan was created without malicious intention but happens to become non-profitable for the borrower after expiration. For example, in the scenario above, Alice opens the escrowed loan believing that the price of `underlyingAsset` will increase and has no intentions to perform such an attack. However, after expiration, she sees that calling `closeLoan()` is non-profitable or would incur a loss for her (e.g., `underlyingAsset` price goes below `putStrikePrice` or the loan incurs late fees), so she performs this attack to grief the escrow supplier.

## Recommendation
Consider having two mappings (e.g., `keeperApprovedForBorrower` and `keeperApprovedForEscrowSupplier`) to separate borrower and escrow supplier approvals. `keeperApprovedForBorrower` would be used in `closeLoan()` while `keeperApprovedForEscrowSupplier` is used in `forecloseLoan()`.

## Collar
Fixed in commit `897a702d` by removing foreclosure flow and complexity entirely. The likelihood is very low since even for the few users that end up in this situation, there is a single target they can grief, and that escrow owner needs to also have a sufficient cash approval and balance to Loans (even though they are a supplier of underlying) and have approved a keeper for foreclosing that specific loan. The attacker has 1 day when this is possible since if their position is empty, foreclosure (by keeper) will happen after `min grace`.

## Spearbit
Verified, `forecloseLoan()` has been removed in the new protocol design. As such, this issue is resolved as escrow suppliers no longer grant approval to the keeper.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Collar Protocol |
| Report Date | N/A |
| Finders | R0bert, Om Parikh, 0xDjango, MiloTruck |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Collar-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

