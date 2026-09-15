---
# Core Classification
protocol: Size
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38046
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-06-size
source_link: https://code4rena.com/reports/2024-06-size
github_link: https://github.com/code-423n4/2024-06-size-findings/issues/179

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
finders_count: 6
finders:
  - 0xStalin
  - bin2chen
  - almurhasan
  - 0xAlix2
  - hyh
---

## Vulnerability Title

[M-07] Credit can be sold forcibly as `forSale` setting can be ignored via Compensate

### Overview


The report discusses a bug where a credit position can be forcibly sold by its borrower, resulting in potential financial loss for the lender. This can happen when the lender's curve is above the market and the borrower overrides the `forSale` flag. The impact of this forced sale can be significant and there are no additional prerequisites for it to occur. The report includes a proof of concept and recommends a mitigation step of passing a flag to prevent the `forSale` flag from being changed. The bug has been fixed by the developers and the severity has been decreased to Medium.

### Original Finding Content


Any credit position can be forcibly sold with the help of its borrower. This will be executed only when have expected profit; for example, when lender's curve is not null and is above the market it is profitable to buy credit from them (lend to them at above market rates), but they might block it with the lack of free collateral and the `forSale = false` flag, which can be overridden by the corresponding borrower of this credit position. The impact of this forced sale is proportional to interest rate volatility and can be substantial. There are no additional prerequisites for the setup.

### Proof of Concept

`createDebtAndCreditPositions` creates credit positions with `forSale == true`:

[AccountingLibrary.sol#L62-L82](https://github.com/code-423n4/2024-06-size/blob/8850e25fb088898e9cf86f9be1c401ad155bea86/src/libraries/AccountingLibrary.sol#L62-L82)

```solidity
    function createDebtAndCreditPositions(
        ...
    ) external returns (CreditPosition memory creditPosition) {
        DebtPosition memory debtPosition =
            DebtPosition({borrower: borrower, futureValue: futureValue, dueDate: dueDate, liquidityIndexAtRepayment: 0});

        uint256 debtPositionId = state.data.nextDebtPositionId++;
        state.data.debtPositions[debtPositionId] = debtPosition;

        emit Events.CreateDebtPosition(debtPositionId, borrower, lender, futureValue, dueDate);

        creditPosition = CreditPosition({
            lender: lender,
            credit: debtPosition.futureValue,
            debtPositionId: debtPositionId,
>>          forSale: true
        });
```

This can be done on demand for any credit position by the borrower of the corresponding debt position, by running Compensate with `params.creditPositionToCompensateId == RESERVED_ID`, which will create new position with `forSale == true` and substitute the existing lender position with it:

[Compensate.sol#L118-L145](https://github.com/code-423n4/2024-06-size/blob/8850e25fb088898e9cf86f9be1c401ad155bea86/src/libraries/actions/Compensate.sol#L118-L145)

```solidity
        CreditPosition memory creditPositionToCompensate;
        if (params.creditPositionToCompensateId == RESERVED_ID) {
>>          creditPositionToCompensate = state.createDebtAndCreditPositions({  // @audit create new credit with `forSale == true`
                lender: msg.sender,
                borrower: msg.sender,
                futureValue: amountToCompensate,
                dueDate: debtPositionToRepay.dueDate
            });
        } else {
            creditPositionToCompensate = state.getCreditPosition(params.creditPositionToCompensateId);
            amountToCompensate = Math.min(amountToCompensate, creditPositionToCompensate.credit);
        }

        // debt and credit reduction
        state.reduceDebtAndCredit(
            creditPositionWithDebtToRepay.debtPositionId, params.creditPositionWithDebtToRepayId, amountToCompensate
        );

        uint256 exiterCreditRemaining = creditPositionToCompensate.credit - amountToCompensate;

        // credit emission
>>      state.createCreditPosition({
            exitCreditPositionId: params.creditPositionToCompensateId == RESERVED_ID  // @audit give it to the lender instead of the existing position with `forSale == false`
                ? state.data.nextCreditPositionId - 1
                : params.creditPositionToCompensateId,
            lender: creditPositionWithDebtToRepay.lender,
            credit: amountToCompensate
        });
```

Then, it can be then bought with `BuyCreditMarket`:

[BuyCreditMarket.sol#L79-L8](https://github.com/code-423n4/2024-06-size/blob/8850e25fb088898e9cf86f9be1c401ad155bea86/src/libraries/actions/BuyCreditMarket.sol#L79-L83)

```solidity
            borrower = creditPosition.lender;
            tenor = debtPosition.dueDate - block.timestamp; // positive since the credit position is transferrable, so the loan must be ACTIVE
        }

        BorrowOffer memory borrowOffer = state.data.users[borrower].borrowOffer;
```

### Recommended Mitigation Steps

Consider passing the flag to `createDebtAndCreditPositions()` indicating `forSale` flag to be set, which be passed from the existing credit in [Compensate.sol#L139](https://github.com/code-423n4/2024-06-size/blob/main/src/libraries/actions/Compensate.sol#L139), so it won't be changed.

**[aviggiano (Size) confirmed and commented](https://github.com/code-423n4/2024-06-size-findings/issues/179#issuecomment-2217877133):**
 > Fixed in https://github.com/SizeCredit/size-solidity/pull/130.

**[hansfriese (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2024-06-size-findings/issues/179#issuecomment-2220706497):**
 > Valid finding.
> 
> Medium is more appropriate due to the below reasons.
> - Buying the lender's credit position doesn't mean any loss to him as it's sold with his borrow offer. (It's just an unintended behavior.)
> - The lender can prevent this by setting `allCreditPositionsForSaleDisabled = false`.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Size |
| Report Date | N/A |
| Finders | 0xStalin, bin2chen, almurhasan, 0xAlix2, hyh, BenRai |

### Source Links

- **Source**: https://code4rena.com/reports/2024-06-size
- **GitHub**: https://github.com/code-423n4/2024-06-size-findings/issues/179
- **Contest**: https://code4rena.com/reports/2024-06-size

### Keywords for Search

`vulnerability`

