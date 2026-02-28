import math # нужен для обработки математических операций

def calculator() -> None:
    """
    Основная функция для отображения главного меню и выбора действий
    :return: Ничего не возвращает, обрабатывает данные от пользователя
    """
    print("\n1) Сложение (+) \n2) Вычитание (-) \n3) Умножение (*) \n4) Деление (/) \n5) Возведение в степень (**) "
          "\n6) Извлечение корня числа (sqrt) \n7) Факториал числа (!) \n8) Синус (sin) \n9) Косинус (cos)")
    try:
        count_numbers = int(input("Выберите сколько чисел будет в операции - 1 или 2: "))
        if count_numbers == 1:
            choice = int(input("Выберите какую операцию хотите использовать: "))
            number = float(input("Введите число: "))
            one_number(number, choice)
        elif count_numbers == 2:
            choice = int(input("Выберите какую операцию хотите использовать: "))
            first_number = float(input("Введите первое число: "))
            second_number = float(input("Введите второе число: "))
            two_numbers(first_number, second_number, choice)
        else:
            print("Ошибка!")
            return
    except ValueError:
        print("Ошибка! Введены не корректные данные!")
        calculator()

def one_number(number: float, choice: int) -> None:
    """
    Функция для обработки математических операций, где требуется только одно число
    :param number: само число с которым будем работать
    :param choice: Число - выбор от пользователя что он хочет что бы калькулятор делал
    :return: Ничего не возвращает, сразу выводи на экран ответ
    """
    if choice == 5:
        number_for_exponentiation = float(input(f"Введите число в которое хотите возвести {number}: "))
        print("Ответ:", number ** number_for_exponentiation)
    if choice == 6:
        print("Ответ:", math.sqrt(number))
    elif choice == 7:
        print("Ответ:", math.factorial(int(number)))
    elif choice == 8:
        print("Ответ:", math.sin(number))
    elif choice == 9:
        print("Ответ:", math.cos(number))

    # дает выбор пользователю продолжить вычисления или выйти из приложения
    continue_or_exit = int(input("Выберите действие: 1 - выйти из приложения или 2 - продолжить: "))
    if continue_or_exit == 1:
        print("Всего доброго!")
        exit()
    elif continue_or_exit == 2:
        calculator()

def two_numbers(first_number: float, second_number: float, choice: int) -> None:
    """
    Функция для вычисления математических операций с двумя числами
    :param first_number: первое число от пользователя
    :param second_number: второе число от пользователя
    :param choice: выбор операции
    :return: ничего не возвращает, выводит результат на экран
    """
    if choice == 1:
        print("Ответ:", first_number + second_number)
    elif choice == 2:
        print("Ответ:", first_number - second_number)
    elif choice == 3:
        print("Ответ:", first_number * second_number)
    elif choice == 4:
        try:
            print("Ответ:", first_number / second_number)
        except ZeroDivisionError:
            print("Делить на 0 нельзя!")
            calculator()

    # дает выбор пользователю продолжить вычисления или выйти из приложения
    continue_or_exit = int(input("Выберите действие: 1 - выйти из приложения или 2 - продолжить: "))
    if continue_or_exit == 1:
        print("Всего доброго!")
        exit()
    elif continue_or_exit == 2:
        calculator()

# запуск программы
if __name__ == "__main__":
    print("Добро пожаловать в простой калькулятор. Вот какие операции доступны:")
    calculator()