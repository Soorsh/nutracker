def build(name: str, calories: float, proteins: float, carbs: float, fats: float) -> dict:
    if name is None or calories is None or proteins is None or carbs is None or fats is None:
        raise ValueError("error: data null")
    else:
        return {
            "name_product": name,
            "product_calories": calories,
            "product_proteins": proteins,
            "product_carbs": carbs,
            "product_fats": fats
        }