import random # for random numbers

KARMA_LIMIT = 500 # constant

"""
empty classes for raise our own exceptions
"""
class KillError(Exception):
    pass
class DrunkError(Exception):
    pass
class CarCrashError(Exception):
    pass
class GluttonyError(Exception):
    pass
class DepressionError(Exception):
    pass

def one_day():
    """
    function for random choice the exception from the list
    :return: random number from 1 to 7 if random number is not 1
    """
    if random.randint(1, 10) == 1:
        exception_class = random.choice([KillError, DrunkError, CarCrashError, GluttonyError, DepressionError])
        raise exception_class("A negative action has occurred!")
    else:
        return random.randint(1, 7)

def main():
    """
    main function; creating the counters: karma and days; opening the log file for writing the exceptions;
    infinity cycle while our karma is not 500: every day + 1, call function one_day() to check the exceptions and
    if random choice is any exception - write it to the log file;
    printing the total karma and finishing the simulation
    """
    karma = 0
    days = 0

    with open("karma.log", "w", encoding = "utf-8") as log_file:
        while True:
            if karma >= KARMA_LIMIT:
                break
            days += 1
            try:
                karma += one_day()
                print(f"Day - {days}. Karma: +{one_day()}. Total karma: {karma}")
            except KillError as e:
                print(f"Day - {days}. The killing has occurred! (KillError)")
                log_file.write(f"Error: {type(e).__name__}, karma: {karma}\n")
            except DrunkError as e:
                print(f"Day - {days}. The intoxication has occurred! (DrunkError)")
                log_file.write(f"Error: {type(e).__name__}, karma: {karma}\n")
            except CarCrashError as e:
                print(f"Day - {days}. The car crashing has occurred! (CarCrashError)")
                log_file.write(f"Error: {type(e).__name__}, karma: {karma}\n")
            except GluttonyError as e:
                print(f"Day - {days}. The gluttony has occurred! (GluttonyError)")
                log_file.write(f"Error: {type(e).__name__}, karma: {karma}\n")
            except DepressionError as e:
                print(f"Day - {days}. The depression has occurred! (GluttonyError)")
                log_file.write(f"Error: {type(e).__name__}, karma: {karma}\n")

        print(f"\nThe karma simulation is over per {days} days.")
        print(f"The total karma - {karma}")

# run the program
if __name__ == "__main__":
    main()