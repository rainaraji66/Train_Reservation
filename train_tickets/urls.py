from django.urls import path
from .views import PurchaseTicketAPI,ReceiptDetailAPI,UserBySectionAPI,RemoveUserAPI,ModifySeatAPI

urlpatterns = [
    path('purchase/', PurchaseTicketAPI.as_view(),name='purchase_ticket'),
    path('receipt/<str:email>/',ReceiptDetailAPI.as_view(),name='receipt_detail'),
    path('users/section/<str:section>/',UserBySectionAPI.as_view(),name='user_by_section'),
    path('remove/user/<str:email>/',RemoveUserAPI.as_view(),name='remove_user'),
    path('modify/seat/<str:email>/',ModifySeatAPI.as_view(),name='modify_seat'),

]
