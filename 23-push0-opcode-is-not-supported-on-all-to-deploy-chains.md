---
# Core Classification
protocol: The Wildcat Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41732
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-wildcat
source_link: https://code4rena.com/reports/2024-08-wildcat
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[23] PUSH0 Opcode is not supported on all to-deploy chains

### Overview

See description below for full details.

### Original Finding Content


### Proof of Concept

Per the readMe protocol is to also deploy on multiple optimistic chains see:<br>
https://github.com/code-423n4/2024-08-wildcat/blob/fe746cc0fbedc4447a981a50e6ba4c95f98b9fe1/README.md#L254

```markdown
| Chains the protocol will be deployed on | Ethereum, Base, Arbitrum, Polygon |
```

Now contracts are being compiled with versions higher than `0.8.20` see https://github.com/code-423n4/2024-08-wildcat/blob/fe746cc0fbedc4447a981a50e6ba4c95f98b9fe1/src/types/TransientBytesArray.sol#L1-L5

```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.8.25;
..snip
```

Issue however is that the PUSH0 opcode is not supported across all these chains.

Note that this version (and every version after 0.8.19) will use the PUSH0 opcode, which is still not supported on some EVM-based chains, for example Arbitrum. Consider using version 0.8.19 so that the same deterministic bytecode can be deployed to all chains. 

### Impact

QA

### Recommended Mitigation Steps

Use a different pragma version.

**[laurenceday (Wildcat) acknowledged and commented](https://github.com/code-423n4/2024-08-wildcat-findings/issues/119#issuecomment-2365291876):**
 > Thank you for the effort involved in putting together this report. There's only one change we'll make here, a docs update based on number 05. The rest is either expected behaviour or things we aren't interested in fixing.
> 
> 1. This is expected behaviour: we don't envisage anyone ever actually creating a market with a 100% reserve ratio, but at the same time it's similarly unlikely that anyone would create one with 90%, so the boundary is somewhat illusory. If someone _did_ do the former, they'd be expected to immediately transfer some assets in upon first deposit to account for protocol fees anyway (indeed, they'd be required to): perhaps if a borrower wanted a vanity wrapped token at 0% APR, for example.
> 
> 2. We're not too fussed about this taking place (it's extremely unlikely that feeRecipient would get blocked by stablecoin issuers/WETH/cbBTC), and if someone created a market for a memecoin that blocked the address, that's just too bad for Wildcat really. One would anticipate that the market wouldn't react well to a token that made a decision like that in any event, so it's not as if the protocol would likely stand to lose much by way of revenue. We want to keep `feeRecipient` immutable, and a pull pattern would need a whitelisted set of addresses anyway that we don't want to have update power for.
> 
> 3. Rebasing tokens are explicitly mentioned in the audit repo and whitepaper for V1 as breaking the underlying interest model, and should not be used as underlying assets (Wildcat is likely to blacklist a few of the most popular ones just to hammer the point home). 
> 
>4. The impact on frequent updating is not nearly as severe as you might imagine - we are well aware of this, however: it is a design choice. (See image [here](https://github.com/user-attachments/assets/8b9363c1-9588-4b4b-8f67-f1d5f0c48772))
> 
> 5. We'll update the docs in time, cheers.
> 
> 6.  It is _extremely_ unlikely that an external protocol would want to integrate the result of a sanctioned escrow account being activated, but fair observation.
> 
> 7. Expected behaviour that we don't wish to fix: the point here is to allow sentinels or borrowers to execute things to keep the withdrawal queue clear. We can't reasonably account for things like wallet upgrades. We _can_ see a lender getting confused and angry that their funds aren't in their wallet because they forgot to execute a queued withdrawal themselves, and it'll just be easier for someone else to sweep things to them.
> 
> 8. Not a concern.
> 
> 9. Not a concern.
> 
> 10. Burning a claim on credit is a mad thing to do (read: we don't expect this to happen, and if it does, good luck to the lender). Adding this check would add unreasonable gas bloat to every single transfer.
> 
> 11. ERC-20s used as underlyings are expected to be well-formed/'standard'. Esoteric tokens such as this aren't a concern of ours.
> 
> 12. We want this in place: it's our observed experience that capped vaults don't have people trying to push right up to the wei, and if they're interested in doing so they should just be using `depositUpTo` instead of `deposit`. Our UI handles this.
> 
> 13. Not expecting this to happen: if it does, the borrower can transfer in from another address using `repay` as needed. More generally, the potential to update the borrower address would be a significant attack vector, and as such we made the early decision to not enable this.
> 
> 14. Market controller factories are deprecated in V2. Even if they weren't, the archcontroller owners would quite simply not be deploying MCFs that were owned by someone else except in the case of a mistake, and any borrower that tried to use them would find that they weren't registered with that new archcontroller address so couldn't deploy anyway.
> 
> 15. This may be precisely what is desired in the event that a borrower is targeted by a hostile Chainalysis oracle, and it's not as if we can distinguish between a 'real' and a 'fake' sanction. Besides, a borrower wouldn't have any market tokens to send into a sentinel escrow contract anyway: they aren't using withdrawals as lenders do.
> 
> 16. Not a concern: fees are read directly into the UI from a lens contract, and even if this happened, a borrower that disagreed would be free to terminate their market as soon as they noticed for minimal 'damage'.
> 
> 17. Expected behaviour - each market is its' own token contract as well, and allowing the 'resetting' of these would be extremely dangerous.
> 
> 18. No response needed.
> 
> 19. No response needed: compilation speed is not a concern of ours for this.
> 
> 20. Dawg, that's eighty years from now. I think we'll be fine. My grandchildren will not be inheriting a Wildcat market.
> 
> 21. Expired credentials are still credentials, and this is used for withdrawal permissions. Unset credentials (i.e. explicitly rescinded) are set to 0. This is expected behaviour.
> 
> 22. Not a concern.
> 
> 23. Not a concern: we'll deploy on chains once PUSH0 is supported.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | The Wildcat Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-wildcat
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-08-wildcat

### Keywords for Search

`vulnerability`

