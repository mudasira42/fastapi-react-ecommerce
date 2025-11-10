"""Seed script to populate the database with sample products"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime, timezone
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

products = [
    {
        "id": str(uuid.uuid4()),
        "name": "Wireless Bluetooth Headphones",
        "description": "Premium noise-canceling headphones with 40-hour battery life and superior sound quality.",
        "price": 199.99,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop",
        "stock": 50,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Smart Watch Series 7",
        "description": "Advanced fitness tracker with heart rate monitor, GPS, and water resistance.",
        "price": 399.99,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop",
        "stock": 30,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Vintage Leather Backpack",
        "description": "Handcrafted genuine leather backpack with laptop compartment and multiple pockets.",
        "price": 149.99,
        "category": "Fashion",
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
        "stock": 25,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Organic Cotton T-Shirt",
        "description": "Comfortable and eco-friendly t-shirt made from 100% organic cotton.",
        "price": 29.99,
        "category": "Fashion",
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop",
        "stock": 100,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Professional Camera Lens",
        "description": "50mm f/1.8 prime lens with ultra-fast autofocus for stunning portraits.",
        "price": 299.99,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1606406308915-8cdb5d6d0d0f?w=500&h=500&fit=crop",
        "stock": 15,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Yoga Mat Premium",
        "description": "Non-slip eco-friendly yoga mat with extra cushioning for comfort.",
        "price": 49.99,
        "category": "Sports",
        "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500&h=500&fit=crop",
        "stock": 60,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Stainless Steel Water Bottle",
        "description": "Insulated bottle that keeps drinks cold for 24 hours or hot for 12 hours.",
        "price": 34.99,
        "category": "Sports",
        "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&h=500&fit=crop",
        "stock": 80,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Designer Sunglasses",
        "description": "UV protection sunglasses with polarized lenses and modern frame design.",
        "price": 159.99,
        "category": "Fashion",
        "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&h=500&fit=crop",
        "stock": 40,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Mechanical Keyboard RGB",
        "description": "Gaming keyboard with customizable RGB lighting and tactile switches.",
        "price": 129.99,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=500&h=500&fit=crop",
        "stock": 35,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Running Shoes Pro",
        "description": "Lightweight running shoes with advanced cushioning and breathable mesh.",
        "price": 119.99,
        "category": "Sports",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
        "stock": 45,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Minimalist Desk Lamp",
        "description": "LED desk lamp with adjustable brightness and modern aesthetic design.",
        "price": 79.99,
        "category": "Home",
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500&h=500&fit=crop",
        "stock": 55,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Portable Bluetooth Speaker",
        "description": "Waterproof speaker with 360-degree sound and 20-hour battery life.",
        "price": 89.99,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&h=500&fit=crop",
        "stock": 70,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

async def seed_database():
    try:
        # Clear existing products
        await db.products.delete_many({})
        print("Cleared existing products")
        
        # Insert new products
        result = await db.products.insert_many(products)
        print(f"Successfully seeded {len(result.inserted_ids)} products")
        
        # Display seeded products
        for product in products:
            print(f"  - {product['name']} (${product['price']})")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Starting database seed...")
    asyncio.run(seed_database())
    print("Database seeding complete!")