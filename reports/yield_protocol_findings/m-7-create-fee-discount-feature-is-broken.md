---
# Core Classification
protocol: Bond Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5675
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/20
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-bond-judging/issues/16

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
  - liquid_staking
  - services
  - cross_chain
  - synthetics
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 8olidity
  - xiaoming90
---

## Vulnerability Title

M-7: Create Fee Discount Feature Is Broken

### Overview


Issue M-7 is a bug found in the Bond Protocol's create fee discount feature. The issue was identified by 8olidity and xiaoming90, and it was found that the `createFeeDiscount` state variable is not initialized, meaning that users of the `BondFixedExpiryTeller.create` and `BondFixedTermTeller.create` functions will not receive any discount from the protocol. The code snippets from the BondFixedExpiryTeller.sol and BondFixedTermTeller.sol files were provided to illustrate the issue. The issue was identified through manual review. The recommended solution was to implement a setter method for the `createFeeDiscount` state variable and the necessary verification checks. The issue was then fixed by Bond-Protocol in the commit 570eb0b74b2401c7b6d07a30f8dd452bf7f225f9.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-bond-judging/issues/16 

## Found by 
8olidity, xiaoming90

## Summary

 The create fee discount feature is found to be broken within the protocol. 

## Vulnerability Detail

The create fee discount feature relies on the `createFeeDiscount` state variable to determine the fee to be discounted from the protocol fee. However, it was observed that there is no way to initialize the `createFeeDiscount` state variable. As a result, the `createFeeDiscount` state variable will always be zero.

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/BondFixedExpiryTeller.sol#L118

```solidity
File: BondFixedExpiryTeller.sol
118:         // If fee is greater than the create discount, then calculate the fee and store it
119:         // Otherwise, fee is zero.
120:         if (protocolFee > createFeeDiscount) {
121:             // Calculate fee amount
122:             uint256 feeAmount = amount_.mulDiv(protocolFee - createFeeDiscount, FEE_DECIMALS);
123:             rewards[_protocol][underlying_] += feeAmount;
124: 
125:             // Mint new bond tokens
126:             bondToken.mint(msg.sender, amount_ - feeAmount);
127: 
128:             return (bondToken, amount_ - feeAmount);
129:         } else {
130:             // Mint new bond tokens
131:             bondToken.mint(msg.sender, amount_);
132: 
133:             return (bondToken, amount_);
134:         }
```

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/BondFixedTermTeller.sol#L118

```solidity
File: BondFixedTermTeller.sol
118:         // If fee is greater than the create discount, then calculate the fee and store it
119:         // Otherwise, fee is zero.
120:         if (protocolFee > createFeeDiscount) {
121:             // Calculate fee amount
122:             uint256 feeAmount = amount_.mulDiv(protocolFee - createFeeDiscount, FEE_DECIMALS);
123:             rewards[_protocol][underlying_] += feeAmount;
124: 
125:             // Mint new bond tokens
126:             _mintToken(msg.sender, tokenId, amount_ - feeAmount);
127: 
128:             return (tokenId, amount_ - feeAmount);
129:         } else {
130:             // Mint new bond tokens
131:             _mintToken(msg.sender, tokenId, amount_);
132: 
133:             return (tokenId, amount_);
134:         }
```

## Impact

 The create fee discount feature is broken within the protocol. There is no way for the protocol team to configure a discount for the users of the `BondFixedExpiryTeller.create` and `BondFixedTermTeller.create` functions. As such, the users will not obtain any discount from the protocol when using the create function.

## Code Snippet

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/BondFixedExpiryTeller.sol#L118

https://github.com/sherlock-audit/2022-11-bond/blob/main/src/BondFixedTermTeller.sol#L118

## Tool used

Manual Review

## Recommendation

Implement a setter method for the `createFeeDiscount` state variable and the necessary verification checks.

```solidity
function setCreateFeeDiscount(uint48 createFeeDiscount_) external requiresAuth {
    if (createFeeDiscount_ > protocolFee)  revert Teller_InvalidParams();
    if (createFeeDiscount_ > 5e3) revert Teller_InvalidParams();
    createFeeDiscount = createFeeDiscount_;
}
```

## Discussion

**Evert0x**

Message from sponsor

----

Agree. We implemented a `setCreateFeeDiscount` function on the BondBaseTeller to allow updating the create fee discount.



**xiaoming9090**

Fixed in https://github.com/Bond-Protocol/bonds/commit/570eb0b74b2401c7b6d07a30f8dd452bf7f225f9

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Bond Protocol |
| Report Date | N/A |
| Finders | 8olidity, xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-bond-judging/issues/16
- **Contest**: https://app.sherlock.xyz/audits/contests/20

### Keywords for Search

`vulnerability`

