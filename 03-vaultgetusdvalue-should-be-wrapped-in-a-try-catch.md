---
# Core Classification
protocol: DYAD
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33478
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-dyad
source_link: https://code4rena.com/reports/2024-04-dyad
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
finders_count: 0
finders:
---

## Vulnerability Title

[03] `vault.getUsdValue()` should be wrapped in a try catch

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/Vault.kerosine.unbounded.sol#L50-L68

```solidity
  function assetPrice()
    public
    view
    override
    returns (uint) {
      uint tvl;
      //@audit
      address[] memory vaults = kerosineManager.getVaults();
      uint numberOfVaults = vaults.length;
      for (uint i = 0; i < numberOfVaults; i++) {
        Vault vault = Vault(vaults[i]);
        tvl += vault.asset().balanceOf(address(vault))
                * vault.assetPrice() * 1e18
                / (10**vault.asset().decimals())
                / (10**vault.oracle().decimals());
      }
      uint numerator   = tvl - dyad.totalSupply();
      uint denominator = kerosineDenominator.denominator();
      return numerator * 1e8 / denominator;
  }
```

This function is used to get the price of an asset, and it gets that by querying the specific vault of that asset for its balance and price. Keep in mind that this function is also used whenever getting price from the bounded vault as shown [here](https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/Vault.kerosine.bounded.sol#L44-L50).

```solidity

  function assetPrice()
    public
    view
    override
    returns (uint) {
      return unboundedKerosineVault.assetPrice() * 2;
        }
```

Going back to the `VaultManager`, we can see that the line `usdValue = vault.getUsdValue(id);  ` is queried whenever there is a need to get the prices as confirmed by [this search command](https://github.com/search?q=repo%3Acode-423n4%2F2024-04-dyad+usdValue+%3D+vault.getUsdValue%28id%29%3B+++NOT+language%3AMarkdown&type=code) and queries the two aforementioned functions as shown [here](https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/Vault.sol#L79-L104).

```solidity
  function getUsdValue(
    uint id
  )
    external
    view
    returns (uint) {
      return id2asset[id] * assetPrice()
              * 1e18
              / 10**oracle.decimals()
              / 10**asset.decimals();
  }



  function assetPrice()
    public
    view
    returns (uint) {
      (
        ,
        int256 answer,
        ,
        uint256 updatedAt,
      ) = oracle.latestRoundData();
      if (block.timestamp > updatedAt + STALE_DATA_TIMEOUT) revert StaleData();
      return answer.toUint256();
  }
```

That is to say that the pricing logic requires us to query chainlink at the end of the calls, but evidently, we can see that this call lacks error handling for the potential failure of `vault.getUsdValue` which could fail due to the call to `oracle.latestRoundData()` via `assetPrice()`. Note that Chainlink pricefeeds could revert due to whatever reason, i.e. say maintenance or maybe the Chainlink team decide to change the underlying address. Now this omission of not considering this call failing would lead to systemic issues, since calls to this would now revert halting any action that requires this call to succeed.

### Impact

Borderline medium/low, as this essentially breaks core functionalities like liquidating and whatever requires for the usd value of an asset to be queried since there would be a complete revert.

### Recommended Mitigation Steps

Wrap the `vault.getUsdValue()` call in a try-catch block, then handle the error (e.g., revert with a specific message or use an alternative pricing method); the latter is a better fix as it ensures the protocol still functions as expected on the fallback oracle.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | DYAD |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-dyad
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-04-dyad

### Keywords for Search

`vulnerability`

