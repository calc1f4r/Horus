---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: pegged

# Attack Vector Details
attack_type: pegged
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5924
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/164

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - pegged

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Trust
  - ladboy233
---

## Vulnerability Title

[M-16] dETH / ETH / LPTokenETH can become depegged due to ETH 2.0 reward slashing

### Overview


This bug report concerns the GiantSavETHVaultPool.sol code, which is a part of the liquid-staking contracts. The vulnerability has to do with ETH 2.0 reward slashing, which could cause dETH, ETH, and LPTokenETH to become depegged. The proof of concept is based on the information given in the documentation, which states that users can pool up to 24 ETH and dETH can be redeemed after staking. The main risk in ETH 2.0 POS staking is the slashing penalty, which could cause the ETH to not be pegged and the validator to not maintain a minimum 32 ETH staking balance. Manual review was used to identify the vulnerability. 

The recommended mitigation steps include adding a mechanism to ensure that dETH is pegged via burning if the ETH is slashed. Additionally, the protocol should consider who is responsible for adding ETH to the staking balance or withdrawing the ETH and distributing the funds if the minimum 32 ETH staking balance is not maintained.

### Original Finding Content


I want to quote the info from the doc:

> SavETH Vault - users can pool up to `24 ETH` where protected staking ensures no-loss. dETH can be redeemed after staking

and

> Allocate savETH <> dETH to `savETH Vault` (24 dETH)

However, the main risk in ETH 2.0 POS staking is the slashing penalty, in that case the ETH will not be pegged and the validator cannot maintain a minimum 32 ETH staking balance.

<https://cryptobriefing.com/ethereum-2-0-validators-slashed-staking-pool-error/>

### Recommended Mitigation Steps

We recommand the protocol to add mechanism to ensure the dETH is pegged via burning if case the ETH got slashed.

And consider when the node do not maintain a minmum 32 ETH staking balance, who is in charge of adding the ETH balance to increase the staking balance or withdraw the ETH and distribute the fund.

**Please note: the following comment occurred after judging and awarding were finalized.**

**[vince0656 (Stakehouse) disputed and commented](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/164#issuecomment-1384355141):**
> There is no peg associated with dETH. Users can redeem underlying staked ETH by rage quitting Stakehouse protocol. This is taken care of by the Stakehouse protocol through SLOT (which protects) dETH due to redemption rate mechanics and further special exit penalty. Please see audit reports for Stakehouse:<br>
> Audit report 1: https://github.com/runtimeverification/publications/blob/main/reports/smart-contracts/Blockswap_Stakehouse.pdf<br>
> Audit report 2: https://github.com/runtimeverification/publications/blob/main/reports/smart-contracts/Blockswap_Stakehouse_2nd_Audit.pdf<br>



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | Trust, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/164
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Pegged`

