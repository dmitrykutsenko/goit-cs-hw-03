from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

def get_collection():
    """
    Підключаємося до локального MongoDB (Docker) та повертаємо колекцію 'cats' у базі 'cats_db'.
    """
    try:
        client = MongoClient("mongodb://localhost:27017/")
        client.admin.command("ping")  # перевірка з'єднання
        db = client["cats_db"]
        return db["cats"], client
    except ConnectionFailure:
        print("❌ Не вдалося підключитися до MongoDB. Перевірте Docker контейнер.")
        return None, None
    except PyMongoError as e:
        print(f"⚠️ Помилка при роботі з MongoDB: {e}")
        return None, None


# ---------------- READ ----------------
def read_all_cats():
    """Виводить усі записи з колекції 'cats'."""
    cats_collection, client = get_collection()
    if cats_collection is not None:
        try:
            empty = True
            for cat in cats_collection.find():
                print(cat)
                empty = False
            if empty:
                print("ℹ️ Колекція порожня.")
        except PyMongoError as e:
            print(f"⚠️ Помилка при читанні: {e}")
        finally:
            client.close()


def read_cat_by_name(name: str):
    """Виводить інформацію про кота за його ім'ям."""
    cats_collection, client = get_collection()
    if cats_collection is not None:
        try:
            cat = cats_collection.find_one({"name": name})
            if cat:
                print(cat)
            else:
                print(f"❌ Кота з ім'ям '{name}' не знайдено.")
        except PyMongoError as e:
            print(f"⚠️ Помилка при читанні: {e}")
        finally:
            client.close()


# ---------------- UPDATE ----------------
def update_cat_age(name: str, new_age: int):
    """Оновлює вік кота за його ім'ям."""
    cats_collection, client = get_collection()
    if cats_collection is not None:
        try:
            result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
            if result.matched_count == 0:
                print(f"❌ Кота з ім'ям '{name}' не знайдено.")
            elif result.modified_count > 0:
                print(f"✅ Вік кота '{name}' оновлено до {new_age}.")
            else:
                print("ℹ️ Дані були такими самими; змін не внесено.")
        except PyMongoError as e:
            print(f"⚠️ Помилка при оновленні: {e}")
        finally:
            client.close()


def add_feature_to_cat(name: str, feature: str):
    """Додає нову характеристику до списку features кота за його ім'ям."""
    cats_collection, client = get_collection()
    if cats_collection is not None:
        try:
            result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
            if result.matched_count == 0:
                print(f"❌ Кота з ім'ям '{name}' не знайдено.")
            elif result.modified_count > 0:
                print(f"✅ Характеристика '{feature}' додана коту '{name}'.")
            else:
                print("ℹ️ Можливо характеристика вже існує або змін не внесено.")
        except PyMongoError as e:
            print(f"⚠️ Помилка при оновленні: {e}")
        finally:
            client.close()


# ---------------- DELETE ----------------
def delete_cat_by_name(name: str):
    """Видаляє запис про кота за його ім'ям."""
    cats_collection, client = get_collection()
    if cats_collection is not None:
        try:
            result = cats_collection.delete_one({"name": name})
            if result.deleted_count > 0:
                print(f"🗑️ Кота '{name}' видалено.")
            else:
                print(f"❌ Кота з ім'ям '{name}' не знайдено.")
        except PyMongoError as e:
            print(f"⚠️ Помилка при видаленні: {e}")
        finally:
            client.close()


def delete_all_cats():
    """Видаляє всі записи з колекції 'cats'."""
    cats_collection, client = get_collection()
    if cats_collection is not None:
        try:
            result = cats_collection.delete_many({})
            print(f"🗑️ Видалено {result.deleted_count} записів.")
        except PyMongoError as e:
            print(f"⚠️ Помилка при видаленні: {e}")
        finally:
            client.close()


# ---------------- MENU ----------------
def menu():
    print("🐱 Програма запущена. Нижче меню:")
    while True:
        print("\n=== МЕНЮ ===")
        print("1. Вивести усіх котів")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота")
        print("4. Додати характеристику коту")
        print("5. Видалити кота за ім'ям")
        print("6. Видалити усіх котів")
        print("0. Вихід")

        try:
            choice = input("Оберіть дію (введіть число і натисніть Enter): ").strip()
        except EOFError:
            print("⚠️ Не вдалося прочитати ввід. Спробуйте ще раз.")
            continue

        if choice == "1":
            read_all_cats()
        elif choice == "2":
            name = input("Введіть ім'я кота: ").strip()
            read_cat_by_name(name)
        elif choice == "3":
            name = input("Введіть ім'я кота: ").strip()
            age_str = input("Введіть новий вік (ціле число): ").strip()
            try:
                new_age = int(age_str)
            except ValueError:
                print("❌ Некоректне число. Спробуйте ще раз.")
                continue
            update_cat_age(name, new_age)
        elif choice == "4":
            name = input("Введіть ім'я кота: ").strip()
            feature = input("Введіть нову характеристику: ").strip()
            if not feature:
                print("❌ Порожня характеристика. Спробуйте ще раз.")
                continue
            add_feature_to_cat(name, feature)
        elif choice == "5":
            name = input("Введіть ім'я кота: ").strip()
            delete_cat_by_name(name)
        elif choice == "6":
            confirm = input("Підтвердіть очищення (наберіть YES): ").strip().upper()
            if confirm == "YES":
                delete_all_cats()
            else:
                print("ℹ️ Скасовано.")
        elif choice == "0":
            print("👋 Вихід з програми.")
            break
        else:
            print("❌ Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    # ключове
    menu()
