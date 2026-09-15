---
# Core Classification
protocol: Across Protocol OFT Integration Differential Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58417
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Insufficient Validation of Sent Amount in OFTTransportAdapter

### Overview


The OFTTransportAdapter contract has a function called `_transferViaOFT` that transfers assets between two locations. However, it only checks the amount received at the destination and not the amount sent at the origin. This could potentially allow a messenger to take more assets at the origin and only deposit a smaller amount at the destination, passing the check. The documentation for this function also states that the amount sent and received may differ. To prevent this, restrictions should be imposed on the values sent at the origin and the tokens used should be validated to ensure they do not have any unusual behavior. This issue has been resolved in a recent update.

### Original Finding Content

In the `OFTTransportAdapter` contract, the [`_transferViaOFT` function](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapter.sol#L94-L97) gets the `OFTReceipt` output containing two elements: the amount sent at origin and the amount received at destination. The current implementation only validates the amount received at destination, ensuring that it matches the input amount specified by the user. However, this approach overlooks the validation of the amount sent, potentially increasing the attack surface.

Due to the lack of validation of values sent at origin, a scenario might materialize whereby the messenger could take more assets at origin, deposit the correct lesser amount at destination, and pass the check. [LayerZero's documentation on the `_debit` function](https://docs.layerzero.network/v2/developers/evm/oft/quickstart#constructing-an-oft-contract) states that *"In NON-default OFT, amountSentLD could be 100, with a 10% fee, the amountReceivedLD amount is 90, therefore amountSentLD CAN differ from amountReceivedLD."*. The current implementation tries to mitigate this through the [`forceApprove` call](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapter.sol#L92) method associated with the token. Still, if its implementation allows flexible or greater values than the amount sent, the outcome would rely on the assumption that the messenger does not take more than needed.

Consider imposing restrictions on the values sent at origin to reduce the attack surface and prevent situations such as the aforementioned ones. In addition, consider validating that the tokens used through the OFT messenger do not present a behavior deviation or edge cases when using the approval functionality.

***Update:** Resolved in [pull request #1027](https://github.com/across-protocol/contracts/pull/1027).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Protocol OFT Integration Differential Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

