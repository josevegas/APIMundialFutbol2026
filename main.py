import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# Cargar variables de entorno desde .env
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")  # Permitir múltiples orígenes separados por comas
if not MONGODB_URI:
    raise ValueError("MONGODB_URI no está definida en el archivo .env")

# Inicializar cliente y base de datos
client = AsyncIOMotorClient(MONGODB_URI)
db = client["mundial2026"]
teams_collection = db["teams"]
stadiums_collection = db["stadiums"]
matches_collection = db["matches"]

app = FastAPI(title="API de Mundial de Futbol 2026")
origins = CORS_ORIGINS if CORS_ORIGINS != ["http://localhost:5173"] else ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Modelos Usados ---
class Match(BaseModel):
    id: str
    homeTeamId: str
    awayTeamId: str
    date: str
    stadiumId: str
    stage: str
    group: Optional[str] = None
    homeScore: Optional[int] = None
    awayScore: Optional[int] = None
    homePenaltyScore: Optional[int] = None
    awayPenaltyScore: Optional[int] = None
    isCompleted: bool = False
    winnerId: Optional[str] = None

class Team(BaseModel):
    id: str
    name: str
    group: Optional[str] = None
    flag: Optional[str] = None
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goalsFor: int = 0
    goalsAgainst: int = 0
    goalDifference: int = 0
    points: int = 0

class Stadium(BaseModel):
    id: str
    name: str
    country: str

class MatchUpdate(BaseModel):
    homeTeamGoals: int
    awayTeamGoals: int
    homeTeamPenaltyGoals: Optional[int] = None
    awayTeamPenaltyGoals: Optional[int] = None
    winnerId: Optional[str] = None

