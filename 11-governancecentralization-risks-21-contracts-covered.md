---
# Core Classification
protocol: Audit 507
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58367
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-05-blackhole
source_link: https://code4rena.com/reports/2025-05-blackhole
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

[11] Governance/centralization Risks (21 contracts covered)

### Overview

See description below for full details.

### Original Finding Content


### Roles/Actors in the system

|  | Contract | Roles/Actors |
| --- | --- | --- |
| 1. | Black.sol | Minter |
| 2. | BlackClaims.sol | Owner/Second Owner |
| 3. | BlackGovernor.sol | - Minter  - Team |
| 4. | Bribes.sol | - Owner - Voter - GaugeManager - Minter - Avm |
| 5. | CustomPoolDeployer.sol | - Owner  - Authorized |
| 6. | CustomToken.sol | Owner |
| 7. | Fan.sol | Owner |
| 8. | GaugeExtraRewarder.sol | - Owner  - GAUGE |
| 9. | GaugeManager.sol | - Owner - GaugeAdmin - Governance |
| 10. | GaugeV2.sol | - Owner - genesisManager |
| 11. | GenesisPool.sol | - genesisManager |
| 12. | GenesisPoolManager.sol | - Owner - Governance |
| 13. | MinterUpgradable.sol | Team |
| 14. | PermissionsRegistry.sol | blackMultisig |
| 15. | RewardsDistributor.sol | Owner |
| 16. | RouterV2.sol | Owner |
| 17. | SetterTopNPoolsStrategy.sol | - Owner  - Executor |
| 18. | Thenian.sol | Owner |
| 19. | TokenHandler.sol | - Governance  - GenesisManager |
| 20. | VoterV3.sol | - Owner - VoterAdmin - Governance - GenesisManager |
| 21. | VotingEscrow.sol | - Voter - Team |

### Powers of each role (along with their risks)

**1. In the Black.sol contract**

* **Minter:** The minter role in the Black token contract holds critical authority over the token’s supply lifecycle. Initially assigned to the contract deployer, the minter can perform a one-time `initialMint()` of 50 million tokens to any specified address, as well as mint arbitrary token amounts at any point via the `mint()` function. This role can also be reassigned to another address using the `setMinter()` function. Here’s how he can misuse his powers:

  + Inflation attack: The minter can call `mint` (address, amount) to mint unlimited new tokens to any address. This would inflate the total supply, devalue user holdings.
  + Mint and dump attack: The minter could mint large amounts of tokens to their own address and immediately dump them on the market.This would crash the token price and exploit unsuspecting holders.
  + Secretly mint tokens to their own account: If this role is misused or compromised, the minter could secretly mint large amounts of BLACK tokens to their own address.
  + Permanently lose the minter role: The `setMinter()` function currently does not have an `address(0)` check , this can lead to the minter to set the new minter’s address as `0x0`. Hence, permanently losing the minter role. This would lead to the protocol to redeploy contracts again.

**2. In the BlackClaims.sol contract**

