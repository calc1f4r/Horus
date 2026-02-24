---
# Core Classification
protocol: The Computable Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16593
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
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
finders_count: 3
finders:
  - Gustavo Grieco
  - Rajeev Gopalakrishna
  - Josselin Feist
---

## Vulnerability Title

Lack of timeout to claim listing fees allows price manipulation

### Overview


This bug report is about a vulnerability in the Listing.vy smart contract, which is used to store data and reward listing owners for their services. After a delivery is at least partially complete, the listing owner should call the claimBytesAccessed function to collect the listing fees. This function will mint new market tokens to pay for the fees, but there is no timeout to call this function. As a result, a malicious listing owner can wait an arbitrary amount of time to claim its tokens and exploit a significant price change in the market. 

To mitigate this vulnerability, the smart contract can be modified to allow any user, the contract owner, the datatrust, or the getBytesAccessed function to call the claimBytesAccessed function. Additionally, off-chain monitoring can be used to detect listing owners with high reward uncollected. In the long term, measures should be taken to ensure that listing owners can't influence the market.

### Original Finding Content

## Description

After a delivery completes, there is no timeout to claim the listing fees. Claiming fees will mint new tokens, affecting the price. As a result, a successful listing owner can wait an arbitrary amount of time to claim its tokens and exploit a significant price change in the market.

After a delivery is at least partially complete, the listing owner should call the `claimBytesAccessed` function to collect the listing fees.

```python
def claimBytesAccessed(hash: bytes32):
    """
    @notice Allows a listing owner to claim the rewards of listing access. These support the market and will be noted at the listing.supply (MarketToken)
    @param hash The listing identifier
    """
    assert msg.sender == self.listings[hash].owner
    # the algo for maker payment is (accessed*cost)/(100/maker_pct)
    accessed: uint256 = self.datatrust.getBytesAccessed(hash)
    maker_fee: wei_value = (self.parameterizer.getCostPerByte() * accessed * self.parameterizer.getMakerPayment()) / 100
    price: wei_value = self.reserve.getSupportPrice()
    
    # if credits accumulated are too low for support, exit now
    assert maker_fee >= price
    
    # clear the credits before proceeding (also transfers fee to reserve)
    self.datatrust.bytesAccessedClaimed(hash, maker_fee)
    
    # support is now called, according to the buy-curve.
    minted: uint256 = (maker_fee * 1000000000) / price  # 1 Billionth token is the smallest denomination...
    self.market_token.mint(minted)
    self.listings[hash].supply += minted
    log.BytesAccessedClaimed(hash, accessed, minted)
```

**Figure 1.** `claimBytesAccessed` function in Listing.vy

This function will mint new market tokens to pay for the fees. However, there is no timeout to call this function. Minting new market tokens will affect the price of it.

## Exploit Scenario

Eve creates a legitimate listing, and other users request her data. After some time, she collects a large amount of fees. Instead of calling `claimBytesAccessed` for each, she waits until there is a convenient moment for her to buy or sell market tokens. As a result, Eve is able to manipulate the price and exploit the market.

## Recommendation

Short term, consider implementing one of the following mitigations:
1. Allow any user to call `claimBytesAccessed`, while incentivizing the caller to get a small fee for it.
2. Allow the contract owner to call `claimBytesAccessed`, if a potential attack to manipulate prices is detected.
3. Allow the datatrust to call `claimBytesAccessed` after a delivery.
4. Automatically call `claimBytesAccessed` when `getBytesAccessed` is called.

Alternatively, off-chain monitoring can be used to detect listing owners with high reward uncollected.

Long term, consider that listing owners can be malicious and ensure they can’t influence the market.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | The Computable Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Rajeev Gopalakrishna, Josselin Feist |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/computable.pdf

### Keywords for Search

`vulnerability`

