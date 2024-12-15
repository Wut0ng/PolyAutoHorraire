import re
import time
import requests
import datetime


def main():
    config = {
        "name": "",
        "password": "",
        "birth": "",
        "courses": {
            "INF2610": { "T": 1, "L": 1 },
            "INF3405": { "T": 1, "L": 2 },
            "LOG2990": { "T": 1, "L": 2 },
            "MTH2304": { "T": 4, "L": 4 },
            "SSH3501": { "T": 8 }
        }
    }
    
    while True:
        print("New session id", datetime.datetime.now().strftime("%m/%d/%Y %Hh%M"))
        session_id = get_session_id(config["name"], config["password"], config["birth"])
        for _ in range(10):
            current_courses = get_courses(session_id, config["courses"])
            modifications = get_possible_modifications(current_courses, config["courses"])
            if len(modifications) > 0:
                print("-------------------------------------")
                print(datetime.datetime.now().strftime("%m/%d/%Y %Hh%M"))
                print("Possible modification detected:", modifications)
                new_courses = get_new_courses(current_courses, modifications)
                apply_modifications(session_id, new_courses)
                print("-------------------------------------")
            time.sleep(61)


def get_new_courses(current_courses, modifications):
    new_courses = {}

    for key, value in current_courses.items():
        sigle = key
        th_group = "" if value["CT"] == 0 else f"{value["CT"]:02}"
        lab_group = "" if value["CL"] == 0 else f"{value["CL"]:02}"
        new_courses[sigle] = {"T": th_group, "L": lab_group}
    
    for modification in modifications:
        sigle = modification["sigle"]
        type = modification["type"]
        group = modification["group"]
        new_courses[sigle][type] = f"{group:02}"
    
    return new_courses


def get_possible_modifications(current_courses, wanted_courses):
    modifications = []
    for key, value in wanted_courses.items():
        for type in ["T", "L"]:
            wanted_group = value.get(type, 0)
            if wanted_group != 0:
                current_group = current_courses[key][f"C{type}"]
                if wanted_group != current_group:
                    is_change_possible = current_courses[key][type][wanted_group]
                    if is_change_possible:
                        modifications.append({"sigle": key, "type": type, "group": wanted_group})
    return modifications


def get_courses(session_id, course_list):
    courses_text = get_courses_text(session_id)

    courses_dict = {}
    for course_name in course_list.keys():
        course_dict = get_course(course_name, courses_text)
        courses_dict[course_name] = course_dict
    
    return courses_dict


