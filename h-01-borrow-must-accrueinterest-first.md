---
# Core Classification
protocol: Union Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25592
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-union
source_link: https://code4rena.com/reports/2021-10-union
github_link: https://github.com/code-423n4/2021-10-union-findings/issues/66

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
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] `borrow` must `accrueInterest` first

### Overview


The bug reported in this report is that the `UToken.borrow` function first checks the borrowed balance and the old credit limit before accruing the actual interest on the market. This leads to borrowers being able to borrow more than the maximum amount and more than their credit limit as these checks are performed before updating accruing interest. 

The recommended mitigation step for this bug is to have the `require(accrueInterest(), "UToken: accrue interest failed");` call at the beginning of the function. This was confirmed by GeraldHost (Union Finance) and was commented on by GalloDaSballo (judge) who agreed with the finding and said that it fundamentally breaks the accounting of the protocol. 

In protocols that calculate interest, it is important to recalculate state after something has changed and to accrue all changes up to this point before proceeding with any other state-changing logic. This bug report highlights the importance of this step in order to ensure accurate accounting of the protocol.

### Original Finding Content

_Submitted by cmichel_

The `UToken.borrow` function first checks the borrowed balance and the old credit limit *before* accruing the actual interest on the market:

```solidity
// @audit this uses the old value
require(borrowBalanceView(msg.sender) + amount + fee <= maxBorrow, "UToken: amount large than borrow size max");

require(
    // @audit this calls uToken.calculateInterest(account) which returns old value
    uint256(_getCreditLimit(msg.sender)) >= amount + fee,
    "UToken: The loan amount plus fee is greater than credit limit"
);

// @audit accrual only happens here
require(accrueInterest(), "UToken: accrue interest failed");
```

Thus the borrowed balance of the user does not include the latest interest as it uses the old global `borrowIndex` but the new `borrowIndex` is only set in `accrueInterest`.

#### Impact
In low-activity markets, it could be that the `borrowIndex` accruals (`accrueInterest` calls) happen infrequently and a long time is between them.
A borrower could borrow tokens, and borrow more tokens later at a different time without first having their latest debt accrued.
This will lead to borrowers being able to borrow more than `maxBorrow` and **more than their credit limit** as these checks are performed before updating accruing interest.

#### Recommended Mitigation Steps
The `require(accrueInterest(), "UToken: accrue interest failed");` call should happen at the beginning of the function.

**[GeraldHost (Union Finance) confirmed](https://github.com/code-423n4/2021-10-union-findings/issues/66)**

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-10-union-findings/issues/66#issuecomment-965931329):**
 > Agree with the finding, this fundamentally breaks the accounting of the protocol
>
> In protocols that calculate interest, and that have to recalculate state after something changed, it is vital that you accrue all changes up to this point before proceeding with any other state-changing logic




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Union Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-union
- **GitHub**: https://github.com/code-423n4/2021-10-union-findings/issues/66
- **Contest**: https://code4rena.com/reports/2021-10-union

### Keywords for Search

`vulnerability`

