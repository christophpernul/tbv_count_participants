# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 11:28:45 2018

@author: csam5106
"""

from selenium import webdriver
from datetime import datetime

datum_saisonbeginn = datetime(2017, 9, 1)
datum_meisterfeier = datetime(2018, 5, 12)

liste = []

browser = webdriver.Firefox()

#### Tirol & B-Turniere ausgewählt
browser.get('http://pool.oepbv.at/?mod=main&mod_id=4&sub=Turniere&BEW=BT+&DIS=&KL=&VERB=T&DAT=&NAME=')
table = browser.find_element_by_id('TBL_Turniere')
rows1 = table.find_elements_by_class_name('pl-odd')
rows2 = table.find_elements_by_class_name('pl-even')
rows = rows1+rows2
#ct = 0
for ct in range(len(rows)):
    print "Turnier #", ct+1
#    browser.get('http://pool.oepbv.at/?mod=main&mod_id=4&sub=Turniere&BEW=BT+&DIS=&KL=&VERB=T&DAT=&NAME=')
    browser.get('http://pool.oepbv.at/?mod=main&mod_id=4&sub=Turniere&BEW=BT+&DIS=&KL=&VERB=T&DAT=&NAME=')
    link1 = browser.find_element_by_id('TBL_Turniere').find_elements_by_class_name('pl-odd') if ct%2==0 else browser.find_element_by_id('TBL_Turniere').find_elements_by_class_name('pl-even')
    site = link1[ct].find_element_by_tag_name('a')
    browser.get(site.get_attribute('href'))###Turnier Seite
    checkTurnierart = browser.find_element_by_xpath("//fieldset").find_elements_by_xpath("//input")
    checkTeilnehmer = browser.find_element_by_class_name("MainFormTbl").find_elements_by_class_name("pl-odd")
    max_teilnehmer = checkTeilnehmer[1].find_elements_by_class_name('pl-data')[1].text
    if checkTurnierart[3].get_attribute("value")!="BT   B-Turnier (regionale Quali.)  ":
        ### Ueberpruefe ob die Turnierart stimmt: hier: B-Turnier
        print "Falsches Turnier, Turnier ist kein B-Turnier!"
        continue
    else:
        date = str(checkTurnierart[5].get_attribute("value")).split(" ")[0].split(".")
        datum = datetime(int(date[2]), int(date[1]), int(date[0]))
        if datum<datum_saisonbeginn or datum_meisterfeier<datum:
            ### Ueberpruefe ob das Turnier in der aktuellen Saison stattfindet
            print "Turnier nicht im richtigen Zeitraum!"
            continue
        else:
            name = checkTurnierart[8].get_attribute("value")
            if "Finale" in name:
                ### Verwerfe Eintraege in denen die Finalrunde eines Turniers ein zweites Mal eingetragen wurde
                continue
            else:
                ### Teilnehmerseite aufgerufen
                turnierliste = []
                nav = browser.find_element_by_class_name('pageposition')
                navLinks = nav.find_elements_by_tag_name('a')
                browser.get(navLinks[1].get_attribute('href'))
                tbl_teilnehmer = browser.find_element_by_id('TBL_Teilnehmer')
                nr1 = tbl_teilnehmer.find_elements_by_class_name('pl-odd')
                nr2 = tbl_teilnehmer.find_elements_by_class_name('pl-even')
                nr = nr1+nr2
                cnt=0
                max_cnt = int(max_teilnehmer)/2
                for player in nr:  
                    ### iteriere durch Teilnehmerliste
                    allfields = player.find_elements_by_class_name('pl-data')
                    data1 = allfields[1].find_elements_by_xpath("//tr[@class='pl-odd']/td[@class='pl-data']/input")
                    data2 = allfields[2].find_elements_by_xpath("//tr[@class='pl-odd']/td[@class='pl-data']/input")   
                    if cnt>max_cnt:
                        break
#                    print cnt, data1[6+16*cnt].get_attribute("value")
                    if str(data2[10+16*cnt].get_attribute("value"))=="Genehmigt":
                        liste.append(data1[6+16*cnt].get_attribute("value")) 
#                            turnierliste.append(data1[6+16*cnt].get_attribute("value"))            
                    cnt+=1
                cnt = 0
                for player in nr:  
                    ### iteriere durch Teilnehmerliste
                    allfields = player.find_elements_by_class_name('pl-data')
                    data1 = allfields[1].find_elements_by_xpath("//tr[@class='pl-even']/td[@class='pl-data']/input")
                    data2 = allfields[2].find_elements_by_xpath("//tr[@class='pl-even']/td[@class='pl-data']/input")   
                    if cnt>max_cnt-1:
                        break
#                    print cnt, data1[6+16*cnt].get_attribute("value")
                    if str(data2[10+16*cnt].get_attribute("value"))=="Genehmigt":
                        liste.append(data1[6+16*cnt].get_attribute("value")) 
#                            turnierliste.append(data1[6+16*cnt].get_attribute("value"))            
                    cnt+=1
    ct+=1
#    liste.append(["BT", turnierliste])
print len(liste), liste





#### Tirol & LM ausgewählt
#browser.get('http://pool.oepbv.at/?mod=main&mod_id=4&sub=Turniere&BEW=LM+&DIS=&KL=&VERB=T&DAT=&NAME=')
