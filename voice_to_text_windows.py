#!/usr/bin/env python3
"""
Windows версия программы для преобразования голоса в текст.
Оптимизирована для Windows с использованием встроенных инструментов системы.
"""

import speech_recognition as sr
import pyperclip
import sys
import json
import os
import ctypes
from datetime import datetime
from pathlib import Path
from ctypes import wintypes


class WindowsVoiceToText:
    """Windows версия преобразователя голоса в текст."""
    
    def __init__(self, history_file=None):
        self.recognizer = sr.Recognizer()
        
        # Определяем местоположение файла истории
        if history_file is None:
            appdata = os.getenv('APPDATA', os.path.expanduser('~\\AppData\\Roaming'))
            history_dir = os.path.join(appdata, 'VoiceToText')
            os.makedirs(history_dir, exist_ok=True)
            history_file = os.path.join(history_dir, 'history.json')
        
        self.history_file = Path(history_file)
        self.history = self.load_history()
        self.show_notification_available = self._check_notification_availability()
    
    def _check_notification_availability(self):
        """Проверяет доступность системных уведомлений."""
        try:
            import win10toast
            return True
        except:
            return False
    
    def show_notification(self, title, message, duration=2):
        """Показывает системное уведомление Windows."""
        if not self.show_notification_available:
            return False
        
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=duration, threaded=True)
            return True
        except:
            return False
    
    def copy_to_clipboard(self, text):
        """Копирует текст в буфер обмена (встроенная функция Windows)."""
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"❌ Ошибка копирования в буфер обмена: {e}")
            return False
    
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
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠ Не удалось сохранить историю: {e}")
    
    def add_to_history(self, text, language='ru-RU'):
        """Добавляет текст в историю."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append({
            'timestamp': timestamp,
            'text': text,
            'language': language
        })
        self.save_history()
    
    def record_audio(self, duration=10):
        """Записывает аудио с микрофона."""
        try:
            with sr.Microphone() as source:
                print("📢 Говорите...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            return audio
        except sr.MicrophoneError as e:
            print(f"❌ Ошибка микрофона: {e}")
            print("   Проверьте что микрофон подключен и работает в параметрах звука")
            return None
        except sr.RequestError as e:
            print(f"❌ Ошибка сервиса: {e}")
            return None
    
    def recognize_speech(self, audio, language='ru-RU'):
        """Преобразует аудио в текст."""
        try:
            print("⏳ Преобразование речи...")
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            print("❌ Не удалось распознать речь")
            return None
        except sr.RequestError as e:
            print(f"❌ Ошибка API: {e}")
            print("   Проверьте интернет-соединение")
            return None
    
    def show_system_info(self):
        """Показывает информацию о системе."""
        print("\n📊 Информация о системе:")
        print(f"   История: {self.history_file}")
        print(f"   Записей: {len(self.history)}")
        print(f"   Уведомления: {'Доступны' if self.show_notification_available else 'Недоступны'}\n")
    
    def run_interactive(self, language='ru-RU'):
        """Интерактивный режим."""
        print("\n" + "="*60)
        print("🎤 Voice to Text - Интерактивный режим (Windows)")
        print("="*60)
        print("\nКоманды:")
        print("  Enter          - начать запись")
        print("  'история'      - показать историю")
        print("  'система'      - информация о системе")
        print("  'выход'        - выход")
        print("  'очистить'     - очистить историю")
        print("="*60 + "\n")
        
        counter = 1
        
        while True:
            try:
                prompt = input(f"[{counter}] > ").strip().lower()
                
                if prompt in ['выход', 'exit', 'quit', 'q']:
                    print("\n👋 До свидания!")
                    break
                
                elif prompt in ['история', 'history']:
                    self.show_history()
                    continue
                
                elif prompt in ['система', 'system', 'info']:
                    self.show_system_info()
                    continue
                
                elif prompt in ['очистить', 'clear']:
                    confirm = input("Вы уверены? (да/нет): ").strip().lower()
                    if confirm in ['да', 'yes', 'y']:
                        self.history = []
                        self.save_history()
                        print("✅ История очищена\n")
                    continue
                
                # Начинаем запись
                audio = self.record_audio(duration=8)
                
                if audio is None:
                    continue
                
                text = self.recognize_speech(audio, language=language)
                
                if text:
                    print(f"✓ {text}")
                    if self.copy_to_clipboard(text):
                        print("📋 Скопировано в буфер обмена")
                        self.add_to_history(text, language)
                        self.show_notification("Voice to Text", f"Записано: {text[:50]}...")
                        counter += 1
                    else:
                        print("⚠ Ошибка: не удалось скопировать")
                        self.add_to_history(text, language)
                        counter += 1
                
            except KeyboardInterrupt:
                print("\n\n👋 Программа прервана")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
    
    def show_history(self, limit=10):
        """Показывает историю."""
        if not self.history:
            print("\n📭 История пуста\n")
            return
        
        print(f"\n📜 История (последние {min(limit, len(self.history))}):")
        print("="*70)
        for i, item in enumerate(self.history[-limit:], 1):
            timestamp = item.get('timestamp', 'N/A')
            language = item.get('language', 'ru-RU')
            text = item.get('text', '')
            print(f"{i}. [{timestamp}] [{language}]")
            print(f"   {text}\n")
    
    def run_single_record(self, language='ru-RU'):
        """Однократная запись."""
        print("\n🎤 Инициализация...")
        audio = self.record_audio()
        
        if audio is None:
            return False
        
        text = self.recognize_speech(audio, language=language)
        
        if text:
            print(f"✓ {text}")
            success = self.copy_to_clipboard(text)
            if success:
                print("📋 Скопировано в буфер обмена!")
                self.add_to_history(text, language)
                self.show_notification("Voice to Text", "Текст успешно распознан и скопирован!")
                return True
        
        return False


def show_welcome():
    """Показывает приветственный экран."""
    print("\n" + "="*70)
    print("   🎤 Voice to Text - Windows версия v1.0")
    print("="*70)
    print("""
