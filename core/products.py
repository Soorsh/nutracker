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
        if isinstance(value, bool):
            raise ValueError(f"error: {value_name} is bool")
        if value_name == "name":
            if isinstance(value, str): 
                if value.strip() == "":
                    raise ValueError(f"error: {value_name} is empty")
            else:
                raise ValueError(f"error: {value_name} is not str")
        else:
            if not isinstance(value, (float, int)):
                raise ValueError(f"error: {value_name} is not number")
            else: 
                if  value < 0:
                    raise ValueError(f"error: {value_name} is not positive")

    return {
        "product_name": name,
        "product_calories": calories,
        "product_proteins": proteins,
        "product_carbs": carbs,
        "product_fats": fats
    }