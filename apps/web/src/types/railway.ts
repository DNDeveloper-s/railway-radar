export type TrainStatus = "ON_TIME" | "DELAYED" | "CANCELLED";

export interface StationCoordinate {
  latitude: number;
  longitude: number;
}

export interface RouteStop {
  stationCode: string;
  stationName: string;
  scheduledArrival: string;
  scheduledDeparture: string;
  haltTimeMinutes: number;
  distanceFromSource: number;
}

export interface Train {
  id: string; // The internal database ID you will use in Phase 3
  trainNumber: string; // The public Indian Railways 5-digit number
  trainName: string;
  sourceStation: string;
  destinationStation: string;
  status: TrainStatus;
  currentLocation: StationCoordinate;
  route: RouteStop[];
}
