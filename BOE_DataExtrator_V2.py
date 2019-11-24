from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import csv

class data_boe_extractor:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        #options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        self.url = 'https://www.boe.es/'
        try:
            self.driver = webdriver.Chrome(executable_path=".\chromedriver.exe", options=options)
        except:
            self.driver = webdriver.Chrome("chromedriver", options=options)
        self.document_name = "titular2019.csv"
        self.record_count = 1
        self.name_list = []
        self.date, self.college, self.teacher, self.position, self.area = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    
    
    def search_for_repeat(self, data):
        if str(data) in self.name_list:
            print("*******************************")
            print("Ya existe")
            print("*******************************")
            return True
        return False

    # Validando la existencia de la palabra clave en el titulo
    def words_finder(self, record_p):
        words = ["Titular de", "Titulares de", "titular de", "titulares de"]
        for word in words:
            if word.lower() in str(record_p.text).lower():
                return word
                break
        return "nothing"
    # Validando la existencia exceptions
    def exceptions_finder(self, record_p):
        # Lista de palabras a excluir
        except_list = ["convocan", "convoca", "corrige", "corrigen", "comisión", "concurso", "plaza", "error", "errores", "erratas"]
        for except_word in except_list:
            if except_word.lower() in str(record_p.text).lower():
                return True
                break
        return False

    # Escribiendo resultado en archivo data
    def write(self):
        self.clean_teacher_area()
        self.clean_teacher_name()
        data=[]
        data.append(str(str(self.date).encode("utf-8")))
        data.append(str(str(self.college).encode("utf-8")))
        data.append(str(str(self.teacher).encode("utf-8")))
        data.append(str(str(self.position).encode("utf-8")))
        data.append(str(str(self.area).encode("utf-8")))
        if not self.search_for_repeat(data) and self.area != "N/A" and self.teacher != " ":
            with open(self.document_name, 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(data)
                self.name_list.append(str(data))
                print(data)
            csvFile.close()
            self.date, self.college, self.teacher, self.position, self.area = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
            self.record_count += 1
            print("Numero de Titulares recopilados hasta el momento {}".format(self.record_count))
            return True
        else:
            return False

    # Buscando el nombre del mes por el numero encontrado
    def month_by(self,m):
        m=int(m)
        res=''
        if m==1:
            res='enero'
        if m==2:
            res='febrero'
        if m==3:
            res='marzo'
        if m==4:
            res='abril'
        if m==5:
            res='mayo'
        if m==6:
            res='junio'
        if m==7:
            res='julio'
        if m==8:
            res='agosto'
        if m==9:
            res='septiembre'
        if m==10:
            res='octubre'
        if m==11:
            res='noviembre'
        if m==12:
            res='diciembre'
        return res
    def clean_teacher_area(self):
        if 'conocimiento de ' in str(self.area):
            self.area = str(self.area).replace('conocimiento de ', '')
        if ' de ' == str(self.area)[:4]:
            self.area = str(self.area)[4:].replace(',', '')
            if 'adscrita ' in str(self.area):
                self.area = str(self.area).split(' adscrita ')
                self.area = str(self.area[1]).replace(',', '')
        if 'adscrita ' in str(self.area):
                self.area = str(self.area).split(' adscrita ')
                self.area = str(self.area[1]).replace(',', '')
        if '«' in str(self.area):
            self.area = str(self.area).split('«')
            self.area = str(self.area[1]).split('»')
            self.area = str(self.area[0])
        if 'al departamento de' in str(self.teacher): 
            self.teacher = str(self.teacher).split('al departamento de')
            self.teacher = str(self.teacher[1]).replace(',', '')
    def clean_teacher_name(self):

        if 'don ' in str(self.teacher):
            self.teacher = str(self.teacher).split('don ')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'Don ' in str(self.teacher):
            self.teacher = str(self.teacher).split('Don ')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'doña ' in str(self.teacher):
            self.teacher = str(self.teacher).split('doña ')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'Doña ' in str(self.teacher):
            self.teacher = str(self.teacher).split('Doña ')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'D. ' in str(self.teacher):
            self.teacher = str(self.teacher).split('D.')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'd. ' in str(self.teacher):
            self.teacher = str(self.teacher).split('d.')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'Dña. ' in str(self.teacher):
            self.teacher = str(self.teacher).split('Dña.')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'D.ª ' in str(self.teacher):
            self.teacher = str(self.teacher).split('D.ª')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        elif 'dña. ' in str(self.teacher):
            self.teacher = str(self.teacher).split('dña.')
            if len(self.teacher) > 1:
                self.teacher = str(self.teacher[1]).replace(',', '')
            else:
                self.teacher = str(self.teacher[0]).replace(',', '')
        if 'Profesora Titular' in str(self.teacher):
            self.teacher = str(self.teacher).split('Profesora Titular')
            self.teacher = str(self.teacher[0]).replace(',', '')
        if 'Profesor Titular' in str(self.teacher):
            self.teacher = str(self.teacher).split('Profesor Titular')
            self.teacher = str(self.teacher[0]).replace(',', '')
        if 'y habiendo cumplido' in str(self.teacher):
            self.teacher = str(self.teacher).split('y habiendo cumplido')
            self.teacher = str(self.teacher[0]).replace(',', '')
        if 'de Universidad en el' in str(self.teacher):
            self.teacher = str(self.teacher).split('de Universidad')
            self.teacher = str(self.teacher[0]).replace(',', '')
        if 'con documento nacional' in str(self.teacher): 
            self.teacher = str(self.teacher).split('con documento nacional')
            self.teacher = str(self.teacher[0]).replace(',', '')
        if ' en el ' in str(self.teacher): 
            self.teacher = str(self.teacher).split(' en el ')
            self.teacher = str(self.teacher[0]).replace(',', '')
        if ',' in str(self.teacher):
            self.teacher = str(self.teacher).split(',')
            self.teacher = str(self.teacher[0])


    def search_area(self, page_body_p, page_body_ps):
        # Buscando area de trabajo de el profesor encontrado en lineas anteriores.
        i = 1
        while i <= 2:
            index_of_teacher_name = page_body_ps.index(page_body_p)
            if i == 1:
                nxtp = page_body_ps[index_of_teacher_name]
            else:
                try:
                    nxtp = page_body_ps[index_of_teacher_name + 1]
                except:
                    nxtp = page_body_ps[index_of_teacher_name]
            nextp = str(nxtp.text).lower()
            
            if 'área' in nextp:
                nt = str(nextp).split('área')
                if '«' in str(nt[1]):
                    nt = str(nt[1]).split('«')
                    nt = str(nt[1]).split('»')
                    self.area = str(nt[0])
                elif ' "' in str(nt[1]):
                    nt = str(nt[1]).split(' "')
                    if '"' in str(nt[1]):
                        nt = str(nt[1]).split('"')
                        self.area = str(nt[0]).replace(',', '')
                    else:
                        self.area = str(nt[1]).replace(',', '')
                
                else:
                    ind2 = page_body_ps.index(nxtp)
                    try:
                        nextp2 = page_body_ps[ind2 + 1]
                    except:
                        nextp2 = page_body_ps[ind2]
                    
                    nextp2 = nextp2.text
                    
                    if ' "' in str(nextp2):
                        nt2 = str(nextp2).split(' "')
                        if '«' in str(nt2[1]):
                            nt2 = str(nt2[1]).split('«')
                            nt2 = str(nt2[1]).split('»')
                            self.area = str(nt2[0])
                        if '"' in str(nt2[1]):
                            nt2 = str(nt2[1]).split('"')
                            self.area = str(nt2[0]).replace(',', '')
                        else:
                            self.area = str(nt2[1]).replace(',', '')
                    elif '"' in str(nextp2):
                        nt2 = str(nextp2).split('"')
                        if '«' in str(nt2[1]):
                            nt2 = str(nt2[1]).split('«')
                            nt2 = str(nt2[1]).split('»')
                            self.area = str(nt2[0])
                        if '"' in str(nt2[1]):
                            nt2 = str(nt2[1]).split('"')
                            self.area = str(nt2[0]).replace(',', '')
                        else:
                            self.area = str(nt2[1]).replace(',', '')
                        self.area = str(nt2[1]).replace(',', '')
                    else:
                        self.area = 'N/A'
            else:
                self.area = 'N/A'
            if self.area != 'N/A':
                break
            i += 1

        self.area = str(self.area).replace('"', '')
    
    # Funcion encarga de extraer fecha del h4 en un resultado de la lista
    def extract_date_from_title(self,record):
        record_title = record.find_element_by_tag_name('h4')
        record_date = str(record_title.text).split('-')
        record_date = str(record_date[0]).split(' ')
        record_date_split = record_date[3].split('/')
        month = str(self.month_by(record_date_split[1]))
        day = str(int(record_date_split[0]))
        year = str(record_date_split[2])
        self.date = day + ' de ' + month + ' de ' + year
    
    # Funcion encarga de extraer fecha del p en un resultado de la lista
    def extract_college_name_from_title(self,record_p):
        if 'Universitat' in str(record_p.text):
            record_college_split = str(record_p.text).split('Universitat')
        else:
            record_college_split = str(record_p.text).split('Universidad')
        if len(record_college_split) > 1:
            record_college_split = str(record_college_split[1]).split(',')
            record_college = str(record_college_split[0])
            self.college = str('Universidad' + record_college).replace(',', '')

    # Funcion se encarga de buscar toda la informacion requerida dentro del cuerpo de la pagina
    def find_in_body(self,record, record_p, word_rs):
        # Buscando fecha del boletín
        self.extract_date_from_title(record)
        body_date = self.date
        print(self.date)
        # Buscando nombre de la universidad
        self.extract_college_name_from_title(record_p)
        body_college = self.college
        print(self.college)
        # Extraer link del resultado en lista
        link = record.find_element_by_tag_name('a').get_attribute('href')
        newTab = 'window.open("' + link + '", "_blank");'
        self.driver.execute_script(newTab)
        self.driver.switch_to.window(self.driver.window_handles[1])
        print("#################################################")
        page_body_tables = self.driver.find_elements_by_xpath('//*[@id="textoxslt"]/table/tbody/tr')

        page_body_tables_head = self.driver.find_elements_by_xpath('//*[@id="textoxslt"]/table/thead/tr/th')
        area_head_index = 4
        name_head_index = 2
        lastname_head_index = 3
        if len(page_body_tables_head) > 0:
            for page_body_table_head in page_body_tables_head:
                try:
                    if 'Área' in str(page_body_table_head.find_element_by_xpath('p').text) or 'ÁREA' in str(page_body_table_head.find_element_by_xpath('p').text):
                        print("Find area")
                        area_head_index = page_body_tables_head.index(page_body_table_head) + 1
                    if 'Nombre' in str(page_body_table_head.find_element_by_xpath('p').text) or 'NOMBRE' in str(page_body_table_head.find_element_by_xpath('p').text):
                        name_head_index = page_body_tables_head.index(page_body_table_head) + 1
                    if 'Apellidos' in str(page_body_table_head.find_element_by_xpath('p').text) or 'APELLIDOS' in str(page_body_table_head.find_element_by_xpath('p').text):
                        lastname_head_index = page_body_tables_head.index(page_body_table_head) + 1
                except:
                    if 'Área' in str(page_body_table_head.text) or 'ÁREA' in str(page_body_table_head.text):
                        print("Find area")
                        area_head_index = page_body_tables_head.index(page_body_table_head) + 1
                    if 'Nombre' in str(page_body_table_head.text) or 'NOMBRE' in str(page_body_table_head.text):
                        name_head_index = page_body_tables_head.index(page_body_table_head) + 1
                    if 'Apellidos' in str(page_body_table_head.text) or 'APELLIDOS' in str(page_body_table_head.text):
                        lastname_head_index = page_body_tables_head.index(page_body_table_head) + 1
                
            
        if len(page_body_tables) > 0:
            print("Si **********************************")
            try:
                for page_body_table in page_body_tables:
                    name = page_body_table.find_element_by_xpath('td['+str(name_head_index)+']')
                    lastname = page_body_table.find_element_by_xpath('td['+str(lastname_head_index)+']')
                    self.teacher = "{name} {lastname}".format(name = name.text, lastname = lastname.text)
                    try:
                        lastname_head_test = self.driver.find_element_by_xpath('//*[@id="textoxslt"]/table/thead/tr/th[3]/p').text
                    except:
                        lastname_head_test = self.driver.find_element_by_xpath('//*[@id="textoxslt"]/table/thead/tr/th[3]').text
                    if "Apellidos" != str(lastname_head_test):
                        self.teacher = "{name}".format(name = name.text)
                    self.area = page_body_table.find_element_by_xpath('td['+str(area_head_index)+']').text
                    print(self.teacher)
                    print(self.area)
                    self.position = word_rs 
                    if self.date == "N/A" and self.college == "N/A":
                        self.date = body_date
                        self.college = body_college
                            # Comprobando si el registro esta repetido o es invalido.
                    if self.teacher == "N/A":
                        print("No se agrega.")
                        pass
                    else:
                        self.write()
            except:
                pass
               
        else:
            print("No **********************************")
            page_body_ps = self.driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
            print("lineas {}".format(len(page_body_ps)))
            time.sleep(2)
            
            for page_body_p in page_body_ps:
                print(page_body_ps.index(page_body_p))
                page_body_p_text = page_body_p.text
                if "área de " in str(page_body_p_text) and 'Titular de ' in str(page_body_p_text) and 'titular de ' in str(page_body_p_text) and 'titulares de ' in str(page_body_p_text) or 'Titulares de ' in str(page_body_p_text):
                    page_body_p_text = str(page_body_p_text).split('Titular de')
                    page_body_p_text = str(page_body_p_text[0]).split(',')
                    self.teacher = str(page_body_p_text[0]).replace("–", "")
                    self.search_area(page_body_p, page_body_ps)
                elif 'Don ' in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('Don ')
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps)
                elif 'don '  in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('don ') 
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps)
                elif 'Doña ' in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('Doña ')
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps)
                elif 'doña ' in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('doña ')
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps)
                elif 'D. ' in str(page_body_p_text) and not '.D. ' in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('D. ')
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps)
                elif 'd. ' in str(page_body_p_text) and not '.d. ' in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('d. ')
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps)
                elif 'Dña. ' in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('Dña. ')
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps) 
                elif 'dña ' in str(page_body_p_text):
                    self.teacher = str(page_body_p_text).split('dña. ')
                    self.teacher = self.teacher[1].split(",", 1)[0]
                    self.search_area(page_body_p, page_body_ps)
                if len(self.teacher) > 4:
                    print(str(self.teacher))
                    if 'Área ' in str(self.teacher):
                        self.teacher = str(self.teacher).split('Área')
                        self.teacher = str(self.teacher[0])
                        self.search_area(page_body_p, page_body_ps)
                    elif 'área ' in str(self.teacher):
                        self.teacher = str(self.teacher).split('área')
                        self.teacher = str(self.teacher[0])
                        self.search_area(page_body_p, page_body_ps)
                

                # Imprimiendo resultados de la busqueda
                
                print(self.area)
                print(self.teacher)
                self.position = word_rs 

                # Validado si la fecha y universidad estan en N/A para asignar nuevamente la valor correcto.
                if self.date == "N/A" and self.college == "N/A":
                    self.date = body_date
                    self.college = body_college
                # Comprobando si el registro esta repetido o es invalido.
                if self.teacher == "N/A":
                    print("No se agrega.")
                    pass
                else:
                     
                    self.write()
                
                    
        self.driver.execute_script('window.close()')
        self.driver.switch_to.window(self.driver.window_handles[0])
        print("#################################################")
        return True


    # Funcion se encarga de buscar toda la informacion requerida dentro del titulo
    def find_in_title(self,record, record_p, word_rs):
        # Buscando fecha del boletín
        self.extract_date_from_title(record)
        print(self.date)

        # Buscando nombre de la universidad
        self.extract_college_name_from_title(record_p)
        print(self.college)

        # Buscando persona nombrada en el p del resultado en la lista
        record_teacher_split_test = str(record_p.text).split('por la que se nombra')
        record_teacher_split_test2 = str(record_p.text).split('por la que se nombran')
        if len(record_teacher_split_test) > 1 and len(record_teacher_split_test2) == 1:
            record_teacher_split_test = str(record_teacher_split_test[1].lower()).split(word_rs.lower())
            if str(record_teacher_split_test[0]) != '' and str(record_teacher_split_test[0]) != ', ' and str(record_teacher_split_test[0]) != ',' and str(
                    record_teacher_split_test[0]) != ' ':
                self.teacher = str(record_teacher_split_test[0]).replace(',', '')
            elif 'a don ' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a don ')
                self.teacher = str(record_teacher_split[1]).replace(',', '')
            elif 'a Don ' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a Don ')
                self.teacher = str(record_teacher_split[1]).replace(',', '')
            elif 'a doña ' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a doña ')
                self.teacher = str(record_teacher_split[1]).replace(',', '')
            elif 'a Doña ' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a Doña ')
                self.teacher = str(record_teacher_split[1]).replace(',', '')
            elif 'a D. ' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a D. ')
                record_teacher_split = str(record_teacher_split_test[1]).split(',')
                self.teacher = str(record_teacher_split[0]).replace(',', '')
            elif 'a D.' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a D.')
                record_teacher_split = str(record_teacher_split_test[1]).split(',')
                self.teacher = str(record_teacher_split[0]).replace(',', '')
            elif 'a d. ' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a d. ')
                record_teacher_split = str(record_teacher_split_test[1]).split(',')
                self.teacher = str(record_teacher_split[0]).replace(',', '')
            elif 'a d.' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('a d.')
                record_teacher_split = str(record_teacher_split_test[1]).split(',')
                self.teacher = str(record_teacher_split[0]).replace(',', '')
            elif 'Dña.' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('Dña.')
                record_teacher_split = str(record_teacher_split_test[1]).split(',')
                self.teacher = str(record_teacher_split[0]).replace(',', '')
            elif 'dña.' in str(record_teacher_split_test[1]):
                record_teacher_split = str(record_teacher_split_test[1]).split('dña.')
                record_teacher_split = str(record_teacher_split_test[1]).split(',')
                self.teacher = str(record_teacher_split[0]).replace(',', '')

            self.position = word_rs 
            self.area = 'N/A'
            print("^^^^^^^^^^^^^^^^^^{}^^^^^^^^^^^^^^".format(self.area))

            # Buscando area de trabajo
            if self.teacher != 'N/A' and self.teacher != '' and self.teacher != ' ':
                temp = str(record_p.text).lower()
                if 'área' in temp:
                    temp = temp.split('área')
                    if ' "' in str(temp[1]):
                        temp = str(temp[1]).split(' "')
                        if '" ' in temp[1]:
                            temp = str(temp[1]).split('" ')
                            self.area = str(temp[0]).replace(',', '')
                        elif '".' in temp[1]:
                            temp = str(temp[1]).split('".')
                            self.area = str(temp[0]).replace(',', '')
                        elif '",' in temp[1]:
                            temp = str(temp[1]).split('",')
                            self.area = str(temp[0]).replace(',', '')
                    elif self.teacher in str(temp[1]):
                        temp = str(temp[1]).split(self.teacher)
                        self.area = str(temp[0]).replace(',', '')
                    else:
                        self.area = str(temp[1]).replace(',', '')

                if self.area == 'N/A':
                    lnk = record.find_element_by_tag_name('a').get_attribute('href')
                    newTab = 'window.open("' + lnk + '", "_blank");'
                    self.driver.execute_script(newTab)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    ps = self.driver.find_elements_by_xpath('//*[@id="textoxslt"]/p')
                    for p in ps:
                        temp = str(p.text).lower()
                        if str(self.teacher).lower() in temp and 'área' in temp:
                            temp = str(temp).split('área')
                            if '«' in str(temp[1]):
                                temp = str(temp[1]).split('«')
                                temp = str(temp[1]).split('»')
                                self.area = str(temp[0])
                            elif 'conocimiento' in str(temp[1]):
                                temp = str(temp[1]).split('conocimiento')
                                temp = str(temp[1]).split(',')
                                if len(temp) == 1:
                                    temp = str(temp[0]).split('.')
                                self.area = str(temp[0])
                            else:
                                ind0 = ps.index(p)
                                try:
                                    nextp0 = ps[ind0 + 1]
                                except:
                                    nextp0 = ps[ind0]
                                nextp0 = str(nextp0.text).lower()
                                if 'conocimiento' in str(nextp0):
                                    nextp0 = str(nextp0).split('conocimiento')
                                    nextp0 = str(nextp0[1]).split(',')
                                    if len(nextp0) == 1:
                                        nextp0 = str(nextp0[0]).split('.')
                                    self.area = str(nextp0[0])
                        elif 'área' in temp:
                            if 'área' in str(p.text):
                                nt = str(p.text).split('área')
                            elif 'Área' in str(p.text):
                                nt = str(p.text).split('Área')
                            lat = str(nt[1]).lower()
                            if '«' in lat:
                                    lat = str(lat).split('«')
                                    lat = str(lat[1]).split('»')
                                    self.area = str(lat[0])
                            elif ' "' in str(nt[1]):
                                nt = str(nt[1]).split(' "')
                                if '"' in str(nt[1]):
                                    nt = str(nt[1]).split('"')
                                    self.area = str(nt[0]).replace(',', '')
                                else:
                                    self.area = str(nt[1]).replace(',', '')
                            elif 'conocimiento' in lat:
                                lat = str(lat).split('conocimiento')
                                if ',' in str(lat[1]):
                                    lat = str(lat[1]).split(',')
                                    self.area = str(lat[0]).replace(',', '')
                                elif '«' in str(lat[1]):
                                    lat = str(lat[1]).split('«')
                                    lat = str(lat[1]).split('»')
                                    self.area = str(lat[0])
                                else:
                                    self.area = str(lat[1])
                            else:
                                ind2 = ps.index(p)
                                try:
                                    nextp2 = ps[ind2 + 1]
                                except:
                                    nextp2 = ps[ind2]
                                nextp2 = nextp2.text
                                if ' "' in str(nextp2):
                                    nt2 = str(nextp2).split(' "')
                                    if '"' in str(nt2[1]):
                                        nt2 = str(nt2[1]).split('"')
                                        self.area = str(nt2[0]).replace(',', '')
                                    else:
                                        self.area = str(nt2[1]).replace(',', '')
                                elif '"' in str(nextp2):
                                    nt2 = str(nextp2).split('"')
                                    self.area = str(nt2[1]).replace(',', '')
                                elif 'conocimiento' in str(nextp2):
                                    lat = str(nextp2).split('conocimiento')
                                    if ',' in str(lat[1]):
                                        lat = str(lat[1]).split(',')
                                        self.area = str(lat[0]).replace(',', '')
                                    elif '«' in str(lat[1]):
                                        lat = str(lat[1]).split('«')
                                        lat = str(lat[1]).split('»')
                                        self.area = str(lat[0])
                                    else:
                                        self.area = str(lat[1])

                                    if self.area != 'N/A':
                                        t = str(self.area).replace(' ', '')
                                        if len(t) <= 3:
                                            if ',' in str(nextp2):
                                                nextp2 = str(nextp2).split(',')
                                                self.area = str(nextp2[0]).replace(',', '')
                                            elif '«' in str(nextp2):
                                                nextp2 = str(nextp2).split('«')
                                                nextp2 = str(nextp2[1]).split('»')
                                                self.area = str(nextp2[0])
                                            else:
                                                self.area = str(nextp2)

                        if self.area != 'N/A':
                            t = str(self.area).replace(' ', '')
                            if len(t) <= 3:
                                ind2 = ps.index(p)
                                try:
                                    nextp2 = ps[ind2 + 1]
                                except:
                                    nextp2 = ps[ind2]
                                nextp2 = nextp2.text
                                if ' "' in str(nextp2):
                                    nt2 = str(nextp2).split(' "')
                                    if '"' in str(nt2[1]):
                                        nt2 = str(nt2[1]).split('"')
                                        self.area = str(nt2[0]).replace(',', '')
                                    else:
                                        self.area = str(nt2[1]).replace(',', '')
                                elif '"' in str(nextp2):
                                    nt2 = str(nextp2).split('"')
                                    self.area = str(nt2[1]).replace(',', '')
                                elif 'conocimiento' in str(nextp2):
                                    lat = str(nextp2).split('conocimiento')
                                    if ',' in str(lat[1]):
                                        lat = str(lat[1]).split(',')
                                        self.area = str(lat[0]).replace(',', '')
                                    elif '«' in str(lat[1]):
                                        lat = str(lat[1]).split('«')
                                        lat = str(lat[1]).split('»')
                                        self.area = str(lat[0])
                                    else:
                                        self.area = str(lat[1])
                    self.driver.execute_script('window.close()')
                    self.driver.switch_to.window(self.driver.window_handles[0])
                self.area = str(self.area).replace('"', '')
            if self.teacher == "N/A":
                return False
            else:
                return True
        else:
            return False
        print(self.teacher)

    def get_data(self,date_list, words_list):
        print("El rango de fechas usado para la busqueda sera de {} a {}".format(date_list[0], date_list[1]))

        for word_for_search in words_list:
            print("~~~~~~~~~~~~~~~~~~~{}~~~~~~~~~~~~~~~~~~~".format(word_for_search))
            print(self.name_list)
            
            for i in range(2):
                self.driver.get(self.url)

                time.sleep(2)
                self.driver.find_element_by_xpath('//*[@id = "diarios"]/div[2]/div[1]/div[1]/div/div/div/ul/li[2]/a/span').click()

                # Definiendo patrones de busqueda.
                if i == 1:
                    self.driver.execute_script("document.getElementById('TIT').value='"+word_for_search+"'")
                else:
                    self.driver.execute_script("document.getElementById('DOC').value='"+word_for_search+"'")

                self.driver.execute_script("document.getElementById('desdeFP').value='"+ date_list[0] +"'")
                self.driver.execute_script("document.getElementById('hastaFP').value='"+ date_list[1] +"'")
                self.driver.find_element_by_xpath('//*[@id = "mostrar"]/option[5]').click()
                self.driver.find_element_by_xpath('//*[@id = "orden"]/option[2]').click()
                time.sleep(2)
                self.driver.find_element_by_xpath('//*[@id = "contenido"]/form/div/div/input[1]').click()

                # Enumerando nuevo de paginas disponibles para los resultados de la busqueda
                pages = self.driver.find_elements_by_xpath('//*[@id = "contenido"]/div[3]/ul/li')

                page = 1 # Determinando pagina de inicio
                if len(pages) == 0:
                    pages = 2
                else:
                    pages = len(pages)
                # Recorriendo paginas de resultado.
                
                while page < pages:
                    if page > 1:
                        if page == 2:
                            page = page
                        else:
                            page = page + 1
                        nextL = self.driver.find_element_by_xpath(
                                '//*[@id = "contenido"]/div[3]/ul/li[' + str(page) + ']/a').get_attribute('href')
                        self.driver.get(nextL)

                    page += 1

                    # Enumeracion de registros en la pagina de resultado actual
                    records = self.driver.find_elements_by_xpath('//*[@id = "contenido"]/div[4]/ul/li')
                    # Recorriendo registros
                    for record in records:
                        # Extrayendo texto del registro para su analisis
                        record_p = record.find_element_by_tag_name('p')
                        except_check = self.exceptions_finder(record_p)
                        if except_check:
                            pass
                        else:
                            word_rs = self.words_finder(record_p)
                            if "por la que se nombra" in record_p.text or "por la que se nombra" in record_p.text:
                                
                                if word_rs == "titular de" or word_rs == "Titular de":
                                    data_record = self.find_in_body(record, record_p, word_rs)
                                    
                                elif word_rs == "titulares de" or word_rs == "Titulares de":
                                    data_record = self.find_in_title(record, record_p, word_rs)
                                    
                                    if data_record:
                                        self.write()
                                else:
                                    pass
                                    # data_record = self.find_in_page(herf)
                            

        self.driver.close()
        return self.record_count



if __name__ == '__main__':
    # Creando archivo contenedor de resultados
    col = ['FECHA', 'UNIVERSIDAD', 'PROFESOR', 'FIGURA', 'AREA']

    

    date_list = ["2019-01-01", "2019-07-31"] # Rango de fechas (Formato yyy/mm/dd)

    words_list = ["Titular de", "Titulares de", "titular de", "titulares de"] # Lista palabras a buscar.
    extractor = data_boe_extractor()
    with open(extractor.document_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(col)
    total = extractor.get_data(date_list, words_list)
    print("Numero de titulares recolectados {}".format(total))
