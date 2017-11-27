import os

#############################
### Environment Variables ###
#############################
APP_ID = os.environ.get("APP_ID") #e.g. amzn1.ask.skill.00000000-0000-0000-0000-000000000000
MUSIC_URL_PREFIX = os.environ.get("MUSIC_URL_PREFIX") #e.g. https://www.example.com/music/

################
### Mappings ###
################

# map of soundex(skater) to program definitions
# TODO move this data to dynamodb
SKATER_DATA = {
    "s5": {
        "name": "shawn",
        "default": "free",
        "programs": {
            "free": {
                "music": "shawn_pan_free.mp3"
            }
        }
    },
    "f46": {
        "name": "flora",
        "default": "long",
        "programs": {
            "long": {
                "music": "flora_su_free.mp3"
            },
            "short": {
                "music": "flora_su_short.mp3"
            }
        }
    },
    "d5": {
        "name": "diane",
        "default": "long",
        "programs": {
            "long": {
                "music": "diane_zhou_free.mp3"
            },
            "short": {
                "music": "diane_zhou_short.mp3"
            }
        }
    },
    "s6": {
        "name": "sarah",
        "default": "free",
        "programs": {
            "free": {
                "music": "sarah_don_free.mp3"
            }
        }
    },
    "k4": {
        "name": "kylie",
        "default": "short",
        "programs": {
            "short": {
                "music": "kylie_ying_short.mp3"
            },
            "show": {
                "music": "kylie_ying_show.mp3"
            }
        }
    }
}

########################
### Play Music Logic ###
########################
def play_program(skater, variant, element, delay):
    print "skater: " + skater
    print "variant: " + variant
    print "element: " + element

    if variant == "cat":
        return response_say("<speak><say-as interpret-as='interjection'>meow</say-as></speak>")

    skater_data = SKATER_DATA.get(soundex(skater))
    if not skater_data:
        return response_say("Sorry, I can't find the skater " + skater)

    if not variant:
        variant = skater_data["default"]
    program = skater_data["programs"].get(variant)

    if not program:
        return response_say("Sorry, I can't find " + variant + " program for " + skater)

    # TODO figure out nice way to handle element bookmarks
    if skater_data["name"] == "shawn" and element.startswith("step"):
        return response_play_music("shawn_pan_free.mp3", offset=44000, message="playing from your step sequence")

    return response_play_music(program["music"], delay=delay)

#################
### Responses ###
#################
def response_blank():
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "shouldEndSession": True
        }
    }

def response_say(message):
    response = response_blank()
    if message.startswith("<speak>"):
        response["response"]["outputSpeech"] = {
            "type": "SSML",
            "ssml": message
        }
    else:
        response["response"]["outputSpeech"] = {
            "type": "PlainText",
            "text": message
        }
    return response

def response_play_music(filename, offset=0, message=None, delay=False):
    # default messages
    if not message:
        if delay:
            message = "<speak>waiting ten seconds <break time='10s'/> playing</speak>"
        else:
            message = "playing your program"

    response = response_say(message)
    response["response"]["directives"] = [
        {
            "type": "AudioPlayer.Play",
            "playBehavior": "REPLACE_ALL",
            "audioItem": {
                "stream": {
                    "token": filename,
                    "url": MUSIC_URL_PREFIX + filename,
                    "offsetInMilliseconds": offset
                }
            }
        }
    ]
    return response

def response_stop_music():
    response = response_blank()
    response["response"]["directives"] = [
        {
            "type": "AudioPlayer.Stop",
        }
    ]
    return response

####################
### Main Handler ###
####################
def lambda_handler(event, context):
    ## convenience fields on event
    session = event.get("session")
    request = event.get("request")
    request_type = request.get("type")

    ## validate request has correct credentials
    try:
        if session: # user requests have a session
            application_id = session["application"]["applicationId"]
        else: # audio player requests have a context
            application_id = event["context"]["System"]["application"]["applicationId"]
    except:
        raise ValueError("Missing Application ID")

    if application_id != APP_ID:
        raise ValueError("Invalid Application ID")

    ## route requests to appropriate handlers
    print "Received request of type: " + request_type

    if request_type == "IntentRequest":
        intent = request["intent"]
        intent_name = intent["name"]
        print "Received intent: " + intent_name
        if intent_name == "PlayProgramIntent" or intent_name == "AMAZON.StartOverIntent":
            skater = intent.get("slots", {}).get("skater", {}).get("value", "").lower()
            variant = intent.get("slots", {}).get("variant", {}).get("value", "").lower()
            element = intent.get("slots", {}).get("element", {}).get("value", "").lower()
            return play_program(skater, variant, element, False)
        elif intent_name == "RunThroughProgramIntent":
            skater = intent.get("slots", {}).get("skater", {}).get("value", "").lower()
            variant = intent.get("slots", {}).get("variant", {}).get("value", "").lower()
            return play_program(skater, variant, "", True)
        elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.PauseIntent":
            return response_stop_music() # TODO persist track info and location on pause
        elif intent_name == "AMAZON.ResumeIntent":
            return response_say("Resume is not yet implemented.")
        elif intent_name == "AMAZON.NextIntent":
            return response_say("Next is not yet implemented.")
        elif intent_name == "AMAZON.PreviousIntent":
            return response_say("Previous is not yet implemented.")
        elif intent_name == "AMAZON.HelpIntent":
            return response_say("Help is not yet implemented.")
    elif request_type == "LaunchRequest":
        return response_say("Sessions are not yet implemented.")
    else:
        print "Ignoring request of type: " + request_type
        return response_blank()

#########################
### Utility Functions ###
#########################

# Creates fingerprint of a lowercase word such that similiar sounds map to the same value.
# Variation of the soundex algorthm (not truncated or padded to 3 digits).
# https://en.wikipedia.org/wiki/Soundex
SOUNDEX_MAPPING = {
  "b": "1", "f": "1", "p": "1", "v": "1",
  "c": "2", "g": "2", "j": "2", "k": "2", "q": "2", "s": "2", "x": "2", "z": "2",
  "d": "3", "t": "3",
  "l": "4",
  "m": "5", "n": "5",
  "r": "6"
}

def soundex(word):
  result = ""
  last = None
  for i, letter in enumerate(word):
    if i == 0:
      result += letter
      last = SOUNDEX_MAPPING.get(letter, "")
    else:
      current = SOUNDEX_MAPPING.get(letter, "")
      if current != last and letter != "h" and letter != "w":
        result += current
        last = current
  return result
