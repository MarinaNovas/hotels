from datetime import date

from sqlalchemy import insert, select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    apartments_count = (
        select(BookingsOrm.room_id, func.count('*').label('apartments_booked'))
        .select_from(BookingsOrm)
        .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
        .group_by(BookingsOrm.room_id)
        .cte(name='apartments_count')
    )

    apartments_left_table = (
        select(
            RoomsOrm.id.label('room_id'),
            RoomsOrm.quantity,
            (RoomsOrm.quantity - func.coalesce(apartments_count.c.apartments_booked, 0)).label(
                'apartment_left'
            ),
        )
        .select_from(RoomsOrm)
        .outerjoin(apartments_count, RoomsOrm.id == apartments_count.c.room_id)
        .cte(name='apartments_left_table')
    )

    get_rooms_by_hotel = select(RoomsOrm.id).select_from(RoomsOrm)

    if hotel_id is not None:
        get_rooms_by_hotel = get_rooms_by_hotel.filter_by(hotel_id=hotel_id)

    get_rooms_by_hotel = get_rooms_by_hotel.subquery(name='get_rooms_by_hotel')

    query = (
        select(apartments_left_table.c.room_id)
        .select_from(apartments_left_table)
        .filter(
            apartments_left_table.c.apartment_left > 0,
            apartments_left_table.c.room_id.in_(get_rooms_by_hotel),
        )
    )
    return query
