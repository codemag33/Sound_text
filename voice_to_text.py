#!/usr/bin/env python3
"""
Программа для преобразования голоса в текст и сохранения в буфер обмена.
"""

import speech_recognition as sr
import pyperclip
import sys


def record_and_convert():
    """
    Записывает голос с микрофона, преобразует в текст и сохраняет в буфер обмена.
    """
    # Инициализируем распознаватель
    recognizer = sr.Recognizer()
    
    print("🎤 Инициализация микрофона...")
    
    try:
        with sr.Microphone() as source:
            print("📢 Говорите... (ожидаю 5 секунд)")
            
            # Настройка порога шума
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Записываем аудио (максимум 5 секунд или пока не будет тишины)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    
    except sr.UnknownValueError:
        print("❌ Ошибка: не удалось распознать речь. Попробуйте еще раз.")
        return False
    except sr.RequestError as e:
        print(f"❌ Ошибка сервиса: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка микрофона: {e}")
        return False
    
    print("⏳ Преобразование речи в текст...")
    
    try:
        # Используем Google Speech Recognition
        text = recognizer.recognize_google(audio, language='ru-RU')
        
        print(f"✓ Распознанный текст: {text}")
        
        # Сохраняем в буфер обмена
        pyperclip.copy(text)
        print("📋 Текст скопирован в буфер обмена!")
        
        return True
        
    except sr.UnknownValueError:
        print("❌ Ошибка: не удалось распознать речь. Говорите четче.")
        return False
    except sr.RequestError as e:
        print(f"❌ Ошибка API: {e}")
        return False


def main():
    """Главная функция."""
    print("=" * 50)
    print("  Преобразование голоса в текст")
    print("=" * 50)
    
    try:
        success = record_and_convert()
        
        if not success:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠ Программа прервана пользователем")
        sys.exit(0)


if __name__ == "__main__":
    main()
