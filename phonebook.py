import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="phonebook1",
    user="postgres",
    password="tima2007", 
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Вставка через консоль
def insert_manual():
    username = input("Введите имя: ")
    phone = input("Введите номер: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print("Контакт добавлен!")

# Вставка из CSV
def insert_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['username']
            phone = row['phone']
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print("Данные из CSV успешно добавлены!")

# Обновление данных
def update_contact():
    username = input("Введите имя контакта, который хотите обновить: ")
    field = input("Что хотите обновить? (username/phone): ")
    new_value = input("Введите новое значение: ")
    
    if field == "username":
        cur.execute("UPDATE phonebook SET username = %s WHERE username = %s", (new_value, username))
    elif field == "phone":
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_value, username))
    else:
        print("Неверное поле.")
        return
    
    conn.commit()
    print("Контакт обновлён!")

# Поиск с фильтрами
def search():
    keyword = input("Введите имя или номер для поиска: ")
    cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s OR phone ILIKE %s", (f"%{keyword}%", f"%{keyword}%"))
    results = cur.fetchall()
    
    if results:
        for row in results:
            print(f"Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("Контакты не найдены.")

# Удаление
def delete_contact():
    keyword = input("Введите имя или номер, который хотите удалить: ")
    cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s", (keyword, keyword))
    conn.commit()
    print("Контакт удалён (если был найден).")

# Главное меню
def main():
    while True:
        print("\n===== PhoneBook Меню =====")
        print("1. Добавить контакт (ручной ввод)")
        print("2. Загрузить контакты из CSV")
        print("3. Обновить контакт")
        print("4. Поиск")
        print("5. Удалить контакт")
        print("0. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            insert_manual()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")

    cur.close()
    conn.close()
    print("До свидания!")

# Запуск
if __name__ == "__main__":
    main()
