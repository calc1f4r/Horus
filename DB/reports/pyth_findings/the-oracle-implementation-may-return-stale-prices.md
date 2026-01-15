---
# Core Classification
protocol: EVM Bridge Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52639
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/pontis/evm-bridge-contracts
source_link: https://www.halborn.com/audits/pontis/evm-bridge-contracts
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

The oracle implementation may return stale prices

### Overview

See description below for full details.

### Original Finding Content

##### Description

Users who want to utilize the `bridgeOutRunes()` function in the `pontis-bridge-v1.sol` contract, have to pay fees in the native token. First the `fetchPrices()` function is called which returns the `runePrice` and `nativePrice`. Both of those prices are fetched from an oracle implementation:

```
    function fetchPrices(string calldata runeId) private view returns (uint256 nativePrice, uint256 runePrice) {
        nativePrice = priceOracle.getPrice(NATIVE_TOKEN_NAME);
        runePrice = priceOracle.getPrice(runeId);
        require(nativePrice > 0, "Invalid Native Price");
        require(runePrice > 0, "Invalid Rune Price");
        return (nativePrice, runePrice);
    }
```

  

The `getPrice()` function fetches the price from a specific contract implementation - `pontis-price-oracle.sol`, where the price is set via the `setPrices()` function. According to the dev team the price will be updated once a day, this is a problem if the price is too volatile. As this will result in users paying more fees than they should, or the protocol receiving less in fees, depending on how the price fluctuates.

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:N/D:N/Y:M/R:N/S:U (3.4)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:N/D:N/Y:M/R:N/S:U)

##### Recommendation

Consider fetching the prices from oracles such as Chainlink or Pyth.

##### Remediation

**RISK ACCEPTED:** The **Pontis team** accepted the risk of this finding.

##### References

[Pontis-Labs/evm-bridge-contracts/contracts/pontis-bridge-v1.sol#L247](https://github.com/Pontis-Labs/evm-bridge-contracts/blob/main/contracts/pontis-bridge-v1.sol#L247)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | EVM Bridge Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/pontis/evm-bridge-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/pontis/evm-bridge-contracts

### Keywords for Search

`vulnerability`

