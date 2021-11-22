def ResponseModel(data: dict = {}, message: str = ""):
    return {"data": data, "success": True, "message": message}


def ErrorModel(data: dict = {}, message: str = ""):
    return {"data": data, "success": False, "message": message}
