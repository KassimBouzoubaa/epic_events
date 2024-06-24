from django.core.management.base import BaseCommand
from app.models import Client, Contract, Event
import datetime
from .utils import get_user_from_token, get_token_from_file, handle_exception


class Command(BaseCommand):
    help = "CRM commands support"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="command")

        # Subparser for read_events_by_support_id
        read_parser = subparsers.add_parser(
            "read_event", help="Read and filter events by support ID"
        )

        # Subparser for update_event
        update_parser = subparsers.add_parser(
            "update_event", help="Update an existing event"
        )
        update_parser.add_argument(
            "event_id", type=int, help="ID of the event to update"
        )
        update_parser.add_argument("--name", type=str, help="Name of the event")
        update_parser.add_argument(
            "--date_de_debut",
            type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
            help="Start date of the event in format YYYY-MM-DD",
        )
        update_parser.add_argument(
            "--date_de_fin",
            type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
            help="End date of the event in format YYYY-MM-DD",
        )
        update_parser.add_argument("--lieu", type=str, help="Location of the event")
        update_parser.add_argument(
            "--participants", type=int, help="Number of participants"
        )
        update_parser.add_argument("--notes", type=str, help="Notes for the event")
        update_parser.add_argument(
            "--contract_id", type=int, help="ID of the associated contract"
        )
        update_parser.add_argument(
            "--client_id", type=int, help="ID of the associated client"
        )

    def handle(self, *args, **kwargs):
        command = kwargs.get("command")
        token = get_token_from_file()

        user = get_user_from_token(token, self.stdout)
        if not user:
            self.stdout.write(self.style.ERROR("Invalid token"))
            return

        if user.role.nom != "support":
            self.stdout.write(self.style.ERROR("You dont have permission"))
            return

        if command == "read_event":
            self.read_events_by_support_id(user=user, **kwargs)
        elif command == "update_event":
            self.update_event(user=user, **kwargs)
        else:
            self.stdout.write(self.style.ERROR("Invalid command"))

    def read_events_by_support_id(self, user, **kwargs):
        try:
            events = Event.objects.filter(support_id=user.id)

            if not events.exists():
                self.stdout.write(
                    self.style.WARNING(f"No events found for support with ID {user.id}")
                )
                return

            self.stdout.write(self.style.SUCCESS("Events:"))
            for event in events:
                self.stdout.write(
                    f"Event ID: {event.id}, Name: {event.name}, Client: {event.client.nom_complet}, "
                    f"Start Date: {event.date_de_debut}, End Date: {event.date_de_fin}, "
                    f"Location: {event.lieu}, Participants: {event.participants}, Notes: {event.notes}"
                )

        except Exception as e:
            handle_exception(e, self.stdout,self.style, f"Error reading events: {e}")

    def update_event(self, user, **kwargs):
        event_id = kwargs["event_id"]

        try:
            event = Event.objects.get(id=event_id)
            if event.support.id != user.id:
                self.stdout.write(
                    self.style.ERROR(f"You are not responsible for the event")
                )
                return

            if kwargs["name"]:
                event.name = kwargs["name"]
            if kwargs["date_de_debut"]:
                event.date_de_debut = kwargs["date_de_debut"]
            if kwargs["date_de_fin"]:
                event.date_de_fin = kwargs["date_de_fin"]
            if kwargs["lieu"]:
                event.lieu = kwargs["lieu"]
            if kwargs["participants"]:
                event.participants = kwargs["participants"]
            if kwargs["notes"]:
                event.notes = kwargs["notes"]
            if kwargs["contract_id"]:
                try:
                    contract = Contract.objects.get(id=kwargs["contract_id"])
                    event.contract = contract
                except Contract.DoesNotExist as e:
                    handle_exception(
                        e, self.stdout,self.style, f'Contract with id {kwargs["contract_id"]} does not exist'
                    )
                    return
            if kwargs["client_id"]:
                try:
                    client = Client.objects.get(id=kwargs["client_id"])
                    event.client = client
                except Client.DoesNotExist as e:
                    handle_exception(
                        e, self.stdout,self.style, f'Client with id {kwargs["client_id"]} does not exist'
                    )
                    return

            event.save()
            self.stdout.write(
                self.style.SUCCESS(f"Event with ID {event_id} updated successfully")
            )

        except Event.DoesNotExist as e:
            handle_exception(e, self.stdout,self.style, f"Event with id {event_id} does not exist")
        except Exception as e:
            handle_exception(e, self.stdout,self.style, f"Error updating event: {e}")
