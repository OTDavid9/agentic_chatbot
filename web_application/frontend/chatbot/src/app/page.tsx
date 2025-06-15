"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <main className="flex flex-col gap-8 row-start-2 items-center text-center sm:text-left sm:items-start">
        <h1 className="text-5xl font-bold max-w-xl leading-tight">
          Welcome to AI Agentic ChatBot
        </h1>

        <p className="text-lg max-w-xl text-gray-300">
          Build, chat, and collaborate with intelligent AI agents. Seamlessly interact and create smarter conversations.
        </p>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <button
            onClick={() => router.push("/signup")}
            className="rounded-full bg-blue-600 text-white px-6 py-3 text-base font-medium hover:bg-blue-700 hover:shadow-lg transition"
          >
            Get Started
          </button>

          <button
            onClick={() => router.push("/login")}
            className="rounded-full border border-gray-500 px-6 py-3 text-base font-medium hover:bg-gray-700 hover:shadow transition"
          >
            Login
          </button>
        </div>
      </main>

      <footer className="row-start-3 flex gap-8 flex-wrap items-center justify-center text-sm text-gray-400">
        <a
          className="hover:underline cursor-pointer"
          onClick={() => router.push("/signup")}
        >
          Create Account
        </a>
        <a
          className="hover:underline cursor-pointer"
          onClick={() => router.push("/login")}
        >
          Login
        </a>
      </footer>
    </div>
  );
}
