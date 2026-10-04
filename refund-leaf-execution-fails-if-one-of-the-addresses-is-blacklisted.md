---
# Core Classification
protocol: Across V3 Incremental Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32548
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-v3-incremental-audit
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

Refund Leaf Execution Fails if One of the Addresses Is Blacklisted

### Overview


The report discusses a bug in the USDC token where transfers to and from a blacklisted address cause the entire transaction to fail. This is due to the way tokens are pushed to recipients during a refund process. The team suggests adding a fallback option to handle problematic addresses separately in the off-chain process. The Risk Labs team has acknowledged the issue and plans to address it in an upcoming update.

### Original Finding Content

If an address is blacklisted in the USDC token then both to and from transfers revert for this address. During refund leaf execution, tokens are [pushed to the recipients](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/SpokePool.sol#L1441-L1445). If one of the recipients is a blacklisted address, the whole execution fails and the blacklisted address as well as other addresses included in the leaf are not refunded. While such issues are inherent to the push pattern as opposed to the pull pattern, in this case, these issues and those similar to them can be remedied off-chain.


Consider adding a fallback option to the off-chain process that can separate problematic addresses to their own refund leaf so that they do not affect legitimate addresses.


***Update:** Acknowledged, will resolve. The Risk Labs team stated:*



> *We will address this in the upcoming UMIP changes for Across V3. Relayer refund leaves that refund any user on the `l2Token`'s blacklist should not be created.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across V3 Incremental Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-v3-incremental-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

