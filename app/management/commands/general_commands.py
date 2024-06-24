from django.core.management.base import BaseCommand
from app.models import Client, Contract, Event
from collaborateur.models import Collaborateur
from .utils import get_user_from_token, get_token_from_file, handle_exception


class Command(BaseCommand):
    help = "CRM commands commercial"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="command")

        # Subparser for read_clients
        read_clients_parser = subparsers.add_parser(
            "read_clients", help="Read all clients"
        )

        # Subparser for read_contracts
        read_contracts_parser = subparsers.add_parser(
            "read_contracts", help="Read all contracts"
        )

        # Subparser for read_events
        read_events_parser = subparsers.add_parser(
            "read_events", help="Read all events"
        )

    def handle(self, *args, **kwargs):
        command = kwargs.get("command")
        token = get_token_from_file()

        user = get_user_from_token(token, self.stdout)
        if not user:
            self.stdout.write(self.style.ERROR("Invalid token"))
            return

        if user.role.nom not in ["gestion", "commercial", "support"]:
            self.stdout.write(self.style.ERROR("You dont have permission"))
            return

        if command == "read_clients":
            self.read_clients()
        elif command == "read_contracts":
            self.read_contracts()
        elif command == "read_events":
            self.read_events()
        else:
            self.stdout.write(self.style.ERROR("Invalid command"))

    def read_clients(self, **kwargs):
        try:
            clients = Client.objects.all()

            if clients.exists():
                self.stdout.write(self.style.SUCCESS("Clients:"))
                for client in clients:
                    self.stdout.write(
                        f"Client ID: {client.id}, Name: {client.nom_complet}, "
                        f"Contact: {client.contact}, Entreprise: {client.nom_entreprise}, "
                        f"Commercial: {client.commercial.nom_complet}"
                    )
            else:
                self.stdout.write(self.style.SUCCESS("No clients found"))

        except Exception as e:
            handle_exception(e, self.stdout, f"Error retrieving clients: {e}")

    def read_contracts(self, **kwargs):
        try:
            contracts = Contract.objects.all()

            if contracts.exists():
                self.stdout.write(self.style.SUCCESS("Contracts:"))
                for contract in contracts:
                    self.stdout.write(
                        f"Contract ID: {contract.id}, "
                        f"Statut: {'signed' if contract.client.statut else 'not_signed'}, "
                        f"Montant total: {contract.montant_total}, "
                        f"Montant restant: {contract.montant_restant}, "
                        f"Client: {contract.client.nom_complet}, "
                        f"Commercial: {contract.commercial.nom_complet}"
                    )
            else:
                self.stdout.write(self.style.SUCCESS("No contracts found"))

        except Exception as e:
            handle_exception(e, self.stdout, f"Error retrieving contracts: {e}")

    def read_events(self, **kwargs):
        try:
            events = Event.objects.all()

            if events.exists():
                self.stdout.write(self.style.SUCCESS("Events:"))
                for event in events:
                    self.stdout.write(
                        f"Event ID: {event.id}, Name: {event.name}, "
                        f"Client: {event.client.nom_complet}, "
                        f"Start Date: {event.date_de_debut}, End Date: {event.date_de_fin}, "
                        f"Location: {event.lieu}, Participants: {event.participants}, "
                        f"Notes: {event.notes}"
                    )
            else:
                self.stdout.write(self.style.SUCCESS("No events found"))

        except Exception as e:
            handle_exception(e, self.stdout, f"Error retrieving events: {e}")
