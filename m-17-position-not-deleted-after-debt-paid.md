---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25833
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/343

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Lotus
  - fs0c
  - obront
---

## Vulnerability Title

[M-17] Position not deleted after debt paid

### Overview


A bug was found in the `_paymentAH` function from the LienToken.sol program. The bug was originally discovered during a Spearbit audit and was resolved, but then re-introduced at a later time. The bug is that the `stack` argument should be storage instead of memory, meaning that the position is not deleted after the debt is paid. Astaria developers have discussed the bug and agree that the first fix should be used again and it would work. The severity of the bug has been decreased to Medium.

### Original Finding Content


In `_paymentAH` function from LienToken.sol, the `stack` argument should be storage instead of memory. This bug was also disclosed in the Spearbit audit of this program and was resolved during here: <https://github.com/AstariaXYZ/astaria-core/pull/201/commits/5a0a86837c0dcf2f6768e8a42aa4215666b57f11>, but was later re-introduced <https://github.com/AstariaXYZ/astaria-core/commit/be9a14d08caafe125c44f6876ebb4f28f06d83d4> here. Marking it as high-severity as it was marked as same in the audit.

### Proof of Concept

```solidity
function _paymentAH(
    LienStorage storage s,
    address token,
    AuctionStack[] memory stack,
    uint256 position,
    uint256 payment,
    address payer
  ) internal returns (uint256) {
    uint256 lienId = stack[position].lienId;
    uint256 end = stack[position].end;
    uint256 owing = stack[position].amountOwed;
    //...[deleted lines to show bug]
    
    delete s.lienMeta[lienId]; //full delete
    delete stack[position]; // <- no effect on storage
    
  }
```

The position here is not deleted after the debt is paid as it is a memory pointer.

### Recommendation

The first fix can be used again and it would work.

**[androolloyd (Astaria) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/343#issuecomment-1403986276):**
 > So digging into this more since this payment flow is designed to run only once, and the state is stored inside the clearing house not the lien token, I'm not sure this matters, the deletion of the auction stack should be handled seperately inside the clearing house for the deposit.

**[SantiagoGregory (Astaria) acknowledged](https://github.com/code-423n4/2023-01-astaria-findings/issues/343)**

**[Picodes (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/343#issuecomment-1435712997):**
 > The description of the impact of the finding is very brief for this issue and its duplicates.
> 
> @androolloyd - the auction stack is in `ClearingHouse`, but the issue still stands as it is not deleted in `ClearingHouse` although it should be, right?

**[androolloyd (Astaria) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/343#issuecomment-1442100489):**
 > > @androolloyd - the auction stack is in `ClearingHouse`, but the issue still stands as it is not deleted in `ClearingHouse` although it should be, right?
> 
> Yes, it should be.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Lotus, fs0c, obront |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/343
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

