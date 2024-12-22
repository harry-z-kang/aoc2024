#!/bin/env python

NUM_OF_FUTURE_PRICES = 2000


def get_next_price(price: int) -> int:
    price = ((price << 6) ^ price) % 0x100_0000
    price = ((price >> 5) ^ price) % 0x100_0000
    price = ((price << 11) ^ price) % 0x100_0000

    return price


def main() -> None:
    with open("input.txt") as f:
        initial_prices = [int(num) for num in f.read().strip().splitlines()]

        total_price = 0
        for initial_price in initial_prices:
            price = initial_price
            for _ in range(NUM_OF_FUTURE_PRICES):
                price = get_next_price(price)
            total_price += price

        print(f"Part 1: {total_price}")

        prices = dict[int, list[int]]()
        price_deltas = dict[int, list[int]]()
        for initial_price in initial_prices:
            prices[initial_price] = [initial_price]
            for _ in range(NUM_OF_FUTURE_PRICES):
                prices[initial_price].append(get_next_price(prices[initial_price][-1]))

            price_deltas[initial_price] = [
                int(str(prices[initial_price][i + 1])[-1])
                - int(str(prices[initial_price][i])[-1])
                for i in range(NUM_OF_FUTURE_PRICES - 1)
            ]

        total_num_of_bananas = dict[tuple[int, int, int, int], int]()
        for initial_price, price_delta in price_deltas.items():
            num_of_bananas = dict[tuple[int, int, int, int], int]()

            for i in range(len(price_delta) - 3):
                target_sequence = tuple(price_delta[i : i + 4])

                if target_sequence not in num_of_bananas:
                    num_of_bananas[target_sequence] = int(
                        str(prices[initial_price][i + 4])[-1]
                    )

            for target_sequence, num_of_banana in num_of_bananas.items():
                if target_sequence not in total_num_of_bananas:
                    total_num_of_bananas[target_sequence] = num_of_banana
                else:
                    total_num_of_bananas[target_sequence] += num_of_banana

        print(f"Part 2: {max(total_num_of_bananas.values())}")


if __name__ == "__main__":
    main()
