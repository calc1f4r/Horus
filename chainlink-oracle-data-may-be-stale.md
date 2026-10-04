---
# Core Classification
protocol: StakeStone Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58995
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/stake-stone-vault/a57e66f0-5f24-4d9d-84f8-23cebac2e34a/index.html
source_link: https://certificate.quantstamp.com/full/stake-stone-vault/a57e66f0-5f24-4d9d-84f8-23cebac2e34a/index.html
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
  - Hamed Mohammadi
  - Ibrahim Abouzied
---

## Vulnerability Title

Chainlink Oracle Data May Be Stale

### Overview


The report states that there is a bug in the `ChainlinkOracle.sol` file, which can result in incorrect pricing data being used for transactions. This can lead to losses for users or the protocol. The bug occurs because the current implementation does not check if the price data is outdated. To fix this, the report recommends validating the output values from Chainlink oracles by checking for successful updates, validating the price value, and verifying price freshness. These recommendations can be found on the Chainlink website.

### Original Finding Content

**Update**
The client added additional data validation in `87b9c378fd2026f5ae36e8f250f18030b970f5a2` and `aef34121fc8c84a3cf029ad45d469c85407d77f8`.

**File(s) affected:**`ChainlinkOracle.sol`

**Description:** Chainlink oracles can return stale pricing data due to network delays or other issues. If stale data is used, transactions may execute with outdated prices, leading to incorrect LP valuations or withdrawals, potentially resulting in losses for users or the protocol. The current implementation does not check if the price data is stale.

**Recommendation:** Consider validating the output values from Chainlink oracles by following these recommendations:

1.   Check for successful updates: Ensure the price feed has been updated and is not stale by verifying that `roundId` is not 0. 
2.   Validate the price value: Confirm that the `answer` field returns a non-zero value. Additionally, you can ensure the price falls within a reasonable range for the asset. 
3.   Verify price freshness: Compare the `updatedAt` timestamp with the current `block.timestamp` to ensure the difference is within the defined heartbeat for the price feed. Heartbeat values can be found on the Chainlink website.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | StakeStone Vault |
| Report Date | N/A |
| Finders | Jennifer Wu, Hamed Mohammadi, Ibrahim Abouzied |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/stake-stone-vault/a57e66f0-5f24-4d9d-84f8-23cebac2e34a/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/stake-stone-vault/a57e66f0-5f24-4d9d-84f8-23cebac2e34a/index.html

### Keywords for Search

`vulnerability`

