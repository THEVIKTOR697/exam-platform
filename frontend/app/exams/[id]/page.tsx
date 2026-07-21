"use client"

import {useEffect, useState} from "react"
import {useParams, useRouter} from "next/navigation"

type Option = {
    id: number
    text: string
}

type Question = {
    question_id: number
    text: string
    options: Option[]
}

type Result = {
    score: number
    passed: boolean
    correct_answers: number
    total_questions: number
}


export default function ExamPage() {
    const params = useParams()
    const router = useRouter()
    const [isSubmitted, setIsSubmitted] = useState(false);

    const examId = params.id as string

    const [questions, setQuestions] = useState<Question[]>([])
    const [answers, setAnswers] = useState<Record<number, number>>({})
    const [result, setResult] = useState<Result | null>(null)

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    useEffect(() => {
        if (!examId) return
        fetchExam()
    }, [examId])

    const fetchExam = async () => {
        console.log('1111111')
        try {
            const token = localStorage.getItem("token");
            console.log('TOOOOOOOOOOOOOOOOOOOOOO', token)
            if (!token) {
                router.push("/login")
                return
            }
            // 🔐 1. Validar acceso
            const accessRes = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/exams/${examId}/access`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )

            if (!accessRes.ok) {
                setError("No autorizado")
                return
            }

            const accessData = await accessRes.json()

            if (!accessData.has_access) {
                setError("No tienes acceso a este examen")
                setLoading(false)

                setTimeout(() => {
                    router.push("/")
                }, 1500)

                return
            }

            // 📥 2. Obtener preguntas
            const res = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/exams/${examId}/questions`
            )

            const data = await res.json()
            setQuestions(data)
        } catch (err) {
            console.error(err)
            setError("Error cargando el examen")
        } finally {
            setLoading(false)
        }
    }
    const handleSubmitExam = async () => {
    console.log('2222222222222')
        try {
            const token = localStorage.getItem("token")

            if (!token) {
                router.push("/login")
                return
            }

            const formattedAnswers = Object.entries(answers).map(
                ([question_id, option_id]) => ({
                    question_id: Number(question_id),
                    selected_option: option_id,
                })
            )

            const res = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/exams/submit-exam`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        exam_id: Number(examId),
                        answers: formattedAnswers,
                    }),
                }
            )
            console.log('RRRRRRRRRRRRRRRRRRRRR', res)

            if (!res.ok) {
                setError("Error enviando examen")
                return
            }

            const data = await res.json()
            setResult(data)
            setIsSubmitted(true);
        } catch (err) {
            console.error(err)
            setError("Error enviando examen")
        }
    }
    if (loading) {
        return <p className="p-6">Cargando examen...</p>
    }

    if (error) {
        return <p className="p-6 text-red-500">{error}</p>
    }

    return (
        <div className="p-6 max-w-2xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">
                Examen #{examId}
            </h1>

            {/* 🎯 Resultado */}
            {result && (
                <div className="mb-6 p-4 rounded bg-gray-100">
                    <p className="text-lg font-semibold">
                        Resultado:
                    </p>
                    <p>Score: {result.score}%</p>
                    <p>
                        Correctas: {result.correct_answers} / {result.total_questions}
                    </p>
                    <p className="mt-2">
                        {result.passed ? "✅ Aprobado" : "❌ Reprobado"}
                    </p>
                </div>
            )}

            {/* 🧠 Preguntas */}
            {questions.map((q, index) => (
                <div key={q.question_id} className="mb-6">
                    <h2 className="font-semibold">
                        {index + 1}. {q.text}
                    </h2>

                    <div className="mt-2 space-y-2">
                        {q.options.map((opt) => (
                            <label key={opt.id} className="block cursor-pointer">
                                <input
                                    type="radio"
                                    name={`q-${q.question_id}`}
                                    className="mr-2"
                                    onChange={() =>
                                        setAnswers((prev) => ({
                                            ...prev,
                                            [q.question_id]: opt.id,
                                        }))
                                    }
                                />
                                {opt.text}
                            </label>
                        ))}
                    </div>
                </div>
            ))}

            {/* 🚀 Submit */}
            <button onClick={handleSubmitExam}
                    disabled={isSubmitted}
                    className={`mt-6 px-6 py-2 rounded text-white 
                    ${isSubmitted ? "bg-gray-400 cursor-not-allowed" : "bg-black hover:bg-gray-800"}`}>
                {isSubmitted ? "Examen enviado" : "Enviar examen 🚀"}
            </button>
            {isSubmitted && (
                <button
                    onClick={() => router.push("/dashboard")}
                    className="mt-6 ml-4 px-6 py-2 bg-black text-white rounded hover:bg-gray-800"
                >
                    Volver al dashboard
                </button>
            )}
        </div>
    )
}