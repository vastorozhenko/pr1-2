
# SDLC Security Demo Project (Flask)

Навчальний демонстраційний проєкт для практичної роботи **«Інтеграція безпеки в SDLC»**.
Мета — показати, як впровадити вимоги безпеки, модель загроз, статичне (SAST) та динамічне тестування (DAST) у типовий цикл розробки.

## Швидкий старт (локально)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=src/app.py
export FLASK_ENV=development
export SECRET_KEY=dev-please-change-me
python src/db.py  # ініціалізація БД
flask run  # або: python src/app.py
```

Відкрийте: http://127.0.0.1:5000

## Структура
- `src/` — вихідний код Flask (наміри порушити безпечні практики для тренування сканерів).
- `docs/` — вимоги безпеки, модель загроз, реєстр ризиків, шаблони звітів.
- `.github/workflows/` — CI з **SAST** (Semgrep, Bandit, pip-audit) і **DAST** (OWASP ZAP baseline).
- `Dockerfile`, `docker-compose.yml` — контейнеризація.
- `Makefile` — корисні команди.

## Завдання студентів
Див. файл [`tasks.md`](tasks.md) — покроково для виконання і критерії оцінювання.

## Зауваження
Код містить **навмисні вразливості** (SQLi, XSS, слабка автентифікація, секрети у змінних оточення). Використовуйте лише в навчальних цілях.
