---
# Core Classification
protocol: Astaria
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7301
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - access_control

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Anyone can take a loan out on behalf of any collateral holder at any terms

### Overview


This bug report is about the VaultImplementation.sol#L225 function called validateCommitment(). This function is intended to ensure that the caller who is requesting the lien has access to the collateral. The caller also inputs a receiver who will receive the lien. The receiver is checked against the collateral holder, and the validation is approved if they match. 

However, this does not imply that the collateral holder wants to take the loan. This opens the door to a malicious lender pushing unwanted loans on holders of collateral by calling commitToLien with their collateralId, as well as their address set to the receiver. This will pass the receiver == holder check and execute the loan. 

In the best case, the borrower discovers this and quickly repays the loan, incurring a fee and small amount of interest. In the worst case, the borrower doesn't know this happens and their collateral is liquidated. 

The recommendation is to only allow calls from the holder or operator to lead to valid commitments. The msg.sender should be checked against the holder, operator, and receiver. If the sender is not the holder, operator, or receiver, then the CT.isApprovedForAll(holder, msg.sender) should be checked. If none of these checks pass, then the loan should be reverted with the NotApprovedForBorrow() message.

### Original Finding Content

## Security Vulnerability Report

## Severity
**High Risk**

## Context
`VaultImplementation.sol#L225`

## Description
In the `_validateCommitment()` function, the initial checks are intended to ensure that the caller who is requesting the lien is someone who should have access to the collateral that it's being taken out against. The caller also inputs a receiver, who will be receiving the lien. 

In this validation, this receiver is checked against the collateral holder, and the validation is approved in the case that `receiver == holder`. However, this does not imply that the collateral holder wants to take this loan.

This opens the door to a malicious lender pushing unwanted loans on holders of collateral by calling `commitToLien` with their `collateralId`, as well as their address set to the receiver. This will pass the `receiver == holder` check and execute the loan.

In the best case, the borrower discovers this and quickly repays the loan, incurring a fee and a small amount of interest. In the worst case, the borrower doesn't know this happens, and their collateral is liquidated.

## Recommendation
Only allow calls from the holder or operator to lead to valid commitments:

```solidity
address holder = CT.ownerOf(collateralId);
address operator = CT.getApproved(collateralId);

if (
    msg.sender != holder &&
    receiver != holder &&
    receiver != operator &&
    !ROUTER().isValidVault(receiver)
) {
    msg.sender != operator &&
    CT.isApprovedForAll(holder, msg.sender)
) {
    if (operator != address(0)) {
        require(operator == receiver);
    } else {
        require(CT.isApprovedForAll(holder, receiver));
    }
} else {
    revert NotApprovedForBorrow();
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Access Control`

