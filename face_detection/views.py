from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import cv2

@api_view(['POST'])
def face_detection(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided'}, status=400)

    image_file = request.FILES['image']
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return Response({'error': 'Invalid image'}, status=400)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

   
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,     
        minNeighbors=6,     
        minSize=(60, 60)     
    )

    face_list = []
    for (x, y, w, h) in faces:
        if w > 50 and h > 50:
            face_list.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h)})

    return Response({
        "face_detected": len(face_list) > 0,
        "faces": face_list
    })
