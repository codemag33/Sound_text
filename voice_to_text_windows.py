#!/usr/bin/env python3
"""
Windows версия программы для преобразования голоса в текст.
"""

import speech_recognition as sr
import pyperclip
import sys
import json
import os
from datetime import datetime
from pathlib import Path


class WindowsVoiceToText:
    def __init__(self, history_file=None):
        self.recognizer = sr.Recognizer()

        if history_file is None:
            appdata = os.getenv('APPDATA', os.path.expanduser('~\\AppData\\Roaming'))
            history_dir = os.path.join(appdata, 'VoiceToText')
            os.makedirs(history_dir, exist_ok=True)
            history_file = os.path.join(history_dir, 'history.json')

        self.history_file = Path(history_file)
        self.history = self.load_history()
        self.show_notification_available = self._check_notification_availability()

    def _check_notification_availability(self):
        try:
            import win10toast
            return True
        except ImportError:
            return False

    def show_notification(self, title, message, duration=2):
        if not self.show_notification_available:
            return False
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=duration, threaded=True)
            return True
        except Exception:
            return False

    def copy_to_clipboard(self, text):
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"❌ Ошибка буфера обмена: {e}")
            return False

    def load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_history(self):
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠ Ошибка сохранения истории: {e}")

    def add_to_history(self, text, language='ru-RU'):
        self.history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'text': text,
            'language': language
        })
        self.save_history()

    def record_audio(self, duration=10):
        try:
            with sr.Microphone() as source:
                print("📢 Говорите...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=duration,
                    phrase_time_limit=duration
                )
            return audio

        except OSError as e:
            print(f"❌ Ошибка микрофона: {e}")
            return None

        except sr.WaitTimeoutError:
            print("⏱ Вы не начали говорить")
            return None

        except Exception as e:
            print(f"❌ Ошибка записи: {e}")
            return None

    def recognize_speech(self, audio, language='ru-RU'):
        try:
            print("⏳ Распознавание...")
            return self.recognizer.recognize_google(audio, language=language)

        except sr.UnknownValueError:
            print("❌ Речь не распознана")
            return None

        except sr.RequestError as e:
            print(f"❌ Ошибка API: {e}")
            return None

    def show_history(self, limit=10):
        if not self.history:
            print("\n📭 История пуста\n")
            return

        print("\n📜 История:")
        print("=" * 60)
        for i, item in enumerate(self.history[-limit:], 1):
            print(f"{i}. [{item['timestamp']}]")
            print(f"   {item['text']}\n")

    def run_interactive(self, language='ru-RU'):
        print("\n🎤 Voice to Text (Windows)\n")

        counter = 1

        while True:
            try:
                cmd = input(f"[{counter}] > ").strip().lower()

                if cmd in ['выход', 'exit']:
                    break

                if cmd == 'история':
                    self.show_history()
                    continue

                audio = self.record_audio(8)
                if not audio:
                    continue

                text = self.recognize_speech(audio, language)

                if text:
                    print(f"✓ {text}")
                    self.copy_to_clipboard(text)
                    self.add_to_history(text, language)
                    self.show_notification("Voice to Text", text[:50])
                    counter += 1

            except KeyboardInterrupt:
                print("\n👋 Выход")
                break

            except Exception as e:
                print(f"❌ Ошибка: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='ru-RU')
    parser.add_argument('--single', action='store_true')

    args = parser.parse_args()

    app = WindowsVoiceToText()

    if args.single:
        audio = app.record_audio()
        if audio:
            text = app.recognize_speech(audio, args.lang)
            if text:
                print(text)
                app.copy_to_clipboard(text)
    else:
        app.run_interactive(args.lang)


if __name__ == "__main__":
    main()
