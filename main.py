films = [
    'Крепкий орешек', 'Назад в будущее', 'Таксист',
    'Леон', 'Богемская рапсодия', 'Город грехов',
    'Мементо', 'Отступники', 'Деревня',
    'Проклятый остров', 'Начало', 'Матрица'
]

top_films = []

def append_film(film):
    top_films.append(film)
    main()

def insert_film(film):
    if film not in top_films:
        index_film = int(input("Enter the index you wanna insert your film: "))
        top_films.insert(index_film + 1, film)
    else:
        print("You have already inserted this film!")
    main()

def remove_film(film):
    if film in top_films:
        top_films.remove(film)
    else:
        print("You have not appended this film!")
    main()

def main():
    print("Your list of the top films:", top_films)
    name_film = input("Please enter the film's name: ")
    if name_film in films:
        print("The commands: append, insert, remove")
        enter_command = input("Please enter the command: ").lower()
        if enter_command == "append":
            append_film(name_film)
        elif enter_command == "insert":
            insert_film(name_film)
        elif enter_command == "remove":
            remove_film(name_film)
        else:
            print("Please enter a valid command")
    else:
        print("Sorry! We don't have this film!")

main()