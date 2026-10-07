"use client";
import "mapbox-gl/dist/mapbox-gl.css";
import { useState } from "react";
import Map from "react-map-gl/mapbox";

function RailwayMap() {
  const [camera] = useState({
    longitude: 78.9629,
    latitude: 20.5937,
    zoom: 4,
  });
  return <div className="h-screen w-screen">
    <Map
    mapboxAccessToken={process.env.NEXT_PUBLIC_MAPBOX_TOKEN}
    initialViewState={camera}
    mapStyle="mapbox://styles/mapbox/streets-v9"
    />
  </div>;
}
export default RailwayMap;
