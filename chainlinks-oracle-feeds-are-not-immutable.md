---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27619
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - 0xVinylDavyl
  - SanketKogekar
  - 0xhals
  - Cosine
  - MaanVader
---

## Vulnerability Title

Chainlinks oracle feeds are not immutable

### Overview


This bug report is about the Chainlink oracle feeds not being immutable. Chainlink oracle feeds are used to provide price information to the protocol, but the protocol prevents the addresses of the price feeds from being updated or removed. This can lead to a complete DoS of the underlying token, as it is not possible to remove price feeds which are no longer supported by chainlink. 

The cause of this bug is the following line of code in ChainlinkARBOracle:

```jsx
if (feeds[token] != address(0)) revert Errors.TokenPriceFeedAlreadySet();
```

The severity of this bug is medium risk. The tools used to find this bug were manual review.

The recommendation to fix this bug is to remove the line of code mentioned above.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/oracles/ChainlinkARBOracle.sol#L239">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/oracles/ChainlinkARBOracle.sol#L239</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/oracles/ChainlinkARBOracle.sol#L65">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/oracles/ChainlinkARBOracle.sol#L65</a>


## Summary

That a chainlink oracle works does not mean it will be supported by chainlink in the future and keeps working, and it could also be possible that the address of the price feed changes. Therefore, it does not make sense to prevent price feed addresses from being updated, or removed, but the protocol prevents that.

## Vulnerability Details

There is only one function inside ChainlinkARBOracle to update the price feed addresses:

```jsx
function addTokenPriceFeed(address token, address feed) external onlyOwner {
  if (token == address(0)) revert Errors.ZeroAddressNotAllowed();
  if (feed == address(0)) revert Errors.ZeroAddressNotAllowed();
  if (feeds[token] != address(0)) revert Errors.TokenPriceFeedAlreadySet();

  feeds[token] = feed;
}
```

As we can see it will only allow to set the price feed ones and revert if trying to update, or remove a price feed. Therefore, if chainlink changes something, or the owner accidentally set the wrong address, or the protocol no longer wants to support a price feed, it can not be removed, or updated.

## Impact

It is not possible to remove price feeds which are no longer supported by chainlink, or update the addresses of price feeds. This can lead to a complete DoS of the underlying token.

As this feeds mapping is also the only check if it is a valid token when calling the oracle and the feed can not be removed, it will always pass this check even if the protocol no longer wishes to support this token:

```jsx
function consult(address token) public view whenNotPaused returns (int256, uint8) {
  address _feed = feeds[token];

  if (_feed == address(0)) revert Errors.NoTokenPriceFeedAvailable();
	...
}
```

## Tools Used

Manual Review

## Recommendations

Remove this line:

```jsx
if (feeds[token] != address(0)) revert Errors.TokenPriceFeedAlreadySet();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | 0xVinylDavyl, SanketKogekar, 0xhals, Cosine, MaanVader |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

