---
# Core Classification
protocol: ReyaNetwork-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41136
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-02] Potential loss of native tokens

### Overview

See description below for full details.

### Original Finding Content

The `fulfillOracleQuery` function within the `OracleUpdateModule` contract is marked as `payable`, which means it can accept Ether (`msg.value`). However, when the `oracleProvider` is set to `STORK`, the function does not handle the `msg.value` in any particular way. This can lead to a situation where a user inadvertently sends Ether along with their call to `fulfillOracleQuery` for a `STORK` oracle provider, resulting in the loss of native tokens. The Ether sent in such a transaction is not utilized or refunded, causing users to lose the sent amount.

```solidity
    function fulfillOracleQuery(
        OracleProvider oracleProvider,
        bytes calldata signedOffchainData
    )
        external
>>>     payable
        override
    {
        FeatureFlagSupport.ensureGlobalAccess();

        // note, if an executor is trusted, they are allowed to execute a fullfill oracle query operation
        // on top of any oracle provider type (e.g. stork, pyth, etc)
        FeatureFlagSupport.ensureExecutorAccess();

>>>     if (oracleProvider == OracleProvider.STORK) {
            address storkVerifyContract = Configuration.getStorkVerifyContractAddress();
            fullfillOracleQueryStork(storkVerifyContract, signedOffchainData);
        } else if (oracleProvider == OracleProvider.PYTH) {
            address pythAddress = Configuration.getPythAddress();
            fullfillOracleQueryPyth(pythAddress, signedOffchainData);
        }
    }
```

In the above code, there is no handling of `msg.value` when `oracleProvider` is `STORK`, which can lead to native token loss.

It is recommended to implement a check to accept Ether only when the `oracleProvider` is `PYTH`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ReyaNetwork-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

