---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29418
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/SSV%20Integration/README.md#1-inability-to-revoke-rights-given-in-setallowedselectorsforclient-and-setallowedselectorsforoperator
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
  - MixBytes
---

## Vulnerability Title

Inability to revoke rights given in `setAllowedSelectorsForClient` and `setAllowedSelectorsForOperator`

### Overview


This bug report concerns the P2pSsvProxyFactory contract, which grants access rights to the SsvNetwork functions for both the client and the operator. However, there is currently no mechanism to revoke those rights. This presents a security risk, as excessive permissions could be incorrectly assigned by the owner, and the SsvNetwork is an upgradeable proxy contract. This issue is classified as medium due to the risks associated with the irreversibility of incorrectly granted access.

To address this issue, it is recommended to introduce functions that enable the revocation of rights for both the client and the operator in invoking specific functions of the SsvNetwork through P2pSsvProxy. These functions should be restricted to the owner only, to ensure that the access rights can be revoked in the event of an interface change.

### Original Finding Content

##### Description
The issue is found in [`setAllowedSelectorsForClient`](https://github.com/p2p-org/p2p-ssv-proxy/blob/9dd4728002d9c275e29e8ba38bcf7d90efc7531b/src/p2pSsvProxyFactory/P2pSsvProxyFactory.sol#L285) and [`setAllowedSelectorsForOperator`](https://github.com/p2p-org/p2p-ssv-proxy/blob/9dd4728002d9c275e29e8ba38bcf7d90efc7531b/src/p2pSsvProxyFactory/P2pSsvProxyFactory.sol#L304) functions of `P2pSsvProxyFactory` contract.
These functions currently grant access rights for invoking `SsvNetwork` functions directly by `client` and `operator` through [`P2pSsvProxy.fallback`](https://github.com/p2p-org/p2p-ssv-proxy/blob/9dd4728002d9c275e29e8ba38bcf7d90efc7531b/src/p2pSsvProxy/P2pSsvProxy.sol#L154-L156) but do not provide a mechanism to revoke these rights. This shortfall presents a significant security risk, especially in scenarios where excessive permissions are incorrectly assigned by the `owner`. Additionally, the `ssvNetwork` is an upgradeable proxy contract, and the inability to revoke rights in the event of an interface change further increases the vulnerability. 
This issue is classified as `medium` due to the risks associated with the irreversibility of incorrectly granted access.

##### Recommendation
To mitigate this risk, it is recommended to introduce `onlyOwner` functions that enable the revocation of rights for both the `client` and `operator` in invoking specific functions of the `SsvNetwork` through `P2pSsvProxy`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/SSV%20Integration/README.md#1-inability-to-revoke-rights-given-in-setallowedselectorsforclient-and-setallowedselectorsforoperator
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

