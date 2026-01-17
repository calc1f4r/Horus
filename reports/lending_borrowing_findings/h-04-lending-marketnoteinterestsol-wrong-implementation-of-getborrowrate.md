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
solodit_id: 25215
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/166

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

[H-04] `lending-market/NoteInterest.sol` Wrong implementation of `getBorrowRate()`

### Overview


This bug report is about an issue with the `getBorrowRate` function in the `NoteInterest.sol` file of the `lending-market` repository on GitHub. This function is supposed to return the Note/gUSDC TWAP in a given interval, but instead returns a random rate based on the caller's address and `baseRatePerYear`. This means that some lucky addresses pay much lower and some addresses pay much higher rates, which can be gamed and is not recommended for production. The judge commented that the functionality is broken and agreed with a High Severity rating.

### Original Finding Content

_Submitted by WatchPug, also found by 0x1f8b, Chom, and gzeon_

<https://github.com/Plex-Engineer/lending-market/blob/b93e2867a64b420ce6ce317f01c7834a7b6b17ca/contracts/NoteInterest.sol#L92-L101><br>

```solidity
function getBorrowRate(uint cash, uint borrows, uint reserves) public view override returns (uint) {
    // Gets the Note/gUSDC TWAP in a given interval, as a mantissa (scaled by 1e18)
    // uint twapMantissa = getUnderlyingPrice(note);
    uint rand = uint(keccak256(abi.encodePacked(msg.sender))) % 100;
    uint ir = (100 - rand).mul(adjusterCoefficient).add(baseRatePerYear).mul(1e16);
    uint newRatePerYear = ir >= 0 ? ir : 0;
    // convert it to base rate per block
    uint newRatePerBlock = newRatePerYear.div(blocksPerYear);
    return newRatePerBlock;
}
```

The current implementation will return a random rate based on the caller's address and `baseRatePerYear`.

This makes some lucky addresses pay much lower and some addresses pay much higher rates.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/166#issuecomment-1205799947):**
 > The warden has shown how, due to most likely a developer oversight, the unimplemented `getBorrowRate` returns a random value which can easily be gamed (and is not recommended for production).
> 
> Because the contract is in scope, and the functionality is broken, I agree with High Severity.



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
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/166
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

