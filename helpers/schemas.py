"""Модуль со схемами."""


GET_BOOKING_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'firstname': {'type': 'string'},
        'lastname': {'type': 'string'},
        'totalprice': {'type': 'integer'},
        'depositpaid': {'type': 'boolean'},
        'bookingdates': {
            'type': 'object',
            'properties': {
                'checkin': {'type': 'string'},
                'checkout': {'type': 'string'}},
            'required': ['checkin', 'checkout']},
        'additionalneeds': {'type': 'string'}},
    'required': ['firstname', 'lastname', 'totalprice', 'depositpaid',
                         'bookingdates', 'additionalneeds']}

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

CREATE_BOOKING_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'bookingid': {'type': 'integer'},
        'booking': GET_BOOKING_SCHEMA},
    'required': ['bookingid', 'booking']}

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


GET_BOOKING_IDS_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'array',
    'items': [
        {'type': 'object',
         'properties': {
             'bookingid': {'type': 'integer'}},
         'required': ['bookingid']}]}
