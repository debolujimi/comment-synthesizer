import re

import nltk
from nltk.corpus import wordnet


DICT_INTENT = {
    "intents": [
        {
            "tag": "Alert",
            "responses": "Eskom power system is under severe pressure. Please switch off all unnecessary lights, your geyser, pool pump, and non-essential appliances. Thank you!",
            "synonyms": {
                "Switch off", "geyser", "Pool pumps", "Appliances", "Severe pressure",
                "switch off your geyser", "switch off appliances", "save electricity",
                "conserve energy", "reduce usage", "turn off lights", "power alert",
                "usage alert", "electricity alert", "pressure on the grid"
            },
        },
        {
            "tag": "Anger",
            "responses": "Eskom is implementing efforts to restore energy supply. We apologise for the inconvenience caused.",
            "synonyms": {
                "sucks", "what the hell", "wtf", "ffs", "fuck", "hell", "fucking", "futsek",
                "nje", "tired", "voetsek", "fvcken tired", "protestors", "corrupt", "nonsense",
                "idiots", "eish", "fuck eskom", "protest", "shit", "damn it", "stupid", "angry",
                "incompetent bullshit", "fuck off", "mad", "why is eskom doing this",
                "eskom is useless", "eskom is pathetic", "eskom is failing", "this is ridiculous",
                "this is unacceptable", "very angry", "fed up", "disgraceful"
            },
        },
        {
            "tag": "App",
            "responses": "Eskom customers can download their loadshedding schedules from loadshedding.eskom.co.za or on the MyEskom App.",
            "synonyms": {
                "EskomSePush", "app", "Schedule", "MyEskom App", "Schedules",
                "loadshedding app", "my eskom app", "eskom app", "schedule app",
                "eskom schedule", "load shedding schedule", "eskom schedules", "schedule download"
            },
        },
        {
            "tag": "Appreciation",
            "responses": "Thank you for reiterating our commitment to always providing excellent service!",
            "synonyms": {
                "major strides", "good strides", "amazing", "celebrate", "remarkable", "better",
                "power restored", "no more loadshedding", "thank you", "gratitude", "well done",
                "appreciate the effort", "well done eskom", "great work", "excellent service",
                "good job", "thank you eskom", "good work", "more stable power",
                "power is back", "much appreciated"
            },
        },
        {
            "tag": "Cable",
            "responses": "Cable theft is one of the main reasons for constant power outages. Report cable theft to @SAPoliceService/Eskom Crime Line 0800 11 27 22 (toll-free) or to your local municipality.",
            "synonyms": {
                "stolen cable", "Theft", "Cable Theft", "stealing", "stolen", "steal", "stole",
                "Arrest", "copper cables", "Arrested", "cable theft", "stole copper",
                "stolen cables", "power lines stolen", "copper theft", "vandalised cables",
                "thieves stole cable", "cable sabotage"
            },
        },
        {
            "tag": "Coal",
            "responses": "The anti-pollution system would increase the plant’s water consumption and increase carbon dioxide emissions.",
            "synonyms": {"Emmissions", "Pollution", "Coal-fine"},
        },
        {
            "tag": "Debt",
            "responses": "The rising electricity debt is crippling Eskom power utility’s service delivery programme. Please, pay your bills!",
            "synonyms": {
                "Arrears", "Overdue", "Bills", "debt", "Owes", "Owed", "Debts",
                "electricity debt", "bill", "arrears account", "outstanding balance",
                "overdue account", "payment due", "pay your bill", "owning electricity"
            },
        },
        {
            "tag": "Financial",
            "responses": "This is not where we want to be as Eskom to ensure sustainability, but it’s a great start in the right direction.",
            "synonyms": {"Profit", "Interim report"},
        },
        {
            "tag": "Illegal",
            "responses": "Buying illegal electricity vouchers and illegal connections is a crime. Consumers that are using illegal prepaid electricity vouchers will be disconnected and fined. Eskom encourages communities to play an active role in curbing these atrocities. Report ghost vendors and illegal connections to Eskom Crime Line on 0800 112722.",
            "synonyms": {"Illegal vouchers", "Illegal connections", "Illegal electricity"},
        },
        {
            "tag": "Lights out",
            "responses": "Eskom is implementing efforts to restore energy supply. The estimated time of restoration is currently unknown. We apologise for the inconvenience caused.",
            "synonyms": {
                "Electricity shortage", "Electricity", "Electricity cut", "Lights", "Light", "Power",
                "Energy", "Current", "Voltage", "No electricity", "no power", "electricity shortage",
                "shortage of electricity", "without electricy", "no light", "unacceptable", "without power",
                "dark", "darkness", "no power supply", "out of electricity", "blackout", "stuck in darkness",
                "lights are out", "there is no electricity", "no lights", "power failure", "electricity off",
                "power gone", "dark at home", "no voltage"
            },
        },
        {
            "tag": "Loadshedding",
            "responses": "Please visit loadshedding.Eskom.co.za at any moment to see the current loadshedding status. We apologise for the inconvenience caused. Thank you!",
            "synonyms": {
                "Loadshedding again", "Eskom loadshedding", "Load shedding", "Load reduction",
                "loadshedded", "Load-shedding", "Loadshed", "Loadsheded", "loadshed",
                "load shed", "stage 2", "stage two", "load shedding stage 2", "load shedding again",
                "eskom has started loadshedding", "loadsheding", "load shedding in my area",
                "why is there loadshedding", "there is loadshed", "loadshed schedule"
            },
        },
        {
            "tag": "Maintenance",
            "responses": "Eskom is implementing efforts to achieve operational stability and to restore the security of energy supply for the country. We apologise for the inconvenience caused.",
            "synonyms": {"Replacement", "Koeberg Unit 2", "Maintenances", "Koeberg"},
        },
        {
            "tag": "Outages",
            "responses": "We are attending to an outage affecting customers in your area. The estimated time of restoration is currently unknown. We apologise for the inconvenience caused.",
            "synonyms": {
                "Power outage", "Power cuts", "Power outages", "Black out", "Power cut", "outage",
                "Power trip", "Power failure", "Power off", "powercut", "power outage in my area",
                "area outage", "outage in my area", "outage again", "electricity outage",
                "there is a blackout", "power restoration", "no power in area", "trip again"
            },
        },
        {
            "tag": "Price",
            "responses": "The price hike is partly being driven by purchases from independent power producers (IPPs) and carbon taxes – two costs that are outside of Eskom\"s direct control",
            "synonyms": {
                "Increase", "Increases", "Tariffs", "Prices", "Price hikes", "Tariffincrease", "Hikes",
                "Tariff hike", "NERSA", "20.5%", "Price hike", "Tariff application", "Units",
                "1 April", "Rate hikes", "Tariff increase", "electricity pricelist", "price increase",
                "electricity cost", "more expensive electricity", "tariff hike", "expensive electricity"
            },
        },
        {
            "tag": "Stage",
            "responses": "Eskom has used significant amounts of its energy reserves. These reserves have been depleted and now need to be replenished. We apologise for the inconvenience caused.",
            "synonyms": {"2nd stage", "Stages", "stage", "stage 2", "stage two", "stage 4", "stage 6", "stage 1", "stage 3", "stages 2"},
        },
        {
            "tag": "Suspension",
            "responses": "Loadshedding will be suspended as generation capacity sufficiently recovers. We thank you for support and patience during the loadshedding.",
            "synonyms": {"Suspended", "Suspend", "Suspending", "not loadshedding", "loadshedding suspended", "suspended again", "power back", "restored"},
        },
        {
            "tag": "Usage",
            "responses": "We urge all customers to help reduce electricity usage in order to ease the pressure on the system. Thank you!",
            "synonyms": {"Consumption", "Reduce usage", "usage", "Generation usage", "system", "electricity usage", "power consumption", "reduce power", "save electricity", "energy usage"},
        },
        {
            "tag": "Vandalism",
            "responses": "Eskom losing millions of rands to vandalism & infrastructure theft, communities are inconvenienced when their electricity supply is interrupted. It is a criminal offence to damage Eskom\"s property. Report offenders to the local @SAPoliceService or Eskom on 0800 11 27 22",
            "synonyms": {"Sabotage", "Damage", "Missing towers", "Explosion", "Transformer", "stolen transformer", "damaged substation", "tower vandalism", "infrastructure theft", "vandalised equipment"},
        },
        {
            "tag": "Warning",
            "responses": "Eskom had the lowest unplanned capacity loss in a very long time, which was a positive reflection on the performance of the system. However, we are implementing efforts to achieve operational stability and restore the security of the energy supply for the country.",
            "synonyms": {"Warns", "warning", "Risk", "Warn", "Exposure", "Jeopardy", "Risks", "high risk", "warning notice", "electricity risk", "system warning", "alert notice"},
        },
    ]
}


