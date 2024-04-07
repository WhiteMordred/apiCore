import subprocess
import cpuinfo
import hashlib
import base64

class EncryptionUtil:
    @staticmethod
    def get_disk_uuid():
        try:
            output = subprocess.check_output(['blkid', '-o', 'value', '-s', 'UUID', '/dev/sda1']).decode().strip()
            return output
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la récupération de l'UUID: {e}")
            return None

    @staticmethod
    def get_cpu_info():
        info = cpuinfo.get_cpu_info()
        return info['brand_raw']

    @staticmethod
    def generate_encryption_key():
        disk_uuid = EncryptionUtil.get_disk_uuid()
        if disk_uuid is None:
            print("UUID du disque non trouvé, impossible de générer la clé de chiffrement.")
            return None
        cpu_serial = EncryptionUtil.get_cpu_info()
        combined_info = f"{disk_uuid}{cpu_serial}".encode()
        key_hash = hashlib.sha256(combined_info).digest()
        key_base64 = base64.urlsafe_b64encode(key_hash).decode()
        return key_base64

    @staticmethod
    def grf(file_path, file_name):
        key = EncryptionUtil.generate_encryption_key()
        if key:
            full_path = f"{file_path}/{file_name}"
            try:
                with open(full_path, "w") as file:
                    file.write(key)
                print(f"Le fichier de récupération a été généré avec succès")
            except Exception as e:
                print(f"Erreur lors de la création du fichier de récupération : {e}")