# Readme for HA eplucon portal warmtepomp setup

This are the instuctions to get information from eplucon portal in Home Assissent

You need have an account setup in the (Eplucon portal)[https://portaal.eplucon.nl/login?ut=user]

Also your heatingpump had to be setup there.

Next you need to get your API token.
You can find in the portal in your account settings.

Also nu need to query your moduleID for the heatingpump
This can be done with this curl:
```
curl --request GET \
  --url https://portaal.eplucon.nl/api/v2/econtrol/modules \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer <your-api-token>'
```
The id is the moduleID

## setup script and configuration

Place the script getinfo.py in config/scripts/ on the Home Assistent server.
Change the url, moduleID, ha-token, and api-token in the script getinfo.py

In the configuration.yaml add the lines:
```
shell_command:
  get_warmtepomp_info: python3 /config/scripts/getinfo.py

sensor: !include sensor.yaml
```

Add the file sensor.yaml to the config directory.
Restart Home Assistent (or reload all yaml file)

## Make an automation to run the script
Make a new automation to run the script every 15 minutes
```
alias: get_warmtepomt_info
description: ""
trigger:
  - platform: time_pattern
    minutes: /15
condition: []
action:
  - service: shell_command.get_warmtepomp_info
    data: {}
mode: single
```

The enities wil be visual in the enties screen and can be uses on a dashboard