# --- Datos iniciales ---
teams_data = {
    'MEX': {"id": 'MEX', "name": 'México', "flag": 'MEX', "group": 'A'},
    'RSA': {"id": 'RSA', "name": 'Sudáfrica', "flag": 'RSA', "group": 'A'},
    'KOR': {"id": 'KOR', "name": 'República de Corea', "flag": 'KOR', "group": 'A'},
    'CZE': {"id": 'CZE', "name": 'Chequia', "flag": 'CZE', "group": 'A'},
    'CAN': {"id": 'CAN', "name": 'Canadá', "flag": 'CAN', "group": 'B'},
    'BIH': {"id": 'BIH', "name": 'Bosnia y Herzegovina', "flag": 'BIH', "group": 'B'},
    'QAT': {"id": 'QAT', "name": 'Catar', "flag": 'QAT', "group": 'B'},
    'SUI': {"id": 'SUI', "name": 'Suiza', "flag": 'SUI', "group": 'B'},
    'BRA': {"id": 'BRA', "name": 'Brasil', "flag": 'BRA', "group": 'C'},
    'MAR': {"id": 'MAR', "name": 'Marruecos', "flag": 'MAR', "group": 'C'},
    'HAI': {"id": 'HAI', "name": 'Haití', "flag": 'HAI', "group": 'C'},
    'SCO': {"id": 'SCO', "name": 'Escocia', "flag": 'SCO', "group": 'C'},
    'USA': {"id": 'USA', "name": 'EE. UU.', "flag": 'USA', "group": 'D'},
    'PAR': {"id": 'PAR', "name": 'Paraguay', "flag": 'PAR', "group": 'D'},
    'AUS': {"id": 'AUS', "name": 'Australia', "flag": 'AUS', "group": 'D'},
    'TUR': {"id": 'TUR', "name": 'Turquía', "flag": 'TUR', "group": 'D'},
    'GER': {"id": 'GER', "name": 'Alemania', "flag": 'GER', "group": 'E'},
    'CUW': {"id": 'CUW', "name": 'Curazao', "flag": 'CUW', "group": 'E'},
    'CIV': {"id": 'CIV', "name": 'Costa de Marfil', "flag": 'CIV', "group": 'E'},
    'ECU': {"id": 'ECU', "name": 'Ecuador', "flag": 'ECU', "group": 'E'},
    'NED': {"id": 'NED', "name": 'Países Bajos', "flag": 'NED', "group": 'F'},
    'JPN': {"id": 'JPN', "name": 'Japón', "flag": 'JPN', "group": 'F'},
    'SWE': {"id": 'SWE', "name": 'Suecia', "flag": 'SWE', "group": 'F'},
    'TUN': {"id": 'TUN', "name": 'Túnez', "flag": 'TUN', "group": 'F'},
    'BEL': {"id": 'BEL', "name": 'Bélgica', "flag": 'BEL', "group": 'G'},
    'EGY': {"id": 'EGY', "name": 'Egipto', "flag": 'EGY', "group": 'G'},
    'IRN': {"id": 'IRN', "name": 'Irán', "flag": 'IRN', "group": 'G'},
    'NZL': {"id": 'NZL', "name": 'Nueva Zelanda', "flag": 'NZL', "group": 'G'},
    'ESP': {"id": 'ESP', "name": 'España', "flag": 'ESP', "group": 'H'},
    'CPV': {"id": 'CPV', "name": 'Cabo Verde', "flag": 'CPV', "group": 'H'},
    'KSA': {"id": 'KSA', "name": 'Arabia Saudí', "flag": 'KSA', "group": 'H'},
    'URU': {"id": 'URU', "name": 'Uruguay', "flag": 'URU', "group": 'H'},
    'FRA': {"id": 'FRA', "name": 'Francia', "flag": 'FRA', "group": 'I'},
    'SEN': {"id": 'SEN', "name": 'Senegal', "flag": 'SEN', "group": 'I'},
    'IRQ': {"id": 'IRQ', "name": 'Irak', "flag": 'IRQ', "group": 'I'},
    'NOR': {"id": 'NOR', "name": 'Noruega', "flag": 'NOR', "group": 'I'},
    'ARG': {"id": 'ARG', "name": 'Argentina', "flag": 'ARG', "group": 'J'},
    'ALG': {"id": 'ALG', "name": 'Argelia', "flag": 'ALG', "group": 'J'},
    'AUT': {"id": 'AUT', "name": 'Austria', "flag": 'AUT', "group": 'J'},
    'JOR': {"id": 'JOR', "name": 'Jordania', "flag": 'JOR', "group": 'J'},
    'POR': {"id": 'POR', "name": 'Portugal', "flag": 'POR', "group": 'K'},
    'COD': {"id": 'COD', "name": 'RD CONGO', "flag": 'COD', "group": 'K'},
    'UZB': {"id": 'UZB', "name": 'Uzbekistán', "flag": 'UZB', "group": 'K'},
    'COL': {"id": 'COL', "name": 'Colombia', "flag": 'COL', "group": 'K'},
    'ENG': {"id": 'ENG', "name": 'Inglaterra', "flag": 'ENG', "group": 'L'},
    'CRO': {"id": 'CRO', "name": 'Croacia', "flag": 'CRO', "group": 'L'},
    'GHA': {"id": 'GHA', "name": 'Ghana', "flag": 'GHA', "group": 'L'},
    'PAN': {"id": 'PAN', "name": 'Panamá', "flag": 'PAN', "group": 'L'},
}

stadiums_data = {
    'EAZ': {"id": 'EAZ', "name": 'Estadio Azteca, Ciudad de México', "country": 'México'},
    'EAK': {"id": 'EAK', "name": 'Estadio Akron, Guadalajara', "country": 'México'},
    'EBB': {"id": 'EBB', "name": 'Estadio BBVA, Monterrey', "country": 'México'},
    'MBS': {"id": 'MBS', "name": 'Mercedes-Benz Stadium, Atlanta', "country": 'EE. UU.'},
    'LES': {"id": 'LES', "name": "Levi's Stadium, San Francisco", "country": 'EE. UU.'},
    'SFS': {"id": 'SFS', "name": 'SoFi Stadium, Los Angeles', "country": 'EE. UU.'},
    'LUS': {"id": 'LUS', "name": 'Lumen Stadium, Seattle', "country": 'EE. UU.'},
    'MLS': {"id": 'MLS', "name": 'MetLife Stadium, NY/NJ', "country": 'EE. UU.'},
    'GIS': {"id": 'GIS', "name": 'Gillette Stadium, Boston', "country": 'EE. UU.'},
    'LFF': {"id": 'LFF', "name": 'Lincoln Financial Field, Philadelphia', "country": 'EE. UU.'},
    'HRS': {"id": 'HRS', "name": 'Hard Rock Stadium, Miami Garden', "country": 'EE. UU.'},
    'NRS': {"id": 'NRS', "name": 'NRG Stadium, Houston', "country": 'EE. UU.'},
    'AHS': {"id": 'AHS', "name": 'Arrowhead Stadium, Kansas City', "country": 'EE. UU.'},
    'ATS': {"id": 'ATS', "name": 'AT&T Stadium, Dallas', "country": 'EE. UU.'},
    'BMO': {"id": 'BMO', "name": 'BMO Field, Toronto', "country": 'Canadá'},
    'BCP': {"id": 'BCP', "name": 'BC Place, Vancouver', "country": 'Canadá'},
}