* **Owner/Second Owner:** The owner has the ability to recoverERC20 tokens, set treasury, start a season, `revokeUnclaimedReward`, finalize a season, `extendClaimDuration`, report rewards and renounce ownership. This contract allows two owners to handle these functionalities. Here’s how any one of them or potentially both misuse their powers:

  + One owner can renounce ownership of the other: However, a potential security risk arises if one of the owner’s private keys is compromised. In such a scenario, the malicious actor could use the compromised key to call the `setOwner2()` function and change the second owner’s address to one under their control. This effectively grants full control to the attacker, bypassing the intended dual-ownership security model.
  + May not ever recoverERC20 tokens: A malicious owner can just not call the `recoverERC20()` function, having the tokens locked in BlackClaims contract forever.
  + Set treasury’s address to himself/or to an `address(0x0)`: The owner can claim all the unclaimed rewards of the season, and potentially send it to “his” treasury address, Moreover, the `setTreasury()` function lacks an `address(0x0)` check, the malicious owner can potentially set an treasury to `address(0x0)` and call the `revokeUnclaimedReward()` function which will lead to the tokens to be permanently locked/lost.
  + Set the start time of a Season very high: The `startSeason()` function allows the owner to set the start time of a reward season without any upper limit or sanity check on the provided timestamp. A malicious or compromised owner could abuse this by setting the start time far into the future (e.g., 100 years ahead), effectively preventing the season from ever beginning.
  + Set treasury to `address(0x0)` and call `revokeUnclaimedReward()`: The malicious or compromised owner can call set the treasury to `address(0x0)` and then call the `revokeUnclaimedReward()` function, permanently loosing the funds.
  + Never finalize a season: The finalize function already holds solid checks; however, there can still be a misuse of a owner to never potentially finalize a season.
  + Extend claim duration to so high that the season never finalizes: The `extendClaimDuration()` function lacks checks to see if the claim duration amount is in bounds or not, the malicious or compromised owner can extend the claim duration to so high that finalization of a season will be impossible. Even if the compromised owner key is retained back to its original owner there is nothing that can be done.
  + Risk of reward censorship: The `reportRewards()` function only updates the rewards for the addresses explicitly passed in, a malicious or biased owner could intentionally omit certain players from the `players_` array. As a result, those omitted players would not receive their rightful rewards, even if they earned them during the season. This introduces a risk of reward censorship.

**3. In the In the BlackGovernor.sol contract**

* **Minter:** The Minter role in the BlackGovernor contract is a role assigned to a smart contract. Since the role is assigned to a contract (predefined methods), no governance manipulation may be possible for this role.
* **Team:** The team role has the ability to set a proposal numerator and renounce its ownership to someone else. Here’s how a user with a team role can misuse his powers:

  + Set proposal numerator to zero: The malicious or compromised user with team role can set the proposal numerator to zero, potentially allowing anyone to propose even with 0 votes.

**4. In the Bribes.sol contract**

* **Owner:** In the Bribes contract, the owner has the ability to set a new Voting, GaugeManager, AVM addresses. He also has the power over `recoverERC20AndUpdateData()` and `emergencyRecoverERC20()` functions. Here’s how he can misuse his powers:

  + Set malicious contracts: The owner can assign malicious contract addresses for the voter, `gaugeManager`, `bribeFactory`, or AVM; such that it benefits him, enabling backdoors or unauthorized control. These contracts could be programmed to redirect fees, manipulate votes, or extract value from user interactions — disguised as legitimate protocol behavior, but actually benefiting the malicious owner.
  + Steal rewards in the guise of recovery: The `onlyAllowed` role can invoke this function to withdraw arbitrary ERC20 tokens from the contract. They could manipulate reward accounting by subtracting `tokenAmount` from the `tokenRewardsPerEpoch`, under-reporting actual rewards. This allows them to steal reward withdraw tokens meant for user rewards under the guise of “recovery”. Potentially few, or many users, might not receive their rewards, as it has been taken by the owner by the guise of recovery.
* **Voter:** No governance manipulation possible for this role since its a smart contract (predefined methods), unless the owner sets a malicious address (contract).
* **GaugeManager:** No governance manipulation possible for this role since its a smart contract (predefined methods), unless the owner sets a malicious address (contract).
* **Minter:** No governance manipulation possible for this role since its a smart contract (predefined methods), unless the owner sets a malicious address (contract).
* **Avm**: No governance manipulation possible for this role since its a smart contract (predefined methods), unless the owner sets a malicious address (contract).

**5. In the CustomPoolDeployer.sol contract**

