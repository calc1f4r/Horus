---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7294
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
  - validation
  - business_logic

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

Refactor _paymentAH()

### Overview


This bug report is about the function _paymentAH() in the LienToken.sol file. The function has several vulnerabilities, including that the stack is a memory parameter and updates made to stack are not applied back to the corresponding storage variable. Additionally, there is no need to update stack[position] as it is deleted later and decreaseEpochLienCount() is always passed 0 as stack[position] is already deleted. The if/else block can be merged and updateAfterLiquidationPayment() expects msg.sender to be LIEN_TOKEN. The recommendation is to apply the given diff to the function and note other issues related to _paymentAH() such as avoiding shadowing variables and commenting or removing unused function parameters. The bug was fixed in PR 201 and verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity: 
**High Risk**

## Context: 
**LienToken.sol#L571**

## Description: 
The `_paymentAH()` function has several vulnerabilities:

- The `stack` parameter is defined as a memory parameter, so any updates made to `stack` do not reflect back in the corresponding storage variable.
- There is no need to update `stack[position]` as it is deleted later.
- The function `decreaseEpochLienCount()` is always passed `0`, as `stack[position]` has already been deleted. Furthermore, `decreaseEpochLienCount()` expects `epoch`, but `end` is passed instead.
- The if/else block can be merged. The function `updateAfterLiquidationPayment()` expects `msg.sender` to be `LIEN_TOKEN`, which should work as expected.

## Recommendation:
Apply the following diff:

```solidity
function _paymentAH(
    LienStorage storage s,
    uint256 collateralId,
    - AuctionStack[] memory stack,
    + AuctionStack[] storage stack,
    uint256 position,
    uint256 payment,
    address payer
) internal returns (uint256) {
    uint256 lienId = stack[position].lienId;
    uint256 end = stack[position].end;
    uint256 owing = stack[position].amountOwed;

    //checks the lien exists
    address owner = ownerOf(lienId);
    address payee = _getPayee(s, lienId);

    - if (owing > payment.safeCastTo88()) {
    -     stack[position].amountOwed -= payment.safeCastTo88();
    - } else {
    + if (owing < payment.safeCastTo88()) {
        payment = owing;
    }

    s.TRANSFER_PROXY.tokenTransferFrom(s.WETH, payer, payee, payment);
    delete s.lienMeta[lienId]; //full delete
    delete stack[position];
    _burn(lienId);

    if (_isPublicVault(s, payee)) {
    -     if (owner == payee) {
            IPublicVault(payee).updateAfterLiquidationPayment(
                IPublicVault.LiquidationPaymentParams({lienEnd: end})
            );
    -     } else {
    -         IPublicVault(payee).decreaseEpochLienCount(stack[position].end);
    -     }
    }
    emit Payment(lienId, payment);
    return payment;
}
```

## Additional Notes:
Other issues related to `_paymentAH()` include:

- Avoid shadowing variables.
- Comment or remove unused function parameters.

**Astaria:** Fixed in PR 201.  
**Spearbit:** Verified.

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

`Validation, Business Logic`