matches_data = {
    'M1': { "id": 'M1', "group": 'A', "homeTeamId": 'MEX', "awayTeamId": 'RSA', "date": '2026-06-11T16:00:00Z', "stadiumId": 'EAZ', "stage": 'GROUP' },
    'M2': { "id": 'M2', "group": 'A', "homeTeamId": 'KOR', "awayTeamId": 'CZE', "date": '2026-06-11T20:00:00Z', "stadiumId": 'EAK', "stage": 'GROUP' },
    'M3': { "id": 'M3', "group": 'B', "homeTeamId": 'CAN', "awayTeamId": 'BIH', "date": '2026-06-12T17:00:00Z', "stadiumId": 'BMO', "stage": 'GROUP' },
    'M4': { "id": 'M4', "group": 'D', "homeTeamId": 'USA', "awayTeamId": 'PAR', "date": '2026-06-12T21:00:00Z', "stadiumId": 'SFS', "stage": 'GROUP' },
    'M5': { "id": 'M5', "group": 'B', "homeTeamId": 'QAT', "awayTeamId": 'SUI', "date": '2026-06-13T15:00:00Z', "stadiumId": 'LES', "stage": 'GROUP' },
    'M6': { "id": 'M6', "group": 'C', "homeTeamId": 'BRA', "awayTeamId": 'MAR', "date": '2026-06-13T18:00:00Z', "stadiumId": 'MLS', "stage": 'GROUP' },
    'M7': { "id": 'M7', "group": 'C', "homeTeamId": 'HAI', "awayTeamId": 'SCO', "date": '2026-06-13T21:00:00Z', "stadiumId": 'GIS', "stage": 'GROUP' },
    'M8': { "id": 'M8', "group": 'D', "homeTeamId": 'AUS', "awayTeamId": 'TUR', "date": '2026-06-13T23:00:00Z', "stadiumId": 'BCP', "stage": 'GROUP' },
    'M9': { "id": 'M9', "group": 'E', "homeTeamId": 'GER', "awayTeamId": 'CUW', "date": '2026-06-14T13:00:00Z', "stadiumId": 'NRS', "stage": 'GROUP' },
    'M10': { "id": 'M10', "group": 'F', "homeTeamId": 'NED', "awayTeamId": 'JPN', "date": '2026-06-14T16:00:00Z', "stadiumId": 'ATS', "stage": 'GROUP' },
    'M11': { "id": 'M11', "group": 'E', "homeTeamId": 'CIV', "awayTeamId": 'ECU', "date": '2026-06-14T19:00:00Z', "stadiumId": 'LFF', "stage": 'GROUP' },
    'M12': { "id": 'M12', "group": 'F', "homeTeamId": 'SWE', "awayTeamId": 'TUN', "date": '2026-06-14T22:00:00Z', "stadiumId": 'EBB', "stage": 'GROUP' },
    'M13': { "id": 'M13', "group": 'H', "homeTeamId": 'ESP', "awayTeamId": 'CPV', "date": '2026-06-15T12:00:00Z', "stadiumId": 'MBS', "stage": 'GROUP' },
    'M14': { "id": 'M14', "group": 'G', "homeTeamId": 'BEL', "awayTeamId": 'EGY', "date": '2026-06-15T15:00:00Z', "stadiumId": 'LUS', "stage": 'GROUP' },
    'M15': { "id": 'M15', "group": 'H', "homeTeamId": 'KSA', "awayTeamId": 'URU', "date": '2026-06-15T18:00:00Z', "stadiumId": 'HRS', "stage": 'GROUP' },
    'M16': { "id": 'M16', "group": 'G', "homeTeamId": 'IRN', "awayTeamId": 'NZL', "date": '2026-06-15T21:00:00Z', "stadiumId": 'SFS', "stage": 'GROUP' },
    'M17': { "id": 'M17', "group": 'I', "homeTeamId": 'FRA', "awayTeamId": 'SEN', "date": '2026-06-16T15:00:00Z', "stadiumId": 'MLS', "stage": 'GROUP' },
    'M18': { "id": 'M18', "group": 'I', "homeTeamId": 'IRQ', "awayTeamId": 'NOR', "date": '2026-06-16T18:00:00Z', "stadiumId": 'GIS', "stage": 'GROUP' },
    'M19': { "id": 'M19', "group": 'J', "homeTeamId": 'ARG', "awayTeamId": 'ALG', "date": '2026-06-16T21:00:00Z', "stadiumId": 'AHS', "stage": 'GROUP' },
    'M20': { "id": 'M20', "group": 'J', "homeTeamId": 'AUT', "awayTeamId": 'JOR', "date": '2026-06-16T00:00:00Z', "stadiumId": 'LES', "stage": 'GROUP' },
    'M21': { "id": 'M21', "group": 'K', "homeTeamId": 'POR', "awayTeamId": 'COD', "date": '2026-06-17T13:00:00Z', "stadiumId": 'NRS', "stage": 'GROUP' },
    'M22': { "id": 'M22', "group": 'L', "homeTeamId": 'ENG', "awayTeamId": 'CRO', "date": '2026-06-17T16:00:00Z', "stadiumId": 'ATS', "stage": 'GROUP' },
    'M23': { "id": 'M23', "group": 'L', "homeTeamId": 'GHA', "awayTeamId": 'PAN', "date": '2026-06-17T19:00:00Z', "stadiumId": 'BMO', "stage": 'GROUP' },
    'M24': { "id": 'M24', "group": 'K', "homeTeamId": 'UZB', "awayTeamId": 'COL', "date": '2026-06-17T22:00:00Z', "stadiumId": 'EAZ', "stage": 'GROUP' },
    'M25': { "id": 'M25', "group": 'A', "homeTeamId": 'CZE', "awayTeamId": 'RSA', "date": '2026-06-18T12:00:00Z', "stadiumId": 'MBS', "stage": 'GROUP' },
    'M26': { "id": 'M26', "group": 'B', "homeTeamId": 'SUI', "awayTeamId": 'BIH', "date": '2026-06-18T15:00:00Z', "stadiumId": 'EAK', "stage": 'GROUP' },
    'M27': { "id": 'M27', "group": 'B', "homeTeamId": 'CAN', "awayTeamId": 'QAT', "date": '2026-06-18T18:00:00Z', "stadiumId": 'BCP', "stage": 'GROUP' },
    'M28': { "id": 'M28', "group": 'A', "homeTeamId": 'MEX', "awayTeamId": 'KOR', "date": '2026-06-18T21:00:00Z', "stadiumId": 'EAK', "stage": 'GROUP' },
    'M29': { "id": 'M29', "group": 'D', "homeTeamId": 'USA', "awayTeamId": 'AUT', "date": '2026-06-19T15:00:00Z', "stadiumId": 'LUS', "stage": 'GROUP' },
    'M30': { "id": 'M30', "group": 'C', "homeTeamId": 'SCO', "awayTeamId": 'MAR', "date": '2026-06-19T18:00:00Z', "stadiumId": 'GIS', "stage": 'GROUP' },
    'M31': { "id": 'M31', "group": 'C', "homeTeamId": 'BRA', "awayTeamId": 'HAI', "date": '2026-06-19T21:00:00Z', "stadiumId": 'LFF', "stage": 'GROUP' },
    'M32': { "id": 'M32', "group": 'D', "homeTeamId": 'TUR', "awayTeamId": 'PAR', "date": '2026-06-19T00:00:00Z', "stadiumId": 'LES', "stage": 'GROUP' },
    'M33': { "id": 'M33', "group": 'F', "homeTeamId": 'NED', "awayTeamId": 'SWE', "date": '2026-06-20T13:00:00Z', "stadiumId": 'NRS', "stage": 'GROUP' },
    'M34': { "id": 'M34', "group": 'E', "homeTeamId": 'GER', "awayTeamId": 'CIV', "date": '2026-06-20T16:00:00Z', "stadiumId": 'BMO', "stage": 'GROUP' },
    'M35': { "id": 'M35', "group": 'E', "homeTeamId": 'ECU', "awayTeamId": 'CUW', "date": '2026-06-20T22:00:00Z', "stadiumId": 'AHS', "stage": 'GROUP' },
    'M36': { "id": 'M36', "group": 'F', "homeTeamId": 'TUN', "awayTeamId": 'JPN', "date": '2026-06-20T00:00:00Z', "stadiumId": 'EBB', "stage": 'GROUP' },
    'M37': { "id": 'M37', "group": 'H', "homeTeamId": 'ESP', "awayTeamId": 'KSA', "date": '2026-06-21T12:00:00Z', "stadiumId": 'MBS', "stage": 'GROUP' },
    'M38': { "id": 'M38', "group": 'G', "homeTeamId": 'BEL', "awayTeamId": 'IRN', "date": '2026-06-21T15:00:00Z', "stadiumId": 'SFS', "stage": 'GROUP' },
    'M39': { "id": 'M39', "group": 'H', "homeTeamId": 'URU', "awayTeamId": 'CPV', "date": '2026-06-21T18:00:00Z', "stadiumId": 'HRS', "stage": 'GROUP' },
    'M40': { "id": 'M40', "group": 'G', "homeTeamId": 'NZL', "awayTeamId": 'EGY', "date": '2026-06-21T21:00:00Z', "stadiumId": 'BCP', "stage": 'GROUP' },
    'M41': { "id": 'M41', "group": 'J', "homeTeamId": 'ARG', "awayTeamId": 'AUT', "date": '2026-06-22T13:00:00Z', "stadiumId": 'ATS', "stage": 'GROUP' },
    'M42': { "id": 'M42', "group": 'I', "homeTeamId": 'FRA', "awayTeamId": 'IRQ', "date": '2026-06-22T17:00:00Z', "stadiumId": 'LFF', "stage": 'GROUP' },
    'M43': { "id": 'M43', "group": 'I', "homeTeamId": 'NOR', "awayTeamId": 'SEN', "date": '2026-06-22T20:00:00Z', "stadiumId": 'MLS', "stage": 'GROUP' },
    'M44': { "id": 'M44', "group": 'J', "homeTeamId": 'JOR', "awayTeamId": 'ALG', "date": '2026-06-22T23:00:00Z', "stadiumId": 'LES', "stage": 'GROUP' },
    'M45': { "id": 'M45', "group": 'K', "homeTeamId": 'POR', "awayTeamId": 'UZB', "date": '2026-06-23T13:00:00Z', "stadiumId": 'NRS', "stage": 'GROUP' },
    'M46': { "id": 'M46', "group": 'L', "homeTeamId": 'ENG', "awayTeamId": 'GHA', "date": '2026-06-23T16:00:00Z', "stadiumId": 'GIS', "stage": 'GROUP' },
    'M47': { "id": 'M47', "group": 'L', "homeTeamId": 'PAN', "awayTeamId": 'CRO', "date": '2026-06-23T19:00:00Z', "stadiumId": 'BMO', "stage": 'GROUP' },
    'M48': { "id": 'M48', "group": 'K', "homeTeamId": 'COL', "awayTeamId": 'COD', "date": '2026-06-23T22:00:00Z', "stadiumId": 'EAK', "stage": 'GROUP' },
    'M49': { "id": 'M49', "group": 'B', "homeTeamId": 'SUI', "awayTeamId": 'CAN', "date": '2026-06-24T15:00:00Z', "stadiumId": 'BCP', "stage": 'GROUP' },
    'M50': { "id": 'M50', "group": 'B', "homeTeamId": 'BIH', "awayTeamId": 'QAT', "date": '2026-06-24T15:00:00Z', "stadiumId": 'LUS', "stage": 'GROUP' },
    'M51': { "id": 'M51', "group": 'C', "homeTeamId": 'SCO', "awayTeamId": 'BRA', "date": '2026-06-24T18:00:00Z', "stadiumId": 'HRS', "stage": 'GROUP' },
    'M52': { "id": 'M52', "group": 'C', "homeTeamId": 'MAR', "awayTeamId": 'HAI', "date": '2026-06-24T18:00:00Z', "stadiumId": 'MBS', "stage": 'GROUP' },
    'M53': { "id": 'M53', "group": 'A', "homeTeamId": 'CZE', "awayTeamId": 'MEX', "date": '2026-06-24T21:00:00Z', "stadiumId": 'CDM', "stage": 'GROUP' },
    'M54': { "id": 'M54', "group": 'A', "homeTeamId": 'RSA', "awayTeamId": 'KOR', "date": '2026-06-24T21:00:00Z', "stadiumId": 'EBB', "stage": 'GROUP' },
    'M55': { "id": 'M55', "group": 'E', "homeTeamId": 'CUW', "awayTeamId": 'CIV', "date": '2026-06-25T16:00:00Z', "stadiumId": 'LFF', "stage": 'GROUP' },
    'M56': { "id": 'M56', "group": 'E', "homeTeamId": 'ECU', "awayTeamId": 'GER', "date": '2026-06-25T16:00:00Z', "stadiumId": 'MLS', "stage": 'GROUP' },
    'M57': { "id": 'M57', "group": 'F', "homeTeamId": 'JPN', "awayTeamId": 'SWE', "date": '2026-06-25T19:00:00Z', "stadiumId": 'ATS', "stage": 'GROUP' },
    'M58': { "id": 'M58', "group": 'F', "homeTeamId": 'TUN', "awayTeamId": 'NED', "date": '2026-06-25T19:00:00Z', "stadiumId": 'AHS', "stage": 'GROUP' },
    'M59': { "id": 'M59', "group": 'D', "homeTeamId": 'TUR', "awayTeamId": 'USA', "date": '2026-06-25T22:00:00Z', "stadiumId": 'SFS', "stage": 'GROUP' },
    'M60': { "id": 'M60', "group": 'D', "homeTeamId": 'PAR', "awayTeamId": 'AUS', "date": '2026-06-25T22:00:00Z', "stadiumId": 'LES', "stage": 'GROUP' },
    'M61': { "id": 'M61', "group": 'I', "homeTeamId": 'NOR', "awayTeamId": 'FRA', "date": '2026-06-26T15:00:00Z', "stadiumId": 'GIS', "stage": 'GROUP' },
    'M62': { "id": 'M62', "group": 'I', "homeTeamId": 'SEN', "awayTeamId": 'IRQ', "date": '2026-06-26T15:00:00Z', "stadiumId": 'BMO', "stage": 'GROUP' },
    'M63': { "id": 'M63', "group": 'H', "homeTeamId": 'CPV', "awayTeamId": 'KSA', "date": '2026-06-26T20:00:00Z', "stadiumId": 'NRS', "stage": 'GROUP' },
    'M64': { "id": 'M64', "group": 'H', "homeTeamId": 'URU', "awayTeamId": 'ESP', "date": '2026-06-26T20:00:00Z', "stadiumId": 'EAK', "stage": 'GROUP' },
    'M65': { "id": 'M65', "group": 'G', "homeTeamId": 'EGY', "awayTeamId": 'IRN', "date": '2026-06-26T23:00:00Z', "stadiumId": 'LUS', "stage": 'GROUP' },
    'M66': { "id": 'M66', "group": 'G', "homeTeamId": 'NZL', "awayTeamId": 'BEL', "date": '2026-06-26T23:00:00Z', "stadiumId": 'BCP', "stage": 'GROUP' },
    'M67': { "id": 'M67', "group": 'L', "homeTeamId": 'PAN', "awayTeamId": 'ENG', "date": '2026-06-27T17:00:00Z', "stadiumId": 'MLS', "stage": 'GROUP' },
    'M68': { "id": 'M68', "group": 'L', "homeTeamId": 'CRO', "awayTeamId": 'GHA', "date": '2026-06-27T17:00:00Z', "stadiumId": 'LFF', "stage": 'GROUP' },
    'M69': { "id": 'M69', "group": 'K', "homeTeamId": 'COL', "awayTeamId": 'POR', "date": '2026-06-27T19:30:00Z', "stadiumId": 'HRS', "stage": 'GROUP' },
    'M70': { "id": 'M70', "group": 'K', "homeTeamId": 'COD', "awayTeamId": 'UZB', "date": '2026-06-27T19:30:00Z', "stadiumId": 'MBS', "stage": 'GROUP' },
    'M71': { "id": 'M71', "group": 'J', "homeTeamId": 'ALG', "awayTeamId": 'AUT', "date": '2026-06-27T22:00:00Z', "stadiumId": 'AHS', "stage": 'GROUP' },
    'M72': { "id": 'M72', "group": 'J', "homeTeamId": 'JOR', "awayTeamId": 'ARG', "date": '2026-06-27T22:00:00Z', "stadiumId": 'ATS', "stage": 'GROUP' },
}

