from django.shortcuts import render
from django.http.response import JsonResponse
from.models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
# Create your views here.
#without REST framework no model query 
def no_rest_no_model(request):
    guests = [

        {
            'id': 1,
            "Name" : "Hanane",
            "phone_number": 632821112,
        },
        {
            'id': 2,
            'name': "Dhiyaa",
            'phone_number' : 7792521566,
        }
    ]
    return JsonResponse (guests, safe=False)

#2 no_rst_from_model
def no_rest_from_model (request):
    data = Guest.objects.all()
    response ={
        'guests':list(data.values('name', 'phone_number'))
    }
    return JsonResponse(response)

#GET
#POST
#pk query ==GGET
#PUT = update
#delete
#3 function based views 
#3.1 GET POST 
@api_view(['GET', 'POST'])
def FBV_List(request):
    #Get 
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many =True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Respponse (serializer.data, status = status.HTTP_400_BAD_REQUEST)
#3-2 GET PUT DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get (pk = pk)
    except:
        return Response(status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    #put
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Respponse (serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    #Delete
    if request.method == 'DELETE':
        guest.delete()
        return Respponse (status.HTTP_204_NO_CONTENT)

#CBV class based views
    #4.1 List and creat == GET and POST
class CBV_List(APIView):
    def get(self, request):
        guest =Guest.objects.all()
        serializer= GuestSerializer(guest, many=True)
        return Response(serializer.data)
    def post (self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
    
#4.2 CVB GET POST DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk= pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guest =self.get_object(pk)
        serializer= GuestSerializer(guest)
        return Response(serializer.data)
    def put (self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
    def delete (self, request, pk ):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

#MIXIN 
    #5.1 mixins list 
class mixins_list( mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView,):
    queryset = Guest.objects.all()
    serializer_class =GuestSerializer

    def get (self, request):
        return self.list(request)
    def post (self, request):
        return self.create(request)
    
#5.2 mixins get put updat
class mixins_pk( mixins.UpdateModelMixin, mixins.DestroyModelMixin,mixins.RetrieveModelMixin, generics.GenericAPIView,
):
    queryset = Guest.objects.all()
    serializer_class =GuestSerializer
    def get (self, request, pk):
        return self.retrieve(request)
    def put (self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

#6 GENERICS 
#6.1 GET POST 
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class = GuestSerializer

#6.2 GET PUT DELETE
class generics_pk (generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
     
#7.1 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class = GuestSerializer
class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']
class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class = ReservationSerializer

#8 find a movie 
@api_view(['Get'])
def find_movie (request):
    movies = Movie.objects.filter(
        movie = request.data ['movie'],
        hall = request.data ['hall'],
    )
    serializer= MovieSerializer(movies, many=True)
    return Response(serializer.data)

#9 MAke reservation              
@api_view(['POST'])
def new_reservation(request):
    movie= Movie.objects.get(
        movie = request.data ['Movie'],
        hall = request.data ['hall'],
    )
    guest= Guest()
    guest.name = request.data['name']
    guest.phone_number = request.data['phone_number']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie =movie
    reservation.save()
    return Response( status=status.HTTP_201_CREATED ) 