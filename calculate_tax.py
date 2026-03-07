class Property:
    """
    Base class for all properties
    :arg worth: the amount worth this property
    """
    def __init__(self, worth):
        self.worth = worth

    def calculate_tax(self):
        """
        pass this method, subclasses must implement this method
        """
        raise NotImplementedError("Subclasses must implement this method")

class Apartment(Property):
    """
    class for calculate properties for apartment
    :arg worth: the amount worth this property
    """
    def __init__(self, worth):
        super().__init__(worth)

    def calculate_tax(self):
        """
        calculating tax for apartment
        :return: tax (float)
        """
        tax = self.worth / 1000
        return tax

class Car(Property):
    """
    class for calculate properties for car
    :arg worth: the amount worth this property
    """
    def __init__(self, worth):
        super().__init__(worth)

    def calculate_tax(self):
        """
        calculating tax for car
        :return: tax (float)
        """
        tax = self.worth / 200
        return tax

class CountryHouse(Property):
    """
    class for calculate properties for country house
    :arg worth: the amount worth this property
    """
    def __init__(self, worth):
        super().__init__(worth)

    def calculate_tax(self):
        """
        calculating tax for country house
        :return: tax (float)
        """
        tax = self.worth / 500
        return tax

def main():
    """
    main function for program, input the worth of the properties, creating the samples for classes
    :return: if inputs - error, finish the program
    """
    try:
        money = int(input("How much money do you have? "))
        apartment_worth = int(input("Enter worth of apartment: "))
        car_worth = int(input("Enter worth of car: "))
        country_house_worth = int(input("Enter worth of country house: "))
    except ValueError:
        print("Error! Must be an integer numbers!")
        return

    apartment = Apartment(apartment_worth)
    car = Car(car_worth)
    country_house = CountryHouse(country_house_worth)

    print(f"The tax for apartment will be {apartment.calculate_tax()} RUB")
    print(f"The tax for car will be {car.calculate_tax()} RUB")
    print(f"The tax for country house will be {country_house.calculate_tax()} RUB")

    total_tax = apartment.calculate_tax() + car.calculate_tax() + country_house.calculate_tax()
    print(f"The total tax for properties will be {total_tax} RUB")

    if money >= total_tax:
        print("You have the money to bill the taxes!")
    else:
        print("Oh... You don't have enough money to bill the taxes!")
        not_enough_money = total_tax - money
        print(f"You don't have enough {not_enough_money} RUB to bill the taxes!")

# run the program
if __name__ == "__main__":
    main()