# --- Función para inicializar datos ---
async def initialize_database():
    """Inicializa las colecciones de MongoDB con datos si están vacías"""
    await teams_collection.create_index("id", unique=True)
    await stadiums_collection.create_index("id", unique=True)
    await matches_collection.create_index("id", unique=True)
    # Inicializar equipos
    for team_id, team_data in teams_data.items():
        team_doc = team_data.copy()
        team_doc.update({"played": 0, "won": 0, "drawn": 0, "lost": 0,
                        "goalsFor": 0, "goalsAgainst": 0, "goalDifference": 0, "points": 0})
        await teams_collection.update_one(
            {"id": team_id}, 
            {"$setOnInsert": team_doc}, 
            upsert=True
        )
    
    # Inicializar estadios
    for stadium_id, stadium_data in stadiums_data.items():
        await stadiums_collection.update_one(
            {"id": stadium_id}, 
            {"$setOnInsert": stadium_data}, 
            upsert=True
        )
    
    # Inicializar partidos
    for match_id, match_data in matches_data.items():
        match_doc = match_data.copy()
        match_doc.update({"homeScore": None, 
                          "awayScore":None, 
                          "homePenaltyScore": None, 
                          "awayPenaltyScore": None, 
                          "isCompleted": False, 
                          "winnerId": None})
        await matches_collection.update_one(
            {"id": match_id}, 
            {"$setOnInsert": match_doc}, 
            upsert=True
        )

