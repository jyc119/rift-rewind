export type Rank =
  | {
      queue: string;
      tier: string;
      rank: string;
      lp?: number;
      wins?: number;
      losses?: number;
    }
  | null;

export type OverviewResponse = {
  valid: boolean;
  rank: Rank;
  message?: string | null;
};

export async function validatePlayer(gameName: string, tagLine: string, region: string) {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/validate-player`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": import.meta.env.VITE_API_KEY as string,
    },
    body: JSON.stringify({ gameName, tagLine, region }),
  });

  const data: any = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.message || `Request failed (${res.status})`);
  }

  return data as { puuid?: string; gameName?: string; tagLine?: string; region?: string; [k: string]: any };
}

export async function getOverview(gameName: string, tagLine: string, region:string | undefined, puuid: string): Promise<OverviewResponse> {
  const res = await fetch(`${import.meta.env.VITE_API_OVERVIEW}/overview`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": import.meta.env.VITE_API_KEY as string,
    },
    body: JSON.stringify({ gameName, tagLine, region, puuid}),
  });

  const data: OverviewResponse = await res.json().catch(() => ({} as any));

  if (!res.ok) {
    throw new Error(data.message || `Request failed (${res.status})`);
  }

  return data; // ✅ includes rank + message + flags
}