# 🎤 Преобразование голоса в текст

Программа на Python для преобразования голоса в текст с сохранением в буфер обмена.

## 📋 Требования

- Python 3.7+
- Микрофон
- Интернет-соединение (для использования Google Speech Recognition API)

## 🚀 Установка

### 1. Установите зависимости системы

**На Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-pip portaudio19-dev libssl-dev libffi-dev
```

**На macOS:**
```bash
brew install portaudio
```

### 2. Установите Python зависимости

```bash
pip install -r requirements.txt
```

Или установите вручную:
```bash
pip install SpeechRecognition==3.10.0
pip install pyperclip==1.8.2
```

## 💻 Использование

Запустите программу:
```bash
python voice_to_text.py
```

Или с разрешением на выполнение:
```bash
chmod +x voice_to_text.py
./voice_to_text.py
```

### Процесс работы:
1. Программа инициализирует микрофон
2. Вы говорите (примерно 5-10 секунд)
3. Программа преобразует речь в текст
4. Текст автоматически копируется в буфер обмена ✓

## 🔧 Расширенная версия с режимами

Для более функциональной версии создайте файл `voice_to_text_advanced.py`:

```bash
python voice_to_text_advanced.py --continuous
```

Это позволит записывать несколько фраз подряд.

## ⚙️ Язык распознавания

По умолчанию используется русский язык (`ru-RU`).

Для других языков отредактируйте строку в `voice_to_text.py`:
```python
text = recognizer.recognize_google(audio, language='en-US')  # Английский
text = recognizer.recognize_google(audio, language='es-ES')  # Испанский
text = recognizer.recognize_google(audio, language='fr-FR')  # Французский
```

## 🆘 Решение проблем

### "Ошибка: микрофон не найден"
- Проверьте, включен ли микрофон
- Проверьте разрешения: `pac allow microphone`

### "Ошибка API"
- Проверьте интернет-соединение
- Google Speech Recognition может быть недоступен в вашей стране

### "Не удалось распознать речь"
- Говорите четче и громче
- Уменьшите фоновой шум
- Приблизьтесь ближе к микрофону

## 📝 Лицензия

MIT

## 🔗 Ссылки

- [SpeechRecognition документация](https://github.com/Uberi/speech_recognition)
- [pyperclip](https://github.com/asweigart/pyperclip)
