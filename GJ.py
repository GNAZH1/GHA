import re
import asyncio
from telethon import TelegramClient, events
import pyperclip

# Replace with your Telegram API credentials
api_id = '26957529'
api_hash = 'ffe7d862b0a31893682a62bbc0654ced'
phone_number = '+201069751355'

# Variable to store monitored channels
channels = []

# Dictionary for replacements
replacements = {
    'ࢪ': 'ر', '؏': 'ع', 'آ': 'ا', 'ٱ': 'ا', 'ے': '', 'ـ': '', 'اول ': '', 'اسم': '',
    'ۅ': 'و', 'حركات': '', '()': '', 'وبالايموجي': '', 'بالايموجي': '', 'يكتب ': '',
    'واحد ': '', ' خليت حركات حته محد ينسخ': '', 'الشات': '', 'بلشات': '', 'فلشات': '',
    'بدون ': '', 'شخص': '', 'اقواس': '', 'بلاقواس': '', 'بالتعليقات': '', 'التعليقات': '',
    'أول ': '', 'فلبوت': '', 'اقواص': '', 'ايموجي': '', 'ݪ': 'ل', 'ݛ': 'ر', 'حرڪات': '',
    'مع ': '', 'ڪ': 'ك', 'گ': 'ك', 'بل ': '', 'مفعل لا تشارك': '', 'أ': 'ا', 'شات ': '',
    'gbfjcfbknkgfbot': '', 'كلمه': '', 'First': '', 'first': '', 'FIRST': '', 'ټ': 'ت',
    'ډ': 'د', 'ﺂ': 'ا', 'ﺑ': 'ب', 'خاص': '', 'ڝ': 'ص', 'ﻣ': 'م', 'ט': 'ن', 'ڼ': 'ن',
    'נ': 'د', 'ﺣ': 'ح', 'ہ': 'ه', 'J_KO_Lbot': '', 'الشات': '', 'بلتعليقات': '', 'في ': '', 'بلا ': '', 'نقاط ': '', 'في ': '', 'بل ': '', 'شات': '', 'في ': '', 'كلمة ': '', 'كلمه ': ''
    , 'يقول ': '', 'يكتب ': '', 'مناقشه ': '', 'كومنت ': '', 'كمنت ': '', 'l_v_0bot': '', 'ک': 'ك', 'او ل': '', 'ا ول': '', 'ا و ل': '', 'ا و  ل': '', 'يرسل': '', 'الخاص': '', 'للخاص': '', 'ال ': '', 'اول': '', 'هنا.': '', 'هنا': '', 'الأقواس': '', 'الاقواس': '', 'يبعت ': '', 'اتنين': '', 'يبعتوا': '', 'يكسبوا': '', 'تلاته': '', 'ثلاثه': '', 'ثلاث': '', 'خمسه ': '', 'يبعتو ': '', 'يكسبو': '', 'يكسب': '', 'نقطة': ''
}
# List of keywords
keywords = ["اول", "frest", "او ل", "ا ول", "ا و ل"]

# Setting up Telegram client session
client = TelegramClient('session_speed', api_id, api_hash)

# ID of the session owner (you)
your_user_id = 7339072496

