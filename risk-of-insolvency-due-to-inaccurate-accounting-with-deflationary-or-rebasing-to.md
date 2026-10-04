---
# Core Classification
protocol: Zero Name Service (ZNS)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59369
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/zero-name-service-zns/4ec9b4dd-2c6b-4ce8-ad3f-c4f4246e0140/index.html
source_link: https://certificate.quantstamp.com/full/zero-name-service-zns/4ec9b4dd-2c6b-4ce8-ad3f-c4f4246e0140/index.html
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
  - Jennifer Wu
  - Mustafa Hasan
  - Hytham Farah
---

## Vulnerability Title

Risk of Insolvency Due to Inaccurate Accounting with Deflationary or Rebasing Tokens

### Overview


This bug report discusses an issue with the `ZNSTreasury.stakeForDomain()` function in the `ZNSTreasury.sol` file. The problem arises when deflationary or rebasing tokens are used for payment, as these tokens can lead to discrepancies between the recorded staked amount and the actual reserve. This can potentially cause insolvency issues during unstaking. To address this, the client plans to either limit the types of currencies accepted or adjust the protocol's accounting mechanisms. They also plan to update their user-facing documentation to warn users about the risks associated with using these types of tokens. 

### Original Finding Content

**Update**
The client acknowledged the issue and provided the following explanation:

> Outline possible problems in the docs. Answer: We consider this a special rare case when a parent domain owner uses rebasing or deflationary token as payment. In order for a subdomain candidate to pay in this token, he first has to purchase it, making him more knowledgeable of the token he is about to use. Also, this is tied to a specific community which operates on a specific token, so participants should be aware of the nature of the token. To solve this we would need to centralize the system more with a token whitelist, which, we believe, goes against our goals of leaning more towards decentralization. This would also add complexity to the system and take the freedom of building your community on your own rules away. We will add and expand the below paragraph in our user-facing docs.

The client plans to provide the following documentation to users:

> Docs: When purchasing a subdomain, be careful and review all the rules set by the parent domain owner, under which you purchase your domain. zNS system is allowing a freedom for a parent domain owner to choose whichever token they like to be used for payments. Please note, that in case of staking, the amount you paid is fixed and saved in the ZNSTreasury contract's state and if you decide to revoke your subdomain later, this is the exact amount you will get back in the same token you staked in. In case a parent domain owner used rebasing or deflationary token for stake payments, the amount you will withdraw upon revocation may not hold the same value it originally did based on the token's total supply at any given time. We recommend to thoroughly research the community you are entering with subdomain purchase and especially the token and the economy this community uses. zNS provides the way to freely set your own rules and tokens for any domain owner, but can not guarantee how these tokens and economies will work outside of zNS.

**File(s) affected:**`ZNSTreasury.sol`

**Description:** The `ZNSTreasury.stakeForDomain()` function accounts for staked amounts based on the tokens deposited. If deflationary tokens, which automatically subtract fees on transfer, or rebasing tokens, which can adjust balances algorithmically, are used, this can lead to discrepancies between the recorded `stakedForDomain.stakedAmount` and the actual reserve. Furthermore, since the protocol accepts any token, a malicious token could exacerbate this discrepancy. These inaccuracies can lead to insolvency issues during unstaking.

**Recommendation:** To address this risk, either limit the types of currencies accepted when registering a subdomain to exclude deflationary or rebasing tokens, or adjust the protocol's accounting mechanisms to properly handle deflationary or rebasing tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Zero Name Service (ZNS) |
| Report Date | N/A |
| Finders | Jennifer Wu, Mustafa Hasan, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/zero-name-service-zns/4ec9b4dd-2c6b-4ce8-ad3f-c4f4246e0140/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/zero-name-service-zns/4ec9b4dd-2c6b-4ce8-ad3f-c4f4246e0140/index.html

### Keywords for Search

`vulnerability`

