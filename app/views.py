from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from googletrans import Translator
import telebot
from telebot import *
from .words import word_definitions
from .models import BotUsers
from django.views.generic import ListView

 

translator = Translator()

bot = telebot.TeleBot("2128941862:AAGCVD78bBtioyDpvmwF2XYWSHR-Iu5xobA")


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("Bot Url Page")
    elif request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)

def home(request):
	total_amount = len(BotUsers.objects.all())
	return render(request, 'home.html', context={'total_amount':total_amount,})


@bot.message_handler(commands=['start'])
def send_welcome(message):
	if len(BotUsers.objects.filter(user_id=message.from_user.id)) == 0:
		new_user = BotUsers.objects.create(
			user_id = message.from_user.id,
			username = message.from_user.username,
			first_name = message.from_user.first_name,
			last_name = message.from_user.last_name,
			)
		new_user.save()
	bot.reply_to(message, "Welcome to Easy Translate Bot\nSend me the word that you don't know and will provide you its definitions and pronunciation.\nAlso you can send text in Uzbek and I will translate it into English.\n\n\
	Easy Translate Botga xush kelibsiz!\nBu botdan siz inglizcha so'zlarning ta'riflarini va talaffuzini topishingiz mumkin. Shuningdek o'zbekcha matnlarni ingliz tiliga tarjima qilishingiz mumkin.\n")
	print(username, first_name, last_name)


@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "Welcome to Easy Translate Bot\nSend me the word that you don't know and will provide you its definitions and pronunciation.\nAlso you can send text in Uzbek and I will translate it into English.\n\n\
	Easy Translate Botga xush kelibsiz!\nBu botdan siz inglizcha so'zlarning ta'riflarini va talaffuzini topishingiz mumkin. Shuningdek o'zbekcha matnlarni ingliz tiliga tarjima qilishingiz mumkin.\n")
	

@bot.message_handler(func=lambda message: True)
def english_translate(message):
	translator = Translator()
	lang = translator.detect(message.text).lang
	
	if len(message.text.split()) > 2:
		dest = 'uz' if lang == 'en' else 'en'
		bot.send_message(message.from_user.id, translator.translate(message.text, dest).text)

	elif lang == 'uz':
			word_id = translator.translate(message.text).text
			if word_id:
				bot.send_message(message.from_user.id, word_id)
			else:
				bot.send_message(message.from_user.id, "Bunday so'z topilmadi😔")

	else:
		if lang == 'en':
			word_id = message.text	
		lookup = word_definitions(word_id)
		
		if lookup:
		    bot.send_message(message.from_user.id, f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
		    
		    if lookup.get('audio'):
		        bot.send_audio(message.from_user.id, lookup['audio'])
		else:
			bot.send_message(message.from_user.id, "Bunday so'z topilmadi😔")

bot.polling()