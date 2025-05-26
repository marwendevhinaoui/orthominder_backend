from datetime import date
import random
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orthominder_backend import settings
from ..serializers import AlignerSerializers, AppointementSerializers, PatientSerializer, DoctorSerializer
from ..models import Patient, Appointement, Doctor
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import jwt


def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=length))

@api_view(['POST'])
def register_patient(request):
    if request.method == 'POST':
        refresh_token = request.COOKIES.get('refresh')  

        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=400)
        try:

            generated_password = generate_random_password()
            data = request.data.copy()
            data['password'] = generated_password
            print('generated_password ----> ', generated_password)
            serializer = PatientSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        'message': 'Patient registered successfully!',
                        'user': PatientSerializer(user).data,
                    },
                    status=200
                )
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': 'Error creating patient please check data!'}, status=500)
            
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)    
    


@api_view(['POST'])
def login_patient(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        if not email and not password:
            return Response({'error': 'Please input email and password'}, status=500)
        try:
            patient = Patient.objects.get(email=email)
            if not patient.check_password(password):
                return Response({'error': 'Invalid password!'}, status=401)
            
            else:
                refresh = RefreshToken()

                access_token = refresh.access_token


                response = Response({
                    'message':'Welcome back!',
                    'access': str(access_token),
                    'refresh': str(refresh),
                    'patient': PatientSerializer(patient).data,
                })

                return response
        except Patient.DoesNotExist:
            return Response({'error': 'Invalid credentials!'}, status=404)

        
@api_view(['GET'])
def get_appointements_by_patient_id(request, patient_id):
    if request.method == 'GET':
        refresh_token = request.COOKIES.get('refresh')  
        auth_header = request.headers.get('Authorization')
        access_token = None
        if not refresh_token:
            return Response({'error': 'No refresh token provided!'}, status=400)
        
        if auth_header:
            if(auth_header.startswith('Bearer ')):
                access_token = auth_header.split(' ')[1]
            else:
                return Response({'error': 'No refresh token provided!'}, status=400)        
        try:
            access_token = RefreshToken(refresh_token)
            refresh = RefreshToken(refresh_token)
            appointements = Appointement.objects.filter(patient_id=patient_id)
            serializer = AppointementSerializers(appointements, many=True)
            return Response(serializer.data, status=200)       
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)




@api_view(['GET'])
def get_appointements_details(request, appointement_id):
    if request.method == 'GET':
        refresh_token = request.COOKIES.get('refresh')  
        auth_header = request.headers.get('Authorization')
        access_token = None
        if not refresh_token:
            return Response({'error': 'No refresh token provided!'}, status=400)
        
        if auth_header:
            if(auth_header.startswith('Bearer ')):
                access_token = auth_header.split(' ')[1]
            else:
                return Response({'error': 'No refresh token provided!'}, status=400)        
        try:
            access_token = RefreshToken(refresh_token)
            refresh = RefreshToken(refresh_token)
            appointement = Appointement.objects.filter(id=appointement_id)
            serializer = AppointementSerializers(appointement, many=True)
            return Response(serializer.data, status=200)       
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)




@api_view(['POST'])
def add_appointement(request):
    if request.method == 'POST':
        refresh_token = request.COOKIES.get('refresh')  

        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=400)
        try:
            refresh = RefreshToken(refresh_token)    # to check refresh token valid or not          
            data = request.data.copy()
            data['is_paid'] = False

            serializer = AppointementSerializers(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        'message': 'Appointement registered successfully!',
                        'appointement': AppointementSerializers(user).data,
                    },
                    status=200
                )
            return Response(serializer.errors, status=400)

            
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)
        




@api_view(['GET'])
def get_patient_by_id(request, patient_id):
    if request.method == 'GET':
        refresh_token = request.COOKIES.get('refresh')  
        auth_header = request.headers.get('Authorization')

        access_token = None 

        if not refresh_token:
            if auth_header and auth_header.startswith('Bearer '):
                access_token = auth_header.split(' ')[1]
            else:
                return Response({'error': 'No refresh token or access token provided!'}, status=404)
        else:
            access_token = refresh_token 

        try:
            patient = Patient.objects.get(id=patient_id)

            patient_serializer = PatientSerializer(patient)

            doctor_name = patient.doctor.full_name  

            response_data = patient_serializer.data
            response_data['doctor_name'] = doctor_name

            return Response(response_data, status=200)  
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)
        

@api_view(['POST'])
def add_aligner(request):
    if request.method == 'POST':
        refresh_token = request.COOKIES.get('refresh')  

        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=400)
        try:
            refresh = RefreshToken(refresh_token)    # to check refresh token valid or not          
            data = request.data.copy()

            serializer = AlignerSerializers(data=data)
            if serializer.is_valid():
                aligner = serializer.save()
                return Response({
                'message': 'Aligner registered successfully!',
                'aligner': AlignerSerializers(aligner).data
            }, status=200)
            return Response(serializer.errors, status=400)

            
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)
        


@api_view(['GET'])
def get_appointements_details_by_patient(request, patient_id):
    refresh_token = request.COOKIES.get('refresh')
    refresh_token = request.COOKIES.get('refresh')  
    auth_header = request.headers.get('Authorization')

    access_token = None 

    if not refresh_token:
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
        else:
            return Response({'error': 'No refresh token or access token provided!'}, status=404)
    else:
        access_token = refresh_token 
    try:
        refresh = RefreshToken(refresh_token)

        # Update out dated appointments for patient_id
        Appointement.objects.filter(
            status='IN PROGRESS',
            next_appointemnt_day__lte=date.today(),
            patient_id=patient_id
        ).update(status='COMPLETED')

        # Retrieve only IN PROGRESS appointments for the patient
        appointments = Appointement.objects.filter(
            status='IN PROGRESS',
            patient_id=patient_id
        ).first()
        serializer = AppointementSerializers(appointments)
        return Response(serializer.data, status=200)

    except jwt.ExpiredSignatureError:
        return Response({'error': 'Refresh token expired'}, status=401)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token'}, status=401)