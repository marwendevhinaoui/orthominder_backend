from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError



@api_view(['POST'])
def blacklisting(request):
    try:
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
        
    except Exception as e:
        return Response("Error blacklisting")
    


@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            response = Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK)
            response.delete_cookie('refresh')
            return response
        else:
            return Response(
            {'error': str(e)})
        
    except TokenError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response(
            {'error': 'An error occurred during logout'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def refresh_token(request):

    refresh_token_value = request.COOKIES.get('refresh')
    if not refresh_token_value:
        return Response({'error': 'Refresh token not found'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token_value)
        access_token = str(refresh.access_token)
        return Response({'access': access_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Try login again!'}, status=status.HTTP_401_UNAUTHORIZED)

