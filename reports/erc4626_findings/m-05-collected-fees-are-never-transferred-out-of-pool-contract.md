---
# Core Classification
protocol: Gondi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35224
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/60

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
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - minhquanym
  - bin2chen
  - oakcobalt
---

## Vulnerability Title

[M-05] Collected fees are never transferred out of Pool contract

### Overview


The Gondi protocol allows lenders to be either EOA (externally owned account) or Gondi Pool, which is an ERC4626 contract that allows anyone to deposit funds and earn yield from lending on Gondi. However, there is a bug in the code where the fees collected from loans are not transferred out of the pool. This means that these funds remain locked in the contract indefinitely. The recommended mitigation step is to add a function to collect the fees from the pool. The severity of this bug has been debated, but it is generally considered to be of medium severity as it falls under the definition of "leak of value". The Gondi team has confirmed the mitigation and details can be found in the reports from the team members involved.

### Original Finding Content


Lenders in the Gondi protocol could be EOA or Gondi Pool. The Gondi Pool, an ERC4626, allows anyone to deposit funds and earn yield from lending on Gondi. When a loan is repaid or liquidated, the pool deducts a fee from the received amount before adding the rest to the pool balance. As shown in the `loanRepayment()` function, the fees are calculated by calling `processFees()` and then added to `getCollectedFees`. After that, the accounting function `_loanTermination()` is called with the amount being `received - fees`.

However, this fee is credited to `getCollectedFees` but never transferred out of the pool. As a result, these funds remain locked in the contract indefinitely.

```solidity
function loanRepayment(
    uint256 _loanId,
    uint256 _principalAmount,
    uint256 _apr,
    uint256,
    uint256 _protocolFee,
    uint256 _startTime
) external override onlyAcceptedCallers {
    uint256 netApr = _netApr(_apr, _protocolFee);
    uint256 interestEarned = _principalAmount.getInterest(netApr, block.timestamp - _startTime);
    uint256 received = _principalAmount + interestEarned;
    uint256 fees = IFeeManager(getFeeManager).processFees(_principalAmount, interestEarned);
    getCollectedFees += fees; // @audit getCollectedFees is never transfer out
    _loanTermination(msg.sender, _loanId, _principalAmount, netApr, interestEarned, received - fees);
}
```

### Proof of Concept

The `processFees()` function only calculates the fee but doesn't transfer anything.

```solidity
function processFees(uint256 _principal, uint256 _interest) external view returns (uint256) {
    /// @dev cached
    Fees memory __fees = _fees;
    return _principal.mulDivDown(__fees.managementFee, PRECISION)
        + _interest.mulDivDown(__fees.performanceFee, PRECISION);
}
```

Then after `getCollectedFees` is credited for `fees`, we can see this `getCollectedFees` is never transferred out of the pool.

### Recommended Mitigation Steps

Add a function to collect the credited fees `getCollectedFees` from the pool in the `FeeManager` contract.

**[0xend (Gondi) confirmed and commented](https://github.com/code-423n4/2024-04-gondi-findings/issues/60#issuecomment-2067072726):**
 > Not sure if it's High; tend to think as high as those that would compromise user's assets. Definitely an issue though.

**[0xA5DF (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2024-04-gondi-findings/issues/60#issuecomment-2067666515):**
 > Marking as med as fees falls under the definition 'leak of value'.

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Added `collectFees` method.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/100), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/70) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/23).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gondi |
| Report Date | N/A |
| Finders | minhquanym, bin2chen, oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/60
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

