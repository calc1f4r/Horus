---
# Core Classification
protocol: Gains Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50957
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/gains-trade/gains-trade-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/gains-trade/gains-trade-smart-contract-security-assessment
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

WRONG FEE SENT TO CHAINLINK NODES

### Overview


The bug report describes an issue with the `makeOpenPnlRequest()` function in the `GTokenOpenPnlFeed` contract. The function uses the `linkFeePerNode` variable to calculate the amount of Link to send to Chainlink oracles. However, the calculation is incorrect as it depends on the contract's balance. This can lead to two scenarios: if the contract's Link balance is too high, it will send more Link than needed, and if it is too low, the transaction will fail. The impact of this bug is low, but the likelihood of it occurring is high. The recommendation is to accept the risk and implement a solution where the contract's Link balance is periodically refilled to ensure the correct amount is always sent to the oracles.

### Original Finding Content

##### Description

In the `GTokenOpenPnlFeed` contract, the `makeOpenPnlRequest()` function is used to send requests to a pool of Chainlink oracles:

#### GTokenOpenPnlFeed.sol

```
// Create requests
function makeOpenPnlRequest() private{
    Chainlink.Request memory linkRequest = buildChainlinkRequest(
        job,
        address(this),
        this.fulfill.selector
    );

    uint linkFeePerNode = IERC20(chainlinkTokenAddress())
        .balanceOf(address(this))
        / LINK_FEE_BALANCE_DIVIDER
        / oracles.length;

    requests[++lastRequestId] = Request({
        initiated: true,
        active: true,
        linkFeePerNode: linkFeePerNode
    });

    nextEpochValuesRequestCount++;
    nextEpochValuesLastRequest = block.timestamp;

    for(uint i; i < oracles.length; i ++){
        requestIds[sendChainlinkRequestTo(
            oracles[i],
            linkRequest,
            linkFeePerNode
        )] = lastRequestId;
    }

    emit NextEpochValueRequested(
        gToken.currentEpoch(),
        lastRequestId,
        job,
        oracles.length,
        linkFeePerNode
    );
}

```

\color{black}
\color{white}

The `linkFeePerNode` variable is wrongly calculated, as it depends on the contract's balance. If the Link balance of the `GTokenOpenPnlFeed` contract is too high, more Link than needed would be sent to the Chainlink oracles as fees. In case that the Link balance of the `GTokenOpenPnlFeed` contract is not high enough, the contract will not send enough Link to the Chainlink oracles and the transactions will revert.

##### Score

Impact: 1  
Likelihood: 5

##### Recommendation

**RISK ACCEPTED**: The `Gains Trade team` accepted the risk and stated:
"We will send enough to the contract so that divided by 1000 it represents the amount we want, and then we will refill it every few months. This pattern allows everyone to send a link to the contract in a decentralized manner. It also means the transaction can never revert, unlike what the issue says because it can never run out of LINK."

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Gains Trade |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/gains-trade/gains-trade-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/gains-trade/gains-trade-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