# --- Eventos de startup ---
@app.on_event("startup")
async def startup_event():
    print("Inicializando base de datos MongoDB...")
    await initialize_database()
    print("Base de datos inicializada correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    print("Cerrando conexión con MongoDB...")
    client.close()

# --- Endpoints de partidos ---
@app.get("/matches/", response_model=List[dict], summary="Obtener la lista de partidos")
async def get_matches():
    matches = await matches_collection.find({}, {"_id": 0}).to_list(length=100)
    return matches

@app.get("/stadiums/", response_model=List[dict], summary="Obtener la lista de estadios")
async def get_stadiums():
    stadiums = await stadiums_collection.find({}, {"_id": 0}).to_list(length=100)
    return stadiums

@app.patch("/matches/{match_id}", summary="Actualizar el resultado de un partido")
async def update_match(match_id: str, match_update: MatchUpdate):
    match = await matches_collection.update_one(
        {"id": match_id},
        {"$set": {
            "homeScore": match_update.homeTeamGoals,
            "awayScore": match_update.awayTeamGoals,
            "homePenaltyScore": match_update.homeTeamPenaltyGoals,
            "awayPenaltyScore": match_update.awayTeamPenaltyGoals,
            "isCompleted": True,
            "winnerId": match_update.winnerId
        }}
    )
        
    if match.matched_count == 0:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    partido_actualizado = await matches_collection.find_one({"id": match_id}, {"_id": 0})
    return partido_actualizado

# --- Endpoint para obtener partidos por grupo ---
@app.get("/matches/group/{group_id}", response_model=List[dict], summary="Obtener partidos por grupo")
async def get_matches_by_group(group_id: str):
    group_upper = group_id.upper()
    matches = await matches_collection.find({"group": group_upper}, {"_id": 0}).to_list(length=100)
    return matches

# --- Endpoint de Tabla de posiciones ---
@app.get("/teams/", summary="Obtener la tabla de posiciones actualizada")
async def obtener_tabla():
    # Reiniciar estadísticas
    await teams_collection.update_many({}, {
        "$set": {
            "played": 0, "won": 0, "drawn": 0, "lost": 0,
            "goalsFor": 0, "goalsAgainst": 0, "goalDifference": 0, "points": 0
        }
    })
    
    # Actualizar estadísticas según resultados de partidos
    matches = await matches_collection.find({"isCompleted": True},{"_id": 0}).to_list(length=100)
    
    for match in matches:
        home_team_id = match.get("homeTeamId")
        away_team_id = match.get("awayTeamId")
        home_goals = match.get("homeScore", 0)
        away_goals = match.get("awayScore", 0)
        
        # Obtener equipos
        home_team = await teams_collection.find_one({"id": home_team_id},{"_id": 0})
        away_team = await teams_collection.find_one({"id": away_team_id},{"_id": 0})
        
        if home_team and away_team:
            # Actualizar estadísticas
            if home_goals > away_goals:
                await teams_collection.update_one(
                    {"id": home_team_id},
                    {"$inc": {"played": 1, "won": 1, "goalsFor": home_goals, "goalsAgainst": away_goals, "points": 3}}
                )
                await teams_collection.update_one(
                    {"id": away_team_id},
                    {"$inc": {"played": 1, "lost": 1, "goalsFor": away_goals, "goalsAgainst": home_goals}}
                )
            elif home_goals < away_goals:
                await teams_collection.update_one(
                    {"id": home_team_id},
                    {"$inc": {"played": 1, "lost": 1, "goalsFor": home_goals, "goalsAgainst": away_goals}}
                )
                await teams_collection.update_one(
                    {"id": away_team_id},
                    {"$inc": {"played": 1, "won": 1, "goalsFor": away_goals, "goalsAgainst": home_goals, "points": 3}}
                )
            else:
                await teams_collection.update_one(
                    {"id": home_team_id},
                    {"$inc": {"played": 1, "drawn": 1, "goalsFor": home_goals, "goalsAgainst": away_goals, "points": 1}}
                )
                await teams_collection.update_one(
                    {"id": away_team_id},
                    {"$inc": {"played": 1, "drawn": 1, "goalsFor": away_goals, "goalsAgainst": home_goals, "points": 1}}
                )
    
    # Calcular diferencia de goles
    teams = await teams_collection.find({},{"_id": 0}).to_list(length=100)
    for team in teams:
        goal_difference = team.get("goalsFor", 0) - team.get("goalsAgainst", 0)
        await teams_collection.update_one(
            {"id": team["id"]},
            {"$set": {"goalDifference": goal_difference}}
        )
    
    # Ordenar tabla
    sorted_teams = await teams_collection.find({},{"_id": 0}).sort([
        ("points", -1),
        ("goalDifference", -1),
        ("goalsFor", -1)
    ]).to_list(length=100)
    
    return sorted_teams

# --- Endpoint raíz ---
@app.get("/", summary="API de Mundial de Fútbol 2026")
async def root():
    return {"mensaje": "API de Mundial de Futbol 2026 con MongoDB", "endpoints": [
        "/docs - Documentación interactiva",
        "/matches/ - Lista de partidos",
        "/teams/ - Datos de equipos y tabla de posiciones",
        "/stadiums/ - Lista de estadios",
        "/matches/{match_id} - Actualizar resultado de un partido",
        "/matches/group/{group_id} - Obtener partidos por grupo"
    ]}
