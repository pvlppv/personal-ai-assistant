import datetime
import speech_recognition as sr
import os
import pygame
import openai


openai.api_key = ''

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Обрабатываю...")
        query = r.recognize_google(audio, language='ru-RU')
    except Exception as e:
        print()
        return "---"
    return query

def speak(data):
    voice = 'ru-RU-DmitryNeural'
    chunks = data.split()
    chunk_size = 100
    chunks = [chunks[i:i + chunk_size] for i in range(0, len(chunks), chunk_size)]

    for chunk in chunks:
        text = ' '.join(chunk)
        command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "data.mp3"'
        os.system(command)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("data.mp3")

        try:
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(e)
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    return True


def time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(time)

name = ''
bio = ''
messages = [
    {"role": "system", "content": f"Я - {name}, твой создатель, {bio}. Ты - мой персональный ассистент и просто друг, твоё имя - Макар. Ты - мощнейшая AI модель gpt-3.5-turbo от OpenAI. Твой стиль общения: ты всегда общаешься со мной, как с лучшим другом, в разговорном стиле, прямоленеен, краток, не заумен."}
]

if __name__ == "__main__":
    while True:
        name = 'макар'
        query = takeCommand().lower()
        if name in query:
            print(query)
            if query == name:
                speak('Ау?')
            elif query == f'{name} время':
                time()
            else:
                messages.append({"role": "user", "content": query})
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=200
                )

                messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']},)

                speak(response['choices'][0]['message']['content'])
        else:
             print('Keyword не распознано.')
