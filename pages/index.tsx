import { Layout } from '../components/Layout'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
  const featuredCourses = [
    { id: 1, name: "Web Development Fundamentals", description: "Learn the basics of HTML, CSS, and JavaScript." },
    { id: 2, name: "Data Science Essentials", description: "Explore data analysis, visualization, and machine learning." },
    { id: 3, name: "Mobile App Development", description: "Create apps for iOS and Android platforms." },
  ]

  return (
    <Layout>
      <h1 className="text-4xl font-bold mb-6">Welcome to Project K</h1>
      <p className="text-xl mb-8">Expand your knowledge with our interactive learning platform.</p>
      
      <h2 className="text-2xl font-bold mb-4">Featured Courses</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {featuredCourses.map((course) => (
          <Card key={course.id}>
            <CardHeader>
              <CardTitle>{course.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{course.description}</p>
            </CardContent>
            <CardFooter>
              <Button>Learn More</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </Layout>
  )
}

