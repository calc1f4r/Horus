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
solodit_id: 35222
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/65

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
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - minhquanym
---

## Vulnerability Title

[M-03] Function `addNewTranche()` should use `protocolFee` from `Loan` struct

### Overview


The bug report discusses an issue with the protocol fee value being inconsistent when adding a new tranche. This occurs because the function uses the current value of `protocolFee.fraction` instead of the value stored in the Loan struct. This could lead to problems with fee collection if the protocol fee value is updated by the admin but not reflected in the Loan struct. The recommended mitigation is to use `_loan.protocolFee` instead of `protocolFee.fraction` in the `addNewTranche()` function. This issue has been confirmed and mitigated by the team.

### Original Finding Content


The protocol fee value is recorded and stored in the Loan struct when a new loan is issued. However, when adding a new tranche, the function uses the current value of `protocolFee.fraction` instead of the value stored in the Loan struct. This could result in inconsistencies in fee collection, as the protocol fee value might be updated by the admin, while the value stored in the Loan struct remains unchanged.

```solidity
if (_renegotiationOffer.fee > 0) {
    /// @dev Cached
    ProtocolFee memory protocolFee = _protocolFee;
    ERC20(_loan.principalAddress).safeTransferFrom(
        _renegotiationOffer.lender,
        protocolFee.recipient,
        _renegotiationOffer.fee.mulDivUp(protocolFee.fraction, _PRECISION) // @audit Use protocolFee from Loan instead
    );
}
```

### Proof of Concept

The protocol fee value is stored in the Loan struct when a new loan is opened.

```solidity
function _processOffersFromExecutionData(
  ...
) ... {
  Loan memory loan = Loan(
      _borrower,
      _tokenId,
      _nftCollateralAddress,
      _principalAddress,
      totalAmount,
      block.timestamp,
      _duration,
      tranche,
      protocolFee.fraction
  );
}
```

### Recommended Mitigation Steps

Consider using `_loan.protocolFee` instead of `protocolFee.fraction` in the `addNewTranche()` function.

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/65#event-12543174602)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> `addNewTranche` uses `protocolFee` from struct.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/98), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/68) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/21).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gondi |
| Report Date | N/A |
| Finders | minhquanym |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/65
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

