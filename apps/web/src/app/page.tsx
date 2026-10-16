import RailwayMap from "@/components/Map/RailwayMap";
import TrainSearchBar from "@/components/Search/TrainSearchBar";

export default function HomePage() {
  return (
    <main className="relative h-screen w-screen overflow-hidden  bg-zinc-950">
      {/* Placeholder for Suraj's RailwayMap component */}
      <RailwayMap />

      <TrainSearchBar />

      {/* Future UI elements (Search Bar, Sidebar) will sit here with absolute positioning */}
    </main>
  );
}
