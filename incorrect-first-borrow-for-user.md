---
# Core Classification
protocol: C.R.E.A.M. Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28463
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/C.R.E.A.M.%20Finance/Compound%20Protocol/README.md#1-incorrect-first-borrow-for-user
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Incorrect first borrow for user

### Overview


This bug report pertains to a smart contract which is used to manage the borrowing of funds. Currently, if a user is not registered but has a balance of CToken greater than 0, then the borrowing will always fail until the user registers his collateral. The report recommends invoking the registerCollateral function after the comptroller adds the user to the market. This would ensure that the user is registered before the borrowing process begins, and thus the borrowing would not fail.

### Original Finding Content

##### Description
In current version of smart contract if user wasn't registered before, but has balance of `CToken > 0`, then borrowing will always fail, until user is registered his collateral.
https://github.com/CreamFi/compound-protocol/blob/23a4ae93adc70334553f5a83429a4e967c1eefaa/contracts/Comptroller.sol#L366

##### Recommendation
We recommend to invoke `registerCollateral` function after comptroller added user to market:
``` solidity=
Error err = addToMarketInternal(CToken(msg.sender), borrower);
if (err != Error.NO_ERROR) {
    return uint(err);
}
CCollateralCapErc20Interface(msg.sender).registerCollateral(borrower);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | C.R.E.A.M. Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/C.R.E.A.M.%20Finance/Compound%20Protocol/README.md#1-incorrect-first-borrow-for-user
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

