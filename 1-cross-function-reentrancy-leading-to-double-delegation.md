---
# Core Classification
protocol: 1Inch
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53456
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2022-11-04-1inch.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

1. Cross-function reentrancy leading to double delegation

### Overview


This bug report describes a critical issue in the ERC20Pods.sol contract, specifically in lines 116-151. The function `_beforeTokenTransfer` is used to process delegation transfers for different pods. The code checks if both the "from" and "to" addresses share the same pod, and if so, transfers the delegation from one to the other. However, there is a vulnerability that allows a malicious actor to abuse this function and mint valid delegation tokens for themselves. This is possible if the "from" address is a fake pod contract and the "to" address only has a valid pod. The attacker can re-enter the function and change the _pods mapping, resulting in a double mint of delegation tokens for the "to" address. This issue has been fixed by reconstructing the logic in the _afterTokenTransfer hook and implementing reentrancy locks. 

### Original Finding Content

**Severity:** Critical

**Path:** ERC20Pods.sol#L116-L151

**Description:** 

In the function `_beforeTokenTransfer` that is being overloaded to process
the delegations transfers for various pods, user pods are being read from
`_pods` mapping and then the code checks whether the “`from`” and “`to`”
addresses share or not the pods, the logic can be described as:
1. When some pod is shared by both parties – call
`pod.updateBalances(from,to,amount)` effectively transferring
delegation from → to
2. Pod is used only by “`from`” – burn the delegation for “`from`” by calling
`pod.updateBalances(from, 0, amount)`
3. Pod is delegated only by “`to`” – mint the delegation for “`to`” by calling
`pod.updateBalances(0,to,amount)`

The assumption here is that user pod arrays cannot be changed during the
call, although in the case when “`from`” is by itself a fake pod contract and
“`to`” has only the valid pod; “`from`” can abuse the updateBalances call in
step 2 to reenter to call `ERC20Pods.addPod()` function with parameter
“`pod`” set as the valid pod, thus changing the _pods mapping and minting
itself valid delegation tokens, after the calls ends the _beforeTokenTransfer
hook will continue processing the old array of pods, thus effecting double
mint of delegation to “`to`” in step 3.
By the end of the attack both “`from`” and “`to`” will have valid delegation topic
tokens, although “`to`” must have been the only beneficiary of the
delegation.

```

function _beforeTokenTransfer(address from, address to, uint256 amount) internal override virtual {
       super._beforeTokenTransfer(from, to, amount);
       if (amount > 0 && from != to) {
           address[] memory a = _pods[from].items.get();
           address[] memory b = _pods[to].items.get();
           for (uint256 i = 0; i < a.length; i++) {
               address pod = a[i];
               uint256 j;
               for (j = 0; j < b.length; j++) {
                   if (pod == b[j]) {
                       // Both parties are participating of the same Pod
                       _updateBalances(pod, from, to, amount);
                       b[j] = address(0);
                       break;
                   }
               }
               if (j == b.length) {
                   // Sender is participating in a Pod, but receiver is not
                   _updateBalances(pod, from, address(0), amount);
               }
           }
           for (uint256 j = 0; j < b.length; j++) {
               address pod = b[j];
               if (pod != address(0)) {
                   // Receiver is participating in a Pod, but sender is not
                   _updateBalances(pod, address(0), to, amount);
               }
           }
       }
   }
```

**Remediation:**  Consider reconstructing the logic in the
_afterTokenTransfer hook instead, also using reentrancy locks can
be effective for cross-function reentrancy miitgation.

**Status:**  Fixed



- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | 1Inch |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2022-11-04-1inch.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

