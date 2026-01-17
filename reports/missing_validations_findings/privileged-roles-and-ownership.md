---
# Core Classification
protocol: Primex Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59062
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
source_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
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
finders_count: 4
finders:
  - Jennifer Wu
  - Andy Lin
  - Adrian Koegl
  - Hytham Farah
---

## Vulnerability Title

Privileged Roles and Ownership

### Overview

See description below for full details.

### Original Finding Content

**Update**
The team provided detailed responses on the privileged roles. Aside from that, the team added a mechanism to have an extra sanity check that certain roles can only be a contract in the commit `db0f92b`. While the contract validation is valuable, it has limitations. Attackers can potentially bypass these checks by routing their calls through a contract if they can set specific roles. Nevertheless, having this check in place helps decrease the potential attack surface.

Since most actions are behind their well-considered time-lock contracts, we would like to set the status as mitigated. We provide a detailed status update on each of the highlighted areas in the description section. Please review it there as well.

The following is their detailed response (note that the client uses the phrase re-audit, but we are only conducting a fix-review here):

> Firstly, we’d like to answer your findings and then provide the general context of our role system that will also be included (after some polishing) in our documentation.
> 
> 
> 1.1 The role VAULT_ACCESS_ROLE will be assigned to several contracts in the protocol: ActivityRewardDistributor, BatchManager, LimitOrderManager, LiquidityMiningRewardDistributor, PositionManager, SpotTradingRewardDistributor, SwapManager. This role is managed by BIG_TIMELOCK_ADMIN, we will add additional requirements that this and several other roles can be only assigned to smart contracts to decrease the risk of setting incorrect addresses.
> 
> 
> 2.1 BIG_TIMELOCK_ADMIN can’t withdraw all PMX, only the undistributed ones: the variable `availablePMX` decreases every period, we will rename it to `undistributedPMX` to increase the code clarity.
> 
> 
> 2.2 BIG_TIMELOCK_ADMIN can cancel margin limit orders only after delisting the corresponding bucket. We will rename this method from `cancelLimitOrdersByAdmin` to `cancelDelistedLimitOrdersByAdmin`. Also, the Trader’s deposit from such an order will be returned to the Trader, this change will be included in the commit for reaudit.
> 
> 
> **UPD 05.09**. This method will be removed, the possibility to cancel limit orders from delisted buckets will be added to the method `cancelExpiredOrder` added for the issue [PRI-39](https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html#findings-qs39).
> 
> 
> 2.3 Redeemer contract has not been finished yet and will not be included in the first release, for now, we will remove these methods and automate ePMX burning after redeem to make it more transparent.
> 
> 
> 2.4 The upgradability system is described in the answer [PRI-48](https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html#findings-qs48)
> 
> 
> 3.1 The method Reserve.transferToTreasury doesn’t allow to transfer all funds from any bucket, the maximum amount is restricted by the number of bucket pTokens owned by the Reserve. Here, the Reserve serves as a regular lender withdrawing the underlying assets with no additional rights. pTokens are accumulated in the Reserve every time when the liquidity index of the corresponding bucket increases, in this way, the Reserve receives a part of the borrowing fee paid by traders.
> 
> 
> 4.1 Redeemer contract has not been finished yet and will not be included in the first release.
> 
> 
> 4.2 It’s correct behaviour, EMERGENCY_ADMIN can’t affect already distributed rewards but can decrease future rewards in the case of suspicious activity.
> 
> 
> We will also perform two post-deployment parameter audits to make sure that all roles are granted correctly.
> 
> 
> Here we’d like to provide more context about how roles are assigned. We use AccessControl registry for several purposes:
> 
> 
> 1) Contract management. Here we have 5 types of admins:
> 
> 
> *   BIG_TIMELOCK_ADMIN - have the biggest rights in the protocol, can assign other roles excluding SMALL and EMERGENCY admins managed by MEDIUM and SMALL admin correspondingly; can make critical changes such as contract upgrades, setting the most important parameters, etc. This role will be assigned to a timelock contract with a 10-day delay. When Primex becomes a DAO, the management of this role and 2 next timelock roles will be transferred to DAO. Initially, will be managed by multisig.
> *   MEDIUM_TIMELOCK_ADMIN - can manage SMALL admins, and change different parameters in the protocol. Has a 2-day delay; initially, will be managed by multisig.
> *   SMALL_TIMELOCK_ADMIN - can manage EMERGENCY admins, unpause contracts paused by EMERGENCY, and make some other actions. Has a 12-hour delay; initially, will be managed by multisig.
> *   EMERGENCY_ADMIN - can pause different contracts, mostly blocking depositing and borrowing, but it can’t block withdrawal or repaying debts. This role will be granted to external monitoring services. We can’t trust EMERGENCY_ADMIN, so their actions are strictly restricted and maximum damage in the case of EMERGENCY compromisation is the restriction of some protocol features until unpausing.
> *   GUARDIAN_ADMIN - can cancel admin proposals in all 3 timelocks. Can pause timelock contracts in the case of the admin compromisation. Can’t change anything in the protocol. Will be managed by multisig (different from the multisig used in BIG/MEDIUM/SMALL admins).
> 
> 
> 2) Cross-contract interactions
> 
> 
> *   VAULT_ACCESS_ROLE - can put funds to TraderBalanceVault and take them from there, will be granted to the following contracts:
>     *   ActivityRewardDistributor
>     *   BatchManager
>     *   LimitOrderManager
>     *   LiquidityMiningRewardDistributor
>     *   PositionManager 
>     *   SpotTradingRewardDistributor
>     *   SwapManager
> 
> *   NO_FEE_ROLE - can use SwapManager.swap without paying fee, will be granted to Buckets and PositionManager
> *   LOM_ROLE - granted to LimitOrderManager
> *   PM_ROLE - granted to PositonManager
> *   BATCH_MANAGER_ROLE - granted to BatchManager
> 
> 
> 3) Other privileged roles
> 
> 
> *   TRUSTED_TOLERABLE_LIMIT_ROLE - a trusted keeper that will be able to liquidate positions with higher OracleTolerableLimit, will be used only in critical case when market liquidity drops significantly and a risky position can’t be closed with a normal OracleTolerableLimit.
> *   NFT_MINTER - can provide signatures to mint NFTs; NFTs will not be included into the first release.

