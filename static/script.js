const getMessagesUrl = 'https://functions.yandexcloud.net/d4e0h2dda9g8beeu01cq'

fetch(getMessagesUrl)
    .then(response => response.json())
    .then(data => {
        const messages = data;
        document.body.innerHTML += "<h3 style=\"text-align: center;\"><br><br>Однако мы передаем сообщения от Вани:</h3>";
        messages.forEach(message => {
            document.body.innerHTML += "<div style=\"text-align: center;\"><br>" + message.text + "</div>";
        });
    })
    .catch(error => console.error('Ошибка:', error));