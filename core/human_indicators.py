def calculate_daily_calories(
    age: int,
    weight_kg: float,
    height_cm: float,
    gender: str,
    activity_level: float
) -> int:
    values_name = ["age", "weight_kg", "height_cm", "gender", "activity_level"]
    values = [age, weight_kg, height_cm, gender, activity_level]
    for value_name, value in zip(values_name, values):
        if value is None:
            raise ValueError(f"error: {value_name} is None")
        if isinstance(value, bool):
            raise ValueError(f"error: {value_name} is bool")
        if value_name == "gender":
            if isinstance(value, str): 
                if value.strip() == "":
                    raise ValueError(f"error: {value_name} is empty")
            else:
                raise ValueError(f"error: {value_name} is not str")
            if not (value == "male" or value == "female"):
                raise ValueError((f"error: {value_name} must be 'male' or 'female'"))
        else:
            if value_name == "age":
                if not isinstance(value, (int)):
                    raise ValueError(f"error: {value_name} is not int")
            else:
                if not isinstance(value, (float, int)):
                    raise ValueError(f"error: {value_name} is not number")
                else: 
                    if  value < 0:
                        raise ValueError(f"error: {value_name} is not positive")
    if age > 0:
        if gender == "male":
            calorieslimit = (10 * weight_kg + 6.25 * height_cm - 5 * age + 5) * activity_level
        else:
            calorieslimit = (10 * weight_kg + 6.25 * height_cm - 5 * age - 161) * activity_level
    else:
        raise ValueError("error: age < 0")
    return round(calorieslimit)
"""
from core.human_indicators import calculate_daily_calories
calculate_daily_calories(21,95,192,"male",1.725)
"""