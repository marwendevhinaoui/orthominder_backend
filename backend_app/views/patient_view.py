import random
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import PatientSerializer
from ..models import Patient
from rest_framework_simplejwt.tokens import RefreshToken

def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))

@api_view(['POST'])
def register_patient(request):
    if request.method == 'POST':
        generated_password = generate_random_password()
        data = request.data.copy()
        data['password'] = generated_password
        print(generated_password)
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'Patient registered successfully',
                    'user': PatientSerializer(user).data,
                },
                status=200
            )
        return Response(serializer.errors, status=400)
    


@api_view(['POST'])
def login_patient(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required!'}, status=400)

        try:
            patient = Patient.objects.get(email=email)
            if patient.check_password(password):
                refresh = RefreshToken.for_user(patient)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': patient.id,
                    'email': patient.email,
                    'full_name': patient.full_name,
                })
            else:
                return Response({'error': 'Invalid password!'}, status=401)

        except Patient.DoesNotExist:
            return Response({'error': 'Invalid credentials!'}, status=404)