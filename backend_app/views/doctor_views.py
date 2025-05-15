from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from ..serializers import DoctorSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Doctor
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from rest_framework_simplejwt.authentication import JWTAuthentication



@api_view(['POST'])
def register_doctor(request):
    if request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'Doctor registered successfully',
                    'user': DoctorSerializer(user).data
                },
                status=200
            )
        return Response(serializer.errors, status=400)



@api_view(['POST'])
def login_doctor(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            doctor = Doctor.objects.get(email=email)
            if not doctor.check_password(password):
                return Response({'error': 'Invalid password!'}, status=401)
            
            else:
                refresh = RefreshToken()
                refresh['doctor_id'] = doctor.id
                refresh['user_type'] = 'doctor'
                print(refresh['user_type'],'-----------------------------------------')
                access_token = refresh.access_token


                response = Response({
                    'access': str(access_token),
                    'refresh': str(refresh),
                    'doctor': DoctorSerializer(doctor).data,
                    'redirect':'/doctor',
                })
                
                response.set_cookie(
                    key='refresh',
                    value=str(refresh),
                    httponly=True, 
                    secure=not settings.DEBUG,  
                    samesite='Lax' if settings.DEBUG else 'Strict', 
                    max_age=60 * 60 * 24,  
                    path='/'
                )

                return response
        except Doctor.DoesNotExist:
            return Response({'error': 'Invalid credentials!'}, status=404)
    


@api_view(['GET'])
def get_doctor_data(request):
    if request.method == 'GET':

        refresh_token = request.COOKIES.get('refresh')  
        
        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=400)
        
        try:
            refresh = RefreshToken(refresh_token)
            doctor_id = refresh['doctor_id']
            if not doctor_id:
                return Response('doctor_id not found in token.')
 
            
            doctor = Doctor.objects.get(id=doctor_id)
            return Response(DoctorSerializer(doctor).data, status=200)
        
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)
        



@api_view(['GET'])
def get_doctor_id_from_refresh(request):
    if request.method == 'GET':

        refresh_token = request.COOKIES.get('refresh')  
        
        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=400)
        
        try:
            refresh = RefreshToken(refresh_token)
            
            doctor_id = refresh['doctor_id']
            
            return Response({'doctor_id': doctor_id}, status=200)
        
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)
        



def blacklist_ref_tokens_with_user(user):
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        try:
            BlacklistedToken.objects.get_or_create(token=token)
        except:
            Response({'error':'error deleting token'})


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_doctor(request, doctor_id):

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        blacklist_ref_tokens_with_user(doctor)
        doctor.delete()
        return Response({"message": "Doctor deleted and tokens blacklisted successfully"}, status=200)
    
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=404)
    
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)