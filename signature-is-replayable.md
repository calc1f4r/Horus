---
# Core Classification
protocol: Zimzam
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37216
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-11-ZimZam.md
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
  - Zokyo
---

## Vulnerability Title

Signature is replayable

### Overview


This bug report is about a vulnerability in the code of a contract called WalletAccount.sol. This vulnerability allows someone to reuse a signature to authorize a new action without the owner's consent. Although the function responsible for validating the signature is supposed to prevent this, it is not properly implemented in the WalletAccount.sol contract. The recommendation is to fix this by overriding the function in WalletAccount.sol to reject used nonces. However, the bug has been marked as resolved because the function is only callable by another contract that already has the proper mechanism in place to prevent replay attacks.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

WalletAccount.sol - Function `validateUserOp()` (i.e. in BaseAccount.sol) is susceptible to replay attacks. A rogue caller is able because of this vulnerability to reuse an already executed signature to authorize a new action without the consent of the signer to have that action repeated.
The implementation of `validateUserOp()` actually validates the nonce (i.e. line 46) which is supposed to mitigate that issue:
// BaseAccount.sol
```solidity
function validateUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 missingAccountFunds)
    external override virtual returns (uint256 validationData) {
44  _requireFromEntryPoint();
45  validationData = _validateSignature(userOp, userOpHash);
46  _validateNonce(userOp.nonce);
```
But WalletAccount.sol is supposed to implement `_validateNonce()` by overriding it since it is not implemented in BaseAccount.sol. Therefore the contract is exposed to replay attack because of the lack of validation of the nonce.
Recommendation - Override _validateNonce() in WalletAccount.sol by rejecting used nonces. 
**Fix**: Issue becomes irrelevant because the function is only callable by EntryPoint contract (out of audit scope). It is worth noting that the EntryPoint includes the required mechanism in NonceManager contract shown as follow:
```solidity
   function _validateAndUpdateNonce(address sender, uint256 nonce) internal returns (bool) {

        uint192 key = uint192(nonce >> 64);
        uint64 seq = uint64(nonce);
        return nonceSequenceNumber[sender][key]++ == seq;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zimzam |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-11-ZimZam.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

