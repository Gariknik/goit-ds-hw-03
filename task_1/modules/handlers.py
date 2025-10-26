import datetime
import json
from .handle_exceptions import handle_exceptions


@handle_exceptions
def create_sample_cats(db):
    """
    Функція для створення тестових даних (Create)
    """
    with open('sample_cats.json', 'r', encoding='utf-8')  as f:
        data = json.load(f)
        result = db.collection.insert_many(data)
        print(f"✅ Успішно додано {len(result.inserted_ids)} тестових котів")
        return result.inserted_ids


# ЧИТАННЯ (READ) операції
@handle_exceptions
def read_all_cats(db):
    """
    Функція для виведення всіх записів із колекції
    """
    cats = list(db.collection.find())
    
    if not cats:
        print("📭 Колекція котів порожня")
        return []
    
    print("\n" + "=" * 60)
    print("📋 СПИСОК ВСІХ КОТІВ")
    print("=" * 60)
    
    for i, cat in enumerate(cats, 1):
        print(f"\n{i}. 🐱 Ім'я: {cat['name']}")
        print(f"   📅 Вік: {cat['age']} років")
        print(f"   🔧 Характеристики: {', '.join(cat['features'])}")
        print(f"   🆔 ID: {cat['_id']}")
    
    print(f"\n📊 Всього котів: {len(cats)}")
    return cats


@handle_exceptions
def read_cat_by_name(db):
    """
    Функція для пошуку кота за ім'ям
    """
    name = input("\n🔍 Введіть ім'я кота для пошуку: ").strip()
    
    if not name:
        print("❌ Будь ласка, введіть ім'я кота")
        return None
    
    cat = db.collection.find_one({"name": name})
    
    if cat:
        print("\n" + "=" * 50)
        print("✅ КІТ ЗНАЙДЕНИЙ")
        print("=" * 50)
        print(f"🐱 Ім'я: {cat['name']}")
        print(f"📅 Вік: {cat['age']} років")
        print(f"🔧 Характеристики: {', '.join(cat['features'])}")
        print(f"🆔 ID: {cat['_id']}")
        return cat
    else:
        print(f"❌ Кота з ім'ям '{name}' не знайдено")
        return None


# ОНОВЛЕННЯ (UPDATE) операції
@handle_exceptions
def update_cat_age(db):
    """
    Функція для оновлення віку кота за ім'ям
    """
    name = input("\n✏️ Введіть ім'я кота для оновлення віку: ").strip()
    
    if not name:
        print("❌ Будь ласка, введіть ім'я кота")
        return 0
    
    # Перевірка чи існує кіт
    cat = db.collection.find_one({"name": name})
    if not cat:
        print(f"❌ Кота з ім'ям '{name}' не знайдено")
        return 0
    
    print(f"📊 Поточний вік кота '{name}': {cat['age']} років")
    
    new_age = int(input("Введіть новий вік: "))
    if new_age <= 0:
        print("❌ Вік повинен бути додатнім числом")
        return 0
    
    result = db.collection.update_one(
        {"name": name},
        {
            "$set": {
                "age": new_age,
                "updated_at": datetime.datetime.now()
            }
        }
    )
    
    if result.modified_count > 0:
        print(f"✅ Вік кота '{name}' успішно оновлено до {new_age} років")
    else:
        print(f"ℹ️ Дані не змінилися (вік вже був {new_age})")
        
    return result.modified_count


