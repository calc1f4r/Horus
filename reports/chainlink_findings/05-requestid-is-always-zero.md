---
# Core Classification
protocol: Art Gobblers
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25406
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-artgobblers
source_link: https://code4rena.com/reports/2022-09-artgobblers
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[05]  `requestId` is always zero

### Overview

See description below for full details.

### Original Finding Content

Chainlink suggests to have a unique `requestId` for every separate randomness request. By always using the same value, it's not possible to tell whether Chainlink returned data for a valid request, or if there was some Chainlink bug that triggered a callback for a request that was never made

*There is 1 instance of this issue:*
```solidity
File: /src/utils/rand/ChainlinkV1RandProvider.sol

62       function requestRandomBytes() external returns (bytes32 requestId) {
63           // The caller must be the ArtGobblers contract, revert otherwise.
64           if (msg.sender != address(artGobblers)) revert NotGobblers();
65   
66:          emit RandomBytesRequested(requestId);

```
https://github.com/code-423n4/2022-09-artgobblers/blob/d2087c5a8a6a4f1b9784520e7fe75afa3a9cbdbe/src/utils/rand/ChainlinkV1RandProvider.sol#L62-L66



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Art Gobblers |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-artgobblers
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-09-artgobblers

### Keywords for Search

`vulnerability`

