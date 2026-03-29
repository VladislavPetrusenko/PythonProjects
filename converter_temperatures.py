def converter(cel: float, far: float) -> str:
    """
    Переводит градусы Цельсия в Фаренгейты и наоборот по формулам.
    
    Args:
        cel (float): градусы Цельсия
        far (float): градусы Фаренгейта
    """
    farengheit = round((cel * 9/5 + 32), 2)
    celsius = round(((far - 32) * 5/9), 2)
    
    return f"Цельсия в Фаренгейты -> {farengheit} F. Фаренгейты в Цельсиях -> {celsius} C."

def main() -> str:
    celcius = float(input("Введите число в Цельсиях, которое хотите перевести в Фаренгейты: "))
    farengheit = float(input("Введите число в Фаренгейтах, которое хотите перевести в Цельсии: "))
        
    return converter(celcius, farengheit)

if __name__ == "__main__":
    print(main())