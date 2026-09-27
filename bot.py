import os
import phonenumbers

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في بوت فحص الأرقام\n\n"
        "📱 أرسل رقم الهاتف مع رمز الدولة، مثال:\n"
        "+963xxxxxxxxx\n"
        "+961xxxxxxxx\n"
        "+905xxxxxxxxx"
    )


async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    number_text = update.message.text.strip()

    try:
        number = phonenumbers.parse(number_text, None)

        valid = phonenumbers.is_valid_number(number)
        possible = phonenumbers.is_possible_number(number)

        country = phonenumbers.region_code_for_number(number)
        country_name = country if country else "غير معروف"

        number_type = phonenumbers.number_type(number)

        types = {
            0: "هاتف ثابت",
            1: "هاتف محمول",
            2: "رقم مجاني",
            3: "رقم مدفوع",
            4: "رقم مشترك",
            5: "رقم VoIP",
            6: "رقم شخصي",
            99: "غير معروف",
        }

        type_name = types.get(number_type, "غير معروف")

        await update.message.reply_text(
            "🔎 نتيجة فحص الرقم:\n\n"
            f"📞 الرقم: {number_text}\n"
            f"🌍 رمز المنطقة: {country_name}\n"
            f"📱 النوع: {type_name}\n"
            f"✅ الصيغة ممكنة: {'نعم' if possible else 'لا'}\n"
            f"✅ الرقم صالح: {'نعم' if valid else 'لا'}\n\n"
            "ℹ️ هذا الفحص لا يكشف اسم صاحب الرقم أو بياناته الشخصية."
        )

    except Exception:
        await update.message.reply_text(
            "❌ لم أستطع قراءة الرقم.\n\n"
            "أرسل الرقم بالصيغة الدولية، مثال:\n"
            "+963xxxxxxxxx"
        )


def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )
