---
# Core Classification
protocol: ENS
chain: everychain
category: logic
vulnerability_type: ownership

# Attack Vector Details
attack_type: ownership
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5545
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-ens-contest
source_link: https://code4rena.com/reports/2022-07-ens
github_link: https://github.com/code-423n4/2022-07-ens-findings/issues/51

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - ownership
  - validation

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-01] `wrapETH2LD` permissioning is over-extended

### Overview


This bug report is about a vulnerability in the code of a wrapper contract, which allows undesired use of ENS (Ethereum Name Service) wrapper. The vulnerability lies in the permissioning for wrapETH2LD which allows msg.senders who are not owners to call it if they are approved for either all on the ERC721 registrar or approved on the wrapper. This means that any user who has been given approval on the wrapper contract can take control of any unwrapped domain by wrapping it. To mitigate this vulnerability, it is recommended to remove line 221 from the code.

### Original Finding Content


Undesired use of ENS wrapper.

### Proof of Concept

[NameWrapper.sol#L219-L223](https://github.com/code-423n4/2022-07-ens/blob/ff6e59b9415d0ead7daf31c2ed06e86d9061ae22/contracts/wrapper/NameWrapper.sol#L219-L223)<br>

Current permissioning for wrapETH2LD allows msg.senders who are not owner to call it if they are EITHER approved for all on the ERC721 registrar or approved on the wrapper. Allowing users who are approved for the ERC721 registrar makes sense. By giving them approval, you are giving them approval to do what they wish with the token. Any other restrictions are moot regardless because they could use approval to transfer themselves the token anyways and bypass them as the new owner. The issue is allowing users who are approved for the wrapper contract to wrap the underlying domain. By giving approval to the contract the user should only be giving approval for the wrapped domains. As it is currently setup, once a user has given approval on the wrapper contract they have essentially given approval for every domain, wrapped or unwrapped, because any unwrapped domain can be wrapped and taken control of. This is an over-extension of approval which should be limited to the tokens managed by the wrapper contract and not extend to unwrapped domains

### Recommended Mitigation Steps

Remove L221.

**[Arachnid (ENS) disagreed with severity and commented](https://github.com/code-423n4/2022-07-ens-findings/issues/51#issuecomment-1196225256):**
 > This was by design, but the warden raises a good point about the implications of this permission model. Recommend downgrading to QA.

**[LSDan (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-07-ens-findings/issues/51#issuecomment-1203751996):**
 > I'm going to downgrade this to medium. There are not assets at direct risk, but with external factors the assets could be at risk due to the user being unaware that in approving wrapped domains, they are also approving unwrapped domains.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | ENS |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-ens
- **GitHub**: https://github.com/code-423n4/2022-07-ens-findings/issues/51
- **Contest**: https://code4rena.com/contests/2022-07-ens-contest

### Keywords for Search

`Ownership, Validation`

