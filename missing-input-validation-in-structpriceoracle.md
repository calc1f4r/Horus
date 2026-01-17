---
# Core Classification
protocol: Struct Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44650
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct Finance.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Missing Input Validation in StructPriceOracle

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**

**Note**: Attacker = (Malicious governance)

**Overview**: 

The StructPriceOracle contract is used to fetch the latest price of the given assets using Chainlink's price feed. The contract allows the owner to set or replace sources for the assets. However, the contract does not have proper input validation in the _setAssetsSources function, which allows an attacker to add a malicious asset source and control the price returned by the getAssetPrice function.

**Vulnerability**: 

The vulnerability exists in the _setAssetsSources function, where the contract allows the owner to set or replace sources for the assets without proper input validation. An attacker can add a malicious asset source that returns an incorrect price. This can lead to incorrect valuation of the assets, which can cause severe financial loss to the users.

**Attack Scenario**: 

An attacker can create a malicious asset source that returns an incorrect price. The attacker can then call the _setAssetsSources function with the malicious asset source address and set it as the source for an asset. When the getAssetPrice function is called with the asset address, the malicious asset source will return the incorrect price, which can cause the valuation of the assets to be incorrect. This can lead to financial loss for the users.

**Impact**: 

The impact of this vulnerability can be severe, as a Malicious Owner can manipulate the price of an asset and cause financial loss to the users. This can also affect the valuation of the assets, which can cause further financial loss. The users can lose trust in the platform, and the reputation of the platform can be damaged.

**Recommendation**: 

To mitigate this vulnerability, the contract should have proper input validation in the _setAssetsSources function. The contract should validate that the address of the asset source is a valid Chainlink aggregator address. Additionally, the contract can also implement a whitelist for the asset sources, where the owner can only set the sources from the whitelist. This will prevent the owner from adding a malicious asset source.

**Comment**: The client'll be using a multisig for governance operations initially. So the scenario is very unlikely to happen as the signers will be some of the industry's trusted parties

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Struct Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

