from pymongo import MongoClient
from pymongo.server_api import ServerApi
from modules import create_sample_cats, read_all_cats, read_cat_by_name, update_cat_age, add_cat_feature, delete_cat_by_name, delete_all_cats, display_menu, close_connection

def main():
    """
    Головна функція програми
    """
    client = MongoClient(
        "mongodb+srv://goitlearn:gsxe1Y5DB8LDo0q7@cluster0.3jjni7d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        server_api=ServerApi('1')
    )

    db = client.cats
    
    try:
        while True:
            display_menu()
            
            choice = input("\n🎯 Виберіть опцію: ").strip()
            match choice:
                case '1' | "read all": read_all_cats(db)
                case '2' | "read by name": read_cat_by_name(db)
                case '3' | "update age": update_cat_age(db)
                case '4' | "add feature": add_cat_feature(db)
                case '5' | "delete by name": delete_cat_by_name(db)    
                case '6' | "delete all": delete_all_cats(db)
                case '7' | "create": create_sample_cats(db)
                case '0' | "exit":
                    print("👋 До побачення!")
                    break
                case _: print("❌ Некоректний вибір. Будь ласка, виберіть опцію від 0 до 7")
            
            input("\n⏎ Натисніть Enter для продовження...")
            
    except KeyboardInterrupt:
        print("\n👋 Програму перервано користувачем")
    except Exception as e:
        print(f"❌ Сталася неочікувана помилка: {e}")
    finally:
        close_connection(db)

if __name__ == "__main__":
    main()