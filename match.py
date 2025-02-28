import requests
import json
import os

matchnum = 1
matchend = 3
event_key = "2025week0"

red_recorded = 0
blue_recorded = 0
red_real = 0
blue_real = 0


#colo: red, blue
#per: auto, teleop
#lvl: bot, mid, top
def add_nodes(dict):
    return sum(value is True for value in dict.values())  

#function to calculate score from official API 
def calc_score(ac1, ac2, ac3, ac4, tc1, tc2, tc3, tc4, algae, end):
    score = 0
    score += (ac1*3) + (ac2*4) + (ac3*6) + (ac4*7) + (tc1*2) + (tc2*3) + (tc3*4) + (tc4*5) + algae + end
    return score


#function to add values from our data (hope this works)
def add_score(key, value):
        score = 0
        if(key in ['AUTONCORAL1', 'TELECORAL2']):
            score += (int(value)*3)
        if(key in ['AUTONCORAL2', 'TELECORAL3']):
            score += (int(value)*4)
        if(key == 'TELECORAL1'):
            score += (int(value)*2)
        if(key == 'TELECORAL4'):
            score += (int(value)*5)
        if(key == 'AUTONCORAL3'):
            score += (int(value)*6)
        if(key == 'AUTONCORAL4'):
            score += (int(value)*7)
        if(key in ['AUTONALGAEPRO', 'TELEALGAEPRO']):
            score += (int(value)*6)
        if(key in ['AUTONALGAENET', 'TELEALGAENET']):
            score += (int(value)*4)
        if(key == 'ENDGAME'):
            if(value == 'Parked'):
                score += 2
            if(value == 'Shallow'):
                score += 6
            if(value == 'Deep'):
                score += 12
        return score

def parse_txt_files(folder_path):
    scores = {'Blue': 0, 'Red': 0}
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                team_color = None
                match_score = 0          
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        if key == "COLOR":
                            if value in scores:  
                                team_color = value
                        else:
                            match_score += add_score(key, value)
                
                if team_color:
                    scores[team_color] += match_score 
    
    return scores

def parse_all_matches(parent_folder):
    match_scores = {}
    for match_folder in os.listdir(parent_folder):
        match_path = os.path.join(parent_folder, match_folder)
        if os.path.isdir(match_path):  # Ensure it's a folder
            match_scores[match_folder] = parse_txt_files(match_path)
    return match_scores

parent_folder = "/Users/celinelou/reefscape validator/matches"  

scores = parse_all_matches(parent_folder)


while (matchnum <= matchend):
    match_key = f"{event_key}_qm{matchnum}"
    url="https://www.thebluealliance.com/api/v3"
    url += f"/match/{match_key}"
    tba = requests.get(url, headers={"X-TBA-Auth-Key":"ingmesQTeprOTbKZRvexSACtqw6bSSdF5WLBiJdbdw38OQAtikq0Rz5MOIYFtR4z"})
    data = json.loads(json.dumps(tba.json()))
    blue_real = calc_score(data['score_breakdown']['blue']['autoReef']['trough'],
                        add_nodes(data['score_breakdown']['blue']['autoReef']['botRow']),
                        add_nodes(data['score_breakdown']['blue']['autoReef']['midRow']),
                        add_nodes(data['score_breakdown']['blue']['autoReef']['topRow']),
                        data['score_breakdown']['blue']['teleopReef']['trough'],
                        add_nodes(data['score_breakdown']['blue']['teleopReef']['botRow']),
                        add_nodes(data['score_breakdown']['blue']['teleopReef']['midRow']),
                        add_nodes(data['score_breakdown']['blue']['teleopReef']['topRow']),
                        data['score_breakdown']['blue']['algaePoints'],
                        data['score_breakdown']['blue']['endGameBargePoints'])

    red_real = calc_score(data['score_breakdown']['red']['autoReef']['trough'],
                        add_nodes(data['score_breakdown']['red']['autoReef']['botRow']),
                        add_nodes(data['score_breakdown']['red']['autoReef']['midRow']),
                        add_nodes(data['score_breakdown']['red']['autoReef']['topRow']),
                        data['score_breakdown']['red']['teleopReef']['trough'],
                        add_nodes(data['score_breakdown']['red']['teleopReef']['botRow']),
                        add_nodes(data['score_breakdown']['red']['teleopReef']['midRow']),
                        add_nodes(data['score_breakdown']['red']['teleopReef']['topRow']),
                        data['score_breakdown']['red']['algaePoints'],
                        data['score_breakdown']['red']['endGameBargePoints'])

    mstring = f"match{matchnum}"
    # Print the real and recorded scores for comparison
    print(f"Match {matchnum}:")
    blue_recorded = scores[f"match{matchnum}"]['Blue']
    red_recorded = scores[f"match{matchnum}"]['Red']
    
    print(f"Recorded Blue: {blue_recorded}, Real Blue: {blue_real}")
    print(f"Recorded Red: {red_recorded}, Real Red: {red_real}")

    blue_error = ((blue_recorded - blue_real) / blue_real) * 100
    red_error = ((red_recorded - red_real) / red_real) * 100
    
    print(f"Match {matchnum} - Blue error: {blue_error}%")
    print(f"Match {matchnum} - Red error: {red_error}%")

    matchnum += 1
    
