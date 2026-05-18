"use client";

import {useEffect, useState} from "react";
import {useRouter} from "next/navigation";

export default function Dashboard() {
    const router = useRouter();

    const [results, setResults] = useState<any[]>([]);
    const [exams, setExams] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            console.log("TOKEN:", token);

            if (!token) {
                router.push("/login");
                return;
            }

            try {
                const [resultsRes, examsRes] = await Promise.all([
                    fetch(`${process.env.NEXT_PUBLIC_API_URL}/results/`, {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                    fetch(`${process.env.NEXT_PUBLIC_API_URL}/exams`),
                ]);

                if (!resultsRes.ok) {
                    console.error("Error auth:", resultsRes.status);

                    if (resultsRes.status === 401) {
                        localStorage.removeItem("token");
                        router.push("/login");
                        return;
                    }
                }

                console.log("resultsRes:", resultsRes);
                console.log("status:", resultsRes.status);
                const resultsData = await resultsRes.json();
                console.log("resultsData:", resultsData);
                const examsData = await examsRes.json();
                console.log("examsData:", examsData);
                const normalizedExams = examsData.map((e: any) => ({
                    id: e.id ?? e.exam_id,
                    title: e.title,
                    price: e.price,
                }));
                console.log("NORMALIZED:", normalizedExams);
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
        <div className="p-6 space-y-8">
            <h1 className="text-3xl font-bold">Dashboard</h1>

            {/* RESULTADOS */}
            <div>
                <h2 className="text-xl font-bold mb-4">Mis resultados</h2>
                {!results || results.length === 0 ? (
                    <p>No tienes resultados aún</p>
                ) : (
                    results.map((r, i) => (
                        <div key={i} className="border p-3 mb-2 rounded">
                            <p className="font-semibold">{r.title}</p>
                            <p>{r.score}%</p>
                            <p>{r.passed ? "Aprobado ✅" : "Reprobado ❌"}</p>
                        </div>
                    ))
                )}
            </div>

            {/* EXÁMENES */}
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
                                onClick={() => {
                                    console.log("NAVIGATING TO:", exam.id)
                                    console.log("CLICK EXAM:", exam)
                                    router.push(`/checkout/${exam.id}`)
                                }
                            }
                                className="mt-2 bg-black text-white px-4 py-2 rounded"
                            >
                                Comprar
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}