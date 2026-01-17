---
# Core Classification
protocol: Futaba
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44058
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Futaba-Security-Review.md
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

[L-10] Ownership Role Transfer Function Implement `Single-Step Role` Transfer

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Description

The current ownership transfer process for all the contracts inheriting from `Ownable` involves the current owner calling the `transferOwnership()` function. If the nominated EOA account is not a valid account, it is entirely possible that the owner may accidentally transfer ownership to an uncontrolled account, losing access to all functions with the `onlyOwner` modifier.

## Location of Affected Code

File: [contracts/Gateway.sol#L23](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol#L23)

File: [contracts/ChainlinkLightClient.sol#L19](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol#L19)

## Recommendation

It is recommended to implement a two-step process where the owner nominates an account and the nominated account needs to call an `acceptOwnership()` function for the transfer of the ownership to fully succeed. This ensures the nominated EOA account is a valid and active account. This can be easily achieved by using OpenZeppelin’s `Ownable2Step` contract instead of `Ownable`.

File: [contracts/Gateway.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol)

```diff
- import "@openzeppelin/contracts/access/Ownable.sol";
+ import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";

- contract Gateway is IGateway, Ownable, ReentrancyGuard, GelatoRelayContextERC2771 {
+ contract Gateway is IGateway, Ownable2Step, ReentrancyGuard, GelatoRelayContextERC2771 {
```

File: [contracts/ChainlinkLightClient.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol)

```diff
- import "@openzeppelin/contracts/access/Ownable.sol";
+ import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";

- contract ChainlinkLightClient is ILightClient, IChainlinkLightClient, Ownable {
+ contract ChainlinkLightClient is ILightClient, IChainlinkLightClient, Ownable2Step {
```

## Team Response

Acknowledged and fixed by changing from `Ownable` to `Ownable2Step`.

## [I-01] Missing Event Emissions

## Severity

Informational

## Description

It has been observed that important functionalities are missing an emitting event - `setOracle()` and `updateHeader()` functions in the `ChainlinkLightClient.sol`. For the `updateHeader()` method there is an event when the state root is updated, consider adding another one in the if statement to note that the state is up-to-date.

Events are a method of informing the transaction initiator about the actions taken by the called function. An event logs its emitted parameters in a specific log history, which can be accessed outside of the contract using some filter parameters.

## Location of Affected Code

File: [contracts/ChainlinkLightClient.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol)

```solidity
function updateHeader(QueryType.OracleResponse[] memory responses) external override onlyOracle {
function setOracle(address _oracle) public onlyOwner {
```

## Recommendation

For best security practices, consider declaring events as often as possible at the end of a function. Events can be used to detect the end of the operation.

## Team Response

Acknowledged and fixed by adding an event even if the state has already been saved in `updateHeader()` and adding an event when `Oracle` is registered in `setOracle()`.

## [I-02] Unused Imports Affect Readability

## Severity

Informational

## Description

There are a few unused imports on the codebase. These imports should be cleaned up from the code if they have no purpose.

## Location of Affected Code

File: [contracts/Gateway.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol)

```solidity
import "@openzeppelin/contracts/utils/Strings.sol";
import "hardhat/console.sol";

import {Address} from "@openzeppelin/contracts/utils/Address.sol";
using Address for address payable;
```

File: [contracts/ChainlinkOracle.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol)

```solidity
import "./interfaces/ILightClient.sol";
import "hardhat/console.sol";
```

## Recommendation

Remove the unused imports.

File: [contracts/Gateway.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol)

```diff
- import "@openzeppelin/contracts/utils/Strings.sol";
- import "hardhat/console.sol";

- import {Address} from "@openzeppelin/contracts/utils/Address.sol";
- using Address for address payable;
```

File: [contracts/ChainlinkOracle.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol)

```diff
- import "./interfaces/ILightClient.sol";
- import "hardhat/console.sol";
```

## Team Response

Acknowledged and fixed by removing unused imports.

## [I-03] Use Locked Solidity Version Pragma

## Severity

Informational

## Description

Currently, version `^0.8.9` is used in the codebase. Contracts should be deployed with the same compiler version that they have been tested with. Locking the pragma helps to ensure that contracts do not accidentally get deployed using, for example, either an outdated compiler version that might introduce bugs or a compiler version too recent that has not been extensively tested yet.

## Location of Affected Code

All smart contracts.

## Recommendation

Consider locking the version pragma to the same Solidity version used during development and testing `(0.8.19)`.

```diff
- pragma solidity ^0.8.9;
+ pragma solidity 0.8.19;
```

## Team Response

Acknowledged and fixed by correcting the locked version.

## [I-04] Mixed Use of Custom Errors and Revert Strings

## Severity

Informational

## Description

In some parts of the code, `custom errors` are declared and later used [Custom Errors](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol#L238), while in other parts, classic revert strings are used in [Require Statements](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol#L291).

Instead of using error strings, custom errors can be used, which would reduce deployment and runtime costs.

## Location of Affected Code

Most contracts.

## Recommendation

Consider using only custom errors as they are more gas-efficient.

## Team Response

Acknowledged and fixed by changing to custom errors.

## [I-05] Missing Error Messages in `require()` Statements

## Severity

Informational

## Description

When encountering transaction failures or unexpected behavior, the utilization of informative error messages is beneficial for troubleshooting exceptional conditions. Otherwise, inadequate error messages can lead to confusion and unnecessary delays during exploits or emergency situations.

## Location of Affected Code

File: [contracts/lib/RLPReader.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/RLPReader.sol)

```solidity
33: require(hasNext(self));
74: require(isList(self));
114: require(isList(item));
195: require(item.len == 1);
215: require(item.len == 21);
221: require(item.len > 0 && item.len <= 33);
241: require(item.len == 33);
253: require(item.len > 0);
270: require(item.len > 0);
```

## Recommendation

Consider adding a descriptive reason in an error string.

## Team Response

Acknowledged and fixed by changing to custom errors too.

## [I-06] Update External Dependency to the Latest Version

## Severity

Informational

## Description

Update the versions `@openzeppelin/contracts` and `@chainlink/contracts` to be the latest in `package.json`.

## Location of Affected Code

According to package.json, `@openzeppelin/contracts` is currently set to `^4.8.2` and `@chainlink/contracts` is `^0.6.1`.

## Recommendation

We also recommend double-checking the versions of other dependencies as a precaution, as they may include important bug fixes.

## Team Response

Acknowledged and fixed by updating the version (If there are no problems after confirming the operation including testing).

## [I-07] Missing/Incomplete NatSpec Comments

## Severity

Informational

## Description

(`@notice`, `@dev`, `@param` and `@return`) are missing in some functions. Given that NatSpec is an important part of code documentation, this affects
code comprehension, audibility, and usability.

This might lead to confusion for other auditors/developers that are interacting with the code.

## Location of Affected Code

In some contacts.

## Recommendation

Consider adding in full NatSpec comments for all functions where missing to have complete code documentation for future use.

## Team Response

Acknowledged and fixed by adding the missing NatSpec.

## [I-08] Use Named Imports Instead of Plain Imports

## Severity

Informational

## Description

It’s possible to name the imports to improve code readability.

E.g. import `import "@openzeppelin/contracts/security/ReentrancyGuard.sol";`; can be rewritten as `import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";`

## Location of Affected Code

Most contracts.

## Recommendation

Consider using named imports.

`import "@openzeppelin/contracts/security/ReentrancyGuard.sol";` -> `import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";`

`import "./interfaces/IGateway.sol";` -> `import {IGateway} from "./interfaces/IGateway.sol";`

`import "./interfaces/ILightClient.sol";` -> `import {ILightClient} from "./interfacesILightClient sol";`

`import "./interfaces/IReceiver.sol";` -> `import {IReceiver} from "./interfaces/IReceiver.sol";`

`import "./QueryType.sol";` -> `import {QueryType} from "./QueryType.sol";`

`import "./interfaces/IChainlinkLightClient.sol";` -> `import {IChainlinkLightClient} from "./interfaces/IChainlinkLightClient.sol";`

`import "./interfaces/IExternalAdapter.sol";` -> `import {IExternalAdapter} from "./interfaces/IExternalAdapter.sol";`

`import "./lib/TrieProofs.sol";` -> `import {TrieProofs} from "./lib/TrieProofs.sol";`

`import "./lib/RLPReader.sol";` -> `import {RLPReader} from "./lib/RLPReader.sol";`

`import "./lib/EthereumDecoder.sol";` -> `import {EthereumDecoder} from "./lib/EthereumDecoder.sol";`

`import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";` -> `import {ConfirmedOwner} from "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";`

## Team Response

Acknowledged and fixed by modifying the Import statement.

## [I-09] Create a Modifier Only if it will be Used in More than One Place

## Severity

Informational

## Description

There is no need to create a separate modifier unless it will be used in more than one place. If this is not the case, simply add the modifier code to the function instead.

## Location of Affected Code

File: [contracts/ChainlinkOracle.sol#L205-L211](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol#L205-L211)

```solidity
modifier onlyLightClient() {
  require(
    msg.sender == lightClient,
    "Futaba: only light client can call this function"
  );
  _;
}
```

File: [contracts/ChainlinkLightClient.sol#L336-L339](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol#L336-L339)

```solidity
modifier onlyOracle() {
  require(msg.sender == oracle, "Futaba: onlyOracle - not oracle");
  _;
}
```

## Recommendation

Add the modifier logic into the function directly.

## Team Response

Acknowledged and fixed by removing modifier and adding a process to perform verification at the beginning of the function.

## [I-10] Choose the Proper Functions Visibility

## Severity

Informational

## Description

It is best practice to mark functions that are not called internally as `external` instead of `public` and `private` instead of `internal` when they should only be called inside the given contract.

## Location of Affected Code

File: [contracts/ChainlinkLightClient.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol)

```solidity
139: function verify(
277: function setOracle(address _oracle) public onlyOwner {
281: function getOracle() public view returns (address) {
```

File: [contracts/ChainlinkOracle.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol)

```solidity
134: function fulfill(
147: function setClient(address _client) public onlyOwner {
153: function getClient() public view returns (address) {
157: function setLinkToken(address _tokenAddress) public onlyOwner {
164: function getLinkToken() public view returns (address) {
168: function setOracle(address _oracle) public onlyOwner {
175: function getOracle() public view returns (address) {
179: function setJobId(bytes32 _jobId) public onlyOwner {
186: function getJobId() public view returns (bytes32) {
190: function setFee(uint256 _fee) public onlyOwner {
197: function getFee() public view returns (uint256) {
318: function getStorageValue(StorageProof memory storageProof) internal pure returns (bytes32) {
335: function checkRoot(Proof[] memory proofs) internal view {
```

## Recommendation

- Consider using `external` modifier for clarity's sake if the function is not called inside the contract.
- Consider using `private` modifier for clarity's sake if the function can only be called inside the given contract.

## Team Response

Acknowledged and fixed by changing the modifier of the function in question from `public` to `external` and from `internal` to `private`.

## [I-11] Complete the `TODO` regarding the `NatSpec`

## Severity

Informational

## Description

NatSpec is an important part of code documentation, this affects code comprehension, audibility, and usability.

This might lead to confusion for other auditors/developers that are interacting with the code.

## Location of Affected Code

File: [contracts/Gateway.sol#L20](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol#L20)

```solidity
// #TODO: Add @notice & @param description for each: FUNCTION + EVENT + ERROR declaration
```

File: [contracts/ChainlinkLightClient.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol)

```solidity
function updateHeader(
function setOracle(address _oracle) public onlyOwner {
function getOracle() public view returns (address) {
```

File: [contracts/lib/EthereumDecoder.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/EthereumDecoder.sol)

File: [contracts/lib/TrieProofs.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/TrieProofs.sol)

## Recommendation

Consider adding full NatSpec comments for all functions where missing to have complete code documentation for future use.

## Team Response

Acknowledged and fixed by adding the missing NatSpec.

## [I-12] Remove Testing Logging

## Severity

Informational

## Description

The smart contract imports the Hardhat console library using import `hardhat/console.sol;`. While the Hardhat console is useful for debugging during the development and testing phases, it is generally not recommended to be included in the production code. The inclusion of debugging tools in production can lead to additional gas costs.

## Location of Affected Code

File: [contracts/ChainlinkOracle.sol#L10](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol#L10)

```solidity
import "hardhat/console.sol";
```

File: [scripts/getProof.ts](https://github.com/Futaba-Labs/Futaba-Relayer/blob/c07005ac8fc24fd8a33dcce793062e210e5e759e/scripts/getProof.ts)

## Recommendation

To maintain a clean, secure, and efficient production environment, it is recommended to exclude the Hardhat console import from the final version of the contract.

File: [contracts/ChainlinkOracle.sol#L10](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol#L10)

```diff
- import "hardhat/console.sol";
```

File: [scripts/getProof.ts](https://github.com/Futaba-Labs/Futaba-Relayer/blob/c07005ac8fc24fd8a33dcce793062e210e5e759e/scripts/getProof.ts)

```diff
- console.log("balance:", balance);
- // console.log("accountProof:", accountProof);
- // console.log("storageProofs:", storageProofs);
- // console.log("proof:", proof);
```

## Team Response

Acknowledged and fixed by removing console import statement and `console.log()`.

## [I-13] All Contracts Are Missing License

## Severity

Informational

## Description

It seems like there is an issue with the licenses for the Smart Contracts in the audit scope. It is crucial to have proper licensing in place to ensure that the code is used and distributed legally.

## Location of Affected Code

All smart contracts.

## Recommendation

To address this, you should consider adding an appropriate license to the smart contracts. Remember to consult with a legal professional if you have specific legal concerns or if you're unsure which license is best for your project.

## Team Response

Acknowledged and fixed by adding a specific license (to be discussed, as it has not yet been decided).

## [I-14] Unit Tests are Incomplete in Futaba Relayer

## Severity

Informational

## Description

The absence of unit tests for essential components like the `Database Client`, `Listener`, and `Relay` is a concern in the `Futaba Relayer`. To ensure the system's integrity and performance, it is imperative that comprehensive testing is implemented.

## Location of Affected Code

File: [client/DatabaseClient.test.ts](https://github.com/Futaba-Labs/Futaba-Relayer/blob/main/src/client/DatabaseClient.test.ts)

File: [handler/eventHandler.test.ts](https://github.com/Futaba-Labs/Futaba-Relayer/blob/main/src/handler/eventHandler.test.ts)

File: [relayer/listener.test.ts](https://github.com/Futaba-Labs/Futaba-Relayer/blob/main/src/relayer/listener.test.ts)

File: [relayer/relay.test.ts](https://github.com/Futaba-Labs/Futaba-Relayer/blob/main/src/relayer/relay.test.ts)

## Recommendation

Consider implementing thorough unit tests for the `Database Client`, `Listener`, and `Relay` components to ensure the system's stability and security.

## Team Response

Acknowledged and fixed by adding Relayer test.

## [I-15] Remove `lightClient != address(0)` Check for `ChainlinkOracle.fulfill()` Function

## Severity

Informational

## Description

Remove this check if you decide to implement a zero address check in the `constructor` and `setClient()` functions as proposed above in `L-07` finding.

## Location of Affected Code

File: [contracts/ChainlinkOracle.sol#L142](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkOracle.sol#L142)

```solidity
require(lightClient != address(0), "Futaba: invalid ligth client");
```

## Recommendation

It is recommended to remove zero address check for `lightClient.sol` contract.

```diff
- require(lightClient != address(0), "Futaba: invalid ligth client");
```

## Team Response

Acknowledged and fixed by removing the require statement regarding the `lightClient` address in `fulfill()` function.

## [I-16] Typos

## Severity

Informational

## Description

There are a few typos in the contract source code. This could result in unforeseeable issues in the future development cycles.

## Location of Affected Code

`ligth` -> `light`

`Depolyed` -> `Deployed`

`transaxtion` -> `transaction`

`exsit` -> `exist`

`transaxtion` -> `transaction`

`orcale` -> `oracle`

## Recommendation

It is recommended to fix typos in smart contracts so that the code is clearer and more understandable.

## Team Response

Acknowledged and fixed by finding and correcting the typos section to see if there are others as well.

## [G-01] No Need to Initialize Variables with Default Values

## Severity

Gas Optimization

## Description

If a variable is not set/initialized, the default value is assumed `(0, false, 0x0 … depending on the data type)`. Saves `8 gas` per instance.

## Location of Affected Code

File: [contracts/ChainlinkLightClient.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol)

```solidity
247: for (uint i = 0; i < addresses.length; i++) {
261: for (uint i = 0; i < toRemoveAddresses.length; i++) {
321: for (uint i = 0; i < proofs.length; i++) {
```

File: [contracts/Gateway.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol)

```solidity
169: for (uint i = 0; i < queries.length; i++) {
242: for (uint i = 0; i < results.length; i++) {
305: uint256 highestHeight = 0;
```

File: [contracts/lib/EthereumDecoder.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/lib/EthereumDecoder.sol)

```solidity
153: for (uint256 i = 0; i < log.topics.length; i++) {
169: for (uint256 i = 0; i < receipt.logs.length; i++) {
192: for (uint256 i = 0; i < list.length; i++) {
215: for (uint256 i = 0; i < list.length; i++) {
```

File: [contracts/lib/RLPEncode.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/RLPEncode.sol)

```solidity
157: for (uint j = 0; j < res.length; j++) {
```

File: [contracts/lib/RLPReader.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/RLPReader.sol)

```solidity
121: for (uint256 i = 0; i < items; i++) {
286: uint256 count = 0;
394: for (uint i = 0; i < idx; i++) {
```

File: [contracts/lib/TrieProofs.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/TrieProofs.sol)

```solidity
34: uint256 pathOffset = 0; // Offset of the proof
43: for (uint256 i = 0; i < proof.length; i++) {
176: uint nibblesLength = 0;
220: uint256 i = 0;
```

## Recommendation

Do not initialize variables with their default values.

```diff
-  for (uint256 i = 0; ...
+  for (uint256 i; ...
```

## Team Response

Acknowledged and fixed by initialization of indexes in for-loop statements.

## [G-02] Cache Array Length Outside of Loops

## Severity

Gas Optimization

## Description

In the absence of caching, the Solidity compiler will consistently retrieve the array's length in every iteration. Specifically, for storage arrays, this entails an additional `sload` operation (resulting in 100 extra gas for each iteration, excluding the first one), while for memory arrays, it leads to an additional `mload` operation (resulting in 3 extra gas for each iteration, excluding the first one).

## Location of Affected Code

File: [contracts/ChainlinkLightClient.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/ChainlinkLightClient.sol)

```solidity
208: for (uint i; i < responses.length; i++) {
247: for (uint i = 0; i < addresses.length; i++) {
261: for (uint i = 0; i < toRemoveAddresses.length; i++) {
321: for (uint i = 0; i < proofs.length; i++) {
```

File: [contracts/Gateway.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol)

```solidity
169: for (uint i = 0; i < queries.length; i++) {
242: for (uint i = 0; i < results.length; i++) {
```

File: [contracts/lib/EthereumDecoder.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/lib/EthereumDecoder.sol)

```solidity
153: for (uint256 i = 0; i < log.topics.length; i++) {
169: for (uint256 i = 0; i < receipt.logs.length; i++) {
192: for (uint256 i = 0; i < list.length; i++) {
215: for (uint256 i = 0; i < list.length; i++) {
```

File: [contracts/lib/RLPEncode.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/RLPEncode.sol)

```solidity
157: for (uint j = 0; j < res.length; j++) {
204: for (i = 0; i < _list.length; i++) {
214: for (i = 0; i < _list.length; i++) {
```

File: [contracts/lib/TrieProofs.sol](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/TrieProofs.sol)

```solidity
43: for (uint256 i = 0; i < proof.length; i++) {
221: for (i = 0; i + xsOffset < xs.length && i < ys.length; i++) {
```

## Recommendation

To optimize gas costs, it is recommended to instantiate a variable in every function that has a for loop, before the loop itself.

```diff
+  uint responsesLength = responses.length;
+  for (uint256 i; i < responsesLength; i++) {
-  for (uint256 i; i < responses.length; i++) {
...
}
```

## Team Response

Acknowledged and fixed as proposed.

## [G-03] Splitting `require()` Statements that Use `&&` Saves Gas

## Severity

Gas Optimization

## Description

Instead of using the `&&` operator in a single `require` statement to check multiple conditions, using multiple require statements with 1 condition per require statement will save 8 GAS per &&. The gas difference would only be realized if the `revert` condition is met.

## Location of Affected Code

File: [contracts/lib/RLPReader.sol#L221](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/lib/RLPReader.sol#L221)

```solidity
require(item.len > 0 && item.len <= 33);
```

## Recommendation

Instead of using the `&&` operator in a single require statement to check multiple conditions, use multiple `require` statements with 1 condition per `require` statement.

## Team Response

Acknowledged and fixed.

## [G-04] Use Assembly to Check for `address(0)`

## Severity

Gas Optimization

## Description

Use assembly to check for `address(0)` to make the gas fees lower.

## Location of Affected Code

Most smart contracts.

## Recommendation

It is recommended to create a helper function that checks if the address is `address(0)` and use it in all the functions that are doing the `if(address(0))` check to reduce gas costs.

```diff
+ function _assemblyOwnerNotZero(address _addr) private pure {
+   assembly {
+     if iszero(_addr) {
+       mstore(0 x00 , "Zero address")
+       revert(0 x00 , 0 x20 )
+     }
+   }
+ }
```

## Team Response

Acknowledged and fixed by adding helper function for `address(0)`.

## [G-05] Remove Internal `_getQueryStatus()` Function For Save Gas

Gas Optimization

## Description

Remove the `_getQueryStatus()` function as there is no need for another internal function to read the `queryStore` mapping store.

## Location of Affected Code

File [contracts/Gateway.sol#L353-L357](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol#L353-L357)

```
function _getQueryStatus(
  bytes32 queryId
) internal view returns (QueryStatus) {
  return queryStore[queryId].status;
}
```

## Recommendation

It is recommended to remove the internal `_getQueryStatus()` function.

```diff
function getQueryStatus(bytes32 queryId) external view returns (QueryStatus) {
- return _getQueryStatus(queryId);
+ return queryStore[queryId].status;
}

- function _getQueryStatus(bytes32 queryId) internal view returns (QueryStatus) {
-  return queryStore[queryId].status;
- }
```

## Team Response

Acknowledged and fixed by deleting `_getQueryStatus()` function.

## [G-06] Using `uint256` Instead `int64` For `Gateway.nonce`

## Severity

Gas Optimization

## Description

Using smaller `uint` variables outside of structs is not cost-efficient, as the EVM performs some additional operations to pad the data. There could also be the hypothetical case of the `query()` function reverting, because of overflow of the `nonce` variable, which is incremented outside of an `unchecked` box. The probability of this happening is almost zero to none, as the max value of `uint64` is `18,446,744,073,709,551,615` and it is big enough for plenty of queries to be made. This will be mitigated to the maximum if `nonce` is changed to `uint256` instead.

## Location of Affected Code

File: [contracts/Gateway.sol#L30](https://github.com/Futaba-Labs/Futaba-Contract/blob/e0e5c247bee19cf2a96926d96895b9e8c221fea3/contracts/Gateway.sol#L30)

```solidity
uint64 public nonce;
```

## Recommendation

Change `nonce` to `uint256`.

```diff
- uint64 public nonce;
+ uint256 public nonce;
```

## Team Response

Acknowledged and fixed by changing `nonce` type from `uint64` to `uint256`.

## Recommendations

`uint256 constant MAX_QUERY_COUNT = 10;` -> `uint256 constant private _MAX_QUERY_COUNT = 10;`

`require(querySize <= 100, "Futaba: Too many queries");` -> `require(querySize <= MAX_QUERY_COUNT, "Futaba: Too many queries");`

`nonce++;` -> `++nonce;`

`function checkRoot(Proof[] memory proofs) internal view {` -> `function _checkRoot(Proof[] memory proofs) internal view {`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Futaba |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Futaba-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

