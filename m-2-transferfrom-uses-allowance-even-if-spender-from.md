---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6704
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/51
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-surge-judging/issues/214

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-2: transferFrom uses allowance even if spender == from

### Overview


This bug report is about a flaw in the Pool#transferFrom method of the Surge Protocol. The issue is that the method attempts to use allowance even when the spender is the same as the from address, which breaks compatibility with a large number of protocols that only use the transferFrom method. This difference will likely result in tokens becoming stranded across different protocols, making them unusable. The code snippet associated with this bug can be found at https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L284-L293. The tool used to identify this issue was the Solidity YouTube Tutorial. The recommendation is to only use allowance when spender != from.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-surge-judging/issues/214 

## Found by 
0x52

## Summary

Pool#transferFrom attempts to use allowance even when spender = from. This breaks compatibility with a large number of protocol who opt to use the transferFrom method all the time (pull only) instead of using both transfer and transferFrom (push and pull). The ERC20 standard only does an allowance check when spender != from. The result of this difference will likely result in tokens becoming irreversibly stranded across different protocols.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L284-L293

The trasnferFrom method shown above always uses allowance even if spender = from.

## Impact

Token won't be compatible with some protocols and will end up stranded

## Code Snippet

https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L284-L293

## Tool used

[Solidity YouTube Tutorial](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## Recommendation

Only use allowance when spender != from:

        require(to != address(0), "Pool: to cannot be address 0");
    +   if (from != msg.sender) {
    +       allowance[from][msg.sender] -= amount;
    +   }
        balanceOf[from] -= amount;

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Surge |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-surge-judging/issues/214
- **Contest**: https://app.sherlock.xyz/audits/contests/51

### Keywords for Search

`vulnerability`

