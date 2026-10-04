---
# Core Classification
protocol: Joyn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1756
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-joyn-contest
source_link: https://code4rena.com/reports/2022-03-joyn
github_link: https://github.com/code-423n4/2022-03-joyn-findings/issues/9

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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - minhquanym
  - leastwood
  - Dravee
  - Ruhum
  - 0xDjango
---

## Vulnerability Title

[H-05] Centralisation RIsk: Owner Of `RoyaltyVault` Can Take All Funds

### Overview


A bug was found in the code of the RoyaltyVault contract, which allows the owner to set the platform fee to any arbitrary value, including 100%. This would result in the owner being able to steal the entire contract balance and any future balances, avoiding the splitter contract.

To mitigate this issue, the code should be amended to include a maximum value for the platform fee, such as 5%, and to call the sendToSplitter() function before adjusting the platform fee. This would only allow the owner to change the fee for future values, excluding the current contract balance. The sendToSplitter() function should also be made public rather than external.

### Original Finding Content

_Submitted by kirk-baird, also found by 0xDjango, defsec, Dravee, hubble, hyh, leastwood, minhquanym, Ruhum, TomFrenchBlockchain, and WatchPug_

The owner of `RoyaltyVault` can set `_platformFee` to any arbitrary value (e.g. 100% = 10000) and that share of the contracts balance and future balances will be set to the `platformFeeRecipient` (which is in the owners control) rather than the splitter contract.

As a result the owner can steal the entire contract balance and any future balances avoiding the splitter.

### Proof of Concept

        function setPlatformFee(uint256 _platformFee) external override onlyOwner {
            platformFee = _platformFee;
            emit NewRoyaltyVaultPlatformFee(_platformFee);
        }

### Recommended Mitigation Steps

This issue may be mitigated by add a maximum value for the `_platformFee` say 5% (or some reasonable value based on the needs of the platform).

Also consider calling `sendToSplitter()` before adjusting the `platformFee`. This will only allow the owner to change the fee for future value excluding the current contract balance.

Consider the following code.

        function setPlatformFee(uint256 _platformFee) external override onlyOwner {
            require(_platformFee < MAX_FEE);
            sendToSplitter(); // @audit this will need to be public rather than external
            platformFee = _platformFee;
            emit NewRoyaltyVaultPlatformFee(_platformFee);
        }


**[sofianeOuafir (Joyn) confirmed and commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/9#issuecomment-1099594175):**
 > This is an issue and we intend to fix it. The recommended mitigation looks good and will be considered.
> 
> We also agree that this is a med risk as this can currently only be done by the contract owner which is us at Joyn

**[deluca-mike (judge) commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/9#issuecomment-1105957959):**
 > Instead of having to come up with a "reasonable" `MAX_FEE`, consider instead just preventing the fee from ever being raised, and only allowing it to be lowered.

**[deluca-mike (judge) increased severity to High and commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/9#issuecomment-1105964175):**
 > While I was originally leaning Medium Risk, after taking the arguments made by the duplicate issues into account, I am now leaning High Risk. The rationale is that, a DOS of `sendToSplitter` via a high `platformFee` not only harms stakeholders of the `RoyaltyVault` that would get the remainder of the balance, split, but may also prevent all NFT transfers if `sendToSplitter` is hooked into as part of all token transfer, via royalty payments. A malicious or disgruntled `RoyaltyVault` owner can hold all the NFTs hostage that call `sendToSplitter` atomically on transfers.
> 
> So there are 2 issues that need to be solved here:
> - protect NFT holders by ensuring `platformFee` (or any other values) cannot be set to a value that would cause `sendToSplitter` to fail (`splitterShare = 0` or `platformShare > balanceOfVault`), or don't have `sendToSplitter` be called on NFT transfers
> - protect royalty split recipients by putting an arbitrary max to the fee, or only allowing the fee to be reduced



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Joyn |
| Report Date | N/A |
| Finders | minhquanym, leastwood, Dravee, Ruhum, 0xDjango, WatchPug, TomFrenchBlockchain, kirk-baird, hyh, hubble, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-joyn
- **GitHub**: https://github.com/code-423n4/2022-03-joyn-findings/issues/9
- **Contest**: https://code4rena.com/contests/2022-03-joyn-contest

### Keywords for Search

`vulnerability`

