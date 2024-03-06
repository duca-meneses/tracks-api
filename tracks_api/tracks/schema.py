from datetime import datetime
from ninja import Schema

class TrackSchema(Schema):
    title: str
    artist: str
    duration: float
    last_play: datetime


class TrackSchemaResponse(TrackSchema):
    id: int

class NotFoundSchema(Schema):
    message: str

class DeleteResponseSchema(NotFoundSchema):
    ...