def apply_modifications(session_id, new_courses):
    new_courses_list = [{"sigle": k, "groupe": v} for k, v in new_courses.items()]

    data = {
        "sigle1": new_courses_list[0]["sigle"],
        "grtheo1": new_courses_list[0]["groupe"]["T"],
        "grlab1": new_courses_list[0]["groupe"]["L"],
        "titre1": "NOYAU D'UN SYST. D'EXPLOIT.",
        "credits1": "3",
        "couIndPFE1": "N",
        "I1": "S",
        "sigle2": new_courses_list[1]["sigle"],
        "grtheo2": new_courses_list[1]["groupe"]["T"],
        "grlab2": new_courses_list[1]["groupe"]["L"],
        "titre2": "RESEAUX INFORMATIQUES",
        "credits2": "3",
        "couIndPFE2": "N",
        "I2": "S",
        "sigle3": new_courses_list[2]["sigle"],
        "grtheo3": new_courses_list[2]["groupe"]["T"],
        "grlab3": new_courses_list[2]["groupe"]["L"],
        "titre3": "PROJET LOGICIEL D'APPLIC. WEB",
        "credits3": "4",
        "couIndPFE3": "N",
        "I3": "S",
        "sigle4": new_courses_list[3]["sigle"],
        "grtheo4": new_courses_list[3]["groupe"]["T"],
        "grlab4": new_courses_list[3]["groupe"]["L"],
        "titre4": "PROBABILITES ET STATISTIQUE AP",
        "credits4": "4",
        "couIndPFE4": "N",
        "I4": "S",
        "sigle5": new_courses_list[4]["sigle"],
        "grtheo5": new_courses_list[4]["groupe"]["T"],
        "grlab5": new_courses_list[4]["groupe"]["L"],
        "titre5": "ETHIQUE APPL. A L'INGENIERIE",
        "credits5": "2",
        "couIndPFE5": "N",
        "I5": "S",
        "sigle6": "",
        "grtheo6": "",
        "grlab6": "",
        "titre6": "",
        "credits6": "",
        "couIndPFE6": "",
        "I6": "",
        "sigle7": "",
        "grtheo7": "",
        "grlab7": "",
        "titre7": "",
        "credits7": "",
        "couIndPFE7": "",
        "I7": "",
        "sigle8": "",
        "grtheo8": "",
        "grlab8": "",
        "titre8": "",
        "credits8": "",
        "couIndPFE8": "",
        "I8": "",
        "sigle9": "",
        "grtheo9": "",
        "grlab9": "",
        "titre9": "",
        "credits9": "",
        "couIndPFE9": "",
        "I9": "",
        "sigle10": "",
        "grtheo10": "",
        "grlab10": "",
        "titre10": "",
        "credits10": "",
        "couIndPFE10": "",
        "I10": "",
        "totalCredits": "16",
        "totalCreditsSansPFE": "0",
        "totalCreditsSansPFE": "0",
        "Isigle1": "",
        "Igrtheo1": "",
        "Igrlab1": "",
        "Itype1": "TLS",
        "Isigle2": "",
        "Igrtheo2": "",
        "Igrlab2": "",
        "Itype2": "TLS",
        "Isigle3": "",
        "Igrtheo3": "",
        "Igrlab3": "",
        "Itype3": "TLS",
        "Isigle4": "",
        "Igrtheo4": "",
        "Igrlab4": "",
        "Itype4": "TL ",
        "Isigle5": "",
        "Igrtheo5": "",
        "Igrlab5": "",
        "Itype5": "T  " ,
        "Isigle6": "",
        "Igrtheo6": "",
        "Igrlab6": "",
        "Itype6": "",
        "Isigle7": "",
        "Igrtheo7": "",
        "Igrlab7": "",
        "Itype7": "",
        "Isigle8": "",
        "Igrtheo8": "",
        "Igrlab8": "",
        "Itype8": "",
        "Isigle9": "",
        "Igrtheo9": "",
        "Igrlab9": "",
        "Itype9": "",
        "Isigle10": "",
        "Igrtheo10": "",
        "Igrlab10": "",
        "Itype10": "",
        "W": "",
        "bascule": "I",
        "errinit": "N",
        "credAcc": "042",
        "gr": "BI",
        "secteur": "BA",
        "nb_ligne": "0",
        "matricule": "2299959",
        "token": "",
        "codeDossier": "01",
        "programme": "BIINF",
        "choixProgramme": "",
        "trimestre": "H 2025",
        "dateDebutTrimestre": "",
        "indTempsCompletEte": "N",
        "dateFinTrimestre":  "",
        "choixProgrammeDates": "",
        "choixTrimestre":  "",
        "codeProgrammesNotes": "01",
        "choixTrimestreProp": "",
        "nbr_cours": "5",
        "messagePasOK": " ",
        "trimestreProp": "20251",
        "trimestreModif": "20251",
        "nbreProg": "1",
        "nbreProgActif": "1",
        "nbreCours": "",
        "conflits10": "",
        "conflits11": "",
        "conflits12": "",
        "conflits13": "",
        "trimestreInscription": "20251",
        "chaineTrimInsc": "hiver 2025",
        "chaineTrimModifChoixCours": "hiver 2025",
        "codeStatutActuel": "NINS",
        "enregistrerDisabled": " ",
        "nbInscRecherche": "0",
        "nbreDoss": "",
        "radioInscriptionDisabled": "disabled" ,
        "radioNonInscriptionDisabled": " ",
        "textRadioNonInscription": "NINS",
        "messageInfo": " ",
        "codeProgrammeInsc": "01",
        "conflits14": "",
        "conflits15": "",
        "conflits16": "",
        "conflits17": "",
        "conflits18": "",
        "conflits19": "",
        "conflits20": "",
        "conflits21": "",
        "conflits22": "",
        "conflits23": "",
        "conflits24": "",
        "conflits25": "",
        "conflits26": "",
        "conflits27": "",
        "conflits28": "",
        "conflits29": "",
        "conflits30": "",
        "conflits31": "",
        "conflits32": "",
        "conflits33": "",
        "conflits34": "",
        "conflits35": "",
        "conflits36": "",
        "conflits37": "",
        "conflits38": "",
        "conflits39": "",
        "conflits40": "",
        "conflits41": "",
        "conflits42": "",
        "conflits43": "",
        "conflits44": "",
        "conflits45": "",
        "conflits46": "",
        "conflits47": "",
        "conflits48": "",
        "conflits49": "",
        "conflits50": "",
        "conflits51": "",
        "conflits52": "",
        "conflits53": "",
        "conflits54": "",
        "conflits55": "",
        "conflits56": "",
        "conflits57": "",
        "conflits58": "",
        "conflits59": "",
        "conflits60": "",
        "conflits61": "",
        "conflits62": "",
        "conflits63": "",
        "conflits64": "",
        "conflits65": "",
        "conflits66": "",
        "conflits67": "",
        "conflits68": "",
        "conflits69": "",
        "conflits70": "",
        "conflits71": "",
        "conflits72": "",
        "conflits73": "",
        "conflits74": "",
        "conflits75": "",
        "conflits76": "",
        "conflits77": "",
        "conflits78": "",
        "conflits79": "",
        "conflits80": "",
        "conflits81": "",
        "conflits82": "",
        "conflits83": "",
        "conflits84": "",
        "conflits85": "",
        "conflits86": "",
        "conflits87": "",
        "conflits88": "",
        "conflits89": "",
        "conflits90": "",
        "conflits91": "",
        "conflits92": "",
        "conflits93": "",
        "conflits94": "",
        "conflits95": "",
        "conflits96": "",
        "conflits97": "",
        "conflits98": "",
        "conflits99": "",
        "conflits00": "",
        "conflits01": "",
        "conflits02": "",
        "conflits03": "",
        "conflits04": "",
        "conflits05": "",
        "conflits06": "",
        "conflits07": "",
        "conflits08": "",
        "conflits09": ""
    }

    url = "https://dossieretudiant.polymtl.ca/WebEtudiant7/ModifCoursServlet"
    cookies = {"SERVERID": "de-1-2022", "JSESSIONID": session_id}

    response = requests.post(url=url, data=data, cookies=cookies, allow_redirects=False)

    print(response.status_code)

