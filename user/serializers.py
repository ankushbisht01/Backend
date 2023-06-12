from rest_framework import serializers
from .models import User , Tour , Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email' , 'name', 'password')

        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self , validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            if password is not None:
                user.set_password(password)
            user.save()
            return user
        

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('id', 'title' , 'description', 'price', 'image1', 'image2', 'dayDescription', 'location', 'duration')

    def create(self , validated_data):
        tour = Tour(**validated_data)
        tour.save()
        return tour

   
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user' , 'tour', 'rating')

    def create(self , validated_data):
        rating = Rating(**validated_data)
        rating.save()
        return rating