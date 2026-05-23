# CRBBot

a discord bot for CRB's discord server.

## Bot Setup (On the Raspberry Pi 0)

### Important Info
rasberry pi 0 ip: 192.168.50.107

user: combatroboticsberkeley

pass: crb123

### Setup 
to ssh into it do ```ssh combatroboticsberkeley@192.168.50.107``` from a cmd and sign in (might need to press enter a couple times after entering password)

then navigate to github_repos/CRBBot (can do ```cd github_repos/CRBBot```)

then run ```source env/bin/activate``` to enter virtual env

then run ```python3 crb_bot.py``` to start the bot

when done, run ```sudo shutdown -h now``` to shut the raspberry pi 0 down before unplugging it

### Other Helpful Commands
```deactivate``` exits you from the virtual environment (in Python) 

## Slash Commands

### Pages
Store and retrieve text snippets in the server. Save/delete require a permitted role (permitted roles set in code as of rn - Cai).

| Command | Description |
|---|---|
| `/view_page <name>` | Display a saved page |
| `/save_page <name> <text>` | Create or overwrite a page |
| `/del_page <name>` | Delete a page |
| `/list_pages` | List all saved page names |

```
/view_page name:onboarding
/save_page name:onboarding text:Welcome to CRB! Here's how to get started...
/del_page name:onboarding
/list_pages
```

---

### Events
Integrates with Google Calendar to ping a channel before meetings start. Save/delete require a permitted role.

| Command | Description |
|---|---|
| `/set_meeting_channel` | Set the current channel as the destination for meeting pings |

```
/set_meeting_channel
```

> The bot automatically pings the meeting channel ~1 minute before any event on the linked Google Calendar.

---

### Reminders

| Command | Description |
|---|---|
| `/remind <delay> <remindees> <message>` | Remind one or more mentioned users after a delay |
| `/remindme <delay> <message>` | Remind yourself after a delay |

Delay format: combine `w` (weeks), `d` (days), `h` (hours), `m` (minutes), `s` (seconds).

```
/remind delay:1h30m remindees:@Kyler @Ty message:Kyler please pay back Ty's money
/remindme delay:2d message:Order motor controllers and ESCs
/remindme delay:45s message:If I'm alive to see this reminder then the test box didn't blow up
```
