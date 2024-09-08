# C2

Connect and Control (C2) is a multifunctional webapp designed for Pentesters to use on engagements. 

## Usage

There are three core peices of functionality: **View Interactions**, **Manage Payloads**, and **Manage Endpoints**.
</br></br>
<img width="266" alt="sidebar" src="https://github.com/user-attachments/assets/fb56852b-1bba-45ef-9e9e-7cd3d73048c9">

### View Interactions

If you send GET or POST requests to the URL specifified in the app, it'll log them. 
This can be used in XSS payloads to exfiltrate data.

It looks a little like so:</br></br>
<img width="1039" alt="Monitor Interactions" src="https://github.com/user-attachments/assets/53202d8f-4ea4-4965-9794-1fdcfbeef2bd">


### Manage Payloads

You can configure payloads within this functionality, which are then served by your various endpoints 
Interactions also get logged below.

Looks a little like this:</br></br>
<img width="1193" alt="Manage Payloads" src="https://github.com/user-attachments/assets/e0fab113-3182-46be-b860-ce6c77190c1e">


### Manage Endpoints

New in the latest update, you can now manage your endpoints - meaning multiple endpoints can be active, all serving different payloads! For maximum havoc.

You can interrogate your currently active endpoints:</br></br>
<img width="1572" alt="View Endpoints" src="https://github.com/user-attachments/assets/18ac54b7-cdaf-43ed-b381-2f107718213c">

...and modify them as you wish:</br></br>
<img width="877" alt="Modify Endpoint" src="https://github.com/user-attachments/assets/4e642f71-9fad-435e-b11b-cb40af3c55c6">


## Installation

#### First...
Clone this repository:

```bash
git clone https://github.com/Gr4y-r0se/C2.git
```

#### Bare Metal 

Then install the requirements:
```bash
pip3 install -r requirements.txt
```

```bash
python3 app.py
```

#### Docker 

```bash
docker build -t c2-app .
docker run -p 443:443 c2-app
```

#### Docker Compose 

```bash
docker-compose up --build
```

#### ...Finally

Then browse to `https://localhost/` to get cracking!

## Contributing

Pull requests are welcome - especially if you want to redesign the UI (it's pretty ugly). 
If you're not yet able to write the update you want to see, that's okay - just open an issue!

Please, for major changes, open an issue first to discuss what you would like to change.

## License

This is released under the [MIT](https://choosealicense.com/licenses/mit/) license. 

## Roadmap

### To Do
 - Support templating for JS (so you can dynamically load files)
 - Support serving files through JS objects
 - Add JS obfuscation so scripts are randomised every time they are served


### Completed
 - Make the UI better (please open a pull request if you're good at this). (Special thanks to [BDragisic](https://github.com/BDragisic) for this one.)
 - Migrate scripts to their own folder, and dynamically inject them into each user account.
 - Add other content types (XML etc) for serving
