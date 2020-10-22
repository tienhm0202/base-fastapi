from zogutils.secret import unique_id


def get_db_id() -> str:
    return unique_id(16, "ID_")


def get_secret() -> str:
    return unique_id(32, "KEY_")
