import telebot

TOKEN = "8649080316:AAGtjwNwEill-hWghEom2e3MkIphKvkLcNo"
ADMIN_ID = 965940152  # Твой Telegram ID

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  if message.from_user.id == ADMIN_ID:
    bot.reply_to(message, "Панель администратора активна.")
    return

  verification_form = (
      "Привет, ты попал в бота WhiteZone для верификации в наш чат. Заполни"
      " анкету ниже:\n\n"
      "1. Ваш ник на сайте?\n"
      "2. Ваш часовой пояс?\n"
      "3. Как вы узнали про нас?\n"
      "4. Готовы ли вы помогать и тапать за нас?\n"
      "5. С какой целью вы пришли к нам?\n"
      "6. Скиньте скриншот вашего аккаунта на сайте\n\n"
      "Отправьте ответы (текст и скриншот) боту."
  )
  bot.reply_to(message, verification_form)


@bot.message_handler(
    func=lambda message: True,
    content_types=["text", "photo", "document", "video"],
)
def handle_messages(message):
  if message.from_user.id == ADMIN_ID:
    if message.reply_to_message:
      reply_text = message.reply_to_message.text or message.reply_to_message.caption
      try:
        for line in reply_text.split("\n"):
          if "ID:" in line:
            target_user_id = int(
                line.replace("ID:", "").replace("`", "").strip()
            )

            if message.content_type == "text":
              bot.send_message(
                  target_user_id,
                  f"Ответ от администрации:\n\n{message.text}",
              )
            elif message.content_type == "photo":
              bot.send_photo(
                  target_user_id,
                  message.photo[-1].file_id,
                  caption=f"Ответ от администрации:\n\n{message.caption or ''}",
              )

            bot.reply_to(message, "✅ Ответ успешно отправлен игроку!")
            return
      except Exception as e:
        bot.reply_to(
            message,
            "⚠️ Не удалось найти ID игрока. Сделай ответ (реплай) на заявку.",
        )
        return
    return

  user_name = message.from_user.first_name
  user_username = (
      f"@{message.from_user.username}"
      if message.from_user.username
      else "нет username"
  )

  report_caption = (
      f"📥 Новая заявка на верификацию!\n\n"
      f"От: {user_name} ({user_username})\n"
      f"ID: {message.from_user.id}\n\n"
      f"Текст/материал заявки:"
  )

  # Новый измененный текст ответа игроку
  bot.reply_to(
      message, "Спасибо! Ваша заявка на верификацию отправлена администрации"
  )

  if message.content_type == "photo":
    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"{report_caption}\n{message.caption or ''}",
    )
  else:
    bot.send_message(
        ADMIN_ID,
        f"{report_caption}\n{message.text}",
    )


if __name__ == "__main__":
  print("Бот запущен...")
  bot.infinity_polling()
