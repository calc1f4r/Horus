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
solodit_id: 27622
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 7
finders:
  - Rozzo
  - Bauer
  - 0xRizwan
  - 0xmuxyz
  - MrjoryStewartBaxter
---

## Vulnerability Title

Unhandled DoS when access to Chainlik oracle is blocked

### Overview

See description below for full details.

### Original Finding Content

## Summary

In certain exceptional scenarios, oracles may become temporarily unavailable. As a result, invoking the `latestRoundData` function could potentially revert without a proper error handling.

## Vulnerability Details

Steadefi documentation gives special focus on Chainlink price feed dependency, (https://github.com/Cyfrin/2023-10-SteadeFi/tree/main "Additional Context"). The concern stems from the potential for Chainlink multisignature entities to deliberately block the access to the price feed. In such a situation, using the `latestRoundData` function could lead to an unexpected revert.

In certain extraordinary situations, Chainlink has already proactively suspended particular oracles. To illustrate, in the case of the UST collapse incident, Chainlink chose to temporarily halt the UST/ETH price oracle to prevent the propagation of incorrect data to various protocols.

Additionally, this danger has been highlighted and very well documented by OpenZeppelin in https://blog.openzeppelin.com/secure-smart-contract-guidelines-the-dangers-of-price-oracles. For our current scenario:

*"While currently there’s no whitelisting mechanism to allow or disallow contracts from reading prices, powerful multisigs can tighten these access controls. In other words, the multisigs can immediately block access to price feeds at will. Therefore, to prevent denial of service scenarios, it is recommended to query ChainLink price feeds using a defensive approach with Solidity’s try/catch structure. In this way, if the call to the price feed fails, the caller contract is still in control and can handle any errors safely and explicitly".*

As a result and taking into consideration the recommendation from OpenZepplin, it is essential to thoroughly tackle this matter within the codebase, as it directly relates to many functionalities of the system which are based on the oracle's output.

Another example to check this vulnerability can be consulted in https://solodit.xyz/issues/m-18-protocols-usability-becomes-very-limited-when-access-to-chainlink-oracle-data-feed-is-blocked-code4rena-inverse-finance-inverse-finance-contest-git 

## Proof of Concept

As previously discussed, to mitigate the potential risks related to a denial-of-service situation, it is recommended to implement a try-catch mechanism when querying Chainlink prices in the `_getChainlinkResponse` function within `ChainlinkARBOracle.sol` (link to code below). By adopting this approach, in case there's a failure in invoking the price feed, the caller contract retains control and can effectively handle any errors securely and explicitly.

https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/contracts/oracles/ChainlinkARBOracle.sol#L188-L194

```

 (
      uint80 _latestRoundId,
      int256 _latestAnswer,
      /* uint256 _startedAt */,
      uint256 _latestTimestamp,
      /* uint80 _answeredInRound */
    ) = AggregatorV3Interface(_feed).latestRoundData();

```

## Impact

In the event of a malfunction or cessation of operation of a configured Oracle feed, attempting to check for the `latestRoundData` will result in a revert that must be managed manually by the system.

## Tools Used

Manual review

## Recommendations

Wrap the invocation of the `latestRoundData()` function within a `try-catch` structure rather than directly calling it. In situations where the function call triggers a revert, the catch block can be utilized to trigger an alternative oracle or handle the error in a manner that aligns with the system's requirements.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | Rozzo, Bauer, 0xRizwan, 0xmuxyz, MrjoryStewartBaxter, ZedBlockchain, 0xanmol |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

