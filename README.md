# 🎤 Voice to Text - Преобразование голоса в текст

Полнофункциональное приложение на Python для преобразования речи в текст с автоматическим сохранением в буфер обмена.

## 🎯 Возможности

- ✅ **Распознавание речи** на русском и других языках
- ✅ **Автоматическое копирование** в буфер обмена
- ✅ **История записей** с временными метками
- ✅ **GNU/Linux оптимизация** (поддержка xclip, xsel, wl-copy)
- ✅ **Интерактивный режим**
- ✅ **Непрерывная запись** для многократного использования
- ✅ **Обработка ошибок** с информативными сообщениями

## 📦 Версии

### 1. **voice_to_text.py** - Базовая версия
Простая однократная запись и преобразование:
```bash
python voice_to_text.py
```

### 2. **voice_to_text_advanced.py** - Расширенная версия
С режимом непрерывной записи и историей:
```bash
python voice_to_text_advanced.py --continuous
python voice_to_text_advanced.py --history
```

### 3. **voice_to_text_gnu.py** - GNU/Linux версия
Оптимизирована для Linux с лучшей интеграцией системы:
```bash
python voice_to_text_gnu.py              # Интерактивный режим
python voice_to_text_gnu.py --lang en-US  # Другой язык
python voice_to_text_gnu.py --history     # История
python voice_to_text_gnu.py --system-info # Информация о системе
```

### 4. **voice_to_text_windows.py** - Windows версия ⭐
Полностью оптимизирована для Windows с системными уведомлениями:
```cmd
python voice_to_text_windows.py           # Интерактивный режим
python voice_to_text_windows.py --single  # Однократная запись
python voice_to_text_windows.py --lang en-US  # Другой язык
python voice_to_text_windows.py --history     # История
python voice_to_text_windows.py --system-info # Информация
```

## 🚀 Установка

### Требования
- Python 3.7+
- Микрофон
- Интернет-соединение (для Google Speech Recognition API)

### 🪟 На Windows:
```cmd
# 1. Установить Python (www.python.org, отметить "Add to PATH")
# 2. Клонировать или скачать проект
git clone https://github.com/codemag33/Sound_text.git
cd Sound_text

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить
python voice_to_text_windows.py
```

👉 **[Подробная инструкция для Windows](INSTALL_WINDOWS.md)**

### 🐧 На Ubuntu/Debian:
```bash
# 1. Установить системные зависимости
sudo apt-get update
sudo apt-get install -y python3-pip portaudio19-dev

# Для буфера обмена (выберите один):
sudo apt-get install -y xclip      # Для X11
# или
sudo apt-get install -y xsel       # Альтернатива

# 2. Установить Python зависимости
pip install -r requirements.txt

# 3. Запустить GNU версию
python voice_to_text_gnu.py
```

### 🔴 На Fedora/RHEL:
```bash
sudo dnf install python3-pip portaudio-devel xclip
pip install -r requirements.txt
python voice_to_text_gnu.py
```

### 🟦 На Arch:
```bash
sudo pacman -S python-pip portaudio xclip
pip install -r requirements.txt
python voice_to_text_gnu.py
```

## 💻 Использование

### Быстрый старт:
```bash
# GNU/Linux версия (рекомендуется)
python voice_to_text_gnu.py

# Говорите и результат автоматически скопируется в буфер обмена
```

### Выбор языка:
```bash
python voice_to_text_gnu.py --lang en-US      # Английский
python voice_to_text_gnu.py --lang es-ES      # Испанский
python voice_to_text_gnu.py --lang fr-FR      # Французский
python voice_to_text_gnu.py --lang de-DE      # Немецкий
```

### Просмотр истории:
```bash
python voice_to_text_gnu.py --history
python voice_to_text_advanced.py --history
```

### Интерактивные команды:
- Нажмите **Enter** - начать запись
- Введите **'история'** - показать историю
- Введите **'система'** - информация о системе (GNU версия)
- Введите **'выход'** - выход из программы

## 🔧 Технические детали

### Поддерживаемые буферы обмена:

**Windows:**
- `pyperclip` - встроенная поддержка, работает со всеми версиями Windows

**Linux:**
- `xclip` - стандартная утилита X11
- `xsel` - альтернативная утилита X11
- `wl-copy` - для Wayland

**macOS:**
- `pbcopy` - встроенная утилита

Программа автоматически определяет доступный инструмент.

### Расположение данных:

**Windows:**
- История: `C:\Users\[YourUsername]\AppData\Roaming\VoiceToText\history.json`
- Следует Windows стандартам для пользовательских данных

**Linux (GNU версия):**
- История: `~/.local/share/voice_to_text/history.json`
- Следует XDG Base Directory Specification

## 📝 Примеры команд

### Windows:
```cmd
# Базовая однократная запись
python voice_to_text_windows.py --single

# Интерактивный режим
python voice_to_text_windows.py

# Другой язык
python voice_to_text_windows.py --lang en-US

# История записей
python voice_to_text_windows.py --history

# Очистка истории
python voice_to_text_windows.py --clear-history
```

### Linux/macOS:
```bash
# GNU версия (Linux)
python voice_to_text_gnu.py

# Расширенная версия
python voice_to_text_advanced.py --continuous

# Просмотр истории
python voice_to_text_gnu.py --history

# Информация о системе
python voice_to_text_gnu.py --system-info

# Выбор языка
python voice_to_text_gnu.py --lang en-US
```

## 🆘 Решение проблем

### "Ошибка: микрофон не найден"
```bash
# Проверьте микрофон
arecord -L
pactl list sources
```

### "Буфер обмена недоступен"
```bash
# Установите xclip
sudo apt-get install xclip

# Или для Wayland:
sudo apt-get install wl-clipboard
```

### "Не удалось распознать речь"
- Говорите четче и громче
- Уменьшите фоновой шум
- Приблизьтесь ближе к микрофону
- Проверьте интернет-соединение

## 📄 Лицензия

MIT License - смотрите LICENSE файл для подробностей

## 🔗 Ссылки

- [SpeechRecognition документация](https://github.com/Uberi/speech_recognition)
- [Google Speech Recognition](https://cloud.google.com/speech-to-text)
- [XDG Base Directory](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

## 🎙️ Поддерживаемые языки

Программа поддерживает все языки Google Speech Recognition API:
- 🇷🇺 Русский (ru-RU)
- 🇺🇸 Английский (en-US)
- 🇩🇪 Немецкий (de-DE)
- 🇫🇷 Французский (fr-FR)
- 🇪🇸 Испанский (es-ES)
- И многие другие...

---

**Полная кроссплатформенная поддержка** 🪟 🐧 🍎
