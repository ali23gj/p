import telebot
import zipfile
import os

# استبدل توكن البوت الخاص بك هنا
TOKEN = "6852440644:AAGH6gGnnPmWrIoe-SXIR_FVlAts7dXI6-M"
bot = telebot.TeleBot(TOKEN)

# الحصول على المجلد الحالي الذي يعمل عليه السكربت
CURRENT_FOLDER = os.getcwd()

# دالة لمعالجة الملفات
@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # تحديد مسار ملف zip الذي تم استلامه
    zip_file_path = os.path.join(CURRENT_FOLDER, message.document.file_name)
    
    # حفظ الملف المؤقت
    with open(zip_file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # التحقق من أن الملف هو zip
    if zipfile.is_zipfile(zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(CURRENT_FOLDER)
        bot.reply_to(message, "تم فك ضغط الملف وحفظه بنجاح في المجلد الحالي.")
    else:
        bot.reply_to(message, "الملف ليس بصيغة ZIP.")
    
    # يمكنك حذف الملف المضغوط بعد فك الضغط إذا أردت
    os.remove(zip_file_path)

# تشغيل البوت
bot.polling()