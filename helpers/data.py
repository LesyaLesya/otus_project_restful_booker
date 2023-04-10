from dataclasses import dataclass, field


@dataclass
class BookingDates:
    checkin: str = None
    checkout: str = None


@dataclass
class BookingData:
    """Dataclass booking."""

    firstname: str = None
    lastname: str = None
    totalprice: int = None
    depositpaid: bool = None
    bookingdates: BookingDates = field(default_factory=dict)
    additionalneeds: str = None
