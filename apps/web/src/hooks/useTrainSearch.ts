import mock_search_trains from "../data/mock_railkit_search.json";

interface Train {
  train_no: string;
  train_name: string;
}

export function filterTrains(trains: Train[], query: string): Train[] {
  // Normalize the query to support case-insensitive matching.
  const filteredQuery = query.trim().toLowerCase();
  // Return no results when the search query is empty.
  if (filteredQuery === "") {
    return [];
  }
  return trains
    .filter((train) => {
      return (
        train.train_no.trim().toLowerCase().includes(filteredQuery) ||
        train.train_name.trim().toLowerCase().includes(filteredQuery)
      );
    })
    .slice(0, 8);
}

export function useTrainSearch(query: string) {
  return filterTrains(mock_search_trains.data, query);
}
