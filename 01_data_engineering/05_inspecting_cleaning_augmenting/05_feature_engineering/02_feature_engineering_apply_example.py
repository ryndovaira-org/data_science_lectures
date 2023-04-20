import pandas as pd

df = pd.DataFrame(
    {
        "user_name": pd.Series(
            [
                "Mr Oleg",
                "Mr Oleg",
                "Mr Pete",
                "Mr Pete",
                "Mrs Elena",
                "Mr Viktor",
                "Mr Anton",
                "Mr Anton",
                "Mrs Alex",
                "Mrs Alex",
            ],
            dtype="string",
        ),
        "user_country": pd.Series(
            [
                "Russia",
                "Russia",
                "USA",
                "USA",
                "India",
                "Germany",
                "Russia",
                "Russia",
                "Germany",
                "Germany",
            ],
            dtype="category",
        ),
        "user_age": pd.Series([25, 25, 66, 66, 36, 15, 48, 48, 86, 86], dtype="int8"),
        "user_rating": pd.Series(
            [
                "5 star",
                "5 star",
                "3 star",
                "3 star",
                "1 star",
                "2 star",
                "5 star",
                "5 star",
                "4 star",
                "4 star",
            ],
            dtype=pd.CategoricalDtype(
                categories=["1 star", "2 star", "3 star", "4 star", "5 star"],
                ordered=True,
            ),
        ),
        "user_complaints": pd.Series(
            [
                "1 point",
                "1 point",
                "4 point",
                "4 point",
                "5 point",
                "5 point",
                "1 point",
                "1 point",
                "2 point",
                "2 point",
            ],
            dtype=pd.CategoricalDtype(
                categories=["5 point", "4 point", "3 point", "2 point", "1 point"],
                ordered=True,
            ),
        ),
        "item_title": pd.Series(
            [
                "toy",
                "Beautiful Cat",
                "Car",
                "TV",
                "Toys",
                "Television",
                "Smartphone",
                "Dog",
                "Kitty",
                "Soft TOY",
            ],
            dtype="string",
        ),
        "item_price_rub": pd.Series(
            [
                300.50,
                5000,
                800_500,
                19_999.99,
                678.23,
                10_999.99,
                10_000,
                1_000,
                100,
                4999.99,
            ],
            dtype="float",
        ),
        "item_width_cm": pd.Series(
            [20, 80, 300, 200, 100, 150, 10, 100, 15, 150], dtype="float"
        ),
        "item_height_cm": pd.Series(
            [30, 50, 200, 100, 80, 80, 15, 90, 10, 150], dtype="float"
        ),
        "item_description": pd.Series(
            [
                "Little kids love things bright and colorful. They are easily attracted to them. Colorful Learning Blocks set to make your little one playtime educational yet fun. ",
                "Kids and adults love cats! This animal is stunning. It likes play with all people in living room or bedroom!",
                "Comfortable seats. Updated interior displays. Beautifully finished interior.",
                "Operating System: Android (Google Assistant & Chromecast in-built). You can enjoy a stunning viewing experience in your living room or bedroom.",
                "Blocks for the creative minds. Perfect for the growing kids. Contains alphabet blocks, 4 animal puzzles and a set of blocks. ",
                "Operating System: Android (Google Assistant & Chromecast in-built). The Gamma Engine, along with the noise reduction feature, delivers lifelike visuals with dynamic contrast and anti-aliasing to enhance your viewing experience.",
                "If you like Android, the Samsung Galaxy S21 Ultra is incredibly good.",
                "This dog is a perfect choice! The dog for free adoption. Perfect for the adults.",
                "Kittens for free adoption. Perfect for the adults. If you like cats, a kitten is an incredibly good choice.",
                "Kids and adults love soft toys! It can beautify interior and perfect for the growing kids.",
            ],
            dtype="string",
        ),
        "item_tags": pd.Series(
            [
                "children, beautiful, good_condition",
                "animal, cat, beautiful",
                "beautiful, good_condition",
                "good_condition",
                "children, animal",
                "good_condition",
                "good_condition",
                "animal, dog",
                "animal",
                "children, good_condition",
            ],
            dtype="string",
        ),
        "item_age_month": pd.Series([1, 0, 6, 12, 3, 4, 18, 1, 9, 8], dtype="int16"),
        "item_color": pd.Series(
            [
                "red",
                "blue",
                "rainbow",
                "white",
                "red",
                "white",
                "rainbow",
                "white",
                "white",
                "blue",
            ],
            dtype="category",
        ),
        "open_date_time": pd.Series(
            [
                "10.10.2020 18:25",
                "20.12.2020 16:36",
                "06.01.2021 10:14",
                "07.04.2021 23:25",
                "26.11.2020 06:17",
                "18.05.2020 15:15",
                "10.03.2021 09:08",
                "25.02.2020 04:57",
                "28.08.2020 12:54",
                "10.09.2019 23:25",
            ],
            dtype="datetime64[ns]",
        ),
        "status": pd.Series(
            [
                "sold out",
                "for sale",
                "for sale",
                "for sale",
                "sold out",
                "sold out",
                "for sale",
                "for sale",
                "sold out",
                "for sale",
            ],
            dtype="string",
        ),
    }
)


def apply_fun(x):
    tmp = pd.Series(True, index=[f"tag_{tag}" for tag in x.split(", ")])
    return tmp


item_tags_df = df.item_tags.apply(apply_fun)
print(item_tags_df)
