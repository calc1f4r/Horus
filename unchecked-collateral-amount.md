---
# Core Classification
protocol: Skillet Kettle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47824
audit_firm: OtterSec
contest_link: https://www.skillet.ai/
source_link: https://www.skillet.ai/
github_link: https://github.com/Skillet-Capital/kettle/

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
finders_count: 3
finders:
  - Robert Chen
  - Woosun Song
  - OtterSec
---

## Vulnerability Title

Unchecked Collateral Amount

### Overview


The report discusses a bug in the refinance function of the Kettle.sol solidity code. This function allows borrowers to refinance their existing loans with a new loan offer. However, the function only checks for the equivalence of the NFT address/ID and neglects the amount, which can be exploited by attackers to steal funds. The report provides a step-by-step attack scenario and suggests adding amount checks for ERC-1155 collateral as a solution. The bug has been fixed in the latest version of the code.

### Original Finding Content

## Refinance Function Overview

The refinance function enables a borrower to refinance an existing loan with a new loan offer. It verifies if the collateral specified in the new loan offer is identical to the original one, which is specified in the lien.

## Kettle.sol - Solidity Code

```solidity
function _refinance(
    Lien calldata lien,
    uint256 lienId,
    uint256 loanAmount,
    LoanOffer calldata offer,
    OfferAuth calldata auth,
    bytes calldata offerSignature,
    bytes calldata authSignature
) internal {
    // [1] address equivalence
    if (lien.collection != offer.collection) {
        revert CollectionsDoNotMatch();
    }
    /* ... */
}

function refinance(
    /* ... */
) public validateLien(lien, lienId) lienIsActive(lien) {
    // token Id equivalence
    CollateralVerifier.verifyCollateral(
        offer.collateralType,
        offer.collateralIdentifier,
        lien.tokenId,
        proof
    );
    _refinance(lien, lienId, loanAmount, offer, auth, offerSignature,
    ,→ authSignature);
}
```

However, the collateral verification for the selected loan type is insufficient, because it only checks the equivalence of the NFT address/ID and neglects the amount. This oversight may allow an attacker to steal funds by manipulating the amount of collateral during refinancing loans backed by ERC-1155 collateral.

## Audit 04 | Vulnerabilities

### Proof of Concept

Below is a step-by-step attack scenario utilizing two loan offers involving an ERC-1155 token (NFTx):

- **Loan Offers:**
  - **Offer A:** This offer takes two units of the ERC-1155 token NFTx as collateral and lends $2000.
  - **Offer B:** This offer takes one unit of the ERC-1155 token NFTx as collateral and lends $1000.

- **Malicious Borrower’s Actions:**
  - The malicious borrower initiates the attack by taking offer B, which requires providing one unit of NFTx as collateral in exchange for a $1000 loan.
  - After obtaining the $1000 loan from offer B, the borrower immediately attempts to refinance the loan with offer A.

- **Refinancing:**
  - During the refinance process, instead of providing the correct collateral hash (NFTx, 2), the borrower constructs an authentication signature that contains the collateral hash for (NFTx, 1), i.e., the collateral hash for offer A.

- **Exploiting the Vulnerability:**
  - Since refinance only checks the collateral type and token ID, the malicious borrower successfully refinances the loan, resulting in a $1000 profit to the borrower. On the other hand, the proposer of Offer B suffers a loss due to its loan being undercollateralized.
  - The verification process fails to acknowledge the difference in the collateral value between the two offers (from one unit to two units of NFTx).

## Remediation

Ensure to add amount checks for the ERC-1155 collateral.

### Patch

Fixed in e46c38d.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Skillet Kettle |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song, OtterSec |

### Source Links

- **Source**: https://www.skillet.ai/
- **GitHub**: https://github.com/Skillet-Capital/kettle/
- **Contest**: https://www.skillet.ai/

### Keywords for Search

`vulnerability`

