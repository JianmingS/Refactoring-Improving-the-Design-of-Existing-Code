from abc import ABC, abstractmethod


class Price(ABC):
    @abstractmethod
    def get_price_code(self):
        pass

    @abstractmethod
    def get_charge(self, days_rented):
        pass

    def get_frequent_renter_points(self, days_rented):
        return 1


class ChildrensPrice(Price):
    def get_price_code(self):
        return Movie.CHILDRENS

    def get_charge(self, days_rented):
        result = 1.5
        if days_rented > 3:
            result += (days_rented - 3) * 1.5
        return result


class NewReleasePrice(Price):
    def get_price_code(self):
        return Movie.NEW_RELEASE

    def get_charge(self, days_rented):
        return days_rented * 3

    def get_frequent_renter_points(self, days_rented):
        return days_rented > 1 and 2 or 1


class RegularPrice(Price):
    def get_price_code(self):
        return Movie.REGULAR

    def get_charge(self, days_rented):
        result = 2
        if days_rented > 2:
            result += (days_rented - 2) * 1.5
        return result


class Movie(object):
    REGULAR = 0
    NEW_RELEASE = 1
    CHILDRENS = 2

    def __init__(self, title, price_code):
        self._title = title
        self._price = None
        self.set_price_code(price_code)

    def get_price_code(self):
        return self._price.get_price_code()

    def set_price_code(self, arg):
        if arg == self.REGULAR:
            self._price = RegularPrice()
        elif arg == self.CHILDRENS:
            self._price = ChildrensPrice()
        elif arg == self.NEW_RELEASE:
            self._price = NewReleasePrice()
        else:
            raise Exception('Incorrect Price Code')

    def get_title(self):
        return self._title

    def get_charge(self, days_rented):
        return self._price.get_charge(days_rented)

    def get_frequent_renter_points(self, days_rented):
        return self._price.get_frequent_renter_points(days_rented)


class Rental(object):

    def __init__(self, movie, days_rented):
        self._movie = movie
        self._days_rented = days_rented

    def get_days_rented(self):
        return self._days_rented

    def get_movie(self):
        return self._movie

    def get_charge(self):
        return self.get_movie().get_charge(self.get_days_rented())

    def get_frequent_renter_points(self):
        return self.get_movie().get_frequent_renter_points(self.get_days_rented())


class Customer(object):

    def __init__(self, name):
        self._name = name
        self._rentals = []

    def addRental(self, arg):
        self._rentals.append(arg)

    def get_name(self):
        return self._name

    def statement(self):
        result = 'Rental Record for ' + self.get_name() + '\n'
        for each in self._rentals:
            result += '\t' + each.get_movie().get_title() + '\t' + \
                str(each.get_charge()) + '\n'

        result += 'Amount owed is ' + str(self.get_total_charge()) + '\n'
        result += 'You earned ' + \
            str(self.get_total_frequent_renter_points()) + \
            ' frequent renter points'
        return result

    def html_statement(self):
        result = '<h1>Rentals for <em>' + self.get_name() + '</em></h1><p>\n'

        for each in self._rentals:
            result += each.get_movie().get_title() + ': ' + str(each.get_charge()) + '<br>\n'
        result += '<p>You own <em>' + \
            str(self.get_total_charge()) + '</em></p>\n'
        result += 'On this rental you earned <em>' \
            + str(self.get_total_frequent_renter_points()) \
            + '</em> frequent renter points</p>'

        return result

    def get_total_charge(self):
        result = 0
        for a_rentals in self._rentals:
            result += a_rentals.get_charge()
        return result

    def get_total_frequent_renter_points(self):
        result = 0
        for a_rental in self._rentals:
            result += a_rental.get_frequent_renter_points()
        return result


if __name__ == "__main__":
    regular1 = Movie('regular1', Movie.REGULAR)
    new_release1 = Movie('new_release1', Movie.NEW_RELEASE)
    children1 = Movie('children1', Movie.CHILDRENS)

    A = Customer('A')
    A.addRental(Rental(regular1, 3))
    A.addRental(Rental(new_release1, 2))
    A.addRental(Rental(children1, 5))

    print(A.statement())
    print('\n\n')
    print(A.html_statement())
