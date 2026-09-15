---
# Core Classification
protocol: The Standard Auto Redemption
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45057
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
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
finders_count: 1
finders:
  - Giovanni Di Siena
---

## Vulnerability Title

`AutoRedemption::fulfillRequest` should never be allowed to revert

### Overview


This bug report is about a problem with the Chainlink Functions DON, which is causing the auto redemption feature to not work properly. This means that requests are not being reset, which is preventing new requests from being triggered. This bug can cause a complete denial of service for the auto redemption feature. The recommended solution is to not revert if there is an error, validate the response length, handle reverts from external calls, and add an admin function to reset the requests. The bug has been fixed by a commit and verified by another source.

### Original Finding Content

**Description:** Given that the Chainlink Functions DON will not retry failed fulfilments, `AutoRedemption::fulfillRequest` should never be allowed to revert; otherwise, `lastRequestId` will not be reset to `bytes32(0)` which means `AutoRedemption::performUpkeep` will never be able to trigger new requests.

Currently, inline comments suggest that there is an intention to revert if the Chainlink Functions DON returns an error; however, this should be avoided for the reason explained above. Similarly, any potential malformed response or reverts caused by external calls should be handled gracefully and fall through to this line:

```solidity
lastRequestId = bytes32(0);
```

**Impact:** Complete DoS of the auto redemption functionality.

**Recommended Mitigation:** * Do __not__ revert if an error is reported.
* Validate the response against its expected length to ensure that the decoding does not revert.
* Handle reverts from all external calls using `try/catch` blocks.
* Short-circuit if `AutoRedemption::calculateUSDsToTargetPrice` returns `0` (since this will cause the swap to [revert](https://github.com/Uniswap/v3-core/blob/main/contracts/UniswapV3Pool.sol#L603)).
* Optionally add an access-controlled admin function to reset `lastRequestId`.

**The Standard DAO:** Fixed by commit [5235524](https://github.com/the-standard/smart-vault/commit/523552498edefe77aa2782d2a887bb1980cf80b9).

**Cyfrin:** Verified. The response length is now validated against its expected length, which will also result in the logic being skipped if an error is reported. `AutoRedemption::runAutoRedemption` will only run if the target `USDs` amount is non-zero and other reverts from external calls are handled using `try/catch` blocks. An admin function to forcibly reset `lastRequestId` has not been added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | The Standard Auto Redemption |
| Report Date | N/A |
| Finders | Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

