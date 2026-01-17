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
solodit_id: 24957
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-04-axelar
source_link: https://code4rena.com/reports/2022-04-axelar
github_link: https://github.com/code-423n4/2022-04-axelar-findings/issues/12

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

[M-02] User's funds can get lost when transferring to other chain

### Overview


This bug report submitted by CertoraInc is about the AxelarGateway.sol#L384-L389 code which is used to transfer tokens from one chain to another. The issue is that if the AxelarGateway doesn't have enough tokens, the `_callERC20Token` with the `transfer` function selector will fail and return false, causing the `_mintToken` function to revert and the user will not receive their funds on the destination chain.

Tools used to detect this issue were VS Code and Remix. The recommended mitigation steps are to instead of reverting the transfer, call the `callContractWithToken` with the source chain as the destination chain in order to return the user their funds. Deluca-mike (Axelar) acknowledged the issue but noted that it cannot be solved since it would require cooperation from the validators to sign the mint/transfer refund command for the source gateway. They also noted that well-behaving validators can still sign a refund mint/transfer for the source gateway if they see that a mint/transfer on the destination gateway failed.

### Original Finding Content

_Submitted by CertoraInc_

[AxelarGateway.sol#L384-L389](https://github.com/code-423n4/2022-04-axelar/blob/dee2f2d352e8f20f20027977d511b19bfcca23a3/src/AxelarGateway.sol#L384-L389)<br>

When transferring tokens to other chain, the tokens in the source chain are burned - if they are external they will be transferred to the AxelarGateway, otherwise they will be burned. In the target chain the same amount of tokens will be minted for the user - if it is external it will be transferred to him from the AxelarGateway, otherwise it will be minted to him.<br>
But there is a problem - if the AxelarGateway doesn't have the needed amount of token for some reason, the `_callERC20Token` with the `transfer` function selector will fail and return false, which will make the `_mintToken` function revert. Because it reverted, the user won't get his funds on the destination chain, although he payed the needed amount in the source chain.

### Tools Used

VS Code and Remix

### Recommended Mitigation Steps

Instead of reverting when the transfer is not successful, simply call the `callContractWithToken` with the source chain as the destination chain in order to return the user his funds.

**[deluca-mike (Axelar) acknowledged and commented](https://github.com/code-423n4/2022-04-axelar-findings/issues/12#issuecomment-1098570273):**
 > While true, the only way the destination gateway cannot mint or transfer token, in response to a burn or transferFrom on the source chain, is foul play on the validators' part. Once we assume foul play, then really there is no protection here, since even with the recommended mitigation steps, you'd still need cooperation from the validators to sign the mint/transfer refund command for the source gateway.
> 
> Because of this, while the issue is acknowledged, it's not really something that can be solved.
> 
> Further, well-behaving validators can still sign a refund mint/transfer for the source gateway if they see that a mint/transfer on the destination gateway failed, without needing to do what is suggested in the Recommended Mitigation Steps.



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
- **GitHub**: https://github.com/code-423n4/2022-04-axelar-findings/issues/12
- **Contest**: https://code4rena.com/reports/2022-04-axelar

### Keywords for Search

`vulnerability`

