import json
def enjosn(opcode,username,uerid,passwd,notes,registpw):
      dict1 = [{'caozuoma': opcode, 'username':username , 's1': uerid,'s2':passwd,'beizhu':notes,'passwd':registpw}]
#  python编码为json类型，json.dumps()
      en_json = json.dumps(dict1)
      return en_json
def dejosn(sjson):
      de_json = json.loads(sjson)
      return de_json