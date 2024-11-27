import { Button } from "@/components/ui/button"

export function Hero() {
  return (
    <section className="bg-blue-600 text-white py-20">
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-6xl font-bold mb-4">Welcome to Project K</h1>
        <p className="text-xl mb-8">Expand your knowledge with our interactive learning platform</p>
        <Button size="lg" variant="secondary">
          Get Started
        </Button>
      </div>
    </section>
  )
}

