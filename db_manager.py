import sqlite3
from config import DATABASE

skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Telegram', 'Flask', 'HTML'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]

# Реальные проекты с GitHub (https://github.com/NightKaiDEV)
GITHUB = 'https://github.com/NightKaiDEV/'
MY_PROJECTS = [
    {
        'name': 'M1L4 Pokemon',
        'url': GITHUB + 'M1L4-pokemon',
        'description': 'Telegram-бот с покемонами: создание, кормление, тренировка и бои. '
                       'Данные берутся из PokeAPI, есть классы Pokemon, Wizard и Fighter.',
        'status': 'Разработан. Готов к использованию.',
        'skills': ['Python', 'API', 'Telegram'],
    },
    {
        'name': 'DayPlan',
        'url': GITHUB + 'dayplan',
        'description': 'Telegram-бот расписания: занятия по дням недели, хранятся в SQLite, '
                       'управление через inline-кнопки.',
        'status': 'Разработан. Готов к использованию.',
        'skills': ['Python', 'SQL', 'Telegram'],
    },
    {
        'name': 'ClimateHero',
        'url': GITHUB + 'kodland_lats_project',
        'description': 'Сайт о глобальном потеплении: регистрация, вход и советы, '
                       'подобранные под возраст пользователя (Flask + SQLAlchemy).',
        'status': 'Разработан. Готов к использованию.',
        'skills': ['Python', 'SQL', 'Flask', 'HTML'],
    },
    {
        'name': 'Speak Game',
        'url': GITHUB + 'speak-game',
        'description': 'Консольная игра на произношение: нужно сказать английский перевод слова. '
                       'Распознавание речи и перевод через Google (3 уровня сложности).',
        'status': 'Разработан. Готов к использованию.',
        'skills': ['Python', 'API'],
    },
    {
        'name': 'Chat Manager Bot',
        'url': GITHUB + '3leessonkodland',
        'description': 'Telegram-бот для управления чатом: бан по ответу на сообщение, '
                       'антиспам, приветствие новых участников.',
        'status': 'Разработан. Готов к использованию.',
        'skills': ['Python', 'Telegram'],
    },
    {
        'name': 'Kodland Bot',
        'url': GITHUB + 'kodland-project',
        'description': 'Учебный Telegram-бот: команды /start, /info, /coin, ответ на фото и викторина.',
        'status': 'Разработан. Готов к использованию.',
        'skills': ['Python', 'Telegram'],
    },
    {
        'name': 'SQLite Starter',
        'url': GITHUB + 'SQlite-starting-teach',
        'description': 'Первое знакомство с SQLite: создание таблицы, вставка, выборка и сортировка.',
        'status': 'Завершен. Не поддерживается',
        'skills': ['Python', 'SQL'],
    },
]

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS projects (
                            project_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            description TEXT,
                            url TEXT,
                            status_id INTEGER,
                            FOREIGN KEY(status_id) REFERENCES status(status_id)
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS skills (
                            skill_id INTEGER PRIMARY KEY,
                            skill_name TEXT UNIQUE
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                            project_id INTEGER,
                            skill_id INTEGER,
                            UNIQUE(project_id, skill_id),
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
                        )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS status (
                            status_id INTEGER PRIMARY KEY,
                            status_name TEXT UNIQUE
                        )''')
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)

    def import_my_projects(self, user_id):
        """Добавляет в базу мои проекты с GitHub (со ссылками, описанием, статусом и навыками).
        Можно вызывать много раз: уже существующие проекты пропускаются."""
        for p in MY_PROJECTS:
            exists = self.__select_data(
                'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?',
                (p['name'], user_id))
            if exists:
                continue
            self.insert_project([(user_id, p['name'], p['url'], self.get_status_id(p['status']))])
            self.update_projects('description', (p['description'], p['name'], user_id))
            for skill in p['skills']:
                self.insert_skill(user_id, p['name'], skill)


    def insert_project(self, data):
        # data: список кортежей (user_id, project_name, url, status_id)
        sql = 'INSERT OR IGNORE INTO projects (user_id, project_name, url, status_id) values(?, ?, ?, ?)'
        self.__executemany(sql, data)


    def insert_skill(self, user_id, project_name, skill):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        project_id = self.__select_data(sql, (project_name, user_id))[0][0]
        skill_id = self.__select_data('SELECT skill_id FROM skills WHERE skill_name = ?', (skill,))[0][0]
        data = [(project_id, skill_id)]
        sql = 'INSERT OR IGNORE INTO project_skills VALUES(?, ?)'
        self.__executemany(sql, data)


    def get_statuses(self):
        sql = 'SELECT status_name FROM status'
        return self.__select_data(sql)


    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        if res: return res[0][0]
        else: return None

    def get_projects(self, user_id):
        sql = 'SELECT * FROM projects WHERE user_id = ?'
        return self.__select_data(sql, data = (user_id,))

    def get_project_id(self, project_name, user_id):
        return self.__select_data(sql='SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?  ', data = (project_name, user_id,))[0][0]

    def get_skills(self):
        return self.__select_data(sql='SELECT * FROM skills')

    def get_project_skills(self, project_name):
        res = self.__select_data(sql='''SELECT skill_name FROM projects
JOIN project_skills ON projects.project_id = project_skills.project_id
JOIN skills ON skills.skill_id = project_skills.skill_id
WHERE project_name = ?''', data = (project_name,) )
        return ', '.join([x[0] for x in res])

    def get_project_info(self, user_id, project_name):
        sql = """
SELECT project_name, description, url, status_name FROM projects
JOIN status ON
status.status_id = projects.status_id
WHERE project_name=? AND user_id=?
"""
        return self.__select_data(sql=sql, data = (project_name, user_id))


    def update_projects(self, param, data):
       
        allowed = {'project_name', 'description', 'url', 'status_id'}
        if param not in allowed:
            raise ValueError(f'Нельзя обновлять поле: {param}')
        sql = f"UPDATE projects SET {param} = ? WHERE project_name = ? AND user_id = ?"
        self.__executemany(sql, [data])


    def delete_project(self, user_id, project_id):
        sql = 'DELETE FROM projects WHERE user_id = ? AND project_id = ?'
        self.__executemany(sql, [(user_id, project_id)])

    def delete_skill(self, project_id, skill_id):
        sql = 'DELETE FROM project_skills WHERE skill_id = ? AND project_id = ?'
        self.__executemany(sql, [(skill_id, project_id)])


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()

    user = 1  # в боте здесь будет Telegram user_id
    manager.import_my_projects(user)
    manager.import_my_projects(user)  # повторный вызов не создаёт дубликатов

    print('Мои проекты в базе:')
    for p in manager.get_projects(user):
        name = p[2]
        info = manager.get_project_info(user, name)[0]
        print(f'- {info[0]} [{info[3]}]')
        print(f'  {info[1]}')
        print(f'  {info[2]}')
        print(f'  Навыки: {manager.get_project_skills(name)}')

    # --- проверка остальных методов на временном проекте ---
    manager.insert_project([(user, 'Тест', 'https://example.com', manager.get_status_id('На этапе проектирования'))])
    manager.insert_skill(user, 'Тест', 'SQL')
    manager.update_projects('status_id', (manager.get_status_id('Обновлен'), 'Тест', user))
    print('\nТестовый проект:', manager.get_project_info(user, 'Тест'), '| навыки:', manager.get_project_skills('Тест'))
    test_id = manager.get_project_id('Тест', user)
    manager.delete_skill(test_id, 2)  # SQL, skill_id = 2
    manager.delete_project(user, test_id)
    print('После удаления теста проектов:', len(manager.get_projects(user)))
