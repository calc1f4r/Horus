---
# Core Classification
protocol: BakerFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33672
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-bakerfi
source_link: https://code4rena.com/reports/2024-05-bakerfi
github_link: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/15

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
finders_count: 0
finders:
---

## Vulnerability Title

[01] Unhandled Chainlink revert can lock price oracle access

### Overview

See description below for full details.

### Original Finding Content


Chainlink's multisigs can immediately block access to price feeds at will. Therefore, to prevent denial of service scenarios, it is recommended to query Chainlink price feeds using a defensive approach with Solidity’s try/catch structure. In this way, if the call to the price feed fails, the caller contract is still in control and can handle any errors safely and explicitly.

Refer to <https://blog.openzeppelin.com/secure-smart-contract-guidelines-the-dangers-of-price-oracles/> for more information regarding potential risks to account for when relying on external price feed providers.

[Link to code](https://github.com/code-423n4/2024-05-bakerfi/blob/main/contracts/oracles/EthOracle.sol#L31):

```js
    function getLatestPrice() public view override returns (IOracle.Price memory price) {
@-->    (, int256 answer, uint256 startedAt, uint256 updatedAt,) = _ethPriceFeed.latestRoundData();
        if ( answer<= 0 ) revert InvalidPriceFromOracle();        
        if ( startedAt ==0 || updatedAt == 0 ) revert InvalidPriceUpdatedAt();    

        price.price = uint256(answer);
        price.lastUpdate = updatedAt;
    }
```

### Similar past issues

*   [Unhandled chainlink revert would lock all price oracle access](https://github.com/code-423n4/2022-07-juicebox-findings/issues/59)
*   [If a token's oracle goes down or price falls to zero, liquidations will be frozen](https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/161)

### Recommended Mitigation Steps

Surround the call to `latestRoundData()` with try/catch instead of calling it directly and provide a graceful alternative/exit.

**[0xleastwood (judge) decreased severity to Low/Non-Critical and commented](https://github.com/code-423n4/2024-05-bakerfi-findings/issues/15#issuecomment-2164037526):**
 > I would not consider this `medium` severity because the likelihood is extremely low. Downgrading to `QA`.

**[hvasconcelos (BakerFi) acknowledged](https://github.com/code-423n4/2024-05-bakerfi-findings/issues/15#event-13203313318)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BakerFi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-bakerfi
- **GitHub**: https://github.com/code-423n4/2024-05-bakerfi-findings/issues/15
- **Contest**: https://code4rena.com/reports/2024-05-bakerfi

### Keywords for Search

`vulnerability`

