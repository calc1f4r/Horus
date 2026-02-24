---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27597
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 6
finders:
  - Slavchew
  - marqymarq10
  - ElHaj
  - FalconHoof
  - 0xCiphky
---

## Vulnerability Title

Setter functions for core GMX contracts

### Overview


This bug report is about the GMX contracts, specifically the ExchangeRouter and GMXOracle. According to the GMX docs, their addresses will change as new logic is added, so setter functions should be added to the GMXVault.sol contract to be able to update the state variables storing those addresses when the need arises. Without the setter functions, the protocol would be unusable given the importance of these contracts. The recommended solution is to create setter functions in the GMXVault.sol as specified in the report. This bug has a medium risk.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/gmx-io/gmx-synthetics#known-issues">https://github.com/gmx-io/gmx-synthetics#known-issues</a>


## Summary
GMX docs state that their ```ExchangeRouter``` and ```GMXOracle``` contracts ```will``` change as new logic is added. Therefore setter functions should be added to ```GMXVault.sol``` to be able to update the state variables storing those addressed when the need arises.

## Vulnerability Details
From the [GMX docs](https://github.com/gmx-io/gmx-synthetics#known-issues):
```
If using contracts such as the ExchangeRouter, Oracle or Reader do note that their addresses will change as new logic is added
```

## Impact
Not being able to use the ```ExchangeRouter``` and ```GMXOracle``` contracts the protocol would effectively be unusable given their importance.

## Tools Used
Manual Review

## Recommendations
Create setter functions in ```GMXVault.sol``` as below:

```
  function updateExchangeRouter(address exchangeRouter) external onlyOwner {
    _store.exchangeRouter = exchangeRouter;
    emit ExchangeRouterUpdated(exchangeRouter);
  }

  function updateGMXOracle(address gmxOracle) external onlyOwner {
    _store.gmxOracle = gmxOracle;
    emit GMXOracleUpdated(gmxOracle);
  }

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | Slavchew, marqymarq10, ElHaj, FalconHoof, 0xCiphky |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

