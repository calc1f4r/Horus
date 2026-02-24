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
solodit_id: 36810
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
finders_count: 3
finders:
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

Call to validateUserOp() won't work

### Overview


This bug report discusses a problem with a function called _verifyUser() in the AtlasVerification.sol file. This function uses another function called validateUserOp() from the ERC4337 standard to validate smart contract wallets. However, there are several issues that prevent this from working properly. These include differences in the layout of UserOperation in different versions, limitations on calls from the EntryPoint, and the possibility of false positives from random smart contracts. The report recommends using a different function called ERC1271.isValidSignature() and mentions a potential solution called OZ SignatureChecker. The bug has been solved by a pull request and verified by Spearbit. 

### Original Finding Content

## Medium Risk Report

**Severity:** Medium Risk  
**Context:** AtlasVerification.sol#L532-L575  

**Description:**  
The function `_verifyUser()` uses the ERC4337 function `validateUserOp()` to validate smart contract wallets. There are several reasons why this won't work:

- `entryPoint v0.6` has a different layout for `UserOperation`.
- `entryPoint v0.7` has yet another layout for `UserOperation`.
- Smart wallets usually allow only calls from the `EntryPoint` to `validateUserOp`, as seen in `BaseAccount.sol`.
- Any random smart contract that has a fallback function that returns `0` on unknown functions would satisfy this check.

**Note:** Other ERC-4337 wallets usually don't put a gas limit when calling `validateUserOp()`.

```solidity
function _verifyUser( /*...*/ ) /*...*/ {
    if (userOp.from.code.length > 0) {
        // ...
        bool validSmartWallet =
        IAccount(userOp.from).validateUserOp{ gas: 30_000 }(userOp, _getProofHash(userOp), 0) == 0;
        return (isSimulation || validSmartWallet);
    }
    // ...
}
```

**Recommendation:**  
`ERC1271.isValidSignature()` seems a more logical solution. Also see OZ `SignatureChecker`. However, be aware of implementation issues of `ERC1271.isValidSignature()`.

**Fastlane:** Solved by PR 250.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

