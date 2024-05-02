from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Intern

@api_view(['Post'])
def create_interns_from_json(request, json_file_path=None):
    if json_file_path is None:
        json_file_path = request.query_params.get('json_file_path')

    if json_file_path:
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                interns_data = data.get('interns', []) 

                for intern_data in interns_data:
                    intern = Intern(
                        name=intern_data.get('name'),
                        email=intern_data.get('email'),
                        phone=intern_data.get('phone'),
                        skills=intern_data.get('skills'),
                        education=intern_data.get('education'),
                    )
                    intern.save()  

            return Response({'message': 'Interns created successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    else:
        return Response({'error': 'No JSON file path provided'}, status=400)