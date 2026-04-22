"use client";

import { useState } from "react";
import { FolderSearch, Terminal, FileCode2, Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [path, setPath] = useState(".");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");

  const handleScan = async () => {
    setLoading(true);
    setResult("");
    
    try {
      // Calls our Python FastAPI backend
      const res = await fetch("http://localhost:8080/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path }),
      });
      
      const data = await res.json();
      setResult(data.analysis);
    } catch (error) {
      setResult("Error connecting to the Archaeologist backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200 p-8 font-sans">
      <header className="mb-8 border-b border-neutral-800 pb-6 flex items-center gap-3">
        <FolderSearch className="w-8 h-8 text-blue-500" />
        <h1 className="text-3xl font-bold text-white">Project Archaeologist</h1>
        <span className="ml-auto bg-blue-500/10 text-blue-400 text-xs px-3 py-1 rounded-full border border-blue-500/20">
          Powered by Claude Opus 4.7
        </span>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT PANEL: Controls */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 h-fit shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Terminal className="w-5 h-5 text-neutral-400" /> Target Directory
          </h2>
          <div className="flex flex-col gap-4">
            <input
              type="text"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              placeholder="e.g., /home/user/my-project"
              className="w-full bg-neutral-950 border border-neutral-700 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-blue-500 transition-colors"
            />
            <button
              onClick={handleScan}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <FolderSearch className="w-5 h-5" />}
              {loading ? "Excavating Directory..." : "Initiate Scan"}
            </button>
          </div>
        </div>

        {/* RIGHT PANEL: Results */}
        <div className="lg:col-span-2 bg-neutral-900 border border-neutral-800 rounded-xl p-6 shadow-lg min-h-[500px]">
          <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2 pb-4 border-b border-neutral-800">
            <FileCode2 className="w-5 h-5 text-neutral-400" /> Analysis Report
          </h2>
          
          <div className="prose prose-invert prose-blue max-w-none">
            {loading ? (
              <div className="flex flex-col items-center justify-center h-64 text-neutral-500 space-y-4">
                <Loader2 className="w-10 h-10 animate-spin text-blue-500" />
                <p>Claude is analyzing the project structure...</p>
              </div>
            ) : result ? (
              <ReactMarkdown>{result}</ReactMarkdown>
            ) : (
              <div className="flex items-center justify-center h-64 text-neutral-600 italic">
                Awaiting target directory to begin analysis.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}