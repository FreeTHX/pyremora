import requests
from enum import Enum


class FpMode(Enum):
    Confort = 'C'
    Arrêt = 'A'
    Eco = 'E'
    HorsGel = 'H'
    Délestage = 'D'
    Eco1 = '1'
    Eco2 = '2'   
   
class RelaisMode(Enum):
        Arrêt = 0
        MarcheForcée = 1
        Automatique = 2

class RelaisEtat(Enum):
        Ouvert = 0
        Fermé = 1
        

# Remora Device : Main class to call the Remora API
#                 Classe principale pour les appels à l'API
class RemoraDevice:

    # Constructeur
    def __init__(self,host):
        self.baseurl = 'http://' + host + '/'

    def getUptime(self):
        uptime = requests.get(self.baseurl + 'uptime')
        return uptime.json()['uptime']

    def getTeleInfo(self):
        tinfo = requests.get(self.baseurl + 'tinfo')
        return tinfo.json()

    def getTeleInfoEtiquette(self, etiquette: str):
        tinfoEtiquette = requests.get(self.baseurl + etiquette)
        if tinfoEtiquette.status_code == requests.codes.not_found:
            return None
        return tinfoEtiquette.json()[etiquette]

    def getRelais(self):
        relais = requests.get(self.baseurl + 'relais')
        return { 'relais'      : RelaisEtat(relais.json()['relais']),
                 'fnct_relais' : RelaisMode( relais.json()['fnct_relais']) }

    def getDelestage(self):
        delestage = requests.get(self.baseurl + 'delestage')
        return delestage.json()

    def getAllFilPilote(self):
        fp = requests.get(self.baseurl +  'fp')
        fpjson = fp.json()
        fpresult = {}
        for k, v in fpjson.items():
            fpresult[k] = FpMode(v)
        return fpresult
    
    def getFilPilote(self, num: int):
        fpX = requests.get(self.baseurl + 'fp' + str(num))
        if fpX.status_code == requests.codes.not_found:
            return None
        return FpMode(fpX.json()['fp'+ str(num)])

    def setAllFilPilote(self, listMode):
        cmd = ''
        for m in listMode:
            if isinstance(m, FpMode):
                cmd += m.value
            elif isinstance(m, str) and \
                 m.upper() in [mode.value.upper() for mode in FpMode]:
                cmd += m.upper()
            else:
                cmd += '-'
        print(cmd)
        fp = requests.get(self.baseurl + '?fp=' + cmd)
        return fp.json()['response'] == 0

    def setFilPilote(self, num: int, mode: FpMode):
        setfpX = requests.get(self.baseurl + '?setfp=' + str(num) + mode.value)
        return setfpX.json()['response'] == 0

    def setRelais(self, state: RelaisEtat):
        setr = requests.get(self.baseurl + '?relais=' + str(state.value))
        return setr.json()['response'] == 0

    def setFnctRelais(self, mode: RelaisMode):
        setfr = requests.get(self.baseurl + '?frelais=' + str(mode.value))
        return setfr.json()['response'] == 0

    def reset(self):
        try:
            reset = requests.get(self.baseurl + 'reset', timeout=3)
        except requests.exceptions.Timeout:
            pass
        return True

    def factoryReset(self, areYouSure):
        if( areYouSure == True ):
            try:
                reset = requests.get(self.baseurl + 'factory_reset', timeout=3)
            except requests.exceptions.Timeout:
                pass
            return True
        else:
            return False
