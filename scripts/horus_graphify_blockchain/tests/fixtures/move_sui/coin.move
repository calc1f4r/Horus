module 0x2::coin {
    use std::string::String;
    use 0x2::balance::{Self, Balance};
    use 0x2::object::{Self, UID};
    use 0x2::transfer;
    use 0x2::tx_context::TxContext;

    struct Coin<phantom T> has key, store {
        id: UID,
        balance: Balance<T>,
    }

    struct CoinMetadata<phantom T> has key, store {
        id: UID,
        decimals: u8,
        name: String,
        symbol: String,
    }

    struct TreasuryCap<phantom T> has key, store {
        id: UID,
        total_supply: u64,
    }

    public fun mint<T>(
        cap: &mut TreasuryCap<T>,
        value: u64,
        ctx: &mut TxContext,
    ): Coin<T> {
        cap.total_supply = cap.total_supply + value;
        Coin {
            id: object::new(ctx),
            balance: balance::create_for_testing(value),
        }
    }

    public fun burn<T>(cap: &mut TreasuryCap<T>, coin: Coin<T>): u64 {
        let Coin { id, balance } = coin;
        object::delete(id);
        let value = balance::value(&balance);
        balance::destroy_zero(balance::split(&mut balance, value));
        cap.total_supply = cap.total_supply - value;
        value
    }

    public fun value<T>(coin: &Coin<T>): u64 {
        balance::value(&coin.balance)
    }

    public fun transfer<T>(coin: Coin<T>, recipient: address) {
        transfer::public_transfer(coin, recipient)
    }
}
