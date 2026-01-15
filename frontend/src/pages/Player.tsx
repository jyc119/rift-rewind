import React, { useEffect, useState } from "react";
import { useLocation, useParams, Navigate } from "react-router-dom";

import mapBg from "../assets/map-bg.jpg";
import { roleIconMap } from "../utils/rankRoleIcon";
import { rankIconMap } from "../utils/rankRoleIcon";


import { getOverview, type OverviewResponse } from "../utils/api";

type PlayerNavState = {
  puuid: string;
}

const Player: React.FC = () => {
  const [hoveredRole, setHoveredRole] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<OverviewResponse | null>(null)

  // Split "Monster-NA1" into "Monster" and "NA1"
  const { region, id } = useParams<{ region: string; id: string }>();
  const [summonerName, tag] = id ? id.split("-") : ["Unknown", ""];
  const {state} = useLocation() as {state: PlayerNavState | null};

  if (!state?.puuid){
    return <Navigate to="/" replace />
  }

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        setError(null);

        const rankData = await getOverview(summonerName, tag, region, state.puuid);

        setData(rankData); // ✅ types now match
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load player data");
      }
    };

    // ✅ actually call it
    fetchOverview();

    return () => {};
  }, [summonerName, tag]);

  const roleInfo: Record<string, string> = {
    top: "Top Lane — Durable champions who thrive in 1v1s and split-pushing.",
    jungle: "Jungle — Controls the map, objectives, and ganks lanes.",
    mid: "Mid Lane — Burst mages and assassins, central influence.",
    adc: "Bot Carry — High DPS ranged carry focused on farming.",
    support: "Support — Protects and enables the team with vision and utility.",
  };

  const tier = data?.rank?.tier;          // e.g. "PLATINUM"
  const division = data?.rank?.rank;      // e.g. "I"
  const lp = data?.rank?.lp;              // e.g. 85

  const icon = tier ? rankIconMap[tier] : undefined;

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-900 text-white">
      {/* --- Top Section: Player Info --- */}
      <div className="w-full max-w-3xl mt-10 mb-6 text-center">
        <h1 className="text-3xl font-bold">{summonerName} #{tag}</h1>
        <img
          src={icon}
          alt="Rank"
          className="mx-auto w-24 h-24 mt-4"
        />
        <p className="text-gray-400 mt-2">Platinum I • 85 LP</p>
      </div>

      {/* --- Bottom Section: Champ Select Map --- */}
      <div className="relative w-full max-w-5xl">
        <img
          src={mapBg}
          alt="Champion Select"
          className="w-full rounded-lg shadow-lg scale-90"
        />

        {/* Role icons positioned manually (can later adjust absolute positions) */}
        <div className="absolute top-[25%] left-[25%]">
          <img
            src={roleIconMap["TOP"]}
            alt="Top"
            className="w-12 h-12 cursor-pointer transition-transform hover:scale-110"
            onMouseEnter={() => setHoveredRole("top")}
            onMouseLeave={() => setHoveredRole(null)}
          />
        </div>

        <div className="absolute top-[40%] left-[30%]">
          <img
            src={roleIconMap["JUNGLE"]}
            alt="Jungle"
            className="w-12 h-12 cursor-pointer transition-transform hover:scale-110"
            onMouseEnter={() => setHoveredRole("jungle")}
            onMouseLeave={() => setHoveredRole(null)}
          />
        </div>

        <div className="absolute top-[50%] left-[45%]">
          <img
            src={roleIconMap["MID"]}
            alt="Mid"
            className="w-12 h-12 cursor-pointer transition-transform hover:scale-110"
            onMouseEnter={() => setHoveredRole("mid")}
            onMouseLeave={() => setHoveredRole(null)}
          />
        </div>

        <div className="absolute bottom-[20%] left-[75%]">
          <img
            src={roleIconMap["BOT"]}
            alt="ADC"
            className="w-12 h-12 cursor-pointer transition-transform hover:scale-110"
            onMouseEnter={() => setHoveredRole("adc")}
            onMouseLeave={() => setHoveredRole(null)}
          />
        </div>

        <div className="absolute bottom-[20%] left-[80%]">
          <img
            src={roleIconMap["SUPPORT"]}
            alt="Support"
            className="w-12 h-12 cursor-pointer transition-transform hover:scale-110"
            onMouseEnter={() => setHoveredRole("support")}
            onMouseLeave={() => setHoveredRole(null)}
          />
        </div>

        {/* Tooltip on hover */}
        {hoveredRole && (
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800/90 px-4 py-2 rounded-lg shadow-lg text-sm">
            {roleInfo[hoveredRole]}
          </div>
        )}
      </div>
    </div>
  );
};

export default Player;
