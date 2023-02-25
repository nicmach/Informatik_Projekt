import customtkinter
import hashlib
from urllib.request import urlopen
from termcolor import colored

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry("1000x700")

save_file = customtkinter.IntVar()

def crack_hash(hash):

    try:
        with open('passwords.txt','r') as password_file:
            password_list = str(password_file.read()) # str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt').read(), 'utf-8')
        for password in password_list.split('\n'):
            guess = hashlib.sha256(bytes(password,'utf-8')).hexdigest()
            if guess == hash:
                print(colored('The password is: '+str(password),'green'))
                entry_2.delete(0, customtkinter.END)
                entry_2.insert(0, f"Password: {password}")

                if save_file.get() == 1:
                    f = open("hash.txt", "a")
                    f.write('Hash: ' + str(hash) + '\n')
                    f.write('Password: ' + str(guess) + '\n')

                break
            elif guess != hash:
                continue
            else:
                print(colored('The password does not matched in the list…','red'))
    except Exception as e:
        print('There was a problem: %s' % (e))
        

def create_hash(password):

    with open('passwords.txt','a') as password_file:
            password_file.write(password)

    hash_obj_1=hashlib.md5()
    hash_obj_1.update(password.encode())
    print('md5: ',hash_obj_1.hexdigest())

    hash_obj_2=hashlib.sha1()
    hash_obj_2.update(password.encode())
    print('sha1: ',hash_obj_2.hexdigest())

    hash_obj_3=hashlib.sha256()
    hash_obj_3.update(password.encode())
    print('sha256: ',hash_obj_3.hexdigest())

    hash_obj_4=hashlib.sha224()
    hash_obj_4.update(password.encode())
    print('sha224: ',hash_obj_4.hexdigest())

    hash_obj_5=hashlib.sha512()
    hash_obj_5.update(password.encode())
    print('sha512: ',hash_obj_5.hexdigest())

    entry_4.delete(0, customtkinter.END)
    entry_4.insert(0, f"Sha1: {hash_obj_2.hexdigest()}")

    if save_file.get() == 1:
        f = open("hash.txt", "a")

        f.write('Password: ' + str(password) + '\n')
        f.write('md5: ' + str(hash_obj_1.hexdigest()) + '\n')
        f.write('sha1: ' + str(hash_obj_2.hexdigest()) + '\n')
        f.write('sha256: ' + str(hash_obj_3.hexdigest()) + '\n')
        f.write('sha224: ' + str(hash_obj_4.hexdigest()) + '\n')
        f.write('sha512: ' + str(hash_obj_5.hexdigest()) + '\n')
        f.write('\n')

        f.close()
    


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=100, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Hash Cracker", height=35, width=500, font=('Time New Roman',30,'bold'))
label.pack(pady=12, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame, placeholder_text="Hash", height=35, width=500)
entry_1.pack(pady=12, padx=10)

entry_2 = customtkinter.CTkEntry(master=frame, placeholder_text="Cracked Hash", height=35, width=500)
entry_2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Crack Hash", command=lambda: crack_hash(entry_1.get()), height=35, width=500)
button.pack(pady=12, padx=10)

entry_3 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", height=35, width=500)
entry_3.pack(pady=12, padx=10)

entry_4 = customtkinter.CTkEntry(master=frame, placeholder_text="Password Hash", height=35, width=500)
entry_4.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Create Hash", command=lambda: create_hash(entry_3.get()), height=35, width=500)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Save to file", variable=save_file, onvalue=1, offvalue=0)
checkbox.pack(pady=12, padx=10)

root.mainloop()

