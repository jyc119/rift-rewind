import Bronze from "../assets/Ranked Emblems Latest/Rank=Bronze.png";
import Silver from "../assets/Ranked Emblems Latest/Rank=Silver.png";
import Gold from "../assets/Ranked Emblems Latest/Rank=Gold.png";
import Platinum from "../assets/Ranked Emblems Latest/Rank=Platinum.png";
import Emerald from "../assets/Ranked Emblems Latest/Rank=Emerald.png";
import Diamond from "../assets/Ranked Emblems Latest/Rank=Diamond.png";
import Master from "../assets/Ranked Emblems Latest/Rank=Master.png";
import Grandmaster from "../assets/Ranked Emblems Latest/Rank=Grandmaster.png";
import Challenger from "../assets/Ranked Emblems Latest/Rank=Challenger.png";

import topIcon from "../assets/roles/Top.png";
import jgIcon from "../assets/roles/Jungle.png";
import midIcon from "../assets/roles/Middle.png";
import botIcon from "../assets/roles/Bot.png";
import supIcon from "../assets/roles/Support.png";

export const roleIconMap: Record<string, string> = {
  TOP: topIcon,
  JUNGLE: jgIcon,
  MID: midIcon,
  BOT: botIcon,
  SUPPORT: supIcon
}

export const rankIconMap: Record<string, string> = {
  BRONZE: Bronze,
  SILVER: Silver,
  GOLD: Gold,
  PLATINUM: Platinum,
  EMERALD: Emerald,
  DIAMOND: Diamond,
  MASTER: Master,
  GRANDMASTER: Grandmaster,
  CHALLENGER: Challenger,
};