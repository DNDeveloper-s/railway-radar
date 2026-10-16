import { useEffect, useState } from "react";

export default function useDebounce(value, delay) {
  const [debouncedVal, setDebounceVal] = useState();

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebounceVal(value);
    }, delay);
    return () => {
      clearTimeout(timer);
    };
  }, [value]);
  return debouncedVal;
}
