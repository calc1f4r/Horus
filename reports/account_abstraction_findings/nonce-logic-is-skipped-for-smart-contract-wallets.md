---
# Core Classification
protocol: Fastlane Atlas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36784
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
finders_count: 3
finders:
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

Nonce logic is skipped for smart contract wallets

### Overview


This bug affects the AtlasVerification contract and can potentially cause high risk. If a user's address is a smart contract, the _verifyUser() function will call the user's validateUserOp() function. However, this call does not include nonce validation, which can lead to signatures being replayed and nonces being reused. This is because most smart contract validation functions do not manage nonces themselves and rely on the caller for this. To fix this issue, the control flow of _verifyUser() should be changed to include _handleNonces() even for smart contract wallets. This issue has been solved in PR 230 and has been verified by Spearbit. 

### Original Finding Content

## Severity: High Risk

## Context
`AtlasVerification.sol#L532-L575`

## Description
If the `userOp.from` address is a smart contract, the `_verifyUser()` function makes a call to the user's `validateUserOp()` function. This call is expected to return a success boolean value, which is instantly returned. Since this return happens before the code reaches `_handleNonces()`, there is no nonce validation for smart contract wallets. Most smart contract validation functions (e.g., `validateUserOp()` in the case of ERC4337 or `isValidSignature()` in the case of ERC1271) do not manage nonces themselves and rely on the caller for this. As a result, signatures can be replayed, and nonces can be reused when the user is a smart contract wallet.

Also see the issue titled **"Call to validateUserOp() won't work,"** which suggests replacing `validateUserOp()` with `isValidSignature()`.

## Recommendation
Change the `_verifyUser()` control flow so that `_handleNonces()` is called even in the case of smart contract wallets.

## Fastlane
Solved in PR 230.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Fastlane Atlas |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf

### Keywords for Search

`vulnerability`