* **Owner:** The owner has the ability to `addAuthorizedAccount`, `removeAuthorizedAccount`, `setPluginForPool`, `setPlugin`, `setPluginConfig`, `setFee`, `setCommunityFee`, `setAlgebraFeeRecipient`, `setAlgebraFeeManager`, `setAlgebraFeeShare`, `setAlgebraFarmingProxyPluginFactory`, `setAlgebraFactory`, `setAlgebraPluginFactory`. Here’s how he can misuse his powers:

  + Backdoor privilege escalation via `addAuthorizedAccount`: The owner can maliciously add multiple alternate EOA addresses or smart contracts as authorized accounts, effectively creating hidden backdoors for retaining control. These authorized entities could automate harmful actions such as setting high fees, bypassing restrictions, or manipulating internal state. Even after ownership is transferred, the previous owner may still retain access through these accounts and manipulate functions which are still accessible to the authorized accounts. While a `removeAuthorizedAccount` function exists, the cleanup burden falls entirely on the new owner, who must manually revoke each account — a tedious process if many were pre-added.
  + Fee manipulation via `setFee()`: A malicious owner can exploit the `setFee()` function to assign excessively high fees to a pool. This would result in an unfairly large portion of each user transaction being taken as fees, effectively discouraging usage, draining user value.
  + Deploy and set malicious factories: The owner could deploy malicious versions of these factories that generate contracts with backdoors or vulnerabilities. For example: farming Plugin Factory could redirect user rewards to the owner’s address, Algebra Factory could deploy pools with manipulated fee logic or ownership traps, Plugin Factory could enable unauthorized access or data leakage.
* **Authorized:** The Authorized role has the ability to `setPluginForPool`, `setPlugin`, `setPluginConfig`, `setFee`, `setCommunityFee`. Here’s how a user with a Authorized role can misuse his power:

  + Set high community fees: The protocol does not implement a cap on fees, allowing the malicious or compromised authorized role to set high fees. This does not pose much risk since the owner can just take away the authorized role from the user and set the fees properly again. However, if the owner is malicious or compromised then it’s a different scenario.

**6. In the CustomToken.sol contract**

* **Owner:** The owner has the ability to mint and burn tokens from an account, Here’s how he can misuse his powers:

  + Mint a large sum: The owner can mint a large sum into a random account to inflate the value of the token. He can even mint tokens to his personal account to have more value.
  + Burn a large sum: The owner can exploit the mint and burn functions to manipulate token supply and market value. For example, the owner could burn a significant number of tokens from user accounts to reduce total supply, artificially inflating the token’s value. Simultaneously, the owner could mint a large number of tokens to their own account, allowing them to benefit from the deflationary effect they induced.

**7. In the Fan.sol contract** - *Note: Same as CustomToken contract (see number 6 above.)*

**8. In the GaugeExtraRewarder.sol contract**

* **Owner:** The owner has the ability to `recoverERC20` and `setDistributionRate`. Here’s how he can misuse his powers:

  + Set an extremely low amount in `setDistributionRate`: A compromised or malicious owner can deliberately set the reward amount very low, causing the distribution rate to slow down significantly and resulting in reduced rewards that may frustrate or disincentivize users.
  + Break reward mechanism: The owner can call `recoverERC20` to withdraw any ERC20 token held by the contract, including the `rewardToken`. Even though there is a check to limit withdrawal of the `rewardToken` to the not-yet-distributed amount, the owner can still withdraw tokens that users expect as rewards; with potential to reduce or disrupt user rewards by withdrawing tokens from the contract.
* **GAUGE:** No governance manipulation possible for this role since its a smart contract (predefined methods).

**9. In the GaugeManager.sol contract**

* **Owner:** The owner has the ability to set the Avm address. Here’s how he can misuse his powers:

  + Set a malicious contract to benefit himself: A compromised or malicious Owner sets avm to a contract that looks like a voting escrow manager but has hidden backdoors. This malicious AVM could potentially divert locked tokens to the owner.
