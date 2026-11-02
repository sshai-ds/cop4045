"""Predator-Prey-Human simulation.

Prey, Predator, and Human objects live on an n x n island
grid. Predators eat prey; humans eat predators.
"""
from __future__ import annotations

import random

import matplotlib.pyplot as plt


class Island:
    """n x n grid where a 0 value means the cell is empty."""

    def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0,
                 count_humans: int = 0) -> None:
        """Create an n x n grid of 0's, then add the animals."""
        self.grid_size = n
        self.grid = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int) -> None:
        """Put the animals at random empty cells.

        Precondition: all the animals fit on the grid.
        """
        for animal_class, total in ((Prey, prey_count),
                                    (Predator, predator_count),
                                    (Human, count_humans)):
            count = 0
            while count < total:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                if not self.animal(x, y):
                    self.register(animal_class(island=self, x=x, y=y))
                    count += 1

    def clear_all_moved_flags(self) -> None:
        """Clear every animal's moved flag before the next turn."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y]:
                    self.grid[x][y].clear_moved_flag()

    def size(self) -> int:
        """Return the length of one side of the island."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """Put animal on the grid at its coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Animal) -> None:
        """Remove animal from the grid."""
        self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Animal | int:
        """Return the animal at (x, y), 0 if empty, -1 if off the island."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        """Return the grid as text, with (0, 0) in the lower left corner."""
        s = ""
        for j in range(self.grid_size - 1, -1, -1):
            for i in range(self.grid_size):
                s += str(self.grid[i][j] or ".") + "  "
            s += "\n"
        return s

    def count_animals(self, animal_type: type) -> int:
        """Return the number of animal_type objects on the island."""
        count = 0
        for row in self.grid:
            for cell in row:
                if isinstance(cell, animal_type):
                    count += 1
        return count

    def count_prey(self) -> int:
        """Return the number of prey on the island."""
        return self.count_animals(Prey)

    def count_predators(self) -> int:
        """Return the number of predators on the island."""
        return self.count_animals(Predator)

    def count_humans(self) -> int:
        """Return the number of humans on the island."""
        return self.count_animals(Human)


class Animal:
    """An animal on the island grid."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "A") -> None:
        """Place the animal at (x, y); s is its grid character."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self) -> tuple[int, int]:
        """Return the (x, y) coordinates."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return the grid character."""
        return self.name

    def check_grid(self,
                   type_looking_for: type = int) -> tuple[int, int] | int:
        """Return a neighbor cell holding a type_looking_for object, or 0."""
        offset = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1),
                  (0, -1), (1, -1)]
        result = 0
        for i in range(len(offset)):
            x = self.x + offset[i][0]
            y = self.y + offset[i][1]
            if not 0 <= x < self.island.size() or \
               not 0 <= y < self.island.size():
                continue
            if type(self.island.animal(x, y)) == type_looking_for:
                result = (x, y)
                break
        return result

    def move(self) -> None:
        """Move to an empty neighbor cell, if there is one."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.island.remove(self)
                self.x = location[0]
                self.y = location[1]
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """Breed into an empty neighbor cell when the breed clock runs out."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                new_animal = self.__class__(self.island, x=location[0],
                                            y=location[1])
                self.island.register(new_animal)

    def eat(self) -> None:
        """Do nothing; animals that hunt override this."""

    def eat_neighbor(self, food_type: type) -> bool:
        """Move onto a neighboring food_type animal and remove it.

        Postcondition: returns True if an animal was eaten.
        """
        location = self.check_grid(food_type)
        if not location:
            return False
        self.island.remove(self.island.animal(location[0], location[1]))
        self.island.remove(self)
        self.x = location[0]
        self.y = location[1]
        self.island.register(self)
        self.moved = True
        return True

    def clear_moved_flag(self) -> None:
        """Mark the animal as not moved this turn."""
        self.moved = False


class Prey(Animal):
    """Prey moves and breeds; predators eat it."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "O") -> None:
        """Create a prey and start its breed clock."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Update the breed clock."""
        self.breed_clock -= 1


class Predator(Animal):
    """Predator eats prey and starves if it doesn't eat in time."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "X") -> None:
        """Create a predator and start its starve and breed clocks."""
        Animal.__init__(self, island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Update the clocks; remove the predator if it starved."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Eat a neighboring prey, if any, and reset the starve clock."""
        if not self.moved and self.eat_neighbor(Prey):
            self.starve_clock = self.starve_time


class Human(Animal):
    """Human moves and breeds like an animal and eats predators, not prey."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = "H") -> None:
        """Create a human and start its breed, starve, and hunt clocks."""
        Animal.__init__(self, island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time
        self.hunt_clock = self.hunt_time

    def clock_tick(self) -> None:
        """Update the clocks; remove the human if it starved."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        self.hunt_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Every hunt_time ticks, eat a neighboring predator if there is one.

        Postcondition: after a kill, the starve clock is reset.
        """
        if not self.moved and self.hunt_clock <= 0:
            self.hunt_clock = self.hunt_time
            if self.eat_neighbor(Predator):
                self.starve_clock = self.starve_time


def main(predator_breed_time: int = 6, predator_starve_time: int = 4,
         initial_predators: int = 40, prey_breed_time: int = 3,
         initial_prey: int = 200, size: int = 20, ticks: int = 1000,
         human_breed_time: int = 15, human_starve_time: int = 20,
         human_hunt_time: int = 6, initial_humans: int = 4,
         stable_ticks: int = 50, seed: int | None = 0) -> None:
    """Run the simulation, print the island, and plot the populations.

    Stops when all three populations stay the same for stable_ticks ticks
    in a row, or after `ticks` ticks (at most 1000). seed makes the run
    repeatable; None gives a different run each time.
    """
    random.seed(seed)
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    prey_list = []
    predator_list = []
    human_list = []
    last = None
    unchanged = 0

    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print(isle)
    print("Tick  Prey  Predators  Humans")

    for i in range(min(ticks, 1000)):
        isle.clear_all_moved_flags()
        # each animal eats (if it hunts), moves, breeds, then ages one tick
        for x in range(size):
            for y in range(size):
                animal = isle.animal(x, y)
                if animal:
                    animal.eat()
                    animal.move()
                    animal.breed()
                    animal.clock_tick()

        counts = (isle.count_prey(), isle.count_predators(),
                  isle.count_humans())
        prey_list.append(counts[0])
        predator_list.append(counts[1])
        human_list.append(counts[2])
        if i % 50 == 0:
            print(f"{i:4d}  {counts[0]:4d}  {counts[1]:9d}  {counts[2]:6d}")

        # converged: no population changed for stable_ticks ticks in a row
        unchanged = unchanged + 1 if counts == last else 0
        last = counts
        if unchanged >= stable_ticks:
            print(f"Populations converged; stopped at tick {i}.")
            break

    print()
    print(isle)
    print(f"Final populations - prey: {prey_list[-1]}, predators: "
          f"{predator_list[-1]}, humans: {human_list[-1]}")

    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.xlabel("Time (ticks)")
    plt.ylabel("Population")
    plt.title("Prey, Predator, and Human Populations")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
