---
# Core Classification
protocol: vusd-stablecoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61773
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
source_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
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
finders_count: 3
finders:
  - Paul Clemson
  - Leonardo Passos
  - Tim Sigl
---

## Vulnerability Title

Lack of Error Handling for Oracle Calls May Cause Temporary Service Disruption

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Will fix it in future release when we have fallback oracle ready.

**File(s) affected:**`Redeemer.sol, Minter.sol`

**Description:** The Redeemer and Minter contracts interact with Chainlink oracles to fetch price data for stablecoins, but they do not implement proper error handling mechanisms for these external calls. In the `_calculateRedeemable()`function of the Redeemer contract and the `_calculateMintage()` function of the Minter contract, the code directly calls `latestRoundData()` without any try-catch block or fallback mechanism. If Chainlink bans the contract address from accessing price feeds or if the oracle service experiences downtime, these functions will fail, leading to a temporary disruption of minting and redemption services.

**Exploit Scenario:**

1.   Chainlink decides to ban the contract address from accessing their price feeds due to policy changes or abuse detection.
2.   All redemption and minting functions in the protocol immediately stop working since they depend on oracle data.
3.   Users are temporarily unable to redeem their VUSD tokens until the governor intervenes.
4.   The governor must identify the issue, remove the problematic token from the whitelist, and then re-add it with a new oracle address.
5.   This process may take time, during which the protocol's core functionality is impaired, potentially causing user frustration and loss of confidence.

**Recommendation:** Consider taking one of the following actions to fix this issue:

1.   Implement a try-catch block around oracle calls to gracefully handle any failures.
2.   Create a fallback mechanism with alternative oracle providers that can be used temporarily in case of main oracle failure.
3.   Add monitoring systems to alert the team when oracle calls start failing so they can take proactive measures.
4.   Document the recovery process for oracle failures so the governor can quickly restore functionality by removing and re-adding the affected token with an updated oracle address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | vusd-stablecoin |
| Report Date | N/A |
| Finders | Paul Clemson, Leonardo Passos, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html

### Keywords for Search

`vulnerability`

