---
# Core Classification
protocol: Art Gobblers
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25402
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-artgobblers
source_link: https://code4rena.com/reports/2022-09-artgobblers
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[01]  Don't roll your own crypto

### Overview

See description below for full details.

### Original Finding Content

The general advice when it comes to cryptography is [don't roll your own crypto](https://security.stackexchange.com/a/18198). The Chainlink VRF best practices page says that in order to get multiple values from a single random value, one should [hash a counter along with the random value](https://docs.chain.link/docs/vrf/v1/best-practices/#getting-multiple-random-numbers). This project does not follow that guidance, and instead recursively hashes previous hashes. Logically, if you have a source of entropy, then truncate, and hash again, over and over, you're going to lose entropy if there's a weakness in the hashing function, and every hashing function will eventually be found to have a weakness. Unless there is a very good reason not to, the code should follow the best practice Chainlink outlines. Furthermore, the current scheme wastes gas updating the random seed in every function call, as is outlined in my separate gas report.

*There is 1 instance of this issue:*
```solidity
File: /src/ArtGobblers.sol

664                  // Update the random seed to choose a new distance for the next iteration.
665                  // It is critical that we cast to uint64 here, as otherwise the random seed
666                  // set after calling revealGobblers(1) thrice would differ from the seed set
667                  // after calling revealGobblers(3) a single time. This would enable an attacker
668                  // to choose from a number of different seeds and use whichever is most favorable.
669                  // Equivalent to randomSeed = uint64(uint256(keccak256(abi.encodePacked(randomSeed))))
670                  assembly {
671                      mstore(0, randomSeed) // Store the random seed in scratch space.
672  
673                      // Moduloing by 1 << 64 (2 ** 64) is equivalent to a uint64 cast.
674                      randomSeed := mod(keccak256(0, 32), shl(64, 1))
675                  }
676              }
677  
678              // Update all relevant reveal state.
679:             gobblerRevealsData.randomSeed = uint64(randomSeed);

```
https://github.com/code-423n4/2022-09-artgobblers/blob/d2087c5a8a6a4f1b9784520e7fe75afa3a9cbdbe/src/ArtGobblers.sol#L664-L679



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Art Gobblers |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-artgobblers
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-09-artgobblers

### Keywords for Search

`vulnerability`

