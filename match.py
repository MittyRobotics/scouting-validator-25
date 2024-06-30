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

#function to calculate score from official API 
def calc_score(autoAmp, autoSpe, teleAmp, teleSpe, teleSpeAmp, trap, park, onstage):
        score = 0
        teleSpe += teleSpeAmp
        score += (autoAmp*2) + (autoSpe*5) + (teleAmp) + (teleSpe*2) + trap + park + onstage
        return score