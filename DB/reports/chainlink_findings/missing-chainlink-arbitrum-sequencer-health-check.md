---
# Core Classification
protocol: Exchange V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51092
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

MISSING CHAINLINK ARBITRUM SEQUENCER HEALTH CHECK

### Overview


The report is about a bug in a blockchain called Arbitrum. The bug involves a node called `sequencer` that is responsible for submitting user transactions to the blockchain. If the node fails, communication between the blockchain and the underlying system is impossible. The bug is located in a specific part of the code and has been given a BVSS score of 6.7. The team has accepted the risk of this issue.

### Original Finding Content

##### Description

Arbitrum is a L2 blockchain leveraging Optimistic Rollups to integrate with the underlying L1. A node called `sequencer` is tasked with submitting user transactions to the L1 and if it fails, communication between the two is impossible. The exchange does not verify if the sequencer is online, which may lead to unexpected behavior if submitting transactions to the Ethereum mainnet is blocked.

Code Location
-------------

[SubstanceUSD.sol#L92](https://github.com/ElijahYao/SubstanceExchangeV1/blob/d122e2c3332478f293d7759465f6739d295ca55e/contracts/core/SubstanceUSD.sol#L92)

#### SubstanceUSD.sol

```
    function getPrice(address token, bool min) public view returns (uint256 price) {
        address oracle = underlyingToken[token].oracle;
        if (oracle == address(0)) {
            revert SubstanceUSD__InvalidToken();
        }
        (, int256 oraclePrice, , , ) = AggregatorV3Interface(oracle).latestRoundData();
        if (oraclePrice <= 0) {
            revert SubstanceUSD__InvalidOraclePrice();
        }
        uint8 pDecimals = AggregatorV3Interface(oracle).decimals();
        price = (uint256(oraclePrice) * PRECISION) / (10**pDecimals);
        price = min ? Math.min(PRECISION, price) : Math.max(PRECISION, price);
    }

```

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:C/D:N/Y:N/R:N/S:U (6.7)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:C/D:N/Y:N/R:N/S:U)

##### Recommendation

**RISK ACCEPTED**: The \client team accepted the risk of this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Exchange V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/substance-exchange/exchange-v1-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

