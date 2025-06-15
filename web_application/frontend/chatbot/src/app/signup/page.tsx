"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const router = useRouter();
  const [full_name, setFull_name] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ full_name, email, password }),
    });

    if (response.ok) {
      router.push("/login");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center flex-1 p-8 sm:p-20">
      <h1 className="text-4xl font-bold mb-8">Create your account</h1>
      <form onSubmit={handleSignup} className="flex flex-col gap-4 w-full max-w-md">
        <input
          type="text"
          placeholder="Full Name"
          value={full_name}
          onChange={(e) => setFull_name(e.target.value)}
          className="p-3 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="p-3 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="p-3 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <button type="submit" className="bg-blue-600 hover:bg-blue-700 py-3 rounded font-medium">
          Sign Up
        </button>
      </form>
    </div>
  );
}
