---
# Core Classification
protocol: Berally Pass
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45971
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Berally-Pass-Security-Review.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-01] Users Can Steal Part of Protocol Fees Through Referrals to Their Own Addresses

### Overview


This report describes a bug in the code that allows users to steal part of the protocol fee by setting the `referral` address to an address they control. This affects the `buyPasses` and `sellPasses` functions in the Passes.sol file. The impact of this bug is that part of the protocol fees can be stolen. The proof of concept shows how the `referralFee` is calculated and how it can be manipulated by the user. The recommendation is to create an admin-controlled function to specify a referral address and the team has responded that the bug has been fixed.

### Original Finding Content

## Severity

High Risk

## Description

Users can steal part of the protocol fee by setting `referral` to addresses they control. `buyPasses` and `sellPasses` allows the caller to specify the `referral` address where the `referralFee` is paid to.

## Location of Affected Code

File: [Passes.sol](https://github.com/berally/smartcontract/blob/73ec1b6ee0b2d9d8fc645529cf3ce10d00792422/passes/contracts/Passes.sol)

```solidity
@>  function sellPasses(address manager, uint256 amount, uint256 minPrice, address referral) public payable {
      // code
      bool success4 = true;
      if(referralFee > 0) {
          (success4, ) = referral.call{value: referralFee}("");
      }

      require(success1 && success2 && success3 && success4, "Unable to send funds");
  }

...

@>  function buyPasses(address manager, uint256 amount, uint256 factor, address referral) public payable {
      // code
      bool success3 = true;
      if(referralFee > 0) {
          (success3, ) = referral.call{value: referralFee}("");
      }

      // code
  }
```

## Impact

Part of the protocol fees can be stolen.

## Proof of Concept

The `referralFee` is calculated as a portion of the protocol fee in both `buyPasses` and `sellPasses`.

```solidity
uint256 referralFee = 0;
if(referral != address(0)) {
    referralFee = price * referralFeePercent / 1 ether;
    protocolFee -= referralFee;
}
```

So by setting `referral` to a user-controlled address, the user can easily recover part of the `protocolFee`.

## Recommendation

Create an admin-controlled function to specify a referral address. The address can then distribute the fees to the required referrals.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Berally Pass |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Berally-Pass-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

