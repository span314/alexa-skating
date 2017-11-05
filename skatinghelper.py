import os

#############################
### Environment Variables ###
#############################
APP_ID = os.environ.get("APP_ID") #e.g. amzn1.ask.skill.00000000-0000-0000-0000-000000000000
MUSIC_URL_PREFIX = os.environ.get("MUSIC_URL_PREFIX") #e.g. https://www.example.com/music/

########################
### Play Music Logic ###
########################
def play_program(skater, variant, element, delay):
    print "skater: " + skater
    print "variant: " + variant
    print "element: " + element

    if skater == "sean":
        if element.startswith("step"):
            return response_play_music("shawn_pan_free.mp3", offset=43000, message="playing from your step sequence")
        else:
            return response_play_music("shawn_pan_free.mp3", delay=delay)

    elif skater == "flora":
        if variant == "short":
            return response_say("Sorry Flora, I don't have music for your short.")
        elif variant == "cat":
            return response_say("<speak><say-as interpret-as='interjection'>meow</say-as></speak>")
        else:
            return response_play_music("flora_su_free.mp3", delay=delay)

    elif skater in ["diane", "dyan"]:
        if variant == "short":
            return response_play_music("diane_zhou_short.mp3", delay=delay)
        else:
            return response_play_music("diane_zhou_free.mp3", delay=delay)

    else:
        return response_say("Sorry, I can't find " + variant + " program for " + skater)

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