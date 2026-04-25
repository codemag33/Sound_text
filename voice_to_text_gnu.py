#!/usr/bin/env python3
"""
GNU/Linux версия программы для преобразования голоса в текст.
Оптимизирована для работы на Linux с поддержкой X11, Wayland и буфера обмена.
"""

import speech_recognition as sr
import subprocess
import sys
import json
import os
from datetime import datetime
from pathlib import Path


class GNUVoiceToText:
    """GNU/Linux версия преобразователя голоса в текст."""
    
    def __init__(self, history_file=None):
        self.recognizer = sr.Recognizer()
        
        # Определяем местоположение файла истории
        if history_file is None:
            xdg_data = os.getenv('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
            os.makedirs(f"{xdg_data}/voice_to_text", exist_ok=True)
            history_file = f"{xdg_data}/voice_to_text/history.json"
        
        self.history_file = Path(history_file)
        self.history = self.load_history()
        self.clipboard_tool = self._detect_clipboard_tool()
    
    def _detect_clipboard_tool(self):
        """Определяет какой инструмент использовать для буфера обмена."""
        tools = {
            'xclip': ['xclip', '-selection', 'clipboard'],
            'xsel': ['xsel', '--clipboard', '--input'],
            'wl-copy': ['wl-copy'],
            'pbcopy': ['pbcopy']  # macOS
        }
        
        for tool_name, cmd in tools.items():
            try:
                subprocess.run(['which', cmd[0]], capture_output=True, check=True)
                return cmd
            except subprocess.CalledProcessError:
                continue
        
        print("⚠ Предупреждение: инструмент буфера обмена не найден")
        return None
    
    def copy_to_clipboard(self, text):
        """Копирует текст в буфер обмена используя подходящий инструмент."""
        if self.clipboard_tool is None:
            print("❌ Ошибка: буфер обмена недоступен")
            return False
        
        try:
            process = subprocess.Popen(
                self.clipboard_tool,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            process.communicate(input=text.encode('utf-8'))
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
            print("   Проверьте что микрофон подключен и работает")
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
            return None
    
    def show_system_info(self):
        """Shows system information."""
        print("\n📊 Информация о системе:")
        print(f"   Буфер обмена: {self.clipboard_tool[0] if self.clipboard_tool else 'не найден'}")
        print(f"   История: {self.history_file}")
        print(f"   Записей: {len(self.history)}\n")
    
    def run_interactive(self, language='ru-RU'):
        """Интерактивный режим."""
        print("\n🎤 Интерактивный режим")
        print("Команды:")
        print("  Enter - начать запись")
        print("  'история' (history) - показать историю")
        print("  'система' (system) - информация о системе")
        print("  'выход' (exit) - выход")
        print("=" * 50 + "\n")
        
        counter = 1
        
        while True:
            try:
                prompt = input(f"[{counter}] > ").strip().lower()
                
                if prompt in ['выход', 'exit', 'quit', 'q']:
                    print("👋 До свидания!")
                    break
                
                elif prompt in ['история', 'history']:
                    self.show_history()
                    continue
                
                elif prompt in ['система', 'system', 'info']:
                    self.show_system_info()
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
            print("📭 История пуста\n")
            return
        
        print(f"\n📜 История (последние {min(limit, len(self.history))}):")
        print("=" * 60)
        for item in self.history[-limit:]:
            timestamp = item.get('timestamp', 'N/A')
            language = item.get('language', 'ru-RU')
            text = item.get('text', '')
            print(f"⏰ {timestamp} [{language}]")
            print(f"📝 {text}\n")


def main():
    """Главная функция."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🎤 GNU/Linux версия - Преобразование голоса в текст',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python voice_to_text_gnu.py              # Интерактивный режим
  python voice_to_text_gnu.py --lang en-US  # Английский язык
  python voice_to_text_gnu.py --history     # Показать историю
  python voice_to_text_gnu.py --system-info # Информация о системе
        """
    )
    
    parser.add_argument('--lang', default='ru-RU',
                        help='Язык распознавания (по умолчанию: ru-RU)')
    parser.add_argument('--history', action='store_true',
                        help='Показать историю записей')
    parser.add_argument('--system-info', action='store_true',
                        help='Показать информацию о системе')
    parser.add_argument('--clear-history', action='store_true',
                        help='Очистить историю')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("  🎤 GNU/Linux версия - Преобразование голоса в текст")
    print("=" * 60)
    
    app = GNUVoiceToText()
    
    try:
        if args.clear_history:
            app.history = []
            app.save_history()
            print("✅ История очищена\n")
        
        elif args.history:
            app.show_history()
        
        elif args.system_info:
            app.show_system_info()
        
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
