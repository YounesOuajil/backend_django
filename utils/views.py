from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from authentication.models import Candidate

# @api_view(['GET'])
# def create_candidates_from_json(request, json_file_path=None):
#     if json_file_path is None:
#         # If json_file_path is not provided as a parameter, assume it's passed as a query parameter in the request
#         json_file_path = request.query_params.get('json_file_path')

#     if json_file_path:
#         try:
#             with open(json_file_path, 'r') as file:
#                 data = json.load(file)
#                 candidates_data = data.get('candidates', [])

#                 for candidate_data in candidates_data:
#                     candidate = Candidate(
#                         username=candidate_data.get('email'),  # Using email as the username
#                         email=candidate_data.get('email'),
#                         first_name=candidate_data.get('first_name'),
#                         last_name=candidate_data.get('last_name'),
#                         cv=candidate_data.get('cv'),
#                         cover_letter=candidate_data.get('cover_letter'),
#                         company=candidate_data.get('company'),
#                         address=candidate_data.get('address'),
#                         city=candidate_data.get('city'),
#                         country=candidate_data.get('country'),
#                         postal_code=candidate_data.get('postal_code'),
#                         step=candidate_data.get('step'),
#                         role='c'  # Assuming all candidates are regular candidates
#                     )
#                     candidate.save()

#             return Response({'message': 'Candidates created successfully'})
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)
#     else:
#         return Response({'error': 'No JSON file path provided'}, status=400)

from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Intern

@api_view(['Post'])
def create_interns_from_json(request, json_file_path=None):
    if json_file_path is None:
        # If json_file_path is not provided as a parameter, assume it's passed as a query parameter in the request
        json_file_path = request.query_params.get('json_file_path')

    if json_file_path:
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                interns_data = data.get('interns', [])  # Corrected key name

                for intern_data in interns_data:
                    intern = Intern(
                        name=intern_data.get('name'),
                        email=intern_data.get('email'),
                        phone=intern_data.get('phone'),
                        skills=intern_data.get('skills'),
                        education=intern_data.get('education'),
                    )
                    intern.save()  # Corrected method call

            return Response({'message': 'Interns created successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    else:
        return Response({'error': 'No JSON file path provided'}, status=400)