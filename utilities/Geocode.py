import requests
import json

def geocode(sch, SingleLineInput="", outFields="Match_addr", outSR="4326"):
    """
    Geocode Jefferson county addresses
    Uses http://jeffco.us/ArcGIS/rest/services/sch/GeocodeServer/findAddressCandidates
    Returns Lat Lon of the first 100% match, if no 100% match returns None
    Usage:
    sch : Jeffco property schedule number accepted formats 5123, 005123, "5123", "005123"
    outSR : Using "4326" returns lat lon
    """
    sch = str(sch).zfill(6)
    f = "pjson"
    URL = "http://jeffco.us/ArcGIS/rest/services/sch/GeocodeServer/findAddressCandidates?"
    payload = ({"SingleKey" : sch,
                "Single Line Input" : SingleLineInput,
                "outFields" : outFields,
                "outSR" : outSR,
                "f" : f,
                "submit" : "Find"})
    data = json.loads(requests.post(URL, data=payload).text)
    try:
        score = data['candidates'][0]['score']
        if score == 100:
            return (data['candidates'][0]['location']['y'], data['candidates'][0]['location']['x'])
        else:
            return None
    except:
        return None