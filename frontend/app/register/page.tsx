"use client"

import {useState} from "react"

export default function RegisterPage() {
    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
    })

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        })
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError("")

        try {
            console.log(form)
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(form),
            })

            if (!res.ok) {
                throw new Error("Error al registrarse")
            }

            alert("Usuario registrado correctamente 🚀")
        } catch (err: any) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
            <form
                onSubmit={handleSubmit}
                className="w-full max-w-md bg-white p-8 rounded-xl shadow"
            >
                <h2 className="text-2xl font-bold mb-6 text-center">
                    Crear cuenta
                </h2>

                {error && (
                    <p className="text-red-500 text-sm mb-4">{error}</p>
                )}

                {/* Nombre */}
                <div className="mb-4">
                    <label className="block text-sm mb-1">Nombre</label>
                    <input
                        type="text"
                        name="name"
                        required
                        onChange={handleChange}
                        className="w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring focus:ring-gray-200"
                    />
                </div>

                {/* Email */}
                <div className="mb-4">
                    <label className="block text-sm mb-1">Correo</label>
                    <input
                        type="email"
                        name="email"
                        required
                        onChange={handleChange}
                        className="w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring focus:ring-gray-200"
                    />
                </div>

                {/* Password */}
                <div className="mb-6">
                    <label className="block text-sm mb-1">Contraseña</label>
                    <input
                        type="password"
                        name="password"
                        required
                        onChange={handleChange}
                        className="w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring focus:ring-gray-200"
                    />
                </div>

                {/* Botón */}
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-black text-white py-2 rounded-lg hover:bg-gray-800 transition"
                >
                    {loading ? "Registrando..." : "Registrarse"}
                </button>

                {/* Link a login */}
                <p className="text-sm text-center mt-4">
                    ¿Ya tienes cuenta?{" "}
                    <a href="/login" className="text-blue-600 hover:underline">
                        Inicia sesión
                    </a>
                </p>
            </form>
        </div>
    )
}