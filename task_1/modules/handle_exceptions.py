from functools import wraps
import json
from pymongo.errors import PyMongoError, ConnectionFailure

def handle_exceptions(func):
    """
    Універсальний декоратор для обробки виключень у CRUD операціях
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except FileNotFoundError:
            print("❌ Файл не знайдено. Перевірте шлях до файлу.")
            return None
        
        except json.JSONDecodeError as e:
            print(f"❌ Помилка декодування JSON: {e}")
            return None
        
        except ConnectionFailure:
            print("❌ Помилка підключення до MongoDB. Перевірте, чи запущена база даних.")
            return None
        
        except PyMongoError as e:
            print(f"❌ Помилка MongoDB: {e}")
            return None
        
        except ValueError as e:
            print(f"❌ Помилка введення даних: {e}")
            return None
        
        except KeyboardInterrupt:
            print("\n⏹️ Операцію перервано користувачем")
            return None
        
        except EOFError:
            print("\n❌ Помилка вводу даних")
            return None
        
        except Exception as e:
            print(f"❌ Неочікувана помилка у функції {func.__name__}: {e}")
            return None
    
    return wrapper