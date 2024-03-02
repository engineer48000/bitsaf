from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from .models import Transactions, AdminHistory
from .serializers import TransactionsSerializer, AdminHistorySerializer

from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
import uuid

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def createTransaction(request):
#     user = request.user
#     data = request.data

#     Transactions.objects.create(
#         # _id=data["_id"],
#         user=user
#     )
#     return Response({"message": "created successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTransaction(request):
    user = request.user
    if Transactions.objects.filter(user=user).exists():
        transactions = Transactions.objects.filter(user=user)
        deposit = 0
        withdrawal = 0
        balance = 0
        Total_earning = 0
        for transaction in transactions:
            deposit = deposit+int(transaction.deposit)
            withdrawal = withdrawal+int(transaction.withdrawal)
            Total_earning = Total_earning+int(transaction.Total_earning)
        balance = Total_earning-withdrawal
        #Total_earning = deposit
        return Response({
            "balance": str(balance),
            "deposit": str(deposit),
            "withdrawal": str(withdrawal),
            "Total_earning": str(Total_earning),
        })
    return Response({
        "balance": "0.00",
        "deposit": "0.00",
        "withdrawal": "0.00",
        "Total_earning": "0.00",
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAdminHistory(request):

    admin = AdminHistory.objects.all()
    serializer = AdminHistorySerializer(admin, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserHistory(request):
    user = request.user
    history = AdminHistory.objects.filter(username=user)
    serializer = AdminHistorySerializer(history, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adminHistory(request):
    #user = request.user

    data = request.data

    user = User.objects.get(username=data["username"])
    id = uuid.uuid1()
    ####################################
    transactions = Transactions.objects.filter(user=user)
    deposit = 0
    withdrawal = 0
    balance = 0
    Total_earning = 0
    for transaction in transactions:
        deposit = deposit+int(transaction.deposit)
        withdrawal = withdrawal+int(transaction.withdrawal)
        Total_earning = Total_earning+int(transaction.Total_earning)
    balance = Total_earning-withdrawal

    ####################################
    if int(balance) < int(data["amount"]) and data["type"] == "Debit":
        return Response({"message": "Insufficient Balance"})
    else:
        Transactions.objects.create(
            _id=id,
            user=user

        )

        admin = AdminHistory.objects.create(
            _id=id,
            username=data["username"],
            amount=data["amount"],
            type=data["type"],
            package=data["package"],
            wallet_address=data["wallet_address"]
        )
        serializer = AdminHistorySerializer(admin, many=False)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def adminHistoryUpdate(request, pk):

    data = request.data
    transaction = Transactions.objects.get(_id=pk)
    admintransaction = AdminHistory.objects.get(_id=pk)

    admintransaction.isapproved = True

    admintransaction.save()

    if admintransaction.type == "Credit":
        transaction.deposit = admintransaction.amount
        transaction.Total_earning = admintransaction.amount

        # transaction.Total_earning = transaction.Total_earning + \
        #     admintransaction.amount

        # transaction.balance = transaction.balance +\
        #     admintransaction.amount
        transaction.save()

    elif admintransaction.type == "Debit":
        transaction.withdrawal = admintransaction.amount

        # transaction.balance = transaction.balance - \
        #     admintransaction.amount

        transaction.save()

    return Response({"message": "updated successfully"})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def listUser(request):
    transact = Transactions.objects.all()
    users = User.objects.all()
    data = []
    for user in users:
        user_datas = User.objects.filter(username=user)
        for user_data in user_datas:

            transactions = Transactions.objects.filter(user=user_data)

            deposit = 0
            withdrawal = 0
           # balance = 0
            Total_earning = 0
            for transaction in transactions:

                deposit = deposit+int(transaction.deposit)
                withdrawal = withdrawal+int(transaction.withdrawal)
                Total_earning = Total_earning+int(transaction.Total_earning)
            balance = Total_earning-withdrawal

            fil = {"userinfo": {"username": user_data.username, "id": user_data.uuid, "is_staff": user_data.is_staff, "firstname": user_data.firstname,
                                "referral": user_data.referral, "date_joined": user_data.date_joined,
                                "deposit": deposit, "withdrawal": withdrawal, "Total_earning": Total_earning, "balance": balance}}
            data.append(fil)
    print(data)

    user_serializer = UserSerializer(users, many=True)
    transact_serializer = TransactionsSerializer(transact, many=True)

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def fundUser(request):
    data = request.data

    user = User.objects.get(username=data["username"])

    Transactions.objects.create(
        _id=uuid.uuid1(),
        user=user,
        Total_earning=data["amount"]

    )

    return Response({"message": "updated successfully"})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete(request, pk):

    #user = request.user

    query = User.objects.get(username=pk)
    query.delete()
    return Response("Deleted!")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    profile = User.objects.get(username=user)

    serializer = UserSerializer(profile, many=False)
    return Response(serializer.data)
