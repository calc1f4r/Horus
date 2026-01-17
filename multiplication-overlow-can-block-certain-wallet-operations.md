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
solodit_id: 16889
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/TokenCard.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Multiplication over�low can block certain wallet operations

### Overview

See description below for full details.

### Original Finding Content

## Access Controls

**Target:** wallet.sol

**Difficulty:** High

## Description

Some wallet transfers involving a very large number of tokens may trigger an integer overflow that will revert the transaction. The `convertToEther` and `convertToStablecoin` functions are designed to compute the value of certain amounts of ERC20 tokens in terms of tokens or stablecoins, respectively, as shown in Figure 1 and Figure 2.

### Function: convertToEther

```solidity
function convertToEther(address _token, uint _amount) public view returns (uint) {
    // Store the token in memory to save map entry lookup gas.
    (, uint256 magnitude, uint256 rate, bool available, , , ) = _getTokenInfo(_token);
    
    // If the token exists require that its rate is not zero.
    if (available) {
        require(rate != 0, "token rate is 0");
        // Safely convert the token amount to ether based on the exchange rate.
        return _amount.mul(rate).div(magnitude);
    }
    return 0;
}
```

*Figure 9.1 convertToEther function*

### Function: convertToStablecoin

```solidity
function convertToStablecoin(address _token, uint _amount) public view returns (uint) {
    // Avoid the unnecessary calculations if the token to be loaded is the stablecoin itself
    if (_token == _stablecoin()) {
        return _amount;
    }
    
    // 0x0 represents ether
    if (_token != address(0)) {
        // Convert to eth first, same as convertToEther()
        // Store the token in memory to save map entry lookup gas.
        (, uint256 magnitude, uint256 rate, bool available, , , ) = _getTokenInfo(_token);
        
        // Require that token both exists in the whitelist and its rate is not zero.
        require(available, "token is not available");
        require(rate != 0, "token rate is 0");
        // Safely convert the token amount to ether based on the exchange rate.
        _amount = _amount.mul(rate).div(magnitude);
    }
    ...
}
```

*Figure 9.2 convertToStablecoin function*

However, they can trigger similar integer overflows when they multiply the amount of tokens to transfer by its rate. Since the Wallet contract is using SafeMath for its arithmetic operations, the integer overflow triggers a revert, as shown in Figure 3.

### Function: mul

```solidity
function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
    // benefit is lost if 'b' is also tested.
    // See: https://github.com/OpenZeppelin/openzeppelin-solidity/pull/522
    if (a == 0) {
        return 0;
    }
    uint256 c = a * b;
    require(c / a == b);
    return c;
}
```

*Figure 9.3 mul(int256 a, int256 b) function*

## Exploit Scenario

A user wants to transfer a very large number of tokens using his Wallet contract. However, he is unable to do so because that transaction will trigger a revert. He may not realize that transferring a smaller amount will work around this limitation. He stops using the Wallet contract.

## Recommendation

**Short-term:** Properly document this limitation and make sure that users are aware of it.

**Long-term:** Alert the user that the transfer fails because of a very large number of tokens. For instance, refactoring the code to detect this overflow and using a suitable error message in the revert call.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

