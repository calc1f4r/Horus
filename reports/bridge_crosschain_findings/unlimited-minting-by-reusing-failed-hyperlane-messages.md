---
# Core Classification
protocol: LMCV part 3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50682
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

UNLIMITED MINTING BY REUSING FAILED HYPERLANE MESSAGES

### Overview


The bug report describes a problem where it is possible to mint an unlimited number of tokens by repeatedly calling a function that retries failed transactions. This can be done by using the data of a failed transaction multiple times. The bug has been fixed by the DAMfinance team by deleting the successfully retried messages from the mapping.

### Original Finding Content

##### Description

It is possible to transfer `dPrime` tokens across chains using the `dPrimeConnectorHyperlane` contract. If minting the tokens on the destination chain fails, then the program stores the failed transaction in a mapping. It is possible to manually retry the failed transactions by calling the `retry` function on the destination chain. The function reads the failed transaction details from a mapping and mints the specified tokens for the receiver. However, the function does not update the mapping after a successfully retried transaction, so it is possible to mint as many tokens as desired by calling the retry function multiple times with the data of the failed transaction.

Code Location
-------------

#### hyperlane/dPrimeConnectorHyperlane.sol

```
function retry(uint32 _origin, address _recipient, uint256 _nonce) external {
    uint256 amount = failedMessages[_origin][_recipient][_nonce];

    try dPrimeLike(dPrimeContract).mint(_recipient, amount) {
        emit ReceivedTransferRemote(_origin, _recipient, amount);
    } catch {
        emit FailedTransferRemote(_origin, _recipient, nonce, amount);
    }
}

```

As proof of concept, a failed Hyperlane message was created in a local test environment. Then the same failed message was used multiple times to mint dPrime tokens for the receiver.

![unlimited_minting.png](https://halbornmainframe.com/proxy/audits/images/659eb9e2a1aa3698c0ed3fd7)

It is noted that it is possible to mint as many tokens as desired using the failed message.

##### Score

Impact: 5  
Likelihood: 5

##### Recommendation

**SOLVED**: The `DAMfinance team` solved the issue in commit [cfc13a8](https://github.com/DecentralizedAssetManagement/lmcv/commit/cfc13a806ba391c8875f9d363ee5b35b9a8f8acf) by deleting the successfully retried messages from the `failedMessages` mapping.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | LMCV part 3 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/damfinance/lmcv-part-3-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

