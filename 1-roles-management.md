---
# Core Classification
protocol: Volt Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 23461
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-volt
source_link: https://code4rena.com/reports/2022-03-volt
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[1] Roles management

### Overview

See description below for full details.

### Original Finding Content


After reviewing the entire volt protocol, we found that role management has been made unnecessarily complex.<br>
While there are no immediate fatal flaws in the current role assignment, from our prior experience in dealing with privilege management, we worry that such a complex system will likely lead to future problems, especially when management gradually moves from the hands of few reliable developers to an open vcon based governance.<br>
Due to this, we feel that there is a need to express our concerns as well as highlight a few role assignments that we find "strange".<br>

First. let's review the roles included in Permissions and Tribes. The admin/members shown below are the ones explicitly assigned in contracts.

    DEFAULT_ADMIN_ROLE							(native)
    	admin DEFAULT_ADMIN_ROLE
    	members

    MINTER_ROLE/MINTER			"MINTER_ROLE"			(native) (tribe-major)
    	admin GOVERN_ROLE
    	members

    BURNER_ROLE				"BURNER_ROLE"			(native)			unused
    	admin GOVERN_ROLE
    	members

    PCV_CONTROLLER_ROLE/PCV_CONTROLLER	"PCV_CONTROLLER_ROLE"		(native) (tribe-major)
    	admin GOVERN_ROLE
    	members

    GOVERN_ROLE/GOVERNOR			"GOVERN_ROLE"			(native) (tribe-major)
    	admin GOVERN_ROLE
    	members
    		core
    		init() caller

    GUARDIAN_ROLE/GUARDIAN			"GUARDIAN_ROLE"			(native) (tribe-major)
    	admin GOVERN_ROLE
    	members

    PARAMETER_ADMIN				"PARAMETER_ADMIN"		(tribe-admin)
    	admin DEFAULT_ADMIN_ROLE
    	members

    ORACLE_ADMIN				"ORACLE_ADMIN_ROLE"		(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    TRIBAL_CHIEF_ADMIN			"TRIBAL_CHIEF_ADMIN_ROLE"	(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    PCV_GUARDIAN_ADMIN			"PCV_GUARDIAN_ADMIN_ROLE"	(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    MINOR_ROLE_ADMIN			"MINOR_ROLE_ADMIN"		(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    FUSE_ADMIN				"FUSE_ADMIN"			(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    VETO_ADMIN				"VETO_ADMIN"			(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    MINTER_ADMIN				"MINTER_ADMIN"			(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    OPTIMISTIC_ADMIN			"OPTIMISTIC_ADMIN"		(tribe-admin)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    LBP_SWAP_ROLE				"SWAP_ADMIN_ROLE"		(tribe-minor)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    VOTIUM_ROLE				"VOTIUM_ADMIN_ROLE"		(tribe-minor)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    MINOR_PARAM_ROLE			"MINOR_PARAM_ROLE"		(tribe-minor)			unused
    	admin DEFAULT_ADMIN_ROLE
    	members

    ADD_MINTER_ROLE				"ADD_MINTER_ROLE"		(tribe-minor)
    	admin DEFAULT_ADMIN_ROLE
    	members

    PSM_ADMIN_ROLE				"PSM_ADMIN_ROLE"		(tribe-minor)
    	admin DEFAULT_ADMIN_ROLE
    	members

Notice how a several of those roles are not used in any of the contracts (marked as unused). This is the first problem. While it is understandable that the protocol is incomplete yet, introducing redundant roles does not make management easier. AccessControl.sol allows introducing new roles post-deployment, so it might be a better idea to keep a list of dynamically introduced roles instead of listing a lot of unused ones upfront, especially since there are roles with similar names (PCV_GUARDIAN_ADMIN and PCV_CONTROLLER), between which the difference is not made clear.

Next, we carry on to see the design of `Permissions`.<br>
We note that this contract is modified from the implementation of fei protocol, but on the other hand, disagree that the implementation is anywhere near optimal. To support our argument, we discuss the logic of role granting and revoking below.<br>
So let's look at the `grantMinter` function.

        function grantMinter(address minter) external override onlyGovernor {
            grantRole(MINTER_ROLE, minter);

The function specifies that it is a `onlyGovernor` function, which should expectedly mean that `GOVERNOR`, and only `GOVERNOR` have the privilege to add `MINTER_ROLE` members. However, if we dig a bit deeper, it is easy to see that this is not the case.

The `grantRole` function defined in AccessControl.sol is as below. Notice that it also has a modifier that specifies only admins of the specific role has privilege to add new members. Additionally, this function is public.

        function grantRole(bytes32 role, address account) public virtual override onlyRole(getRoleAdmin(role)) {
            _grantRole(role, account);
        }

Combining this logic with the `grantMinter` one above, we can see that the workflow essentially becomes

1.  caller is allowed to add new users if it only has admin of `MINTER_ROLE` (call `grantRole` directly)
2.  caller is allowed to add new users if it has admin of `MINTER_ROLE` and `GOVERNOR` role (call `grantRole` or `grantMinter`)
3.  caller is not allowed to add new users if it only has `GOVERNOR` role (blocked by `grantRole`)

It is clear that the `grantMinter` function now becomes semi-useless, since callers with only `GOVERNOR` role cannot do anything without admin of `MINTER_ROLE`, and admin of `MINTER_ROLE` can always call `grantRole` directly even if it does not have `GOVERNOR` role.

Our best guess of the original intention is that `GOVERNOR` has full privilege over role management, while admin of roles are neglected. To realize this concept, it might be better to override the `grantRole` function and make it non-public, so that callers can't circumvent the `GOVERNOR` check. Finally, change `grantMinter` to use the internal function `_grantRole`. Similar modifications should also be done to the `revokeXXX` series of functions.

Now we've gone through `Permissions`, time to look at `CoreRef` and `OracleRef`.<br>
One of the more interesting design choice in `CoreRef` is the introduction of `CONTRACT_ADMIN_ROLE`. This allows an additional role to be granted admin over the specific contract. However, throughout the volt protocol, `CONTRACT_ADMIN_ROLE` does not serve any particularly useful purpose. Moreover, in some places, the usage of `CONTRACT_ADMIN_ROLE` does not make much sense.

For instance, let's look at implementation of `RateLimited` and `MultiRateLimited`.<br>
`RateLimited` defines a global limit to the `bufferCap` and `rateLimitPerSecond`, and `MultiRateLimited` defines the upper limit of `individualMaxBufferCap` and `individualMaxRateLimitPerSecond`. In our opinion, for the system to make sense, a user granted permission to change `bufferCap` and `rateLimitPerSecond` should also have permission to change `individualMaxBufferCap` and `individualMaxRateLimitPerSecond`. However, it can be seen that `CONTRACT_ADMIN_ROLES` are allowed to change the global limits through `onlyGovernorOrAdmin` modifier, while individual limits can only be changed by `GOVERNOR` since `onlyGovernor` is used.
The flexibility introduced through `CONTRACT_ADMIN_ROLE` is not properly utilized in volt protocol, and as we see in the example above, leads to potential role privilege confusions, thus we deemed it more appropriate to remove the `CONTRACT_ADMIN_ROLE` mechanism altogether for simplicity.

The next aspect we would like to discuss is more of a design choice, and not really a management problem. Take it with a grain of salt.<br>
Throughout the contract, there are several places that use the `onlyGovernor` modifier. However given that the roles already included controllers/admins for each specific component (`PCV_CONTROLLER_ROLE`, `PSM_ADMIN_ROLE`), it is probably more appropriate to limit `GOVERNOR` to only manage the `Core` contract. If a governor needs to modify stuff from other contracts, add the corresponding admin role to itself and use that role to authenticate further actions. This design can create a clean cut between metadata management, and actually protocol management, at the cost of slightly more gas spent in granting roles. From our limited experience, this kind of management is more robust and greatly lowers the probability of mis-management in the future.

Now we've discussed all general suggestions we have for role management, we finally note a few role modifier usage that we find "strange", but are uncertain whether intended or not.

1.  `NonCustodialPSM.withdrawERC20` uses modifier `onlyPCVController`. We find it strange that a function in the PSM module requires PCVController role. Shouldn't this require `PSM_ADMIN_ROLE` instead?
2.  `CompoundPCVDepositBase.withdraw` uses the modifier `onlyPCVController`. This would require `NonCustodialPSM` to have the `PCV_CONTROLLER_ROLE` to call `withdraw`, and while it is not a problem strictly speaking, we find it strange to grant such a role. A more usual implementation would be to have `CompoundPCVDepositBase` do internal bookkeeping on the amount each address deposited, and allow withdraw with respect to those values (similar to implementation of ERC20). This avoids the introduction of an additional role (a.k.a potential point of failure due to mis-management).

Overall, complexity in role management easily creates confusions over the privilege of each role, and in the specific case of volt protocol, does not really introduce any benefits. We thus urge the developers to re-think the current role management system, and preferably simplify the design.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Volt Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-volt
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-03-volt

### Keywords for Search

`vulnerability`

