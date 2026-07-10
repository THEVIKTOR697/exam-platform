"use client"

import Link from "next/link"
import {useEffect, useState} from "react"
import {useRouter, useSearchParams} from "next/navigation"

export default function SuccessPage() {
    const router = useRouter()
    const searchParams = useSearchParams()

    const sessionId = searchParams.get("session_id")

    const [status, setStatus] = useState<"loading" | "error">("loading")
    const [message, setMessage] = useState("Procesando tu pago... ⏳")

    useEffect(() => {
        if (!sessionId) {
            setStatus("error")
            setMessage("Falta session_id en la URL")
            return
        }

        const verify = async () => {
            for (let i = 0; i < 10; i++) {
                try {
                    const res = await fetch(
                  `${process.env.NEXT_PUBLIC_API_URL}/payments/verify-session?session_id=${sessionId}`
                    )
                    console.log(res)
                    if (res.status === 404) {
                        // webhook aún no llega
                        await sleep(1000)
                        continue
                    }

                    const data = await res.json()

                    if (data.status === "success") {
                        setMessage("¡Pago confirmado! Redirigiendo... 🚀")

                        setTimeout(() => {
                            router.push(`/exams/${data.exam_id}`)
                        }, 1000)

                        return
                    }

                    await sleep(1000)
                } catch (err) {
                    console.error(err)
                    setStatus("error")
                    setMessage("Error verificando el pago")
                    return
                }
            }

            // si después de varios intentos no llegó
            setStatus("error")
            setMessage("El pago está tardando más de lo esperado")
        }

        verify()
    }, [sessionId, router])

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
            <div className="bg-white shadow rounded-2xl p-8 text-center max-w-md">
                {status === "loading" && (
                    <>
                        <div
                            className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-800 mx-auto mb-4"></div>
                        <h1 className="text-xl font-semibold">{message}</h1>
                        <p className="text-gray-500 mt-2">
                            Esto puede tardar unos segundos
                        </p>
                    </>
                )}

                {status === "error" && (
                    <>
                        <h1 className="text-xl font-semibold text-red-600">
                            Algo salió mal ❌
                        </h1>
                        <p className="text-gray-500 mt-2">{message}</p>

                        <button
                            onClick={() => router.push("/")}
                            className="mt-4 px-4 py-2 bg-black text-white rounded"
                        >
                            Volver al inicio
                        </button>
                    </>
                )}
            </div>
        </div>
    )
}

function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms))
}
// return (
//     <div className="p-6">
//         <h1 className="text-2xl font-bold text-green-600">
//             ¡Pago exitoso! 🎉
//         </h1>
//
//         <p className="mt-2">
//             Examen comprado: {title}
//         </p>
//
//         {title && (
//             <Link
//                 href={`/exams/${title}`}
//                 className="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
//             >
//                 Ir al examen 🚀
//             </Link>
//         )}
//     </div>
// )
