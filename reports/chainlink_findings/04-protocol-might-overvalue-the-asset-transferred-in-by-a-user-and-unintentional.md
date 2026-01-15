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
solodit_id: 33479
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

[04] Protocol might overvalue the asset transferred in by a user and unintentionally flaw their accounting logic

### Overview

See description below for full details.

### Original Finding Content


First would be key to note that protocol is to support different types of ERC20, which include tokens that apply fee whenever being transferred, this can be seen from the _### ERC20 token behaviours in scope_ section of the audit's README [here](https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/README.md#L155).

https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/VaultManagerV2.sol#L122-L134

```solidity
  function deposit(
    uint    id,
    address vault,
    uint    amount
  )
    external
      isValidDNft(id)
  {
    idToBlockOfLastDeposit[id] = block.number;
    Vault _vault = Vault(vault);
    _vault.asset().safeTransferFrom(msg.sender, address(vault), amount);
    _vault.deposit(id, amount);
  }
```

This function allows a `dNFT` owner to deposit collateral into a vault, it first transfers the amount from the caller and then deposits it to the vault with the function [here](https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/Vault.sol#L42-L52).

```solidity
  function deposit(
    uint id,
    uint amount
  )
    external
      onlyVaultManager
  {
    id2asset[id] += amount;
    emit Deposit(id, amount);
  }
```

The issue with this implementation is that it could get very faulty for some assets, that's to say for tokens that remove fees whenever they are being transferred, then protocol is going to have an accounting flaw as it assumes the amount of assets sent with this line: `_vault.asset().safeTransferFrom(msg.sender, address(vault), amount);` is what's being received. It would be key to note that the impact of this varies on the logic of the `asset` in some cases this could be just fees that might amount to little value which would still be considered as a leak of value.

However in some cases, for some tokens such as the [`cUSDCv3`](https://etherscan.io/address/0xbfc4feec175996c08c8f3a0469793a7979526065#code), it contains a special case for when the amount to be `deposited == type(uint256).max` in their transfer functions that result in only the user's balance being transferred. This can easily be used to exploit or rug pull the vault depending on the context, as in the vault during deposits, this execution `id2asset[id] += amount` would assume `amount` to be `type(uint256).max` and depositor can then withdraw as much tokens as they like in [consequent withdrawals](https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/Vault.sol#L53-L64), breaking the intended rate of redemption `1 DYAD` to always be `$1`, as they are no collaterals to back this.

Also the protocol has stated that among tokens to consider as collaterals, we should consider LSTs and LRTs; however, even these set of tokens are vulnerable to this, from LSTs that support positive/negative rebases to LSTs that [have 1-2 wei corner cases when querying their transfers](https://docs.lido.fi/guides/lido-tokens-integration-guide/).

### Impact

As explained in the last section, this could lead to multiple bug cases depending on the specific `fee/transfer` logic applied to the asset, but in both cases this leads to a heavy accounting flaw and one might easily game the system by coupling this with the minting/withdrawal logic.

Keep in mind that protocol already integrates Lido's `WSTETH` on the mainnet, but since Chainlink does not have a specific feed for `WSTETH/USD` on the mainnet, protocol uses the Chainlink mainnet's `STETH/USD` feed instead as seen [here](https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/script/deploy/Deploy.V2.s.sol#L55-L61), since this is not for the asset used as collateral. The protocol would decide to change and decide to integrate into protocol `STETH` directly instead which still opens them up to this issue, specifically the ` 1-2 wei corner case`, otherwise this bug case is still applicable to other.

Additional note to judge: This finding was first submitted as a H/M finding and then withdrawn after the scope of tokens to consider were refactored; however, going through the docs and information passed by sponsors we can see that protocol plans on integrating LSTs and LRTs and in that case the `1-2` wei corner case is applicable to LSTs which still makes protocol vulnerable to bug case, so consider upgrading.

### Recommended Mitigation Steps

Do not support these tokens; alternatively a pseudo fix would be to only account for the difference in balance when receiving tokens, but this might not suffice for all tokens considering the future integration of LSTs/LRTs that have rebasing logic attached to them.

### Additional Note

This bug case is applicable to attempts of `safeTransfer/safeTransferFrom` in scope, and can be pinpointed using these search commands

- [https://github.com/search?q=repo%3Acode-423n4%2F2024-04-dyad+safeTransfer%28&type=code](https://github.com/search?q=repo%3Acode-423n4%2F2024-04-dyad+safeTransfer%28&type=code)
- [https://github.com/search?q=repo%3Acode-423n4%2F2024-04-dyad+safeTransferFrom%28&type=code](https://github.com/search?q=repo%3Acode-423n4%2F2024-04-dyad+safeTransferFrom%28&type=code)

Main focus should be in the instances where these tokens are being deposited to protocol.



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

