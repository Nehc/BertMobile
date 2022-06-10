# BertMobile

Игрушечный пример для решения задачи [диалогового  бота](http://dumbot.ru/Home/MobileOperatorRate) с использованием архитектуры BERT. 

Используются синтетически сгенерированные реплики на основе данных о тарифах оператора ([data.json](https://github.com/Nehc/BertMobile/blob/main/data.json)). намного лучше было бы иметь реальный датасет вопросов людей! 

Так же используется проверочный [датаcет](https://github.com/Nehc/BertMobile/blob/main/eval.json) всего из 10 вопросов, чего явно мало... 

Процесс обучения расписан [в этом Colab](https://colab.research.google.com/drive/1u1VM696xXkR4DSxlDN1rT3i4IROgFn9i?usp=sharing). 

так же прилагается файл [telebot.py](https://github.com/Nehc/BertMobile/blob/main/telebot.py) для запуска бота с обученной моделью. Формат запуска:
    
    python telebot.py 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    
не забудьте подставить свой токен бота.

Так же можно развернуть бота как docker-контейнер посредством следующих команд:
    
    git clone https://github.com/Nehc/BertMobile.git
    cd BertMobile
    docker build --tag="<your_name>/telebot" .
    docker run --user 1000:100 -tid --gpus all --name telebot --mount \
    type=bind,src=/home/<your_name>/BertMobile,target=/home/telebot \
    -e TG_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 <your_name>/telebot

с поправкой на ваши локальные пути, имя пользователя и тп...
