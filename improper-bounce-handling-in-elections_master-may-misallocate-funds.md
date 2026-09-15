---
# Core Classification
protocol: XDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61886
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
source_link: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
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
finders_count: 3
finders:
  - István Böhm
  - Andy Lin
  - Cameron Biniamow
---

## Vulnerability Title

Improper Bounce Handling in `elections_master` May Misallocate Funds

### Overview


The report discusses a bug in the `elections_master` contract that causes voter fees to be refunded to the proposal creator instead of being distributed among the voters or the DAO treasury. This can happen when a proposal fails due to insufficient votes or when a message sent to the `master` contract bounces. The team is recommended to clarify their intentions regarding fund distribution and implement a new refund mechanism to handle failed proposals. Alternative solutions, such as sending all locked funds to the `fee_manager` or `master` contracts, are also suggested. Adjustments should also be made to the `master` contract's fund transfer mechanism.

### Original Finding Content

**Update**
Voters may request a refund of their paid fees within one week after a proposal passes but fails during execution. Unclaimed refunds after this period are forfeited and transferred to the fee manager. However, when a proposal fails due to insufficient votes, voter fees are not refundable.

Addressed in: `9f21558ee2373d55ad862e78e349160b25dcbbf9`, `2015a26f6a3bc3ab467edc33bc620384e5c66568`, and, `a0301a896903c7e4706e37923cc9b75070bae4cf`.

**File(s) affected:**`contracts/elections_master.fc`

**Description:** The `on_bounce()` handler in `elections_master` treats any bounced message other than `op::vote_internal` as a failure of the governing action and refunds the entire contract balance to `data::initiated_by_address`. This includes bounces from the `op::make_action` message sent to `master`. If that message fails (e.g., due to gas exhaustion, malformed payloads, or upgrade incompatibilities) the refund goes to the proposal creator rather than preserving funds for voters or protocol maintenance, violating expected fund flows.

At the root of the issue is the lack of a clear mechanism to refund the locked fees for a failed proposal. Another failure path occurs when a proposal fails to reach sufficient votes. Both cases should be handled in a consistent manner.

**Exploit Scenario:**

1.   A proposal concludes and `elections_master` sends an `op::make_action` message to `master`.
2.   The message bounces (e.g., gas exhaustion).
3.   `on_bounce()` refunds the full balance to the proposal creator, diverting funds away from voters and the DAO treasury.

**Recommendation:** First, the team should clarify whether they intend to return any failed funds to the initiator, even if the initiator did not contribute to the proposal's locking fee. However, a new `refund` operation is still recommended to support proposals that never reach the successful threshold.

Otherwise, modify `on_bounce()` to distinguish `op::make_action` bounces and avoid refunding the entire balance to the initiator. Instead, implement a safe fallback that retains or redistributes funds according to protocol rules.

The ideal approach is to refund the voters. This will require leveraging the `elections_wallet` as well. A potential design is for the `elections_wallet` to store the voted amount during the voting process and include an additional `op::refund` that checks whether the wallet participated in voting, then sends the voted balance to the `elections_master`. The `elections_master` will use the received balance to calculate the refund amount and return it to each voter.

Some alternative approaches include sending all locked funds to the `fee_manager` or `master` contracts. Under this model, regardless of whether a proposal succeeds, the collected fees are never returned to the voters. Participants must be aware of this protocol mechanism. The change should include both modifications in bounce handling and the introduction of a new refund mechanism/operation.

Note: the `master` contract has a similar fund transfer mechanism to the proposal initiator in `op::call_jetton_mint`, within the `if msg_value < fees + fee_value + BASE_FEE {}` block. This should also be adjusted depending on the clarified intention.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | XDAO |
| Report Date | N/A |
| Finders | István Böhm, Andy Lin, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/xdao/2670863d-2e1c-42e6-a15c-5572dd4fef85/index.html

### Keywords for Search

`vulnerability`

