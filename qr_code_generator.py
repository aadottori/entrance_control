import qrcode
import uuid
import config
import os

def create_qr_code():
    ticket = uuid.uuid4()
    img = qrcode.make(ticket)
    img.save(os.path.join(config.base_path, "tickets", "ticket-{}.png".format(ticket)))
    return ticket
