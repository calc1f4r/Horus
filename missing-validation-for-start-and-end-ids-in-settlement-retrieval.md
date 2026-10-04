---
# Core Classification
protocol: Name Service (BNS) Contracts v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52521
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
source_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
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
  - Halborn
---

## Vulnerability Title

Missing validation for start and end IDs in settlement retrieval

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `getSettlements(uint256, uint256)` function in the **BeraAuctionHouse** contract does not validate whether the `startId` is less than or equal to the `endId`. If an invalid range (e.g., `startId > endId`) is provided, the function will still execute and iterate unnecessarily, resulting in wasted gas and potential unintended behavior. This could also create confusion for users expecting a logical result when querying settlements.

  

Code Location
-------------

The `getSettlements` function does not validate whether the `startId` is less than or equal to the `endId`

```
    function getSettlements(uint256 startId, uint256 endId) external view returns (Settlement[] memory settlements) {
        settlements = new Settlement[](endId - startId);
        uint256 actualCount = 0;

        SettlementState memory settlementState;
        for (uint256 id = startId; id < endId; ++id) {
            settlementState = settlementHistory[id];

            settlements[actualCount] = Settlement({
                blockTimestamp: settlementState.blockTimestamp,
                amount: uint64PriceToUint256(settlementState.amount),
                winner: settlementState.winner,
                tokenId: id
            });
            ++actualCount;
        }

        if (settlements.length > actualCount) {
            // this assembly trims the settlements array, getting rid of unused cells
            assembly {
                mstore(settlements, actualCount)
            }
        }
    }
```

##### BVSS

[AO:A/AC:L/AX:H/R:N/S:U/C:N/A:N/I:N/D:L/Y:N (0.8)](/bvss?q=AO:A/AC:L/AX:H/R:N/S:U/C:N/A:N/I:N/D:L/Y:N)

##### Recommendation

Add an explicit check to validate the input parameters at the start of the function. This ensures that the function operates on a valid range, optimizing gas usage and preventing logical errors.

##### Remediation

**SOLVED:** The **Beranames team** solved the issue in the specified commit id.

##### Remediation Hash

<https://github.com/Beranames/beranames-contracts-v2/pull/104/commits/54c72638bc45d5c2190f108dd79c7f8c1547da37>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Name Service (BNS) Contracts v2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2

### Keywords for Search

`vulnerability`

