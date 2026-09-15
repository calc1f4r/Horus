---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3689
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/141

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - neila
---

## Vulnerability Title

M-14: LiquidityProvider can also lend to PrivateVault

### Overview


This bug report is about an issue found in the AstariaRouter.sol code which is part of the Astaria project. The issue is that Liquidity Providers can lend to PrivateVaults, which is not intended behavior. This unexpected behavior was found by neila and yawn-c111 during a manual review of the code. 

The vulnerability is due to the lendToVault function being controlled by a mapping of address to address, which includes PrivateVaults. This leads to an unexpected attack vector, where unexpected liquidity providers can lend to private vaults. 

The code snippets provided show the lendToVault function, which transfers funds from the WETH token to the address of the vault, and the _newVault function which creates a new vault and sets the sender of the message as the owner of the vault. 

The recommendation for this issue is to create a requirement to lend to only PublicVaults.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/141 

## Found by 
neila

## Summary
Insufficient access control for lending to PublicVault
found by [yawn-c111](https://github.com/yawn-c111)

## Vulnerability Detail
Docs says as follows
https://docs.astaria.xyz/docs/intro
> Any strategists may provide their own capital to fund these loans through their own `PrivateVaults`, and whitelisted strategists can deploy `PublicVaults` that accept funds from other liquidity providers.

However, Liquidity Providers can also lend to `PrivateVault`.

This is because `lendToVault` function is controlled by `mapping(address => address) public vaults`, which are managed by `_newVault` function and include `PrivateVault`s

This leads to unexpected atttack.

## Impact 
Unexpected liquidity providers can lend to private vaults

## Code Snippet
https://github.com/unchain-dev/2022-10-astaria-UNCHAIN/blob/main/src/AstariaRouter.sol#L324

```solidity
function lendToVault(IVault vault, uint256 amount) external whenNotPaused {
    TRANSFER_PROXY.tokenTransferFrom(
      address(WETH),
      address(msg.sender),
      address(this),
      amount
    );

    require(
      vaults[address(vault)] != address(0),
      "lendToVault: vault doesn't exist"
    );
    WETH.safeApprove(address(vault), amount);
    vault.deposit(amount, address(msg.sender));
  }
```

https://github.com/unchain-dev/2022-10-astaria-UNCHAIN/blob/main/src/AstariaRouter.sol#L500

```solidity
function _newVault(
    uint256 epochLength,
    address delegate,
    uint256 vaultFee
  ) internal returns (address) {
    uint8 vaultType;

    address implementation;
    if (epochLength > uint256(0)) {
      require(
        epochLength >= minEpochLength && epochLength <= maxEpochLength,
        "epochLength must be greater than or equal to MIN_EPOCH_LENGTH and less than MAX_EPOCH_LENGTH"
      );
      implementation = VAULT_IMPLEMENTATION;
      vaultType = uint8(VaultType.PUBLIC);
    } else {
      implementation = SOLO_IMPLEMENTATION;
      vaultType = uint8(VaultType.SOLO);
    }

    //immutable data
    address vaultAddr = ClonesWithImmutableArgs.clone(
      implementation,
      abi.encodePacked(
        address(msg.sender),
        address(WETH),
        address(COLLATERAL_TOKEN),
        address(this),
        address(COLLATERAL_TOKEN.AUCTION_HOUSE()),
        block.timestamp,
        epochLength,
        vaultType,
        vaultFee
      )
    );

    //mutable data
    VaultImplementation(vaultAddr).init(
      VaultImplementation.InitParams(delegate)
    );

    vaults[vaultAddr] = msg.sender;

    emit NewVault(msg.sender, vaultAddr);

    return vaultAddr;
  }
```

## Tool used
Manual Review

## Recommendation
create requirement to lend to only PublicVaults.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | neila |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/141
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

