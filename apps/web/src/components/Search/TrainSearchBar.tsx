"use client";

import useDebounce from "@/hooks/useDebounce";
import { useState } from "react";

const TrainSearchBar = () => {
  const [search, setSearch] = useState("");

  const [selectIndex, setSelectIndex] = useState(-1);

  const trainData = [];

  const keyDown = (e) => {
    if (trainData.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();

      const nextIndex =
        selectIndex < trainData.length - 1 ? selectIndex + 1 : 0;

      setSelectIndex(nextIndex);
      setSearch(
        `${trainData[nextIndex].train_name} - ${trainData[nextIndex].train_no}`,
      );
    } else if (e.key === "ArrowUp") {
      e.preventDefault();

      const nextIndex =
        selectIndex > 0 ? selectIndex - 1 : trainData.length - 1;

      setSelectIndex(nextIndex);
      setSearch(
        `${trainData[nextIndex].train_name} - ${trainData[nextIndex].train_no}`,
      );
    } else if (e.key === "Enter" && selectIndex !== -1) {
      setSearch(
        `${trainData[selectIndex].train_name} - ${trainData[selectIndex].train_no}`,
      );
      setSelectIndex(-1);
    }
  };

  const debouncedvalue = useDebounce(search, 300);

  return (
    <div
      className={`absolute top-4 left-4 right-4 z-50 md:left-1/2 md:right-auto md:w-[480px] md:-translate-x-1/2`}
    >
      <input
        className={`${debouncedvalue ? "rounded-t-xl " : " rounded-xl"}  border-2 w-xl  text-sm font-medium  tracking-normal text-zinc-100 z-40   shadow-lg shadow-black/40 font-sans bg-zinc-900 p-3  border-black rounded-t-xl outline-none `}
        type="text"
        placeholder="Search..."
        value={search}
        onChange={(e) => {
          const value = e.target.value;

          setSearch(value);

          if (value === "") {
            setSelectIndex(-1);
          }
        }}
        onKeyDown={keyDown}
      />

      <div
        className={`${debouncedvalue ? "visible " : "hidden "}absolute top-11      justify-start w-xl rounded-b-xl bg-zinc-900 text-sm font-medium  tracking-normal  shadow-2xl shadow-black/60 overflow-hidden z-50  "`}
      >
        {trainData.length > 0 ? (
          // If trains available, show this
          trainData.map((train, index) => (
            <p
              key={train.train_no}
              className={`${selectIndex === index ? "bg-zinc-600 text-white" : "text-white"} hover:bg-zinc-600 cursor-pointer mt-1 px-3 py-2 rounded-xl text-base`}
              onClick={() =>
                setSearch(`${train.train_name} - ${train.train_no}`)
              }
            >
              {train.train_name} - {train.train_no}
            </p>
          ))
        ) : (
          // If no trains found, show this...
          <div
            className="rounded-b-xl border border-zinc-600
               bg-zinc-900 px-5 py-8 text-center
               shadow-xl shadow-black/30"
          >
            <p className="text-base font-semibold text-zinc-100">
              No results founds
            </p>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              We couldn't find any trains matching your search.
            </p>

            <p className="mt-1 text-xs text-zinc-500">
              Try another train name or train number.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrainSearchBar;
