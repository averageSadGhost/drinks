from .models import Drink, Vote
from .serializer import DrinkSerializer, LoginSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def drink_list(request, format=None):
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response({'drinks': serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def drink_detail(request, id, format=None):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data)
    
    else:
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user != drink.author_id and not request.user.is_staff:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'PUT':
            serializer = DrinkSerializer(drink, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'PATCH':
            serializer = DrinkSerializer(drink, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            drink.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    if not request.user.is_staff:
        return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)
    user = request.user

    # Check if the user already downvoted
    if Vote.objects.filter(user=user, drink=drink, is_upvote=False).exists():
        # If the user already downvoted, remove the downvote
        Vote.objects.filter(user=user, drink=drink, is_upvote=False).delete()
        drink.vote_count += 1  # Increment vote count as the downvote is removed
        drink.save()
        return Response({'message': 'Downvote removed successfully'}, status=200)
    elif not Vote.objects.filter(user=user, drink=drink).exists():
        # If the user hasn't voted on this drink yet, downvote it
        Vote.objects.create(user=user, drink=drink, is_upvote=False)
        drink.vote_count -= 1  # Decrement vote count as a downvote is added
        drink.save()
        return Response({'message': 'Drink downvoted successfully'}, status=200)
    else:
        return Response({'message': 'You have already voted on this drink'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)
    user = request.user

    # Check if the user already downvoted
    if Vote.objects.filter(user=user, drink=drink, is_upvote=False).exists():
        # If the user already downvoted, remove the downvote
        Vote.objects.filter(user=user, drink=drink, is_upvote=False).delete()
        drink.vote_count -= 1  # Decrement vote count
        drink.save()
        return Response({'message': 'Downvote removed successfully'}, status=200)
    elif not Vote.objects.filter(user=user, drink=drink).exists():
        # If the user hasn't voted on this drink yet, downvote it
        Vote.objects.create(user=user, drink=drink, is_upvote=False)
        drink.vote_count -= 1  # Decrement vote count
        drink.save()
        return Response({'message': 'Drink downvoted successfully'}, status=200)
    else:
        return Response({'message': 'You have already voted on this drink'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)
    user = request.user

    # Check if the user already downvoted
    if Vote.objects.filter(user=user, drink=drink, is_upvote=False).exists():
        # If the user already downvoted, remove the downvote
        Vote.objects.filter(user=user, drink=drink, is_upvote=False).delete()
        drink.vote_count -= 1  # Decrement vote count
        drink.save()
        return Response({'message': 'Downvote removed successfully'}, status=200)
    elif not Vote.objects.filter(user=user, drink=drink, is_upvote=True).exists():
        # If the user hasn't upvoted before, downvote the drink
        Vote.objects.create(user=user, drink=drink, is_upvote=False)
        drink.vote_count -= 1  # Decrement vote count
        drink.save()
        return Response({'message': 'Drink downvoted successfully'}, status=200)
    else:
        # If the user previously upvoted, change the vote to downvote
        vote = Vote.objects.get(user=user, drink=drink, is_upvote=True)
        vote.is_upvote = False
        vote.save()
        drink.vote_count -= 2  # Adjust vote count (remove previous upvote and add downvote)
        drink.save()
        return Response({'message': 'Vote changed to downvote'}, status=200)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def downvote(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)
    user = request.user

    # Check if the user already downvoted
    if Vote.objects.filter(user=user, drink=drink, is_upvote=False).exists():
        # If the user already downvoted, remove the downvote
        Vote.objects.filter(user=user, drink=drink, is_upvote=False).delete()
        drink.vote_count += 1  # Increment vote count (since downvote is removed)
        drink.save()
        return Response({'message': 'Downvote removed successfully'}, status=200)
    elif not Vote.objects.filter(user=user, drink=drink, is_upvote=True).exists():
        # If the user hasn't upvoted before, downvote the drink
        Vote.objects.create(user=user, drink=drink, is_upvote=False)
        drink.vote_count -= 1  # Decrement vote count
        drink.save()
        return Response({'message': 'Drink downvoted successfully'}, status=200)
    else:
        # If the user previously upvoted, change the vote to downvote
        vote = Vote.objects.get(user=user, drink=drink, is_upvote=True)
        vote.is_upvote = False
        vote.save()
        drink.vote_count -= 2  # Adjust vote count (remove previous upvote and add downvote)
        drink.save()
        return Response({'message': 'Vote changed to downvote'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)
    user = request.user

    # Check if the user already upvoted
    if Vote.objects.filter(user=user, drink=drink, is_upvote=True).exists():
        # If the user already upvoted, remove the upvote
        Vote.objects.filter(user=user, drink=drink, is_upvote=True).delete()
        drink.vote_count -= 1  # Decrement vote count
        drink.save()
        return Response({'message': 'Upvote removed successfully'}, status=200)
    elif not Vote.objects.filter(user=user, drink=drink, is_upvote=False).exists():
        # If the user hasn't downvoted before, upvote the drink
        Vote.objects.create(user=user, drink=drink, is_upvote=True)
        drink.vote_count += 1  # Increment vote count
        drink.save()
        return Response({'message': 'Drink upvoted successfully'}, status=200)
    else:
        # If the user previously downvoted, change the vote to upvote
        vote = Vote.objects.get(user=user, drink=drink, is_upvote=False)
        vote.is_upvote = True
        vote.save()
        drink.vote_count += 2  # Adjust vote count (remove previous downvote and add upvote)
        drink.save()
        return Response({'message': 'Vote changed to upvote'}, status=200)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_votes_for_post(request, drink_id):
    user = request.user
    drink = get_object_or_404(Drink, id=drink_id)
    
    # Check if the user is staff or their ID matches the author ID of the drink
    if not (user.is_staff or user.id == drink.author_id.id):
        return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    votes = Vote.objects.filter(drink=drink)
    vote_data = [{'user': vote.user.username, 'vote': 'Upvote' if vote.is_upvote else 'Downvote'} for vote in votes]
    return Response({'votes': vote_data})