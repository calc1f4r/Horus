---
# Core Classification
protocol: GMI and Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51839
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
source_link: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
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

GMPriceOracle does not check for for the Chainlink sequencer to NOT be down

### Overview

See description below for full details.

### Original Finding Content

##### Description

When utilizing Chainlink in L2 chains like Arbitrum, it's important to ensure that the prices provided are not falsely perceived as fresh, even when the sequencer is down. This is because the sequencer can be down, and a malicious actor could reuse invalid prices to gain advantage on the pool or even liquidate users in certain cases. It can be easily seen in the code responsible for that:

<https://github.com/GloopFinance/gm-lending-protocol/blob/37c4ebbf16e997a5aefad9c8c6715af8454ed14d/src/GMPriceOracle.sol#L59C1-L69C6>

```
    function getPriceFromChainlink(address feedId) internal view returns (uint256) {
        AggregatorV3Interface dataFeed = AggregatorV3Interface(feedId);
        (
            ,
            /* uint80 roundID */ int answer /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/,
            ,
            ,

        ) = dataFeed.latestRoundData();
        return uint256(answer);
    }
```

that it does not check anything and returns `answer` without further validation.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:M/R:N/S:U (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:M/R:N/S:U)

##### Recommendation

As a reference, you can follow [this implementation](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code) from Chainlink.

### Remediation Plan

**SOLVED:** The **Gloop Finance team** solved this issue as recommended above.

##### Remediation Hash

<https://github.com/GloopFinance/gm-lending-protocol/commit/9f79538287d22ed076b95760483203dfe37ac0f2#diff-dfbed02222b608a1b2e2157b7482a24afffe2c989483c72fe6750d1849532e44>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | GMI and Lending |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/gloop-finance/gmi-and-lending
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/gloop-finance/gmi-and-lending

### Keywords for Search

`vulnerability`

