from dataclasses import dataclass
from functools import cached_property


@dataclass
class Product:
    name: str
    price: int
    brand: str
    category: str
    rating: int

    @cached_property
    def categories(self) -> set[str]:
        return {cat.strip() for cat in self.category.split(",")}


PRODUCTS = (
    Product(
        name="iPhone 14",
        price=999,
        brand="Apple",
        category="Smartphone, Electronics",
        rating=5,
    ),
    Product(
        name="Galaxy S23",
        price=899,
        brand="Samsung",
        category="Smartphone, Electronics",
        rating=4,
    ),
    Product(
        name="Pixel 7",
        price=599,
        brand="Google",
        category="Smartphone, Electronics",
        rating=4,
    ),
    Product(
        name="MacBook Pro 16",
        price=2499,
        brand="Apple",
        category="Laptop, Electronics",
        rating=5,
    ),
    Product(
        name="Dell XPS 13",
        price=1399,
        brand="Dell",
        category="Laptop, Electronics",
        rating=4,
    ),
    Product(
        name="ThinkPad X1 Carbon",
        price=1499,
        brand="Lenovo",
        category="Laptop, Electronics",
        rating=4,
    ),
    Product(
        name="AirPods Pro",
        price=249,
        brand="Apple",
        category="Audio, Accessories",
        rating=5,
    ),
    Product(
        name="Galaxy Buds 2",
        price=149,
        brand="Samsung",
        category="Audio, Accessories",
        rating=4,
    ),
    Product(
        name="Sony WH-1000XM4",
        price=349,
        brand="Sony",
        category="Audio, Accessories",
        rating=5,
    ),
    Product(
        name="PlayStation 5",
        price=499,
        brand="Sony",
        category="Gaming, Electronics",
        rating=5,
    ),
    Product(
        name="Xbox Series X",
        price=499,
        brand="Microsoft",
        category="Gaming, Electronics",
        rating=4,
    ),
    Product(
        name="Nintendo Switch",
        price=299,
        brand="Nintendo",
        category="Gaming, Electronics",
        rating=4,
    ),
    Product(
        name="Kindle Paperwhite",
        price=139,
        brand="Amazon",
        category="E-Reader, Electronics",
        rating=5,
    ),
    Product(
        name="Echo Dot",
        price=49,
        brand="Amazon",
        category="Smart Home, Electronics",
        rating=4,
    ),
    Product(
        name="Nest Hub",
        price=99,
        brand="Google",
        category="Smart Home, Electronics",
        rating=4,
    ),
    Product(
        name="Fitbit Charge 5",
        price=179,
        brand="Fitbit",
        category="Wearable, Fitness",
        rating=4,
    ),
    Product(
        name="Apple Watch Series 8",
        price=399,
        brand="Apple",
        category="Wearable, Fitness",
        rating=5,
    ),
    Product(
        name="Garmin Forerunner 245",
        price=299,
        brand="Garmin",
        category="Wearable, Fitness",
        rating=4,
    ),
    Product(
        name="Oculus Quest 2",
        price=299,
        brand="Meta",
        category="VR, Gaming",
        rating=5,
    ),
    Product(
        name="Razer Blade 15",
        price=1999,
        brand="Razer",
        category="Gaming Laptop, Electronics",
        rating=4,
    ),
    Product(
        name="ASUS ROG Zephyrus G14",
        price=1499,
        brand="ASUS",
        category="Gaming Laptop, Electronics",
        rating=4,
    ),
    Product(
        name="Bose SoundLink Revolve",
        price=199,
        brand="Bose",
        category="Audio, Accessories",
        rating=5,
    ),
    Product(
        name="Samsung Galaxy Tab S8",
        price=699,
        brand="Samsung",
        category="Tablet, Electronics",
        rating=4,
    ),
    Product(
        name="iPad Air",
        price=599,
        brand="Apple",
        category="Tablet, Electronics",
        rating=5,
    ),
    Product(
        name="Microsoft Surface Pro 8",
        price=1099,
        brand="Microsoft",
        category="Tablet, Electronics",
        rating=4,
    ),
    Product(
        name="Nikon D3500",
        price=499,
        brand="Nikon",
        category="Camera, Electronics",
        rating=4,
    ),
    Product(
        name="Canon EOS Rebel T7",
        price=449,
        brand="Canon",
        category="Camera, Electronics",
        rating=4,
    ),
    Product(
        name="GoPro HERO10",
        price=399,
        brand="GoPro",
        category="Camera, Electronics",
        rating=5,
    ),
    Product(
        name="Anker PowerCore 20100",
        price=39,
        brand="Anker",
        category="Accessories, Electronics",
        rating=4,
    ),
    Product(
        name="Logitech MX Master 3",
        price=99,
        brand="Logitech",
        category="Accessories, Electronics",
        rating=5,
    ),
    Product(
        name="Razer Huntsman Elite",
        price=199,
        brand="Razer",
        category="Accessories, Electronics",
        rating=4,
    ),
    Product(
        name="Samsung 970 EVO Plus 1TB",
        price=129,
        brand="Samsung",
        category="Storage, Electronics",
        rating=5,
    ),
    Product(
        name="Western Digital My Passport 2TB",
        price=69,
        brand="Western Digital",
        category="Storage, Electronics",
        rating=4,
    ),
    Product(
        name="Seagate Expansion 2TB",
        price=59,
        brand="Seagate",
        category="Storage, Electronics",
        rating=4,
    ),
    Product(
        name="Apple iMac 24",
        price=1299,
        brand="Apple",
        category="Desktop, Electronics",
        rating=5,
    ),
    Product(
        name="HP Envy Desktop",
        price=899,
        brand="HP",
        category="Desktop, Electronics",
        rating=4,
    ),
    Product(
        name="Lenovo IdeaCentre 3",
        price=699,
        brand="Lenovo",
        category="Desktop, Electronics",
        rating=4,
    ),
)

BRANDS = frozenset(product.brand for product in PRODUCTS)
CATEGORIES = frozenset(
    cat.strip() for product in PRODUCTS for cat in product.category.split(",")
)

MIN_PRICE = min(product.price for product in PRODUCTS)
MIN_PRICE = MIN_PRICE // 10 * 10
MAX_PRICE = max(product.price for product in PRODUCTS)
MAX_PRICE = (MAX_PRICE + 9) // 10 * 10
