---
# Core Classification
protocol: TokenCard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16887
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
github_link: none

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
finders_count: 1
finders:
  - Michael Colburn | Trail of Bits Gustavo Grieco | Trail of Bits John Dunlap | Trail of Bits
---

## Vulnerability Title

No sanitization is performed when the Oraclize query is constructed

### Overview


This bug report is about data validation for the licence.sol target. It is classified as a low difficulty bug. The oracle contract defines a function _updateTokenRatesList to construct an Oraclize URL query, execute it and save its result. When constructing the query, the token symbol is directly concatenated with the URL parameters. The token symbol is specified when a new token is added into the whitelist by a controller, however it is not clear how that string should be sanitized or which characters are allowed in the name.

An attacker can manipulate the price of the token if they use a specially crafted token name. For example, using "DAI&tsyms=ETH#" will trick the CryptoCompare web service to return the value of DAI, instead of the attacker's token.

To solve this problem, it is recommended to not allow any user to add tokens into the whitelist without carefully reviewing the token string. In the long term, a proper documentation of how to sanitize the token names or a Solidity function to remove special characters used in URLs should be implemented.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** licence.sol

**Difficulty:** Low

## Description

An Oraclize URL query is not carefully constructed using the name of the token and can be manipulated using special characters (e.g., &, %, #, etc). The oracle contract defines `_updateTokenRatesList`, a function to construct an Oraclize URL query, execute it, and save its result as shown in Figure 1. In order to construct the query, the token symbol is directly concatenated with the URL parameters.

```solidity
/// @notice Re-usable helper function that performs the Oraclize Query for a specific list of tokens.
/// @param _gasLimit the gas limit is passed, this is used for the Oraclize callback.
/// @param _tokenList the list of tokens that need to be updated.
function _updateTokenRatesList(uint _gasLimit, address[] _tokenList) private {
    // Check if there are any existing tokens.
    if (_tokenList.length == 0) {
        // Emit a query failure event.
        emit FailedUpdateRequest("empty token list");
    } else if (oraclize_getPrice("URL") * _tokenList.length > address(this).balance) {
        // Emit a query failure event.
        emit FailedUpdateRequest("insufficient balance");
    } else {
        // Set up the cryptocompare API query strings.
        strings.slice memory apiPrefix = "https://min-api.cryptocompare.com/data/price?fsym=".toSlice();
        strings.slice memory apiSuffix = "&tsyms=ETH&sign=true".toSlice();
        // Create a new oraclize query for each supported token.
        for (uint i = 0; i < _tokenList.length; i++) {
            // token must exist, revert if it doesn't
            (string memory tokenSymbol, , , bool available, , , ) = _getTokenInfo(_tokenList[i]);
            require(available, "token must be available");
            // Store the token symbol used in the query.
            strings.slice memory symbol = tokenSymbol.toSlice();
            // Create a new oraclize query from the component strings.
            bytes32 queryID = oraclize_query("URL", apiPrefix.concat(symbol).toSlice().concat(apiSuffix), _gasLimit);
            // Store the query ID together with the associated token address.
            _queryToToken[queryID] = _tokenList[i];
            // Emit the query success event.
            emit RequestedUpdate(symbol.toString());
        }
    }
}
```

Figure 7.1 Function `_updateTokenRatesList` queries oraclize and saves the result.

The token symbol is specified when a new token is added into the whitelist by a controller. However, it is unclear how that string should be sanitized or which characters are allowed in the name.

## Exploit Scenario

An attacker manages to add a new token into the whitelist. He can manipulate the price of that token if he uses a specially crafted token name. For instance, using `"DAI&tsyms=ETH#"` will trick the CryptoCompare web service to return the value of DAI, instead of his token.

## Recommendation

- **Short term:** Do not allow any user to add tokens into the whitelist without carefully reviewing the token string.
  
- **Long term:** Properly document how to sanitize the token names or implement a Solidity function to remove special characters used in URLs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | TokenCard |
| Report Date | N/A |
| Finders | Michael Colburn | Trail of Bits Gustavo Grieco | Trail of Bits John Dunlap | Trail of Bits |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf

### Keywords for Search

`vulnerability`

