---
# Core Classification
protocol: Yeet Cup
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44211
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Yeet-Cup-Security-Review.md
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

[L-06] Avoid Drafting the Same Winner Multiple Times by the Increasing Pseudo-Randomness in `Yeetback.sol`

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

In the `draftWinners()` method, 10 winners are drafted in a loop based on `randomData` which is the `keccak256` hash of `smallNumbers`.
Each iteration's `smallNumbers` are derived from the base entropy given by `randomNumber` and could potentially be the same in multiple iterations leading to drafting the same winner multiple times.

## Location of Affected Code

File: [src/Yeetback.sol#L66](https://github.com/0xKingKoala/contracts/blob/f43ad283290293e18e5d9ab0c9d56e29bffa3eb3/src/Yeetback.sol#L66)

```solidity
bytes32 randomData = keccak256(abi.encodePacked(smallNumbers));
```

## Recommendation

In order to increase the pseudo-randomness based on the entropy given by `randomNumber`, it is recommended to hash further data like the loop counter `i` and the `block.timestamp`.

```diff
- bytes32 randomData = keccak256(abi.encodePacked(smallNumbers));
+ bytes32 randomData = keccak256(abi.encodePacked(smallNumbers, i, block.timestamp));
```

## Team Response

Fixed as suggested

## [R-01] Miscellaneous Remarks

- The codebase in scope does not fund the `Reward` contract with YEET tokens. Make sure the `Reward` contract is appropriately funded during operation to avoid insolvency.
- Set the `yeetardsNFTsAddress` in the constructor of the Yeet contract, similar to other addresses which are required for operation. Otherwise, the `yeet()` method will fail when used after deployment without `yeetardsNFTsAddress` being set.
- Adding a start delay on each new round. Currently, a user could call `restart()` and `yeet()` within the same transaction which is an unfair advantage over other participants, since the first one to `yeet()` is added to the `Yeetback` draw for the lowest price.

## [I-01] `Yeet.sol` Does Not Compile

## Description

```console
Error (5132): Different number of arguments in return statement than in returns declaration.
   --> src/Yeet.sol:309:9:
    |
309 |         return (_lastYeeted, _lastYeetedAt, _potToWinner, _potToYeetback, _nrOfYeets, _yeetTimeInSeconds, _endOfYeetTime);
    |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

## Recommendation

Add the missing `uint256` return declaration:

```diff
+ function getTotals() public view returns (address, uint256, uint256, uint256, uint256, uint256, uint256) {
- function getTotals() public view returns (address, uint256, uint256, uint256, uint256, uint256) {
     return (_lastYeeted, _lastYeetedAt, _potToWinner, _potToYeetback, _nrOfYeets, _yeetTimeInSeconds, _endOfYeetTime);
 }
```

## [I-02] Unnecessary Imports and Variables

## Description

- There is no point in importing `Ownable` in contracts that inherit from other contracts that already have imported it.
- Consider removing the testing import - `import "forge-std/console.sol";` from `Yeet`, `Stake` and `Reward` contracts.
- The `isInitialized` variable in `YeetToken` is defined and never used, consider removing it.
- Unnecessary balance sufficiency check in `claim()` in Reward.sol.
- In `Yeet.sol:L322`, cache the global constant `LATEST_HISTORY_LENGTH` instead of shadowing it with a local magic number.
- The `tokenContract` (YEET token) is not used at all within the `Yeet` contract. Reconsider any intended interaction.

## [I-03] Inconsistency with the Licenses

## Description

`NFTVesting`, `Stake`, `RewardSettings` and `YeetGameSettings` are missing SPDX License Identifier, the other contracts except for `YeetToken` are `UNLICENSED`.

SPDX License Identifiers are crucial because they provide clear and standardized information about the licensing terms under which a software or contract is distributed. This information helps users and developers understand their rights and obligations when using or modifying the code. Additionally, SPDX License Identifiers facilitate compliance with open-source licensing requirements, promote legal clarity, and encourage collaboration within the software development community.

## Recommendation

Consider selecting an appropriate license for your contracts and consistently applying it across all contracts to ensure legal clarity and foster a collaborative development environment.

## [I-04] Some Event Parameters Are Not `indexed`

## Description

Some event parameters are not `indexed`. While this does not pose any threat to the code, it makes it cumbersome for the off-chain scripts to efficiently filter them. Making the event parameters `indexed` will improve the off-chain services’ ability to search and filter them.

## Location of Affected Code

File: Reward.sol

```solidity
    event EpochEnded(uint256 epoch, uint256 timestamp);
```

File: RewardSettings.sol

```solidity
    event YeetRewardSettingsChanged(uint256 maxCapPerWalletPerEpoch);
```

File: YeetGameSettings.sol

```solidity
event YeetSettingsChanged(
        uint256 yeetTimeSeconds,
        uint256 potDivision,
        uint256 taxPerYeet,
        uint256 taxToStakers,
        uint256 taxToPublicGoods,
        uint256 taxToLPStaking,
        uint256 taxToTreasury,
        uint256 yeetbackPercentage
    )
```

File: Yeetback.sol

```solidity
  event RandomNumberRequested(uint64 sequenceNumber);
    event YeetbackAdded(uint256 round, uint256 amount);
    event YeetbackWinner(uint256 round, address winner, uint256 amount);
```

## Recommendation

Consider making up to three of the most important parameters in these events `indexed`.

## [I-05] Ownership Role Transfer Function Implement `Single-Step Role` Transfer

## Description

The current ownership transfer process for all the contracts inheriting from `Ownable` involves the current owner calling the `transferOwnership()` function. If the nominated EOA account is not a valid account, it is entirely possible that the owner may accidentally transfer ownership to an uncontrolled account, losing access to all functions with the `onlyOwner` modifier.

## Location of Affected Code

File: src/OnlyYeetContract.sol

File: src/RewardSettings.sol

File: src/Yeetback.sol

File: src/YeetGameSettings.sol

File: src/YeetToken.sol

## Recommendation

It is recommended to implement a two-step process where the owner nominates an account and the nominated account needs to call an `acceptOwnership()` function for the transfer of the ownership to fully succeed. This ensures the nominated EOA account is a valid and active account. This can be easily achieved by using OpenZeppelin’s `Ownable2Step` contract instead of `Ownable`.

## [I-06] Some Write Functions Do Not Emit Events

## Description

Some of the functions that change the state of the game do not emit events. This essentially disables the ability for off-chain monitoring which could potentially result in inconsistent data tracking and acquisition.

## Location of Affected Code

File: NFTVesting.sol

```solidity
function claim(uint256 tokenId) public {
function claimMany(uint256[] calldata tokenIds) public {
```

File: Reward.sol

```solidity
function addYeetVolume(address user, uint256 amount) external onlyYeetOwner {
```

File: Stake.sol

```solidity
function depositReward() external payable {
function startUnstake(uint256 unStakeAmount) external {
function stake(uint256 amount) external {
function unstake(uint256 index) external {
function rageQuit(uint256 index) external {
function reStake() external {
function claim() external {
```

File: Yeet.sol

```solidity
function setPublicGoodsAddress(address _publicGoodsAddress) external onlyOwner {
function setLpStakingAddress(address _lpStakingAddress) external onlyOwner {
function setTreasuryRevenueAddress(address _treasuryRevenueAddress) external onlyOwner {
function setYeetardsNFTsAddress(address _yeetardsNFTsAddress) external onlyOwner {
```

File: Yeetback.sol

```solidity
function draftWinners(uint256 randomNumber, uint256 round) private {
function addYeetsInRound(uint256 round, address user) public onlyOwner {
function claim(uint256 round) public {
```

## Recommendation

Ensure that each state-altering method emits a suitable event to adhere to established best practices.

## [G-01] `getWinners()` Method Missing Pagination

Add pagination to the `getWinners()` method of the `Yeet` contract to avoid perpetually growing gas costs of this call.

## [G-02] Cache array length outside of a loop

If not cached, the solidity compiler will always read the length of the array during each iteration. That is, if it is a storage array, this is an extra sload operation (100 additional extra gas for each iteration except for the first) and if it is a memory array, this is an extra mload operation (3 additional gas for each iteration except for the first).

File: NFTVesting.sol

```solidity
for (uint256 i = 0; i < tokenIds.length; i++) {
for (uint256 i = 0; i < tokenIds.length; i++) {
```

File: Stake.sol

```solidity
for (uint i = _index; i < arr.length - 1; i++) {
```

## [G-03] Don't initialize variables with a default value

File: MockNFTContract.sol

```solidity
for (uint256 i = 0; i < amount; i++) {
```

File: NFTVesting.sol

```solidity
for (uint256 i = 0; i < tokenIds.length; i++) {
uint256 amountClaimable = 0;
for (uint256 i = 0; i < tokenIds.length; i++) {
```

File: Reward.sol

```solidity
uint256 totalClaimable = 0;
```

File: Stake.sol

```solidity
uint256 unlockedAmount = 0;
uint256 lockedAmount = 0;
```

File: Yeet.sol

```solidity
for (uint256 i = 0; i < length; i++) {
```

File: Yeetback.sol

```solidity
for (uint8 i = 0; i < 10; i++) {
```

## [G-04] Using `private` rather than `public` for constants, saves gas

If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table

File: Reward.sol

```solidity
uint256 public constant DISTRIBUTION_CHANGE = 7 days;
uint256 public constant STARTING_TOKEN_COUNT = 275_106 * 10 ** 18;
uint256 public constant EPOCH_LENGTH = 1 days;
uint256 public constant DECAY_RATE = 50;
uint256 public constant SCALE_FACTOR = 1e4;
```

File: Stake.sol

```solidity
uint public constant VESTING_PERIOD = 10 days;
```

## [G-05] Use != 0 instead of > 0 for unsigned integer comparison

File: Reward.sol

```solidity
require(amountEarned > 0, "Nothing to claim");
```

File: Stake.sol

```solidity
require(unlockedAmount > 0, "No unlocked amount");
require(reward > 0, "No rewards to claim");
require(reward > 0, "No rewards to claim");
```

File: Yeet.sol

```solidity
require(winnings[msg.sender] > 0, "Yeet: No winnings to claim");
require(publicGoodsAmount > 0, "Yeet: No public goods to pay out");
require(lpStakingAmount > 0, "Yeet: No LP staking to pay out");
require(treasuryRevenueAmount > 0, "Yeet: No Treasury revenue to pay out");
```

File: Yeetback.sol

```solidity
require(winner.amount > 0, "Yeetback: No winnings to claim");
if (winner.amount > 0 && !winner.claimed) {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Yeet Cup |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Yeet-Cup-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

