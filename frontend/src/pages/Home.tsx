import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import mapBg from "../assets/homepage.webp";

const Home = () => {
  const [summonerName, setSummonerName] = useState("");
  const [tag, setTag] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (summonerName && tag) {
      navigate(`/player/${summonerName}-${tag}`);
    }
  };

  return (
    <div className="relative flex items-center justify-center min-h-screen bg-black overflow-hidden">
      {/* Background */}
      <img
        src={mapBg}
        alt="League map"
        className="absolute inset-0 w-full h-full object-cover blur-sm brightness-50"
      />

      {/* Foreground content */}
      <div className="relative z-10 text-center">
        <h1 className="text-4xl font-bold text-white mb-8">Enter Summoner Name!</h1>

        <form
          onSubmit={handleSubmit}
          className="flex items-center justify-center gap-3"
        >
        <input
            type="text"
            placeholder="Summoner Name"
            value={summonerName}
            onChange={(e) => setSummonerName(e.target.value)}
            className="px-6 py-3 w-72 bg-gray-900/80 border border-gray-600 text-white text-lg rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />

        <input
            type="text"
            placeholder="Tag"
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            className="px-6 py-3 w-48 bg-gray-900/80 border border-gray-600 text-white text-lg rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition"
          >
            Search
          </button>
        </form>
      </div>
    </div>
  );
};

export default Home;
