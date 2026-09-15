---
# Core Classification
protocol: Contracts V2 Updates
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50115
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/moonwell/contracts-v2-updates
source_link: https://www.halborn.com/audits/moonwell/contracts-v2-updates
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
  - Halborn
---

## Vulnerability Title

SILENT FAILURE DURING TOKEN MINTING ON THE ROUTER CONTRACT

### Overview


The bug report is about a function in Compound's ERC20 `mToken` contracts that does not behave as expected. The function, `mToken.mint(msg.value);`, does not revert on failure, but instead returns an error code as a `uint` value. This is not the standard behavior for Solidity functions and can cause problems for calling contracts. If the calling contract does not check the return value, failures in this function will not cause the overall transaction to revert. This can lead to imbalances between the perceived balance of `mTokens` and the actual supply of minted `mTokens`. The report provides a proof of concept and a BVSS score for the bug. It also recommends adding return value validation and includes a remediation plan. The Moonwell Finance team has solved the issue by adding the return value validation in their code.

### Original Finding Content

##### Description

The `mToken.mint(msg.value);` function, originating from Compound's ERC20 `mToken` contracts, is a call that does not revert on failure but returns an error code as a `uint` value instead. This behavior deviates from the standard expected of typical Solidity functions that revert on failure.

This non-standard behavior makes it difficult for calling contracts (like the one above) to correctly handle failures. As the above contract does not check the return value of `mToken.mint()`, failures in this function will not cause the overall transaction to revert.

This could lead to serious imbalances between the perceived balance of `mTokens` on the router contract and the actual supply of minted `mTokens`.

* **Code Location**

```
    /// @notice Deposit ETH into the Moonwell protocol
    /// @param recipient The address to receive the mToken
    function mint(address recipient) external payable {
        weth.deposit{value: msg.value}();

        mToken.mint(msg.value);

        IERC20(address(mToken)).safeTransfer(
            recipient,
            mToken.balanceOf(address(this))
        );
    }

```

##### Proof of Concept

`Step 1 :` An external actor calls the `mint()` function, sending some ETH along with the transaction.

`Step 2 :` The function attempts to convert the sent ETH to WETH by calling `weth.deposit{value: msg.value}();`.

`Step 3 :` The contract calls `mToken.mint(msg.value);`, but this operation fails for some reason. However, instead of reverting the transaction, `mToken.mint()` returns an error code.

`Step 4 :` Ignoring the failure from `mToken.mint()`, the contract proceeds to `IERC20(address(mToken)).safeTransfer(recipient, mToken.balanceOf(address(this)));`.

  
![poc1.png](https://halbornmainframe.com/proxy/audits/images/659f1a09a1aa3698c0f33b9b)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:H/A:H/D:H/Y:H/R:P/S:C (8.2)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:H/A:H/D:H/Y:H/R:P/S:C)

##### Recommendation

It is recommended to add the return value validation.

  

### Remediation Plan

**SOLVED**: The `Moonwell Finance team` solved the issue by adding the return value validation.

`Commit ID:` [c39f98bdc9dd4e448ba585923034af1d47f74dfa](https://github.com/moonwell-fi/moonwell-contracts-v2/commit/c39f98bdc9dd4e448ba585923034af1d47f74dfa)

##### Remediation Hash

<https://github.com/moonwell-fi/moonwell-contracts-v2/commit/c39f98bdc9dd4e448ba585923034af1d47f74dfa>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Contracts V2 Updates |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/moonwell/contracts-v2-updates
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/moonwell/contracts-v2-updates

### Keywords for Search

`vulnerability`

