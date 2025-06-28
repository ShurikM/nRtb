// Campaigns.tsx
import { useEffect, useState } from "react";
import api from "../api";
import CampaignList from "../components/CampaignList";
import CampaignDetails from "../components/CampaignDetails";

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);

  useEffect(() => {
    api.get("/campaigns")
      .then((res) => {
        setCampaigns(res.data);
        if (res.data.length > 0) setSelectedId(res.data[0].id);
      })
      .catch((err) => console.error("Failed to load campaigns", err));
  }, []);

  const selected = campaigns.find((c: any) => c.id === selectedId);

  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
        <CampaignList
          campaigns={campaigns}
          selectedId={selectedId}
          onSelect={setSelectedId}
        />
      </aside>
      <main className="flex-1 p-6 overflow-auto">
        {selected ? (
          <CampaignDetails campaign={selected} />
        ) : (
          <p className="text-gray-500">Select a campaign to view details.</p>
        )}
      </main>
    </div>
  );
}
