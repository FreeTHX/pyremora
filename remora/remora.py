import aiohttp
import asyncio
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

    async def getUptime(self) -> str:
        async with aiohttp.request('GET', self.baseurl + 'uptime') as uptime:
            # uptime return an invalid content_type (text/json)
            return (await uptime.json(content_type=None))['uptime']

    async def getTeleInfo(self) -> dict:
        async with aiohttp.request('GET', self.baseurl + 'tinfo') as tinfo:
            return (await tinfo.json())

    async def getTeleInfoEtiquette(self, etiquette: str) -> str:
        async with aiohttp.request('GET', self.baseurl + etiquette) as tinfoEtiquette:
            if tinfoEtiquette.status == 404:
                return None
            return (await tinfoEtiquette.json())[etiquette]

    async def getRelais(self) -> dict:
        async with aiohttp.request('GET', self.baseurl + 'relais') as relais:
            rjson = await relais.json()
            return { 
                'relais'      : RelaisEtat(rjson['relais']),
                'fnct_relais' : RelaisMode( rjson['fnct_relais']) }

    async def getDelestage(self) -> dict:
        async with aiohttp.request('GET', self.baseurl + 'delestage') as delestage:
            return (await delestage.json())

    async def getAllFilPilote(self) -> dict:
        async with aiohttp.request('GET', self.baseurl + 'fp') as fp:
            fpjson = await fp.json()
            fpresult = {}
            for k, v in fpjson.items():
                fpresult[k] = FpMode(v)
            return fpresult
    
    async def getFilPilote(self, num: int) -> str:
        async with aiohttp.request('GET', self.baseurl + 'fp' + str(num)) as fpX:
            if fpX.status_code == 404:
                return None
            return (await FpMode(fpX.json())['fp'+ str(num)])

    async def setAllFilPilote(self, listMode) -> bool:
        cmd = ''
        for m in listMode:
            if isinstance(m, FpMode):
                cmd += m.value
            elif isinstance(m, str) and \
                 m.upper() in [mode.value.upper() for mode in FpMode]:
                cmd += m.upper()
            else:
                cmd += '-'
        async with aiohttp.request('GET', self.baseurl, params = { 'fp' : cmd }) as fp:
            return (await fp.json())['response'] == 0

    async def setFilPilote(self, num: int, mode: FpMode) -> bool:
        async with aiohttp.request('GET', self.baseurl, params = { 'setfp' : str(num) + mode.value }) as setfpX:
            return (await setfpX.json())['response'] == 0

    async def setRelais(self, state: RelaisEtat) -> bool:
        async with aiohttp.request('GET', self.baseurl, params = { 'relais' : str(state.value) }) as setr:
            return (await setr.json())['response'] == 0

    async def setFnctRelais(self, mode: RelaisMode) -> bool:
        async with aiohttp.request('GET', self.baseurl, params = { 'frelais' : str(mode.value) }) as setfr:
            return (await setfr.json())['response'] == 0

    async def reset(self) -> bool:
        try:
            async with aiohttp.request('GET', self.baseurl + 'reset', timeout=aiohttp.ClientTimeout(total=3)):
                return True
        except (aiohttp.ServerTimeoutError, aiohttp.client_exceptions.ClientOSError, asyncio.TimeoutError):
            pass
        return True

    async def factoryReset(self, areYouSure) -> bool:
        if( areYouSure == True ):
            try:
                async with aiohttp.request('GET', self.baseurl + 'factory_reset', timeout=aiohttp.ClientTimeout(total=3)):
                    return True
            except (aiohttp.ServerTimeoutError, aiohttp.client_exceptions.ClientOSError, asyncio.TimeoutError):
                pass
            return True
        else:
            return False
