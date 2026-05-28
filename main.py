from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date

app= FastAPI(tittle="API de Mundial de Futbol 2026")
# --- Modelos Usados ---
# --- modelo de partidos ---
class Match(BaseModel):
    "id": str
    homeTeam"id": str
    awayTeam"id": str
    date: date
    stadium"id": str
    homeScore: Optional[int] = None
    awayScore: Optional[int] = None
    homePenaltyScore: Optional[int] = None
    awayPenaltyScore: Optional[int] = None
    played: bool = False

# --- modelo de equipos ---
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

# --- modelo de estadios ---
class Stadium(BaseModel):
    id: str
    name: str
    country: str

# --- Bases de Datos ---
# --- BD de equipos ---
teams_db={
  1: { "id": 'MEX', "name": 'México', "flag": 'MEX', "group": 'A', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  2: { "id": 'RSA', "name": 'Sudáfrica', "flag": 'RSA', "group": 'A', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  3: { "id": 'KOR', "name": 'República de Corea', "flag": 'KOR', "group": 'A', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  4: { "id": 'CZE', "name": 'Chequia', "flag": 'CZE', "group": 'A', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  5: { "id": 'CAN', "name": 'Canadá', "flag": 'CAN', "group": 'B', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  6: { "id": 'BIH', "name": 'Bosnia y Herzegovina', "flag": 'BIH', "group": 'B', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  7: { "id": 'QAT', "name": 'Catar', "flag": 'QAT', "group": 'B', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  8: { "id": 'SUI', "name": 'Suiza', "flag": 'SUI', "group": 'B', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  9: { "id": 'BRA', "name": 'Brasil', "flag": 'BRA', "group": 'C', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  10: { "id": 'MAR', "name": 'Marruecos', "flag": 'MAR', "group": 'C', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  11: { "id": 'HAI', "name": 'Haití', "flag": 'HAI', "group": 'C', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  12: { "id": 'SCO', "name": 'Escocia', "flag": 'SCO', "group": 'C', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  13: { "id": 'USA', "name": 'EE. UU.', "flag": 'USA', "group": 'D', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  14: { "id": 'PAR', "name": 'Paraguay', "flag": 'PAR', "group": 'D', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  15: { "id": 'AUS', "name": 'Australia', "flag": 'AUS', "group": 'D', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  16: { "id": 'TUR', "name": 'Turquía', "flag": 'TUR', "group": 'D', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  17: { "id": 'GER', "name": 'Alemania', "flag": 'GER', "group": 'E', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  18: { "id": 'CUW', "name": 'Curazao', "flag": 'CUW', "group": 'E', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  19: { "id": 'CIV', "name": 'Costa de Marfil', "flag": 'CIV', "group": 'E', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  20: { "id": 'ECU', "name": 'Ecuador', "flag": 'ECU', "group": 'E', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  21: { "id": 'NED', "name": 'Países Bajos', "flag": 'NED', "group": 'F', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  22: { "id": 'JPN', "name": 'Japón', "flag": 'JPN', "group": 'F', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  23: { "id": 'SWE', "name": 'Suecia', "flag": 'SWE', "group": 'F', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  24: { "id": 'TUN', "name": 'Túnez', "flag": 'TUN', "group": 'F', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  25: { "id": 'BEL', "name": 'Bélgica', "flag": 'BEL', "group": 'G', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  26: { "id": 'EGY', "name": 'Egipto', "flag": 'EGY', "group": 'G', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  27: { "id": 'IRN', "name": 'Irán', "flag": 'IRN', "group": 'G', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  28: { "id": 'NZL', "name": 'Nueva Zelanda', "flag": 'NZL', "group": 'G', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  29: { "id": 'ESP', "name": 'España', "flag": 'ESP', "group": 'H', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  30: { "id": 'CPV', "name": 'Cabo Verde', "flag": 'CPV', "group": 'H', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  31: { "id": 'KSA', "name": 'Arabia Saudí', "flag": 'KSA', "group": 'H', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  32: { "id": 'URU', "name": 'Uruguay', "flag": 'URU', "group": 'H', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  33: { "id": 'FRA', "name": 'Francia', "flag": 'FRA', "group": 'I', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  34: { "id": 'SEN', "name": 'Senegal', "flag": 'SEN', "group": 'I', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  35: { "id": 'IRQ', "name": 'Irak', "flag": 'IRQ', "group": 'I', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  36: { "id": 'NOR', "name": 'Noruega', "flag": 'NOR', "group": 'I', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  37: { "id": 'ARG', "name": 'Argentina', "flag": 'ARG', "group": 'J', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  38: { "id": 'ALG', "name": 'Argelia', "flag": 'ALG', "group": 'J', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  39: { "id": 'AUT', "name": 'Austria', "flag": 'AUT', "group": 'J', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  40: { "id": 'JOR', "name": 'Jordania', "flag": 'JOR', "group": 'J', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  41: { "id": 'POR', "name": 'Portugal', "flag": 'POR', "group": 'K', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  42: { "id": 'COD', "name": 'RD CONGO', "flag": 'COD', "group": 'K', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  43: { "id": 'UZB', "name": 'Uzbekistán', "flag": 'UZB', "group": 'K', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  44: { "id": 'COL', "name": 'Colombia', "flag": 'COL', "group": 'K', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },

  45: { "id": 'ENG', "name": 'Inglaterra', "flag": 'ENG', "group": 'L', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  46: { "id": 'CRO', "name": 'Croacia', "flag": 'CRO', "group": 'L', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  47: { "id": 'GHA', "name": 'Ghana', "flag": 'GHA', "group": 'L', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
  48: { "id": 'PAN', "name": 'Panamá', "flag": 'PAN', "group": 'L', "played": 0, "won": 0, "drawn": 0, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalsDifference": 0, "pointst": 0 },
}