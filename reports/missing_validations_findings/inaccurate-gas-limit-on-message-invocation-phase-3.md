---
# Core Classification
protocol: Taiko Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34354
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/taiko-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Inaccurate Gas Limit on Message Invocation - Phase 3

### Overview

See description below for full details.

### Original Finding Content

Users can send cross-chain messages by calling [`sendMessage`](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L126C14-L126C25) on the `Bridge` contract. An optional gas limit can be defined for this message. In that case, if a user wants their message to be [executed with at least `A` gas](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L488), `message.gasLimit` has to be at least `A + minGas`, where `minGas` depends on the [message length plus a flat gas amount](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L452).


When a message is processed by a third party, the gas remaining before invoking the user's message is validated to be [greater than](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L611-L613) `64 / 63 * A`. This is because of [EIP-150](https://eips.ethereum.org/EIPS/eip-150), which silently caps the amount of gas sent in external calls to `63 / 64 * gasleft()`. If such a check were not present, it would be possible for the gas to be capped by EIP-150, executing the call with less than `A` gas.


However, while the intention was correct, a gas limit of `A` is not guaranteed. This is due to the gas expenses that accumulate between the [EIP-150 check](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L611-L613) and the actual [message execution on the target](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L488):


* Memory expansion costs
* Account access
* Transfers
* Opcode costs


Because `1 / 64 * gasleft()` has to be enough to execute the [rest of the `processMessage` function](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L265-L296) without running out of gas, a gas limit below `A` on the target is only possible for high gas limits. This [proof of concept](https://gist.github.com/0xmp/4da10ab59c04f71cdb9557ff320f9fc2) shows the issue in practice.


Consider addressing the above to build a more predictable bridge for users and projects sending cross-chain messages. What follows is an example of how this could be achieved.


The goal of the computation is to ensure that EIP-150 does not silently cap the amount of gas sent with the external call to be less than `A`. We note:


* `memory_cost`: the amount of gas needed to expand the memory when storing the inputs and outputs of the external call.
* `access_gas_cost`: the gas cost of accessing the `message.to` account. This currently corresponds to 2600 gas if the account is cold, and 100 otherwise.
* `transfer_gas_cost`: the cost of transferring a non-zero `msg.value`. This cost is currently 9000 gas but provides a 2300 gas stipend to the called contract.
* `create_gas_cost`: the cost of creating a new account, currently 25000 gas. This only applies if `message.value != 0`, `message.to.nounce == 0`, `message.to.code == b""`, and `message.to.balance == 0`. Since `message.to` is [checked to have code](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L645), this cost can be ignored here.


Thus, we want to check that the following:




```
 63 / 64 * (gasleft() - memory_cost - access_gas_cost - transfer_gas_cost)

```


is at least as much as `A` ([reference implementation](https://github.com/ethereum/execution-specs/blob/master/src/ethereum/cancun/vm/gas.py#L230)). The sum of `access_gas_cost` and `transfer_gas_cost` can be upper-bounded with `2_600 + 9_000 - 2_300 = 9_300`. The [`memory_cost`](https://github.com/ethereum/execution-specs/blob/master/src/ethereum/cancun/vm/gas.py#L128) is cumbersome to compute in practice, but by estimating the costs through tests, we can upper-bound the cost of memory expansion for up to `10_000` bytes of `message.data` in the context of the call with the formula `1_200 + 3 * message.data.length / 32`.


As such, it would be possible to validate that the call will have enough gas by checking the following condition right before the external call is made:




```
 63 * gasleft() >= 64 * A + 63 * (9_300 + 1_200 + 3 * message.data.length / 32) + small_buffer

```


This would be accurate for messages with up to `10_000` bytes of `message.data`. Any message above this limit could be required to have a gas limit of zero which would force it to be [processed by its `destOwner`](https://github.com/taikoxyz/taiko-mono/blob/dd8725f8d27f835102fa3c5a013003090268357d/packages/protocol/contracts/bridge/Bridge.sol#L233-L235). A similar approach, without a constraint on the data size, has been adopted by [Optimism](https://github.com/ethereum-optimism/optimism/blob/8dd18f0efd9719762961897bf93ef1dd8ce702a7/packages/contracts-bedrock/src/libraries/SafeCall.sol#L51-L81) and can be used as inspiration.


***Update:** Resolved in [pull request #17529](https://github.com/taikoxyz/taiko-mono/pull/17529) at commit [a937ec5](https://github.com/taikoxyz/taiko-mono/tree/a937ec5d7bbb42721caf9702141164c72cd92c34). After further discussions with the audit team, the fix implemented follows an alternative, more efficient approach than the one suggested in the issue.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Taiko Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/taiko-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

