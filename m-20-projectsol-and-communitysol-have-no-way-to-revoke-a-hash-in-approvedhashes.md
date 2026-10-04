---
# Core Classification
protocol: Rigor Protocol
chain: everychain
category: access_control
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3124
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-rigor-protocol-contest
source_link: https://code4rena.com/reports/2022-08-rigor
github_link: https://github.com/code-423n4/2022-08-rigor-findings/issues/64

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - business_logic
  - access_control

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

[M-20] `Project.sol` and `Community.sol` have no way to revoke a hash in approvedHashes

### Overview


This bug report is about a vulnerability that prevents users from revoking a previously approved hash. This means that if the user reconsiders or notices something malicious about the hash after signing, they are not able to revoke it. This could lead to loss of funds or access. To mitigate this issue, the report recommends adding a function called revokeHash which will allow users to revoke the hash. The code for the function is provided in the report.

### Original Finding Content

_Submitted by 0x52_

[Community.sol#L501-L506](https://github.com/code-423n4/2022-08-rigor/blob/5ab7ea84a1516cb726421ef690af5bc41029f88f/contracts/Community.sol#L501-L506)<br>
[Project.sol#L108-L115](https://github.com/code-423n4/2022-08-rigor/blob/5ab7ea84a1516cb726421ef690af5bc41029f88f/contracts/Project.sol#L108-L115)<br>

User is unable to revoke previously approved hash.

### Proof of Concept

If user reconsiders or notices something malicious about the hash after signing, they should be able to revoke the hash. For example the user approves a hash only to find out later that the hash has been spoofed and they weren't approving what they thought they were. To protect themselves the user should be able to revoke approval, otherwise it may lead to loss of funds or access.

### Recommended Mitigation Steps

Add the following function:

    function revokeHash(bytes32 _hash) external virtual {
        approvedHashes[_msgSender()][_hash] = false;
    }

**[parv3213 (Rigor) disputed and commented](https://github.com/code-423n4/2022-08-rigor-findings/issues/64#issuecomment-1243284914):**
 > I do not find it essential to revoke a hash. As off-chain signatures can never be marked as invalid, adding this feature for on-chain signatures makes no sense. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Rigor Protocol |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-rigor
- **GitHub**: https://github.com/code-423n4/2022-08-rigor-findings/issues/64
- **Contest**: https://code4rena.com/contests/2022-08-rigor-protocol-contest

### Keywords for Search

`Business Logic, Access Control`

