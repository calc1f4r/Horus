---
# Core Classification
protocol: Reservoir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51146
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/fortunafi/reservoir-updated
source_link: https://www.halborn.com/audits/fortunafi/reservoir-updated
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

Use of Deprecated Chainlink's latestAnswer() Function

### Overview


The bug report discusses an issue in the `AssetAdapter` and `PegStabilityModule` contracts where the deprecated `latestAnswer()` function from Chainlink is used to retrieve prices. This function is no longer recommended and can cause incorrect prices to be fed or even a Denial of Service. The report suggests implementing the recommended `latestRoundData()` method and improving the logic to avoid these issues. The FortunaFi team has already solved this issue by implementing a wrapper for the recommended method. 

### Original Finding Content

##### Description

In the contracts `AssetAdapter` and `PegStabilityModule`, the deprecated `latestAnswer()` function is used to retrieve prices from Chainlink:

```
function _underlyingPriceOracleLatestAnswer()
  private
  view
  returns (uint256)
  {
    int256 latestAnswer = underlyingPriceOracle.latestAnswer();

    return latestAnswer > 0 ? uint256(latestAnswer) : 0;
}

function _fundPriceOracleLatestAnswer() private view returns (uint256) {
    int256 latestAnswer = fundPriceOracle.latestAnswer();

    return latestAnswer > 0 ? uint256(latestAnswer) : 0;
}
```

According to Chainlink’s documentation ([API Reference](https://docs.chain.link/data-feeds/api-reference#latestanswer)), the `latestAnswer` function is deprecated. This function does not throw an error if no answer has been reached, but instead returns 0, possibly causing an incorrect price to be fed to the different price feeds or even a Denial of Service by a division by zero.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:N/R:N/S:U)

##### Recommendation

Consider implementing the [latestRoundData()](https://docs.chain.link/data-feeds/api-reference#latestrounddata) method and improving logic to take advantage of its improved features.

Remediation plan
----------------

**SOLVED**: The **FortunaFi team** implemented a wraper of the Chainlink's method `latestRoundData` which is the safer and recommended one.

##### Remediation Hash

<https://github.com/fortunafi/reservoir/commit/08ac0f59cdc6a73f5027ec08628283e40981b825>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Reservoir |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/fortunafi/reservoir-updated
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/fortunafi/reservoir-updated

### Keywords for Search

`vulnerability`

