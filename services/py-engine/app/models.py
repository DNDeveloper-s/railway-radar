"""Pydantic models for the RailKit live-train response.

This file mirrors RailKit's response only. The shape that the web app receives is a
different set of models.
"""

from pydantic import BaseModel
from typing import List, Optional


class RouteCoordinate(BaseModel):
    lat: float
    lon: float


class StationPoint(BaseModel):
    code: str
    name: str
    lat: float
    lng: float


class TrainInfo(BaseModel):
    number: str
    name: str
    type: str
    category: str
    source: StationPoint
    destination: StationPoint
    runDays: List[str]
    distance: float
    duration: int
    avgSpeed: float
    totalHalts: int
    coachPosition: str
    rakeType: str


class StationBrief(BaseModel):
    sequence: int
    stnCode: str
    stnName: str
    distance: Optional[float] = None


class CurrentLocation(BaseModel):
    sequence: int
    stnCode: str
    stnName: str
    status: str
    distanceToNextStationKm: float
    nextStation: StationBrief
    distanceFromOriginKm: float
    distanceFromLastStationKm: float
    delayMinutes: int


class Timing(BaseModel):
    scheduled: str
    actual: Optional[str] = None
    delay: Optional[int] = None


class RoutePoint(BaseModel):
    sequence: int
    stnCode: str
    stnName: str
    isHalt: bool
    status: str
    distance: float
    platform: Optional[str] = None
    day: Optional[int] = None
    cord: RouteCoordinate
    arrival: Timing
    departure: Timing


class LiveTrainData(BaseModel):
    startDate: str
    lastUpdatedAt: str
    status: str
    trainInfo: List[TrainInfo]
    isLive: bool
    statusText: str
    currentLocation: CurrentLocation
    previousHalt: StationBrief
    nextHalt: StationBrief
    delayMinutes: int
    route: List[RoutePoint]


class RailKitResponse(BaseModel):
    success: bool
    data: LiveTrainData
