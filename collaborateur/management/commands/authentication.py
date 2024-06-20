from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import os
from ...models import Collaborateur

class Command(BaseCommand):
    help = 'Generate JWT token for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('password', type=str, help='Password of the user')
        parser.add_argument('--logout', action='store_true', help='Logout and delete token file')

    def handle(self, *args, **kwargs):
        
        if kwargs['logout']:
            self.logout()
            return
        
        username = kwargs['username']
        password = kwargs['password']
        output_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../storage/token.txt"))

         # Créer le répertoire s'il n'existe pas
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        if not username or not password:
            self.stdout.write(self.style.ERROR('Username and password are required'))
            return
        
        try:
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                with open(output_file, 'w') as f:
                     f.write(access_token + '\n')
                     f.write(refresh_token + '\n')
                     self.stdout.write(self.style.SUCCESS(f'Tokens saved to {output_file}'))

            else:
                self.stdout.write(self.style.ERROR(f'Invalid credentials'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

    def logout(self):
        output_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../storage/token.txt"))
        if os.path.exists(output_file):
            os.remove(output_file)
            self.stdout.write(self.style.SUCCESS(f'{output_file} has been deleted'))
        else:
            self.stdout.write(self.style.ERROR(f'{output_file} does not exist'))