---
# Core Classification
protocol: Gondi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35205
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/64

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
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - zhaojie
  - minhquanym
---

## Vulnerability Title

[H-03] Function `distribute()` lacks access control allowing anyone to spam and disrupt the pool's accounting

### Overview


The `LiquidationDistributor` contract is responsible for distributing funds to lenders after a liquidation auction. However, there is a bug that allows an attacker to manipulate the accounting process and receive incorrect funds. This is due to a lack of access control in the `distribute()` function. The recommended mitigation is to only allow loan contracts to call this function. The issue has been confirmed and mitigated by the team.

### Original Finding Content


The `LiquidationDistributor` contract manages the distribution of funds after a liquidation auction is settled. It distributes the received funds to the lenders of the loan. If the lender has implemented the `LoanManager` interface, it will also call `loanLiquidation()` on the lender's address. The Pool, when `loanLiquidation()` is called, will conduct an accounting process to ensure that the received funds are fairly distributed to the depositors.

```solidity
function loanLiquidation(
    uint256 _loanId,
    uint256 _principalAmount,
    uint256 _apr,
    uint256,
    uint256 _protocolFee,
    uint256 _received,
    uint256 _startTime
) external override onlyAcceptedCallers {
    uint256 netApr = _netApr(_apr, _protocolFee);
    uint256 interestEarned = _principalAmount.getInterest(netApr, block.timestamp - _startTime);
    uint256 fees = IFeeManager(getFeeManager).processFees(_received, 0);
    getCollectedFees += fees;
    // @audit Accounting logic
    _loanTermination(msg.sender, _loanId, _principalAmount, netApr, interestEarned, _received - fees);
}
```

However, the `distribute()` function lacks access control. Consequently, an attacker could directly call it with malicious data, leading to incorrect accounting in the Pool.

### Proof of Concept

Observe how the `loanLiquidation()` function is called:

```solidity
function _handleLoanManagerCall(IMultiSourceLoan.Tranche calldata _tranche, uint256 _sent) private {
    if (getLoanManagerRegistry.isLoanManager(_tranche.lender)) {
        LoanManager(_tranche.lender).loanLiquidation(
            _tranche.loanId,
            _tranche.principalAmount,
            _tranche.aprBps,
            _tranche.accruedInterest,
            0,
            _sent,
            _tranche.startTime
        );
    }
}
```

As shown above, the `principalAddress` is not passed in, meaning it will not be validated by the Pool. Therefore, an attacker can simply call the `distribute()` function with `loan.principalAddress` set to a random ERC20 token. This token will still be transferred to the Pool. However, the Pool will mistake this token as its asset token (USDC/WETH) and perform the accounting accordingly.

### Recommended Mitigation Steps

Only allow Loan contracts to call the `distribute()` function.

### Assessed type

Access Control

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/64#event-12543191121)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Added caller check to avoid anyone calling `distribute`.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/43), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/52) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/4).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gondi |
| Report Date | N/A |
| Finders | zhaojie, minhquanym |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/64
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

