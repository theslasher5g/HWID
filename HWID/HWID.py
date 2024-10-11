import os
import subprocess
import psutil
import shutil

def find_usb_drive():

    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'removable' in partition.opts.lower() or 'usb' in partition.opts.lower():
            return partition.device
    return None

def get_hardware_hash():

    try:
        result = subprocess.run('wmic csproduct get UUID', shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n')[-1].strip()
    except Exception as e:
        print(f"Fehler beim Abrufen des Hardware-Hash: {e}")
        return None

def get_serial_number():

    try:
        result = subprocess.run('wmic bios get SerialNumber', shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n')[-1].strip()
    except Exception as e:
        print(f"Fehler beim Abrufen der Seriennummer: {e}")
        return None

def get_windows_product_id():

    try:
        result = subprocess.run('wmic os get SerialNumber', shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n')[-1].strip()
    except Exception as e:
        print(f"Fehler beim Abrufen der Windows Product ID: {e}")
        return None

def main():

    display_name = input("Geben Sie den Display Name ein: ")
    group_tag = input("Geben Sie den Group Tag ein: ")


    hardware_hash = get_hardware_hash()
    serial_number = get_serial_number()
    windows_product_id = get_windows_product_id()


    if not hardware_hash or not serial_number or not windows_product_id:
        print("Es konnten nicht alle benötigten Informationen abgerufen werden.")
        return


    usb_drive = find_usb_drive()
    if not usb_drive:
        print("Kein USB-Laufwerk gefunden. Bitte stecken Sie einen USB-Stick ein.")
        return


    usb_path = os.path.join(usb_drive, "HWID")
    os.makedirs(usb_path, exist_ok=True)

    # Pfad für die Datei auf dem USB-Stick
    usb_hwid_file = os.path.join(usb_path, "HWID_Collection.csv")

    # Überprüfen, ob die Datei bereits existiert, und die Kopfzeile nur einmal schreiben
    file_exists = os.path.exists(usb_hwid_file)
    with open(usb_hwid_file, mode='a', newline='') as file:
        if not file_exists:
            # Schreibe die Kopfzeile, falls die Datei neu erstellt wird
            file.write("Display Name,Group Tag,Device Serial Number,Windows Product ID,Hardware Hash\n")
        # Schreibe die neue Zeile mit den gesammelten Informationen
        file.write(f"{display_name},{group_tag},{serial_number},{windows_product_id},{hardware_hash}\n")

    print(f"Hardware-Informationen erfolgreich auf USB-Stick in '{usb_hwid_file}' gespeichert.")

if __name__ == "__main__":
    main()
