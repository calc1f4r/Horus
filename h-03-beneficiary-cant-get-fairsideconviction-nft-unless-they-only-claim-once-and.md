---
# Core Classification
protocol: FairSide
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 982
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-fairside-contest
source_link: https://code4rena.com/reports/2021-11-fairside
github_link: https://github.com/code-423n4/2021-11-fairside-findings/issues/62

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - wrong_math

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - cmichel
---

## Vulnerability Title

[H-03] Beneficiary cant get fairSideConviction NFT unless they only claim once, and only after it’s fully vested

### Overview


This bug report is about the WatchPug vulnerability. According to the report, when a beneficiary claims all their vesting tokens, they should get the `fairSideConviction` NFT, but in the current implementation, if the beneficiary has claimed any amounts before it's fully vested, then they will never get the `fairSideConviction` NFT. This is because the `tokenbClaim` requires the initial vesting amount. The recommendation is to change the code at line 138 so that the `amount == totalClaimed` instead of `amount == tokenClaim`. This will ensure that the beneficiary will be able to get the `fairSideConviction` NFT, regardless of whether they have claimed any amounts before it is fully vested.

### Original Finding Content

## Handle

WatchPug


## Vulnerability details

Based on the context, once the beneficiary claimed all their vesting tokens, they should get the `fairSideConviction` NFT.

However, in the current implementation, if the beneficiary has claimed any amounts before it's fully vested, then they will never be able to get the `fairSideConviction` NFT, because at L138, it requires the `tokenbClaim` to be equal to the initial vesting amount.

https://github.com/code-423n4/2021-11-fairside/blob/20c68793f48ee2678508b9d3a1bae917c007b712/contracts/token/FSDVesting.sol#L124-L142

```solidity=124
function claimVestedTokens() external override onlyBeneficiary {
    uint256 tokenClaim = calculateVestingClaim();
    require(
        tokenClaim > 0,
        "FSDVesting::claimVestedTokens: Zero claimable tokens"
    );

    totalClaimed = totalClaimed.add(tokenClaim);
    lastClaimAt = block.timestamp;

    fsd.safeTransfer(msg.sender, tokenClaim);

    emit TokensClaimed(msg.sender, tokenClaim, block.timestamp);

    if (amount == tokenClaim) {
        uint256 tokenId = fsd.tokenizeConviction(0);
        fairSideConviction.transferFrom(address(this), msg.sender, tokenId);
    }
}
```

### Recommendation

Change to:

```solidity=124
function claimVestedTokens() external override onlyBeneficiary {
    uint256 tokenClaim = calculateVestingClaim();
    require(
        tokenClaim > 0,
        "FSDVesting::claimVestedTokens: Zero claimable tokens"
    );

    totalClaimed = totalClaimed.add(tokenClaim);
    lastClaimAt = block.timestamp;

    fsd.safeTransfer(msg.sender, tokenClaim);

    emit TokensClaimed(msg.sender, tokenClaim, block.timestamp);

    if (amount == totalClaimed) {
        uint256 tokenId = fsd.tokenizeConviction(0);
        fairSideConviction.transferFrom(address(this), msg.sender, tokenId);
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | FairSide |
| Report Date | N/A |
| Finders | WatchPug, cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-fairside
- **GitHub**: https://github.com/code-423n4/2021-11-fairside-findings/issues/62
- **Contest**: https://code4rena.com/contests/2021-11-fairside-contest

### Keywords for Search

`Wrong Math`

