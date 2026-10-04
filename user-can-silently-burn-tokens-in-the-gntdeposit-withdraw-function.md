---
# Core Classification
protocol: Golem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17017
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf
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
finders_count: 5
finders:
  - Gustavo Grieco
  - 2018: April 5
  - 2018: Initial report delivered Retest report delivered
  - Changelog March 23
  - Chris Evans
---

## Vulnerability Title

User can silently burn tokens in the GNTDeposit withdraw function

### Overview


This bug report is about access controls in the GNTDeposit contract. It states that normal users can use the withdraw function to transfer tokens to a special address, 0xdeadbeef, which effectively allows tokens to be burned without firing a Burn event. The exploit scenario explains how Bob, a malicious third party, can use this bug to destabilize the Golem network by burning a large amount of tokens to cause an internal inconsistency between the amount of tokens in circulation and tracked token supply count. The recommendation suggests implementing the recommended fix in TOB-Golem-08 to prevent regular users from being able to burn. Additionally, it is suggested that the edge case of withdrawing deposits to an account that has not yet been registered via the gate proxy should be handled in tests when adding additional functionality.

### Original Finding Content

## Type: Access Controls  
**Target:** GNTDeposit  

**Difficulty:** Medium  

## Description  
Only the Concent user should be able to burn tokens, but normal users can work around this restriction using the `withdraw` function to transfer tokens to the special address `0xdeadbeef`. This effectively allows tokens to be burned without firing a Burn event.  

```solidity
function withdraw(address _to) onlyUnlocked external {
    var _amount = balances[msg.sender];
    balances[msg.sender] = 0;
    locked_until[msg.sender] = 0;
    require(token.transfer(_to, _amount));
    Withdraw(msg.sender, _to, _amount);
}
```

**Figure 6:** The `withdraw` function allows the transfer/burn of tokens to `0xdeadbeef` by allowing any address as a parameter.  

## Exploit Scenario  
Bob is a malicious third party intent on destabilizing the Golem network. He burns a significant amount of tokens in the GNTDeposit contract to cause an internal inconsistency between the amount of tokens in circulation and the tracked token supply count. He can use this discrepancy either to manipulate the economics of additional token minting or to cause an invariant failure in token supply conditions for a contract migration.  

## Recommendation  
Implementing the recommended fix in TOB-Golem-08 will prevent regular users from being able to burn since the 0 address will be reverted by the token transfer. Since it is possible (and valid) to withdraw a deposit to an account that has not yet been registered via the gate proxy, ensure that this edge case is handled appropriately in tests when adding additional functionality.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Golem |
| Report Date | N/A |
| Finders | Gustavo Grieco, 2018: April 5, 2018: Initial report delivered Retest report delivered, Changelog March 23, Chris Evans |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/golem.pdf

### Keywords for Search

`vulnerability`

