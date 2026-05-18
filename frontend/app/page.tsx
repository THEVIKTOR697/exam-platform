export default function Home() {
    return (
        <div className="min-h-screen flex flex-col bg-gray-50">

            {/* 🚀 Hero Section */}
            <main className="flex flex-1 flex-col items-center justify-center text-center px-6">
                <h2 className="text-4xl font-bold text-gray-900 mb-4">
                    Plataforma de Exámenes
                </h2>

                <p className="text-gray-600 max-w-xl mb-6">
                    Administra, crea y presenta exámenes de forma sencilla y eficiente.
                    Diseñado para estudiantes y profesores.
                </p>

                <div className="flex gap-4">
                    <a href="/register"
                       className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition">
                        Empezar ahora
                    </a>

                    <a href="/login"
                       className="border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-100 transition">
                        Ya tengo cuenta
                    </a>
                </div>
            </main>

            <footer className="text-center py-4 text-sm text-gray-500">
                © {new Date().getFullYear()} Exam Platform
            </footer>
        </div>
    );
}
