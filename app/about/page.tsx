import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">About Project K</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Our Mission</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Project K, inspired by Kiebitz, is dedicated to providing high-quality education in the fields of IT and business. We aim to empower individuals with practical skills and knowledge, preparing them for the challenges of the modern workplace.</p>
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
        <Card>
          <CardHeader>
            <CardTitle>Our Courses</CardTitle>
          </CardHeader>
          <CardContent>
            <p>We offer a wide range of courses in web development, data science, digital marketing, and more. Whether you're a beginner or looking to advance your skills, we have courses tailored to your needs.</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Our Team</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Our instructors are industry professionals with years of experience in their respective fields. They bring real-world insights and best practices to the classroom, ensuring you receive relevant and up-to-date education.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

