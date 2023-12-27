from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','POST'])
def drink_list(request,format=None):

    if request.method == 'GET':
        #get all the drinks from db
        #serialize them
        #return json
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        # return JsonResponse({'drinks':serializer.data}, safe=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        #get the userinput data
        #deserialize it
        #add it to the db and return it to the user
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        


@api_view(['GET','PUT','DELETE'])
def drink_detail(request,id,format=None):
    
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
   
    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)