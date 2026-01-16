---
# Core Classification
protocol: /Reach Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59783
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/reach-protocol/274e391f-ca34-4d87-b76c-0f799573fb89/index.html
source_link: https://certificate.quantstamp.com/full/reach-protocol/274e391f-ca34-4d87-b76c-0f799573fb89/index.html
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
finders_count: 3
finders:
  - Poming Lee
  - Julio Aguilar
  - Mostafa Yassin
---

## Vulnerability Title

Greedy Contract / ERC20 Tokens Will Get Locked in the Contract

### Overview


The client has marked a bug as "Fixed" and provided an explanation. The issue is that the contract is unable to send ERC20 tokens as rewards because a variable called `tokenDistribution` is not set and there is no way to change it. This means that any tokens sent to the contract will be stuck there. A solution could be to add a function to change `tokenDistribution`, but this would negatively impact the user experience. It is recommended to remove the variable and create a new function for claiming ERC20 token rewards to improve the user experience.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `8afbbf4`. The client provided the following explanation:

> There is a new enum "PaymentType" now createMission/claimRewards. will take this PaymentType as input

**Description:** The contract should be able to send either ETH or some ERC20 token when users claim rewards. The decision is based on the value of the state variable `tokenDistribution`. However, said variable remains uninitialized and there is also no setter function for it. This will lead the function `claimRewards()` to always try to send ETH even when it should send some `ERC20` tokens. Therefore, any ERC20 tokens sent to this contract will remain locked forever.

**Recommendation:** One solution could be to add a setter function to the contract to change the value of `tokenDistribution` according to the rewards token type. However, the need to keep switching `tokenDistribution` on and off to allow some users to claim their ETH and others to claim their ERC20 tokens would impact the user experience negatively since they would have to wait until their rewards are claimable. Therefore, consider removing this variable and creating a new function to claim rewards of ERC20 tokens which would increase the friendliness of the user experience.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | /Reach Protocol |
| Report Date | N/A |
| Finders | Poming Lee, Julio Aguilar, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/reach-protocol/274e391f-ca34-4d87-b76c-0f799573fb89/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/reach-protocol/274e391f-ca34-4d87-b76c-0f799573fb89/index.html

### Keywords for Search

`vulnerability`