def get_course(course_name, courses_text):
    matches = re.findall(rf'GC\["{course_name}(.*?)";', courses_text)

    course_dict = {}
    for match in matches:
        splitted_match = match.split('"]="')
        full_group = splitted_match[0]
        if len(full_group) == 3:
            group = int(full_group[:2])
            type = full_group[2]
            disponible = int(splitted_match[1][:3]) > 0
            course_dict.setdefault(type, {})[group] = disponible
    
    isolated_string = re.search(rf'value="{course_name}(.*?)eight columns', courses_text).group(1)
    current_matches = re.findall(r'value="(.*?)"', isolated_string)

    course_dict["CT"] = int("0" + current_matches[0])
    course_dict["CL"] = int("0" + current_matches[1])
    
    return course_dict


def get_courses_text(session_id):
    data = {
        "selProgInscrit": "01",
        "selProgBulletinCumulatif": "01",
        "selProgHorPers": "01",
        "selTrimHorPers": "20251",
        "numDossierHoraire": "01",
        "trimHoraire": "20251",
        "selProgModif": "01",
        "selProgAttestation": "",
        "selTrimestreAttestation": "",
        "stProgRensPers": "",
        "stProgResAcad": "",
        "stProgHorPers": "",
        "stTrimHorPers": "",
        "stProgPropo": "",
        "stProgModif": "",
        "stProgStage": "",
        "stProgPlan": "",
        "token": "",
        "matricule": "2299959",
        "choixProgramme": "",
        "dateDebutTrimestre": "",
        "choixProgrammeDates": "",
        "codeDossier": "01",
        "dateFinTrimestre": "",
        "trimestreActuel": "",
        "choixTrimestre": "",
        "messagePasOK": "",
        "trimestreModif": "20251",
        "trimestreProp": "20251",
        "anneeCollation": "",
        "codeProgrammesBulletin": "01",
        "codeProgrammesNotes": "",
        "codeProgrammesHoraire": "01",
        "codeProgrammeInsc": "1",
        "trimestre": "20251",
        "codeProgrammesProposition": "",
        "codeProgrammesPlan": "",
        "codeProgrammesModification": "01",
        "nbreDoss": "1",
        "nbreDossES": "0",
        "nbreDossStage": "",
        "nbreDossActif": "1",
        "nbreTrim": "5",
        "trimestreAttestation": "",
        "dateRelAnt": "Choisir",
        "trimestreInscription": "20251",
        "codeStatutActuel": "NINS",
        "chaineTrimInsc": "hiver 2025",
        "chaineTrimModifChoixCours": "hiver 2025",
        "nbInscRecherche": "0",
        "selectionMandat": "",
        "selectionMandat1": "",
        "selectionMandat2": "",
        "selectionMandat3": "",
        "selectionMandat4": "",
        "selectionMandat5": "",
        "selectionMandat6": "",
        "selectionMandat7": "",
        "selectionMandat8": "",
        "selectionMandat9": "",
        "selectionMandat10": "",
        "messagePopup": "",
        "conflits10": "",
        "conflits11": "",
        "conflits12": "",
        "conflits13": "",
        "conflits14": "",
        "conflits15": "",
        "conflits16": "",
        "conflits17": "",
        "conflits18": "",
        "conflits19": "",
        "conflits20": "",
        "conflits21": "",
        "conflits22": "",
        "conflits23": "",
        "conflits24": "",
        "conflits25": "",
        "conflits26": "",
        "conflits27": "",
        "conflits28": "",
        "conflits29": "",
        "conflits30": "",
        "conflits31": "",
        "conflits32": "",
        "conflits33": "",
        "conflits34": "",
        "conflits35": "",
        "conflits36": "",
        "conflits37": "",
        "conflits38": "",
        "conflits39": "",
        "conflits40": "",
        "conflits41": "",
        "conflits42": "",
        "conflits43": "",
        "conflits44": "",
        "conflits45": "",
        "conflits46": "",
        "conflits47": "",
        "conflits48": "",
        "conflits49": "",
        "conflits50": "",
        "conflits51": "",
        "conflits52": "",
        "conflits53": "",
        "conflits54": "",
        "conflits55": "",
        "conflits56": "",
        "conflits57": "",
        "conflits58": "",
        "conflits59": "",
        "conflits60": "",
        "conflits61": "",
        "conflits62": "",
        "conflits63": "",
        "conflits64": "",
        "conflits65": "",
        "conflits66": "",
        "conflits67": "",
        "conflits68": "",
        "conflits69": "",
        "conflits70": "",
        "conflits71": "",
        "conflits72": "",
        "conflits73": "",
        "conflits74": "",
        "conflits75": "",
        "conflits76": "",
        "conflits77": "",
        "conflits78": "",
        "conflits79": "",
        "conflits80": "",
        "conflits81": "",
        "conflits82": "",
        "conflits83": "",
        "conflits84": "",
        "conflits85": "",
        "conflits86": "",
        "conflits87": "",
        "conflits88": "",
        "conflits89": "",
        "conflits90": "",
        "conflits91": "",
        "conflits92": "",
        "conflits93": "",
        "conflits94": "",
        "conflits95": "",
        "conflits96": "",
        "conflits97": "",
        "conflits98": "",
        "conflits99": "",
        "conflits00": "",
        "conflits01": "",
        "conflits02": "",
        "conflits03": "",
        "conflits04": "",
        "conflits05": "",
        "conflits06": "",
        "conflits07": "",
        "conflits08": "",
        "conflits09": "",
    }

    url = "https://dossieretudiant.polymtl.ca/WebEtudiant7/ChoixCoursServlet"
    cookies = {"SERVERID": "de-1-2022", "JSESSIONID": session_id}

    response = requests.post(url=url, data=data, cookies=cookies)

    return response.text


def get_session_id(name, password, birth):
    url = "https://dossieretudiant.polymtl.ca/WebEtudiant7/ValidationServlet"
    data = {"code": name, "nip": password, "naissance": birth}
    cookies = {"SERVERID": "de-1-2022"}

    response = requests.post(url=url, data=data, cookies=cookies, allow_redirects=False)
    if response.status_code != 302:
        raise ValueError(f"Login failed: {response.status_code}\n{response.text}")
    session_id = response.cookies.get("JSESSIONID")

    if not session_id:
        raise ValueError(f"Login failed: {response.status_code}\n{response.text}")
    
    return session_id


if __name__ == "__main__":
    main()
