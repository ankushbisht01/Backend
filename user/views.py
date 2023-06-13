from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


import jwt , datetime

from .serializers import UserSerializer , TourSerializer , RatingSerializer
from .models import User , Tour , Rating

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView):
    def post(self , request ):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email , password = password).first()

        if user is None:
            raise AuthenticationFailed('Login Failed! ')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token =  jwt.encode(payload ,  'secret' , algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt' , value=token , httponly=True)
        response.data = {
            'jwt': token
        }
        return response
        

class UserView(APIView):
    def get(self , request ):
        token =   request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated! ')
        
        try:
            payload = jwt.decode(token , 'secret' , algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! ')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)


        return  Response( serializer.data)
    
class LogoutView(APIView):
    def post(self , request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    

class  TourView(APIView):
    def get(self , request):
        tours = Tour.objects.all()
        serializer = TourSerializer(tours , many=True)
        return Response(serializer.data)
    
   
    def post(self , request):
        serializer = TourSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    
class SingleTourView(APIView):
    def get(self , request , pk):
        tour = Tour.objects.get(id=pk)
        serializer = TourSerializer(tour , many=False)
        return Response(serializer.data)
    
    def put(self , request , pk):
        tour = Tour.objects.get(id=pk)
        serializer = TourSerializer(instance=tour , data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self , request , pk):
        tour = Tour.objects.get(id=pk)
        tour.delete()
        return Response('Tour Deleted')
    

class RatingView(APIView):
    def get(self , request , pk):
        print(request.headers)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            # Extract the token from the header
            token = auth_header.split(' ')[1]
        
        if not token:
            raise AuthenticationFailed('Unauthenticated! ')

        try:
            payload = jwt.decode(token , 'secret' , algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('FAiled ! ')
        
        user = User.objects.filter(id=payload['id']).first()
        tour = Tour.objects.get(id=pk)
        ratings = Rating.objects.filter(user=user , tour = tour)
        serializer = RatingSerializer(ratings , many=True)
        
        return Response(serializer.data)
    
    def post(self , request , pk):
        #save the rating for the tour with pk 
        token =  request.COOKIES.get('jwt')
        
        
        if not token:
            raise AuthenticationFailed('Unauthenticated! ')
        
        try:
            payload = jwt.decode(token , 'secret' , algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Failes deoding ')
        
        user = User.objects.filter(id=payload['id']).first()
        tour = Tour.objects.get(id=pk)
        data = {
            'user': user.id,
            'tour': tour.id,
            'rating': request.data['rating'],
        }
        #check if there is a rating for this user and this tour delete it 
        rating = Rating.objects.filter(user=user , tour = tour)
        if rating is not None:
            rating.delete()
        serializer = RatingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    

    
    
