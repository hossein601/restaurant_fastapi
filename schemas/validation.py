@validator("") #
def validate_if_float(cls, value):
    if isinstance(value, float):
        # do validation here
    return value