from django.core.management.base import BaseCommand
from app.models import Client, Contract, Event
from collaborateur.models import Collaborateur
import datetime
from .utils import get_user_from_token, get_token_from_file, handle_exception


class Command(BaseCommand):
    help = "CRM commands commercial"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="command")

        # Subparser for create_client
        create_client_parser = subparsers.add_parser(
            "create_client", help="Create a new client"
        )
        create_client_parser.add_argument(
            "information", type=str, help="Information about the client"
        )
        create_client_parser.add_argument(
            "nom", type=str, help="Last name of the client"
        )
        create_client_parser.add_argument(
            "prenom", type=str, help="First name of the client"
        )
        create_client_parser.add_argument("email", type=str, help="Email of the client")
        create_client_parser.add_argument(
            "telephone", type=str, help="Phone number of the client"
        )
        create_client_parser.add_argument(
            "nom_entreprise", type=str, help="Company name of the client"
        )

        # Subparser for update_client
        update_client_parser = subparsers.add_parser(
            "update_client", help="Update an existing client"
        )
        update_client_parser.add_argument(
            "client_id", type=int, help="ID of the client to update"
        )
        update_client_parser.add_argument(
            "--information", type=str, help="New information about the client"
        )
        update_client_parser.add_argument(
            "--nom", type=str, help="New last name of the client"
        )
        update_client_parser.add_argument(
            "--prenom", type=str, help="New first name of the client"
        )
        update_client_parser.add_argument(
            "--email", type=str, help="New email of the client"
        )
        update_client_parser.add_argument(
            "--telephone", type=str, help="New phone number of the client"
        )
        update_client_parser.add_argument(
            "--nom_entreprise", type=str, help="New company name of the client"
        )
        update_client_parser.add_argument(
            "--commercial_id", type=int, help="New ID of the commercial collaborator"
        )

        # Subparser for read_contract
        read_contract_parser = subparsers.add_parser(
            "read_contract", help="Read and filter contracts"
        )
        read_contract_parser.add_argument(
            "--client_id", type=int, help="Filter contracts by client ID"
        )
        read_contract_parser.add_argument(
            "--commercial",
            action="store_true",
            help="Filter contracts by commercial ID",
        )
        read_contract_parser.add_argument(
            "--unpaid_only",
            action="store_true",
            help="Filter contracts that are not fully paid",
        )
        read_contract_parser.add_argument(
            "--inactive_only", action="store_true", help="Filter inactive contracts"
        )

        # Subparser for update_contract
        update_contract_parser = subparsers.add_parser(
            "update_contract", help="Update an existing contract"
        )
        update_contract_parser.add_argument(
            "contract_id", type=int, help="ID of the contract to update"
        )
        update_contract_parser.add_argument(
            "--montant_total", type=int, help="New montant total for the contract"
        )
        update_contract_parser.add_argument(
            "--montant_restant", type=int, help="New montant restant for the contract"
        )
        update_contract_parser.add_argument(
            "--signed", action="store_true", help="Set the contract status to signed"
        )
        update_contract_parser.add_argument(
            "--not_signed",
            action="store_true",
            help="Set the contract status to not signed",
        )
        update_contract_parser.add_argument(
            "--client_id", type=int, help="Set the client for the contract"
        )

        # Subparser for create_event
        create_event_parser = subparsers.add_parser(
            "create_event", help="Create a new event"
        )
        create_event_parser.add_argument("name", type=str, help="Name of the event")
        create_event_parser.add_argument(
            "date_de_debut",
            type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
            help="Start date of the event in format YYYY-MM-DD",
        )
        create_event_parser.add_argument(
            "date_de_fin",
            type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
            help="End date of the event in format YYYY-MM-DD",
        )
        create_event_parser.add_argument("lieu", type=str, help="Location of the event")
        create_event_parser.add_argument(
            "participants", type=int, help="Number of participants"
        )
        create_event_parser.add_argument("notes", type=str, help="Notes for the event")
        create_event_parser.add_argument(
            "support_id", type=int, help="ID of the supporting collaborator"
        )
        create_event_parser.add_argument(
            "contract_id", type=int, help="ID of the associated contract"
        )

    def handle(self, *args, **kwargs):
        command = kwargs.get("command")
        token = get_token_from_file()

        user = get_user_from_token(token, self.stdout)
        if not user:
            self.stdout.write(self.style.ERROR("Invalid token"))
            return

        if user.role.nom != "commercial":
            self.stdout.write(self.style.ERROR("You dont have permission"))
            return

        if command == "create_client":
            self.create_client(user=user, **kwargs)
        elif command == "update_client":
            self.update_client(user=user, **kwargs)
        elif command == "read_contract":
            self.read_contract(user=user, **kwargs)
        elif command == "update_contract":
            self.update_contract(user=user, **kwargs)
        elif command == "create_event":
            self.create_event(user=user, **kwargs)
        else:
            self.stdout.write(self.style.ERROR("Invalid command"))

    def create_client(self, user, **kwargs):
        information = kwargs["information"]
        nom = kwargs["nom"]
        prenom = kwargs["prenom"]
        email = kwargs["email"]
        telephone = kwargs["telephone"]
        nom_entreprise = kwargs["nom_entreprise"]

        try:
            commercial = Collaborateur.objects.get(id=user.id)
            client = Client.objects.create(
                information=information,
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                nom_entreprise=nom_entreprise,
                commercial=commercial,
            )
            client.save()
            self.stdout.write(
                self.style.SUCCESS(f"Client {client.nom_complet} created successfully")
            )
        except Collaborateur.DoesNotExist as e:
            handle_exception(
                e, self.stdout,self.style,  f"Collaborateur with id {commercial.id} does not exist"
            )

    def update_client(self, user, **kwargs):
        client_id = kwargs["client_id"]

        try:
            client = Client.objects.get(id=client_id)
            if client.commercial.id != user.id:
                self.stdout.write(
                    self.style.ERROR(f"You are not responsible of this client")
                )
                return

            if kwargs["information"]:
                client.information = kwargs["information"]
            if kwargs["nom"]:
                client.nom = kwargs["nom"]
            if kwargs["prenom"]:
                client.prenom = kwargs["prenom"]
            if kwargs["email"]:
                client.email = kwargs["email"]
            if kwargs["telephone"]:
                client.telephone = kwargs["telephone"]
            if kwargs["nom_entreprise"]:
                client.nom_entreprise = kwargs["nom_entreprise"]

            client.save()
            self.stdout.write(
                self.style.SUCCESS(f"Client {client.nom_complet} updated successfully")
            )

        except Client.DoesNotExist as e:
            handle_exception(
                e, self.stdout, self.style, f"Client with id {client_id} does not exist"
            )

    def read_contract(self, user, **kwargs):
        client_id = kwargs.get("client_id")
        unpaid_only = kwargs.get("unpaid_only")
        inactive_only = kwargs.get("inactive_only")
        commercial = kwargs.get("commercial")

        contracts = Contract.objects.all()

        if client_id:
            contracts = contracts.filter(client_id=client_id)
        if commercial:
            contracts = contracts.filter(commercial_id=user.id)
        if unpaid_only:
            contracts = contracts.filter(montant_restant__gt=0)
        if inactive_only:
            contracts = contracts.filter(statut=False)

        for contract in contracts:
            self.stdout.write(
                f"Contract ID: {contract.id}, Client: {contract.client.nom_complet}, "
                f"Commercial: {contract.commercial.nom_complet}, Total Amount: {contract.montant_total}, "
                f"Remaining Amount: {contract.montant_restant}, Status: {'Active' if contract.statut else 'Inactive'}"
            )

    def update_contract(self, user, **kwargs):
        contract_id = kwargs["contract_id"]

        try:
            contract = Contract.objects.get(id=contract_id)
            client_id = contract.client.id
            client = Client.objects.get(id=client_id)
           
            if client.commercial.id != user.id:
                self.stdout.write(
                    self.style.ERROR(f"You are not responsible of this client")
                )
                return

            if kwargs["montant_total"]:
                contract.montant_total = kwargs["montant_total"]
            if kwargs["montant_restant"]:
                contract.montant_restant = kwargs["montant_restant"]
            if kwargs["signed"]:
                contract.statut = True
            if kwargs["not_signed"]:
                contract.statut = False
            if kwargs["client_id"]:
                try:
                    client = Client.object.get(id=kwargs["client_id"])
                    contract.client = client
                except Client.DoesNotExist as e:
                    handle_exception(
                        e,
                        self.stdout,
                        self.style,
                        f'Client with id {kwargs["client_id"]} does not exist',
                    )
                    return

            contract.save()
            self.stdout.write(
                self.style.SUCCESS(f"Contract {contract.id} updated successfully")
            )

        except Contract.DoesNotExist as e:
            handle_exception(
                e, self.stdout, self.style, f"Contract with id {contract_id} does not exist"
            )

    def create_event(self, user, **kwargs):
        name = kwargs["name"]
        contract_id = kwargs["contract_id"]
        date_de_debut = kwargs["date_de_debut"]
        date_de_fin = kwargs["date_de_fin"]
        support_id = kwargs["support_id"]
        lieu = kwargs["lieu"]
        participants = kwargs["participants"]
        notes = kwargs["notes"]

        try:
            contract = Contract.objects.get(id=contract_id)
            client = Client.objects.get(id=contract.client.id)
            support = Collaborateur.objects.get(id=support_id)

            if client.commercial.id != user.id:
                self.stdout.write(
                    self.style.ERROR(f"You are not responsible of this client")
                )
                return

            if not contract.statut:
                self.stdout.write(
                    self.style.ERROR(
                        f"Cannot create event for an unsigned contract (ID: {contract_id})."
                    )
                )
                return

            event = Event.objects.create(
                name=name,
                contract=contract,
                client=client,
                date_de_debut=date_de_debut,
                date_de_fin=date_de_fin,
                support=support,
                lieu=lieu,
                participants=participants,
                notes=notes,
            )
            event.save()
            self.stdout.write(
                self.style.SUCCESS(f"Event {event.name} created successfully")
            )
        except Contract.DoesNotExist as e:
            handle_exception(
                e, self.stdout, self.style, f"Contract with id {contract_id} does not exist"
            )
        except Client.DoesNotExist as e:
            handle_exception(
                e, self.stdout, self.style, f"Client with id {client.id} does not exist"
            )
        except Collaborateur.DoesNotExist as e:
            handle_exception(
                e, self.stdout, f"Collaborateur with id {support_id} does not exist"
            )
