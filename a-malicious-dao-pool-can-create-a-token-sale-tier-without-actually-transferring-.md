---
# Core Classification
protocol: Dexe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27298
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
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

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

A malicious DAO Pool can create a token sale tier without actually transferring any DAO tokens

### Overview


A bug was found in the `TokenSaleProposalCreate::createTier` function of the DAO Pool, which is called by a DAO Pool owner to create a new token sale tier. The bug is related to the lack of validation of the token balances after the transfer of the `totalTokenProvided` amount of DAO tokens to the `TokenSaleProposal` contract. A malicious Gov Pool owner could exploit this vulnerability by implementing a custom ERC20 implementation of a token that overrides the `transferFrom` function and fakes a successful transfer without actually transferring underlying tokens. This would enable them to create a fake tier without the proportionate amount of DAO Pool token balance in the `TokenSaleProposal` contract, leading naive users to participate in such a token sale. This could result in a permanent DOS if users attempt to claim the DAO pool tokens.

The recommended mitigation for this bug is to calculate the contract balance before and after the low-level call and verify if the account balance increases by `totalTokenProvided` for non-fee-on-transfer tokens. For fee-on-transfer tokens, the balance increase needs to be further adjusted for the transfer fees. The fix was implemented in [PR177](https://github.com/dexe-network/DeXe-Protocol/commit/64bbcf5b1575e88ead4e5fd58d8ee210a815aad6) and changed from using `transferFrom` to `safeTransferFrom`, however the recommendation still requires that the actual balance be checked before and after the transfer to verify the correct amount of tokens have actually been transferred.

### Original Finding Content

**Description:** `TokenSaleProposalCreate::createTier` is called by a DAO Pool owner to create a new token sale tier. A fundamental prerequisite for creating a tier is that the DAO Pool owner must transfer the `totalTokenProvided` amount of DAO tokens to the `TokenSaleProposal`.

Current implementation implements a low-level call to transfer tokens from `msg.sender(GovPool)` to `TokenSaleProposal` contract. However, the implementation fails to validate the token balances after the transfer is successful. We notice a `dev` comment stating "return value is not checked intentionally" - even so, this vulnerability is not related to checking return `status` but to verifying the contract balances before & after the call.

```solidity
function createTier(
        mapping(uint256 => ITokenSaleProposal.Tier) storage tiers,
        uint256 newTierId,
        ITokenSaleProposal.TierInitParams memory _tierInitParams
    ) external {

       ....
         /// @dev return value is not checked intentionally
  >      tierInitParams.saleTokenAddress.call(
            abi.encodeWithSelector(
                IERC20.transferFrom.selector,
                msg.sender,
                address(this),
                totalTokenProvided
            )
        );  //@audit -> no check if the contract balance has increased proportional to the totalTokenProvided
   }
```

Since a DAO Pool owner can use any ERC20 as a DAO token, it is possible for a malicious Gov Pool owner to implement a custom ERC20 implementation of a token that overrides the `transferFrom` function. This function can override the standard ERC20 `transferFrom` logic that fakes a successful transfer without actually transferring underlying tokens.

**Impact:** A fake tier can be created without the proportionate amount of DAO Pool token balance in the `TokenSaleProposal` contract. Naive users can participate in such a token sale assuming their DAO token claims will be honoured at a future date. Since the pool has insufficient token balance, any attempts to claim the DAO pool tokens can lead to a permanent DOS.

**Recommended Mitigation:** Calculate the contract balance before and after the low-level call and verify if the account balance increases by `totalTokenProvided`. Please be mindful that this check is only valid for non-fee-on-transfer tokens. For fee-on-transfer tokens, the balance increase needs to be further adjusted for the transfer fees. Example code for non-free-on-transfer-tokens:
```solidity
        // transfer sale tokens to TokenSaleProposal and validate the transfer
        IERC20 saleToken = IERC20(_tierInitParams.saleTokenAddress);

        // record balance before transfer in 18 decimals
        uint256 balanceBefore18 = saleToken.balanceOf(address(this)).to18(_tierInitParams.saleTokenAddress);

        // perform the transfer
        saleToken.safeTransferFrom(
            msg.sender,
            address(this),
            _tierInitParams.totalTokenProvided.from18Safe(_tierInitParams.saleTokenAddress)
        );

        // record balance after the transfer in 18 decimals
        uint256 balanceAfter18 = saleToken.balanceOf(address(this)).to18(_tierInitParams.saleTokenAddress);

        // verify that the transfer has actually occured to protect users from malicious
        // sale tokens that don't actually send the tokens for the token sale
        require(balanceAfter18 - balanceBefore18 == _tierInitParams.totalTokenProvided,
                "TSP: token sale proposal creation received incorrect amount of tokens"
        );
```

**Dexe:**
Fixed in [PR177](https://github.com/dexe-network/DeXe-Protocol/commit/64bbcf5b1575e88ead4e5fd58d8ee210a815aad6).

**Cyfrin:** The fix changed from using `transferFrom` to `safeTransferFrom` however the recommendation requires that the actual balance be checked before and after the transfer to verify the correct amount of tokens have actually been transferred.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Dexe |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

