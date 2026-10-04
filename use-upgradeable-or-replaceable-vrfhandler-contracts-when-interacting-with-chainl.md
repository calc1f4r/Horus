---
# Core Classification
protocol: Earnm Dropbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41173
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
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
  - Dacian
---

## Vulnerability Title

Use upgradeable or replaceable `VRFHandler` contracts when interacting with Chainlink VRF

### Overview

This bug report is about an issue with Chainlink's VRF 2.0 that could potentially cause problems for contracts that rely on it. The issue is that Chainlink plans to make changes to VRF 2.0 at the end of November 2024, which could cause it to stop working for existing subscriptions. This could have a significant impact on any immutable contracts that use VRF 2.0, and the same could happen in the future with VRF 2.5. To mitigate this, it is recommended to create a separate contract called `VRFHandler` that acts as a bridge between immutable contracts and Chainlink VRF. This contract should have certain features, such as being replaceable and allowing the contract owner to set the address of the immutable contract. The issue has been fixed in a recent commit by implementing a replaceable `VRFHandler` contract to act as a bridge between `DropBox` and Chainlink VRF. This fix has been verified by Cyfrin, the company that reported the bug.

### Original Finding Content

**Description:** Cyfrin has been made aware by our private audit clients that Chainlink intends on bricking VRF 2.0 at the end of November 2024 such that _"VRF 2.0 will stop working"_ even for existing subscriptions.

**Impact:** All immutable contracts dependent on VRF 2.0 will be bricked when Chainlink bricks VRF 2.0. The same will apply in the future to immutable contracts depending on VRF 2.5 when/if Chainlink does the same to it.

**Recommended Mitigation:** Immutable contracts should be insulated from directly interacting with Chainlink VRF. One way to achieve this is to create a separate `VRFHandler` contract that acts as a bridge between immutable contracts and Chainlink VRF; this contract should:
* be either a replaceable immutable contract using [VRFConsumerBaseV2Plus](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol) such that a new `VRFHandler` can be deployed, or an upgradeable contract using [VRFConsumerBaseV2Upgradeable](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Upgradeable.sol)
* allow the contract owner to set the address of the immutable contract (and vice versa in the immutable contract to set the address of the `VRF Handler`)
* provide an API to the immutable contract that will not need to change
* handle all the Chainlink VRF API calls and callbacks, passing randomness back to the immutable contract as required

**Mode:**
Fixed in commit [dc3412f](https://github.com/Earnft/dropbox-smart-contracts/commit/dc3412fda8bf988bac579d215c1b7f8f58b973a1) by implementing a replaceable immutable `VRFHandler` contract to act as a bridge between `DropBox` and Chainlink VRF.

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Earnm Dropbox |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

