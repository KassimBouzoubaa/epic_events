from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
import os

User = get_user_model()

def get_user_from_token(token, stdout):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        stdout.write(f'Error retrieving user from token: {e}')
        return None
    
def get_token_from_file():
    file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../storage/token.txt"))
    try:
        with open(file_path, 'r') as file:
            token = file.readline().strip()
            return token
    except FileNotFoundError:
        print(f"File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

