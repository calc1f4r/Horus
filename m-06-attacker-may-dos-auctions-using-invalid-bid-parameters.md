---
# Core Classification
protocol: SIZE
chain: everychain
category: dos
vulnerability_type: denial-of-service

# Attack Vector Details
attack_type: denial-of-service
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5827
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-size-contest
source_link: https://code4rena.com/reports/2022-11-size
github_link: https://github.com/code-423n4/2022-11-size-findings/issues/237

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - denial-of-service
  - dos

protocol_categories:
  - services
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 30
finders:
  - codexploder
  - _141345_
  - Picodes
  - ladboy233
  - cryptonue
---

## Vulnerability Title

[M-06] Attacker may DOS auctions using invalid bid parameters

### Overview


This bug report is about a vulnerability in the SIZE protocol where attackers can submit invalid bids to DOS auctions. The bids can be invalid due to passing a wrong public key, commitment or quote amount. In the code, the public key is never validated and the base amount is not encrypted. This allows attackers to pass a wrong public key, a 0 commitment or a 0 quote amount to force the auction to reject the bid. If 1000 such invalid bids are submitted, the auction will be completely DOSed. The recommended mitigation steps are to implement a slashing mechanism, where some percentage of the submitted quote tokens will go to the protocol and auction creator if the bid cannot be executed due to user's fault.

### Original Finding Content


<https://github.com/code-423n4/2022-11-size/blob/706a77e585d0852eae6ba0dca73dc73eb37f8fb6/src/SizeSealed.sol#L258-L263><br>
<https://github.com/code-423n4/2022-11-size/blob/706a77e585d0852eae6ba0dca73dc73eb37f8fb6/src/SizeSealed.sol#L157-L159><br>
<https://github.com/code-423n4/2022-11-size/blob/706a77e585d0852eae6ba0dca73dc73eb37f8fb6/src/SizeSealed.sol#L269-L280>

Buyers submit bids to SIZE using the bid() function. There's a max of 1000 bids allowed per auction in order to stop DOS attacks (Otherwise it could become too costly to execute the finalize loop). However, setting a max on number of bids opens up other DOS attacks.

In the finalize loop this code is used:

    ECCMath.Point memory sharedPoint = ECCMath.ecMul(b.pubKey, sellerPriv);
    // If the bidder public key isn't on the bn128 curve
    if (sharedPoint.x == 1 && sharedPoint.y == 1) continue;
    bytes32 decryptedMessage = ECCMath.decryptMessage(sharedPoint, b.encryptedMessage);
    // If the bidder didn't faithfully submit commitment or pubkey
    // Or the bid was cancelled
    if (computeCommitment(decryptedMessage) != b.commitment) continue;

Note that pubKey is never validated. Therefore, attacker may pass pubKey = (0,0).
In ecMul, the code will return (1,1):
`if (scalar == 0 || (point.x == 0 && point.y == 0)) return Point(1, 1);`
As a result, we enter the continue block and the bid is ignored. Later, the bidder may receive their quote amount back using refund().

Another way to reach `continue` is by passing a 0 commitment.

One last way to force the auction to reject a bid is a low quotePerBase:

    uint256 quotePerBase = FixedPointMathLib.mulDivDown(b.quoteAmount, type(uint128).max, baseAmount);
    // Only fill if above reserve price
    if (quotePerBase < data.reserveQuotePerBase) continue;

baseAmount is not validated as it is encrypted to seller's public key. Therefore, buyer may pass baseAmount = 0, making quotePerBase = 0.

So, attacker may submit 1000 invalid bids and completely DOS the auction.

### Impact

Attacker may DOS auctions using invalid bid parameters.

### Recommended Mitigation Steps

Implement a slashing mechanism. If the bid cannot be executed due to user's fault, some % their submitted quote tokens will go to the protocol and auction creator.

**[0xean (judge) commented](https://github.com/code-423n4/2022-11-size-findings/issues/237#issuecomment-1308875345):**
 > leaving open for sponsor review, issue is somewhat similar to the baseAmount 0 revert, but is unique enough to stand alone. 

**[RagePit (SIZE) commented](https://github.com/code-423n4/2022-11-size-findings/issues/237#issuecomment-1331289059):**
 > While possibly an issue in extreme cases, we implemented the `minimumBidQuote` for this reason. As anyone looking to DOS this way would have to lockup `minimumBidQuote*1000` tokens for the duration of the auction

**[RagePit (SIZE) commented](https://github.com/code-423n4/2022-11-size-findings/issues/237#issuecomment-1331295562):**
 > Separate from the unintended `#64` issue where the DOS would require no funds locked

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | SIZE |
| Report Date | N/A |
| Finders | codexploder, _141345_, Picodes, ladboy233, cryptonue, HE1M, c7e7eff, minhtrng, Trust, slowmoses, yixxas., TomJ, joestakey, gz627, Lambda, skyle, ktg, 0x1f8b, fs0c, simon135, hihen, RaymondFam, corerouter, chaduke, 0xdapper, KIntern_NA, RedOneN, wagmi, rvierdiiev, V_B |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-size
- **GitHub**: https://github.com/code-423n4/2022-11-size-findings/issues/237
- **Contest**: https://code4rena.com/contests/2022-11-size-contest

### Keywords for Search

`Denial-Of-Service, DOS`

