---
# Core Classification
protocol: Possum
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44144
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Possum-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-04] Hardcoded Addresses

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The existence of hardcoded addresses could lead to detrimental consequences for the protocol if the smart contracts, deployed at these addresses are exploited in some way.

## Location of Affected Code

File: [contracts/Portal.sol#L67-L77](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol#L67-L77)

```solidity
address payable private constant compounderAddress = payable (0x8E5D083BA7A46f13afccC27BFB7da372E9dFEF22);
address payable private constant HLPstakingAddress = payable (0xbE8f8AF5953869222eA8D39F1Be9d03766010B1C);
address private constant HLPprotocolRewarder = 0x665099B3e59367f02E5f9e039C3450E31c338788;
address private constant HLPemissionsRewarder = 0x6D2c18B559C5343CB0703bB55AADB5f22152cC32;
address private constant HMXstakingAddress = 0x92E586B8D4Bf59f4001604209A292621c716539a;
address private constant HMXprotocolRewarder = 0xB698829C4C187C85859AD2085B24f308fC1195D3;
address private constant HMXemissionsRewarder = 0x94c22459b145F012F1c6791F2D729F7a22c44764;
address private constant HMXdragonPointsRewarder = 0xbEDd351c62111FB7216683C2A26319743a06F273;
```

## Recommendations

Consider adding a setter function for all the hardcoded addresses, callable only by the owner of the `Portal.sol` contract.

## Team Response

Acknowledged.

## [I-01] Missing Event Emission in Multiple Functions

## Severity

Informational

## Description

It has been observed that important functionality is missing an emitting event for `convert()`, `burnBtokens()`, `mintPortalEnergyToken()`, `burnPortalEnergyToken()` and `updateMaxLockDuration()` functions. Events are a method of informing the transaction initiator about the actions taken by the called function. An event logs its emitted parameters in a specific log history, which can be accessed outside of the contract using some filter parameters.

## Location of Affected Code

File: [contracts/Portal.sol](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol)

```solidity
function convert(address _token, uint256 _minReceived) external nonReentrant {
function burnBtokens(uint256 _amount) external nonReentrant {
function mintPortalEnergyToken(address _recipient, uint256 _amount) external nonReentrant {
function burnPortalEnergyToken(address _recipient, uint256 _amount) external nonReentrant {
function updateMaxLockDuration() external {
```

## Recommendations

For best security practices, consider declaring events as often as possible at the end of a function. Events can be used to detect the end of the operation.

## Team Response

N/A

## [I-02] Function Ordering Does not Follow the Solidity Style Guide

## Severity

Informational

## Description

One of the guidelines mentioned in the style guide is to order functions in a specific way to improve readability and maintainability. By following this order, you can achieve a consistent and logical structure in your contract code.

## Location of Affected Code

File: [contracts/Portal.sol](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol)

## Recommendation

It is recommended to follow the recommended order of functions in Solidity, as outlined in the Solidity style guide (https://docs.soliditylang.org/en/latest/style-guide.html#order-of-layout).

Functions should be grouped according to their visibility and ordered:

1. constructor
2. external
3. public
4. internal
5. private

## Team Response

N/A

## [I-03] Redundant `return` Statements in Functions With Named Returns

## Severity

Informational

## Description

If a function defines a named return variable, it is not necessary to explicitly return it. It will automatically be returned at the end of the function.

## Location of Affected Code

File: [contracts/Portal.sol](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol)

```solidity
function getBurnValuePSM(uint256 _amount) public view returns(uint256 burnValue) {
function getUpdateAccount(address _user, uint256 _amount) public view returns(
function quoteforceUnstakeAll(address _user) public view returns(uint256 portalEnergyTokenToBurn) {
function getPendingRewards(address _rewarder) public view returns(uint256 claimableReward){
```

## Recommendation

Consider removing the redundant `return` statements in functions with named returns.

## Team Response

N/A

## [I-04] Large Numeric Literals Can Use Days Instead of Seconds

## Severity

Informational

## Description

The `Portal` contract contains large numeric literals that can be represented with days instead of seconds or at least use underscores for readability.

## Location of Affected Code

File: [contracts/Portal.sol#L61-L62](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol#L61-L62)

```solidity
uint256 constant private secondsPerYear = 31536000;
uint256 public maxLockDuration = 7776000;
```

## Recommendations

Consider inserting underscores for improved readability.

File: [contracts/Portal.sol#L61-L62](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol#L61-L62)

```diff
-  uint256 constant private secondsPerYear = 31536000;
+ uint256 private constant SECONDS_PER_YEAR = 365 days;

-  uint256 public maxLockDuration = 7776000;
+  uint256 private constant MAX_LOCK_DURATION = 90 days;
```

## Team Response

N/A

## [I-05] File Missing NatSpec Comments

## Severity

Informational

## Description

The `MintBurnToken.sol` contract lacks NatSpec comments. Given that NatSpec is an important part of code documentation, this affects code comprehension, audibility, and usability.

This might lead to confusion for other auditors/developers that are interacting with the code.

## Location of Affected Code

File: [contracts/MintBurnToken.sol](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/MintBurnToken.sol)

## Recommendations

Consider adding full NatSpec comments for all functions where missing to have complete code documentation for future use.

## Team Response

N/A

## [I-06] Useless Authorization Check in `_burnPortalEnergyToken` Function

## Severity

Informational

## Description

The `_burnPortalEnergyToken` function is only called by `forceUnstakeAll()`, in which the account existence check is performed right at the beginning. This is not only gas inefficiency but also burdens code readability.

## Location of Affected Code

File: [contracts/Portal.sol#L703](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol#L703)

```solidity
require(accounts[_user].isExist == true);
```

## Recommendations

Consider removing the redundant validation.

## Team Response

N/A

## [I-07] Event Names Should Begin With Capital Letters

## Severity

Informational

## Description

According to the [Solidity style guide](https://docs.soliditylang.org/en/latest/style-guide.html), events should be named using the CapWords style.

## Location of Affected Code

File: [contracts/Portal.sol#L110-L111](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol#L110-L111)

```solidity
event portalEnergyBuyExecuted(address indexed, uint256 amount);
event portalEnergySellExecuted(address indexed, uint256 amount);
```

## Recommendations

Use capital letters instead of mixed for the two event declarations mentioned above.

## Team Response

N/A

## [I-08] Replace magic numbers with constants

## Severity

Informational

## Description

The contract contains various magic numbers, i.e., unnamed numerical constants. The use of magic numbers is generally considered an anti-pattern and should be avoided.

## Location of Affected Code

File: contracts/Portal.sol#L375-L376

```solidity
1689206400,
115792089237316195423570985008687907853269984665640564039457584007913129639935,
```

File: contracts/Portal.sol#L394-L395

```solidity
1689206400,
115792089237316195423570985008687907853269984665640564039457584007913129639935,
```

## Recommendations

Generally, numbers should be written as a constant at the top of the contract.

## Team Response

N/A

## [I-09] `constant`/`immutable`s should use `UPPER_CASE_WITH_UNDERSCORES`

## Severity

Informational

## Description

According to the [Solidity style guide](https://docs.soliditylang.org/en/latest/style-guide.html), variable names for `constant`/`immutable`s should use UPPER_CASE_WITH_UNDERSCORES.

## Location of Affected Code

File: contracts/Portal.sol#L55-L61

```solidity
address immutable public bToken;                        // address of the bToken which is the receipt token from bootstrapping
address immutable public portalEnergyToken;             // address of portalEnergyToken, the ERC20 representation of portalEnergy
address immutable public tokenToAcquire;                // address of PSM token
uint256 immutable public amountToConvert;               // constant amount of PSM tokens required to withdraw yield in the contract
uint256 immutable public terminalMaxLockDuration;       // terminal maximum lock duration of user´s balance in seconds
uint256 immutable public creationTime;                  // time stamp of deployment
uint256 constant private secondsPerYear = 31536000;     // seconds in a 365 day year
```

File: contracts/Portal.sol#L67-L80

```solidity
address immutable public principalToken;                // address of the token accepted by the strategy as deposit (HLP)
address payable private constant compounderAddress = payable (0x8E5D083BA7A46f13afccC27BFB7da372E9dFEF22);

address payable private constant HLPstakingAddress = payable (0xbE8f8AF5953869222eA8D39F1Be9d03766010B1C);
address private constant HLPprotocolRewarder = 0x665099B3e59367f02E5f9e039C3450E31c338788;
address private constant HLPemissionsRewarder = 0x6D2c18B559C5343CB0703bB55AADB5f22152cC32;

address private constant HMXstakingAddress = 0x92E586B8D4Bf59f4001604209A292621c716539a;
address private constant HMXprotocolRewarder = 0xB698829C4C187C85859AD2085B24f308fC1195D3;
address private constant HMXemissionsRewarder = 0x94c22459b145F012F1c6791F2D729F7a22c44764;
address private constant HMXdragonPointsRewarder = 0xbEDd351c62111FB7216683C2A26319743a06F273;

// bootstrapping related
uint256 immutable private fundingPhaseDuration;         // seconds that the funding phase lasts before Portal can be activated
```

File: contracts/Portal.sol#L85-L87

```solidity
uint256 immutable public fundingRewardRate;             // baseline return on funding the Portal
uint256 immutable private fundingExchangeRatio;         // amount of portalEnergy per PSM for calculating k during the funding process
uint256 constant public fundingRewardShare = 10;        // 10% of the yield goes to the funding pool until investors are paid back
```

## Recommendations

Consider using UPPER_CASE_WITH_UNDERSCORES for all of the above `constant`/`immutable`s.

## Team Response

N/A

## [I-10] Use Named Imports Instead of Plain Imports

## Severity

Informational

## Description

It’s possible to name the imports to improve code readability.

E.g. import `import "@openzeppelin/contracts/security/ReentrancyGuard.sol";`; can be rewritten as `import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";`

## Location of Affected Code

File: [contracts/MintBurnToken.sol##L4-L6](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/MintBurnToken.sol#L4-L6)

```solidity
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
```

## Recommendation

Consider using named imports.

## Team Response

N/A

## [I-11] Public functions not called by the contract should be external

## Severity

Informational

## Description

For the sake of clarity, public functions not called by the contract should be declared external instead.

## Location of Affected Code

File: contracts/MintBurnToken.sol#L11

```solidity
function mint(address to, uint256 amount) public onlyOwner {
```

File: contracts/Portal.sol#L495

```solidity
function quoteBuyPortalEnergy(uint256 _amountInput) public view returns(uint256) {
```

File: contracts/Portal.sol#L511

```solidity
function quoteSellPortalEnergy(uint256 _amountInput) public view returns(uint256) {
```

File: contracts/Portal.sol#L773

```solidity
function quoteforceUnstakeAll(address _user) public view returns(uint256 portalEnergyTokenToBurn) {
```

File: contracts/Portal.sol#L791

```solidity
function getBalanceOfToken(address _token) public view returns (uint256) {
```

File: contracts/Portal.sol#L799

```solidity
function getPendingRewards(address _rewarder) public view returns(uint256 claimableReward){
```

## Recommendations

Consider changing the visibility modifiers as follows:

File: contracts/MintBurnToken.sol#L11

```diff
- function mint(address to, uint256 amount) public onlyOwner {
+ function mint(address to, uint256 amount) external onlyOwner {
```

File: contracts/Portal.sol#L495

```diff
- function quoteBuyPortalEnergy(uint256 _amountInput) public view returns(uint256) {
+ function quoteBuyPortalEnergy(uint256 _amountInput) external view returns (uint256) {
```

File: contracts/Portal.sol#L511

```diff
- function quoteSellPortalEnergy(uint256 _amountInput) public view returns(uint256) {
+ function quoteSellPortalEnergy(uint256 _amountInput) external view returns (uint256) {
```

File: contracts/Portal.sol#L773

```diff
- function quoteforceUnstakeAll(address _user) public view returns(uint256 portalEnergyTokenToBurn) {
+ function quoteforceUnstakeAll(address _user) external view returns (uint256 portalEnergyTokenToBurn) {
```

File: contracts/Portal.sol#L791

```diff
- function getBalanceOfToken(address _token) public view returns (uint256) {
+ function getBalanceOfToken(address _token) external view returns (uint256) {
```

File: contracts/Portal.sol#L799

```diff
- function getPendingRewards(address _rewarder) public view returns(uint256 claimableReward){
+ function getPendingRewards(address _rewarder) external view returns (uint256 claimableReward) {
```

## Team Response

N/A

## [I-12] No Need to Initialize Variables with Default Values

## Severity

Informational

## Description

If a variable is not set/initialized, the default value is assumed (0, false, 0x0 … depending on the data type). Saves `8 gas` per instance.

## Location of Affected Code

File: [contracts/Portal.sol#L64](https://github.com/PossumLabsCrypto/Portals/blob/03b6a8272ac9ff8afe76c8748aa16f970ba1a338/contracts/Portal.sol#L64)

```solidity
bool public isActivePortal = false;
```

## Recommendations

```diff
- bool public isActivePortal = false;
+ bool public isActivePortal;
```

## Team Response

N/A

## [I-13] Confusing Name of `bToken` and `PortalEnergy` Tokens' Base Contracts

## Severity

Informational

## Description

Both `bToken` and `portalEnergy` will use the basic `MintBurnToken` contract. However, its name is confusing and does not directly communicate the correct usage.
Additionally, the immutable variable `tokenToAcquire` , points to the address of the PSM token. Using this variable name might confuse developers/other auditors in a sense that there might be several tokens to be acquired.

## Location of Affected Code

[MintBurnToken.sol](https://github.com/PossumLabsCrypto/Portals/blob/main/contracts/MintBurnToken.sol)

## Recommendations

Consider changing the name of the `MintBurnToken` contract to one, that easily describes what tokens it will be used for. It is also recommended that another name is used for the PSM token address instead of `tokenToAcquire`, for example, `PSM`.

## [I-14] Use a Fixed Solidity Version

## Severity

Informational

## Description

Currently, the `MintBurnToken` and `Portal.sol` contracts use version `^0.8.19`. Use the latest stable Solidity version to get all compiler features, bug fixes, and optimizations. However, when upgrading to a new Solidity version, it's crucial to carefully review the release notes, consider any breaking changes, and thoroughly test your code to ensure compatibility and correctness. Additionally, be aware that some features or changes may not be backward compatible, requiring adjustments in your code.

## Location of Affected Code

[MintBurnToken.sol] (https://github.com/PossumLabsCrypto/Portals/blob/main/contracts/MintBurnToken.sol)
[Portal.sol] (https://github.com/PossumLabsCrypto/Portals/blob/main/contracts/Portal.sol)

## Recommendations

Use the latest Solidity version and lock it (do not use the `^` sign when declaring it).

## [I-15] Checks Can be Exported Into Separate Modifiers

## Severity

Informational

## Description

There are several instances in the `Portal.sol` contract, where checks are made for the `isActivePortal`, `isExist`. It is a good practice to export checks that are used more than once into their own modifier.

## Location of Affected Code

[Portal.sol](https://github.com/PossumLabsCrypto/Portals/blob/main/contracts/Portal.sol)

## Recommendations

Make individual modifiers for the three checks and include those in the functions in which they are used.

```solidity
modifier activePortalCheck() {
    if (!isActivePortal) {
        revert PortalNotActive();
    }
    _;
}

modifier nonActivePortalCheck(){
    if (isActivePortal) {
      revert PortalAlreadyActive();
    }
    _;
}

modifier existingAccount (){
    if (!accounts[msg.sender].isExist) {
        revert AccountDoesNotExist();
    }
    _;
}

function stake(uint256 _amount) external nonReentrant activePortalCheck {
function contributeFunding(uint256 _amount) external nonReentrant nonActivePortalCheck {
function burnBtokens(uint256 _amount) external nonReentrant activePortalCheck{
function activatePortal() external nonActivePortalCheck {
function stake(uint256 _amount) external nonReentrant existingAccount {
function unstake(uint256 _amount) external nonReentrant existingAccount {
function forceUnstakeAll() external nonReentrant existingAccount {
function buyPortalEnergy(uint256 _amountInput, uint256 _minReceived) external nonReentrant existingAccount {
function sellPortalEnergy(uint256 _amountInput, uint256 _minReceived) external nonReentrant existingAccount {

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Possum |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Possum-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

