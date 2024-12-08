import os
import openai
from dotenv import load_dotenv
import streamlit as st

# Загрузка переменных окружения
load_dotenv()

# Установка ключа OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Инициализация истории сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help?"}]

def get_assistant_response(messages):
    """
    Отправляет запрос в OpenAI и получает ответ от ассистента.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    return response["choices"][0]["message"]["content"]

# Заголовок приложения
st.title("Chatbot with OpenAI")

# Отображение истории сообщений
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f"**Assistant**: {message['content']}")
    else:
        st.markdown(f"**You**: {message['content']}")

# Поле ввода сообщения от пользователя
user_input = st.text_input("Your message:", key="user_input")

# Обработка ввода
if st.button("Send"):
    if user_input:
        # Добавление сообщения пользователя в историю
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Получение ответа от ассистента
        assistant_response = get_assistant_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        # Обновление интерфейса
        st.rerun()  # Обновляет интерфейс, чтобы отобразить новые сообщения
