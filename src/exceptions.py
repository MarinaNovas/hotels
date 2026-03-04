
class BookingException(Exception):
    detail = "Упс"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(BookingException):
    detail = "Объект не найден"

class AllRoomsAreBookedException(BookingException):
    detail = "Нет свободных номеров"