**File(s) affected:**`all contracts`

**Description:** The protocol incorporates several privileged roles, and it is important to highlight the associated centralization risk to users interacting with the protocol. The following is a list of the privileged roles and their corresponding privileges:

1.   VAULT_ACCESS_ROLE
    1.   Acknowledged May call `TraderBalanceVault.withdrawFrom()` to withdraw any amount of tokens from any trader. 

2.   BIG_TIMELOCK_ADMIN
    1.   Acknowledged May call `SpotTradingRewardDistributor.withdrawPmx()` to withdraw all the PMX. **Update**: To clarify, only the `undistributedPMX` (previously `availablePMX`) can be withdrawn.
    2.   Fixed May cancel limit orders by calling `cancelLimitOrdersByAdmin()`. **Update:** The `LimitOrderManager._unlockAssetsAndDeleteOrder()` function has been modified to return the funds to the trader of the order, rather than to the `msg.sender`, which would be the admin if called through the `cancelLimitOrdersByAdmin()` function.
    3.   Fixed May claim an arbitrary amount of `earlyPMX` and `PMX` tokens from the `Redeemer` contract by calling `adminClaimEarlyTokens()` and `adminClaimRegularTokens()` respectively. **Update:** Those functions have been removed.
    4.   Acknowledged May change the implementation of any upgradeable contract calling `PrimexProxyAdmin.upgrade()` or `upgradeAndCall()`. **Update:** Please refer to [PRI-48](https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html#findings-qs48) for a detailed response regarding the upgradeability.

3.   MEDIUM_TIMELOCK_ADMIN
    1.   Fixed May transfer tokens as long from any bucket as long as they leave `transferRestrictions[].minAmountToBeLeft` tokens in the bucket, by calling `Reserve.transferToTreasury()`. However, the same admin can also change the `transferRestrictions[]` struct by calling `Reserve.setTransferRestriction()`. Hence, they have the ability to transfer the entire funds of any bucket to the protocol treasury. **Update:** The maximum amount is determined by the number of pTokens owned by the Reserve. This design enables the Reserve to receive a portion of the borrowing fee paid by traders. We have marked the status as "fixed" as this is not inherently an issue.

4.   EMERGENCY_ADMIN
    1.   Acknowledged May prevent all users from redeeming early `PMX` tokens by calling `Redeemer.pause()`. Note that the `SMALL_TIMELOCK_ADMIN` could then unpause. **Update:** The client states that the Redeemer will not be included in the first release.
    2.   Acknowledged May decrease the amount of rewards by calling `SpotTradingRewardDistributor.decreaseRewardPerPeriod()`. **Update:** The team clarifies that this is the intended behavior, enabling the emergency role to respond to suspicious activity. This trade-off represents the team's decision between decentralization and operational security.

**Recommendation:** We understand that the team has carefully designed the privileged roles and attempted to balance the operational risk and centralization risk. However, it is crucial to make the centralization of power clear to the users.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Primex Finance |
| Report Date | N/A |
| Finders | Jennifer Wu, Andy Lin, Adrian Koegl, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html

### Keywords for Search

`vulnerability`

