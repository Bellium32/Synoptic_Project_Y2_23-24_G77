from twilio.rest import Client
import keys

client = Client(keys.account_sid, keys.auth_token)

message = client.messages.create (
    body = "hey its ash, it works :)",
    from_=keys.twilio_number,
    to=keys.my_phone_number

)

print(message.body)