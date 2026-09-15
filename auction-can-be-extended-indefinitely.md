---
# Core Classification
protocol: Ocean Protocol H2O System and Action
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50388
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
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

AUCTION CAN BE EXTENDED INDEFINITELY

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the contract, `SurplusAuctionHouse.sol` observed that the function `restartAuction` lacks access control; thus, anyone can make an external call to this function. Furthermore, calling the `restartAuction` function just before the auction expires (no bid is issued) allows the auction to be extended by `two` days. An external call to `restartAuction` only requires a valid auction `id,` the auction `id` can easily be obtainable via the `startAuction` function `emit` event. This can be done repeatedly to extend the auction forever for any auction.

Code Location
-------------

* Default Auction length is of `two` days

```{language=solidity firstnumber=297 caption=SurplusAuctionHouse.sol hlines=298}
// Total length of the auction
uint48 public totalAuctionLength = 2 days;

```

- Active auction's `id` can be obtained via emit event of `startAuction` function

```{language=solidity firstnumber=386 caption=SurplusAuctionHouse.sol hlines=386}
        emit StartAuction(id, auctionsStarted, amountToSell, initialBid, bids[id].auctionDeadline);

```

* Condition `bids[id].auctionDeadline < now` will always be true if `restartAuction` function is called just before an auction expires, as a result, `bids[id].auctionDeadline = addUint48(uint48(now), totalAuctionLength);` increase the auction length again by 2 days.

#### SurplusAuctionHouse.sol

```
    function restartAuction(uint256 id) external {
        require(bids[id].auctionDeadline < now, "RecyclingSurplusAuctionHouse/not-finished");
        require(bids[id].bidExpiry == 0, "RecyclingSurplusAuctionHouse/bid-already-placed");
        bids[id].auctionDeadline = addUint48(uint48(now), totalAuctionLength);
        emit RestartAuction(id, bids[id].auctionDeadline);
    }

```

##### Score

Impact: 1  
Likelihood: 1

##### Recommendation

**ACKNOWLEDGED**: The team claims the above issue is intended behavior. Moreover, the team will add the intended behavior note in the `README documentation`. Furthermore, the team added that, similar to MakerDAO and RAI, the H2O protocol is optimized to maximize the final bid amount rather than minimize the auction time. Therefore, auctions can be extended if there is no bid as this does not affect the outcome of other auctions or the operation of other parts of the protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ocean Protocol H2O System and Action |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/ocean-protocol/ocean-protocol-h2o-system-and-action-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

