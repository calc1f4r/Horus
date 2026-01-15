---
# Core Classification
protocol: Subscription Token - Fabric
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60236
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/subscription-token-fabric/3d319dfc-3e44-4b0a-9016-52d9af89c920/index.html
source_link: https://certificate.quantstamp.com/full/subscription-token-fabric/3d319dfc-3e44-4b0a-9016-52d9af89c920/index.html
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
  - Danny Aksenov
  - Mostafa Yassin
  - Guillermo Escobero
---

## Vulnerability Title

Checks-Effects-Interactions Pattern Violation

### Overview


The client has marked a bug as "Fixed" in the file `SubscriptionTokenV1.sol` with the code `88b955a75e0b3de2838dff83113a215d4406778e`. The bug is related to the Checks-Effects-Interactions coding pattern, which is used to prevent other contracts from manipulating the blockchain in unexpected or malicious ways. The bug was found in two instances, `_refund()` and `_fetchSubscription()`, where external calls were made before checking and acting on internal conditions. The recommendation is to refactor the code to follow the Checks-Effects-Interactions pattern.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `88b955a75e0b3de2838dff83113a215d4406778e`.

**File(s) affected:**`SubscriptionTokenV1.sol`

**Description:** The [Checks-Effects-Interactions](https://solidity.readthedocs.io/en/latest/security-considerations.html#use-the-checks-effects-interactions-pattern) coding pattern is meant to mitigate any chance of other contracts manipulating the state of the blockchain in unexpected and possibly malicious ways before control is returned to the original contract. As the name implied, only after checking whether appropriate conditions are met and acting internally on those conditions should any external calls to, or interactions with, other contracts be done.

The following instance(s) have been identified:

*   `_refund()`

```
uint256 tokens = balance * _tokensPerSecond;

if (balance > 0) {
    sub.secondsPurchased -= balance;
    _transferOut(account, tokens);  <== External Call
}

 _subscriptions[account] = sub; <== State Change
```

*   `_fetchSubscription()`

```
if (sub.tokenId == 0) {
    require(_supplyCap == 0 || _tokenCounter < _supplyCap, "Supply cap reached");
    _tokenCounter += 1;
    sub = Subscription(_tokenCounter, 0, 0, block.timestamp, block.timestamp, 0, 0, 0); <== This state gets updated in `purchaseTime()`
    _safeMint(account, sub.tokenId); <== External Call 
}
```

**Recommendation:** We recommend refactoring the code so that it conforms to the Checks-Effects-Interactions pattern.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Subscription Token - Fabric |
| Report Date | N/A |
| Finders | Danny Aksenov, Mostafa Yassin, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/subscription-token-fabric/3d319dfc-3e44-4b0a-9016-52d9af89c920/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/subscription-token-fabric/3d319dfc-3e44-4b0a-9016-52d9af89c920/index.html

### Keywords for Search

`vulnerability`