* **GaugeAdmin:** The GaugeAdmin has the ability to `setBribeFactory`, `setPermissionsRegistry`, `setVoter`, `setGenesisManager`, `setBlackGovernor`, `setFarmingParam`, `setNewBribes`, `setInternalBribeFor`, `setExternalBribeFor`, `setMinter`, `addGaugeFactory`, `replaceGaugeFactory`, `removeGaugeFactory`, `addPairFactory`, `replacePairFactory`, `removePairFactory`, `acceptAlgebraFeeChangeProposal`. Here’s how he can misuse his power:

  + Misuse critical functions: A malicious or compromised admin, having exclusive access to these functions, can misuse their powers by arbitrarily setting or replacing critical contract components such as the minter, gauge factories, and pair factories, which control key protocol behaviors like minting and gauge creation. By setting a malicious minter or injecting compromised factories, the admin could mint unlimited tokens, manipulate liquidity incentives, or redirect funds. Furthermore, the admin can unilaterally accept fee changes on Algebra pools, potentially increasing fees or redirecting revenue without community consent.
  + Arbitrarily change addresses: They can arbitrarily change the addresses of key farming contracts (`farmingCenter`, `algebraEternalFarming`, `nfpm`), potentially redirecting farming rewards or incentives to malicious contracts. Additionally, by setting or replacing internal and external bribes on any gauge, the admin can manipulate voting incentives and reward distributions, possibly favoring certain participants or contracts unfairly. Since these settings directly influence how rewards and incentives flow within the protocol, the admin’s unchecked ability to alter them creates a significant risk of abuse, including funneling rewards to themselves or collaborators, destabilizing the ecosystem, and undermining user trust.
  + Admin replaces the Bribe Factory and Permission Registry with malicious contracts: The admin, having full control, sets the `bribefactory` to a malicious contract they control. This fake bribe factory redirects all bribe rewards intended for legitimate liquidity providers or voters to the admin’s own address. Meanwhile, the admin also replaces the `permissionRegistry` with a contract that falsely approves only their own addresses or bots for privileged actions, effectively locking out honest participants. With the voter contract replaced by one that the admin controls, they can manipulate governance votes or decisions, passing proposals that benefit themselves or their allies, like lowering fees or minting tokens unfairly. At the same time, the admin sets `blackGovernor` to their own address, giving them the power to block or censor any proposals or actions from other users, consolidating full control over governance.
* **Governance:** The governance role has the ability to revive and kill a gauge. Here’s how he can misuse his powers:

  + Kill gauges with malicious intent: A malicious governance actor can intentionally kill legitimate gauges under the pretense that they are “malicious”, using the `killGauge` function. Since there is no on-chain validation of malicious behavior in the function itself, just a check that `isAlive[_gauge]` is true—they can arbitrarily target any active gauge.

**10. In the GaugeV2.sol contract**

* **Owner:** The owner has the ability to `setDistribution`, `setGaugeRewarder`, `setInternalBribe`, `activateEmergencyMode`, `stopEmergencyMode` and `setGenesisPoolManager`. Here’s how he can misuse his powers;

  + A malicious owner could stealthily redirect critical reward and bribe flows to attacker-controlled contracts by setting the internal bribe, gauge rewarder, and distribution addresses to malicious contracts. They could also consolidate control by assigning the genesis pool manager to themselves or colluding contracts, gaining influence over early-stage pools and rewards. Additionally, the owner can arbitrarily trigger and stop emergency mode, halting or manipulating protocol operations to stall users while executing self-serving upgrades or migrations. This unchecked power enables fund diversion, governance capture, loss of user trust, and backdoor control of key system parameters without any DAO or governance oversight, posing severe risks to protocol integrity and participant fairness.
* **GenesisManager:** The GenesisManager has the ability to set pools, Here’s how he can misuse his power:

  + Setting as `address(0)`: A compromised or malicious owner can set the Genesis Pool Manager to the zero address (`address(0)`), as the `setGenesisPoolManager()` function lacks a validation check to prevent this. This could disable or break core protocol functionality that depends on the genesis manager.

**11. In the GenesisPool.sol contract**

