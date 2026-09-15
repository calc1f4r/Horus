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
solodit_id: 25907
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

Dapp May Suppress User Confirmation on Request to Extract Pubkey; May Extract Any Net-Key

### Overview


A bug has been reported in the `request.params.confirm` parameter of requests to signTransaction and signAllTransactions. This parameter allows the dapp to control if the user is asked to extract certain (derived) information from the snap, which could potentially leak sensitive information. It is recommended that the snap should strictly enforce user confirmation on the first time the pubkey is requested from an origin, as a potentially untrusted dapp should never be able to silently dictate what security measures be enabled with a snap request. An example of the code affected can be seen in the `../solflare-snap/src/index.js:L23-L36` file.

### Original Finding Content

#### Description


With the `request.params.confirm` parameter in requests to signTransaction and signAllTransactions the dapp controls if the user is requested confirmation to return the public key. If the dapp sets `confirm=false` the user will not be informed that the dapp accessed their pubkey information (any account). Allowing the dapp to control if the user is asked to extract certain (derived) information from the snap is intransparent and may leak sensitive information. Especially in a setting where the snap is gatekeeping access to user specific information.


#### Examples


Affects all snaps under review.


**../solflare-snap/src/index.js:L23-L36**



```
case 'getPublicKey': {
 const { derivationPath, confirm = false } = request.params || {};

 assertInput(derivationPath);
 assertIsString(derivationPath);
 assertIsBoolean(confirm);

 const keyPair = await deriveKeyPair(derivationPath);
 const pubkey = bs58.encode(keyPair.publicKey);

 if (confirm) {
 const accepted = await renderGetPublicKey(dappHost, pubkey);
 assertConfirmation(accepted);
 }

```
#### Recommendation


The snap should strictly enforce user confirmation on the first time the pubkey is requested from an origin. A potentially untrusted dapp (even though origin restricted; a dapp might turn malicious and should therefore be treated as untrusted) should never be able to silently dictate what security measures be enabled with a snap request.

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

