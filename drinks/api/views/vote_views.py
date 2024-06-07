from ...models import Drink, Vote
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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