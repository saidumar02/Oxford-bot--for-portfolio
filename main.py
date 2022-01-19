from aiogram import Bot, Dispatcher, executor, types
from oxfordLookup import getDefinitions
from googletrans import Translator

translator = Translator()

API_TOKEN = 'your token'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(" Assalomu alaykum \nOxford Dictionary botiga xush kelibsiz!\n")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('Botga 2 tadan ortiq so\'z yuboring! \n😉  ENG >> UZB \n😉   UZB >> ENG')

@dp.message_handler()
async def tarjimon(message: types.Message):
    wait = await message.reply('Qabul qilindi.. Kutib turing!')
    lang = translator.detect(message.text).lang
   
    if len(message.text.split()) >= 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:
            if message.text and lang == 'uz':
                uzbek = translator.translate(message.text, dest='en').text
                await message.reply(f"English translation 👉  {uzbek}\nDefinition 👉 {lookup['definitions']}")
            else:
                english = translator.translate(message.text, dest='uz').text
                await message.reply(f"Word: 👉  {word_id}\nUzbek translation: 👉 {english}\nDefinition: 👉 {lookup['definitions']}")

            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
                bool = await bot.delete_message(message.chat.id,message.message_id + 1) #delete message
        else:
            await message.reply("Bunday so'z topilmadi ☹☹")
            bool = await bot.delete_message(message.chat.id,message.message_id + 1) #delete message

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
