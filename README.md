# Лабораторная 11 — CI/CD (GitHub Actions + Selenium + Pages)

Кратко по [lab.md](lab.md): простая страница с формой, ветки `main` / `dev` / `fix`, автотесты на push/PR, деплой на **GitHub Pages** только с ветки **main** после успешных тестов.

## Локальный запуск тестов

**Без сервера** (по умолчанию открывается `file:///…/index.html`):

```bash
cd lab11
pip install -r requirements.txt
pytest tests -v
```

**Через HTTP** (как в CI):

```bash
cd lab11
python3 -m http.server 8765 --bind 127.0.0.1 &
sleep 1
BASE_URL=http://127.0.0.1:8765 pytest tests -v
kill %1
```

Или одной сессией:

```bash
cd lab11 && python3 -m http.server 8765 --bind 127.0.0.1 &
sleep 1 && BASE_URL=http://127.0.0.1:8765 pytest tests -v
```

## GitHub

1. Включите **Settings → Pages**: источник — **GitHub Actions** (не branch).
2. Репозиторий с монолитом TPO: workflow уже в `.github/workflows/ci.yml`, триггер только при изменениях в `lab11/` или самом workflow.
3. Если заводите **отдельный** репозиторий под лабу: скопируйте в его корень содержимое папки `lab11` и файл `.github/workflows/ci.yml`, затем в `ci.yml` удалите `defaults.working-directory` и префикс `lab11/` у шага с `cp` (оставьте `cp index.html _site/index.html`), блок `paths:` в `on:` можно убрать.

## Ветки и PR (п. 6–7 методички)

| Ветка | Назначение |
|--------|------------|
| `main` | продакшен; деплой Pages только отсюда |
| `dev` | основная разработка |
| `fix/*` | задачи / фиксы от `dev` |

Не коммитьте напрямую в `main`: изменения через **Pull Request**.

Типичный сценарий:

1. От ветки `dev` создайте `fix/lab11-demo`.
2. В `lab11/index.html` поменяйте текст кнопки с **Отправить** на что угодно другое → закоммитьте и запушьте → откройте **PR в `dev`** → CI упадёт на тесте `test_submit_button_label_and_demo_success_message`.
3. Верните текст **Отправить** → CI зелёный → merge в `dev`.
4. **PR из `dev` в `main`** → снова CI → после merge на `main` запустится деплой Pages.

Так же можно временно сломать заголовок `#page-title`, чтобы упали тесты по заголовку.

## Что рассказать на защите (чеклист)

- Что такое CI/CD и зачем в учебном проекте.
- Где workflow (`.github/workflows/ci.yml`): триггеры, job `test`, job `deploy-pages` с условием `main`.
- Как подключены тесты: pytest + Selenium, headless Chrome на runner.
- Показать в GitHub **ветки**, при желании — **branch protection** / reviewers (не обязательно по методичке).
- Осознанно внести ошибку → упавший workflow → исправление → зелёный прогон → merge → сайт на Pages.

## Полезная статья из методички

[Habr — CI/CD обзор](https://habr.com/ru/companies/intec_balance/articles/865098/)