@handle_exceptions
def add_cat_feature(db):
    """
    Функція для додавання нової характеристики до списку features кота за ім'ям
    """
    name = input("\n🔧 Введіть ім'я кота для додавання характеристики: ").strip()
    
    if not name:
        print("❌ Будь ласка, введіть ім'я кота")
        return 0
    
    # Перевірка чи існує кіт
    cat = db.collection.find_one({"name": name})
    if not cat:
        print(f"❌ Кота з ім'ям '{name}' не знайдено")
        return 0
    
    print(f"📋 Поточні характеристики кота '{name}': {', '.join(cat['features'])}")
    
    new_feature = input("Введіть нову характеристику: ").strip()
    
    if not new_feature:
        print("❌ Будь ласка, введіть характеристику")
        return 0
    
    result = db.collection.update_one(
        {"name": name},
        {
            "$push": {"features": new_feature},
            "$set": {"updated_at": datetime.datetime.now()}
        }
    )
    
    if result.modified_count > 0:
        print(f"✅ Характеристику '{new_feature}' успішно додано коту '{name}'")
        # Показати оновлений список характеристик
        updated_cat = db.collection.find_one({"name": name})
        print(f"📋 Оновлені характеристики: {', '.join(updated_cat['features'])}")
    else:
        print("❌ Не вдалося додати характеристику")
        
    return result.modified_count
        

# ВИДАЛЕННЯ (DELETE) операції
@handle_exceptions
def delete_cat_by_name(db):
    """
    Функція для видалення запису з колекції за ім'ям тварини
    """
    name = input("\n🗑️ Введіть ім'я кота для видалення: ").strip()
    
    if not name:
        print("❌ Будь ласка, введіть ім'я кота")
        return 0
    
    # Перевірка чи існує кіт
    cat = db.collection.find_one({"name": name})
    if not cat:
        print(f"❌ Кота з ім'ям '{name}' не знайдено")
        return 0
    
    # Показати інформацію про кота перед видаленням
    print(f"\n📋 Інформація про кота, якого буде видалено:")
    print(f"🐱 Ім'я: {cat['name']}")
    print(f"📅 Вік: {cat['age']} років")
    print(f"🔧 Характеристики: {', '.join(cat['features'])}")
    
    confirmation = input("\n⚠️ Ви впевнені, що хочете видалити цього кота? (так/ні): ").strip().lower()
    
    if confirmation in ['так', 'yes', 'y', 'т']:
        result = db.collection.delete_one({"name": name})
        
        if result.deleted_count > 0:
            print(f"✅ Кота '{name}' успішно видалено")
            return result.deleted_count
        else:
            print("❌ Не вдалося видалити кота")
            return 0
    else:
        print("❌ Видалення скасовано")
        return 0
            

@handle_exceptions
def delete_all_cats(db):
    """
    Функція для видалення всіх записів із колекції
    """
    # Підрахунок кількості записів перед видаленням
    count = db.collection.count_documents({})
    
    if count == 0:
        print("📭 Колекція вже порожня")
        return 0
    
    print(f"\n⚠️ УВАГА: Ви збираєтеся видалити ВСІХ котів ({count} записів)")
    confirmation = input("Ця дія незворотня! Введіть 'Yes' для підтвердження: ").strip().lower()
    
    if confirmation == "yes":
        result = db.collection.delete_many({})
        print(f"✅ Успішно видалено {result.deleted_count} котів")
        return result.deleted_count
    else:
        print("❌ Видалення всіх записів скасовано")
        return 0

@handle_exceptions
def display_menu():
    """
    Функція для відображення головного меню
    """
    print("\n" + "=" * 60)
    print("🐱 МЕНЕДЖЕР КОТІВ - CRUD ОПЕРАЦІЇ З MongoDB")
    print("=" * 60)
    print("1. 📋 Переглянути всіх котів (read all)")
    print("2. 🔍 Знайти кота за ім'ям (read by name)")
    print("3. ✏️ Оновити вік кота (update age)")
    print("4. 🔧 Додати характеристику коту (add feature)")
    print("5. 🗑️ Видалити кота за ім'ям (delete by name)")
    print("6. 💥 Видалити всіх котів (delete all)")
    print("7. 🎯 Створити тестові дані (create)")
    print("0. 🚪 Вихід (exit)")
    print("=" * 60)

@handle_exceptions
def close_connection(db):
    """
    Закриття підключення до MongoDB
    """
    db.client.close()
    print("🔌 Підключення до MongoDB закрито")