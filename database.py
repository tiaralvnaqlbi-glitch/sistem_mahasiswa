import json

class Person:
    def __init__(self, nama: str, gender: str):
        self._nama = nama
        self.gender = gender  # "L" atau "P"

class Mahasiswa(Person):
    def __init__(self, nim: str, nama: str, jurusan: str, semester: int, ipk: float, gender: str):
        super().__init__(nama, gender)
        self.__nim = nim
        self.jurusan = jurusan
        self.semester = int(semester)
        self.__ipk = float(ipk)

    @property
    def nim(self): return self.__nim

    @property
    def ipk(self): return self.__ipk

    @ipk.setter
    def ipk(self, value):
        if 0.0 <= float(value) <= 4.0: self.__ipk = float(value)
        else: raise ValueError("IPK harus 0.0 - 4.0")

    def to_dict(self):
        return {
            "nim": self.__nim, "nama": self._nama, "jurusan": self.jurusan,
            "semester": self.semester, "ipk": self.__ipk, "gender": self.gender
        }

class DataManager:
    def __init__(self, file_path="data_mahasiswa.json"):
        self.file_path = file_path
        self.mahasiswa_list = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.mahasiswa_list = [Mahasiswa(**d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.mahasiswa_list = []

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump([m.to_dict() for m in self.mahasiswa_list], f, indent=4)

    def get_metrics(self):
        total = len(self.mahasiswa_list)
        if total == 0: 
            return {"total": 0, "avg_ipk": 0.0, "l": 0, "p": 0}
            
        avg_ipk = sum(m.ipk for m in self.mahasiswa_list) / total
        l_count = sum(1 for m in self.mahasiswa_list if m.gender == "L")
        p_count = sum(1 for m in self.mahasiswa_list if m.gender == "P")
        return {"total": total, "avg_ipk": round(avg_ipk, 2), "l": l_count, "p": p_count}
    
    # ... kode DataManager sebelumnya ...

    def cari_mahasiswa(self, keyword):
        if not keyword:
            return [m.to_dict() for m in self.mahasiswa_list]
        
        keyword = str(keyword).strip().lower()
        hasil = []
        for m in self.mahasiswa_list:
            # Menggunakan str() untuk memastikan NIM angka/teks dikonversi dengan aman sebelum dicari
            nama_mhs = str(m.to_dict().get('nama', '')).lower()
            nim_mhs = str(m.to_dict().get('nim', '')).lower()
            jurusan_mhs = str(m.to_dict().get('jurusan', '')).lower()
            
            if keyword in nim_mhs or keyword in nama_mhs or keyword in jurusan_mhs:
                hasil.append(m.to_dict())
        return hasil

    def urut_mahasiswa(self, tipe, urutan):
        sorted_list = list(self.mahasiswa_list)
        reverse_order = (urutan == "desc")
        
        if tipe == "ipk":
            sorted_list.sort(key=lambda m: float(m.ipk), reverse=reverse_order)
        elif tipe == "semester":
            sorted_list.sort(key=lambda m: int(m.semester), reverse=reverse_order)
        elif tipe == "nim":  # <--- Tambahan jika ingin mengurutkan berdasarkan NIM
            sorted_list.sort(key=lambda m: str(m.nim), reverse=reverse_order)
        elif tipe == "nama":
            sorted_list.sort(key=lambda m: str(m.nama).lower(), reverse=reverse_order)
            
        return [m.to_dict() for m in sorted_list]