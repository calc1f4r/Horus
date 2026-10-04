---
# Core Classification
protocol: Solflare MetaMask Snaps - Solflare, Sui, Aptos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25906
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/08/solflare-metamask-snaps-solflare-sui-aptos/
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
  - Martin Ortner

---

## Vulnerability Title

Insufficient Input Validation deriveKeyPair()

### Overview


This bug report describes an issue with the API design in the `path` checking process for the `getPublicKey` function in the `solflare-snap/src/index.js` file. This function does not check for a valid key derivation path format which may lead to unexpected outcomes or unhandled exceptions. For example, the function allows non alpha-num `0-9+'`, `slip:x` prefixes, or empty elements. This bug affects all snaps under review.

The recommendation is that the API design should be re-designed with the RPC functions receiving and validating only the last part of the key part, enforcing the format to be valid for the use case.

### Original Finding Content

#### Description


`path` is checked for correct type: `string`


**../solflare-snap/src/index.js:L23-L30**



```
case 'getPublicKey': {
 const { derivationPath, confirm = false } = request.params || {};

 assertInput(derivationPath);
 assertIsString(derivationPath);
 assertIsBoolean(confirm);

 const keyPair = await deriveKeyPair(derivationPath);

```
but is not checked for valid key derivation path format which may lead to unexpected outcomes or unhandled exceptions.


**../solflare-snap/src/privateKey.js:L20-L20**



```
const segments = path.split('/').slice(3).filter(Boolean);

```
For example, the function allows non alpha-num `0-9+'`, `slip:x` prefixes, or empty elements (`"m/44'/784'".split("/").slice(3).filter(Boolean) => []`).


Affects all snaps under review.


#### Recommendation


In general, the API design should be re-designed with the RPC functions receiving and validating only the last part of the key part, enforcing the format to be valid for the use case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Solflare MetaMask Snaps - Solflare, Sui, Aptos |
| Report Date | N/A |
| Finders | Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/08/solflare-metamask-snaps-solflare-sui-aptos/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

