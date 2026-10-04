---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34509
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 20
finders:
  - lealCodes
  - Mlome
  - CircleLooper
  - sobieski
  - JMTT
---

## Vulnerability Title

Lender can Sandwich a borrower to seize his collateral

### Overview


The bug report discusses a vulnerability in a lending platform where a malicious lender can take advantage of a small time window to seize the borrower's collateral. This can happen if the lender sets a very short auction length and then starts the loan auction after the borrower has already borrowed. This can result in the borrower losing their collateral, which is usually worth more than the debt. The report recommends implementing a validation check for the expected auction length to prevent this issue.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L232-L287">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Lender.sol#L232-L287</a>


## Summary
A malicious lender can sandwich a borrow making him eligible to seize the collateral in the first block after 1 second.

## Vulnerability Details
A loan auction can be seized after auctionLength seconds have passed since the start of the auction. Seizing the loan gives the lender the collateral amount which would usually be worth much more than the debt.  

A very small value of auctionLength like 1 would allow the lender to seize the loan. If the block time of the network is more than 1 second, he can start an auction by calling the startAuction function in a block and then call the seizeLoan function in the next block front-running any attempt to repay from the borrower. If the block time is less than 1second, he can stuff the blocks till 1 second passes to prevent the borrower from repaying although it is very unlikely that a borrower will be able to attempt to repay within 1second.  

But since the borrower has the ability to know the auctionLength before borrowing from a pool, he can avoid borrowing from such pools. But a malicious lender can perform the following attack to obtain the above result:  
1. Lender creates a pool with a reasonable auctionLength
1. A borrower attempts to borrow from the lender's pool
1. Lender sandwiches the borrowers transaction and sets the auctionLength of the pool to 1 by calling the setPool function before the borrowers transaction and starts the loan auction after the borrower has borrowed.
1. He calls the seizeLoan function after 1 second passes 

## Impact
The borrower will loose the collateral which will usually be worth much more than the debt.

## Tools Used
Manual review

## Recommendations
Allow the borrower to pass the expected state of the pool when attempting to borrow and perform validation.

```solidity

struct Borrow {
    /// @notice the pool ID to borrow from
    bytes32 poolId;
    /// @notice the amount to borrow
    uint256 debt;
    /// @notice the amount of collateral to put up
    uint256 collateral;
    /// @notice the expected auction length
    uint256 expectedAuctionLength;
}

function borrow(Borrow[] calldata borrows) public {
      
        for (uint256 i = 0; i < borrows.length; i++) {
            .......  

            bytes32 poolId = borrows[i].poolId;
            Pool memory pool = pools[poolId];  

            // validate the auctionLength
            if (pool.auctionLength != borrows[i].expectedAuctionLength) revert PoolConfig();  

            ........        
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | lealCodes, Mlome, CircleLooper, sobieski, JMTT, 0xAsen, qbs, Juntao, Norah, Cosine, Bernd, 0xDetermination, 0xANJAN143, GoSoul22, Bobface, Crunch, pep7siup, hash, ubermensch, ayeslick |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

