from django.urls import path

from . import views

urlpatterns = [
    # path('transact/', views.createTransaction, name="create-transaction"),
    path('transaction/', views.getTransaction, name="transaction"),
    path('histories/', views.getAdminHistory, name="admin-history"),

    path('history/', views.getUserHistory, name="user-history"),

    path('admin/', views.adminHistory, name="admin"),

    path('admin/<str:pk>/', views.adminHistoryUpdate, name="admin-update"),
    path('users/', views.listUser, name="users"),
    path('fund/', views.fundUser, name="fund"),
    path('user/delete/<str:pk>/', views.delete, name="delete"),
    path('profile/', views.profile, name="profile"),
]
