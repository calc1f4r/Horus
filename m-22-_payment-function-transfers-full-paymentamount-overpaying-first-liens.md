---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3697
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/28

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - bin2chen
  - 0xRajeev
  - hansfriese
  - \_\_141345\_\_
  - ak1
---

## Vulnerability Title

M-22: _payment() function transfers full paymentAmount, overpaying first liens

### Overview


This bug report is about the `_payment()` function in the LienToken.sol smart contract, which is part of the Sherlock Audit's 2022-10-astaria-judging project. The bug was identified by obront, 0xRajeev, hansfriese, rvierdiiev, ak1, \_\_141345\_\_, bin2chen, and tives. 

The bug is that when the `_payment()` function is called, it sends the full `paymentAmount` argument to the lien owner, which can result in overpaying lien owners if borrowers accidentally overpay, or sending the first lien owner all the funds for the entire loop if the borrower is intending to pay back multiple loans. 

The `_payment()` function is called with the first lien with `paymentAmount` set to the full amount sent to the function. This means that the first lien holder receives the full amount, which could greatly exceed the amount they are owed. 

The bug was found using manual review. The recommended fix is to modify the `_payment()` function so that if `lien.amount < paymentAmount`, `paymentAmount` is set to `lien.amount`. This will ensure that only the amount owed is transferred to the lien owner, and that this value is also returned from the function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/28 

## Found by 
obront, 0xRajeev, hansfriese, rvierdiiev, ak1, \_\_141345\_\_, bin2chen, tives

## Summary

The `_payment()` function sends the full `paymentAmount` argument to the lien owner, which both (a) overpays lien owners if borrowers accidentally overpay and (b) sends the first lien owner all the funds for the entire loop of a borrower is intending to pay back multiple loans.

## Vulnerability Detail

There are two `makePayment()` functions in LienToken.sol. One that allows the user to specific a `position` (which specific lien they want to pay back, and another that iterates through their liens, paying each back.

In both cases, the functions call out to `_payment()` with a `paymentAmount`, which is sent (in full) to the lien owner.

```solidity
TRANSFER_PROXY.tokenTransferFrom(WETH, payer, payee, paymentAmount);
```

This behavior can cause problems in both cases.

The first case is less severe: If the user is intending to pay off one lien, and they enter a `paymentAmount` greater than the amount owed, the function will send the full `paymentAmount` to the lien owner, rather than just sending the amount owed.

The second case is much more severe: If the user is intending to pay towards all their loans, the `_makePayment()` function loops through open liens and performs the following:

```solidity
uint256 paymentAmount = totalCapitalAvailable;
for (uint256 i = 0; i < openLiens.length; ++i) {
  uint256 capitalSpent = _payment(
    collateralId,
    uint8(i),
    paymentAmount,
    address(msg.sender)
  );
  paymentAmount -= capitalSpent;
}
```

The `_payment()` function is called with the first lien with `paymentAmount` set to the full amount sent to the function. The result is that this full amount is sent to the first lien holder, which could greatly exceed the amount they are owed. 

## Impact

A user who is intending to pay off all their loans will end up paying all the funds they offered, but only paying off their first lien, potentially losing a large amount of funds.

## Code Snippet

The `_payment()` function with the core error:

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L594-L649

The `_makePayment()` function that uses `_payment()` and would cause the most severe harm:

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L410-L424

## Tool used

Manual Review

## Recommendation

In `_payment()`, if `lien.amount < paymentAmount`, set `paymentAmount = lien.amount`. 

The result will be that, in this case, only `lien.amount` is transferred to the lien owner, and this value is also returned from the function to accurately represent the amount that was paid.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | bin2chen, 0xRajeev, hansfriese, \_\_141345\_\_, ak1, tives, rvierdiiev, obront |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/28
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

