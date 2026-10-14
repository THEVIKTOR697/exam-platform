"use client"

import { useParams } from "next/navigation"
import {useRef, useState} from "react";

const token = localStorage.getItem("token")

export default function Checkout(){
    const params = useParams()
    console.log("PARAMETROS:", params)
    const examId = Number(params.id)
    const checkoutRequestId = useRef<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleCheckout = async () => {
        console.log("SUPERCLIC", examId)
        if (loading) return;
        setLoading(true);
        setError("");
        // Generate the ID only once for this operation.
        if (!checkoutRequestId.current) {
            checkoutRequestId.current = crypto.randomUUID();
        }
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                throw new Error("You must log in first.");
            }
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
                        checkout_request_id: checkoutRequestId.current,
                    }),
                }
            );

            console.log('RES', res);
            const data = await res.json();

            if (!res.ok) {
                throw new Error(
                    data.detail ?? "Could not create checkout."
                );
            }

            if (!data.url) {
                throw new Error(
                    "The server did not return a Checkout URL."
                );
            }

            // Redirige Stripe Checkout
            window.location.href = data.url;
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "An unexpected error occurred."
            );

            // Keep checkoutRequestId so a retry uses
            // the same operation ID.
        } finally {
            setLoading(false);
        }
    };

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