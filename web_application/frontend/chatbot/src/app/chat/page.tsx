// "use client";

// import { useState, useEffect, useRef } from "react";
// import { useRouter } from "next/navigation";

// export default function ChatPage() {
//   const router = useRouter();
//   const fileInputRef = useRef<HTMLInputElement | null>(null);
//   const websocketRef = useRef<WebSocket | null>(null);
//   const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);

//   const [user, setUser] = useState<string>("");
//   const [message, setMessage] = useState("");
//   const [messages, setMessages] = useState<string[]>([]);

//   const [selectedFile, setSelectedFile] = useState<File | null>(null);
//   const [uploading, setUploading] = useState(false);
//   const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

//   const [sessionId, setSessionId] = useState<string>("");
//   const [isWebSocketConnected, setIsWebSocketConnected] = useState(false);
//   const [retryCount, setRetryCount] = useState(0);

//   useEffect(() => {
//     const storedUser = localStorage.getItem("user");
//     if (storedUser) {
//       setUser(storedUser);
//       const generatedSessionId = crypto.randomUUID();
//       setSessionId(generatedSessionId);
//       connectWebSocket(generatedSessionId);
//     } else {
//       router.push("/login");
//     }

//     return () => {
//       if (websocketRef.current) websocketRef.current.close();
//       if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
//     };
//   }, [router]);

//   const connectWebSocket = (sessionId: string) => {
//     console.log(`Connecting to ${process.env.NEXT_PUBLIC_WEBSOCKET_API}/${sessionId}`);
//     const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WEBSOCKET_API}/${sessionId}`);
//     websocketRef.current = ws;

//     ws.onopen = () => {
//       console.log("WebSocket connected.");
//       setIsWebSocketConnected(true);
//       setRetryCount(0);
//     };

//     ws.onmessage = (event) => {
//       const response = event.data;
//       setMessages((prev) => [...prev, `Assistant: ${response}`]);
//     };

//     ws.onclose = () => {
//       console.warn("WebSocket closed. Attempting to reconnect...");
//       setIsWebSocketConnected(false);
//       attemptReconnect(sessionId);
//     };

//     ws.onerror = () => {
//       console.error("WebSocket error occurred. Forcing connection close.");
//       ws.close(); // Triggers onclose for auto-reconnect
//     };
//   };

//   const attemptReconnect = (sessionId: string) => {
//     const delay = Math.min(5000, 1000 * 2 ** retryCount);
//     console.log(`Reconnecting in ${delay / 1000} seconds...`);

//     reconnectTimeout.current = setTimeout(() => {
//       setRetryCount((prev) => prev + 1);
//       connectWebSocket(sessionId);
//     }, delay);
//   };

//   const sendMessage = (e: React.FormEvent) => {
//     e.preventDefault();

//     if (isWebSocketConnected && websocketRef.current?.readyState === WebSocket.OPEN) {
//       const payload = { message, session_id: sessionId };

//       try {
//         websocketRef.current.send(JSON.stringify(payload));
//         setMessages((prev) => [...prev, `You: ${message}`]);
//         setMessage("");
//       } catch (error) {
//         console.error("Failed to send message over WebSocket.", error);
//         alert("WebSocket is disconnected. Please wait for reconnection.");
//       }
//     } else {
//       alert("WebSocket is not connected yet. Please wait...");
//     }
//   };

//   const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     if (e.target.files && e.target.files.length > 0) {
//       setSelectedFile(e.target.files[0]);
//     }
//   };

//   const triggerFilePicker = () => {
//     fileInputRef.current?.click();
//   };

//   const uploadFile = async () => {
//     if (!selectedFile) return;

//     setUploading(true);

//     try {
//       const formData = new FormData();
//       formData.append("file", selectedFile);

//       const response = await fetch(`${process.env.NEXT_PUBLIC_UPLOAD_API}/upload_and_index`, {
//         method: "POST",
//         body: formData,
//       });

//       if (!response.ok) {
//         console.error("Upload failed with status:", response.status);
//         alert("File upload failed. Please try again.");
//         return;
//       }

//       const data = await response.json();
//       const filePath = data.file_path;
//       const fileName = filePath.split("\\").pop() || "Unknown File";

//       setUploadedFiles((prev) => [...prev, fileName]);
//       alert("File uploaded successfully.");
//       resetFileSelection();
//     } catch (error) {
//       console.error("Upload error:", error);
//       alert("An error occurred during file upload. Please check your network.");
//     } finally {
//       setUploading(false);
//     }
//   };

//   const resetFileSelection = () => {
//     if (fileInputRef.current) {
//       fileInputRef.current.value = "";
//     }
//     setSelectedFile(null);
//   };

//   return (
//     <div className="flex min-h-screen bg-gray-100 text-gray-900">
//       {/* Sidebar */}
//       <aside className="w-72 bg-gray-800 text-white p-6 flex flex-col gap-6">
//         <h2 className="text-2xl font-bold mb-4">File Upload</h2>

