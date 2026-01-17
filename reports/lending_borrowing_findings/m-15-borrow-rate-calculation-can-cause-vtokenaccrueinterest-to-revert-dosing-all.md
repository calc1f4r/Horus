---
# Core Classification
protocol: Venus Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20784
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-venus
source_link: https://code4rena.com/reports/2023-05-venus
github_link: https://github.com/code-423n4/2023-05-venus-findings/issues/10

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
  - dacian
  - Co0nan
  - nadin
  - SaeedAlipoor01988
---

## Vulnerability Title

[M-15] Borrow rate calculation can cause VToken.accrueInterest() to revert, DoSing all major functionality

### Overview


A bug report has been filed for the VToken contract, which is part of the 2023-05-venus project. The bug is that the VToken contract hard-codes a maximum borrow rate, and `accrueInterest()` reverts if the dynamically calculated rate is greater than the hard-coded value. This causes a major DoS as most VToken functions call `accrueInterest()`.

The recommended mitigation steps are to change `accrueInterest()` to not revert in this case, but to set `borrowRateMantissa = borrowRateMaxMantissa` if the dynamically calculated value would be greater than the hard-coded max. This would allow execution to continue operating with the system-allowed maximum borrow rate, allowing all functions that depend upon `accrueInterest()` to continue as normal. It would also allow `borrowRateMantissa` to be naturally set to the dynamically calculated rate as soon as that rate becomes less than the hard-coded max.

The assessed type of the bug is DoS, and the severity has been disputed. One suggestion was to deploy a new implementation of the VToken contract, with a higher maximum, and fix the lock. This was confirmed via a duplicate issue, but it was also noted that upgrading a contract does not mitigate that there would be an impact to the protocol, so the severity was determined to be Medium.

### Original Finding Content


Borrow rates are calculated dynamically and `VToken.accrueInterest()` [reverts](https://github.com/code-423n4/2023-05-venus/blob/main/contracts/VToken.sol#L695-L696) if the calculated rate is greater than a hard-coded maximum. As `accrueInterest()` is called by most VToken functions, this state causes a major DoS.

### Proof of Concept

VToken [hard-codes](https://github.com/code-423n4/2023-05-venus/blob/main/contracts/VTokenInterfaces.sol#L53) the maximum borrow rate and `accrueInterest()` [reverts](https://github.com/code-423n4/2023-05-venus/blob/main/contracts/VToken.sol#L695-L696) if the dynamically calculated rate is greater than the hard-coded value.

The actual calculation is dynamic [[1](https://github.com/code-423n4/2023-05-venus/blob/main/contracts/BaseJumpRateModelV2.sol#L172-L190), [2](https://github.com/code-423n4/2023-05-venus/blob/main/contracts/WhitePaperInterestRateModel.sol#L50-L57)] and takes no notice of the hard-coded cap, so it is very possible that this state will manifest, causing a major DoS due to most VToken functions calling `accrueInterest()` and `accrueInterest()` reverting.

### Recommended Mitigation Steps

Change `VToken.accrueInterest()` to not revert in this case, but simply to set `borrowRateMantissa = borrowRateMaxMantissa` if the dynamically calculated value would be greater than the hard-coded max. This would:

1.  Allow execution to continue operating with the system-allowed maximum borrow rate, allowing all functionality that depends upon `accrueInterest()` to continue as normal.
2.  Allow `borrowRateMantissa` to be naturally set to the dynamically calculated rate as soon as that rate becomes less than the hard-coded max.

### Assessed type

DoS

**[chechu (Venus) disagreed with severity and commented](https://github.com/code-423n4/2023-05-venus-findings/issues/10#issuecomment-1560068055):**
 > We could deploy a new implementation of the VToken contract, with a higher maximum, and fix the lock. Via VIP, with the votes from the community.

 **[chechu (Venus) confirmed via duplicate issue #110](https://github.com/code-423n4/2023-05-venus-findings/issues/110#issuecomment-1560087513)**

**[0xean (judge) commented](https://github.com/code-423n4/2023-05-venus-findings/issues/10#issuecomment-1569312936):**
 > Upgrading a contract does not mitigate that there would be an impact to the protocol, so I think this does qualify as Medium. 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Venus Protocol |
| Report Date | N/A |
| Finders | dacian, Co0nan, nadin, SaeedAlipoor01988 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-venus
- **GitHub**: https://github.com/code-423n4/2023-05-venus-findings/issues/10
- **Contest**: https://code4rena.com/reports/2023-05-venus

### Keywords for Search

`vulnerability`

