// components/CampaignDetails.tsx
interface Creative {
  width: number;
  height: number;
  banner_url: string;
  click_url: string;
  name: string;
}

interface Campaign {
  id: number;
  name: string;
  status: string;
  advertiser_id: string;
  bid_price: number;
  budget_total: number;
  budget_spent: number;
  start_date: string;
  end_date: string;
  creatives: Creative[];
}

export default function CampaignDetails({ campaign }: { campaign: Campaign }) {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">{campaign.name}</h2>
      <div className="text-sm text-gray-600">Status: <span className="font-medium text-black">{campaign.status}</span></div>
        <div className="space-y-1 text-sm">
            <p><strong>Advertiser:</strong> {campaign.advertiser_id}</p>
            <p><strong>Bid Price:</strong> ${campaign.bid_price} CPM</p>
            <p>
                <strong>Budget:</strong>{" "}
                {campaign.budget_total != null ? `$${campaign.budget_total.toLocaleString()}` : "N/A"}
            </p>
            <p>
                <strong>Spent:</strong>{" "}
                {campaign.budget_spent != null ? `$${campaign.budget_spent.toLocaleString()}` : "N/A"}
            </p>
            <p>
                <strong>Start:</strong>{" "}
                {campaign.start_date ? new Date(campaign.start_date).toLocaleString() : "N/A"}
            </p>
            <p>
                <strong>End:</strong>{" "}
                {campaign.end_date ? new Date(campaign.end_date).toLocaleString() : "N/A"}
            </p>
        </div>

        <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">Creatives</h3>
            <div className="space-y-4">
                {campaign.creatives.map((c, i) => (
              <div key={i} className="border p-4 rounded-md bg-white shadow-sm">
                <p className="text-sm font-medium">{c.name} ({c.width}×{c.height})</p>
                <img src={c.banner_url} alt={c.name} className="mt-2 w-full max-w-xs border" />
                <p className="text-blue-500 text-sm mt-2">Click URL: <a href={c.click_url}>{c.click_url}</a></p>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
