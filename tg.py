async def post_telegram(telegram_chat_id, bot, text, image):
    if image:
        message = await bot.send_photo(chat_id=telegram_chat_id, photo=image, caption=text)
    else:
        message = await bot.send_message(chat_id=telegram_chat_id, text=text)
    return message['message_id']
