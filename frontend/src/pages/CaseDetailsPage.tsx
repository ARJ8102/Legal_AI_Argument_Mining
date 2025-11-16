import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

const CaseDetailsPage = () => {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/cases/${id}`).then((res) => {
      setData(res.data.case);
    });
  }, [id]);

  if (!data) return <p>Loading...</p>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">{data.filename}</h1>

      {/* Entities */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Named Entities</h2>
        <div className="bg-gray-800 p-4 rounded-lg">
          {data.entities.map((e: any, i: number) => (
            <p key={i}>
              <span className="text-green-400">{e.entity_group}</span>: {e.word}
            </p>
          ))}
        </div>
      </div>

      {/* Argument Mining */}
      <div>
        <h2 className="text-xl font-semibold mb-2">Argument Classification</h2>
        <div className="bg-gray-800 p-4 rounded-lg">
          {data.classifications.map((c: any, i: number) => (
            <div key={i} className="mb-3">
              <p className="font-semibold">{c.sentence}</p>
              <p className="text-blue-300">→ {c.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CaseDetailsPage;
