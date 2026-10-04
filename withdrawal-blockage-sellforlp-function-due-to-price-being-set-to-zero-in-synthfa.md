---
# Core Classification
protocol: Entangle Trillion
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51362
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/entangle-trillion
source_link: https://www.halborn.com/audits/entangle-labs/entangle-trillion
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Withdrawal blockage sellForLP Function Due to Price Being Set to Zero in SynthFactory Contract

### Overview


The SynthFactory smart contract has a bug that allows the price of a synthetic asset (synth) to be set to zero, resulting in users losing their synths without receiving any LP tokens in return. This can happen if the **setPrice** function is used by the **PRICE\_MANAGER** role to set the price to zero. The **sellForLP** function, which allows users to sell their synths for LP tokens, calculates the LP token amount as zero when the price is set to zero. This can lead to a loss of funds for users. The recommended solution is to implement a validation check in the **setPrice** function to prevent the price from being set to zero. The Entangle team has already fixed this issue by preventing the price setter from setting the price to zero.

### Original Finding Content

##### Description

The **SynthFactory** smart contract contains a critical vulnerability related to the **sellForLP** function. This function is designed to allow users to sell their synthetic assets (synths) for LP (Liquidity Provider) tokens. The price of the synth is fetched from the contract using the **getPrice** function, which is set by the **setPrice** function.  
The vulnerability arises from the fact that the **setPrice** function allows the **PRICE\_MANAGER** role to set the price of a synth to zero. When the price is set to zero, the **sellForLP** function calculates the amount of LP tokens to be received (**lpAmount**) as zero, regardless of the amount of synth being sold. This scenario leads to a situation where users can burn their synths without receiving any LP tokens in return, effectively resulting in a loss of funds.

Users can lose their synths without receiving any LP tokens if the price is maliciously or accidentally set to zero.

  

[[EntangleDexV2.sol#L159](https://github.com/Entangle-Protocol/entangle-lsd-protocol/blob/48e025e4ddf330e8ac710e82114db704a76d2857/contracts/EntangleDexV2.sol#L159)](<https://github.com/Entangle-Protocol/entangle-lsd-protocol/blob/48e025e4ddf330e8ac710e82114db704a76d2857/contracts/EntangleDexV2.sol#L159>)

```
   function sellForLP(uint128 sid, uint256 synthAmount, address recipient) public isPausedSID(sid) onlyLpStakingSid(sid) nonReentrant {
       if (synthAmount == 0) revert EntangleDex__E5();
       synthFactory.burn(sid, synthAmount, msg.sender, 0);
       uint price = synthFactory.getPrice(sid);
       uint lpAmount = (synthAmount * price) / 10 ** 18;
       if (block.chainid == SidLibrary.chainId(sid)) {
           masterSynthChef.withdrawLP(sid, lpAmount, recipient);
       } else {
           emit LPStackingSynthSell(sid, lpAmount, synthAmount, recipient);
           balanceManager.proposeSellForLp(sid, synthAmount, recipient);
       }
   }
```

##### Proof of Concept

![image (8).png](https://halbornmainframe.com/proxy/audits/images/65ca775a4e98381432d558f7)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:C (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:C/Y:N/R:N/S:C)

##### Recommendation

Implement a validation check in the **setPrice** function to ensure that the price cannot be set to zero. Consider setting a reasonable minimum price threshold.

  

**Remediation Plan:** The Entangle team solved the issue by preventing the price setter with "0".

##### Remediation Hash

<https://github.com/Entangle-Protocol/entangle-lsd-protocol/commit/519ab1768dddc4842b09baae55fc0f8a76d98365>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Entangle Trillion |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/entangle-trillion
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/entangle-trillion

### Keywords for Search

`vulnerability`

