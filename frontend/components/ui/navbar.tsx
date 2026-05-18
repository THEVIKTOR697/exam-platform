"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Navbar() {
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        const t = localStorage.getItem("token");
        setToken(t);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("token");
        window.location.href = "/";
    };

    return (
        <nav className="flex items-center justify-between px-8 py-4 bg-white shadow">
            <h1 className="text-xl font-bold text-gray-800">
                Exam Platform
            </h1>

            <div className="flex gap-4">
                {token ? (
                    <>
                        <Link
                            href="/dashboard"
                            className="border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-100 transition"
                        >
                            Dashboard
                        </Link>

                        <button
                            onClick={handleLogout}
                            className="bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 transition"
                        >
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link
                            href="/login"
                            className="border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-100 transition"
                        >
                            Iniciar sesión
                        </Link>

                        <Link
                            href="/register"
                            className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition"
                        >
                            Registrarse
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
}

// "use client";
//
// import { useRouter } from "next/navigation";
//
// export default function Navbar() {
//     const router = useRouter();
//
//     const token = typeof window !== "undefined"
//       ? localStorage.getItem("token")
//       : null;
//
//     const handleLogout = () => {
//         localStorage.removeItem("token");
//         router.push("/login");
//     };
//
//     return (
//         <nav className="bg-black text-white px-6 py-4 flex justify-between items-center">
//             <h1
//                 className="font-bold text-lg cursor-pointer"
//                 onClick={() => router.push("/dashboard")}
//             >
//                 Exam Platform
//             </h1>
//
//             <div className="space-x-4">
//                 <button onClick={() => router.push("/dashboard")}>
//                     Dashboard
//                 </button>
//
//                 <button
//                     onClick={handleLogout}
//                     className="bg-red-500 px-3 py-1 rounded"
//                 >
//                     Logout
//                 </button>
//             </div>
//         </nav>
//     );
// }
