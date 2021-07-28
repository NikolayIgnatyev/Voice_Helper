from plyer import notification
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import speech_recognition
import pyttsx3
import wave                     # настоятельно рекомендую запускать не через pycharm и ideone.com 
import time                     # я все тестировал простым запуском через cmd
import datetime
import sys, os


options = {
    "alias": ['том'],
    "cmd": 
    {
    'time':
        ["время", "времени"],
    'browser':
        ['браузер']
    }
}


class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи
    """
    name = ""
    sex = ""
    speech_language = ""            
    recognition_language = ""

def setup_assistant_voice():
    """
    Установка зависимости по умолчанию(индекс может изменяться
    в зависимости от настроек операциионой системы)
    """
    voices = ttsEngine.getProperty("voices")
    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            # microsoft zira dekstop
            ttsEngine.setProperty("voice", voices[1].id)
        else:
            # microsoft david dekstop
            ttsEngine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru- RU"
        #microsoft irina dekstop
        ttsEngine.setProperty("voice", voices[0].id)

def speak_voice(text_to_speech):
    """
    Проигрование речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech текст, который нужно преобразовать в речь
    """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def record_and_recognize_audio():
    while True:
        """
        Запись и распознавание аудио
        """
        with microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            recognizer.adjust_for_ambient_noise(microphone, duration=1)

            try:
                print("Listening...")
                audio = recognizer.listen(microphone, 5, 5)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                return

            # использование online-распознавания через Google 
            # (высокое качество распознавания)
            try:
                print("Started recognition...")
                recognized_data = recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                pass

            return recognized_data

def intersection(lst1, lst2):

    lst3 = [value for value in lst1 if value in lst2]

    return lst3


if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # синтез речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосовго помощника
    assistant = VoiceAssistant()
    assistant.name = "Tom"
    assistant.sex = "male"
    assistant.speech_language = "ru"

    # установка голоса по умолчанию
    setup_assistant_voice()

    speak_voice("Привет, я твой голосовой помощник, Том")

    while True:

        # старт записи речи с последующим выводом распознанной речи
        voice_input = record_and_recognize_audio()
        print(voice_input)
        command = voice_input

        # отброс тишины
        if not voice_input:
            pass
        else:
            voice_input = voice_input.split(" ")
            command = voice_input
            print(command)

            name = options['alias']
            
            #сравнение с помощью fuzzywuzzy
            while True:
                name = ''.join(name)
                fuzz_num = process.extractOne(name, command)
                fuzz_num = fuzz_num[1]
                break
            names = [name]
            names.append('exception') # костыли 
            print(name)

            score = False
            if fuzz_num >= 65:
                for i in name:
                    count = len(name)
                    if count > 1:       # один большой КОСТЫЛЬ который мне лень исправлять XD
                        score = True
                    elif 'exception' in name:
                        score = False
            else:
                pass

            print(score)

            # выполнение команд если к нему обращаются
            while score:
                print('hi')
                
                # срез лишней информации
                list_cmd = options['cmd']['time']
                cmd = intersection(list_cmd, command)


                    # команды
                for list_cmd in cmd:
                    # сказать текущее время и показать
                    ttsEngine = pyttsx3.init()
                    now = datetime.datetime.now()
                    notification.notify(
                    title='Время на компьютере',
                    message="Сейчас " + str(now.hour) + ":" + str(now.minute),
                    app_name='',
                    )
                    speak_voice("Сейчас " + str(now.hour) + ":" + str(now.minute))
                    break
                break
        # последующие удаление записанного в микрофон аудиo
        audio_file = open("microphone-results.wav", "w+")
        audio_file.close()
        os.remove("microphone-results.wav")



        

