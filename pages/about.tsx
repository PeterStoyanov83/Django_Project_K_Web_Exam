import { Layout } from '../components/Layout'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function About() {
  return (
    <Layout>
      <h1 className="text-4xl font-bold mb-6">About Project K</h1>
      <p className="text-xl mb-8">Project K is a cutting-edge learning platform dedicated to providing high-quality education in IT and business fields.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Our Mission</CardTitle>
          </CardHeader>
          <CardContent>
            <p>We aim to empower individuals with practical skills and knowledge, preparing them for the challenges of the modern workplace.</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Our Approach</CardTitle>
          </CardHeader>
          <CardContent>
            <p>We believe in hands-on learning and real-world application. Our courses are designed to be interactive and engaging, combining theoretical knowledge with practical exercises and projects.</p>
          </CardContent>
        </Card>
      </div>
    </Layout>
  )
}

