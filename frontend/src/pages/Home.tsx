import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { validatePlayer } from "../utils/api";
import mapBg from "../assets/homepage.webp";

const Home = () => {
  const [summonerName, setSummonerName] = useState("");
  const [tag, setTag] = useState("");
  const [region, setRegion] = useState("")

  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setError(null);

    const gameName = summonerName.trim();
    const tagLine = tag.trim();

    if (!gameName || !tagLine) {
      setError("Please enter both Summoner Name and Tag.");
      return;
    }

    try {
      setIsSubmitting(true);

      // ✅ call AWS API to validate
      const data = await validatePlayer(gameName, tagLine);

      // (optional) if backend returns canonical casing, use it:
      const finalGameName = (data.gameName ?? gameName).trim();
      const finalTagLine = (data.tagLine ?? tagLine).trim();

      // ✅ navigate only on success
      navigate(
        `/player/${encodeURIComponent(finalGameName)}-${encodeURIComponent(finalTagLine)}`
      );
    } catch (err) {
      // ❌ show error line under form
      const msg =
        err instanceof Error ? err.message : "Validation failed. Please try again.";
      setError(msg);
    } finally {
      setIsSubmitting(false);
      }
  }

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
            disabled={isSubmitting}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition"
          >
            {isSubmitting ? "Checking..." : "Search"}
          </button>

          {error && (
            <p className="text-sm text-red-400">
              {error}
            </p>
          )}
        </form>
      </div>
    </div>
  );
};

export default Home;
