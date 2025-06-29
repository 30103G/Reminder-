from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions


bot_token = '7587245488:AAHMsMIJQmVcCeE7M8AJ8mKuhImsqFdnIk4'  # Replace with your bot token
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
Botname = '@luminarywispbot'

print('started.')
one = InlineKeyboardButton(text="00:00-1:00", callback_data="one")
two = InlineKeyboardButton(text="1:00-2:00", callback_data="two")
three = InlineKeyboardButton(text="2:00-3:00", callback_data="three")
four = InlineKeyboardButton(text="3:00-4:00", callback_data="four")
five = InlineKeyboardButton(text="4:00-5:00", callback_data="five")
six = InlineKeyboardButton(text="5:00-6:00", callback_data="six")
seven = InlineKeyboardButton(text="6:00-7:00", callback_data="seven")
eight = InlineKeyboardButton(text="7:00-8:00", callback_data="eight")
nine = InlineKeyboardButton(text="8:00-9:00", callback_data="nine")
ten = InlineKeyboardButton(text="9:00-10:00", callback_data="ten")
eleven = InlineKeyboardButton(text="10:00-11:00", callback_data="eleven")
twelve = InlineKeyboardButton(text="11:00-12:00", callback_data="twelve")
thirteen = InlineKeyboardButton(text="12:00-13:00", callback_data="thirteen")
fourteen = InlineKeyboardButton(text="13:00-14:00", callback_data="fourteen")
fifteen = InlineKeyboardButton(text="14:00-15:00", callback_data="fifteen")
sixteen = InlineKeyboardButton(text="15:00-16:00", callback_data="sixteen")
seventeen = InlineKeyboardButton(text="16:00-17:00", callback_data="seventeen")
eighteen = InlineKeyboardButton(text="17:00-18:00", callback_data="eighteen")
nineteen = InlineKeyboardButton(text="18:00-19:00", callback_data="nineteen")
twenty = InlineKeyboardButton(text="19:00-20:00", callback_data="twenty")
twentyOne = InlineKeyboardButton(text="20:00-21:00", callback_data="twentyOne")
twentyTwo = InlineKeyboardButton(text="21:00-22:00", callback_data="twentyTwo")
twentyThree = InlineKeyboardButton(text="22:00-23:00", callback_data="twentyThree")
twentyFour = InlineKeyboardButton(text="23:00-00:00", callback_data="twentyFour")

time_slots = InlineKeyboardMarkup().add(one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, sixteen, seventeen, eighteen, nineteen, twenty, twentyOne, twentyTwo, twentyThree, twentyFour)

# /start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Howdy👋! {name}")
    await message.answer("--------------------------")
    await message.answer("Choose the time to remind You", reply_markup=time_slots)
    
@dp.callback_query_handler(text=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twentyOne', 'twentyTwo', 'twentyThree', 'twentyFour'])
async def check(call: types.CallbackQuery):
    try:
        if call.data in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twentyOne', 'twentyTwo', 'twentyThree', 'twentyFour']:
            await call.message.answer("Enter the Event name or Notes to remind you")
    except exceptions.MessageNotModified as e:
        print("Message was not modified:", e)
    except exceptions.TelegramAPIError as e:
        if "Query is too old" in str(e):
            print("Query is too old. Retrying...")
            # Retry the request here
        else:
            print("An error occurred:", e)
if __name__ == '__main__':
    print("polling..")
    executor.start_polling(dp)
