# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 15:11:27 2020

@author: daviszhang
"""

from pathlib import Path
import logging
import time
import json
import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime


print("DAX Beautifier  version --1.0.2--")
amo_path=None
adomd_path=None
logger = logging.getLogger(__name__)

baseurl = "https://www.daxformatter.com/?embed=1&fx="
endurl = "&r=US"

toolbar_width = 40
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1))

import clr  
    
root = Path(r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL")

try:
    if amo_path is None:
        amo_path = str(
            max((root / "Microsoft.AnalysisServices.Tabular").iterdir())
            / "Microsoft.AnalysisServices.Tabular.dll"
        )
except: 
    print("Warning: Please install AMO library and make sure the path is correct.")
    time.sleep(1)


logger.info("Loading .Net assemblies...")
clr.AddReference("System")
clr.AddReference("System.Data")
clr.AddReference(amo_path)

global System, DataTable, AMO

import Microsoft.AnalysisServices.Tabular as AMO

logger.info("Successfully loaded these .Net assemblies: ")

try:
    print("Connect to Analysis Services")     
    try:
        conn = "Provider=MSOLAP;Data Source="+str(sys.argv[1])+";Initial Catalog='';"
        #conn = "Provider=MSOLAP;Data Source=localhost:63963;Initial Catalog='';"
        AMOServer = AMO.Server()
        AMOServer.Connect(conn)
    except:
        print("Warning: Please run this program from Power BI Desktop")
        time.sleep(1)
        raise Exception()
    for item in AMOServer.Databases:
        print("Server: ", str(sys.argv[1]))        
        print("Compatibility Level: ", item.CompatibilityLevel) 
        if item.CompatibilityLevel < 1500:
            print("Warning: The model database has a lower compatibility level and it will cause the job to fail!")
            time.sleep(1)
        print("Created: ", item.CreatedTimestamp)
   
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    
    def daxformatter(name,exp):
        item = name + "=" + exp
        url = baseurl + item + endurl
        r = requests.post(url)          
        soup = BeautifulSoup(r.text, 'html.parser')
        html_result = soup.body.div.div
        if html_result.div is None:
            result = str(html_result).replace("<br/>","\n")
            result = result.replace("\xa0"," ")
            result = cleanhtml(result)
            result = result.replace("&lt;","<")
            result = result.replace("&gt;",">")
            result = result.split("=",1)[1]
        else:
            result = exp
        return result

    if str(requests.post(baseurl))=='<Response [200]>':
        print("Connected to DAX Formatter")
    else:
        print("Warning: Please make sure you are connected to the internet and try again")
        time.sleep(1)
        raise Exception()
    print("Refresh Model")
    AMOServer.Databases.GetByName(AMOServer.Databases[0].Name).Refresh(True)
    PowerBIDatabase_JSON = AMO.JsonSerializer.SerializeDatabase(AMOServer.Databases[0])
    PowerBIDatabase_JSON = json.loads(PowerBIDatabase_JSON)
    _var = input("""
    Do you want to format all DAX formulas? If so, enter 0. 
    Otherwise, please enter an integer greater than 0 to apply formatting 
    only to DAX formulas created or modified in the last N hours:\n""")
    if int(_var)<0:
        print("Error: Invalid Input")   
        time.sleep(1)
        raise Exception()
    elif int(_var)==0:
        _x = 1
        print("Processing Begin")
        try:
            for n in range(0,len(PowerBIDatabase_JSON['model']['tables'])):
                item_table_name = PowerBIDatabase_JSON['model']['tables'][n]['name']
                try:
                    PowerBIDatabase_JSON['model']['tables'][n]['isHidden']
                except:
                    print("Formatting in %s" %(item_table_name))
                    try:         
                        item_p_name = PowerBIDatabase_JSON['model']['tables'][n]['partitions'][0]['name']
                        item_p_exp = PowerBIDatabase_JSON['model']['tables'][n]['partitions'][0]['source']['expression']
                        AMOServer.Databases[0].Model.Tables.Find(item_table_name).Partitions.Find(item_p_name).Source.Expression = daxformatter(item_p_name,item_p_exp)
                    except:
                        pass
                    
                    try:
                        for i in range(0,len(PowerBIDatabase_JSON['model']['tables'][n]['measures'])):
                            item_m_name = PowerBIDatabase_JSON['model']['tables'][n]['measures'][i]['name']
                            item_m_exp = PowerBIDatabase_JSON['model']['tables'][n]['measures'][i]['expression']
                            AMOServer.Databases[0].Model.Tables.Find(item_table_name).Measures.Find(item_m_name).Expression = daxformatter(item_m_name,item_m_exp)
                            sys.stdout.write("-")
                            sys.stdout.flush()
                    except:
                        pass
                    
                    for i in range(1,len(PowerBIDatabase_JSON['model']['tables'][n]['columns'])):
                        try:
                            item_c_name = PowerBIDatabase_JSON['model']['tables'][n]['columns'][-i]['name']
                            item_c_exp = PowerBIDatabase_JSON['model']['tables'][n]['columns'][-i]['expression']
                            AMOServer.Databases[0].Model.Tables.Find(item_table_name).Columns.Find(item_c_name).Expression = daxformatter(item_c_name,item_c_exp)
                            sys.stdout.write("-")
                            sys.stdout.flush()
                        except:
                            pass
                    sys.stdout.write("-")
                    sys.stdout.flush()
                    sys.stdout.write("|\n")
        except:
             print("Error: Processing Failed")   
             time.sleep(1)
             raise Exception()
        print("Processing End") 
    else:
        import dateutil.parser
        from datetime import timedelta
        _datetime = datetime.utcnow()-timedelta(hours=int(_var)) #The model use UTC timezone.
        _x = 0
        try:
            for n in range(0,len(PowerBIDatabase_JSON['model']['tables'])):
                item_table_name = PowerBIDatabase_JSON['model']['tables'][n]['name']
                try:
                    PowerBIDatabase_JSON['model']['tables'][n]['isHidden']
                except:
                    print("Formatting in %s" %(item_table_name))
                    try:
                        if dateutil.parser.parse(PowerBIDatabase_JSON['model']['tables'][n]['modifiedTime'])>_datetime:
                            item_p_name = PowerBIDatabase_JSON['model']['tables'][n]['partitions'][0]['name']
                            item_p_exp = PowerBIDatabase_JSON['model']['tables'][n]['partitions'][0]['source']['expression']
                            AMOServer.Databases[0].Model.Tables.Find(item_table_name).Partitions.Find(item_p_name).Source.Expression = daxformatter(item_p_name,item_p_exp)
                            _x += 1
                    except:
                        pass
                    
                    try:
                        for i in range(0,len(PowerBIDatabase_JSON['model']['tables'][n]['measures'])):
                            if dateutil.parser.parse(PowerBIDatabase_JSON['model']['tables'][n]['measures'][i]['modifiedTime'])>_datetime:
                                item_m_name = PowerBIDatabase_JSON['model']['tables'][n]['measures'][i]['name']
                                item_m_exp = PowerBIDatabase_JSON['model']['tables'][n]['measures'][i]['expression']
                                AMOServer.Databases[0].Model.Tables.Find(item_table_name).Measures.Find(item_m_name).Expression = daxformatter(item_m_name,item_m_exp)
                                _x += 1
                                sys.stdout.write("-")
                                sys.stdout.flush()
                    except:
                        pass
                    
                    for i in range(1,len(PowerBIDatabase_JSON['model']['tables'][n]['columns'])):
                        try:
                            if dateutil.parser.parse(PowerBIDatabase_JSON['model']['tables'][n]['columns'][-i]['modifiedTime'])>_datetime:
                                item_c_name = PowerBIDatabase_JSON['model']['tables'][n]['columns'][-i]['name']
                                item_c_exp = PowerBIDatabase_JSON['model']['tables'][n]['columns'][-i]['expression']
                                AMOServer.Databases[0].Model.Tables.Find(item_table_name).Columns.Find(item_c_name).Expression = daxformatter(item_c_name,item_c_exp)
                                _x += 1
                                sys.stdout.write("-")
                                sys.stdout.flush()
                        except:
                            pass
                    sys.stdout.write("-")
                    sys.stdout.flush()
                    sys.stdout.write("|\n")
        except:
             print("Error: Processing Failed")   
             time.sleep(1)
             raise Exception()
        print("Processing End") 
    
    if _x > 0:
        print("Committing Begin\nPlease Wait...")
        try:
            AMOServer.Databases[0].Model.RequestRefresh(AMO.RefreshType.Full)
            AMOServer.Databases[0].Model.SaveChanges()
            print("Committing End")
        except:
            print("Error: Committing Failed")
            time.sleep(1)
            raise Exception()
    print("Job Succeeded!")
except:
    print("Program terminated: Some Error Occurred!")

