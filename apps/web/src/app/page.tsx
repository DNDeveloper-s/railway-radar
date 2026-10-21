"use client";
import RailwayMap from "@/components/Map/RailwayMap";
import TrainSearchBar from "@/components/Search/TrainSearchBar";

export default function HomePage() {
  const handleSelectTrain = (train_no: string) => {
    console.log("Train Number is : ", train_no);
  };
  return (
    <main className="relative h-screen w-screen overflow-hidden  bg-zinc-950">
      {/* Placeholder for Suraj's RailwayMap component */}
      <RailwayMap />

      <TrainSearchBar onSelectTrain={handleSelectTrain} />

      {/* Future UI elements (Search Bar, Sidebar) will sit here with absolute positioning */}
    </main>
  );
}
