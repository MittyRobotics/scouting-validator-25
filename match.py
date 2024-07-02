import requests
import json

matchnum = 77
event_key = "2024casj"
match_key = f"{event_key}_qm{matchnum}"
url="https://www.thebluealliance.com/api/v3"
url += f"/match/{match_key}"
tba = requests.get(url, headers={"X-TBA-Auth-Key":"ingmesQTeprOTbKZRvexSACtqw6bSSdF5WLBiJdbdw38OQAtikq0Rz5MOIYFtR4z"})
red_recorded = 0
blue_recorded = 0
bluescore = 0
redscore = 0
red_real = 0
blue_real = 0
data = json.loads(json.dumps(tba.json()))

#function to add values from our data (hope this works)
def add_score(key, value):
        score = 0
        if(key in ['AUTONAMP', 'TELEOPSPEAKER']):
            score += (int(value)*2)
        if(key == 'AUTONSPEAKER'):
            score += (int(value)*5)
        if(key == 'TELEOPAMP'):
            score += (int(value))
        if(key == 'TRAP' and value == 'true'):
            score += 5
        if(key == 'ENDGAME'):
            if(value == 'Parked'):
                score += 1
            if(value == 'Onstage'):
                score += 3
        return score

#function to calculate score from official API 
def calc_score(autoAmp, autoSpe, teleAmp, teleSpe, teleSpeAmp, trap, park, onstage):
        score = 0
        teleSpe += teleSpeAmp
        score += (autoAmp*2) + (autoSpe*5) + (teleAmp) + (teleSpe*2) + trap + park + onstage
        return score

blue_real = calc_score(data['score_breakdown']['blue']['autoAmpNoteCount'], 
                        data['score_breakdown']['blue']['autoSpeakerNoteCount'],
                        data['score_breakdown']['blue']['teleopAmpNoteCount'],
                        data['score_breakdown']['blue']['teleopSpeakerNoteCount'],
                        data['score_breakdown']['blue']['teleopSpeakerNoteAmplifiedCount'],
                        data['score_breakdown']['blue']['endGameNoteInTrapPoints'],
                        data['score_breakdown']['blue']['endGameParkPoints'],
                        data['score_breakdown']['blue']['endGameOnStagePoints'])
red_real = calc_score(data['score_breakdown']['red']['autoAmpNoteCount'], 
                        data['score_breakdown']['red']['autoSpeakerNoteCount'],
                        data['score_breakdown']['red']['teleopAmpNoteCount'],
                        data['score_breakdown']['red']['teleopSpeakerNoteCount'],
                        data['score_breakdown']['red']['teleopSpeakerNoteAmplifiedCount'],
                        data['score_breakdown']['red']['endGameNoteInTrapPoints'],
                        data['score_breakdown']['red']['endGameParkPoints'],
                        data['score_breakdown']['red']['endGameOnStagePoints'])

blueerror = ((blue_real - blue_recorded)/blue_recorded) * 100
rederror = ((red_real - red_recorded)/red_recorded) * 100