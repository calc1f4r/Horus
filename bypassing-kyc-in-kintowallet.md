---
# Core Classification
protocol: Kinto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30492
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Kinto/README.md#1-bypassing-kyc-in-kintowallet
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
  - MixBytes
---

## Vulnerability Title

Bypassing KYC in KintoWallet

### Overview


The bug report discusses an issue with the KintoWallet, which can have up to three owners and different signer policies. The problem is that the `_validateSignature()` and `resetSigners()` functions only check the first owner's KintoID, allowing someone to set up a KintoWallet without a KintoID. This can be exploited by a hacker who obtains a KintoID and wallet through fraudulent means, and then sets up a 2/3 signature scheme with the first owner being a legitimate account, while the other two owners are the hacker's accounts without KintoIDs. This means that the KintoWallet is no longer tied to the original account that created it, and the revocation of the original owner's KintoID does not affect it. The recommendation is to change the `_validateSignature()` function to check the KYC of each owner, rather than just the first one. 

### Original Finding Content

##### Description

* https://github.com/KintoXYZ/kinto-core/blob/f7dd98f66b9dfba1f73758703b808051196e740b/src/wallet/KintoWallet.sol#L204

A KintoWallet can have from one to three owners and have different signer policies. `_validateSignature()` and `resetSigners()` check KintoID only for the `owner[0]`, which allows setting up a KintoWallet in such a way that it can be used by a user without a KintoID.

To do this, a hacker first obtains a KintoID and KintoWallet. This is done either through a fake or stolen ID, or by stealing someone else's private key.

Next, the hacker sets a 2/3 signature scheme in the KintoWallet and sets `owner[0]` to a person who has passed KYC and is not connected to the hacker. For example, they set Vitalik Buterin's account as `owner[0]`. The `owner[1]` and `owner[2]` accounts are the hacker's regular EOAs (Externally Owned Accounts) without KintoID.

Now, the KintoWallet is in no way tied to the original account that created it, and the revocation or invalidation of the original owner's KintoID does not affect it.

The hacker can use the KintoWallet, as they own 2/3 of the signatures, and the `_validateSignature()` function checks the KYC of only the first owner, who, in our example, is Vitalik Buterin.

##### Recommendation

We recommend that in the `_validateSignature()` function, instead of checking the KYC of the first owner, each signature be simply counted valid only if its owner had a KintoID.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Kinto |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Kinto/README.md#1-bypassing-kyc-in-kintowallet
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

