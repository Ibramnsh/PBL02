import csv
import io
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
# --- [EDIT] Tambahkan import untuk CORSMiddleware dan FileResponse ---
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Cars CRUD API",
    description="API untuk mengelola data mobil dengan fitur upload CSV.",
    version="1.0.0"
)

# --- [EDIT] Tambahkan Konfigurasi CORS Middleware ---
# Ini memungkinkan frontend (HTML/JS) untuk berkomunikasi dengan API ini.
# origins = ["*"] berarti mengizinkan semua sumber. Untuk produksi, lebih baik
# spesifik, contoh: ["http://localhost", "http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Mengizinkan semua header
)

# ---- Model Data ----
class Car(BaseModel):
    id: Optional[int] = None
    brand: str
    model: str
    price: int

# ---- "Database" In-Memory ----
cars_db: Dict[int, Car] = {
    1: Car(id=1, brand='Toyota', model='Avanza', price=250000000),
    2: Car(id=2, brand='Honda', model='Brio', price=180000000)
}
next_car_id = 3

def get_new_id():
    """Fungsi untuk menghasilkan ID unik baru."""
    global next_car_id
    if cars_db:
        max_id = max(cars_db.keys()) if cars_db else 0
        new_id = max_id + 1
    else:
        new_id = 1
    next_car_id = new_id + 1
    return new_id

# --- [EDIT] Endpoint baru untuk menyajikan frontend HTML ---
@app.get("/", include_in_schema=False)
async def read_root():
    """
    Menyajikan file frontend index.html.
    Pastikan file 'index.html' berada di direktori yang sama dengan 'main.py'.
    """
    return FileResponse('templates/index.html')


# ---- Endpoint CRUD (Create, Read, Update, Delete) ----

@app.post("/cars/", response_model=Car, status_code=201, tags=["Cars CRUD"])
def create_car(car: Car):
    """
    Membuat data mobil baru.
    """
    new_id = get_new_id()
    car.id = new_id
    cars_db[new_id] = car
    return car

@app.get("/cars/", response_model=List[Car], tags=["Cars CRUD"])
def read_cars():
    """
    Membaca semua data mobil yang ada di database.
    """
    return list(cars_db.values())

@app.get("/cars/{car_id}", response_model=Car, tags=["Cars CRUD"])
def read_car(car_id: int):
    """
    Membaca data mobil spesifik berdasarkan ID.
    """
    if car_id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Mobil dengan id {car_id} tidak ditemukan")
    return cars_db[car_id]

@app.put("/cars/{car_id}", response_model=Car, tags=["Cars CRUD"])
def update_car(car_id: int, car_update: Car):
    """
    Memperbarui data mobil berdasarkan ID.
    """
    if car_id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Mobil dengan id {car_id} tidak ditemukan")
    
    car_update.id = car_id
    cars_db[car_id] = car_update
    return car_update

@app.delete("/cars/{car_id}", tags=["Cars CRUD"])
def delete_car(car_id: int):
    """
    Menghapus data mobil berdasarkan ID.
    """
    if car_id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Mobil dengan id {car_id} tidak ditemukan")
    del cars_db[car_id]
    return JSONResponse(status_code=200, content={"message": f"Mobil dengan id {car_id} berhasil dihapus"})


# ---- Endpoint untuk Upload File CSV ----

@app.post("/upload-csv/", tags=["File Upload"])
async def upload_cars_csv(file: UploadFile = File(...)):
    """
    Mengunggah file CSV dan memuat datanya.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berformat CSV")

    contents = await file.read()
    buffer = io.StringIO(contents.decode('utf-8'))
    csv_reader = csv.DictReader(buffer)
    
    loaded_count = 0
    try:
        for row in csv_reader:
            car_data = Car(
                id=int(row['id']),
                brand=row['brand'],
                model=row['model'],
                price=int(row['price'])
            )
            cars_db[car_data.id] = car_data
            loaded_count += 1
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Error memproses file CSV: {e}")

    return {"message": f"{loaded_count} mobil berhasil dimuat dari file {file.filename}."}

# Jalankan server Uvicorn jika file ini dieksekusi secara langsung
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)