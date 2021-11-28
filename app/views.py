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
	print(total_amount)
	return render(request, 'home.html', context={'total_amount':total_amount,})


@bot.message_handler(commands=['start'])
def send_welcome(message):
	username = message.from_user.username
	first_name = message.from_user.first_name
	last_name = message.from_user.last_name
	new_user = BotUsers.objects.create(username=username, first_name=first_name, last_name=last_name)
	new_user.save()
	bot.reply_to(message, "Welcome to Easy Translate bot\nSend me the word that you don't know and will provide you its definitions and pronunciation.\nAlso you can send texts in Uzbek and I will translate it into English.")
	print(username, first_name, last_name)


@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Send me the word that you don't know and will provide you its definitions and pronunciation.\nAlso you can send texts in Uzbek and I will translate it into English.")
	

@bot.message_handler(func=lambda message: True)
def english_translate(message):
	translator = Translator()
	lang = translator.detect(message.text).lang
	print(lang)
	
	if len(message.text.split()) > 2:
		dest = 'uz' if lang == 'en' else 'en'
		bot.send_message(message.from_user.id, translator.translate(message.text, dest).text)

	else:
		if lang == 'en':
			word_id = message.text
		
		if lang == 'uz':
			word_id = translator.translate(message.text).text
			bot.send_message(message.from_user.id, word_id)
		lookup = word_definitions(word_id)
		
		if lookup:
		    bot.send_message(message.from_user.id, f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
		    
		    if lookup.get('audio'):
		        bot.send_audio(message.from_user.id, lookup['audio'])
		else:
			bot.send_message(message.from_user.id, "Bunday so'z topilmadi😔")

	

bot.polling()