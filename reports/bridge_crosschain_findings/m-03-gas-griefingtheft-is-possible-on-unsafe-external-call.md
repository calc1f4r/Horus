---
# Core Classification
protocol: Zerem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20311
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-11-01-Zerem.md
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
  - Pashov
---

## Vulnerability Title

[M-03] Gas griefing/theft is possible on unsafe external call

### Overview


This bug report is about a potential attack-vector in a contract called `unlockFor` which is usually called by relayers. The attack-vector is gas griefing on the ETH transfer. This is possible because the `data` that is returned from the `receiver` is copied to memory, and memory allocation becomes very costly if the payload is big. A malicious actor can launch a gas griefing attack on a relayer, and it has been classified as Medium severity. The bug was fixed by using a low-level assembly `call` since it does not automatically copy return data to memory.

### Original Finding Content

**Proof of Concept**

This comment `// TODO: send relayer fees here` in the `unlockFor` method and its design show that it is possible that `unlockFor` is usually called by relayers. This opens up a new attack-vector in the contract and it is gas griefing on the ETH transfer

```solidity
(bool success,) = payable(receiver).call{gas: 3000, value: amount}(hex"");
```

Now `(bool success, )` is actually the same as writing `(bool success, bytes memory data)` which basically means that even though the `data` is omitted it doesn’t mean that the contract does not handle it. Actually, the way it works is the `bytes data` that was returned from the `receiver` will be copied to memory. Memory allocation becomes very costly if the payload is big, so this means that if a `receiver` implements a fallback function that returns a huge payload, then the `msg.sender` of the transaction, in our case the relayer, will have to pay a huge amount of gas for copying this payload to memory.

**Impact**

Malicious actor can launch a gas griefing attack on a relayer. Since griefing attacks have no economic incentive for the attacker and it also requires relayers it should be Medium severity.

**Recommendation**

Use a low-level assembly `call` since it does not automatically copy return data to memory

```solidity
bool success;
assembly {
    success := call(3000, receiver, amount, 0, 0, 0, 0)
}
```

**Client response**

Fixed by using a low-level assembly `call`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Zerem |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2022-11-01-Zerem.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

