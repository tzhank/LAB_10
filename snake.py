import psycopg2
import random
import time
import curses

# Подключение к базе данных
def connect_db():
    return psycopg2.connect(
        dbname="snake",  # Имя базы данных
        user="postgres",    # Имя пользователя
        password="tima2007",  # Твой пароль
        host="localhost",  # Хост базы данных
        port="5432"  # Порт базы данных
    )

# Функция для получения или создания пользователя
def get_or_create_user(username):
    conn = connect_db()
    cur = conn.cursor()

    # Проверка, существует ли пользователь в базе
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    
    if user:
        print(f"Пользователь {username} найден в базе!")
        cur.close()
        conn.close()
        return user[0]  # Возвращаем ID пользователя
    else:
        # Если пользователя нет в базе, добавляем его
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        conn.commit()  # Сохраняем изменения
        print(f"Пользователь {username} добавлен в базу!")
        user_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return user_id

# Функция для обновления данных о счете
def update_user_score(user_id, score, level):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
        (user_id, score, level)
    )
    conn.commit()  # Сохраняем изменения
    print(f"Данные о счете для пользователя {user_id} обновлены!")

    cur.close()
    conn.close()

# Настройка игры
def main(stdscr):
    # Инициализация игры
    curses.curs_set(0)  # Скрытие курсора
    stdscr.nodelay(1)  # Ожидание без блокировки
    stdscr.timeout(100)  # Время задержки для обновления экрана

    sh, sw = stdscr.getmaxyx()  # Размеры экрана
    w = curses.newwin(sh, sw, 0, 0)  # Создание нового окна

    # Начальные параметры змейки
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_PI)  # Отображаем еду

    key = curses.KEY_RIGHT  # Направление движения
    score = 0
    level = 1

    username = input("Введите имя пользователя: ")
    user_id = get_or_create_user(username)

    # Игра
    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        # Проверка на выход за границы
        if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
            curses.endwin()  # Завершаем игру при столкновении
            print("Game Over!")
            update_user_score(user_id, score, level)
            break

        # Двигаем змейку
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        # Проверка на съеденную еду
        if snake[0] == food:
            score += 10
            level += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 1),
                    random.randint(1, sw - 1)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Отображение змейки
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

# Запуск игры
if __name__ == "__main__":
    curses.wrapper(main)
