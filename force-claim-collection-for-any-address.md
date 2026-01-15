---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6803
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Denis Milicevic
  - Gerard Persoon
---

## Vulnerability Title

Force Claim Collection For Any Address

### Overview


A bug was reported in the Divider.sol and Claim.sol contracts. In this scenario, an actor did a transferFrom transaction on the Claim token contract with a specific from and an amount of 0 tokens. This transaction will succeed in the ERC20 contract as allowance == 0 and amount <= allowance. Then collect() inDivider.sol will be called with uBalTransfer == 0. The _collect() function will be called where uBal and uBalTransfer are set to uBal (which is the balance of the from). This scenario triggers the claim collection from the from, which the from might not want to do at that point in time. 

The bug was likely created to support the calling of collect() in contract Claim.sol, which has a function collect() that returns the Divider.sol contract. 

The recommendation is to differentiate between the two calls from the Claim.sol contract, transferFrom() and collect(), and not trigger a collect() from an empty transferFrom(). The bug has been fixed in #168 and acknowledged.

### Original Finding Content

## Medium Risk Report

**Severity:** Medium Risk  
**Context:** `Divider.sol#L331-398`, `Claim.sol#L37-44`

## Situation
In this scenario, assume an actor performs a `transferFrom` transaction on the Claim token contract with a specific `from` address and an amount of 0 tokens. This transaction will succeed in the ERC20 contract as `allowance == 0` and `amount <= allowance`. Then, `collect()` in `Divider.sol` will be called with `uBalTransfer == 0`. 

The `_collect()` function will be invoked where `uBal` and `uBalTransfer` are set to `uBal` (which is the balance of the `from`). This scenario triggers the claim collection from the `from`. The `from` might not want to do the claim collection at that point in time. 

The claim itself will go to the `from`, so nothing is lost there, but the control over timing could be an issue.

```solidity
contract Claim is Token {
    ...
    function transferFrom(...) public override returns (bool) {
        Divider(divider).collect(from, adapter, maturity, value, to);
        return super.transferFrom(from, to, value); // No revert on
        super.transferFrom(from, to, 0); // ,!
    }
}
```

```solidity
contract Divider is Trust, ReentrancyGuard, Pausable {
    ...
    function collect(address usr, address adapter, uint256 maturity, uint256 uBalTransfer, // uBalTransfer == 0 ,!
        address to) external nonReentrant onlyClaim(adapter, maturity)
        whenNotPaused returns (uint256 collected) { 
            uint256 uBal = Claim(msg.sender).balanceOf(usr);
            return _collect(usr, adapter, maturity, uBal, uBalTransfer > 0 ? uBalTransfer : uBal, to); //_collect is called with uBal as second last parameter,!
    } 
}
```

This construction is likely created to support the calling of `collect()` in the `Claim.sol` contract:

```solidity
function collect() external returns (uint256 _collected) {
    return Divider(divider).collect(msg.sender, adapter, maturity, 0, address(0)); // ,!
}
```

## Recommendation
Differentiate between these two calls from the `Claim.sol` contract: `transferFrom()` and `collect()`, and do not trigger a `collect()` from an empty `transferFrom()`.

**Sense:** Fixed in #168.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sense |
| Report Date | N/A |
| Finders | Max Goodman, Denis Milicevic, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sense-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

