#!/bin/env python

from multiprocessing import Process


NUM_OF_ROWS = 103
NUM_OF_COLS = 101


class Robot:
    def __init__(
        self, start_position: tuple[int, int], velocity: tuple[int, int]
    ) -> None:
        self.start_position = start_position
        self.velocity = velocity
        self.trace = list[tuple[int, int]]()

        position = self.start_position
        while True:
            self.trace.append(position)
            position = (
                (position[0] + self.velocity[0]) % NUM_OF_ROWS,
                (position[1] + self.velocity[1]) % NUM_OF_COLS,
            )

            if position == self.trace[0]:
                break


def print_grid(robots: list[Robot], start_t: int, end_t: int) -> None:
    with open(f"{start_t}-{end_t}.txt", "w") as f:
      for t in range(start_t, end_t):
          f.write(f"Time: {t}\n")
          robot_positions = [robot.trace[t] for robot in robots]
          for row in range(NUM_OF_COLS):
              for col in range(NUM_OF_ROWS):
                  f.write("#" if (row, col) in robot_positions else ".")
              f.write("\n")
          f.write("\n")


def main() -> None:
    with open("input.txt") as f:
        robots_raw = f.read().strip().splitlines()

        robots = list[Robot]()
        for robot_raw in robots_raw:
            position_raw, velocity_raw = robot_raw.split()
            position_x, position_y = position_raw.split("=")[1].split(",")
            velocity_x, velocity_y = velocity_raw.split("=")[1].split(",")

            robots.append(
                Robot(
                    (int(position_y), int(position_x)),
                    (int(velocity_y), int(velocity_x)),
                )
            )

        robot_positions = [robot.trace[100 % len(robot.trace)] for robot in robots]

        num_of_robots_q1 = 0
        for row in range((NUM_OF_ROWS - 1) // 2):
            for col in range((NUM_OF_COLS - 1) // 2):
                num_of_robots_q1 += robot_positions.count((row, col))

        num_of_robots_q2 = 0
        for row in range((NUM_OF_ROWS - 1) // 2):
            for col in range((NUM_OF_COLS + 1) // 2, NUM_OF_COLS):
                num_of_robots_q2 += robot_positions.count((row, col))

        num_of_robots_q3 = 0
        for row in range((NUM_OF_ROWS + 1) // 2, NUM_OF_ROWS):
            for col in range((NUM_OF_COLS - 1) // 2):
                num_of_robots_q3 += robot_positions.count((row, col))

        num_of_robots_q4 = 0
        for row in range((NUM_OF_ROWS + 1) // 2, NUM_OF_ROWS):
            for col in range((NUM_OF_COLS + 1) // 2, NUM_OF_COLS):
                num_of_robots_q4 += robot_positions.count((row, col))

        print(
            f"Part 1: {num_of_robots_q1 * num_of_robots_q2 * num_of_robots_q3 * num_of_robots_q4}"
        )

        # Part 2: Literally print out everything and look for the chirstmas tree
        # 6752 is the answer
        processes = list[Process]()
        for i in range(11):
            if i == 10:
                p = Process(target=print_grid, args=(robots, i * 1000, len(robots[0].trace)))
            else:
                p = Process(target=print_grid, args=(robots, i * 1000, (i + 1) * 1000))

            processes.append(p)
            p.start()

        for p in processes:
            p.join()



if __name__ == "__main__":
    main()
