"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    }
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-white rounded-xl shadow">Usuarios</div>
        <div className="p-4 bg-white rounded-xl shadow">Exámenes</div>
        <div className="p-4 bg-white rounded-xl shadow">Resultados</div>
      </div>
    </div>
  )
}
