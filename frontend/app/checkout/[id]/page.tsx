"use client"

import { useParams } from "next/navigation"

const token = localStorage.getItem("token")

export default function Checkout(){
    const params = useParams()
    console.log("PARAMETROS:", params)
    const examId = Number(params.id)

    const handleCheckout = async () => {
        console.log("SUPERCLIC", examId)
        const res = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/payments/create-checkout-session`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    exam_id: Number(params.id),
                    title: "Examen",
                    price: 10,
                }),
            }
        )

        console.log('RES', res)

        const data = await res.json()

        // redirige a Stripe Checkout
        window.location.href = data.url
    }

    return (
        <div className="p-6">
            <button
                onClick={handleCheckout}
                className="bg-black text-white px-4 py-2"
            >
                Pagar con Stripe
            </button>
        </div>
    )
}