//         {/* File Picker */}
//         <div className="flex flex-col gap-3">
//           <input
//             type="file"
//             ref={fileInputRef}
//             onChange={handleFileChange}
//             className="hidden"
//           />
//           <button
//             onClick={triggerFilePicker}
//             className="w-full py-2 rounded bg-gray-700 hover:bg-gray-600 transition"
//           >
//             {selectedFile ? "Change File" : "Pick a File"}
//           </button>

//           {selectedFile && (
//             <p className="text-sm text-gray-300 truncate">{selectedFile.name}</p>
//           )}

//           <button
//             onClick={uploadFile}
//             disabled={!selectedFile || uploading}
//             className={`w-full py-2 rounded font-medium ${uploading ? "bg-gray-600 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"} transition`}
//           >
//             {uploading ? "Uploading..." : "Upload File"}
//           </button>
//         </div>

//         {/* Uploaded Files */}
//         <div className="mt-8">
//           <h3 className="text-lg font-semibold mb-2">Uploaded Files</h3>
//           <div className="max-h-48 overflow-y-auto space-y-1 text-sm">
//             {uploadedFiles.length > 0 ? (
//               uploadedFiles.map((file, idx) => (
//                 <div key={idx} className="truncate text-gray-300">
//                   {file}
//                 </div>
//               ))
//             ) : (
//               <p className="text-gray-400 text-sm">No files uploaded yet.</p>
//             )}
//           </div>
//         </div>
//       </aside>

//       {/* Chat Area */}
//       <main className="flex flex-col items-center justify-center flex-1 p-8 sm:p-20">
//         <h1 className="text-4xl font-bold mb-8">Welcome, {user}!</h1>

//         <div className="w-full max-w-2xl bg-white border border-gray-300 p-4 rounded-lg mb-4 overflow-y-auto max-h-[400px]">
//           {messages.map((msg, idx) => {
//             const isUserMessage = msg.startsWith("You:");

//             return (
//               <div
//                 key={idx}
//                 className={`mb-2 flex ${isUserMessage ? "justify-end" : "justify-start"}`}
//               >
//                 <div
//                   className={`max-w-[70%] p-3 rounded-lg ${
//                     isUserMessage
//                       ? "bg-blue-500 text-white self-end"
//                       : "bg-gray-200 text-gray-900 self-start"
//                   }`}
//                 >
//                   {isUserMessage ? msg.replace("You: ", "") : msg.replace("Assistant: ", "")}
//                 </div>
//               </div>
//             );
//           })}
//         </div>

//         <form onSubmit={sendMessage} className="flex gap-4 w-full max-w-2xl">
//           <input
//             type="text"
//             placeholder="Type your message..."
//             value={message}
//             onChange={(e) => setMessage(e.target.value)}
//             className="flex-1 p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
//             required
//           />
//           <button
//             type="submit"
//             className="bg-blue-600 hover:bg-blue-700 py-3 px-6 rounded font-medium text-white"
//           >
//             Send
//           </button>
//         </form>

//         {/* WebSocket Status */}
//         <div className="mt-4 text-sm">
//           WebSocket Status:{" "}
//           <span className={isWebSocketConnected ? "text-green-600" : "text-red-600"}>
//             {isWebSocketConnected ? "Connected" : "Disconnected"}
//           </span>
//         </div>
//       </main>
//     </div>
//   );
// }
"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";

