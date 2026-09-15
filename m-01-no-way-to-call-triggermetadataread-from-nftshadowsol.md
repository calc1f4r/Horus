---
# Core Classification
protocol: NFTMirror_2024-12-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50039
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/NFTMirror-security-review_2024-12-30.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] No way to call `triggerMetadataRead()` from `NFTShadow.sol`

### Overview


This bug report is about a low severity issue that has a high likelihood of occurring. The problem is with the `NFTShadow.sol#tokenURI()` function, which is used to return the token URI for token IDs. This function calls another function, `tokenURI()`, from the `MetadataReadRenderer.sol` contract. However, there is a problem with the `MetadataReadRenderer.sol` contract. It has a function called `triggerMetadataRead()` that is used to read token URIs from the base collection and display them in the shadow collection. This function uses the **lzRead** from the LayerZero protocol. The issue is that the `triggerMetadataRead()` function needs to know the `baseCollectionAddress` value, which is determined by the `msg.sender`. However, the `triggerMetadataRead()` function is not being called from the correct place, which is `NFTShadow.sol`. As a result, the `MetadataReadRenderer.sol` contract is unable to do anything and the `NFTShadow.sol#tokenURI()` function can only return the base URI. To fix this issue, a new function should be created in `NFTShadow.sol` to trigger the `MetadataReadRenderer.sol#tokenURI()` function.

### Original Finding Content

## Severity

**Impact:** Low

**Likelihood:** High

## Description

The `NFTShadow.sol#tokenURI()` function returns the token URI for token IDs by invoking `tokenURI()` from `MetadataReadRenderer.sol`.
However, the `MetadataReadRenderer.sol` contract has a function `triggerMetadataRead()` to read token URIs from the base collection (from the original chain ) and render them on the shadow collection. using the **lzRead** from LayerZero protocol.

But, because it takes `msg.sender` to determine the `baseCollectionAddress` value.

```solidity
        address baseCollectionAddress = IBeacon(beacon).shadowToBase(
            msg.sender
        );
```

The `triggerMetadataRead()` should get called from `NFTShadow.sol` which is not implemented yet.
With the current implementation `MetadataReadRenderer.sol` can do nothing and `NFTShadow.sol#tokenURI()` can just return the base URI.

## Recommendations

Create a new function in `NFTShadow.sol` to trigger `MetadataReadRenderer.sol#tokenURI()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | NFTMirror_2024-12-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/NFTMirror-security-review_2024-12-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

