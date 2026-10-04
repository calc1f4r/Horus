---
# Core Classification
protocol: SKALE
chain: everychain
category: reentrancy
vulnerability_type: reentrancy

# Attack Vector Details
attack_type: reentrancy
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1598
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-skale-contest
source_link: https://code4rena.com/reports/2022-02-skale
github_link: https://github.com/code-423n4/2022-02-skale-findings/issues/24

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - reentrancy

protocol_categories:
  - dexes
  - cdp
  - yield
  - launchpad
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-01] Reentrancy in `MessageProxyForSchain` leads to replay attacks

### Overview


This bug report discusses a vulnerability in the `postIncomingMessages` function of the `MessageProxyForSchain.sol` contract. This function calls `_callReceiverContract(fromChainHash, messages[i], startingCounter + 1)` which gives control to a contract that is potentially attacker-controlled before updating the `incomingMessageCounter`. This allows an attacker to re-enter the `postIncomingMessages` function and submit the same messages again, creating a replay attack. 

A proof of concept (POC) is provided to demonstrate the vulnerability. In the POC, the attacker can submit two cross-chain messages to be executed: one to transfer 1000 USDC and one to call their attacker-controlled contract. Some node submits the `postIncomingMessages(params)` transaction, transfers 1000 USDC, then calls the attackers contract, who can then call `postIncomingMessages(params)` again, receive 1000 USDC a second time, and stop the recursion.

The recommended mitigation step is to add a `messageInProgressLocker` modifier to `postIncomingMessages` as was done in `MessageProxyForMainnet`.

### Original Finding Content

_Submitted by cmichel_

The `postIncomingMessages` function calls `_callReceiverContract(fromChainHash, messages[i], startingCounter + 1)` which gives control to a contract that is potentially attacker controlled *before* updating the `incomingMessageCounter`.

```solidity
for (uint256 i = 0; i < messages.length; i++) {
    // @audit re-entrant, can submit same postIncomingMessages again
    _callReceiverContract(fromChainHash, messages[i], startingCounter + 1);
}
connectedChains[fromChainHash].incomingMessageCounter += messages.length;
```

The attacker can re-enter into the `postIncomingMessages` function and submit the same messages again, creating a replay attack.
Note that the `startingCounter` is the way how messages are prevented from replay attacks here, there are no further nonces.

### Proof of Concept

Attacker can submit two cross-chain messages to be executed:

1.  Transfer 1000 USDC
2.  A call to their attacker-controlled contract, could be masked as a token contract that allows re-entrance on `transfer`.

Some node submits the `postIncomingMessages(params)` transaction, transfers 1000 USDC, then calls the attackers contract, who can themself call `postIncomingMessages(params)` again, receive 1000 USDC a second time, and stop the recursion.

### Recommended Mitigation Steps

Add a `messageInProgressLocker` modifier to `postIncomingMessages` as was done in `MessageProxyForMainnet`.

**cstrangedk (SKALE) resolved:**

Resolved via https://github.com/skalenetwork/IMA/pull/1054


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | SKALE |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-skale
- **GitHub**: https://github.com/code-423n4/2022-02-skale-findings/issues/24
- **Contest**: https://code4rena.com/contests/2022-02-skale-contest

### Keywords for Search

`Reentrancy`

