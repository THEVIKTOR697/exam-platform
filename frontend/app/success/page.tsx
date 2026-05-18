export default function SuccessPage({
  searchParams,
}: {
  searchParams: { exam_id?: string }
}) {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-green-600">
        ¡Pago exitoso! 🎉
      </h1>

      <p className="mt-2">
        Examen comprado: {searchParams.exam_id}
      </p>
    </div>
  )
}