def _normalize_text(value):
    cleaned = str(value).lower().strip()
    cleaned = cleaned.replace("-", " ")
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _keyword_variants(phrase):
    base = _normalize_text(phrase)
    variants = {base}
    if not base:
        return variants

    variants.add(base.replace(" ", ""))

    words = base.split()
    if len(words) > 1:
        joined = "".join(words)
        variants.add(joined)
        variants.add(" ".join(words))

    replacements = {
        " load shedding ": " loadshedding ",
        " load shed ": " loadshedding ",
        " power cut ": " power outage ",
        " power cuts ": " power outage ",
        " lights out ": " no power ",
        " no electricity ": " electricity off ",
        " powercut ": " power outage ",
        " loadshed ": " loadshedding ",
        " loadsheding ": " loadshedding ",
        " black out ": " power outage ",
        " no lights ": " no electricity ",
        " no power ": " electricity off ",
    }

    for source, target in replacements.items():
        if source in f" {base} ":
            cleaned = _normalize_text(base.replace(source.strip(), target.strip()))
            if cleaned:
                variants.add(cleaned)
                variants.add(cleaned.replace(" ", ""))

    return {item for item in variants if item.strip()}


def _build_keyword_map():
    keyword_map = {}
    for intent in DICT_INTENT["intents"]:
        tag = intent["tag"]
        synonyms = {tag.lower()}

        try:
            synsets = wordnet.synsets(tag)
        except LookupError:
            # WordNet enrichment is optional. The curated synonym set below
            # keeps the response engine functional in offline installations.
            synsets = []

        for syn in synsets:
            for lemma in syn.lemmas():
                cleaned = _normalize_text(lemma.name())
                if cleaned:
                    synonyms.add(cleaned)

        for synonym in intent.get("synonyms", []):
            for variant in _keyword_variants(synonym):
                synonyms.add(variant)

        synonyms = {item for item in synonyms if item.strip()}
        pattern_parts = []
        for synonym in sorted(synonyms, key=len, reverse=True):
            pattern_parts.append(r"\b" + re.escape(synonym.strip()) + r"\b")

        regex = "|".join(pattern_parts)
        if not regex:
            regex = r"\b\b"
        keyword_map[tag] = re.compile(regex, re.IGNORECASE)

    return keyword_map


