# Sendme
A simple server app to receive a file over the local network from a dumb device or a user via an HTTP form.

## Usecase
This app aims to solve sending files over the **local network**. This is useful because:
- doesn't rely on services on the internet
- is usually faster because the transfer goes just through the local router, not across the world
- doesn't use data from your mobile data plan
- works in remote areas where there might be little to no connectivity to the internet
- no advanced tools such as ssh, rsync, etc. are needed on the sender side

for example:
- quickly receive a large file from your phone
- receive a file where there is slow internet or no internet at all

## How
1. Alice - clone repo `git clone git@github.com:martin-kokos/sendme.git`, enter project `cd sendme`, install dependencies `poetry install`
2. Alice - start the server `./start_receiver.sh`

3. Bob - go to the URL presented on Alice's computers. Select the file to uplad and click *Upload file*

4. Alice can see on her screen a file has been received and where it's been saved

## Tips

- To do the opposite and "push" a file to a dumb device, use the pytohn buit-in `python -m http.server`.
- Use a phone's hotspot to join two computers on a local network. Because the transfer happens locally, mobile data plan is not being used up.
- Send the file with cURL `curl -X 'POST' 'http://ip_address:9999/' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'file=@/path/file'`
