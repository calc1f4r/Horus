---
# Core Classification
protocol: AVA Teleporter Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32760
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ava-teleporter-audit
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

Fees Do Not Follow a Predictable Calculation

### Overview


This bug report discusses an issue with the `TeleporterMessenger` contract, which is used to send messages between different networks. Currently, there is no check in place to ensure that the fee deposited for the relayer will cover the gas cost of executing the message. This can result in users either spending more or less than necessary, which could lead to the message not being relayed. Other message bridging protocols have a solution for this by predicting the gas cost and providing a view-only function to estimate the necessary fee before submitting the message. The suggestion is to add this functionality to the `Teleporter` contract. However, the developers at AVA Labs have acknowledged the issue but have not yet resolved it. They explain that the fee and fee asset accepted by a relayer is determined by the relayer themselves and can vary based on factors such as the current gas price and asset prices. Therefore, they believe it is best to handle fee estimation and publishing on a case-by-case basis off-chain. 

### Original Finding Content

When sending a message with the `TeleporterMessenger` contract, there is [no check to ensure that the fee deposited](https://github.com/ava-labs/teleporter/blob/253b833518aa7a6448650388cc288bd76d8470a7/contracts/src/Teleporter/TeleporterMessenger.sol#L624-L627) for the relayer who will submit the message on the destination subnet will be sufficient to cover the gas cost incurred by executing the message. This could cause users to spend more than what is required to execute their message, or less, in which case the message may not be relayed as it would not be profitable for a relayer.


Some message bridging protocols remedy this by predicting the gas cost based on the size of the message and the expected gas limit on the other subnet, which is translated into `feeAsset` units. Moreover, such protocols provide a view-only function to predict this value off-chain before submitting the message.


Consider adding functionality to estimate the necessary fee and assert it against the transferred fee assets.


***Update:** Acknowledged, not resolved. AVA Labs stated the following about the issue:*



> *The fee asset and amount "accepted" by a given relayer is defined by that individual relayer themselves, so it makes sense for those fee estimates to be published off-chain, out of the scope of the `Teleporter` contract. For instance, some dApps/subnets may run a relayer that relays messages for free to attract more users. In other cases, one relayer may only accept fees paid in AVAX, while another accepts fees paid in USDC or other arbitrary ERC20 tokens. The fee amount of a given asset expected for a given relayer may also depend on the current gas price at the destination chain for a given message, the current price of the native gas token being spent by the relayer, and the current price of the asset being used to pay the relayer's fee. This information isn't necessarily available on-chain, and even if it were, different relayers may use different sources for this information. For these reasons, we think it's best to leave fee estimation and publishing to be handled on a case-by-case basis off-chain.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | AVA Teleporter Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ava-teleporter-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

