---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: erc20

# Attack Vector Details
attack_type: erc20
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3559
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/19
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-sense-judging/issues/48

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - erc20
  - allowance

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - supernova
  - 8olidity
  - pashov
  - 0x52
  - minhquanym
---

## Vulnerability Title

M-1: Anyone can spend on behalf of roller periphery

### Overview


This bug report is about the approve() function in the RollerPeriphery contract. This function allows anyone to spend ERC20 tokens owned by the contract, leading to a potential loss of funds. The code snippet provided shows that the approve call does not have any access control, meaning that any user can call the approve call and transfer the tokens from the contract as a spender. The bug was found by 8olidity, 0x52, supernova, ctf\_sec, pashov, cryptphi, minhquanym and was confirmed by manual review. It was suggested to add access control to the approve call, so that only the RollerFactory can call it. Finally, it was decided to group all the issues as medium as they point out the same flaw with different impacts.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-sense-judging/issues/48 

## Found by 
8olidity, 0x52, supernova, ctf\_sec, pashov, cryptphi, minhquanym

## Summary
The approve() function in RollerPeriphery contract allows anyone to spend ERC20 token owned by the contract

## Vulnerability Detail
RollerPeriphery.approve() does not have any access control, this allows any user to be able to call the approve call which would make an ERC20 approve call to the token inputed, and allowing the 'to' address to spend. In the cases where RollerPeriphery owns some ERC20 tokens. The user will be able to transfer the tokens from the contract as a spender.

## Impact
Loss of funds

## Code Snippet
https://github.com/sherlock-audit/2022-11-sense/blob/main/contracts/src/RollerPeriphery.sol#L100-L102

```solidity
function approve(ERC20 token, address to, uint256 amount) public payable {
        token.safeApprove(to, amount);
    }
```

ERC20 approve call is:
```solidity
function approve(address spender, uint256 amount) public virtual returns (bool) {
        allowance[msg.sender][spender] = amount;

        emit Approval(msg.sender, spender, amount);

        return true;
    }
```

## Tool used
Manual Review

## Recommendation
There should be some access control, according to the provided contracts, this function is called by RollerFactory, this can be the only address allowed to call the RollerPeriphery.approve() function.

## Discussion

**jparklev**

We don't expect that the Periphery will ever hold onto funds of its own, so this is acceptable behavior to us. However, the DOS version of this ticket #46 might be valid as a `medium`

**Evert0x**

Grouping all as medium as they point out the same flaw with different impacts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Sense |
| Report Date | N/A |
| Finders | supernova, 8olidity, pashov, 0x52, minhquanym, cryptphi, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-sense-judging/issues/48
- **Contest**: https://app.sherlock.xyz/audits/contests/19

### Keywords for Search

`ERC20, Allowance`