export default function ChatPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const websocketRef = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);

  const [user, setUser] = useState<string>("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false); // New loading state

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

  const [sessionId, setSessionId] = useState<string>("");
  const [isWebSocketConnected, setIsWebSocketConnected] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(storedUser);
      const generatedSessionId = crypto.randomUUID();
      setSessionId(generatedSessionId);
      connectWebSocket(generatedSessionId);
    } else {
      router.push("/login");
    }

    return () => {
      if (websocketRef.current) websocketRef.current.close();
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
    };
  }, [router]);

  const connectWebSocket = (sessionId: string) => {
    console.log(`Connecting to ${process.env.NEXT_PUBLIC_WEBSOCKET_API}/${sessionId}`);
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WEBSOCKET_API}/${sessionId}`);
    websocketRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected.");
      setIsWebSocketConnected(true);
      setRetryCount(0);
    };

    ws.onmessage = (event) => {
      const response = event.data;
      setMessages((prev) => [...prev, `Assistant: ${response}`]);
      setIsLoading(false); // Response received, stop loading
    };

    ws.onclose = () => {
      console.warn("WebSocket closed. Attempting to reconnect...");
      setIsWebSocketConnected(false);
      attemptReconnect(sessionId);
    };

    ws.onerror = () => {
      console.error("WebSocket error occurred. Forcing connection close.");
      ws.close(); // Triggers onclose for auto-reconnect
    };
  };

  const attemptReconnect = (sessionId: string) => {
    const delay = Math.min(5000, 1000 * 2 ** retryCount);
    console.log(`Reconnecting in ${delay / 1000} seconds...`);

    reconnectTimeout.current = setTimeout(() => {
      setRetryCount((prev) => prev + 1);
      connectWebSocket(sessionId);
    }, delay);
  };

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();

    if (isWebSocketConnected && websocketRef.current?.readyState === WebSocket.OPEN) {
      const payload = { message, session_id: sessionId };

      try {
        websocketRef.current.send(JSON.stringify(payload));
        setMessages((prev) => [...prev, `You: ${message}`]);
        setMessage("");
        setIsLoading(true); // Start loading when message is sent
      } catch (error) {
        console.error("Failed to send message over WebSocket.", error);
        alert("WebSocket is disconnected. Please wait for reconnection.");
      }
    } else {
      alert("WebSocket is not connected yet. Please wait...");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const triggerFilePicker = () => {
    fileInputRef.current?.click();
  };

  const uploadFile = async () => {
    if (!selectedFile) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${process.env.NEXT_PUBLIC_UPLOAD_API}/upload_and_index`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        console.error("Upload failed with status:", response.status);
        alert("File upload failed. Please try again.");
        return;
      }

      const data = await response.json();
      const filePath = data.file_path;
      const fileName = filePath.split("\\").pop() || "Unknown File";

      setUploadedFiles((prev) => [...prev, fileName]);
      alert("File uploaded successfully.");
      resetFileSelection();
    } catch (error) {
      console.error("Upload error:", error);
      alert("An error occurred during file upload. Please check your network.");
    } finally {
      setUploading(false);
    }
  };

  const resetFileSelection = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    setSelectedFile(null);
  };

  return (
    <div className="flex min-h-screen bg-gray-100 text-gray-900">
      {/* Sidebar */}
      <aside className="w-72 bg-gray-800 text-white p-6 flex flex-col gap-6">
        <h2 className="text-2xl font-bold mb-4">File Upload</h2>

        {/* File Picker */}
        <div className="flex flex-col gap-3">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
          />
          <button
            onClick={triggerFilePicker}
            className="w-full py-2 rounded bg-gray-700 hover:bg-gray-600 transition"
          >
            {selectedFile ? "Change File" : "Pick a File"}
          </button>

          {selectedFile && (
            <p className="text-sm text-gray-300 truncate">{selectedFile.name}</p>
          )}

          <button
            onClick={uploadFile}
            disabled={!selectedFile || uploading}
            className={`w-full py-2 rounded font-medium ${uploading ? "bg-gray-600 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"} transition`}
          >
            {uploading ? "Uploading..." : "Upload File"}
          </button>
        </div>

        {/* Uploaded Files */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-2">Uploaded Files</h3>
          <div className="max-h-48 overflow-y-auto space-y-1 text-sm">
            {uploadedFiles.length > 0 ? (
              uploadedFiles.map((file, idx) => (
                <div key={idx} className="truncate text-gray-300">
                  {file}
                </div>
              ))
            ) : (
              <p className="text-gray-400 text-sm">No files uploaded yet.</p>
            )}
          </div>
        </div>
      </aside>

      {/* Chat Area */}
      <main className="flex flex-col items-center justify-center flex-1 p-8 sm:p-20">
        <h1 className="text-4xl font-bold mb-8">Welcome, {user}!</h1>

        <div className="w-full max-w-2xl bg-white border border-gray-300 p-4 rounded-lg mb-4 overflow-y-auto max-h-[400px]">
          {messages.map((msg, idx) => {
            const isUserMessage = msg.startsWith("You:");

            return (
              <div
                key={idx}
                className={`mb-2 flex ${isUserMessage ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[70%] p-3 rounded-lg ${
                    isUserMessage
                      ? "bg-blue-500 text-white self-end"
                      : "bg-gray-200 text-gray-900 self-start"
                  }`}
                >
                  {isUserMessage ? msg.replace("You: ", "") : msg.replace("Assistant: ", "")}
                </div>
              </div>
            );
          })}

          {isLoading && (
            <div className="mb-2 flex justify-start">
              <div className="max-w-[70%] p-3 rounded-lg bg-gray-200 text-gray-900 self-start italic">
                Assistant is typing...
              </div>
            </div>
          )}
        </div>

        <form onSubmit={sendMessage} className="flex gap-4 w-full max-w-2xl">
          <input
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-1 p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 py-3 px-6 rounded font-medium text-white"
            disabled={isLoading}
          >
            Send
          </button>
        </form>

        {/* WebSocket Status */}
        <div className="mt-4 text-sm">
          WebSocket Status:{" "}
          <span className={isWebSocketConnected ? "text-green-600" : "text-red-600"}>
            {isWebSocketConnected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </main>
    </div>
  );
}
