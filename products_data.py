import random

from product import Product

brands = [
    "Apple",
    "Samsung",
    "Google",
    "Dell",
    "Lenovo",
    "Sony",
    "Microsoft",
    "Nintendo",
    "Amazon",
    "Fitbit",
    "Garmin",
    "Meta",
    "Razer",
    "ASUS",
    "Bose",
    "Nikon",
    "Canon",
    "GoPro",
    "Anker",
    "Logitech",
    "Western Digital",
    "Seagate",
    "HP",
]

product_types = [
    "iPhone",
    "Galaxy S",
    "Pixel",
    "MacBook Pro",
    "XPS",
    "ThinkPad",
    "AirPods Pro",
    "Galaxy Buds",
    "WH-1000XM",
    "PlayStation",
    "Xbox Series",
    "Switch",
    "Kindle Paperwhite",
    "Echo Dot",
    "Nest Hub",
    "Charge",
    "Watch Series",
    "Forerunner",
    "Quest",
    "Blade",
    "Zephyrus",
    "SoundLink Revolve",
    "Tab S",
    "iPad Air",
    "Surface Pro",
    "D",
    "EOS Rebel",
    "HERO",
    "PowerCore",
    "MX Master",
    "Huntsman Elite",
    "970 EVO Plus",
    "My Passport",
    "Expansion",
    "iMac",
    "Envy Desktop",
    "IdeaCentre",
]

categories = [
    "Smartphone, Electronics",
    "Laptop, Electronics",
    "Audio, Accessories",
    "Gaming, Electronics",
    "E-Reader, Electronics",
    "Smart Home, Electronics",
    "Wearable, Fitness",
    "VR, Gaming",
    "Gaming Laptop, Electronics",
    "Tablet, Electronics",
    "Camera, Electronics",
    "Accessories, Electronics",
    "Storage, Electronics",
    "Desktop, Electronics",
]

price_ranges = {
    "Smartphone": (300, 1200),
    "Laptop": (500, 3000),
    "Audio": (50, 500),
    "Gaming": (200, 800),
    "E-Reader": (80, 300),
    "Smart Home": (30, 200),
    "Wearable": (100, 600),
    "VR": (200, 600),
    "Gaming Laptop": (1000, 3000),
    "Tablet": (150, 1200),
    "Camera": (200, 1500),
    "Accessories": (20, 300),
    "Storage": (40, 300),
    "Desktop": (400, 2000),
}

# Suffixes for more realistic model names
suffixes = [
    "",
    "Pro",
    "Max",
    "Ultra",
    "Plus",
    "Mini",
    "Lite",
    "SE",
    "Elite",
    "Edge",
    "Advance",
    "Prime",
]


def get_price(category):
    main_cat = category.split(",")[0].strip()
    low, high = price_ranges.get(main_cat, (50, 1000))
    return random.randint(low, high)


def get_rating():
    return random.choices([3, 4, 5], weights=[1, 5, 7])[0]


def make_product_name(brand, product_type):
    # Extract base type and number if present
    base = product_type.rstrip("0123456789 ")
    number = "".join(filter(str.isdigit, product_type))
    if not number:
        number = str(random.randint(1, 30))
    suffix = random.choice(suffixes)
    # Compose name
    name = f"{brand} {base.strip()} {number}"
    if suffix:
        name += f" {suffix}"
    return name.strip()


def generate_products(count: int = 500):
    products = []
    for _ in range(count):
        brand = random.choice(brands)
        product_type = random.choice(product_types)
        category = random.choice(categories)
        price = get_price(category)
        rating = get_rating()
        name = make_product_name(brand, product_type)
        products.append(
            Product(
                name=name,
                price=price,
                brand=brand,
                category=category,
                rating=rating,
            )
        )
    return products


def main():

    # Example: print first 5 products
    products = generate_products()
    for p in products[:5]:
        print(p)


if __name__ == "__main__":
    main()
