from chat_news.models import Post, Tag, Picture
import configparser
# import json
import os
from django.conf import settings

from telethon.tl.types import MessageMediaPhoto
from telethon.sync import TelegramClient

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

# Адреса чатов
channels = {
            'ozon': 'https://t.me/ozonmarketplace',
            'yandex': 'https://t.me/market_marketplace', }

# создаем теги в модели
for ch in channels:
    if not Tag.objects.filter(name=ch).exists():
        Tag.objects.create(name=ch)

posts_group = {}
message_media_group = {}


# proxy = (proxy_server, proxy_port, proxy_key)

client = TelegramClient(username, api_id, api_hash)

client.start()


async def get_messages(entity, channel):
    """Считываем посты с каналов в telegram"""
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 50   # максимальное число записей, передаваемых за один раз
    number_of_posts = 10

    history = await client(GetHistoryRequest(
        peer=entity,
        offset_id=offset_msg,
        offset_date=None, add_offset=0,
        limit=limit_msg, max_id=0, min_id=0,
        hash=0))
    if not history.messages:
        return None

    messages = history.messages
    while len(posts_group) < number_of_posts:
        for message in messages:
            if message.message != '':
                await save_text_and_img(message, channel)
            elif isinstance(message.media, MessageMediaPhoto):
                if is_grouped(message):
                    save_picture(message, channel,
                                 posts_group[message.grouped_id])
                else:
                    if message.grouped_id:
                        message_media_group[message.grouped_id] = (
                            [message] if message.grouped_id in
                            message_media_group else
                            message_media_group[message.grouped_id].append(
                                message))
        # all_messages.append(message.to_dict())
    # offset_msg = messages[len(messages) - 1].id

# with open('channel_messages.json', 'w', encoding='utf8') as outfile:
# 	json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def is_grouped(message):
    return await bool(message.grouped_id in posts_group)


async def save_text_and_img(message, channel):

    if not Post.objects.filter(content=message.message).exists():
        post = Post.objects.create(
                content=message.message,
                post_time=message.date.strftime("%Y-%m-%d %H:%M:%S"),
                tag=Tag.objects.filter(channel),
            )
    if message.grouped_id in message_media_group:
        for img in message_media_group[message.grouped_id]:
            await save_picture(img, channel, post)

    await save_picture(message, channel, post)

    if message.grouped_id:
        posts_group[message.grouped_id] = post


async def save_picture(message, channel, post):
    if isinstance(message.media, MessageMediaPhoto):
        photo = message.media.photo
        filename = f"{channel}_{message.id}.jpg"
        if not Picture.objects.filter(image=os.path.join(
                settings.MEDIA_ROOT, filename)).exists():
            Picture.objects.create(
                image=await client.download_media(
                    photo, file=os.path.join(settings.MEDIA_ROOT, filename)),
                post=post,
                tag=Tag.objects.filter(channel),
                )


async def main():
    for channel in channels:
        entity = await client.get_entity(channels[channel])
        # await dump_all_participants(channel)
        await get_messages(entity, channel)


def start():
    with client:
        client.loop.run_until_complete(main())