# Function to process new messages
@client.on(events.NewMessage)
async def handle_new_message(event):
    global channels, replacements, keywords

    message_text = event.raw_text.lower()  # Convert message to lowercase

    # تحقق من أن الرسالة صادرة منك فقط لتنفيذ الأوامر
    if event.sender_id == your_user_id:
        # التحقق من الأمر لإضافة القنوات للمراقبة
        if message_text.startswith('/set '):
            try:
                chat_ids = message_text.split()[1:]
                for chat_id in chat_ids:
                    if len(channels) < 10:
                        channels.append(int(chat_id))
                await event.reply(f'تمت إضافة القنوات للمراقبة: {channels}')
            except (IndexError, ValueError):
                await event.reply('صيغة الأمر غير صحيحة. يجب أن يكون: /set <channel_id_1> <channel_id_2> ...')

        # التحقق من الأمر لإزالة قناة من المراقبة
        elif message_text.startswith('/rm '):
            try:
                channel_index = int(message_text.split()[1]) - 1
                if 0 <= channel_index < len(channels):
                    removed_channel = channels.pop(channel_index)
                    await event.reply(f'تمت إزالة القناة: {removed_channel}')
                else:
                    await event.reply('مؤشر القناة غير صحيح.')
            except (IndexError, ValueError):
                await event.reply('صيغة الأمر غير صحيحة. يجب أن يكون: /rm <channel_index>')

        # التحقق من الأمر لعرض القنوات المراقبة
        elif message_text.startswith('/ls'):
            await event.reply(f'القنوات المراقبة حالياً: {channels}')

        # التحقق من الأمر لإضافة كلمة محظورة
        elif message_text.startswith('/aw'):
            try:
                # استخراج الكلمة المحظورة والبديل من الأمر
                command_parts = re.split(r'\s*\'(.+?)\'\s*:\s*\'(.+?)\'', message_text)
                if len(command_parts) >= 3:
                    word = command_parts[1].strip()
                    replacement = command_parts[2].strip()

                    # إذا كان البديل فارغًا، اجعله خاليًا
                    if replacement == 'البديل لها':
                        replacement = ''

                    # إضافة الكلمة المحظورة وبديلها إلى القائمة replacements
                    replacements[word] = replacement
                    await event.reply(f'تمت إضافة الكلمة المحظورة: {word} مع البديل: {replacement}')
                    save_data()  # Save data after modification
                else:
                    await event.reply('صيغة الأمر غير صحيحة. يجب أن يكون: /aw \'الكلمة المحظورة\' : \'البديل لها\'')
            except IndexError:
                await event.reply('صيغة الأمر غير صحيحة. يجب أن يكون: /aw \'الكلمة المحظورة\' : \'البديل لها\'')
        # التحقق من الأمر لإزالة كلمة محظورة
        elif message_text.startswith('/rw'):
            try:
                word = message_text.split()[1]
                if word in replacements:
                    del replacements[word]
                    await event.reply(f'تمت إزالة الكلمة المحظورة: {word}')
                else:
                    await event.reply(f'لم يتم العثور على الكلمة: {word}')
            except IndexError:
                await event.reply('صيغة الأمر غير صحيحة. يجب أن يكون: /rw <word>')

        # التحقق من الأمر لإضافة كلمة مفتاحية
        elif message_text.startswith('/ak'):
            try:
                keyword = message_text.split()[1]
                if keyword not in keywords:
                    keywords.append(keyword)
                    await event.reply(f'تمت إضافة الكلمة المفتاحية: {keyword}')
                else:
                    await event.reply(f'الكلمة المفتاحية موجودة بالفعل: {keyword}')
            except IndexError:
                await event.reply('صيغة الأمر غير صحيحة. يجب أن يكون: /ak <keyword>')

        # التحقق من الأمر لإزالة كلمة مفتاحية
        elif message_text.startswith('/rk'):
            try:
                keyword = message_text.split()[1]
                if keyword in keywords:
                    keywords.remove(keyword)
                    await event.reply(f'تمت إزالة الكلمة المفتاحية: {keyword}')
                else:
                    await event.reply(f'لم يتم العثور على الكلمة المفتاحية: {keyword}')
            except IndexError:
                await event.reply('صيغة الأمر غير صحيحة. يجب أن يكون: /rk <keyword>')

        # التحقق من الأمر لعرض رسالة المساعدة
        elif message_text.startswith('/help'):
            help_message = (
                "`/set -100` <channel_id_1> <channel_id_2> ... : إضافة قنوات للمراقبة (حتى 10).\n\n"
                "`/rm` <channel_index> : إزالة قناة من قائمة المراقبة.\n\n"
                "`/ls` : عرض جميع القنوات المراقبة.\n\n"
                "`/aw` /aw 'here' : '' : إضافة كلمة محظورة وبديلها.\n\n"
                "`/rw` <word> : إزالة كلمة محظورة.\n\n"
                "`/ak` <keyword> : إضافة كلمة مفتاحية.\n\n"
                "`/rk` <keyword> : إزالة كلمة مفتاحية.\n\n"
                "`/help` : عرض رسالة المساعدة.\n\n"
                "`/restart` : إعادة تشغيل البوت."
            )
            await event.reply(help_message)

    # Command to restart
    elif message_text.startswith('/re'):
        await event.reply('Restarting the bot...')
        await client.disconnect()
        await client.start(phone_number)

    # Check for keywords in messages from the monitored channels
    if event.chat_id in channels:
        if any(keyword in message_text for keyword in keywords):
            bot_username = find_bot_username(event.raw_text)
            if bot_username:
                cleaned_text = clean_and_copy(event.raw_text, bot_username)
                await send_to_bot(cleaned_text, bot_username)

def find_bot_username(text):
    # Find username after @ symbol in the message
    match = re.search(r'@([\w]+)', text)
    if match:
        return match.group(1)
    return None

def clean_and_copy(text, bot_username):
    global replacements

    # Remove the bot username if exists
    text = text.replace(f'@{bot_username}', '')

    # Remove Arabic diacritics and unwanted symbols
    text = re.sub(r'[\u064b-\u065f\u0610-\u061a]+', '', text)
    text = re.sub(r'[^\w\s@]', '', text)  # Keep '@' symbol for username extraction

    # Other replacements
    for pattern, replacement in replacements.items():
        text = text.replace(pattern, replacement)

    # Remove extra spaces and correct periods
    text = text.replace(' . ', ' ').replace(' .', '').replace('. ', '')
    text = text.replace('  ', ' ').strip()

    words_to_check = ["تفكيك", "يفكك", "فكك"]
    for word in words_to_check:
        if word in text:
            text = text.replace(word, '')
            text = ' '.join(list(text)).strip().replace('  ', ' ')

    # Convert text to bold
    text = f'**{text}**'

    return text

async def send_to_bot(text, bot_username):
    if bot_username:
        try:
            await client.send_message(bot_username, text)
            print(f'Sent processed text to {bot_username}')
        except Exception as e:
            print(f'Error sending message to {bot_username}: {str(e)}')

# Start the session and connect to Telegram
async def main():
    await client.start(phone_number)
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
