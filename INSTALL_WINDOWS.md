# 🪟 Установка Voice to Text на Windows

Полная инструкция по установке и использованию программы на Windows.

## 📋 Требования

- **Windows 7 и выше** (Windows 10/11 рекомендуется)
- **Python 3.7 или выше** (скачать с www.python.org)
- **Микрофон** и разрешение на доступ к микрофону
- **Интернет-соединение** для использования Google Speech Recognition API

## 🚀 Пошаговая установка

### Шаг 1: Установка Python

1. Переходим на https://www.python.org/downloads/
2. Скачиваем **Python 3.10+** (для Windows)
3. Запускаем установщик
4. ⚠️ **ВАЖНО**: Отмечаем галочку "Add Python to PATH"
5. Нажимаем "Install Now"

**Проверка установки:**
```cmd
python --version
```

### Шаг 2: Проверка микрофона

1. Открываем **Параметры звука** (Settings → Sound)
2. Проверяем что микрофон включен и доступен
3. Тестируем микрофон в параметрах

### Шаг 3: Загрузка проекта

```cmd
# Открываем Command Prompt или PowerShell
# Переходим в папку с проектом
cd C:\path\to\Sound_text

# Или клонируем с GitHub
git clone https://github.com/codemag33/Sound_text.git
cd Sound_text
```

### Шаг 4: Установка зависимостей

```cmd
# Обновляем pip
python -m pip install --upgrade pip

# Устанавливаем необходимые пакеты
pip install -r requirements.txt

# Опционально: для красивых уведомлений
pip install win10toast
```

**Проверка установки:**
```cmd
python -c "import speech_recognition; import pyperclip; print('✅ Все зависимости установлены')"
```

### Шаг 5: Первый запуск

```cmd
python voice_to_text_windows.py
```

## 💻 Использование

### Интерактивный режим (по умолчанию)
```cmd
python voice_to_text_windows.py
```

**Команды:**
- Нажмите `Enter` - начать запись
- Введите `'история'` - показать историю
- Введите `'система'` - информация о системе
- Введите `'выход'` - выход

### Однократная запись
```cmd
python voice_to_text_windows.py --single
```
Записывает одну фразу и выходит.

### Просмотр истории
```cmd
python voice_to_text_windows.py --history
```

### Выбор языка
```cmd
python voice_to_text_windows.py --lang en-US      # Английский
python voice_to_text_windows.py --lang de-DE      # Немецкий
python voice_to_text_windows.py --lang fr-FR      # Французский
python voice_to_text_windows.py --lang es-ES      # Испанский
python voice_to_text_windows.py --lang ja-JP      # Японский
```

### Очистка истории
```cmd
python voice_to_text_windows.py --clear-history
```

## 🌍 Поддерживаемые языки

- 🇷🇺 Русский (ru-RU)
- 🇺🇸 Английский (en-US)
- 🇬🇧 Британский английский (en-GB)
- 🇩🇪 Немецкий (de-DE)
- 🇫🇷 Французский (fr-FR)
- 🇪🇸 Испанский (es-ES)
- 🇮🇹 Итальянский (it-IT)
- 🇯🇵 Японский (ja-JP)
- 🇪🇸 Испанский (Мексика) (es-MX)
- И многие другие...

## 📁 Расположение данных

История и конфигурация сохраняются в:
```
C:\Users\[YourUsername]\AppData\Roaming\VoiceToText\history.json
```

Это соответствует Windows стандартам для пользовательских данных приложений.

## 🆘 Решение проблем

### "Python не является внутренней или внешней командой"

**Решение:**
1. Переустановите Python
2. **Отметьте галочку "Add Python to PATH"** при установке
3. Перезагрузите компьютер
4. Попробуйте снова

### "ModuleNotFoundError: No module named 'speech_recognition'"

```cmd
# Переустановите зависимости
pip install --upgrade SpeechRecognition pyperclip
```

### "Ошибка микрофона"

1. Проверьте что микрофон подключен
2. Откройте Параметры → Конфиденциальность и безопасность → Микрофон
3. Убедитесь что доступ разрешен
4. Тестируйте микрофон через встроенные приложения Windows

### "Не удалось распознать речь"

- **Говорите четче** и громче
- **Уменьшите фоновой шум** (закройте окна, отключите музыку)
- **Приблизьтесь ближе** к микрофону
- **Проверьте интернет** - соединение должно быть стабильным
- **Повторите** - иногда требуется несколько попыток

### "Нет доступа в интернет" или ошибка API

Программа требует интернета для работы Google Speech Recognition API.

**Решения:**
- Проверьте подключение интернета
- Перезагрузите маршрутизатор
- Попробуйте позже (сервис может быть временно недоступен)

### Уведомления Windows не работают

Установите пакет для красивых уведомлений:
```cmd
pip install win10toast
```

Если не поможет, программа всё равно будет работать - уведомления просто не будут показаны.

## 🔧 Расширенные параметры

```cmd
# Показать информацию о системе
python voice_to_text_windows.py --system-info

# Не показывать уведомления
python voice_to_text_windows.py --no-tray

# Помощь и все параметры
python voice_to_text_windows.py --help
```

## 📱 Интеграция с другими приложениями

После того как текст скопирован в буфер обмена, вы можете:
- Вставить в любой текстовый редактор (`Ctrl+V`)
- Вставить в браузер для поиска
- Использовать в мессенджерах и социальных сетях

## 🎯 Советы и трюки

### Быстрый доступ

Создайте ярлык на рабочем столе:
1. Правой клавишей на рабочий стол → Создать → Ярлык
2. В поле адреса: `C:\Users\[YourUsername]\AppData\Local\Programs\Python\Python310\python.exe voice_to_text_windows.py`
3. Установите значок и название

### Автозапуск

Добавьте в автозагрузку:
1. Нажмите `Win+R`, введите `shell:startup`
2. Скопируйте туда ярлык программы

### Горячие клавиши

Используйте программы типа AutoHotkey для создания горячих клавиш:
```autohotkey
F12::Run python voice_to_text_windows.py --single
```

## 📝 Лицензия

MIT License

## 🔗 Полезные ссылки

- [Python.org](https://www.python.org)
- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text)
- [pyperclip](https://github.com/asweigart/pyperclip)

---

**Разработано для Windows** 🪟
