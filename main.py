import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "8470181529:AAFnfNGSsMLzAJ3XhZhJ4pP8hJ1VUFXsgu4"
TIMEZONE = pytz.timezone('Asia/Kolkata')

# Complete Mess Schedule Data
MESS_SCHEDULE = {
    "Monday": {
        "07:30": [
            "Poha + Namkeen / Layered Butter Paratha + Aloo Gravy (alt)",
            "Onion + Lemon Pieces",
            "Seasonal Mixed Fruit Pieces",
            "Milk + Bournvita",
            "Tea + Coffee",
            "Bread + Butter + Jam",
            "Fresh Sprouts"
        ],
        "12:00": [
            "Veg Kofta / Lauki Chana Masala (alt)",
            "Dal Makhani / Moong Masoor Dal (alt)",
            "Rice",
            "Butter Roti",
            "Salad + Lemon + Pickle",
            "Papad / Fryums",
            "Masala Shikanji"
        ],
        "17:00": [
            "Aloo Chana Chaat / Ragda Pattice (alt)",
            "Tea + Coffee",
            "Pudina Chutney + Imli Chutney"
        ],
        "19:30": [
            "Seasonal Vegetable",
            "Mix Dal / Dal Palak",
            "Veg Pulao",
            "Butter Roti",
            "Salad + Lemon + Pickle",
            "Rasam",
            "Jalebi"
        ]
    },
    "Tuesday": {
        "07:30": [
            "Pao Bhaji / Chole Kulche (alt)",
            "Onion + Lemon Pieces",
            "Seasonal Mixed Fruit Pieces",
            "Milk + Bournvita",
            "Tea + Coffee",
            "Bread + Butter + Jam",
            "Fresh Sprouts"
        ],
        "12:00": [
            "Kadai Paneer / Methi Malai Paneer (alt)",
            "Rajma Masala",
            "Jeera Rice",
            "Butter Roti",
            "Curd",
            "Salad + Lemon + Pickle",
            "Papad / Fryums"
        ],
        "17:00": [
            "Bread Pakora / Bread Roll (alt)",
            "Tea + Coffee",
            "Pudina Chutney + Imli Chutney",
            "Rooh Afza Milkshake"
        ],
        "19:30": [
            "Aloo Gravy",
            "Kala Chana / Chole (alt)",
            "Rice",
            "Poori + Butter Roti",
            "Salad + Lemon + Pickle",
            "Tomato Soup"
        ]
    },
    "Wednesday": {
        "07:30": [
            "Idli + Medu Vada + Sambhar",
            "Coconut Chutney",
            "Seasonal Mixed Fruit Pieces",
            "Milk + Bournvita",
            "Tea + Coffee",
            "Bread + Butter + Jam",
            "Fresh Sprouts"
        ],
        "12:00": [
            "Aloo Jeera",
            "Kadhi Pakoda",
            "Rice",
            "Butter Roti",
            "Vegetable Raita",
            "Salad + Lemon + Pickle",
            "Papad / Fryums"
        ],
        "17:00": [
            "Bhel Puri / Jhal Muri",
            "Tea + Coffee",
            "Pudina Chutney + Imli Chutney",
            "Masala Shikanji"
        ],
        "19:30": [
            "Egg Curry + Shahi Paneer / Palak Paneer",
            "Mix Dal / Akka Masoor Dal (alt)",
            "Jeera Rice",
            "Butter Roti",
            "Salad + Lemon",
            "Rasam",
            "Pickle",
            "Rice Kheer / Seviyan Kheer (alt)"
        ]
    },
    "Thursday": {
        "07:30": [
            "Besan Chilla / Aloo Sandwich (alt) + Omelette",
            "Tomato Ketchup",
            "Seasonal Mixed Fruit Pieces",
            "Milk + Bournvita",
            "Tea + Coffee",
            "Bread + Butter + Jam",
            "Fresh Sprouts"
        ],
        "12:00": [
            "Sev Tamatar / Papad Pyaz (alt)",
            "Mix Dal",
            "Rice",
            "Butter Roti",
            "Curd",
            "Salad + Lemon + Pickle",
            "Papad / Fryums"
        ],
        "17:00": [
            "Maggi / Chowmein (alt)",
            "Tea + Coffee",
            "Tomato Ketchup"
        ],
        "19:30": [
            "Seasonal Vegetable",
            "Lobia Dal / Arhar Dal (alt)",
            "Veg Biryani",
            "Butter Roti",
            "Salad + Lemon + Pickle",
            "Rasam"
        ]
    },
    "Friday": {
        "07:30": [
            "Corn Flakes",
            "Upma / Masala Khichdi (alt)",
            "Seasonal Mixed Fruit Pieces",
            "Milk + Bournvita",
            "Tea + Coffee",
            "Bread + Butter + Jam",
            "Fresh Sprouts"
        ],
        "12:00": [
            "Dam Aloo / Aloo Pyaz (alt)",
            "Jeera Rice",
            "Butter Roti",
            "Salad + Lemon + Pickle",
            "Papad / Fryums"
        ],
        "17:00": [
            "Fried Idli Masala / Poha"
        ],
        "19:30": [
            "Mix Veg"
        ]
    },
    "Saturday": {
        "07:30": [
            "Aloo Pyaz Parantha / Paneer Pyaz Parantha (alt)",
            "Curd + Pickle + Sauce",
            "Seasonal Mixed Fruit Pieces",
            "Milk + Bournvita",
            "Tea + Coffee",
            "Bread + Butter + Jam",
            "Fresh Sprouts",
            "Corn Flakes"
        ],
        "12:00": [
            "Seasonal Vegetable",
            "Chana Dal Tadka / Moong Dal Tadka (alt)",
            "Jeera Rice",
            "Butter Roti",
            "Vegetable Raita",
            "Salad + Lemon + Pickle",
            "Papad / Fryums"
        ],
        "17:00": [
            "Samosa Chaat / Vada Sambar (alt)",
            "Tea + Coffee",
            "Pudina Chutney + Imli Chutney"
        ],
        "19:30": [
            "Masala Dosa + Onion Dosa + Sambar + Idli",
            "Coconut Chutney",
            "Veg Biryani",
            "Salad + Lemon + Pickle",
            "Fruit Custard",
            "Rasam"
        ]
    },
    "Sunday": {
        "07:30": [
            "Chole + Puri + Bhature",
            "Fried Chilly"
        ],
        "12:00": [
            "Paneer Bhurji / Paneer Butter Masala (alt)",
            "Dal Fry"
        ],
        "17:00": [
            "Veg Sandwich / Coleslaw Sandwich (alt)",
            "Tea + Coffee"
        ],
        "19:30": [
            "Malai Kofta / Vegetable Shahi Korma (alt)",
            "Rajma / Dal Makhani (alt)"
        ]
    }
}

class MessBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.scheduler = AsyncIOScheduler(timezone=TIMEZONE)
        self.user_chat_ids = set()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        self.user_chat_ids.add(chat_id)

        today = datetime.now(TIMEZONE).strftime("%A")
        schedule_text = f"🍽️ **Today's Mess Schedule ({today})**\n\n"

        if today in MESS_SCHEDULE:
            day_schedule = MESS_SCHEDULE[today]
            for meal_time, menu_items in day_schedule.items():
                menu_text = "\n".join(f"• {item}" for item in menu_items)
                schedule_text += f"**Meal Time: {meal_time}**\n{menu_text}\n\n"
        else:
            schedule_text += "No schedule available for today."

        schedule_text += "🔔 Automatic meal reminders are active!"

        await update.message.reply_text(schedule_text, parse_mode='Markdown')
        logger.info(f"User {chat_id} started the bot")

    async def send_meal_reminder(self, meal_time: str):
        today = datetime.now(TIMEZONE).strftime("%A")

        if today not in MESS_SCHEDULE or meal_time not in MESS_SCHEDULE[today]:
            return

        menu_items = MESS_SCHEDULE[today][meal_time]
        menu_text = "\n".join(f"• {item}" for item in menu_items)

        reminder_text = f"🔔 **Meal Time: {meal_time}**\n\n{menu_text}\n\nEnjoy your meal! 😊"

        for chat_id in self.user_chat_ids.copy():
            try:
                await self.application.bot.send_message(
                    chat_id=chat_id,
                    text=reminder_text,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to send reminder to {chat_id}: {e}")
                self.user_chat_ids.discard(chat_id)

    def setup_meal_schedules(self):
        for day_schedule in MESS_SCHEDULE.values():
            for meal_time, menu_items in day_schedule.items():
                hour, minute = map(int, meal_time.split(':'))

                job_id = f"{meal_time}_{hour}_{minute}"
                self.scheduler.add_job(
                    func=self.send_meal_reminder,
                    trigger=CronTrigger(hour=hour, minute=minute),
                    args=[meal_time],
                    id=job_id,
                    replace_existing=True
                )
                logger.info(f"Scheduled reminder at {meal_time}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
🤖 **Mess Schedule Bot Commands**

/start - Show today's full mess schedule  
/help - Show this help message  
/today - Show today's full mess schedule  
/tomorrow - Show tomorrow's full mess schedule  
/monday - Show full Monday's menu  
/tuesday - Show full Tuesday's menu  
/wednesday - Show full Wednesday's menu  
/thursday - Show full Thursday's menu  
/friday - Show full Friday's menu  
/saturday - Show full Saturday's menu  
/sunday - Show full Sunday's menu  

🔔 Automatic reminders at:
• Breakfast: 07:30 AM  
• Lunch: 12:00 PM  
• Snacks: 05:00 PM  
• Dinner: 07:30 PM
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        today = datetime.now(TIMEZONE).strftime("%A")

        schedule_text = f"🍽️ **Today's Full Menu ({today})**\n\n"
        if today in MESS_SCHEDULE:
            day_schedule = MESS_SCHEDULE[today]
            for meal_time, menu_items in day_schedule.items():
                menu_text = "\n".join(f"• {item}" for item in menu_items)
                schedule_text += f"**Meal Time: {meal_time}**\n{menu_text}\n\n"
        else:
            schedule_text += "No schedule available for today."

        await update.message.reply_text(schedule_text, parse_mode='Markdown')

    async def tomorrow_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tomorrow_date = datetime.now(TIMEZONE) + timedelta(days=1)
        tomorrow = tomorrow_date.strftime("%A")

        schedule_text = f"🍽️ **Tomorrow's Full Menu ({tomorrow})**\n\n"
        if tomorrow in MESS_SCHEDULE:
            day_schedule = MESS_SCHEDULE[tomorrow]
            for meal_time, menu_items in day_schedule.items():
                menu_text = "\n".join(f"• {item}" for item in menu_items)
                schedule_text += f"**Meal Time: {meal_time}**\n{menu_text}\n\n"
        else:
            schedule_text += "No schedule available for tomorrow."

        await update.message.reply_text(schedule_text, parse_mode='Markdown')

    async def day_summary_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        command = update.message.text.lstrip("/").capitalize()

        schedule_text = f"🍽️ **Full Menu for {command}**\n\n"

        if command in MESS_SCHEDULE:
            day_schedule = MESS_SCHEDULE[command]
            for meal_time, menu_items in day_schedule.items():
                menu_text = "\n".join(f"• {item}" for item in menu_items)
                schedule_text += f"**Meal Time: {meal_time}**\n{menu_text}\n\n"
        else:
            schedule_text += "No schedule available for this day."

        await update.message.reply_text(schedule_text, parse_mode='Markdown')

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Exception while handling update: {context.error}")

    async def run(self):
        logger.info("Starting Mess Schedule Bot...")

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("today", self.today_command))
        self.application.add_handler(CommandHandler("tomorrow", self.tomorrow_command))

        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            self.application.add_handler(CommandHandler(day, self.day_summary_command))

        self.application.add_error_handler(self.error_handler)

        self.setup_meal_schedules()
        self.scheduler.start()

        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        logger.info("Bot is running...")

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down bot...")

        await self.stop()

    async def stop(self):
        self.scheduler.shutdown()
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()


async def main():
    bot = MessBot()
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")


if __name__ == "__main__":
    print("🤖 Starting Telegram Mess Schedule Bot...")
    print("📋 Features: /today, /tomorrow, /monday to /sunday commands and automatic reminders")

    asyncio.run(main())
