from pandas.io.pytables import IndexCol
import requests
from xml.etree import ElementTree
import pandas

def get_data(payload):
    req = requests.post(url="http://localhost:9000", data=payload)
    res = req.text.encode("UTF-8")
    #print(res)
    return res

def get_payload(fromdate, todate, ledger):
    xml = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>DATA</TYPE>"
    xml += "<ID>LedgerVouchers</ID></HEADER><BODY><DESC><STATICVARIABLES>"
    xml += "<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT><LEDGERNAME>"+ledger+"</LEDGERNAME><EXPLODEVNUM>YES</EXPLODEVNUM></STATICVARIABLES><TDL>"
    xml += "<TDLMESSAGE><REPORT Name='LedgerVouchers' ISMODIFY='Yes'><SET>SVFROMDATE:"+"'"+fromdate+"'"+"</SET>"
    xml += "<SET>SVTODATE:"+"'"+todate+"'"+"</SET></REPORT></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"
    return xml

ledger = input("Enter name")
from_dt = "01/04/2020"
to_dt = "31/03/2021"
payload = get_payload(from_dt,to_dt,ledger)
#print(payload)
xml = ElementTree.fromstring(get_data(payload))
dates = []
ledgers = []
vtypes = []
debits = []
credits = []
VchNos =[]
# for date in xml.findall("DSPVCHDATE"):
#     dates.append(date.text)
for led in xml.findall("DSPVCHLEDACCOUNT"):
    ledgers.append(led.text)
for vtype in xml.findall("DSPVCHTYPE"):
    vtypes.append(vtype.text)
for dr in xml.findall("DSPVCHDRAMT"):
    debits.append(float(dr.text) if dr.text != None else 0)
for cr in xml.findall("DSPVCHCRAMT"):
    credits.append(float(cr.text) if cr.text != None else 0)
# for vchNo in xml.findall("DSPEXPLVCHNUMBER"):
#     VchNos.append(vchNo.text)
df=pandas.DataFrame(list(zip(ledgers,debits,credits)),columns=["Name","Debit","Credit"])
df=df.groupby(by='Name').sum()
print(df)
df.to_clipboard(sep=',') 