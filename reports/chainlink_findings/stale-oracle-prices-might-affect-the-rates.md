---
# Core Classification
protocol: Definer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13534
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/02/definer/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Alex Wade
  - Shayan Eskandari
---

## Vulnerability Title

Stale Oracle prices might affect the rates

### Overview


This bug report is related to the ChainLink oracle, which is used to update prices for tokens. Due to network congestion or other reasons, the price that the ChainLink oracle returns may be old and not up to date. This is more extreme in lesser known tokens that have fewer ChainLink Price feeds. The codebase does not check the timestamp of the price, thus the bug. 

To fix this issue, it is recommended to do a sanity check on the price returned from the oracle. If the price is older than a threshold, the code should revert or handle it in other means. This will ensure that the prices returned from the oracle are up to date.

### Original Finding Content

#### Description


It’s possible that due to network congestion or other reasons, the price that the ChainLink oracle returns is old and not up to date. This is more extreme in lesser known tokens that have fewer ChainLink Price feeds to update the price frequently.
The codebase as is, relies on `chainLink().getLatestAnswer()` and does not check the timestamp of the price.


#### Examples


/contracts/registry/TokenRegistry.sol#L291-L296



```
    function priceFromAddress(address tokenAddress) public view returns(uint256) {
        if(Utils.\_isETH(address(globalConfig), tokenAddress)) {
            return 1e18;
        }
        return uint256(globalConfig.chainLink().getLatestAnswer(tokenAddress));
    }

```
#### Recommendation


Do a sanity check on the price returned from the oracle. If the price is older than a threshold, revert or handle in other means.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Definer |
| Report Date | N/A |
| Finders | Alex Wade, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/02/definer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

