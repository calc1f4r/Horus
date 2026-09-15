---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25212
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/22

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
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] Anyone can set the `baseRatePerYear` after the `updateFrequency` has passed

### Overview


A bug was discovered in the `updateBaseRate()` function of the Plex Engineer's Lending Market code. This public function lacks access control, meaning anyone can set the variable `baseRatePerYear` once the block delta has surpassed the `updateFrequency` variable. This could have negative effects on the borrow and supply rates used in the protocol. The `updateFrequency` is set to 24 hours, so this vulnerability is available every day. The admin can fix the `baseRatePerYear` by calling the admin-only `_setBaseRatePerYear()` function, but this does not set the `lastUpdateBlock` so users can still change the rate back after the 24 hours waiting period.

The severity of this bug was deemed high by Alex the Entreprenerd, due to the potential for economic exploits and bricking of integrating contracts. The recommended mitigation steps are to delete the function or add access control for only trusted parties.

### Original Finding Content

_Submitted by 0xDjango, also found by 0x52, Chom, csanuragjain, JMukesh, k, oyc&#95;109, Picodes, Soosh, and WatchPug_

<https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/NoteInterest.sol#L118-L129>

The `updateBaseRate()` function is public and lacks access control, so anyone can set the critical variable `baseRatePerYear` once the block delta has surpassed the `updateFrequency` variable. This will have negative effects on the borrow and supply rates used anywhere else in the protocol.

The updateFrequency is explained to default to 24 hours per the comments, so this vulnerability will be available every day. Important to note, the admin can fix the `baseRatePerYear` by calling the admin-only `_setBaseRatePerYear()` function. However, calling this function does not set the `lastUpdateBlock` so users will still be able to change the rate back after the 24 hours waiting period from the previous change.

### Proof of Concept

        function updateBaseRate(uint newBaseRatePerYear) public {
            // check the current block number
            uint blockNumber = block.number;
            uint deltaBlocks = blockNumber.sub(lastUpdateBlock);


            if (deltaBlocks > updateFrequency) {
                // pass in a base rate per year
                baseRatePerYear = newBaseRatePerYear;
                lastUpdateBlock = blockNumber;
                emit NewInterestParams(baseRatePerYear);
            }
        }

### Recommended Mitigation Steps

I have trouble understanding the intention of this function. It appears that the rate should only be able to be set by the admin, so the `_setBaseRatePerYear()` function seems sufficient. Otherwise, add access control for only trusted parties.

**[tkkwon1998 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-findings/issues/22)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/22#issuecomment-1205570803):**
 > The warden has shown how, due to probably an oversight, a core function that has impact in determining the yearly interest rate was left open for anyone to change once every 24 hrs.
> 
> Because the impact is:
> - Potential bricking of integrating contracts
> - Economic exploits
> 
> And anyone can perform it
> 
> I believe that High Severity is appropriate.
> 
> Mitigation requires either deleting the function or adding access control.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/22
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