* **genesisManager:** The genesisManager has the ability to `setGenesisPoolInfo`, `rejectPool`, `approvePool`, `depositToken`, `transferIncentives`, `setPoolStatus`, `launch`, `setAuction`, `setMaturityTime` and `setStartTime`. Here’s how he can misuse his powers:

  + Set arbitrary parameters: The manager can misuse their role in `setGenesisPoolInfo` by providing malicious or incorrect input values since the function lacks proper input validation checks on critical parameters such as `genesisInfo`, `allocationInfo`, and `auction`. This enables the manager to set arbitrary genesis configurations, manipulate token allocation amounts, or assign a malicious `auction` contract that could siphon funds or behave unfairly.
  + Reject pools arbitrarily: The manager can call `rejectPool()` to mark any pool as `NOT_QUALIFIED` prematurely, blocking legitimate pools from proceeding and unfairly refunding proposed native tokens, potentially disrupting or censoring projects.
  + Approve malicious or fake pools: Using `approvePool()`, the manager can approve pools with fake or attacker-controlled pair addresses (`_pairAddress`), enabling front-running, rug pulls, or other malicious activities disguised as legitimate pools.
  + Manipulate deposits: In `depositToken()`, the manager controls when deposits are accepted (by controlling `poolStatus` and `genesisInfo.startTime`) and can arbitrarily restrict or allow deposits, effectively censoring or favoring certain users.
  + `setPoolStatus` to any pools without secondary authorization: The genesisManager can randomly set any pool’s status to “NOT QUALIFIED”. The protocol should implement a secondary role to make sure all interactions of genesisManager are appropriate or not.
  + Set a very high maturity: A compromised or malicious genesisManager can set a very high maturity time, the protocol does not implement an check to ensure that the maturity time is in bounds or not, making this scenario possible.

**12. In the GenesisPoolManager.sol contract**

* **Owner:** The owner has the ability to set a router. Here’s how he can misuse his powers:

  + The current implementation of the code is incorrect, it only allows `address(0)` to be passed via `setRouter()` function, already favors the compromised or malicious owner.
* **Governance:** The Governance role has the ability to `whiteListUserAndToken`, `depositNativeToken`, `rejectGenesisPool`, `approveGenesisPool`, `setAuction`, `setEpochController`, `setMinimumDuration`, `setMinimumThreshold`, `setMaturityTime` and `setGenesisStartTime`. Here’s how he can misuse his powers:

  + Whitelisting arbitrary tokens or users (backdoor access): By calling
    `whiteListUserAndToken` (`proposedToken`, `tokenOwner`), governance can whitelist unvetted or malicious tokens and users.
  + Approving fraudulent or unqualified pools: Governance can approve a genesis pool (`approveGenesisPool`) regardless of community consensus or the token’s legitimacy. The function only checks a few conditions like balance and duration, but there’s no check on project credibility or voting outcome.The Governor can even approve pools which benefits him(a cut directed to his address on every transaction that takes place.)
  + Silencing legitimate pools via rejection: By calling `rejectGenesisPool` (`nativeToken`), governance can deliberately shut down valid pools, sabotaging competitor projects.

    *Note: Additionally all governance functions can be executed immediately with no time lock, delay, or DAO-based confirmation.*
  + `setGenesisStartTime` to years: The compromised or malicious governor can set the genesis start time to a long duration, such that genesis never begins.

**13. In the MinterUpgradable.sol contract**

* **Team:** The team role has the ability to set gauge manager and set team rate. Here’s how he can misuse his powers:

  + Set malicious `gaugeManager` contract: A compromised or malicious user with the team role can pass in a malicious `gaugeManager` address such that it benefits him (e.g., Gauge emissions can be routed to attacker wallets).
  + Set team rate as Zero: Setting this as 0 would lead to the `teamEmissions` be transferred to the team as 0 every time `update_period` is called once every week.

**14. In the PermissionsRegistry.sol contract**

* **blackMultisig:** This role has the ability to `addRole`, `removeRole`, `setRoleFor`, `removeRoleFrom`, `setEmergencyCouncil` and `setBlackMultisig`. Here’s how he can misuse his powers:

  + Add arbitrary roles: The multisig can create meaningless or deceptive roles like, `SUPER_ADMIN` or `UNLIMITED_MINTER` — misleading names that may imply more power. Duplicate logical roles with different names (`GAUGE_ADMIN` vs `GaugeAdmin`).
  + Assign roles to malicious addresses: Assign critical roles (e.g., `MINTER`, `GAUGE_ADMIN`, `ROUTER_SETTER`, etc.) to an EOA owned by attacker, Malicious contract or rotate them silently over time.

