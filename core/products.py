def build(
        name: str,
        calories: float,
        proteins: float,
        carbs: float,
        fats: float
    ) -> dict:

    values_name = ["name", "calories", "proteins", "carbs", "fats"]
    values = [name, calories, proteins, carbs, fats]
    for value_name, value in zip(values_name, values):
        if value is None:
            raise ValueError(f"error: {value_name} is None")
        
    if name.strip() == "":
        raise ValueError(f"error: name is empty")
    
    return {
        "name_product": name,
        "product_calories": calories,
        "product_proteins": proteins,
        "product_carbs": carbs,
        "product_fats": fats
    }