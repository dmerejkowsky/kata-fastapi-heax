# fastapi-hexa

The code given as a starting point uses a simple layered architecture.

The goal is to introduce an hexagonal architecture, so that business rules are easier to write and test.

## API


* `GET http://localhost:8081/data_for_train/<train_name>`
This will return a json document with information about the seats that this train has. The document you get back will look for example like this:

```json
{
  "seats": {
    "1A": {
      "booking_reference": "abc123def",
      "seat_number": "1",
      "coach": "A"
    },
    "2A": {
      "booking_reference": "",
      "seat_number": "2",
      "coach": "A"
    }
  }
}
```

Here, seat "1A" is booked, but seat "2A" is free.

* `POST http://localhost:8081/book`
The body should look like:

```json
{
  "train": "express_2000",
  "seats": ["1A", "2A"],
  "booking_reference": "abc123def"
}
```

Note that the server will prevent you from booking a seat that is already reserved with another booking reference, by returning a 409 conflict status.
It is however OK to try and book the same seat with twice with the same booking reference.