**15. In the RewardsDistributor.sol contract**

* **Owner:** The owner has the ability to `setDepositor`, `withdrawERC20`, `setAVM` and renounce his ownership. Here’s how he can misuse his powers:

  + Silent draining: Owner can drain any ERC-20 token held by the contract at any time, He can do this silently since no event is emitted when the owner withdraws erc20 tokens.
  + Set a malicious avm: As stated in my previous governance risks, the owner can set a malicious avm address such that it benefits him. This is a direct setting; there is no external validation by any other sources that the avm address set by the owner is actually valid or not.

**16. In the RouterV2.sol contract**

* **Owner:** The owner has the ability to `setSwapRouter`, `setAlgebraFactory`, `setQuoterV2`, `setAlgebraPoolAPI`. Here’s how he can misuse his powers:

  + Malicious router: Owner sets `swapRouter` to a malicious contract that, front-runs user swaps by manipulating pricing logic, steals tokens during swaps by redirecting `transferFrom` to self and overrides routing logic to siphon fees to themselves.
  + Set a fake Algebra Factory: Owner sets a fake factory that, creates fake pools with manipulated or spoofed token addresses.
  + Set malicious `setAlgebraPoolAPI`: If this API contract stores sensitive pool metadata (e.g., fee config, pool status, time-weighted data). Owner can redirect it to a contract that lies about past data which could affect, time-weighted average price (TWAP), fee growth history and Oracle usage.

**17. In the SetterTopNPoolsStrategy.sol contract**

* **Owner:** The owner has the ability to set a avm address. Here’s how he can misuse his powers:

  + Set a malicious avm: As stated in my previous governance risks, the owner can set a malicious avm address such that it benefits him. This is an direct setting; there is no external validation by any other sources that the avm address set by the owner is actually valid or not.
* **Executor:** The executor role has the ability to `setTopNPools`. Here’s how he can misuse his powers:

  + The executor sets top pools to low-volume, illiquid, or fake pools that they own or control, have no real trading activity, inflate stats or visibility. These pools could then attract volume, wrongly perceived as top pools, to receive higher incentives or emissions and trick users or LPs into providing liquidity or trading, leading to loss.

**18. In the Thenian.sol contract**

* **Owner:** The owner has the ability to withdraw, `setRoot`, `setNftPrice` and `reserveNFTs`. Here’s how he can misuse his powers:

  + Rug pull: Owner can withdraw all ETH (e.g. mint proceeds) to any `multiSig` they control, leaving users who paid for NFTs with nothing in return.
  + Increase price: Owner can dynamically raise the price after users are onboarded or committed, or lower the price for themselves or insiders after initial hype.
  + Owner can mint NFTs to themselves or insiders, before any public sale (sniping rare tokens), without paying in bulk to flip on secondary markets.

**19. In the TokenHandler.sol contract**

* **Governance:** The governance role has the ability to `setPermissionsRegistry`, `whitelistTokens`, `whitelistToken`, `blacklistTokens`, `whitelistNFT`, `blacklistNFT`, `whitelistConnectors`, `whitelistConnector`, `blacklistConnector`, `setBucketType`, `updateTokenVolatilityBucket`. Here’s how he can misuse his powers:

  + The primary governance risk across these functions lies in the potential abuse of role-based control. A malicious governance actor could assign critical roles (e.g., connector tokens, whitelisted NFTs) to unauthorized or malicious addresses in exchange for bribes or personal gain. This could lead to privileged access, unfair trading advantages, or manipulation of protocol logic. Similarly, by removing or blacklisting legitimate entries, governance could censor users or competitors, undermining the fairness and neutrality of the protocol.
  + `whitelistNFT`/`blacklistNFT`: The governance can misuse this by selectively whitelisting NFTs they own, allowing them to access exclusive features such as staking rewards, airdrops, or protocol privileges. Conversely, they could blacklist legitimate user NFTs to exclude them from benefits, creating unfair advantages or censorship.
  + `whitelistConnector`/`whitelistConnectors`: These functions allow governance to mark certain tokens as routing connectors, which can significantly influence DEX trading paths. A malicious actor could whitelist low-liquidity, high-fee, or malicious tokens to manipulate swaps, favor certain assets, or enable exploitative routing for personal gain.
  + `blacklistConnector`: By blacklisting a connector, governance can disrupt the routing mechanism and effectively remove a token from trading paths. This could be used to block competitor tokens, harm projects that don’t align with governance interests, or censor tokens used widely by users, reducing decentralization and fairness.
  + `setBucketType`: This function allows governance to define or redefine the volatility bucket of tokens, potentially affecting their fee rates, risk handling, or trading logic. A dishonest actor could classify risky tokens as low-risk to game the system, offer misleading yields, or misrepresent token safety to users.
