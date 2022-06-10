import os
import sys
import torch
import telebot
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification

if len(sys.argv)>1:
    token = sys.argv[1]
else:
    token = os.getenv('TG_TOKEN')
    if not token: 
        print('bot token needed...')
        quit()

if len(sys.argv)>2:
    my_chat_id = int(sys.argv[2])
else: 
    my_chat_id = int(os.getenv('MY_CHAT'))

# открываем файл в режиме чтения
with open('ans.json', 'r', encoding='UTF-8') as fr:
    # читаем из файла
    ans = json.load(fr)

model_name = "Nehc/FakeMobile"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
# turn on cuda if GPU is available
use_cuda = torch.cuda.is_available()

if use_cuda:
    model.cuda()

bot = telebot.TeleBot(token)

print(f'Main cicle whith cuda is {use_cuda} start...')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Бот обучен на данных фейкового оператора мобильной связи ООО «Говори громко» (http://dumbot.ru/Home/MobileOperatorRate).  Можно задавать вопросы о стоимости услуг на тарифах.")

@bot.message_handler(content_types='text')
def message_reply(message):
    
    text = f"[CLS] {message.text.lower()} [SEP]"
    inpt = tokenizer.encode(text, return_tensors="pt")    

    # Run eval step for caption
    with torch.no_grad():
        if use_cuda:
            inpt = inpt.cuda()
        out = model(inpt)

    it = torch.argmax(out[0], dim=1).item()
    s = ans[it]
    m = torch.nn.Softmax(dim=1)
    prc = torch.max(m(out[0]))*100
    bot.reply_to(message, f'{s} ({prc:.2f}%)')

#bot.polling(interval=3, timeout=45)
bot.infinity_polling()
