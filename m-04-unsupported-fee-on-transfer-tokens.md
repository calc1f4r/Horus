---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24959
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-04-axelar
source_link: https://code4rena.com/reports/2022-04-axelar
github_link: https://github.com/code-423n4/2022-04-axelar-findings/issues/5

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
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] Unsupported fee-on-transfer tokens

### Overview


This bug report is about an issue with the _burnTokenFrom_ function in the AxelarGateway.sol contract. When the tokenAddress is a fee-on-transfer token, the amount of tokens received by the contract will be less than the amount expected. To address this issue, the recommended mitigation step is to calculate the difference of token balance (using balanceOf) before and after the transferFrom. It is noted that in the case of a malicious token contract, it could also lie about the balanceOf. If fee-on-transfer tokens are accepted in the gateway, the recommended mitigation steps might need to be implemented. However, it is not that simple because there is not a link (on-chain) to ensure the amount the gateway burns is equal to the amount the gateway/validators mint elsewhere.

### Original Finding Content

_Submitted by cccz_

When tokenAddress is fee-on-transfer tokens, in the \_burnTokenFrom function, the actual amount of tokens received by the contract will be less than the amount.

### Proof of Concept

[AxelarGateway.sol#L284-L334](https://github.com/code-423n4/2022-04-axelar/blob/main/src/AxelarGateway.sol#L284-L334)<br>

### Recommended Mitigation Steps

Consider getting the received amount by calculating the difference of token balance (using balanceOf) before and after the transferFrom.

**[deluca-mike (Axelar) confirmed and commented](https://github.com/code-423n4/2022-04-axelar-findings/issues/5#issuecomment-1098474999):**
 > Valid for `TokenType.External`, since it is a token implementation that is not ours, and thus could actually transfer us less than expected due to fees.
> 
> Keep in mind that, in the case of a malicious token contract, it could also lie about the `balanceOf`.
> 
> In any case, if and when we wanted to accept fee-on-transfer tokens in the gateway, we _might_ need to implement the recommended mitigation steps; however, it is not that simple because the is not link (on-chain) here that ensure the amount the gateway burns to be equal to the amount the gateway/validators mint elsewhere. Knowing the actual amount burned is not critical to the source gateway, but rather to the validators that will need to create the mint command elsewhere.



***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-axelar
- **GitHub**: https://github.com/code-423n4/2022-04-axelar-findings/issues/5
- **Contest**: https://code4rena.com/reports/2022-04-axelar

### Keywords for Search

`vulnerability`

