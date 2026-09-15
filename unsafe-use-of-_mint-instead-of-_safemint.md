---
# Core Classification
protocol: Newwit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20991
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-10-19-Newwit.md
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
  - AuditOne
---

## Vulnerability Title

Unsafe use of `_mint` instead of  `_safeMint`

### Overview


Bug report summary: The bug report is about the usage of the `_safeMint`function in the OpenZeppelin library. This function guarantees that the receiver ‘to’ address is either a smart contract that implements `IERC721Receiver.onERC721Received`or an EOA. The recommendation is to use `_safeMint`whenever possible instead of `_mint`. A link to the OpenZeppelin documentation is provided for more information.

### Original Finding Content

**Description:** 

The usage of `_safeMint`guarantees that the receiver `to`address is either a smart contract that implements `IERC721Receiver.onERC721Received`or an EOA. 

**Recommendations:** 

According to OpenZeppelin usage of `_mint`is discouraged,use `_safeMint`whenever possible.

See the docs: [https://docs.openzeppelin.com/contracts/4.x/api/token/erc721#ERC721-_safeMint-address -uint256-](https://docs.openzeppelin.com/contracts/4.x/api/token/erc721#ERC721-_safeMint-address-uint256-)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Newwit |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-10-19-Newwit.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

