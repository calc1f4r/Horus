---
# Core Classification
protocol: Sense
chain: everychain
category: uncategorized
vulnerability_type: first_depositor_issue

# Attack Vector Details
attack_type: first_depositor_issue
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3556
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/19
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-sense-judging/issues/50

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - first_depositor_issue
  - initial_deposit
  - erc4626

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ak1
---

## Vulnerability Title

H-1: Public vault : Initial depositor can manipulate the price per share value and future depositors are forced to deposit huge value in vault.

### Overview


This bug report is about a vulnerability in the "Public Vault" of the ERC4626 implementation. The issue is that the initial depositor can manipulate the price per share value, and this will force future depositors to deposit huge values in the vault. This issue is found in most share-based vault implementations. The vulnerability is that the shares are minted based on the deposit value, so if the initial depositor deposits a large amount, they can take advantage of future depositors. This has been previously reported and acknowledged. The impact of this vulnerability is that future depositors are forced to deposit huge values, which not all users can do, and this can lead to a decrease in the number of users of the system. The code snippet and recommendation are included in the bug report. There is also a discussion about how the initial depositor can bypass the initial deposit.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-sense-judging/issues/50 

## Found by 
ak1

## Summary
Most of the share based vault implementation will face this issue.
The vault is based on the ERC4626 where the shares are calculated based on the deposit value.
By depositing large amount as initial deposit, initial depositor can influence the future depositors value.

## Vulnerability Detail

Shares are minted based on the deposit value.
https://github.com/sherlock-audit/2022-11-sense/blob/main/contracts/src/RollerPeriphery.sol#L59-L79
Public vault is based on the ERC4626 where the shares are calculated based on the deposit value.

By depositing large amount as initial deposit, first depositor can take advantage over other depositors.

I am sharing reference for this type of issue that already reported and acknowledged. This explain how the share price could be manipulated to  large value.

https://github.com/sherlock-audit/2022-08-sentiment-judging#issue-h-1-a-malicious-early-userattacker-can-manipulate-the-ltokens-pricepershare-to-take-an-unfair-share-of-future-users-deposits:~:text=Issue%20H%2D1%3A%20A%20malicious%20early%20user/attacker%20can%20manipulate%20the%20LToken%27s%20pricePerShare%20to%20take%20an%20unfair%20share%20of%20future%20users%27%20deposits

ERC4626 implementation
    function mint(uint256 shares, address receiver) public virtual returns (uint256 assets) {
        assets = previewMint(shares); // No need to check for rounding error, previewMint rounds up.

        // Need to transfer before minting or ERC777s could reenter.
        asset.safeTransferFrom(msg.sender, address(this), assets);

        _mint(receiver, shares);

        emit Deposit(msg.sender, receiver, assets, shares);

        afterDeposit(assets, shares);
    }

      function previewMint(uint256 shares) public view virtual returns (uint256) {
        uint256 supply = totalSupply; // Saves an extra SLOAD if totalSupply is non-zero.

        return supply == 0 ? shares : shares.mulDivUp(totalAssets(), supply);
    }


## Impact
Future depositors are forced for huge value of asset to deposit. It is not practically possible for all the users.
This could directly affect on the attrition of users towards this system.

## Code Snippet

https://github.com/sherlock-audit/2022-11-sense/blob/main/contracts/src/RollerPeriphery.sol#L59-L79

ERC4626 implementation
    function mint(uint256 shares, address receiver) public virtual returns (uint256 assets) {
        assets = previewMint(shares); // No need to check for rounding error, previewMint rounds up.

        // Need to transfer before minting or ERC777s could reenter.
        asset.safeTransferFrom(msg.sender, address(this), assets);

        _mint(receiver, shares);

        emit Deposit(msg.sender, receiver, assets, shares);

        afterDeposit(assets, shares);
    }

      function previewMint(uint256 shares) public view virtual returns (uint256) {
        uint256 supply = totalSupply; // Saves an extra SLOAD if totalSupply is non-zero.

        return supply == 0 ? shares : shares.mulDivUp(totalAssets(), supply);
    }

## Tool used

Manual Review

## Recommendation
Consider requiring a minimal amount of share tokens to be minted for the first minter, and send a portion of the initial mints as a reserve to the DAO/ burn so that the price per share can be more resistant to manipulation.

## Discussion

**Evert0x**

Depositor can bypass this initial deposit https://github.com/sherlock-audit/2022-11-sense/blob/main/contracts/src/AutoRoller.sol#L160

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Sense |
| Report Date | N/A |
| Finders | ak1 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-sense-judging/issues/50
- **Contest**: https://app.sherlock.xyz/audits/contests/19

### Keywords for Search

`First Depositor Issue, Initial Deposit, ERC4626`

