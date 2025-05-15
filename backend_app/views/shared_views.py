from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError




@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        try:
            refresh_token = request.COOKIES.get('refresh')

            if refresh_token:
                response = Response(
                {'message': 'Successfully logged out'},
                status=200)
                response.delete_cookie('refresh')
                return response
            else:
                return Response(
                {'error': str(e)})

        except TokenError as e:
            return Response(
                {'error': str(e)},
                status=400)

        except Exception as e:
            return Response(
                {'error': 'An error occurred during logout'},
                status=500)


@api_view(["POST"])
def refresh_token(request):
    if request.method == "POST":

        refresh_token_value = request.COOKIES.get("refresh")
        if not refresh_token_value:
            return Response({"error": "Refresh token not found"}, status=400)

        try:
            refresh = RefreshToken(refresh_token_value)
            access_token = str(refresh.access_token)
            return Response({"access": access_token, "redirection":"/"+refresh['user_type']}, status=200)
        except Exception as e:
            return Response({"error": "Try login again!"}, status=401)
