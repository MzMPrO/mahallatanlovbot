import datetime
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import exceptions
from aiogram.types import InputFile
import asyncio
import pandas as pd

from apps.location.models import Village, Area, Region
from bot.button.reply import menu_rkm
from bot.handler import db, MyStates
from bot.utils.log import log
from bot.utils.validator import excel_upload, generate_statistics, write_data_to_excel


async def post_command(message: types.Message):
    users_count = await db.get_users_count()
    await message.answer(f"{users_count} ta obunachiga yubormoqchi bo'lgan xabaringizni yuboring")
    await MyStates.post_state.set()


async def post_handler(message: types.Message, state: FSMContext):
    from_chat_id = message.chat.id
    message_id = message.message_id
    await state.update_data(from_chat_id=from_chat_id, message_id=message_id)
    confirm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Ha", "Yo'q")
    await message.answer("Xabar kimdan yuborilgani ko'rinsinmi?", reply_markup=confirm_keyboard)
    await MyStates.forward_type_state.set()


async def forward_type_forward_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.bot.forward_message(
        chat_id=message.chat.id,
        from_chat_id=data['from_chat_id'],
        message_id=data['message_id'],
    )
    await state.update_data(forward_type='forward')
    confirm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Ha", "Yo'q")
    await message.answer("Shu xabar yuborilishini tasdiqlaysizmi?", reply_markup=confirm_keyboard)
    await MyStates.confirm_state.set()


async def forward_type_copy_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=data['from_chat_id'],
        message_id=data['message_id'],
    )
    await state.update_data(forward_type='copy')
    confirm_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Ha", "Yo'q")
    await message.answer("Shu xabar yuborilishini tasdiqlaysizmi?", reply_markup=confirm_keyboard)
    await MyStates.confirm_state.set()


async def confirm_yes_handler(message: types.Message, state: FSMContext):
    await message.answer("Xabar yuborilyapti...", reply_markup=types.ReplyKeyboardRemove())
    data = await state.get_data()
    users = await db.get_users()
    successful, blocked, not_found, deactivated = 0, 0, 0, 0

    for user_id in users:
        try:
            await message.bot.forward_message(
                chat_id=user_id.chat_id,
                from_chat_id=data['from_chat_id'],
                message_id=data['message_id'],
            ) if data['forward_type'] == 'forward' else await message.bot.copy_message(
                chat_id=user_id.chat_id,
                from_chat_id=data['from_chat_id'],
                message_id=data['message_id'],
            )

            successful += 1
            await db.update_user_status(status='active', chat_id=user_id.chat_id)
            if successful % 1000 == 0:
                await message.answer(
                    f"Xabar {successful} ta obunachiga yuborildi. Qolgan obunachilarga ham yuborilyapti...")

            await asyncio.sleep(.05)
        except exceptions.RetryAfter as e:
            log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
        except (exceptions.BotBlocked, exceptions.UserDeactivated, exceptions.TelegramAPIError) as e:
            log.error(f"Target [ID:{user_id.chat_id}]: {str(e).lower()}")
            if isinstance(e, exceptions.BotBlocked):
                blocked += 1
                await db.update_user_status(status='blocked', chat_id=user_id.chat_id)
            elif isinstance(e, exceptions.UserDeactivated):
                deactivated += 1
                await db.update_user_status(status='deactivated', chat_id=user_id.chat_id)
            elif isinstance(e, exceptions.ChatNotFound):
                not_found += 1
                await db.update_user_status(status='not_found', chat_id=user_id.chat_id)
                log.error(f"Target [ID:{user_id.chat_id}]: invalid user ID")

    await message.answer(
        f"Xabar {successful} ta obunachiga muvaffaqiyatli yuborildi\nBloklangan: {blocked}\nO'chirilgan: {deactivated}\nChat topilmadi: {not_found}",
        reply_markup=menu_rkm()
    )
    log.info(f"{successful} messages successful sent.")
    await state.finish()


async def confirm_no_handler(message: types.Message, state: FSMContext):
    await message.answer('Xabar yuborish bekor qilindi!', reply_markup=menu_rkm())
    await state.finish()


# async def get_command(message: types.Message):
#     users = await db.get_users()
#     names = []
#     date_of_birth = []
#     regions = []
#     areas = []
#     villages = []
#     jobs = []
#     phone_numbers = []
#     chat_ids = []
#     for user in users:
#         village = await Village.objects.aget(id=user.village_id)
#         area = await Area.objects.aget(id=village.area_id)
#         region = await Region.objects.aget(id=area.region_id)
#         names.append(user.name)
#         date_of_birth.append(user.age)
#         regions.append(region.name)
#         areas.append(area.name)
#         villages.append(village.name)
#         jobs.append(user.job_position)
#         phone_numbers.append(user.phone_number)
#         chat_ids.append(user.chat_id)
#
#     data = {
#         "Chat id": chat_ids,
#         "F.I.Sh.": names,
#         "Tug'ilgan yilingiz": date_of_birth,
#         "Yashash manzilingiz": regions,
#         "Tuman/shahar": areas,
#         "Mahalla": villages,
#         "Ish/o'qish joyingiz": jobs,
#         "Telefon raqamingiz": phone_numbers
#     }
#     output_path = excel_upload(data)
#     file = InputFile(output_path)
#     await message.bot.send_document(message.chat.id, file)
#

async def get_command(message: types.Message):
    # Получаем пользователей из базы данных
    users = await db.get_users()

    # Списки для хранения данных
    data = {
        "Chat id": [],
        "F.I.Sh.": [],
        "Tug'ilgan yilingiz": [],
        "Yashash manzilingiz": [],
        "Tuman/shahar": [],
        "Mahalla": [],
        "Ish/o'qish joyingiz": [],
        "Telefon raqamingiz": []
    }

    # Создаем словари для кэширования данных о деревнях, районах и регионах
    village_cache = {}
    area_cache = {}
    region_cache = {}

    # Заполняем списки данными
    for user in users:
        # Кэшируем деревни
        if user.village_id not in village_cache:
            village_cache[user.village_id] = await Village.objects.aget(id=user.village_id)
        village = village_cache[user.village_id]

        # Кэшируем районы
        if village.area_id not in area_cache:
            area_cache[village.area_id] = await Area.objects.aget(id=village.area_id)
        area = area_cache[village.area_id]

        # Кэшируем регионы
        if area.region_id not in region_cache:
            region_cache[area.region_id] = await Region.objects.aget(id=area.region_id)
        region = region_cache[area.region_id]

        # Заполняем данные
        data["Chat id"].append(user.chat_id)
        data["F.I.Sh."].append(user.name)
        data["Tug'ilgan yilingiz"].append(user.age)
        data["Yashash manzilingiz"].append(region.name)
        data["Tuman/shahar"].append(area.name)
        data["Mahalla"].append(village.name)
        data["Ish/o'qish joyingiz"].append(user.job_position)
        data["Telefon raqamingiz"].append(user.phone_number)

    # Создаем Excel файл
    output_path = excel_upload(data)

    # Отправляем файл
    file = InputFile(output_path)
    await message.bot.send_document(message.chat.id, file)


async def get_all_command(message: types.Message):
    file_path = await write_data_to_excel(f'MahallaTanlovBot {datetime.date.today()}.xlsx')
    await message.reply_document(InputFile(file_path))

    os.remove(file_path)


async def send_message(message: types.Message):
    try:
        for i in range(10000):
            await message.answer("Hi!")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{message.chat.id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
