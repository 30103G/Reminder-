import asyncio
import sys,re,os
import json
from openai import OpenAI
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Windows event loop fix
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# with open("config.json") as f:
#     config = json.load(f)

# Load config
# bot_token=config['Reminder_token']
bot_token = os.getenv("REMINDER_TOKEN")
# OpenAI.base_URL="https://openrouter.ai/api/v1"
# OpenAI.api_key = config['OpenAI_API_Key']

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Store user selections
user_data = {}

# Buttons
bulk = InlineKeyboardButton(text="Bulk", callback_data="Bulk")
cut = InlineKeyboardButton(text="Cuts", callback_data="Cuts")
category_buttons = InlineKeyboardMarkup().add(bulk, cut)

weights = ["50-55", "55-60", "60-65", "65-70", "70-75"]
weight_buttons = [InlineKeyboardButton(text=w, callback_data=w) for w in weights]
weight_list = InlineKeyboardMarkup(row_width=2).add(*weight_buttons)

# Height Buttons
heights = ["160-165", "165-170", "170-175", "175-180"]
height_buttons = [InlineKeyboardButton(text=h, callback_data=h) for h in heights]
height_list = InlineKeyboardMarkup(row_width=2).add(*height_buttons)

def clean_markdown(text):
    text = re.sub(r'#+\s?', '', text)                # Remove headings
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)     # Bold
    text = re.sub(r'__(.*?)__', r'\1', text)         # Italic
    text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)  # Bullets
    return text.strip()

# Start command
@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    user_data[msg.from_user.id] = {}  # Reset user data
    await msg.answer(f"Howdy👋! {msg.from_user.first_name}")
    await msg.answer("Please select your fitness goal:", reply_markup=category_buttons)

# Category selected
@dp.callback_query_handler(text=["Bulk", "Cuts"])
async def handle_category(call: types.CallbackQuery):
    user_data[call.from_user.id]["category"] = call.data
    await call.message.answer("Please select your weight range:", reply_markup=weight_list)

# Weight selected
@dp.callback_query_handler(text=["50-55", "55-60", "60-65", "65-70", "70-75"])
async def handle_weight(call: types.CallbackQuery):
    user_data[call.from_user.id]["weight"] = call.data
    await call.message.answer("Now select your height:", reply_markup=height_list)

# Height selected 
@dp.callback_query_handler(text=["160-165", "165-170", "170-175", "175-180"])
async def handle_height(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_data[user_id]["height"] = call.data

    # Get user selections
    goal = user_data[user_id]["category"]
    weight = user_data[user_id]["weight"]
    height = user_data[user_id]["height"]
    # print(goal,weight,height)

    msg = await call.message.answer("Generating your personalized diet plan... 🥗")

    # OpenAI prompt
    prompt = f"""
You are a professional dietitian. Suggest a personalized diet plan for a person who wants to {goal.lower()}.
Weight: {weight} kg
Height: {height} cm
The plan should include meals for breakfast, lunch, and dinner with timings and calorie breakdown.
    """

    # Call OpenAI API
    try:
        client=OpenAI(
            base_url="https://openrouter.ai/api/v1",
            # api_key=config['OpenAI_API_Key']
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        plan = response.choices[0].message.content
        clean_plan=clean_markdown(plan)
        await msg.delete()
        await call.message.answer(clean_plan)
    except Exception as e:
        await call.message.answer("Failed to fetch diet plan. Try again later.")
        print(f"OpenAI error: {e}")

# Run bot
if __name__ == '__main__':
    print("Polling")
    executor.start_polling(dp)
