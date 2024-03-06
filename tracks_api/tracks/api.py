from typing import List, Optional
from ninja import File, NinjaAPI, UploadedFile
from tracks.models import Track
from tracks.schema import DeleteResponseSchema, TrackSchema, NotFoundSchema, TrackSchemaResponse

#https://localhost:8000/api/tracks
api = NinjaAPI()



@api.get("/tracks", response=List[TrackSchemaResponse], tags=['track'], description='List all tracks')
def tracks(request, title: Optional[str] = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()

@api.get('/tracks/{track_id}',
        response={200: TrackSchemaResponse, 404: NotFoundSchema},
        tags=['track'], description='Get track by id')
def track(request, track_id: int):    
    try:
        track = Track.objects.get(pk=track_id)
        return track
    except Track.DoesNotExist as error:
        return 404, { 'message': 'Track does not exists'}

@api.post('/tracks', response={201: TrackSchemaResponse},
          tags=['track'], description='Create a track')
def create_track(request, track: TrackSchema):
    track = Track.objects.create(**track.dict()) 
    return track

@api.put('/tracks/{track_id}',
         response={200: TrackSchemaResponse, 404: NotFoundSchema},
         tags=['track'], description='Update track by track ID')
def change_track(request, track_id: int, data: TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attribute, value in data.dict().items():
            setattr(track, attribute, value)
        track.save()
        return 200, track
    except Track.DoesNotExist as error:
        return 404, { 'message': 'Track does not exists'}
    
@api.delete('/tracks/{track_id}',
            response={200: DeleteResponseSchema, 404: NotFoundSchema},
            tags=['track'], description='Delete track by track ID')
def delete_track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        track.delete()
        return 200, { 'message': 'Track deleted successfully'}
    except Track.DoesNotExist as error:
        return 404, { 'message': 'Track does not exists'}


@api.post('/upload', url_name='upload',
          tags=['upload'], description='Returns the name and data of an upload file')
def upload(request, file: UploadedFile = File(...)):     
    data = file.read().decode()
    return {
        'name': file.name,
        'data': data
    }
