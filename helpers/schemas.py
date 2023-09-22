"""Модуль со схемами."""

from typing import Optional, Union, List
from pydantic import BaseModel, RootModel


class BookingDatesSchema(BaseModel):
    checkin: str
    checkout: str


class GetBookingSchema(BaseModel):
    firstname: str
    lastname: str
    totalprice: Union[int, None]
    depositpaid: bool
    bookingdates: BookingDatesSchema
    additionalneeds: Optional[str] = None


class CreateBookingSchema(BaseModel):
    bookingid: int
    booking: GetBookingSchema


class BookingIds(BaseModel):
    bookingid: int


class GetBookingIds(RootModel):
    root: List[BookingIds]


class XSDSchemas:
    GET_BOOKING_SCHEMA_XSD = """<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
      <xs:element name="booking">
        <xs:complexType>
          <xs:sequence>
            <xs:element type="xs:string" name="firstname"/>
            <xs:element type="xs:string" name="lastname"/>
            <xs:element type="xs:byte" name="totalprice"/>
            <xs:element type="xs:string" name="depositpaid"/>
            <xs:element name="bookingdates">
              <xs:complexType>
                <xs:sequence>
                  <xs:element type="xs:date" name="checkin"/>
                  <xs:element type="xs:date" name="checkout"/>
                </xs:sequence>
              </xs:complexType>
            </xs:element>
            <xs:element type="xs:string" name="additionalneeds"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:schema>"""

    CREATE_BOOKING_SCHEMA_XSD = """<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
      <xs:element name="created-booking">
        <xs:complexType>
          <xs:sequence>
            <xs:element type="xs:short" name="bookingid"/>
            <xs:element name="booking">
              <xs:complexType>
                <xs:sequence>
                  <xs:element type="xs:string" name="firstname"/>
                  <xs:element type="xs:string" name="lastname"/>
                  <xs:element type="xs:byte" name="totalprice"/>
                  <xs:element type="xs:string" name="depositpaid"/>
                  <xs:element name="bookingdates">
                    <xs:complexType>
                      <xs:sequence>
                        <xs:element type="xs:date" name="checkin"/>
                        <xs:element type="xs:date" name="checkout"/>
                      </xs:sequence>
                    </xs:complexType>
                  </xs:element>
                  <xs:element type="xs:string" name="additionalneeds"/>
                </xs:sequence>
              </xs:complexType>
            </xs:element>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:schema>"""
