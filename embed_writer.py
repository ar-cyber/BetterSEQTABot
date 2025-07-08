import json

filename = "spatial"

jsons = {
    "embed": {
        "title": "How to Enable Spatial Audio With Voicemeeter",
        "description": """For spatial audio with voicemeeter, simply make “Voicemeeter Input” your default playback device in windows (https://imgur.com/QlYfNz1).

Then follow this, (https://imgur.com/DQY73Cm)

IF it’s “greyed out” (Not Working)

This could be from a driver/application that comes with SteelSeries devices. It’s called “SteelSeries Sonar”.

1.) Type “device manager” into the Windows search bar and open it.
2.) Next, find “sound, video and game controllers” and uninstall the device called “SteelSeries Sonar” (Reference: https://imgur.com/ebVwv6r )

3.) Next go to
C:\\Program Files\\SteelSeries\\GG and delete the “Sonar” folder.

4.) Lastly, Restart PC""",
    }
}

with open(f'cogs/embed/{filename}.json', 'w') as fp:
    json.dump(jsons, fp)