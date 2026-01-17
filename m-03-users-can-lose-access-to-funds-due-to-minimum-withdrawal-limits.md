---
# Core Classification
protocol: Ondo Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32010
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-ondo-finance
source_link: https://code4rena.com/reports/2024-03-ondo-finance
github_link: https://github.com/code-423n4/2024-03-ondo-finance-findings/issues/142

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
  - leveraged_farming
  - rwa
  - services
  - cdp
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - carrotsmuggler
  - radev\_sw
  - dvrkzy
  - 0xmystery
  - Breeje
---

## Vulnerability Title

[M-03] Users can lose access to funds due to minimum withdrawal limits

### Overview


This bug report is about a contract called `InstantManager` that limits the minimum amount of deposits and withdrawals for users. The issue is that the minimum withdrawal limit can cause users to lose access to part of their funds. For example, if a user deposits 100k `USDC` tokens and later withdraws 60k `USDC` tokens, they will only have 40k `USDC` tokens left in their account and cannot withdraw them because it falls below the minimum limit of 50k `USDC` tokens. The only option for the user is to deposit an additional 100k `USDC` tokens and then withdraw the full 140k `USDC` amount, incurring extra fees. The recommended solution is to allow users to withdraw all their funds, even if it falls below the minimum limit. However, the team behind the contract has disputed this solution and will not be implementing it. 

### Original Finding Content


The `InstantManager` contract restricts deposits and withdrawals to certain minimum amounts. Users can deposit a minimum of 100k `USDC` tokens, and withdraw a minimum of 50k `USDC` tokens.

The issue is that the minimum withdrawal limit can lead to users losing access to part of their funds. Say a user deposits 100k `USDC` tokens and then later withdraws 60k `USDC` tokens. Now, the user only has 40k `USDC` worth holdings in their account, and cannot withdraw the full amount. This is because it falls below the minimum withdrawal limit of 50k `USDC` tokens. The user is now stuck with 40k `USDC` tokens in their account, and cannot withdraw them.

The only option the user has is to deposit 100k `USDC` more, and then withdraw the whole 140k `USDC` amount. This will incur fees on the extra 100k `USDC` the user brings as well. Thus this is a Medium severity issue.

### Proof of Concept

The scenario can be recreated in the following steps:

1. User ALICE deposits 100k `USDC` tokens.
2. User ALICE withdraws 60k `USDC` tokens.
3. User ALICE tries to withdraw 40k `USDC` tokens. The contract reverts, as the amount is below the minimum withdrawal limit of 50k `USDC` tokens.

### Recommended Mitigation Steps

Allow users to remove all their funds from the contract even if it is below the minimum limit. Since the protocol now uses a more liquid system such as the `BUIDL` token, this should be possible and should not affect the protocol's functioning.

**[3docSec (judge) commented](https://github.com/code-423n4/2024-03-ondo-finance-findings/issues/142#issuecomment-2044819320):**
 > I acknowledge this behavior is a design decision. However, I would keep this as a valid Medium for an audit report:
> - There is an availability impact for users, in a condition that they did not necessarily have to purposely create for themselves.
> - Users can decide to still withdraw for a loss in fees "for minting more to redeem all".
> - The report highlights what I find to be a very reasonable mitigation - which could be the behavior users reasonably expect:
> 
> > Allow users to remove all their funds from the contract even if it is below the minimum limit.
> 
> This mitigation seems feasible and difficult to exploit for systematic, abusive bypasses of `minimumRedemptionAmount`, because both `OUSG` and `rOUSG` have a KYC requirement on token holders.

**[cameronclifton (Ondo) disputed and commented](https://github.com/code-423n4/2024-03-ondo-finance-findings/issues/142#issuecomment-2073178615):**
 > We will not be removing minimum redemption requirement from the smart contract as there are other means in which users can redeem OUSG or rOUSG tokens from Ondo Finance.

*Note: For full discussion, see [here](https://github.com/code-423n4/2024-03-ondo-finance-findings/issues/142).*

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ondo Finance |
| Report Date | N/A |
| Finders | carrotsmuggler, radev\_sw, dvrkzy, 0xmystery, Breeje, 0xCiphky |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-ondo-finance
- **GitHub**: https://github.com/code-423n4/2024-03-ondo-finance-findings/issues/142
- **Contest**: https://code4rena.com/reports/2024-03-ondo-finance

### Keywords for Search

`vulnerability`

