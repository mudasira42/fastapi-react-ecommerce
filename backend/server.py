from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# ============ MODELS ============

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    image: str
    stock: int = 100
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CartItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    product_id: str
    quantity: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: str
    product: Product
    quantity: int

# ============ AUTH UTILITIES ============

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_doc = await db.users.find_one({"id": user_id}, {"_id": 0})
    if user_doc is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    return User(**user_doc)

# ============ AUTH ROUTES ============

@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    # Check if user exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password)
    )
    
    user_dict = user.model_dump()
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    await db.users.insert_one(user_dict)
    
    # Create token
    token = create_access_token({"sub": user.id})
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(id=user.id, email=user.email, name=user.name)
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user_doc = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    user = User(**user_doc)
    
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.id})
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(id=user.id, email=user.email, name=user.name)
    )

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, email=current_user.email, name=current_user.name)

# ============ PRODUCT ROUTES ============

@api_router.get("/products", response_model=List[Product])
async def get_products(search: Optional[str] = None, category: Optional[str] = None):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if category:
        query["category"] = category
    
    products = await db.products.find(query, {"_id": 0}).to_list(1000)
    
    for product in products:
        if isinstance(product.get('created_at'), str):
            product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if isinstance(product.get('created_at'), str):
        product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return Product(**product)

# ============ CART ROUTES ============

@api_router.get("/cart", response_model=List[CartItemResponse])
async def get_cart(current_user: User = Depends(get_current_user)):
    cart_items = await db.cart.find({"user_id": current_user.id}, {"_id": 0}).to_list(1000)
    
    result = []
    for item in cart_items:
        product = await db.products.find_one({"id": item["product_id"]}, {"_id": 0})
        if product:
            if isinstance(product.get('created_at'), str):
                product['created_at'] = datetime.fromisoformat(product['created_at'])
            result.append(CartItemResponse(
                id=item["id"],
                product=Product(**product),
                quantity=item["quantity"]
            ))
    
    return result

@api_router.post("/cart", response_model=CartItemResponse)
async def add_to_cart(item_data: CartItemCreate, current_user: User = Depends(get_current_user)):
    # Check if product exists
    product = await db.products.find_one({"id": item_data.product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item already in cart
    existing = await db.cart.find_one({
        "user_id": current_user.id,
        "product_id": item_data.product_id
    })
    
    if existing:
        # Update quantity
        new_quantity = existing["quantity"] + item_data.quantity
        await db.cart.update_one(
            {"id": existing["id"]},
            {"$set": {"quantity": new_quantity}}
        )
        cart_item = CartItem(**existing)
        cart_item.quantity = new_quantity
    else:
        # Create new cart item
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        cart_dict = cart_item.model_dump()
        cart_dict['created_at'] = cart_dict['created_at'].isoformat()
        await db.cart.insert_one(cart_dict)
    
    if isinstance(product.get('created_at'), str):
        product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return CartItemResponse(
        id=cart_item.id,
        product=Product(**product),
        quantity=cart_item.quantity
    )

@api_router.patch("/cart/{cart_id}", response_model=CartItemResponse)
async def update_cart_item(cart_id: str, update_data: CartItemUpdate, current_user: User = Depends(get_current_user)):
    cart_item = await db.cart.find_one({"id": cart_id, "user_id": current_user.id})
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    await db.cart.update_one(
        {"id": cart_id},
        {"$set": {"quantity": update_data.quantity}}
    )
    
    product = await db.products.find_one({"id": cart_item["product_id"]}, {"_id": 0})
    if isinstance(product.get('created_at'), str):
        product['created_at'] = datetime.fromisoformat(product['created_at'])
    
    return CartItemResponse(
        id=cart_id,
        product=Product(**product),
        quantity=update_data.quantity
    )

@api_router.delete("/cart/{cart_id}")
async def delete_cart_item(cart_id: str, current_user: User = Depends(get_current_user)):
    result = await db.cart.delete_one({"id": cart_id, "user_id": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@api_router.post("/cart/sync")
async def sync_cart(guest_cart: List[CartItemCreate], current_user: User = Depends(get_current_user)):
    """Merge guest cart with user cart after login"""
    for item in guest_cart:
        # Check if product exists
        product = await db.products.find_one({"id": item.product_id})
        if not product:
            continue
        
        # Check if already in user cart
        existing = await db.cart.find_one({
            "user_id": current_user.id,
            "product_id": item.product_id
        })
        
        if existing:
            # Add quantities
            new_quantity = existing["quantity"] + item.quantity
            await db.cart.update_one(
                {"id": existing["id"]},
                {"$set": {"quantity": new_quantity}}
            )
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            cart_dict = cart_item.model_dump()
            cart_dict['created_at'] = cart_dict['created_at'].isoformat()
            await db.cart.insert_one(cart_dict)
    
    return {"message": "Cart synced successfully"}

# Root route
@api_router.get("/")
async def root():
    return {"message": "E-Commerce API"}

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()