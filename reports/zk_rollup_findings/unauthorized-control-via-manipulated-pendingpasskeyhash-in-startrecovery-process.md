---
# Core Classification
protocol: SSO Account OIDC Recovery Solidity Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56713
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/sso-account-oidc-recovery-solidity-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Unauthorized Control via Manipulated pendingPasskeyHash in startRecovery Process

### Overview


A bug was found in the `OidcRecoveryValidator` and `WebAuthValidator` contracts, which are used for account recovery on the zksync-sso-clave platform. When a user loses access to their account, they can initiate a recovery process using a zero-knowledge proof. However, there is a vulnerability where the person initiating the recovery can submit a malicious `pendingPasskeyHash` and take control of the account, even if they were not the intended recipient of the recovery request. The suggested solution is to add a public signal to the proof to bind the `pendingPasskeyHash` and only store it after the proof has been verified. This has been resolved in a recent update by the Matter Labs team.

### Original Finding Content

When both the `OidcRecoveryValidator` and `WebAuthValidator` contract are active for an account, and the account owner loses access, a recovery process can be initiated using a zero-knowledge (ZK) proof. This proof demonstrates ownership of the associated OIDC identity, as registered in the `OidcRecoveryValidator` contract. Once the proof and associated data are verified, any party can call the `startRecovery` function to begin account recovery.

Although most parameters in the [`startRecovery` function](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/ed21d09add8da99d9c82d0f7c30659625c6636e6/src/validators/OidcRecoveryValidator.sol#L201) are validated by both the ZK circuit and the contract, there is no verification of the `data.pendingPasskeyHash` before [it is written to the account’s storage](https://github.com/matter-labs/zksync-sso-clave-contracts/blob/ed21d09add8da99d9c82d0f7c30659625c6636e6/src/validators/OidcRecoveryValidator.sol#L239C58-L239C76). This enables a scenario where the party initiating recovery (who has access to the valid ZK proof) could submit a malicious `pendingPasskeyHash` (one for which they possess the corresponding private key). As a result, they can complete the recovery through the `WebAuthValidator` contract, effectively taking control of the account, even if they were not the intended recipient of the recovery request.

Consider adding a public signal to the ZK proof to bind the `pendingPasskeyHash` parameter to the proof itself, and store this hash only after the proof has been verified.

***Update:** Resolved in [pull request #431](https://github.com/matter-labs/zksync-sso-clave-contracts/pull/431) at commit [ba4967a](https://github.com/matter-labs/zksync-sso-clave-contracts/pull/431/commits/ba4967ac13586e6b859393a135ee0fb5b7372b28). The Matter Labs team stated:*

> *In order to address this issue we included the `pendingPasskeyHash` inside the content of the JWT nonce. The nonce content was previously calculated as:*

```
 keccak256(abi.encode(msg.sender, oidcData.recoverNonce, data.timeLimit));

```

> *Now it’s calculated as:* `solidity
> keccak256(abi.encode(msg.sender, targetAccount, data.pendingPasskeyHash, oidcData.recoverNonce, data.timeLimit));` *This ensures that the user actually wanted to use the given passkey, and also makes the pendingKeyHash part of the data being checked by the circuit.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | SSO Account OIDC Recovery Solidity Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/sso-account-oidc-recovery-solidity-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

