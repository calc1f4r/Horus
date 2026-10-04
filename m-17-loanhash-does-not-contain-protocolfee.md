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
solodit_id: 35236
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/15

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
finders_count: 3
finders:
  - minhquanym
  - bin2chen
  - oakcobalt
---

## Vulnerability Title

[M-17] `loan.hash()` does not contain `protocolFee`

### Overview


The bug report discusses a problem with the current IMultiSourceLoan.loop.hash() function. Specifically, it does not include the protocolFee, which can lead to an arbitrary protocolFee being specified in various methods. This can result in escaping fees or causing an accounting error in the LoanManager. The recommended mitigation is to add the protocolFee field in the hash function. The severity of the bug has been decreased to Medium, and the status is confirmed as mitigated. 

### Original Finding Content


The current `IMultiSourceLoan.loop.hash()` does not contain `protocolFee`:

```solidity
    function emitLoan(LoanExecutionData calldata _loanExecutionData)
        external
        nonReentrant
        returns (uint256, Loan memory)
    {
...
@>      _loans[loanId] = loan.hash();
        emit LoanEmitted(loanId, offerIds, loan, totalFee);

        return (loanId, loan);
    }

    function hash(IMultiSourceLoan.Loan memory _loan) internal pure returns (bytes32) {
        bytes memory trancheHashes;
        for (uint256 i; i < _loan.tranche.length;) {
            trancheHashes = abi.encodePacked(trancheHashes, _hashTranche(_loan.tranche[i]));
            unchecked {
                ++i;
            }
        }
        return keccak256(
            abi.encode(
                _MULTI_SOURCE_LOAN_HASH,
                _loan.borrower,
                _loan.nftCollateralTokenId,
                _loan.nftCollateralAddress,
                _loan.principalAddress,
                _loan.principalAmount,
                _loan.startTime,
                _loan.duration,
@>              //@audit miss protocolFee
                keccak256(trancheHashes)
            )
        );
    }

   struct Loan {
        address borrower;
        uint256 nftCollateralTokenId;
        address nftCollateralAddress;
        address principalAddress;
        uint256 principalAmount;
        uint256 startTime;
        uint256 duration;
        Tranche[] tranche;
@>      uint256 protocolFee;
    }
```

Then, you can specify `protocolFee` arbitrarily in many methods, but the `_baseLoanChecks()` security check doesn't `revert`.

```solidity
    function _baseLoanChecks(uint256 _loanId, Loan memory _loan) private view {
@>      if (_loan.hash() != _loans[_loanId]) {
            revert InvalidLoanError(_loanId);
        }
        if (_loan.startTime + _loan.duration < block.timestamp) {
            revert LoanExpiredError();
        }
    }
```

Example: `repayLoan(loadn.protocolFee=0)` to escape `fees` and cause a `LoanManager` accounting error. `refinancePartial()/refinanceFull()` can also specify the wrong `fees` to skip the fees.

### Impact

The loan hash does not contain a `protocolFee`, leading to an arbitrary `protocolFee` that can be specified to escape `fees` or cause an accounting error.

### Recommended Mitigation

```diff
    function hash(IMultiSourceLoan.Loan memory _loan) internal pure returns (bytes32) {
        bytes memory trancheHashes;
        for (uint256 i; i < _loan.tranche.length;) {
            trancheHashes = abi.encodePacked(trancheHashes, _hashTranche(_loan.tranche[i]));
            unchecked {
                ++i;
            }
        }
        return keccak256(
            abi.encode(
                _MULTI_SOURCE_LOAN_HASH,
                _loan.borrower,
                _loan.nftCollateralTokenId,
                _loan.nftCollateralAddress,
                _loan.principalAddress,
                _loan.principalAmount,
                _loan.startTime,
                _loan.duration, 
                keccak256(trancheHashes),
+               _loan.protocolFee
            )
        );
    }
```

### Assessed type

Context

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/15#event-12543524712)**

**[0xA5DF (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2024-04-gondi-findings/issues/15#issuecomment-2068016928):**
 > Avoiding fees is just a Medium. For the accounting error, I'll need more proof that this can lead to something significant to mark this as High.

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Added field in hash.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/112), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/82) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/35).

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
| Finders | minhquanym, bin2chen, oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/15
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

