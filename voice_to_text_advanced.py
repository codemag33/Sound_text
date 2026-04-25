#!/usr/bin/env python3
"""
Расширенная версия программы для преобразования голоса в текст.
Поддерживает режим непрерывной записи, сохранение истории и другие функции.
"""

import speech_recognition as sr
import pyperclip
import sys
import json
from datetime import datetime
from pathlib import Path


class VoiceToTextApp:
    """Класс для управления преобразованием голоса в текст."""
    
    def __init__(self, history_file='voice_history.json'):
        self.recognizer = sr.Recognizer()
        self.history_file = Path(history_file)
        self.history = self.load_history()
    
    def load_history(self):
        """Загружает историю из файла."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Сохраняет историю в файл."""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_to_history(self, text):
        """Добавляет текст в историю."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append({
            'timestamp': timestamp,
            'text': text
        })
        self.save_history()
    
    def record_audio(self, duration=10):
        """Записывает аудио с микрофона."""
        try:
            with sr.Microphone() as source:
                print("📢 Говорите... (ожидаю запись)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            return audio
        except sr.MicrophoneError as e:
            print(f"❌ Ошибка микрофона: {e}")
            return None
        except sr.RequestError as e:
            print(f"❌ Ошибка сервиса: {e}")
            return None
    
    def recognize_speech(self, audio, language='ru-RU'):
        """Преобразует аудио в текст."""
        try:
            print("⏳ Преобразование речи в текст...")
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            print("❌ Не удалось распознать речь")
            return None
        except sr.RequestError as e:
            print(f"❌ Ошибка API: {e}")
            return None
    
    def copy_to_clipboard(self, text):
        """Копирует текст в буфер обмена."""
        pyperclip.copy(text)
        print("📋 Текст скопирован в буфер обмена!")
    
    def show_history(self, limit=10):
        """Показывает историю последних записей."""
        if not self.history:
            print("📭 История пуста")
            return
        
        print("\n📜 История последних записей:")
        print("=" * 50)
        for item in self.history[-limit:]:
            print(f"⏰ {item['timestamp']}")
            print(f"📝 {item['text']}\n")
    
    def run_single(self):
        """Запускает однократное преобразование."""
        print("🎤 Инициализация микрофона...")
        audio = self.record_audio()
        
        if audio is None:
            return False
        
        text = self.recognize_speech(audio)
        
        if text:
            print(f"✓ Распознано: {text}")
            self.copy_to_clipboard(text)
            self.add_to_history(text)
            return True
        
        return False
    
    def run_continuous(self):
        """Запускает режим непрерывной записи."""
        print("\n🔄 Режим непрерывной записи")
        print("Введите 'выход' чтобы выйти, 'история' чтобы показать историю")
        print("=" * 50 + "\n")
        
        counter = 1
        
        while True:
            try:
                print(f"\n📍 Запись #{counter}")
                user_input = input("Нажмите Enter для записи (или введите команду): ").strip().lower()
                
                if user_input == 'выход':
                    print("👋 До свидания!")
                    break
                elif user_input == 'история':
                    self.show_history()
                    continue
                
                print("🎤 Слушаю...")
                audio = self.record_audio(duration=8)
                
                if audio is None:
                    continue
                
                text = self.recognize_speech(audio)
                
                if text:
                    print(f"✓ {text}")
                    self.copy_to_clipboard(text)
                    self.add_to_history(text)
                    counter += 1
                    print("✅ Скопировано в буфер обмена")
                
            except KeyboardInterrupt:
                print("\n\n👋 Программа прервана")
                break


def main():
    """Главная функция."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Преобразование голоса в текст',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python voice_to_text_advanced.py              # Однократная запись
  python voice_to_text_advanced.py --continuous # Режим непрерывной записи
  python voice_to_text_advanced.py --history    # Показать историю
        """
    )
    
    parser.add_argument('--continuous', '-c', action='store_true',
                        help='Режим непрерывной записи')
    parser.add_argument('--history', action='store_true',
                        help='Показать историю записей')
    parser.add_argument('--lang', default='ru-RU',
                        help='Язык распознавания (по умолчанию: ru-RU)')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 50)
    print("  🎤 Преобразование голоса в текст v2.0")
    print("=" * 50)
    
    app = VoiceToTextApp()
    
    try:
        if args.history:
            app.show_history()
        elif args.continuous:
            app.run_continuous()
        else:
            app.run_single()
            
    except KeyboardInterrupt:
        print("\n\n⚠ Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
