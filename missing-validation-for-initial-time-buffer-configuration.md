---
# Core Classification
protocol: Name Service (BNS) Contracts v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52500
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
source_link: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
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

Missing validation for initial time buffer configuration

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `constructor`of the **BeraAuctionHouse** contract directly assigns the `timeBuffer_`parameter to the `timeBuffer` state variable without validating that it adheres to the defined upper bound of **MAX\_TIME\_BUFFER**. This omission could allow a deployment with an invalid `timeBuffer`value that exceeds **MAX\_TIME\_BUFFER**.

  

Such a misconfiguration would undermine the auction process by allowing excessively long extensions for bids placed close to the end time. It could also lead to unintended behaviors or inefficiencies in the auction system.

  

Code Location
-------------

The `constructor` does not validate that `timeBuffer_` is lower than or equal to **MAX\_TIME\_BUFFER**:

```
    constructor(
        BaseRegistrar base_,
        BeraDefaultResolver resolver_,
        IWETH weth_,
        uint256 auctionDuration_,
        uint256 registrationDuration_,
        uint192 reservePrice_,
        uint56 timeBuffer_,
        uint8 minBidIncrementPercentage_,
        address paymentReceiver_
    ) Ownable(msg.sender) {
        base = base_;
        resolver = resolver_;
        weth = weth_;
        auctionDuration = auctionDuration_;
        registrationDuration = registrationDuration_;
        paymentReceiver = paymentReceiver_;

        _pause();

        reservePrice = reservePrice_;
        timeBuffer = timeBuffer_;
        minBidIncrementPercentage = minBidIncrementPercentage_;
    }
```

##### BVSS

[AO:A/AC:L/AX:M/R:N/S:U/C:N/A:N/I:M/D:N/Y:N (3.4)](/bvss?q=AO:A/AC:L/AX:M/R:N/S:U/C:N/A:N/I:M/D:N/Y:N)

##### Recommendation

It is recommended to add a check in the `constructor`to ensure `timeBuffer_`does not exceed **MAX\_TIME\_BUFFER**.

##### Remediation

**SOLVED:** The **Beranames team** solved the issue in the specified commit id.

##### Remediation Hash

<https://github.com/Beranames/beranames-contracts-v2/pull/91/commits/92c2b0414ec80b76f86cd3e2032bb15e0b393797>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Name Service (BNS) Contracts v2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/beranames/name-service-bns-contracts-v2

### Keywords for Search

`vulnerability`

