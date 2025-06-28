// components/CampaignList.tsx
interface Campaign {
  id: number;
  name: string;
  status: string;
}

interface Props {
  campaigns: Campaign[];
  selectedId: number | null;
  onSelect: (id: number) => void;
}

export default function CampaignList({ campaigns, selectedId, onSelect }: Props) {
  return (
    <ul className="divide-y divide-gray-200">
      {campaigns.map((c) => (
        <li
          key={c.id}
          onClick={() => onSelect(c.id)}
          className={`cursor-pointer px-4 py-3 hover:bg-gray-100 ${
            selectedId === c.id ? "bg-gray-100 font-semibold" : ""
          }`}
        >
          <div className="text-sm">{c.name}</div>
          <div className="text-xs text-gray-500">{c.status}</div>
        </li>
      ))}
    </ul>
  );
}
