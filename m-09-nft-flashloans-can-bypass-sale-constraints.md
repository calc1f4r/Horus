---
# Core Classification
protocol: Boot Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 976
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-boot-finance-contest
source_link: https://code4rena.com/reports/2021-11-bootfinance
github_link: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/276

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
  - dexes
  - cdp
  - services
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - pauliax
---

## Vulnerability Title

[M-09] NFT flashloans can bypass sale constraints

### Overview


This bug report is about a vulnerability in the public sale of a token that allows anyone to bypass the constraint that only NFT holders can access the sale. This is done by using flash loans, which allow users to borrow the NFT, participate in the sale, and then return the NFT in one transaction. This can be done with only one NFT, which can be flashloaned again and again to give access to the sale for everyone. The bug report suggests that the most elegant solution for this problem is unclear, but some potential solutions include transferring and locking the NFT for at least one block, taking a snapshot of user balances so the same NFT can only be used by one address, or checking that the caller is an EOA.

### Original Finding Content

## Handle

pauliax


## Vulnerability details

## Impact
Public sale has a constraint that for the first 4 weeks only NFT holders can access the sale:
  if (currentEra < firstPublicEra) {
    require(nft.balanceOf(msg.sender) > 0, "You need NFT to participate in the sale.");
  }

However, this check can be easily bypassed with the help of flash loans. You can borrow the NFT, participate in the sale and then return this NFT in one transaction. It takes only 1 NFT that could be flashloaned again and again to give access to the sale for everyone (burnEtherForMember).

## Recommended Mitigation Steps
I am not sure what could be the most elegant solution to this problem. You may consider transferring and locking this NFT for at least 1 block but then the user will need to do an extra tx to retrieve it back. You may consider taking a snapshot of user balances so the same NFT can be used by one address only but then this NFT will lose its extra benefit of selling it during the pre-sale when it acts as a pre-sale token. You may consider checking that the caller is EOA but again there are ways to bypass that too.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Boot Finance |
| Report Date | N/A |
| Finders | pauliax |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-bootfinance
- **GitHub**: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/276
- **Contest**: https://code4rena.com/contests/2021-11-boot-finance-contest

### Keywords for Search

`vulnerability`

