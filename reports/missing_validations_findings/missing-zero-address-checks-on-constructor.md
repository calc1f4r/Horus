---
# Core Classification
protocol: Earn V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51874
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/earn-v1
source_link: https://www.halborn.com/audits/concrete/earn-v1
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
  - Halborn
---

## Vulnerability Title

Missing zero address checks on constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description

It has been observed missing zero address checks on the `Radiant` and `Silo` constructors:

```
constructor(
        IERC20 baseAsset_,
        address feeRecipient_,
        address owner_,
        uint256 rewardFee_,
        address siloAsset_,
        address siloRepository_,
        address siloIncentivesController_,
        address[] memory extraRewardAssets,
        uint256[] memory extraRewardFees,
        address vault_
    ) {
        IERC20Metadata metaERC20 = IERC20Metadata(address(baseAsset_));

        siloRepository = ISiloRepository(siloRepository_);
        silo = ISilo(siloRepository.getSilo(siloAsset_));
        if (address(silo) == address(0)) revert InvalidAssetAddress();
        // validate the bridge asset
        if (siloAsset_ != address(baseAsset_)) {
            address[] memory siloAssets_ = silo.getAssets();
            uint256 length = siloAssets_.length;
            uint256 i;
            while (i < length) {
                if (siloAssets_[i] == address(baseAsset_)) {
                    break;
                }
                unchecked {
                    i++;
                }
            }
            if (i == length) revert AssetDivergence();
        }
        siloIncentivesController = ISiloIncentivesController(siloIncentivesController_);
        ISilo.AssetStorage memory assetStorage = silo.assetStorage(address(baseAsset_));
        collateralToken = IERC20(assetStorage.collateralToken);

        // prepare rewardTokens array

        uint256 rewardsLength = extraRewardAssets.length;
        RewardToken[] memory rewardTokenArray = new RewardToken[](rewardsLength + 1);
        // assign the silo reward token first and then process the extra reward tokens
        address[] memory rewards = getRewardTokenAddresses();
        rewardTokenArray[0] = RewardToken(IERC20(rewards[0]), rewardFee_, 0);

        for (uint256 i = 0; i < rewardsLength;) {
            rewardTokenArray[i+1] = RewardToken(IERC20(extraRewardAssets[i]), extraRewardFees[i], 0);
            unchecked {
                i++;
            }
        }

        if (address(collateralToken) == address(0)) revert InvalidAssetAddress();
        __StrategyBase_init(
            baseAsset_,
            string.concat("Concrete Earn SiloV1 ", metaERC20.symbol(), " Strategy"),
            string.concat("ctSlV1-", metaERC20.symbol()),
            feeRecipient_,
            type(uint256).max,
            owner_,
            rewardTokenArray,
            vault_
        );
        //slither-disable-next-line unused-return
        baseAsset_.approve(address(silo), type(uint256).max);
    }
```

```
constructor(
        IERC20 baseAsset_,
        address feeRecipient_,
        address owner_,
        uint256 rewardFee_,
        address addressesProvider_,
        address vault_
    ) {
        IERC20Metadata metaERC20 = IERC20Metadata(address(baseAsset_));

        addressesProvider = ILendingPoolAddressesProvider(addressesProvider_);
        lendingPool = ILendingPool(addressesProvider.getLendingPool());
        DataTypes.ReserveData memory reserveData = lendingPool.getReserveData(address(baseAsset_));
        rToken = IAToken(reserveData.aTokenAddress);
        if (rToken.UNDERLYING_ASSET_ADDRESS() != address(baseAsset_)) {
            revert AssetDivergence();
        }
        rewardsEnabled = false;
        incentiveController = IChefIncentivesController(rToken.getIncentivesController());

        __StrategyBase_init(
            baseAsset_,
            string.concat("Concrete Earn RadiantV2 ", metaERC20.symbol(), " Strategy"),
            string.concat("ctRdV2-", metaERC20.symbol()),
            feeRecipient_,
            type(uint256).max,
            owner_,
            _getRewardTokens(rewardFee_),
            vault_
        );
        //slither-disable-next-line unused-return
        baseAsset_.approve(address(lendingPool), type(uint256).max);
    }
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

Consider adding proper checks on the constructor.

##### Remediation

**SOLVED:** The **Concrete team** solved the issue by applying recommendations.

##### Remediation Hash

ef76d69792cc6aec1d60982536bab8af21992608

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Earn V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/concrete/earn-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/concrete/earn-v1

### Keywords for Search

`vulnerability`

