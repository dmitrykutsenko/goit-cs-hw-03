from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure, PyMongoError
import json

def create_database():
    client = None
    try:
        # 🔧 Вибери правильний URI:
        # Для локального Docker:
        client = MongoClient("mongodb://localhost:27017/")
        # Для Atlas заміни рядок на свій справжній URI з консолі Atlas:
        # client = MongoClient("mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority")

        client.admin.command("ping")
        print("✅ Успішне підключення до MongoDB")

        db = client["cats_db"]
        cats_collection = db["cats"]

        cat_document = {
            "_id": ObjectId("60d24b783733b1ae668d4a77"),
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"]
        }

        # Перевірка на дублікати
        if not cats_collection.find_one({"_id": cat_document["_id"]}):
            result = cats_collection.insert_one(cat_document)
            print(f"🐾 Документ вставлено з _id: {result.inserted_id}")
        else:
            print("ℹ️ Документ з таким _id вже існує, вставка пропущена.")

        # Вивести документ у правильному форматі
        cat = cats_collection.find_one({"_id": cat_document["_id"]})
        if cat:
            ordered = {
                "_id": cat["_id"],
                "name": cat["name"],
                "age": cat["age"],
                "features": cat["features"]
            }
            print("\n=== Поточний стан документа ===")
            print(json.dumps(ordered, indent=4, default=str, ensure_ascii=False))

    except ConnectionFailure:
        print("❌ Не вдалося підключитися до MongoDB.")
    except PyMongoError as e:
        print(f"⚠️ Помилка при роботі з MongoDB: {e}")
    finally:
        if client is not None:
            client.close()
            print("🔒 З'єднання закрито")

if __name__ == "__main__":
    create_database()
