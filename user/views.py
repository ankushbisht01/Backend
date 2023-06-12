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
        token =  request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated! ')

        try:
            payload = jwt.decode(token , 'secret' , algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! ')
        
        user = User.objects.filter(id=payload['id']).first()

        ratings = Rating.objects.filter(user=user , pk = pk)
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
            raise AuthenticationFailed('Unauthenticated! ')
        
        user = User.objects.filter(id=payload['id']).first()
        tour = Tour.objects.get(id=pk)
        #create an object of rating
        rating = Rating.objects.create(user=user , tour=tour , **request.data)
        rating.save()
        serializer = RatingSerializer(rating , many=False)
        return Response(serializer.data)
    

    
    