* **GenesisManager:** Has similar but limited access as compared to governance. Thus, the risks remain same for both.

**20. In the VoterV3.sol**

* **Owner:** Does not have much access in this contract, but has the ability to set an epoch owner.

  + Does not contain much risk (except that he can set it to a malicious address).
* **VoterAdmin:** The voter admin has the ability to `setPermissionsRegistry`, `setMaxVotingNum`, `setAVM`. Here’s how he can misuse his powers:

  + In the `setPermissionsRegistry` function, the VoterAdmin can set a new `permissionRegistry` contract. If misused, they could point it to a malicious or manipulated contract that disables or weakens access control checks. This could allow unauthorized gauge creation, voting participation, or protocol interactions that would normally be restricted, effectively undermining governance integrity and enabling privilege escalation.
  + Through the `setMaxVotingNum` function, the VoterAdmin can adjust the maximum number of pools or items a user can vote on. While this is intended for flexibility, an abusive admin could set this value excessively high or low. A very high value could spam or overload the system, potentially exhausting gas or storage, while a low value could limit voter effectiveness, censor specific users or preferences, and bias the outcome of votes.
  + The `setAVM` function allows the admin to assign the Auto Voting Manager (avm) by fetching it from the Voting Escrow contract. If `_ve` is compromised or misconfigured, this function could silently redirect AVM privileges to an untrusted actor. This risks vote automation being controlled by a malicious contract, allowing votes to be cast or overridden without user consent, compromising the fairness of governance.
* **Governance:** Modifier is defined in this contract, but has no access to any of the functions.
* **GenesisManager:** Modifier is defined in this contract, but has no access to any of the functions.

**21. In the VotingEscrow.sol contract**

* **Team:** Has the ability to `setArtProxy`, `setAVM`, `toggleSplit`, `setSmNFTBonus`. Here’s how he can misuse his powers:

  + `setArtProxy` (address proxy): The team can change the art rendering proxy to a malicious or broken contract. This can result in NFTs displaying incorrect metadata or art, potentially misleading users or damaging the visual and branding integrity of the collection. If metadata is dynamic and depends on this proxy, they could also encode hidden traits, tracking, or backdoors.
  + `setAVM` (address avm): By changing the Auto Voting Manager (AVM) to a manipulated contract, the team can automate votes in favor of their interests. This undermines fair governance by enabling vote hijacking, centralized decision-making, or even bribe-taking via scripted AVM behavior that does not reflect real user preferences.
  + `toggleSplit` (bool state): This function may control whether NFTs can be split (e.g., fractionalized or split into sub-assets). Maliciously toggling this could disrupt NFT functionality, cause loss of composability or break integrations with platforms. Re-enabling or disabling split arbitrarily can be used to lock users out of expected functionality or manipulate secondary market behavior.
  + `setSmNFTBonus` (uint bonus): This sets the bonus for special SM NFTs. If the team assigns excessively high bonuses, they can create unfair yield or voting power advantages for themselves or insiders holding those NFTs. This distorts protocol incentives and governance, allowing the team to indirectly accumulate more control or rewards.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Audit 507 |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-05-blackhole
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-05-blackhole

### Keywords for Search

`vulnerability`

