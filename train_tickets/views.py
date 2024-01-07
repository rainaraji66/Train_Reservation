from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import User,Ticket_Model
from .serializers import TicketSerializer,UserSerializer,NestedSerializer

class PurchaseTicketAPI(generics.CreateAPIView):
    queryset = Ticket_Model.objects.all()
    serializer_class = TicketSerializer

    def get(self,request,*args,**kwargs):
        purchases =Ticket_Model.objects.all()
        serializer_purchase = TicketSerializer(purchases,many=True)
        return Response(serializer_purchase.data)
    
    def post(self,request,*args,**kwargs):
        seat_number = request.data.get('seat')
        seat_exists = Ticket_Model.objects.filter(seat=seat_number).exists()
        if seat_exists:
            return Response({'message': f"Seat {seat_number} is already booked."},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class ReceiptDetailAPI(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    lookup_field = 'user__email'

    def get_object(self):
        user_email = self.kwargs.get('email')

        try:
            user = User.objects.get(email=user_email)
            ticket = Ticket_Model.objects.get(user__email=user_email)
            return ticket
        except (Ticket_Model.DoesNotExist):
            return 'nill'
            
    
class UserBySectionAPI(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        section = self.kwargs.get('section')
        return Ticket_Model.objects.filter(section=section)
    
class RemoveUserAPI(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  
            self.perform_destroy(instance)
            return Response("User deleted successfully", status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)
 

class ModifySeatAPI(generics.UpdateAPIView):
    queryset = Ticket_Model.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'user__email'

    def update(self,request,*args,**kwargs):
        
        user_email = self.kwargs.get('email')
    
        user = User.objects.get(email=user_email)
        ticket = Ticket_Model.objects.get(user__email=user_email)
            
        new_seat_number = request.data.get('seat')
        seat_exists = Ticket_Model.objects.filter(seat=new_seat_number).exists()
        if seat_exists:
            return Response({'message': f"Seat {new_seat_number} is already booked."},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            ticket.seat = new_seat_number
            ticket.save()
            serializer=self.get_serializer(ticket,data=request.data)
            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data)
    
        