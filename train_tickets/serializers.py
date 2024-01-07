from rest_framework import serializers
from .models import User,Ticket_Model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class NestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket_Model
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    nested_field = NestedSerializer(read_only=True)

    class Meta:
        model = Ticket_Model
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)  
        ticket = Ticket_Model.objects.create(user=user, **validated_data)
        return ticket
    
    
