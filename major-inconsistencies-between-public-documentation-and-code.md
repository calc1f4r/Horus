---
# Core Classification
protocol: Pheasant Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60323
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
source_link: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
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
finders_count: 5
finders:
  - Danny Aksenov
  - Faycal Lalidji
  - Ruben Koch
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Major Inconsistencies Between Public Documentation and Code

### Overview


The client has updated their documentation to include information about the current development status, potential risks, and their approach to mitigating those risks. However, the public documentation does not accurately reflect the code, and there are inconsistencies between the two. These include undocumented features, inaccuracies in user protection, and centralized liquidity. The client recommends clearly separating the current implementation from planned items in the roadmap in the documentation.

### Original Finding Content

**Update**
The client provided the following explanation:

> We have updated the documentation to address the current development status, potential risks, and our approach to mitigating those risks. Additionally, we have included a roadmap for future development, outlining the planned milestones and objectives.

**Description:** The public documentation greatly differs from the code. In general, the protocol is less decentralized and trustless and provides less user protection than what is stated in the documentation. We will elaborate on some of the inconsistencies in individual issues, for now an overview of collected inconsistencies:

*   Undocumented possibility of unslashable networks;
*   Relayer does not necessarily have to hold a bond while subject to slashing;
*   Inaccurate reimbursements of user funds in case of slashing;
*   There is no decentralized liquidity, as there is only a single relayer. Therefore, the liquidity is centralized in the `BondManager`;
*   Pheasant Fee is unimplemented;
*   Cheaper gas fees are not enforced on the protocol level, as the relayer can arbitrarily set them;
*   Undocumented pause mechanism;
*   Undocumented possibility of updating most of the global state variables associated to fees and slashing by the owner;

**Recommendation:** In the documentation, clearly separate the current implementation and planned items in the roadmap.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Pheasant Network |
| Report Date | N/A |
| Finders | Danny Aksenov, Faycal Lalidji, Ruben Koch, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/index.html

### Keywords for Search

`vulnerability`

