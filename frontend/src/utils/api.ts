export async function validatePlayer(gameName: string, tagLine: string) {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/validate-player`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": import.meta.env.VITE_API_KEY as string,
    },
    body: JSON.stringify({ gameName, tagLine }),
  });

  const data: any = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.message || `Request failed (${res.status})`);
  }

  return data as { puuid?: string; gameName?: string; tagLine?: string; [k: string]: any };
}
