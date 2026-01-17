---
# Core Classification
protocol: Ethos EVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47343
audit_firm: OtterSec
contest_link: https://www.ethosstake.com/
source_link: https://www.ethosstake.com/
github_link: https://github.com/Ethos-Works/ethos

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Robert Chen
  - Woosun Song
---

## Vulnerability Title

Denial Of Slashing

### Overview


This report discusses a vulnerability in the verifyDoubleSigning function, which can be exploited by a malicious operator to evade slashing. This vulnerability is due to the linear complexity of the function, which can be increased indefinitely by repeatedly calling the updateDelegation function. This can result in an unbounded expansion of the delegatedValidators array, causing a denial-of-slashing attack. The report suggests enforcing a reasonable length limit on the array and implementing a public method to clear its contents. However, this mitigation may also introduce another issue where an attacker can block the StakeRegistry from updating the stake by reaching the length limit. The vulnerability has been fixed in the latest update.

### Original Finding Content

## Vulnerability Report: verifyDoubleSigning

`verifyDoubleSigning` is vulnerable to gas griefing attacks, allowing a malicious operator to evade slashing. This vulnerability stems from the linear complexity \( O(N) \) of `verifyDoubleSigning`, where \( N \) denotes the length of the delegators array (`delegatedValidators`). The complexity arises from the loop that iterates over the delegated validators to check for evidence of double-signing. The malicious operator may repeatedly invoke `updateDelegation` with the same operator and consumer chain, thereby increasing the length of the delegators array. As the cost of this operation remains constant, the operator may execute it indefinitely, resulting in an unbounded expansion of the delegators array.

## Code Snippet
> _EthosAVS ServiceManager.sol Solidity_
```solidity
function verifyDoubleSigning(
    address operator,
    DoubleSigningEvidence memory e
) external {
    [...]
    for (uint256 i = 0; i < delegatedValidators.length; i++) {
        [...]
        if (EthosAVSUtils.compareStrings(delegatedValidators[i].validatorPubkey,
                                          e.validatorPubkey) &&
            isDelegationSlashable(delegatedValidators[i].endTimestamp))
        {
            timestampValid = true;
            stake = EthosAVSUtils.maxUint96(stake, delegatedValidators[i].stake);
        }
    }
    [...]
}
```

On the Ethereum mainnet, there is a gas limit per block (currently 30 million). If a transaction exceeds this limit, it will be rejected by the network. By increasing the length of the delegators array beyond what may be processed within the gas limit, the malicious operator effectively performs denial-of-slashing, preventing `verifyDoubleSigning` from completing successfully.

## Remediation
- Enforce a reasonable length limit (e.g., 100) on the delegators array.
- Implement a public method to clear the contents of the delegators array to avoid reaching this limit.

However, this mitigation introduces another issue: an attacker may block the StakeRegistry from updating the stake in an operator’s delegations by deliberately reaching the length limit. As a follow-up, the team decided to store the percentage of the delegation instead of the actual Ether amount.

## Patch
- Fixed in commit `6795911`.
- Follow-up fix implemented in commit `6120463`.

© 2024 Otter Audits LLC. All Rights Reserved. 6/11  
Ethos Stake Audit 04 — Vulnerabilities  
© 2024 Otter Audits LLC. All Rights Reserved. 7/11

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Ethos EVM |
| Report Date | N/A |
| Finders | Robert Chen, Woosun Song |

### Source Links

- **Source**: https://www.ethosstake.com/
- **GitHub**: https://github.com/Ethos-Works/ethos
- **Contest**: https://www.ethosstake.com/

### Keywords for Search

`vulnerability`

