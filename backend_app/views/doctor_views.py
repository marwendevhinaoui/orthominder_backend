from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import DoctorSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Doctor
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import AccessToken

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
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_doctor(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        doctor = Doctor.objects.get(email=email)
        if doctor.password != password:
            return Response({'error': 'Invalid credentials'}, status=401)

        refresh = RefreshToken()
        refresh['doctor_id'] = doctor.id

        access_token = refresh.access_token
        access_token['doctor_id'] = doctor.id 

        return Response({
            'access': str(access_token),
            'refresh': str(refresh),
            'doctor': DoctorSerializer(doctor).data,
            'redirect':'/doctor'
        })
    except Doctor.DoesNotExist:
        return Response({'error': 'Email not exist!'}, status=404)
    



@api_view(['GET'])
def get_doctor_data(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'error': 'Authorization header missing or malformed'}, status=401)

    token_str = auth_header.split(' ')[1]

    try:
        token = AccessToken(token_str)
        doctor_id = token.get('doctor_id')

        if not doctor_id:
            raise AuthenticationFailed('doctor_id not found in token.')

        doctor = Doctor.objects.get(id=doctor_id)
        return Response(DoctorSerializer(doctor).data)

    except Exception as e:
        return Response({'error': f'Authentication failed: {str(e)}'}, status=401)