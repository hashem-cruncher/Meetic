from configparser import SectionProxy
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.message import Message
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder,
)
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import (
    SendMailPostRequestBody,
)
from msgraph.generated.users.item.user_item_request_builder import (
    UserItemRequestBuilder,
)


class Graph:
    settings: SectionProxy
    client_credential: ClientSecretCredential
    user_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings["clientId"]
        tenant_id = self.settings["tenantId"]
        client_secret = self.settings["clientSecret"]
        self.user_email = self.settings.get("userEmail", "m.marei@ai-crunch.com")

        self.client_credential = ClientSecretCredential(
            tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
        )

        self.user_client = GraphServiceClient(
            self.client_credential, ["https://graph.microsoft.com/.default"]
        )

    async def get_user_token(self):
        access_token = self.client_credential.get_token(
            "https://graph.microsoft.com/.default"
        )
        return access_token.token

    async def get_user(self):
        # Fixed: Using users endpoint instead of /me
        query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
            select=["displayName", "mail", "userPrincipalName"]
        )

        request_config = (
            UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
        )

        # This is the key change: using users endpoint instead of me
        user = await self.user_client.users.by_user_id(self.user_email).get(
            request_configuration=request_config
        )
        return user

    async def get_inbox(self):
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            select=["from", "isRead", "receivedDateTime", "subject"],
            top=25,
            orderby=["receivedDateTime DESC"],
        )
        request_config = (
            MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
        )

        messages = (
            await self.user_client.users.by_user_id(self.user_email)
            .mail_folders.by_mail_folder_id("inbox")
            .messages.get(request_configuration=request_config)
        )
        return messages

    async def send_mail(self, subject: str, body: str, recipient: list[str]):
        message = Message()
        message.subject = subject

        message.body = ItemBody()
        message.body.content_type = BodyType.Text
        message.body.content = body

        message.to_recipients = []
        for email in recipient:
            to_recipient = Recipient()
            to_recipient.email_address = EmailAddress()
            to_recipient.email_address.address = email
            message.to_recipients.append(to_recipient)

        request_body = SendMailPostRequestBody()
        request_body.message = message
        request_body.save_to_sent_items = True

        await self.user_client.users.by_user_id(self.user_email).send_mail.post(
            body=request_body
        )

    async def get_call_records(self):
        try:
            records = await self.user_client.communications.call_records.get()
            return records
        except Exception as e:
            print(f"Error getting call records: {str(e)}")
            raise
