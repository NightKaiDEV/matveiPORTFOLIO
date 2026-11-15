# matveiPORTFOLIO
<div align="center">

# 🌙 Night Kai — Telegram-бот визитка

Бот-портфолио, который рассказывает о разработчике и показывает его проекты прямо в Telegram.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-Telegram%20Bot-26A5E4?logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-database-003B57?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/status-ready-success)

</div>

---

## ✨ Возможности

После команды `/start` бот присылает меню с инлайн-кнопками:

| Кнопка | Что делает |
|---|---|
| 👤 **Про меня** | Показывает рассказ о разработчике (по README профиля на GitHub) |
| 📁 **Мои проекты** | Открывает список проектов из базы данных |

Внутри списка проектов у каждого есть своя карточка:

- 📝 описание проекта
- 📌 статус (например, «Разработан. Готов к использованию.»)
- 🛠 используемые навыки и технологии
- 🔗 кнопка **«Открыть на GitHub»**

Бот не засоряет чат: при нажатии на кнопки он **редактирует то же сообщение**, а не отправляет новые.

---

## 🧱 Структура проекта

```
project_bot/
├── bot.py               # Telegram-бот: меню, кнопки, обработчики
├── db_manager.py        # Класс DB_Manager: работа с SQLite
├── config.example.py    # Пример настроек (скопируй в config.py)
├── config.py            # Твои секреты: токен и имя базы (не попадает в git)
├── requirements.txt     # Зависимости
└── .gitignore
```

---

## 🚀 Установка и запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/NightKaiDEV/project_bot.git
cd project_bot
```

### 2. Создай виртуальное окружение и установи зависимости

**Linux / macOS (bash, zsh):**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Linux (fish):**
```fish
python -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Настрой `config.py`

Скопируй пример и впиши свой токен от [@BotFather](https://t.me/BotFather):

```bash
cp config.example.py config.py
```

```python
token = "ТОКЕН_ОТ_BOTFATHER"
DATABASE = "portfolio_db"
```

> ⚠️ Файл `config.py` добавлен в `.gitignore`. Никогда не публикуй токен бота.
> Если он всё-таки утёк, отзови его в @BotFather командой `/revoke`.

### 4. Запусти бота

```bash
python bot.py
```

При первом запуске бот сам создаст таблицы и добавит проекты в базу. Повторные запуски дубликатов не создают.

---

## 🗄 База данных

Данные хранятся в SQLite. Работу с ней берёт на себя класс `DB_Manager`.

```
projects          project_skills        skills
─────────         ───────────────       ─────────
project_id  ◄──── project_id            skill_id
user_id           skill_id ───────────► skill_name
project_name
description       status
url               ─────────
status_id ──────► status_id
                  status_name
```

Основные методы `DB_Manager`:

| Метод | Назначение |
|---|---|
| `create_tables()` | Создаёт таблицы |
| `default_insert()` | Добавляет навыки и статусы по умолчанию |
| `import_my_projects(user_id)` | Добавляет мои проекты с GitHub |
| `insert_project(data)` / `insert_skill(...)` | Добавление проекта и навыков |
| `get_projects(user_id)` / `get_project_info(...)` | Получение проектов и подробностей |
| `update_projects(param, data)` | Изменение полей проекта |
| `delete_project(...)` / `delete_skill(...)` | Удаление |

---

## 📂 Проекты в портфолио

| Проект | Технологии |
|---|---|
| **M1L4 Pokemon**: бот с покемонами на PokeAPI | Python, API, Telegram |
| **DayPlan**: бот-расписание | Python, SQL, Telegram |
| **ClimateHero**: сайт о глобальном потеплении | Python, SQL, Flask, HTML |
| **Speak Game**: игра на произношение | Python, API |
| **Chat Manager Bot**: бан, антиспам, приветствие | Python, Telegram |
| **Kodland Bot**: учебный бот | Python, Telegram |
| **SQLite Starter**: знакомство с SQLite | Python, SQL |

---

## 🛠 Технологии

- [Python](https://www.python.org/)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [SQLite](https://www.sqlite.org/)

---

## 👤 Автор

**Matvei (Night Kai)**: ночной разработчик, который кодит при лунном свете. 🌙

[![GitHub](https://img.shields.io/badge/GitHub-NightKaiDEV-181717?logo=github&logoColor=white)](https://github.com/NightKaiDEV)

> Каждая ошибка — это урок. Продолжай делать, даже в 3 часа ночи.
