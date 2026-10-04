---
# Core Classification
protocol: Abacus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48702
audit_firm: OtterSec
contest_link: https://abacus.wtf/
source_link: https://abacus.wtf/
github_link: github.com/0xMedici/abacusLend.

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
finders_count: 4
finders:
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Liquidate is not Clearing the State Properly . . . . . . . . . .

### Overview


The Lend contract has a bug that can cause an NFT to get locked in the vault. This happens when a user borrows an NFT, liquidates it, and then another user borrows the same NFT. The details of the loan are not initialized properly, causing repay and liquidate functions to fail. To fix this, the loanDeployed[nft][id] value needs to be cleared in the liquidate function. This bug has been fixed in the latest version of the contract.

### Original Finding Content

## Lend Contract Overview

The Lend contract uses `loans[nft][id]` to store details and `loanDeployed[nft][id]` to track the state of the loan for an NFT. There are two ways to clear the loan: **repay** or **liquidate**. 

## Loan Clearing Methods

- **Repay:** This method clears both `loans[nft][id]` and `loanDeployed[nft][id]`.
- **Liquidate:** This method clears only `loans[nft][id]` and leaves `loanDeployed[nft][id]`.

## Borrow Function

The Borrow function uses `loanDeployed[nft][id]` to perform insertions or updates to the loan.

```solidity
if(!loanDeployed[nft][id]) {
    openLoan.pool = _pool;
    openLoan.amount = _amount;
    openLoan.borrower = msg.sender;
    loanDeployed[nft][id] = true;
} else {
    openLoan.amount += _amount;
}
```

Since `loanDeployed[nft][id]` was not cleared in the liquidate function, if the NFT is borrowed again, the details of the loan (pool, borrower) will not be initialized. This NFT would get locked in the vault, since repay requires borrower and liquidate requires pool values.

## Proof of Concept

To reproduce the issue, follow the steps below:

1. User A takes a loan by depositing an NFT.
2. The NFT is liquidated and User B buys the NFT.
3. User B takes a loan with the same NFT.

Since `openLoan.pool` and `openLoan.borrower` were not initialized, attempts to repay and liquidate will fail on User B’s loan.

---

© 2022 OtterSec LLC. All Rights Reserved.

## Remediation

Clear the `loanDeployed[nft][id]` value in the liquidate function.

```solidity
emit BorrowerLiquidated(openLoan.borrower, _pool, nft, id, loanAmount);
delete loanDeployed[nft][id];
delete loans[nft][id];
}
```

## Patch

`loanDeployed[nft][id]` was deleted in the liquidate function. Fixed in `762e95a`.

```diff
@@ -218,6 +218,7 @@ contract Lend is ReentrancyGuard {
    payable(msg.sender).transfer(2 * payoutPerResCurrent / 100);
    emit BorrowerLiquidated(openLoan.borrower, _pool, nft, id, loanAmount);
+   delete loanDeployed[nft][id];
    delete loans[nft][id];
}
```

---

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Abacus |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://abacus.wtf/
- **GitHub**: github.com/0xMedici/abacusLend.
- **Contest**: https://abacus.wtf/

### Keywords for Search

`vulnerability`

