---
# Core Classification
protocol: The Graph
chain: everychain
category: logic
vulnerability_type: refund_ether

# Attack Vector Details
attack_type: refund_ether
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6179
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-the-graph-l2-bridge-contest
source_link: https://code4rena.com/reports/2022-10-thegraph
github_link: https://github.com/code-423n4/2022-10-thegraph-findings/issues/294

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - refund_ether
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - yield
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-02] If L1GraphTokenGateway’s outboundTransfer is called by a contract, the entire msg.value is blackholed, whether the ticket got redeemed or not

### Overview


This bug report is about the outboundTransfer function in the L1GraphTokenGateway, which is used to transfer user's Graph tokens to L2. The issue is that it passes the caller's address in the submissionRefundAddress and valueRefundAddress, which can cause the loss of the submissionRefund (ETH passed to outboundTransfer() minus the total submission fee), or in the event of failed L2 ticket creation, the whole submission fee. This is because ETH and Arbitrum addresses are congruent, but the calling contract may not exist on L2 and even if it does, it may not have a function to move out the refund. The impact is that if L1GraphTokenGateway's outboundTransfer is called by a contract, the entire msg.value is blackholed, whether the ticket got redeemed or not. 

A proof of concept example is provided, which is about Alice who has a multisig wallet. She sends 100 Graph tokens to L1GraphTokenGateway, and passes X ETH for submission. She receives an L1 ticket, but since the max gas was too low, the creation failed on L2 and the funds got sent to the multisig address at L2. Therefore, Alice loses X ETH. 

The recommended mitigation steps are to add an isContract flag, or to add a refundAddr address parameter to the API. 

Overall, this bug report is about the outboundTransfer function in the L1GraphTokenGateway, which can cause the loss of the submissionRefund or the whole submission fee if called by a contract. The proof of concept and the recommended mitigation steps are also provided.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-thegraph/blob/309a188f7215fa42c745b136357702400f91b4ff/contracts/gateway/L1GraphTokenGateway.sol#L236


## Vulnerability details

The outboundTransfer function in L1GraphTokenGateway is used to transfer user's Graph tokens to L2. To do that it eventually calls the standard Arbitrum Inbox's createRetryableTicket. The issue is that it passes caller's address in the `submissionRefundAddress` and `valueRefundAddress`. This behaves fine if caller is an EOA, but if it's called by a contract it will lead to loss of the submissionRefund (ETH passed to outboundTransfer() minus the total submission fee), or in the event of failed L2 ticket creation, the whole submission fee. The reason it's fine for EOA is because of the fact that ETH and Arbitrum addresses are congruent. However, the calling contract probably does not exist on L2 and even in the rare case it does, it might not have a function to move out the refund.

The docs don't suggest contracts should not use the TokenGateway, and it is fair to assume it will be used in this way. Multisigs are inherently contracts, which is one of the valid use cases. Since likelihood is high and impact is medium (loss of submission fee), I believe it to be a HIGH severity find.

## Impact

If L1GraphTokenGateway's outboundTransfer is called by a contract, the entire msg.value is blackholed, whether the ticket got redeemed or not.

## Proof of Concept

Alice has a multisig wallet. She sends 100 Graph tokens to L1GraphTokenGateway, and passes X ETH for submission. She receives an L1 ticket, but since the max gas was too low, the creation failed on L2 and the funds got sent to the multisig address at L2. Therefore, Alice loses X ETH.

## Tools Used

https://github.com/OffchainLabs/arbitrum/blob/master/docs/L1_L2_Messages.md
Manual audit

## Recommended Mitigation Steps

A possible fix is to add an `isContract` flag. If sender is a contract, require the flag to be true.

Another option is to add a `refundAddr` address parameter to the API.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | The Graph |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-thegraph
- **GitHub**: https://github.com/code-423n4/2022-10-thegraph-findings/issues/294
- **Contest**: https://code4rena.com/contests/2022-10-the-graph-l2-bridge-contest

### Keywords for Search

`Refund Ether, Business Logic`

