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
solodit_id: 61772
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
source_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 2

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

Stale Oracle Price Data Not Checked Before Token Operations May Drain Assets From Protocol

### Overview


The client has marked a bug as "Fixed" in the Redeemer and Minter contracts, which use Chainlink oracles to fetch price data for stablecoins. However, the contracts do not verify the freshness of the price data, which could be exploited by an attacker. The attacker could use stale price data to mint VUSD at a lower price and then redeem it for a different stablecoin at a higher price, draining assets from the protocol and making a profit. To prevent this, it is recommended to add a check for the staleness of price data from Chainlink oracles by comparing the current timestamp to the `updatedAt` timestamp and setting a maximum acceptable staleness threshold. This check should be implemented in both the Redeemer and Minter contracts.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `5f55a01c23fde5764bbef05ca11593c430df854c`.

**Further Update** Additional fixes applied in `b3dc7e4233ce5818d9f01bc73ba72ed047b04659` and `e9a6380cc1888e6ae96b44f11e838b4aa52fa8b8`.

**File(s) affected:**`Redeemer.sol, Minter.sol`

**Description:** The Redeemer and Minter contracts use Chainlink oracles to fetch price data for stablecoins to calculate redemption and minting amounts. However, these contracts only check if the price falls within a tolerance range but don not verify the freshness of the price data. In the `_calculateRedeemable()` function of the Redeemer contract and the `_calculateMintage()` function of the Minter contract, the code calls `latestRoundData()` but only uses the price value without checking the timestamp of when this price was last updated.

**Exploit Scenario:**

1.   The Chainlink oracle for a stablecoin stops updating for an extended period due to technical issues or other reasons.
2.   During this time, the actual market price of the stablecoin deviates significantly from its pegged value (e.g., during a depeg event).
3.   An attacker notices this situation and uses the stale price data to their advantage.
4.   The attacker can mint VUSD using the depegged stablecoin at its previous pegged price.
5.   The attacker then redeems this VUSD for a different, non-depegged stablecoin.
6.   This arbitrage opportunity allows the attacker to drain assets from the protocol and make significant profits.

**Recommendation:** Add staleness checks when getting price data from Chainlink oracles by:

Retrieve and check the `updatedAt` timestamp from the `latestRoundData()` function. Define a maximum acceptable staleness threshold based on the heartbeat (the update frequency) of the oracle. Require that the time difference between the current timestamp and `updatedAt` is less than this threshold. Implement this check in both the `_calculateRedeemable()` function in the Redeemer contract and the `_calculateMintage()` function in the Minter contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
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

