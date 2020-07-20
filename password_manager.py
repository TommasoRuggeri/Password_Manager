from cryptography.fernet import Fernet
import os , getpass , sys , keyboard
import tkinter as tk
from tkinter import filedialog , Text
import win32file
import win32con
import win32api
from pathlib import Path
import win32com.shell.shell as shell

home = str(Path.home())


class Crypto:
    
    def __init__(self):
        self.password_right = False
        self.password_provided = str
        self.attempts = 0
        self.key = str
        self.can_go = False
        self.filesize = int
        self.password_key = str
        self.command_list = ("""supported actions :
            - command list            (help) 
            - insert new record       (insert)
            - list all records        (list)
            - exit                    (close)
            - search a record by item (record)
            - delete a record         (delete)
            - download passwords      (download)""")

    def login(self, attempts):
        self.attempts = attempts
        while not self.password_right:
            if self.attempts > 0:
                print(f"Remaning attempts: {self.attempts} \n")
                password_to_compare = getpass.getpass("Insert master password: ")
                if password_to_compare == self.password_provided:
                    print("\nPassword correct \n")
                    self.password_right = True
                    self.filesize = os.path.getsize(home +'\\file_key.png') # check if the file that contains the key is empty
                    if self.filesize == 0: #if is empty i will generate a key to use in future
                        self.key = Fernet.generate_key()
                        print("key not found \n")
                        with open(home+"\\file_key.png" , 'wb') as file:
                            file.write(self.key)

                    elif self.filesize != 0: # if the file contains a key i will load into a variable and i will use it
                        print("key found \n")
                        with open(home +"\\file_key.png", 'rb') as file:
                            self.key = file.read()  #key_to_use  
                    pass
                else:
                    print("Password wrong! \n")
                    self.attempts-= 1
                    os.system('cls')
            if self.attempts <= 0:
                print("Deleting crypted file \n")
                os.remove(home+"\\file.jpg")
                os.remove(home +"\\file_key.png")
                os.remove(home +"\\password_key.txt")
                os.remove(home+"\\password.encrypted")
                sys.exit(0)


    def encrypt_file_content(self):

        with open(home +"\\file.jpg" , 'rb') as f:
            data = f.read() #file content to encrypt
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(data)

        with open(home+"\\file.jpg" , 'wb') as f:
            f.write(encrypted_data)

    def decrypt_file_content(self):

        with open(home+"\\file.jpg" , 'rb') as file:
            
            data = file.read() #file content to decrypt

            element_splitted = data.split(b'\n')

            for element in element_splitted:
                if element == b'':
                    pass
                else:
                    fernet = Fernet(self.key)
                    decrypted_element = fernet.decrypt(element)
                    decrypted_element = decrypted_element.decode()
                    s = decrypted_element.split(' ')
                    print(f"util: {s[0]} user: {s[1]} password: {s[2]} \n")
        
    def search_record(self):
        item_to_search = input("\nWhat do you want to research? ")
        found = False
        with open(home+"\\file.jpg" , 'rb') as file:
            data = file.read()

            element_splitted = data.split(b'\n')
            for element in element_splitted:
                if element == b'':
                    pass
                elif element != b'':
                    fernet = Fernet(self.key)
                    decrypted_element = fernet.decrypt(element)
                    decrypted_element = decrypted_element.decode()
                    s = decrypted_element.split(' ')
                    if item_to_search in s:
                        print(f"util: {s[0]} user: {s[1]} password: {s[2]} \n")
                        found = True
                        break

        if not found:
            print(f"no record found that contains: {item_to_search}")

    def delete_record(self):
        os.system('cls')
        to_delete = input("\nWhat do you want to delete? ")
        os.system('cls')
        found = False
        fernet = Fernet(self.key)
        with open(home+"\\file.jpg" , 'rb') as file:
            data = file.read()

            element_splitted = data.split(b'\n')
            for element in element_splitted:
                if element == b'':
                    pass
                elif element != b'':
                    decrypted_element = fernet.decrypt(element)
                    decrypted_element = decrypted_element.decode()
                    s = decrypted_element.split(' ')
                    if to_delete in s:         #s[0] == util_to_search:
                        os.system('cls')
                        answer = input(f"util: {s[0]} user: {s[1]} password: {s[2]} \n Do you want to delete this record? yes/no    ")
                        while answer != "yes" and answer != "no":
                            os.system('cls')
                            print(f"command not recognized: {answer}")
                            answer = input(f"util: {s[0]} user: {s[1]} password: {s[2]} \n Do you want to delete this record? yes/no    ")
                            os.system('cls')
                        if answer == 'yes':
                            os.system('cls')
                            erc = element
                            erc = fernet.decrypt(erc)
                            erc = erc.decode()
                            if erc == decrypted_element and element in data:
                                data = data.replace(element,b'')
                                with open(home+"\\file.jpg" , 'wb') as f:
                                    f.write(data)
                                

                      

                        found = True
                        break

        if not found:
            print(f"no record found that contains: {to_delete}")
                    
    def backup_passwords(self):
        fernet = Fernet(self.key)

        if os.path.exists(home+"\\backup_file.txt"):
            answer = input("backup file already exists do you want to overwriting it:  ")
            if answer == 'yes':
                os.remove(home+"\\backup_file.txt")
                open(home + "\\backup_file.txt", 'x').close()
                os.system('cls')
                with open(home + "\\file.jpg", 'rb') as file:
                    data = file.read()

                    element_splitted = data.split(b'\n')
                    for element in element_splitted:
                        if element == b'':
                            pass
                        elif element != b'':
                            decrypted_element = fernet.decrypt(element)
                            decrypted_element = decrypted_element.decode()

                            with open(home+"\\backup_file.txt", 'a') as backup_file:
                                backup_file.write(decrypted_element + '\n')
                print("backup overwritten :)")
            if answer == 'no':
                os.system('cls')
                return
            while answer != 'yes' and answer != 'no':
                os.system('cls')
                print(f"{answer} is not a command")
                answer = input("backup file already exists do you want to overwriting it:  ")

        if not os.path.exists(home+"\\backup_file.txt"):
            open(home+"\\backup_file.txt", 'x').close()
            print("backup_file created")
            with open(home+"\\file.jpg" , 'rb') as file:
                data = file.read()
                element_splitted = data.split(b'\n')
                for element in element_splitted:
                    if element == b'':
                        pass
                    elif element != b'':
                        decrypted_element = fernet.decrypt(element)
                        decrypted_element = decrypted_element.decode()
                        erc = element
                        erc = fernet.decrypt(erc)
                        erc = erc.decode()
                        with open(home+"\\backup_file.txt" , 'a') as backup_file:
                            backup_file.write(erc)
            print("backup created :)")

        
    def insert_new_record_in_file(self):
        is_good_util = False
        is_good_user = False
        is_good_pass = False

        while not is_good_util:
            util = input("\nInsert the util: ")
            if not util or  ' ' in util:
                print("util value cannot be null or cannot contains spaces")
            else:
                is_good_util = True

        while not is_good_user:
            user = input("\nInsert mail: ")
            if not user or ' ' in user:
                 print("user value cannot be null or cannot contains spaces")
            else:
                is_good_user = True
            
        while not is_good_pass:
            password = input("\nInsert password: ")
            if not password or ' ' in password:
                 print("password value cannot be null or cannot contains spaces")
            else:
                is_good_pass = True
            
        text_to_insert = util + ' ' +  user + ' ' + password
        text_to_append = text_to_insert.encode()

        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(text_to_append)
        fz = os.path.getsize(home+"\\file.jpg")
        if fz == 0:
            with open(home+"\\file.jpg" , 'wb') as file:
                file.write(encrypted_data)
                file.write(b'\n')
        elif fz != 0:
            with open(home+"\\file.jpg" , 'ab') as file:
                file.write(encrypted_data)
                file.write(b'\n')


    def check_file(self):
        os.system('cls')
        try:
            if not os.path.exists(home+"\\file.jpg"):
                open(home+"\\file.jpg" , 'x').close()
            else:
                pass
        
            if not os.path.exists(home+"\\file_key.png"):
                open(home+"\\file_key.png" , 'x').close()
            else:
                pass

            if not os.path.exists(home+"\\password_key.txt"):
                open(home+"\\password_key.txt" , 'x').close()
            else:
                pass

            if not os.path.exists(home+"\\password.encrypted"):
                open(home+"\\password.encrypted" , 'x').close()
            else:
                pass
        except:
            print("something gone wrong")

    def create_password(self):
        file_dimension = os.path.getsize(home+"\\password_key.txt")
        if file_dimension == 0:
            self.password_key = Fernet.generate_key()#creo la chiave di codifica della password
            with open(home+"\\password_key.txt" , 'wb') as file: #apro il file che dovrebbe contenere la chiave di cifratura della password
                file.write(self.password_key)#scrivo la chiave nela file
            self.password_provided = input("Create master password: ") #creo la master password
            text_to_append = self.password_provided.encode() #trasformo la password da stringa a bytes
            fernet = Fernet(self.password_key)
            encrypted_data = fernet.encrypt(text_to_append) #cifro la password con la chiave di cifratura
            with open(home+"\\password.encrypted" , 'wb') as file: #apro il file che dovrebbe contenere la password cifrata
                file.write(encrypted_data) #scrivo la password cifrata nel file


        if file_dimension > 0: #se esiste il file che contiene la password
            with open(home+"\\password_key.txt" , 'rb') as file: #apro il file che contiene la chiave di cifratura della password
                self.password_key = file.read() #leggo la chiave di cifratura e la inserisco nella variabile apposita
            self.password_key = self.password_key#.decode() #decodifico la chiave di cifratura
            with open(home+"\\password.encrypted" , 'rb') as file: #apro il file che contiene la password cifrata
                self.password_provided = file.read() #inserisco la password cifrata nell' apposita variabile
            fernet = Fernet(self.password_key)
            decrypted_element = fernet.decrypt(self.password_provided)
            decrypted_element = decrypted_element.decode()
            self.password_provided = decrypted_element


    def input_manager(self):
        os.system('cls')
        print("""                 ###################################################
                 ###################################################
                 ########### WELCOME TO PASSWORD MANAGER ###########
                 ###################################################
                 ################################################### \n\n\n""")
        
        print(self.command_list)
        while not self.can_go:
            action = input("Enter action: ")
            os.system('cls')
            if action == 'insert':
                self.insert_new_record_in_file()
            elif action == 'list':
                self.decrypt_file_content()
            elif action == 'record':
                self.search_record()
            elif action == 'delete':
                self.delete_record()
            elif action == 'help':
                print(self.command_list)
            elif action == 'download':
                self.backup_passwords()
            elif action == 'close':
                self.hide_files()
                os.close(0)
                sys.exit()
            else:
                print(action + " command not found")
    
    def hide_files(self):
        flags = win32file.GetFileAttributesW(home+"\\file.jpg")
        win32file.SetFileAttributes(home+"\\file.jpg", 
        win32con.FILE_ATTRIBUTE_ENCRYPTED | flags)

        flags = win32file.GetFileAttributesW(home+"\\file_key.png")
        win32file.SetFileAttributes(home+"\\file_key.png", 
        win32con.FILE_ATTRIBUTE_ENCRYPTED | flags)

        flags = win32file.GetFileAttributesW(home+"\\password.encrypted")
        win32file.SetFileAttributes(home+"\\password.encrypted", 
        win32con.FILE_ATTRIBUTE_ENCRYPTED | flags)

        flags = win32file.GetFileAttributesW(home+"\\password_key.txt")
        win32file.SetFileAttributes(home+"\\password_key.txt", 
        win32con.FILE_ATTRIBUTE_ENCRYPTED | flags)


ASADMIN = 'asadmin'

if sys.argv[-1] != ASADMIN:
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)

    my_crypto = Crypto()
    my_crypto.check_file()
    my_crypto.create_password()
    my_crypto.login(3)
    my_crypto.input_manager()
