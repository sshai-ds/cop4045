"""Problem 2: university parking permits."""


class ParkingPermit:
    """Parking permit with an owner, months purchased, and a fee schedule."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, float]) -> None:
        """Store the owner's name, the number of months, and the fees.

        Precondition: months >= 1.
        """
        self.owner = owner
        self.months = months
        self.fees = fees

    def cost(self) -> float:
        """Return the permit cost; each subclass overrides this.

        Raises: NotImplementedError for a plain ParkingPermit.
        """
        raise NotImplementedError("subclasses define cost()")

    def __str__(self) -> str:
        """Return a readable description, e.g. 'Ana Lopez, 4 months'."""
        return f"{self.owner}, {self.months} months"

    def __repr__(self) -> str:
        """Return a constructor call that recreates the permit."""
        return f"ParkingPermit({self.owner!r}, {self.months}, {self.fees})"


class StudentPermit(ParkingPermit):
    """Student permit; also stores the number of vehicles registered."""

    def __init__(self, owner: str, months: int, fees: dict[str, float],
                 vehicles: int) -> None:
        """Create a student permit.

        Precondition: vehicles >= 1 and fees has the keys 'monthly' and
            'extra_vehicle'.
        """
        super().__init__(owner, months, fees)
        self.vehicles = vehicles

    def cost(self) -> float:
        """Return the monthly fee times months, plus a one-time fee for
        each vehicle after the first.
        """
        return (self.months * self.fees["monthly"]
                + (self.vehicles - 1) * self.fees["extra_vehicle"])

    def __str__(self) -> str:
        """Return a readable description of the student permit."""
        return (f"Student permit: {super().__str__()}, "
                f"vehicles: {self.vehicles}")

    def __repr__(self) -> str:
        """Return a constructor call that recreates the permit."""
        return (f"StudentPermit({self.owner!r}, {self.months}, {self.fees}, "
                f"{self.vehicles})")


class FacultyPermit(ParkingPermit):
    """Faculty permit; also stores whether garage access is included."""

    def __init__(self, owner: str, months: int, fees: dict[str, float],
                 garage: bool) -> None:
        """Create a faculty permit.

        Precondition: fees has the keys 'monthly' and 'garage'.
        """
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """Return months times the monthly fee, plus the monthly garage fee
        if garage access is included.
        """
        monthly = self.fees["monthly"]
        if self.garage:
            monthly += self.fees["garage"]
        return self.months * monthly

    def __str__(self) -> str:
        """Return a readable description of the faculty permit."""
        access = "with" if self.garage else "without"
        return f"Faculty permit: {super().__str__()}, {access} garage"

    def __repr__(self) -> str:
        """Return a constructor call that recreates the permit."""
        return (f"FacultyPermit({self.owner!r}, {self.months}, {self.fees}, "
                f"{self.garage})")


def summarize_list(permits: list[ParkingPermit]) -> float:
    """Print each permit with its cost and return the total revenue."""
    total = 0.0
    for permit in permits:
        cost = permit.cost()
        print(f"{permit} -> ${cost:.2f}")
        total += cost
    return total


def main() -> None:
    """Show how the permit classes and summarize_list() are used."""
    student_fees = {"monthly": 25, "extra_vehicle": 10}
    faculty_fees = {"monthly": 40, "garage": 15}
    permits = [
        StudentPermit("Ana Lopez", 4, student_fees, 1),
        StudentPermit("Ben Carter", 12, student_fees, 3),
        FacultyPermit("Dr. Kim", 6, faculty_fees, True),
        FacultyPermit("Dr. Patel", 3, faculty_fees, False),
    ]
    print("Permits:")
    for permit in permits:
        print(repr(permit))
    print("\nCosts:")
    total = summarize_list(permits)
    print(f"Total revenue: ${total:.2f}")


if __name__ == "__main__":
    main()
