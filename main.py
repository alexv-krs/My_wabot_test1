# тестовый ватсап бот
import requests, os, json

class Wabot():
    # задаю константы
    headers = {
        'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'
    }
    params = {}
    files = {}
    payload = {}
    URL = 'https://dev.wapp.im/v3/'
    NEW_CHAT = 'chat/spare?crm=TEST&domain=test'

    # получаю id и токен, так же получаю qr код и статус о подключении
    def __init__(self):
        response = self.new_chat()
        self.id = response.json()['id']
        self.token = response.json()['token']
        self.chatId = response.json()['chat_id']
        self.get_qr_code()
        self.get_me()


    # генерирую url для работы с api
    def get_url(self, method):
        return f'{self.URL}instance{self.id}/{method}?token={self.token}'

    # полчуение нового чата
    def new_chat(self):
        url = f'{self.URL}{self.NEW_CHAT}'
        response = requests.get(url, headers=self.headers)
        print('Чат получен:', response.text)
        if 'id' and 'token' not in response.text:
            trying = 1
            while 'id' and 'token' not in response.text:
                trying +=1
                response = requests.get(url, headers=self.headers)
                print(f'Поиск чата. Попытка №{trying}')
        else:
            # загружаю данные в json
            with open(f'new_chat_id_{response.json()["id"]}.json', 'w') as f:
                json.dump(response.json(), f)
            f.close()
        return response
    # получаю qr код и сохряняю его в файл и запускаю, если он получен
    def get_qr_code(self):
        method = 'qr_code'
        url = self.get_url(method)
        response = requests.request("GET", url, headers=self.headers, data=self.payload)

        # записываю полученный qr в файл для аутентификации
        if 'img src' in response.text:
            f = open(f"qr_code_for_id_{self.id}.html", 'w')
            f.write(response.text)
            f.close()
            print(f'Файл "qr_code_for_id_{self.id}.html" записан')
            os.system(f"start qr_code_for_id_{self.id}.html")
            input('Нажмите Enter после того как отсканируете QR_CODE')

        else:
            print('qr_code не сохранен')
        print('Полученный Qr_code:', response.text)

    # делаю запрос на сервер для получения данных о пользователе
    def get_me(self):
        method = 'me'
        url = self.get_url(method)
        response = requests.get(url, headers=self.headers)
        print('Информация о телефоне WhatsApp:', response.text)
        return response

    # получение статуса
    def get_status(self):
        # делаю запрос на сервер для получения статуса
        method = 'status'
        url = self.get_url(method)
        response = requests.get(url, headers=self.headers)
        print('Статус аккаунта:', response.text)
        return response

    # отправляю сообщение
    def send_message(self, phone, message):
        # создаю сообщение
        payload = {
            'chatId': phone,
            'body': message
        }
        # делаю запрос на сервер для отправки сообщения
        method = 'sendMessage'
        url = self.get_url(method)
        response = requests.get(url, headers=self.headers, data=payload)
        print('Статус отправки сообщения:', response.text)

    # получение пользовательского ввода для отправик сообщений
    def get_input(self, message):
        response = input(message)
        return response

    # удяляю чат
    def removeChat(self):
        method = 'removeChat'
        url = self.get_url(method)
        payload = {
            "phone" : self.chatId
        }
        response = requests.request("GET", url, headers=self.headers, data=payload)
        print(response.text)

# запускаю бота
if __name__ == '__main__':
    wabot = Wabot()
    wabot.send_message(wabot.get_input('Введите номер: '), wabot.get_input('Введите сообщение: '))
    wabot.removeChat()
