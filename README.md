# CRBBot

a discord bot for CRB's discord server.

## Google Calendar Setup

### Which Google Calendars does CRBBot read from?
Text goes here.

---

### What is CRBBot looking for in Google Calendar events?
CRBBot reads (fill this out)

---

## Bot Setup (On the Raspberry Pi 0)

### Important Info
rasberry pi 0 ip: 192.168.50.107

user: combatroboticsberkeley

pass: crb123

---

### Setup 
to ssh into it do ```ssh combatroboticsberkeley@192.168.50.107``` from a cmd and sign in (might need to press enter a couple times after entering password)

then navigate to github_repos/CRBBot (can do ```cd github_repos/CRBBot```)

then run ```source env/bin/activate``` to enter virtual env

then run ```python3 CRBBot.py``` to start the bot

when done, run ```sudo shutdown -h now``` to shut the raspberry pi 0 down before unplugging it

---

### Other Helpful Commands
```deactivate``` exits you from the virtual environment (in Python) 

---

## Slash Commands

### Pages
Pages allow for the storing and retrieval of any pages of text within the server. Saving/deleting pages require a permitted role.

`/view_page <name>` -> Display a saved page 
 `/save_page <name> <text>`-> Create or overwrite a page
 `/del_page <name>` -> Delete a page 
 `/list_pages` -> List all saved page names 

```
/view_page name:onboarding
/save_page name:onboarding text:Welcome to CRB! Here's how to get started...
/del_page name:onboarding
/list_pages
```

---

### Events
CRBBot is integrated with Google Calendar to ping channels before events start.

`/set_lead_calendar_channel` -> Sets the current channel as the channel where Lead Calendar pings are sent.
`/set_general_calendar_channel` -> Sets the current channel as the channel where General Calendar pings are sent.

```
/set_lead_calendar_channel
/set_general_calendar_channel
```

> CRBBot will ping a channel ~1 minute prior to any event on that channel's associated Google Calendar.

---

### Reminders

`/remind <delay> <remindees> <message>` -> Remind one or more mentioned users after a delay 
`/remindme <delay> <message>` -> Remind yourself after a delay 

Delay format: combine `w` (weeks), `d` (days), `h` (hours), `m` (minutes), `s` (seconds).

```
/remind delay:1h30m remindees:@Kyler @Ty message:Kyler please pay back Ty's money
/remindme delay:2d message:Order motor controllers and ESCs
/remindme delay:45s message:If I'm alive to see this reminder then the test box didn't blow up
```
