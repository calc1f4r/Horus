---
# Core Classification
protocol: USDV_2025-03-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57863
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-10] Shared whitelist usage prevents token-specific address whitelisting

### Overview

See description below for full details.

### Original Finding Content

First, take a look at `deploy.s.sol`

```solidity
// deploying the whitelist contract
whitelist = IAddressesWhitelistExtended(address(new AddressesWhitelist()));

address[] memory whitelistedTokens = new address[](2);
whitelistedTokens[0] = usdcAddress;
whitelistedTokens[1] = usdtAddress;

// deploying the ExternalRequestsManager contract for FunLP tokens
externalRequestsManager = IExternalRequestsManagerExtended(
    address(new ExternalRequestsManager(address(funLpToken), treasury, address(whitelist), whitelistedTokens))
);

funLpToken.grantRole(SERVICE_ROLE, address(externalRequestsManager));

externalRequestsManager.grantRole(SERVICE_ROLE, service);

usfExternalRequestsManager = IExternalRequestsManagerExtended(
    address(new ExternalRequestsManager(address(funToken), treasury, address(whitelist), whitelistedTokens))
);

funToken.grantRole(SERVICE_ROLE, address(usfExternalRequestsManager)); // requires for mint and burn functions


// ..snip

whitelist.transferOwnership(admin);

```

As seen in the script, we use the same `whitelist` contract instance for both `ExternalRequestsManager` instances which are then relayed for the `funLpToken` and `funToken` tokens. Which then creates a shared whitelist situation where any provider whitelisted for one token is automatically whitelisted for the other.

Now the use of a shared whitelist contract for both ExternalRequestsManager instances eliminates the possibility of implementing token-specific provider access controls.

Note that this can be translated as not the appropriate path, since per the script there is an intention to have two seperate `ExternalRequestsManager`s, which should translate to two different instances for the whitelisting of `funLpToken` and `funToken` tokens.

However the current design decision means we now have the inability to implement different risk profiles for both tokens - providers that might be trusted to interact with one token cannot be restricted from interacting with the other.

One could also hint regulatory considerations here, since different tokens might have different regulatory requirements for provider whitelisting that cannot be accommodated, assume OFAC where one is to be compliant and block those in the OFAC list whereas the other isn't, however this is impossible.

i.e in our case, looking at `requestMint()`, there could be an argument that, some providers might have regulatory approval to interact with liquidity tokens per their complexity but not with stablecoins.

**Recommendation**

Since we are having two seperate `ExternalRequestsManager`s, we should also have two seperate `AddressesWhitelist`s to enable token-specific access control:

```solidity
// Deploy separate whitelist contracts
IAddressesWhitelistExtended funLpWhitelist = IAddressesWhitelistExtended(address(new AddressesWhitelist()));
IAddressesWhitelistExtended usfWhitelist = IAddressesWhitelistExtended(address(new AddressesWhitelist()));

// Use token-specific whitelists for each manager
externalRequestsManager = IExternalRequestsManagerExtended(
    address(new ExternalRequestsManager(address(funLpToken), treasury, address(funLpWhitelist), whitelistedTokens))
);

usfExternalRequestsManager = IExternalRequestsManagerExtended(
    address(new ExternalRequestsManager(address(funToken), treasury, address(usfWhitelist), whitelistedTokens))
);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | USDV_2025-03-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

