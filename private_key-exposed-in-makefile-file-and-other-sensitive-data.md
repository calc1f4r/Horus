---
# Core Classification
protocol: D
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49406
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-02-24-cyfrin-d2-v2.1.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
---

## Vulnerability Title

`PRIVATE_KEY` exposed in `makefile` file and other sensitive data

### Overview


This bug report is about a project's Makefile that contains sensitive credentials, including a private key and multiple API keys. These credentials could potentially grant unauthorized access to funds and allow for the deployment of fake vaults. The report recommends immediate actions to remove the exposed credentials, transfer any assets from the compromised address, and regenerate all API keys. The issue has been fixed in the project's code and has been verified by a third-party. 

### Original Finding Content

**Description:** The project's Makefile contains hardcoded sensitive credentials including:

- A private key used for contract deployments
- Multiple RPC endpoint URLs with API keys
- Several Etherscan API keys for different networks

**Impact:** Although no customer funds were at risk and the deployer key had no admin rights on any of the deployed strategies, this exposure is critical because:

1. The private key grants complete control over the associated address, including:
    - Full access to any funds held by the wallet
    - Impersonate the protocol and deploy fake vaults
2. The RPC endpoints could be used to:
    - Execute unauthorized API calls
    - Potentially incur costs to the project
    - Exceed rate limits affecting production services

**Recommended Mitigation:** Immediate Actions Required:
- Remove all exposed credentials immediately
- Transfer any assets from the compromised address
- Revoke any contract permissions from the address
- Regenerate all API keys

Future mitigation use methods in this Updraft [lesson](https://updraft.d2sd2s.io/courses/foundry/foundry-simple-storage/never-use-a-env-file?lesson_format=video) to safely store private keys.

**D2:** Fixed in [`a4f3517`](https://github.com/d2sd2s/d2-contracts/commit/a4f3517d7c410278c1703b89aaad2315b5b86ba7) and [`228d0e17`](https://github.com/d2sd2s/d2-contracts/commit/228d0e17a1574d704380c3106a8d0caf6143ffd7)

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Cyfrin |
| Protocol | D |
| Report Date | N/A |
| Finders | Immeas |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-02-24-cyfrin-d2-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

