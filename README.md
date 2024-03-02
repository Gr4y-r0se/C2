# C2

Connect and Control (C2) is a multifunctional webapp intended for Pentesters to use on engagements. 

## Usage

There are two core peices of functionality: **Manage Payloads** and **Monitor Interactions**.
</br></br>
<img width="464" alt="Welcome" src="https://github.com/Gr4y-r0se/C2/assets/59868499/cf3d57e4-2c13-40ea-bf2d-640ce176a440">

But first, simply set up the app (if it's the first time, make a note of the admin password):
```bash
python3 app.py
```

Then browse to `https://localhost/` to get cracking!

### Manage Payloads

You can configure JavaScript payloads within this functionality, which can then pulled in and executed (for better proof of concepts!)
Interactions also get logged below.

Looks a little like this:</br></br>
<img width="718" alt="Manage Payloads" src="https://github.com/Gr4y-r0se/C2/assets/59868499/0c5d6397-9f51-445d-ac0f-9c6c4e942841">


### Monitor Interactions

If you send GET or POST requests to the URL specifified in the app, it'll log them. 
This can be used in XSS payloads to exfiltrate data on local apps (if you can't access collaborator).

It looks a little like so:</br></br>
<img width="912" alt="Monitor Interactions" src="https://github.com/Gr4y-r0se/C2/assets/59868499/ea3b847b-fe21-4320-b45f-1c964e45f177">


## Installation

Clone this repository:

```bash
git clone https://github.com/Gr4y-r0se/C2.git
```

Then install the requirements:
```bash
pip3 install -r requirements.txt
```

## Contributing

Pull requests are welcome - especially if you want to redesign the UI (it's pretty ugly). 
If you're not yet able to write the update you want to see, that's okay - just open an issue!

Please, for major changes, open an issue first to discuss what you would like to change.
(Nnless it's the UI. I am not a graphic designer, and it's sure not my passion. Please help.)

## License

This is released under the [MIT](https://choosealicense.com/licenses/mit/) license. 

## Roadmap

 - Add other content types (XML etc) for serving
 - Migrate scripts to their own folder, and dynamically inject them into each user account.
 - Make the UI better (please open a pull request if you're good at this)