KEYWORDS_DICT = _build_keyword_map()
RESPONSE_DICT = {intent["tag"]: intent["responses"] for intent in DICT_INTENT["intents"]}
RESPONSE_DICT["Unrelated messages"] = (
    "We are currently unable to match that message to a specific Eskom issue. "
    "Please try a message about loadshedding, outages, power cuts, billing, or electricity usage."
)


def _fallback_response(message):
    text = _normalize_text(message)
    if not text:
        return RESPONSE_DICT["Unrelated messages"]

    if any(word in text for word in ["thank", "appreciate", "well done", "good work", "great work"]):
        return RESPONSE_DICT["Appreciation"]
    if any(word in text for word in ["angry", "fed up", "ridiculous", "unacceptable", "annoyed", "sucks", "mad"]):
        return RESPONSE_DICT["Anger"]
    if any(word in text for word in ["billing", "bill", "debt", "arrears", "account", "payment"]):
        return RESPONSE_DICT["Debt"]
    if any(word in text for word in ["load shed", "loadshedding", "loadshed", "stage", "power cut"]):
        return RESPONSE_DICT["Loadshedding"]
    if any(word in text for word in ["outage", "blackout", "no power", "power failure", "trip"]):
        return RESPONSE_DICT["Outages"]
    if any(word in text for word in ["electricity", "light", "power", "no lights", "dark"]):
        return RESPONSE_DICT["Lights out"]
    return RESPONSE_DICT["Unrelated messages"]


def _score_match(cleaned_input, intent, pattern):
    score = 0
    for match in pattern.finditer(cleaned_input):
        matched_text = match.group(0)
        score += len(matched_text) * 2

    if intent == "Loadshedding" and any(word in cleaned_input for word in ["loadshedding", "loadshed", "stage", "scheduled outage"]):
        score += 8
    if intent == "Outages" and any(word in cleaned_input for word in ["outage", "blackout", "power failure", "trip"]):
        score += 8
    if intent == "Lights out" and any(word in cleaned_input for word in ["no electricity", "no power", "lights out", "dark"]):
        score += 8
    if intent == "Debt" and any(word in cleaned_input for word in ["bill", "debt", "arrears", "account", "payment"]):
        score += 8
    return score


def translate_chat(user_input):
    """Return the best matching Eskom response for a tweet/message."""
    if user_input is None:
        return RESPONSE_DICT["Unrelated messages"]

    cleaned_input = _normalize_text(user_input)
    if not cleaned_input:
        return RESPONSE_DICT["Unrelated messages"]

    matched_intent = None
    best_score = -1

    for intent, pattern in KEYWORDS_DICT.items():
        score = _score_match(cleaned_input, intent, pattern)
        if score > best_score:
            matched_intent = intent
            best_score = score

    if matched_intent is None or best_score <= 0:
        return _fallback_response(cleaned_input)

    key = matched_intent if matched_intent in RESPONSE_DICT else "Unrelated messages"
    return "Suggested response template: " + RESPONSE_DICT[key]
