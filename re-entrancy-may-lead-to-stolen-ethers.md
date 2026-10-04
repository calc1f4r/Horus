---
# Core Classification
protocol: Parity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17190
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - Andy Ying
  - 2018: June 15
  - Jay Little
  - Josselin Feist
  - 2018: Initial report delivered Added Appendix D with retest results Added additional retest results https://docs.google.com/document/d/1M6lrQWHQLqzLnlwlPNcpAq_ulWTpmpﬁ9D_sbnH2S-c/edit# 1/80
---

## Vulnerability Title

Re-entrancy may lead to stolen ethers

### Overview


This bug report describes a re-entrancy vulnerability found in the Operations contract which allows authorized users to send ethers. A malicious user may be able to send more ethers than expected due to a flaw in the checkProxy function. The checkProxy function is invoked when a transaction is confirmed, and it executes the transaction before deleting it from the proxy list. This allows a malicious transaction destination to confirm the transaction a second time before it is deleted, resulting in the transaction being executed twice and the ethers being sent multiple times.

To exploit this vulnerability, the attacker must have access to an authorized client that is not needed to confirm the transaction. This could be achieved by incorrectly initializing a contract.

The recommendation to fix this vulnerability is to delete the transaction from the proxy prior to execution and to avoid state changes after an external call. The check-effects-interactions pattern should also be applied.

### Original Finding Content

## Data Validation Report

## Type: 
Data Validation

## Target: 
InnerOwnedSet.sol

## Difficulty: 
Low

## Description
The `Operations` contract allows authorized users to send ethers. A re-entrancy vulnerability may allow a malicious user to send more ethers than expected. Once a transaction is confirmed, the `checkProxy` function is invoked (`Operations.sol#L278-L284`):

```solidity
function checkProxy(bytes32 _txid) internal when_proxy_confirmed(_txid) returns (uint txSuccess) {
    var tx = proxy[_txid];
    var success = tx.to.call.value(tx.value).gas(tx.gas)(tx.data);
    TransactionRelayed(_txid, success);
    txSuccess = success ? 2 : 1;
    delete proxy[_txid];
}
```

**Figure 1**: The `checkProxy` implementation

The transaction is executed before it is deleted from the `proxy` list. A malicious transaction destination may be able to confirm the transaction a second time prior to the transaction’s deletion. As a result, the ethers will be sent multiple times.

To exploit this vulnerability, the attacker needs to have access to an authorized client that is not needed to confirm the transaction. It is expected that all the authorized clients are needed to confirm a transaction. However, this assumption can be broken, for example, by incorrectly initializing a contract.

## Exploit Scenario
The number of authorized clients to confirm a transaction is set to two, but three authorized clients are added during initialization. Bob’s smart contract is one of the authorized clients. There is a pending transaction with one ether to Bob’s smart contract. The transaction is executed, and Bob’s smart contract fallback function is triggered. The fallback function confirms the transaction a second time. As a result, the transaction is executed twice, and two ethers are sent instead of one.

## Recommendation
- Delete the transaction from `proxy` prior to execution.
- Avoid state changes after an external call. Apply the `check-effects-interactions` pattern.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Parity |
| Report Date | N/A |
| Finders | Andy Ying, 2018: June 15, Jay Little, Josselin Feist, 2018: Initial report delivered Added Appendix D with retest results Added additional retest results https://docs.google.com/document/d/1M6lrQWHQLqzLnlwlPNcpAq_ulWTpmpﬁ9D_sbnH2S-c/edit# 1/80, 2018: July 6, Changelog February 23 |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/parity.pdf

### Keywords for Search

`vulnerability`

