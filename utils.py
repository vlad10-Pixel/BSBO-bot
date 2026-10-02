import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

TOKEN_WEATHER = os.getenv("TOKEN_WEATHER")


async def get_weather(lat: float, lon: float) -> str:
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?APPID={TOKEN_WEATHER}"
        f"&lang=ru"
        f"&units=metric"
        f"&lat={lat}"
        f"&lon={lon}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:

                if resp.status != 200:
                    return f"Ошибка при получении данных о погоде. Код: {resp.status}"

                data = await resp.json()

    except aiohttp.ClientError:
        return "Ошибка соединения с сервером погоды."

    except Exception:
        return "Произошла непредвиденная ошибка при получении погоды."

    try:
        city = data.get("name", "Неизвестное место")
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        wind_speed = data["wind"]["speed"]

    except (KeyError, IndexError, TypeError):
        return "Сервер погоды вернул данные в неожиданном формате."

    if wind_speed < 5:
        wind_recom = "🌤 Погода хорошая, ветра почти нет"
    elif wind_speed < 10:
        wind_recom = "🌫 На улице ветрено, оденьтесь чуть теплее"
    elif wind_speed < 20:
        wind_recom = "🌬 Ветер очень сильный, будьте осторожны, выходя из дома"
    else:
        wind_recom = "🌪 На улице шторм, на улицу лучше не выходить"

    return (
        f"Сейчас в {city} {weather}\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"💨 Ветер: {wind_speed} м/с\n"
        f"{wind_recom}"
    )


async def get_cat_url() -> str:
    url = "https://api.thecatapi.com/v1/images/search"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:

                if resp.status != 200:
                    raise aiohttp.ClientError(
                        f"Ошибка API: {resp.status}"
                    )

                data = await resp.json()

        return data[0]["url"]

    except aiohttp.ClientError:
        return ""

    except (KeyError, IndexError, TypeError):
        return ""

    except Exception:
        return ""


async def get_exchange_rate() -> str:
    url = "https://api.frankfurter.dev/v2/rates?base=USD&quotes=RUB"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:

                if resp.status != 200:
                    return f"Ошибка API. Код: {resp.status}"

                data = await resp.json()

        rate = data[0]["rate"]

        return f"💱 1 USD = {rate:.2f} RUB"

    except aiohttp.ClientError:
        return "❌ Не удалось подключиться к API курсов валют."

    except (KeyError, IndexError, TypeError):
        return "❌ API вернул данные в неожиданном формате."

    except Exception:
        return "⚠️ Произошла непредвиденная ошибка при получении курса валют."