from django.shortcuts import render
from django.http import JsonResponse


from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics

import jwt , datetime
from decouple import config

from .serializers import UserSerializer , TourSerializer , RatingSerializer , ChatMessageSerializer , BookingSerializer , CommentSerializer
from .models import User , Tour , Rating , ChatMessage , Booking , comment , ContactUs

# from gpt4_openai import GPT4OpenAI
from jwt import ExpiredSignatureError, DecodeError
import json
from rest_framework_simplejwt.authentication import JWTAuthentication



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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60000),
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
        token1 =   request.COOKIES.get('jwt')
        token = request.headers.get('Authorization').split(' ')[1]
        
        
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
        
        token1 =   request.COOKIES.get('jwt')
        token = request.headers.get('Authorization').split(' ')[1]
        
        
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
        token1 =   request.COOKIES.get('jwt')
        token = request.headers.get('Authorization').split(' ')[1]
        
        
        
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
    

    
class ChatBotAPIView(APIView):
    def post(self, request):
        my_token = config('Token')
        # llm = GPT4OpenAI(token=my_token, model='gpt-3')
        # message = request.data['content']
        # response = llm(message)
        response = 'Hello'


        return Response({'message': response})


class BookingView(APIView):
    def post(self , request , pk):
        token1 =   request.COOKIES.get('jwt')
        token = request.headers.get('Authorization').split(' ')[1]
        

        if not token:
            raise AuthenticationFailed('Unauthenticated! ')
        
        try:
            payload = jwt.decode(token , 'secret' , algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Failes deoding ')
        
        user = User.objects.filter(id=payload['id']).first()
        tour = Tour.objects.get(id=pk)
        #create a booking model    
        #set all the other attributes 
        fname =   request.data['first_name']
        lname =   request.data['last_name']
        email =   request.data['email']
        phone =   request.data['phone_number']
        numberOfPeople =   request.data['group_size']
        totalPrice =  request.data['totalPrice']
        date = request.data["selected_date"]
        #convert date into datetime object 
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        
        Book = Booking.objects.create(user=user , tour=tour , fname=fname , lname=lname , email=email ,  numberOfPeople=numberOfPeople , 
                                      totalPrice=totalPrice , date=date , phone = phone )


        Book.save()

        return Response({
            'message': 'success'
        })
    


class CommentView(APIView):
    def get(self , request , pk):
        tour = Tour.objects.get(id=pk)
        comments = comment.objects.filter(tour=tour)
        serializer = CommentSerializer(comments , many=True)
        
        response = []
        for i in serializer.data:
            user = User.objects.get(id=i['user'])
            response.append({
                'user': user.name,
                'comment': i['comment']
            })
        
        return Response(response)
    
    def post(self , request , pk):
        token1 =  request.COOKIES.get('jwt')
        token = request.headers.get('Authorization').split(' ')[1]
        

        if not token:
            raise AuthenticationFailed('Unauthenticated! ')
        
        try:
            payload = jwt.decode(token , 'secret' , algorithms=['HS256'])
        except ExpiredSignatureError:
            raise AuthenticationFailed('Token expired!', code=401)
        except DecodeError:
            raise AuthenticationFailed('Invalid token!', code=401)

        
        user = User.objects.filter(id=payload['id']).first()
        tour = Tour.objects.get(id=pk)
        #create a booking model    
        #set all the other attributes 
        content =   request.data['comment']
        print(content)
        comment.objects.create(user=user , tour=tour , comment=content).save()
        return Response({
            'message': 'success'
        })
    
class Contact(APIView):
    def post(self , request):
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')
        ContactUs.objects.create(name=name, email=email, message=message)
        return Response({'message': 'success'})
