import re
from flask import Flask, render_template, request, jsonify
from database import DataManager, Mahasiswa

app = Flask(__name__)
db = DataManager()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', metrics=db.get_metrics())

@app.route('/mahasiswa')
def mahasiswa_page():
    return render_template('mahasiswa.html')

@app.route('/pencarian')
def pencarian_page():
    return render_template('pencarian.html')

@app.route('/pengurutan')
def pengurutan_page():
    return render_template('pengurutan.html')

# ==================== API Endpoints Utama ====================

@app.route('/api/mahasiswa', methods=['GET'])
def get_all():
    return jsonify([m.to_dict() for m in db.mahasiswa_list])

@app.route('/api/mahasiswa', methods=['POST'])
def add_mhs():
    try:
        data = request.json
        if not re.match(r"^\d{8}$", data['nim']): 
            return jsonify({"success": False, "msg": "NIM harus 8 digit angka"}), 400
        
        mhs = Mahasiswa(data['nim'], data['nama'], data['jurusan'], data['semester'], data['ipk'], data['gender'])
        db.mahasiswa_list.append(mhs)
        db.save_data()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 400

@app.route('/api/mahasiswa/<nim>', methods=['DELETE'])
def delete_mhs(nim):
    db.mahasiswa_list = [m for m in db.mahasiswa_list if m.nim != nim]
    db.save_data()
    return jsonify({"success": True})

# ==================== API Fitur Pencarian & Pengurutan ====================

@app.route('/api/mahasiswa/cari', methods=['GET'])
def api_cari():
    q = request.args.get('q', '')
    return jsonify(db.cari_mahasiswa(q))

@app.route('/api/mahasiswa/urut', methods=['GET'])
def api_urut():
    tipe = request.args.get('by', 'nama')       
    urutan = request.args.get('order', 'asc')   
    return jsonify(db.urut_mahasiswa(tipe, urutan))

# CUKUP SATU SAJA DI PALING BAWAH FILE
if __name__ == '__main__':
    app.run(debug=True, port=5000)