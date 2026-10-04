---
# Core Classification
protocol: SecondSwap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49539
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-secondswap
source_link: https://code4rena.com/reports/2024-12-secondswap
github_link: https://code4rena.com/audits/2024-12-secondswap/submissions/F-5

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
finders_count: 8
finders:
  - 0xStalin
  - Taiger
  - 0xAkira
  - 0xrex
  - Bryan\_Conquer
---

## Vulnerability Title

[M-03] Missing option to remove tokens from the `isTokenSupport` mapping can result in huge financial loss for users and the protocol

### Overview


This bug report discusses an issue with the SecondSwap Marketplace contract code. The problem is that there is no way for the admin to remove a token from the list of supported currencies, which can lead to significant financial loss for users and the protocol. This is because even if a whitelisted stable coin loses its peg and becomes worthless, users can still list their tokens for sale using this currency, resulting in loss for both the seller and the protocol. The recommended solution is to add an option for the admin to remove currencies from the whitelist and to check if the currency used for a listing is still supported before executing a sale. This issue has been deemed as a medium risk by the validator and the SecondSwap team has stated that they will include a fix for it in their initial design.

### Original Finding Content



<https://github.com/code-423n4/2024-12-secondswap/blob/214849c3517eb26b31fe194bceae65cb0f52d2c0/contracts/SecondSwap_Marketplace.sol# L205-L218>

Because there is no option for the admin to remove a token from the `isTokenSupport` mapping, a depeg of a whitelisted token can lead to significant financial loss for users and the protocol.

### Proof of Concept

When selling a vesting on the marketplace, users need to specify the currency the buyer should pay for the sold tokens. To ensure the safety of the users and the safety of the protocol’s revenue, only currencies whitelisted in the `isTokenSupport` mapping can be used and according to the protocol only stable coins will be whitelisted. For a token to be whitelisted the function `addCoin` needs to be called by the admin.

The issue arises from the fact that there is no way to remove a coin from the whitelist once it is on it. This poses a significant risk for the users and the revenue of the protocol in case a whitelisted stable coin loses his peg and becomes worthless. Even though the coin becomes worthless:

* unsuspecting users can still list their vestings using the worthless currency, practically giving away their tokens for free
* all listings using this currency can still be bought, resulting in significant loss for the seller
* the fees for the protocol collected for listings using the depegged currency will also be worthless

This results in significant financial loss for users as well as the protocol.

### Recommended Mitigation Steps

Add an option for the admin to remove currencies from the whitelist. This way, no new listings can be created with a depegged currency. To protect the vestings already listed with the bad currency, make sure to check if the currency used for a listing is still on the whitelist before executing a sale. This way, sellers of the impacted listings are protected from selling their vestings for worthless currency and can delist their listings once they become aware of the depeg.

**[Koolex (judge) commented](https://code4rena.com/audits/2024-12-secondswap/submissions/F-5?commentParent=oqzGF8YKF6F&commentChild=jqRYiA7MBKZ):**

> Validator’s comment:
>
> > The supported tokens are under protocol team’s review, we can expect that most widely used token such as ETH/USDC/USDC to be included as currency token. Though it’s a good idea to have a quit design, QA is proper to this issue.
>
> My view after further evaluation:
> Since all ERC20 tokens are supported, depegged currency risk is still there, even for USDC which actually dropped under 1$ about a year ago. Therefore, at this point, I believe this can be Medium.

**[calvinx (SecondSwap) commented](https://code4rena.com/audits/2024-12-secondswap/submissions/F-5?commentParent=Kpd4tnLcYeF):**

> In our initial design, we will only use liquid stables, i.e. USDT and USDC. In a depeg scenario, we can freeze listing and recommend sellers to remove their listings. We will include a fix.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | SecondSwap |
| Report Date | N/A |
| Finders | 0xStalin, Taiger, 0xAkira, 0xrex, Bryan\_Conquer, BajagaSec, BenRai, zanderbyte |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-secondswap
- **GitHub**: https://code4rena.com/audits/2024-12-secondswap/submissions/F-5
- **Contest**: https://code4rena.com/reports/2024-12-secondswap

### Keywords for Search

`vulnerability`

