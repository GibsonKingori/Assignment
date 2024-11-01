from abc import ABC, abstractmethod

# User class representing a user in the system
class User:
    def __init__(self, name: str, balance: float):
        self.name = name
        self._balance = balance  # Encapsulated balance

    def get_balance(self):
        return self._balance

    def add_balance(self, amount: float):
        if amount > 0:
            self._balance += amount
            print(f"{amount} added to balance. New balance is {self._balance}")
        else:
            print("Amount to add must be positive.")

    def deduct_balance(self, amount: float):
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"{amount} deducted from balance. New balance is {self._balance}")
        else:
            print("Insufficient balance or invalid amount.")


# Abstract base class for travel packages
class TravelPackage(ABC):
    def __init__(self, package_name: str, price: float):
        self.package_name = package_name
        self.price = price

    @abstractmethod
    def calculate_price(self):
        pass


# DomesticPackage subclass
class DomesticPackage(TravelPackage):
    def __init__(self, package_name: str, price: float, discount: float = 0.1):
        super().__init__(package_name, price)
        self.discount = discount

    # Override calculate_price with a discount for domestic packages
    def calculate_price(self):
        return self.price * (1 - self.discount)


# InternationalPackage subclass
class InternationalPackage(TravelPackage):
    def __init__(self, package_name: str, price: float, surcharge: float = 0.2):
        super().__init__(package_name, price)
        self.surcharge = surcharge

    # Override calculate_price with an added surcharge for international packages
    def calculate_price(self):
        return self.price * (1 + self.surcharge)


# BookingSystem class for managing travel bookings
class BookingSystem:
    def __init__(self):
        self.users = {}
        self.packages = []
        self.bookings = []

    def add_user(self, name: str, balance: float):
        user = User(name, balance)
        self.users[name] = user
        print(f"User '{name}' added with balance {balance}.")

    def add_package(self, package: TravelPackage):
        self.packages.append(package)
        print(f"Package '{package.package_name}' added.")

    def create_booking(self, user_name: str, package_name: str):
        user = self.users.get(user_name)
        package = next((p for p in self.packages if p.package_name == package_name), None)

        if user and package:
            package_price = package.calculate_price()
            if user.get_balance() >= package_price:
                user.deduct_balance(package_price)
                self.bookings.append((user_name, package_name))
                print(f"Booking created for {user_name} on package '{package_name}'.")
            else:
                print("Insufficient balance to complete booking.")
        else:
            print("User or package not found.")

    def cancel_booking(self, user_name: str, package_name: str):
        booking = (user_name, package_name)
        if booking in self.bookings:
            self.bookings.remove(booking)
            print(f"Booking cancelled for {user_name} on package '{package_name}'.")
        else:
            print("Booking not found.")

# Create instances and simulate interactions
if __name__ == "__main__":
    # Initialize the booking system
    booking_system = BookingSystem()

    # Adding users
    booking_system.add_user("Alice", 1000)
    booking_system.add_user("Bob", 500)

    # Adding travel packages
    domestic_package = DomesticPackage("Beach Getaway", 200)
    international_package = InternationalPackage("Paris Adventure", 800)

    booking_system.add_package(domestic_package)
    booking_system.add_package(international_package)

    # Create bookings
    booking_system.create_booking("Alice", "Beach Getaway")
    booking_system.create_booking("Bob", "Paris Adventure")

    # Cancel a booking
    booking_system.cancel_booking("Alice", "Beach Getaway")
