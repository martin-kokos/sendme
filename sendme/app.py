import re
import os
import io
import socket
from pathlib import Path
from logging import getLogger
from string import Template

import qrcode
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse


log = getLogger(__name__)

app = FastAPI()

UPLOAD_DIR = Path("./received_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("iana.org", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def get_qr_code() -> str:
    server_ip = get_ip()
    SERVER_URL = "http://" + server_ip + ":9999/"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(SERVER_URL)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return str(f.read())


def get_invite_text() -> str:
    server_ip = get_ip()
    SERVER_URL = "http://" + server_ip + ":9999/"
    QR_CODE = get_qr_code()

    return f"""
    Sender can go here to send you a file over the local network / Wi-fi:

    {QR_CODE}

    {SERVER_URL}

    You'll be presented with a form to send a file.

    (This works over the local network and won't work over the internet.)
    """


def get_template() -> Template:
    TEMPPLATE_PATH = Path(__file__).parent / "index.htmlx"
    with open(TEMPPLATE_PATH) as f:
        template = Template(f.read())
    return template


def get_safe_filename(filename: str) -> Path:
    safe_filename = re.sub(r'[^\w\d\-\_\.]', '_', filename)
    while (UPLOAD_DIR / Path(safe_filename)).exists():
        log.warn(f"{(UPLOAD_DIR / Path(safe_filename))} already exists")
        counter = re.findall(r'_\d*$', safe_filename)
        if not counter:
            safe_filename = safe_filename + '_1'
            continue
        counter_next = int(counter[0][1:]) + 1
        safe_filename = safe_filename.rstrip(counter[-1]) + f'_{counter_next}'

    return Path(safe_filename)


print()
print(get_invite_text())


@app.get("/", response_class=HTMLResponse)
async def form():
    return get_template().substitute(invite_text=get_invite_text())


@app.post("/", response_class=HTMLResponse)
async def receive(file: UploadFile):
    safe_filename = get_safe_filename(file.filename)

    with open(UPLOAD_DIR / safe_filename, 'wb') as writefile:
        writefile.write(file.file.read())

    print(f"Already have files in directory {UPLOAD_DIR}/. :")
    print('\n'.join(os.listdir(UPLOAD_DIR)))
    print()
    print(f"Accepted a new file: {safe_filename}")

    return get_template().substitute(invite_text=get_invite_text())
