---
# Core Classification
protocol: Centrifuge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35792
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
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
finders_count: 4
finders:
  - Devtooligan
  - 0xLeastwood
  - Jonatas Martins
  - Gerard Persoon
---

## Vulnerability Title

Frozen users may transfer tranche tokens

### Overview


This bug report discusses a problem in the PoolManager.sol code, specifically in lines 96-117. The issue is that a user whose account has been frozen can still transfer tranche tokens by calling the transferTrancheTokens() function on the PoolManager. However, if the same function is called on the CentrifugeRouter, the transaction will fail. This is because the restriction manager is checked when the function is called on the CentrifugeRouter, but not when it is called on the PoolManager. This can lead to wasted gas and time if the transfer fails in the last step due to the recipient being frozen or not a member. The report includes a proof of concept for this issue and recommends adding a check for the restriction manager in the transferTrancheTokens() function. The Centrifuge team has already implemented a fix for this issue in the commit bc1c02e2.

### Original Finding Content

## Severity: Medium Risk

## Context
`PoolManager.sol#L96-L117`

## Description
A user whose account has been frozen may freely transfer tranche tokens by calling `transferTrancheTokens()` on the PoolManager. If a frozen user were to call `transferTrancheTokens()` on the CentrifugeRouter, the transaction would revert.

```solidity
/// @inheritdoc ICentrifugeRouter
function transferTrancheTokens(
    address vault,
    Domain domain,
    uint64 chainId,
    bytes32 recipient,
    uint128 amount,
    uint256 topUpAmount
) public payable protected {
    SafeTransferLib.safeTransferFrom(IERC7540Vault(vault).share(), _initiator(), address(this), amount);
    _approveMax(IERC7540Vault(vault).share(), address(poolManager));
    _pay(topUpAmount);
    IPoolManager(poolManager).transferTrancheTokens(
        IERC7540Vault(vault).poolId(), 
        IERC7540Vault(vault).trancheId(), 
        domain, 
        chainId, 
        recipient,
        amount, 
        !
    );
}
```

The frozen user is prevented from calling this function because the restriction manager is checked in the call to the hook during the transfer of the tranche tokens from the user to the router. However, when a user calls the same function on the PoolManager, the tokens are immediately burned, and there is no call to the hook or restriction manager. 

Another problem stemming from this missing check is that a transfer may be initiated to a recipient that is either frozen or not a member. This process would ultimately fail in the last step when the tokens were attempted to be transferred to the recipient; however, the sender's shares are already burned, resulting in a waste of gas and time to process the round-trip message to the Centrifuge chain.

## Proof of Concept
```solidity
function testPOC_frozenAccountTransfer(uint128 amount) public {
    uint64 validUntil = uint64(block.timestamp + 7 days);
    address destinationAddress = makeAddr("destinationAddress");
    vm.assume(amount > 0);
    address vault_ = deploySimpleVault();
    ERC7540Vault vault = ERC7540Vault(vault_);
    ITranche tranche = ITranche(address(ERC7540Vault(vault_).share()));
    
    centrifugeChain.updateMember(vault.poolId(), vault.trancheId(), destinationAddress, validUntil);
    centrifugeChain.updateMember(vault.poolId(), vault.trancheId(), address(this), validUntil);
    
    assertTrue(tranche.checkTransferRestriction(address(0), address(this), 0));
    assertTrue(tranche.checkTransferRestriction(address(0), destinationAddress, 0));

    // Fund this address with amount
    centrifugeChain.incomingTransferTrancheTokens(
        vault.poolId(), 
        vault.trancheId(), 
        uint64(block.chainid), 
        address(this), 
        amount
    );
    
    assertEq(tranche.balanceOf(address(this)), amount);
    
    // Fails for invalid tranche token
    uint64 poolId = vault.poolId();
    bytes16 trancheId = vault.trancheId();
    
    centrifugeChain.freeze(poolId, trancheId, address(this));
    assertFalse(tranche.checkTransferRestriction(address(this), destinationAddress, 0));
    
    // Approve and transfer amount from this address to destinationAddress
    tranche.approve(address(poolManager), amount);
    
    poolManager.transferTrancheTokens(
        vault.poolId(), 
        vault.trancheId(), 
        Domain.EVM, 
        uint64(block.chainid),
        destinationAddress.toBytes32(), 
        amount, 
        !
    );
    
    assertEq(tranche.balanceOf(address(this)), 0);
}
```

## Recommendation
Call `tranche.checkTransferRestriction`, which will revert if the sender or recipient are frozen or if the recipient is not a member.

```solidity
/// @inheritdoc IPoolManager
function transferTrancheTokens(
    uint64 poolId,
    bytes16 trancheId,
    Domain destinationDomain,
    uint64 destinationId,
    bytes32 recipient,
    uint128 amount
) external {
    ITranche tranche = ITranche(getTranche(poolId, trancheId));
    require(address(tranche) != address(0), "PoolManager/unknown-token");
    require(tranche.checkTransferRestriction(msg.sender, address(uint160(uint256(recipient))), amount));

    tranche.burn(msg.sender, amount);
}
```

## Centrifuge
We have already implemented a fix for that. Also, please note: in case a user is frozen on EVM, their address on the Centrifuge chain is also frozen and not a member anymore. So even if they would try to exploit the transfer, they wouldn't be able to use their own accounts on the Centrifuge chain and would need to find another account that passed KYC to participate.

**Fixed in commit:** `bc1c02e2`.

## Spearbit
Fixed by adding the `_onTransfer()` function in `Tranche.burn()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Centrifuge |
| Report Date | N/A |
| Finders | Devtooligan, 0xLeastwood, Jonatas Martins, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Centrifuge-Spearbit-Security-Review-July-2024.pdf

### Keywords for Search

`vulnerability`

