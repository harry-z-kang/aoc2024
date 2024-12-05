#!/bin/env python


def main() -> None:
    with open("input.txt") as f:
        rules, updates = [part.splitlines() for part in f.read().split("\n\n")]

        order_dict = dict[int, list[int]]()
        for rule in rules:
            key, value = rule.split("|")
            try:
                order_dict[int(key)].append(int(value))
            except KeyError:
                order_dict[int(key)] = [int(value)]

        update_list = [
            [int(page_num) for page_num in update.split(",")] for update in updates
        ]

        incorrectly_ordered_updates = list[list[int]]()
        sum_middle_page_nums = 0
        for update in update_list:
            in_correct_order = True

            for i, page_num in enumerate(update[:-1]):
                if update[i + 1] not in order_dict[page_num]:
                    in_correct_order = False
                    break

            if in_correct_order:
                sum_middle_page_nums += update[len(update) // 2]
            else:
                incorrectly_ordered_updates.append(update)

        print(f"Part 1: {sum_middle_page_nums}")

        sum_middle_page_nums = 0
        for update in incorrectly_ordered_updates:
            for i in range(len(update) - 1):
                for j in range(i + 1, len(update)):
                    if update[j] not in order_dict[update[i]]:
                        tmp = update[j]
                        update[j] = update[i]
                        update[i] = tmp

            sum_middle_page_nums += update[len(update) // 2]

        print(f"Part 2: {sum_middle_page_nums}")


if __name__ == "__main__":
    main()
