from midjourney_api import MidjourneyApi

prompt = 'a humanoid frog looking under the water looking at his reflection on the surface, pondering life and why he stays underwater when he could go above the surface'
authorization = 'NTcwMjgwMTcxMzI0ODMzODEz.GNZXyC.kDueMI3_8Vd1RN_Glz9MTD5RFv3OhU1qhgh_J0'
application_id = '936929561302675456'
guild_id = '884622163146059826'
channel_id = '1201996275160191027'
version = '1166847114203123795'
id = '938956540159881230'

midjourney = MidjourneyApi(prompt=prompt, application_id=application_id, guild_id=guild_id, channel_id=channel_id, version=version, id=id, authorization=authorization)