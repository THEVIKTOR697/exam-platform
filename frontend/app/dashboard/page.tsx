"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
    const router = useRouter();

    const [results, setResults] = useState<any[]>([]);
    const [exams, setExams] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState<any>(null);

    const [activeSection, setActiveSection] = useState("results");

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            console.log("TOKEN:", token);

            if (!token) {
                router.push("/login");
                return;
            }

            try {
                const [resultsResponse, examsResponse] = await Promise.all([
                    fetch(`${process.env.NEXT_PUBLIC_API_URL}/results/`, {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                    fetch(`${process.env.NEXT_PUBLIC_API_URL}/exams/`),
                ]);

                if (!resultsResponse.ok) {
                    console.error("Error auth:", resultsResponse.status);

                    if (resultsResponse.status === 401) {
                        localStorage.removeItem("token");
                        router.push("/login");
                        return;
                    }
                }

                const [userResponse] = await Promise.all([
                    fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me/`, {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    })
                ])
                const userData = await userResponse.json();
                const resultsData = await resultsResponse.json();
                const examsData = await examsResponse.json();
                const normalizedExams = examsData.map((e: any) => ({
                    id: e.id ?? e.exam_id,
                    title: e.title,
                    price: e.price,
                }));
                console.log("userData:", userData);
                console.log("resultsData:", resultsData);
                console.log("examsData:", examsData);
                console.log("NORMALIZED:", normalizedExams);
                setUser(userData);
                setResults(resultsData.results);
                setExams(normalizedExams);

            } catch (err) {
                console.error("Error cargando datos", err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [router]);

    if (loading) return <p className="p-6">Cargando...</p>;

    return (
        <div className="flex">
            {/* 🔥 SIDEBAR */}
            <aside className="fixed left-0 top-0 h-screen w-64 bg-black text-white p-6">
                <h2 className="text-xl font-bold mb-6">Menú</h2>

                <nav className="space-y-4">
                    <button
                        onClick={() => setActiveSection("profile")}
                        className="block w-full text-left hover:text-gray-300"
                    >
                        Mi perfil
                    </button>
                    <button
                        onClick={() => setActiveSection("report_card")}
                        className="block w-full text-left hover:text-gray-300"
                    >
                        Mis calificaciones
                    </button>
                    <button
                        onClick={() => setActiveSection("schedule")}
                        className="block w-full text-left hover:text-gray-300"
                    >
                        Mi horario
                    </button>
                    <button
                        onClick={() => setActiveSection("results")}
                        className="block w-full text-left hover:text-gray-300"
                    >
                        Mis resultados
                    </button>

                    <button
                        onClick={() => setActiveSection("available_certifications")}
                        className="block w-full text-left hover:text-gray-300"
                    >
                        Tienda
                    </button>
                </nav>
            </aside>

            {/* 📄 CONTENIDO */}
            <main className="ml-64 p-6 w-full space-y-8">
                {/*<h1 className="text-3xl font-bold">KK</h1>*/}

                {/* PROFILE */}
                {activeSection === "profile" && (
                    <div>
                        <h2 className="text-xl font-bold">Mi perfil</h2>
                        <p className="mt-2 text-gray-600">
                            Consultar y modificar mis datos personales
                        </p>
                        <p>{user?.id}</p>
                        <p>{user?.name}</p>
                        <p>{user?.email}</p>
                    </div>
                )}
                {/* SCHEDULE */}
                {activeSection === "schedule" && (
                    <div>
                        <h2 className="text-xl font-bold">Horario escolar</h2>
                        <p className="mt-2 text-gray-600">
                            (Aquí puedes renderizar tu horario después)
                        </p>
                    </div>
                )}
                {/* REPORT CARD */}
                {activeSection === "report_card" && (
                    <div>
                        <h2 className="text-xl font-bold">Mi perfil</h2>
                        <p className="mt-2 text-gray-600">
                            Consultar calificaciones
                        </p>
                    </div>
                )}
                {/* MY RESULTS */}
                {activeSection === "results" && (
                    <div>
                        <h2 className="text-xl font-bold mb-4">Certificaciones</h2>

                        {results.length === 0 ? (
                            <p>No tienes resultados aún</p>
                        ) : (
                            results.map((r, i) => (
                                <div key={i} className="border p-3 mb-2 rounded">
                                    <p className="font-semibold">{r.title}</p>
                                    <p>Score: {r.score}%</p>
                                    <p>
                                        Resultado: {r.passed ? "Aprobado ✅" : "Reprobado ❌"}
                                    </p>
                                    <p>Fecha: {r.created_at}</p>
                                </div>
                            ))
                        )}
                    </div>
                )}

                {/* CERTIFICATIONS SHOP */}
                {activeSection === "available_certifications" && (
                    <div>
                        <h2 className="text-2xl font-bold mb-4">
                            Certificaciones disponibles
                        </h2>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {exams.map((exam) => (
                                <div key={exam.id} className="border p-4 rounded-lg">
                                    <h3 className="font-semibold">{exam.title}</h3>
                                    <p>${exam.price}</p>

                                    <button
                                        onClick={() => router.push(`/checkout/${exam.id}`)}
                                        className="mt-2 bg-black text-white px-4 py-2 rounded"
                                    >
                                        Comprar
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}