---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34494
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 74
finders:
  - jprod15
  - Daniel526
  - neocrao
  - dacian
  - 0xdice91
---

## Vulnerability Title

[H-04] Lender#buyLoan - Malicious user could take over a loan for free without having a pool because of wrong access control

### Overview


The bug report discusses a critical vulnerability in the **`buyLoan`** function of the Lender contract. This vulnerability allows a malicious user to take over a loan without owning the required pool. The bug report suggests implementing an authorization check at the beginning of the function to prevent unauthorized access. This vulnerability can lead to financial losses for legitimate users and lenders within the system. 

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L518-L522">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L518-L522</a>


## **Summary**

The **`buyLoan`** function within the Lender contract displays a critical vulnerability due to improper access controls. This loophole can potentially allow a malicious actor to gain unauthorized control over a loan.

## **Vulnerability Details**

In the `buyLoan` function, we’re buying a loan that has gone to auction. A malicious user can send in the `loanId` to buy and a random `poolId` that passes the requirement checks in the function such as having an `interestRate` lower than the `currentAuctionRate` and that the pool is big enough.

The vulnerability exploit lies in these lines where we’re setting the `msg.sender` as the new lender.

```solidity
// update the loan with the new info
        loans[loanId].lender = msg.sender;
        loans[loanId].interestRate = pools[poolId].interestRate;
        loans[loanId].startTimestamp = block.timestamp;
        loans[loanId].auctionStartTimestamp = type(uint256).max;
        loans[loanId].debt = totalDebt
```

## **Impact**

A malicious user can exploit this oversight to gain unauthorized ownership of a loan despite not being the owner of the specified `poolId`. This not only compromises the security and trustworthiness of the lending protocol but can also lead to significant financial losses for legitimate users and lenders within the system.

## **Tools Used**

Manual Review.

## **Recommendations**

Implement an authorization check at the beginning of the **`buyLoan`** function. This should verify that the caller is the rightful owner of the specified **`poolId`.**

```solidity
if(msg.sender != pool.lender) revert Unauthorized();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | jprod15, Daniel526, neocrao, dacian, 0xdice91, toshii, Mlome, lealCodes, sobieski, CircleLooper, 0xAsen, JMTT, akalout, qbs, Marzel, B353N, Kral01, 0xsandy, MahdiKarimi, 0x11singh99, sonny2k, jnrlouis, Juntao, 0xhuy0512, serialcoder, Silvermist, tiesstevelink, leasowillow, KupiaSec, VanGrim, amar, Norah, deadrosesxyz, 0xDanielH, Mukund, Aarambh, Cosine, ADM, qckhp, Bernd, Aamir, 0xbepresent, Niki, ElHaj, credence0x, 0xdeth, 0x3b, kutu, nabeel, 0xSCSamurai, 0xlemon, Crunch, dimulski, owade, StErMi, PTolev, 0xl3xx, trtrth, pep7siup, BanditSecurity, pengun, ptsanev, 1nc0gn170, ubermensch, 0xCiphky, Lalanda, rvierdiiev, aak, jonatascm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