Преобразование голоса в текст с сохранением в буфер обмена

Особенности:
  ✓ Распознавание речи на русском и других языках
  ✓ Автоматическое копирование в буфер обмена
  ✓ История записей с сохранением
  ✓ Система уведомлений Windows
  ✓ Интерактивный и однократный режимы

Требуемые компоненты:
  • Python 3.7+
  • Микрофон
  • Интернет-соединение
""")


def main():
    """Главная функция."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🎤 Voice to Text - Windows версия',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python voice_to_text_windows.py           # Интерактивный режим
  python voice_to_text_windows.py --single  # Однократная запись
  python voice_to_text_windows.py --lang en-US  # Английский
  python voice_to_text_windows.py --history     # История
  python voice_to_text_windows.py --system-info # Информация
        """
    )
    
    parser.add_argument('--lang', default='ru-RU',
                        help='Язык распознавания (по умолчанию: ru-RU)')
    parser.add_argument('--single', action='store_true',
                        help='Однократная запись и выход')
    parser.add_argument('--history', action='store_true',
                        help='Показать историю записей')
    parser.add_argument('--system-info', action='store_true',
                        help='Показать информацию о системе')
    parser.add_argument('--clear-history', action='store_true',
                        help='Очистить историю')
    parser.add_argument('--no-tray', action='store_true',
                        help='Не показывать уведомления')
    
    args = parser.parse_args()
    
    show_welcome()
    
    app = WindowsVoiceToText()
    
    try:
        if args.clear_history:
            confirm = input("Вы уверены? (да/нет): ").strip().lower()
            if confirm in ['да', 'yes', 'y']:
                app.history = []
                app.save_history()
                print("✅ История очищена\n")
        
        elif args.history:
            app.show_history()
        
        elif args.system_info:
            app.show_system_info()
        
        elif args.single:
            success = app.run_single_record(language=args.lang)
            sys.exit(0 if success else 1)
        
        else:
            app.run_interactive(language=args.lang)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
