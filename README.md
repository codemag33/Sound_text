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

### 3. **voice_to_text_gnu.py** - GNU/Linux версия ⭐
Оптимизирована для Linux с лучшей интеграцией системы:
```bash
python voice_to_text_gnu.py              # Интерактивный режим
python voice_to_text_gnu.py --lang en-US  # Другой язык
python voice_to_text_gnu.py --history     # История
python voice_to_text_gnu.py --system-info # Информация о системе
```

## 🚀 Установка

### Требования
- Python 3.7+
- Микрофон
- Интернет-соединение (для Google Speech Recognition API)

### На Ubuntu/Debian:
```bash
# Установить системные зависимости
sudo apt-get update
sudo apt-get install -y python3-pip portaudio19-dev

# Для буфера обмена (выберите один):
sudo apt-get install -y xclip      # Для X11
# или
sudo apt-get install -y xsel       # Альтернатива

# Установить Python зависимости
pip install -r requirements.txt
```

### На Fedora/RHEL:
```bash
sudo dnf install python3-pip portaudio-devel xclip
pip install -r requirements.txt
```

### На Arch:
```bash
sudo pacman -S python-pip portaudio xclip
pip install -r requirements.txt
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
- `xclip` - стандартная утилита X11
- `xsel` - альтернативная утилита X11
- `wl-copy` - для Wayland
- `pbcopy` - для macOS

Программа автоматически определяет доступный инструмент.

### Расположение данных (GNU версия):
- История: `~/.local/share/voice_to_text/history.json`
- Следует XDG Base Directory Specification

## 📝 Примеры команд

```bash
# Базовая однократная запись
./voice_to_text.py

# Непрерывная запись с историей
./voice_to_text_advanced.py --continuous

# GNU/Linux с русским языком
./voice_to_text_gnu.py

# Просмотр истории записей
./voice_to_text_gnu.py --history

# Очистка истории
./voice_to_text_gnu.py --clear-history

# Информация о системе
./voice_to_text_gnu.py --system-info
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

**Разработано для GNU/Linux систем** 🐧
