import mock_search_trains from "../data/mock_railkit_search.json";

interface Train {
  train_no: string;
  train_name: string;
}

export function filterTrains(trains: Train[], query: string) {
  // filtering logic
  const filteredQuery = query.trim().toLowerCase();

  if (filteredQuery === "") {
    return [];
  }
  const searchedTrains = trains
    .filter((train) => {
      return (
        train.train_no.trim().toLowerCase().includes(filteredQuery) ||
        train.train_name.trim().toLowerCase().includes(filteredQuery)
      );
    })
    .slice(0, 8);
  return searchedTrains;
}

export function useTrainSearch(query: string) {
  //hook logic
  const result = filterTrains(mock_search_trains.data, query);
  return result;
}
