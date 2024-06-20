from django.core.management.base import BaseCommand
from app.models import Client, Contract, Event
from collaborateur.models import Collaborateur, Role
import datetime
from .utils import get_user_from_token, get_token_from_file

class Command(BaseCommand):
    help = 'CRM commands gestion'
    
    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command')
        
        # Subparser for create_collaborateur
        create_collaborateur_parser = subparsers.add_parser('create_collaborateur', help="Create a new collaborateur")
        create_collaborateur_parser.add_argument('nom', type=str, help='Last name of the collaborateur')
        create_collaborateur_parser.add_argument('prenom', type=str, help='First name of the collaborateur')
        create_collaborateur_parser.add_argument('username', type=str, help='Username of the collaborateur')
        create_collaborateur_parser.add_argument('email', type=str, help='Email of the collaborateur')
        create_collaborateur_parser.add_argument('role_name', type=str, help='Role name of the collaborateur')
        create_collaborateur_parser.add_argument('password', type=str, help='Password of the collaborateur')
        
        # Subparser for update_collaborateur
        update_collaborateur_parser = subparsers.add_parser('update_collaborateur', help='Update an existing collaborateur')
        update_collaborateur_parser.add_argument('collaborateur_id', type=int, help='ID of the collaborateur to update')
        update_collaborateur_parser.add_argument('--nom', type=str, help='New last name of the collaborateur')
        update_collaborateur_parser.add_argument('--prenom', type=str, help='New first name of the collaborateur')
        update_collaborateur_parser.add_argument('--email', type=str, help='New email name of the collaborateur')
        update_collaborateur_parser.add_argument('--role_name', type=str, help='New role of the collaborateur')
        
        # Subparser for read_collaborateur
        read_collaborateur_parser = subparsers.add_parser('read_collaborateur', help='Read and filter collaborateur')
        read_collaborateur_parser.add_argument('--role_name', type=str, help='Filter collaborateurs by role name')
       
        # Subparser for delete_collaborateur
        delete_collaborateur_parser = subparsers.add_parser('delete_collaborateur', help='Delete collaborateur')
        delete_collaborateur_parser.add_argument('collaborateur_id', type=int, help='ID of the collaborateur to delete')
       
        # Subparser for create_contract
        create_contract_parser = subparsers.add_parser('create_contract', help="Create a new contract")
        create_contract_parser.add_argument('montant_total', type=int, help='Total amount of the contract')
        create_contract_parser.add_argument('client_id', type=int, help='ID of the client associated with the contract')
        create_contract_parser.add_argument('commercial_id', type=int, help='ID of the commercial collaborator associated with the contract')

        # Subparser for update_contract
        update_contract_parser = subparsers.add_parser('update_contract', help='Update an existing contract')
        update_contract_parser.add_argument('contract_id', type=int, help='ID of the contract to update')
        update_contract_parser.add_argument('--montant_total', type=int, help='New montant total for the contract')
        update_contract_parser.add_argument('--montant_restant', type=int, help='New montant restant for the contract')
        update_contract_parser.add_argument('--signed', action='store_true', help='Set the contract statut to true')
        update_contract_parser.add_argument('--not_signed', action='store_true', help='Set the contract statut to false')
        update_contract_parser.add_argument('--client_id', type=int, help='ID of the associated client')
        update_contract_parser.add_argument('--commercial_id', type=int, help='ID of the associated commercial')

        # Subparser for read_event_without_support
        read_event_parser = subparsers.add_parser('read_event', help='Read and filter events without support')
        
        # Subparser for update_event
        update_event_parser = subparsers.add_parser('update_event', help='Update an existing event')
        update_event_parser.add_argument('event_id', type=int, help='ID of the event to update')
        update_event_parser.add_argument('--name', type=str, help='Name of the event')
        update_event_parser.add_argument('--date_de_debut', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(), help='Start date of the event in format YYYY-MM-DD')
        update_event_parser.add_argument('--date_de_fin', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(), help='End date of the event in format YYYY-MM-DD')
        update_event_parser.add_argument('--lieu', type=str, help='Location of the event')
        update_event_parser.add_argument('--participants', type=int, help='Number of participants')
        update_event_parser.add_argument('--notes', type=str, help='Notes for the event')
        update_event_parser.add_argument('--support_id', type=int, help='ID of the supporting collaborator')
        update_event_parser.add_argument('--contract_id', type=int, help='ID of the associated contract')
        update_event_parser.add_argument('--client_id', type=int, help='ID of the associated client')

    def handle(self, *args, **kwargs):
        command = kwargs.get('command')        
        token = get_token_from_file()

        user = get_user_from_token(token, self.stdout)
        print(user)
        if not user:
            print(token)
            self.stdout.write(self.style.ERROR('Invalid token'))
            return
        
        if not user.is_superuser and user.role.nom != "gestion":
            self.stdout.write(self.style.ERROR('You do not have permission'))
            return
        
        if command == 'create_collaborateur':
            self.create_collaborateur(**kwargs)
        elif command == 'update_collaborateur':
            self.update_collaborateur(**kwargs)
        elif command == 'read_collaborateur':
            self.read_collaborateur(**kwargs)
        elif command == 'delete_collaborateur':
            self.delete_collaborateur(**kwargs)
        elif command == 'create_contract':
            self.create_contract(**kwargs)
        elif command == 'update_contract':
            self.update_contract(**kwargs)
        elif command == 'read_event':
            self.read_event_without_support(**kwargs)
        elif command == 'update_event':
            self.update_event(**kwargs)
        else:
            self.stdout.write(self.style.ERROR('Invalid command'))    
           
    def create_collaborateur(self, **kwargs):
        nom = kwargs['nom']
        prenom = kwargs['prenom']
        username = kwargs['username']
        email = kwargs['email']
        role_name = kwargs['role_name']
        password = kwargs['password']
        
        try:
            role = Role.objects.get(nom=role_name)
            collaborateur = Collaborateur.objects.create(
                nom=nom,
                prenom=prenom,
                email=email,
                role=role,
                username=username
            )
            collaborateur.set_password(password)
            collaborateur.save()
            self.stdout.write(self.style.SUCCESS(f'Collaborateur {collaborateur.nom_complet} created successfully'))
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Role with id {role_name} does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating collaborateur: {e}'))
            
    def update_collaborateur(self, **kwargs):
        collaborateur_id = kwargs['collaborateur_id']
        
        try:
            collaborateur = Collaborateur.objects.get(id=collaborateur_id)
        
            if kwargs['nom']:
                collaborateur.nom = kwargs['nom']
            if kwargs['prenom']:
                collaborateur.prenom = kwargs['prenom']
            if kwargs['email']:
                collaborateur.email = kwargs['email']
            if kwargs['role_name']:
                try:
                    role = Role.objects.get(nom=kwargs['role_name'])
                    collaborateur.role = role
                except Role.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Role with id {kwargs["role_name"]} does not exist'))
                    return
            
            collaborateur.save()
            self.stdout.write(self.style.SUCCESS(f'Collaborateur {collaborateur.nom_complet} updated successfully'))
        
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Collaborateur with id {collaborateur_id} does not exist'))

    def read_collaborateur(self, **kwargs):
                role_name = kwargs.get('role_name')

                collaborateurs = Collaborateur.objects.all()

                if role_name:
                    try:
                        role = Role.objects.get(nom=role_name)
                        collaborateurs = collaborateurs.filter(role=role)
                    except Role.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Role with id {kwargs["role_name"]} does not exist'))
                        return

                for collaborateur in collaborateurs:
                    self.stdout.write(
                        f"Collaborateur ID: {collaborateur.id}, Collaborateur: {collaborateur.nom_complet}")
                    
    def delete_collaborateur(self, **kwargs):
        collaborateur_id = kwargs["collaborateur_id"]
        
        try:
            collaborateur = Collaborateur.objects.get(id=collaborateur_id)
            collaborateur.delete()
            self.stdout.write(self.style.SUCCESS(f'Collaborateur {collaborateur.nom_complet} deleted successfully'))
        except Collaborateur.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Collaborateur with id {collaborateur_id} does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error deleting collaborateur: {e}'))


    def create_contract(self, **kwargs):
        
        montant_total = kwargs['montant_total']
        client_id = kwargs['client_id']
        commercial_id = kwargs['commercial_id']
      
        try:
                client = Client.objects.get(id=client_id)
                commercial = Collaborateur.objects.get(id=commercial_id)

                if montant_total <= 0:
                    raise ValueError("Invalid montant values")

                Contract.objects.create(
                    montant_total=montant_total,
                    montant_restant=montant_total,
                    client=client,
                    commercial=commercial
                )
                self.stdout.write(self.style.SUCCESS('Contract created successfully'))

        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Client with id {client_id} does not exist'))
        except Collaborateur.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Commercial with id {commercial_id} does not exist'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Error creating contract: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))

            
    def update_contract(self, **kwargs):
        contract_id = kwargs['contract_id']

        try:
            contract = Contract.objects.get(id=contract_id)

            if kwargs['montant_total']:
                contract.montant_total = kwargs['montant_total']
            if kwargs['montant_restant']:
                contract.montant_restant = kwargs['montant_restant']
            if kwargs['signed']:
                contract.statut = True
            if kwargs['not_signed']:
                contract.statut = False
            if kwargs['client_id']:
                try:
                    client = Client.object.get(id=kwargs["client_id"])
                    contract.client = client
                except Client.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Client with id {kwargs["client_id"]} does not exist'))
                    return
            if kwargs['commercial_id']:
                try: 
                    commercial = Collaborateur.objects.get(id=kwargs["commercial_id"])
                    contract.commercial = commercial
                    
                except Collaborateur.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Collaborateur with id {kwargs["commercial_id"]} does not exist'))
                    return

            contract.save()
            self.stdout.write(self.style.SUCCESS(f'Contract {contract.id} updated successfully'))

        except Contract.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Contract with id {contract_id} does not exist'))


    def read_event_without_support(self, **kwargs):
        try:
            events_without_support = Event.objects.filter(support=None)

            if events_without_support.exists():
                self.stdout.write(self.style.SUCCESS('Events without support:'))
                for event in events_without_support:
                    self.stdout.write(
                        f"Event ID: {event.id}, Name: {event.name}, Client: {event.client.nom_complet}, "
                        f"Start Date: {event.date_de_debut}, End Date: {event.date_de_fin}, "
                        f"Location: {event.lieu}, Participants: {event.participants}, Notes: {event.notes}"
                    )
            else:
                self.stdout.write(self.style.SUCCESS('No events without support found'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error retrieving events: {e}'))
            
    def update_event(self, **kwargs):
        event_id = kwargs['event_id']

        try:
            event = Event.objects.get(id=event_id)

            if kwargs['name']:
                event.name = kwargs['name']
            if kwargs['date_de_debut']:
                event.date_de_debut = kwargs['date_de_debut']
            if kwargs['date_de_fin']:
                event.date_de_fin = kwargs['date_de_fin']
            if kwargs['lieu']:
                event.lieu = kwargs['lieu']
            if kwargs['participants']:
                event.participants = kwargs['participants']
            if kwargs['notes']:
                event.notes = kwargs['notes']
            if kwargs['support_id']:
                try:
                    support = Collaborateur.objects.get(id=kwargs['support_id'])
                    event.support = support
                except Collaborateur.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Support collaborator with id {kwargs["support_id"]} does not exist'))
                    return
            if kwargs['contract_id']:
                try:
                    contract = Contract.objects.get(id=kwargs['contract_id'])
                    event.contract = contract
                except Contract.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Contract with id {kwargs["contract_id"]} does not exist'))
                    return
            if kwargs['client_id']:
                try:
                    client = Client.objects.get(id=kwargs['client_id'])
                    event.client = client
                except Client.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Client with id {kwargs["client_id"]} does not exist'))
                    return

            event.save()
            self.stdout.write(self.style.SUCCESS(f'Event with ID {event_id} updated successfully'))

        except Event.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Event with id {event_id} does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating event: {e}'))