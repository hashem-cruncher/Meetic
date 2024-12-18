import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph


async def main():
    print("Python Graph Tutorial\n")

    # Load settings
    config = configparser.ConfigParser()
    config.read(["config.cfg", "config.dev.cfg"])
    azure_settings = config["azure"]

    graph: Graph = Graph(azure_settings)

    await greet_user(graph)

    choice = -1

    while choice != 0:
        print("\nPlease choose one of the following options:")
        print("0. Exit")
        print("1. Display access token")
        print("2. List my inbox")
        print("3. Send mail")
        print("4. List Teams call records")
        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print("Goodbye...")
            elif choice == 1:
                await display_access_token(graph)
            elif choice == 2:
                await list_inbox(graph)
            elif choice == 3:
                await send_mail(graph)
            elif choice == 4:
                await display_call_records(graph)
            else:
                print("Invalid choice!\n")
        except ODataError as odata_error:
            print("Error:")
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)


async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user:
        print("Hello,", user.display_name)
        # For Work/school accounts, email is in mail property
        # Personal accounts, email is in userPrincipalName
        print("Email:", user.mail or user.user_principal_name, "\n")


async def display_access_token(graph: Graph):
    token = await graph.get_user_token()
    print("User token:", token, "\n")


async def list_inbox(graph: Graph):
    message_page = await graph.get_inbox()
    if message_page and message_page.value:
        # Output each message's details
        for message in message_page.value:
            print("Message:", message.subject)
            if message.from_ and message.from_.email_address:
                print("  From:", message.from_.email_address.name or "NONE")
            else:
                print("  From: NONE")
            print("  Status:", "Read" if message.is_read else "Unread")
            print("  Received:", message.received_date_time)

        # If @odata.nextLink is present
        more_available = message_page.odata_next_link is not None
        print("\nMore messages available?", more_available, "\n")


async def send_mail(graph: Graph):
    # Define recipients
    recipients = [
        "m.marei@ai-crunch.com",
        "a.shehadeh@ai-crunch.com",
        "mo.marei@ai-crunch.com",
    ]

    try:
        # Send mail to multiple recipients
        await graph.send_mail(
            subject="Testing Microsoft Graph",
            body="Hello world!",
            recipient=recipients,
        )
        print("Mail sent to:", ", ".join(recipients), "\n")
    except Exception as e:
        print(f"Error sending mail: {str(e)}")


# async def send_mail(graph: Graph):
#     # Send mail to the signed-in user
#     # Get the user for their email address
#     user = await graph.get_user()
#     if user:
#         user_email = user.mail or user.user_principal_name

#         await graph.send_mail(
#             "Testing Microsoft Graph", "Hello world!", user_email or ""
#         )
#         print("Mail sent.\n")


async def display_call_records(graph: Graph):
    try:
        records = await graph.get_call_records()
        if records and records.value:
            print("\nRecent Teams Call Records:")
            print("------------------------")
            for record in records.value:
                start_time = (
                    record.start_date_time.strftime("%Y-%m-%d %H:%M:%S")
                    if record.start_date_time
                    else "Unknown"
                )
                end_time = (
                    record.end_date_time.strftime("%Y-%m-%d %H:%M:%S")
                    if record.end_date_time
                    else "Unknown"
                )
                print(f"Call ID: {record.id}")
                print(f"Start Time: {start_time}")
                print(f"End Time: {end_time}")
                print(f"Type: {record.type}")
                print(
                    f"Modalities: {', '.join(record.modalities) if record.modalities else 'Unknown'}"
                )
                print("------------------------")
        else:
            print("\nNo call records found.")
    except Exception as e:
        print(f"Error displaying call records: {str(e)}")


# Run main
asyncio.run(main())
