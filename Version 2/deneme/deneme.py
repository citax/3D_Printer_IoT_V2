import os
import sys

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    # Buraya programınızın geri kalanı gelecektir

    # Örnek olarak, kullanıcıdan bir onay alalım
    user_input = input("Programı yeniden başlatmak için 'Y' tuşuna basın, çıkmak için 'N' tuşuna basın: ")
    
    if user_input.upper() == 'Y':
        print("Program yeniden başlatılıyor...")
        restart_program()
    else:
        print("Programdan çıkılıyor...")
